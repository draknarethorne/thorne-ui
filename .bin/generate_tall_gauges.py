"""
Generate tall gauge textures for all gauge variants.

This script stretches standard gauge textures (103x32 or 100x32, 8px slices)
to tall gauge format (120x64, 15px slices) for Bars, Basic, Bubbles, and 
Light Bubbles variants.

Thorne variant already has tall gauges and will be skipped.

Standard layout:  103x32 or 100x32 with 4x 8px slices at Y=0,8,16,24
Tall layout:      120x64 with 4x 15px slices at Y=0,16,31,47
"""

from PIL import Image
from pathlib import Path

# Base path for gauge variants
GAUGES_DIR = Path(__file__).parent.parent / "thorne_drak" / "Options" / "Gauges"

# Variants to process (excluding Thorne which already has tall gauges)
VARIANTS = ["Bars", "Basic", "Bubbles", "Light Bubbles"]

# Target dimensions for tall gauges
TALL_WIDTH = 120
TALL_HEIGHT = 64

def generate_tall_gauge(variant_name: str) -> bool:
    """
    Generate tall gauge texture for a specific variant.
    
    Args:
        variant_name: Name of the gauge variant subdirectory
        
    Returns:
        True if successful, False otherwise
    """
    variant_dir = GAUGES_DIR / variant_name
    source_file = variant_dir / "gauge_pieces01.tga"
    target_file = variant_dir / "gauge_pieces01_tall.tga"
    
    if not source_file.exists():
        print(f"❌ Source file not found: {source_file}")
        return False
    
    if target_file.exists():
        print(f"⚠️  Target file already exists: {target_file}")
        response = input(f"   Overwrite {variant_name} tall gauge? (y/n): ")
        if response.lower() != 'y':
            print(f"   Skipped {variant_name}")
            return False
    
    try:
        # Load source image
        img = Image.open(source_file)
        source_width, source_height = img.size
        
        print(f"📏 {variant_name}: {source_width}x{source_height} → {TALL_WIDTH}x{TALL_HEIGHT}")
        
        # Resize to tall format using high-quality LANCZOS resampling
        tall_img = img.resize((TALL_WIDTH, TALL_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save as TGA (preserve original format)
        tall_img.save(target_file, format='TGA')
        
        print(f"✅ Generated: {target_file.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {variant_name}: {e}")
        return False

def main():
    """Process all gauge variants."""
    print("=" * 60)
    print("Tall Gauge Generator")
    print("=" * 60)
    print()
    
    if not GAUGES_DIR.exists():
        print(f"❌ Gauges directory not found: {GAUGES_DIR}")
        return
    
    print(f"Source directory: {GAUGES_DIR}")
    print(f"Variants to process: {', '.join(VARIANTS)}")
    print()
    
    results = {}
    for variant in VARIANTS:
        success = generate_tall_gauge(variant)
        results[variant] = success
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    successful = sum(1 for v in results.values() if v)
    print(f"✅ Successful: {successful}/{len(VARIANTS)}")
    
    if successful < len(VARIANTS):
        failed = [name for name, success in results.items() if not success]
        print(f"❌ Failed: {', '.join(failed)}")
    
    print()
    print("Next steps:")
    print("- Test at least one variant in-game to verify rendering")
    print("- Commit changes with: git add thorne_drak/Options/Gauges/")
    print("- Reference issue #47 in commit message")

if __name__ == "__main__":
    main()
