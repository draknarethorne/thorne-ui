# Item Icons — Source Assets & Data Pipeline

Source TGA sprite sheets (dragitem1–34) and pipeline-generated data for
class-specific equipment slot art in Thorne UI.

## Directory Layout

```
.Items/
  dragitem1.tga … dragitem34.tga   # Source sprite sheets (6×6 grid, 40px cells)
  README.md                         # This file
  .cache/
    dragitem1/ … dragitem34/        # Extracted cell PNGs (r1c1.png … r6c6.png)
    eq_items.csv                    # 26,971 items from Quarm SQL database
    eq_items.json                   # Same data, JSON format
    slot_icon_reference.csv         # Archetype → slot → icon reference
    slot_icon_reference.json        # Same data, JSON format
    class_icon_picks.csv            # 15-class scoring results (flat)
    class_icon_picks.json           # Same data (structured: class → slot → ranked)
    class_icon_picks.html           # Visual grid with PNG thumbnails
```

## Pipeline Scripts

All scripts live in `.bin/` at the repo root. Run from the project root.

### 1. extract_eq_items.py — Parse Quarm Database

Extracts item data from the SecretsOTheP/EQMacEmu SQL dump.

```bash
python .bin/extract_eq_items.py
```

**Source:** `.tmp/quarm_*.sql` (not tracked — download separately)
**Output:** `.Items/.cache/eq_items.csv` + `.json`

### 2. build_slot_reference.py — Archetype Slot Reference

Builds a reference of which icons are used by which class archetypes at each slot.

```bash
python .bin/build_slot_reference.py
```

**Input:** `eq_items.csv`
**Output:** `.Items/.cache/slot_icon_reference.csv` + `.json`

### 3. pick_class_icons.py — Class-Specific Icon Scoring

Scores every icon for each of the 15 EQ classes using stat-weighted scoring,
class-specificity multipliers, and armor-slot class-restricted filtering.

```bash
python .bin/pick_class_icons.py
```

**Input:** `eq_items.csv`
**Output:** `.Items/.cache/class_icon_picks.csv` + `.json` + `.html`

### Icon → Dragitem Formula

```
adjusted = icon - 500
file     = adjusted // 36 + 1     → dragitem file number
cell     = adjusted % 36
row      = cell % 6 + 1           → 1-based, col-major ordering
col      = cell // 6 + 1          → 1-based, col-major ordering
```

Example: Cloth Cap (icon 639) → adjusted=139, file=4 (dragitem4), cell=31,
row=2 (31%6+1), col=6 (31//6+1) → `dragitem4/r2c6.png`

## Deprecated Scripts

The following `.bin/` scripts are preserved as reference for their AI techniques
but are **no longer used** in the active pipeline:

- **generate_catalog.py** — Pixel feature analysis + iterative learning catalog
- **vision_classify.py** — CLIP / Ollama / HOG icon classification

These were superseded when we obtained the Quarm SQL database, which provides
authoritative item-to-icon mappings rather than visual guesses.

## Dependencies

- **Python 3.10+** (stdlib only — no external packages needed for the active pipeline)
