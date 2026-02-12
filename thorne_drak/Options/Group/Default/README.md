# Window: Group - Default Variant

**File**: [EQUI_GroupWindow.xml](./EQUI_GroupWindow.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Active - Optimized Layout  
**Author**: Draknare Thorne

---
## Purpose

The Group Window displays status information for all active group members. Each group member slot shows a name, character data, health gauge, and pet health indicator. This window enables rapid assessment of party composition and member vitality during group content.

**Key Features**:
- **6-Member Display**: Full group roster (standard EQ groups)
- **Per-Member Gauges**: HP tracking for each group member
- **Pet Status Indicators**: Mini pet health gauges below member slots
- **F-Key Navigation**: Quick access hotkeys (F2-F7) for group members
- **Color-Coded Health**: Red fill indicates damage, yellow for lines
- **Compact Layout**: Vertical stacking with 25-27px per member row
- **Low Visual Weight**: Designed for peripheral monitoring

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 125 × 155 pixels (6 members × 25px + header) |
| **Layout Type** | Vertical member stack (Cornerstone) |
| **Resizable** | No |
| **Sizable** | No |
| **Titlebar** | Hidden |
| **Closebox** | Yes |
| **Minimizebox** | Yes |
| **Draw Template** | WDT_RoundedNoTitle |
| **Default Position** | X=970, Y=400 |
| **Member Rows** | 6 (F2-F7 targeting) |
| **Text Color** | RGB(240, 240, 240) - Off-white |
| **Font** | Font 1-3 (size varies) |

---

## Visual Layout

```
┌─────────────────────────┐
│ F2 [Member 1      ]     │  Y=13-27px
│    ▓▓▓▓▓▓░░░░░░ (HP)    │
│    ▓░░░░░░░░░░░ (Pet)   │
├─────────────────────────┤
│ F3 [Member 2      ]     │  Y=41-55px
│    ▓▓▓▓░░░░░░░░ (HP)    │
│    ▓▓░░░░░░░░░░ (Pet)   │
├─────────────────────────┤
│ F4 [Member 3      ]     │  Y=69-83px
│    ▓▓▓▓▓▓▓░░░░░ (HP)    │
│    [no pet]             │
├─────────────────────────┤
│ [Additional rows...]    │
└─────────────────────────┘
```

---

## Element Inventory

### Member 1 (F2 - Leader)

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| F2 Label | GW_F2Label | — | (0, 13) | 12×12px | Hotkey indicator "F2" |
| Member 1 Gauge | Gauge1 | 11 | (11, 0) | 114×24px | Full member stat display |
| Member 1 HP Fill | — | — | (3px offset) | —  | Health percentage visualization |
| Pet 1 Gauge | PetGauge1 | 17 | (11, 22) | 114×2px | Companion pet HP (thin) |

**Colors**:
- HP Fill: RGB(220, 0, 0) - Red
- Health Lines: RGB(220, 220, 0) - Yellow
- Text: RGB(240, 240, 240) - Off-white

### Member 2 (F3)

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| F3 Label | GW_F3Label | — | (0, 41) | 12×12px | Hotkey indicator "F3" |
| Member 2 Gauge | Gauge2 | 12 | (11, 28) | 114×24px | Second member display |
| Pet 2 Gauge | PetGauge2 | 18 | (11, 50) | 114×2px | Second pet HP (thin) |

### Member 3-6 (F4-F7)

**Repeating Pattern**:
- F-key label at Y=69, Y=97, Y=125, Y=153 (28px intervals)
- Member gauge spans 24px height
- Pet gauge spans 2px height below member gauge
- All maintain 114px width, 11px left offset

---

## Color Reference

**Health Gauge Colors** (Standardized):
- **Fill Color**: RGB(220, 0, 0) - Dark red for urgent visibility
- **Lines Color**: RGB(220, 220, 0) - Yellow for contrast
- **Text Color**: RGB(240, 240, 240) - Off-white for readability
- **Pet Fill**: RGB(51, 192, 51) - Green for companion distinction

**State Indicators**:
- **Full HP** (100%): Gauge shows solid bar
- **Damaged** (50-99%): Partial fill visible
- **Critical** (0-50%): Heavy flash/warning context
- **Pet Absent**: Pet gauge invisible or 0%

---

## Technical Details

### Gauge Configuration

**Member Gauges** (Sizes: 114×24px):
- **EQType 11**: Member 1 (F2)
- **EQType 12**: Member 2 (F3)
- **EQType 13**: Member 3 (F4)
- **EQType 14**: Member 4 (F5)
- **EQType 15**: Member 5 (F6)
- **EQType 16**: Member 6 (F7) -- *NOTE: Conflicts with PetHP in other windows; context-dependent*

**Pet Gauges** (Sizes: 114×2px):
- **EQType 17**: Pet 1 (under Member 1)
- **EQType 18**: Pet 2 (under Member 2)
- **EQType 19**: Pet 3
- **EQType 20**: Pet 4
- **EQType 21**: Pet 5
- **EQType 22**: Pet 6

### Layout Calculation

**Vertical Spacing**:
```
Member 1 Gauge: Y=0, Height=24px (occupies Y=0-23)
Member 1 Pet:   Y=22, Height=2px (occupies Y=22-23, overlaps with gauge)
Row Divider:    Y=25 (1px visual separator)
Member 2 Gauge: Y=28, Height=24px
[Pattern repeats every 28px]
```

**Text Offsets**:
- **TextOffsetX**: 4px (member name/data positioning)
- **TextOffsetY**: 4px (vertical centering within 24px slot)
- **GaugeOffsetX**: 3px (horizontal fill alignment)

### Relative Positioning

All elements use `RelativePosition=true` for compact layout:
- F-key labels positioned absolutely
- Gauge and pet elements chain relatively
- Divider line spans full window width (250px line decorations)

---

## Related Windows & Dependencies

### Connected Windows
- **Player Window** (EQUI_PlayerWindow.xml): Primary character data source
- **Target Window** (EQUI_TargetWindow.xml): Target member selection interface
- **Actions Window** (EQUI_ActionsWindow.xml): May coordinate group actions

### Standards References
- F-key bindings: F2=Member1, F3=Member2, .... F7=Member6
- EQType system for real-time member data updates
- Group composition data fed by game client

---

## Recent Updates (v1.0.0)

**January-February 2026**:
- ✅ Fixed F-key label overlap with player names
- ✅ Optimized layout and positioning for readability
- ✅ Enhanced visual clarity for group member information
- ✅ Gauge border styling applied consistently
- ✅ Pet health indicators visible and styled

**Design Improvements**:
- F-key labels moved to prevent text collision with member names
- Spacing adjusted to 28px per member for visual separation
- Pet gauge height reduced to 2px for minimal intrusion
- Divider lines added between member slots for clarity

---

## Developer Notes

**One-Glance Assessment**: The Group Window prioritizes **rapid status reading**. Players should instantly recognize:
1. Which members are alive (gauge visible)
2. Rough damage level (fill height)
3. Pet summoning status (pet gauge presence)

**F-Key Integration**: F2-F7 hotkeys allow direct member targeting without mouse interaction. Position of labels is optimized to not obscure member names.

**Future Enhancements**:
- Class icons next to member names
- Buff/debuff indicator dots
- Mana/Endurance secondary gauges (optional)
- Group member level indicators

---

**Version**: 1.0.0 | **Last Updated**: February 3, 2026 | **Status**: ✅ Active
