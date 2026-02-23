# Cast Window - Standard Variant

**File**: [EQUI_CastSpellWnd.xml](./EQUI_CastSpellWnd.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-09  
**Status**: ✅ Active variant (traditional EverQuest appearance)  
**Author**: Draknare Thorne (variant adaptation)  
**Based On**: Original by Tabashir, modified by Brujoloco (QQQuarm Nov 2023)

---
## Purpose

The Standard Cast Spell Window variant preserves the traditional EverQuest spell gem appearance using standard spell gem sprites (A_SpellGemHolder, A_SpellGemBackground). This variant maintains the compact 140-pixel width and classic spell gem graphics found in original EverQuest UI designs, providing a familiar experience for players who prefer traditional aesthetics.

**Key Differentiators from Default**:
- Traditional spell gem sprites instead of custom button graphics
- Compact 140px window width (vs 160px Default)
- Mixed spell gem sizing for varied visual layout
- No custom textures required

**Key Features**:

- **Traditional Spell Gem Graphics**: Uses standard A_SpellGemHolder and A_SpellGemBackground animations from EQUI_Animations.xml
- **Compact Window Layout**: 140px width maintains classic EverQuest spell window footprint
- **Mixed Gem Sizing**: Spell gems use varied dimensions (31×23px and 138×23px) for traditional visual pattern
- **No Custom Textures**: Relies entirely on standard EverQuest UI texture assets
- **Varied Draw Templates**: Different spell gems use different holder templates (A_SpellGemHolder, A_SquareBtnPressed, A_BtnNormal, A_RecessedBox) for visual variety
- **Classic Positioning**: Spell names and numbers positioned for compact layout (spell names at X=40)
- **Lightweight**: No additional texture loading beyond standard UI assets

**Design Philosophy**: Maintains the classic EverQuest appearance for players who prefer traditional UI aesthetics or need the most compact spell window possible.

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 140 × 237 pixels (fixed) |
| Resizable | No (`Style_Sizable=false`) |
| Fadeable | No (`Style_Transparent=false`) |
| Screen ID | CastSpellWnd |
| DrawTemplate | WDT_RoundedNoTitle |
| Default Position | X=1, Y=281 |
| Titlebar | No (`Style_Titlebar=false`) |
| Closebox | No (`Style_Closebox=false`) |
| Minimizebox | No (`Style_Minimizebox=false`) |
| Border | Yes (`Style_Border=true`) |
| Spell Gem Count | 9 (8 visible, 1 hidden at Y=300) |
| Spell Gem Sizes | Mixed: 138×23px (gems 0-3), 31×23px (gems 4-8) |
| Spellbook Button | 140×20 pixels at Y=209 |

---

## Layout Overview

### Window Hierarchy

```
CastSpellWnd (140×237px)
├── Spell Gems (CSPW_Spell0 through CSPW_Spell8)
│   ├── SpellGem elements (mixed sizes: 138×23px or 31×23px)
│   │   ├── CSPW_Spell0: 138×23px (A_SpellGemHolder)
│   │   ├── CSPW_Spell1: 138×23px (A_SpellGemHolder)
│   │   ├── CSPW_Spell2: 138×23px (A_SpellGemHolder)
│   │   ├── CSPW_Spell3: 138×23px (A_SpellGemHolder)
│   │   └── CSPW_Spell4-8: 138×23px (A_SpellGemHolder)
│   ├── Spell name labels (Font 1, positioned at X=40)
│   └── Spell number labels (Font 4, positioned at X=29)
└── Spellbook Button (CSPW_SpellBook, 140×20px at bottom)
```

### Visual Diagram

```
┌──────────────────────────────────────────┐
│ Spells                                   │
├──────────────────────────────────────────┤
│ 1 [◆◆◆◆◆◆◆ Spell Name 1 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=1)
│ 2 [◆◆◆◆◆◆◆ Spell Name 2 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=27)
│ 3 [◆◆◆◆◆◆◆ Spell Name 3 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=53)
│ 4 [◆◆◆◆◆◆◆ Spell Name 4 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=79)
│ 5 [◆◆◆◆◆◆◆ Spell Name 5 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=105)
│ 6 [◆◆◆◆◆◆◆ Spell Name 6 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=131)
│ 7 [◆◆◆◆◆◆◆ Spell Name 7 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=157)
│ 8 [◆◆◆◆◆◆◆ Spell Name 8 ◆◆◆◆◆◆◆◆◆]  │ ← 138×23px gem (Y=183)
│                                          │
│    [      Spellbook Button      ]       │ ← 140×20px button (Y=209)
└──────────────────────────────────────────┘
   (Spell gem 9 hidden off-screen at Y=300)
```

**Note**: ◆ symbol represents traditional spell gem appearance with gem-shaped graphics.

---

## Spell Gem Sizing Patterns

### Size Distribution

| Spell Gem Range | Width | Height | Draw Template Holder |
|-----------------|-------|--------|----------------------|
| CSPW_Spell0 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell1 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell2 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell3 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell4 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell5 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell6 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell7 | 138px | 23px | A_SpellGemHolder |
| CSPW_Spell8 | 138px | 23px | A_SpellGemHolder |

**Note**: All spell gems now use uniform 138×23px sizing with A_SpellGemHolder draw templates for consistency.

### Draw Template Variations

Each spell gem uses standard EverQuest spell gem draw templates:

```
SpellGemDrawTemplate:
  - Holder: A_SpellGemHolder
  - Background: A_SpellGemBackground
  - Highlight: A_SpellGemHighlight
```

**Visual Effect**: Traditional spell gem appearance with gem-shaped border, transparent areas, and classic EverQuest spell gem aesthetics.

---

## Y-Position Layout

| Spell Gem | Y Position | Spacing from Previous |
|-----------|------------|-----------------------|
| CSPW_Spell0 | 1 | — |
| CSPW_Spell1 | 27 | 26px |
| CSPW_Spell2 | 53 | 26px |
| CSPW_Spell3 | 79 | 26px |
| CSPW_Spell4 | 105 | 26px |
| CSPW_Spell5 | 131 | 26px |
| CSPW_Spell6 | 157 | 26px |
| CSPW_Spell7 | 183 | 26px |
| CSPW_Spell8 | 300 | (hidden, off-screen) |

**Consistent Spacing**: 26-pixel vertical spacing between all visible spell gems, providing 3px gap between 23px tall gems.

---

## Differences from Default Variant

| Feature | Standard (This Variant) | Default (Custom Button) Variant |
|---------|-------------------------|----------------------------------|
| **Window Width** | 140px | 160px |
| **Spell Gem Width** | 138px (uniform) | 150px (uniform) |
| **Spell Gem Height** | 23px | 24px |
| **Draw Templates** | A_SpellGemHolder (all gems) | A_CastBtnNormal, A_CastBtnReady (custom) |
| **Custom Textures** | ❌ No (uses standard animations) | ✅ Yes (buttons_dark_thorne01.tga × 2) |
| **Spell Icon Offset** | ❌ No | ✅ Yes (SpellIconOffsetX=2) |
| **Spell Name Font** | Font 1 | Font 2 |
| **Spell Name Position** | X=40 | X=47 |
| **Visual Style** | Traditional gem sprites | Button-style (high contrast) |
| **Use Case** | Compact, traditional EQ appearance | Enhanced visibility, wider layout |
| **Texture Loading** | None (uses EQUI_Animations.xml) | +2 custom textures (button_pieces) |

---

## Use Cases

**Best For**:
- Players who prefer traditional EverQuest UI aesthetics
- Users who want the most compact spell window possible (140px width)
- Players on lower resolutions or who need to conserve screen space
- Users who prefer classic spell gem graphics over modern button styles
- Players who want a lightweight variant with no custom texture loading

**Not Ideal For**:
- Players who find traditional spell gems hard to see or too subtle
- Users who want enhanced visual contrast for spell states
- Players with wider screens who benefit from larger spell name display

---

## Installation

**Automatic (via Options Selector)**:
1. Use Thorne UI Options Selector if available
2. Navigate to Cast Window → Standard variant
3. Apply selection and reload UI

**Manual Installation**:
1. Copy `EQUI_CastSpellWnd.xml` from `Options/Cast/Standard/` to `thorne_drak/` directory
2. No additional textures required (uses standard EQUI_Animations.xml assets)
3. Reload UI with `/loadskin thorne_drak` or restart client
4. Cast Spell Window will display with traditional spell gem graphics

**Compatibility**: TAKP/P2002 clients with UI customization support.

---

## Technical Notes

### Standard Animation References

- **A_SpellGemHolder**: Defined in `EQUI_Animations.xml`, provides gem-shaped border frame
- **A_SpellGemBackground**: Defined in `EQUI_Animations.xml`, provides gem interior/fill graphics
- **A_SpellGemHighlight**: Defined in `EQUI_Animations.xml`, provides mouse hover state

### No Custom Elements

- **Zero Custom Textures**: Relies entirely on standard EverQuest texture assets
- **No Inline Animations**: No `<Ui2DAnimation>` or `<TextureInfo>` definitions within file
- **Lightweight**: Minimal memory footprint, fast loading

### Spell Gem Structure Pattern

Each spell gem follows this standard pattern:

```xml
<SpellGem item="CSPW_Spell#">
  Location: X=1, Y=[varies]
  Size: 138×23 or 31×23 pixels
  DrawTemplate:
    - Holder: A_SpellGemHolder (or variant)
    - Background: A_SpellGemBackground (or variant)
    - Highlight: A_SpellGemHighlight
</SpellGem>

<Label item="CSPW_Spell#_Name">
  Location: X=40, Y=[matches spell gem Y]
  Font: 1
  Size: 87×24 pixels
  EQType: 60-67, 133
</Label>

<Label item="CSPW_Spell#_No">
  Location: X=29, Y=[spell gem Y + 3-4px]
  Font: 4
  Size: 20×40 pixels
  Text: "1"-"9"
</Label>
```

---

## Performance Considerations

- **Minimal Overhead**: Uses pre-loaded standard animations from EQUI_Animations.xml
- **No Additional Texture Loading**: Zero custom texture files required
- **Fast Rendering**: Simple spell gem sprites render efficiently
- **Low Memory**: Standard variant has smallest memory footprint of all Cast Window variants

---

## Development Notes

**Variant Creation**:
- Standard variant represents the baseline Thorne UI cast window before custom button enhancements
- Maintained for users who prefer traditional EverQuest spell gem appearance
- Serves as fallback option for players experiencing issues with custom texture variants

**Based On**:
- Original EQUI_CastSpellWnd.xml by Tabashir
- QQQuarm compilation revision by Brujoloco (Nov 2023)
- Adapted as "Standard" variant when Default variant adopted custom buttons

**Future Updates** (potential):
- Optional mixed gem sizing patterns for visual variety
- Alternative draw template combinations for different gem appearance variations

---

**Variant Type**: Original/Baseline  
**Complexity**: Low (standard spell gems only)  
**Maintenance**: Low (stable, no custom dependencies)
