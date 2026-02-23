"""regen_thorne.py -- Generate item icon atlases from source dragitem files.

Reads .regen_thorne.json config and dragitem source TGA files, composites them into
grayscale item icon atlases. Output (thorne_item01.tga + variants) is consumed by
regen_slots.py to generate finished slot textures.

Usage:
    python regen_thorne.py                       # Default: .Master directory
    python regen_thorne.py .Master               # Explicit directory
    python regen_thorne.py --class Thorne        # Generate a single class override
    python regen_thorne.py --all-classes         # .Master + class overrides under .Master/.Classes/
    python regen_thorne.py --help                # Show help

Inputs (per directory):
  .regen_thorne.json       -- Item grid layout config
  dragitem*.tga            -- Individual item source icons
  logo_atlas_thorne01.tga       -- Logo source tiles

Output (per directory):
  thorne_item01.tga        -- Base composited item atlas (40px cells, 256x256)
  thorne_icons01.tga       -- Icon variant (20px cells, 256x256, if configured)
  .regen_thorne-stats.json -- Processing statistics
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

CONFIG_FILENAME = ".regen_thorne.json"
STATS_FILENAME = ".regen_thorne-stats.json"


# ---------------------------------------------------------------------------
# Image processing functions
# ---------------------------------------------------------------------------

def to_grayscale_rgba(img: Image.Image, contrast: float, brightness: float) -> Image.Image:
    """Convert image to grayscale while preserving alpha, with tone controls."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))

    gray_enhanced = ImageEnhance.Contrast(gray).enhance(contrast)
    gray_enhanced = ImageEnhance.Brightness(gray_enhanced).enhance(brightness)

    return Image.merge("RGBA", (gray_enhanced, gray_enhanced, gray_enhanced, a))


