# Inventory Analysis: Nemesis

## Executive Summary

The Nemesis inventory is a compact, vertically oriented window that consolidates character stats, equipment, and primary inventory bags into a single, unified view. It deviates significantly from the default layout, opting for a tall and narrow footprint. Its most notable feature is the integration of player stats directly alongside the equipment slots, creating a dense but efficient character overview. The design prioritizes function over elaborate visuals, using standard UI elements.

## Quick Reference
- **Directory**: `Nemesis/`
- **Window Size**: Approx. 240x330 (inferred from element positions)
- **Template**: Custom, not based on `EQLSUI_Templates.xml`
- **Total Elements**: ~120
- **Subwindows**: No
- **Unique Features**:
    - Integrated stats and equipment panel.
    - Vertical layout.
    - Compact footprint.
    - No distinct visual separation between equipment and stats.

## Layout Architecture

The Nemesis inventory window is a single, non-subwindow layout. It is organized into three main vertical sections: a left-side character/stat block, a central equipment block, and a right-side inventory block, though the equipment and stats are heavily intertwined.

```
┌──────────────────────────────────────────┐
│ Nemesis Inventory (Approx. 240x330)      │
├──────────────────────────────────────────┤
│ ┌──────────────────┬───────────────────┐ │
│ │ CHARACTER INFO   │ EQUIPMENT SLOTS   │ │
│ │ (X:8, Y:4)       │ (X:0-200, Y:0-160)│ │
│ │ Name, Level,     │ Anatomical Layout   │ │
│ │ Deity, HP, AC,   │                   │ │
│ │ ATK, Stats       │                   │ │
│ └──────────────────┴───────────────────┘ │
│ ┌──────────────────────────────────────┐ │
│ │ GAUGES (XP/AA)                       │ │
│ │ (X:2, Y:112)                         │ │
│ └──────────────────────────────────────┘ │
│ ┌──────────────────────────────────────┐ │
│ │ INVENTORY BAGS (8 slots)             │ │
│ │ (X:80-120, Y:165-285)                │ │
│ └──────────────────────────────────────┘ │
│ ┌──────────────────────────────────────┐ │
│ │ BUTTONS (Done, etc.)                 │ │
│ │ (Not defined in this file)           │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## Equipment Display

The equipment slots are arranged in a loose, non-standard anatomical layout. The positions are somewhat counter-intuitive compared to other UIs.

**Complete Equipment Coordinate Map**
```
ROW 1 - HEAD LEVEL (Y=0):
├─ InvSlot0  [CHARM]      (40x40, X=0, Y=0)
├─ InvSlot1  [LEFT_EAR]   (40x40, X=40, Y=0)
├─ InvSlot5  [NECK]       (40x40, X=80, Y=0)
├─ InvSlot3  [FACE]       (40x40, X=120, Y=0)
├─ InvSlot2  [HEAD]       (40x40, X=160, Y=0)
└─ InvSlot4  [RIGHT_EAR]  (40x40, X=0, Y=0)  <- Overlaps with Charm

ROW 2 - ARM LEVEL (Y=40):
├─ InvSlot15 [LEFT_FINGER](40x40, X=0, Y=40)
├─ InvSlot9  [LEFT_WRIST] (40x40, X=40, Y=40)
├─ InvSlot7  [ARMS]       (40x40, X=80, Y=40)
├─ InvSlot12 [HANDS]      (40x40, X=120, Y=40)
├─ InvSlot10 [RIGHT_WRIST](40x40, X=160, Y=40)
└─ InvSlot16 [RIGHT_FINGER](40x40, X=200, Y=40)

ROW 3 - CHEST LEVEL (Y=80):
├─ InvSlot6  [SHOULDERS]  (40x40, X=0, Y=80)
├─ InvSlot17 [CHEST]      (40x40, X=40, Y=80)
├─ InvSlot8  [BACK]       (40x40, X=80, Y=80)
├─ InvSlot20 [WAIST]      (40x40, X=120, Y=80)
├─ InvSlot18 [LEGS]       (40x40, X=160, Y=80)
└─ InvSlot19 [FEET]       (40x40, X=200, Y=80)

