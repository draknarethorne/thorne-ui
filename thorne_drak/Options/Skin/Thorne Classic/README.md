# Skin Window - Slightly Taller and Wider Variant

**File**: [EQUI_LoadskinWnd.xml](./EQUI_LoadskinWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-10
**Status**: ✅ Active variant  
**Author**: Draknare Thorne (based on Infiniti-Blue port)

---
## Purpose

The Slightly Taller and Wider LoadskinWnd variant provides an expanded UI skin selector window with enhanced list display dimensions. This variant offers better browsing of available UI skins with increased vertical space to show more skins at once.

**Key Features**:

- **Expanded List Display**: 128×228px listbox (vs standard 128×180px) for viewing more skins simultaneously
- **Enhanced Vertical Space**: Taller window design reduces scrolling when browsing available UI themes
- **Clear Skin Label**: Centered "Skins" header with Font 5 for better readability
- **Standard Controls**: INI button and list controls consistent with base design
- **Improved Browsing**: Better visibility of skin names without excessive scrolling

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 130 × 290 pixels (approximate) |
| List Display | 128 × 228 pixels |
| List Position | X=1, Y=30 |
| Label Position | X=0, Y=2 |
| Label Size | 130 × 24 pixels |
| Column Width | 118 pixels |

---

## Window Layout

```
┌─────────────────────────────┐
│         Skins              │ ← Label (Font 5, centered)
├─────────────────────────────┤
│ ┌─────────────────────────┐│
│ │ default                 ││ ← Listbox (128×228px)
│ │ duxaUI                  ││   Taller display area
│ │ Infiniti-Blue           ││   Shows more skins
│ │ QQ                      ││   without scrolling
│ │ thorne_drak             ││
│ │ thorne_v0_6_0           ││
│ │ vert                    ││
│ │ zeal                    ││
│ │                         ││
│ │                         ││
│ │                         ││
│ └─────────────────────────┘│
├─────────────────────────────┤
│         [ INI ]            │ ← INI Button
└─────────────────────────────┘
```

---

## Differences from Standard Variant

| Feature | Standard | Slightly Taller and Wider |
|---------|----------|---------------------------|
| **Listbox Height** | 180px | 228px (+48px) |
| **Visible Skins** | ~9-10 | ~12-13 |
| **Window Height** | ~242px | ~290px |
| **Scrolling Required** | More frequent | Less frequent |

---

## Use Cases

**Best For**:
- Players with many custom UI themes installed
- Users who frequently switch between UI skins
- Players who prefer less scrolling when browsing options
- Higher resolution displays where vertical space is available

**Not Ideal For**:
- Players with limited vertical screen space
- Users who prefer minimal window footprints
- Players who only use 1-2 UI skins

---

## Installation

1. Copy `EQUI_LoadskinWnd.xml` to your EverQuest UI directory
2. Reload UI (`/loadskin` or restart client)
3. Open skin selector to see expanded list view

**Compatibility**: Works with all EverQuest TAKP/P2002 clients with UI customization support.

---

## Element Inventory

| Element | ScreenID | Position | Size | Type | Purpose |
|---------|----------|----------|------|------|---------|
| LoadskinWnd | LoadskinWnd | (0, 0) | 130×290 | Screen | Main window container |
| LoadskinLabel | SKINW_SkinLabel | (0, 2) | 130×24 | Label | "Skins" header (Font 5, centered) |
| SkinListbox | SKINW_SkinList | (1, 30) | 128×228 | Listbox | Skin selection list (EXPANDED +48px) |
| INIButton | SKINW_INIButton | (5, 260) | 120×20 | Button | Load INI configuration button |

## Size Modifications (vs Standard)

| Element | Standard | This Variant | Difference | Impact |
|---------|----------|--------------|-----------|--------|
| Window Height | 242px | 290px | +48px | Taller window |
| Listbox Height | 180px | 228px | +48px taller | Shows 2 more skins |
| Listbox Position | (1, 30) | (1, 30) | Same | N/A |
| Window Width | 130px | 130px | Same | No change |

## Technical Details

### Listbox Configuration
```xml
<Listbox item="SKINW_SkinList">
  <Size>
    <CX>128</CX>
    <CY>228</CY>  <!-- +48px taller than standard -->
  </Size>
  <Columns>
    <Width>118</Width>
  </Columns>
  <Style_Border>true</Style_Border>
  <Style_VScroll>true</Style_VScroll>
</Listbox>
```

### Label Configuration
```xml
<Label item="SKINW_SkinLabel">
  <Font>5</Font>
  <Size>
    <CX>130</CX>
    <CY>24</CY>
  </Size>
  <Text>Skins</Text>
  <AlignCenter>true</AlignCenter>
</Label>
```

---

## Variant Comparison

| Feature | Standard | Slightly Taller | Difference |
|---------|----------|-----------------|------------|
| List Display Height | 180px | 228px | +48px |
| Window Total Height | 242px | 290px | +48px |
| Skins Per View | 7-8 | 10-11 | +2-3 visible |
| Scrolling Frequency | More | Less | ~25% reduction |
| Screen Footprint | Minimal | Expanded | Vertical trade-off |

---

## Performance & Compatibility

- **Rendering**: Simple listbox expansion - negligible performance impact on EQ client
- **EverQuest Version**: Works on TAKP and P2002+ servers with UI customization enabled
- **Resolution**: Designed for 800×600 minimum; works on all modern displays (1080p, 1440p, 4K)
- **Backward Compatibility**: Standard variant remains available for limited vertical space scenarios

---

## Known Limitations

- Window size increase is vertical only; width remains fixed at 130px.
- Very long skin names may still truncate in the list box.

---

## Credits

**Based on**: Infiniti-Blue UI port  
**Modified by**: Draknare Thorne (January 2026)  
**Original Design**: EverQuest default UI architecture

---

*This variant recommended for players with 10+ available UI skins and moderate vertical screen space.*

---

## Related Files

- `Options/Skin/Standard/` - Standard LoadskinWnd variant (compact)
- `EQUI_LoadskinWnd.xml` (main) - Main directory skin selector

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial variant with expanded listbox (+48px height) |

---

**Maintainer**: Draknare Thorne  
**Repository**: draknarethorne/thorne-ui
