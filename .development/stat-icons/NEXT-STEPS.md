# Stat Icons: Next Steps

**Date:** 2026-02-15  
**Status:** Ready to locate missing icon coordinates  
**Goal:** Complete v0.7.0 stat-icons feature for Inventory window

---

## Summary

The stat-icons system is **partially complete**. You have:

✅ **Completed:**
- Master layout defined (18 icon positions in 3-column grid)
- Three texture files generated with available icons
- Regeneration and validation scripts ready

⏳ **Pending:**
- **9 missing icon coordinates** from gemicon source files
- Window integration (Inventory, Player, etc.)

---

## Step 1: Locate Missing Icon Coordinates

### What You Need to Find

**Missing icons (9 total):**

| Icon | Column | Position | Size | Search Hints |
|------|--------|----------|------|--------------|
| **AC** | 1 | (needs coords) | 24×24 | Shield or armor icon |
| **ATK** | 1 | (needs coords) | 24×24 | Sword or weapon icon |
| **HP** | 1 | (needs coords) | 24×24 | Red heart or health vial |
| **MANA** | 1 | (needs coords) | 24×24 | Blue orb or mana flask |
| **STA** | 1 | (needs coords) | 24×24 | Lungs or wind icon |
| **Weight** | 1 | (needs coords) | 24×24 | Scale or backpack icon |
| **AGI** | 3 | (needs coords) | 24×24 | Feather or running figure |
| **DEX** | 3 | (needs coords) | 24×24 | Hand or precise tool |
| **CHA** | 3 | (needs coords) | 24×24 | Star or speech bubble |

### Where to Look

**Primary sources (check in order):**

1. **`default/gemicons01.tga`** (256×256)
   - Most likely to have all combat/stat icons
   - Grid: ~10 icons per row × 10 per column
   - Cell size: 24×24 pixels

2. **`default/gemicons02.tga`** (256×256)
   - Secondary icon set
   - Similar grid layout

3. **`default/gemicons03.tga`** (256×256)
   - Extended icon set (if exists)

4. **`duxaUI/window_pieces22.tga`** (256×256)
   - Alternative icon source with stat icons
   - Check archive docs for analysis results

---

## Step 2: Manual Icon Discovery Process

### Method A: Visual Inspection (Recommended)

1. **Open gemicons files in image viewer**
   ```bash
   # Navigate to default directory
   cd C:\Thorne-UI\default
   
   # Open in your preferred image viewer
   # (Windows Photos, GIMP, Photoshop, etc.)
   ```

2. **Scan for recognizable icons**
   - Look for shield (AC), sword (ATK), heart (HP)
   - Icons are typically 24×24 pixels
   - Usually arranged in grid pattern

3. **Measure coordinates**
   - Use image editor with pixel ruler (GIMP, Photoshop)
   - Note top-left corner coordinates (X, Y)
   - Verify size is 24×24 pixels

### Method B: Grid Detection Script (Automated)

**Check archive for analysis tools:**
```bash
cd "C:\Thorne-UI\.development\stat-icons\archive"
cat GEM-ICON-ANALYSIS-README.md
```

**Possible tools mentioned:**
- `analyze_gemicons.py` - Shows gemicon analysis
- `detect_gemicon_grid.py` - Creates visual grid overlay

Run these if they exist in `.bin/archive/` or `.bin/`

---

## Step 3: Update Configuration File

**File:** `.development/stat-icons-config.json`

### Current State (Incomplete)

All missing icons have placeholder coordinates `(0, 0)`:

```json
{
  "AC": {
    "file": "gemicons01.tga",
    "x": 0,        // ← NEEDS UPDATE
    "y": 0,        // ← NEEDS UPDATE
    "w": 24,
    "h": 24
  },
  "HP": {
    "file": "gemicons01.tga",
    "x": 0,        // ← NEEDS UPDATE
    "y": 0,        // ← NEEDS UPDATE
    "w": 24,
    "h": 24
  }
  // ... etc for all 9 missing icons
}
```

### What to Update

Once you find an icon:

1. **Note source file** (e.g., `gemicons01.tga`)
2. **Note coordinates** (e.g., X=48, Y=96)
3. **Verify size** (should be 24×24)
4. **Update JSON:**

```json
{
  "AC": {
    "file": "gemicons01.tga",  // ← Source file name
    "x": 48,                    // ← Top-left X coordinate
    "y": 96,                    // ← Top-left Y coordinate
    "w": 24,                    // ← Width (24px)
    "h": 24                     // ← Height (24px)
  }
}
```

---

## Step 4: Regenerate Texture Files

**After updating coordinates in `stat-icons-config.json`:**

```bash
cd C:\Thorne-UI

# Regenerate all three stat_icon_pieces files
python .bin/regen_stat_icons.py

# Validate coordinate consistency
python .bin/validate_stat_icons.py
```

**Expected output:**
```
✅ stat_icon_pieces01.tga - 18/18 positions valid
✅ stat_icon_pieces02.tga - 18/18 positions valid  
✅ stat_icon_pieces03.tga - 18/18 positions valid
✅ Cross-file consistency - PASS
```

---

## Step 5: Window Integration (Inventory Window)

**After texture files are complete:**

### Create Animation Definitions

**File:** `thorne_drak/EQUI_InventoryWindow.xml`

Add animation definitions for each icon:

```xml
<!-- Stat Icon Animations -->
<Ui2DAnimation item="A_IW_STRIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>170</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<Ui2DAnimation item="A_IW_INTIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>170</X><Y>40</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- ... repeat for all 18 icons -->
```

