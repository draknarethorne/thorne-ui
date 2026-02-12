# Inventory Analysis: QQQuarm

## Executive Summary

The QQQuarm inventory is a heavily modified, feature-rich window that serves as a comprehensive character management hub. It is based on the original QQ UI but includes numerous enhancements for the Quarm server context. The layout is split into three distinct columns: equipment on the left, stats and character info in the center, and inventory bags on the right. It introduces several quality-of-life features not found in the default UI, such as explicit percentage labels for XP/AA and a more detailed stat breakdown.

## Quick Reference
- **Directory**: `QQQuarm/`
- **Window Size**: Approx. 365x330 (inferred from element positions)
- **Template**: Custom, not based on `EQLSUI_Templates.xml`
- **Total Elements**: ~150
- **Subwindows**: No
- **Unique Features**:
    - Three-column layout (Equip | Stats | Bags).
    - Explicit XP and AA percentage labels.
    - Detailed stat and resistance groupings.
    - Clickable inventory bags with labels.
    - Modernized aesthetic with custom colors.

## Layout Architecture

QQQuarm uses a clean, three-column design that separates equipment, character information, and inventory into logical, easy-to-read sections.

```
┌──────────────────────────────────────────────────┐
│ QQQuarm Inventory (Approx. 365x330)              │
├──────────────────────────────────────────────────┤
│ ┌──────────────┬────────────────┬──────────────┐ │
│ │ EQUIPMENT    │ CHARACTER INFO │ INVENTORY    │ │
│ │ (X:0, Y:0)   │ (X:245, Y:4)   │ (X:156, Y:165)│ │
│ │ Anatomical   │ Name, Level,   │ 8 Bag Slots  │ │
│ │ Grid Layout  │ Deity, HP, AC, │ in 2 columns │ │
│ │              │ ATK, Stats     │              │ │
│ └──────────────┴────────────────┴──────────────┘ │
│                ┌────────────────┐                │
│                │ GAUGES (XP/AA) │                │
│                │ (X:244, Y:129) │                │
│                └────────────────┘                │
│ ┌──────────────────────────────────────────────┐ │
│ │ BUTTONS (Done, etc.)                         │ │
│ │ (Not defined in this file)                   │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

## Equipment Display

The equipment slots are arranged in a clean, symmetrical, and anatomical grid on the left side of the window.

**Complete Equipment Coordinate Map**
```
ROW 1 - HEAD LEVEL (Y=-1):
├─ InvSlot1  [LEFT_EAR]   (40x40, X=38, Y=-1)
├─ InvSlot5  [NECK]       (40x40, X=77, Y=-1)
├─ InvSlot3  [FACE]       (40x40, X=116, Y=-1)
├─ InvSlot2  [HEAD]       (40x40, X=155, Y=-1)
└─ InvSlot4  [RIGHT_EAR]  (40x40, X=194, Y=-1)

ROW 2 - ARM LEVEL (Y=38):
├─ InvSlot15 [LEFT_FINGER](40x40, X=-1, Y=38)
├─ InvSlot9  [LEFT_WRIST] (40x40, X=38, Y=38)
├─ InvSlot7  [ARMS]       (40x40, X=77, Y=38)
├─ InvSlot12 [HANDS]      (40x40, X=116, Y=38)
├─ InvSlot10 [RIGHT_WRIST](40x40, X=155, Y=38)
└─ InvSlot16 [RIGHT_FINGER](40x40, X=194, Y=38)

ROW 3 - CHEST LEVEL (Y=77):
├─ InvSlot6  [SHOULDERS]  (40x40, X=-1, Y=77)
├─ InvSlot17 [CHEST]      (40x40, X=38, Y=77)
├─ InvSlot8  [BACK]       (40x40, X=77, Y=77)
├─ InvSlot20 [WAIST]      (40x40, X=116, Y=77)
├─ InvSlot18 [LEGS]       (40x40, X=155, Y=77)
└─ InvSlot19 [FEET]       (40x40, X=194, Y=77)

