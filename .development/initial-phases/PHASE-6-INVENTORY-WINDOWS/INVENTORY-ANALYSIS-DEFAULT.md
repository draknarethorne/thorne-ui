# Inventory Analysis: Default

## 1. Executive Summary

The `default/EQUI_Inventory.xml` file represents the foundational inventory screen for EverQuest. Its design philosophy is rooted in direct, unambiguous functionality, serving as the baseline upon which nearly all custom UIs are built. The layout is static and utilitarian, with a clear, if inefficient, spatial organization that prioritizes function over form. Every element has a hardcoded position, creating a rigid but predictable user experience that was standard for MMOs of its era.

Architecturally, the window is defined as a single, flat container. It does not employ subwindows or complex container elements, opting instead for a direct placement of all components—labels, gauges, and inventory slots—onto the main screen. This makes the file relatively easy to understand but difficult to modify or rearrange without manually recalculating the coordinates for every affected element. The equipment slots are arranged in a classic "paper doll" or anatomical layout, intuitively mapping gear to the character's body.

Compared to modern UI variants, the default inventory is notable for its simplicity and lack of advanced features. There are no integrated bags, no dynamic stat displays, and no user-configurable elements. Its primary contribution is establishing the core set of `EQType` bindings and element naming conventions (`InvSlot1`, `IW_STR`, etc.) that have become the standard. It is the essential starting point, and its inefficiencies—such as the large amounts of empty space and scattered information—provide the primary motivation for the creation of custom UIs.

## 2. Quick Reference
- **Directory**: `default/`
- **File**: `EQUI_Inventory.xml`
- **Window Size**: 420x350 px
- **Template**: `WDT_Rounded`
- **Total Elements**: 148
- **Subwindows**: No
- **Unique Features**:
    - Establishes the baseline for all inventory variants.
    - Purely functional, non-configurable layout.
    - Classic anatomical "paper doll" equipment view.

## 3. Layout Architecture

The layout is a single, fixed-size window with three conceptual vertical zones. The left zone is dedicated to character information and stats. The center and right-center are dedicated to the anatomical equipment display. The far right contains the main bag slots. The bottom area houses currency information.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ InventoryWindow (420x350)                                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┬──────────────────────────────────┬────────────────────┐ │
│ │ LEFT COLUMN      │ CENTER EQUIPMENT                 │ RIGHT BAGS         │ │
│ │ (X=0, Y=0)       │ (X=120, Y=0)                     │ (X=330, Y=160)     │ │
│ │ 120x320          │ 200x320                          │ 80x160             │ │
│ │                  │                                  │                    │ │
│ │ [Name]           │   [Ear] [Neck] [Head] [Face] [Ear] │ [Bag1] [Bag5]      │ │
│ │ [Level/Class]    │   [Chest]                  [Back]  │ [Bag2] [Bag6]      │ │
│ │ [Deity]          │   [Arms]               [Shoulders] │ [Bag3] [Bag7]      │ │
│ │                  │   [Wrist]                  [Wrist] │ [Bag4] [Bag8]      │ │
│ │ [HP/AC/ATK]      │   [Waist]                  [Hands] │                    │ │
│ │ [XP Gauge]       │   [Ring]                    [Ring] │                    │ │
│ │                  │         [Legs] [Feet]            │                    │ │
│ │ [Stats Block]    │   [Primary] [Secondary] [Range] [Ammo] │                │ │
│ │                  │                                  │                    │ │
│ └──────────────────┴──────────────────────────────────┴────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Bottom Row: Currency] Y=326                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 4. Equipment Display

The 21 equipment slots are arranged anatomically. The coordinates are relative to the `InventoryWindow`.

**ROW 1 - HEAD LEVEL (Y=0):**
├─ InvSlot1  [LEFT_EAR]   (40x40, X=120, Y=0, EQType: 1)
├─ InvSlot5  [NECK]       (40x40, X=160, Y=0, EQType: 5)
├─ InvSlot2  [HEAD]       (40x40, X=200, Y=0, EQType: 2)
├─ InvSlot3  [FACE]       (40x40, X=240, Y=0, EQType: 3)
└─ InvSlot4  [RIGHT_EAR]  (40x40, X=280, Y=0, EQType: 4)

**ROW 2 - CHEST/BACK (Y=40):**
├─ InvSlot17 [CHEST]      (40x40, X=120, Y=40, EQType: 17)
└─ InvSlot8  [BACK]       (40x40, X=280, Y=40, EQType: 8)

