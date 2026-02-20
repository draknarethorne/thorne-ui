# Cast Spell Window - Enhanced Variant

**Status:** ✅ ACTIVE  
**Version:** 0.7.0  
**Last Updated:** February 18, 2026  
**Author:** Draknare Thorne

## Overview

The **Enhanced** variant of the cast spell window features custom button-style spell gems with improved visibility and contrast, but without individual spell recast timer displays.

## Features

### Custom Button-Style Spell Gems
- **Wider buttons**: 150px × 24px (vs 120px × 23px in Nillipuss)
- **Custom textures**: Dark and light button states for clear ready/cooldown feedback
- **Clear typography**: Spell names displayed prominently with improved readability
- **Consistent layout**: All spell gems use identical sizing and styling

### Design Characteristics
- Window size: **160px × 242px** (slightly wider than standard)
- Spell gem styling: Custom `A_CastBtnNormal` / `A_CastBtnReady` animations
- Texture assets: `button_dark-opaque01.tga` and `button_light-opaque01.tga`
- Visual feedback: Button state changes indicate when spells are ready to cast
- No individual spell cooldown indicators (see Default variant for recast timers)

## When to Use This Variant

Choose **Enhanced** if you:
- Prefer clean, uncluttered spell buttons
- Want to rely on visual button state changes for readiness feedback
- Prefer less information density on screen
- Use alternative methods to track spell cooldowns (hotbar feedback, audio cues, etc.)

## Comparison with Other Variants

| Feature | Enhanced | Default |
|---------|----------|---------|
| **Button Width** | 150px | 150px |
| **Button Height** | 24px | 24px |
| **Custom Textures** | Yes | Yes |
| **Recast Timers** | No | Yes (adds ~30px height) |
| **Window Height** | 242px | 273px |
| **Visual Simplicity** | Maximized | Balanced |
| **Information Density** | Low | Medium |

## Installation

1. **Backup Current:** Make a copy of your current cast spell window configuration
2. **Copy to Thorne Dev:**
   ```
   From: Options/Cast/Enhanced/EQUI_CastSpellWnd.xml
   To:   C:\TAKP\uifiles\thorne_dev\EQUI_CastSpellWnd.xml
   ```
3. **Reload in Game:** `/loadskin thorne_dev`
4. **Verify Position:** Use `/windowpos CastSpellWnd` to set preferred location if needed

## Technical Details

### Spell Gems (CSPW_Spell0-8)
- **SpellGem type**: Custom button layout
- **Draw template**: Uses A_CastBtnNormal (inactive) and A_CastBtnReady (active)
- **Icon offsets**: X=2, Y=0 for proper alignment within button frames
- **EQTypes**: 60-67 for spell names, 133 for 9th gem

### Spell Names (CSPW_Spell#_Name)
- **Font**: Font 1 (smaller than Font 2)
- **Position**: X=47 (right side of icon area)
- **Alignment**: Center-aligned for visual balance
- **Truncation**: Handles longer spell names without overflow

### Spell Numbers (CSPW_Spell#_No)
- **Font**: Font 4 (very small)
- **Purpose**: Shows gem number (1-9) for quick reference
- **Position**: Top-left of button

### Custom Textures
- **button_dark-opaque01.tga** (256×256)
  - Contains normal button state (120×24px at coordinates 100,0)
  - Used for inactive/normal spell gems
  
- **button_light-opaque01.tga** (256×256)
  - Contains active/ready button state (120×24px at coordinates 100,24)
  - Used when spell is ready to cast

## EQType Bindings

| Element | EQType | Purpose |
|---------|--------|---------|
| CSPW_Spell0_Name | 60 | Spell gem 1 name |
| CSPW_Spell1_Name | 61 | Spell gem 2 name |
| CSPW_Spell2_Name | 62 | Spell gem 3 name |
| CSPW_Spell3_Name | 63 | Spell gem 4 name |
| CSPW_Spell4_Name | 64 | Spell gem 5 name |
| CSPW_Spell5_Name | 65 | Spell gem 6 name |
| CSPW_Spell6_Name | 66 | Spell gem 7 name |
| CSPW_Spell7_Name | 67 | Spell gem 8 name |
| CSPW_Spell8_Name | 133 | Spell gem 9 name |

## Customization Options

### Change Button Colors
Edit the texture files or modify the ColorInfo sections in EQUI_CastSpellWnd.xml to adjust:
- Button background colors
- Text colors for spell names
- Number label colors

### Adjust Spell Button Size
Modify the `<Size>` elements for CSPW_Spell# items:
```xml
<Size>
  <CX>150</CX>  <!-- Change width -->
  <CY>24</CY>   <!-- Change height -->
</Size>
```

### Reposition Window
Use in-game: `/windowpos CastSpellWnd X Y` to move the window to your preferred location

## Known Limitations

- No individual spell cooldown visual indicators
- Recast timing information not displayed (must use other feedback methods)
- Window height is fixed (cannot be resized with `/windowsize`)
- Button state changes may be subtle depending on monitor/graphics settings

## Variants Reference

**Current Cast Spell Window Options:**
- **Enhanced** (this file) - Custom buttons, no recast timers
- **Default** - Custom buttons with individual spell recast timer gauges
- *Future: Standard* - Original spell gem graphics (when implemented)

## Support & Feedback

For issues, suggestions, or improvements:
- Check existing window positioning with `/windowpos CastSpellWnd`
- Verify spell gems appear correctly in your UI
- Test with different character classes and spell configurations
- Feedback welcome for future variant improvements

## Credits

- **Original Design**: Tabashir (initial creation)
- **QQQuarm Revision**: Brujoloco (November 15, 2023)
- **Thorne UI Enhancement**: Draknare Thorne (January 2026)
  - Custom button textures and layout improvements
  - Window size optimization
  - Enhanced typography and readability

---

**Part of Thorne UI** - Custom UI files for TAKP and other EverQuest classic servers.
