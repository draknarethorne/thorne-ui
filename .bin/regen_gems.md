# Gem Icon Regeneration (regen_gems.py)

Complete automation for regenerating gemicons and spell icon textures from source spell files.

## Overview

**Purpose:** Generate `gemicons*.tga` (24×24) and `spell_icons_thorne*.tga` (22×22) from source `spells*.tga` files in each icon variant. Automatically triggers stat icon regeneration after completion.

**Key Features:**
- Full pipeline: spells → gemicons + spell icons → stat icons (chained)
- Three border modes for gemicon appearance (transparent, black, blend)
- LANCZOS downscaling + SHARPEN pass for high-quality icons
- Auto-discovers variants by scanning for `spells*.tga` source files
- Smart copyback to `thorne_drak/` and deployment to `thorne_dev/`
- Writes statistics JSON per variant

---

## Quick Start

### Auto-Discover All Variants

```bash
python .bin/regen_gems.py --all
```

**What happens:**
1. Scans `thorne_drak/Options/Icons/` for all subdirectories with `spells*.tga` files
2. Auto-discovers all variants (e.g., Thorne, Classic, Duxa, WoW)
3. Extracts 36 icons per spell file → generates `gemicons*.tga` and `spell_icons_thorne*.tga`
4. Triggers `regen_icons.py <variant>` for each variant (stat icons auto-updated)
5. Copies `Thorne` to `thorne_drak/` (default deployment variant)
6. Deploys `Thorne` to `thorne_dev/` for testing

**Best for:** Rapid iteration or updating all icon styles at once

### Single Variant (Most Common)

```bash
python .bin/regen_gems.py Thorne
```

**What happens:**
1. Reads `spells*.tga` from `thorne_drak/Options/Icons/Thorne/`
2. Extracts all icons (40×40 each, 6×6 grid per file)
3. Scales to 24×24 → saves `gemicons01.tga`, `gemicons02.tga`, `gemicons03.tga`
4. Scales to 22×22 → saves `spell_icons_thorne01.tga` etc.
5. Automatically runs `regen_icons.py Thorne` (stat icons updated)
6. Copies gemicons and spell_icons_thorne to `thorne_drak/`
7. Deploys to `thorne_dev/` for testing

### With Border Mode

```bash
python .bin/regen_gems.py Thorne --border blend
python .bin/regen_gems.py Thorne --border black
python .bin/regen_gems.py --all --border transparent
```

Border mode only affects **gemicons** (24×24). `spell_icons_thorne` always uses plain scaling.

### Multiple Variants

```bash
python .bin/regen_gems.py Thorne Classic Duxa
```

**What happens:**
1. Regenerates all 3 variants
2. Only copies `Thorne` to `thorne_drak/` (smart copyback — see below)
3. Others remain in their Options subdirectories

---

## Usage Patterns

### Workflow 1: Edit Spell Icons & Rebuild

**Goal:** You've edited a `spells*.tga` source file and want to rebuild everything downstream.

```bash
# 1. Edit the source file
#    File: thorne_drak/Options/Icons/Thorne/spells01.tga

# 2. Rebuild the full pipeline (one command)
python .bin/regen_gems.py Thorne

# 3. Test in-game
#    Command: /loadskin thorne_dev
```

All three outputs rebuild automatically: gemicons → spell_icons_thorne → stat_icons_thorne.

### Workflow 2: Test Border Styles

**Goal:** Compare how border treatments look in-game.

```bash
# Default (transparent border — 1px padding around 22×22 content)
python .bin/regen_gems.py Thorne

# Darkened 1px edge (blend — darkens outermost pixels by 40%)
python .bin/regen_gems.py Thorne --border blend

# Hard black 1px edge
python .bin/regen_gems.py Thorne --border black
```

Border mode is a visual preference — try all three and use `/loadskin thorne_dev` to compare in-game.

### Workflow 3: Bulk Rebuild All Variants

```bash
python .bin/regen_gems.py --all
```

Use this after updating spell icon source files across multiple variants, or when checking visual consistency across all icon styles.

---

## Command-Line Options

**Usage:**
```bash
python .bin/regen_gems.py --all                             # Auto-discover all variants
python .bin/regen_gems.py <variant> [variant2 ...]          # Specific variants
python .bin/regen_gems.py <variant> --border <mode>         # With border mode
python .bin/regen_gems.py --help                            # Show help
```

**Arguments & Flags:**

- `--all` — Auto-discover and regenerate all variants from `Options/Icons/`
  - Discovers variants by checking for `spells*.tga` files
  - Future-proof: new variant directories are picked up automatically

- `variant` — Variant name(s) to regenerate (positional, space-separated)
  - `Thorne` — Primary development variant
  - `Classic`, `Duxa`, `WoW` — Other variants (if present)

- `--border <mode>` — Gemicon border treatment (default: `transparent`)
  - `transparent` — 1px transparent padding; no edge treatment on content
  - `blend` — Outermost content pixels darkened to 60% brightness (subtle definition)
  - `black` — Hard 1px solid black border around content
  - Using `--border` alone (no value) defaults to `blend`

