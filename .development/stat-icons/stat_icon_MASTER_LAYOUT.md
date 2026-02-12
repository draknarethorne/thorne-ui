# Stat Icon Master Layout Template

**Version:** 1.0  
**Created:** 2026-02-10  
**Purpose:** Define a unified coordinate system for all stat icon texture files

---

## Overview

This document defines the **master template layout** used by all `stat_icon_pieces*.tga` files in ThorneUI. By using identical coordinate systems across all three texture files, they become **fully swappable** without requiring XML coordinate changes.

### Key Benefits

1. **Swappable Files**: Change texture files without updating XML
2. **Consistent Layout**: All icons at identical positions across files
3. **Future-Proof**: Reserved space for additional icons
4. **Easy Maintenance**: Single source of truth for coordinates

---

## Template Specifications

### File Format
- **Dimensions:** 256×256 pixels
- **Color Mode:** RGBA (with transparency)
- **Icon Size:** 22×22 pixels (all icons)
- **Row Spacing:** 30 pixels (22px icon + 8px gap)
- **Column Spacing:** 70-80 pixels between columns

### Three-Column Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Column 1 (X=10)    Column 2 (X=90)    Column 3 (X=170)    │
│  Player Stats       Resistances        Attributes           │
├─────────────────────────────────────────────────────────────┤
│  Row 1 (Y=10)                                               │
│  [AC____22×22]      [Fire___22×22]     [STR___22×22]       │
│                                                             │
│  Row 2 (Y=40)                                               │
│  [ATK___22×22]      [Cold___22×22]     [INT___22×22]       │
│                                                             │
│  Row 3 (Y=70)                                               │
│  [HP____22×22]      [Magic__22×22]     [WIS___22×22]       │
│                                                             │
│  Row 4 (Y=100)                                              │
│  [MANA__22×22]      [Poison_22×22]     [AGI___22×22]       │
│                                                             │
│  Row 5 (Y=130)                                              │
│  [STA___22×22]      [Disease22×22]     [DEX___22×22]       │
│                                                             │
│  Row 6 (Y=160)                                              │
│  [Weight22×22]      [Reserve22×22]     [CHA___22×22]       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Coordinate Table

| Icon    | Column | Row | X   | Y   | Size  | Purpose              |
|---------|--------|-----|-----|-----|-------|----------------------|
| AC      | 1      | 1   | 10  | 10  | 22×22 | Armor Class          |
| ATK     | 1      | 2   | 10  | 40  | 22×22 | Attack Power         |
| HP      | 1      | 3   | 10  | 70  | 22×22 | Hit Points           |
| MANA    | 1      | 4   | 10  | 100 | 22×22 | Mana Points          |
| STA     | 1      | 5   | 10  | 130 | 22×22 | Stamina              |
| Weight  | 1      | 6   | 10  | 160 | 22×22 | Character Weight     |
| Fire    | 2      | 1   | 90  | 10  | 22×22 | Fire Resistance      |
| Cold    | 2      | 2   | 90  | 40  | 22×22 | Cold Resistance      |
| Magic   | 2      | 3   | 90  | 70  | 22×22 | Magic Resistance     |
| Poison  | 2      | 4   | 90  | 100 | 22×22 | Poison Resistance    |
| Disease | 2      | 5   | 90  | 130 | 22×22 | Disease Resistance   |
| Reserve | 2      | 6   | 90  | 160 | 22×22 | Reserved/Future Use  |
| STR     | 3      | 1   | 170 | 10  | 22×22 | Strength             |
| INT     | 3      | 2   | 170 | 40  | 22×22 | Intelligence         |
| WIS     | 3      | 3   | 170 | 70  | 22×22 | Wisdom               |
| AGI     | 3      | 4   | 170 | 100 | 22×22 | Agility              |
| DEX     | 3      | 5   | 170 | 130 | 22×22 | Dexterity            |
| CHA     | 3      | 6   | 170 | 160 | 22×22 | Charisma             |

---

## File-Specific Content

### stat_icon_pieces01.tga
**Source:** `vert/window_pieces06.tga`  
**Description:** Icons from vert UI (22×22 native size)

**Real Icons (10):**
- AC, ATK, STR, WIS, INT (Column 1 & 3 stats)
- Fire, Cold, Magic, Poison, Disease (Column 2 resists)

