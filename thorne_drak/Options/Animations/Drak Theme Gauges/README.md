# Animations Window - Drak Theme Gauges Variant

**File**: [EQUI_Animations.xml](./EQUI_Animations.xml)
**Version**: 1.0.0
**Last Updated**: January 25, 2026
**Status**: ✅ Active - Drak-Themed Gauge Textures
**Author**: Draknare Thorne

---
## Purpose

The Animations window (EQUI_Animations.xml) defines texture animations and gauge display settings used throughout the Thorne UI. This "Drak Theme Gauges" variant applies a custom gauge texture set optimized for the "Drak" UI theme - using modern blue gradients and refined visual styling for all resource gauges (HP, Mana, Stamina, XP, Pet Health).

**Key Features**:

- **Custom Gauge Textures**: Modern blue gradient textures designed for clarity and visual appeal
- **Optimized Tall Gauges**: 15px height gauges for primary resources (HP, Mana, XP)
- **Dark Line Variants**: Optional darker grid lines for XP gauge depth and progression visibility
- **Stamina/Pet Gauges**: 8px height compact gauges for secondary resource tracking
- **Multiple Texture Backups**: Inactive variants (gauge_pieces02-06) available for testing alternative themes
- **Infiniti-Blue Base**: Built from proven Infiniti-Blue color palette for consistency with thorne_drak theme

---

## Specifications

| Property | Value |
|----------|-------|
| **Primary Textures** | gauge_pieces01.tga, gauge_pieces01_tall.tga |
| **Active Gauges** | 5 (HP, Mana, XP, Stamina, Pet) |
| **Standard Height** | 8px (Stamina, Pet) |
| **Tall Height** | 15px (HP, Mana, XP) |
| **Color Scheme** | Infiniti-Blue modified (blue gradients) |
| **Backup Variants** | 5 inactive texture sets (gauge_pieces02-06.tga) |
| **Theme Alignment** | thorne_drak (primary variant) |

---

## Active Gauge Textures

### gauge_pieces01.tga (103x32)

**Source**: Infiniti-Blue
**Status**: ACTIVE
**Used By**:

- `A_GaugeBackground` (Y=0, 8px)
- `A_GaugeFill` (Y=8, 8px)
- `A_GaugeLines` (Y=16, 8px)
- `A_GaugeLinesFill` (Y=24, 8px)

**Current Usage:**

- Stamina gauge (PW_Gauge_Stamina) - 120x8
- Pet Health gauge (PW_Gauge_PetHP) - 103x8

**Style**: Modern blue gradient with transparency; clean smooth fill

### gauge_pieces01_tall.tga (120x64)

**Source**: Custom built from Infiniti-Blue rows
**Status**: ACTIVE
**Used By**:

- `A_GaugeBackground_Tall` (Y=1, 15px)
- `A_GaugeFill_Tall` (Y=16, 15px)
- `A_GaugeLines_Tall` (Y=31, 15px) - Original light lines
- `A_GaugeLines_Tall_Dark` (Y=46, 16px) - Darker lines variant

**Texture Layout:**

- Rows 1-15: Background (15px)
- Rows 16-30: Fill (15px)
- Rows 31-45: Lines light (15px)
- Rows 46-61: Lines dark (16px) - Created by copying rows 26-29 to 58-61

**Current Usage:**

- HP gauge (PW_Gauge_HP) - 120x15, no lines
- Mana gauge (PW_Gauge_Mana) - 120x15, no lines
- XP gauge (PW_Gauge_XP) - 120x15, dark lines at bottom

**Style**: Taller variant for primary resource gauges; darker lines provide visual depth for XP progression

---

## Inactive Gauge Variants (Available for Testing)

### gauge_pieces02.tga (103x32)

**Source**: Copy of gauge_pieces01.tga
**Status**: INACTIVE (backup/testing)
**Purpose**: Create modifications while preserving original gauge_pieces01.tga

### gauge_pieces03.tga (100x32)

