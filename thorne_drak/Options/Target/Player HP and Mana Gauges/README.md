# Target Window - Player HP and Mana Gauges Variant

**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Experimental variant (Phase 5)  
**Author**: Draknare Thorne  
**Based On**: Lunakin Oval Target (modified by Brujoloco for QQQuarm)

---
## Purpose

Enhanced Target Window featuring **player HP and Mana gauges** displayed above your target's information. This experimental variant adds visual health and mana bars to complement the numeric displays, providing at-a-glance awareness of your character's status while monitoring your target.

**Key Features**:

- **Player HP Gauge**: Visual red HP bar with percentage and value displays (EQType 1)
- **Player Mana Gauge**: Visual blue mana bar with percentage and value displays (EQType 2)
- **Player HP %**: Percentage display on left side (EQType 19)
- **Player Mana %**: Percentage display on right side (EQType 20)
- **Target HP Gauge**: Oval-style HP bar showing target's health (EQType 6)
- **Target HP Percentage**: Numeric percentage display (EQType 29)
- **Target Casting Gauge**: Shows target's spellcasting progress (EQType 7)
- **Expanded Height**: Taller window (70px) to accommodate player gauges
- **Symmetric Layout**: Balanced positioning of HP/Mana elements

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 260 × 70 pixels (fixed) |
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
TargetWindow (260×70)
├── Player Stats Row 1 (Y=0-15) - Percentages and Values
│   ├── TW_HPPlayerLabel (HP %, EQType 19)
│   ├── TW_HP_PctSign ("%" symbol, Font 2)
│   ├── TW_PlayerHPvalue (Current/Max HP, EQType 70)
│   ├── TW_Player_Mana_P (Current/Max Mana, EQType 80)
│   ├── TW_manalabel (Mana %, EQType 20)
│   └── TW_Mana_PctSign ("%" symbol, Font 2)
├── Player Gauges Row (Y=16-31) - Visual Health/Mana Bars
│   ├── TW_PlayerHP_Gauge (HP bar, 122×15px, EQType 1)
│   └── TW_PlayerMana_Gauge (Mana bar, 122×15px, EQType 2)
├── Target HP Gauge (Y=31-60, EQType 6)
│   ├── Oval bar background (ovalbar.tga)
│   ├── HP fill animation (red)
│   └── Target_HPLabel (HP %, EQType 29, top right)
└── Target Casting Gauge (Y=46-60, EQType 7)
    ├── Purple fill when target is casting
    └── Displays spell name being cast
```

### Visual Layout

```
┌──────────────────────────────────────────────────────┐
│ 100%  1500/1500              400/500          100%   │ ← Player % and values
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         │ ← Player HP/Mana gauges
│ ══════════════════════════════════════════════  95%  │ ← Target HP gauge
│ [Target Name]                                        │ ← Target casting bar
└──────────────────────────────────────────────────────┘
  260px wide × 70px tall
