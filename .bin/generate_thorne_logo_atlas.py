"""generate_thorne_logo_atlas.py -- Generate lighting + transparency variants of the Thorne logo.

Reads the source logo from the atlas, applies a different lighting technique to each column
(source, flat, radial glow, top-light, radial+top combo, rim light), then applies transparency
levels across rows 2-6.

The result is a 6x6 grid (255x255 atlas) where:
  - Each column showcases a unique lighting style
  - Rows vary in transparency (100% → 50% opacity)

Configuration is read from .bin/generate_thorne_logo_atlas.json.

Usage:
  python .bin/generate_thorne_logo_atlas.py [--dry-run]

Output:
  .master/logo_atlas_thorne01.tga  (updated in-place)
"""

import json
import math
import sys
from collections import deque
from pathlib import Path

from PIL import Image


# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "generate_thorne_logo_atlas.json"
MASTER_DIR = SCRIPT_DIR.parent / ".master"


def load_config() -> dict:
    """Load configuration from JSON file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Missing config: {CONFIG_FILE}")
    with open(CONFIG_FILE) as f:
        return json.load(f)


def load_tga(filepath: Path) -> Image.Image:
    """Load TGA file as RGBA Image."""
    return Image.open(filepath).convert("RGBA")


def save_tga(image: Image.Image, filepath: Path) -> None:
    """Save PIL Image as TGA format (uncompressed, top-left origin, 32-bit BGRA)."""
    w, h = image.size

    header = bytearray(18)
    header[2] = 2  # Uncompressed true color
    header[12] = w & 0xFF
    header[13] = (w >> 8) & 0xFF
    header[14] = h & 0xFF
    header[15] = (h >> 8) & 0xFF
    header[16] = 32  # 32 bits per pixel (RGBA)
    header[17] = 0x20  # Origin top-left

    pixel_data = image.convert("RGBA").tobytes("raw", "BGRA")

    with open(filepath, "wb") as f:
        f.write(header)
        f.write(pixel_data)


def extract_cell(atlas: Image.Image, row: int, col: int, cell_size: int, spacing: int) -> Image.Image:
    """Extract a single cell from the atlas grid (1-based row/col)."""
    x = (col - 1) * (cell_size + spacing)
    y = (row - 1) * (cell_size + spacing)
    return atlas.crop((x, y, x + cell_size, y + cell_size))


def lighten_grayscale(source: Image.Image, target_gray: int) -> Image.Image:
    """Uniform brightness shift — classic flat lightening.

    Shifts all opaque pixel luminances by a fixed offset so the average
    brightness matches target_gray. Preserves relative contrast.
    """
    result = source.copy()
    pixels = result.load()
    w, h = result.size

    luminances: list[int] = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 0:
                luminances.append((r + g + b) // 3)

    if not luminances:
        return result

    src_mid = sum(luminances) / len(luminances)
    offset = target_gray - src_mid

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            lum = (r + g + b) // 3
            new_lum = int(max(0, min(255, lum + offset)))
            pixels[x, y] = (new_lum, new_lum, new_lum, a)

    return result


# ---------------------------------------------------------------------------
# Lighting engines
# ---------------------------------------------------------------------------

def _analyze_source(source: Image.Image) -> dict:
    """Pre-compute source metrics needed by lighting functions.

    Returns dict with: opaque_pixels, centroid, max_dist, edge_set, dist_map,
    max_inner_dist, src_mid.
    """
    w, h = source.size
    px = source.load()

    opaque: list[tuple[int, int, int, int]] = []  # (x, y, lum, alpha)
    opaque_set: set[tuple[int, int]] = set()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0:
                opaque.append((x, y, (r + g + b) // 3, a))
                opaque_set.add((x, y))

    if not opaque:
        return {"opaque": [], "centroid": (w / 2, h / 2), "max_dist": 1.0,
                "edge_set": set(), "dist_map": {}, "max_inner_dist": 1, "src_mid": 128.0}

    xs = [p[0] for p in opaque]
    ys = [p[1] for p in opaque]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)

    max_dist = max(math.sqrt((p[0] - cx) ** 2 + (p[1] - cy) ** 2) for p in opaque)
    max_dist = max(max_dist, 0.1)

    src_mid = sum(p[2] for p in opaque) / len(opaque)

    # Edge detection — pixels adjacent to transparent or image boundary
    edge_set: set[tuple[int, int]] = set()
    for (x, y) in opaque_set:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= w or ny < 0 or ny >= h or (nx, ny) not in opaque_set:
                edge_set.add((x, y))
                break

    # BFS distance from edge (for rim light)
    dist_map: dict[tuple[int, int], int] = {}
    q: deque[tuple[int, int]] = deque()
    for pos in edge_set:
        dist_map[pos] = 0
        q.append(pos)
    while q:
        cx2, cy2 = q.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            npos = (cx2 + dx, cy2 + dy)
            if npos not in dist_map and npos in opaque_set:
                dist_map[npos] = dist_map[(cx2, cy2)] + 1
                q.append(npos)

    max_inner = max(dist_map.values()) if dist_map else 1

    return {
        "opaque": opaque,
        "centroid": (cx, cy),
        "max_dist": max_dist,
        "edge_set": edge_set,
        "dist_map": dist_map,
        "max_inner_dist": max_inner,
        "src_mid": src_mid,
        "width": w,
        "height": h,
        "min_y": min(ys),
        "max_y": max(ys),
    }


def apply_lighting(source: Image.Image, col_cfg: dict, analysis: dict) -> Image.Image:
    """Apply a lighting technique to the source logo based on column config.

    Supported modes: source, flat, radial_glow, top_light, bottom_light, radial_top_bias, rim_light.
    """
    mode = col_cfg["mode"]

    if mode == "source":
        return source.copy()

    if mode == "flat":
        return lighten_grayscale(source, col_cfg["target_gray"])

    target = col_cfg.get("target_gray", 170)
    intensity = col_cfg.get("intensity", 0.85)
    falloff = col_cfg.get("falloff", 1.0)
    cx, cy = analysis["centroid"]
    max_dist = analysis["max_dist"]
    min_y = analysis["min_y"]
    max_y = analysis["max_y"]
    y_span = max(max_y - min_y, 1)

    result = source.copy()
    pixels = result.load()
    w, h = result.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            lum = (r + g + b) // 3

            if mode == "radial_glow":
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                t = 1.0 - (d / max_dist)
                t = max(0.0, min(1.0, t)) ** falloff
                new_lum = lum + (target - lum) * t * intensity

            elif mode == "top_light":
                t = 1.0 - (y - min_y) / y_span
                t = max(0.0, min(1.0, t)) ** falloff
                new_lum = lum + (target - lum) * t * intensity

            elif mode == "bottom_light":
                t = (y - min_y) / y_span
                t = max(0.0, min(1.0, t)) ** falloff
                new_lum = lum + (target - lum) * t * intensity

            elif mode == "radial_top_bias":
                radial_weight = col_cfg.get("radial_weight", 0.65)
                top_weight = 1.0 - radial_weight
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                rt = max(0.0, min(1.0, 1.0 - d / max_dist)) ** falloff
                tt = max(0.0, min(1.0, 1.0 - (y - min_y) / y_span))
                t = rt * radial_weight + tt * top_weight
                new_lum = lum + (target - lum) * t * intensity

            elif mode == "rim_light":
                dist = analysis["dist_map"].get((x, y), 0)
                max_inner = analysis["max_inner_dist"]
                t = 1.0 - (dist / max(max_inner, 1))
                new_lum = lum + (target - lum) * t * intensity

            else:
                raise ValueError(f"Unknown lighting mode: {mode}")

            clamped = int(max(0, min(255, new_lum)))
            pixels[x, y] = (clamped, clamped, clamped, a)

    return result


def apply_transparency(source: Image.Image, target_alpha: int) -> Image.Image:
    """Reduce alpha of all opaque pixels to target_alpha, preserving colors.

    Args:
        source: RGBA source image.
        target_alpha: Target alpha value (0-255) for opaque pixels.

    Returns:
        New RGBA image with reduced alpha on previously-opaque pixels.
    """
    result = source.copy()
    pixels = result.load()
    w, h = result.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            # Scale alpha proportionally (handles partially-transparent source pixels)
            new_alpha = int(a * target_alpha / 255)
            pixels[x, y] = (r, g, b, new_alpha)

    return result


def gold_tint(source: Image.Image, r_mul: float, g_mul: float, b_mul: float) -> Image.Image:
    """Apply warm gold/bronze tint to a grayscale image.

    Multiplies each channel independently to shift gray toward gold. Matches
    the muted bronze aesthetic of original EQ tab icons in window_pieces01.tga.
    """
    result = source.copy()
    pixels = result.load()
    w, h = result.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            v = r  # grayscale — R == G == B
            pixels[x, y] = (
                min(255, int(v * r_mul)),
                min(255, int(v * g_mul)),
                min(255, int(v * b_mul)),
                a,
            )

    return result


def generate_icons(row1_variants: list[Image.Image], config: dict) -> None:
    """Generate 18x18 tab icon atlas from Row 1 lighting variants.

    Creates a small atlas with two rows:
      - Row 1 (Y=0): Normal gray icons (shifted up)
      - Row 2 (Y=icon_size+spacing): Gold-tinted icons (shifted up)

    Output is saved to thorne_drak/ root for direct use by the EQ client.
    """
    icons_cfg = config.get("icons")
    if not icons_cfg or not icons_cfg.get("enabled", False):
        print("\n  Icon generation: disabled")
        return

    icon_size = icons_cfg["icon_size"]
    icon_spacing = icons_cfg["icon_spacing"]
    atlas_w = icons_cfg["atlas_width"]
    atlas_h = icons_cfg["atlas_height"]
    shift_up = icons_cfg["shift_up"]
    gold_cfg = icons_cfg["gold_tint"]
    r_mul = gold_cfg["r_multiplier"]
    g_mul = gold_cfg["g_multiplier"]
    b_mul = gold_cfg["b_multiplier"]

    output_path = SCRIPT_DIR.parent / "thorne_drak" / icons_cfg["output_file"]
    cols = len(row1_variants)

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))

    print(f"\nIcon atlas ({atlas_w}x{atlas_h}, {icon_size}px icons, shift_up={shift_up}):")

    for c, variant in enumerate(row1_variants):
        # Downscale 40→18 with high-quality filter
        icon = variant.resize((icon_size, icon_size), Image.LANCZOS)

        # Shift up to remove faint top rows
        shifted = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        shifted.paste(icon, (0, -shift_up))

        dx = c * (icon_size + icon_spacing)

        # Row 1: normal gray
        atlas.paste(shifted, (dx, 0))

        # Row 2: gold tinted
        gold = gold_tint(shifted, r_mul, g_mul, b_mul)
        atlas.paste(gold, (dx, icon_size + icon_spacing))

        pix = shifted.load()
        opaque = sum(
            1 for x in range(icon_size) for y in range(icon_size)
            if pix[x, y][3] > 0
        )
        print(f"  Col {c + 1}: {opaque}px  normal@({dx},0)  gold@({dx},{icon_size + icon_spacing})")

    save_tga(atlas, output_path)
    print(f"  Saved: {output_path}")


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    config = load_config()

    # Extract settings
    grid = config["grid"]
    cell_size = grid["cell_size"]
    spacing = grid["spacing"]
    num_cols = grid["cols"]
    num_rows = grid["rows"]
    atlas_size = grid["atlas_size"]

    source_cfg = config["source"]
    source_file = MASTER_DIR / source_cfg["file"]
    source_row = source_cfg["row"]
    source_col = source_cfg["col"]

    columns = config["lighting_columns"]["columns"]
    alpha_values = config["transparency_rows"]["alpha_values"]

    output_file = MASTER_DIR / config["output"]["file"]

    # Validate
    if not source_file.exists():
        raise FileNotFoundError(f"Missing source: {source_file}")
    if len(columns) != num_cols:
        raise ValueError(f"lighting_columns has {len(columns)} entries, need {num_cols}")
    if len(alpha_values) != num_rows:
        raise ValueError(f"transparency_rows has {len(alpha_values)} entries, need {num_rows}")

    # Load source atlas and extract the source logo cell
    atlas = load_tga(source_file)
    source_logo = extract_cell(atlas, source_row, source_col, cell_size, spacing)

    # Count opaque pixels for info
    opaque_count = sum(
        1 for y in range(cell_size) for x in range(cell_size)
        if source_logo.getpixel((x, y))[3] > 0
    )
    print(f"Source logo: {source_file.name} row={source_row} col={source_col}")
    print(f"  Size: {cell_size}x{cell_size}, {opaque_count} opaque pixels")

    # Pre-compute source analysis (shared by all lighting modes)
    analysis = _analyze_source(source_logo)
    print(f"  Centroid: ({analysis['centroid'][0]:.1f}, {analysis['centroid'][1]:.1f})")
    print(f"  Edge pixels: {len(analysis['edge_set'])}, max inner dist: {analysis['max_inner_dist']}px")

    # Generate row 1: one lighting variant per column
    row1_variants: list[Image.Image] = []
    print()
    for col_idx, col_cfg in enumerate(columns):
        mode = col_cfg["mode"]
        variant = apply_lighting(source_logo, col_cfg, analysis)
        row1_variants.append(variant)

        # Build label
        if mode == "source":
            label = "source (original)"
        elif mode == "flat":
            label = f"flat (gray={col_cfg['target_gray']})"
        else:
            parts = [f"gray={col_cfg.get('target_gray', '?')}"]
            if "intensity" in col_cfg:
                parts.append(f"int={col_cfg['intensity']}")
            if "falloff" in col_cfg:
                parts.append(f"fall={col_cfg['falloff']}")
            if "radial_weight" in col_cfg:
                parts.append(f"rw={col_cfg['radial_weight']}")
            label = f"{mode} ({', '.join(parts)})"

        print(f"  Col {col_idx + 1}: {label}")

    print()

    # Build full atlas
    new_atlas = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))

    for row_idx in range(num_rows):
        alpha = alpha_values[row_idx]
        y_pos = row_idx * (cell_size + spacing)

        for col_idx in range(num_cols):
            x_pos = col_idx * (cell_size + spacing)
            base = row1_variants[col_idx]

            if alpha >= 255:
                cell = base.copy()
            else:
                cell = apply_transparency(base, alpha)

            new_atlas.paste(cell, (x_pos, y_pos))

        alpha_pct = round(alpha / 255 * 100)
        print(f"  Row {row_idx + 1} @ y={y_pos}: {alpha_pct}% opacity (A={alpha})")

    if dry_run:
        print(f"\n[DRY RUN] Would write: {output_file}")
        print(f"Atlas: {atlas_size}x{atlas_size}, {num_cols}x{num_rows} grid")
        return

    save_tga(new_atlas, output_file)

    col_modes = [c["mode"] for c in columns]
    print(f"\nUpdated: {output_file}")
    print(f"Logo atlas layout ({atlas_size}x{atlas_size}):")
    print(f"  Columns: {' | '.join(col_modes)}")
    print(f"  Rows: {num_rows} transparency levels (100% → 50%)")
    print(f"  Grid: {cell_size}px cells, {spacing}px gaps")

    # --- Icon atlas generation ---
    generate_icons(row1_variants, config)


if __name__ == "__main__":
    main()