**ROW 3 - ARMS/SHOULDERS (Y=80):**
├─ InvSlot7  [ARMS]       (40x40, X=120, Y=80, EQType: 7)
└─ InvSlot6  [SHOULDERS]  (40x40, X=280, Y=80, EQType: 6)

**ROW 4 - WRISTS (Y=120):**
├─ InvSlot9  [LEFT_WRIST] (40x40, X=120, Y=120, EQType: 9)
└─ InvSlot10 [RIGHT_WRIST](40x40, X=280, Y=120, EQType: 10)

**ROW 5 - WAIST/HANDS (Y=160):**
├─ InvSlot20 [WAIST]      (40x40, X=120, Y=160, EQType: 20)
└─ InvSlot12 [HANDS]      (40x40, X=280, Y=160, EQType: 12)

**ROW 6 - FINGERS (Y=200):**
├─ InvSlot15 [LEFT_FINGER](40x40, X=120, Y=200, EQType: 15)
└─ InvSlot16 [RIGHT_FINGER](40x40, X=280, Y=200, EQType: 16)

**ROW 7 - LEGS/FEET (Y=240):**
├─ InvSlot18 [LEGS]       (40x40, X=180, Y=240, EQType: 18)
└─ InvSlot19 [FEET]       (40x40, X=220, Y=240, EQType: 19)

**ROW 8 - WEAPONS/AMMO (Y=280):**
├─ InvSlot13 [PRIMARY]    (40x40, X=140, Y=280, EQType: 13)
├─ InvSlot14 [SECONDARY]  (40x40, X=180, Y=280, EQType: 14)
├─ InvSlot11 [RANGE]      (40x40, X=220, Y=280, EQType: 11)
└─ InvSlot21 [AMMO]       (40x40, X=260, Y=280, EQType: 21)

## 5. Stats & Character Info

All stat and character labels are positioned in the left column of the window.

**Character Info Section:**
├─ IW_Name       (Label, X=8, Y=4, EQType: 1)
├─ IW_Level      (Label, X=8, Y=18, EQType: 2)
├─ IW_Class      (Label, X=28, Y=18, EQType: 3)
└─ IW_Deity      (Label, X=8, Y=32, EQType: 4)

**Combat Stats Section:**
├─ IW_HP         (Label, X=14, Y=50)
├─ IW_CurrentHP  (Label, X=40, Y=50, EQType: 17)
├─ IW_MaxHP      (Label, X=83, Y=50, EQType: 18)
├─ IW_AC         (Label, X=14, Y=64)
├─ IW_ACNumber   (Label, X=40, Y=64, EQType: 22)
├─ IW_ATK        (Label, X=14, Y=78)
└─ IW_ATKNumber  (Label, X=40, Y=78, EQType: 23)

**Core Attributes Section (STR, STA, AGI, DEX):**
├─ IW_STR        (Label, X=30, Y=130)
├─ IW_STRNumber  (Label, X=60, Y=130, EQType: 5)
├─ IW_STA        (Label, X=30, Y=144)
├─ IW_STANumber  (Label, X=60, Y=144, EQType: 6)
├─ IW_AGI        (Label, X=30, Y=158)
├─ IW_AGINumber  (Label, X=60, Y=158, EQType: 8)
├─ IW_DEX        (Label, X=30, Y=172)
└─ IW_DEXNumber  (Label, X=60, Y=172, EQType: 7)

**Core Attributes Section (WIS, INT, CHA):**
├─ IW_WIS        (Label, X=30, Y=186)
├─ IW_WISNumber  (Label, X=60, Y=186, EQType: 9)
├─ IW_INT        (Label, X=30, Y=200)
├─ IW_INTNumber  (Label, X=60, Y=200, EQType: 10)
├─ IW_CHA        (Label, X=30, Y=214)
└─ IW_CHANumber  (Label, X=60, Y=214, EQType: 11)

**Resistances Section:**
├─ IW_MR         (Label, X=30, Y=232)
├─ IW_MRNumber   (Label, X=60, Y=232, EQType: 14)
├─ IW_FR         (Label, X=30, Y=246)
├─ IW_FRNumber   (Label, X=60, Y=246, EQType: 15)
├─ IW_CR         (Label, X=30, Y=260)
├─ IW_CRNumber   (Label, X=60, Y=260, EQType: 13)
├─ IW_DR         (Label, X=30, Y=274)
├─ IW_DRNumber   (Label, X=60, Y=274, EQType: 16)
├─ IW_PR         (Label, X=30, Y=288)
└─ IW_PRNumber   (Label, X=60, Y=288, EQType: 12)

## 6. Icons & Graphics

