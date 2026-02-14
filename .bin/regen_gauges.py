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
import shutil


def is_png_file(file_path):
    """Check if a .tga file is actually PNG format"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            # PNG signature: 89 50 4E 47 0D 0A 1A 0A
            return header.startswith(b'\x89PNG\r\n\x1a\n')
    except Exception:
        return False


def fix_tga_file(file_path):
    """Convert PNG file (mislabeled as .tga) to proper TGA format if needed"""
    if not file_path.exists():
        return False
    
    if not is_png_file(file_path):
        # Already valid TGA
        return False
    
    # Convert PNG to TGA
    try:
        img = Image.open(file_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(str(file_path), format='TGA')
        print(f"  Fixed: {file_path.name} (converted from PNG to TGA)")
        return True
    except Exception as e:
        print(f"  ERROR: Failed to fix {file_path.name}: {e}")
        return False

def regenerate_tall_gauge(variant_dir):
    """Regenerate tall gauge by properly scaling each section."""
    variant_dir = Path(variant_dir)
    std_file = variant_dir / 'gauge_pieces01.tga'
    tall_file = variant_dir / 'gauge_pieces01_tall.tga'
    
    if not std_file.exists():
        print(f"ERROR: {std_file} not found")
        return False
    
    # Fix source TGA file if it's actually PNG
    fix_tga_file(std_file)
    
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
    def scale_with_borders(section, width, interp_method="BILINEAR"):
        """Scale 8px section to 16px preserving 1px top/bottom borders.
        
        Args:
            interp_method: Interpolation for middle section.
                          "BILINEAR" (default), "LANCZOS", or "NEAREST"
        """
        top = section.crop((0, 0, width, 1))  # Y=0: 1px border
        middle = section.crop((0, 1, width, 7))  # Y=1-6: 6px content
        bottom = section.crop((0, 7, width, 8))  # Y=7: 1px border
        
        # Choose interpolation method
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:  # Default to BILINEAR
            interp = Image.Resampling.BILINEAR
        
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
    
    bg_tall = scale_with_borders(bg, std_width, interp_method="BILINEAR")
    fill_tall = scale_with_borders(fill, std_width, interp_method="BILINEAR")
    lines_tall = scale_with_borders(lines, std_width, interp_method="NEAREST")
    linesfill_tall = scale_with_borders(linesfill, std_width, interp_method="NEAREST")
    
    interp_note = "BILINEAR for Background/Fill, NEAREST for crisp Lines"
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
    print(f"  [OK] {variant_dir.name} tall gauge regenerated")
    
    return True


def regenerate_wide_gauge(variant_dir):
    """Regenerate wide gauge by horizontally stretching each section from 60px to 120px."""
    variant_dir = Path(variant_dir)
    std_file = variant_dir / 'gauge_pieces01.tga'
    wide_file = variant_dir / 'gauge_pieces01_wide.tga'
    
    if not std_file.exists():
        print(f"ERROR: {std_file} not found")
        return False
    
    # Fix source TGA file if it's actually PNG (note: only fix once on first call)
    # This is safe to call multiple times per variant since fix returns early if already valid
    fix_tga_file(std_file)
    
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
    def scale_horizontal_with_borders(section, target_width=120, interp_method="BILINEAR"):
        """Horizontally scale section to 120px preserving 1px left/right borders.
        
        Args:
            interp_method: Interpolation for middle section.
                          "BILINEAR" (default), "LANCZOS", or "NEAREST"
        """
        width, height = section.size
        
        # Extract borders and middle
        left = section.crop((0, 0, 1, height))  # X=0: 1px border
        middle = section.crop((1, 0, width-1, height))  # X=1 to width-2: middle content
        right = section.crop((width-1, 0, width, height))  # X=width-1: 1px border
        
        # Choose interpolation method
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:  # Default to BILINEAR
            interp = Image.Resampling.BILINEAR
        
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
    
    bg_wide = scale_horizontal_with_borders(bg, interp_method="BILINEAR")
    fill_wide = scale_horizontal_with_borders(fill, interp_method="BILINEAR")
    lines_wide = scale_horizontal_with_borders(lines, interp_method="NEAREST")
    linesfill_wide = scale_horizontal_with_borders(linesfill, interp_method="NEAREST")
    
    interp_note = "BILINEAR for Background/Fill, NEAREST for crisp Lines"
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
    print(f"  [OK] {variant_dir.name} wide gauge regenerated")
    
    return True


def regenerate_tall_wide_gauge(variant_dir):
    """Regenerate tall_wide gauge by scaling vertically (tall: 16px) and horizontally to 250px."""
    variant_dir = Path(variant_dir)
    std_file = variant_dir / 'gauge_pieces01.tga'
    tall_wide_file = variant_dir / 'gauge_pieces01_tall_wide.tga'
    
    if not std_file.exists():
        print(f"ERROR: {std_file} not found")
        return False
    
    # Fix source TGA file if it's actually PNG
    fix_tga_file(std_file)
    
    print(f"Processing {variant_dir.name} (TALL_WIDE)...")
    
    # Load standard gauge
    std = Image.open(std_file)
    std_width = std.size[0]  # Usually 60
    
    # Extract individual sections (8px tall each)
    bg = std.crop((0, 0, std_width, 8))
    fill = std.crop((0, 8, std_width, 16))
    lines = std.crop((0, 16, std_width, 24))
    linesfill = std.crop((0, 24, std_width, 32))
    
    print(f"  Extracted sections from {std_width}x32 standard gauge")
    
    # Scale sections to 250x16 (preserving 1px borders on all sides)
    def scale_tall_wide_with_borders(section, target_width=250, target_height=16, interp_method="BILINEAR"):
        """Scale section to target dimensions preserving 1px borders on all sides.
        
        Vertical scaling: 8px → 16px (1px top + 14px middle + 1px bottom)
        Horizontal scaling: std_width → 250px (1px left + 248px middle + 1px right)
        
        Args:
            target_width: Target width (default 250)
            target_height: Target height (default 16)
            interp_method: Interpolation for fill ("BILINEAR", "LANCZOS", "NEAREST")
        """
        width, height = section.size
        
        # Extract top border, middle, and bottom border (vertical 1px strips)
        top = section.crop((0, 0, width, 1))
        middle = section.crop((0, 1, width, height-1))
        bottom = section.crop((0, height-1, width, height))
        
        # Choose interpolation
        if interp_method == "LANCZOS":
            interp = Image.Resampling.LANCZOS
        elif interp_method == "NEAREST":
            interp = Image.Resampling.NEAREST
        else:  # Default BILINEAR
            interp = Image.Resampling.BILINEAR
        
        # Helper to scale a single row/section with horizontal borders preserved
        def scale_row_with_h_borders(row_section, target_w=target_width):
            """Scale a row horizontally preserving 1px left/right borders."""
            sect_width, sect_height = row_section.size
            
            left_border = row_section.crop((0, 0, 1, sect_height))
            middle_content = row_section.crop((1, 0, sect_width-1, sect_height))
            right_border = row_section.crop((sect_width-1, 0, sect_width, sect_height))
            
            # Scale middle horizontally to (target_w - 2)
            middle_scaled = middle_content.resize((target_w-2, sect_height), interp)
            
            # Keep borders crisp with NEAREST
            left_scaled = left_border.resize((1, sect_height), Image.Resampling.NEAREST)
            right_scaled = right_border.resize((1, sect_height), Image.Resampling.NEAREST)
            
            # Composite horizontally
            result = Image.new('RGBA', (target_w, sect_height), (0, 0, 0, 0))
            result.paste(left_scaled, (0, 0))
            result.paste(middle_scaled, (1, 0))
            result.paste(right_scaled, (target_w-1, 0))
            return result
        
        # Scale top border (1px tall) horizontally only
        top_scaled = scale_row_with_h_borders(top, target_width)
        
        # Scale middle section both vertically (6px→14px) and horizontally
        # First scale horizontally to preserve left/right borders
        middle_h_scaled = scale_row_with_h_borders(middle, target_width)
        # Then scale vertically
        middle_scaled = middle_h_scaled.resize((target_width, 14), interp)
        
        # Scale bottom border (1px tall) horizontally only
        bottom_scaled = scale_row_with_h_borders(bottom, target_width)
        
        # Composite: top(1) + middle(14) + bottom(1) = 16px tall
        result = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
        result.paste(top_scaled, (0, 0))
        result.paste(middle_scaled, (0, 1))
        result.paste(bottom_scaled, (0, target_height-1))
        
        return result
    
    bg_tall_wide = scale_tall_wide_with_borders(bg, interp_method="BILINEAR")
    fill_tall_wide = scale_tall_wide_with_borders(fill, interp_method="BILINEAR")
    lines_tall_wide = scale_tall_wide_with_borders(lines, interp_method="NEAREST")
    linesfill_tall_wide = scale_tall_wide_with_borders(linesfill, interp_method="NEAREST")
    
    interp_note = "BILINEAR for Background/Fill, NEAREST for crisp Lines"
    print(f"  Scaled: 1px borders (NEAREST) + 248px middle to 250px width ({interp_note})")
    
    # Create new 250x64 image
    tall_wide_new = Image.new('RGBA', (250, 64), (0, 0, 0, 0))
    
    # Paste sections at correct Y coordinates
    tall_wide_new.paste(bg_tall_wide, (0, 0))          # Y=0-15
    tall_wide_new.paste(fill_tall_wide, (0, 16))       # Y=16-31
    tall_wide_new.paste(lines_tall_wide, (0, 32))      # Y=32-47
    tall_wide_new.paste(linesfill_tall_wide, (0, 48))  # Y=48-63
    
    print("  Composited sections into 250x64 tall_wide gauge")
    
    # Save
    tall_wide_new.save(tall_wide_file)
    print(f"  Saved to {tall_wide_file.name}")
    print(f"  [OK] {variant_dir.name} tall_wide gauge regenerated")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h', 'help'):
        print("""