ROW 4 - WEAPONS/AMMO (Y=120):
├─ InvSlot13 [PRIMARY]    (40x40, X=0, Y=120)
├─ InvSlot14 [SECONDARY]  (40x40, X=40, Y=120)
├─ InvSlot11 [RANGE]      (40x40, X=80, Y=120)
└─ InvSlot21 [AMMO]       (40x40, X=120, Y=120)
```

## Stat Display

Stats are displayed to the left of the equipment slots, in a single column.

**Complete Stat Coordinate Listing**
```
├─ IW_Name       (Label, X=8, Y=4)
├─ IW_Level      (Label, X=8, Y=18)
├─ IW_Deity      (Label, X=8, Y=32)
├─ IW_HP         (Label, X=14, Y=50)
├─ IW_CurrentHP  (Label, X=40, Y=50)
├─ IW_MaxHP      (Label, X=83, Y=50)
├─ IW_AC         (Label, X=14, Y=64)
├─ IW_ACNumber   (Label, X=40, Y=64)
├─ IW_ATK        (Label, X=14, Y=78)
├─ IW_ATKNumber  (Label, X=40, Y=78)
├─ IW_STR        (Label, X=30, Y=130)
├─ IW_STRNumber  (Label, X=60, Y=130)
├─ IW_STA        (Label, X=30, Y=144)
├─ IW_STANumber  (Label, X=60, Y=144)
├─ IW_AGI        (Label, X=30, Y=158)
├─ IW_AGINumber  (Label, X=60, Y=158)
├─ IW_DEX        (Label, X=30, Y=172)
├─ IW_DEXNumber  (Label, X=60, Y=172)
├─ IW_WIS        (Label, X=30, Y=186)
├─ IW_WISNumber  (Label, X=60, Y=186)
├─ IW_INT        (Label, X=30, Y=200)
├─ IW_INTNumber  (Label, X=60, Y=200)
├─ IW_CHA        (Label, X=30, Y=214)
├─ IW_CHANumber  (Label, X=60, Y=214)
├─ IW_MR         (Label, X=10, Y=238)
├─ IW_MRNumber   (Label, X=40, Y=238)
├─ IW_FR         (Label, X=10, Y=252)
├─ IW_FRNumber   (Label, X=40, Y=252)
├─ IW_CR         (Label, X=10, Y=266)
├─ IW_CRNumber   (Label, X=40, Y=266)
├─ IW_DR         (Label, X=10, Y=280)
├─ IW_DRNumber   (Label, X=40, Y=280)
├─ IW_PR         (Label, X=10, Y=294)
├─ IW_PRNumber   (Label, X=40, Y=294)
```

## Gauges & Progress Bars

A standard XP gauge is present below the main stat block.

**Gauge Specifications**
```
├─ IW_ExpGauge    (X=2, Y=112, 1x1, Color: 220,150,0, EQType: 4)
├─ IW_AltAdvGauge (X=2, Y=112, 1x1, Color: 0,180,255, EQType: 25)
```

## Unique Features

- **Overlapping Slots**: `InvSlot0` (Charm) and `InvSlot4` (Right Ear) have the same coordinates (X=0, Y=0), which is unusual and may indicate a bug or a specific design choice for certain classes.
- **Compact Stat Block**: All primary stats, saves, and combat stats are tightly packed into a single vertical column, making it easy to see everything at a glance without scrolling or tabbing.
- **Non-Standard Layout**: The equipment layout does not follow the typical "paper doll" arrangement, requiring some user adjustment.

## Recommendations for Thorne_Drak

1. **Adopt Compactness**: The Nemesis layout is very efficient in its use of space. A similar compact, all-in-one approach could be a valuable option for users who prefer minimal UI footprints.
2. **Re-evaluate Stat Placement**: Placing stats directly next to equipment is a strong design pattern. Consider integrating stats more closely with the equipment display in Thorne variants.
3. **Avoid Overlapping Elements**: The overlapping ear/charm slots should be avoided. Ensure all slots have unique and clear positions.
4. **Consider Vertical Orientation**: While most inventories are horizontal, a vertical option inspired by Nemesis could appeal to users with specific screen setups or playstyles.

---
*Analysis generated by GitHub Copilot. February 4, 2026.*