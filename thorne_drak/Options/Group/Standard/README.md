# Group Window - Standard Variant

**File**: [EQUI_GroupWindow.xml](./EQUI_GroupWindow.xml)
**Version**: 1.1.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Enhanced with optimized positioning  
**Author**: Draknare Thorne

---
## Purpose

The "Standard" Group Window displays real-time health and mana information for 5-member groups (F2-F6 raid targets). This is the baseline, recommended configuration for all group play scenarios.

**Key Features**:

- **Group Member Tracking**: 5 separate rows (F2 through F6)
- **Health Gauges**: Red HP bars (EQType 11-15) showing current/maximum health
- **Mana Display**: Blue mana bars with percentage indicators
- **Percentage Display**: Health and mana percentages at standardized X positions
- **Color-Coded**: Red for HP, blue for mana, white text on colored bars
- **Clean Layout**: Minimalist design optimized for quick information scanning
- **Multi-Class Support**: Works for any group composition

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 260 × 160 pixels (approximate) |
| Resizable | Yes |
| Fadeable | Yes |
| Screen ID | GroupWindow |
| DrawTemplate | WDT_RoundedNoTitle |
| Titlebar | Yes |
| Closebox | Yes |
| Minimizebox | Yes |
| Number of Group Members | 5 (F2-F6) |
| Member Row Height | 26 pixels |
| Gauge Height | 24 pixels |

---

## Key Modifications (v1.1.0 - Feb 3, 2026)

### Positioning Optimization

**Gauge Positioning** (Applied to all 5 group members):
- **Previous**: X=16
- **Updated**: X=11
- **Change**: Moved left 5px for more compact layout
- **Benefit**: Shifts entire window left, reducing screen real estate usage

**Health Label Positioning** (Applied to all 5 group members):
- **Previous**: X=74
- **Updated**: X=82
- **Change**: Moved right 8px
- **Benefit**: Aligns with Player Window and Target Window for cross-window consistency

**Health Percentage Positioning** (Applied to all 5 group members):
- **Previous**: X=136
- **Updated**: X=142
- **Change**: Moved right 6px
- **Benefit**: Standard alignment across all player/target/group windows

### Visual Consistency

These positioning changes align Group Window with Player Window and Target Window, allowing players to reference health information across windows without cognitive dissonance from varying label positions.

---

## Layout Details

### Vertical Organization

```
┌────────────────────────────────────┐
│ Group Window (F2-F6 Targets)       │
├────────────────────────────────────┤
│ [HP Gauge] [Label] [Pct] [Mana]   │  ← F2
│ [HP Gauge] [Label] [Pct] [Mana]   │  ← F3
│ [HP Gauge] [Label] [Pct] [Mana]   │  ← F4
│ [HP Gauge] [Label] [Pct] [Mana]   │  ← F5
│ [HP Gauge] [Label] [Pct] [Mana]   │  ← F6
└────────────────────────────────────┘
```

### Positioning Reference

| Element | Position | Size | EQType | Notes |
|---------|----------|------|--------|-------|
| **F2 HP Gauge** | X=11, Y=4 | 114×24 | 11 | Red bar, left-aligned |
| **F2 HP Label** | X=82, Y=10 | - | N/A | Numeric health value |
| **F2 HP %** | X=142, Y=10 | - | N/A | Percentage indicator |
| **F3 HP Gauge** | X=11, Y=32 | 114×24 | 12 | Red bar |
| **F3 HP Label** | X=82, Y=38 | - | N/A | Numeric health value |
| **F3 HP %** | X=142, Y=38 | - | N/A | Percentage indicator |
| **F4 HP Gauge** | X=11, Y=60 | 114×24 | 13 | Red bar |
| **F4 HP Label** | X=82, Y=66 | - | N/A | Numeric health value |
| **F4 HP %** | X=142, Y=66 | - | N/A | Percentage indicator |
| **F5 HP Gauge** | X=11, Y=88 | 114×24 | 14 | Red bar |
| **F5 HP Label** | X=82, Y=94 | - | N/A | Numeric health value |
| **F5 HP %** | X=142, Y=94 | - | N/A | Percentage indicator |
| **F6 HP Gauge** | X=11, Y=116 | 114×24 | 15 | Red bar |
| **F6 HP Label** | X=82, Y=122 | - | N/A | Numeric health value |
| **F6 HP %** | X=142, Y=122 | - | N/A | Percentage indicator |

### Color Scheme

| Element | RGB Values | Usage |
|---------|-----------|-------|
| HP Gauge Bar | (255, 0, 0) | Red health display |
| HP Gauge Border | (0, 0, 0) | Black outline |
| Text Labels | (255, 255, 255) | White text (high contrast) |
| Window Background | (50, 50, 50) | Dark gray |
| Window Border | (0, 0, 0) | Black edge |

---

## Alignment with Other Windows

Group Window Standard positioning now aligns with:

- **Target Window**: Percentage displays at X=142
- **Player Window**: Health value positions at X=82
- **Pet Window**: Gauge styling (red HP, white text)

**Cross-Window Consistency**:
```
Standard X Positions (v1.1.0):
- Health values: X=82 (Group, Player, Target)
- Percentages: X=142 (Group, Player, Target)
- Pet gauges: Positioned identically across windows
```

---

## Configuration

To use this variant, place this folder's files in your EverQuest UI directory:

```bash
EverQuest/
├── UIFILES/
│   └── thorne_drak/
│       ├── Options/
│       │   └── Group/
│       │       └── Standard/
│       │           ├── EQUI_GroupWindow.xml
│       │           └── README.md
```

Then load with:
```
/loadskin thorne_drak
```

---

## Testing Recommendations

1. Load UI: `/loadskin thorne_drak`
2. Join a group and verify:
   - All 5 member rows display correctly
   - Health gauges update in real-time
   - Percentages display accurately
   - Text doesn't overlap gauge or labels
3. Check positioning:
   - Gauges at X=11 (left edge)
   - Health labels at X=82 (right side)
   - Percentages at X=142 (far right)
4. Compare with other windows:
   - Player Window health values should align at X=82
   - Percentages should align at X=142

---

## Modification History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | Feb 3, 2026 | Optimized positioning (gauges X=16→11, labels X=74→82, pct X=136→142) |
| 1.0.0 | Feb 1, 2026 | Initial Standard Group Window variant |

---

## Technical Notes

- **Gauge Synchronization**: All 5 member row gauges update simultaneously using EQType 11-15 for HP and EQType 36-40 for Mana
- **Cross-Window Alignment**: Horizontal positioning (X=82 labels, X=142 percentages) matches Player Window and Target Window for visual consistency
- **Memory Efficiency**: Standard 5-member layout uses minimal texture resources compared to larger raid windows

---

## See Also

- [Target Window - Player Gauges and Weight](../../Target/Player%20Gauges%20and%20Weight/README.md)
- [Player Window - Pet Bottom](../../Player/Pet%20Bottom/README.md)
- [Pet Window - Tall Gauge](../../Pet/Tall%20Gauge/README.md)
- [Options Directory Overview](../README.md)
