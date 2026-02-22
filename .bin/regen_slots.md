# Slot Texture Regeneration (regen_slots.py)

Compositing automation for generating themed item slot textures from source item and button tiles.

## Overview

**Purpose:** Composite item icons onto button backgrounds to produce `item_slots_thorne01.tga` — the themed texture used for inventory and container slot graphics.

**Key Features:**
- **Config split:** master layout (`.bin/regen_slots.json`) + per-variant styling (`.regen_slots.json`) — no duplication across variants
- Auto-discovers all configured variants in `Options/Slots/`
- `SlotGenerator` class — consistent architecture with other regen scripts
- Supports per-item gradient tinting (vertical tint, direct color, or none)
- Multiple fit modes for item scaling: `tile` (full source) or `visible` (alpha-bounded crop)
- Separator-aware button grid extraction (supports 2px separators between cells)
- Per-item shape hints (`fit_size`, `button_col`, `offset_y`) live in master — intrinsic to icon/slot type, not color variant
- Gradient presets in variant config for reusable color treatments
- Smart copyback to `thorne_drak/` and auto-deploy to `thorne_dev/`
- Writes `.regen_slots-stats.json` per variant

**Source file workflow:** Source textures (item and button atlases) are prepared by separate `generate_thorne_*.py`
scripts that work on `Options/Slots/.Master/` directly. Source filenames are defined in `.bin/regen_slots.json`
and can be overridden per-variant if needed.

---

## Quick Start

### Auto-Discover All Variants

```bash
python .bin/regen_slots.py --all
```

**What happens:**
1. Scans `thorne_drak/Options/Slots/` for all subdirectories with a `.regen_slots.json` config
2. Auto-discovers all configured variants (e.g., Gold, Silver, Metal)
3. Composites item icons onto button backgrounds for each variant
4. Copies the primary variant (`Gold`) to `thorne_drak/` as `item_slots_thorne01.tga`
5. Deploys to `thorne_dev/` for immediate testing

**Best for:** Rebuilding all slot variants at once after updating source atlases.

### Single Variant (Most Common)

```bash
python .bin/regen_slots.py Gold
```

**What happens:**
1. Reads `.bin/regen_slots.json` (master layout: all 26 item entries + source filenames)
2. Reads `.regen_slots.json` from `thorne_drak/Options/Slots/Gold/` (variant styling: gradients, item_overrides)
3. Merges the two configs — variant `item_overrides` layer on top of master item fields
4. Loads `thorne_item01.tga` and `thorne_buttons01.tga` from the variant directory
5. Composites each item entry onto its configured button background
6. Saves `item_slots_thorne01.tga` in the variant directory
7. Copies to `thorne_drak/` (for git commits)
8. Deploys to `thorne_dev/` (ready to test in-game)
9. Prints: `Ready to test in-game with: /loadskin thorne_dev`

### Multiple Variants

```bash
python .bin/regen_slots.py Gold Silver Metal
```

**What happens:**
1. Regenerates all 3 variants using shared master layout from `.bin/regen_slots.json`
2. Only copies `Gold` back to `thorne_drak/` as `item_slots_thorne01.tga` (smart copyback — see below)
3. Others remain in their Options subdirectories

---

## Command-Line Options

**Usage:**
```bash
python .bin/regen_slots.py --all                             # Auto-discover all variants
python .bin/regen_slots.py <variant> [variant2 ...]          # Specific variants
python .bin/regen_slots.py --help                            # Show help
```

**Arguments & Flags:**

- `--all` — Auto-discover and regenerate all variants from `Options/Slots/`
  - Discovers variants by checking for `.regen_slots.json` in each subdirectory
  - Skips hidden directories (`.Master` etc.) automatically
  - Future-proof: new variant directories are picked up without code changes

- `variant` — Variant name(s) to regenerate (positional, space-separated)
  - `Gold` — Primary development variant
  - `Silver`, `Metal` — Other variants (when configured)

**Examples:**
```bash
python .bin/regen_slots.py --all                   # All variants (auto-discovered)
python .bin/regen_slots.py Gold                    # Single variant
python .bin/regen_slots.py Gold Silver             # Two variants
python .bin/regen_slots.py --help                  # Show help message
```

---

## Config File Format

The script uses a **split config** model: a shared master config holds item layout; each variant config holds
only styling. This eliminates duplication and lets you add new variants by writing only colors.

---

### Master Config (`.bin/regen_slots.json`)

Shared across all variants. Contains source filenames, grid geometry, and the full `items` array with per-item shape hints. **Do not put gradient or color data here.**

