# Stat Icon Texture Regeneration (regen_icons.py)

Complete automation for regenerating, fixing, and deploying stat icon textures from icon variants.

## Overview

**Purpose:** Regenerate stat icon texture files from icon variants in the Options/Icons directory structure, with flexible label options and intelligent deployment.

**Key Features:**
- Auto-discovers all icon variants from Options/Icons/
- Flexible JSON config for icon coordinate mapping
- Extracts and resizes icons to 22×22 pixels
- Abbreviation labels within icons (text overlay)
- Optional text labels next to icons (--labels flag)
- Placeholder generation for missing icons
- Smart copyback to editing directories
- Direct deployment to thorne_dev/ for testing

---

## Quick Start

### Auto-Discover All Variants

```bash
python .bin/regen_icons.py --all
```

**What happens:**
1. Scans `thorne_drak/Options/Icons/` for all subdirectories
2. Auto-discovers all variants (e.g., Thorne, Classic, Duxa, WoW)
3. Regenerates each variant's staticons01.tga texture
4. Copies `Thorne` to `thorne_drak/` (default deployment variant)
5. Deploys `Thorne` to `thorne_dev/` for testing

**Best for:** Rapid iteration or updating all icon styles at once

### Single Variant (Most Common)

```bash
python .bin/regen_icons.py Thorne
```

**What happens:**
1. Reads source from `thorne_drak/Options/Icons/Thorne/gemicons*.tga`
2. Uses config from `.bin/regen_icons.json` for icon coordinates
3. Extracts icons, resizes to 22×22, adds abbreviation labels
4. Generates `staticons01.tga` in variant directory
5. Copies to `thorne_drak/` (for git commits)
6. Deploys to `thorne_dev/` (ready to test in-game)
7. Prints: `Ready to test in-game with: /loadskin thorne_drak`

### With Text Labels (For Editing Reference)

```bash
python .bin/regen_icons.py Thorne --labels
```

**What happens:**
1. Same as above, PLUS:
2. Renders white text labels next to each icon (x + 24px)
3. Creates labeled version for easier manual editing
4. Useful for: Identifying icons during texture editing

### Batch Regeneration

```bash
python .bin/regen_icons.py Thorne Classic Duxa WoW
```

**What happens:**
1. Regenerates ALL 4 variants
2. Only copies `Thorne` variant back to `thorne_drak/` (default deployment variant)
3. Useful for: Systematic updates across all icon styles

---

## Usage Patterns

### Workflow 1: Edit & Test Quickly

**Goal:** Edit icon coordinates, regenerate, test immediately

```bash
# 1. Edit the config coordinates
#    File: .bin/regen_icons.json

# 2. Add/update source icons
#    File: thorne_drak/Options/Icons/Thorne/gemicons*.tga

# 3. Regenerate and deploy (one step)
python .bin/regen_icons.py Thorne

# 4. Test in-game
#    Command: /loadskin thorne_drak
```

**Time to test:** ~1 second (regeneration + deployment)

### Workflow 2: Edit With Reference Labels

**Goal:** Generate texture with labels for easier editing

```bash
# 1. Generate labeled version to see icon identification
python .bin/regen_icons.py Thorne --labels

# 2. Reference the labeled version while editing gemicon files
#    File: thorne_drak/Options/Icons/Thorne/staticons01.tga

# 3. After editing, regenerate without labels for final version
python .bin/regen_icons.py Thorne

# 4. Test in-game
#    Command: /loadskin thorne_drak
```

### Workflow 3: Commit to Git

**Goal:** Regenerate, update git repository, commit

```bash
# 1. Edit/update source icons and config
# 2. Run regeneration:
python .bin/regen_icons.py Thorne

# 3. Review changes in thorne_drak/
# 4. Commit to git:
git add -A
git commit -m "feat(icons): Updated stat icon appearance"

# 5. Full sync to TAKP (if needed):
.\sync-thorne-ui.bat
```

### Workflow 4: Bulk Update All Variants

**Goal:** Regenerate all icon variants at once (auto-discover)

```bash
# One command - auto-discovers all variants in Options/Icons/
python .bin/regen_icons.py --all

# Only Thorne is copied to thorne_drak/ for deployment
# Others remain in their Options subdirectories for reference
```

**Best for:**
- Systematic updates to all icon styles
- Testing visual consistency across variants
- New variants are automatically included (future-proof)

---

## Command-Line Options

