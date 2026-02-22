# Player Window - AA and XP Bottom Variant

**File**: [EQUI_PlayerWindow.xml](./EQUI_PlayerWindow.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-17
**Status**: ✅ Active (First Draft Implementation)  
**Author**: Draknare Thorne

---
## Purpose

The AA and XP Bottom Player Window variant features a completely redesigned player interface with AA (Alternate Advancement) and Experience gauges positioned at the bottom of the window. This layout combines visual elements from multiple UI designs to create an enhanced, information-dense character display.

**Design Philosophy**:
- **Infiniti-Blue gauges** - Custom gauge textures and styling from Infiniti-Blue community UI
- **duxaUI/vert icon methodology** - Class/race icon integration
- **vert stats layout** - Vertical stat arrangement for efficient space usage

**Key Features**:

- **Bottom-Positioned AA/XP Gauges**: AA and Experience bars anchored at window bottom
- **Custom Gauge Graphics**: Red (HP), Blue (Mana), Gray (Stamina), Green (XP), Yellow (AA) with matching empty states
- **Enhanced Visual Presentation**: Thorne UI gauge textures (`window_pieces03.tga`, `window_pieces04.tga`)
- **Information Density**: Comprehensive stat display in organized vertical layout
- **Class/Race Icons**: Visual character identification elements
- **Compact Footprint**: Efficient screen space usage with maximum information display

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | ~160 × 300+ pixels |
| Gauge Types | HP, Mana, Stamina, Experience, AA |
| Layout Style | Vertical stats with bottom-positioned progress bars |
| Gauge Height | 12px (standard Thorne UI gauge height) |
| Gauge Width | 120px |
| Status | First Draft Implementation |

---

## Window Layout

```
┌─────────────────────────────────┐
│   [Class Icon]  Character Name  │ ← Header with icon/name
├─────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓░░░░  1250/2000 HP  │ ← HP Gauge (red)
│ ▓▓▓▓▓▓▓▓░░░░░░░░   850/1200 MP │ ← Mana Gauge (blue)
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░   950/1000 ST │ ← Stamina Gauge (gray)
├─────────────────────────────────┤
│ Level: 60          AC: 1250     │ ← Stats section
│ STR: 180    INT: 120            │   (vertical layout)
│ STA: 165    WIS: 135            │
│ AGI: 155    CHA: 80             │
│ DEX: 142                        │
├─────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓░░░░░░  65% XP        │ ← Experience (green) - BOTTOM
│ ▓▓▓▓▓▓▓░░░░░░░░░░  42% AA       │ ← AA Points (yellow) - BOTTOM
└─────────────────────────────────┘
```

---

## Gauge System Details

### Custom Gauge Textures

All gauges use modular gauge patterns from `Infiniti-Blue` with custom adaptations:

| Gauge Type | Full Texture | Empty Texture | Color |
|------------|--------------|---------------|-------|
| **HP** | `window_pieces03.tga` (0,0) | `window_pieces03.tga` (0,13) | Red |
| **Mana** | `window_pieces04.tga` (0,0) | `window_pieces04.tga` (0,13) | Blue |
| **Stamina** | `window_pieces05.tga` (0,0) | `window_pieces05.tga` (0,13) | Gray |
| **Experience** | `window_pieces06.tga` (0,0) | `window_pieces06.tga` (0,13) | Green |
| **AA Points** | `window_pieces07.tga` (0,0) | `window_pieces07.tga` (0,13) | Yellow |

### Gauge Dimensions
- **Width**: 120px (standardized across all gauges)
- **Height**: 12px (consistent Thorne UI gauge height)
- **Texture Source**: 120×12px regions from window_pieces textures

---

## Design Influences

### Infiniti-Blue Gauge Reference
- Custom gauge texture system with distinct colors per resource
- 120×12px modular gauge design
- Matching empty/full states for smooth transitions
- High-contrast visual clarity

### duxaUI/vert Icon Methodology
- Class and race icon integration
- Visual character identification
- Icon-based design elements

### vert Stats Layout
- Vertical stat arrangement
- Efficient information density
- Organized attribute grouping (STR/STA/AGI/DEX in left column, INT/WIS/CHA in right)

---

## Differences from Pet Bottom Variant

| Feature | AA and XP Bottom | Pet Bottom |
|---------|------------------|------------|
| **Bottom Section** | AA + Experience gauges | Pet window integration |
| **Window Height** | Standard | Extended for pet display |
| **Focus** | Character progression | Pet management |
| **Use Case** | Solo/general play | Pet class players |

---

## Use Cases

**Best For**:
- Players tracking AA and level progression
- Users who want AA/XP status visible at all times
- Classes focused on character advancement (all classes)
- Players who prefer bottom-weighted visual layouts
- Solo players or group members monitoring personal progression

**Not Ideal For**:
- Pet class players who want integrated pet display (use Pet Bottom variant)
- Players who prefer minimal player window footprint
- Users who don't actively track AA progression

---

## Installation

1. Copy `EQUI_PlayerWindow.xml` to your EverQuest UI directory
2. Reload UI (`/loadskin` or restart client)
3. Player window will display with AA/XP gauges at bottom

**Compatibility**: Works with all EverQuest TAKP/P2002 clients with UI customization support.

---

## Development Status

**Current Status**: First Draft Implementation

This variant represents the initial implementation of the AA and XP Bottom design concept. Future iterations may include:
- Fine-tuned positioning and spacing
- Additional stat displays or toggles
- Visual polish and texture refinements
- User feedback-driven adjustments

---

## Technical Details

### Gauge Implementation Pattern
```xml
<Ui2DAnimation item="A_Gauge_[Color]_Full">
  <Texture>window_pieces0[N].tga</Texture>
  <Location><X>0</X><Y>0</Y></Location>
  <Size><CX>120</CX><CY>12</CY></Size>
</Ui2DAnimation>
```

### Required Texture Files
- `window_pieces03.tga` - Red HP gauges
- `window_pieces04.tga` - Blue Mana gauges
- `window_pieces05.tga` - Gray Stamina gauges
- `window_pieces06.tga` - Green XP gauges
- `window_pieces07.tga` - Yellow AA gauges

---

## Credits

**Author**: Draknare Thorne (January 2026)  
**Design Influences**:
- **Infiniti-Blue** - Gauge texture system and visual style reference
- **duxaUI/vert** - Icon methodology and layout concepts
- **vert** - Vertical stats arrangement pattern

---

## Related Files

- `Options/Player/Pet Bottom/` - Pet-integrated player window variant
- `Options/Player/Standard/` - Standard player notes configuration
- `EQUI_PlayerWindow.xml` (main) - Main directory player window

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Jan 2026 | First draft implementation with AA/XP bottom layout |

---

**Maintainer**: Draknare Thorne  
**Repository**: draknarethorne/thorne-ui  
**Status**: Active Development (First Draft)
