# Spellbook Window - Standard Variant

**File**: [EQUI_SpellBookWnd.xml](./EQUI_SpellBookWnd.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-17
**Status**: ✅ Active variant  
**Author**: Draknare Thorne

---
## Purpose

The Standard Spellbook window variant provides a baseline spell management interface with standard layout and configuration. This variant serves as the default spellbook implementation for players who prefer classic spell browsing and memorization without extended customizations.

**Key Features**:

- **Standard Layout**: Classic spellbook page design with spell slot grid
- **Page Navigation**: Left/right page controls for browsing spell collection
- **Spell Gem Integration**: Direct spell memorization to casting bar
- **Note Fill Animations**: Visual page background elements
- **Efficient Spell Management**: Organized spell slots with category filtering
- **Clean Interface**: Minimal distractions, focus on spell organization

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | ~400 × 300 pixels |
| Spell Slots per Page | ~16 spells (4×4 grid per page side) |
| Page Navigation | ✅ Yes (left/right arrows) |
| Spell Categories | All standard EQ spell categories |
| Memorization | Direct to spell gem slots |

---

## Window Layout

```
┌─────────────────────────────────────────────────┐
│  ◄                SPELLBOOK                 ►   │ ← Page navigation
├──────────────────┬──────────────────────────────┤
│  ┌────┐ ┌────┐  │  ┌────┐ ┌────┐             │
│  │ S1 │ │ S2 │  │  │ S9 │ │S10 │             │ ← Left page
│  └────┘ └────┘  │  └────┘ └────┘             │   (spells 1-8)
│  ┌────┐ ┌────┐  │  ┌────┐ ┌────┐             │
│  │ S3 │ │ S4 │  │  │S11 │ │S12 │             │ ← Right page
│  └────┘ └────┘  │  └────┘ └────┘             │   (spells 9-16)
│  ┌────┐ ┌────┐  │  ┌────┐ ┌────┐             │
│  │ S5 │ │ S6 │  │  │S13 │ │S14 │             │
│  └────┘ └────┘  │  └────┘ └────┘             │
│  ┌────┐ ┌────┐  │  ┌────┐ ┌────┐             │
│  │ S7 │ │ S8 │  │  │S15 │ │S16 │             │
│  └────┘ └────┘  │  └────┘ └────┘             │
└──────────────────┴──────────────────────────────┘
```

---

## Spell Slot Configuration

### Standard Spell Buttons
- **Size**: 24×20 pixels per spell button
- **Layout**: 4×4 grid on each page side (left and right)
- **Total per Page**: 16 spell slots (8 per side)
- **Interaction**: Click to memorize to spell gem bar
- **Visual**: Displays spell icon when learned

### Note Fill Backgrounds
- **SBW_A_NoteFill2**: 180×201px background element (positioned at X=74, Y=54)
- **SBW_A_NoteFill4**: 180×100px background element (positioned at X=74, Y=0)
- Purpose: Visual page texture and depth

---

## Spell Management Workflow

### Browsing Spells
1. Use left/right arrow buttons to navigate pages
2. Each page shows up to 16 spells in your spellbook
3. Spells organized by level and category

### Memorizing Spells
1. Click spell in spellbook
2. Click empty spell gem slot on casting bar
3. Wait for memorization timer to complete
4. Spell is ready to cast

### Spell Organization
- Spells automatically sorted by level and category
- Can scribe new spells from scrolls
- Delete unwanted spells to free slots

---

## Use Cases

**Best For**:
- Standard spell management needs
- Players familiar with classic EQ spellbook interface
- Users who don't require extended spellbook customizations
- All caster classes (Wizard, Cleric, Shaman, Druid, Enchanter, Necromancer, Magician, Bard, Paladin, Shadow Knight, Ranger, Beastlord)

**Provides**:
- Familiar, proven spellbook layout
- Efficient spell browsing and memorization
- Clean interface without distractions
- Standard functionality for all spell types

---

## Installation

1. Copy `EQUI_SpellBookWnd.xml` to your EverQuest UI directory
2. Reload UI (`/loadskin` or restart client)
3. Open spellbook (/book or keybind)

**Compatibility**: Works with all EverQuest TAKP/P2002 clients with UI customization support.

---

## Technical Details

### Window Components

**Spell Buttons**:
```xml
<Button item="SBW_Spell0">
  <Size>
    <CX>24</CX>
    <CY>20</CY>
  </Size>
  <Location>
    <X>0</X>
    <Y>0</Y>
  </Location>
</Button>
```

**Background Animations**:
```xml
<Ui2DAnimation item="SBW_A_NoteFill2">
  <Frames>
    <Location><X>74</X><Y>54</Y></Location>
    <Size><CX>180</CX><CY>201</CY></Size>
  </Frames>
</Ui2DAnimation>
```

### Spell Slot Indexing
- Slots numbered SBW_Spell0 through SBW_Spell15 per page
- Multiple pages accessible via navigation
- Total spell capacity determined by class and level

---

## Configuration Options

### Standard Settings
- **Transparent Background**: Disabled for standard appearance
- **Checkbox Style**: Disabled (radio-style spell selection)
- **Relative Positioning**: Enabled for consistent layout
- **VScroll**: Disabled (page-based navigation instead)

---

## Interface Synchronization

This spellbook variant is synchronized with:
- `EQUI_CastSpellWnd.xml` - Spell gem bar for memorized spells
- `EQUI_SpellBookWnd.xml` (main) - Main directory spellbook layout
- Default EverQuest spell memorization system

---

## Credits

**Author**: Draknare Thorne (January 2026)  
**Original Design**: EverQuest default spellbook interface  
**Layout Synchronization**: Thorne UI standardization

---

## Related Files

- `EQUI_SpellBookWnd.xml` (main) - Main directory spellbook window
- `EQUI_CastSpellWnd.xml` - Spell gem/casting bar interface
- `Options/Spellbook/` - Future spellbook variants directory

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Standard spellbook variant established |

---

**Maintainer**: Draknare Thorne  
**Repository**: draknarethorne/thorne-ui
