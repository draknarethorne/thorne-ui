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

def regenerate_tall_gauge(variant_dir):
    """Regenerate tall gauge by properly scaling each section."""
    variant_dir = Path(variant_dir)
    std_file = variant_dir / 'gauge_pieces01.tga'
    tall_file = variant_dir / 'gauge_pieces01_tall.tga'
    
    if not std_file.exists():
        print(f"ERROR: {std_file} not found")
        return False
    
    print(f"Processing {variant_dir.name}...")
    
    # Load standard gauge
    std = Image.open(std_file)
    std_width = std.size[0]  # Usually 103 or 100
    
    # Extract individual sections (8px each)
    bg = std.crop((0, 0, std_width, 8))
    fill = std.crop((0, 8, std_width, 16))
    lines = std.crop((0, 16, std_width, 24))
    linesfill = std.crop((0, 24, std_width, 32))
    
    print(f"  Extracted sections from {std_width}x32 standard gauge")
    
    # Scale sections preserving single-pixel top/bottom borders
    # For each 8px section: top border (1px) + middle (6px→14px) + bottom border (1px) = 16px
    def scale_with_borders(section, width, use_lanczos=True):
        """Scale 8px section to 16px preserving 1px top/bottom borders.
        
        Args:
            use_lanczos: If True, use LANCZOS for smooth gradients (backgrounds/fills).
                        If False, use NEAREST for crisp edges (lines).
        """
        top = section.crop((0, 0, width, 1))  # Y=0: 1px border
        middle = section.crop((0, 1, width, 7))  # Y=1-6: 6px content
        bottom = section.crop((0, 7, width, 8))  # Y=7: 1px border
        
        # Choose interpolation method
        interp = Image.Resampling.LANCZOS if use_lanczos else Image.Resampling.NEAREST
        
        # Scale middle from 6px to 14px height
        middle_scaled = middle.resize((120, 14), interp)
        
        # Scale borders to 120px width only (keep 1px height) with NEAREST for crisp edges
        top_scaled = top.resize((120, 1), Image.Resampling.NEAREST)
        bottom_scaled = bottom.resize((120, 1), Image.Resampling.NEAREST)
        
        # Composite: top(1) + middle(14) + bottom(1) = 16px
        result = Image.new('RGBA', (120, 16), (0, 0, 0, 0))
        result.paste(top_scaled, (0, 0))
        result.paste(middle_scaled, (0, 1))
        result.paste(bottom_scaled, (0, 15))
        
        return result
    
    bg_tall = scale_with_borders(bg, std_width, use_lanczos=True)
    fill_tall = scale_with_borders(fill, std_width, use_lanczos=True)
    lines_tall = scale_with_borders(lines, std_width, use_lanczos=False)
    linesfill_tall = scale_with_borders(linesfill, std_width, use_lanczos=False)
    
    interp_note = "LANCZOS for Background/Fill smoothness, NEAREST for crisp Lines"
    print(f"  Scaled: 1px borders (NEAREST) + 14px middle ({interp_note})")
    
    # Create new 120x64 image
    tall_new = Image.new('RGBA', (120, 64), (0, 0, 0, 0))
    
    # Paste sections at correct Y coordinates
    tall_new.paste(bg_tall, (0, 0))          # Y=0-15
    tall_new.paste(fill_tall, (0, 16))       # Y=16-31
    tall_new.paste(lines_tall, (0, 32))      # Y=32-47
    tall_new.paste(linesfill_tall, (0, 48))  # Y=48-63
    
    print("  Composited sections into 120x64 tall gauge")
    
    # Save
    tall_new.save(tall_file)
    print(f"  Saved to {tall_file.name}")
    print(f"  ✓ {variant_dir.name} tall gauge regenerated\n")
    
    return True


