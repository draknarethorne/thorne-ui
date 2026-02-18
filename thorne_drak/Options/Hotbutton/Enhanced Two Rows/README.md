# Hotbutton Window - Enhanced Two Rows Variant

**File**: [EQUI_HotButtonWnd.xml](./EQUI_HotButtonWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-10
**Status**: ✅ Multi-row variant with inventory integration  
**Author**: Draknare Thorne (based on Daciana/Brujoloco mods)

---
## Purpose

The Two Rows variant combines a dual-row hotbar (20 visible buttons) with integrated inventory tabs, providing quick access to abilities and equipment in a consolidated interface. This reduces window clutter by combining hotbar and inventory functionality.

**Key Features**:

- **Two-Row Hotbar Layout**: 20 hotbar buttons visible (2 rows × 10 buttons)
- **Vertical Page Navigation**: Up/down arrows for switching between hotbar pages
- **Integrated Inventory Tabs**: Quick access to inventory, bags, bank, and spell gems
- **Consolidated Interface**: Single window replaces separate hotbar and inventory windows
- **Extended Width**: 870×90 pixels to accommodate dual-row display + inventory tabs
- **Client Limitation**: Only buttons 1-10 are fully functional (EQ client hardcoding)

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 870 × 90 pixels (resizable) |
| Resizable | Yes (`Style_Sizable=true`) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | HotButtonWnd |
| DrawTemplate | WDT_Rounded |
| Default Position | X=0, Y=230 (bottom-center screen area) |
| Titlebar | Yes (`Style_Titlebar=true`, title: "Hot Buttons") |
| Closebox | Yes (`Style_Closebox=true`) |
| Visible Buttons | 20 (rows 1-2, buttons 1-10 each) |
| Functional Buttons | 10 (buttons 1-10 first row only) |
| Total Pages | 10 (100 button capacity total) |

---

## Layout Overview

### Window Hierarchy

```text
HotButtonWnd (870×90, resizable)
├── Row 1: HB_Button1-10 (X=2 to X=380, Y=2)
├── Row 2: HB2_Button1-10 (X=2 to X=380, Y=44)
├── Row 3: HB3_Button1-10 (decorative, non-functional)
├── Row 4: HB4_Button1-10 (decorative, non-functional)
├── Page Navigation (right side, vertical)
│   ├── HB_PageLeftButton (up arrow)
│   ├── HB_CurrentPageLabel (page number)
│   └── HB_PageRightButton (down arrow)
├── HB_InvSlot1-10 (inventory quick slots for each row)
├── HB2_InvSlot1-10
├── HB3_InvSlot1-10
└── HB4_InvSlot1-10
```

### Two-Row Button Layout

```text
Row 1:  [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]   [▲]
Row 2: [11][12][13][14][15][16][17][18][19][20]   [#]
(Rows 3-4 displayed but non-functional)           [▼]
```

---

## Key Elements

### Hotbar Buttons - Row 1 (Functional)

| Element | Location | Size | Notes |
|---------|----------|------|-------|
| HB_Button1-10 | Y=2, X=2 to 380 | 40×40 each | **Fully functional** - standard EQ hotbar |

### Hotbar Buttons - Row 2 (Display Only)

| Element | Location | Size | Notes |
|---------|----------|------|-------|
| HB2_Button1-10 | Y=44, X=2 to 380 | 40×40 each | **Visual only** - client limitation prevents functionality |

### Hotbar Buttons - Rows 3-4 (If present)

| Element | Location | Notes |
|---------|----------|-------|
| HB3_Button1-10, HB4_Button1-10 | Additional rows | **Decorative only** - not executed by client |

### Page Navigation (Vertical)

| Element | Location | Size | Function |
|---------|----------|------|----------|
| HB_PageLeftButton | X=420, Y=2 | 12×10 | Previous page (up arrow, uses A_VSBUpNormal template) |
| HB_CurrentPageLabel | X=412, Y=15 | 25×16 | Displays current page (1-10) |
| HB_PageRightButton | X=420, Y=28 | 12×10 | Next page (down arrow, uses A_VSBDownNormal template) |

### Inventory Integration

| Element Set | Count per Row | Purpose |
|-------------|---------------|----------|
| HB_InvSlot1-10 | 10 | Quick inventory slots for row 1 |
| HB2_InvSlot1-10 | 10 | Quick inventory slots for row 2 |
| HB3_InvSlot1-10 | 10 | Quick inventory slots for row 3 |
| HB4_InvSlot1-10 | 10 | Quick inventory slots for row 4 |

---

## Color Scheme

**Text Colors**:
- **Button Text**: RGB(255, 255, 255) - White
- **Page Number**: RGB(255, 255, 255) - White

**Button Templates**:
- **Action Buttons**: `A_SquareBtnNormal` series (Normal/Pressed/Flyby/Disabled/PressedFlyby)
- **Navigation**: `A_VSBUpNormal` and `A_VSBDownNormal` for vertical arrows

---

## Technical Notes

- **Button Spacing**: Horizontal buttons spaced at +42px increments (40px button + 2px gap)
- **Row Spacing**: Rows placed at Y=2, Y=44 (+42px vertical spacing)
- **DecalSize**: Each button has DecalSize 40×40 for ability icons
- **Font**: Font 2 used for window title, Font 1 for button labels
- **Page System**: 10 pages × 10 buttons = 100 total button capacity (per row)
- **Navigation Change**: Uses **vertical arrows** (VSBUp/VSBDown) instead of horizontal (HSBLeft/HSBRight)
- **Relative Positioning**: All child elements use relative positioning
- **Window Width**: 870px accommodates button rows + navigation + potential tab areas

### ⚠️ Critical Limitation: Client Hardcoding

**Only buttons 1-10 are fully functional** due to EverQuest client limitations:
- **Row 1 (HB_Button1-10)**: ✅ **Functional** - clicks execute assigned actions
- **Row 2 (HB2_Button11-20)**: ❌ **Visual Only** - buttons display but don't execute actions when clicked
- **Rows 3-4**: ❌ **Decorative** - purely cosmetic, no functionality

**Why This Limitation Exists**:
- The EverQuest client is hardcoded to only respond to hotbar buttons 1-10
- Additional button rows can be *displayed* in the UI, but the game engine won't process clicks on buttons 11+
- This is a **client-side limitation**, not a UI bug
- Multi-row displays are useful for *visual reference* (seeing multiple button pages simultaneously) but don't grant access to additional executable buttons

**Workaround**: Players must use page navigation to cycle button 1-10 assignments

---

## Comparison: Standard vs Two Rows Inventory and Bags

| Feature | Standard (Single Row) | Two Rows Inv & Bags | Difference |
|---------|----------------------|---------------------|-------------|
| Window Width | 440px | 870px | +430px wider |
| Window Height | 66px | 90px | +24px taller |
| Visible Buttons | 10 | 20 | +10 buttons (visual) |
| Functional Buttons | 10 | 10 | Same (EQ limitation) |
| Inventory Integration | No | Yes | Consolidated UI |
| Page Navigation | Horizontal ←→ | Vertical ↑↓ | Different layout |
| Use Case | Compact hotbar | Full-featured toolbar | Extended interface |
| Screen Footprint | Minimal height | Extended width | Trade-off: width for visibility |

## What Makes This "Two Rows Inventory and Bags"

This variant represents the integrated multi-row design:
- **Dual-Row Display**: Shows buttons 1-20 simultaneously (though only 1-10 functional)
- **Inventory Integration**: Combines hotbar with inventory quick-access slots
- **Consolidated Interface**: Single window replaces separate hotbar + inventory
- **Extended Width**: 870px (almost 2x the 440px standard hotbar) for comprehensive display
- **Vertical Navigation**: Up/down arrows match multi-row vertical layout
- **Comparison to Standard**: Standard variant is 440×66 (single row, no inventory tabs), this is 870×90
- **Comparison to Four Rows**: Four-row variant extends to even more rows (all still limited to buttons 1-10 functionality)
- **Visual Benefit**: See multiple button pages at once for quick reference, even if execution requires page switching

---

## Client Limitations & Design Tradeoffs

The EverQuest (2002) client hardcodes hotbar functionality to buttons 1-10 only. This variant displays rows 2-4 buttons visually for reference and future customization, but they cannot execute actions. This is an engine constraint, not a UI limitation. Consider the Standard variant if you prefer minimal visual clutter, or use this variant if you appreciate the extended page-at-a-glance reference.

---

## Installation

1. Copy `EQUI_HotButtonWnd.xml` from this directory to `thorne_drak/` directory (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Window will reload with this variant

**Note**: Remember that only buttons 1-10 will execute actions when clicked

## Reverting

To switch to other variants:
- **Standard Single Row**: Copy from `Options/Hotbutton/Standard/EQUI_HotButtonWnd.xml`
- **Four Rows**: Copy from `Options/Hotbutton/Four Rows Inventory and Bags/EQUI_HotButtonWnd.xml`
- Other variants available in sibling directories

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Standard](../Standard/README.md), [Four Rows Inventory and Bags](../Four%20Rows%20Inventory%20and%20Bags/README.md)  
**Known Limitation**: ⚠️ Only buttons 1-10 are functionally clickable due to EQ client hardcoding
