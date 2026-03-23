#!/usr/bin/env python3
"""
Properly regenerate tall and wide gauge textures by scaling each section individually.

Source master (4 rows x 8px = 32px tall):
  Y=0-7:   Background
  Y=8-15:  Fill
  Y=16-23: Lines
  Y=24-31: LinesFill

Generated main output (_thorne01.tga, ORIGINAL dimensions preserved):
  Standard (4 rows x 8px = 32px):   BG / Fill / Lines / LinesFill
  Tall     (4 rows x 16px = 64px):  BG / Fill / Lines / LinesFill

Generated composite output (_thorne02.tga, SEPARATE file):
  Standard (4 rows x 8px = 32px):
    Y=0-7:   Overlay        (auto: dark marks from Background on transparent)
    Y=8-15:  SolidFill      (auto: Fill with transparent gaps filled)
    Y=16-23: GridFill       (auto: SolidFill with gray grid lines + depth)
    Y=24-31: LightGridFill  (auto: SolidFill with light gray grid lines)
  Tall (4 rows x 16px = 64px):
    Y=0-15:   Overlay        (auto-generated)
    Y=16-31:  SolidFill      (auto-generated)
    Y=32-47:  GridFill       (auto: gray grid + depth)
    Y=48-63:  LightGridFill  (auto: light gray grid)

Composite rows enable clean multi-color gauge stacking:
  - Overlay: dark tick marks on transparent (renders on top of stacked fills)
  - SolidFill: opaque fill with no transparent gaps (prevents color bleed)
  - GridFill: SolidFill with gray grid lines + neighbor darkening for depth
    (for stacked gauges where XML Lines renders gauge-wide not fill-clipped)
  - LightGridFill: SolidFill with light gray grid lines, no darkening (subtle)

CRITICAL: Composite data lives in a separate _thorne02 file so that the
original _thorne01 texture dimensions are preserved. EQ client computes UV
coordinates relative to total texture height — changing .tga dimensions
breaks all existing animation Y-offset mappings.
"""

from PIL import Image, ImageOps
from pathlib import Path
import sys
import json
import shutil


# ============================================================================
# CONFIGURATION: Gauge sizing variants
# ============================================================================
# To add a new wide size: add to WIDE_WIDTHS
# To add a new tall size: add to TALL_WIDTHS
WIDE_WIDTHS = [120]  # Base is 120, can expand with 150, 160, etc.
TALL_WIDTHS = [105, 120, 250]  # Base is 120 (from standard), others scale from 120t
CANONICAL_BASE_WIDTH = 120  # Normalize source section width before scaling variants


