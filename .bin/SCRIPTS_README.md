# Stat Icon Scripts

Scripts for generating stat icon texture files with flexible source variants and abbreviations.

## PRIMARY WORKFLOW

### `generate_stat_icons.py` **MAIN TOOL**

Complete one-step script for generating stat icon files from any icon variant.

**Features:**
- Reads icon coordinates from flexible JSON config
- Extracts icons from gemicon files in source directory
- Resizes from 24×24 to 22×22 pixels
- Places in 256×256 template at master layout positions
- **Adds abbreviation labels automatically** (no separate step)
- Generates placeholder graphics for missing icons
- Works with any icon variant (Classic, Duxa, Modern, WoW, etc.)

**Usage:**

```bash
# Generate stat icons for Classic variant with abbreviations
python .bin/generate_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Classic \
  --config .development/stat-icons-config.json \
  --output thorne_drak/stat_icon_pieces01.tga \
  --add-abbreviations

# Generate for Duxa variant
python .bin/generate_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Duxa \
  --config .development/stat-icons-config.json \
  --output thorne_drak/stat_icon_pieces_duxa.tga \
  --add-abbreviations
```

**Command-line Options:**
- `--source-dir`: Source directory containing gemicon files (required)
- `--config`: JSON config file with icon mappings (default: `.development/stat-icons-config.json`)
- `--output`: Output file path (required)
- `--add-abbreviations`: Add abbreviation labels to icons

**Output:**
- `stat_icon_pieces*.tga`: Generated stat icon texture file (256×256 RGBA)
- `*-stats.json`: Generation statistics and source information

---

## SUPPORTING TOOLS

### `add_abbreviations_to_textures.py`

If you need to add abbreviations to already-generated texture files.

**Usage:**
```bash
python .bin/add_abbreviations_to_textures.py --input stat_icon_pieces01.tga --output output.tga
```

**Note:** The `generate_stat_icons.py` script does this automatically with `--add-abbreviations` flag.

### `validate_stat_icons.py`

Validate stat icon texture files for errors and consistency.

**Usage:**
```bash
python .bin/validate_stat_icons.py thorne_drak/stat_icon_pieces01.tga
```

---

## ARCHIVE TOOLS

The following tools are in `.bin/archive/` for reference and maintenance:

- **`analyze_gemicons.py`** - Analyzes gemicon layout and creates reference guides
- **`detect_gemicon_grid.py`** - Visual grid mapper for identifying icon positions
- **`extract_gemicon_coordinates.py`** - Documentation tool for gem icon coordinates
- **`generate_abbreviation_reference.py`** - Creates standalone abbreviation reference guides
- **`generate_master_stat_icons.py`** - Original version with hard-coded paths (replaced by new workflow)

These were discovery/analysis tools used during development. They're kept for reference but not needed for regular stat icon generation.

---

## Icon Abbreviations

The stat icon template includes 18 icons in a 3×6 grid:

**Column 1 - Combat Stats**
- AC (Armor Class)
- ATK (Attack)
- HP (Hit Points)
- MP (Mana Points)
- ST (Stamina)
- WT (Weight)

**Column 2 - Resistances**
- FR (Fire)
- CR (Cold)
- MR (Magic)
- PR (Poison)
- DR (Disease)
- RV (Reserve)

**Column 3 - Attributes**
- STR (Strength)
- INT (Intelligence)
- WIS (Wisdom)
- AGI (Agility)
- DEX (Dexterity)
- CHA (Charisma)

---

## Configuration File

The `.development/stat-icons-config.json` file is fully flexible:

```json
{
  "IconName": {
    "file": "which_gemicon_or_spells_file.tga",
    "x": 0,
    "y": 0,
    "w": 24,
    "h": 24,
    "description": "Optional description"
  }
}
```

This allows:
- Referencing different source files
- Any pixel coordinates within the source files
- Full flexibility to support multiple UI variants with different icon sources
- Easy maintenance and documentation

---

## Installation

These scripts require:
- Python 3.6+
- PIL/Pillow (for texture editing): `pip install Pillow`

All other dependencies are standard library.