**Usage:**
```bash
python .bin/regen_icons.py --all                      # Auto-discover all variants
python .bin/regen_icons.py <variant> [variant2 ...]  # Specific variants
python .bin/regen_icons.py <variant> --labels         # With text labels
python .bin/regen_icons.py --help                     # Show help
```

**Arguments & Flags:**

- `--all` - Auto-discover and regenerate all variants from Options/Icons/ directory
  - No limits, instantly picks up new variants
  - Useful for: Bulk updates, systematic testing
  - Example: `python .bin/regen_icons.py --all`

- `<variant>` - Variant name to regenerate (required if not using --all)
  - `Thorne` - Primary development variant
  - `Classic`, `Duxa`, `WoW` - Other variants
  - Use space-separated list for multiple: `Classic Duxa Thorne`
  - Example: `python .bin/regen_icons.py Thorne`

- `--labels` - Add text labels next to each icon
  - Renders white text labels for editing reference
  - Does NOT appear in game (game uses abbreviations within icons)
  - Use with: Single variant or --all
  - Example: `python .bin/regen_icons.py Thorne --labels`

**Examples:**
```bash
python .bin/regen_icons.py --all                      # All variants (auto-discovered)
python .bin/regen_icons.py Thorne                     # Single variant
python .bin/regen_icons.py Thorne Classic             # Two variants
python .bin/regen_icons.py Thorne --labels            # With reference labels
python .bin/regen_icons.py --all --labels             # All variants with labels
python .bin/regen_icons.py --help                     # Show help message
```

---

## How It Works

### 1. Configuration

The script reads icon coordinates from `regen_icons.json`:

```json
{
  "AC": {
    "file": "gemicons01.tga",
    "x": 192,
    "y": 216,
    "w": 24,
    "h": 24,
    "description": "Armor Class"
  },
  ...
}
```

- `file`: Source gemicon file to extract from
- `x`, `y`: Top-left corner of icon in source file
- `w`, `h`: Icon size in source (typically 24×24)
- `description`: Human-readable label

### 2. Icon Extraction

For each icon in the config:
1. Loads source gemicon file (e.g., `gemicons01.tga`)
2. Extracts rectangle at (x, y, w, h)
3. Resizes to 22×22 pixels (preserves aspect ratio)
4. Falls back to placeholder if file/coordinates not found

### 3. Master Layout

Creates 256×256 output texture with fixed layout:

```
Column 1 (x=10):         Column 2 (x=90):         Column 3 (x=170):
AC (10,10)               Fire (90,10)             STR (170,10)
ATK (10,40)              Cold (90,40)             INT (170,40)
HP (10,70)               Magic (90,70)            WIS (170,70)
MANA (10,100)            Poison (90,100)          AGI (170,100)
STA (10,130)             Disease (90,130)         DEX (170,130)
Weight (10,160)          Reserve (90,160)         CHA (170,160)
```

Each icon:
- Positioned at fixed (x, y) coordinates
- Size: 22×22 pixels
- Abbreviation label overlaid on icon

### 4. Label Options

**Abbreviations Within Icons (Default):**
- Small text overlaid on bottom-right of icon
- Appears in-game on player interface
- Examples: "AC", "HP", "STR", "MP", etc.

**Text Labels Next To Icons (--labels):**
- White text rendered to the right of icon
- For editing/reference only (not used in-game)
- Helps identify which icon is which during manual texture editing

### 5. Smart Copyback

**Single variant (e.g., `Thorne`):**
- Copies generated texture to `thorne_drak/staticons01.tga`
- Ready for git commit and immediate testing

**Multiple variants (e.g., `Thorne Classic Duxa`):**
- Only copies `Thorne` to `thorne_drak/staticons01.tga`
- Others remain in their Options subdirectories
- Prevents accidentally overwriting main variant

### 6. Automatic Deployment

After copyback, automatically copies to:
- `C:\TAKP\uifiles\thorne_dev\staticons01.tga` (testing directory)

