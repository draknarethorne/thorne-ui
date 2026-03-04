# Inventory Window Analysis: Infiniti-Blue

## Executive Summary
The Infiniti-Blue inventory window is a masterclass in thematic consistency and efficient design. It leverages a texture atlas (`window_pieces_i3.tga`) to create a cohesive, blue-toned aesthetic that defines the entire UI suite. The layout is a standard, spacious paper-doll arrangement that prioritizes clarity and ease of use. Its most notable feature is the use of four `StaticAnimation` elements, which stitch together different parts of a single texture file to form a complete, non-repeating background. This technique provides a high-quality visual identity with minimal performance overhead, as only one texture file needs to be loaded.

## Quick Reference
- **Directory**: `Infiniti-Blue/`
- **File**: `EQUI_Inventory.xml`
- **Window Size**: 292x373 px
- **Template**: `WDT_Untextured`
- **Total Elements**: 71
- **Subwindows**: 0
- **Unique Features**:
    - Extensive use of a single texture atlas (`window_pieces_i3.tga`) for all window dressing.
    - Background constructed from four separate `StaticAnimation` pieces.
    - Clean, spacious layout with clearly defined sections.
    - Horizontal XP and AA gauges at the bottom.

## Layout Architecture
The window uses a traditional three-column design. The left column is dedicated to bag slots, the center column features the paper-doll equipment slots, and the right column displays character stats and information. The bottom of the window contains gauges for XP and Alternate Advancement. The entire window is framed by a custom border and background drawn from the `window_pieces_i3.tga` texture atlas, creating a strong, unified theme.

```
┌───────────────────────────────────────────────────┐
│                      TOP BAR                      │
├──────────┬──────────────────────┬─────────────────┤
│          │   ┌────────────────┐   │                 │
│          │   │   HEAD/FACE    │   │   NAME / CLASS  │
│          │   │  (130,8) (40x80)│   │   (213,41)      │
│          │   └────────────────┘   │                 │
│          │                      │                 │
│ BAG SLOTS│   PAPER-DOLL SLOTS   │  CHARACTER STATS│
│ (2x4 Grid) │   (Anatomical)       │  (213, 76)      │
│ (9, 168)   │   (90, 8)            │                 │
│          │                      │                 │
│          │                      │                 │
│          │                      │                 │
├──────────┴──────────────────────┴─────────────────┤
│             GAUGES (XP / AA)                    │
│             (176, 359)                          │
└───────────────────────────────────────────────────┘
```

## Icons & Graphics: The Texture Atlas Technique
A key innovation of the Infiniti-Blue UI is its efficient use of a texture atlas, `window_pieces_i3.tga`. Instead of using multiple image files for different UI elements, it defines animations that act as viewports into a single, larger texture.

The inventory background is composed of four `StaticAnimation` elements: `A_Inv_BG1`, `A_Inv_BG2`, `A_Inv_BG3`, and `A_Inv_BG4`. Each of these animations sources its texture from `window_pieces_i3.tga` but uses a different `Location` (X/Y offset) to clip a specific quadrant of the source image. These are then arranged in a 2x2 grid to form the complete background.

- **`Infiniti-Inv_BG1`**: Clips `window_pieces_i3.tga` at (0, 0) with size 144x168.
- **`Infiniti-Inv_BG2`**: Clips `window_pieces_i3.tga` at (38, 0) with size 144x168.
- **`Infiniti-Inv_BG3`**: Clips `window_pieces_i3.tga` at (0, 87) with size 144x168.
- **`Infiniti-Inv_BG4`**: Clips `window_pieces_i3.tga` at (38, 87) with size 144x168.

These are then positioned in the window:
- `A_Inv_BG1` at `(0, 0)`
- `A_Inv_BG2` at `(144, 0)`
- `A_Inv_BG3` at `(0, 168)`
- `A_Inv_BG4` at `(144, 168)`

This method is highly efficient, reducing draw calls and memory usage while allowing for a complex and visually interesting background that defines the UI's theme.

## Equipment Display
The equipment slots follow a standard paper-doll layout, centered in the window. All slots are 40x40 pixels.

**ROW 1 - HEAD LEVEL (Y=8)**
├─ InvSlot1  [LEFT_EAR]   (Size: 40x40, X=90, Y=8)
├─ InvSlot2  [HEAD]       (Size: 40x40, X=130, Y=8)
└─ InvSlot4  [RIGHT_EAR]  (Size: 40x40, X=170, Y=8)

**ROW 2 - NECK/SHOULDERS (Y=48)**
├─ InvSlot6  [SHOULDERS]  (Size: 40x40, X=90, Y=48)
├─ InvSlot3  [FACE]       (Size: 40x40, X=130, Y=48)
└─ InvSlot5  [NECK]       (Size: 40x40, X=170, Y=48)

**ROW 3 - CHEST/BACK (Y=88)**
├─ InvSlot8  [BACK]       (Size: 40x40, X=90, Y=88)
├─ InvSlot17 [CHEST]      (Size: 40x40, X=130, Y=88)
└─ InvSlot20 [WAIST]      (Size: 40x40, X=170, Y=88)

**ROW 4 - ARMS/WRISTS (Y=128)**
├─ InvSlot9  [LEFT_WRIST] (Size: 40x40, X=90, Y=128)
├─ InvSlot7  [ARMS]       (Size: 40x40, X=130, Y=128)
└─ InvSlot10 [RIGHT_WRIST](Size: 40x40, X=170, Y=128)

