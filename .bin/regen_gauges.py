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

from PIL import Image
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


class GaugeGenerator:
    """Manages gauge generation with stats tracking."""
    
    def __init__(self, variant_dir):
        """Initialize generator for a gauge variant.
        
        Args:
            variant_dir: Path to variant directory (e.g., thorne_drak/Options/Gauges/Thorne)
        """
        self.variant_dir = Path(variant_dir)
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
        
        # Scale each section horizontally
        bg_wide = self._scale_horizontal_with_borders(bg, width)
        fill_wide = self._scale_horizontal_with_borders(fill, width, interp_method="BILINEAR")
        lines_wide = self._scale_horizontal_with_borders(lines, width, interp_method="NEAREST")
        linesfill_wide = self._scale_horizontal_with_borders(linesfill, width, interp_method="NEAREST")
        
        # Create new image
        result = Image.new('RGBA', (width, 32), (0, 0, 0, 0))
        result.paste(bg_wide, (0, 0))
        result.paste(fill_wide, (0, 8))
        result.paste(lines_wide, (0, 16))
        result.paste(linesfill_wide, (0, 24))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
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
        
        # Extract individual sections (8px each)
        bg = std.crop((0, 0, std_width, 8))
        fill = std.crop((0, 8, std_width, 16))
        lines = std.crop((0, 16, std_width, 24))
        linesfill = std.crop((0, 24, std_width, 32))
        
        # Scale each section vertically (8px → 16px)
        bg_tall = self._scale_with_borders(bg, std_width)
        fill_tall = self._scale_with_borders(fill, std_width, interp_method="BILINEAR")
        lines_tall = self._scale_with_borders(lines, std_width, interp_method="NEAREST")
        linesfill_tall = self._scale_with_borders(linesfill, std_width, interp_method="NEAREST")
        
        # Create new image (120×64)
        result = Image.new('RGBA', (std_width, 64), (0, 0, 0, 0))
        result.paste(bg_tall, (0, 0))
        result.paste(fill_tall, (0, 16))
        result.paste(lines_tall, (0, 32))
        result.paste(linesfill_tall, (0, 48))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
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
        
        # Scale each section horizontally
        bg_scaled = self._scale_horizontal_with_borders(bg, width)
        fill_scaled = self._scale_horizontal_with_borders(fill, width, interp_method="BILINEAR")
        lines_scaled = self._scale_horizontal_with_borders(lines, width, interp_method="NEAREST")
        linesfill_scaled = self._scale_horizontal_with_borders(linesfill, width, interp_method="NEAREST")
        
        # Create new image at target dimensions
        result = Image.new('RGBA', (width, 64), (0, 0, 0, 0))
        result.paste(bg_scaled, (0, 0))
        result.paste(fill_scaled, (0, 16))
        result.paste(lines_scaled, (0, 32))
        result.paste(linesfill_scaled, (0, 48))
        
        # Save
        result.save(str(output_file), format='TGA')
        print(f"    Saved: {output_filename}")
        self.stats["generated"]["tall"].append(output_filename)
        return True
    
    def _scale_with_borders(self, section, width, interp_method="BILINEAR"):
        """Scale 8px section to 16px preserving 1px top/bottom borders.
        
        Args:
            section: Image section to scale
            width: Width to preserve (no horizontal scaling)
            interp_method: Interpolation for middle section
        
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
        middle_scaled = middle.resize((width, 14), interp)
        
        # Keep borders crisp
        top_scaled = top.resize((width, 1), Image.Resampling.NEAREST)
        bottom_scaled = bottom.resize((width, 1), Image.Resampling.NEAREST)
        
        # Composite vertically
        result = Image.new('RGBA', (width, 16), (0, 0, 0, 0))
        result.paste(top_scaled, (0, 0))
        result.paste(middle_scaled, (0, 1))
        result.paste(bottom_scaled, (0, 15))
        
        return result
    
    def _scale_horizontal_with_borders(self, section, target_width, interp_method="BILINEAR"):
        """Scale section horizontally to target width, preserving 1px left/right borders.
        
        Args:
            section: Image section to scale
            target_width: Target width in pixels
            interp_method: Interpolation for middle section
        
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
        middle_scaled = middle.resize((target_width-2, height), interp)
        
        # Keep borders crisp
        left_scaled = left.resize((1, height), Image.Resampling.NEAREST)
        right_scaled = right.resize((1, height), Image.Resampling.NEAREST)
        
        # Composite horizontally
        result = Image.new('RGBA', (target_width, height), (0, 0, 0, 0))
        result.paste(left_scaled, (0, 0))
        result.paste(middle_scaled, (1, 0))
        result.paste(right_scaled, (target_width-1, 0))
        
        return result
    
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
    # Help text
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
REGENERATE GAUGE TEXTURES

Regenerates tall (×64px) and wide (×32px) gauge texture variants from a standard
source file. Supports multiple scaling factors with proper border preservation.

AUTO-DISCOVERY:
    Reads from: thorne_drak/Options/Gauges/<Variant>/
    Looks for gauge source files with pattern: gauge_inlay*_thorne0X.tga

VARIANTS:
    Thorne, Bars, Basic, Bubbles, Light Bubbles

FEATURES:
    ✓ Dynamic sizing from configuration lists (WIDE_WIDTHS, TALL_WIDTHS)
    ✓ Automatic TGA format fixing (PNG→TGA conversion)
    ✓ Smart copyback (single→thorne_drak, multi→Thorne only)
    ✓ Automatic deployment to thorne_dev/ for immediate testing
    ✓ Stats JSON generation (.regen_gauges-stats.json)
    ✓ BILINEAR interpolation for fills, NEAREST for crisp lines

WORKFLOW:
    1. Edit source: thorne_drak/Options/Gauges/Thorne/gauge_inlay_thorne01.tga
    2. Run: python regen_gauges.py --all  (or: python regen_gauges.py Thorne)
    3. Test: /loadskin thorne_drak

To add new widths:
    - Edit WIDE_WIDTHS for wide variants (e.g., [120, 150, 160])
    - Edit TALL_WIDTHS for tall variants (e.g., [120, 150, 230, 240, 250, 260])
    - Script automatically generates all combinations

For detailed documentation, see: .bin/regen_gauges.md
        """)
        sys.exit(0)
    
    base_path = Path(__file__).parent.parent / 'thorne_drak' / 'Options' / 'Gauges'
    root_path = Path(__file__).parent.parent / 'thorne_drak'
    
    # Determine which variants to process
    if '--all' in sys.argv:
        # Auto-discover all variants
        if base_path.exists():
            variant_names = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
            print(f"Auto-discovered {len(variant_names)} variants: {', '.join(variant_names)}\n")
        else:
            print(f"ERROR: Gauges directory not found at {base_path}")
            sys.exit(1)
    else:
        # Use explicitly specified variants
        variant_names = sys.argv[1:]
    
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
            generator = GaugeGenerator(variant_path)
            
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
            
            # Copy all generated files
            files_to_copy = (
                generator.stats["generated"]["wide"] +
                generator.stats["generated"]["tall"]
            )
            
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
                
                # Deploy from root_path (where we just copied to)
                files_to_deploy = (
                    generator.stats["generated"]["wide"] +
                    generator.stats["generated"]["tall"]
                )
                
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
