"""regen_slots.py -- Generate slot item textures from source button and item atlases.

Composites item icons onto button backgrounds to produce themed inventory and equipment
slot textures for each variant in Options/Slots/.

Config is split across two files:
  .bin/regen_slots.json              -- Master layout: which dragitem maps to which output slot.
                                        Shared across ALL variants. Do not add colors here.
  <variant>/.regen_slots.json        -- Variant styling: gradient_presets, default_button,
                                        default_item, button_grid, item_overrides.

Each variant directory must also contain:
  <source_items>      -- Item icon atlas (default: thorne_item01.tga, copied from .Master/)
  <source_buttons>    -- Button background atlas (default: thorne_buttons01.tga, copied from .Master/)

Usage:
  python regen_slots.py --all                  # Auto-discover all configured variants
  python regen_slots.py Gold                   # Single variant
  python regen_slots.py Gold Silver Metal      # Multiple variants
  python regen_slots.py --help                 # Show help

Output (per variant):
  item_slots_thorne01.tga      -- Composited slot texture atlas
  .regen_slots-stats.json      -- Processing statistics
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

CONFIG_FILENAME = ".regen_slots.json"
MASTER_CONFIG_PATH = Path(__file__).resolve().parent / "regen_slots.json"
OUTPUT_FILENAME = "item_slots_thorne01.tga"
STATS_FILENAME = ".regen_slots-stats.json"


# ---------------------------------------------------------------------------
# Image utility functions
# ---------------------------------------------------------------------------

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


def tint_item_gradient(
    item_tile: Image.Image,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
    middle_color: tuple[int, int, int] | None = None,
    direction: str = "vertical",
) -> Image.Image:
    """Tint grayscale item by luminance with a color ramp.

    direction:
      "vertical"     -- top to bottom (default)
      "horizontal"   -- left to right
      "diagonal_tl"  -- top-left to bottom-right
      "diagonal_tr"  -- top-right to bottom-left

    middle_color:
      Optional midpoint color for 3-stop gradients (e.g., red/white/blue).
      When set, the gradient interpolates top->middle over the first half
      and middle->bottom over the second half.
    """
    rgba = item_tile.convert("RGBA")
    r_ch, _, _, a_ch = rgba.split()
    lum = r_ch.load()   # source atlas is grayscale, R=G=B
    ap = a_ch.load()
    w, h = rgba.size
    direction = (direction or "vertical").strip().lower()

    tr, tg, tb = top_color
    br, bg, bb = bottom_color
    has_mid = middle_color is not None
    mr, mg, mb = middle_color if has_mid else (0, 0, 0)

    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()

    for y in range(h):
        for x in range(w):
            alpha = ap[x, y]
            if alpha == 0:
                op[x, y] = (0, 0, 0, 0)
                continue

            # Gradient position t in [0.0, 1.0] based on direction
            if direction == "horizontal":
                t = x / max(1, w - 1)
            elif direction == "diagonal_tl":
                t = (x / max(1, w - 1) + y / max(1, h - 1)) / 2.0
            elif direction == "diagonal_tr":
                t = ((w - 1 - x) / max(1, w - 1) + y / max(1, h - 1)) / 2.0
            else:  # vertical (default)
                t = y / max(1, h - 1)

            if has_mid:
                if t < 0.5:
                    s = t * 2.0
                    row_r = tr + (mr - tr) * s
                    row_g = tg + (mg - tg) * s
                    row_b = tb + (mb - tb) * s
                else:
                    s = (t - 0.5) * 2.0
                    row_r = mr + (br - mr) * s
                    row_g = mg + (bg - mg) * s
                    row_b = mb + (bb - mb) * s
            else:
                row_r = tr + (br - tr) * t
                row_g = tg + (bg - tg) * t
                row_b = tb + (bb - tb) * t

            lum_t = lum[x, y] / 255.0
            op[x, y] = (
                int(max(0, min(255, row_r * lum_t))),
                int(max(0, min(255, row_g * lum_t))),
                int(max(0, min(255, row_b * lum_t))),
                alpha,
            )

    return out


def apply_item_gradient(
    item_tile: Image.Image,
    gradient_type: str,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
    middle_color: tuple[int, int, int] | None = None,
) -> Image.Image:
    """Apply item coloration before compositing onto button."""
    if gradient_type in ("none", "direct"):
        return item_tile.convert("RGBA")
    return tint_item_gradient(
        item_tile,
        top_color=top_color,
        bottom_color=bottom_color,
        middle_color=middle_color,
        direction=gradient_type,
    )


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


# ---------------------------------------------------------------------------
# SlotGenerator class
# ---------------------------------------------------------------------------

class SlotGenerator:
    """Composites item icons onto button backgrounds for one slot variant."""

    def __init__(self, variant_dir: Path) -> None:
        self.variant_dir = variant_dir
        self.variant_name = variant_dir.name
        self.config_file = variant_dir / CONFIG_FILENAME
        self.stats: dict = {
            "variant": self.variant_name,
            "summary": {
                "items_total": 0,
                "items_with_overrides": 0,
                "source_files": {},
            },
            "items": [],
            "output_file": None,
            "errors": [],
        }

    def generate(self) -> bool:
        """Run the full compositing pipeline. Returns True on success."""
        print(f"\n{'='*70}")
        print(f"GENERATING SLOTS: {self.variant_name}")
        print(f"{'='*70}")

        # Load master layout config (.bin/regen_slots.json)
        if not MASTER_CONFIG_PATH.exists():
            print(f"  ERROR: Master config not found: {MASTER_CONFIG_PATH}")
            return False
        with open(MASTER_CONFIG_PATH, "r", encoding="utf-8") as f:
            master_config = json.load(f)

        # Load variant styling config (<variant>/.regen_slots.json)
        if not self.config_file.exists():
            print(f"  ERROR: Variant config not found: {self.config_file}")
            return False
        with open(self.config_file, "r", encoding="utf-8") as f:
            variant_config = json.load(f)

        # Source files: master defines defaults, variant can override
        source_items = variant_config.get("source_items", master_config.get("source_items", "thorne_item01.tga"))
        source_buttons = variant_config.get("source_buttons", master_config.get("source_buttons", "thorne_buttons01.tga"))

        # Fallback: if source file not in variant dir, look in .Master/
        master_dir = self.variant_dir.parent / ".Master"

        def _resolve_source(filename: str) -> tuple[Image.Image | None, str]:
            """Load a source TGA, falling back to .Master/ if not in variant dir."""
            p = self.variant_dir / filename
            if p.exists():
                try:
                    return Image.open(p).convert("RGBA"), "variant"
                except Exception as e:
                    print(f"  Warning: Could not load {p}: {e}")
            p2 = master_dir / filename
            if p2.exists():
                try:
                    img = Image.open(p2).convert("RGBA")
                    print(f"  Info: {filename} not in variant dir — loaded from .Master/")
                    return img, "master"
                except Exception as e:
                    print(f"  Warning: Could not load {p2}: {e}")
            return None, "missing"

        items_img, items_loc = _resolve_source(source_items)
        buttons_img, buttons_loc = _resolve_source(source_buttons)

        if items_img is None:
            print(f"  ERROR: {source_items} not found in variant dir or .Master/")
            return False
        if buttons_img is None:
            print(f"  ERROR: {source_buttons} not found in variant dir or .Master/")
            return False

        items_src = items_img
        buttons_src = buttons_img
        self.stats["summary"]["source_files"] = {
            source_items: items_loc,
            source_buttons: buttons_loc,
        }

        # Layout dimensions from master; variant can override if needed
        output_size = int(variant_config.get("output_size", master_config.get("output_size", 256)))
        cell_size = int(variant_config.get("cell_size", master_config.get("cell_size", 40)))
        button_grid = variant_config.get("button_grid", {})
        sep_x = int(button_grid.get("sep_x", 2))
        sep_y = int(button_grid.get("sep_y", 2))
        origin_x = int(button_grid.get("origin_x", 0))
        origin_y = int(button_grid.get("origin_y", 0))

        default_button = variant_config.get("default_button", {})
        default_item = variant_config.get("default_item", {})

        # Merge gradient_presets: master provides the base palette, variant can add/override
        gradient_presets: dict = {
            **master_config.get("gradient_presets", {}),
            **variant_config.get("gradient_presets", {}),
        }

        item_overrides = variant_config.get("item_overrides", {})
        master_items = master_config.get("items", [])

        output_atlas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

        def _src(field: str, override: dict, master_item: dict, default_name: str = "default") -> str:
            """Return the source label for a resolved field."""
            if field in override:
                return "variant_override"
            if field in master_item:
                return "master_shape"
            return default_name

        for master_item in master_items:
            item_name = master_item.get("name", "")
            override = item_overrides.get(item_name, {})
            item_entry = {**master_item, **override}
            overridden_fields = list(override.keys())

            item_row = int(item_entry.get("item_row", 1)) - 1
            item_col = int(item_entry.get("item_col", 1)) - 1

            button_row_raw = item_entry.get("button_row", default_button.get("button_row", 1))
            button_row = int(button_row_raw) - 1
            button_col_raw = item_entry.get("button_col", default_button.get("button_col", 1))
            button_col = int(button_col_raw) - 1
            button_col_src = _src("button_col", override, master_item, "default_button")

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

            # --- Gradient resolution ---
            gradient_name = item_entry.get("gradient", default_button.get("gradient", "gold"))
            gradient_name_src = _src("gradient", override, master_item, "default_button")
            preset = gradient_presets.get(gradient_name, {}) if isinstance(gradient_presets, dict) else {}

            top_color = parse_rgb(
                item_entry.get("top_color", preset.get("top_color", default_button.get("top_color"))),
                fallback=(220, 200, 100),
            )
            bottom_color = parse_rgb(
                item_entry.get("bottom_color", preset.get("bottom_color", default_button.get("bottom_color"))),
                fallback=(180, 160, 80),
            )
            raw_mid = item_entry.get("middle_color", preset.get("middle_color"))
            middle_color = parse_rgb(raw_mid, fallback=(255, 255, 255)) if raw_mid is not None else None
            gradient_type = item_entry.get("gradient_type", preset.get("type", "vertical"))

            item_colored = apply_item_gradient(
                item_tile, gradient_type, top_color, bottom_color, middle_color=middle_color
            )

            # --- Fit/layout resolution ---
            fit_size = int(item_entry.get("fit_size", default_item.get("fit_size", 36)))
            fit_size_src = _src("fit_size", override, master_item, "default_item")
            fit_mode = str(item_entry.get("fit_mode", default_item.get("fit_mode", "tile"))).strip().lower()
            fit_mode_src = _src("fit_mode", override, master_item, "default_item")
            offset_x = int(item_entry.get("offset_x", default_item.get("offset_x", 0)))
            offset_x_src = _src("offset_x", override, master_item, "default_item")
            offset_y = int(item_entry.get("offset_y", default_item.get("offset_y", -1)))
            offset_y_src = _src("offset_y", override, master_item, "default_item")
            item_opacity = float(item_entry.get("item_opacity", default_item.get("item_opacity", 0.92)))
            item_opacity_src = _src("item_opacity", override, master_item, "default_item")

            item_fitted = fit_item_to_button(
                item_colored,
                cell_size=cell_size,
                fit_size=fit_size,
                offset_x=offset_x,
                offset_y=offset_y,
                fit_mode=fit_mode,
            )

            composite = composite_item_on_button(
                item_tile=item_fitted,
                button_tile=button_tile,
                item_opacity=item_opacity,
                output_size=cell_size,
            )

            out_row = int(item_entry.get("out_row", 1)) - 1
            out_col = int(item_entry.get("out_col", 1)) - 1
            out_x = out_col * cell_size
            out_y = out_row * cell_size

            output_atlas.alpha_composite(composite, (out_x, out_y))

            # Console output — flag overrides with a marker
            override_marker = " *" if overridden_fields else ""
            print(
                f"  {item_name:12s} @ ({out_x:3d},{out_y:3d})  "
                f"gradient={gradient_name:<8s}[{gradient_name_src[0]}]  "
                f"fit={fit_size:2d}[{fit_size_src[0]}]  "
                f"mode={fit_mode}[{fit_mode_src[0]}]  "
                f"btn_col={button_col+1}[{button_col_src[0]}]"
                f"{override_marker}"
            )

            # Per-item stats record
            item_stat: dict = {
                "name": item_name,
                "out_row": out_row + 1,
                "out_col": out_col + 1,
                "gradient": gradient_name,
                "gradient_source": gradient_name_src,
                "gradient_type": gradient_type,
                "top_color": list(top_color),
                "bottom_color": list(bottom_color),
                "middle_color": list(middle_color) if middle_color is not None else None,
                "fit_size": fit_size,
                "fit_size_source": fit_size_src,
                "fit_mode": fit_mode,
                "fit_mode_source": fit_mode_src,
                "button_col": button_col + 1,
                "button_col_source": button_col_src,
                "offset_x": offset_x,
                "offset_x_source": offset_x_src,
                "offset_y": offset_y,
                "offset_y_source": offset_y_src,
                "item_opacity": item_opacity,
                "item_opacity_source": item_opacity_src,
                "overrides_applied": overridden_fields,
                "has_override": bool(overridden_fields),
            }
            self.stats["items"].append(item_stat)
            self.stats["summary"]["items_total"] += 1
            if overridden_fields:
                self.stats["summary"]["items_with_overrides"] += 1

        output_file = self.variant_dir / OUTPUT_FILENAME
        output_atlas.save(output_file, format="TGA")
        self.stats["output_file"] = str(output_file)

        total = self.stats["summary"]["items_total"]
        overridden = self.stats["summary"]["items_with_overrides"]
        print(f"\n  Created: {output_file.name}  ({output_atlas.size[0]}×{output_atlas.size[1]})")
        print(f"  Items: {total} total, {overridden} with variant overrides (* in list above)")
        print(f"  [OK] Slots complete: {self.variant_name}")
        return True

    def save_stats(self) -> None:
        """Write processing statistics to .regen_slots-stats.json."""
        stats_file = self.variant_dir / STATS_FILENAME
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2)


# ---------------------------------------------------------------------------
# Variant discovery
# ---------------------------------------------------------------------------

def discover_variants(base_dir: Path) -> list[str]:
    """Auto-discover slot variants from Options/Slots/ that have a .regen_slots.json config."""
    variants: list[str] = []
    slots_dir = base_dir / "thorne_drak" / "Options" / "Slots"

    if not slots_dir.exists():
        return variants

    for item in sorted(slots_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            if (item / CONFIG_FILENAME).exists():
                variants.append(item.name)

    return variants


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate slot item textures from source button and item atlases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python regen_slots.py --all              # All configured variants
  python regen_slots.py Gold               # Single variant
  python regen_slots.py Gold Silver Metal  # Multiple variants

Note: Each variant directory must contain a .regen_slots.json config file.
Source files (item/button atlases) should be copied from Options/Slots/.Master/
before running this script.
        """,
    )

    parser.add_argument(
        "variants",
        nargs="*",
        help="Slot variant names (e.g., Gold, Silver, Metal)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all auto-discovered variants (requires .regen_slots.json in each)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    base_dir = script_dir.parent

    if args.all:
        variants = discover_variants(base_dir)
        if not variants:
            print("ERROR: No configured variants found in thorne_drak/Options/Slots/")
            print(f"  Each variant directory needs a {CONFIG_FILENAME} config file.")
            return 1
        print(f"Auto-discovered {len(variants)} variant(s): {', '.join(variants)}")
    elif args.variants:
        variants = args.variants
    else:
        parser.print_help()
        return 1

    success_count = 0
    total_count = len(variants)
    regenerated_variants: list[tuple[str, Path]] = []

    for variant in variants:
        variant_dir = base_dir / "thorne_drak" / "Options" / "Slots" / variant

        if not variant_dir.exists():
            print(f"\nERROR: Variant directory not found: {variant_dir}")
            continue

        generator = SlotGenerator(variant_dir)
        if generator.generate():
            generator.save_stats()
            success_count += 1
            regenerated_variants.append((variant, variant_dir))

    # Smart copyback: single variant → copy it; multiple → copy Gold (primary)
    variants_to_copy: list[tuple[str, Path]] = []
    root_path = base_dir / "thorne_drak"

    if len(regenerated_variants) == 1:
        variants_to_copy = regenerated_variants
    elif len(regenerated_variants) > 1:
        for name, path in regenerated_variants:
            if name.lower() == "gold":
                variants_to_copy = [(name, path)]
                break

    if variants_to_copy:
        print(f"\n{'='*70}")
        print("Copying regenerated files back to thorne_drak/...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            src = variant_path / OUTPUT_FILENAME
            dst = root_path / OUTPUT_FILENAME
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Copied {variant_name}/{OUTPUT_FILENAME} → thorne_drak/")

    # Deploy to thorne_dev for immediate testing
    thorne_dev_path = Path(r"C:\TAKP\uifiles\thorne_dev")
    if thorne_dev_path.exists() and variants_to_copy:
        print(f"\n{'='*70}")
        print("Deploying to thorne_dev for testing...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            src = variant_path / OUTPUT_FILENAME
            dst = thorne_dev_path / OUTPUT_FILENAME
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Deployed {variant_name}/{OUTPUT_FILENAME} → thorne_dev/")

    print(f"\n{'='*70}")
    print(f"SUMMARY: {success_count}/{total_count} variant(s) processed successfully")
    print(f"{'='*70}\n")

    if success_count > 0 and variants_to_copy:
        print("Ready to test in-game with: /loadskin thorne_dev\n")

    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