def regenerate_wide_gauge(variant_dir):
    """Regenerate wide gauge by horizontally stretching each section from 60px to 120px."""
    variant_dir = Path(variant_dir)
    std_file = variant_dir / 'gauge_pieces01.tga'
    wide_file = variant_dir / 'gauge_pieces01_wide.tga'
    
    if not std_file.exists():
        print(f"ERROR: {std_file} not found")
        return False
    
    print(f"Processing {variant_dir.name} (WIDE)...")
    
    # Load standard gauge
    std = Image.open(std_file)
    std_width = std.size[0]  # Usually 60
    
    # Extract individual sections (8px tall each)
    bg = std.crop((0, 0, std_width, 8))
    fill = std.crop((0, 8, std_width, 16))
    lines = std.crop((0, 16, std_width, 24))
    linesfill = std.crop((0, 24, std_width, 32))
    
    print(f"  Extracted sections from {std_width}x32 standard gauge")
    
    # Scale sections horizontally preserving single-pixel left/right borders
    # For each section: left border (1px) + middle (58px→118px) + right border (1px) = 120px
    def scale_horizontal_with_borders(section, target_width=120, use_lanczos=True):
        """Horizontally scale section to 120px preserving 1px left/right borders.
        
        Args:
            use_lanczos: If True, use LANCZOS for smooth gradients (backgrounds/fills).
                        If False, use NEAREST for crisp edges (lines).
        """
        width, height = section.size
        
        # Extract borders and middle
        left = section.crop((0, 0, 1, height))  # X=0: 1px border
        middle = section.crop((1, 0, width-1, height))  # X=1 to width-2: middle content
        right = section.crop((width-1, 0, width, height))  # X=width-1: 1px border
        
        # Choose interpolation method
        interp = Image.Resampling.LANCZOS if use_lanczos else Image.Resampling.NEAREST
        
        # Scale middle from (width-2)px to (target_width-2)px
        middle_width = target_width - 2
        middle_scaled = middle.resize((middle_width, height), interp)
        
        # Scale borders to 1px width only (keep height) with NEAREST for crisp edges
        left_scaled = left.resize((1, height), Image.Resampling.NEAREST)
        right_scaled = right.resize((1, height), Image.Resampling.NEAREST)
        
        # Composite: left(1) + middle(118) + right(1) = 120px
        result = Image.new('RGBA', (target_width, height), (0, 0, 0, 0))
        result.paste(left_scaled, (0, 0))
        result.paste(middle_scaled, (1, 0))
        result.paste(right_scaled, (target_width-1, 0))
        
        return result
    
    bg_wide = scale_horizontal_with_borders(bg, use_lanczos=True)
    fill_wide = scale_horizontal_with_borders(fill, use_lanczos=True)
    lines_wide = scale_horizontal_with_borders(lines, use_lanczos=False)
    linesfill_wide = scale_horizontal_with_borders(linesfill, use_lanczos=False)
    
    interp_note = "LANCZOS for Background/Fill smoothness, NEAREST for crisp Lines"
    print(f"  Scaled: 1px borders (NEAREST) + 118px middle ({interp_note})")
    
    # Create new 120x32 image
    wide_new = Image.new('RGBA', (120, 32), (0, 0, 0, 0))
    
    # Paste sections at correct Y coordinates
    wide_new.paste(bg_wide, (0, 0))          # Y=0-7
    wide_new.paste(fill_wide, (0, 8))        # Y=8-15
    wide_new.paste(lines_wide, (0, 16))      # Y=16-23
    wide_new.paste(linesfill_wide, (0, 24))  # Y=24-31
    
    print("  Composited sections into 120x32 wide gauge")
    
    # Save
    wide_new.save(wide_file)
    print(f"  Saved to {wide_file.name}")
    print(f"  ✓ {variant_dir.name} wide gauge regenerated\n")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: regenerate_tall_gauge_proper.py <variant_dir> [variant_dir2 ...]")
        print("Example: regenerate_tall_gauge_proper.py root Bars Basic Bubbles")
        print("  'root' = thorne_drak/ directory")
        print("  others = thorne_drak/Options/Gauges/<variant>/ directories")
        sys.exit(1)
    
    variant_names = sys.argv[1:]
    base_path = Path(__file__).parent.parent / 'thorne_drak' / 'Options' / 'Gauges'
    root_path = Path(__file__).parent.parent / 'thorne_drak'
    
    tall_success = 0
    wide_success = 0
    for variant in variant_names:
        if variant.lower() == 'root':
            variant_path = root_path
        else:
            variant_path = base_path / variant
            
        if variant_path.exists():
            if regenerate_tall_gauge(variant_path):
                tall_success += 1
            if regenerate_wide_gauge(variant_path):
                wide_success += 1
        else:
            print(f"ERROR: {variant_path} not found\n")
    
    print(f"Regenerated {tall_success}/{len(variant_names)} tall variants")
    print(f"Regenerated {wide_success}/{len(variant_names)} wide variants")