Gauge Texture Regeneration Tool
================================

Regenerates tall (120×64) and wide (120×32) gauge textures from source files.

USAGE:
    python regen_gauges.py --all                           # Auto-discover all variants
    python regen_gauges.py <variant> [variant2 ...]       # Specific variants
    python regen_gauges.py --help

EXAMPLES:
    # Regenerate ALL variants (auto-discovered from Gauges/ directory)
    python regen_gauges.py --all
    
    # Single variant - copies to thorne_drak/ and deploys to thorne_dev/
    python regen_gauges.py Thorne
    
    # Two variants
    python regen_gauges.py Bars Basic
    
    # Multiple variants - only Thorne copied to thorne_drak/
    python regen_gauges.py root Bars Basic Bubbles "Light Bubbles" Thorne
    
    # Show this help message
    python regen_gauges.py --help
    python regen_gauges.py -h

OPTIONS:
    --all               Auto-discover and regenerate all variants from Gauges/
    <variant>           Specific variant name (e.g., Thorne, Bars, Basic)
    root                Direct regeneration of thorne_drak/ directory

AVAILABLE VARIANTS (auto-discovered):
    Thorne              Primary development variant
    Bars, Basic         Gauge style variants
    Bubbles, Light Bubbles

FEATURES:
    ✓ Regenerates both tall (120×64) and wide (120×32) gauges
    ✓ Automatic TGA format fixing (PNG→TGA conversion)
    ✓ Smart copyback (single→thorne_drak, multi→Thorne only)
    ✓ Automatic deployment to thorne_dev/ for immediate testing
    ✓ BILINEAR interpolation for fills, NEAREST for crisp lines