```

---

## Key Elements

### Player Stats Display (Top Row, Y=0)

| Element | Type | EQType | Position (X,Y) | Size (W×H) | Alignment | Notes |
|---------|------|--------|----------------|------------|-----------|-------|
| TW_HPPlayerLabel | Label | 19 | -1, 0 | 25×15 | Right | HP percentage value |
| TW_HP_PctSign | Label | - | 24, 0 | 16×15 | - | "%" symbol (Font 2) |
| TW_PlayerHPvalue | Label | 70 | 42, 0 | 81×15 | Center | Current/Max HP (e.g., "1500/1500") |
| TW_Player_Mana_P | Label | 80 | 132, 0 | 81×15 | Center | Current/Max Mana values |
| TW_manalabel | Label | 20 | 214, 0 | 25×15 | Right | Mana percentage value |
| TW_Mana_PctSign | Label | - | 239, 0 | 16×15 | - | "%" symbol (Font 2) |

**Layout Notes**:
- HP % positioned at far left (X=-1 to X=24)
- HP values centered left of window midpoint (X=42)
- Mana values centered right of window midpoint (X=132)
- Mana % positioned at far right (X=214 to X=239)
- Percentage signs use smaller font (Font 2) for visual balance

### Player Gauges (Y=16-31)

| Element | Type | EQType | Position (X,Y) | Size (W×H) | Fill Color (RGB) | Notes |
|---------|------|--------|----------------|------------|------------------|-------|
| TW_PlayerHP_Gauge | Gauge | 1 | 4, 16 | 122×15 | 255,0,0 | Player HP gauge (red) |
| TW_PlayerMana_Gauge | Gauge | 2 | 146, 16 | 122×15 | 30,30,255 | Player Mana gauge (blue) |

**Gauge Details**:
- **HP Gauge**: Bright red fill (RGB 255,0,0) with darker red lines (180,70,70)
- **Mana Gauge**: Deep blue fill (RGB 30,30,255) with muted blue lines (70,105,180)
- **Template**: A_GaugeBackground / A_GaugeFill
- **GaugeOffset**: X=0, Y=0
- **TextOffset**: Y=-50 (hidden)
- **Z-Order**: Rendered behind target gauges for proper layering

### Target Information

| Element | Type | EQType | Position | Size | Notes |
|---------|------|--------|----------|------|-------|
| Target_HP | Gauge | 6 | 1, 1 | 250×60 | Main target HP oval gauge |
| Target_HPLabel | Label | 29 | 217, 30 | 32×15 | HP percentage (e.g., "95") |
| Target_Casting_Gauge | Gauge | 7 | 1, 1 | 250×60 | Purple casting progress bar |

**Target Gauge Offsets**:
- **Target_HP**: GaugeOffsetY=31, TextOffsetY=30
- **Target_Casting_Gauge**: GaugeOffsetY=46, TextOffsetY=45
- Adjusted to accommodate player gauges above

---

## Color Scheme

### Player HP Elements
| Element | Red | Green | Blue | Hex | Notes |
|---------|-----|-------|------|-----|-------|
| HP Gauge Fill | 255 | 0 | 0 | #FF0000 | Bright red |
| HP Gauge Lines | 180 | 70 | 70 | #B44646 | Darker red outline |
| HP Values Text | 255 | 100 | 100 | #FF6464 | Light red text |
| HP % Text | 255 | 255 | 255 | #FFFFFF | White |

### Player Mana Elements
| Element | Red | Green | Blue | Hex | Notes |
|---------|-----|-------|------|-----|-------|
| Mana Gauge Fill | 30 | 30 | 255 | #1E1EFF | Deep blue |
| Mana Gauge Lines | 70 | 105 | 180 | #4669B4 | Muted blue outline |
| Mana Values Text | 150 | 150 | 255 | #9696FF | Light blue text |
| Mana % Text | 255 | 255 | 255 | #FFFFFF | White |

**Color Philosophy**:
- Player gauges match colors from Player Window (EQUI_PlayerWindow.xml)
- HP: Red spectrum for health
- Mana: Blue spectrum for magical energy
- Percentages: White for high contrast and readability

### Target Elements
| Element | Red | Green | Blue | Hex | Notes |
|---------|-----|-------|------|-----|-------|
| Target HP Gauge | 255 | 0 | 0 | #FF0000 | Red HP bar |
| Target HP % | 255 | 255 | 255 | #FFFFFF | White text |
| Casting Gauge | 192 | 0 | 192 | #C000C0 | Purple when casting |

---

## Technical Details

### EQType Reference

| EQType | Purpose | Data Displayed |
|--------|---------|----------------|
| 1 | Player HP Gauge | Visual HP bar (% of max) |
| 2 | Player Mana Gauge | Visual mana bar (% of max) |
| 6 | Target HP Gauge | Target's health bar |
| 7 | Target Casting Gauge | Target's spellcasting progress |
| 19 | Player HP % | HP percentage value (e.g., "100") |
| 20 | Player Mana % | Mana percentage value (e.g., "100") |
| 29 | Target HP % Label | Target's HP percentage |
| 70 | Player HP Values | Current/Max HP (e.g., "1500/1500") |
| 80 | Player Mana Values | Current/Max Mana (e.g., "400/500") |

### Z-Order Rendering (Pieces List Order)

1. **TW_PlayerHP_Gauge** - Back layer (player HP bar)
2. **TW_PlayerMana_Gauge** - Back layer (player mana bar)
3. **Target_HP** - Mid layer (target HP oval)
4. **Target_Casting_Gauge** - Mid layer (target casting bar)
5. **TW_Player_Mana_P** - Front layer (mana values text)
6. **Target_HPLabel** - Front layer (target HP %)
7. **TW_PlayerHPvalue** - Front layer (HP values text)
8. **TW_manalabel** - Front layer (mana % text)
9. **TW_Mana_PctSign** - Front layer (mana % symbol)
10. **TW_HPPlayerLabel** - Front layer (HP % text)
11. **TW_HP_PctSign** - Front layer (HP % symbol)
12. **A_TargetBoxStaticAnim** - Top layer (decorative frame)
13. **necessary** - Utility element

**Z-Order Notes**:
- Player gauges render behind target gauges to prevent obstruction
- All text labels render in front for readability
- Percentage signs positioned after their respective values

---

## Positioning Details

### Symmetric Layout Design

The window uses a **symmetric design** with HP on the left and Mana on the right:

**Left Side (HP)**:
- HP % starts at X=-1 (extends to X=24 when right-aligned)
- HP % sign at X=24
- HP values centered at X=42 (81px wide field)
- HP gauge starts at X=4 (122px wide)

**Right Side (Mana)**:
- Mana values centered at X=132 (81px wide field)
- Mana gauge starts at X=146 (122px wide)
- Mana % ends at X=239 (right-aligned from X=214)
- Mana % sign at X=239

**Calculation Notes**:
- Window width: 260px
- HP gauge: 4 to 126 (122px)
- Mana gauge: 146 to 268 (122px, extends 8px beyond window for alignment)
- Gap between gauges: ~20px

---

## Comparison to Standard Variant

| Feature | Standard | Player HP/Mana Gauges |
|---------|----------|------------------------|
| Window Height | 50px | **70px** (+20px) |
| Player HP Display | Values only | **Gauge + Values + %** |
| Player Mana Display | Values only | **Gauge + Values + %** |
| Player Gauges | None | **2 gauges (122×15px each)** |
| Player % Display | None | **Both sides (HP/Mana)** |
| Target HP Position | Y=1 (GaugeOffsetY=15) | **Y=1 (GaugeOffsetY=31)** |
| Target Casting Position | Y=1 (GaugeOffsetY=27) | **Y=1 (GaugeOffsetY=46)** |
| Visual Information | Numeric only | **Numeric + Visual bars** |

**Advantages**:
- ✅ At-a-glance awareness of player HP/Mana status
- ✅ Visual gauges complement numeric displays
- ✅ Percentage displays for precise monitoring
- ✅ Symmetric, balanced layout
- ✅ Color-coded for quick recognition

**Trade-offs**:
- ⚠️ Taller window (70px vs 50px) requires more screen space
- ⚠️ More visual complexity (may not suit minimalist preferences)
- ⚠️ Experimental status (Phase 5 testing phase)

---

## Installation

### Option A: Copy to Main UI Directory
```bash
# Copy this variant to your main thorne_drak directory
cp EQUI_TargetWindow.xml ../../
```

### Option B: Link via Symbolic Link (Advanced)
```bash
# Windows (requires admin privileges)
mklink "..\..\EQUI_TargetWindow.xml" "EQUI_TargetWindow.xml"

