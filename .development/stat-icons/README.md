# Stat Icons System

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2026-02-10

---

## Overview

The ThorneUI stat icons system provides **three swappable texture files** with identical coordinate layouts. This allows users to switch between different icon aesthetics without modifying XML files.

### Files Generated

1. **stat_icon_pieces01.tga** - Vert UI icons (comprehensive set)
2. **stat_icon_pieces02.tga** - Vert-blue resist icons (detailed variant)
3. **stat_icon_pieces03.tga** - Default EQ resist icons (classic variant)

All three files:
- Use **identical 256×256 RGBA format**
- Have **18 icon positions** at the same coordinates
- Support **22×22 pixel icons**
- Are **fully swappable** in XML without coordinate changes

---

## Quick Start

### Using in XML

```xml
<!-- Reference any of the three files -->
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Swap to different file - coordinates stay the same! -->
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces02.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>  <!-- ← UNCHANGED -->
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Validate Files

```bash
python .bin/validate_stat_icons.py
```

### Regenerate Files

```bash
python .bin/generate_master_stat_icons.py
```

---

## Layout Structure

### Three-Column Grid

```
Column 1 (X=10)     Column 2 (X=90)      Column 3 (X=170)
Player Stats        Resistances          Attributes
───────────────────────────────────────────────────────
AC      (10,10)     Fire     (90,10)     STR     (170,10)
ATK     (10,40)     Cold     (90,40)     INT     (170,40)
HP      (10,70)     Magic    (90,70)     WIS     (170,70)
MANA    (10,100)    Poison   (90,100)    AGI     (170,100)
STA     (10,130)    Disease  (90,130)    DEX     (170,130)
Weight  (10,160)    Reserve  (90,160)    CHA     (170,160)
```

**All icons:** 22×22 pixels  
**Row spacing:** 30 pixels (Y increments)  
**Column spacing:** 80 pixels between columns

---

## File Comparison

### stat_icon_pieces01.tga
**Source:** `vert/window_pieces06.tga`

- ✅ **10 real icons:** AC, ATK, STR, WIS, INT, Fire, Cold, Magic, Poison, Disease
- ○ **8 placeholders:** HP, MANA, STA, Weight, Reserve, AGI, DEX, CHA
- **Best for:** Comprehensive stat displays, cohesive vert aesthetic
- **Icon style:** 22×22 native vert UI icons

### stat_icon_pieces02.tga
**Source:** `vert-blue/gemicons01.tga`

- ✅ **5 real icons:** Fire, Cold, Magic, Poison, Disease (Column 2 only)
- ○ **13 placeholders:** All Column 1 and 3 positions
- **Best for:** Resistance-focused displays, vert-blue theme
- **Icon style:** 24×24 gemicons resized to 22×22 (detailed, blue palette)

### stat_icon_pieces03.tga
**Source:** `default/gemicons01.tga`

- ✅ **5 real icons:** Fire, Cold, Magic, Poison, Disease (Column 2 only)
- ○ **13 placeholders:** All Column 1 and 3 positions
- **Best for:** Classic EQ aesthetic, familiar look
- **Icon style:** 24×24 gemicons resized to 22×22 (traditional EQ colors)

---

## Complete Icon Reference

| Icon    | Column | X   | Y   | pieces01 | pieces02 | pieces03 |
|---------|--------|-----|-----|----------|----------|----------|
| AC      | 1      | 10  | 10  | ✅ Real  | ○ Placeholder | ○ Placeholder |
| ATK     | 1      | 10  | 40  | ✅ Real  | ○ Placeholder | ○ Placeholder |
| HP      | 1      | 10  | 70  | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| MANA    | 1      | 10  | 100 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| STA     | 1      | 10  | 130 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| Weight  | 1      | 10  | 160 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| Fire    | 2      | 90  | 10  | ✅ Real  | ✅ Real  | ✅ Real  |
| Cold    | 2      | 90  | 40  | ✅ Real  | ✅ Real  | ✅ Real  |
| Magic   | 2      | 90  | 70  | ✅ Real  | ✅ Real  | ✅ Real  |
| Poison  | 2      | 90  | 100 | ✅ Real  | ✅ Real  | ✅ Real  |
| Disease | 2      | 90  | 130 | ✅ Real  | ✅ Real  | ✅ Real  |
| Reserve | 2      | 90  | 160 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| STR     | 3      | 170 | 10  | ✅ Real  | ○ Placeholder | ○ Placeholder |
| INT     | 3      | 170 | 40  | ✅ Real  | ○ Placeholder | ○ Placeholder |
| WIS     | 3      | 170 | 70  | ✅ Real  | ○ Placeholder | ○ Placeholder |
| AGI     | 3      | 170 | 100 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| DEX     | 3      | 170 | 130 | ○ Placeholder | ○ Placeholder | ○ Placeholder |
| CHA     | 3      | 170 | 160 | ○ Placeholder | ○ Placeholder | ○ Placeholder |

---

## Placeholder System

Positions without source icons use **subtle placeholder graphics**:

- **Appearance:** Light gray bordered box with center X mark
- **Dimensions:** 22×22 (matches real icons)
- **Visibility:** Semi-transparent, non-intrusive
- **Purpose:** Reserve space, maintain grid structure

**Note:** Placeholders are intentionally subtle and should NOT be referenced in XML animations. They exist only to maintain consistent file structure.

---

## Technical Details

### File Specifications
- **Format:** TGA (Targa) RGBA
- **Dimensions:** 256×256 pixels
- **Bit Depth:** 32-bit (8-bit RGBA channels)
- **Compression:** None (uncompressed)
- **Color Space:** sRGB

### Icon Extraction Details

**pieces01 sources (vert/window_pieces06.tga):**
- All icons extracted at 22×22 (native size, no resize)
- Positions: AC (205,85), ATK (231,85), STR (179,85), etc.

**pieces02 sources (vert-blue/gemicons01.tga):**
- Resist icons extracted at 24×24, resized to 22×22
- Algorithm: LANCZOS resampling (high quality)
- Positions: Fire (48,120), Cold (168,120), etc.

**pieces03 sources (default/gemicons01.tga):**
- Same as pieces02 but from default UI source
- Identical coordinates, classic EQ color palette

---

## Validation Results

**Last Validation:** 2026-02-10

```
✅ stat_icon_pieces01.tga - 18/18 positions valid
✅ stat_icon_pieces02.tga - 18/18 positions valid  
✅ stat_icon_pieces03.tga - 18/18 positions valid
✅ Cross-file consistency - PASS
✅ Swappability confirmed
```

All three files passed validation:
- Correct size (256×256 RGBA)
- All 18 positions have content
- Coordinates match across files
- Files are swappable

---

## Adding New Icons

To add icons to the master template:

1. **Update source dictionaries** in `.bin/generate_master_stat_icons.py`
2. **Add to all THREE files** (maintain swappability)
3. **Run generator:** `python .bin/generate_master_stat_icons.py`
4. **Validate:** `python .bin/validate_stat_icons.py`
5. **Update documentation:** Add to this README and MASTER_LAYOUT.md
6. **Test in-game:** Verify icons display correctly

### Priority Targets for Future Icons

Current placeholders ready to be filled:
- **HP** (10,70) - Hit Points icon
- **MANA** (10,100) - Mana icon
- **STA** (10,130) - Stamina icon
- **Weight** (10,160) - Weight/Burden icon
- **AGI** (170,100) - Agility icon
- **DEX** (170,130) - Dexterity icon
- **CHA** (170,160) - Charisma icon
- **Reserve** (90,160) - Could be Corruption resist or special icon

---

## Related Files

### Generated Files
- `thorne_drak/stat_icon_pieces01.tga` - Primary texture (vert icons)
- `thorne_drak/stat_icon_pieces02.tga` - Alt texture (vert-blue resists)
- `thorne_drak/stat_icon_pieces03.tga` - Alt texture (default resists)

### Documentation
- `stat_icon_MASTER_LAYOUT.md` - Complete layout documentation
- `.development/stat-icons-coordinates.json` - Machine-readable coordinate data
- `.docs/VERT-ICON-EXTRACTION-SUMMARY.md` - Original extraction notes
- `.docs/GEMICON-REFERENCE.md` - Gemicon source reference

### Tools
- `.bin/generate_master_stat_icons.py` - Generate all three files
- `.bin/validate_stat_icons.py` - Validate layout consistency
- `.bin/verify_stat_icons.py` - Legacy verification tool

---

## Usage Examples

### Basic Icon Animation

```xml
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Multiple Icons in Sequence

