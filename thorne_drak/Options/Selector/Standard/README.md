# Selector Window - Standard Variant

**File**: [EQUI_SelectorWnd.xml](./EQUI_SelectorWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Baseline horizontal layout  
**Author**: Draknare Thorne

---
## Purpose

The Window Selector displays a toolbar of quick-toggle buttons for accessing key UI windows. Each button provides toggle access to a major player interface function, allowing rapid access to critical windows during gameplay.

**Key Features**:

- **Quick Window Access**: Single-click toggles for 9 major UI functions
- **Persistent Toolbar**: Always accessible without keybind interference
- **Visual Feedback**: Checkbox-style buttons show current toggle state
- **Tooltips**: Hover tooltips identify each button function
- **Framerate-Friendly**: Minimal overhead, lightweight integration

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 278 × 50 pixels (horizontal layout) |
| Layout Orientation | **Horizontal** (left-to-right) |
| Button Count | 9 buttons |
| Button Size | 26 × 26 pixels each |
| Button Spacing | 30 pixels (6px gap between buttons) |
| Starting Position | X=135, Y=0 (top-center of screen) |
| Resizable | No |
| Sizable | No |
| Titlebar | Yes |
| Closebox | No |
| Minimizebox | No |

---

## Button Layout

### Current (v1.0.0 - Horizontal)

```
┌────────────────────────────────────────────┐
│ Window Selector                            │
├────────────────────────────────────────────┤
│ A  I  O  F  H  S  P  B  ?                 │
└────────────────────────────────────────────┘
(Left to right, Y=0, X incrementing by 30)
```

### Button Order

| Position | X | Button | Function | Tooltip |
|----------|---|--------|----------|---------|
| 1 | 0 | SELW_ActionsToggleButton | Access/toggle Actions window | Actions |
| 2 | 30 | SELW_InventoryToggleButton | Access/toggle Inventory window | Inventory |
| 3 | 60 | SELW_OptionsToggleButton | Access/toggle Options window | Options |
| 4 | 90 | SELW_FriendsToggleButton | Access/toggle Friends window | Friends |
| 5 | 120 | SELW_HotboxToggleButton | Access/toggle Hotbuttons bar | Hotbuttons |
| 6 | 150 | SELW_CastSpellToggleButton | Access/toggle Spell book | Spells |
| 7 | 180 | SELW_PetInfoToggleButton | Access/toggle Pet Info window | Pet Info |
| 8 | 210 | SELW_BuffToggleButton | Access/toggle Effects/Buffs window | Effects |
| 9 | 240 | SELW_HelpToggleButton | Access/toggle Help window | Help |

---

## Technical Specifications

### Button Properties (All Buttons)

- **Type**: Checkbox-style toggle button
- **Size**: 26 × 26 pixels (square)
- **RelativePosition**: true (positioned relative to parent)
- **Style_Checkbox**: true (maintains pressed/unpressed state)
- **Button States**: 
  - Normal: default appearance
  - Pressed: highlighted/toggled appearance
  - Flyby: hover appearance
  - PressedFlyby: hover while pressed
  - Disabled: greyed-out (unused - buttons never disabled)

### Window Properties

**Screen Item: SelectorWindow**

```
Location: X=135, Y=0 (top of screen, centered)
Size: 278 × 50px (wide and short for horizontal buttons)
Style Elements:
  - Titlebar: Enabled (shows "Window Selector" title)
  - Closebox: Disabled
  - Minimizebox: Disabled
  - Border: Enabled
  - Sizable: Disabled (fixed size)
  - DrawTemplate: WDT_Rounded (rounded corners)
```

---

## Element Inventory

| Element | ScreenID | Position | Size | Type | Purpose |
|---------|----------|----------|------|------|---------|
| SelectorWindow | N/A | (135, 0) | 278×50 | Container | Main window frame |
| ActionsToggleButton | SELW_ActionsToggleButton | (2, 16) | 26×26 | Button | Toggle Actions window |
| InventoryToggleButton | SELW_InventoryToggleButton | (32, 16) | 26×26 | Button | Toggle Inventory window |
| OptionsToggleButton | SELW_OptionsToggleButton | (62, 16) | 26×26 | Button | Toggle Options (Alt+O) |
| FriendsToggleButton | SELW_FriendsToggleButton | (92, 16) | 26×26 | Button | Toggle Friends window |
| HotboxToggleButton | SELW_HotboxToggleButton | (122, 16) | 26×26 | Button | Toggle Hotbuttons |
| CastSpellToggleButton | SELW_CastSpellToggleButton | (152, 16) | 26×26 | Button | Toggle Spell book |
| PetInfoToggleButton | SELW_PetInfoToggleButton | (182, 16) | 26×26 | Button | Toggle Pet Info |
| BuffToggleButton | SELW_BuffToggleButton | (212, 16) | 26×26 | Button | Toggle Effects/Buffs |
| HelpToggleButton | SELW_HelpToggleButton | (242, 16) | 26×26 | Button | Toggle Help window |

---

## Usage

Each button toggles its associated window on/off. Click once to show, click again to hide.

**Keyboard Alternative**: Most windows have keybinds accessible through `Options > Hotkeys`

**Positioning**: Window selector appears at top-center of screen by default. Can be moved by dragging the titlebar.

---

## Configuration

To use this variant:

```bash
EverQuest/
├── UIFILES/
│   └── thorne_drak/
│       └── Options/
│           └── Selector/
│               └── Standard/
│                   ├── EQUI_SelectorWnd.xml
│                   └── README.md
```

Load with:
```
/loadskin thorne_drak
```

---

## Alternative Layouts

### Vertical Layout Variant

A vertical orientation variant is now available that features:

- **Window size**: 38 × 278px (tall and narrow)
- **Button positioning**: X=2, Y incrementing by 30 (2, 32, 62, 92... 242)
- **No titlebar**: Streamlined WDT_RoundedNoTitle design
- **Closebox enabled**: Easy window management
- **Use case**: Players preferring vertical toolbar layout or with limited horizontal screen space

See [Window Selector - Vertical](../Vertical/README.md) for full details.

---

## Testing Recommendations

1. Load UI: `/loadskin thorne_drak`
2. Verify each button:
   - Appears in correct position
   - Shows tooltip on hover
   - Toggles associated window on/off
   - Visual feedback shows pressed/unpressed state
3. Check positioning:
   - Window appears at top-center
   - All 9 buttons visible without overlap
   - Window can be moved by dragging title
4. Test window state persistence:
   - Toggle windows closed
   - Reload UI or zone
   - Verify button states are preserved

---

## Modification History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 3, 2026 | Initial Standard selector window (horizontal layout) |

---

## See Also

- [Options Directory Overview](../../README.md)
- [Window Selector - Vertical](../Vertical/README.md) (Vertical layout)

---

*Last Updated: February 3, 2026*  
*Author: Draknare Thorne*  
*Status: Baseline established - Ready for vertical variant development*
