# Merchant Window - Standard Variant

**File**: [EQUI_MerchantWnd.xml](./EQUI_MerchantWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne

---
## Purpose

The standard Merchant window variant provides a compact vertical vendor interface without integrated inventory display. This baseline implementation focuses on efficient vendor transactions with minimal screen footprint, designed to work alongside separate inventory windows.

**Key Features**:

- **Compact Vertical Layout**: 2-column grid of merchant item slots (80 items maximum)
- **Merchant Name Display**: Centered merchant name label at top
- **Resizable Window**: Adjustable height to show more/fewer vendor items (`Style_Sizable=true`)
- **Selected Item Preview**: Displays currently selected item for purchase/sale
- **Buy/Sell Buttons**: Dedicated transaction buttons
- **No Inventory Integration**: Designed to work with separate inventory window (contrast with "Large Inventory and Bags" variant)
- **Minimal Width**: 125px width for efficient side-screen placement

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 125 × 480 pixels (default, vertically resizable) |
| Resizable | Yes (`Style_Sizable=true`, vertical resize) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | MerchantWnd |
| DrawTemplate | WDT_RoundedNoTitle |
| Default Position | X=0, Y=25 (top-left screen area) |
| Titlebar | Yes (`Style_Titlebar=true`, title: "Merchant") |
| Closebox | Yes (`Style_Closebox=true`) |
| Merchant Slot Count | 80 slots (0-79) in 2-column layout |
| Slot Size | 40×40 pixels each |

---

## Layout Overview

### Window Hierarchy

```text
MerchantWnd (125×480, resizable)
├── MW_MerchantName (merchant NPC name)
├── MW_MerchantSlotsWnd (sub-window containing item grid)
│   ├── MW_MerchantSlot0 (X=5, Y=0)
│   ├── MW_MerchantSlot1 (X=50, Y=0)
│   ├── MW_MerchantSlot2 (X=5, Y=40)
│   ├── MW_MerchantSlot3 (X=50, Y=40)
│   └── ... (continues to MW_MerchantSlot79)
├── MW_SelectedItemLabel (label for selected item)
├── MW_SelectedItem (selected item display)
├── MW_Buy_Button (purchase selected item)
├── MW_Sell_Button (sell selected item)
└── MW_DoneButton (close merchant window)
```

### Merchant Slot Grid Pattern

```text
Column 1 (X=5)   Column 2 (X=50)
[Slot 0]         [Slot 1]        Y=0
[Slot 2]         [Slot 3]        Y=40
[Slot 4]         [Slot 5]        Y=80
[Slot 6]         [Slot 7]        Y=120
[Slot 8]         [Slot 9]        Y=160
  ...
[Slot 78]        [Slot 79]       Y=1560

(80 total slots in 2-column vertical scroll)
```

---

## Key Elements

### Merchant Item Slots

| Element Pattern | Location | Size | EQType Range | Notes |
|-----------------|----------|------|--------------|-------|
| MW_MerchantSlot0-78 (even) | X=5, Y varies | 40×40 | 6000-6078 | Left column (slots 0, 2, 4, ..., 78) |
| MW_MerchantSlot1-79 (odd) | X=50, Y varies | 40×40 | 6001-6079 | Right column (slots 1, 3, 5, ..., 79) |

**Y-Position Formula**:
- **Even slots** (column 1): Y = (slot# / 2) * 40
- **Odd slots** (column 2): Y = ((slot# - 1) / 2) * 40

**Example Positions**:
- Slot 0: X=5, Y=0
- Slot 1: X=50, Y=0
- Slot 20: X=5, Y=400
- Slot 21: X=50, Y=400
- Slot 79: X=50, Y=1560

### Window Components

| Element | Location | Size | EQType/Notes |
|---------|----------|------|-------------|
| MW_MerchantName | X=0, Y=1 | 115×40 | Static label showing merchant NPC name, centered |
| MW_SelectedItemLabel | Positioned below grid | Varies | Label for "Selected Item:" |
| MW_SelectedItem | Below label | Varies | Shows currently selected item for transaction |
| MW_Buy_Button | Bottom area | Standard | Purchases selected item from merchant |
| MW_Sell_Button | Bottom area | Standard | Sells selected inventory item to merchant |
| MW_DoneButton | Bottom area | Standard | Closes merchant window |

### Sub-Window: MW_MerchantSlotsWnd

| Property | Value | Notes |
|----------|-------|-------|
| Type | Screen (sub-window) | Scrollable merchant inventory container |
| Contains | All 80 MW_MerchantSlot elements | Item grid |
| Size | Varies | Dynamically sized based on window height |
| Location | Positioned below merchant name | Top section of window |

---

## Color Scheme

**Text Colors**:
- **Merchant Name**: RGB(255, 255, 255) - White, centered alignment
- **Labels**: RGB(255, 255, 255) - White (default)

**Backgrounds**:
- **Merchant Slots**: `A_RecessedBox` template (standard recessed item slot)
- **Item Offset**: ItemOffsetX=2, ItemOffsetY=2 (centers item icons in 40×40 slots)

---

## Technical Notes

- **Resizable Behavior**: Window height adjustable via `Style_Sizable=true`, allowing view of more merchant inventory simultaneously
- **Slot Count**: 80 slots accommodate large merchant inventories (most merchants have fewer items)
- **EQType Mapping**: Merchant slots use EQTypes 6000-6079 (game-specific merchant inventory range)
- **Background Template**: All slots use `A_RecessedBox` for consistent recessed appearance
- **Item Offset**: 2-pixel offset centers 36×36 item icons within 40×40 slots
- **Scrolling**: MW_MerchantSlotsWnd sub-window provides vertical scrolling through full 80-slot inventory
- **Transaction Flow**: Click item → appears in MW_SelectedItem → click Buy/Sell button
- **Font**: Default font (no explicit Font property in most elements)
- **No VScroll/HScroll Styles**: Individual slots have `Style_VScroll=false, Style_HScroll=false`
- **Merchant Name Width**: 115px label width fits within 125px window (5px margins)
- **Draw Template**: WDT_RoundedNoTitle provides rounded window without prominent titlebar background

---

## Variant Comparison

| Feature | Standard (This) | Large Inventory | Large Inv & Bags |
|---------|-----------------|-----------------|------------------|
| Window Width | 125px | 280px | 400px |
| Has Inventory Tabs | No | Yes | Yes |
| Merchant Slots Only | ✅ Yes | No | No |
| Resizable Height | Yes | Yes | Yes |
| Slot Grid | 2 columns | 2 columns | 3 columns |
| Use Case | Vendor-only | Inv + Merchant | Full UI side-panel |

---

## What Makes This "Standard"

This variant represents the compact baseline merchant window:
- **Vertical 2-Column Layout**: Minimizes horizontal width (125px) for efficient screen placement
- **No Inventory Integration**: Designed to work with separate inventory window (opens side-by-side)
- **Resizable Height**: Allows vertical expansion to view more items without horizontal growth
- **Compact Slots**: 40×40 slots keep width minimal while maintaining item icon readability
- **Full Slot Count**: All 80 possible merchant slots included
- **Comparison to Large Variants**: "Large Inventory and Bags" variant includes integrated inventory tabs, while this is merchant-only
- **Minimal Footprint**: 125px width designed for corner/edge placement without obstructing gameplay
- **Standard Features**: Buy/Sell/Done buttons, selected item preview - no advanced features

---

## Installation

1. Copy `EQUI_MerchantWnd.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

**Note**: Works best with separate inventory window open for buy/sell transactions

## Reverting

To switch to other variants:
- **Large Inventory and Bags**: Copy from `Options/Merchant/Large Inventory and Bags/EQUI_MerchantWnd.xml`
- **Large Inventory**: Copy from `Options/Merchant/Large inventory/EQUI_MerchantWnd.xml`
- Other merchant window variants in sibling directories

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Large Inventory and Bags](../Large%20Inventory%20and%20Bags/README.md), [Large inventory](../Large%20inventory/README.md)
