# Loot Window - Standard Variant

**File**: [EQUI_LootWnd.xml](./EQUI_LootWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne (based on Calmethar/Brujoloco mods with Zeal integration)

---
## Purpose

The standard Loot window variant provides a compact vertical corpse looting interface with streamlined item display. This baseline implementation focuses on efficient looting with minimal screen space usage.

**Key Features**:

- **Compact Vertical Layout**: 2-column grid of loot slots (95 items maximum)
- **Corpse Name Display**: Large corpse owner name at top (210-wide label)
- **Resizable Window**: Adjustable height to show more/fewer slots (`Style_Sizable=true`)
- **Zeal Integration**: Includes "Link All" button for sharing loot to chat
- **Loot All Button**: Quick-loot all items from corpse
- **Minimal Footprint**: 120×470 default size, expandable vertically

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 120 × 470 pixels (default, vertically resizable) |
| Resizable | Yes (`Style_Sizable=true`, vertical only) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | LootWnd |
| DrawTemplate | WDT_RoundedNoTitle |
| Default Position | X=0, Y=25 (top-left screen area) |
| Titlebar | Yes (but Style_Titlebar=false for "no title" draw) |
| Closebox | No (`Style_Closebox=false`) |
| Loot Slot Count | 95 slots (0-94) in 2-column layout |
| Loot Slot Size | 40×40 pixels each |

---

## Layout Overview

### Window Hierarchy

```text
LootWnd (120×470, resizable)
├── LW_LootInvWnd (sub-window containing loot grid)
│   ├── LW_LootSlot0 (X=5, Y=0)
│   ├── LW_LootSlot1 (X=50, Y=0)
│   ├── LW_LootSlot2 (X=5, Y=40)
│   ├── LW_LootSlot3 (X=50, Y=40)
│   └── ... (continues to LW_LootSlot94)
├── LW_CorpseName (corpse owner label)
├── LW_DoneButton (close loot window)
├── LW_LinkAllButton (link all items to chat)
└── LW_LootAllButton (loot everything)
```

### Loot Slot Grid Pattern

```text
Column 1 (X=5)   Column 2 (X=50)
[Slot 0]         [Slot 1]        Y=0
[Slot 2]         [Slot 3]        Y=40
[Slot 4]         [Slot 5]        Y=80
[Slot 6]         [Slot 7]        Y=120
[Slot 8]         [Slot 9]        Y=160
  ...
[Slot 94]                        Y=1880

(95 total slots in 2-column vertical scroll)
```

---

## Key Elements

### Loot Slots

| Element Pattern | Location | Size | EQType Range | Notes |
|-----------------|----------|------|--------------|-------|
| LW_LootSlot0-94 (even) | X=5, Y varies | 40×40 | 5000-5094 | Left column (slots 0, 2, 4, ..., 94) |
| LW_LootSlot1-93 (odd) | X=50, Y varies | 40×40 | 5001-5093 | Right column (slots 1, 3, 5, ..., 93) |

**Y-Position Formula**:
- **Even slots** (column 1): Y = (slot# / 2) * 40
- **Odd slots** (column 2): Y = ((slot# - 1) / 2) * 40

**Example Positions**:
- Slot 0: X=5, Y=0
- Slot 1: X=50, Y=0  
- Slot 10: X=5, Y=200
- Slot 11: X=50, Y=200

### Window Components

| Element | Location | Size | Function |
|---------|----------|------|----------|
| LW_CorpseName | X=210, Y=180 | 100×40 | Displays "[Name]'s Corpse" (centered) |
| LW_DoneButton | Positioned in window | Standard | Closes loot window |
| LW_LinkAllButton | Positioned in window | Standard | Links all loot to current chat channel (Zeal feature) |
| LW_LootAllButton | Positioned in window | Standard | Loots all items to inventory |

### Sub-Window: LW_LootInvWnd

| Property | Value |
|----------|-------|
| Type | Screen (sub-window container) |
| Contains | All 95 LW_LootSlot elements |
| Purpose | Scrollable loot grid container |

---

## Color Scheme

**Text Colors**:
- **Corpse Name**: RGB(255, 255, 255) - White, centered alignment

**Backgrounds**:
- **Loot Slots**: `A_RecessedBox` template (standard recessed item slot)
- **Item Offset**: ItemOffsetX=2, ItemOffsetY=2 (centers item icons in 40×40 slots)

---

## Technical Notes

- **Resizable Behavior**: Window height adjustable via `Style_Sizable=true`, allowing players to expand view for more simultaneous loot visibility
- **Slot Count**: 95 slots support extremely large corpse loots (far exceeds typical corpse capacity)
- **EQType Mapping**: Loot slots use EQTypes 5000-5094 (game-specific loot inventory range)
- **Background Template**: All slots use `A_RecessedBox` for consistent recessed appearance
- **Item Offset**: 2-pixel offset centers 36×36 item icons within 40×40 slots
- **Scrolling**: LW_LootInvWnd sub-window enables scrolling through full 95-slot list
- **Zeal Button**: "Link All" button is a Zeal client feature, may not function in non-Zeal clients
- **Corpse Name Label**: Positioned at X=210, Y=180 (off-window coordinates suggest overlay or dynamic positioning)
- **No VScroll/HScroll Styles**: Slots have `Style_VScroll=false, Style_HScroll=false`
- **Draw Template**: WDT_RoundedNoTitle provides rounded window without explicit titlebar text area
- **Font**: Default font (no explicit Font property specified)

---

---

## Element Inventory - Detailed

| Element | ScreenID | Position | Size | Type | EQType | Function |
|---------|----------|----------|------|------|--------|----------|
| Loot Window | LootWnd | (0, 0) | 120×470 | Screen | N/A | Main window container |
| Corpse Name | LW_CorpseName | (210, 180) | 100×40 | Label | N/A | Displays "[Name]'s Corpse" name |
| Loot Grid | LW_LootInvWnd | Dynamic | Varies | SubWindow | N/A | Scrollable loot slot container |
| Loot Slots | LW_LootSlot 0-94 | Grid (X=5/50, Y varies) | 40×40 | Slot | 5000-5094 | Individual loot item slots |
| Done Button | LW_DoneButton | Window-relative | Standard | Button | N/A | Close loot interface |
| Link All Button | LW_LinkAllButton | Window-relative | Standard | Button | N/A | Share loot list to chat (Zeal) |
| Loot All Button | LW_LootAllButton | Window-relative | Standard | Button | N/A | Quick-loot all items to inventory |

---

## Loot Item Type Reference

| Item Type | Color Coding | Notes | Rarity |
|-----------|--------------|-------|--------|
| Armor/Clothing | Blues, Greens | Wearable equipment | Varies |
| Weapons | Oranges, Browns | Melee/Ranged weapons, ammo | Varies |
| Spells/Improvements | Purples | Spell scrolls, AA items, augments | Variable |
| Potions/Consumables | Blues, Greens | Healing, buff potions, food | Common |
| Combines | Grays, Browns | Tradeskill components | Variable |
| Artifacts | Golds, Glowing | Unique items, quest items | Rare |
| Currency | Yellows, Golds | Platinum, gems, tribute | Common |
| Books/Lore | Tans, Browns | Lore items, quest notes | Variable |

---

## Technical Implementation Details

- **Resizable Behavior**: Window height adjustable via `Style_Sizable=true`, allowing players to expand view for more simultaneous loot visibility
- **Slot Count**: 95 slots support extremely large corpse loots (far exceeds typical corpse capacity)
- **EQType Mapping**: Loot slots use EQTypes 5000-5094 (game-specific loot inventory range)
- **Background Template**: All slots use `A_RecessedBox` for consistent recessed appearance
- **Item Offset**: 2-pixel offset centers 36×36 item icons within 40×40 slots
- **Scrolling**: LW_LootInvWnd sub-window enables scrolling through full 95-slot list
- **Zeal Button**: "Link All" button is a Zeal client feature, may not function in non-Zeal clients
- **Corpse Name Label**: Positioned at X=210, Y=180 (off-window coordinates suggest overlay or dynamic positioning)
- **No VScroll/HScroll Styles**: Slots have `Style_VScroll=false, Style_HScroll=false`
- **Draw Template**: WDT_RoundedNoTitle provides rounded window without explicit titlebar text area
- **Font**: Default font (no explicit Font property specified)
- **Decay Timer**: Loot items remain until corpse decays (~20-30 minutes typical), slot clearing happens automatically
- **Personal Loot Control**: Players cannot loot items belonging to others (permission-based)

---

This variant represents the compact baseline loot window:
- **Vertical 2-Column Layout**: Minimizes horizontal width (120px) for side-screen placement
- **Resizable Height**: Unlike fixed-size variants, allows vertical expansion
- **Compact Slots**: 40×40 slots keep width minimal while maintaining readability
- **Full Slot Count**: All 95 possible loot slots included (no artificial limitations)
- **Zeal Integration**: Includes Zeal client-specific features (Link All button)
- **Comparison to Large Loot**: "Large Loot" variant likely uses larger slots or different layout
- **Minimal Width**: 120px width designed to not obstruct main gameplay view

---

## Installation

1. Copy `EQUI_LootWnd.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

## Reverting

To switch to other variants:
- **Large Loot**: Copy from `Options/Loot/Large Loot/EQUI_LootWnd.xml` (if available)
- Other loot window variants in sibling directories

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Large Loot](../Large%20Loot/README.md)
