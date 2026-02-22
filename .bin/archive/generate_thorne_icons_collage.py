"""generate_thorne_icons_collage.py -- EXPERIMENTAL / LEGACY

Early exploration script for sampling icon visual treatments (dark-transparent vs
clear-transparent) across multiple sizes. References source files that no longer
exist (thorne_drak01.jpg, thorne_drak01.tga in thorne_drak root).

Do NOT run this script. It is retained as a reference for the background-removal
and sizing logic explored during early icon pipeline development.

The active pipeline for icon atlases is:
  - generate_thorne_icons_master.py  -- Produces .Master/thorne_icons01.tga
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


ATLAS_SIZE = 255
FIT_SIZE = 250
PADDING = 0
BORDER = 1
GAP = 1

# Paired sizes requested by user
SAMPLE_SIZES = [100, 80, 40, 20]

# Background detection thresholds (same family used for prior cleanup pass)
L_LOW, L_HIGH = 165.0, 245.0
S_MAX = 55.0

# Border colors (no text labels inside EQ textures, so color-coded frames)
DARK_BORDER = (70, 170, 255, 220)   # blue-ish = dark-transparent background variant
CLEAR_BORDER = (255, 170, 80, 220)  # amber = fully-transparent background variant


@dataclass
class Entry:
    name: str
    variant: str
    size: int
    image: Image.Image


def build_clear_variant(jpg: Image.Image) -> Image.Image:
    """Create a fully-transparent background variant from the original JPG.

    The foreground remains opaque while background/fringe transitions alpha to 0.
    """
    w, h = jpg.size
    out = Image.new("RGBA", (w, h))

    src = jpg.load()
    dst = out.load()

    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]

            cmax = max(r, g, b)
            cmin = min(r, g, b)
            sat = float(cmax - cmin)
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b

            # Same soft mask idea: high luminance + low saturation => background/fringe
            if sat <= S_MAX and lum >= L_LOW:
                t = (lum - L_LOW) / (L_HIGH - L_LOW)
                if t < 0.0:
                    t = 0.0
                elif t > 1.0:
                    t = 1.0
                bg_amt = t * t * (3.0 - 2.0 * t)  # smoothstep

                # Keep color, reduce alpha toward fully transparent for background
                a = int(round((1.0 - bg_amt) * 255.0))
                dst[x, y] = (r, g, b, a)
            else:
                dst[x, y] = (r, g, b, 255)

    return out


def normalize_to_255(image: Image.Image) -> Image.Image:
    """Fit image content into a 250x250 box on a 255x255 transparent canvas."""
    src = image.convert("RGBA")
    alpha = src.split()[3]
    bbox = alpha.getbbox()
    if bbox is None:
        raise RuntimeError("Cannot normalize image with empty alpha bounds")

    cropped = src.crop(bbox)
    cw, ch = cropped.size
    scale = min(FIT_SIZE / cw, FIT_SIZE / ch)
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))
    resized = cropped.resize((nw, nh), Image.LANCZOS)

    canvas = Image.new("RGBA", (ATLAS_SIZE, ATLAS_SIZE), (0, 0, 0, 0))
    ox = (ATLAS_SIZE - nw) // 2
    oy = (ATLAS_SIZE - nh) // 2
    canvas.alpha_composite(resized, (ox, oy))
    return canvas


def make_entries(dark_source: Image.Image, clear_source: Image.Image) -> dict[int, tuple[Entry, Entry]]:
    pairs: dict[int, tuple[Entry, Entry]] = {}
    for size in SAMPLE_SIZES:
        dark_img = dark_source.resize((size, size), Image.LANCZOS)
        clear_img = clear_source.resize((size, size), Image.LANCZOS)
        dark_e = Entry(name=f"dark_{size}", variant="dark", size=size, image=dark_img)
        clear_e = Entry(name=f"clear_{size}", variant="clear", size=size, image=clear_img)
        pairs[size] = (dark_e, clear_e)
    return pairs


def tile_dims(size: int) -> tuple[int, int]:
    d = size + (PADDING * 2) + (BORDER * 2)
    return d, d


def place_entries(pairs: dict[int, tuple[Entry, Entry]]) -> list[tuple[Entry, int, int]]:
    """Place dark/clear pairs by size in columns so each pair stays together."""
    placed: list[tuple[Entry, int, int]] = []

    x = 1
    for size in SAMPLE_SIZES:
        dark_e, clear_e = pairs[size]
        tw, th = tile_dims(size)

        y_dark = 1
        y_clear = y_dark + th + GAP

        if x + tw > ATLAS_SIZE - 1:
            raise RuntimeError(f"Atlas overflow horizontally at size {size}")
        if y_clear + th > ATLAS_SIZE - 1:
            raise RuntimeError(f"Atlas overflow vertically at size {size}")

        placed.append((dark_e, x, y_dark))
        placed.append((clear_e, x, y_clear))

        x += tw + GAP

    return placed


def render_atlas(placed: list[tuple[Entry, int, int]], out_path: Path) -> None:
    atlas = Image.new("RGBA", (ATLAS_SIZE, ATLAS_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)

    # Outer frame to define texture boundary in editors
    draw.rectangle(
        [(0, 0), (ATLAS_SIZE - 1, ATLAS_SIZE - 1)],
        outline=(255, 255, 255, 64),
        width=1,
    )

    for entry, x, y in placed:
        tw, th = tile_dims(entry.size)
        x2 = x + tw - 1
        y2 = y + th - 1

        border_color = DARK_BORDER if entry.variant == "dark" else CLEAR_BORDER

        # Tile border so each sample is easy to distinguish
        draw.rectangle([(x, y), (x2, y2)], outline=border_color, width=BORDER)

        # Paste centered icon inside tile
        px = x + BORDER + PADDING
        py = y + BORDER + PADDING
        atlas.alpha_composite(entry.image, (px, py))

    atlas.save(out_path, format="TGA")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src_jpg = root / "thorne_drak" / "thorne_drak01.jpg"
    src_dark_tga = root / "thorne_drak" / "thorne_drak01.tga"
    out_tga = root / "thorne_drak" / "thorne_icons01.tga"

    if not src_jpg.exists():
        raise FileNotFoundError(f"Missing source JPG: {src_jpg}")
    if not src_dark_tga.exists():
        raise FileNotFoundError(f"Missing source normalized TGA: {src_dark_tga}")

    jpg = Image.open(src_jpg).convert("RGB")
    dark = Image.open(src_dark_tga).convert("RGBA")
    clear = normalize_to_255(build_clear_variant(jpg))

    entries = make_entries(dark_source=dark, clear_source=clear)
    placed = place_entries(entries)
    render_atlas(placed, out_tga)

    print(f"Created atlas: {out_tga}")
    print(f"Size: {ATLAS_SIZE}x{ATLAS_SIZE}")
    print("Included samples:")
    for e, x, y in placed:
        print(f"  - {e.name:9s} @ ({x:3d},{y:3d})")


if __name__ == "__main__":
    main()
