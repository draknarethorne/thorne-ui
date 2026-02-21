# Stat Icons System - Complete Reference

**Status:** ✅ COMPLETE - All 18 icons configured and generated  
**Version:** 2.0  
**Last Updated:** 2026-02-15

---

## Overview

**Stat icons system** provides 18 standardized icon textures for displaying player statistics (HP, Mana, Attributes, Resistances) in Thorne UI. The system features complete automation for generation, deployment, and testing.

### System Status

✅ **Configuration:** Complete - all 18 icon coordinates mapped  
✅ **Generation:** Complete - production-ready script and automation  
✅ **Output:** Complete - 256×256 RGBA textures with all icons  
✅ **Documentation:** Complete - usage guides and specifications  
⏳ **Window Integration:** In Progress (v0.7.0 Inventory work)

---

## Quick Start

### Generate All Stat Icons

```bash
# Auto-discover all icon variants and regenerate
cd C:\Thorne-UI
python .bin/regen_icons.py --all

# Or regenerate single variant (most common)
python .bin/regen_icons.py Thorne
```

### With Reference Labels (for editing)

```bash
python .bin/regen_icons.py Thorne --labels
```

**Result:** `stat_icons_thorne01.tga` generated in variant directory and deployed to `thorne_dev/` for immediate testing.

---

## Master Layout (256×256)

All stat icons arranged in 3 columns × 6 rows with 22×22 pixel icons:

```
Column 1 (X=10)     | Column 2 (X=90)      | Column 3 (X=170)
Player Stats        | Resistances          | Attributes
────────────────────┼──────────────────────┼────────────────
AC      (10,10)     | Fire     (90,10)     | STR     (170,10)
ATK     (10,40)     | Cold     (90,40)     | INT     (170,40)
HP      (10,70)     | Magic    (90,70)     | WIS     (170,70)
MANA    (10,100)    | Poison   (90,100)    | AGI     (170,100)
STA     (10,130)    | Disease  (90,130)    | DEX     (170,130)
Weight  (10,160)    | Reserve  (90,160)    | CHA     (170,160)
```

### Icon Specifications

- **Texture Size:** 256×256 pixels (RGBA)
- **Format:** TGA (Targa image)
- **Icon Size:** 22×22 pixels
- **Labels:** Abbreviated text overlaid on icons (AC, ATK, HP, MP, ST, WT, etc.)
- **Grid Spacing:** 30px row height, 80px column width

---

## Files & Organization

### Generation System

```
.bin/
├── regen_icons.py              # Main generation script (549 lines)
├── regen_icons.json            # Configuration (all 18 icons)
├── regen_icons.md              # Comprehensive guide (490 lines)
└── README.md                   # Script index

.development/
├── stat-icons-coordinates.json # Master layout reference (meta)
└── stat-icons/
    ├── README.md               # This file
    ├── ABBREVIATIONS.md        # Icon shorthand reference
    ├── REDESIGN-REVIEW.md      # Complete system analysis
    └── archive/                # Historical docs
```

### Generated Stat Icons

```
thorne_drak/
├── stat_icons_thorne01.tga             # Generated texture (primary)
└── Options/Icons/
    ├── Thorne/
    │   ├── gemicons01-03.tga   # Source icon files
    │   ├── stat_icons_thorne01.tga     # Generated texture
    │   └── stat_icons_thorne01-stats.json # Generation metadata
    ├── Classic/
    ├── Duxa/
    ├── Infiniti/
    ├── Steamworks/
    └── WoW/
```

---

## Configuration: regen_icons.json

All 18 icons fully configured with source coordinates in `.bin/regen_icons.json`:

**Example entry:**
```json
{
  "AC": {
    "file": "gemicons01.tga",
    "x": 192, "y": 216,
    "w": 24, "h": 24,
    "description": "Armor Class"
  }
}
```

**Key Mappings:**
- Player Stats (Column 1): AC, ATK, HP, MANA, STA, Weight
- Resistances (Column 2): Fire, Cold, Magic, Poison, Disease, Reserve
- Attributes (Column 3): STR, INT, WIS, AGI, DEX, CHA

All 18 icons have complete, verified coordinates. No placeholders.

---

## Features

### ✅ Automated Generation
- Reads config from `.bin/regen_icons.json`
- Extracts icons from gemicon source files
- Resizes 24×24 → 22×22 pixels (LANCZOS interpolation)
- Places in master layout grid
- Adds abbreviation labels automatically
- Generates metadata JSON with audit trail

### ✅ Multi-Variant Support
- Auto-discovers all icon variants in `Options/Icons/`
- Currently supported: Thorne, Classic, Duxa, Infiniti, Steamworks, WoW
- Smart copy logic: Single variant → copies to `thorne_drak/`; Multiple → Thorne only

### ✅ Smart Deployment
- Automatic copying to `thorne_drak/stat_icons_thorne01.tga`
- Direct deployment to `C:\TAKP\uifiles\thorne_dev/` for testing
- In-game testing: `/loadskin thorne_drak`

### ✅ Detailed Metadata
Generates `stat_icons_thorne01-stats.json` with:
- Source file and coordinates for each icon
- Position in final texture
- Type: "extracted" vs "placeholder"
- Complete audit trail

---

## Command Reference

### Regenerate All Variants
```bash
python .bin/regen_icons.py --all
```

### Regenerate Single Variant
```bash
python .bin/regen_icons.py Thorne
python .bin/regen_icons.py Classic
```

### With Reference Labels
```bash
python .bin/regen_icons.py Thorne --labels
```

### Multiple Variants
```bash
python .bin/regen_icons.py Thorne Classic Duxa
```

See [.bin/regen_icons.md](../../.bin/regen_icons.md) for comprehensive usage guide.

---

## Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | This file - system overview and quick reference |
| **ABBREVIATIONS.md** | Icon shorthand reference (AC, MP, ST, FR, etc.) |
| **REDESIGN-REVIEW.md** | Complete technical analysis and design review |
| **.bin/regen_icons.md** | Detailed usage guide (490 lines) with workflows |
| **.bin/README.md** | Script index with quick reference |

---

## Next Phase: Window Integration (v0.7.0)

**Goal:** Integrate stat icons into Inventory window with Options-driven display modes

**Tasks:**
1. Create Options/UI variants (text-only, icons-only, icons+text)
2. Modify EQUI_Inventory.xml to support stat icon display
3. Test with Player, Target, Merchant windows
4. Release as v0.7.0

See [REDESIGN-REVIEW.md](REDESIGN-REVIEW.md) for complete integration roadmap.

---

**Maintainer:** Draknare Thorne  
**Repository:** [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Related Issue:** [#8 - Stat Icons Integration](https://github.com/draknarethorne/thorne-ui/issues/8)