def to_inverted_grayscale_rgba(img: Image.Image, contrast: float, brightness: float) -> Image.Image:
    """Invert source, then grayscale and apply tone controls (keeps alpha)."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))
    inverted = ImageOps.invert(rgb)
    gray = ImageOps.grayscale(inverted)

    gray_enhanced = ImageEnhance.Contrast(gray).enhance(contrast)
    gray_enhanced = ImageEnhance.Brightness(gray_enhanced).enhance(brightness)

    return Image.merge("RGBA", (gray_enhanced, gray_enhanced, gray_enhanced, a))


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


def load_sources(directory: Path, fallback_dir: Path | None = None) -> dict[str, Image.Image]:
    """Load all TGA source files from a directory, with optional fallback."""
    sources: dict[str, Image.Image] = {}
    for path in directory.glob("*.tga"):
        try:
            sources[path.name] = Image.open(path).convert("RGBA")
        except Exception:
            continue
    if fallback_dir and fallback_dir.exists() and fallback_dir != directory:
        for path in fallback_dir.glob("*.tga"):
            if path.name in sources:
                continue
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


# ---------------------------------------------------------------------------
# ThorneGenerator class
# ---------------------------------------------------------------------------

class ThorneGenerator:
    """Generates item icon atlases from source dragitem files."""

    def __init__(
        self,
        directory: Path,
        config_override: dict | None = None,
        source_dir: Path | None = None,
        fallback_dir: Path | None = None,
        verbose: bool = False,
    ) -> None:
        self.directory = directory
        self.config_file = directory / CONFIG_FILENAME
        self.config_override = config_override
        self.source_dir = source_dir or directory
        self.fallback_dir = fallback_dir
        self.stats: dict = {
            "directory": str(directory.name),
            "summary": {
                "items_total": 0,
                "atlases_generated": 0,
            },
            "items": [],
            "output_files": [],
            "errors": [],
        }
        self.verbose = verbose
        self._dot_count = 0
        self._dot_line_open = False

    def _progress_dot(self) -> None:
        print(".", end="", flush=True)
        self._dot_count += 1
        self._dot_line_open = True
        if self._dot_count % 80 == 0:
            print()
            self._dot_line_open = False

    def _ensure_newline(self) -> None:
        if self._dot_line_open:
            print()
            self._dot_line_open = False

    def render_item(
        self,
        entry: dict,
        sources: dict[str, Image.Image],
        source_cell_size: int,
        output_cell_size: int,
        default_tone: dict,
    ) -> Image.Image:
        """Render a single item tile from config entry."""
        mode = entry.get("mode", "grayscale")
        if mode == "empty":
            return Image.new("RGBA", (output_cell_size, output_cell_size), (0, 0, 0, 0))

        source_file = entry.get("source_file")
        source_mode = entry.get("source_mode", "grid")
        src_row = int(entry.get("src_row", 1)) - 1  # Convert 1-based to 0-based
        src_col = int(entry.get("src_col", 1)) - 1  # Convert 1-based to 0-based

        if not source_file or source_file not in sources:
            raise FileNotFoundError(f"Missing source file: {source_file}")

        src_img = sources[source_file]

        if source_mode == "full":
            tile = src_img.resize((source_cell_size, source_cell_size), Image.Resampling.LANCZOS)
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
            result = result.resize((output_cell_size, output_cell_size), Image.Resampling.LANCZOS)

        return result

    def generate_atlas(
        self,
        items: list,
        sources: dict,
        source_cell_size: int,
        output_cell_size: int,
        output_size: int,
        default_tone: dict,
        atlas_name: str = "base",
    ) -> Image.Image:
        """Generate a single atlas with the given cell and output sizes."""
        atlas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

        for entry in items:
            out_row = int(entry.get("out_row", 1)) - 1  # Convert 1-based to 0-based
            out_col = int(entry.get("out_col", 1)) - 1  # Convert 1-based to 0-based
            name = entry.get("name", "(unnamed)")

            try:
                tile = self.render_item(entry, sources, source_cell_size, output_cell_size, default_tone)
                x = out_col * output_cell_size
                y = out_row * output_cell_size
                atlas.alpha_composite(tile, (x, y))

                if self.verbose:
                    print(f"  [{atlas_name:6s}] {name:12s} @ ({x:3d},{y:3d})")
                else:
                    self._progress_dot()

                # Per-item stats
                item_stat = {
                    "name": name,
                    "out_row": out_row + 1,
                    "out_col": out_col + 1,
                    "source_file": entry.get("source_file", ""),
                    "src_row": entry.get("src_row", 1),
                    "src_col": entry.get("src_col", 1),
                    "mode": entry.get("mode", "grayscale"),
                    "has_tone_override": "tone" in entry,
                }
                self.stats["items"].append(item_stat)
                self.stats["summary"]["items_total"] += 1

            except Exception as e:
                err_msg = f"Failed to render {name}: {e}"
                print(f"  ERROR: {err_msg}")
                self.stats["errors"].append(err_msg)

        return atlas

    def generate(self) -> bool:
        """Run the full atlas generation pipeline. Returns True on success."""
        print(f"\n{'='*70}")
        print(f"GENERATING ITEM ATLASES: {self.directory.name}")
        print(f"{'='*70}")

        if self.config_override is None:
            if not self.config_file.exists():
                print(f"  ERROR: Config not found: {self.config_file}")
                return False

            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = self.config_override

        # Base configuration
        base_cell_size = int(config.get("cell_size", 40))
        base_output_size = int(config.get("output_size", 256))
        base_output_filename = config.get("output_file", "item_atlas_thorne01.tga")
        default_tone = config.get("default_tone", {"contrast": 1.10, "brightness": 0.95})
        items = config.get("items", [])
        variants = config.get("variants", [])

        sources = load_sources(self.source_dir, fallback_dir=self.fallback_dir)

        if not items:
            print("  ERROR: Config has no items to render.")
            return False

        # Generate base atlas
        print(f"\n  Generating base atlas ({base_output_filename})...")
        atlas = self.generate_atlas(
            items, sources, base_cell_size, base_cell_size, base_output_size, default_tone, atlas_name="base"
        )
        out_base = self.directory / base_output_filename
        atlas.save(out_base, format="TGA")
        self._ensure_newline()
        self.stats["output_files"].append(str(out_base.name))
        self.stats["summary"]["atlases_generated"] += 1
        print(f"\n  Created: {out_base.name}  ({atlas.size[0]}×{atlas.size[1]})")

        # Generate variant atlases
        for variant in variants:
            variant_name = variant.get("name", "variant")
            variant_cell_size = int(variant.get("cell_size", base_cell_size))
            variant_output_size = int(variant.get("output_size", base_output_size))
            variant_output_filename = variant.get("output_file", f"item_{variant_name}01.tga")

            print(f"\n  Generating variant '{variant_name}' ({variant_output_filename})...")
            variant_atlas = self.generate_atlas(
                items, sources, base_cell_size, variant_cell_size, variant_output_size, default_tone, atlas_name=variant_name
            )
            out_variant = self.directory / variant_output_filename
            variant_atlas.save(out_variant, format="TGA")
            self._ensure_newline()
            self.stats["output_files"].append(str(out_variant.name))
            self.stats["summary"]["atlases_generated"] += 1
            print(f"\n  Created: {out_variant.name}  ({variant_atlas.size[0]}×{variant_atlas.size[1]})")

        print(f"\n  [OK] Thorne atlas generation complete: {self.directory.name}")
        print(f"  Items rendered: {self.stats['summary']['items_total']}")
        print(f"  Atlases created: {self.stats['summary']['atlases_generated']}")
        return True

    def save_stats(self) -> None:
        """Write processing statistics to .regen_thorne-stats.json."""
        stats_file = self.directory / STATS_FILENAME
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _merge_items(base_items: list[dict], override_items: list[dict]) -> list[dict]:
    base_by_name = {item.get("name"): item for item in base_items}
    merged = list(base_items)
    for override in override_items:
        name = override.get("name")
        if not name:
            merged.append(override)
            continue
        if name in base_by_name:
            for idx, item in enumerate(merged):
                if item.get("name") == name:
                    merged[idx] = {**item, **override}
                    break
        else:
            merged.append(override)
    return merged


def _merge_variants(base_variants: list[dict], override_variants: list[dict]) -> list[dict]:
    base_by_name = {variant.get("name"): variant for variant in base_variants}
    merged = list(base_variants)
    for override in override_variants:
        name = override.get("name")
        if not name:
            merged.append(override)
            continue
        if name in base_by_name:
            for idx, variant in enumerate(merged):
                if variant.get("name") == name:
                    merged[idx] = {**variant, **override}
                    break
        else:
            merged.append(override)
    return merged


def _merge_config(base: dict, override: dict) -> dict:
    merged = {**base, **override}
    if "items" in base or "items" in override:
        merged["items"] = _merge_items(base.get("items", []), override.get("items", []))
    if "variants" in base or "variants" in override:
        merged["variants"] = _merge_variants(base.get("variants", []), override.get("variants", []))
    return merged


def _discover_class_overrides(master_dir: Path) -> list[Path]:
    class_dirs: list[Path] = []
    classes_dir = master_dir / ".Classes"
    if not classes_dir.exists():
        return class_dirs
    for item in sorted(classes_dir.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if (item / CONFIG_FILENAME).exists():
            class_dirs.append(item)
    return class_dirs


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate item icon atlases from source dragitem files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python regen_thorne.py --master           # Update .Master directory (REQUIRES --master flag)
  python regen_thorne.py --class Thorne     # Generate single class override (safe, no --master needed)
  python regen_thorne.py --all-classes      # Generate all classes under .Master/.Classes/

SAFETY:
  - Direct .Master/ updates REQUIRE --master flag to prevent accidental writes
  - Class-specific updates (--class) do NOT need --master
  - Use --all-classes to regenerate all class overrides

Directory must contain .regen_thorne.json config file and source dragitem TGA files.
        """,
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="(Deprecated) Use --master flag instead",
    )
    parser.add_argument(
        "--master",
        action="store_true",
        help="Explicitly allow updates to .Master/ directory (required safety gate)",
    )
    parser.add_argument(
        "--class",
        dest="class_name",
        help="Class name under .Master/.Classes to generate (uses base + class overrides).",
    )
    parser.add_argument(
        "--all-classes",
        action="store_true",
        help="Generate atlases for .Master and all class overrides under .Master/.Classes/",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed per-item output (default is compact progress dots).",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    slots_dir = base_dir / "thorne_drak" / "Options" / "Slots"

    # Safety check: .Master requires explicit --master flag
    if args.directory and args.directory == ".Master" and not args.master:
        print("ERROR: Direct .Master/ updates require --master flag")
        print("  Usage: python regen_thorne.py --master")
        print("\nFor safer class-specific updates:")
        print("  python regen_thorne.py --class Thorne")
        return 1

    if args.all_classes and args.class_name:
        print("ERROR: Use --class or --all-classes, not both.")
        return 1

    # If no flags provided, show usage
    if not args.master and not args.class_name and not args.all_classes:
        print("ERROR: No target specified.")
        print("\nUsage:")
        print("  python regen_thorne.py --master              # Update .Master/")
        print("  python regen_thorne.py --class Thorne        # Update class override")
        print("  python regen_thorne.py --all-classes         # Update all classes")
        print("\nFor help: python regen_thorne.py --help")
        return 1

    if args.class_name:
        master_dir = slots_dir / ".Master"
        class_dir = master_dir / ".Classes" / args.class_name
        if not master_dir.exists():
            print(f"ERROR: Master directory not found: {master_dir}")
            return 1
        if not class_dir.exists():
            print(f"ERROR: Class directory not found: {class_dir}")
            return 1

        base_config_path = master_dir / CONFIG_FILENAME
        class_config_path = class_dir / CONFIG_FILENAME
        if not base_config_path.exists():
            print(f"ERROR: Config not found: {base_config_path}")
            return 1
        if not class_config_path.exists():
            print(f"ERROR: Config not found: {class_config_path}")
            return 1

        with open(base_config_path, "r", encoding="utf-8") as f:
            base_config = json.load(f)
        with open(class_config_path, "r", encoding="utf-8") as f:
            class_config = json.load(f)

        merged_config = _merge_config(base_config, class_config)
        generator = ThorneGenerator(
            class_dir,
            config_override=merged_config,
            source_dir=master_dir / ".Items",
            fallback_dir=master_dir,
            verbose=args.verbose,
        )
        if generator.generate():
            generator.save_stats()
            print(f"\n{'='*70}")
            print(f"SUMMARY: Generated {generator.stats['summary']['atlases_generated']} atlas(es)")
            print(f"{'='*70}\n")
            return 0
        print("\n[FAILED] Generation did not complete successfully.\n")
        return 1

    if args.master:
        master_dir = slots_dir / ".Master"
        if not master_dir.exists():
            print(f"ERROR: Master directory not found: {master_dir}")
            return 1

        base_config_path = master_dir / CONFIG_FILENAME
        if not base_config_path.exists():
            print(f"ERROR: Config not found: {base_config_path}")
            return 1
        with open(base_config_path, "r", encoding="utf-8") as f:
            base_config = json.load(f)

        items_dir = master_dir / ".Items"
        generator = ThorneGenerator(
            master_dir,
            source_dir=items_dir,
            verbose=args.verbose,
        )
        if generator.generate():
            generator.save_stats()
            print(f"\n{'='*70}")
            print(f"SUMMARY: Generated {generator.stats['summary']['atlases_generated']} atlas(es)")
            print(f"{'='*70}\n")
            return 0
        print("\n[FAILED] Generation did not complete successfully.\n")
        return 1

    if args.all_classes:
        master_dir = slots_dir / ".Master"
        base_config_path = master_dir / CONFIG_FILENAME
        if not base_config_path.exists():
            print(f"ERROR: Config not found: {base_config_path}")
            return 1
        with open(base_config_path, "r", encoding="utf-8") as f:
            base_config = json.load(f)

        class_dirs = _discover_class_overrides(master_dir)
        total = 1 + len(class_dirs)
        success = 0

        # Generate base .Master
        items_dir = master_dir / ".Items"
        generator = ThorneGenerator(master_dir, source_dir=items_dir, verbose=args.verbose)
        if generator.generate():
            generator.save_stats()
            success += 1

        # Generate each class override, using .Master sources and merged config
        for class_dir in class_dirs:
            class_config_path = class_dir / CONFIG_FILENAME
            with open(class_config_path, "r", encoding="utf-8") as f:
                class_config = json.load(f)
            merged_config = _merge_config(base_config, class_config)
            generator = ThorneGenerator(
                class_dir,
                config_override=merged_config,
                source_dir=items_dir,
                verbose=args.verbose,
            )
            if generator.generate():
                generator.save_stats()
                success += 1

        print(f"\n{'='*70}")
        print(f"SUMMARY: Generated {success}/{total} atlas(es)")
        print(f"{'='*70}\n")
        return 0 if success == total else 1

    generator = ThorneGenerator(
        target_dir,
        source_dir=target_dir / ".Items",
        fallback_dir=target_dir,
        verbose=args.verbose,
    )
    if generator.generate():
        generator.save_stats()
        print(f"\n{'='*70}")
        print(f"SUMMARY: Generated {generator.stats['summary']['atlases_generated']} atlas(es)")
        print(f"{'='*70}\n")
        return 0
    else:
        print("\n[FAILED] Generation did not complete successfully.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