ROW 4 - WEAPONS/AMMO (Y=116):
├─ InvSlot13 [PRIMARY]    (40x40, X=77, Y=116)
├─ InvSlot14 [SECONDARY]  (40x40, X=116, Y=116)
├─ InvSlot11 [RANGE]      (40x40, X=155, Y=116)
└─ InvSlot21 [AMMO]       (40x40, X=194, Y=116)
```

## Stat Display

Stats are neatly organized in the central column with clear labels and custom colors.

**Complete Stat Coordinate Listing**
```
├─ IW_Name         (Label, X=245, Y=4)
├─ IW_Level        (Label, X=245, Y=18)
├─ IW_Class        (Label, X=265, Y=18)
├─ IW_Deity        (Label, X=245, Y=32)
├─ IW_HP           (Label, X=245, Y=50)
├─ IW_CurrentHP    (Label, X=284, Y=50)
├─ IW_AC           (Label, X=245, Y=78)
├─ IW_ACNumber     (Label, X=284, Y=78)
├─ IW_ATK          (Label, X=245, Y=92)
├─ IW_ATKNumber    (Label, X=284, Y=92)
├─ IW_EXP_Percentage (Label, X=284, Y=114)
├─ IW_STR          (Label, X=245, Y=144)
├─ IW_STRNumber    (Label, X=315, Y=144)
├─ IW_STA          (Label, X=245, Y=158)
├─ IW_STANumber    (Label, X=315, Y=158)
├─ IW_AGI          (Label, X=245, Y=172)
├─ IW_AGINumber    (Label, X=315, Y=172)
├─ IW_DEX          (Label, X=245, Y=186)
├─ IW_DEXNumber    (Label, X=315, Y=186)
├─ IW_WIS          (Label, X=245, Y=200)
├─ IW_WISNumber    (Label, X=315, Y=200)
├─ IW_INT          (Label, X=245, Y=214)
├─ IW_INTNumber    (Label, X=315, Y=214)
├─ IW_CHA          (Label, X=245, Y=228)
├─ IW_CHANumber    (Label, X=315, Y=228)
├─ IW_MR           (Label, X=245, Y=252)
├─ IW_MRNumber     (Label, X=315, Y=252)
├─ IW_FR           (Label, X=245, Y=266)
├─ IW_FRNumber     (Label, X=315, Y=266)
├─ IW_CR           (Label, X=245, Y=280)
├─ IW_CRNumber     (Label, X=315, Y=280)
├─ IW_DR           (Label, X=245, Y=294)
├─ IW_DRNumber     (Label, X=315, Y=294)
├─ IW_PR           (Label, X=245, Y=308)
├─ IW_PRNumber     (Label, X=315, Y=308)
```

## Gauges & Progress Bars

Includes standard XP and AA gauges, but with the addition of explicit percentage labels.

**Gauge Specifications**
```
├─ IW_ExpGauge    (X=244, Y=129, 116x8, Color: 220,150,0, EQType: 4)
├─ IW_AltAdvGauge (X=244, Y=140, 116x8, Color: 0,180,255, EQType: 25)
```

## Unique Features

- **Explicit Percentages**: `IW_EXP_Percentage` (EQType 26) and `IW_AA_Percentage` (EQType 27) provide a numerical display for progress, a significant QoL improvement.
- **Three-Column Design**: The separation of concerns into three columns makes the window exceptionally clean and easy to navigate.
- **Custom Colors**: Use of distinct colors for stat labels (`50,160,250`) and HP (`200,120,145`) adds a level of polish and visual distinction.
- **Hidden Charm Slot**: `InvSlot0` (Charm) is sized to 1x1, effectively hiding it. This is a common practice in modern UIs where the charm slot is considered less critical to display permanently.

## Recommendations for Thorne_Drak

1. **Adopt the Three-Column Layout**: This is a superior design for organizing a large amount of information. A Thorne variant based on this structure would be highly effective and user-friendly.
2. **Implement Explicit Percentage Labels**: The `IW_EXP_Percentage` and `IW_AA_Percentage` labels are a must-have feature. This provides clear, at-a-glance progress information that users love. This should be a high-priority addition.
3. **Use Color to Differentiate Stat Blocks**: The QQQuarm approach of using color to group related stats (e.g., primary attributes vs. resistances) is an excellent visual design pattern to adopt.
4. **Provide an Option to Hide Charm**: The 1x1 charm slot is a good solution for decluttering the UI. This could be a user-configurable option in Thorne settings.

---
*Analysis generated by GitHub Copilot. February 4, 2026.*