class GaugeGenerator:
    """Manages gauge generation with stats tracking."""
    
    def __init__(self, variant_dir, black_mask_thin=1, debug=False, black_threshold=0):
        """Initialize generator for a gauge variant.
        
        Args:
            variant_dir: Path to variant directory (e.g., thorne_drak/Options/Gauges/Thorne)
            black_mask_thin: Number of thinning passes for stretched black mask
            debug: If True, emit per-output debug visualization TGAs
            black_threshold: Max RGB value considered black (0=exact black only)
        """
        self.variant_dir = Path(variant_dir)
        self.black_mask_thin = max(0, int(black_mask_thin))
        self.debug = bool(debug)
        self.black_threshold = max(0, min(255, int(black_threshold)))
        self.stats = {
            "variant": self.variant_dir.name,
            "variant_path": str(self.variant_dir),
            "source_base_found": False,
            "source_base_name": None,
            "config_loaded": False,
            "generated": {
                "wide": [],
                "tall": [],
            }
        }
        self.config = self._load_variant_config()
        self.stats["config_loaded"] = (self.variant_dir / ".regen_gauges.json").exists()
    
    def _load_variant_config(self):
        """Load per-variant config from .regen_gauges.json if present.

        Config schema:
            {
                "description": "Human description of gauge variant",
                "interpolation": "BILINEAR",
                "sections": {
                    "background": { "preserve_black": true },
                    "fill":       { "preserve_black": false },
                    "lines":      { "preserve_black": true },
                    "linesfill":  { "preserve_black": false },
                    "solidfill":  { "preserve_black": false, "fill_gaps": true },
                    "overlay":    { "preserve_black": true, "enabled": true },
                    "gridfill":   { "preserve_black": false, "bake_overlay": true }
                }
            }

        Section-specific properties:
            preserve_black  — all sections: whether to use nearest-neighbor for
                              dark pixels during scaling (preserves sharp edges)
            fill_gaps       — solidfill only: whether to fill transparent gaps
                              with interpolated colors (true=solid bar, false=
                              preserve original fill shape with its contours)
            enabled         — overlay only: whether to generate overlay marks.
                              When false, the overlay row is fully transparent
                              (useful for variants without structural grid lines,
                              e.g. Bubbles, where dark pixel extraction picks up
                              unwanted artifacts)
            bake_overlay    — gridfill/lightgridfill: whether to blend overlay
                              marks into the fill. When false, result = plain
                              SolidFill copy (same animations still work)
            gray_level      — gridfill/lightgridfill: RGB intensity for grid
                              lines (0=pure black/GridFill default,
                              140=LightGridFill default, 255=invisible)
            darken          — gridfill/lightgridfill: darkening factor for
                              neighbor pixels around grid lines. Range 0.0-1.0
                              (0=no darkening, 0.15=GridFill default,
                              0.0=LightGridFill default, 1.0=full black)
            spread          — gridfill/lightgridfill: pixel radius for the
                              darkening gradient around each grid mark
                              (1=immediate neighbors/default, 2+=wider glow)

        Defaults match the original hard-coded behavior so existing variants
        without a config file produce identical output.
        """
        defaults = {
            "interpolation": "BILINEAR",
            "sections": {
                # --- thorne01 rows (original source art) ---
                "background": {"preserve_black": True},
                "fill":       {"preserve_black": False},
                "lines":      {"preserve_black": True},
                "linesfill":  {"preserve_black": False},
                # --- thorne02 rows (composite output, top to bottom) ---
                "overlay":       {"preserve_black": True, "enabled": True},
                "solidfill":     {"preserve_black": False, "fill_gaps": True},
                "gridfill":      {"preserve_black": False, "bake_overlay": True, "gray_level": 0, "darken": 0.15, "spread": 1},
                "lightgridfill": {"preserve_black": False, "bake_overlay": True, "gray_level": 140, "darken": 0.0, "spread": 1},
            }
        }

        config_file = self.variant_dir / ".regen_gauges.json"
        if not config_file.exists():
            return defaults

        try:
            with open(config_file) as f:
                user_config = json.load(f)

            # Merge user config over defaults
            merged = dict(defaults)
            if "interpolation" in user_config:
                merged["interpolation"] = user_config["interpolation"]
            if "sections" in user_config:
                for section_name in list(defaults["sections"]):
                    if section_name in user_config["sections"]:
                        merged["sections"][section_name] = {
                            **defaults["sections"][section_name],
                            **user_config["sections"][section_name],
                        }
            # snap_columns: per-width column snapping for grid marks
            # Format: { "105": [21, 42, 63, 84], "120": [24, 48, 72, 96], ... }
            if "snap_columns" in user_config:
                merged["snap_columns"] = user_config["snap_columns"]

            print(f"  Loaded config: {config_file.name}")
            return merged
        except Exception as e:
            print(f"  WARNING: Failed to load config {config_file.name}: {e}")
            return defaults

    def _section_preserve_black(self, section_name):
        """Get preserve_black setting for a specific section."""
        return self.config.get("sections", {}).get(section_name, {}).get("preserve_black", False)

    def _section_overlay_enabled(self):
        """Whether to generate overlay marks (overlay section config).

        When False, the overlay row is fully transparent — no dark pixel
        extraction from Background. Useful for variants like Bubbles where
        the source art has no structural grid lines.
        """
        return self.config.get("sections", {}).get("overlay", {}).get("enabled", True)

    def _section_bake_overlay(self):
        """Whether to bake overlay marks into GridFill (gridfill section config)."""
        return self.config.get("sections", {}).get("gridfill", {}).get("bake_overlay", True)

    def _section_gridfill_gray_level(self):
        """Gray intensity for GridFill grid lines (0=black/default, 255=invisible)."""
        return self.config.get("sections", {}).get("gridfill", {}).get("gray_level", 0)

    def _section_gridfill_darken(self):
        """Darkening factor for GridFill neighbor pixels (0.0=none, 0.15=default, 1.0=black)."""
        return self.config.get("sections", {}).get("gridfill", {}).get("darken", 0.15)

    def _section_gridfill_spread(self):
        """Pixel radius for GridFill darkening gradient (1=immediate neighbors/default)."""
        return self.config.get("sections", {}).get("gridfill", {}).get("spread", 1)

    def _section_lightgridfill_bake_overlay(self):
        """Whether to bake overlay marks into LightGridFill (lightgridfill section config)."""
        return self.config.get("sections", {}).get("lightgridfill", {}).get("bake_overlay", True)

    def _section_lightgridfill_gray_level(self):
        """Gray intensity for LightGridFill grid lines (0=black, 140=default, 255=invisible)."""
        return self.config.get("sections", {}).get("lightgridfill", {}).get("gray_level", 140)

    def _section_lightgridfill_darken(self):
        """Darkening factor for LightGridFill neighbor pixels (0.0=none/default, 1.0=black)."""
        return self.config.get("sections", {}).get("lightgridfill", {}).get("darken", 0.0)

    def _section_lightgridfill_spread(self):
        """Pixel radius for LightGridFill darkening gradient (1=immediate neighbors/default)."""
        return self.config.get("sections", {}).get("lightgridfill", {}).get("spread", 1)

    def _get_snap_columns(self, width):
        """Get snap column positions for a given target width, or None if not configured.

        Returns list of integer column positions, or None.
        """
        snap_cfg = self.config.get("snap_columns")
        if not snap_cfg:
            return None
        # Config keys are strings (JSON keys), so look up by string
        positions = snap_cfg.get(str(width))
        if positions and isinstance(positions, list):
            return [int(p) for p in positions]
        return None

    def _snap_dark_columns(self, section, width):
        """Snap dark mark columns to exact configured positions.

        Detects current dark-pixel columns in the section interior, clears them,
        then redraws 1px dark columns at the configured snap positions.
        Only modifies columns if snap_columns is configured for this width.

        Args:
            section: RGBA image to modify (mutated in place and returned)
            width: Target width (used to look up snap_columns config)

        Returns:
            The (possibly modified) section image.
        """
        snap_positions = self._get_snap_columns(width)
        if not snap_positions:
            return section

        threshold = self.black_threshold
        w, h = section.size
        px = section.load()

        # Step 1: Detect existing dark mark columns (interior only, skip borders)
        dark_cols = set()
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                r, g, b, a = px[x, y]
                if a > 0 and r <= threshold and g <= threshold and b <= threshold:
                    dark_cols.add(x)
                    break

        if not dark_cols:
            return section  # No marks to snap

        # Step 2: Sample the background color of a non-dark interior column
        # for use when clearing old dark columns
        bg_sample = None
        for x in range(1, w - 1):
            if x not in dark_cols:
                # Use the middle interior row as representative
                mid_y = h // 2
                r, g, b, a = px[x, mid_y]
                if a > 0:
                    bg_sample = (r, g, b, a)
                    break

        # Step 3: Clear old dark mark columns (replace with neighbor colors)
        for x in sorted(dark_cols):
            # Find nearest non-dark neighbor column for color blending
            left_x = x - 1 if x - 1 >= 1 and x - 1 not in dark_cols else None
            right_x = x + 1 if x + 1 < w - 1 and x + 1 not in dark_cols else None
            for y in range(1, h - 1):
                r, g, b, a = px[x, y]
                if a > 0 and r <= threshold and g <= threshold and b <= threshold:
                    # Replace with neighbor color
                    if left_x is not None:
                        px[x, y] = px[left_x, y]
                    elif right_x is not None:
                        px[x, y] = px[right_x, y]
                    elif bg_sample is not None:
                        px[x, y] = bg_sample
                    else:
                        px[x, y] = (0, 0, 0, 0)

        # Step 4: Draw new dark marks at snap positions
        for target_x in snap_positions:
            if 1 <= target_x < w - 1:
                for y in range(1, h - 1):
                    px[target_x, y] = (0, 0, 0, 255)

        snapped_from = sorted(dark_cols)
        print(f"    Snapped grid marks: {snapped_from} -> {snap_positions}")
        return section

    def _snap_fill_gaps(self, fill_section, width):
        """Snap transparent gap columns in fill to match configured snap positions.

        After bg dark columns are snapped, the fill's transparent gaps may remain
        at old interpolated positions.  This method detects those gaps, fills them
        using neighbor colors, then punches new 1px transparent columns at the
        configured snap positions so fill and bg stay aligned in thorne01 output.

        Args:
            fill_section: RGBA fill image (mutated in place and returned)
            width: Target width for snap_columns config lookup

        Returns:
            The (possibly modified) fill image.
        """
        snap_positions = self._get_snap_columns(width)
        if not snap_positions:
            return fill_section

        w, h = fill_section.size
        px = fill_section.load()

        # Detect gap columns: interior columns where majority of pixels are transparent
        gap_cols = set()
        for x in range(1, w - 1):
            transparent_count = 0
            total = 0
            for y in range(1, h - 1):
                _, _, _, a = px[x, y]
                total += 1
                if a < 128:
                    transparent_count += 1
            if total > 0 and transparent_count > total * 0.5:
                gap_cols.add(x)

        if not gap_cols:
            return fill_section

        # Fill in old gap columns with neighbor colors
        for x in sorted(gap_cols):
            left_x = x - 1 if x - 1 >= 1 and x - 1 not in gap_cols else None
            right_x = x + 1 if x + 1 < w - 1 and x + 1 not in gap_cols else None
            for y in range(1, h - 1):
                _, _, _, a = px[x, y]
                if a < 255:
                    if left_x is not None:
                        px[x, y] = px[left_x, y]
                    elif right_x is not None:
                        px[x, y] = px[right_x, y]

        # Punch new transparent gaps at snap positions
        for target_x in snap_positions:
            if 1 <= target_x < w - 1:
                for y in range(1, h - 1):
                    px[target_x, y] = (0, 0, 0, 0)

        snapped_from = sorted(gap_cols)
        print(f"    Snapped fill gaps: {snapped_from} -> {snap_positions}")
        return fill_section

    def _section_fill_preserve_gaps(self):
        """Whether to preserve 1px transparent gaps when scaling Fill (fill section config).

        When True, the fill is made solid before scaling (preventing gap
        expansion from interpolation), then 1px transparent gaps are punched
        back at grid-line positions detected from the scaled background.
        Suitable for structural grid variants (Basic, Grid, Thorne).

        When False (default), fill is scaled normally with interpolation,
        which may widen transparent gaps at larger target widths.
        """
        return self.config.get("sections", {}).get("fill", {}).get("preserve_gaps", False)

    def _section_fill_gaps(self):
        """Whether to fill transparent gaps in SolidFill (solidfill section config)."""
        return self.config.get("sections", {}).get("solidfill", {}).get("fill_gaps", True)

    def _section_interpolation(self, section_name=None):
        """Get interpolation method. Section-level overrides top-level default."""
        if section_name:
            section_interp = self.config.get("sections", {}).get(section_name, {}).get("interpolation")
            if section_interp:
                return section_interp
        return self.config.get("interpolation", "BILINEAR")

    def extract_base_name(self):
        """Extract base filename from source gauge.
        
        Looks for gauge_inlay*.tga pattern. Returns base name without size suffix.
        E.g., "gauge_inlay_thorne01" from "gauge_inlay_thorne01.tga"
        
        Returns:
            Base name string, or None if not found
        """
        # Find the standard gauge source file (no size suffix)
        # Pattern: gauge_inlay[optional suffix]_thorne0X.tga where no size is in the middle
        for file in self.variant_dir.glob('gauge_inlay*_thorne*.tga'):
            name = file.stem  # Remove .tga
            # Check if this looks like the base file (not containing dimension markers like "120t", "150", etc.)
            # Build dynamic marker list from active width configs
            _markers = []
            for w in sorted(set(TALL_WIDTHS), reverse=True):
                _markers.append(f'{w}t')
                _markers.append(str(w))
            for w in sorted(set(WIDE_WIDTHS), reverse=True):
                if str(w) not in _markers:
                    _markers.append(str(w))
            if not any(marker in name for marker in _markers):
                self.stats["source_base_found"] = True
                self.stats["source_base_name"] = name
                return name
        
        return None
    
    def get_source_file(self):
        """Get the standard (base) source gauge file."""
        base_name = self.extract_base_name()
        if not base_name:
            return None
        source = self.variant_dir / f"{base_name}.tga"
        if source.exists():
            return source
        return None
    
    def get_output_filename(self, base_name, width, is_tall=False):
        """Generate output filename for a given size.
        
        Args:
            base_name: Base filename (e.g., "gauge_inlay_thorne01")
            width: Target width in pixels (120, 150, 230, etc.)
            is_tall: If True, use 't' suffix (120t, 150t, 230t, etc.)
        
        Returns:
            Filename string (e.g., "gauge_inlay120t_thorne01.tga")
            Width is inserted between the descriptor and the _thorne suffix.
        """
        # Split at last underscore: "gauge_inlay_thorne01" -> "gauge_inlay" + "_thorne01"
        last_underscore = base_name.rfind('_')
        if last_underscore == -1:
            # No underscore - just append size before extension as fallback
            size_str = f"{width}t" if is_tall else str(width)
            return f"{base_name}{size_str}.tga"
        
        prefix = base_name[:last_underscore]   # e.g., "gauge_inlay"
        suffix = base_name[last_underscore:]   # e.g., "_thorne01"
        
        size_str = f"{width}t" if is_tall else str(width)
        return f"{prefix}{size_str}{suffix}.tga"  # e.g., "gauge_inlay120t_thorne01.tga"
    
    def get_composite_filename(self, base_name, width, is_tall=False):
        """Generate output filename for composite (Overlay+SolidFill) texture.
        
        Replaces '01' suffix with '02' to create a companion file, e.g.:
          gauge_inlay120t_thorne01.tga  (main, 4 rows)
          gauge_inlay120t_thorne02.tga  (composite, 2 rows: Overlay + SolidFill)
        """
        # Derive from get_output_filename and swap 01 -> 02
        main_filename = self.get_output_filename(base_name, width, is_tall)
        return main_filename.replace('01.tga', '02.tga')
    
    def fix_tga_file(self, file_path):
        """Check if file is actually PNG (mislabeled as TGA) and convert if needed."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                # PNG signature: 89 50 4E 47 0D 0A 1A 0A
                if header.startswith(b'\x89PNG\r\n\x1a\n'):
                    # Convert PNG to TGA
                    img = Image.open(file_path)
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    img.save(str(file_path), format='TGA')
                    print(f"    Fixed: {file_path.name} (converted from PNG to TGA)")
                    return True
        except Exception as e:
            print(f"    WARNING: Could not fix {file_path.name}: {e}")
        return False
    
    def generate_wide_gauge(self, width):
        """Generate wide gauge variant at specified width.
        
        Args:
            width: Target width in pixels (120, 150, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        source = self.get_source_file()
        if not source or not source.exists():
            print(f"  ERROR: Source gauge not found")
            return False
        
        # Fix TGA if needed
        self.fix_tga_file(source)
        
        base_name = self.extract_base_name()
        output_filename = self.get_output_filename(base_name, width, is_tall=False)
        output_file = self.variant_dir / output_filename
        
        print(f"  Generating wide gauge @ {width}px...")
        
        # Load standard gauge
        std = Image.open(source)
        std_width = std.size[0]
        
        # Extract individual sections (8px tall each)
        bg = std.crop((0, 0, std_width, 8))
        fill = std.crop((0, 8, std_width, 16))
        lines = std.crop((0, 16, std_width, 24))
        linesfill = std.crop((0, 24, std_width, 32))

        # Normalize to canonical base width so downstream scaling patterns are
        # consistent across variants with different source widths (100/103/etc).
        if std_width != CANONICAL_BASE_WIDTH:
            print(f"    Normalizing source width {std_width} -> {CANONICAL_BASE_WIDTH} before wide scaling")
            bg = self._scale_horizontal_with_borders(bg, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("background"), preserve_black=self._section_preserve_black("background"))
            fill = self._scale_horizontal_with_borders(fill, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("fill"), preserve_black=self._section_preserve_black("fill"))
            lines = self._scale_horizontal_with_borders(lines, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("lines"), preserve_black=self._section_preserve_black("lines"))
            linesfill = self._scale_horizontal_with_borders(linesfill, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("linesfill"), preserve_black=self._section_preserve_black("linesfill"))
            std_width = CANONICAL_BASE_WIDTH
        
        debug_sections = [] if self.debug else None

        # Scale each section horizontally
        bg_wide = self._scale_horizontal_with_borders(
            bg, width, interp_method=self._section_interpolation("background"),
            preserve_black=self._section_preserve_black("background"),
            debug_bucket=debug_sections, debug_label="background"
        )
        if self._section_fill_preserve_gaps():
            fill_wide = self._scale_fill_preserving_gaps(
                fill, bg_wide, width,
                interp_method=self._section_interpolation("fill"),
                preserve_black=self._section_preserve_black("fill"),
                debug_bucket=debug_sections, debug_label="fill"
            )
        else:
            fill_wide = self._scale_horizontal_with_borders(
                fill, width, interp_method=self._section_interpolation("fill"),
                preserve_black=self._section_preserve_black("fill"),
                debug_bucket=debug_sections, debug_label="fill"
            )
        lines_wide = self._scale_horizontal_with_borders(
            lines, width, interp_method=self._section_interpolation("lines"),
            preserve_black=self._section_preserve_black("lines"),
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_wide = self._scale_horizontal_with_borders(
            linesfill, width, interp_method=self._section_interpolation("linesfill"),
            preserve_black=self._section_preserve_black("linesfill"),
            debug_bucket=debug_sections, debug_label="linesfill"
        )
        
        # Auto-generate composite rows from scaled sections
        solidfill_wide = self._generate_solidfill(fill_wide)
        overlay_wide = self._generate_overlay(bg_wide)
        gridfill_wide = self._generate_gridfill(fill_wide, bg_wide)
        lightgridfill_wide = self._generate_lightgridfill(fill_wide, bg_wide)
        
        # Create main image (4 rows x 8px = 32px, ORIGINAL dimensions preserved)
        result = Image.new('RGBA', (width, 32), (0, 0, 0, 0))
        result.paste(bg_wide, (0, 0))
        result.paste(fill_wide, (0, 8))
        result.paste(lines_wide, (0, 16))
        result.paste(linesfill_wide, (0, 24))
        
        # Save main gauge (unchanged dimensions)
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
        
        # Save composite file (Overlay + SolidFill + GridFill + LightGridFill, 4 rows x 8px = 32px)
        composite_filename = self.get_composite_filename(base_name, width, is_tall=False)
        composite_file = self.variant_dir / composite_filename
        composite = Image.new('RGBA', (width, 32), (0, 0, 0, 0))
        composite.paste(overlay_wide, (0, 0))
        composite.paste(solidfill_wide, (0, 8))
        composite.paste(gridfill_wide, (0, 16))
        composite.paste(lightgridfill_wide, (0, 24))
        composite.save(str(composite_file), format='TGA')
        print(f"    Saved: {composite_filename}")
        if self.debug and debug_sections:
            self._write_debug_canvas(output_file, debug_sections)
        self.stats["generated"]["wide"].append(output_filename)
        return True
    
    def generate_tall_gauge(self):
        """Generate tall gauge (120×64) from standard source.
        
        Returns:
            True if successful, False otherwise
        """
        source = self.get_source_file()
        if not source or not source.exists():
            print(f"  ERROR: Source gauge not found")
            return False
        
        # Fix TGA if needed
        self.fix_tga_file(source)
        
        base_name = self.extract_base_name()
        output_filename = self.get_output_filename(base_name, 120, is_tall=True)
        output_file = self.variant_dir / output_filename
        
        print(f"  Generating tall gauge (120×64)...")
        
        # Load standard gauge
        std = Image.open(source)
        std_width = std.size[0]
        target_width = 120
        
        # Extract individual sections (8px each)
        bg = std.crop((0, 0, std_width, 8))
        fill = std.crop((0, 8, std_width, 16))
        lines = std.crop((0, 16, std_width, 24))
        linesfill = std.crop((0, 24, std_width, 32))

        # Normalize to canonical base width before vertical expansion to keep
        # tall scaling behavior consistent across source widths.
        if std_width != CANONICAL_BASE_WIDTH:
            print(f"    Normalizing source width {std_width} -> {CANONICAL_BASE_WIDTH} before tall scaling")
            bg = self._scale_horizontal_with_borders(bg, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("background"), preserve_black=self._section_preserve_black("background"))
            fill = self._scale_horizontal_with_borders(fill, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("fill"), preserve_black=self._section_preserve_black("fill"))
            lines = self._scale_horizontal_with_borders(lines, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("lines"), preserve_black=self._section_preserve_black("lines"))
            linesfill = self._scale_horizontal_with_borders(linesfill, CANONICAL_BASE_WIDTH, interp_method=self._section_interpolation("linesfill"), preserve_black=self._section_preserve_black("linesfill"))
            std_width = CANONICAL_BASE_WIDTH
        
        debug_sections = [] if self.debug else None

        # Scale each section vertically (8px → 16px), then normalize to 120px width.
        # This guarantees 120t is truly 120px wide regardless of source art width.
        bg_tall = self._scale_with_borders(
            bg, std_width, interp_method=self._section_interpolation("background"),
            preserve_black=self._section_preserve_black("background"),
            debug_bucket=debug_sections, debug_label="background"
        )
        fill_tall = self._scale_with_borders(
            fill, std_width, interp_method=self._section_interpolation("fill"),
            preserve_black=self._section_preserve_black("fill"),
            debug_bucket=debug_sections, debug_label="fill"
        )
        lines_tall = self._scale_with_borders(
            lines, std_width, interp_method=self._section_interpolation("lines"),
            preserve_black=self._section_preserve_black("lines"),
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_tall = self._scale_with_borders(
            linesfill, std_width, interp_method=self._section_interpolation("linesfill"),
            preserve_black=self._section_preserve_black("linesfill"),
            debug_bucket=debug_sections, debug_label="linesfill"
        )

        if std_width != target_width:
            bg_tall = self._scale_horizontal_with_borders(bg_tall, target_width, interp_method=self._section_interpolation("background"), preserve_black=self._section_preserve_black("background"))
            if self._section_fill_preserve_gaps():
                fill_tall = self._scale_fill_preserving_gaps(fill_tall, bg_tall, target_width, interp_method=self._section_interpolation("fill"), preserve_black=self._section_preserve_black("fill"))
            else:
                fill_tall = self._scale_horizontal_with_borders(fill_tall, target_width, interp_method=self._section_interpolation("fill"), preserve_black=self._section_preserve_black("fill"))
            lines_tall = self._scale_horizontal_with_borders(lines_tall, target_width, interp_method=self._section_interpolation("lines"), preserve_black=self._section_preserve_black("lines"))
            linesfill_tall = self._scale_horizontal_with_borders(linesfill_tall, target_width, interp_method=self._section_interpolation("linesfill"), preserve_black=self._section_preserve_black("linesfill"))
        
        # Snap grid marks and fill gaps to exact configured positions
        bg_tall = self._snap_dark_columns(bg_tall, target_width)
        fill_tall = self._snap_fill_gaps(fill_tall, target_width)

        # Auto-generate composite rows from scaled sections
        solidfill_tall = self._generate_solidfill(fill_tall)
        overlay_tall = self._generate_overlay(bg_tall)
        gridfill_tall = self._generate_gridfill(fill_tall, bg_tall)
        lightgridfill_tall = self._generate_lightgridfill(fill_tall, bg_tall)
        
        # Create main image (120x64, 4 rows x 16px — ORIGINAL dimensions preserved)
        result = Image.new('RGBA', (target_width, 64), (0, 0, 0, 0))
        result.paste(bg_tall, (0, 0))
        result.paste(fill_tall, (0, 16))
        result.paste(lines_tall, (0, 32))
        result.paste(linesfill_tall, (0, 48))
        
        # Save main gauge (unchanged dimensions)
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
        
        # Save composite file (Overlay + SolidFill + GridFill + LightGridFill, 4 rows x 16px = 64px)
        composite_filename = self.get_composite_filename(base_name, 120, is_tall=True)
        composite_file = self.variant_dir / composite_filename
        composite = Image.new('RGBA', (target_width, 64), (0, 0, 0, 0))
        composite.paste(overlay_tall, (0, 0))
        composite.paste(solidfill_tall, (0, 16))
        composite.paste(gridfill_tall, (0, 32))
        composite.paste(lightgridfill_tall, (0, 48))
        composite.save(str(composite_file), format='TGA')
        print(f"    Saved: {composite_filename}")
        if self.debug and debug_sections:
            self._write_debug_canvas(output_file, debug_sections)
        self.stats["generated"]["tall"].append(output_filename)
        return True
    
    def generate_tall_variant(self, width):
        """Generate tall variant at specified width, scaling from 120t source.
        
        Args:
            width: Target width in pixels (150, 230, 240, 250, 260, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        base_name = self.extract_base_name()
        
        # Get 120t main source (must be generated first)
        source_filename = self.get_output_filename(base_name, 120, is_tall=True)
        source = self.variant_dir / source_filename
        
        if not source.exists():
            # Source not yet generated, skip
            return False
        
        # Get 120t composite source
        composite_source_filename = self.get_composite_filename(base_name, 120, is_tall=True)
        composite_source = self.variant_dir / composite_source_filename
        
        output_filename = self.get_output_filename(base_name, width, is_tall=True)
        output_file = self.variant_dir / output_filename
        
        scale_factor = width / 120.0
        print(f"  Generating tall gauge @ {width}x64 ({scale_factor:.2f}x from 120t)...")
        
        # Load 120t main source (4 rows x 16px = 64px)
        tall = Image.open(source)
        tall_width = tall.size[0]  # Should be 120
        
        # Extract main sections (16px each, 4 rows from 64px source)
        bg = tall.crop((0, 0, tall_width, 16))
        fill = tall.crop((0, 16, tall_width, 32))
        lines = tall.crop((0, 32, tall_width, 48))
        linesfill = tall.crop((0, 48, tall_width, 64))
        
        debug_sections = [] if self.debug else None

        # Scale each section horizontally
        bg_scaled = self._scale_horizontal_with_borders(
            bg, width, interp_method=self._section_interpolation("background"),
            preserve_black=self._section_preserve_black("background"),
            debug_bucket=debug_sections, debug_label="background"
        )
        # Snap bg marks before fill gap detection uses them
        bg_scaled = self._snap_dark_columns(bg_scaled, width)
        if self._section_fill_preserve_gaps():
            fill_scaled = self._scale_fill_preserving_gaps(
                fill, bg_scaled, width,
                interp_method=self._section_interpolation("fill"),
                preserve_black=self._section_preserve_black("fill"),
                debug_bucket=debug_sections, debug_label="fill"
            )
        else:
            fill_scaled = self._scale_horizontal_with_borders(
                fill, width, interp_method=self._section_interpolation("fill"),
                preserve_black=self._section_preserve_black("fill"),
                debug_bucket=debug_sections, debug_label="fill"
            )
        lines_scaled = self._scale_horizontal_with_borders(
            lines, width, interp_method=self._section_interpolation("lines"),
            preserve_black=self._section_preserve_black("lines"),
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_scaled = self._scale_horizontal_with_borders(
            linesfill, width, interp_method=self._section_interpolation("linesfill"),
            preserve_black=self._section_preserve_black("linesfill"),
            debug_bucket=debug_sections, debug_label="linesfill"
        )

        # Create main image at target dimensions (4 rows x 16px = 64px)
        result = Image.new('RGBA', (width, 64), (0, 0, 0, 0))
        result.paste(bg_scaled, (0, 0))
        result.paste(fill_scaled, (0, 16))
        result.paste(lines_scaled, (0, 32))
        result.paste(linesfill_scaled, (0, 48))
        
        # Save main gauge
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
        
        # Scale composite rows if composite source exists
        if composite_source.exists():
            comp = Image.open(composite_source)
            comp_width = comp.size[0]
            
            # Extract composite sections (Overlay@Y=0, SolidFill@Y=16, GridFill@Y=32)
            overlay = comp.crop((0, 0, comp_width, 16))
            solidfill = comp.crop((0, 16, comp_width, 32))
            
            overlay_scaled = self._scale_horizontal_with_borders(
                overlay, width, interp_method=self._section_interpolation("overlay"),
                preserve_black=self._section_preserve_black("overlay"),
                debug_bucket=debug_sections, debug_label="overlay"
            )
            # Snap overlay marks to match bg_scaled snap positions
            overlay_scaled = self._snap_dark_columns(overlay_scaled, width)
            solidfill_scaled = self._scale_horizontal_with_borders(
                solidfill, width, interp_method=self._section_interpolation("solidfill"),
                preserve_black=self._section_preserve_black("solidfill"),
                debug_bucket=debug_sections, debug_label="solidfill"
            )
            
            # Generate GridFill fresh at target width from scaled sections,
            # rather than scaling the pre-blended 120t GridFill (which causes
            # interpolation to spread darkened pixels into wide bands)
            gridfill_scaled = self._generate_gridfill(fill_scaled, bg_scaled)
            lightgridfill_scaled = self._generate_lightgridfill(fill_scaled, bg_scaled)
            
            # Save composite file (Overlay + SolidFill + GridFill + LightGridFill, 4 rows x 16px = 64px)
            composite_filename = self.get_composite_filename(base_name, width, is_tall=True)
            composite_file = self.variant_dir / composite_filename
            composite = Image.new('RGBA', (width, 64), (0, 0, 0, 0))
            composite.paste(overlay_scaled, (0, 0))
            composite.paste(solidfill_scaled, (0, 16))
            composite.paste(gridfill_scaled, (0, 32))
            composite.paste(lightgridfill_scaled, (0, 48))
            composite.save(str(composite_file), format='TGA')
            print(f"    Saved: {composite_filename}")
        if self.debug and debug_sections:
            self._write_debug_canvas(output_file, debug_sections)
        self.stats["generated"]["tall"].append(output_filename)
        return True
    
    def _generate_solidfill(self, fill_section):
        """Generate SolidFill from Fill section.
        
        When fill_gaps is True (default): fills transparent vertical gaps
        using interpolated colors from nearest opaque neighbors, producing
        a fully solid bar suitable for composite gauges.
        
        When fill_gaps is False: returns the fill as-is, preserving its
        original shape and transparent contours (e.g., bubble outlines).
        """
        if not self._section_fill_gaps():
            return fill_section.copy()
        
        result = fill_section.copy()
        px = result.load()
        width, height = result.size
        
        for y in range(height):
            # Collect fully opaque pixel positions and colors
            opaque_positions = []
            for x in range(width):
                r, g, b, a = px[x, y]
                if a == 255:
                    opaque_positions.append((x, (r, g, b, 255)))
            
            if not opaque_positions:
                continue  # Entirely transparent row (border), skip
            
            # Fill non-fully-opaque pixels from nearest opaque neighbors
            for x in range(width):
                r, g, b, a = px[x, y]
                if a == 255:
                    continue  # Already fully opaque
                
                # Find nearest left and right fully opaque pixels
                left = None
                right = None
                for pos, color in opaque_positions:
                    if pos < x:
                        left = (pos, color)
                    elif pos > x:
                        right = (pos, color)
                        break
                
                if left and right:
                    # Interpolate between neighbors
                    lx, (lr, lg, lb, _) = left
                    rx, (rr, rg, rb, _) = right
                    t = (x - lx) / (rx - lx)
                    px[x, y] = (
                        int(lr + (rr - lr) * t),
                        int(lg + (rg - lg) * t),
                        int(lb + (rb - lb) * t),
                        255,
                    )
                elif left:
                    px[x, y] = left[1]
                elif right:
                    px[x, y] = right[1]
        
        return result
    
    def _generate_gridfill(self, fill_section, bg_section):
        """Generate GridFill: SolidFill with gray grid lines and depth shading.
        
        When gridfill.bake_overlay is True (per-variant section config),
        extracts interior overlay marks from Background, converts them to
        black lines (gray_level=0 default), and blends into SolidFill with
        subtle neighbor darkening for depth. Stronger visual than LightGridFill.
        
        When gridfill.bake_overlay is False, GridFill is an identical copy
        of SolidFill. This ensures the same animations work regardless of
        gauge variant.
        """
        solidfill = self._generate_solidfill(fill_section)
        if not self._section_bake_overlay():
            return solidfill
        
        # Only extract interior marks (skip border pixels)
        overlay = self._generate_overlay(bg_section, interior_only=True)
        gray_level = self._section_gridfill_gray_level()
        
        # Convert overlay marks to configured gray level
        gray_overlay = overlay.copy()
        px = gray_overlay.load()
        w, h = gray_overlay.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a > 0:
                    px[x, y] = (gray_level, gray_level, gray_level, a)
        
        result = self._blend_overlay_into_fill(
            solidfill, gray_overlay,
            spread=self._section_gridfill_spread(),
            darken=self._section_gridfill_darken(),
        )
        
        # Clear first and last columns so the background border shows through
        width, height = result.size
        res_px = result.load()
        for y in range(height):
            res_px[0, y] = (0, 0, 0, 0)
            res_px[width - 1, y] = (0, 0, 0, 0)
        
        return result
    
    def _generate_lightgridfill(self, fill_section, bg_section):
        """Generate LightGridFill: SolidFill with gray grid lines (softer than GridFill).
        
        Same grid structure as GridFill but marks are rendered in gray instead
        of black, with no neighbor darkening. Produces a subtle, soft grid
        appearance that's visible but not as harsh as the full GridFill.
        
        When lightgridfill.bake_overlay is True (per-variant section config),
        extracts interior overlay marks from Background, converts them to gray,
        and composites onto SolidFill without neighbor darkening.
        
        When lightgridfill.bake_overlay is False, LightGridFill is an identical
        copy of SolidFill.
        """
        solidfill = self._generate_solidfill(fill_section)
        if not self._section_lightgridfill_bake_overlay():
            return solidfill
        
        overlay = self._generate_overlay(bg_section, interior_only=True)
        gray_level = self._section_lightgridfill_gray_level()
        
        # Convert black overlay marks to gray
        gray_overlay = overlay.copy()
        px = gray_overlay.load()
        width, height = gray_overlay.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = px[x, y]
                if a > 0:
                    px[x, y] = (gray_level, gray_level, gray_level, a)
        
        # Composite gray marks onto SolidFill (with optional neighbor darkening)
        darken = self._section_lightgridfill_darken()
        if darken > 0:
            result = self._blend_overlay_into_fill(
                solidfill, gray_overlay,
                spread=self._section_lightgridfill_spread(),
                darken=darken,
            )
        else:
            result = Image.alpha_composite(solidfill, gray_overlay)
        
        # Clear first and last columns so the background border shows through
        res_px = result.load()
        for y in range(height):
            res_px[0, y] = (0, 0, 0, 0)
            res_px[width - 1, y] = (0, 0, 0, 0)
        
        return result
    
    def _scale_fill_preserving_gaps(self, fill_section, bg_scaled, target_width,
                                     interp_method="BILINEAR", preserve_black=False,
                                     debug_bucket=None, debug_label=None):
        """Scale fill section while keeping transparent gaps at 1px wide.
        
        Segment-based approach that preserves internal shading:
          1) Identify opaque segments (contiguous non-gap columns) in source fill
          2) Detect grid-line columns from the already-scaled background
          3) Calculate proportional target widths for each segment
          4) Scale each segment independently (preserving its shading)
          5) Reassemble with 1px transparent gaps at grid-line positions
        
        Args:
            fill_section: Source fill image (with transparent gap columns)
            bg_scaled: Already-scaled background at target_width (used to
                       detect grid-line column positions)
            target_width: Target width in pixels
            interp_method: Interpolation method for scaling
            preserve_black: If True, use preserve-black pipeline
            debug_bucket: Optional debug stage collector
            debug_label: Optional debug label
        
        Returns:
            Scaled fill image (target_width × height) with 1px transparent
            gaps at each grid-line column, inner shading preserved
        """
        src_width, src_height = fill_section.size
        fill_px = fill_section.load()
        
        # Step 1: Identify gap columns in source fill (fully transparent interior columns)
        src_gap_cols = set()
        for x in range(1, src_width - 1):       # Skip border columns
            is_gap = True
            for y in range(1, src_height - 1):   # Check interior rows only
                _, _, _, a = fill_px[x, y]
                if a > 0:
                    is_gap = False
                    break
            if is_gap:
                src_gap_cols.add(x)
        
        # If no gaps found, fall back to normal scaling
        if not src_gap_cols:
            return self._scale_horizontal_with_borders(
                fill_section, target_width, interp_method=interp_method,
                preserve_black=preserve_black,
                debug_bucket=debug_bucket, debug_label=debug_label,
            )
        
        # Step 2: Detect grid-line columns from scaled background
        bg_width, bg_height = bg_scaled.size
        bg_px = bg_scaled.load()
        threshold = self.black_threshold
        
        dst_gap_cols = sorted(set(
            x for x in range(1, bg_width - 1)
            if any(
                bg_px[x, y][3] > 0 and bg_px[x, y][0] <= threshold
                and bg_px[x, y][1] <= threshold and bg_px[x, y][2] <= threshold
                for y in range(1, bg_height - 1)
            )
        ))
        
        # Step 3: Parse source into segments (runs of non-gap columns)
        # A segment is a contiguous run of columns that are NOT gap columns
        # and NOT border columns (first/last)
        interior_cols = list(range(1, src_width - 1))  # Exclude border pixels
        segments = []  # List of (start_x, width) tuples
        seg_start = None
        for x in interior_cols:
            if x not in src_gap_cols:
                if seg_start is None:
                    seg_start = x
            else:
                if seg_start is not None:
                    segments.append((seg_start, x - seg_start))
                    seg_start = None
        if seg_start is not None:
            segments.append((seg_start, (src_width - 1) - seg_start))
        
        num_gaps = len(dst_gap_cols)
        # Available interior pixels = target - 2 borders - gap pixels
        available = target_width - 2 - num_gaps
        
        if available <= 0 or not segments:
            # Degenerate case: fall back to normal scaling
            return self._scale_horizontal_with_borders(
                fill_section, target_width, interp_method=interp_method,
                preserve_black=preserve_black,
                debug_bucket=debug_bucket, debug_label=debug_label,
            )
        
        # Step 4: Distribute available width proportionally among segments
        total_src_seg_width = sum(w for _, w in segments)
        seg_target_widths = []
        assigned = 0
        for i, (_, seg_w) in enumerate(segments):
            if i == len(segments) - 1:
                # Last segment gets remainder to avoid rounding drift
                tw = available - assigned
            else:
                tw = max(1, round(seg_w / total_src_seg_width * available))
            seg_target_widths.append(tw)
            assigned += tw
        
        # Choose interpolation
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:
            interp = Image.Resampling.BILINEAR
        
        # Step 5: Scale each segment and reassemble
        result = Image.new('RGBA', (target_width, src_height), (0, 0, 0, 0))
        
        # Copy left border column
        left_border = fill_section.crop((0, 0, 1, src_height))
        result.paste(left_border, (0, 0))
        
        # Build sorted gap set for fast lookup during assembly
        gap_set = set(dst_gap_cols)
        
        # Place segments into the result, skipping gap columns
        cursor = 1  # Start after left border
        seg_idx = 0
        for seg_idx, ((src_x, src_w), tgt_w) in enumerate(zip(segments, seg_target_widths)):
            # Skip any gap columns at current cursor position
            while cursor < target_width - 1 and cursor in gap_set:
                cursor += 1  # Gap column stays transparent
            
            if cursor + tgt_w > target_width - 1:
                tgt_w = target_width - 1 - cursor  # Clamp to fit
            if tgt_w <= 0:
                break
            
            # Extract source segment
            seg_img = fill_section.crop((src_x, 0, src_x + src_w, src_height))
            
            # Scale segment to target width
            seg_scaled = seg_img.resize((tgt_w, src_height), interp)
            
            # Paste into result
            result.paste(seg_scaled, (cursor, 0))
            cursor += tgt_w
        
        # Copy right border column
        right_border = fill_section.crop((src_width - 1, 0, src_width, src_height))
        result.paste(right_border, (target_width - 1, 0))
        
        return result
    
    def _blend_overlay_into_fill(self, solidfill, overlay, spread=1, darken=0.15):
        """Blend overlay marks into fill with subtle gradient depth.
        
        For each overlay mark pixel:
          - The mark itself is composited at full strength
          - Immediate neighbor fill pixels are lightly darkened,
            creating a subtle shadow/depth around each grid line
        
        Args:
            solidfill: SolidFill image (fully opaque where fill exists)
            overlay: Overlay image (dark marks on transparent)
            spread: Pixels of gradient falloff around each mark (1=immediate neighbors only)
            darken: Max darkening factor for immediate neighbors (0=none, 1=black)
        """
        result = solidfill.copy()
        width, height = result.size
        res_px = result.load()
        ovr_px = overlay.load()
        
        # First pass: collect overlay mark positions
        marks = []
        for y in range(height):
            for x in range(width):
                _, _, _, a = ovr_px[x, y]
                if a > 0:
                    marks.append((x, y))
        
        if not marks:
            return result
        
        # Second pass: darken neighbors within spread radius
        for mx, my in marks:
            for dy in range(-spread, spread + 1):
                for dx in range(-spread, spread + 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = mx + dx, my + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        r, g, b, a = res_px[nx, ny]
                        if a == 0:
                            continue
                        dist = max(abs(dx), abs(dy))  # Chebyshev distance
                        factor = 1.0 - darken * (1.0 - (dist - 1) / spread)
                        factor = max(0.0, min(1.0, factor))
                        res_px[nx, ny] = (
                            int(r * factor),
                            int(g * factor),
                            int(b * factor),
                            a,
                        )
        
        # Final pass: stamp overlay marks at full strength
        result = Image.alpha_composite(result, overlay)
        return result
    
    def _generate_overlay(self, bg_section, threshold=None, interior_only=False):
        """Generate Overlay by extracting dark tick-mark pixels from Background.
        
        Creates a transparent canvas with only black/dark mark pixels from
        the Background section preserved at full opacity.
        
        If overlay is disabled via config ("enabled": false), returns a fully
        transparent canvas (no marks extracted).
        
        Args:
            bg_section: Background image section to extract marks from
            threshold: Max RGB value considered dark (default: self.black_threshold)
            interior_only: If True, skip edge pixels (first/last row & column).
                          Used for GridFill baking where borders are already in BG slot.
        """
        if not self._section_overlay_enabled():
            return Image.new('RGBA', bg_section.size, (0, 0, 0, 0))
        if threshold is None:
            threshold = self.black_threshold
        
        width, height = bg_section.size
        result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        src_px = bg_section.load()
        dst_px = result.load()
        
        for y in range(height):
            for x in range(width):
                if interior_only and (y == 0 or y == height - 1 or x == 0 or x == width - 1):
                    continue
                r, g, b, a = src_px[x, y]
                if a > 0 and r <= threshold and g <= threshold and b <= threshold:
                    dst_px[x, y] = (r, g, b, 255)
        
        return result
    
    def _scale_with_borders(self, section, width, interp_method="BILINEAR", preserve_black=False, debug_bucket=None, debug_label=None):
        """Scale 8px section to 16px preserving 1px top/bottom borders.
        
        Args:
            section: Image section to scale
            width: Width to preserve (no horizontal scaling)
            interp_method: Interpolation for middle section
            preserve_black: If True, remap pure-black source pixels onto scaled output
        
        Returns:
            Scaled image (width×16)
        """
        # Extract top, middle, bottom
        top = section.crop((0, 0, width, 1))      # Y=0: 1px border
        middle = section.crop((0, 1, width, 7))   # Y=1-6: 6px content
        bottom = section.crop((0, 7, width, 8))   # Y=7: 1px border
        
        # Choose interpolation
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:  # Default BILINEAR
            interp = Image.Resampling.BILINEAR
        
        # Scale middle vertically (6px → 14px)
        middle_color = None
        section_black_mask = None

        if preserve_black:
            # Two-layer pipeline:
            # 1) Remove black from blend input to prevent dark bleed/halos
            # 2) Scale color layer smoothly
            # 3) Re-apply black mask as a final pass on the whole section
            middle_color = self._build_color_layer_without_black(middle)
            middle_scaled = middle_color.resize((width, 14), interp)
        else:
            middle_scaled = middle.resize((width, 14), interp)
        
        # Keep borders crisp
        top_scaled = top.resize((width, 1), Image.Resampling.NEAREST)
        bottom_scaled = bottom.resize((width, 1), Image.Resampling.NEAREST)
        
        # Composite vertically
        result = Image.new('RGBA', (width, 16), (0, 0, 0, 0))
        result.paste(top_scaled, (0, 0))
        result.paste(middle_scaled, (0, 1))
        result.paste(bottom_scaled, (0, 15))

        if preserve_black:
            # Final-pass black overlay on full section so borders and inline strokes are
            # applied once, as solid black, after all stretching/compositing.
            section_black_mask = self._scale_black_mask_vertical(section, 16, thin_passes=self.black_mask_thin)
            result = self._apply_black_mask_overlay(result, section_black_mask)

        if debug_bucket is not None:
            debug_bucket.append({
                "label": debug_label or "section",
                "stages": [
                    ("source", section.copy()),
                    ("color_no_black", (middle_color if middle_color is not None else middle).copy()),
                    ("scaled_middle", middle_scaled.copy()),
                    ("black_mask", section_black_mask.copy() if section_black_mask is not None else Image.new('L', result.size, 0)),
                    ("final", result.copy()),
                ]
            })
        
        return result
    
    def _scale_horizontal_with_borders(self, section, target_width, interp_method="BILINEAR", preserve_black=False, debug_bucket=None, debug_label=None):
        """Scale section horizontally to target width, preserving 1px left/right borders.
        
        Args:
            section: Image section to scale
            target_width: Target width in pixels
            interp_method: Interpolation for middle section
            preserve_black: If True, remap pure-black source pixels onto scaled output
        
        Returns:
            Scaled image (target_width×height)
        """
        width, height = section.size
        
        # Extract left, middle, right
        left = section.crop((0, 0, 1, height))
        middle = section.crop((1, 0, width-1, height))
        right = section.crop((width-1, 0, width, height))
        
        # Choose interpolation
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:  # Default BILINEAR
            interp = Image.Resampling.BILINEAR
        
        # Scale middle to (target_width - 2)
        middle_color = None
        section_black_mask = None

        if preserve_black:
            # Two-layer pipeline:
            # 1) Remove black from blend input to prevent dark bleed/halos
            # 2) Scale color layer smoothly
            # 3) Re-apply black mask as a final pass on the whole section
            middle_color = self._build_color_layer_without_black(middle)
            middle_scaled = middle_color.resize((target_width-2, height), interp)
        else:
            middle_scaled = middle.resize((target_width-2, height), interp)
        
        # Keep borders crisp
        left_scaled = left.resize((1, height), Image.Resampling.NEAREST)
        right_scaled = right.resize((1, height), Image.Resampling.NEAREST)
        
        # Composite horizontally
        result = Image.new('RGBA', (target_width, height), (0, 0, 0, 0))
        result.paste(left_scaled, (0, 0))
        result.paste(middle_scaled, (1, 0))
        result.paste(right_scaled, (target_width-1, 0))

        if preserve_black:
            # Final-pass black overlay on full section so borders and inline strokes are
            # applied once, as solid black, after all stretching/compositing.
            section_black_mask = self._scale_black_mask_horizontal(section, target_width, thin_passes=self.black_mask_thin)
            result = self._apply_black_mask_overlay(result, section_black_mask)

        if debug_bucket is not None:
            debug_bucket.append({
                "label": debug_label or "section",
                "stages": [
                    ("source", section.copy()),
                    ("color_no_black", (middle_color if middle_color is not None else middle).copy()),
                    ("scaled_middle", middle_scaled.copy()),
                    ("black_mask", section_black_mask.copy() if section_black_mask is not None else Image.new('L', result.size, 0)),
                    ("final", result.copy()),
                ]
            })
        
        return result

    def _is_pure_black(self, pixel, threshold=None):
        """Return True if RGBA pixel is effectively solid black with visible alpha."""
        if threshold is None:
            threshold = self.black_threshold
        r, g, b, a = pixel
        return a > 0 and r <= threshold and g <= threshold and b <= threshold

    def _build_color_layer_without_black(self, source, threshold=None):
        """Create a color-only layer by replacing pure-black pixels with nearby non-black color.

        This prevents pure black pixels from entering interpolation kernels, which is the
        primary source of black bleed into adjacent gray during bilinear scaling.
        """
        if threshold is None:
            threshold = self.black_threshold

        result = source.copy()
        src_px = source.load()
        out_px = result.load()
        width, height = source.size

        for y in range(height):
            for x in range(width):
                p = src_px[x, y]
                if self._is_pure_black(p, threshold=threshold):
                    replacement = self._find_nearest_non_black_pixel(src_px, width, height, x, y, threshold)
                    if replacement is None:
                        # Fallback: make it fully transparent instead of black so it cannot darken blend.
                        out_px[x, y] = (0, 0, 0, 0)
                    else:
                        out_px[x, y] = replacement

        return result

    def _find_nearest_non_black_pixel(self, pixels, width, height, x, y, threshold=None):
        """Find nearest non-black pixel using expanding-radius search."""
        if threshold is None:
            threshold = self.black_threshold

        max_radius = max(width, height)

        for radius in range(1, max_radius + 1):
            x_min = max(0, x - radius)
            x_max = min(width - 1, x + radius)
            y_min = max(0, y - radius)
            y_max = min(height - 1, y + radius)

            # Top and bottom edges of current ring
            for xx in range(x_min, x_max + 1):
                p_top = pixels[xx, y_min]
                if not self._is_pure_black(p_top, threshold=threshold):
                    return p_top

                p_bottom = pixels[xx, y_max]
                if not self._is_pure_black(p_bottom, threshold=threshold):
                    return p_bottom

            # Left and right edges of current ring (excluding corners already checked)
            for yy in range(y_min + 1, y_max):
                p_left = pixels[x_min, yy]
                if not self._is_pure_black(p_left, threshold=threshold):
                    return p_left

                p_right = pixels[x_max, yy]
                if not self._is_pure_black(p_right, threshold=threshold):
                    return p_right

        return None

    def _build_black_mask(self, source, threshold=None):
        """Build an L-mode binary mask for pure-black pixels (0 or 255)."""
        if threshold is None:
            threshold = self.black_threshold

        width, height = source.size
        mask = Image.new('L', (width, height), 0)
        src_px = source.load()
        m_px = mask.load()

        for y in range(height):
            for x in range(width):
                if self._is_pure_black(src_px[x, y], threshold=threshold):
                    m_px[x, y] = 255

        return mask

    def _scale_black_mask_horizontal(self, source, target_width, threshold=None, thin_passes=0):
        """Build a target-width black mask by proportional position mapping.

        Instead of scaling a bitmap mask with NEAREST (which causes inconsistent
        doubling of 1px marks), this detects black run positions in each row
        and re-creates them at proportionally-mapped positions in the target.

        Guarantees:
          - Single-pixel source marks always produce single-pixel target marks
          - Multi-pixel source runs scale proportionally
          - Consistent spacing between marks across all target widths
        """
        if threshold is None:
            threshold = self.black_threshold

        src_w, src_h = source.size
        source_mask = self._build_black_mask(source, threshold=threshold)
        target_mask = Image.new('L', (target_width, src_h), 0)

        if src_w <= 1:
            return target_mask

        src_px = source_mask.load()
        dst_px = target_mask.load()
        scale = (target_width - 1) / (src_w - 1)

        for y in range(src_h):
            x = 0
            while x < src_w:
                if src_px[x, y] > 0:
                    start = x
                    while x < src_w and src_px[x, y] > 0:
                        x += 1
                    end = x - 1  # inclusive
                    run_len = end - start + 1

                    if run_len == 1:
                        # Single-pixel mark -> single-pixel at mapped position
                        tx = round(start * scale)
                        dst_px[max(0, min(target_width - 1, tx)), y] = 255
                    else:
                        # Multi-pixel run -> proportionally mapped run
                        t_start = round(start * scale)
                        t_end = round(end * scale)
                        t_start = max(0, min(target_width - 1, t_start))
                        t_end = max(t_start, min(target_width - 1, t_end))
                        for tx in range(t_start, t_end + 1):
                            dst_px[tx, y] = 255
                else:
                    x += 1

        return target_mask

    def _scale_black_mask_vertical(self, source, target_height, threshold=None, thin_passes=0):
        """Build a target-height black mask by proportional position mapping.

        Same approach as horizontal: detects black run positions in each column
        and re-creates them at proportionally-mapped positions in the target.
        """
        if threshold is None:
            threshold = self.black_threshold

        src_w, src_h = source.size
        source_mask = self._build_black_mask(source, threshold=threshold)
        target_mask = Image.new('L', (src_w, target_height), 0)

        if src_h <= 1:
            return target_mask

        src_px = source_mask.load()
        dst_px = target_mask.load()
        scale = (target_height - 1) / (src_h - 1)

        for x in range(src_w):
            y = 0
            while y < src_h:
                if src_px[x, y] > 0:
                    start = y
                    while y < src_h and src_px[x, y] > 0:
                        y += 1
                    end = y - 1  # inclusive
                    run_len = end - start + 1

                    if run_len == 1:
                        ty = round(start * scale)
                        dst_px[x, max(0, min(target_height - 1, ty))] = 255
                    else:
                        t_start = round(start * scale)
                        t_end = round(end * scale)
                        t_start = max(0, min(target_height - 1, t_start))
                        t_end = max(t_start, min(target_height - 1, t_end))
                        for ty in range(t_start, t_end + 1):
                            dst_px[x, ty] = 255
                else:
                    y += 1

        return target_mask


    def _apply_black_mask_overlay(self, target, black_mask):
        """Overlay pure opaque black onto target wherever black_mask is set."""
        tw, th = target.size
        mw, mh = black_mask.size
        if tw != mw or th != mh:
            return target

        t_px = target.load()
        m_px = black_mask.load()

        for y in range(th):
            for x in range(tw):
                if m_px[x, y] > 0:
                    t_px[x, y] = (0, 0, 0, 255)

        return target

    def _render_debug_stage(self, image, cell_w, cell_h):
        """Render a stage image into a debug cell with predictable sizing."""
        if image.mode == 'L':
            # Visualize mask as white background + black pixels
            vis = Image.new('RGBA', image.size, (255, 255, 255, 255))
            m_px = image.load()
            v_px = vis.load()
            w, h = image.size
            for y in range(h):
                for x in range(w):
                    if m_px[x, y] > 0:
                        v_px[x, y] = (0, 0, 0, 255)
        else:
            vis = image.convert('RGBA')

        thumb = ImageOps.contain(vis, (cell_w, cell_h), Image.Resampling.NEAREST)
        cell = Image.new('RGBA', (cell_w, cell_h), (30, 30, 30, 255))
        ox = (cell_w - thumb.size[0]) // 2
        oy = (cell_h - thumb.size[1]) // 2
        cell.paste(thumb, (ox, oy), thumb)
        return cell

    def _write_debug_canvas(self, output_file, debug_sections):
        """Write a compact 255x255 stacked debug TGA for one generated output file.

        Each section row overlays all stages with small offsets, reducing whitespace and
        making step progression easier to see in a single glance.
        """
        canvas = Image.new('RGBA', (255, 255), (18, 18, 18, 255))

        margin = 4
        rows = 4
        row_gap = 2
        row_h = 60
        stack_w = 247
        stack_h = 58
        offset_step_x = 10
        offset_step_y = 1

        for row, section in enumerate(debug_sections[:rows]):
            y0 = margin + row * (row_h + row_gap)
            row_bg = Image.new('RGBA', (stack_w, stack_h), (28, 28, 28, 255))

            stages = section.get("stages", [])[:5]
            for idx, (_, stage_img) in enumerate(stages):
                cell = self._render_debug_stage(stage_img, 200, 56)

                # Stack with slight offset so stage progression is visible.
                x = 2 + idx * offset_step_x
                y = 1 + idx * offset_step_y

                # Fade earlier stages slightly; keep later stages stronger.
                alpha = min(255, 110 + idx * 35)
                layer = cell.copy()
                a = layer.split()[3]
                a = a.point(lambda v: int(v * alpha / 255))
                layer.putalpha(a)

                row_bg.alpha_composite(layer, (x, y))

            canvas.paste(row_bg, (margin, y0))

        debug_name = f"{output_file.stem}_debug.tga"
        debug_file = output_file.with_name(debug_name)
        canvas.save(str(debug_file), format='TGA')
        print(f"    Debug: {debug_name}")
    
    def save_stats(self):
        """Save generation statistics to JSON file."""
        base_name = self.extract_base_name()
        if not base_name:
            return False
        
        stats_file = self.variant_dir / ".regen_gauges-stats.json"
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            print(f"  Saved stats: {stats_file.name}")
            return True
        except Exception as e:
            print(f"  WARNING: Failed to save stats: {e}")
            return False


def cleanup_orphaned_gauges(search_dirs):
    """Remove gauge .tga files whose size suffix is not in WIDE_WIDTHS or TALL_WIDTHS.

    Builds valid suffixes from the active width lists (e.g. '120', '105t', '250t')
    and deletes any gauge_inlay*_thorne*.tga that carries an unrecognised suffix.
    Base files (no suffix) are never touched.

    Args:
        search_dirs: Iterable of Path objects to scan for orphaned files.

    Returns:
        Number of files removed.
    """
    import re

    # Build the set of valid size markers from current config
    valid_markers = set()
    for w in WIDE_WIDTHS:
        valid_markers.add(str(w))
    for w in TALL_WIDTHS:
        valid_markers.add(f'{w}t')
        valid_markers.add(str(w))

    # Pattern: gauge_inlay<SIZE_MARKER>_thorne0X.tga
    # SIZE_MARKER is digits optionally followed by 't' (e.g. 120, 105t, 250t)
    marker_re = re.compile(r'^gauge_inlay(\d+t?)_thorne\d+\.tga$', re.IGNORECASE)

    removed = 0
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for f in sorted(search_dir.glob('gauge_inlay*_thorne*.tga')):
            if f.name.endswith('_debug.tga'):
                continue
            m = marker_re.match(f.name)
            if not m:
                # No size marker → base file, skip
                continue
            marker = m.group(1)
            if marker not in valid_markers:
                f.unlink()
                print(f"  Removed orphan: {f.name}  (from {search_dir})")
                removed += 1
    return removed


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Regenerate gauge textures in multiple sizes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
GAUGE TEXTURE REGENERATION

Regenerates tall (×64px) and wide (×32px) gauge texture variants from a standard
source file. Supports multiple scaling factors with proper border preservation.

DISCOVERY:
    Reads from: thorne_drak/Options/Gauges/<Variant>/
    Looks for: gauge_inlay*_thorne0X.tga source files

VARIANTS:
    Thorne, Bars, Basic, Bubbles, Grid, Light Bubbles, Oval, Thorne 7

PER-VARIANT CONFIG (.regen_gauges.json):
    Each variant directory may contain a .regen_gauges.json config file that
    controls scaling behavior per section (background, fill, lines, linesfill):
      - preserve_black: true/false  (extract & re-stamp black as overlay)
      - interpolation: BILINEAR/LANCZOS/NEAREST

    Structural gauges (Thorne, Grid, Bars) use preserve_black to keep tick marks
    crisp at 1px. Gradient gauges (Bubbles, Oval) disable it for smooth scaling.

FEATURES:
    [*] Per-variant .regen_gauges.json config
    [*] Proportional black mask position mapping (1px→1px guaranteed)
    [*] Dynamic sizing (WIDE_WIDTHS, TALL_WIDTHS)
    [*] Canonical normalization to 120px base width
    [*] Automatic TGA format fixing
    [*] Smart copyback (single->thorne_drak, multi->Thorne only)
    [*] Automatic deployment to thorne_dev/
    [*] Stats JSON generation

WORKFLOW:
    1. Edit source: thorne_drak/Options/Gauges/Thorne/gauge_inlay_thorne01.tga
    2. Edit config: thorne_drak/Options/Gauges/Thorne/.regen_gauges.json
    3. Run: python regen_gauges.py --all  (or specify: Thorne)
    4. Test: /loadskin thorne_drak

SIZE CONFIGURATION:
    To add new widths, edit WIDE_WIDTHS and TALL_WIDTHS at top of script.
        """,
    )

    parser.add_argument(
        "variants",
        nargs="*",
        help="Gauge variant names (e.g., Thorne, Basic, Bars)"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all discovered variants"
    )

    parser.add_argument(
        "--master",
        action="store_true",
        help="(Consistency flag - not used, for compatibility)"
    )

    parser.add_argument(
        "--black-mask-thin",
        type=int,
        default=0,
        help="(Legacy, no-op) Retained for backwards compatibility"
    )

    parser.add_argument(
        "--black-threshold",
        type=int,
        default=0,
        help="Max RGB value treated as black for mask extraction (default: 0 exact black)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Emit *_debug.tga 255x255 stacked stage visualizations"
    )

    args = parser.parse_args()

    # If no arguments provided, show usage
    if not args.all and not args.variants:
        print("ERROR: No target specified.")
        print("\nUsage:")
        print("  python regen_gauges.py --all           # All variants")
        print("  python regen_gauges.py Thorne          # Single variant")
        print("  python regen_gauges.py Thorne Basic    # Multiple variants")
        print("\nFor help: python regen_gauges.py --help")
        return 1
    
    base_path = Path(__file__).parent.parent / 'thorne_drak' / 'Options' / 'Gauges'
    root_path = Path(__file__).parent.parent / 'thorne_drak'

    def cleanup_debug_files(paths):
        removed = 0
        for path in paths:
            if not path.exists():
                continue
            for file in path.glob('*_debug.tga'):
                try:
                    file.unlink()
                    removed += 1
                except Exception:
                    pass
        return removed

    # If debug mode is off, proactively remove stale debug artifacts.
    if not args.debug:
        thorne_dev_path = Path('C:\\TAKP\\uifiles\\thorne_dev')
        cleanup_targets = []
        if base_path.exists():
            cleanup_targets.extend([d for d in base_path.iterdir() if d.is_dir()])
        cleanup_targets.append(root_path)
        cleanup_targets.append(thorne_dev_path)
        removed_count = cleanup_debug_files(cleanup_targets)
        if removed_count > 0:
            print(f"Removed {removed_count} stale *_debug.tga file(s)\n")
    
    # Determine which variants to process
    if args.all:
        # Auto-discover all variants
        if base_path.exists():
            variant_names = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
            print(f"Auto-discovered {len(variant_names)} variants: {', '.join(variant_names)}\n")
        else:
            print(f"ERROR: Gauges directory not found at {base_path}")
            return 1
    else:
        # Use explicitly specified variants
        variant_names = args.variants
    
    print(f"{'='*70}")
    print(f"GAUGE TEXTURE REGENERATION")
    print(f"{'='*70}")
    print(f"Wide variants: {WIDE_WIDTHS}")
    print(f"Tall variants: {TALL_WIDTHS}")
    print(f"{'='*70}\n")
    
    regenerated_variants = []
    
    for variant in variant_names:
        if variant.lower() == 'root':
            variant_path = root_path
        else:
            variant_path = base_path / variant
        
        if variant_path.exists():
            print(f"Processing {variant}...")
            generator = GaugeGenerator(
                variant_path,
                black_mask_thin=args.black_mask_thin,
                debug=args.debug,
                black_threshold=args.black_threshold,
            )
            
            # Generate base tall gauge
            if generator.generate_tall_gauge():
                regenerated_variants.append((variant, variant_path, generator))
            else:
                print(f"  ERROR: Failed to generate tall gauge")
                continue
            
            # Generate wide variants
            for width in WIDE_WIDTHS:
                if width == 120:
                    # Base wide is generated as part of standard tall generation
                    print(f"  Generating wide gauge @ {width}px (base)...")
                    generator.generate_wide_gauge(width)
                else:
                    generator.generate_wide_gauge(width)
            
            # Generate tall variants (skip 120, which is the base)
            for width in TALL_WIDTHS:
                if width != 120:
                    generator.generate_tall_variant(width)
            
            # Save stats
            generator.save_stats()
            print()
        else:
            print(f"ERROR: {variant_path} not found\n")
    
    # Copy regenerated files back to thorne_drak root
    # Logic: single variant → copy all; multiple variants → copy only Thorne
    variants_to_copy = []
    
    if len(regenerated_variants) == 1 and regenerated_variants[0][0].lower() != 'root':
        variants_to_copy = regenerated_variants
    elif len(regenerated_variants) > 1:
        variants_to_copy = [(name, path, gen) for name, path, gen in regenerated_variants if name.lower() == 'thorne']
    
    if variants_to_copy:
        print(f"{'='*70}")
        print(f"Copying regenerated files back to thorne_drak/...")
        print(f"{'='*70}")
        
        for variant_name, variant_path, generator in variants_to_copy:
            base_name = generator.extract_base_name()
            if not base_name:
                continue

            # Copy full gauge asset set from selected variant directory.
            # This includes generated sizes AND the base source gauge file
            # (e.g., gauge_inlay_thorne01.tga), which is needed by standard gauges.
            files_to_copy = sorted([f.name for f in variant_path.glob('gauge*.tga') if not f.name.endswith('_debug.tga')])
            
            for filename in files_to_copy:
                src = variant_path / filename
                dst = root_path / filename
                
                if src.exists():
                    shutil.copy2(src, dst)
                    print(f"  Copied {filename}")
        
        # Deploy to thorne_dev
        thorne_dev_path = Path('C:\\TAKP\\uifiles\\thorne_dev')
        if thorne_dev_path.exists():
            print(f"\n{'='*70}")
            print(f"Deploying to thorne_dev for testing...")
            print(f"{'='*70}")
            
            for variant_name, variant_path, generator in variants_to_copy:
                base_name = generator.extract_base_name()
                if not base_name:
                    continue

                # Deploy full gauge asset set from root_path (already copied above).
                files_to_deploy = sorted([f.name for f in variant_path.glob('gauge*.tga') if not f.name.endswith('_debug.tga')])
                
                for filename in files_to_deploy:
                    src = root_path / filename
                    dst = thorne_dev_path / filename
                    
                    if src.exists():
                        shutil.copy2(src, dst)
                        print(f"  Deployed {filename}")
        
        # --- Orphan cleanup: remove gauge .tga files for widths no longer in config ---
        cleanup_dirs = [root_path]
        if base_path.exists():
            cleanup_dirs.extend([d for d in base_path.iterdir() if d.is_dir()])
        if thorne_dev_path.exists():
            cleanup_dirs.append(thorne_dev_path)
        
        orphans_removed = cleanup_orphaned_gauges(cleanup_dirs)
        if orphans_removed:
            print(f"\n{'='*70}")
            print(f"CLEANUP: Removed {orphans_removed} orphaned gauge file(s)")
            print(f"{'='*70}")
        
        print(f"\n{'='*70}")
        print(f"SUMMARY: {len(regenerated_variants)} variant(s) regenerated successfully")
        print(f"{'='*70}")
        print(f"\nReady to test in-game with: /loadskin thorne_drak")
    else:
        print(f"\n{'='*70}")
        print(f"SUMMARY: No files copied to thorne_drak/")
        if len(regenerated_variants) > 1:
            print(f"(Multiple variants regenerated - only Thorne variant would be copied)")
        print(f"{'='*70}")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
