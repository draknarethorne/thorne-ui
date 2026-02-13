# Gauge Texture Regeneration (regen_gauges.py)

Complete automation for regenerating, fixing, and deploying gauge textures.

## Overview

**Purpose:** Regenerate tall (120×64) and wide (120×32) gauge textures from source files, with automatic format fixing and intelligent deployment.

**Key Features:**
- Regenerates both tall and wide gauges in one command
- Automatic TGA format fixing (converts mislabeled PNG→TGA)
- Smart copyback to editing directories
- Direct deployment to thorne_dev/ for testing
- Supports single variants or batch regeneration
- BILINEAR interpolation for fills, NEAREST for crisp lines

---

## Quick Start

### Single Variant (Most Common)

```bash
python .bin/regen_gauges.py Thorne
```

**What happens:**
1. Reads source from `thorne_drak/Options/Gauges/Thorne/gauge_pieces01.tga`
2. Fixes TGA format if needed (PNG→TGA conversion)
3. Regenerates `gauge_pieces01_tall.tga` and `gauge_pieces01_wide.tga`
4. Copies both to `thorne_drak/` (for git commits)
5. Deploys both to `thorne_dev/` (ready to test in-game)
6. Prints: `Ready to test in-game with: /loadskin thorne_drak`

### Batch Regeneration

```bash
python .bin/regen_gauges.py root Bars Basic Bubbles "Light Bubbles" Thorne
```

**What happens:**
1. Regenerates ALL 6 variants
2. Only copies `Thorne` variant back to `thorne_drak/` (default deployment variant)
3. Useful for: Systematic updates across all gauge styles

---

## Usage Patterns

### Workflow 1: Edit & Test Quickly

**Goal:** Edit a gauge variant locally, test immediately in-game

```bash
# 1. Edit the source file
#    File: thorne_drak/Options/Gauges/Thorne/gauge_pieces01.tga

# 2. Regenerate and deploy (one step)
python .bin/regen_gauges.py Thorne

# 3. Test in-game
#    Command: /loadskin thorne_drak
```

**Time to test:** ~1 second (regeneration + deployment)

### Workflow 2: Commit to Git

**Goal:** Regenerate, update git repository, then full sync

```bash
# 1. Edit source gauge in Options directory
# 2. Run:
python .bin/regen_gauges.py Thorne

# 3. Review changes in thorne_drak/
# 4. Commit to git:
git add -A
git commit -m "refactor(gauges): Updated Thorne gauge appearance"

# 5. Full sync to TAKP (if needed):
.\sync-thorne-ui.bat
```

### Workflow 3: Batch Update Multiple Variants

**Goal:** Regenerate all gauge variants, only deploy current work variant

```bash
# Check all variants are visually consistent
python .bin/regen_gauges.py root Bars Basic Bubbles "Light Bubbles" Thorne

# Only Thorne is copied to thorne_drak/ for deployment
# Others are regenerated in their Options subdirectory for reference
```

---

## Command-Line Options

```bash
python .bin/regen_gauges.py <variant> [variant2 ...]
```

**Arguments:**
- `variant` - Variant name to regenerate (required, can specify multiple)
  - `Thorne` - Primary development variant
  - `Bars`, `Basic`, `Bubbles`, `Light Bubbles`, `root` - Other variants
  - Use space-separated list for multiple: `Bars Basic Thorne`

**Examples:**
```bash
python .bin/regen_gauges.py Thorne              # Single variant
python .bin/regen_gauges.py Bars Basic          # Two variants
python .bin/regen_gauges.py root Thorne         # Root + Thorne
```

---

## How It Works

### 1. Source File Detection

The script looks for `gauge_pieces01.tga` in:
- `thorne_drak/Options/Gauges/<Variant>/` for named variants
- `thorne_drak/` for "root" variant

### 2. TGA Format Fixing

If source file is actually PNG (mislabeled):
- Detects PNG signature automatically
- Converts to proper TGA format (RGBA)
- Prints: `Fixed: gauge_pieces01.tga (converted from PNG to TGA)`

### 3. Gauge Generation

**Tall Gauges (120×64):**
- Extracts 4 sections (8px tall each) from source
- Scales vertically: 8px → 16px
- Splits each section: 1px border + middle + 1px border
- Borders use NEAREST (crisp)
- Middle uses BILINEAR (smooth fill)
- Lines section uses NEAREST (crisp edges)

