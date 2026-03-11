"""generate_thorne_button_atlas.py -- Generate transparency variants of the button source atlas.

Reads configuration from .bin/generate_thorne_button_atlas.json, loads the solid-row button atlas from
Options/Slots/.Master/, detects all buttons in the top row, and generates additional opacity rows below
them while preserving opaque borders and all original pixel colors.

Run this after editing the solid button row in .Master/button_atlas_thorne01.tga.

Usage:
  python .bin/generate_thorne_button_atlas.py [--dry-run]

Output:
  Options/Slots/.Master/button_atlas_thorne01.tga  (updated in-place with 6 rows: solid + 5 opacity levels)
"""

import json
import sys
from pathlib import Path

from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "generate_thorne_button_atlas.json"
MASTER_DIR = SCRIPT_DIR.parent / "thorne_drak" / "Options" / "Slots" / ".Master"


def load_config() -> dict:
    """Load configuration from JSON file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Missing config: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


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
    dry_run = "--dry-run" in sys.argv

    config = load_config()

    # Extract settings
    grid = config["grid"]
    cell_size = grid["cell_size"]
    spacing = grid["spacing"]
    atlas_size = grid["atlas_size"]

    border_width = config["border"]["width"]
    alpha_values = config["transparency_rows"]["alpha_values"]

    source_file = MASTER_DIR / config["source"]["file"]
    output_file = MASTER_DIR / config["output"]["file"]

    if not source_file.exists():
        raise FileNotFoundError(f"Missing button source: {source_file}")

    # Load the button atlas
    atlas = load_tga(source_file)

    print(f"Source atlas: {atlas.size} {atlas.mode}")

    # Detect all buttons in top row (y=0) by scanning for content regions
    source_buttons: list[tuple[int, Image.Image]] = []

    x = 0
    while x < atlas_size - cell_size:
        button_test = atlas.crop((x, 0, x + cell_size, cell_size))

        has_content = False
        for y in range(cell_size):
            for px in range(cell_size):
                _, _, _, a = button_test.getpixel((px, y))
                if a > 0:
                    has_content = True
                    break
            if has_content:
                break

        if has_content:
            source_buttons.append((x, button_test))
            print(f"  Found button at x={x}")
            x += cell_size + spacing
        else:
            x += 1

    if not source_buttons:
        raise ValueError("No buttons found in top row (y=0)")

    print(f"Detected {len(source_buttons)} source button(s) in top row\n")

    # Build full atlas: row 1 solid + remaining rows with transparency
    new_atlas = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))

    for row_idx, alpha in enumerate(alpha_values):
        y_pos = row_idx * (cell_size + spacing)

        for btn_x, btn_solid in source_buttons:
            if alpha >= 255:
                cell = btn_solid.copy()
            else:
                cell = make_transparent_variant(btn_solid, alpha, border_width)

            # Direct paste to preserve exact RGBA values (mask would double-apply alpha)
            new_atlas.paste(cell, (btn_x, y_pos))

        alpha_pct = round(alpha / 255 * 100)
        if alpha >= 255:
            print(f"  Row {row_idx + 1} @ y={y_pos}: Solid ({alpha_pct}% opacity, A={alpha})")
        else:
            print(f"  Row {row_idx + 1} @ y={y_pos}: {alpha_pct}% opacity (A={alpha}) - {len(source_buttons)} button(s), borders preserved")

    if dry_run:
        print(f"\n[DRY RUN] Would write: {output_file}")
        print(f"Atlas: {atlas_size}x{atlas_size}, {len(source_buttons)} buttons x {len(alpha_values)} rows")
        return

    save_tga(new_atlas, output_file)

    print(f"\nUpdated: {output_file}")
    print(f"Button atlas layout ({atlas_size}x{atlas_size}):")
    print(f"  {len(source_buttons)} buttons, {len(alpha_values)} rows ({cell_size}px cells, {spacing}px gaps)")
    print(f"  Border: {border_width}px opaque preserved on all variants")


if __name__ == "__main__":
    main()
