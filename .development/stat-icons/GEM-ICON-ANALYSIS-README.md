# Gem Icon Analysis Tools

## Overview

You were right that the gemicon icons are **larger than stat icons**. Here's what I found:

### Icon Sizing

- **Gemicon source icons**: 24×24 pixels
- **Stat icon destinations**: 22×22 pixels
- **Operation**: Extract 24×24 from gemicons → Resize to 22×22 → Place in stat_icons

This is exactly how the existing `generate_master_stat_icons.py` script works - it pulls 24×24 icons and automatically resizes them.

## Analysis Tools Created

### 1. `analyze_gemicons.py`

Analyzes gemicon texture files and creates a comprehensive reference guide.

**Usage:**
```bash
python .bin/analyze_gemicons.py --source default
```

**Output:**
- Console display with gemicon analysis
- JSON reference file: `.development/gemicon-analysis.json`
- Shows estimated icon count and layout
- Lists actual coordinates of existing resist icons (Fire, Cold, Magic, Poison, Disease)
- Provides suggestions for where to look for missing icons

**Key Data:**
```
Gemicons: 256×256 texture
Icon size: 24×24 pixels
Grid layout: ~10-11 icons per row/column
Total icons per file: 100-120

Existing extractions (gemicons01.tga):
  Fire:     (48, 120)   24×24 → resize to 22×22 → place at (90, 10)
  Cold:     (168, 120)  24×24 → resize to 22×22 → place at (90, 40)
  Magic:    (216, 144)  24×24 → resize to 22×22 → place at (90, 70)
  Poison:   (24, 144)   24×24 → resize to 22×22 → place at (90, 100)
  Disease:  (120, 144)  24×24 → resize to 22×22 → place at (90, 130)
```

### 2. `detect_gemicon_grid.py`

Creates a visual grid overlay showing 24×24 icon cells and marks which cells contain icons.

**Usage:**
```bash
python .bin/detect_gemicon_grid.py --file default/gemicons01.tga --grid-size 24 --export grid_map.png
```

**Output:**
- PNG visualization with red grid lines (24×24 cells)
- Green dots mark cells with opaque content (actual icons)
- Helps visually identify icon positions without manual searching
- Console summary of grid analysis

**Example:**
```
Loaded gemicons01.tga (256x256)
Detected icon size: 20x20 pixels (from spacing analysis)
Grid analysis: 10 icons per row × 10 per column = 100 cells
Saved visualization: gemicon_grid_map.png
```

## Workflow for Finding Missing Icons

### Step 1: Visualize the Grid
```bash
python .bin/detect_gemicon_grid.py --file default/gemicons01.tga \
                                   --grid-size 24 \
                                   --export gemicons01_grid.png
```

### Step 2: Identify Icons Manually
Open the generated PNG in an image viewer:
- Red grid shows 24×24 cell boundaries
- Green dots mark cells with icon content
- Allows you to visually locate specific icon types

### Step 3: Extract Coordinates
Open the actual gemicon*.tga file in an image editor (Photoshop, GIMP):
- Find icons matching missing stat types (HP heart, MANA orb, etc.)
- Note exact pixel coordinates
- Verify they're roughly 24×24 pixels

### Step 4: Update Extraction Rules
Edit `generate_master_stat_icons.py`:

```python
# Add to PIECES02_SOURCES or PIECES03_SOURCES
PIECES02_SOURCES = {
    # ... existing entries ...
    "HP":      {"file": "vert-blue/gemicons01.tga", "x": 96,  "y": 72,  "w": 24, "h": 24},
    "MANA":    {"file": "vert-blue/gemicons01.tga", "x": 48,  "y": 48,  "w": 24, "h": 24},
    # ... etc ...
}
```

### Step 5: Generate Files
Run the generation script:
```bash
python .bin/generate_master_stat_icons.py
```

The script automatically:
- Extracts the 24×24 source icon
- Resizes to 22×22
- Places at correct position in stat_icon_pieces file
- Creates placeholder for any remaining missing icons

## Integration with Existing Scripts

The analysis tools work seamlessly with your existing infrastructure:

### Extraction Pipeline
```
gemicons*.tga files (24×24 icons)
    ↓ (detect_gemicon_grid.py) - Visual reference
    ↓ (analyze_gemicons.py) - Coordinate documentation  
    ↓ (generate_master_stat_icons.py) - Extract 24×24 → Resize to 22×22
    ↓
stat_icon_pieces*.tga files (22×22 icons in 256×256 template)
    ↓
add_abbreviations_to_textures.py - Add labels
    ↓
Final stat_icons with labels and abbreviations
```

## Corrected Understanding

### What Was Initially Wrong
My first grid detector assumed 20×20 icons (incorrect) because it was looking at spacing patterns that didn't clearly identify the actual icon boundaries.

### What's Actually True
- Gemicons contain **24×24 pixel icons** with small spacing
- 256px ÷ 24px = ~10-11 icons per dimension
- Each file contains roughly 100-120 icons total
- The reduce-to-22×22 step is **intentional** and built into `generate_master_stat_icons.py`
- This sizing mismatch is NOT a problem - it's by design to allow slight compression without quality loss

## Missing Stat Icons (To Be Extracted)

Currently using placeholder graphics for:
- **HP** (Hit Points) - need red heart or healing icon
- **MANA** (Mana Points) - need blue orb or flask icon
- **STA** (Stamina) - need lungs or endurance icon
- **Weight** - need scale or balance icon
- **STR** (Strength) - need fist or weapon icon
- **INT** (Intelligence) - need book or scroll icon
- **WIS** (Wisdom) - need eye or spirit icon
- **AGI** (Agility) - need lightning or movement icon
- **DEX** (Dexterity) - need crosshair or precision icon
- **CHA** (Charisma) - need star or sparkle icon

For each, the workflow is:
1. Run `detect_gemicon_grid.py` to see all available icons
2. Find the best match visually in gemicons01.tga/02.tga/03.tga
3. Note coordinates in image editor (ensure ~24×24 size)
4. Add to `PIECES*_SOURCES` in `generate_master_stat_icons.py`
5. Run script to generate files

## Future Automation

Once you've manually identified several icons, we could potentially:
- Create a visual comparison tool matching gem icons to stat icon types
- Build a database of "best matches" across UI variants
- Automate the extraction by recognizing icon patterns
- Generate a visual report showing all available gem icons with suggestions

For now, the grid visualization tool provides a solid foundation for manual discovery!