```json
{
  "source_items": "thorne_item01.tga",
  "source_buttons": "thorne_buttons01.tga",
  "output_size": 256,
  "cell_size": 40,
  "items": [
    {
      "name": "head",
      "item_row": 1, "item_col": 1,
      "out_row": 1,  "out_col": 2,
      "button_col": 2
    },
    {
      "name": "back",
      "item_row": 1, "item_col": 3,
      "out_row": 1,  "out_col": 4,
      "fit_size": 35
    }
  ]
}
```

**Per-item shape hints** (intrinsic to icon shape, not color variant):
- `button_col` — Override button column for this slot (e.g., `2` = wider button style for helm/weapons)
- `fit_size` — Smaller fit for taller icons like back, fingers, ammo, bag (default: from `default_item`)
- `offset_y` — Vertical nudge for logo slots (e.g., `-2` to shift icon up slightly)

---

### Variant Config (`<variant>/.regen_slots.json`)

Each variant directory requires a `.regen_slots.json` focused on **styling only**. The dotfile prefix keeps it hidden from the EQ client's UI directory browser.

```json
{
  "_comment": "Gold variant — warm gold gradient treatment",
  "button_grid": {
    "sep_x": 2,
    "sep_y": 2,
    "origin_x": 0,
    "origin_y": 0
  },
  "gradient_presets": {
    "gold":   { "type": "vertical", "top_color": [220, 200, 100], "bottom_color": [180, 160, 80] },
    "silver": { "type": "vertical", "top_color": [200, 210, 220], "bottom_color": [160, 170, 180] },
    "logo":   { "type": "vertical", "top_color": [180, 170, 140], "bottom_color": [140, 130, 110] },
    "none":   { "type": "none" }
  },
  "default_button": {
    "button_row": 1,
    "button_col": 1,
    "gradient": "gold"
  },
  "default_item": {
    "fit_mode": "tile",
    "fit_size": 28,
    "offset_x": 1,
    "offset_y": 1,
    "item_opacity": 0.92
  },
  "item_overrides": {
    "logo_1": { "gradient": "none" },
    "logo_2": { "gradient": "logo" },
    "logo_3": { "gradient": "logo" },
    "logo_4": { "gradient": "logo" },
    "logo_5": { "gradient": "logo" }
  }
}
```

### `button_grid`

Controls extraction from `thorne_buttons01.tga`:
- `sep_x` / `sep_y` — Pixel gap between cells (default: 2px)
- `origin_x` / `origin_y` — Pixel offset of the first button cell (default: 0)

### `default_button`

Fallback button position and gradient for all items unless overridden.

### `default_item`

Fallback item rendering for all items unless overridden.
- `fit_size` — Target resize dimension for item icon
- `fit_mode` — `"tile"` (scale full source tile) or `"visible"` (scale visible alpha bounds only)
- `offset_x` / `offset_y` — Fine-tune centring offsets in pixels
- `item_opacity` — Alpha multiplier for item layer (0.0–1.0)

### `gradient_presets`

Named presets for `top_color` / `bottom_color` / `type`. Items reference these by name via `gradient` to avoid repeating color values. Currently supported type: `"vertical"` and `"none"`.

### `item_overrides`

Sparse per-item styling overrides, keyed by item `name`. Only the fields you specify are overridden —
everything else falls through to `default_button` / `default_item` and the master shape hints.

```json
"item_overrides": {
  "logo_1": { "gradient": "none" },
  "primary": { "button_row": 2, "gradient": "gold" }
}
```

**Merge order (lowest → highest priority):**
1. `default_button` / `default_item` (variant config)
2. Master item fields (`fit_size`, `button_col`, `offset_y` shape hints)
3. `item_overrides` for that item name (variant config)

Row/col values are **1-based** throughout.

---

## How It Works

### 1. Config Loading

Loads two config files and merges them:
1. **`.bin/regen_slots.json`** — master layout: 26 item entries (`item_row/col`, `out_row/col`, shape hints), source filenames, grid geometry
2. **`<variant>/.regen_slots.json`** — variant styling: `gradient_presets`, `default_button`, `default_item`, `item_overrides`

Merge logic per item: `{**master_item, **item_overrides.get(name, {})}` — variant overrides only what it specifies; shape hints from master always apply unless explicitly overridden.

### 2. Source Atlas Loading

Two source textures are loaded:
- **thorne_item01.tga** — Grid of item icon source tiles (40×40 per cell)
- **thorne_buttons01.tga** — Grid of button background tiles (40×40 per cell, with separator pixels)