**Source**: default/window_pieces01.tga
**Status**: INACTIVE
**Style**: Classic EverQuest default appearance
**Note**: 100px width (3px narrower than current 103px)

### gauge_pieces04.tga (100x32)

**Source**: duxaUI/window_pieces01.tga
**Status**: INACTIVE
**Style**: DuxaUI theme variant

### gauge_pieces05.tga (100x32)

**Source**: QQ/window_pieces01.tga
**Status**: INACTIVE
**Style**: QQ UI theme variant

### gauge_pieces06.tga (100x32)

**Source**: vert/window_pieces01.tga
**Status**: INACTIVE
**Style**: Vertical layout theme variant

---

## How to Test Alternative Variants

**To switch to a different gauge texture:**

1. Open `EQUI_Animations.xml`
2. Locate the gauge animations you want to modify:
   - `A_GaugeBackground`
   - `A_GaugeFill`
   - `A_GaugeLines`
   - `A_GaugeLinesFill`
3. Change the `<Texture>` element:

   ```xml
   <Texture>gauge_pieces01.tga</Texture>
   <!-- Change to -->
   <Texture>gauge_pieces03.tga</Texture>
   ```

4. Reload UI in-game: `/loadskin thorne_drak 1`

**Width Compatibility Notes:**

- **103px variants** (01, 02): Compatible with current Infiniti-Blue style
- **100px variants** (03-06): 3px narrower; may require gauge positioning adjustments
- When switching between widths, check gauge alignment and adjust X coordinates if needed

---

## Animation Coordinate Reference

### Standard Gauges (gauge_pieces01.tga - 103x32)

Stacked vertical layout (8px slices):

| Slice | Y Position | Height | Animation Name |
|-------|------------|--------|----------------|
| Background | 0 | 8px | A_GaugeBackground |
| Fill | 8 | 8px | A_GaugeFill |
| Lines | 16 | 8px | A_GaugeLines |
| LinesFill | 24 | 8px | A_GaugeLinesFill |

### Tall Gauges (gauge_pieces01_tall.tga - 120x64)

Compressed vertical layout (15-16px slices):

| Slice | Y Position | Height | Animation Name |
|-------|------------|--------|----------------|
| Background | 1 | 15px | A_GaugeBackground_Tall |
| Fill | 16 | 15px | A_GaugeFill_Tall |
| Lines (light) | 31 | 15px | A_GaugeLines_Tall |
| Lines (dark) | 46 | 16px | A_GaugeLines_Tall_Dark |

---

## Creating New Gauge Variants

**To extract gauge textures from other UI themes:**

1. Open the source UI's `EQUI_Animations.xml`
2. Find `A_GaugeBackground` animation definition
3. Note:
   - Texture filename
   - X/Y coordinates in `<Location>`
   - Size in `<Size>` (CX/CY)
4. Extract that region from the source .tga file
5. Save as `gauge_pieces##.tga` in thorne_drak directory
6. Add `<TextureInfo>` entry to `thorne_drak/EQUI_Animations.xml`
7. Test by updating animation `<Texture>` references

**Python Extraction Script** (if available):

```bash
python extract_gauge_texture.py --source <source_ui> --output gauge_pieces##.tga
```

---

## Performance Considerations

- **Texture Cache**: Gauge_pieces01*.tga files (2 active, 5 inactive backups) loaded at UI startup
- **Animation Frame Rate**: Gauge animations update synchronously with EQType value changes
- **Memory Impact**: Each gauge texture (~32-64 KB) minimal impact on modern systems
- **Alternative Testing**: Backup texture variants (gauge_pieces02-06.tga) available for visual comparison without recompiling

---

## Related Files

- [EQUI_Animations.xml](EQUI_Animations.xml) — Gauge animation definitions
- [EQUI_PlayerWindow.md](EQUI_PlayerWindow.md) — Player Window implementation using these textures
- Reference: `Infiniti-Blue/` — Source of gauge_pieces01.tga style

---

*Last Updated: January 25, 2026*
*Author: Draknare Thorne*
*Status: Active Textures Documented*
