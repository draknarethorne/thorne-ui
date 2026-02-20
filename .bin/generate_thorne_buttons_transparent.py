"""Generate transparency variants of button source atlas with proper border preservation.

This script creates multiple opacity levels (75%, 50%, 25%) from the solid button
source, preserving:
- 3px opaque borders (original alpha unmodified)
- Inner pixel colors (original RGB preserved, only alpha reduced)
"""

from pathlib import Path
from PIL import Image


ROOT = Path("C:/Thorne-UI")
BUTTON_SOURCE = ROOT / "thorne_drak" / "thorne_buttons01.tga"

# Transparency levels: (description, alpha_value)
TRANSPARENCY_LEVELS = [
    ("90", 230),   # 90% of 255
    ("80", 204),   # 80% of 255
    ("75", 191),   # 75% of 255
]

BORDER_WIDTH = 3


def load_tga(filepath: Path) -> Image.Image:
    """Load TGA file as RGBA Image."""
    return Image.open(filepath).convert("RGBA")


def save_tga(image: Image.Image, filepath: Path) -> None:
    """Save PIL Image as TGA format."""
    w, h = image.size
    
    # Create TGA header
    header = bytearray(18)
    header[2] = 2   # Image type: uncompressed true color
    header[12] = w & 0xFF
    header[13] = (w >> 8) & 0xFF
    header[14] = h & 0xFF
    header[15] = (h >> 8) & 0xFF
    header[16] = 32  # Bits per pixel (RGBA)
    header[17] = 0x20  # Image descriptor (origin top-left)
    
    # Get pixel data in BGRA format
    pixels = image.convert('RGBA')
    pixel_data = pixels.tobytes('raw', 'BGRA')
    
    # Write file
    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(pixel_data)


def make_transparent_variant(button: Image.Image, target_alpha: int, border_width: int = 3) -> Image.Image:
    """Create transparency variant preserving colors and 3px opaque border.
    
    Args:
        button: Source button image (40x40)
        target_alpha: Target alpha value for inner pixels (0-255)
        border_width: Width of opaque border to preserve
    
    Returns:
        New image with inner transparency, opaque border
    """
    variant = button.copy()
    pixels = variant.load()
    w, h = variant.size
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = variant.getpixel((x, y))
            
            # Fully transparent pixels: keep as-is
            if a == 0:
                continue
            
            # Check if in border region
            is_border = (x < border_width or x >= w - border_width or 
                        y < border_width or y >= h - border_width)
            
            if is_border:
                # Keep border opaque with original colors
                pixels[x, y] = (r, g, b, a)
            else:
                # Inner: preserve color, reduce alpha
                pixels[x, y] = (r, g, b, target_alpha)
    
    return variant


def main() -> None:
    if not BUTTON_SOURCE.exists():
        raise FileNotFoundError(f"Missing button source: {BUTTON_SOURCE}")
    
    # Load the 255x255 button atlas
    atlas = load_tga(BUTTON_SOURCE)
    
    print(f"Source atlas: {atlas.size} {atlas.mode}")
    
    # Extract solid buttons (row 1 @ y=0)
    button1_solid = atlas.crop((0, 0, 40, 40))
    button2_solid = atlas.crop((40, 0, 80, 40))
    
    print(f"Extracted: button1_solid {button1_solid.size}, button2_solid {button2_solid.size}")
    
    # Create variants for each transparency level
    for trans_label, trans_alpha in TRANSPARENCY_LEVELS:
        button1_trans = make_transparent_variant(button1_solid, trans_alpha, BORDER_WIDTH)
        button2_trans = make_transparent_variant(button2_solid, trans_alpha, BORDER_WIDTH)
        
        print(f"  Generated {trans_label}% opacity variants (A={trans_alpha})")
    
    # Create new expanded atlas with all variants stacked
    new_atlas = Image.new('RGBA', (255, 255), (0, 0, 0, 0))
    
    # Row 1 @ y=0: Solid (already in source)
    new_atlas.paste(button1_solid, (0, 0), button1_solid)
    new_atlas.paste(button2_solid, (40, 0), button2_solid)
    
    # Rows 2-4: Transparency variants
    y_positions = [44, 88, 132]
    for (trans_label, trans_alpha), y_pos in zip(TRANSPARENCY_LEVELS, y_positions):
        button1_trans = make_transparent_variant(button1_solid, trans_alpha, BORDER_WIDTH)
        button2_trans = make_transparent_variant(button2_solid, trans_alpha, BORDER_WIDTH)
        
        new_atlas.paste(button1_trans, (0, y_pos), button1_trans)
        new_atlas.paste(button2_trans, (40, y_pos), button2_trans)
        
        print(f"✓ Placed {trans_label}% opacity @ y={y_pos}")
    
    # Save updated atlas
    save_tga(new_atlas, BUTTON_SOURCE)
    
    print(f"\nUpdated: {BUTTON_SOURCE}")
    print("Button atlas layout (255x255):")
    print("  Row 1 @ y=0:   Solid (100% opacity, A=255)")
    print("  Row 2 @ y=44:  90% opacity (A=230) - both buttons, colors preserved, border opaque")
    print("  Row 3 @ y=88:  80% opacity (A=204) - both buttons, colors preserved, border opaque")
    print("  Row 4 @ y=132: 75% opacity (A=191) - both buttons, colors preserved, border opaque")


if __name__ == "__main__":
    main()
