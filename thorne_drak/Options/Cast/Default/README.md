# Window: Cast - Default Variant

**File**: [EQUI_CastSpellWnd.xml](./EQUI_CastSpellWnd.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-09  
**Status**: ✅ Active variant  
**Author**: Draknare Thorne  
**Based On**: Original by Tabashir, modified by Brujoloco (QQQuarm Nov 2023)

---
## Purpose

The Default Cast Spell Window variant features custom button-style spell gem graphics designed to enhance visibility and readability in the spell casting interface. This variant replaces traditional spell gem sprites with custom button textures that provide superior color contrast and a wider layout for better spell name display.

**Key Differentiators from Standard**:
- Button-style spell gems instead of traditional gem sprites
- Custom texture assets specific to this window
- Wider window layout (160px vs 140px)
- Uniform spell gem sizing across all 9 slots

**Key Features**:

- **Custom Button Graphics**: Uses `button_pieces01.tga` and `button_pieces01_light.tga` for normal and active button states, providing enhanced visual contrast
- **Standardized Spell Gem Sizing**: All 9 spell gems use identical 150×24 pixel dimensions (previously mixed sizes)
- **Widened Window Layout**: 160px width (vs 140px Standard) accommodates full spell names with reduced truncation
- **Custom Animations**: `A_CastBtnNormal` and `A_CastBtnReady` provide distinct visual states for spell readiness
- **Spell Icon Offsets**: Precisely positioned spell icons (SpellIconOffsetX=2, SpellIconOffsetY=0) for proper alignment within custom button frames
- **Enhanced Text Positioning**: Spell names positioned at X=47 with improved alignment for better readability
- **Window-Specific Design**: Custom textures used ONLY in Cast Spell Window, not in hotbars or other UI elements (those retain standard spell gem appearance)

**Design Philosophy**: Button-style spell gems provide superior visibility for the main spell casting interface where spell selection is critical, while hotbuttons and other compact displays retain traditional gem graphics for space efficiency.

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 160 × 238 pixels (fixed) |
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
| Spell Gem Size | 150×24 pixels (uniform across all gems) |
| Spellbook Button | 144×20 pixels at Y=209 |

---

## Layout Overview

### Window Hierarchy

```
CastSpellWnd (160×238px)
├── Custom Texture Definitions
│   ├── button_pieces01.tga (256×256px)
│   └── button_pieces01_light.tga (256×256px)
├── Custom Animations
│   ├── A_CastBtnNormal (uses button_pieces01.tga at 100,0, 120×24px)
│   └── A_CastBtnReady (uses button_pieces01_light.tga at 100,24, 120×24px)
├── Spell Gems (CSPW_Spell0 through CSPW_Spell8)
│   ├── SpellGem elements (150×24px, custom draw templates)
│   ├── Spell name labels (Font 2, positioned at X=47)
│   └── Spell number labels (Font 4, positioned at X=27-29)
└── Spellbook Button (CSPW_SpellBook, 144×20px at bottom)
```

### Visual Diagram

```
┌────────────────────────────────────────────────────┐
│ Spells                                             │
├────────────────────────────────────────────────────┤
│ 1 [█████████ Spell Name 1 ████████████████████]   │ ← 150×24px button (Y=1)
│ 2 [█████████ Spell Name 2 ████████████████████]   │ ← 150×24px button (Y=27)
│ 3 [█████████ Spell Name 3 ████████████████████]   │ ← 150×24px button (Y=53)
│ 4 [█████████ Spell Name 4 ████████████████████]   │ ← 150×24px button (Y=79)
│ 5 [█████████ Spell Name 5 ████████████████████]   │ ← 150×24px button (Y=105)
│ 6 [█████████ Spell Name 6 ████████████████████]   │ ← 150×24px button (Y=131)
│ 7 [█████████ Spell Name 7 ████████████████████]   │ ← 150×24px button (Y=157)
│ 8 [█████████ Spell Name 8 ████████████████████]   │ ← 150×24px button (Y=183)
│                                                    │
│        [        Spellbook Button         ]        │ ← 144×20px button (Y=209)
└────────────────────────────────────────────────────┘
   (Spell gem 9 hidden off-screen at Y=300)
```

**Note**: Each spell gem includes:
- Spell icon on left (offset 2px right for proper button frame alignment)
- Spell number overlay (Font 4, distinct visibility)
- Spell name text (Font 2, centered/aligned for readability)

---

## Custom Texture System

### Texture Files

| Texture File | Purpose | Size | Region Used |
|--------------|---------|------|-------------|
| `button_pieces01.tga` | Normal button state (darker) | 256×256px | 100,0 → 120×24px |
| `button_pieces01_light.tga` | Ready button state (lighter) | 256×256px | 100,24 → 120×24px |

### Animation Definitions

| Animation | Texture Source | Usage | Visual State |
|-----------|----------------|-------|--------------|
| **A_CastBtnNormal** | button_pieces01.tga | SpellGemDrawTemplate Holder | Normal/inactive spell |
| **A_CastBtnReady** | button_pieces01_light.tga | SpellGemDrawTemplate Background | Ready/memorized spell |
| **A_SpellGemHighlight** | (Standard) | SpellGemDrawTemplate Highlight | Mouse hover state |

**Technical Details**:
- Textures are window-specific and defined inline within EQUI_CastSpellWnd.xml
- NOT referenced by hotbutton windows or other UI elements
- 120×24px animation frames extracted from 256×256px texture atlases
- Cycle duration: 1000ms per frame

---

## Spell Gem Layout Pattern

### Individual Spell Gem Structure

Each spell gem (CSPW_Spell0 through CSPW_Spell7) follows this pattern:

```xml
<SpellGem item="CSPW_Spell#">
  Location: X=1, Y=[varies by spell number]
  Size: 150×24 pixels
  DrawTemplate:
    - Holder: A_CastBtnNormal
    - Background: A_CastBtnReady
    - Highlight: A_SpellGemHighlight
  SpellIconOffset: X=2, Y=0
</SpellGem>

<Label item="CSPW_Spell#_Name">
  Location: X=47, Y=[matches spell gem Y]
  Font: 2
  Size: 87×24 or 92×24 pixels
  EQType: 60-67, 133 (spell name binding)
  Alignment: Center
</Label>

<Label item="CSPW_Spell#_No">
  Location: X=27-29, Y=[spell gem Y + 3-4px]
  Font: 4
  Size: 20×40 pixels
  Text: "1"-"9"
  Alignment: Center
</Label>
```

### Y-Position Progression

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

**Spacing Pattern**: 26-pixel vertical spacing between visible spell gems, providing 2px gap between 24px tall buttons.

---

## Differences from Standard Variant

| Feature | Default (This Variant) | Standard Variant |
|---------|------------------------|------------------|
| **Window Width** | 160px | 140px |
| **Spell Gem Width** | 150px (uniform) | Mixed (31px, 127px, 138px) |
| **Spell Gem Height** | 24px (uniform) | 23px (uniform) |
| **Draw Templates** | A_CastBtnNormal (Holder), A_CastBtnReady (Background) | A_SpellGemHolder, A_SpellGemBackground (varies by gem) |
| **Custom Textures** | ✅ Yes (button_pieces01.tga × 2) | ❌ No (uses standard animations) |
| **Spell Icon Offset** | ✅ Yes (SpellIconOffsetX=2) | ❌ No |
| **Spell Name Font** | Font 2 (all gems) | Font 1 (most gems) |
| **Spell Name Position** | X=47 | X=40 |
| **Visual Style** | Button-style (high contrast) | Traditional gem sprites |
| **Use Case** | Enhanced visibility, wider layout | Compact, traditional EQ appearance |

---

## Use Cases

**Best For**:
- Players who want enhanced spell gem visibility
- Users who prefer modern button-style UI elements
- Casters who need to quickly identify spell states (memorized vs empty)
- Players with wider screen resolutions who benefit from larger spell window
- Users who find traditional spell gems too subtle or hard to read

**Not Ideal For**:
- Players who prefer traditional EverQuest spell gem aesthetics
- Users who want the most compact possible spell window (use Standard variant)
- Players on lower resolutions where 160px width is problematic

---

## Installation

**Automatic (via Options Selector)**:
1. Use Thorne UI Options Selector if available
2. Navigate to Cast Window → Default variant
3. Apply selection and reload UI

**Manual Installation**:
1. Copy `EQUI_CastSpellWnd.xml` from `Options/Cast/Default/` to `thorne_drak/` directory
2. Ensure `button_pieces01.tga` and `button_pieces01_light.tga` exist in `thorne_drak/`
3. Reload UI with `/loadskin thorne_drak` or restart client
4. Cast Spell Window will display with custom button-style spell gems

**Compatibility**: TAKP/P2002 clients with UI customization support.

---

## Technical Notes

### Custom Texture Integration

- **Inline Definitions**: Textures defined directly within EQUI_CastSpellWnd.xml via `<TextureInfo>` and `<Ui2DAnimation>` elements
- **No External Animation References**: Does not rely on EQUI_Animations.xml for custom button graphics
- **Window-Scoped Animations**: A_CastBtnNormal and A_CastBtnReady only exist within this window's scope

### Spell Icon Positioning

- **SpellIconOffsetX=2**: Shifts spell icon 2 pixels right to align within custom button frame
- **SpellIconOffsetY=0**: No vertical offset needed (already centered in 24px height)
- Without offsets, spell icons would appear misaligned within custom button graphics

### Font Choices

- **Font 2 for Spell Names**: Provides better readability in wider button layout
- **Font 4 for Spell Numbers**: Large, bold numbers ensure clear hotkey identification

### Performance Considerations

- Two 256×256px custom textures loaded for this window
- Minimal performance impact (small texture atlas regions used)
- No animation cycling (static frame display)

---

## Development Notes

**Modification History**:
- **Jan 2026**: Created custom button variant with button_pieces01 textures
- **Jan 2026**: Standardized all spell gem sizes to 150×24 pixels
- **Jan 2026**: Widened window from 140px to 160px
- **Jan 2026**: Added spell icon offsets for proper button frame alignment

**Based On**:
- Original EQUI_CastSpellWnd.xml by Tabashir
- QQQuarm compilation revision by Brujoloco (Nov 2023)

**Future Enhancements** (potential):
- Optional color themes for button backgrounds
- Alternative button texture sets
- Configurable spell gem sizing

---

**Variant Type**: Custom Enhancement  
**Complexity**: Moderate (custom textures + animation definitions)  
**Maintenance**: Low (stable custom texture system)
