# Hotbutton Window - Standard Variant

**File**: [EQUI_HotButtonWnd.xml](./EQUI_HotButtonWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-10
**Status**: ✅ Standard variant  
**Author**: Draknare Thorne (based on Daciana/Brujoloco mods)

---
## Purpose

The standard Hotbutton window variant provides a clean single-row hotbar displaying buttons 1-10 with page navigation. This is the baseline implementation for players who prefer a compact hotbar separate from inventory integration.

**Key Features**:

- **Single Row Layout**: 10 hotbar buttons (40×40 each) in a horizontal row
- **Page Navigation**: Left/right arrows for switching between hotbar pages (10 pages total, 100 button capacity)
- **Current Page Indicator**: Centered page number display
- **Compact Footprint**: 440×66 pixels - narrow horizontal bar
- **Separate from Inventory**: Designed to work alongside separate Inventory and Spell Gem windows
- **Quick-Access Slots**: Additional quick slots for inventory items and spell gems

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 440 × 66 pixels (fixed) |
| Resizable | No (`Style_Sizable=false`) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | HotButtonWnd |
| DrawTemplate | WDT_Rounded |
| Default Position | X=0, Y=230 (bottom-center screen area) |
| Titlebar | Yes (`Style_Titlebar=true`, title: "Hot Buttons") |
| Closebox | Yes (`Style_Closebox=true`) |
| Button Count | 10 visible (buttons 1-10) |
| Total Pages | 10 (100 total button capacity) |

---

## Layout Overview

### Window Hierarchy

```text
HotButtonWnd (440×66)
├── HB_Button1 (X=2, Y=2, 40×40)
├── HB_Button2 (X=44, Y=2, 40×40)
├── HB_Button3 (X=86, Y=2, 40×40)
├── HB_Button4 (X=128, Y=2, 40×40)
├── HB_Button5 (X=170, Y=2, 40×40)
├── HB_Button6 (X=212, Y=2, 40×40)
├── HB_Button7 (X=254, Y=2, 40×40)
├── HB_Button8 (X=296, Y=2, 40×40)
├── HB_Button9 (X=338, Y=2, 40×40)
├── HB_Button10 (X=380, Y=2, 40×40)
├── Page Navigation (right side)
│   ├── HB_PageLeftButton (X=420, Y=2)
│   ├── HB_CurrentPageLabel (X=412, Y=15)
│   └── HB_PageRightButton (X=420, Y=28)
├── HB_InvSlot1-10 (quick inventory slots)
└── HB_SpellGem1-10 (quick spell gem slots)
```

### Button Layout

```text
[1] [2] [3] [4] [5] [6] [7] [8] [9] [10]  [▲]
                                          [#]
                                          [▼]
```

---

## Key Elements

### Hotbar Buttons

| Element | Location | Size | Notes |
|---------|----------|------|-------|
| HB_Button1 | X=2, Y=2 | 40×40 | First hotbar button (top-left) |
| HB_Button2 | X=44, Y=2 | 40×40 | Second button (+42px X offset per button) |
| HB_Button3-10 | Continues +42px | 40×40 | Horizontal row, 2px spacing |

### Page Navigation

| Element | Location | Size | Function |
|---------|----------|------|----------|
| HB_PageLeftButton | X=420, Y=2 | 10×12 | Previous page (uses A_HSBLeftNormal template) |
| HB_CurrentPageLabel | X=412, Y=15 | 25×16 | Displays current page number (1-10) |
| HB_PageRightButton | X=420, Y=28 | 10×12 | Next page (uses A_HSBRightNormal template) |

### Quick Access Slots

| Element | Type | Count | Notes |
|---------|------|-------|-------|
| HB_InvSlot1-10 | InvSlot | 10 | Quick inventory item slots |
| HB_SpellGem1-10 | SpellGem | 10 | Quick spell casting slots |

---

## Color Scheme

**Text Colors**:
- **Button Text**: RGB(255, 255, 255) - White (button numbers and labels)
- **Page Number**: RGB(255, 255, 255) - White

**Button Templates**:
- Uses `A_SquareBtnNormal` series for button states (Normal/Pressed/Flyby/Disabled/PressedFlyby)
- Navigation uses `A_HSBLeftNormal` and `A_HSBRightNormal` for directional arrows

---

## Element Inventory

### Hotbar Buttons (Row 1 - Primary)

| Element | ScreenID | EQType | Position | Size | Function |
|---------|----------|--------|----------|------|----------|
| Button 1 | HB_Button1 | Hotkey 1 | (2, 2) | 40×40 | First hotbar ability slot (page-based) |
| Button 2 | HB_Button2 | Hotkey 2 | (44, 2) | 40×40 | Second hotbar ability slot |
| Button 3 | HB_Button3 | Hotkey 3 | (86, 2) | 40×40 | Third hotbar ability slot |
| Button 4 | HB_Button4 | Hotkey 4 | (128, 2) | 40×40 | Fourth hotbar ability slot |
| Button 5 | HB_Button5 | Hotkey 5 | (170, 2) | 40×40 | Fifth hotbar ability slot |
| Button 6 | HB_Button6 | Hotkey 6 | (212, 2) | 40×40 | Sixth hotbar ability slot |
| Button 7 | HB_Button7 | Hotkey 7 | (254, 2) | 40×40 | Seventh hotbar ability slot |
| Button 8 | HB_Button8 | Hotkey 8 | (296, 2) | 40×40 | Eighth hotbar ability slot |
| Button 9 | HB_Button9 | Hotkey 9 | (338, 2) | 40×40 | Ninth hotbar ability slot |
| Button 10 | HB_Button10 | Hotkey 10 | (380, 2) | 40×40 | Tenth hotbar ability slot (rightmost) |

### Page Navigation Elements

| Element | ScreenID | EQType | Position | Size | Function |
|---------|----------|--------|----------|------|----------|
| Page Left | HB_PageLeftButton | — | (420, 2) | 10×12 | Previous page arrow (up/left chevron) |
| Page Indicator | HB_CurrentPageLabel | — | (412, 15) | 25×16 | Current page number display (1-10) |
| Page Right | HB_PageRightButton | — | (420, 28) | 10×12 | Next page arrow (down/right chevron) |

### Quick Slots Element Details

| Element | ScreenID | Type | Position | Size | Count | Function |
|---------|----------|------|----------|------|-------|----------|
| Inv Slots | HB_InvSlot1-10 | InvSlot | Varies | 40×40 | 10 | Per-button inventory quick access |
| Spell Gems | HB_SpellGem1-10 | SpellGem | Varies | 40×40 | 10 | Per-button spell gem quick slots |

---

## Variant Comparison: Standard vs Multi-Row

| Feature | Standard (This) | Two Rows | Four Rows |
|---------|-----------------|----------|-----------|
| Window Width | 440px | 870px | 1200px |
| Window Height | 66px | 90px | 132px |
| Visible Buttons | 10 | 20 | 40 |
| Functional Buttons | 10 | 10 | 10 |
| Page Navigation | Horizontal (←→) | Vertical (↑↓) | Vertical (↑↓) |
| Inventory Integration | No | Yes | Yes |
| Use Case | Compact bar | Multi-row toolbar | Extended feature bar |
| Screen Footprint | Minimal | Extended width | Maximum |

---

## Technical Notes

- **Button Spacing**: Buttons positioned with 2-pixel gaps (X increments of 42 for 40px buttons)
- **DecalSize**: Each button has DecalSize 40×40 for ability icons/graphics
- **Font**: Font 1 used for button labels and page number
- **Page System**: 10 pages × 10 buttons = 100 total hotbar button capacity
- **Client Limitation**: Only buttons 1-10 on current page are functionally active, multi-row displays don't grant access to buttons 11+
- **Button Templates**: Standard square button templates with 5 states for full visual feedback
- **Quick Slots**: Inventory and spell gem slots provide rapid access without opening full windows
- **Window Title**: "Hot Buttons" displayed in titlebar
- **Relative Positioning**: All child elements use relative positioning within window frame

---

## What Makes This "Standard"

This variant represents the classic single-row hotbar design:
- **Single Row**: Unlike multi-row variants, displays only one row of 10 buttons
- **No Inventory Integration**: Separate from inventory tabs (contrast with "Two Rows Inventory and Bags" variant)
- **Compact Width**: 440px width designed to sit at screen bottom without obstruction
- **Traditional Layout**: Matches classic EverQuest hotbar expectations
- **Page-Based Navigation**: Uses page switching rather than vertical button rows
- **Minimal Height**: 66px height leaves maximum screen space for gameplay view
- **Reference Implementation**: Multi-row variants build upon this baseline structure

---

## Installation

1. Copy `EQUI_HotButtonWnd.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

## Reverting

To switch to other variants:
- **Two Rows Inventory and Bags**: Copy from `Options/Hotbutton/Two Rows Inventory and Bags/EQUI_HotButtonWnd.xml`
- **Four Rows Inventory and Bags**: Copy from `Options/Hotbutton/Four Rows Inventory and Bags/EQUI_HotButtonWnd.xml`
- Other multi-row variants available in sibling directories

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Two Rows Inventory and Bags](../Two%20Rows%20Inventory%20and%20Bags/README.md), [Four Rows Inventory and Bags](../Four%20Rows%20Inventory%20and%20Bags/README.md)
