# UI Standardization Roadmap

> **Purpose**: Identify cross-codebase standardization opportunities to improve long-term maintenance and consistency across PlayerWindow, TargetWindow, and other UI components.

**Status**: Analysis phase - identifying patterns and proposing refactoring roadmap

---

## 1. Gauge System Standardization

### Current State: Highly Repeated Gauge Patterns

Every window that displays health/mana/stamina/XP repeats the entire gauge XML block:

```xml
<Gauge item="IdentifierHP_Gauge">
  <ScreenID>IdentifierHP</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>2</X><Y>16</Y></Location>
  <Size><CX>122</CX><CY>8</CY></Size>
  <GaugeOffsetX>0</GaugeOffsetX>
  <GaugeOffsetY>0</GaugeOffsetY>
  <TextOffsetY>-50</TextOffsetY>
  <Style_VScroll>false</Style_VScroll>
  <Style_HScroll>false</Style_HScroll>
  <Style_Transparent>false</Style_Transparent>
  <FillTint><R>255</R><G>0</G><B>0</B></FillTint>
  <LinesFillTint><R>180</R><G>70</G><B>70</B></LinesFillTint>
  <DrawLinesFill>false</DrawLinesFill>
  <EQType>1</EQType>
  <GaugeDrawTemplate><Fill>A_GaugeFill</Fill></GaugeDrawTemplate>
</Gauge>
```

**Problem**: 
- 20+ files with identical gauge structures
- Any change to base gauge pattern requires updating multiple files
- Different identifier naming schemes (some use `TW_`, `PW_`, `IW_` prefixes inconsistently)
- Hard to ensure consistency across variants

**Opportunities**:

#### Option A: XML Template Includes (Complex, Advanced)
- Create shared gauge templates (if supported by EQUI XML parser)
- Define once, reference many times
- **Risk**: Requires validation that EQ client supports includes
- **Benefit**: Single source of truth for gauge structures

#### Option B: Code Generation Pattern (Medium effort)
- Create Python script to generate gauge XML blocks from config file
- Feed into build process
- Config file format:
  ```yaml
  windows:
    PlayerWindow:
      gauges:
        - id: HP
          eqtype: 1
          size: [122, 8]
          location: [2, 16]
          colors: [255, 0, 0]
          animation: A_GaugeFill
        - id: Mana
          eqtype: 2
          size: [122, 8]
          location: [2, 43]
          colors: [100, 150, 255]
  ```
- Output: Consistent XML across all windows
- **Benefit**: Maintains DRY principle, easier updates
- **Risk**: Requires build process setup

#### Option C: CSS-like Constants System (Immediate, Low-hanging fruit)
- Create `EQUI_GaugeConstants.xml` or separate constant file
- Define reusable gauge "classes" with standard properties
- **Current Best Option**: Low risk, high value

---

## 2. Window Position/Size Standardization

### Current State: Inconsistent Definitions

Window sizes and default positions vary:

| File | Window Size | Default X | Default Y |
|------|------------|-----------|-----------|
| EQUI_PlayerWindow.xml | 234×140 | Varies | Varies |
| EQUI_TargetWindow.xml | 260×78 | Varies | Varies |
| EQUI_BuffWindow.xml | 160×160 | Varies | Varies |

**Problem**:
- Default positions not documented consistently
- No central registry of "standard" window sizes
- Difficult to maintain UI layout contracts

**Opportunity**:
- Create [WINDOW-REGISTRY.md](WINDOW-REGISTRY.md)
- Document:
  - Standard dimensions (width × height)
  - Default screen position (X, Y)
  - Minimum/maximum sizes allowed
  - Rationale for each dimension
  - Associated animations/textures

---

## 3. Label/Text Styling Standardization

### Current State: Repeated Text Color Definitions

Every window that displays text repeats RGB color definitions:

```xml
<!-- Appears 50+ times across codebase -->
<R>255</R><G>255</G><B>255</B>  <!-- White -->
<R>200</R><G>200</G><B>200</B>  <!-- Light gray -->
<R>100</R><G>100</G><B>100</B>  <!-- Dark gray -->
```

**Problem**:
- No central color reference
- Risk of RGB values drifting across files
- If we want to adjust a color (e.g., "player white"), must update 20+ files
- Hard to know what each RGB represents

**Opportunity**:

#### Create Color Constant System

```xml
<!-- EQUI_ColorConstants.xml -->
<ColorPalette>
  <Color name="UI_White"><R>255</R><G>255</G><B>255</B></Color>
  <Color name="UI_LightGray"><R>200</R><G>200</G><B>200</B></Color>
  <Color name="UI_DarkGray"><R>100</R><G>100</G><B>100</B></Color>
  <Color name="Gauge_PlayerHP"><R>255</R><G>0</G><B>0</B></Color>
  <Color name="Gauge_PlayerMana"><R>100</R><G>150</G><B>255</B></Color>
  <!-- ... etc -->
</ColorPalette>
```

Then reference in files:
```xml
<FillTint><Color ref="Gauge_PlayerHP"/></FillTint>
```

**Status**: Requires parser support validation

---

## 4. Animation Reference Standardization

### Current State: Inconsistent Animation Naming

Same animations referenced with different naming schemes:

| Animation | Used as | Instances |
|-----------|---------|-----------|
| `A_GaugeFill` | Fill animation | Player HP, Mana, Stamina, XP, AA, Pet |
| `A_GaugeLinesFill` | LinesFill animation | Mana tick (compact) |
| `A_GaugeLinesFill_Tall` | LinesFill animation | Mana tick (player window) |