# Linux/Mac
ln -s EQUI_TargetWindow.xml ../../EQUI_TargetWindow.xml
```

### Option C: Temporary Testing
Simply copy the file to test it temporarily without affecting your main UI setup.

---

## Usage Notes

1. **HP/Mana Gauges**: Update in real-time as your character takes damage or regenerates
2. **Percentage Displays**: Show exact HP/Mana percentages on left and right edges
3. **Value Displays**: Show current/max values in center areas
4. **Target Information**: Functions identically to Standard variant (HP gauge, casting bar)
5. **Window Position**: Can be moved and position will be saved in UI settings

---

## Development History

### Version 1.0.0 (February 2, 2026)
- ✅ Added player HP gauge (EQType 1, X=4, 122×15px)
- ✅ Added player Mana gauge (EQType 2, X=146, 122×15px)
- ✅ Added HP percentage display (EQType 19) on left side
- ✅ Added Mana percentage display (EQType 20) on right side
- ✅ Added percentage signs (Font 2) next to % values
- ✅ Implemented symmetric layout with balanced spacing
- ✅ Increased window height from 50px to 70px
- ✅ Adjusted target gauge offsets (HP: Y=31, Casting: Y=46)
- ✅ Configured proper z-order rendering (player gauges behind target gauges)
- ✅ Matched colors to Player Window (HP: RGB 255,0,0 / Mana: RGB 30,30,255)
- ✅ Configured text colors to match Player Window values
- ✅ Fine-tuned positioning through iterative adjustments
- ✅ Created comprehensive documentation

### Based On:
- **Lunakin Oval Target** (Nov 2023)
- **Modified by Brujoloco** for QQQuarm (Mana version)
- **Zeal Code Conversion** (May 2025)
- **Thorne UI Phase 5** enhancements (Feb 2026)

---

## Credits

- **Original Design**: Lunakin (Oval Target)
- **QQQuarm Adaptation**: Brujoloco (Mana version)
- **Zeal Conversion**: Brujoloco (May 2025)
- **Player Gauges Enhancement**: Draknare Thorne (Feb 2026)
- **UI Framework**: Thorne UI Phase 5

---

## Support and Feedback

This is an **experimental variant** created during Phase 5 development. Feedback welcome on:
- Gauge positioning and sizing
- Color choices and visibility
- Window height and layout
- Performance and resource usage
- Preference vs. Standard variant

**Repository**: draknarethorne/thorne-ui  
**Branch**: feature/phase-5-target-window  
**Status**: Active development
