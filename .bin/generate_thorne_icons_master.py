from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path("C:/Thorne-UI")
SOURCE_ICON_FILE = ROOT / "thorne_drak" / "thorne_icon.tga"
OUT_MASTER = ROOT / "thorne_drak" / "thorne_icons01.tga"

ATLAS_SIZE = 255
ICON_X, ICON_Y = 2, 2

# Layout: one master row with 4x 40px icons + 4x 20px icons
GAP = 2
ICON40_SIZE = 40
ICON20_SIZE = 20

# 40px copies on top row
X40_START = 0
X40_COUNT = 4
Y40 = 0

# 20px copies continue on same top row
# 4x40 + 3 gaps = 166, then 2px group gap -> 168
X20_START = 168
X20_COUNT = 4
Y20 = 0

# Small-icon sharpening tuning (20x20 only)
SMALL_UNSHARP_RADIUS = 0.9
SMALL_UNSHARP_PERCENT = 260
SMALL_UNSHARP_THRESHOLD = 1
SMALL_ALPHA_CONTRAST = 1.12


def load_icon_40(icon_source: Image.Image, x: int, y: int) -> Image.Image:
    """Extract and prepare 40x40 icon from source file."""
    icon = icon_source.crop((x, y, x + ICON40_SIZE, y + ICON40_SIZE)).convert("RGBA")

    # Keep same sharpening logic used in slot generator
    rgb = icon.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.0, percent=220, threshold=2))
    a = ImageEnhance.Contrast(icon.split()[3]).enhance(1.25)
    return Image.merge("RGBA", (*rgb.split(), a))


def make_20_from_40(img40: Image.Image) -> Image.Image:
    """Create 20x20 icon using current slot-variant scaling logic."""
    img20 = img40.resize((ICON20_SIZE, ICON20_SIZE), Image.LANCZOS)
    img20 = img20.filter(
        ImageFilter.UnsharpMask(
            radius=SMALL_UNSHARP_RADIUS,
            percent=SMALL_UNSHARP_PERCENT,
            threshold=SMALL_UNSHARP_THRESHOLD,
        )
    )

    # Tighten alpha edges slightly so mini-icons read cleaner at 20x20
    r, g, b, a = img20.split()
    a = ImageEnhance.Contrast(a).enhance(SMALL_ALPHA_CONTRAST)
    return Image.merge("RGBA", (r, g, b, a))


def main() -> None:
    if not SOURCE_ICON_FILE.exists():
        raise FileNotFoundError(f"Missing source icon: {SOURCE_ICON_FILE}")

    icon_source = Image.open(SOURCE_ICON_FILE).convert("RGBA")
    icon40 = load_icon_40(icon_source, ICON_X, ICON_Y)
    icon20 = make_20_from_40(icon40)

    atlas = Image.new("RGBA", (ATLAS_SIZE, ATLAS_SIZE), (0, 0, 0, 0))

    placements: list[tuple[str, int, int, int]] = []

    # Place four 40x40 copies
    for i in range(X40_COUNT):
        x = X40_START + i * (ICON40_SIZE + GAP)
        atlas.alpha_composite(icon40, (x, Y40))
        placements.append((f"icon40_{i+1}", x, Y40, ICON40_SIZE))

    # Place four 20x20 copies
    for i in range(X20_COUNT):
        x = X20_START + i * (ICON20_SIZE + GAP)
        atlas.alpha_composite(icon20, (x, Y20))
        placements.append((f"icon20_{i+1}", x, Y20, ICON20_SIZE))

    atlas.save(OUT_MASTER, format="TGA")

    print(f"Created master icon atlas: {OUT_MASTER}")
    print(f"Size: {ATLAS_SIZE}x{ATLAS_SIZE}")
    print("Top-row placements:")
    for name, x, y, size in placements:
        print(f"  {name:10s} @ ({x:3d},{y:3d}) size {size}x{size}")


if __name__ == "__main__":
    main()
