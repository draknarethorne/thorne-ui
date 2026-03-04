# Inventory Analysis: duxaUI

## Quick Reference
- **Directory**: `duxaUI/`
- **Window Size**: 380x350 px
- **Template**: `SIDL_IW_InventoryWnd`
- **Total Elements**: ~150
- **Subwindows**: No
- **Unique Features**:
    - Compact three-column layout.
    - Anatomical equipment grid.
    - Stat icons next to core attributes.
    - Horizontal HP/Mana/Stamina/XP/AA gauges.
    - Integrated 2x4 bag slots.

## Layout Architecture
The duxaUI inventory is a compact, all-in-one window divided into three main vertical columns. It does not use subwindows, instead defining all elements within the main `InventoryWindow` piece list.

- **Left Column**: Contains the character render view, Done button, and main action buttons (Face, Skills, Destroy).
- **Center Column**: Houses the anatomical equipment grid, currency, and the 2x4 bag slots at the bottom.
- **Right Column**: Displays all character stats, gauges, and resists. This column is notable for its use of small icons next to the primary stats (STR, STA, etc.).

The overall design prioritizes information density, placing almost all character-related information in a single, non-overlapping view.

**Detailed ASCII Art Layout**
```
┌───────────────────────────────────────────────────────────────────────────┐
│ InventoryWindow (380x350)                                                 │
├────────────────────────────────┬───────────────────────┬──────────────────┤
│ LEFT COLUMN (X:5, W:82)        │ CENTER COLUMN (X:89)  │ RIGHT COLUMN     │
│                                │                       │ (X:260, W:115)   │
│ ┌────────────────────────────┐ │ ┌─ Head Row (Y:4) ───┐ │ ┌─ Name/Class ─┐ │
│ │                            │ │ │ L.Ear Neck Face... │ │ │ Name         │ │
│ │   Character View           │ │ └───────────────────┘ │ │ Lvl Class    │ │
│ │   (5,133) 82x162           │ │ ┌─ Arm Row (Y:47) ───┐ │ │ Deity        │ │
│ │                            │ │ │ L.Fng L.Wri Arm... │ │ └──────────────┘ │
│ │                            │ │ └───────────────────┘ │ ┌─ Gauges (Y:50)┐ │
│ │                            │ │ ┌─ Body Row (Y:90) ──┐ │ │ HP Gauge     │ │
│ └────────────────────────────┘ │ │ Shld Chst Back...  │ │ │ Mana Gauge   │ │
│ ┌──────────┐ ┌───────────────┐ │ └───────────────────┘ │ │ Stamina Gauge│ │
│ │ Done     │ │ Face          │ │ ┌─ Weapon Row(Y:133)─┐ │ └──────────────┘ │
│ │ (5,298)  │ │ Skills        │ │ │ Pri Sec Rng Ammo   │ │ ┌─ Stats (Y:100)│ │
│ │ 82x46    │ │ Destroy       │ │ └───────────────────┘ │ │ STR [icon]   │ │
│ └──────────┘ │ (89,272)      │ │ ┌─ Currency (Y:176) ─┐ │ │ STA [icon]   │ │
│              └───────────────┘ │ │ Plat Gold Silv Cop │ │ │ ...          │ │
│                                │ └───────────────────┘ │ └──────────────┘ │
│                                │ ┌─ Bags (Y:176)──────┐ │ ┌─ Resists(Y:208)│
│                                │ │ [B1][B2] [B5][B6]  │ │ │ MR/CR/FR...  │ │
│                                │ │ [B3][B4] [B7][B8]  │ │ └──────────────┘ │
│                                │ └───────────────────┘ │ ┌─ XP Gauges(Y:288)
│                                │                       │ │ XP Gauge     │ │
│                                │                       │ │ AA Gauge     │ │
│                                │                       │ └──────────────┘ │
└────────────────────────────────┴───────────────────────┴──────────────────┘
```

## Equipment Display
DuxaUI uses a classic anatomical layout, grouping slots by body area. The arrangement is logical and closely mirrors the paper doll concept.

