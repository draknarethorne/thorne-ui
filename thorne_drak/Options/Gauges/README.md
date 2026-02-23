# Gauge Options

**Directory**: `thorne_drak/Options/Gauges/`  
**Version**: 3.0.0  
**Last Updated**: February 21, 2026  
**Status**: ✅ Active - Subdirectory-Based Organization  
**Author**: Draknare Thorne

---

## 📋 Overview

This directory contains gauge texture variants for HP, Mana, Stamina, Experience, and Pet Health bars used throughout Thorne UI. Each subdirectory contains a complete set of pre-built textures at all supported sizes — just copy the files for your chosen variant into the main `thorne_drak/` directory.

**Key Features:**
- **7 Visual Styles**: Multiple gauge aesthetics to match your preference
- **Subdirectory Organization**: Each variant isolated in its own folder
- **Multiple Sizes**: Wide (120, 150) and tall (120t, 150t, 230t, 240t, 250t, 260t) — all pre-built and ready to use
- **Easy Switching**: Copy desired variant's `.tga` files to main thorne_drak directory
- **Shared Animation Definitions**: All variants use same EQUI_Animations.xml

---

## 🎨 Available Gauge Variants

All variants contain the same complete set of generated size files (see [Generated Files](#generated-files) below). The visual style is determined by the source `gauge_inlay_thorne01.tga`.

### **[Thorne/](Thorne/)** ⭐ **ACTIVE DEFAULT**

**Visual Style**: Modern blue gradients with transparency  
**Source**: Infiniti-Blue (modified)

**Features**:
- Clean smooth fills with subtle gradients
- Dark line variant for XP progression depth
- Optimized for thorne_drak color palette

**Best For**: Players who prefer modern, polished gauge aesthetics

---

### **[Bars/](Bars/)**

**Visual Style**: Solid bar-style gauges

**Features**:
- Simple, clean bar appearance
- High contrast for easy reading
- Minimal visual effects

**Best For**: Players who prefer straightforward, no-frills gauges

---

### **[Basic/](Basic/)**

**Visual Style**: Classic EverQuest default appearance  
**Source**: Default UI

**Features**:
- Traditional EQ look and feel
- Familiar to veteran players
- Lightweight texture

**Best For**: Players who want classic EQ aesthetics

**⚠️ Note**: Source texture is 100px wide (3px narrower than all other variants) — may require position adjustments in window XML after switching.

---

### **[Bubbles/](Bubbles/)**

**Visual Style**: Bubble/spherical gauge styling

**Features**:
- Rounded, bubble-like appearance
- Playful visual aesthetic
- Distinct from traditional bar gauges

**Best For**: Players who want unique gauge visuals

---

### **[Grid/](Grid/)**

**Visual Style**: Grid-overlay gauge styling

**Features**:
- Grid line pattern over fills
- Structured, technical appearance
- Strong visual definition

**Best For**: Players who want a more tactical information display

---

### **[Light Bubbles/](Light%20Bubbles/)**

**Visual Style**: Lighter variant of bubble gauges

**Features**:
- Softer, lighter color palette
- Less visually prominent
- Subtle gauge presence

**Best For**: Players who prefer understated UI elements

---

### **[Oval/](Oval/)**

**Visual Style**: Oval/pill-shaped gauge styling

**Features**:
- Softer rounded edges
- Organic gauge shape
- Distinct from traditional rectangular bars

**Best For**: Players who prefer a more stylized, shaped gauge

---

## 🗂️ Included Files Per Variant

Every variant directory contains the same complete set of pre-built texture files:

| File | Dimensions | Type | Description |
|------|-----------|------|-------------|
| `gauge_inlay_thorne01.tga` | ~103×32 | Standard | Standard 8px gauge |
| `gauge_inlay120_thorne01.tga` | 120×32 | Wide | 120px wide standard |
| `gauge_inlay150_thorne01.tga` | 150×32 | Wide | 150px wide standard |
| `gauge_inlay120t_thorne01.tga` | 120×64 | Tall | 120px wide, 16px tall sections |
| `gauge_inlay150t_thorne01.tga` | 150×64 | Tall | 150px wide tall |
| `gauge_inlay230t_thorne01.tga` | 230×64 | Tall | 230px wide tall |
| `gauge_inlay240t_thorne01.tga` | 240×64 | Tall | 240px wide tall |
| `gauge_inlay250t_thorne01.tga` | 250×64 | Tall | 250px wide tall |
| `gauge_inlay260t_thorne01.tga` | 260×64 | Tall | 260px wide tall |

> **Developers**: Size variants are generated from `gauge_inlay_thorne01.tga` using `.bin/regen_gauges.py`. See the repository source for details.

## 🔧 How to Switch Gauge Variants

### Method 1: Copy Textures (Recommended)

1. **Choose your variant** from the list above
2. **Copy all `.tga` files** from that variant's folder into the main `thorne_drak/` directory:

   ```powershell
   # PowerShell — switch to Bubbles variant
   Copy-Item "thorne_drak\Options\Gauges\Bubbles\*.tga" "thorne_drak\"
   ```

   ```cmd
   rem Command Prompt
   copy "thorne_drak\Options\Gauges\Bubbles\*.tga" "thorne_drak\"
   ```

3. **Reload UI in-game**:
   ```
   /loadskin thorne_drak 1
   ```

### Method 2: Modify EQUI_Animations.xml

For advanced users who want to test a variant without copying files:

1. Open `thorne_drak/EQUI_Animations.xml`
2. Find gauge animation definitions (search for `A_GaugeBackground`)
3. Update `<Texture>` paths to point to variant subdirectory:

   ```xml
   <!-- Original -->
   <Texture>gauge_inlay_thorne01.tga</Texture>
   
   <!-- Updated to use Bubbles variant -->
   <Texture>Options/Gauges/Bubbles/gauge_inlay_thorne01.tga</Texture>
   ```

4. Reload UI in-game

## 📐 Technical Specifications

### Standard Gauge Layout (gauge_inlay_thorne01.tga - 103x32 or 100x32)

All standard gauge textures use a stacked vertical layout with 8px slices:

| Component | Y Position | Height | Animation Name | Purpose |
|-----------|------------|--------|----------------|---------|
| Background | 0 | 8px | `A_GaugeBackground` | Gauge background track |
| Fill | 8 | 8px | `A_GaugeFill` | Colored fill (HP/Mana) |
| Lines | 16 | 8px | `A_GaugeLines` | Grid overlay lines |
| LinesFill | 24 | 8px | `A_GaugeLinesFill` | Combined lines+fill |

**Used By:**
- Stamina gauge (8px height)
- Pet Health gauge (8px height)

---

### Tall Gauge Layout (gauge_inlay120t_thorne01.tga - 120x64)

Available in **all variants** (auto-generated by regen script). Provides taller gauges for primary resources:

| Component | Y Position | Height | Animation Name | Purpose |
|-----------|------------|--------|----------------|--------|
| Background | 0 | 16px | `A_GaugeBackground_Tall` | Tall gauge background |
| Fill | 16 | 16px | `A_GaugeFill_Tall` | Tall colored fill |
| Lines | 32 | 16px | `A_GaugeLines_Tall` | Grid overlay lines |
| LinesFill | 48 | 16px | `A_GaugeLinesFill_Tall` | Combined lines+fill |

**Used By:**
- HP gauge (16px height)
- Mana gauge (16px height)
- Experience gauge (16px height, with DrawLinesFill)
- AA Experience gauge (16px height, with DrawLinesFill)

---

## 📝 Width Compatibility Notes

### 103px Variants

- **Variants**: Thorne, Bars, Bubbles, Grid, Light Bubbles, Oval
- **Compatibility**: Matches current Thorne UI gauge positioning
- **No adjustments needed** when switching between these variants

### 100px Variants

- **Variants**: Basic (default UI source)
- **Compatibility**: 3px narrower than Thorne standard
- **May require position adjustments** in Player/Pet/Group windows
- Test thoroughly after switching

**Recommendation**: Stick with 103px variants unless you specifically want the classic EQ look.

---

## 🎮 Current Active Configuration

**File**: [EQUI_Animations.xml](EQUI_Animations.xml)

The animations file in this directory contains gauge animation definitions that reference `gauge_inlay_thorne01.tga`. By default, this points to textures in the main `thorne_drak/` directory, which should contain your chosen variant.

**Active Variant**: Thorne (default)

**Gauge Assignments:**
- **HP**: 16px tall gauge, blue gradient, no lines
- **Mana**: 16px tall gauge, blue gradient, no lines
- **Experience**: 16px tall gauge, blue gradient, dark lines
- **Stamina**: 8px standard gauge
- **Pet Health**: 8px standard gauge

---

## 🔍 Creating Custom Variants

To create your own gauge texture variant:

1. **Create subdirectory**: `Options/Gauges/YourVariantName/`
2. **Extract gauge textures** from source UI (see extraction guide below)
3. **Save as** `gauge_inlay_thorne01.tga` in your new variant directory
4. **Copy to thorne_drak/** to test:
   ```powershell
   Copy-Item "thorne_drak\Options\Gauges\YourVariantName\*.tga" "thorne_drak\"
   ```
5. **Test** in-game: `/loadskin thorne_drak 1`

> **Developers (repo clone)**: Run `regen_gauges YourVariantName` to auto-generate all size variants from the source texture.

### Gauge Extraction Guide

**From another UI:**

1. Open source UI's `EQUI_Animations.xml`
2. Find `A_GaugeBackground` animation
3. Note texture file and coordinates:
   - `<Texture>` - Source filename
   - `<Location>` - X/Y position
   - `<Size>` - Width/Height (CX/CY)
4. Open source texture in image editor
5. Extract the gauge region (typically 100x32 or 103x32)
6. Save as `gauge_inlay_thorne01.tga` in your variant directory

**Python Script** (if available):
```bash
python .bin/extract_gauge_texture.py --source <ui_name> --output Options/Gauges/YourVariant/
```

---

## 📚 Related Documentation

- **[../../EQUI_Animations.xml](../../EQUI_Animations.xml)** - Main animations file (in thorne_drak root)
- **[../Player/README.md](../Player/README.md)** - Player window gauge usage
- **[../Pet/README.md](../Pet/README.md)** - Pet window gauge configuration
- **[../../.docs/STANDARDS.md](../../.docs/STANDARDS.md)** - Gauge styling standards

---

## 🚀 Performance Considerations

- **Texture Loading**: Only textures in main thorne_drak directory are loaded
- **Variant Storage**: Subdirectories don't impact performance (textures not loaded until copied)
- **Memory Impact**: Each gauge texture (~32-64 KB) has minimal impact
- **Switching Speed**: Copying textures is instant; UI reload takes 1-2 seconds
- **Animation Frame Rate**: Gauge updates sync with EQType value changes

**Best Practice**: Keep only your active variant in main thorne_drak directory for optimal performance.

---

## 🛠️ Troubleshooting

### Gauge Not Appearing

**Symptom**: Gauge shows as blank or missing  
**Solution**:
1. Verify `gauge_inlay_thorne01.tga` exists in main thorne_drak directory
2. Check EQUI_Animations.xml has correct `<TextureInfo>` entry
3. Ensure texture path in animations matches filename exactly
4. Reload UI: `/loadskin thorne_drak 1`

### Wrong Gauge Style Showing

**Symptom**: Different gauge style than expected  
**Solution**:
1. Check which `gauge_inlay_thorne01.tga` is in main thorne_drak directory
2. Copy desired variant from subdirectory
3. Overwrite existing texture in main directory
4. Reload UI

### Gauge Misaligned After Switching

**Symptom**: Gauge position shifted after changing variants  
**Solution**:
1. Check texture width (100px vs 103px)
2. If using Basic (100px), adjust gauge X positions in window XML
3. Stick with 103px variants (Thorne, Bars, Bubbles) for consistent positioning

---

## 📋 Quick Reference

### Switching to a Variant

```powershell
# PowerShell
Copy-Item "thorne_drak\Options\Gauges\Bubbles\*.tga" "thorne_drak\"
```

```cmd
rem Command Prompt
copy "thorne_drak\Options\Gauges\Bubbles\*.tga" "thorne_drak\"
```

### In-Game Reload

```
/loadskin thorne_drak 1
```

### For Developers (Repo Clone)

```bash
# Rebuild all size variants for all 7 gauges
regen_gauges

# Rebuild a single variant (auto-copies to thorne_drak/ and thorne_dev/)
regen_gauges Thorne
```

---

## 📦 Repository Information

**Repository**: [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Documentation**: [Thorne UI Standards](.docs/STANDARDS.md)  
**Issues**: [GitHub Issues](https://github.com/draknarethorne/thorne-ui/issues)

---

*Maintainer: Draknare Thorne*  
*Last Updated: February 21, 2026*  
*Status: ✅ Active - 7 Variants, Full Size Generation*
