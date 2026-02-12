# Item Display Analysis: Nillipuss vs. Thorne

## High-Level Differences Summary

The most significant difference regarding item display is the absence of a dedicated `EQUI_ItemDisplay.xml` or `EQUI_ItemDisplayWindow.xml` file in the Nillipuss UI.

*   **Nillipuss**: Does not use a separate window for item display. Instead, item details are shown in a tooltip that appears when the user hovers over an item in their inventory or other windows. This is the default behavior for EverQuest if no custom item display window is specified.
*   **Thorne UI**: Utilizes a custom `EQUI_ItemDisplay.xml` file. This creates a dedicated, persistent window that displays the details of an item when it is right-clicked. This window can be moved, resized, and kept open for reference, which is a significant departure from the transient nature of tooltips.

This represents a fundamental difference in how users interact with and view item information.

## Layout/Positioning Analysis

### Nillipuss Layout (Tooltip)

Nillipuss relies on the default engine-driven tooltip for item information. The layout is not defined by XML but by the game engine itself. It typically looks like this:

```
(Appears on hover near the cursor)
┌──────────────────────────┐
│ Item Name                │
│ [Item Stats]             │
│ [Classes/Races]          │
│ [Effect Information]     │
│ ...                      │
└──────────────────────────┘
```

### Thorne UI Layout (Dedicated Window)

Thorne UI provides a dedicated window, allowing the information to persist on screen.

```
┌──────────────────────────┐
│ [ Window Titlebar ] [X]  │
├──────────────────────────┤
│ ┌──────┐ ┌─────────────┐ │
│ │      │ │ Item Name   │ │
│ │ ICON │ │ [Stats]     │ │
│ │      │ │ [Classes]   │ │
│ └──────┘ │ ...         │ │
│          └─────────────┘ │
│                          │
└──────────────────────────┘
```

## Element-by-Element Comparison

| Feature | Nillipuss | Thorne UI | Analysis |
| :--- | :--- | :--- | :--- |
| **Dedicated Window** | **No** | **Yes** | Major functional difference. Nillipuss uses tooltips. |
| **Persistence** | Transient (on hover) | Persistent (on right-click) | Thorne allows for item comparison and reference. |
| **XML File** | `(none)` | `EQUI_ItemDisplay.xml` | Nillipuss omits the file to force default tooltip behavior. |
| **Content Display** | `STMLbox` (in tooltip) | `STMLbox` (in window) | Both use the same underlying element type to render the text. |
| **Item Icon** | Part of tooltip | `IDW_IconButton` in window | Thorne UI gives the icon a dedicated spot in the window. |

---

## EQType Validation

No EQType-bound `Label` or `Gauge` elements were detected in either file. The item data is rendered via `STMLbox` and engine-driven formatting, so EQType comparison is not applicable here.

## Feature Additions/Removals

*   **Nillipuss Additions/Removals**:
    *   By **removing** the `EQUI_ItemDisplayWindow.xml` file, Nillipuss intentionally reverts to the default tooltip-based item inspection. This is a design choice to keep the UI less cluttered with persistent windows.

*   **Thorne UI Additions/Removals**:
    *   The **addition** of `EQUI_ItemDisplay.xml` is a significant feature. It provides a draggable, sizable, and persistent window for item details, which is a common feature in modern MMO UIs and many popular EQ UIs.
    *   The window is composed of an `STMLbox` for the text and a `Button` for the icon, which is standard for this file.

## Stat-Icons Relevance

*   The existence of a dedicated item display window in Thorne UI has little direct impact on the stat-icons project for the inventory itself.
*   However, it reinforces the design philosophy of Thorne UI to provide clear, persistent information sources. The item window is where a user would go for full, detailed text about an item's stats. This supports the idea of using icons in the inventory for a quick glance, with the full details being available in this separate window.
*   If stat-icons were ever to be implemented *within* the item display window itself (e.g., replacing "STR: +5" with a strength icon and "+5"), the Thorne UI's dedicated window would be the place to do it.
