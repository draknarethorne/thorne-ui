# Target Window - Standard Variant

**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne  
**Based On**: Lunakin Oval Target (modified by Brujoloco for QQQuarm)

---
## Purpose

The Standard Target Window displays your current target's information with integrated player HP/Mana display at the top. This variant uses the Lunakin "Oval Target" design with Thorne UI customizations.

**Key Features**:

- **Target HP Gauge**: Oval-style HP bar showing target's health (EQType 6)
- **Target HP Percentage**: Numeric percentage display (EQType 29)
- **Target Casting Gauge**: Shows target's spellcasting progress (EQType 7)
- **Player HP/Mana Display**: Integrated player stats at top of window
- **Compact Design**: Minimal footprint (260×50 pixels)
- **Frameless Style**: Clean, modern aesthetic without titlebar

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 260 × 50 pixels (fixed) |
| Resizable | No (`Style_Sizable=false`) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | TargetWindow |
| DrawTemplate | WDT_RoundedNoTitle |
| Default Position | X=516, Y=242 |
| Titlebar | No (`Style_Titlebar=false`) |
| Closebox | No (`Style_Closebox=false`) |
| Minimizebox | No (`Style_Minimizebox=false`) |
| Border | Yes (`Style_Border=true`) |

---

## Layout Overview

### Window Hierarchy

```text
TargetWindow (260×50)
├── Player Stats (Top Row, Y=0-15)
│   ├── TW_HPPlayerLabel ("HP" label)
│   ├── TW_PlayerHPvalue (Current/Max HP, EQType 70)
│   ├── TW_manalabel ("MANA" label)
│   └── TW_Player_Mana_P (Current/Max Mana, EQType 80)
├── Target HP Gauge (Y=1-40, EQType 6)
│   ├── Oval bar background (ovalbar.tga)
│   ├── HP fill animation (red)
│   └── Target_HPLabel (HP %, EQType 29, top right)
└── Target Casting Gauge (Y=1-40, EQType 7)
    ├── Purple fill when target is casting
    └── Displays spell name being cast
```

### Visual Layout

```
┌────────────────────────────────────────────────┐
│ HP  1500/1500        MANA     400/500      95% │ ← Player stats
│ ═══════════════════════════════════════════════ │ ← Target HP gauge
│ [Mob Name]                                      │ ← Target info
└────────────────────────────────────────────────┘
  260px wide × 50px tall
```

---

## Key Elements

### Player Stats Display (Top Row)

| Element | Type | EQType | Position | Notes |
|---------|------|--------|----------|-------|
| TW_HPPlayerLabel | Label | - | X=4, Y=0 | "HP" text label |
| TW_PlayerHPvalue | Label | 70 | X=30, Y=0 | Current/Max HP (e.g., "1500/1500") |
| TW_manalabel | Label | - | X=115, Y=0 | "MANA" text label (uppercase) |
| TW_Player_Mana_P | Label | 80 | X=155, Y=0 | Current/Max Mana values |

### Target Information

| Element | Type | EQType | Position | Notes |
|---------|------|--------|----------|-------|
| Target_HP | Gauge | 6 | X=1, Y=1 (250×39) | Main target HP gauge |
| Target_HPLabel | Label | 29 | X=217, Y=14 | HP percentage (e.g., "95") |
| Target_Casting_Gauge | Gauge | 7 | X=1, Y=1 (250×39) | Purple casting progress bar |

---

## Color Scheme

### Player Stats
- **HP Label**: RGB(255, 255, 255) - White
- **HP Values**: RGB(255, 100, 100) - Red  
- **Mana Label**: RGB(255, 255, 255) - White
- **Mana Values**: RGB(100, 150, 255) - Bright Blue *(Thorne UI modification)*

### Target Gauges
- **HP Gauge Fill**: RGB(240, 0, 0) - Red
- **HP Percentage**: RGB(255, 255, 255) - White
- **Casting Gauge Fill**: RGB(240, 0, 240) - Purple
- **Text**: RGB(240, 240, 240) - Light Gray

---

## EQTypes Used