### Wire Icons to Stat Displays

Add `StaticAnimation` elements in stat blocks:

```xml
<!-- Example: STR stat line with icon -->
<StaticAnimation item="IW_STR_Icon">
  <ScreenID>IW_STR_Icon</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>5</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
  <Animation>A_IW_STRIcon</Animation>
</StaticAnimation>

<Label item="IW_STR_Label">
  <ScreenID>IW_STR_Label</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>30</X><Y>10</Y></Location>
  <Size><CX>30</CX><CY>14</CY></Size>
  <Text>STR</Text>
</Label>

<Label item="IW_STR_Value">
  <ScreenID>IW_STR_Value</ScreenID>
  <EQType>122</EQType>  <!-- Player STR stat -->
  <RelativePosition>true</RelativePosition>
  <Location><X>65</X><Y>10</Y></Location>
  <Size><CX>40</CX><CY>14</CY></Size>
</Label>
```

### Create Options Variants

**Three layout options:**

1. **Text-only** (current baseline) - No icons
2. **Icon-only** - Icon + value, no text labels
3. **Icon+Text** - Icon + text label + value (full display)

---

## Step 6: Testing & Validation

### In-Game Testing

1. **Load Thorne UI variant in-game**
2. **Open Inventory window**
3. **Verify icon display:**
   - Icons appear at correct positions
   - Icons align with stat values
   - No visual glitches or overlaps

### Test All Options Variants

```
Options/Icons/
  Text-only/      # No icons (baseline)
  Icon-only/      # Icons + values only
  Icon-Text/      # Icons + text + values
```

Switch between variants and verify layout consistency.

---

## Step 7: Documentation & PR

### Update Documentation

1. **Window-specific docs:** Create `EQUI_InventoryWindow.md`
2. **Update DEVELOPMENT.md:** Mark stat-icons v0.7.0 complete
3. **README.md:** Add implementation notes

### Create Pull Request

```bash
git add thorne_drak/EQUI_InventoryWindow.xml
git add thorne_drak/stat_icon_pieces*.tga
git add .development/stat-icons-config.json
git commit -m "feat(inventory): add stat-icons to inventory window"

# Create PR via GitHub MCP or web interface
```

---

## Quick Reference

### Key Files

| File | Purpose | Status |
|------|---------|--------|
| `.development/stat-icons-config.json` | Source coordinates | ⏳ Needs 9 coords |
| `.development/stat-icons-coordinates.json` | Master layout | ✅ Complete |
| `thorne_drak/stat_icon_pieces01.tga` | Generated texture | ✅ Partial (10/18) |
| `.bin/regen_stat_icons.py` | Regeneration script | ✅ Ready |
| `.bin/validate_stat_icons.py` | Validation script | ✅ Ready |

### Commands

```bash
# Regenerate textures after updating config
python .bin/regen_stat_icons.py

# Validate coordinate consistency
python .bin/validate_stat_icons.py

# List gemicon files
ls -l default/gemicons*.tga
```

---

## Unknown Status Items

### Check If Available

**Possible analysis scripts (may exist in `.bin/` or `.bin/archive/`):**
- `analyze_gemicons.py` - Gemicon analysis tool
- `detect_gemicon_grid.py` - Grid overlay generator
- `extract_gemicon_coordinates.py` - Coordinate extraction

**To check:**
```bash
ls -l .bin/*gemicon*.py
ls -l .bin/archive/*gemicon*.py
```

If these exist, they may automate icon coordinate discovery.

---

## Timeline Estimate

**Per icon:** ~5-10 minutes (visual inspection + measurement)  
**Total for 9 icons:** ~1-2 hours  
**Regeneration + validation:** ~5 minutes  
**Window integration:** ~2-4 hours  
**Testing + refinement:** ~1-2 hours

**Total estimated time:** 4-8 hours

---

## Blockers & Risks

**Current blockers:**
- None (all tools ready, just needs manual icon discovery)

**Potential risks:**
- Icon might not exist in gemicon files (use placeholder if needed)
- Icon size might not be 24×24 (resize or find alternative)
- Visual quality might vary (test in-game before finalizing)

**Mitigation:**
- Start with easiest icons (HP/MANA likely heart/orb)
- Test incremental updates (don't wait to find all 9 before regenerating)
- Create Options variant to allow text-only fallback

---

## Support Resources

### Documentation
- [README.md](README.md) - System overview
- [ABBREVIATIONS.md](ABBREVIATIONS.md) - Icon shorthand reference
- [archive/README-OLD-VERBOSE.md](archive/README-OLD-VERBOSE.md) - Historical detailed docs
- [archive/GEMICON-EXTRACTION-SUMMARY.md](archive/GEMICON-EXTRACTION-SUMMARY.md) - Previous extraction results

### Example Coordinates (Already Found)

```json
{
  "Fire":    {"file": "gemicons01.tga", "x": 48,  "y": 120, "w": 24, "h": 24},
  "Cold":    {"file": "gemicons01.tga", "x": 168, "y": 120, "w": 24, "h": 24},
  "Magic":   {"file": "gemicons01.tga", "x": 216, "y": 144, "w": 24, "h": 24},
  "Poison":  {"file": "gemicons01.tga", "x": 24,  "y": 144, "w": 24, "h": 24},
  "Disease": {"file": "gemicons01.tga", "x": 120, "y": 144, "w": 24, "h": 24}
}
```

Use these as reference for coordinate format.

---

**Next Action:** Open `default/gemicons01.tga` in image viewer and begin visual icon discovery.

**Maintainer:** Draknare Thorne