**Benefits:**
- No need to run separate sync script
- Test immediately with `/loadskin thorne_drak`
- thorne_dev/ stays isolated (manual changes won't be overwritten)

---

## Icon Specifications

### Output Texture

- **Size:** 256×256 pixels (RGBA)
- **Format:** TGA (Targa)
- **Icons:** 18 stat icons total
- **Icon Size:** 22×22 pixels each

### Icon Layout

Three columns of six icons each:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| AC       | Fire     | STR      |
| ATK      | Cold     | INT      |
| HP       | Magic    | WIS      |
| MANA     | Poison   | AGI      |
| STA      | Disease  | DEX      |
| Weight   | Reserve  | CHA      |

### Abbreviations (In-Game)

Used as text overlays on icons in the player interface:

```
AC     = Armor Class
ATK    = Attack
HP     = Hit Points
MANA/MP = Mana Points
STA/ST  = Stamina
WT     = Weight
FR     = Fire Resistance
CR     = Cold Resistance
MR     = Magic Resistance
PR     = Poison Resistance
DR     = Disease Resistance
RV     = Reserve (Dragon Resist)
STR    = Strength
INT    = Intelligence
WIS    = Wisdom
AGI    = Agility
DEX    = Dexterity
CHA    = Charisma
```

---

## Placeholder Icons

If an icon cannot be extracted (missing file or invalid coordinates):

**Placeholder appearance:**
- Dark grey square (43, 43, 43 RGBA)
- Black border (2px outer)
- Inner accent line (68, 68, 68)
- Center cross pattern

**When generated:**
- During development if gemicon files incomplete
- Obvious visual indicator to find missing icons
- Configuration is invalid or out of sync

**To fix:** Update `.bin/regen_icons.json` with correct coordinates

---

## Troubleshooting

### Error: Config file not found

**Cause:** `.bin/regen_icons.json` missing or moved

**Fix:** Verify file exists at `.bin/regen_icons.json`

### Error: Variant directory not found

**Cause:** Icon variant directory doesn't exist in Options/Icons/

**Fix:** Create directory structure:
```
thorne_drak/
  └── Options/
      └── Icons/
          └── <VariantName>/
              ├── gemicons01.tga
              ├── gemicons02.tga
              └── ...
```

### Icons look wrong (coordinates off)

**Cause:** Gemicon file changed or coordinates in config are wrong

**Fix:** Update `.bin/regen_icons.json` with correct icon coordinates

**To find coordinates:**
1. Open gemicon file in image editor (GIMP, Photoshop)
2. Measure icon position (x, y)
3. Note size (usually 24×24)
4. Update config JSON

### Text labels not visible with --labels

**Cause:** White text on transparent background not visible

**Fix:** Expected behavior - labels render on transparent areas
- Labels intended for editing reference only
- View in image editor like GIMP to see them
- In-game display only shows abbreviations within icons

### thorne_dev/ deployment failed

**Cause:** Directory path or permissions issue

**Fix:** Check that `C:\TAKP\uifiles\thorne_dev\` exists and is writable

---

## Configuration Examples

### Standard Icon (From Gemicon File)

```json
"AC": {
  "file": "gemicons01.tga",
  "x": 192,
  "y": 216,
  "w": 24,
  "h": 24,
  "description": "Armor Class"
}
```

### Custom Size Icon

```json
"CustomIcon": {
  "file": "customicons.tga",
  "x": 0,
  "y": 0,
  "w": 32,
  "h": 32,
  "description": "Custom 32x32 Icon"
}
```

The script automatically resizes any size to 22×22 for output.

### Icon Not Found (Placeholder)

```json
"FutureIcon": {
  "file": "icons_v2.tga",
  "x": 0,
  "y": 0,
  "w": 24,
  "h": 24,
  "description": "Not yet implemented"
}
```

If `icons_v2.tga` doesn't exist, generates placeholder instead of crashing.

---

## Related Documentation

- [.bin/README.md](.bin/README.md) - Script index
- [.bin/STANDARDS.md](STANDARDS.md) - Script documentation standards
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Phase 3.9 icon redesign details
- [.docs/STANDARDS.md](../.docs/STANDARDS.md) - UI design standards
- [regen_icons.json](regen_icons.json) - Icon coordinate configuration

---

## Advanced: Batch Processing

### Generate multiple variants with labels for editing

```bash
python .bin/regen_icons.py Classic Duxa Thorne --labels
```

Results in:
- `thorne_drak/Options/Icons/Classic/staticons01.tga` (with labels)
- `thorne_drak/Options/Icons/Duxa/staticons01.tga` (with labels)  
- `thorne_drak/Options/Icons/Thorne/staticons01.tga` (with labels)
- `thorne_drak/staticons01.tga` (with labels - Thorne copy)
- `C:\TAKP\uifiles\thorne_dev\staticons01.tga` (with labels - deployment)

### Generate all variants, then specific variant without labels

```bash
# Generate all with labels for reference
python .bin/regen_icons.py --all --labels

# Edit and finalize Thorne variant
python .bin/regen_icons.py Thorne
```

This workflow allows:
1. View all variants with labels (editing reference)
2. Focus on Thorne variant without labels (production version)
3. Selective deployment while keeping all variants updated

