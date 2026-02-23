# Inventory Window - Standard Variant

**File**: [EQUI_Inventory.xml](./EQUI_Inventory.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-17
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne

---
## Purpose

The standard Inventory window variant provides the traditional EverQuest paperdoll equipment display with standard slot backgrounds and default styling. This is the baseline implementation for character equipment management and stats viewing.

**Key Features**:

- **Full Paperdoll Layout**: All 21 equipment slots (ears, head, face, neck, shoulders, arms, chest, back, wrists, hands, rings, waist, legs, feet, primary, secondary, range, ammo)
- **Character Preview**: 3D character model display with rotation capability
- **Complete Stats Display**: Base attributes (STR-CHA), resistances (MR/FR/CR/PR/DR), weight tracking, AA progression
- **Standard Slot Backgrounds**: Default EQ slot backgrounds (ear, head, face, neck, etc. templates)
- **Bag Slots**: Cursor slot + 8 general inventory slots
- **FacePick & Tinting**: Character customization buttons

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | Varies by content (no fixed CX/CY in main Screen) |
| Resizable | No (`Style_Sizable` not specified = false) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID  | InventoryWindow |
| DrawTemplate | Not explicitly specified (uses default) |
| Equipment Slots | 21 worn + 8 bags + 1 cursor = 30 total InvSlots |
| Sub-Screens | IW_CharacterView (3D model display) |

---

## Layout Overview

### Window Hierarchy

```text
InventoryWindow
├── Equipment Slots (Top Row)
│   ├── InvSlot1 (L_EAR) - X=44, Y=-1
│   ├── InvSlot5 (NECK) - X=88, Y=-1
│   ├── InvSlot3 (FACE) - X=133, Y=-1
│   ├── InvSlot2 (HEAD) - X=178, Y=-1
│   └── InvSlot4 (R_EAR) - X=223, Y=-1
├── Body Equipment (Left Column)
│   ├── InvSlot6 (SHOULDERS)
│   ├── InvSlot9 (L_WRIST)
│   ├── InvSlot13 (PRIMARY)
│   └── InvSlot11 (RANGE)
├── Core Body (Center)
│   ├── InvSlot7 (ARMS)
│   ├── InvSlot8 (ABOUT_BODY/Chest)
│   └── InvSlot20 (WAIST)
├── Body Equipment (Right Column)
│   ├── InvSlot10 (R_WRIST)
│   ├── InvSlot14 (SECONDARY)
│   └── InvSlot21 (AMMO)
├── Lower Body
│   ├── InvSlot15 (L_RING)
│   ├── InvSlot12 (HANDS)
│   ├── InvSlot16 (R_RING)
│   ├── InvSlot18 (LEGS)
│   └── InvSlot19 (FEET)
├── Character Stats Display
│   ├── IW_STR, IW_STA, IW_AGI, IW_DEX, IW_WIS, IW_INT, IW_CHA
│   ├── IW_Magic, IW_Fire, IW_Cold, IW_Poison, IW_Disease
│   ├── IW_Weight, IW_CurrentWeight, IW_MaxWeight
│   └── IW_AltAdv, IW_AltAdvGauge
├── IW_CharacterView (3D model display)
├── IW_DoneButton
├── IW_FacePick (face customization)
└── IW_Tinting (armor tinting)
```

### Equipment Slot Layout (Paperdoll)

```text
     [L_EAR] [NECK] [FACE] [HEAD] [R_EAR]
[SHOULDER]   [ARMS]  [CHEST]   [R_WRIST]
             [WAIST]
[L_WRIST]    [HANDS]            [LEGS]
[PRIMARY]                       [FEET]
[RANGE]                         [SECONDARY]
[AMMO]       [L_RING] [R_RING]
```

---

## Key Elements

### Equipment Slots by EQType

| Slot Name | InvSlot# | Location | Size | EQType | Background Template |
|-----------|----------|----------|------|--------|--------------------|
| Charm | InvSlot0 | Hidden | 1×1 | 0 | Hidden (unused) |
| Left Ear | InvSlot1 | X=44, Y=-1 | 45×45 | 1 | A_InvEar |
| Head | InvSlot2 | X=178, Y=-1 | 45×45 | 2 | A_InvHead |
| Face | InvSlot3 | X=133, Y=-1 | 45×45 | 3 | A_InvFace |
| Right Ear | InvSlot4 | X=223, Y=-1 | 45×45 | 4 | A_InvEar |
| Neck | InvSlot5 | X=88, Y=-1 | 45×45 | 5 | A_InvNeck |
| Shoulders | InvSlot6 | X=-1, Y=82 | 45×45 | 6 | A_InvShoulders |
| Arms | InvSlot7 | X=88, Y=41 | 45×45 | 7 | A_InvArms |
| About Body | InvSlot8 | X=88, Y=82 | 45×45 | 8 | A_InvAboutBody |
| Left Wrist | InvSlot9 | X=44, Y=41 | 45×45 | 9 | A_InvWrist |
| Right Wrist | InvSlot10 | X=133, Y=41 | 45×45 | 10 | A_InvWrist |
| Range | InvSlot11 | X=-1, Y=205 | 45×45 | 11 | A_InvRange |
| Hands | InvSlot12 | X=88, Y=164 | 45×45 | 12 | A_InvHands |
| Primary | InvSlot13 | X=-1, Y=123 | 45×45 | 13 | A_InvPrimary |
| Secondary | InvSlot14 | X=223, Y=164 | 45×45 | 14 | A_InvSecondary |
| Left Ring | InvSlot15 | X=44, Y=164 | 45×45 | 15 | A_InvRing |
| Right Ring | InvSlot16 | X=133, Y=164 | 45×45 | 16 | A_InvRing |
| Chest | InvSlot17 | Hidden | 45×45 | 17 | A_InvChest |
| Legs | InvSlot18 | X=178, Y=164 | 45×45 | 18 | A_InvLegs |
| Feet | InvSlot19 | X=178, Y=205 | 45×45 | 19 | A_InvFeet |
| Waist | InvSlot20 | X=88, Y=123 | 45×45 | 20 | A_InvWaist |
| Ammo | InvSlot21 | X=223, Y=205 | 45×45 | 21 | A_InvAmmo |

### Bag/Inventory Slots (General Inventory)

| Slot | EQType | Notes |
|------|--------|-------|
| InvSlot22-29 | 22-29 | General inventory bags (8 slots) |
| InvSlot30 | 30 | Cursor slot (item on cursor) |

---

## Color Scheme

**Uses default EQ color scheme** - no custom RGB values specified for standard backgrounds.

**Background Templates**:
- Specialized backgrounds for each slot type (A_InvEar, A_InvHead, A_InvFace, etc.)
- `A_RecessedBox` used in other variants for generic slots

---

## Technical Notes

- **Slot Size Consistency**: All equipment slots are 45×45 pixels
- **Charm Slot**: InvSlot0 (EQType 0) is hidden with 1×1 size - charm slot not used in classic EQ
- **Negative Positioning**: Top row uses Y=-1 for tight alignment at window top edge
- **Left Column Alignment**: X=-1 used for left edge slots (shoulders, primary, range)
- **Font**: Font 3 used for labels and stat displays
- **Background Templates**: Each slot type has unique background graphic (ear icon, head silhouette, etc.)
- **Style Flags**: All slots have `Style_VScroll=false, Style_HScroll=false, Style_Transparent=false`
- **Character View**: IW_CharacterView sub-screen provides 3D model display with rotation
- **AA Display**: IW_AltAdvGauge shows alternative advancement progression
- **Weight Tracking**: Current weight (EQType 24) / Max weight (EQType 25) display
- **Stats Display**: Full attribute and resistance readouts

---

## What Makes This "Standard"

This variant represents the traditional EverQuest inventory interface:
- **Default Backgrounds**: Uses standard slot background templates (no dark slots or color-coded variations)
- **Standard Paperdoll**: Classic EQ equipment layout matching original game design
- **No Custom Colors**: Weapon slots and equipment use default textures
- **Reference Baseline**: "Dark Slots and Color Weapons" variant modifies slot backgrounds, while this maintains defaults
- **Complete Feature Set**: All slots, stats, and customization options included
- **Classic Visual Style**: Matches traditional EQ aesthetic expectations

---

## Installation

1. Copy `EQUI_Inventory.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

**Note**: File is named `EQUI_Inventory.xml` (not `EQUI_InventoryWindow.xml`)

## Reverting

To switch to other variants:
- **Dark Slots and Color Weapons**: Copy from `Options/Inventory/Dark Slots and Color Weapons/` (texture-based variant)
- Other visual variants may be available

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Dark Slots and Color Weapons](../Dark%20Slots%20and%20Color%20Weapons/README.md)
