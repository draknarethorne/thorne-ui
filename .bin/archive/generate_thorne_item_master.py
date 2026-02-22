"""generate_thorne_item_master.py -- Generate item icon atlas for Options/Slots/.Master.

Reads dragitem source TGA files and thorne_item01.json config from .Master/, then composites
them into a grayscale item icon atlas. The output (thorne_item01.tga) is the source file
consumed by regen_slots.py to generate the finished slot textures for each variant.

Run this after editing source dragitem*.tga files or updating thorne_item01.json.

Usage:
  python .bin/generate_thorne_item_master.py

Inputs:
  Options/Slots/.Master/thorne_item01.json   -- Item grid layout config
  Options/Slots/.Master/dragitem*.tga         -- Individual item source icons

Output:
  Options/Slots/.Master/thorne_item01.tga    -- Composited item atlas (source for regen_slots.py)
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


MASTER_DIR = Path(__file__).resolve().parent.parent / "thorne_drak" / "Options" / "Slots" / ".Master"
CONFIG_PATH = MASTER_DIR / "thorne_item01.json"


def to_grayscale_rgba(img: Image.Image, contrast: float, brightness: float) -> Image.Image:
    """Convert image to grayscale while preserving alpha, with tone controls."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))

    gray = ImageEnhance.Contrast(gray).enhance(contrast)
    gray = ImageEnhance.Brightness(gray).enhance(brightness)

    return Image.merge("RGBA", (gray, gray, gray, a))


