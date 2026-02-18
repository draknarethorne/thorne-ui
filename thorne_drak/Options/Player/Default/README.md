# Window: Player - Default Variant

**File**: [EQUI_PlayerWindow.xml](./EQUI_PlayerWindow.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-17
**Status**: ✅ Active - First Draft Implementation  
**Author**: Draknare Thorne

---
## Purpose

The Player Window displays comprehensive character information and vital statistics. Designed with a hybrid aesthetic combining Infiniti-Blue gauge styling, duxaUI icon methodology, and vert stats layout. This window serves as the central hub for monitoring player health, mana, stamina, experience, and other critical performance metrics.

**Key Features**:
- **Three-Gauge Primary Display**: HP (Red), Mana (Blue), Stamina (Yellow)
- **Experience Tracking**: Green XP gauge for level progression
- **Mana Regeneration Timer**: Cyan tick gauge showing mana regen status
- **Pet Health Display**: Purple gauge for companion pet HP (when applicable)
- **Percentage Indicators**: Real-time percentage displays for all major gauges
- **Attack Indicator Border**: Visual combat state indication
- **Character Information**: Player name, class, and level display
- **Numeric Values Display**: Current/Max values for HP and Mana

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 268 × 70 pixels (expanded content area) |
| **Layout Type** | Vertical gauge stack (Cornerstone) |
| **Resizable** | No |
| **Sizable** | No |
| **Titlebar** | Hidden |
| **Closebox** | Present |
| **Minimizebox** | Present |
| **Draw Template** | WDT_RoundedNoTitle |
| **Default Position** | X=100, Y=100 |
| **Text Color (Primary)** | RGB(255, 255, 255) - White |
| **Font (Primary)** | Font 1-2 (variable sizing) |

---

## Visual Layout

```
┌─────────────────────────────────────────┐
│ Player_Name      Class_Name        Lv60 │  Y=6px
├─────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░  100% │  Y=26px (HP)
│ HP: Current/Max                         │
├─────────────────────────────────────────┤
│ ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░  75% │  Y=43px (Mana)
│ Mana: Current/Max                       │
├─────────────────────────────────────────┤
│ ▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 45% │  Y=60px (Stamina)
│ [Mana Tick - 0/0]                       │  Y=52px
└─────────────────────────────────────────┘
```

---

## Element Inventory

### Header Section

| Element | ScreenID | Type | Position | Size | Purpose |
|---------|----------|------|----------|------|---------|
| Player Name | PW_PlayerName | Label | (5, 6) | 100×14px | Character name display (White text) |
| Class Name | PW_PlayerClass | Label | (107, 6) | 90×14px | Player class name (centered) |
| Player Level | PW_PlayerLevel | Label | (200, 6) | 20×14px | Level value (right-aligned, e.g., "60") |

### Gauge Section

| Element | ScreenID | EQType | Position | Size | Fill Color | Purpose |
|---------|----------|--------|----------|------|------------|---------|
| HP Gauge | PW_Gauge_HP | 1 | (2, 26) | 120×15px | Red (255, 0, 0) | Current HP visualization |
| HP Percent | PW_HP_Pct | 19 | (123, 26) | 25×12px | White | HP percentage (EQType-driven) |
| HP Values | PW_HP_Values | 70 | (170, 26) | 50×12px | Red-tinted (255, 100, 100) | Current/Max HP display |
| Mana Gauge | PW_Gauge_Mana | 2 | (2, 43) | 120×15px | Blue (30, 30, 255) | Current Mana visualization |
| Mana Percent | PW_Mana_Pct | 20 | (123, 43) | 25×12px | White | Mana percentage (EQType-driven) |
| Mana Values | PW_Mana_Values | 80 | (170, 43) | 50×12px | "Thorne Blue" (100, 150, 255) | Current/Max Mana display |

### Additional Gauges

| Element | ScreenID | EQType | Position | Size | Fill Color | Purpose |
|---------|----------|--------|----------|------|------------|---------|
| Stamina Gauge | PW_Gauge_Stamina | 3 | (2, 60) | 120×15px | Yellow (255, 255, 0) | Stamina visualization |
| XP Gauge | PW_Gauge_XP | 4 | (2, 77) | 120×12px | Green (0, 200, 0) | Experience progression bar |
| Mana Tick | ManaTick | 24 | (2, 52) | 120×8px | Cyan (0, 220, 220) | Mana regen timer indicator |
| Pet HP Gauge | PW_Gauge_PetHP | 5 | (2, 94) | 120×3px | Purple (150, 0, 200) | Pet companion health (small) |

---

## Color Reference

**Primary Gauges** (Standardized across Thorne UI):
- **HP (Red)**: RGB(255, 0, 0) - Critical player vitals
- **Mana (Blue)**: RGB(30, 30, 255) or Thorne Blue RGB(100, 150, 255) - Resource management
- **Stamina (Yellow)**: RGB(255, 255, 0) - Endurance indicator
- **XP (Green)**: RGB(0, 200, 0) - Progression tracking
- **Pet HP (Purple)**: RGB(150, 0, 200) - Companion status
- **Mana Tick (Cyan)**: RGB(0, 220, 220) - Regen countdown

**Text Colors**:
- Primary text: RGB(255, 255, 255) - White
- HP values: RGB(255, 100, 100) - Red-tinted for emphasis
- Mana values: RGB(100, 150, 255) - Blue-tinted for emphasis

---

## Technical Details

### EQType Mappings

- **EQType 1**: Player HP (primary gauge connection)
- **EQType 2**: Player Mana (primary gauge connection)
- **EQType 3**: Stamina (secondary vital)
- **EQType 4**: Experience progression
- **EQType 5**: Pet HP (if pet active)
- **EQType 19**: HP Percentage (calculated display)
- **EQType 20**: Mana Percentage (calculated display)
- **EQType 24**: Mana Tick/Regen Timer
- **EQType 70**: HP Values display (Current/Max format)
- **EQType 80**: Mana Values display (Current/Max format)

### Gauge Draw Templates

All gauges utilize standardized draw templates:
- **Background**: `A_GaugeBackground_Tall` - Recessed background for 15px gauges
- **Fill**: `A_GaugeFill_Tall` - Color-filled portion indicating current value
- **Lines** (disabled): Would show grid lines if enabled
- **LinesFill** (disabled): Suppressed for cleaner appearance

### Relative Positioning Strategy

- **RelativePosition**: true (for most elements except Name/Class/Level)
- **Automatic Z-ordering**: Elements render in declaration order
- **Text Offset Suppression**: TextOffsetY=-250 hides EQType-driven labels for clean UI

---

## Related Windows & Dependencies

### Connected Windows
- **Actions Window** (EQUI_ActionsWindow.xml): May display player stats in integrated format
- **Target Window** (EQUI_TargetWindow.xml): Shows parallel player gauge data for comparison
- **Group Window** (EQUI_GroupWindow.xml): References player data in group UI

### Standards References
- See STANDARDS.md for window positioning guidelines
- See EQTYPES.md for EQType value mappings and auto-update mechanics
- Part of "Phase 1" and "Phase 5" UI standardization efforts

---

## Variant Comparison - Player Window Variants

| Feature | Default (This) | Standard | Pet Bottom | AA & XP Bottom |
|---------|----------------|----------|-----------|-----------------|
| **Window Height** | 70px | 120px | 70px | 75px |
| **Gauges Displayed** | HP, Mana, Stamina, XP, Pet, Mana Tick | HP, Mana, Stamina, XP, Mana Tick | HP, Mana, Stamina, Pet (focused) | HP, Mana, Stamina, AA, XP |
| **Compact Layout** | ✅ Yes | No (taller) | ✅ Yes | ✅ Yes |
| **Pet Display** | ✅ Small separate | No | ✅ Prominent | No |
| **Use Case** | General gameplay | Balanced display | Pet-focused | AA builders |

---

## What Makes This "Default" Variant

This Player Window variant represents the optimal balance:
- **Hybrid Layout**: Combines best of Standard (info density) and specialized variants (pet support, AA tracking)
- **All Primary Gauges**: HP, Mana, Stamina, XP all present without excessive height
- **Pet Support**: Small pet gauge included without compromising main information
- **Space Efficient**: 70px height balances info with screen real estate usage
- **Reference Implementation**: Serves as middle ground between compact and comprehensive variants
- **Thorne Standard**: Matches overall design philosophy of accessibility + customization

### Design Advantages

- **Balanced Information**: Player, standard targets, and pets all fit in minimal window space
- **Combat Ready**: HP and Mana are immediate visual focus with percentage indicators
- **Extensible**: Support for future gauge additions (buff bars, resources) without breaking layout
- **Resolution Agnostic**: 268×70 pixel window works on 800×600 through modern displays
- **Consistency**: Window metric positions align with Target, Group, and Pet windows for UI cohesion

---

## Developer Notes

**Design Philosophy**: This window prioritizes **information density** while maintaining **visual clarity**. The three primary gauges (HP/Mana/Stamina) are the first visual focus, with smaller secondary indicators for XP and pet status.

### Key Performance Metrics

The Player/Default variant is optimized for:
- **Combat Readiness**: HP gauge placement at eye-level for instant threat assessment
- **Resource Management**: Mana and stamina always visible for ability usage decisions
- **Pet Awareness**: Dedicated small gauge for summoned companion tracking without clutter
- **Experience Tracking**: Green XP gauge provides constant level progression feedback

---

**Version**: 1.0.0 | **Last Updated**: February 3, 2026 | **Status**: ✅ Active
