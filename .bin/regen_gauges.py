#!/usr/bin/env python3
"""
Properly regenerate tall and wide gauge textures by scaling each section individually.

Standard gauge sections (60px wide, 8px tall each):
  Y=0-7:   Background
  Y=8-15:  Fill
  Y=16-23: Lines
  Y=24-31: LinesFill

Tall gauge sections (120px wide, 16px tall each, 2x vertical scale):
  Y=0-15:   Background
  Y=16-31:  Fill
  Y=32-47:  Lines
  Y=48-63:  LinesFill

Wide gauge sections (120px wide, 8px tall each, 2x horizontal scale):
  Y=0-7:   Background
  Y=8-15:  Fill
  Y=16-23: Lines
  Y=24-31: LinesFill
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
WIDE_WIDTHS = [120, 150]  # Base is 120, can expand with 150, 160, etc.
TALL_WIDTHS = [120, 150, 230, 240, 250, 260]  # Base is 120 (from standard), others scale from 120t
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
            "generated": {
                "wide": [],
                "tall": [],
            }
        }
    
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
            if not any(marker in name for marker in ['120t', '120', '150t', '150', '230t', '230', '240t', '240', '250t', '250', '260t', '260']):
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
            bg = self._scale_horizontal_with_borders(bg, CANONICAL_BASE_WIDTH, interp_method="BILINEAR", preserve_black=True)
            fill = self._scale_horizontal_with_borders(fill, CANONICAL_BASE_WIDTH, interp_method="BILINEAR")
            lines = self._scale_horizontal_with_borders(lines, CANONICAL_BASE_WIDTH, interp_method="BILINEAR", preserve_black=True)
            linesfill = self._scale_horizontal_with_borders(linesfill, CANONICAL_BASE_WIDTH, interp_method="BILINEAR")
            std_width = CANONICAL_BASE_WIDTH
        
        debug_sections = [] if self.debug else None

        # Scale each section horizontally
        bg_wide = self._scale_horizontal_with_borders(
            bg, width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="background"
        )
        fill_wide = self._scale_horizontal_with_borders(
            fill, width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="fill"
        )
        lines_wide = self._scale_horizontal_with_borders(
            lines, width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_wide = self._scale_horizontal_with_borders(
            linesfill, width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="linesfill"
        )
        
        # Create new image
        result = Image.new('RGBA', (width, 32), (0, 0, 0, 0))
        result.paste(bg_wide, (0, 0))
        result.paste(fill_wide, (0, 8))
        result.paste(lines_wide, (0, 16))
        result.paste(linesfill_wide, (0, 24))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
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
            bg = self._scale_horizontal_with_borders(bg, CANONICAL_BASE_WIDTH, interp_method="BILINEAR", preserve_black=True)
            fill = self._scale_horizontal_with_borders(fill, CANONICAL_BASE_WIDTH, interp_method="BILINEAR")
            lines = self._scale_horizontal_with_borders(lines, CANONICAL_BASE_WIDTH, interp_method="BILINEAR", preserve_black=True)
            linesfill = self._scale_horizontal_with_borders(linesfill, CANONICAL_BASE_WIDTH, interp_method="BILINEAR")
            std_width = CANONICAL_BASE_WIDTH
        
        debug_sections = [] if self.debug else None

        # Scale each section vertically (8px → 16px), then normalize to 120px width.
        # This guarantees 120t is truly 120px wide regardless of source art width.
        bg_tall = self._scale_with_borders(
            bg, std_width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="background"
        )
        fill_tall = self._scale_with_borders(
            fill, std_width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="fill"
        )
        lines_tall = self._scale_with_borders(
            lines, std_width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_tall = self._scale_with_borders(
            linesfill, std_width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="linesfill"
        )

        if std_width != target_width:
            bg_tall = self._scale_horizontal_with_borders(bg_tall, target_width, interp_method="BILINEAR", preserve_black=True)
            fill_tall = self._scale_horizontal_with_borders(fill_tall, target_width, interp_method="BILINEAR")
            lines_tall = self._scale_horizontal_with_borders(lines_tall, target_width, interp_method="BILINEAR", preserve_black=True)
            linesfill_tall = self._scale_horizontal_with_borders(linesfill_tall, target_width, interp_method="BILINEAR")
        
        # Create new image (120×64)
        result = Image.new('RGBA', (target_width, 64), (0, 0, 0, 0))
        result.paste(bg_tall, (0, 0))
        result.paste(fill_tall, (0, 16))
        result.paste(lines_tall, (0, 32))
        result.paste(linesfill_tall, (0, 48))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
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
        
        # Get 120t source (must be generated first)
        source_filename = self.get_output_filename(base_name, 120, is_tall=True)
        source = self.variant_dir / source_filename
        
        if not source.exists():
            # Source not yet generated, skip
            return False
        
        output_filename = self.get_output_filename(base_name, width, is_tall=True)
        output_file = self.variant_dir / output_filename
        
        scale_factor = width / 120.0
        print(f"  Generating tall gauge @ {width}×64 ({scale_factor:.2f}x from 120t)...")
        
        # Load 120t source
        tall = Image.open(source)
        tall_width = tall.size[0]  # Should be 120
        
        # Extract individual sections (16px each)
        bg = tall.crop((0, 0, tall_width, 16))
        fill = tall.crop((0, 16, tall_width, 32))
        lines = tall.crop((0, 32, tall_width, 48))
        linesfill = tall.crop((0, 48, tall_width, 64))
        
        debug_sections = [] if self.debug else None

        # Scale each section horizontally
        bg_scaled = self._scale_horizontal_with_borders(
            bg, width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="background"
        )
        fill_scaled = self._scale_horizontal_with_borders(
            fill, width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="fill"
        )
        lines_scaled = self._scale_horizontal_with_borders(
            lines, width, interp_method="BILINEAR", preserve_black=True,
            debug_bucket=debug_sections, debug_label="lines"
        )
        linesfill_scaled = self._scale_horizontal_with_borders(
            linesfill, width, interp_method="BILINEAR",
            debug_bucket=debug_sections, debug_label="linesfill"
        )
        
        # Create new image at target dimensions
        result = Image.new('RGBA', (width, 64), (0, 0, 0, 0))
        result.paste(bg_scaled, (0, 0))
        result.paste(fill_scaled, (0, 16))
        result.paste(lines_scaled, (0, 32))
        result.paste(linesfill_scaled, (0, 48))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
        if self.debug and debug_sections:
            self._write_debug_canvas(output_file, debug_sections)
        self.stats["generated"]["tall"].append(output_filename)
        return True
    
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
    Thorne, Bars, Basic, Bubbles, Light Bubbles

FEATURES:
    [*] Dynamic sizing (WIDE_WIDTHS, TALL_WIDTHS)
    [*] Automatic TGA format fixing
    [*] Smart copyback (single->thorne_drak, multi->Thorne only)
    [*] Automatic deployment to thorne_dev/
    [*] Stats JSON generation

WORKFLOW:
    1. Edit source: thorne_drak/Options/Gauges/Thorne/gauge_inlay_thorne01.tga
    2. Run: python regen_gauges.py --all  (or specify: Thorne)
    3. Test: /loadskin thorne_drak

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
