#!/usr/bin/env python3
"""
Sync a single UI Option variant into thorne_dev for in-game testing.

Examples:
  python .bin/sync_option.py spellbook/large
  python .bin/sync_option.py "Music/Thorne 14 Row"
  python .bin/sync_option.py --list
  python .bin/sync_option.py --list inventory
  python .bin/sync_option.py --option spellbook/large --dry-run --verbose
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import List

DEFAULT_SOURCE = Path(r"C:\Thorne-UI\thorne_drak")
DEFAULT_DEST = Path(r"C:\TAKP\uifiles\thorne_dev")

EXCLUDED_FILENAMES = {"Thumbs.db", ".DS_Store"}
EXCLUDED_EXTENSIONS = {".md"}


def normalize_path(path_str: str) -> str:
    return path_str.lower().replace("\\", "/").strip("/")


def option_dir_has_ui_file(path: Path) -> bool:
    if not path.is_dir():
        return False
    return any(f.name.startswith("EQUI_") and f.suffix.lower() == ".xml" for f in path.iterdir() if f.is_file())


def find_matching_options(options_root: Path, search_pattern: str) -> List[str]:
    if not options_root.is_dir():
        return []

    raw_pattern = search_pattern.strip().replace("\\", "/").strip("/")
    normalized_pattern = normalize_path(search_pattern)
    matches: List[str] = []

    # Full path form: category/variant
    if "/" in raw_pattern:
        parts = [p for p in raw_pattern.split("/") if p]

        exact = options_root.joinpath(*parts)
        if option_dir_has_ui_file(exact):
            return [str(exact.relative_to(options_root)).replace("\\", "/")]

        # Fuzzy prefix match per path segment (case-insensitive)
        current = options_root
        matched = True
        for part in parts:
            candidates = [
                child for child in current.iterdir()
                if child.is_dir() and normalize_path(child.name).startswith(normalize_path(part))
            ]
            if not candidates:
                matched = False
                break
            current = sorted(candidates, key=lambda p: p.name.lower())[0]

        if matched and option_dir_has_ui_file(current):
            return [str(current.relative_to(options_root)).replace("\\", "/")]

        return []

    # Category-only form: inventory / spellbook / music
    for category in sorted([d for d in options_root.iterdir() if d.is_dir()], key=lambda p: p.name.lower()):
        if not normalize_path(category.name).startswith(normalized_pattern):
            continue

        for variant in sorted([d for d in category.iterdir() if d.is_dir()], key=lambda p: p.name.lower()):
            if option_dir_has_ui_file(variant):
                matches.append(str(variant.relative_to(options_root)).replace("\\", "/"))

    return sorted(set(matches), key=str.lower)


def list_available(options_root: Path, category_filter: str | None = None) -> int:
    if not options_root.is_dir():
        print(f"Error: Options directory not found: {options_root}")
        return 1

    if category_filter:
        matches = find_matching_options(options_root, category_filter)
        if not matches:
            print(f"No options found for category/pattern: {category_filter}")
            return 1

        print(f"\nMatching options for '{category_filter}':")
        for m in matches:
            print(f"  - {m}")
        print()
        return 0

    print("\nAvailable option categories and variants:")
    for category in sorted([d for d in options_root.iterdir() if d.is_dir()], key=lambda p: p.name.lower()):
        variants = [
            variant.name
            for variant in sorted([d for d in category.iterdir() if d.is_dir()], key=lambda p: p.name.lower())
            if option_dir_has_ui_file(variant)
        ]
        if not variants:
            continue

        print(f"\n{category.name}/")
        for v in variants:
            print(f"  - {v}")

    print()
    return 0


def copy_option_files(source_option_dir: Path, dest_dir: Path, *, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    if not source_option_dir.is_dir():
        return False, f"Source option directory not found: {source_option_dir}"

    files_to_copy: List[Path] = []
    skipped: List[str] = []

    for item in sorted(source_option_dir.iterdir(), key=lambda p: p.name.lower()):
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if item.name in EXCLUDED_FILENAMES:
            continue
        if item.suffix.lower() in EXCLUDED_EXTENSIONS:
            skipped.append(item.name)
            continue
        files_to_copy.append(item)

    if not files_to_copy:
        if skipped:
            return True, f"No files copied (skipped {len(skipped)} markdown file(s))."
        return True, "No files found to copy."

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    copied: List[str] = []
    for src in files_to_copy:
        dst = dest_dir / src.name
        if dry_run:
            copied.append(src.name)
            continue

        shutil.copy2(src, dst)
        copied.append(src.name)
        if verbose:
            print(f"  copied: {src.name}")

    preview = ", ".join(copied[:5])
    suffix = "" if len(copied) <= 5 else ", ..."
    return True, f"Copied {len(copied)} file(s): {preview}{suffix}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sync_option.py",
        description="Copy one option variant from thorne_drak/Options to thorne_dev root for testing.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  .bin\\sync-option.bat spellbook/large\n"
            "  .bin\\sync-option.bat \"Music/Thorne 14 Row\"\n"
            "  .bin\\sync-option.bat --list\n"
            "  .bin\\sync-option.bat --list music\n"
            "  .bin\\sync-option.bat --option inventory/enhanced --dry-run --verbose"
        ),
    )

    parser.add_argument(
        "option_path",
        nargs="?",
        help="Option path under Options, e.g. spellbook/large or 'Music/Thorne 14 Row'.",
    )
    parser.add_argument(
        "--option",
        dest="option_flag",
        help="Same as positional option_path (takes precedence when provided).",
    )
    parser.add_argument(
        "--list",
        nargs="?",
        const="",
        metavar="CATEGORY",
        help="List options (all if no category is provided).",
    )
    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE),
        help=f"Source thorne_drak directory (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--dest",
        default=str(DEFAULT_DEST),
        help=f"Destination thorne_dev directory (default: {DEFAULT_DEST})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would copy without writing files.")
    parser.add_argument("--verbose", action="store_true", help="Show detailed file operations.")
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Fail instead of prompting when multiple options match.",
    )

    return parser


def choose_match(matches: List[str], *, no_interactive: bool) -> str | None:
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]

    print("Multiple options found:")
    for idx, item in enumerate(matches, 1):
        print(f"  {idx}. {item}")

    if no_interactive:
        print("\nError: Multiple matches found and --no-interactive was specified.")
        return None

    while True:
        choice = input(f"\nSelect option (1-{len(matches)}): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]
        except ValueError:
            pass
        print(f"Invalid selection. Enter a number between 1 and {len(matches)}.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    source_base = Path(args.source)
    options_root = source_base / "Options"
    dest_base = Path(args.dest)

    if args.list is not None:
        category = args.list.strip() or None
        return list_available(options_root, category)

    requested = (args.option_flag or args.option_path or "").strip()
    if not requested:
        parser.print_help()
        return 1

    if not options_root.is_dir():
        print(f"Error: Options directory not found: {options_root}")
        return 1

    print(f"\nSearching for options matching '{requested}'...")
    matches = find_matching_options(options_root, requested)
    selected = choose_match(matches, no_interactive=args.no_interactive)

    if not selected:
        print(f"\nNo options found matching '{requested}'.")
        print("\nTip: run with --list to browse available options.")
        return 1

    source_option_dir = options_root / Path(selected)

    print(f"\nSelected: {selected}")
    print(f"From: {source_option_dir}")
    print(f"To:   {dest_base}")
    if args.dry_run:
        print("Mode: dry-run")

    ok, message = copy_option_files(
        source_option_dir,
        dest_base,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    if not ok:
        print(f"\n✗ {message}")
        return 1

    print(f"\n* {message}")
    if not args.dry_run:
        print("\nReady to test in TAKP")
        print("In-game command: /loadskin thorne_dev")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
