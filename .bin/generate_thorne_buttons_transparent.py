"""Generate transparency variants of button source atlas with proper border preservation.

This script dynamically detects all buttons in the top row and generates multiple
opacity levels for each, preserving:
- 3px opaque borders (original alpha unmodified)
- Inner pixel colors (original RGB preserved, only alpha reduced)

Top row can contain multiple source buttons at any 40px-aligned position.
Script will generate transparency variants for all detected buttons.
"""

from pathlib import Path
from PIL import Image


ROOT = Path("C:/Thorne-UI")
BUTTON_SOURCE = ROOT / "thorne_drak" / "thorne_buttons01.tga"

# Transparency levels: (description, alpha_value)
# Ordered from highest opacity to lowest
TRANSPARENCY_LEVELS = [
    ("95", 242),   # 95% of 255
    ("90", 230),   # 90% of 255
    ("85", 217),   # 85% of 255
    ("75", 191),   # 75% of 255
    ("50", 128),   # 50% of 255
]

BORDER_WIDTH = 3
BUTTON_SIZE = 40
BUTTON_SCAN_WIDTH = 255  # Total width to scan for buttons


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
    
    # Load the button atlas
    atlas = load_tga(BUTTON_SOURCE)
    
    print(f"Source atlas: {atlas.size} {atlas.mode}")
    
    # Detect all buttons in top row (y=0) by scanning at 40px intervals
    source_buttons = []  # List of (x_position, button_image)
    
    for x in range(0, BUTTON_SCAN_WIDTH, BUTTON_SIZE):
        # Extract potential button region
        if x + BUTTON_SIZE > atlas.width:
            break
        
        button_img = atlas.crop((x, 0, x + BUTTON_SIZE, BUTTON_SIZE))
        
        # Check if button has any visible pixels (not fully transparent)
        pixels = button_img.load()
        has_content = False
        for y in range(BUTTON_SIZE):
            for px in range(BUTTON_SIZE):
                r, g, b, a = button_img.getpixel((px, y))
                if a > 0:
                    has_content = True
                    break
            if has_content:
                break
        
        if has_content:
            source_buttons.append((x, button_img))
            print(f"  Found button at x={x}")
    
    if not source_buttons:
        raise ValueError("No buttons found in top row (y=0)")
    
    print(f"Detected {len(source_buttons)} source button(s) in top row\n")
    
    # Create new expanded atlas with all variants
    # Need: 1 solid row + 5 transparency rows = 6 rows total
    # 6 × 40px = 240px (leaves 15px padding)
    new_atlas = Image.new('RGBA', (BUTTON_SCAN_WIDTH, 255), (0, 0, 0, 0))
    
    # Row 1 @ y=0: Solid (copy from source)
    for btn_x, btn_img in source_buttons:
        new_atlas.paste(btn_img, (btn_x, 0), btn_img)
    
    # Rows 2-6: Transparency variants (3px gaps to fit 6×40px in 255px height)
    y_positions = [43, 86, 129, 172, 215]  # Calculated: (255-240)/5 = 3px gaps
    
    for (trans_label, trans_alpha), y_pos in zip(TRANSPARENCY_LEVELS, y_positions):
        for btn_x, btn_solid in source_buttons:
            variant = make_transparent_variant(btn_solid, trans_alpha, BORDER_WIDTH)
            new_atlas.paste(variant, (btn_x, y_pos), variant)
        
        print(f"✓ Generated {trans_label}% opacity variants @ y={y_pos}")
    
    # Save updated atlas
    save_tga(new_atlas, BUTTON_SOURCE)
    
    print(f"\nUpdated: {BUTTON_SOURCE}")
    print(f"Button atlas layout ({BUTTON_SCAN_WIDTH}×{new_atlas.height}):")
    print(f"  Row 1 @ y=0:   Solid (100% opacity, A=255)")
    print(f"  Row 2 @ y=43:  95% opacity (A=242)  - {len(source_buttons)} button(s), colors preserved")
    print(f"  Row 3 @ y=86:  90% opacity (A=230)  - {len(source_buttons)} button(s), colors preserved")
    print(f"  Row 4 @ y=129: 85% opacity (A=217)  - {len(source_buttons)} button(s), colors preserved")
    print(f"  Row 5 @ y=172: 75% opacity (A=191)  - {len(source_buttons)} button(s), colors preserved")
    print(f"  Row 6 @ y=215: 50% opacity (A=128)  - {len(source_buttons)} button(s), colors preserved")


if __name__ == "__main__":
    main()