**ROW 5 - HANDS/FINGERS (Y=168)**
├─ InvSlot15 [LEFT_FINGER](Size: 40x40, X=90, Y=168)
├─ InvSlot12 [HANDS]      (Size: 40x40, X=130, Y=168)
└─ InvSlot16 [RIGHT_FINGER](Size: 40x40, X=170, Y=168)

**ROW 6 - LEGS/FEET/AMMO (Y=208)**
├─ InvSlot18 [LEGS]       (Size: 40x40, X=90, Y=208)
├─ InvSlot19 [FEET]       (Size: 40x40, X=130, Y=208)
└─ InvSlot21 [AMMO]       (Size: 40x40, X=170, Y=208)

**ROW 7 - WEAPONS/RANGE (Y=248)**
├─ InvSlot13 [PRIMARY]    (Size: 40x40, X=90, Y=248)
├─ InvSlot14 [SECONDARY]  (Size: 40x40, X=130, Y=248)
└─ InvSlot11 [RANGE]      (Size: 40x40, X=170, Y=248)

## Stat Display
Stats are neatly organized in the top-right quadrant of the window.

**Character Info:**
├─ IW_Name       (Label, X=213, Y=41)
├─ IW_Level      (Label, X=214, Y=52)
├─ IW_Class      (Label, X=226, Y=52)
└─ IW_Deity      (Label, X=214, Y=63)

**Core Stats:**
├─ IW_HP         (Label, X=213, Y=76)
├─ IW_CurrentHP  (Label, X=234, Y=76)
├─ IW_AC         (Label, X=214, Y=88)
├─ IW_ACNumber   (Label, X=247, Y=88)
├─ IW_ATK        (Label, X=214, Y=99)
└─ IW_ATKNumber  (Label, X=247, Y=99)

**Attributes:**
├─ IW_STR        (Label, X=213, Y=111)
├─ IW_STRNumber  (Label, X=246, Y=111)
├─ IW_STA        (Label, X=213, Y=123)
├─ IW_STANumber  (Label, X=246, Y=123)
├─ IW_AGI        (Label, X=213, Y=135)
├─ IW_AGINumber  (Label, X=246, Y=135)
├─ IW_DEX        (Label, X=213, Y=147)
├─ IW_DEXNumber  (Label, X=246, Y=147)
├─ IW_WIS        (Label, X=213, Y=159)
├─ IW_WISNumber  (Label, X=246, Y=159)
├─ IW_INT        (Label, X=213, Y=171)
├─ IW_INTNumber  (Label, X=246, Y=171)
├─ IW_CHA        (Label, X=213, Y=183)
└─ IW_CHANumber  (Label, X=246, Y=183)

**Resistances:**
├─ IW_MR         (Label, X=213, Y=195)
├─ IW_MRNumber   (Label, X=246, Y=195)
├─ IW_FR         (Label, X=213, Y=207)
├─ IW_FRNumber   (Label, X=246, Y=207)
├─ IW_CR         (Label, X=213, Y=219)
├─ IW_CRNumber   (Label, X=246, Y=219)
├─ IW_DR         (Label, X=213, Y=231)
├─ IW_DRNumber   (Label, X=246, Y=231)
├─ IW_PR         (Label, X=213, Y=243)
└─ IW_PRNumber   (Label, X=246, Y=243)

## Gauges & Progress Bars
Two horizontal gauges are placed at the bottom of the window.

├─ IW_ExpGauge    (X=176, Y=359, Size: 116x8, Color: 220,150,0, EQType: 4)
└─ IW_AltExpGauge (X=176, Y=349, Size: 116x8, Color: 150,220,0, EQType: 5)

## Bag Slots
The eight primary inventory bag slots are arranged in a 2x4 grid on the left side.

**Column 1 (X=9)**
├─ InvSlot22 [BAG1] (Size: 40x40, X=9, Y=168)
├─ InvSlot23 [BAG2] (Size: 40x40, X=9, Y=208)
├─ InvSlot24 [BAG3] (Size: 40x40, X=9, Y=248)
└─ InvSlot25 [BAG4] (Size: 40x40, X=9, Y=288)

**Column 2 (X=49)**
├─ InvSlot26 [BAG5] (Size: 40x40, X=49, Y=168)
├─ InvSlot27 [BAG6] (Size: 40x40, X=49, Y=208)
├─ InvSlot28 [BAG7] (Size: 40x40, X=49, Y=248)
└─ InvSlot29 [BAG8] (Size: 40x40, X=49, Y=288)

## Unique Features
- **Visual Theming via Texture Atlas**: The entire window's look and feel is derived from a single texture file (`window_pieces_i3.tga`). This creates a highly consistent and professional aesthetic.
- **Spacious Layout**: Compared to other UIs, Infiniti-Blue provides ample spacing between elements, which improves readability and reduces mis-clicks.
- **Texture Efficiency**: The use of `Ui2DAnimation` to clip parts of a larger texture is a smart optimization that reduces the number of files and memory required to render the window.

## Implementation Notes
- **Theming**: To change the theme of the inventory window, one would need to edit or replace `window_pieces_i3.tga`. The XML file itself defines the coordinates for clipping, so any replacement texture must align with the existing layout or the XML must be updated.
- **Texture Dependencies**: The window is entirely dependent on `window_pieces_i3.tga` and the standard icon set provided by the game (e.g., `A_InvEar`, `A_InvHead`). Without `window_pieces_i3.tga`, the window would lose its entire custom background and border.
- **Customization**: The layout is straightforward. Moving elements requires changing their `Location` tags. Because the background is composed of four static pieces, moving elements across the boundaries of these pieces (e.g., from X=143 to X=145) has no adverse effect.
