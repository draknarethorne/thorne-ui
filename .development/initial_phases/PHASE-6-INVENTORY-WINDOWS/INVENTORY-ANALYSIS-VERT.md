# Inventory Analysis: Vert

## Executive Summary
The Vert inventory window represents a masterclass in vertical design and horizontal compactness. Its design philosophy is centered on creating the narrowest possible footprint (285px) by organizing all functional components into two strict vertical columns. The left column contains all interactive elements—equipment, bag slots, and currency—stacked vertically. The right column is a dedicated, read-only display for all character statistics. This strict functional separation creates a clean, highly organized, and space-efficient window that prioritizes vertical screen real estate above all else.

## Quick Reference
- **Directory**: `vert/`
- **Window Size**: 285x330 px
- **Template**: `IW_DefaultTemplate`
- **Total Elements**: ~100
- **Subwindows**: No (Stats are individual labels, not in a subwindow)
- **Unique Features**:
  - Extreme 285px width (narrowest variant).
  - Strict two-column layout: interactive left, info-display right.
  - Vertical stacking of equipment slots in a 3-column grid.
  - Functional separation between item management and stat review.

## Layout Architecture
The window is divided into two distinct vertical zones. The LEFT ZONE handles all inventory and item management, while the RIGHT ZONE is exclusively for displaying character stats. Gauges for XP and AA are positioned horizontally at the very bottom, spanning both zones.

```
┌──────────────────────────────────┐
│ LEFT ZONE (Items)  │ RIGHT ZONE  │
│ (X:0, Y:0)         │ (Stats)     │
│ W:206, H:280       │ (X:206, Y:0)│
│                    │ W:79, H:280 │
│ ┌──────────┐       ├─────────────┤
│ │ Bags     │       │ Name/Class  │
│ │ (2x4 Grid) │       │ HP/AC/ATK   │
│ └──────────┘       │ STR/STA/AGI │
│ ┌──────────┐       │ DEX/WIS/INT │
│ │ Equip    │       │ CHA         │
│ │ (3-Col   │       │ Resists     │
│ │  Grid)   │       │ ...etc      │
│ └──────────┘       │             │
│ ┌──────────┐       │             │
│ │ Currency │       │             │
│ └──────────┘       │             │
├────────────────────┴─────────────┤
│ XP/AA Gauges                     │
│ (X:4, Y:312)                     │
└──────────────────────────────────┘
```

## Equipment Display
Equipment is organized into a compact, 3-column vertical grid, abandoning the traditional anatomical layout to achieve maximum density.

**Complete Equipment Coordinate Map**
```
ROW 1 - HEAD LEVEL (Y=0):
├─ InvSlot1  [LEFT_EAR]   (Size: 40x40, X=84, Y=0)
├─ InvSlot2  [HEAD]       (Size: 40x40, X=124, Y=0)
└─ InvSlot4  [RIGHT_EAR]  (Size: 40x40, X=164, Y=0)

ROW 2 - NECK/SHOULDERS (Y=40):
├─ InvSlot6  [SHOULDERS]  (Size: 40x40, X=84, Y=40)
├─ InvSlot3  [FACE]       (Size: 40x40, X=124, Y=40)
└─ InvSlot5  [NECK]       (Size: 40x40, X=164, Y=40)

ROW 3 - CHEST/BACK (Y=80):
├─ InvSlot8  [BACK]       (Size: 40x40, X=84, Y=80)
├─ InvSlot17 [CHEST]      (Size: 40x40, X=124, Y=80)
└─ InvSlot20 [WAIST]      (Size: 40x40, X=164, Y=80)

ROW 4 - ARMS/WRISTS (Y=120):
├─ InvSlot9  [LEFT_WRIST] (Size: 40x40, X=84, Y=120)
├─ InvSlot7  [ARMS]       (Size: 40x40, X=124, Y=120)
└─ InvSlot10 [RIGHT_WRIST](Size: 40x40, X=164, Y=120)

ROW 5 - HANDS/FINGERS (Y=160):
├─ InvSlot15 [LEFT_FINGER](Size: 40x40, X=84, Y=160)
├─ InvSlot12 [HANDS]      (Size: 40x40, X=124, Y=160)
└─ InvSlot16 [RIGHT_FINGER](Size: 40x40, X=164, Y=160)

ROW 6 - LEGS/FEET (Y=200):
├─ InvSlot18 [LEGS]       (Size: 40x40, X=84, Y=200)
├─ InvSlot19 [FEET]       (Size: 40x40, X=124, Y=200)
└─ InvSlot21 [AMMO]       (Size: 40x40, X=164, Y=200)

ROW 7 - WEAPONS (Y=240):
├─ InvSlot13 [PRIMARY]    (Size: 40x40, X=84, Y=240)
├─ InvSlot14 [SECONDARY]  (Size: 40x40, X=124, Y=240)
└─ InvSlot11 [RANGE]      (Size: 40x40, X=164, Y=240)
```

