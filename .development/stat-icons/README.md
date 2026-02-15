# Stat Icons System

**Status:** ⏳ In Progress (Needs icon coordinates)  
**Version:** 1.0  
**Last Updated:** 2026-02-15

---

## Overview

Three swappable stat icon texture files with **identical coordinate layouts**. Users can switch between icon aesthetics without modifying XML files.

### Generated Files

| File | Source | Icons | Status |
|------|--------|-------|--------|
| `stat_icon_pieces01.tga` | vert UI | 10 real + 8 placeholders | ✅ Generated |
| `stat_icon_pieces02.tga` | vert-blue resists | 5 real + 13 placeholders | ✅ Generated |
| `stat_icon_pieces03.tga` | default EQ resists | 5 real + 13 placeholders | ✅ Generated |

**Specifications:** 256×256 RGBA, 22×22px icons, identical coordinates across all files

---

## Master Layout (256×256)

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

**Spacing:** 22×22px icons, 30px row spacing, 80px column spacing

---

## Usage in XML

### Basic Animation

```xml
<Ui2DAnimation item="A_STRIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>170</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Swappable Files (Coordinates Unchanged)

```xml
<!-- Switch between files without coordinate changes -->
<Texture>stat_icon_pieces01.tga</Texture>  <!-- vert comprehensive -->
<Texture>stat_icon_pieces02.tga</Texture>  <!-- vert-blue resists -->
<Texture>stat_icon_pieces03.tga</Texture>  <!-- default resists -->
```

---

## Icon Status

### pieces01 (vert UI)
✅ **Real Icons:** AC, ATK, STR, WIS, INT, Fire, Cold, Magic, Poison, Disease  
○ **Placeholders:** HP, MANA, STA, Weight, Reserve, AGI, DEX, CHA

### pieces02/03 (gemicons)
✅ **Real Icons:** Fire, Cold, Magic, Poison, Disease  
○ **Placeholders:** All Column 1 & 3 positions

---

## Implementation Status

### ✅ Complete
- Master layout defined (18 positions)
- Three swappable texture files generated
- Validation and regeneration scripts

### ⏳ Pending
**Missing source coordinates in `stat-icons-config.json`:**
- **Column 1:** AC, ATK, HP, MANA, STA, Weight
- **Column 3:** AGI, DEX, CHA

**To complete:**
1. Locate icons in gemicon files (24×24px)
2. Update `.development/stat-icons-config.json` with coordinates
3. Regenerate: `python .bin/regen_stat_icons.py`
4. Validate: `python .bin/validate_stat_icons.py`

---

## Window Integration (Next Phase)

**Primary Target:** Inventory Window
- Format: `[Icon] Label Value` (e.g., `[STR] STR 150`)
- Create Options variants (text-only, icon-only, icon+text)

**Secondary Targets:** Player, Actions, Merchant Windows
- Format: `[Icon] Value` (space-saving)

---

## File Organization

```
thorne_drak/
  stat_icon_pieces01.tga          # Generated texture (vert)
  stat_icon_pieces02.tga          # Generated texture (vert-blue)
  stat_icon_pieces03.tga          # Generated texture (default)

.development/
  stat-icons-coordinates.json     # Master layout (18 positions)
  stat-icons-config.json          # Source coordinates (NEEDS COMPLETION)

.development/stat-icons/
  README.md                       # This file
  ABBREVIATIONS.md                # Abbreviation reference
  archive/                        # Historical docs + analysis
    README-OLD-VERBOSE.md
    stat_icon_MASTER_LAYOUT.md
    VISUAL_LAYOUT_GUIDE.md
    ... (9 analysis documents)

.bin/
  regen_stat_icons.py             # Regenerate texture files
  validate_stat_icons.py          # Validate coordinates
```

---

## Tools

### Regenerate Textures
```bash
python .bin/regen_stat_icons.py
```

### Validate Coordinates
```bash
python .bin/validate_stat_icons.py
```

**Requirements:** `pillow>=12.1.1`

---

## Next Steps

1. **Find missing gemicon coordinates** (manual inspection or grid detection)
2. **Update `stat-icons-config.json`** with extracted coordinates
3. **Regenerate texture files** with complete icon set
4. **Integrate into Inventory window** (primary v0.7.0 goal)
5. **Create Options variants** (text-only, icon-only, icon+text)

---

**Maintainer:** Draknare Thorne  
**Repository:** [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Reference:** See [ABBREVIATIONS.md](ABBREVIATIONS.md) for icon shorthand