**Examples:**
```bash
python .bin/regen_gems.py --all                    # All variants, default border
python .bin/regen_gems.py Thorne                   # Single variant
python .bin/regen_gems.py Thorne Classic           # Two variants
python .bin/regen_gems.py Thorne --border blend    # Blended border
python .bin/regen_gems.py --all --border black     # All with black border
python .bin/regen_gems.py --help                   # Show help message
```

---

## How It Works

### 1. Source File Structure

**Spell files** (`spells01.tga`, `spells02.tga`, ...):
- 256×256 pixels each
- 6×6 grid of 40×40 icons = 36 icons per file
- Remaining buffer pixels (16px) on right and bottom

Variant directories are discovered by scanning for `spells*.tga` in each subdirectory of `Options/Icons/`.

### 2. Gemicon Generation (24×24)

For each extracted 40×40 icon:
1. Scale to 22×22 using LANCZOS (high-quality downscaling)
2. Apply SHARPEN filter (compensates for downscale blur)
3. Apply border treatment (transparent / blend / black)
4. Paste into 24×24 canvas at (1,1) — 1px transparent margin on all sides

**Output grid:** 10×10 = 100 icons per file at 24px → 240px used of 256px (16px buffer)

**Files created:** `gemicons01.tga`, `gemicons02.tga`, `gemicons03.tga`

### 3. Spell Icon Generation (22×22)

For each extracted 40×40 icon:
1. Scale to 22×22 using LANCZOS
2. Apply SHARPEN filter

No border treatment — these are used for stat icon generation (regen_icons.py reads these).

**Output grid:** 10×10 = 100 icons per file at 22px → 220px used of 256px (36px buffer)

**Files created:** `spell_icons_thorne01.tga`, `spell_icons_thorne02.tga`, `spell_icons_thorne03.tga`

### 4. Chained Stat Icon Regeneration

After generating `spell_icons_thorne*.tga`, the script automatically calls:
```
regen_icons.py <variant>
```

This regenerates `stat_icons_thorne01.tga` in the variant directory without needing a separate command.

### 5. Smart Copyback

**Single variant (e.g., `Thorne`):**
- Copies `gemicons*.tga` and `spell_icons_thorne*.tga` to `thorne_drak/`

**Multiple variants (e.g., `Thorne Classic Duxa`):**
- Only copies `Thorne` to `thorne_drak/`
- Others stay in their Options subdirectories

### 6. Automatic Deployment

After copyback, copies to `C:\TAKP\uifiles\thorne_dev\` for immediate in-game testing.

---

## Output Files

Per variant, the following files are written to `thorne_drak/Options/Icons/<Variant>/`:

| File | Size | Grid | Content |
|------|------|------|---------|
| `gemicons01.tga` | 256×256 | 10×10 | Icons 1–100 (24×24 with 1px border) |
| `gemicons02.tga` | 256×256 | 10×10 | Icons 101–200 |
| `gemicons03.tga` | 256×256 | 10×10 | Icons 201–300 |
| `spell_icons_thorne01.tga` | 256×256 | 10×10 | Icons 1–100 (22×22) |
| `spell_icons_thorne02.tga` | 256×256 | 10×10 | Icons 101–200 |
| `spell_icons_thorne03.tga` | 256×256 | 10×10 | Icons 201–300 |
| `.regen_gems-stats.json` | — | — | Processing statistics |

---

## Statistics JSON

Each run writes `.regen_gems-stats.json` to the variant directory:

```json
{
  "variant": "Thorne",
  "spell_files_processed": 3,
  "icons_scaled": 108,
  "gemicon_files_created": 2,
  "spellicon_files_created": 2,
  "border_mode": "transparent"
}
```

---

## Troubleshooting

### Error: No spell files found

**Cause:** Variant directory doesn't contain any `spells*.tga` files.

**Fix:** Ensure source files are named `spells01.tga`, `spells02.tga`, etc. (not `spell_icons*.tga` or other names).

### Gemicons look pixelated

**Cause:** Downscaling from 40×40 to 24×24 loses detail.

**Fix:** The LANCZOS + SHARPEN pass is the best available. If icons look too soft, try `--border blend` to add definition. If still unsatisfactory, the source spell icon quality may need improvement.

### Stat icons not updating

**Cause:** `regen_icons.py` not found or failed silently.

**Fix:** Check that `.bin/regen_icons.py` exists. Run manually to see errors:
```bash
python .bin/regen_icons.py Thorne
```

### thorne_dev/ deployment failed

**Cause:** Directory path or permissions issue.

**Fix:** Check that `C:\TAKP\uifiles\thorne_dev\` exists and is writable.

---

## Related Documentation

- [README.md](README.md) — Script index
- [regen_icons.md](regen_icons.md) — Downstream stat icon regeneration
- [STANDARDS.md](STANDARDS.md) — Script documentation standards
- [DEVELOPMENT.md](../DEVELOPMENT.md) — Project roadmap and phase details
