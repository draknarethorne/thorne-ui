# Actions Window - Standard Variant

**File**: [EQUI_ActionsWindow.xml](./EQUI_ActionsWindow.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne

---
## Purpose

The standard Actions window variant provides a comprehensive character management interface combining action buttons, stats display, and inventory access in a dual-tabbed system. This is the baseline implementation with full character information and equipment management.

**Key Features**:

- **Dual TabBox System**: Separate tab groups for Actions (Info/Main/Abilities/Combat/Socials) and Inventory (Bags/Worn)
- **Integrated Inventory Tabs**: Full equipment display including bags (slots 22-29) and worn armor/jewelry
- **Complete Stats Display**: Character attributes (STR, STA, AGI, DEX, WIS, INT, CHA), combat stats (AC, ATK), and resistances (MR, FR, CR, PR, DR)
- **Action Buttons**: Quick access to abilities, combat actions, and social macros
- **Player Info Summary**: HP/Mana, AC/ATK, Weight, and AA progression on Info page

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | Fixed (no explicit CX/CY in Screen definition) |
| Resizable | No (`Style_Sizable` not specified = false) |
| Fadeable | No (no `Style_Transparent` flag) |
| Screen ID | ActionsWindow |
| DrawTemplate | Standard window template |
| Default Position | Not specified (client default) |
| Tab Systems | 2 independent TabBoxes |
| Total Pages | 7 (5 Actions + 2 Inventory) |

---

## Layout Overview

### Window Hierarchy

```text
ActionsWindow
├── ACTW_ActionsSubwindows (TabBox at X=4, Y=8, 145×170)
│   ├── ActionsInfoPage (player stats summary)
│   ├── ActionsMainPage (character stats, action buttons)
│   ├── ActionsAbilitiesPage (6 ability buttons)
│   ├── ActionsCombatPage (melee/range attack, 4 abilities)
│   └── ActionsSocialsPage (social macros grid)
└── ACTW_InventorySubwindows (TabBox at X=4, Y=180, 145×203)
    ├── ActionsEquipmentPage1 "Bags" (bags 22-29 + weapons)
    └── ActionsEquipmentPage2 "Worn" (all worn equipment slots)
```

### Action TabBox Layout (145×170)

**Info Page**: Displays player name, level, class, HP/Mana values, AC, ATK, Weight, and AA progression  
**Main Page**: Base stats (STR-CHA), resistances (MR/FR/CR/PR/DR), AC/ATK, and 9 action buttons  
**Abilities Page**: 6 ability buttons in 3×2 grid  
**Combat Page**: Melee/Range attack buttons + 4 combat abilities  
**Socials Page**: Social macro management

### Inventory TabBox Layout (145×203)

**Bags Page**: Primary/Secondary/Range/Ammo weapons (left column) + Bag slots 22-29 (right grid)  
**Worn Page**: All 17 worn equipment slots in paperdoll layout

---

## Key Elements

### Actions TabBox Components

| Element | Location | Size | EQType/Notes |
|---------|----------|------|-------------|
| ACTW_ActionsSubwindows | X=4, Y=8 | 145×170 | Main action tabs container |
| ACTW_PlayerName | X=8, Y=8 | 128×16 | EQType 1 (player name) |
| ACTW_Level | X=117, Y=8 | 19×16 | EQType 2 (level) |
| ACTW_PlayerClass | X=8, Y=24 | 128×16 | EQType 3 (class name) |
| ACTW_CurrentHP | X=86, Y=52 | 50×14 | EQType 70 (HP cur/max) |
| ACTW_CurrentMana | X=86, Y=66 | 50×14 | EQType 80 (Mana cur/max) |
| STRnum - CHAnum | Various | 30×14 | EQTypes 5-11 (base stats) |
| ACnum | X=105, Y=0 | 30×14 | EQType 22 (armor class) |
| ATKnum | X=105, Y=11 | 30×14 | EQType 23 (attack rating) |
| SvMnum - SvDnum | X=105 | 30×15 | EQTypes 12-16 (resistances) |

### Inventory TabBox Components

| Element | Location | Size | EQType/Notes |
|---------|----------|------|-------------|
| ACTW_InventorySubwindows | X=4, Y=180 | 145×203 | Inventory tabs container |
| ACTW_Primary | X=2, Y=2 | 44×44 | EQType 13 (primary weapon) |
| ACTW_Secondary | X=2, Y=46 | 44×44 | EQType 14 (secondary weapon) |
| ACTW_Range | X=2, Y=90 | 44×44 | EQType 11 (ranged weapon) |
| ACTW_Ammo | X=2, Y=134 | 44×44 | EQType 21 (ammo slot) |
| ACTW_BagSlot22-29 | Grid layout | 44×44 each | EQTypes 22-29 (inventory bags) |
| ACTW_Head, Face, Ears, etc. | Paperdoll grid | 36×36 each | EQTypes 1-20 (worn slots) |

---

## Color Scheme

**Character Stats Colors**:
- **Base Stats Labels** (STR, STA, AGI, DEX, WIS, INT, CHA): RGB(50, 160, 250) - Light blue
- **Stat Values**: RGB(255, 255, 255) - White
- **AC/ATK Labels**: RGB(255, 165, 0) - Orange
- **Resistance Labels**: 
  - Magic: RGB(195, 0, 185) - Purple
  - Fire: RGB(195, 20, 20) - Red
  - Cold: RGB(0, 120, 255) - Blue
  - Poison: RGB(0, 130, 100) - Green
  - Disease: RGB(205, 205, 0) - Yellow

**Info Page Colors**:
- **HP Display**: RGB(255, 100, 100) - Light red
- **Mana Display**: RGB(150, 150, 255) - Light blue
- **AC/ATK Values**: RGB(150, 150, 255) - Light blue

---

## Technical Notes

- **Button Size Standard**: All action buttons are 40×40 pixels with matching DecalSize
- **Equipment Slots - Two Sizes**: Weapons/bags use 44×44, worn equipment uses 36×36
- **Independent Tab Systems**: Actions and Inventory TabBoxes operate independently, allowing different pages active simultaneously
- **EQType Coverage**: Full coverage of character stats (1-25), HP/Mana (70/80), weight (24/25), AA (36/37), and all equipment slots (1-29)
- **Button Templates**: Uses `A_SquareBtnNormal` for action buttons, `A_SmallBtnNormal` for social buttons
- **Background Templates**: `A_RecessedBox` for bag slots, specialized backgrounds (A_InvPrimary, A_InvHead, etc.) for equipment
- **Tab Navigation**: Each TabBox has icon-based tabs with active/inactive states
- **Font Usage**: Font 2 for stats/labels, Font 3 for player info

---

## Element Inventory - Complete Tab System

### Actions TabBox Pages (ACTW_ActionsSubwindows @ X=4, Y=8)

| Page | Element | Row | Column | Size (px) | EQType | Function |
|------|---------|-----|--------|-----------|--------|----------|
| Info | ACTW_PlayerName | 1 | 1 | 128×16 | 1 | Character name display |
| Info | ACTW_Level | 1 | 2 | 19×16 | 2 | Character level |
| Info | ACTW_PlayerClass | 2 | 1 | 128×16 | 3 | Class name (Warrior, Cleric, etc.) |
| Info | ACTW_CurrentHP | 3 | 1 | 50×14 | 70 | Current/Max HP display (red) |
| Info | ACTW_CurrentMana | 4 | 1 | 50×14 | 80 | Current/Max Mana display (blue) |
| Main | STR-CHA Stats | 1-7 | Stat Area | 30×14 | 5-11 | Base attributes (Strength-Charisma) |
| Main | AC Value | AC Row | Right | 30×14 | 22 | Armor Class numeric |
| Main | ATK Value | ATK Row | Right | 30×14 | 23 | Attack rating numeric |
| Main | Resistances | Resist Rows | Right | 30×15 | 12-16 | MR/FR/CR/PR/DR columns |
| Main | 9 Action Buttons | Grid 3×3 | X=16-120, Y=52-142 | 40×40 | N/A | Quick ability access buttons |
| Abilities | Ability Button 1 | Row 1 | Col 1 | 40×40 | N/A | Ability slot 1 |
| Abilities | Ability Button 2 | Row 1 | Col 2 | 40×40 | N/A | Ability slot 2 |
| Abilities | Ability Button 3 | Row 2 | Col 1 | 40×40 | N/A | Ability slot 3 |
| Abilities | Ability Button 4 | Row 2 | Col 2 | 40×40 | N/A | Ability slot 4 |
| Abilities | Ability Button 5 | Row 3 | Col 1 | 40×40 | N/A | Ability slot 5 |
| Abilities | Ability Button 6 | Row 3 | Col 2 | 40×40 | N/A | Ability slot 6 |
| Combat | MeleeAttackButton | Row 1 | Col 1 | 40×40 | N/A | Melee attack trigger |
| Combat | RangeAttackButton | Row 1 | Col 2 | 40×40 | N/A | Ranged attack trigger |
| Combat | Combat Ability 1 | Row 2 | Col 1 | 40×40 | N/A | Combat ability slot 1 |
| Combat | Combat Ability 2 | Row 2 | Col 2 | 40×40 | N/A | Combat ability slot 2 |
| Combat | Combat Ability 3 | Row 3 | Col 1 | 40×40 | N/A | Combat ability slot 3 |
| Combat | Combat Ability 4 | Row 3 | Col 2 | 40×40 | N/A | Combat ability slot 4 |
| Socials | Page Left Button | Nav | Left | 20×20 | N/A | Previous social page |
| Socials | Page Right Button | Nav | Right | 20×20 | N/A | Next social page |
| Socials | Social Buttons 1-12 | Grid 3×4 | X=16-120, Y=40-142 | 32×32 | N/A | Social macro slots 1-12 |

### Inventory TabBox Pages (ACTW_InventorySubwindows @ X=4, Y=180)

| Page | Element | Slot | Position | Size (px) | EQType | Function |
|------|---------|------|----------|-----------|--------|----------|
| Bags | Primary Weapon | Eq-13 | X=2, Y=2 | 44×44 | 13 | Main hand weapon |
| Bags | Secondary Weapon | Eq-14 | X=2, Y=46 | 44×44 | 14 | Off-hand weapon/shield |
| Bags | Ranged Weapon | Eq-11 | X=2, Y=90 | 44×44 | 11 | Bow/crossbow/thrown |
| Bags | Ammo | Eq-21 | X=2, Y=134 | 44×44 | 21 | Arrow/bolt/throwing stars |
| Bags | Bag Slots 22-29 | 8 Bags | Grid 2×4 @ X=46, Y=2-134 | 44×44 | 22-29 | Inventory bags (8 slots) |
| Worn | Head | Eq-2 | Paperdoll head area | 36×36 | 2 | Head armor slot |
| Worn | Face | Eq-3 | Paperdoll face area | 36×36 | 3 | Face coverage (goggles, masks) |
| Worn | Ears (L/R) | Eq-1,4 | Paperdoll ears | 36×36 | 1, 4 | Left/Right earrings |
| Worn | Neck | Eq-5 | Paperdoll neck | 36×36 | 5 | Necklace/collar |
| Worn | Shoulders | Eq-6 | Paperdoll shoulders | 36×36 | 6 | Shoulder armor |
| Worn | Arms | Eq-7 | Paperdoll arms | 36×36 | 7 | Arm guards/sleeves |
| Worn | Wrists (L/R) | Eq-9,10 | Paperdoll wrists | 36×36 | 9, 10 | Left/Right bracer |
| Worn | Hands | Eq-12 | Paperdoll hands | 36×36 | 12 | Gloves/braces |
| Worn | About Body | Eq-8 | Paperdoll back | 36×36 | 8 | Cloak/shawl/back slot |
| Worn | Chest | Eq-17 | Paperdoll chest | 36×36 | 17 | Breastplate/tunic |
| Worn | Waist | Eq-20 | Paperdoll waist | 36×36 | 20 | Belt/girdle |
| Worn | Rings (L/R) | Eq-15,16 | Paperdoll hands | 36×36 | 15, 16 | Left/Right ring |
| Worn | Legs | Eq-18 | Paperdoll legs | 36×36 | 18 | Pants/leggings |
| Worn | Feet | Eq-19 | Paperdoll feet | 36×36 | 19 | Boots/shoes |

---

## Variant Comparison - Actions Window Layouts

| Feature | Standard | Bags & Inventory |
|---------|----------|------------------|
| **Window Size** | Fixed (no explicit sizing) | 160×394 px (fixed) |
| **Resizable** | No | No |
| **Tab Organization** | Vertical (5+2 pages stacked) | Side-by-side dual-column |
| **Actions Pages** | 5 (Info/Main/Abilities/Combat/Socials) | 4 (Main/Abilities/Combat/Socials, no Info) |
| **Inventory Access** | Top inventory tabs below actions | Right column simultaneous view |
| **Stat Display** | Full on Main & Info pages | Compact at bottom |
| **Layout Priority** | Actions primary, Inventory secondary | Dual-priority layout |
| **Typical Usage** | Character building, combat | Crafting, inventory management |
| **Equipment View** | Sequential (switch between tabs) | Always visible (right column) |
| **Social Macros** | Dedicated Socials page (12 slots) | Socials page (12 slots) |

---

## Technical Implementation - Standard Variant

### TabBox Architecture

**ACTW_ActionsSubwindows** (X=4, Y=8, 145×170):
- Page control via tab icons at top
- Active page content renders within bounding box
- Page switching doesn't affect Inventory TabBox state
- Tab styling uses active/inactive state graphics

**ACTW_InventorySubwindows** (X=4, Y=180, 145×203):
- Separate from Actions TabBox
- Can display Bags or Worn tab while Actions shows any page
- Weapon/Ammo slots (44×44) in column 1; Bag slots (44×44) in column 2
- Worn equipment uses compact paperdoll layout (36×36 per slot)

### EQType Coverage & Button Standards

- **Character Stats**: EQType 1-25 provides all base attributes, HP/Mana, weight, AC/ATK
- **Gauges**: EQType 70 (HP current), 80 (Mana current) for tinted displays
- **Equipment**: EQType 1-29 covers all wearable and bag slots
- **Button Size**: Action buttons standardized at 40×40 DecalSize with consistent spacing
- **Social Buttons**: Smaller at 32×32 DecalSize on Socials page
- **Font Usage**: Font 2 for labels/stats, Font 3 for player name/level

### Performance & Compatibility

- Independent TabBox rendering prevents performance impact from hidden pages
- Fixed-size windows compatible with all screen resolutions
- Weapon/Bag slot positioning uses absolute X/Y for consistency
- Paperdoll layout mirrors standard EverQuest conventions for familiarity

---

## What Makes This "Standard"

This variant represents the comprehensive baseline Actions window with full functionality:
- **Complete Feature Set**: All available stats, equipment slots, and action pages enabled
- **No Simplification**: Unlike minimal variants, includes full stat displays and resistance values
- **Dual Tab System**: Both Actions and Inventory tabs integrated for one-window character management
- **Paperdoll Layout**: Traditional EverQuest equipment display on "Worn" page
- **Reference Implementation**: Other variants may remove or reorganize features found here

---

## Installation

1. Copy `EQUI_ActionsWindow.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

## Reverting

To switch to other variants:
- **Bags and Inventory**: Copy from `Options/Actions/Bags and Inventory/EQUI_ActionsWindow.xml`
- Other variants may be available in sibling directories

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Bags and Inventory](../Bags%20and%20Inventory/README.md)
