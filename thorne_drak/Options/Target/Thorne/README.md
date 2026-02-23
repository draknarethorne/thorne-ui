# Window: Target - Thorne Variant

**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)  
**Version**: 2.5.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Active - Phase 6 Experimental (Player Gauges Added)  
**Author**: Draknare Thorne

---
## Purpose

The Target Window displays information about the currently selected combat target. It shows target health, mana, casting status, and integrates player vitals for quick reference during combat. Unique among Thorne UI windows, this window displays **both player and target data**, enabling side-by-side comparison of combat readiness.

**Key Features**:
- **Dual HP/Mana Display**: Player gauges (top) + Target gauges (middle)
- **Real-time Status Updates**: Target health, mana, and AC indicators
- **Casting Indicator Gauge**: Shows spell casting progress/duration
- **Pet Health Tracking**: Small purple gauge for summoned companion HP
- **Mana Regen Timer**: Cyan gauge showing player mana cooldown
- **Weight Display**: Experimental center display showing player weight burden
- **Percentage Indicators**: HP/Mana percentages for both player and target
- **Combat Efficiency Metrics**: AC, Resistances (if applicable)

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 272 × 70 pixels (dual-gauge layout) |
| **Layout Type** | Symmetric dual-section (Player left, Target right) |
| **Resizable** | No |
| **Sizable** | No |
| **Titlebar** | Hidden |
| **Closebox** | Present |
| **Minimizebox** | Present |
| **Draw Template** | WDT_RoundedNoTitle |
| **Thorne Position** | X=500, Y=100 |
| **Background** | Dark with subtle gradient |
| **Divider** | Center-aligned between player/target data |
| **Font (Primary)** | Font 2-5 (size varies) |

---

## Visual Layout

```
┌──────────────────┬──────────────────┐
│ HP: 100% | /Mana │ Target: 75% HP   │  Y=0-15px
│ ▓▓▓▓▓▓▓▓▓░░░░░░░│▓▓▓▓▓▓░░░░░░░░░░│  Red/Target fills
├──────────────────┼──────────────────┤
│ 999/999 ▓░░▓░░   │ [AC] [Target HP] │  Y=16-24px
│ Wgt: 999/999     │ ▓▓▓▓▓▓▓░░░░░░░░ │  Player weight
├──────────────────┼──────────────────┤
│ Pet: ▓▓▓░░░░░░░░ │ Cast: ▓▓▓▓░░░░░ │  Y=25-34px
│                   │ ▓▓▓░░░░░░░░░░░░ │  Casting bar
└──────────────────┴──────────────────┘
```

---

## Element Inventory

### Header Section (Player Left Side)

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| Player HP % | TW_HP_Pct | 19 | (-1, 0) | 25×15px | HP percentage (right-aligned) |
| Player HP % Sign | TW_HP_PctSign | — | (24, 0) | 16×15px | % symbol separator |
| Player HP Values | TW_HP_Values | 70 | (36, 0) | 81×15px | Current/Max HP display |
| Player Mana % | TW_Mana_Pct | 20 | (216, 0) | 25×15px | Mana percentage (right-aligned) |
| Player Mana % Sign | TW_Mana_PctSign | — | (241, 0) | 16×15px | % symbol separator |

### Gauge Row 1 (Player Metrics - Y=16px)

| Element | ScreenID | EQType | Position | Size | Fill Color | Purpose |
|---------|----------|--------|----------|------|------------|---------|
| Player HP Gauge | TW_PlayerHP_Gauge | 1 | (2, 16) | 122×8px | Red (255, 0, 0) | Player current HP bar |
| Player Mana Gauge | TW_PlayerMana_Gauge | 2 | (148, 16) | 122×8px | Blue (30, 30, 255) | Player current Mana bar |

### Weight Display (Experimental - Center)

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| Weight Current | TW_Weight_Current | 24 | (99, 18) | 25×13px | Current weight (right-aligned) |
| Weight Divider | TW_Weight_Divider | — | (123, 18) | 7×13px | "/" separator |
| Weight Max | TW_Weight_Max | 25 | (129, 18) | 25×13px | Max capacity (left-aligned) |

### Pet & Regen Section (Y=21-24px)

| Element | ScreenID | EQType | Position | Size | Fill Color | Purpose |
|---------|----------|--------|----------|------|------------|---------|
| Pet Health Gauge | TW_PetHealth_Gauge | 16 | (2, 24) | 122×8px | Purple (200, 80, 200) | Pet companion HP |
| Mana Tick Gauge | TW_ManaTick_Gauge | 24 | (148, 21) | 103×8px | Cyan (0, 220, 220) | Mana regeneration timer |

### Target Data Section (Right Half)

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| Target HP Gauge | TW_TargetHP_Gauge | 29 | (2, 34) | 122×12px | Red gradient | Target current HP |
| Target HP % | TW_TargetHP_Pct | 29 | (204, 34) | 30×15px | HP percentage indicator |
| Target Mana Gauge | TW_TargetMana_Gauge | 30 | (148, 34) | 122×12px | Blue gradient | Target current Mana |
| Casting Bar | TW_CastingBar_Gauge | 31 | (2, 46) | 268×8px | Green/Yellow | Spell casting progress |

