# Target Window - Player Gauges and Weight Variant

**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)
**Version**: 1.1.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Enhanced variant with experimental features  
**Author**: Draknare Thorne  
**Based On**: Lunakin Oval Target (modified by Brujoloco for QQQuarm)

---
## Purpose

The "Player Gauges and Weight" Target Window variant displays your current target's information with enhanced player HP/Mana gauges and an experimental player weight display. This variant adds valuable context to the target window by showing your own health, mana, and carrying capacity alongside target information.

**Key Features**:

- **Target HP Gauge**: Oval-style HP bar showing target's health (EQType 6)
- **Target HP Percentage**: Numeric percentage display (EQType 29)
- **Target Casting Gauge**: Shows target's spellcasting progress (EQType 7)
- **Player HP/Mana Gauges**: Large 122×15px gauges showing your own stats at top
- **Player Weight Display**: EXPERIMENTAL - Shows current/max weight centered between HP/Mana
- **Uniform Positioning**: Player stats aligned with Pet Window and Group Window for consistency
- **Compact Design**: Minimal footprint (260×70 pixels)
- **Frameless Style**: Clean, modern aesthetic without titlebar

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
├── Player Stats Row (Y=0, spans full width)
│   ├── TW_HP_Pct (HP %, EQType 19)
│   ├── TW_HP_PctSign (%)
│   ├── TW_Weight_Current (Current weight, EQType 24) - EXPERIMENTAL
│   ├── TW_Weight_Divider (/)
│   ├── TW_Weight_Max (Max weight, EQType 25) - EXPERIMENTAL
│   ├── TW_Mana_Pct (Mana %, EQType 20)
│   └── TW_Mana_PctSign (%)
├── Player HP Gauge (Y=16, 122×15px)
├── Player Mana Gauge (Y=16, 122×15px)
├── Target HP Gauge (Y=31, centered)
├── Target Casting Gauge (Y=46, centered)
└── [Target Info on separate row below]
```

### Element Positioning

| Element | Position | Size | Type | Purpose |
|---------|----------|------|------|---------|
| TW_HP_Pct | (42, 0) | 81×15 | Value+% | Player HP display |
| TW_Weight_Current | (99, 12) | 25×11 | Value | Current weight (EXPERIMENTAL) |
| TW_Weight_Divider | (123, 12) | 7×11 | Text | Weight separator (EXPERIMENTAL) |
| TW_Weight_Max | (129, 12) | 25×11 | Value | Max weight (EXPERIMENTAL) |
| TW_Mana_Pct | (134, 0) | 81×15 | Value+% | Player Mana display |
| TW_PlayerHP_Gauge | (4, 16) | 122×15 | Gauge | HP bar (EQType 1, RGB 255,0,0) |
| TW_PlayerMana_Gauge | (148, 16) | 122×15 | Gauge | Mana bar (EQType 2, RGB 30,30,255) |
| Target_HP | Centered | Auto | Gauge | Target HP (EQType 6) |
| Target_Casting | Centered | Auto | Gauge | Target Casting (EQType 7) |

---

## Key Modifications (v1.1.0 - Feb 3, 2026)

### Added Features
- **Player Weight Display**: EXPERIMENTAL three-part format (current/max) centered between HP and Mana
  - Positioned at X=99-129, Y=12
  - Font 2 (smaller than gauge values)
  - Uses EQTypes 24 (current) and 25 (max)
  - Center-aligned divider "/" for visual balance

### Positioning Updates
- Mana fields moved right 2px for better spacing
- Weight fields positioned to center precisely at window midline
- All labels use consistent Font 2 for weight display

### Color Standardization
- Pet name text changed to white (RGB 255,255,255) for better contrast against purple gauges
- Maintained red HP gauges (RGB 255,0,0) and blue Mana gauges (RGB 30,30,255)

---

## EQTypes Reference

| EQType | Purpose | Source | Range |
|--------|---------|--------|-------|
| 1 | Player HP Gauge | Dynamic | 0-max HP |
| 2 | Player Mana Gauge | Dynamic | 0-max Mana |
| 6 | Target HP Gauge | Dynamic | 0-100 |
| 7 | Target Casting | Dynamic | 0-100 |
| 19 | Player HP % | Dynamic | 0-100 |
| 20 | Player Mana % | Dynamic | 0-100 |
| 24 | Player Weight Current | Dynamic | 0-weight |
| 25 | Player Weight Maximum | Static | char class |
| 29 | Target HP % | Dynamic | 0-100 |

---

## Experimental Features 

⚠️ **EXPERIMENTAL**: The weight display (EQType 24/25) is marked experimental and may be removed or redesigned before v0.6.0 release based on:

- **In-game testing feedback**: Usability and visual impact
- **Information value**: Whether displaying weight in combat scenario is actually useful
- **UI clutter assessment**: Balance between information density and clean presentation
- **User preferences**: Community feedback on feature usefulness

**Testing Recommendations**:
1. Load UI with `/loadskin thorne_drak`
2. Open Character window to view Player window with pet gauge
3. Target various NPCs/players to view Target window with weight display
4. Assess visual clarity and positioning
5. Evaluate whether weight information is valuable in combat context
6. Report back with feedback on positioning, sizing, or feature necessity

---

## Alignment with Other Windows

This variant maintains consistent positioning with:

- **Group Window**: Health labels at X=82, percentage signs at X=142
- **Pet Info Window**: Pet name gauge positioning and text offsets
- **Player Window**: Pet HP gauge layout and text color (white)

---

## Compatibility Notes

- **Gauge Heights**: Tall gauges (15px) used for both player stats
- **Window Height**: 70px accommodates players + target info
- **Color Scheme**: Purple window frame with red/blue player gauges
- **Screen Resolution**: Tested at 800×600 minimum
- **RelativePosition**: Player gauges use relative positioning for window scaling

---

## Variant Comparison

| Feature | Default | Player Gauges | Player & Weight |
|---------|---------|---------------|-----------------|
| Has Player HP/Mana | No | Yes | Yes |
| Has Weight Display | No | No | ✅ Yes (Experimental) |
| Window Height | Standard | 70px | 70px (same) |
| Uses EQType 24/25 | No | No | ✅ Yes |

---

## Configuration

To use this variant, place this folder's files in your EverQuest UI directory:

```bash
EverQuest/
├── UIFILES/
│   └── thorne_drak/
│       ├── Options/
│       │   └── Target/
│       │       └── Player Gauges and Weight/
│       │           └── EQUI_TargetWindow.xml
```

Then load with:
```
/loadskin thorne_drak
```

---

## Modification History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | Feb 3, 2026 | Added experimental weight display, positioned gauges, standardized colors |
| 1.0.0 | Feb 1, 2026 | Initial variant with player HP/Mana gauges |

---

## See Also

- [Group Window - Standard](../../Group/Standard/README.md)
- [Pet Window - Tall Gauge](../../Pet/Tall%20Gauge/README.md)
- [Player Window - Pet Bottom](../../Player/Pet%20Bottom/README.md)
- [Target Window - Standard](../Standard/README.md)
