# Stat Icon Extraction from Vert UI - Summary

**Date:** 2026-02-10  
**Task:** Extract stat and resist icons from vert UI to recreate thorne_drak/stat_icon_pieces01.tga

---

## Icons Successfully Extracted

### Source File
- **File:** `vert/window_pieces06.tga`
- **Size:** 256×256
- **Format:** TGA (RGBA)

### Extracted Icons (10 total)

#### Column 1: Player Window Stats (5 icons)
All 22×22 pixels from window_pieces06.tga

| Icon | Source Coords | New Position | Description |
|------|---------------|--------------|-------------|
| AC   | (205, 85)     | (10, 10)     | Armor Class |
| ATK  | (231, 85)     | (10, 40)     | Attack Power |
| STR  | (179, 85)     | (10, 70)     | Strength |
| WIS  | (205, 111)    | (10, 100)    | Wisdom |
| INT  | (179, 137)    | (10, 130)    | Intelligence |

#### Column 2: Resist Icons (5 icons)
All 22×22 pixels from window_pieces06.tga

| Icon    | Source Coords | New Position | Description |
|---------|---------------|--------------|-------------|
| Fire    | (231, 137)    | (90, 10)     | Fire Resist |
| Cold    | (231, 111)    | (90, 40)     | Cold Resist |
| Magic   | (231, 189)    | (90, 70)     | Magic Resist |
| Poison  | (231, 215)    | (90, 100)    | Poison Resist |
| Disease | (231, 163)    | (90, 130)    | Disease Resist |

---

## Output Files

### Created Files

1. **thorne_drak/stat_icon_pieces01.tga**
   - Size: 256×256 RGBA
   - Contains: 10 extracted icons in 2-column layout
   - Column 1 (X=10): Stats (AC, ATK, STR, WIS, INT)
   - Column 2 (X=90): Resists (Fire, Cold, Magic, Poison, Disease)
   - Column 3 (X=170): Reserved for future icons

2. **thorne_drak/stat-icons-coordinates.json**
   - Updated with stat_icon_pieces01.tga coordinates
   - Includes source location mapping
   - Documents extraction provenance

---

## Source XML References

### Player Window (EQUI_PlayerWindow.xml)

```xml
<!-- AC Icon -->
<Ui2DAnimation item="A_Player_ACImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>205</X><Y>85</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- ATK Icon -->
<Ui2DAnimation item="A_Player_ATKImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>85</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- STR Icon -->
<Ui2DAnimation item="A_Player_STRImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>179</X><Y>85</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Hotbutton Window (EQUI_HotButtonWnd.xml)

```xml
<!-- Fire Resist -->
<Ui2DAnimation item="A_FireImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>137</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Cold Resist -->
<Ui2DAnimation item="A_ColdImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>111</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Magic Resist -->
<Ui2DAnimation item="A_MagicImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>189</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Poison Resist -->
<Ui2DAnimation item="A_PoisonImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>215</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Disease Resist -->
<Ui2DAnimation item="A_DiseaseImage">
  <Texture>window_pieces06.tga</Texture>
  <Location><X>231</X><Y>163</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

---

## Layout Design

```
stat_icon_pieces01.tga (256×256)
┌───────────────────────────────────┐
│ Column 1    Column 2    Column 3  │
│ (X=10)      (X=90)      (X=170)   │
│                                    │
│ AC (22×22)  Fire       [Reserved] │
│ ATK         Cold       [Reserved] │
│ STR         Magic      [Reserved] │
│ WIS         Poison     [Reserved] │
│ INT         Disease    [Reserved] │
│                                    │
│                                    │
│ (30px vertical spacing between    │
│  each icon: 22px icon + 8px gap)  │
└───────────────────────────────────┘
```

---

## Vert UI Observations

### Design Philosophy
- **Consistent icon size:** All stat/resist icons are 22×22 pixels
- **Single texture:** Uses window_pieces06.tga for both window types
- **Organized layout:** Icons grouped by type in texture
  - Stats row at Y=85 (STR, AC, ATK from left to right)
  - Resists column at X=231 (various Y positions)

### Icon Quality
- Clean, minimalist design
- High contrast for visibility
- Consistent with classic EverQuest aesthetic
- No transparency issues

### Missing Icons
- **Weight:** Not found in vert/EQUI_PlayerWindow.xml
- **HP/Mana icons:** Present as gauge end caps, not standalone icons

---

## Challenges & Solutions

### Challenge 1: Weight Icon Not Found
- **Issue:** Vert UI doesn't display Weight with an icon
- **Solution:** Extracted available stats (AC, ATK, STR, WIS, INT) instead
- **Future:** Can add Weight from duxaUI or gemicons if needed

### Challenge 2: Coordinate Accuracy
- **Issue:** Must extract exact pixel coordinates from XML
- **Solution:** Created Python script to automate extraction with source tracking
- **Benefit:** JSON maintains provenance (source file + original coords)

### Challenge 3: Layout Organization
- **Issue:** Need logical grouping for future maintainability
- **Solution:** 3-column layout with reserved space for expansion
- **Benefit:** Easy to add more icons without reorganizing

---

## Comparison with Other Icon Sets

### stat_icon_pieces02.tga (vert-blue gemicons)
- Uses 24×24 pixel resist icons from gemicons01.tga
- Larger, more detailed designs
- Single column layout

### stat_icon_pieces03.tga (default gemicons)
- Uses 24×24 pixel resist icons from default gemicons01.tga
- Identical layout to pieces02
- Classic EQ color palette

### stat_icon_pieces01.tga (NEW - this extraction)
- Uses 22×22 pixel icons from vert UI
- Multi-column layout supporting stats + resists
- Matches vert's custom aesthetic
- **Advantage:** All icons from single cohesive source

---

## Usage in ThorneUI

These icons can be referenced in XML files like this:

```xml
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<Ui2DAnimation item="A_FireResist">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

---

## Script Used

**File:** `.bin/extract_vert_icons.py`

```python
# Automated extraction script that:
# 1. Loads vert/window_pieces06.tga
# 2. Extracts 10 icons at specified coordinates
# 3. Creates 256×256 output texture with 2-column layout
# 4. Updates stat-icons-coordinates.json with mapping
# 5. Preserves source provenance for each icon
```

**Run command:**
```bash
python .bin/extract_vert_icons.py
```

---

## Next Steps

### Optional Enhancements

1. **Add Weight Icon**
   - Search duxaUI for weight icon
   - Or use gemicons balance/scale icon
   - Add to column 1 at Y=160

2. **Add HP/Mana Icons**
   - Extract from gauge end caps if suitable
   - Or design custom icons matching vert aesthetic
   - Add to column 1 continuing downward

3. **Add Remaining Stats**
   - STA, AGI, DEX, CHA from vert if available
   - Reserve column 3 for these character stats

4. **Create Animation Definitions**
   - Add to EQUI_Animations.xml in thorne_drak
   - Define A_ACIcon, A_ATKIcon, etc.
   - Enable easy XML references

---

## Conclusion

Successfully extracted 10 stat and resist icons from vert UI's window_pieces06.tga and created a new stat_icon_pieces01.tga texture with organized 3-column layout. All icons maintain original 22×22 size, with generous spacing for readability. JSON coordinate mapping documents both output positions and source provenance for future reference.

**Status:** ✓ Complete  
**Files Modified:** 2 (stat_icon_pieces01.tga created, stat-icons-coordinates.json updated)  
**Icons Extracted:** 10 (5 stats + 5 resists)
