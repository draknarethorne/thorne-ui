#!/usr/bin/env python3
"""Generate .regen_thorne.json files for all 15 EQ classes.

Reads class_icon_picks.json (from pick_class_icons.py) and produces one
.regen_thorne.json per class in the .Research directory. Each file contains
item_overrides that map the top-scoring icon per equipment slot to the
master atlas grid position.

Usage:
    python .bin/generate_regen_json.py

Input:  thorne_drak/Options/Slots/.Master/.Items/.cache/class_icon_picks.json
Output: thorne_drak/Options/Slots/.Master/.Research/{ClassName}/.regen_thorne.json
"""

import json
import os

# ----- paths -----
BASE = os.path.join("thorne_drak", "Options", "Slots", ".Master")
PICKS_FILE = os.path.join(BASE, ".Items", ".cache", "class_icon_picks.json")
RESEARCH_DIR = os.path.join(BASE, ".Research")
MASTER_REGEN = os.path.join(BASE, ".regen_thorne.json")

# ----- slot name mapping: pipeline name -> regen name -----
SLOT_NAME_MAP = {
    "shoulder": "shoulders",
    "waist": "belt",
}

# ----- default tone (neutral — tune per class later if desired) -----
DEFAULT_TONE = {"contrast": 1.0, "brightness": 1.0}


def load_master_grid(path):
    """Load master .regen_thorne.json and return grid positions for equipment slots."""
    with open(path, encoding="utf-8") as f:
        master = json.load(f)
    # Only rows 1-3 (equipment), keyed by regen slot name
    grid = {}
    for item in master["items"]:
        if item["out_row"] <= 3:
            grid[item["name"]] = {
                "out_row": item["out_row"],
                "out_col": item["out_col"],
            }
    return grid


def build_override(regen_name, grid_pos, pick):
    """Build a single item_overrides entry from a grid position and icon pick."""
    return {
        "name": regen_name,
        "out_row": grid_pos["out_row"],
        "out_col": grid_pos["out_col"],
        "src_row": pick["dragitem_row"],
        "src_col": pick["dragitem_col"],
        "source_file": f"dragitem{pick['dragitem_file']}.tga",
        "tone": dict(DEFAULT_TONE),
    }


def generate_class_regen(class_name, class_data, grid):
    """Generate a complete .regen_thorne.json dict for one class."""
    overrides = []
    slots = class_data["slots"]

    # Process in master grid order (row-major)
    grid_order = sorted(grid.items(), key=lambda kv: (kv[1]["out_row"], kv[1]["out_col"]))

    for regen_name, grid_pos in grid_order:
        # Reverse-map regen name to pipeline name
        pipeline_name = regen_name
        for pipe_name, reg_name in SLOT_NAME_MAP.items():
            if reg_name == regen_name:
                pipeline_name = pipe_name
                break

        if pipeline_name not in slots:
            continue

        picks = slots[pipeline_name]
        if not picks:
            continue

        # Use the top-scoring pick
        top_pick = picks[0]
        overrides.append(build_override(regen_name, grid_pos, top_pick))

    description = class_data.get("description", "")
    return {
        "_comment": f"{class_name} class item overrides (auto-generated from item data pipeline)",
        "_note": description,
        "class_name": class_name,
        "item_overrides": overrides,
    }


def main():
    # Load source data
    with open(PICKS_FILE, encoding="utf-8") as f:
        all_picks = json.load(f)

    grid = load_master_grid(MASTER_REGEN)

    print(f"Loaded {len(all_picks)} classes from {PICKS_FILE}")
    print(f"Master grid: {len(grid)} equipment slots")
    print()

    for class_name, class_data in sorted(all_picks.items()):
        regen = generate_class_regen(class_name, class_data, grid)

        # Create output directory
        out_dir = os.path.join(RESEARCH_DIR, class_name)
        os.makedirs(out_dir, exist_ok=True)

        # Write .regen_thorne.json
        out_path = os.path.join(out_dir, ".regen_thorne.json")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(regen, f, indent=2)
            f.write("\n")

        n_overrides = len(regen["item_overrides"])
        print(f"  {class_name:15s} -> {n_overrides} slot overrides -> {out_path}")

    print(f"\nDone. Generated .regen_thorne.json for {len(all_picks)} classes.")


if __name__ == "__main__":
    main()