| EQType | Element Type | Data Displayed | Notes |
|--------|--------------|----------------|-------|
| **6** | Gauge | Target HP | Standard target health gauge |
| **7** | Gauge | Target Casting | Shows spell being cast |
| **29** | Label | Target HP % | Percentage value (0-100) |
| **70** | Label | Player HP (Cur/Max) | Zeal-specific, shows "1500/1500" format |
| **80** | Label | Player Mana (Cur/Max) | Zeal-specific, shows "400/500" format |

**Note**: EQTypes 70 and 80 are Zeal client enhancements. On standard P2002 client, these will be blank or show 0 values.

---

## Thorne UI Modifications

Based on the original Lunakin Oval Target design, the following modifications have been made:

### Styling Changes
- **Mana Label**: Changed from "mana" (lowercase) → "MANA" (uppercase) for consistency
- **Mana Label Position**: Repositioned from X=180 → X=115 for better alignment with value display
- **Mana Color**: Updated to RGB(100, 150, 255) for improved visibility (brighter blue)

### Technical Updates
- **Zeal Conversion**: Updated EQTypes 70/80 for Zeal client compatibility (May 2025 by Brujoloco)
- **Phase 5 Standard**: Part of color standardization across all Thorne UI windows

---

## Installation

1. **Backup Current File** (if customized):
   ```bash
   cd C:\Program Files (x86)\EverQuest\uifiles\thorne_drak
   copy EQUI_TargetWindow.xml EQUI_TargetWindow.xml.backup
   ```

2. **Copy Standard Variant**:
   ```bash
   copy Options\Target\Standard\EQUI_TargetWindow.xml EQUI_TargetWindow.xml
   ```

3. **Reload UI** (in-game):
   ```
   /loadskin thorne_drak 1
   ```

---

## Technical Notes

### Oval Bar Texture
- Uses `ovalbar.tga` texture for smooth, rounded gauge appearance
- Texture size: 256×32 pixels
- Two animations: Background (A_OvalTarBG) and Fill (A_OvalTarFill)

### Gauge Overlays
- Target HP and Casting gauges occupy the same space (X=1, Y=1)
- Casting gauge only displays when target is actively casting
- HP gauge shows target's current health at all times

### Window Transparency
- `Style_Transparent=false` prevents client-enforced fading
- Window remains fully visible at all times (non-fadeable)
- See [DEVELOPMENT.md](../../../DEVELOPMENT.md#client-enforced-fading) for fading limitations

### Credits
- **Original Design**: Lunakin (Oval Target)
- **QQQuarm Adaptation**: Brujoloco (Nov 2023)
- **Zeal Conversion**: Brujoloco (May 2025)
- **Thorne UI Modifications**: Draknare Thorne (Feb 2026)

---

## Related Options

Currently, only the Standard variant exists for the Target Window. Future variants may include:
- Minimalist (HP gauge only, no player stats)
- Extended (with additional target information if EQTypes become available)

---

## Limitations

### P2002 Client Constraints

The Target Window is limited by what the P2002 client exposes through EQTypes:
- **No Target Level**: EQType 2 shows player level, not target level
- **No Target Class**: EQType 3 shows player class, not target class
- **No Target Name**: Target name appears in gauge but cannot be separately positioned
- **No Guild Info**: Target guild affiliation not exposed via EQTypes

**All UI mods** (default, duxaUI, QQ, Infiniti, vert, etc.) share these same limitations. Only EQTypes 6, 7, and 29 work for target data.

### Zeal Client Features

EQTypes 70 and 80 (Player HP/Mana cur/max values) **only work with Zeal client**:
- On vanilla P2002 client: These fields will be blank or show "0/0"
- On Zeal client: Shows exact values like "1500/1500" and "400/500"
- Window remains functional on both clients (graceful degradation)

---

## See Also

- [STANDARDS.md](../../../.docs/STANDARDS.md) - Thorne UI design standards
- [DEVELOPMENT.md](../../../DEVELOPMENT.md) - Development workflow and architecture
- [.docs/technical/eqtypes.md](../../../.docs/technical/eqtypes.md) - Complete EQType reference
- [.docs/technical/zeal-features.md](../../../.docs/technical/zeal-features.md) - Zeal client enhancements

---

**Maintainer**: Draknare Thorne  
**Repository**: [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Last Verified**: February 1, 2026