The default UI uses `A_` prefixed assets, which are standard textures from the game's core UI files.
- **Equipment Slots**: Each slot has a unique background texture (e.g., `A_InvHead`, `A_InvChest`, `A_InvRing`).
- **Bag Slots**: Use a generic `A_RecessedBox` texture.
- **Gauges**: Use a standard set of gauge textures: `A_GaugeBackground`, `A_GaugeFill`, `A_GaugeLines`, `A_GaugeLinesFill`, `A_GaugeEndCapLeft`, `A_GaugeEndCapRight`.
- **Buttons**: Standard button textures like `A_BtnNormal`, `A_BtnPressed`, etc.
- **Race Graphic**: A `Picture` element (`IW_RaceImage`) is defined at (X=160, Y=40) with a size of 128x192, but it is not visible by default as it is layered behind other elements. It is intended to display the character's portrait.

There are no custom icon implementations; all graphics are loaded from the game's default texture sets.

## 7. Gauges & Progress Bars

Only one gauge is present in the default inventory window.
├─ IW_ExpGauge    (Gauge, X=2, Y=112, 116x8, Horizontal, Color: 220,150,0, EQType: 4)

## 8. Bag Slots

There are 8 primary bag slots arranged in a 2x4 grid on the right side of the window.
- **Column 1 (X=330):**
  ├─ InvSlot22 [Bag 1] (40x40, X=330, Y=160, EQType: 22)
  ├─ InvSlot23 [Bag 2] (40x40, X=330, Y=200, EQType: 23)
  ├─ InvSlot24 [Bag 3] (40x40, X=330, Y=240, EQType: 24)
  └─ InvSlot25 [Bag 4] (40x40, X=330, Y=280, EQType: 25)
- **Column 2 (X=370):**
  ├─ InvSlot26 [Bag 5] (40x40, X=370, Y=160, EQType: 26)
  ├─ InvSlot27 [Bag 6] (40x40, X=370, Y=200, EQType: 27)
  ├─ InvSlot28 [Bag 7] (40x40, X=370, Y=240, EQType: 28)
  └─ InvSlot29 [Bag 8] (40x40, X=370, Y=280, EQType: 29)

## 9. Currency & Economy

Currency is displayed in a series of labels at the bottom of the window.
- **Platinum:**
  ├─ IW_PlatinumLabel (Label, X=10, Y=326)
  └─ IW_PlatinumAmount (Label, X=30, Y=326, EQType: 30)
- **Gold:**
  ├─ IW_GoldLabel (Label, X=80, Y=326)
  └─ IW_GoldAmount (Label, X=100, Y=326, EQType: 31)
- **Silver:**
  ├─ IW_SilverLabel (Label, X=150, Y=326)
  └─ IW_SilverAmount (Label, X=170, Y=326, EQType: 32)
- **Copper:**
  ├─ IW_CopperLabel (Label, X=220, Y=326)
  └─ IW_CopperAmount (Label, X=240, Y=326, EQType: 33)

## 10. Unique Features

The most "unique" feature of the default inventory is its role as the universal baseline. It establishes the fundamental layout and `EQType` bindings that all other mods react to, modify, or replace entirely.
- **Anatomical Purity**: The equipment layout is a clear, if spatially inefficient, anatomical map.
- **Simplicity**: It contains no complex logic, scripts, or nested windows. What you see is what you get.
- **Inefficiency as a Feature**: The significant amount of unused space and the scattered nature of the stats serve as the primary motivation for the UI modding community. It presents a clear problem to be solved.

## 11. Implementation Notes

- **EQType Usage**: `EQType`s are used extensively to bind UI labels and slots to game data. The numbering scheme established here is the de facto standard (e.g., `EQType: 1` for Name, `EQType: 5` for STR, `EQType: 22` for the first bag slot).
- **Texture Loading**: All textures are loaded via `<Background>` tags for slots and `<GaugeDrawTemplate>` for gauges, referencing assets from the default UI texture files (e.g., `A_InvHead`, `A_GaugeFill`).
- **Positioning**: All elements use `<RelativePosition>true</RelativePosition>` but are effectively absolute, as their coordinates are relative to the top-left corner of the parent `InventoryWindow`. There is no use of dynamic or anchored positioning.
- **Naming Conventions**: A consistent naming convention is used: `IW_` prefix for most inventory window elements (`IW_Name`, `IW_STR`), and `InvSlot` for all item slots. This convention is widely adopted.
- **Window Definition**: The main window is defined with `<Screen item = "InventoryWindow">`, and its properties (size, template) are set within a `<ScreenDef>` tag. All other elements are defined as direct children.
