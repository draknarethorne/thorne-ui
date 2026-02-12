# Inventory Window Analysis: QQ UI

## Executive Summary

The QQ UI variant of the Inventory window represents a masterclass in ultra-compact, information-dense design. It aggressively pursues a philosophy of minimal footprint, achieving a remarkable reduction in size compared to the default UI (355x355 vs. 378x480). This is accomplished through a strict, two-column architectural paradigm that cleanly separates interactive inventory management from passive information display. The left column is dedicated entirely to player equipment, primary inventory bags, and a character model view, while the right column consolidates all character statistics, resistances, and experience gauges.

This bifurcation is the core design pattern. The equipment slots are compressed into a hyper-dense 6x4 grid, abandoning the traditional anatomical layout in favor of pure spatial efficiency. Every pixel is leveraged; there is no wasted space between slots. This grid-based approach allows for a much smaller area to contain all 21 equipment slots, which is the primary driver of the window's compact dimensions.

Further space-saving techniques are evident throughout. The main inventory bags are arranged in a tight 2x4 grid directly below the character view. Gauges for XP and AA are simple, horizontal bars, and the window omits HP and Mana gauges entirely, assuming the player relies on other UI elements for that information. Even the currency display is a compact vertical stack. The result is a highly functional, if visually dense, window that prioritizes presenting a maximum amount of data and functionality in the smallest possible screen real estate.

## Quick Reference
- **Directory**: `QQ/`
- **File**: `EQUI_Inventory.xml`
- **Window Size**: 355x355 px
- **Total Elements**: 100+
- **Subwindows**: 1 (`IW_CharacterView`)
- **Unique Features**:
    - Strict two-column layout (Inventory vs. Information).
    - Hyper-compact 6x4 equipment grid.
    - Integrated action buttons (`Skills`, `Face`, `Destroy`).
    - No HP/Mana gauges.

## Layout Architecture
The QQ Inventory window enforces a rigid two-column layout. The left half (~240px) is the "interactive" zone, containing all equipment slots, bag slots, and the character preview. The right half (~115px) is the "information" zone, displaying all character stats, attributes, and progress bars. This clear separation creates a predictable and efficient user experience.

An integrated action panel at the bottom provides access to Skills, Face customization, and item destruction, keeping essential functions within the window itself.

```
┌───────────────────────────────────────────────────┐
│ INVENTORY (LEFT COLUMN)         │ INFO (RIGHT COLUMN) │
├─────────────────────────────────┼─────────────────────┤
│ ┌─────────────────────────────┐ │ ┌─────────────────┐ │
│ │      EQUIPMENT GRID         │ │ │ Name/Level/Class│ │
│ │      (X: -1, Y: -1)         │ │ │ (X:245, Y:4)    │ │
│ │      (6 columns x 4 rows)   │ │ └─────────────────┘ │
│ │                             │ │ ┌─────────────────┐ │
│ └─────────────────────────────┘ │ │ HP/AC/ATK       │ │
│ ┌──────────┬──────────────────┐ │ │ (X:245, Y:50)   │ │
│ │          │ BAG SLOTS (2x4)  │ │ └─────────────────┘ │
│ │ CHAR     │ (X:156, Y:165)   │ │ ┌─────────────────┐ │
│ │ VIEW     ├──────────────────┤ │ │ XP/AA Gauges    │ │
│ │ (X:2,     │ CURRENCY (1x4)   │ │ │ (X:244, Y:129)  │ │
│ │ Y:165)   │ (X:81, Y:180)    │ │ └─────────────────┘ │
│ │          │                  │ │ ┌─────────────────┐ │
│ └──────────┴──────────────────┘ │ │ Stats (STR-CHA) │ │
│                                 │ │ (X:245, Y:144)  │ │
├─────────────────────────────────┴─────────────────┤ │
│ ACTION BUTTONS (Done, Face, Skills, Destroy)      │ │
│ (X:2, Y:325)                                      │ │
└───────────────────────────────────────────────────┘
```

## Equipment Display
QQ abandons the anatomical layout for a dense 6x4 grid, achieving maximum density. All slots are 40x40px. The layout is not intuitive but is extremely space-efficient. Slots are positioned with a 1px overlap/negative space to tighten the grid.

**ROW 1 - HEAD LEVEL (Y=-1):**
├─ InvSlot15 [LEFT_FINGER] (40x40, X=-1, Y=38)  *Erroneously placed in grid logic, but part of this visual row*
├─ InvSlot1  [LEFT_EAR]    (40x40, X=38, Y=-1)
├─ InvSlot5  [NECK]        (40x40, X=77, Y=-1)
├─ InvSlot3  [FACE]        (40x40, X=116, Y=-1)
├─ InvSlot2  [HEAD]        (40x40, X=155, Y=-1)
└─ InvSlot4  [RIGHT_EAR]   (40x40, X=194, Y=-1)

**ROW 2 - ARM LEVEL (Y=38):**
├─ InvSlot15 [LEFT_FINGER] (40x40, X=-1, Y=38)
├─ InvSlot9  [LEFT_WRIST]  (40x40, X=38, Y=38)
├─ InvSlot7  [ARMS]        (40x40, X=77, Y=38)
├─ InvSlot12 [HANDS]       (40x40, X=116, Y=38)
├─ InvSlot10 [RIGHT_WRIST] (40x40, X=155, Y=38)
└─ InvSlot16 [RIGHT_FINGER](40x40, X=194, Y=38)