**Complete Equipment Coordinate Map**
```
ROW 1 - HEAD LEVEL (Y=4):
├─ InvSlot1  [LEFT_EAR]   (Size 40x40, X=47,  Y=4)
├─ InvSlot5  [NECK]       (Size 40x40, X=89,  Y=4)
├─ InvSlot3  [FACE]       (Size 40x40, X=131, Y=4)
├─ InvSlot2  [HEAD]       (Size 40x40, X=173, Y=4)
└─ InvSlot4  [RIGHT_EAR]  (Size 40x40, X=215, Y=4)

ROW 2 - ARM/HAND LEVEL (Y=47):
├─ InvSlot15 [LEFT_FINGER](Size 40x40, X=5,   Y=47)
├─ InvSlot9  [LEFT_WRIST] (Size 40x40, X=47,  Y=47)
├─ InvSlot7  [ARMS]       (Size 40x40, X=89,  Y=47)
├─ InvSlot12 [HANDS]      (Size 40x40, X=131, Y=47)
├─ InvSlot10 [RIGHT_WRIST](Size 40x40, X=173, Y=47)
└─ InvSlot16 [RIGHT_FINGER](Size 40x40, X=215, Y=47)

ROW 3 - BODY/TORSO LEVEL (Y=90):
├─ InvSlot6  [SHOULDERS]  (Size 40x40, X=5,   Y=90)
├─ InvSlot17 [CHEST]      (Size 40x40, X=47,  Y=90)
├─ InvSlot8  [BACK]       (Size 40x40, X=89,  Y=90)
├─ InvSlot20 [WAIST]      (Size 40x40, X=131, Y=90)
├─ InvSlot18 [LEGS]       (Size 40x40, X=173, Y=90)
└─ InvSlot19 [FEET]       (Size 40x40, X=215, Y=90)

ROW 4 - WEAPON/AMMO LEVEL (Y=133):
├─ InvSlot13 [PRIMARY]    (Size 40x40, X=89,  Y=133)
├─ InvSlot14 [SECONDARY]  (Size 40x40, X=131, Y=133)
├─ InvSlot11 [RANGE]      (Size 40x40, X=173, Y=133)
└─ InvSlot21 [AMMO]       (Size 40x40, X=215, Y=133)
```

## Stat Display
Stats are arranged in a single column on the right side. The most innovative feature is the use of small icons next to the seven primary stats, providing a quick visual reference.

**Stat Icon Implementation**:
The icons are implemented via `<Ui2DAnimation>` definitions that point to a spritesheet (`stat_icons.tga`). Each icon is a `StaticAnimation` piece that references one of these animations.

1.  **`Ui2DAnimation` Definitions**: A block of `Ui2DAnimation` elements defines the texture and coordinates for each stat icon.
    ```xml
    <Ui2DAnimation item="A_StatStr">
        <Cycle>false</Cycle>
        <Grid>true</Grid>
        <CellHeight>12</CellHeight>
        <CellWidth>12</CellWidth>
        <Frames>
            <Texture>stat_icons.tga</Texture>
            <Location>
                <X>0</X>
                <Y>0</Y>
            </Location>
        </Frames>
    </Ui2DAnimation>
    ... and so on for STA, DEX, AGI, WIS, INT, CHA
    ```
2.  **`StaticAnimation` Pieces**: Each stat label has a corresponding `StaticAnimation` piece placed next to it.
    ```xml
    <StaticAnimation item="IW_StrIcon">
        <ScreenID>StrIcon</ScreenID>
        <Location><X>260</X><Y>100</Y></Location>
        <Size><CX>12</CX><CY>12</CY></Size>
        <Animation>A_StatStr</Animation>
    </StaticAnimation>
    ```