WORKFLOW:
    1. Edit source: thorne_drak/Options/Gauges/Thorne/gauge_pieces01.tga
    2. Run: python regen_gauges.py --all  (or: python regen_gauges.py Thorne)
    3. Test: /loadskin thorne_drak

For detailed documentation, see: .bin/regen_gauges.md
        """)
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    base_path = Path(__file__).parent.parent / 'thorne_drak' / 'Options' / 'Gauges'
    root_path = Path(__file__).parent.parent / 'thorne_drak'
    
    # Determine which variants to process
    if '--all' in sys.argv:
        # Auto-discover all variants from Gauges directory
        if base_path.exists():
            variant_names = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
            print(f"Auto-discovered {len(variant_names)} variants: {', '.join(variant_names)}\n")
        else:
            print(f"ERROR: Gauges directory not found at {base_path}")
            sys.exit(1)
    else:
        # Use explicitly specified variants
        variant_names = sys.argv[1:]
    
    tall_success = 0
    wide_success = 0
    tall_wide_success = 0
    regenerated_variants = []  # Track which variants were successfully regenerated
    
    for variant in variant_names:
        if variant.lower() == 'root':
            variant_path = root_path
        else:
            variant_path = base_path / variant
            
        if variant_path.exists():
            if regenerate_tall_gauge(variant_path):
                tall_success += 1
                regenerated_variants.append((variant, variant_path))
            if regenerate_wide_gauge(variant_path):
                wide_success += 1
            if regenerate_tall_wide_gauge(variant_path):
                tall_wide_success += 1
        else:
            print(f"ERROR: {variant_path} not found\n")
    
    print(f"Regenerated {tall_success}/{len(variant_names)} tall variants")
    print(f"Regenerated {wide_success}/{len(variant_names)} wide variants")
    print(f"Regenerated {tall_wide_success}/{len(variant_names)} tall_wide variants")
    
    # Copy regenerated files back to thorne_drak root directory
    # Logic: single variant → copy that one; multiple variants → copy only Thorne
    variants_to_copy = []
    
    if len(regenerated_variants) == 1 and regenerated_variants[0][0].lower() != 'root':
        # Single variant (not root) - copy it
        variants_to_copy = regenerated_variants
    elif len(regenerated_variants) > 1:
        # Multiple variants - only copy Thorne if it was regenerated
        variants_to_copy = [(name, path) for name, path in regenerated_variants if name.lower() == 'thorne']
    
    if variants_to_copy:
        print(f"\nCopying regenerated files back to thorne_drak/...")
        for variant_name, variant_path in variants_to_copy:
            main_src = variant_path / 'gauge_pieces01.tga'
            tall_src = variant_path / 'gauge_pieces01_tall.tga'
            wide_src = variant_path / 'gauge_pieces01_wide.tga'
            tall_wide_src = variant_path / 'gauge_pieces01_tall_wide.tga'
            main_dst = root_path / 'gauge_pieces01.tga'
            tall_dst = root_path / 'gauge_pieces01_tall.tga'
            wide_dst = root_path / 'gauge_pieces01_wide.tga'
            tall_wide_dst = root_path / 'gauge_pieces01_tall_wide.tga'
            
            if main_src.exists():
                shutil.copy2(main_src, main_dst)
                print(f"  Copied {variant_name} main gauge to thorne_drak/")
            if tall_src.exists():
                shutil.copy2(tall_src, tall_dst)
                print(f"  Copied {variant_name} tall gauge to thorne_drak/")
            if wide_src.exists():
                shutil.copy2(wide_src, wide_dst)
                print(f"  Copied {variant_name} wide gauge to thorne_drak/")
            if tall_wide_src.exists():
                shutil.copy2(tall_wide_src, tall_wide_dst)
                print(f"  Copied {variant_name} tall_wide gauge to thorne_drak/")
        
        # Also copy to thorne_dev for immediate testing
        thorne_dev_path = Path('C:\\TAKP\\uifiles\\thorne_dev')
        if thorne_dev_path.exists():
            print(f"\nDeploying to thorne_dev for testing...")
            for variant_name, variant_path in variants_to_copy:
                main_src = root_path / 'gauge_pieces01.tga'
                tall_src = root_path / 'gauge_pieces01_tall.tga'
                wide_src = root_path / 'gauge_pieces01_wide.tga'
                tall_wide_src = root_path / 'gauge_pieces01_tall_wide.tga'
                main_dst = thorne_dev_path / 'gauge_pieces01.tga'
                tall_dst = thorne_dev_path / 'gauge_pieces01_tall.tga'
                wide_dst = thorne_dev_path / 'gauge_pieces01_wide.tga'
                tall_wide_dst = thorne_dev_path / 'gauge_pieces01_tall_wide.tga'
                
                if main_src.exists():
                    shutil.copy2(main_src, main_dst)
                    print(f"  Deployed {variant_name} main gauge to thorne_dev/")
                if tall_src.exists():
                    shutil.copy2(tall_src, tall_dst)
                    print(f"  Deployed {variant_name} tall gauge to thorne_dev/")
                if wide_src.exists():
                    shutil.copy2(wide_src, wide_dst)
                    print(f"  Deployed {variant_name} wide gauge to thorne_dev/")
                if tall_wide_src.exists():
                    shutil.copy2(tall_wide_src, tall_wide_dst)
                    print(f"  Deployed {variant_name} tall_wide gauge to thorne_dev/")
            print(f"\nReady to test in-game with: /loadskin thorne_drak")