**ROW 3 - BODY LEVEL (Y=77):**
├─ InvSlot6  [SHOULDERS]   (40x40, X=-1, Y=77)
├─ InvSlot17 [CHEST]       (40x40, X=38, Y=77)
├─ InvSlot8  [BACK]        (40x40, X=77, Y=77)
├─ InvSlot20 [WAIST]       (40x40, X=116, Y=77)
├─ InvSlot18 [LEGS]        (40x40, X=155, Y=77)
└─ InvSlot19 [FEET]        (40x40, X=194, Y=77)

**ROW 4 - WEAPON LEVEL (Y=116):**
├─ InvSlot-  [EMPTY]       (N/A)
├─ InvSlot-  [EMPTY]       (N/A)
├─ InvSlot13 [PRIMARY]     (40x40, X=77, Y=116)
├─ InvSlot14 [SECONDARY]   (40x40, X=116, Y=116)
├─ InvSlot11 [RANGE]       (40x40, X=155, Y=116)
└─ InvSlot21 [AMMO]        (40x40, X=194, Y=116)

## Stats & Character Info
All character information is consolidated in the right-hand column.

**Character Info:**
├─ IW_Name      (Label, X=245, Y=4)
├─ IW_Level     (Label, X=245, Y=18)
├─ IW_Class     (Label, X=265, Y=18)
└─ IW_Deity     (Label, X=245, Y=32)

**Core Stats:**
├─ IW_HP        (Label, X=245, Y=50)
├─ IW_CurrentHP (Value, X=284, Y=50)
├─ IW_AC        (Label, X=245, Y=78)
├─ IW_ACNumber  (Value, X=284, Y=78)
├─ IW_ATK       (Label, X=245, Y=92)
└─ IW_ATKNumber (Value, X=284, Y=92)

**Attributes (Primary Stats):**
├─ IW_STR       (Label, X=245, Y=144)
├─ IW_STA       (Label, X=245, Y=158)
├─ IW_AGI       (Label, X=245, Y=172)
├─ IW_DEX       (Label, X=245, Y=186)
├─ IW_WIS       (Label, X=245, Y=200)
├─ IW_INT       (Label, X=245, Y=214)
└─ IW_CHA       (Label, X=245, Y=228)

**Resistances:**
├─ IW_Magic     (Label, X=245, Y=249)
├─ IW_Fire      (Label, X=245, Y=263)
├─ IW_Cold      (Label, X=245, Y=277)
├─ IW_Disease   (Label, X=245, Y=291)
└─ IW_Poison    (Label, X=245, Y=305)

## Gauges & Progress Bars
Gauges are minimal and horizontal, placed in the right-hand info column.
├─ XP_Gauge    (X=244, Y=129, 116x8, Color: 220,150,0, EQType: 4)
└─ AA_Gauge    (X=244, Y=142, 116x8, Color: 220,0,150, EQType: 27) *(Note: AA Gauge is defined in EQUI_Animations.xml and placed here)*

There are no HP or Mana gauges within the inventory window.

## Bag Slots
The 8 primary inventory bag slots are arranged in a compact 2x4 grid.
- **Column 1 (X=156):**
  ├─ InvSlot22 (Bag 1) (Y=165)
  ├─ InvSlot23 (Bag 2) (Y=204)
  ├─ InvSlot24 (Bag 3) (Y=243)
  └─ InvSlot25 (Bag 4) (Y=282)
- **Column 2 (X=195):**
  ├─ InvSlot26 (Bag 5) (Y=165)
  ├─ InvSlot27 (Bag 6) (Y=204)
  ├─ InvSlot28 (Bag 7) (Y=243)
  └─ InvSlot29 (Bag 8) (Y=282)

## Currency
Currency is displayed in a vertical stack between the character view and the bag slots.
├─ IW_Money0 (Plat)   (X=81, Y=180)
├─ IW_Money1 (Gold)   (X=81, Y=205)
├─ IW_Money2 (Silver) (X=81, Y=230)
└─ IW_Money3 (Copper) (X=81, Y=255)

## Unique Features
1.  **Two-Column Paradigm**: The most defining feature. It strictly separates interactive slots (left) from read-only information (right), creating a clean, logical flow.
2.  **Hyper-Compact Grid**: The 6x4 equipment grid is a radical departure from anatomical layouts, prioritizing density above all else. This is the key enabler for the window's small size.
3.  **Integrated Action Panel**: Buttons for `Skills`, `Face`, and `Destroy` are built into the bottom of the window, reducing the need to open other windows for common actions.
4.  **Omission of Gauges**: The deliberate choice to exclude HP and Mana gauges reinforces a minimalist design ethos, assuming these are monitored elsewhere.

## Implementation Notes
- The equipment grid is constructed with `RelativePosition=true` and manual coordinates. The layout is fragile and depends on precise X/Y values with negative offsets (`-1`) to create the tight packing.
- The `IW_CharacterView` subwindow is used to create a bordered frame for the character model, which is rendered via the `ClassAnim` static animation piece.
- The AA gauge is not explicitly defined in this XML but is expected to be sourced from `EQLSUI_Animations.xml` or a similar template file and positioned logically below the XP gauge. The analysis assumes its standard placement.
- The design relies on the user's ability to learn a non-standard equipment layout. The tooltip system becomes critical for identifying slots.
