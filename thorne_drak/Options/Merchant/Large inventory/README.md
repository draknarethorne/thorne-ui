# Merchant Window - Large inventory Variant

**File**: [EQUI_MerchantWnd.xml](./EQUI_MerchantWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-10
**Status**: ✅ Active variant  
**Author**: Draknare Thorne

---
## Purpose

The Large Inventory Merchant window variant provides an expanded vendor interface with larger merchant item display area. This variant focuses on showing more vendor merchandise at once without integrated player inventory, offering efficient vendor browsing with minimal scrolling.

**Key Features**:

- **Large Merchant Display**: Expanded 2-column grid showing more vendor items simultaneously
- **Reduced Scrolling**: Taller window dimension reduces need to scroll through merchant inventory
- **Enhanced Tab System**: Items / Buy / Sell tabs for organized vendor transactions
- **Resizable Window**: Vertically adjustable to show even more items when needed
- **No Inventory Integration**: Designed to work with separate inventory window (contrast with "Large Inventory and Bags" variant)
- **Efficient Browsing**: Larger display area for vendors with extensive stock

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | ~125 × 600+ pixels (vertically resizable) |
| Layout | 2-column vertical grid |
| Maximum Items | 80 merchant slots |
| Tab System | 3 tabs (Items, Buy, Sell) |
| Resizable | ✅ Yes (vertical only) |
| Inventory Integration | ❌ No (separate window) |

---

## Window Layout

```
┌───────────────────────────────┐
│      Merchant Name            │ ← Merchant info header
├───────────────────────────────┤
│ [Items] [Buy] [Sell]          │ ← Tab controls
├───────────────────────────────┤
│ ┌────────┐ ┌────────┐        │
│ │ Item 1 │ │ Item 2 │        │ ← Merchant slot grid
│ └────────┘ └────────┘        │   (2 columns)
│ ┌────────┐ ┌────────┐        │   Large vertical display
│ │ Item 3 │ │ Item 4 │        │   for extensive inventory
│ └────────┘ └────────┘        │
│ ┌────────┐ ┌────────┐        │
│ │ Item 5 │ │ Item 6 │        │
│ └────────┘ └────────┘        │
│ ┌────────┐ ┌────────┐        │
│ │ Item 7 │ │ Item 8 │        │
│ └────────┘ └────────┘        │
│ ...                           │
│ ...                           │   (vertically resizable)
│ ...                           │
├───────────────────────────────┤
│    Selected Item Preview      │ ← Current selection
├───────────────────────────────┤
│      [Buy/Sell Button]        │ ← Transaction controls
└───────────────────────────────┘
```

---

## Differences from Other Merchant Variants

| Feature | Standard | Large Inventory | Large Inventory and Bags |
|---------|----------|-----------------|--------------------------|
| **Height** | ~470px | ~600+px | ~600+px |
| **Width** | 125px | 125px | ~500+px |
| **Merchant Display** | Standard | Large (taller) | Large (taller) |
| **Inventory Integration** | ❌ No | ❌ No | ✅ Yes (side-by-side) |
| **Use Case** | Compact | Browse-heavy | One-stop shopping |

---

## Use Cases

**Best For**:
- Vendors with extensive merchandise (100+ items)
- Players who prefer to see more vendor items at once
- Efficient browsing without constant scrolling
- Players who keep separate inventory window open elsewhere
- Shopping sessions where you browse before buying

**Not Ideal For**:
- Quick vendor transactions (standard is faster)
- Players with limited vertical screen space
- Users who prefer integrated merchant+inventory view

---

## Element Inventory

### Header & Navigation Elements

| Element | ScreenID | Position | Size | Type | Function |
|---------|----------|----------|------|------|----------|
| Merchant Window | LargeMerchantWnd | (0, 0) | 125×600+ | Screen | Main window container |
| Merchant Name | MW_MerchantName | (5, 5) | 115×20 | Label | Display NPC merchant name |
| Tab Controls | MW_TabBox | (2, 25) | 121×30 | TabBox | Items/Buy/Sell tab navigation |
| Items Tab | MW_ItemsTab | (8, 30) | 25×20 | Tab | Browse available merchant items |
| Buy Tab | MW_BuyTab | (35, 30) | 20×20 | Tab | Review previous purchases |
| Sell Tab | MW_SellTab | (58, 30) | 20×20 | Tab | Manage vendor buybacks |

### Merchant Slot Grid (2-Column Layout)

| Element Pattern | Position | Size | Count | Function |
|-----------------|----------|------|-------|----------|
| MW_MerchantSlot 0-79 (even) | X=5, Y varies | 40×40 | 40 slots | Left column merchant items |
| MW_MerchantSlot 1-79 (odd) | X=50, Y varies | 40×40 | 40 slots | Right column merchant items |

**Y-Position Formula** (starting Y=55):
- Slot N: Y = 55 + ((N / 2) × 40)  
- Example: Slot 0 at Y=55, Slot 2 at Y=95, Slot 10 at Y=255, Slot 40 at Y=855

### Selection & Transaction Elements

| Element | ScreenID | Position | Size | Function |
|---------|----------|----------|------|----------|
| Selected Item Display | MW_SelectedItem | Dynamic | Auto | Shows item preview/details |
| Buy/Sell Button | MW_TransactButton | Bottom-center | Standard | Execute transaction (context-dependent) |
| Close/Done Button | MW_DoneButton | Bottom-right | Standard | Close merchant window |

---

## Technical Notes - Large Inventory Variant

- **Extended Height**: 600px default (vs 470px Standard) creates larger browsable area
- **Same Width**: 125px maintained for consistent side-screen placement
- **Tab System**: Items/Buy/Sell tabs match standard merchant UI conventions
- **Item Count**: 80 total slots in 2-column grid (same as Standard)
- **Scrolling Efficiency**: Larger window shows ~10-11 visible slots vs 6-7 in Standard
- **Slot Spacing**: Same 40×40 formatting as Standard variant
- **Vertical Resizability**: `Style_Sizable=true` allows even more expansion for extensive vendors
- **Integration Philosophy**: Remains separate from inventory (unlike "Large Inventory and Bags" variant)
- **Visual Consistency**: Matches Standard merchant window styling/appearance

---

## Variant Comparison Matrix

| Aspect | Standard | Large Inventory | Large Inv & Bags |
|--------|----------|-----------------|------------------|
| Display Area | 470px tall | 600+px tall | 600+px tall |
| Visible Slots | 6-7 per view | 10-11 per view | 10-11 per view |
| Scrolling Needed | More | Less | Less |
| Inventory Tabs | None | None | Yes (integrated) |
| Typical Use | Quick shops | Long browsing | One-stop |

---

## Installation

1. Copy `EQUI_MerchantWnd.xml` to your EverQuest UI directory
2. Reload UI (`/loadskin` or restart client)
3. Open merchant window to see expanded vendor display

**Compatibility**: Works with all EverQuest TAKP/P2002 clients with UI customization support.

---

## Workflow Recommendations

### Efficient Shopping Workflow
1. Open merchant window (large vendor display)
2. Position inventory window separately (right side or top corner)
3. Browse merchant items with minimal scrolling
4. Click items to select, see preview in bottom section
5. Use Buy/Sell buttons for transactions
6. Resize vertically if needed to see even more items

### Window Positioning Tips
- **Merchant**: Left or center screen (takes minimal horizontal space)
- **Inventory**: Right side or top-right (separate window)
- **Container**: Center or bottom (for quick access during shopping)

---

## Technical Details

### Window Configuration
- Vertically resizable (`Style_Sizable=true`)
- Fixed width (125px) maintains compact horizontal footprint
- 2-column merchant slot grid maximizes vertical efficiency
- Tab system separates Items/Buy/Sell for organization

### Tab System
- **Items Tab**: Shows all merchant inventory
- **Buy Tab**: Focus on purchasing workflow
- **Sell Tab**: Focus on selling player items

---

## Credits

**Author**: Draknare Thorne (January 2026)  
**Original Design**: EverQuest default merchant interface  
**Tab System**: Thorne UI 3-tab redesign

---

## Related Files

- `Options/Merchant/Standard/` - Compact merchant window (~470px height)
- `Options/Merchant/Large Inventory and Bags/` - Integrated merchant+inventory+bags view
- `EQUI_MerchantWnd.xml` (main) - Main directory merchant window

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Large vertical merchant display variant created |

---

**Maintainer**: Draknare Thorne  
**Repository**: draknarethorne/thorne-ui
