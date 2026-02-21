from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image


def load_sources(directory: Path, source_files: list[str]) -> dict[str, Image.Image]:
    """Load source TGA images from the option directory."""
    sources: dict[str, Image.Image] = {}
    for filename in source_files:
        filepath = directory / filename
        if filepath.exists():
            try:
                sources[filename] = Image.open(filepath).convert("RGBA")
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
    return sources


def parse_rgb(value: list[int] | tuple[int, int, int] | None, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
    if value is None:
        return fallback
    if len(value) != 3:
        return fallback
    r, g, b = value
    return (
        int(max(0, min(255, r))),
        int(max(0, min(255, g))),
        int(max(0, min(255, b))),
    )


def tint_item_vertical(
    item_tile: Image.Image,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """Tint grayscale item by luminance with a top->bottom color ramp."""
    rgba = item_tile.convert("RGBA")
    r, g, b, a = rgba.split()
    lum = r.load()  # source atlas is grayscale, so R=G=B
    ap = a.load()
    w, h = rgba.size

    tr, tg, tb = top_color
    br, bg, bb = bottom_color

    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()

    for y in range(h):
        y_mix = y / max(1, h - 1)
        row_r = tr + (br - tr) * y_mix
        row_g = tg + (bg - tg) * y_mix
        row_b = tb + (bb - tb) * y_mix

        for x in range(w):
            alpha = ap[x, y]
            if alpha == 0:
                op[x, y] = (0, 0, 0, 0)
                continue

            t = lum[x, y] / 255.0
            rr = int(max(0, min(255, row_r * t)))
            gg = int(max(0, min(255, row_g * t)))
            bbv = int(max(0, min(255, row_b * t)))
            op[x, y] = (rr, gg, bbv, alpha)

    return out


def apply_item_gradient(
    item_tile: Image.Image,
    gradient_type: str,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """Apply item coloration before compositing onto button."""
    if gradient_type in ("none", "direct"):
        return item_tile.convert("RGBA")
    return tint_item_vertical(item_tile, top_color=top_color, bottom_color=bottom_color)


def extract_cell(img: Image.Image, row: int, col: int, cell_width: int, cell_height: int) -> Image.Image:
    """Extract a cell from a grid image. Indices are 0-based."""
    # For now, use standard grid extraction
    # Button grid may have custom spacing (2px separators), so coordinates come from config
    return img.crop((col * cell_width, row * cell_height, col * cell_width + cell_width, row * cell_height + cell_height))


def extract_button_cell(
    img: Image.Image,
    row: int,
    col: int,
    cell_size: int,
    sep_x: int,
    sep_y: int,
    origin_x: int,
    origin_y: int,
) -> Image.Image:
    """Extract button cell with separator-aware coordinates. Input indices are 0-based."""
    x = origin_x + col * (cell_size + sep_x)
    y = origin_y + row * (cell_size + sep_y)
    return img.crop((x, y, x + cell_size, y + cell_size))


def fit_item_to_button(
    item: Image.Image,
    cell_size: int,
    fit_size: int,
    offset_x: int,
    offset_y: int,
    fit_mode: str,
) -> Image.Image:
    """Scale item to fit_size and place on transparent cell with offsets.

    fit_mode:
      - "tile": scale the full source tile (no alpha cropping)
      - "visible": scale only visible alpha bounds
    """
    fit_size = max(1, min(cell_size, int(fit_size)))
    item_rgba = item.convert("RGBA")
    mode = str(fit_mode).strip().lower()

    canvas = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))

    if mode == "tile":
        fitted = item_rgba.resize((fit_size, fit_size), Image.LANCZOS)
        x = ((cell_size - fit_size) // 2) + int(offset_x)
        y = ((cell_size - fit_size) // 2) + int(offset_y)
        canvas.alpha_composite(fitted, (x, y))
        return canvas

    # Scale visible pixels (alpha bbox), not the entire tile including transparent padding.
    alpha = item_rgba.split()[3]
    bbox = alpha.getbbox()
    if bbox is None:
        return canvas

    visible = item_rgba.crop(bbox)
    src_w, src_h = visible.size
    if src_w <= 0 or src_h <= 0:
        return canvas

    scale = min(fit_size / src_w, fit_size / src_h)
    dst_w = max(1, int(round(src_w * scale)))
    dst_h = max(1, int(round(src_h * scale)))
    fitted = visible.resize((dst_w, dst_h), Image.LANCZOS)

    x = ((cell_size - dst_w) // 2) + int(offset_x)
    y = ((cell_size - dst_h) // 2) + int(offset_y)
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def composite_item_on_button(
    item_tile: Image.Image,
    button_tile: Image.Image,
    item_opacity: float,
    output_size: int = 40,
) -> Image.Image:
    """Composite an item onto a button base."""
    # Create output canvas
    result = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

    item_rgba = item_tile.convert("RGBA")
    ir, ig, ib, ia = item_rgba.split()
    ia = ia.point(lambda v: int(v * max(0.0, min(1.0, item_opacity))))
    item_rgba = Image.merge("RGBA", (ir, ig, ib, ia))

    # Composite button first, then item on top
    result.alpha_composite(button_tile, (0, 0))
    result.alpha_composite(item_rgba, (0, 0))

    return result


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python regen_slots.py <option_path>")
        print("Example: python regen_slots.py Options/Gold")
        sys.exit(1)

    option_path = Path(sys.argv[1])
    config_file = option_path / "config_slots.json"

    if not option_path.exists():
        raise FileNotFoundError(f"Option directory not found: {option_path}")
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    source_items = config.get("source_items", "thorne_item01.tga")
    source_buttons = config.get("source_buttons", "thorne_buttons01.tga")

    # Load source images
    sources = load_sources(option_path, [source_items, source_buttons])

    if source_items not in sources:
        raise FileNotFoundError(f"Missing {source_items} in {option_path}")
    if source_buttons not in sources:
        raise FileNotFoundError(f"Missing {source_buttons} in {option_path}")

    items_src = sources[source_items]
    buttons_src = sources[source_buttons]

    output_size = int(config.get("output_size", 256))
    cell_size = int(config.get("cell_size", 40))
    button_grid = config.get("button_grid", {})
    sep_x = int(button_grid.get("sep_x", 2))
    sep_y = int(button_grid.get("sep_y", 2))
    origin_x = int(button_grid.get("origin_x", 0))
    origin_y = int(button_grid.get("origin_y", 0))

    default_button = config.get("default_button", {})
    default_item = config.get("default_item", {})
    gradient_presets = config.get("gradient_presets", {})
    items_config = config.get("items", [])

    # Create output atlas
    output_atlas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

    # Process each item
    for item_entry in items_config:
        item_row = int(item_entry.get("item_row", 1)) - 1  # Convert to 0-based
        item_col = int(item_entry.get("item_col", 1)) - 1
        
        # Determine button placement
        button_row = int(item_entry.get("button_row", default_button.get("button_row", 1))) - 1
        button_col = int(item_entry.get("button_col", default_button.get("button_col", 1))) - 1
        
        # Get button and item tiles
        item_tile = extract_cell(items_src, item_row, item_col, cell_size, cell_size)
        button_tile = extract_button_cell(
            buttons_src,
            row=button_row,
            col=button_col,
            cell_size=cell_size,
            sep_x=sep_x,
            sep_y=sep_y,
            origin_x=origin_x,
            origin_y=origin_y,
        )

        # Item color treatment
        gradient_name = item_entry.get("gradient", default_button.get("gradient", "gold"))
        preset = gradient_presets.get(gradient_name, {}) if isinstance(gradient_presets, dict) else {}

        top_color = parse_rgb(
            item_entry.get("top_color", preset.get("top_color", default_button.get("top_color"))),
            fallback=(220, 200, 100),
        )
        bottom_color = parse_rgb(
            item_entry.get("bottom_color", preset.get("bottom_color", default_button.get("bottom_color"))),
            fallback=(180, 160, 80),
        )
        gradient_type = item_entry.get("gradient_type", preset.get("type", "vertical"))

        item_colored = apply_item_gradient(item_tile, gradient_type, top_color, bottom_color)

        # Fit/offset controls (defaults with per-item override)
        fit_from_item = "fit_size" in item_entry
        fit_mode_from_item = "fit_mode" in item_entry
        fit_size = int(item_entry.get("fit_size", default_item.get("fit_size", 36)))
        fit_mode = str(item_entry.get("fit_mode", default_item.get("fit_mode", "tile"))).strip().lower()
        offset_x = int(item_entry.get("offset_x", default_item.get("offset_x", 0)))
        offset_y = int(item_entry.get("offset_y", default_item.get("offset_y", -1)))
        item_opacity = float(item_entry.get("item_opacity", default_item.get("item_opacity", 0.92)))

        item_fitted = fit_item_to_button(
            item_colored,
            cell_size=cell_size,
            fit_size=fit_size,
            offset_x=offset_x,
            offset_y=offset_y,
            fit_mode=fit_mode,
        )

        # Composite item onto button
        composite = composite_item_on_button(
            item_tile=item_fitted,
            button_tile=button_tile,
            item_opacity=item_opacity,
            output_size=cell_size,
        )

        # Place on output atlas
        out_row = int(item_entry.get("out_row", 1)) - 1
        out_col = int(item_entry.get("out_col", 1)) - 1
        out_x = out_col * cell_size
        out_y = out_row * cell_size
        
        output_atlas.alpha_composite(composite, (out_x, out_y))
        
        item_name = item_entry.get("name", f"item_{out_row}_{out_col}")
        fit_source = "item" if fit_from_item else "default"
        fit_mode_source = "item" if fit_mode_from_item else "default"
        print(
            f"Composited {item_name:12s} @ ({out_x:3d},{out_y:3d}) "
            f"fit={fit_size:2d} ({fit_source}) mode={fit_mode} ({fit_mode_source})"
        )

    # Save output
    output_file = option_path / "thorne_slots01.tga"
    output_atlas.save(output_file, format="TGA")
    print(f"Created: {output_file}")
    print(f"Size: {output_atlas.size}")


if __name__ == "__main__":
    main()