**Complete Stat Coordinate Listing**
```
TOP SECTION:
├─ IW_Name       (Label, X=260, Y=4,   "Name")
├─ IW_Level      (Label, X=260, Y=18,  "Level")
├─ IW_Class      (Label, X=280, Y=18,  "Class")
└─ IW_Deity      (Label, X=260, Y=32,  "Deity")

PRIMARY STATS (Name Label, Icon, Value Label):
├─ IW_StrLabel   (Label, X=275, Y=100, "STR")
├─ IW_StrIcon    (StaticAnimation, X=260, Y=100)
└─ IW_STR        (Label, X=332, Y=100, "180")

├─ IW_StaLabel   (Label, X=275, Y=114, "STA")
├─ IW_StaIcon    (StaticAnimation, X=260, Y=114)
└─ IW_STA        (Label, X=332, Y=114, "180")

├─ IW_AgiLabel   (Label, X=275, Y=128, "AGI")
├─ IW_AgiIcon    (StaticAnimation, X=260, Y=128)
└─ IW_AGI        (Label, X=332, Y=128, "180")

├─ IW_DexLabel   (Label, X=275, Y=142, "DEX")
├─ IW_DexIcon    (StaticAnimation, X=260, Y=142)
└─ IW_DEX        (Label, X=332, Y=142, "180")

├─ IW_WisLabel   (Label, X=275, Y=156, "WIS")
├─ IW_WisIcon    (StaticAnimation, X=260, Y=156)
└─ IW_WIS        (Label, X=332, Y=156, "180")

├─ IW_IntLabel   (Label, X=275, Y=170, "INT")
├─ IW_IntIcon    (StaticAnimation, X=260, Y=170)
└─ IW_INT        (Label, X=332, Y=170, "180")

├─ IW_ChaLabel   (Label, X=275, Y=184, "CHA")
├─ IW_ChaIcon    (StaticAnimation, X=260, Y=184)
└─ IW_CHA        (Label, X=332, Y=184, "180")

COMBAT/HP STATS:
├─ IW_HP         (Label, X=265, Y=50,  "HP")
├─ IW_CurrentHP  (Label, X=287, Y=50,  "1400/1400")
├─ IW_Mana       (Label, X=265, Y=64,  "Mana")
├─ IW_CurrentMana(Label, X=287, Y=64,  "1400/1400")
├─ IW_Stamina    (Label, X=265, Y=78,  "Stamina")
├─ IW_ATK        (Label, X=260, Y=274, "ATK: 950")
└─ IW_AC         (Label, X=320, Y=274, "AC: 1250")

RESISTANCES:
├─ IW_MR         (Label, X=260, Y=208, "MR: 100")
├─ IW_FR         (Label, X=260, Y=222, "FR: 100")
├─ IW_CR         (Label, X=260, Y=236, "CR: 100")
├─ IW_DR         (Label, X=320, Y=208, "DR: 100")
└─ IW_PR         (Label, X=320, Y=222, "PR: 100")
```

## Gauges & Progress Bars
DuxaUI uses thin, horizontal gauges for HP, Mana, Stamina, XP, and Alt XP. They are all located in the right-hand column.

**Gauge Specifications**
```
├─ IW_HPGauge    (X=350, Y=52,  Size 22x10, Color: 240,0,0,   EQType: hp)
├─ IW_ManaGauge  (X=350, Y=66,  Size 22x10, Color: 0,0,240,   EQType: mana)
├─ IW_StamGauge  (X=350, Y=80,  Size 22x10, Color: 240,240,0, EQType: stamina)
├─ IW_XPBar      (X=260, Y=288, Size 112x12,Color: 180,180,0, EQType: xp)
└─ IW_AltXPBar   (X=260, Y=302, Size 112x12,Color: 0,180,180, EQType: altxp)
```

## Bag Slots
The inventory includes a 2x4 grid for the first 8 bag slots, located in the center column below the currency display.

**Bag Slot Coordinates**
```
COLUMN 1:
├─ InvSlot22 [BAG1] (Size 40x40, X=173, Y=176)
├─ InvSlot23 [BAG2] (Size 40x40, X=173, Y=219)
├─ InvSlot24 [BAG3] (Size 40x40, X=173, Y=262)
└─ InvSlot25 [BAG4] (Size 40x40, X=173, Y=305)

COLUMN 2:
├─ InvSlot26 [BAG5] (Size 40x40, X=215, Y=176)
├─ InvSlot27 [BAG6] (Size 40x40, X=215, Y=219)
├─ InvSlot28 [BAG7] (Size 40x40, X=215, Y=262)
└─ InvSlot29 [BAG8] (Size 40x40, X=215, Y=305)
```

## Recommendations for Thorne_Drak
1.  **Adopt Stat Icons**: The stat icon implementation is a significant visual and usability improvement. It's lightweight, using a single small texture file (`stat_icons.tga`) and simple `Ui2DAnimation` definitions. This would be a high-value, low-complexity addition to the Thorne UI.
2.  **Consider Compact Layout**: While the spaciousness of the default UI has its merits, the duxaUI three-column layout is a masterclass in information density. A similar compact mode or variant for Thorne could be very popular.
3.  **Horizontal Gauges**: The thin horizontal gauges next to the HP/Mana/Stamina labels are more space-efficient than the default vertical gauges. This is a simple change that could free up significant vertical space for other elements.
4.  **Anatomical Grouping**: The equipment layout is more intuitive than the default's grid. Adopting this anatomical grouping would improve usability, especially for new players.
5.  **Integrated Bags**: Placing the primary bag slots directly in the inventory window is a major quality-of-life improvement, reducing the number of open windows. This is a core feature of many modern UIs and should be a priority.
