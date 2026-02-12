# Gemicon Extraction Tool - Summary

## Tool Created

**File:** `.bin/extract_gemicon_coordinates.py`

A comprehensive Python tool that analyzes EverQuest UI XML files across multiple variant directories and extracts all icon coordinate information from gemicon texture files.

## What Was Discovered

### Total Findings
- **23 icon frame definitions** found across 6 UI variants
- **3 gemicon texture files** documented
- **16 unique animations** using gemicons

### Gemicon Files

#### gemicons01.tga (256×256)
**Most commonly used** - Found in all 6 variants

**Resist Icons** (24×24 pixels):
- **Fire**: `(48, 120)` in vert-blue, `(24, 120)` in duxaUI
- **Cold**: `(168, 120)` in vert-blue, `(144, 0)` in duxaUI
- **Magic**: `(216, 144)` in vert-blue, `(216, 24)` in duxaUI
- **Poison**: `(24, 144)` in vert-blue, `(24, 48)` in duxaUI
- **Disease**: `(120, 144)` in vert-blue, `(24, 0)` in duxaUI

**Grid Animation** (A_SpellGems):
- Cell size: 24×24 pixels (most variants)
- Cell size: 36×28 pixels (QQ variant)
- Full texture: 256×256 pixels
- Used for spell gem cycling and icon selection

#### gemicons02.tga (256×256)
**Secondary spell gem source** - Found in all 6 variants
- Grid animation: 24×24 cells
- Alternative/additional spell gems

#### gemicons03.tga (256×256)
**Extended icons** - Only found in vert-blue
- Grid animation: 24×24 cells
- Additional spell gem graphics

## Recommended Coordinates for Thorne UI

Based on the vert-blue variant (cleanest implementation):

```json
{
  "resist_icons_from_gemicons01": {
    "Fire":    { "x": 48,  "y": 120, "size": "24x24" },
    "Cold":    { "x": 168, "y": 120, "size": "24x24" },
    "Magic":   { "x": 216, "y": 144, "size": "24x24" },
    "Poison":  { "x": 24,  "y": 144, "size": "24x24" },
    "Disease": { "x": 120, "y": 144, "size": "24x24" }
  }
}
```

## How to Use in Thorne UI

### Create Animation Definitions

Add to `EQUI_Animations.xml`:

```xml
<!-- Fire Resist Icon -->
<Ui2DAnimation item="A_FireImage">
  <Cycle>true</Cycle>
  <Frames>
    <Texture>gemicons01.tga</Texture>
    <Location>
      <X>48</X>
      <Y>120</Y>
    </Location>
    <Size>
      <CX>24</CX>
      <CY>24</CY>
    </Size>
    <Hotspot>
      <X>0</X>
      <Y>0</Y>
    </Hotspot>
    <Duration>1000</Duration>
  </Frames>
</Ui2DAnimation>

<!-- Repeat for Cold, Magic, Poison, Disease -->
```

### Use in Windows

Add to `EQUI_PlayerWindow.xml` or `EQUI_Inventory.xml`:

```xml
<StaticAnimation item="Player_FireIcon">
  <RelativePosition>true</RelativePosition>
  <Location>
    <X>60</X>
    <Y>10</Y>
  </Location>
  <Size>
    <CX>24</CX>
    <CY>24</CY>
  </Size>
  <Animation>A_FireImage</Animation>
</StaticAnimation>
```

## Generated Documentation

### JSON Reference
**File:** `.docs/GEMICON-COORDINATES.json`
- Complete coordinate mappings
- All variants documented
- Structured data for programmatic use

### Markdown Guide  
**File:** `.docs/GEMICON-REFERENCE.md`
- Human-readable reference
- XML usage examples for each icon
- Comparison table across variants

## Comparison with Current Thorne UI Icons

The current `stat-icon-coordinates.json` uses custom texture files:
- `stat_icon_pieces01.tga` - Window pieces and backup icons (20×20)
- `stat_icon_pieces02.tga` - Gem-style icons (20×20)

**Gemicons provide:**
- Native EQ icons at 24×24 (higher quality)
- Battle-tested across multiple UI variants
- Grid system for easy access to hundreds of spell/buff icons

**Recommendation:** Consider using gemicons for resist icons in the Player Window and Inventory Window, as they're already familiar to EQ players and higher resolution than the current 20px icons.

## Tool Usage

### Run the extractor anytime:
```bash
python .bin/extract_gemicon_coordinates.py
```

### Output:
- Console summary with all found icons
- Updated `.docs/GEMICON-COORDINATES.json`
- Updated `.docs/GEMICON-REFERENCE.md`

### Expand search:
Edit these constants in the script:
```python
SEARCH_DIRS = ['default', 'vert', 'vert-blue', 'duxaUI', 'QQ', 'thorne_drak']
TARGET_FILES = ['EQUI_Animations.xml', 'EQUI_PlayerWindow.xml', ...]
GEMICON_FILES = ['gemicons01.tga', 'gemicons02.tga', 'gemicons03.tga']
```

## Next Steps

1. **Review** the generated `.docs/GEMICON-REFERENCE.md` for visual coordinate examples
2. **Decide** if Thorne UI should use gemicons or custom stat icons
3. **Implement** resist icons using coordinates from vert-blue (recommended)
4. **Consider** using the A_SpellGems grid for buff/spell displays
5. **Test** in-game to verify icons display correctly

## Summary of Variants

| Variant    | gemicons01 | gemicons02 | gemicons03 | Resist Icons? | Grid Size |
|------------|:----------:|:----------:|:----------:|:-------------:|:---------:|
| default    | ✓          | ✓          | -          | -             | 24×24     |
| vert       | ✓          | ✓          | -          | -             | 24×24     |
| vert-blue  | ✓          | ✓          | ✓          | ✓ (5 icons)   | 24×24     |
| duxaUI     | ✓          | ✓          | -          | ✓ (5 icons)   | 24×24     |
| QQ         | ✓          | ✓          | -          | -             | 36×28     |
| thorne_drak| ✓          | ✓          | -          | -             | 24×24     |

**Best source for resist icons:** vert-blue or duxaUI (both define all 5 resist types)

---

**Tool Status:** ✓ Complete and ready for reuse  
**Documentation:** ✓ JSON and Markdown files generated  
**Next Action:** Review `.docs/GEMICON-REFERENCE.md` and decide on implementation
