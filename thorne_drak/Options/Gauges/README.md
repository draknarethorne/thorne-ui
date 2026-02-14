# Gauge Options

**Directory**: `thorne_drak/Options/Gauges/`  
**Version**: 2.0.0  
**Last Updated**: February 11, 2026  
**Status**: ✅ Active - Subdirectory-Based Organization  
**Author**: Draknare Thorne

---

## 📋 Overview

This directory contains gauge texture variants for HP, Mana, Stamina, Experience, and Pet Health bars used throughout Thorne UI. Each subdirectory contains a complete gauge texture set with a distinct visual style.

**Key Features:**
- **5 Visual Styles**: Multiple gauge aesthetics to match your preference
- **Subdirectory Organization**: Each variant isolated in its own folder
- **Standard Heights**: 8px (stamina/pet) and 15px (HP/Mana/XP) gauge support
- **Easy Switching**: Copy desired variant to main thorne_drak directory
- **Shared Animation Definitions**: All variants use same EQUI_Animations.xml

---

## 🎨 Available Gauge Variants

### **[Thorne/](Thorne/)** ⭐ **ACTIVE DEFAULT**

**Visual Style**: Modern blue gradients with transparency  
**Source**: Infiniti-Blue (modified)  
**Files**:
- `gauge_pieces01.tga` (103x32) - Standard 8px gauges
- `gauge_120t_pieces01.tga` (120x64) - Tall 15px gauges

**Features**:
- Clean smooth fills with subtle gradients
- Dark line variant for XP progression depth
- Optimized for thorne_drak color palette
- Both standard and tall gauge support

**Best For**: Players who prefer modern, polished gauge aesthetics

---

### **[Bars/](Bars/)**

**Visual Style**: Solid bar-style gauges  
**Source**: TBD  
**Files**:
- `gauge_pieces01.tga` (103x32)

**Features**:
- Simple, clean bar appearance
- High contrast for easy reading
- Minimal visual effects

**Best For**: Players who prefer straightforward, no-frills gauges

---

### **[Basic/](Basic/)**

**Visual Style**: Classic EverQuest default appearance  
**Source**: Default UI  
**Files**:
- `gauge_pieces01.tga` (100x32)

**Features**:
- Traditional EQ look and feel
- Familiar to veteran players
- Lightweight texture

**Best For**: Players who want classic EQ aesthetics

**⚠️ Note**: 100px width (3px narrower than Thorne variant) - may require position adjustments

---

### **[Bubbles/](Bubbles/)**

**Visual Style**: Bubble/spherical gauge styling  
**Source**: TBD  
**Files**:
- `gauge_pieces01.tga` (103x32)

**Features**:
- Rounded, bubble-like appearance
- More playful visual aesthetic
- Distinct from traditional bar gauges

**Best For**: Players who want unique gauge visuals

---

### **[Light Bubbles/](Light Bubbles/)**

**Visual Style**: Lighter variant of bubble gauges  
**Source**: TBD  
**Files**:
- `gauge_pieces01.tga` (103x32)

**Features**:
- Softer, lighter color palette
- Less visually prominent
- Subtle gauge presence

**Best For**: Players who prefer understated UI elements

---

## 🔧 How to Switch Gauge Variants

### Method 1: Copy Textures (Recommended)

1. **Choose your variant** from the subdirectories above
2. **Copy the texture file(s)** to main thorne_drak directory:
   
   ```bash
   # Example: Switch to Bubbles variant
   cp "thorne_drak/Options/Gauges/Bubbles/gauge_pieces01.tga" "thorne_drak/"
   ```

3. **Reload UI in-game**:
   ```
   /loadskin thorne_drak 1
   ```

### Method 2: Modify EQUI_Animations.xml

For advanced users who want to test without copying files:

1. Open `thorne_drak/EQUI_Animations.xml`
2. Find gauge animation definitions (search for `A_GaugeBackground`)
3. Update `<Texture>` paths to point to variant subdirectory:

   ```xml
   <!-- Original -->
   <Texture>gauge_pieces01.tga</Texture>
   
   <!-- Updated to use Bubbles variant -->
   <Texture>Options/Gauges/Bubbles/gauge_pieces01.tga</Texture>
   ```

4. Reload UI in-game

---

## 📐 Technical Specifications

### Standard Gauge Layout (gauge_pieces01.tga - 103x32 or 100x32)

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

### Tall Gauge Layout (gauge_120t_pieces01.tga - 120x64)

Only available in **Thorne/** variant. Provides taller gauges for primary resources:

| Component | Y Position | Height | Animation Name | Purpose |
|-----------|------------|--------|----------------|---------|
| Background | 0 | 15px | `A_GaugeBackground_Tall` | Tall gauge background |
| Fill | 15 | 15px | `A_GaugeFill_Tall` | Tall colored fill |
| Lines | 30 | 15px | `A_GaugeLines_Tall` | Grid overlay lines |
| LinesFill | 45 | 15px | `A_GaugeLinesFill_Tall` | Combined lines+fill |

**Used By:**
- HP gauge (15px height)
- Mana gauge (15px height)
- Experience gauge (15px height, with DrawLinesFill)
- AA Experience gauge (15px height, with DrawLinesFill)

---

## 📝 Width Compatibility Notes

### 103px Variants
- **Variants**: Thorne, Bars, Bubbles, Light Bubbles
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

The animations file in this directory contains gauge animation definitions that reference `gauge_pieces01.tga`. By default, this points to textures in the main `thorne_drak/` directory, which should contain your chosen variant.

**Active Variant**: Thorne (default)

**Gauge Assignments:**
- **HP**: 15px tall gauge, blue gradient, no lines
- **Mana**: 15px tall gauge, blue gradient, no lines
- **Experience**: 15px tall gauge, blue gradient, dark lines
- **Stamina**: 8px standard gauge
- **Pet Health**: 8px standard gauge

---

## 🔍 Creating Custom Variants

To create your own gauge texture variant:

1. **Create subdirectory**: `Options/Gauges/YourVariantName/`
2. **Extract gauge textures** from source UI (see extraction guide below)
3. **Save as** `gauge_pieces01.tga` (and optionally `gauge_120t_pieces01.tga`)
4. **Test** by copying to main thorne_drak directory

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
6. Save as `gauge_pieces01.tga` in your variant directory

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
1. Verify `gauge_pieces01.tga` exists in main thorne_drak directory
2. Check EQUI_Animations.xml has correct `<TextureInfo>` entry
3. Ensure texture path in animations matches filename exactly
4. Reload UI: `/loadskin thorne_drak 1`

### Wrong Gauge Style Showing

**Symptom**: Different gauge style than expected  
**Solution**:
1. Check which `gauge_pieces01.tga` is in main thorne_drak directory
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

```bash
# Windows (PowerShell)
Copy-Item "thorne_drak/Options/Gauges/Bubbles/gauge_pieces01.tga" "thorne_drak/"

# Windows (Command Prompt)
copy "thorne_drak\Options\Gauges\Bubbles\gauge_pieces01.tga" "thorne_drak\"

# Linux/Mac
cp thorne_drak/Options/Gauges/Bubbles/gauge_pieces01.tga thorne_drak/
```

### In-Game Reload

```
/loadskin thorne_drak 1
```

---

## 📦 Repository Information

**Repository**: [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Documentation**: [Thorne UI Standards](.docs/STANDARDS.md)  
**Issues**: [GitHub Issues](https://github.com/draknarethorne/thorne-ui/issues)

---

*Maintainer: Draknare Thorne*  
*Last Updated: February 11, 2026*  
*Status: ✅ Subdirectory Organization Complete*