## Stat Display
All character stats are neatly positioned in the narrow right-hand column, providing a quick, comprehensive overview.

**Complete Stat Coordinate Listing**
```
├─ IW_Name         (Label, X=208, Y=2)
├─ IW_Level/Class  (Label, X=208, Y=18)
├─ IW_Deity        (Label, X=208, Y=30)
├─ IW_HP           (Label, X=208, Y=44)
├─ IW_AC           (Label, X=208, Y=56)
├─ IW_ATK          (Label, X=208, Y=68)
├─ IW_STR          (Label, X=208, Y=84)
├─ IW_STA          (Label, X=208, Y=96)
├─ IW_AGI          (Label, X=208, Y=108)
├─ IW_DEX          (Label, X=208, Y=120)
├─ IW_WIS          (Label, X=208, Y=132)
├─ IW_INT          (Label, X=208, Y=144)
├─ IW_CHA          (Label, X=208, Y=156)
├─ IW_MR           (Label, X=208, Y=172)
├─ IW_FR           (Label, X=208, Y=184)
├─ IW_CR           (Label, X=208, Y=196)
├─ IW_DR           (Label, X=208, Y=208)
└─ IW_PR           (Label, X=208, Y=220)
```

## Gauges & Progress Bars
Gauges are placed horizontally at the bottom of the window.
```
├─ IW_ExpGauge    (X=4, Y=312, WxH: 136x12, Color: 220,150,0, EQType: experience)
└─ IW_AltExpGauge (X=145, Y=312, WxH: 136x12, Color: 0,180,150, EQType: alt_experience)
```

## Bag Slots
The 8 primary bag slots are arranged in a 2x4 grid in the top-left corner.
```
COLUMN 1 (X=2):
├─ InvSlot22 (Y=40)
├─ InvSlot23 (Y=80)
├─ InvSlot24 (Y=120)
└─ InvSlot25 (Y=160)

COLUMN 2 (X=42):
├─ InvSlot26 (Y=40)
├─ InvSlot27 (Y=80)
├─ InvSlot28 (Y=120)
└─ InvSlot29 (Y=160)
```

## Currency
Currency is displayed in a vertical stack in the bottom-left corner.
```
├─ IW_PlatinumCoin (X=4, Y=284)
├─ IW_GoldCoin     (X=4, Y=292)
├─ IW_SilverCoin   (X=4, Y=300)
└─ IW_CopperCoin   (X=4, Y=308)
```

## Unique Features
- **Vertical-First Columnar Design**: The entire layout is built on a principle of vertical organization, allowing for its extreme narrowness.
- **Strict Functional Separation**: The hard division between the left (interactive items) and right (display-only stats) columns is a key usability feature, preventing mis-clicks and creating a clean visual hierarchy.
- **285px Width**: This is arguably the most important feature, making it the most compact and screen-space-conscious inventory design available.

## Implementation Notes
- The stat display is achieved by placing individual `Label` elements directly onto the main window background. The area typically reserved for the `IW_CharacterView` piece (the 3D paperdoll model) is repurposed as the container for this column of stats. This avoids the need for a separate subwindow, simplifying the XML structure.
- The equipment layout's density is achieved by abandoning the standard anatomical mapping in favor of a pure grid system, demonstrating a willingness to prioritize space efficiency over traditional presentation.
- The window's background and borders are defined in `EQUI_Templates.xml` under `IW_DefaultTemplate`, which provides the standard frame for this highly customized interior layout.