def to_inverted_grayscale_rgba(img: Image.Image, contrast: float, brightness: float) -> Image.Image:
    """Invert source, then grayscale and apply tone controls (keeps alpha)."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))
    inverted = ImageOps.invert(rgb)
    gray = ImageOps.grayscale(inverted)

    gray = ImageEnhance.Contrast(gray).enhance(contrast)
    gray = ImageEnhance.Brightness(gray).enhance(brightness)

    return Image.merge("RGBA", (gray, gray, gray, a))


def to_inverted_impression_rgba(
    img: Image.Image,
    mid_tone: int = 128,
    contrast: float = 0.6,
    depth_gradient: bool = True,
) -> Image.Image:
    """Match slots_variants inverted-impression logic for darker emboss base."""
    rgba = img.convert("RGBA")
    rgb = rgba.convert("RGB")
    alpha = rgba.split()[3]

    gray = ImageOps.grayscale(rgb)
    inverted = ImageOps.invert(gray)

    inv_array = inverted.load()
    w, h = inverted.size

    out = Image.new("RGBA", (w, h))
    op = out.load()
    ap = alpha.load()

    for y in range(h):
        for x in range(w):
            a = ap[x, y]
            if a > 0:
                norm = inv_array[x, y] / 255.0
                val = mid_tone + (norm - 0.5) * contrast * 255

                if depth_gradient:
                    y_norm = y / (h - 1) if h > 1 else 0.5
                    gradient = 1.0 - 4 * (y_norm - 0.5) ** 2
                    gradient_mult = 0.85 + gradient * 0.15
                    val *= gradient_mult

                val = int(max(0, min(255, val)))
                op[x, y] = (val, val, val, a)
            else:
                op[x, y] = (0, 0, 0, 0)

    return out


def load_sources(master_dir: Path) -> dict[str, Image.Image]:
    sources: dict[str, Image.Image] = {}
    for path in master_dir.glob("*.tga"):
        try:
            sources[path.name] = Image.open(path).convert("RGBA")
        except Exception:
            continue
    return sources


def extract_cell(img: Image.Image, row: int, col: int, cell_size: int) -> Image.Image:
    """Extract a cell from a grid image. Indices are 0-based."""
    x = col * cell_size
    y = row * cell_size
    return img.crop((x, y, x + cell_size, y + cell_size))


def render_item(entry: dict, sources: dict[str, Image.Image], source_cell_size: int, output_cell_size: int, default_tone: dict) -> Image.Image:
    mode = entry.get("mode", "grayscale")
    if mode == "empty":
        return Image.new("RGBA", (output_cell_size, output_cell_size), (0, 0, 0, 0))

    source_file = entry.get("source_file")
    source_mode = entry.get("source_mode", "grid")
    src_row = int(entry.get("src_row", 1)) - 1  # Convert 1-based to 0-based
    src_col = int(entry.get("src_col", 1)) - 1  # Convert 1-based to 0-based

    if not source_file or source_file not in sources:
        raise FileNotFoundError(f"Missing source file in .Master: {source_file}")

    src_img = sources[source_file]

    if source_mode == "full":
        tile = src_img.resize((source_cell_size, source_cell_size), Image.LANCZOS)
    else:
        tile = extract_cell(src_img, src_row, src_col, source_cell_size)

    tone = entry.get("tone", {})
    contrast = float(tone.get("contrast", default_tone.get("contrast", 1.10)))
    brightness = float(tone.get("brightness", default_tone.get("brightness", 0.95)))

    if mode == "direct":
        result = tile.convert("RGBA")
    elif mode == "invert_grayscale":
        result = to_inverted_grayscale_rgba(tile, contrast=contrast, brightness=brightness)
    elif mode == "invert_impression":
        mid_tone = int(entry.get("mid_tone", 128))
        imp_contrast = float(entry.get("imp_contrast", 0.6))
        depth_gradient = bool(entry.get("depth_gradient", True))
        result = to_inverted_impression_rgba(
            tile,
            mid_tone=mid_tone,
            contrast=imp_contrast,
            depth_gradient=depth_gradient,
        )
    else:
        result = to_grayscale_rgba(tile, contrast=contrast, brightness=brightness)

    # Scale to output cell size if different from source
    if output_cell_size != source_cell_size:
        result = result.resize((output_cell_size, output_cell_size), Image.LANCZOS)

    return result


def generate_atlas(
    items: list,
    sources: dict,
    source_cell_size: int,
    output_cell_size: int,
    output_size: int,
    default_tone: dict,
) -> Image.Image:
    """Generate a single atlas with the given cell and output sizes."""
    atlas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

    for entry in items:
        out_row = int(entry.get("out_row", 1)) - 1  # Convert 1-based to 0-based
        out_col = int(entry.get("out_col", 1)) - 1  # Convert 1-based to 0-based
        name = entry.get("name", "(unnamed)")

        tile = render_item(entry, sources, source_cell_size, output_cell_size, default_tone)
        x = out_col * output_cell_size
        y = out_row * output_cell_size
        atlas.alpha_composite(tile, (x, y))

        print(f"Placed {name:12s} @ ({x:3d},{y:3d})")

    return atlas


def main() -> None:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Base configuration
    base_cell_size = int(config.get("cell_size", 40))
    base_output_size = int(config.get("output_size", 256))
    default_tone = config.get("default_tone", {"contrast": 1.10, "brightness": 0.95})
    items = config.get("items", [])
    variants = config.get("variants", [])

    sources = load_sources(MASTER_DIR)

    if not items:
        raise ValueError("Config has no items to render.")

    # Generate base atlas (thorne_item01.tga)
    print("Generating base atlas (item)...")
    atlas = generate_atlas(items, sources, base_cell_size, base_cell_size, base_output_size, default_tone)
    out_base = MASTER_DIR / "thorne_item01.tga"
    out_base.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(out_base, format="TGA")
    print(f"Created: {out_base}")
    print(f"Size: {atlas.size}\n")

    # Generate variant atlases
    for variant in variants:
        variant_name = variant.get("name", "variant")
        variant_cell_size = int(variant.get("cell_size", base_cell_size))
        variant_output_size = int(variant.get("output_size", base_output_size))

        print(f"Generating variant '{variant_name}'...")
        variant_atlas = generate_atlas(items, sources, base_cell_size, variant_cell_size, variant_output_size, default_tone)
        out_variant = MASTER_DIR / f"thorne_{variant_name}01.tga"
        variant_atlas.save(out_variant, format="TGA")
        print(f"Created: {out_variant}")
        print(f"Size: {variant_atlas.size}\n")



if __name__ == "__main__":
    main()