### 3. Per-Item Compositing

For each item in `items`:
1. **Extract item tile** — Crop from `thorne_item01.tga` at `(item_row, item_col)`
2. **Extract button tile** — Crop from `thorne_buttons01.tga` using separator-aware coordinates
3. **Color treatment** — Apply vertical tint gradient or direct color to item tile
4. **Fit and offset** — Scale item to `fit_size`, center on `cell_size` canvas with offsets
5. **Composite** — Apply `item_opacity`, paste button, paste item on top
6. **Place on output** — Paste result at `(out_row, out_col)` in the output atlas

### 4. Auto-Discovery (--all)

When using `--all`, the script scans `thorne_drak/Options/Slots/` for any subdirectory that contains a
`.regen_slots.json` config file. Hidden directories (prefixed with `.`) are skipped automatically, so
`.Master/` is never processed.

### 5. Output

Saves `item_slots_thorne01.tga` (RGBA, `output_size × output_size`) to the variant directory.

### 6. Smart Copyback

**Single variant (e.g., `Gold`):**
- Copies `item_slots_thorne01.tga` to `thorne_drak/`

**Multiple variants (e.g., `Gold Silver Metal`):**
- Only copies `Gold` to `thorne_drak/`
- Others stay in their Options subdirectories

### 7. Automatic Deployment

After copyback, copies to `C:\TAKP\uifiles\thorne_dev\` for immediate in-game testing.

---

## Gradient / Tint Modes

| `gradient_type` | Behavior |
|---|---|
| `vertical` | Top-to-bottom linear tint between `top_color` and `bottom_color` |
| `none` | No tint applied — item rendered as-is |
| `direct` | Same as `none` — passes item through without tint |

Colors are specified as `[R, G, B]` arrays (0–255 each).

---

## Future Work

### `item_slots_thorne02.tga` — Colored Button Variant

Second atlas using colored/tinted button backgrounds — one button row per slot type (armor, weapon,
jewelry, bag). Requires a new `button_col` range in `thorne_buttons01.tga` or a separate source file.

### Gradient Palette Expansion

Add silver and multi-stop gradients (e.g., red-white-blue). Current vertical logic is 2-color only;
multi-stop requires revised gradient rendering in `SlotGenerator`.

### New Variant Configs

`Silver`, `Metal`, `Texture`, `Transparent` — copy source `.tga` files from `.Master/` into a new variant
dir, write a `.regen_slots.json` with the desired `gradient_presets` + `item_overrides`. No code changes
needed.

### Source File Naming Alignment

`thorne_item01.tga` / `thorne_buttons01.tga` intermediate sources →`item_thorne01.tga` /
`button_thorne01.tga` convention — when source pipeline naming is aligned across all scripts.

---

## Troubleshooting

### Error: No configured variants found

**Cause:** Running `--all` but no variant directories contain `.regen_slots.json`.

**Fix:** Ensure at least one subdirectory of `Options/Slots/` has a `.regen_slots.json` config, and that it contains the required source textures.

### Error: Variant directory not found

**Cause:** The variant name passed doesn't match a directory in `Options/Slots/`.

**Fix:** Check available variants with:
```bash
ls thorne_drak/Options/Slots/
```
Variant names are case-sensitive (e.g., `Gold` not `gold`).

### Error: Config file not found

**Cause:** No `.regen_slots.json` in the variant directory, or `.bin/regen_slots.json` is missing.

**Fix:**
- Master config: `.bin/regen_slots.json` must exist (shared, version-controlled).
- Variant config: create a `.regen_slots.json` in `Options/Slots/<variant>/`. See variant config format above.

### Error: Missing source texture

**Cause:** `thorne_item01.tga` or `thorne_buttons01.tga` not found in the variant directory.

**Fix:** Source textures live in `Options/Slots/.Master/` and must be copied to the variant directory before
running. Run `generate_thorne_item_master.py` and `generate_thorne_buttons_transparent.py` to regenerate them
from raw assets, then copy to the variant directory.

### Output looks misaligned

**Cause:** `out_row`/`out_col` coordinates, offsets, or `button_grid` settings are off.

**Fix:** Check the item entry's `out_row`/`out_col` values (1-based). Review `sep_x`/`sep_y` and `origin_x`/`origin_y` in `button_grid` for the button source alignment.

---

## Related Documentation

- [README.md](README.md) — Script index
- [STANDARDS.md](STANDARDS.md) — Script documentation standards
- [DEVELOPMENT.md](../DEVELOPMENT.md) — Project roadmap and phase details