**Placeholders (8):**
- HP, MANA, STA, Weight (Column 1)
- Reserve (Column 2)
- AGI, DEX, CHA (Column 3)

### stat_icon_pieces02.tga
**Source:** `vert-blue/gemicons01.tga`  
**Description:** Resist icons from vert-blue variant (24×24 resized to 22×22)

**Real Icons (5):**
- Fire, Cold, Magic, Poison, Disease (Column 2 only)

**Placeholders (13):**
- All Column 1 icons (AC, ATK, HP, MANA, STA, Weight)
- Reserve (Column 2)
- All Column 3 icons (STR, INT, WIS, AGI, DEX, CHA)

### stat_icon_pieces03.tga
**Source:** `default/gemicons01.tga`  
**Description:** Resist icons from default EQ UI (24×24 resized to 22×22)

**Real Icons (5):**
- Fire, Cold, Magic, Poison, Disease (Column 2 only)

**Placeholders (13):**
- All Column 1 icons (AC, ATK, HP, MANA, STA, Weight)
- Reserve (Column 2)
- All Column 3 icons (STR, INT, WIS, AGI, DEX, CHA)

---

## Placeholder Design

For positions without icons, a **dark placeholder graphic** is used, inspired by vert UI aesthetic:

- **Dimensions:** 22×22 pixels (matches real icons)
- **Outer Border:** 2px solid black (#000000, 255 alpha)
- **Fill:** Dark gray (#2B2B2B, 255 alpha) - matches vert's dark color scheme
- **Inner Accent:** 1px mid-gray (#444444, 255 alpha) at 1px inset
- **Center Mark:** Small hollow square (6×6) in darker tone
- **Purpose:** Reserve space for future icons, clearly visible to identify missing icons

**Visual Appearance:**
```
┌────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  ← 2px black border
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│  ← 1px mid-gray accent
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│  Dark gray fill (#2B2B2B)
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓░░░░░░░░░░░░░░░░▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└────────────────────┘
```

**Design Philosophy:**  
Placeholders are **intentionally visible** (not subtle) to help identify which icons still need 
to be created or extracted. The dark aesthetic matches vert UI's color scheme, making them look 
like reserved/empty slots rather than missing assets.

**Updated:** 2026-02-10 - Changed from subtle light gray to dark vert-inspired design

---

## XML Animation Examples

### Using stat_icon_pieces01.tga

```xml
<!-- AC Icon (Column 1, Row 1) -->
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Fire Resist (Column 2, Row 1) -->
<Ui2DAnimation item="A_FireResist">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- STR Icon (Column 3, Row 1) -->
<Ui2DAnimation item="A_STRIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>170</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Swapping to stat_icon_pieces02.tga

To use vert-blue resist icons instead:

```xml
<!-- Fire Resist (SAME COORDINATES, different file) -->
<Ui2DAnimation item="A_FireResist">
  <Texture>stat_icon_pieces02.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>  <!-- ← UNCHANGED -->
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

**No coordinate changes needed!** Only the `<Texture>` tag changes.

---

## Usage Guidelines

### When to Use Each File

1. **pieces01** (vert icons)
   - Full stat icon set
   - Cohesive vert aesthetic
   - Best for comprehensive stat displays
   - Use when you need ALL icons from one source

2. **pieces02** (vert-blue resists)
   - Larger, more detailed resist icons
   - Blue color scheme variant
   - Use for resistance-focused displays
   - Pairs well with vert-blue UI themes

3. **pieces03** (default resists)
   - Classic EverQuest resist icons
   - Familiar to long-time players
   - Use for traditional EQ aesthetic
   - Good for vanilla UI feel

### Best Practices

1. **Test swappability:** Verify all three files work with your XML
2. **Document which file you're using:** Add comments in XML
3. **Use placeholders wisely:** Don't reference placeholder icons in XML
4. **Reserve space:** Leave row 6 positions open for future expansion
5. **Maintain consistency:** If adding new icons, update ALL three files

---

## Source File Mapping

### pieces01 Extraction (vert/window_pieces06.tga)

| Icon    | Source X | Source Y | Source Size | Resize? |
|---------|----------|----------|-------------|---------|
| AC      | 205      | 85       | 22×22       | No      |
| ATK     | 231      | 85       | 22×22       | No      |
| STR     | 179      | 85       | 22×22       | No      |
| WIS     | 205      | 111      | 22×22       | No      |
| INT     | 179      | 137      | 22×22       | No      |
| Fire    | 231      | 137      | 22×22       | No      |
| Cold    | 231      | 111      | 22×22       | No      |
| Magic   | 231      | 189      | 22×22       | No      |
| Poison  | 231      | 215      | 22×22       | No      |
| Disease | 231      | 163      | 22×22       | No      |

### pieces02 Extraction (vert-blue/gemicons01.tga)

| Icon    | Source X | Source Y | Source Size | Resize? |
|---------|----------|----------|-------------|---------|
| Fire    | 48       | 120      | 24×24       | **Yes** |
| Cold    | 168      | 120      | 24×24       | **Yes** |
| Magic   | 216      | 144      | 24×24       | **Yes** |
| Poison  | 24       | 144      | 24×24       | **Yes** |
| Disease | 120      | 144      | 24×24       | **Yes** |

**Note:** Resized from 24×24 to 22×22 using LANCZOS resampling for quality.

### pieces03 Extraction (default/gemicons01.tga)

| Icon    | Source X | Source Y | Source Size | Resize? |
|---------|----------|----------|-------------|---------|
| Fire    | 48       | 120      | 24×24       | **Yes** |
| Cold    | 168      | 120      | 24×24       | **Yes** |
| Magic   | 216      | 144      | 24×24       | **Yes** |
| Poison  | 24       | 144      | 24×24       | **Yes** |
| Disease | 120      | 144      | 24×24       | **Yes** |

**Note:** Same coordinates as pieces02, different source file aesthetic.

---

## Validation

Use the validation script to verify layout consistency:

```bash
python .bin/validate_stat_icons.py
```

This checks:
- ✓ All three files exist
- ✓ All files are 256×256 RGBA
- ✓ Icons appear at identical coordinates
- ✓ No position conflicts or overlaps
- ✓ Layout matches master template

---

## Future Expansion

### Adding New Icons

When adding icons to the master template:

1. **Update all THREE files** to maintain swappability
2. **Use Row 6** (Y=160) first - currently reserved
3. **Add to JSON**: Update `.development/stat-icons-coordinates.json`
4. **Document source**: Note extraction coordinates
5. **Test validation**: Run validation script
6. **Update this document**: Add to coordinate table

### Potential Future Icons

- **HP** (Hit Points) - Currently placeholder in Column 1, Row 3
- **MANA** (Mana) - Currently placeholder in Column 1, Row 4
- **STA** (Stamina) - Currently placeholder in Column 1, Row 5
- **Weight** - Currently placeholder in Column 1, Row 6
- **AGI** (Agility) - Currently placeholder in Column 3, Row 4
- **DEX** (Dexterity) - Currently placeholder in Column 3, Row 5
- **CHA** (Charisma) - Currently placeholder in Column 3, Row 6
- **Corruption Resist** - Could use Reserve slot (Column 2, Row 6)

---

## Related Documentation

- **Implementation Plan:** `.development/stat-icons/STAT-ICONS-IMPLEMENTATION.md`
- **Coordinate JSON:** `.development/stat-icons-coordinates.json`
- **Extraction Summary:** `.docs/VERT-ICON-EXTRACTION-SUMMARY.md`
- **Gemicon Reference:** `.docs/GEMICON-REFERENCE.md`
- **Validation Script:** `.bin/validate_stat_icons.py`
- **Generation Script:** `.bin/generate_master_stat_icons.py`

---

## Changelog

### Version 1.1 (2026-02-10)
- **Updated placeholder design:** Changed from subtle light gray to dark vert-inspired aesthetic
  - New colors: Black border (#000000), dark gray fill (#2B2B2B), mid-gray accent (#444444)
  - Intentionally visible to help identify missing icons
  - Matches vert UI's dark color scheme
- **Regenerated all three files** with new darker placeholders
- **Updated documentation:** extract_gemicon_coordinates.py now shows master layout mapping

### Version 1.0 (2026-02-10)
- Initial master template definition
- Three-column layout with 18 icon positions
- Generated all three texture files with identical layouts
- Created placeholder system for missing icons
- Established swappability design