**Problem**:
- Animation references scattered across many files
- Hard to validate which animations are actually used
- No documentation of animation purpose/compatibility

**Opportunity**:
- Create [ANIMATION-REGISTRY.md](ANIMATION-REGISTRY.md)
- Document:
  - Animation name and purpose
  - Dimensions (width × height) 
  - Compatible gauges/element types
  - Usage count across repository
  - Texture source reference

---

## 5. Gauge Sizing and Spacing Patterns

### Current State: Manual Spacing Calculations

Every gauge adds manual spacing:

```xml
<!-- Gauge sizing: 8px height -->
<!-- Next element: manually calculate Y = previous_Y + previous_height + gap -->
```

**Opportunity**:
Document standardized spacing rules:

```markdown
## Standard Gauge Spacing

### Compact Windows (8px gauges)
- Vertical gap between gauges: -2px (slight overlap)
- This allows line fills to display close but separate

### Tall Windows (15px gauges)  
- Vertical gap between gauges: 3px
- Pattern: 15px + 3px = 18px total spacing

### Mana Tick Special Case
- Always overlaps with mana gauge by 1-2px
- Visual line displays at bottom of overlap zone
```

---

## 6. Screen/Zone Divisions Consistency

### Current State: Inconsistent Zone Naming

Different windows use different zone division schemes:

```xml
<!-- PlayerWindow -->
<Screen item="PlayerWindow_MainPage">  <!-- All-in-one -->

<!-- InventoryWindow -->
<Screen item="IW_LeftZone">             <!-- Split zones -->
<Screen item="IW_RightZone">

<!-- GroupWindow -->
<Screen item="GroupWindow_Main">        <!-- Monolithic -->
```

**Opportunity**:
- Establish zone division guidelines
- Document when to use monolithic vs. split-zone approach
- Create templates for common patterns

---

## 7. Prefix Conventions - Already Standardized ✅

### Current State: Generally Good

Prefixes established:
- `PW_` = PlayerWindow element
- `TW_` = TargetWindow element
- `IW_` = InventoryWindow element
- `GW_` = GroupWindow element
- `MW_` = MerchantWindow element

**Status**: Consistent, documented in STANDARDS.md ✅

---

## 8. Label/Value Naming Patterns

### Current State: Mostly Consistent

Established patterns:
- `PW_Label_*` for constant labels
- `PW_Value_*` for dynamic value displays
- `PW_*_Pct` for percentage displays
- `PW_*_PctSign` for percentage symbols ("%")

**Status**: Documented in STANDARDS.md, some opportunities for expansion

---

## Implementation Priority Matrix

| Opportunity | Effort | Value | Complexity | Priority |
|------------|--------|-------|-----------|----------|
| **Gauge Constants Doc** | Low | High | Low | 🔴 **NOW** |
| **Window Registry Doc** | Low | Medium | Low | 🟠 HIGH |
| **Animation Registry Doc** | Low | Medium | Low | 🟠 HIGH |
| **Gauge Spacing Rules Doc** | Low | Medium | Low | 🟠 HIGH |
| **RGB Color Constants** | High | High | High | 🟡 MEDIUM |
| **XML Template System** | Very High | Very High | Very High | 🟢 FUTURE |
| **Code Generation** | Very High | High | High | 🟢 FUTURE |

---

## Recommended Next Steps (Phase 1)

### 1. **Gauge Properties Reference** [IMMEDIATE]
Create `GAUGE-PROPERTIES-REFERENCE.md`:
- Table of all gauge standard properties
- Default values template
- Copy-paste ready examples

### 2. **Window Dimensions Registry** [IMMEDIATE]
Create `WINDOW-DIMENSIONS.md`:
- Table: Window Name | Width | Height | Purpose | Default Location
- Rationale for each dimension
- Links to files implementing each window

### 3. **Animation Compatibility Matrix** [IMMEDIATE]
Create `ANIMATION-COMPATIBILITY.md`:
- Table: Animation | Dimensions | Compatible EQTypes | Files Using
- Document which animations work with which gauges
- Warn about mismatches

### 4. **Spacing Standards Reference** [IMMEDIATE]
Expand STANDARDS.md with:
- Vertical spacing rules for different window types
- Horizontal alignment rules
- Gap standardization (when to use -2px overlap vs. 3px gap)

---

## Long-Term Vision (Phase 2+)

### Build System Integration
Once standardization documented:
1. Create Python build script that validates XML consistency
2. Auto-generate certain XML sections from config
3. Validate that all gauges follow standard patterns
4. Warn on deviations

### Validation Rules
```
- All HP gauges must be RGB(255, 0, 0)
- All mana gauges must be RGB(100, 150, 255)
- All standard gauges must be 103×8 or 122×8
- All tall gauges must be 120×15
- All Label text must use approved font sizes (9, 11, 12 only)
```

---

## Questions for Review

Before proceeding to implementation, consider:

1. **Should we create a master constants file** (like `EQUI_UIConstants.xml`) that centralizes all reusable values?

2. **How much coordination is needed** between PlayerWindow, TargetWindow, BuffWindow, etc. regarding gauge properties?

3. **Should variants (Options subdirectory files) inherit from main** or stay independently documented?

4. **For future expansion**, would a YAML config + build pipeline be worth the setup effort?

5. **Should we document "why"** certain dimensions were chosen (e.g., why is TargetWindow 260×78 exactly)?

---

## Related Files

- Current standards: [STANDARDS.md](STANDARDS.md)
- Gauge system: [Gauge Sizing Standards Table](STANDARDS.md#standard-gauge-sizes)
- Color palette: [Gauge Fill Colors](STANDARDS.md#gauge-fill-colors)