```xml
<!-- AC Icon -->
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- ATK Icon (30px below AC) -->
<Ui2DAnimation item="A_ATKIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>40</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Fire Resist (same row as AC, Column 2) -->
<Ui2DAnimation item="A_FireResist">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Switching Between Files

```xml
<!-- Use vert icons (comprehensive) -->
<Texture>stat_icon_pieces01.tga</Texture>

<!-- OR use vert-blue resists (detailed) -->
<Texture>stat_icon_pieces02.tga</Texture>

<!-- OR use default resists (classic) -->
<Texture>stat_icon_pieces03.tga</Texture>

<!-- Coordinates remain identical! -->
<Location><X>90</X><Y>10</Y></Location>
```

---

## Best Practices

1. **File Selection**
   - Use pieces01 for complete stat icon sets
   - Use pieces02/03 for resistance-only displays
   - Document which file you chose (add XML comments)

2. **Coordinate Usage**
   - Always use coordinates from master template
   - Never hardcode icon positions without checking table
   - Use 22×22 size for all icons

3. **Swappability**
   - Test XML with all three files
   - Ensure layout works regardless of file choice
   - Don't rely on placeholder positions

4. **Maintenance**
   - Run validation after any changes
   - Keep all three files in sync
   - Update JSON and documentation together

---

## Troubleshooting

### Icons Not Appearing

1. **Check coordinates:** Verify against master template table
2. **Check size:** Must be 22×22 pixels
3. **Check file path:** Ensure TGA file is in correct location
4. **Check transparency:** Verify RGBA mode with alpha channel

### Files Out of Sync

1. **Regenerate all files:** Run `generate_master_stat_icons.py`
2. **Validate:** Run `validate_stat_icons.py`
3. **Review JSON:** Check `.development/stat-icons-coordinates.json`

### Swapping Doesn't Work

1. **Validate coordinates:** Must be identical across files
2. **Check for placeholders:** Don't reference placeholder positions in XML
3. **Verify file format:** All must be 256×256 RGBA

---

## Version History

### 1.0 (2026-02-10)
- Initial master template system
- Generated three swappable texture files
- Created validation and generation tools
- Established 18-icon grid layout (3 columns × 6 rows)
- Documented complete coordinate system
- Implemented placeholder system

---

## Contributing

When adding new icons:

1. Source high-quality icons (prefer 22×22 or larger)
2. Add to PIECES01_SOURCES, PIECES02_SOURCES, PIECES03_SOURCES
3. Update MASTER_LAYOUT if adding new positions
4. Run generator to create new files
5. Validate all three files
6. Update documentation (this README + MASTER_LAYOUT.md)
7. Test in-game

---

**Status:** ✅ Production Ready  
**Validation:** All tests passing  
**Documentation:** Complete and current

For detailed layout information, see [stat_icon_MASTER_LAYOUT.md](stat_icon_MASTER_LAYOUT.md)