---

## Color Reference

**Player-Side Gauges**:
- **HP (Red)**: RGB(255, 0, 0) - Standard player health
- **Mana (Blue)**: RGB(30, 30, 255) - Player resource
- **Pet HP (Purple)**: RGB(200, 80, 200) - Companion status
- **Mana Tick (Cyan)**: RGB(0, 220, 220) - Regen countdown

**Target-Side Gauges**:
- **Target HP**: RGB(200, 0, 0) - Reduced intensity red
- **Target Mana**: RGB(60, 100, 200) - Muted blue
- **Casting Bar** (active): RGB(100, 200, 100) - Green for completion
- **Casting Bar** (pending): RGB(200, 150, 50) - Gold/yellow for hold

**Text Colors**:
- HP values: RGB(255, 100, 100) - Red-tinted
- Mana values: RGB(100, 150, 255) - Blue-tinted
- Target name: RGB(255, 255, 255) - White (standard)

---

## Technical Details

### Window Zones

**Zone 1 (Player Left - X=2-145)**:
- Player HP/Mana percentage displays (Y=0-15px)
- Player weight center display (experimental)
- Player HP/Mana gauges (Y=16-24px)
- Pet health mini-gauge

**Zone 2 (Divider - X=146-147)**:
- Logical separator between player and target data
- Not rendered (invisible boundary)

**Zone 3 (Target Right - X=148-271)**:
- Target HP percentage and values
- Target HP/Mana gauges
- Casting bar spanning full width
- Mana regen timer in corner

### EQType Mappings

- **EQType 1**: Player HP (gauge fill %)
- **EQType 2**: Player Mana (gauge fill %)
- **EQType 16**: Pet HP (secondary gauge)
- **EQType 19**: Player HP percentage (label)
- **EQType 20**: Player Mana percentage (label)
- **EQType 24**: Mana regeneration timer (tick gauge)
- **EQType 25**: Player max weight (display)
- **EQType 29**: Target HP percentage (label)
- **EQType 30**: Target Mana gauge
- **EQType 31**: Casting bar progress (spell duration)
- **EQType 70**: Player HP numeric (Current/Max)
- **EQType 80**: Player Mana numeric (Current/Max)

### Gauge Dimensions

**Standard Gauge**:
- **Width**: 122×8px (typical horizontal bar)
- **Height**: 8-12px variant for different gauge types

**Extended Gauges**:
- **Casting Bar**: Full-window width (268px) for dramatic spell visualization

**Mini Gauges**:
- **Pet HP**: Compact 3-8px height for space efficiency  
- **Mana Tick**: Minimal 8px height with low visual weight

---

## Recent Updates & Experimental Features

**Phase 5 Enhancements (Feb 2026)**:
- ✅ Added player HP gauge (EQType 1) - symmetric with target
- ✅ Added player Mana gauge (EQType 2) - balanced display
- ✅ Increased window height to accommodate player metrics
- ✅ Implemented symmetric layout (player left, target right)
- ✅ Standardized mana color to "Thorne blue" RGB(100,150,255)

**Phase 6 Experimental Features**:
- 🔬 Player weight display (center-positioned)
  - Format: "999/999" (current/max capacity)
  - Location: X=90-147, Y=20px
  - **Status**: Experimental - may be removed if cluttered
- 🔬 All EQType labels maintained with % symbols
- 🔬 Compatible with "Exact Mana" calculations (Zeal addon)

**Known Limitations**:
- Target updates dependent on game client targeting system
- Pet gauge only displays when pet is summoned
- Casting bar visibility tied to spell queue system
- Weight display may conflict with narrow UI layouts

---

## Related Windows & Dependencies

### Connected Windows
- **Player Window** (EQUI_PlayerWindow.xml): Provides player data source
- **Group Window** (EQUI_GroupWindow.xml): May reference target data
- **Actions Window** (EQUI_ActionsWindow.xml): May use target state for ability qualifying
- **Combat Windows**: General combat UI coordination

### Standards References
- Zeal Addon: Exact mana calculation support
- QQQuarm Server: Target system compatibility
- See EQTYPES.md for EQType system documentation

---

## Developer Notes (Draknare Thorne)

**Design Intent**: The Target Window serves as **combat command center**, enabling players to quickly assess both personal readiness and target vulnerability. The player data on the left is always-visible context, while target data dominates the right side for tactical focus.

**Phase 6 Experimentation**: The weight display is intentionally center-positioned to test whether burden indicators improve combat awareness. Player feedback will determine retention in v2.6.0.

**Future Enhancements**:
- Distance to target indicator
- Target AC display
- Resistances breakdown by type
- Buff/debuff icons adjacent to gauges

---

**Version**: 2.5.0 | **Last Updated**: February 3, 2026 | **Status**: ✅ Active with Experimental Features