**Wide Gauges (120×32):**
- Extracts 4 sections (8px tall each) from source
- Scales horizontally: ~60px → 120px
- Same border/middle preservation as tall gauges
- Result: 120×32 texture (perfect for stamina gauge)

### 4. Smart Copyback

**Single variant (e.g., `Thorne`):**
- Copies generated textures to `thorne_drak/`
- Ready for git commit and immediate testing

**Multiple variants (e.g., `root Bars Basic Bubbles Light Bubbles Thorne`):**
- Only copies `Thorne` to `thorne_drak/`
- Others remain in their Options subdirectories
- Prevents accidentally overwriting main variant

**Root variant:**
- No copyback (already in main location)

### 5. Automatic Deployment

After copyback, automatically copies to:
- `C:\TAKP\uifiles\thorne_dev\` (testing directory)

**Benefits:**
- No need to run separate sync script
- Test immediately with `/loadskin thorne_drak`
- thorne_dev/ stays isolated (manual changes won't be overwritten)

---

## Gauge Specifications

### Texture Dimensions

**Tall Gauges:**
- Size: 120×64 pixels
- Sections: 4 × 16px tall
- Y positions: 0, 16, 32, 48
- Used for: HP, Mana, XP, AAXP, Pet HP

**Wide Gauges:**
- Size: 120×32 pixels
- Sections: 4 × 8px tall
- Y positions: 0, 8, 16, 24
- Used for: Stamina (no vertical cropping needed)

### Gauge Sections

All gauges have 4 sections (Y-stacked):

1. **Background** (Y=0) - Gauge outline/background
2. **Fill** (Y=16/8) - Colored fill bar
3. **Lines** (Y=32/16) - Outline or detail lines
4. **LinesFill** (Y=48/24) - Filled version of lines

### Interpolation

When scaling:

- **Borders (1px):** NEAREST
  - Preserves pixel-perfect edges
  - No blurring or artifacts

- **Fills/Background:** BILINEAR
  - Smooth gradient appearance
  - No ringing artifacts (better than LANCZOS)

- **Lines/LinesFill:** NEAREST
  - Crisp, clean lines
  - No blurred edges

---

## Troubleshooting

### Error: TGA file conversion failed

**Cause:** File is corrupted or not actually PNG

**Fix:** Re-export the gauge file from source tool (GIMP, Photoshop, etc.)

### Gauges look blurry

**Cause:** BILINEAR interpolation enabled for lines

**Fix:** This is intentional for fills. Lines section should use NEAREST (check XML animations)

### File is stuck in PNG format

**Cause:** TGA format conversion didn't work

**Fix:** Manually convert:
```python
from PIL import Image
img = Image.open('file.tga')
img.convert('RGBA').save('file.tga', format='TGA')
```

### thorne_dev/ deployment failed

**Cause:** Directory path or permissions issue

**Fix:** Check that `C:\TAKP\uifiles\thorne_dev\` exists and is writable

---

## Advanced: Interpolation Methods

The script supports configurable interpolation. To use different methods, edit the script:

**Current defaults in regen_gauges.py:**
```python
# Tall gauge scaling
bg_tall = scale_with_borders(bg, std_width, interp_method="BILINEAR")
fill_tall = scale_with_borders(fill, std_width, interp_method="BILINEAR")
lines_tall = scale_with_borders(lines, std_width, interp_method="NEAREST")

# Wide gauge scaling  
bg_wide = scale_horizontal_with_borders(bg, interp_method="BILINEAR")
fill_wide = scale_horizontal_with_borders(fill, interp_method="BILINEAR")
lines_wide = scale_horizontal_with_borders(lines, interp_method="NEAREST")
```

**Available methods:**
- `"BILINEAR"` - Balanced smoothness (default for fills)
- `"LANCZOS"` - Very smooth (can cause ringing artifacts)
- `"NEAREST"` - Crisp pixels (default for lines)

To experiment: Change the `interp_method=` parameter and re-run the script.

---

## Related Documentation

- [.bin/README.md](.bin/README.md) - Script index
- [.bin/STANDARDS.md](STANDARDS.md) - Script documentation standards
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Phase 3.9 gauge redesign details
- [.docs/STANDARDS.md](../.docs/STANDARDS.md) - UI design standards

