# Stat Icons Implementation Guide

**Project**: Thorne UI  
**Phase**: Stat Icons Integration  
**Status**: Research & Planning  
**Date**: February 6, 2026

---

## 🎯 Objective

Integrate stat icons (STR, STA, AGI, DEX, WIS, INT, CHA) into Thorne UI windows to provide visual representations of character statistics, improving usability and visual polish.

**Implementation Priority:**

1. **Primary Target: Inventory Window**
   - Most space available for comprehensive display
   - Uses **[Icon] Text Value** format (all three elements)
   - Shows both icon and text label for maximum clarity
   - Example: `[STR Icon] STR  150`

2. **Secondary Targets: Other Windows**
   - Player Window, Actions Window, Merchant Window
   - May use **[Icon] Value** format (icon + value only, no text)
   - Saves space in more compact layouts
   - Example: `[STR Icon] 150`
   - Decision made based on visual results during implementation

3. **Always Provide Options Variants**
   - Text-only (current baseline - no icons)
   - Icon-only (icon + value, no text labels)
   - Icon + Text (icon + text label + value)
   - Users choose based on preference and screen space

**Approach:** Iterative and flexible - assess visual results as we implement and adjust based on what looks best in each window context.

## 📋 Design Philosophy

### Self-Contained Window Definitions

**Key Principle**: Window .xml files should be as self-sustainable as possible.

- **Prefer**: Define textures and animations directly in the window .xml file
- **Avoid**: Adding custom definitions to EQUI_Animations.xml
- **Rationale**: 
  - Easier to understand window implementations (all resources in one file)
  - Simpler to create Options variants (no cross-file dependencies)
  - Better encapsulation (window owns its resources)
  - Reduces EQUI_Animations.xml bloat

**Trade-off**: Some texture definitions may be duplicated across multiple windows, but this is acceptable for the encapsulation benefits.

---

## 🔍 Research Phase

### 1. Source Assets Discovery

**Available Texture Files** (from community UIs):

```
duxaUI/window_pieces22.tga  - 256×256 RGBA (primary candidate for stat icons)
duxaUI/window_pieces21.tga  - 256×256 RGBA (check for additional icons)
duxaUI/window_pieces23.tga  - 256×256 RGBA (check for additional icons)
vert/mini_inv.tga           - 256×256 RGBA (alternative icon source)
```

**Investigation Steps**:

1. **Visual Inspection**
   ```bash
   # Open each file in an image viewer to identify icon locations
   # Look for: STR, STA, AGI, DEX, WIS, INT, CHA icons
   # Document: icon dimensions, grid layout, spacing
   ```

2. **Icon Mapping**
   - Measure icon dimensions (likely 16×16 or 20×20 pixels)
   - Document X/Y coordinates for each stat icon
   - Note any background/border elements around icons
   - Check for pressed/hover states if applicable

3. **Create Icon Map Document**
   ```
   Example format:
   window_pieces22.tga layout:
   - STR icon: X=0,   Y=0,   Size=16×16
   - STA icon: X=16,  Y=0,   Size=16×16
   - AGI icon: X=32,  Y=0,   Size=16×16
   ... etc
   ```

### 2. Existing Implementation Research

**Check for existing icon usage**:

```bash
# Search duxaUI XML files (if available) for stat icon patterns
grep -r "window_pieces22\|ICON_STR\|StaticAnimation.*stat" duxaUI/ 2>/dev/null

# Check default EQ UI for any icon bindings
grep -r "EQType.*icon\|stat.*icon" default/EQUI_*.xml
```

---

## 📐 Implementation Approach

### Pattern 1: Inline Texture Definition (Preferred)

Define textures directly in the window .xml file using `<Ui2DAnimation>` and `<TextureInfo>`.

**Example: Player Window with STR Icon**

```xml
<?xml version="1.0"?>
<XML ID="EQInterfaceDefinitionLanguage">
  <Schema xmlns="EverQuestData" xmlns:dt="EverQuestDataTypes"/>
  
  <!-- ===================================================================== -->
  <!-- TEXTURE DEFINITIONS (Self-Contained) -->
  <!-- ===================================================================== -->
  
  <!-- Define the stat icons texture (dimensions from window_pieces22.tga) -->
  <TextureInfo item="window_pieces22.tga">
    <Size>
      <CX>256</CX>
      <CY>256</CY>
    </Size>
  </TextureInfo>
  
  <!-- STR Icon Animation -->
  <Ui2DAnimation item="ICON_STR">
    <Cycle>false</Cycle>
    <Frames>
      <Texture>window_pieces22.tga</Texture>
      <Location>
        <X>0</X>    <!-- Adjust based on actual texture layout -->
        <Y>0</Y>    <!-- Adjust based on actual texture layout -->
      </Location>
      <Size>
        <CX>16</CX> <!-- Icon width -->
        <CY>16</CY> <!-- Icon height -->
      </Size>
      <Duration>1000</Duration>
    </Frames>
  </Ui2DAnimation>
  
  <!-- STA Icon Animation -->
  <Ui2DAnimation item="ICON_STA">
    <Cycle>false</Cycle>
    <Frames>
      <Texture>window_pieces22.tga</Texture>
      <Location>
        <X>16</X>   <!-- Adjust based on actual texture layout -->
        <Y>0</Y>    <!-- Adjust based on actual texture layout -->
      </Location>
      <Size>
        <CX>16</CX>
        <CY>16</CY>
      </Size>
      <Duration>1000</Duration>
    </Frames>
  </Ui2DAnimation>
  
  <!-- Repeat for AGI, DEX, WIS, INT, CHA... -->
  
  <!-- ===================================================================== -->
  <!-- WINDOW LAYOUT -->
  <!-- ===================================================================== -->
  
  <Screen item="PW_StatsZone">
    <ScreenID>PW_StatsZone</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location><X>10</X><Y>100</Y></Location>
    <Size><CX>120</CX><CY>200</CY></Size>
    
    <!-- STR Display with Icon -->
    <Pieces>PW_STR_Icon PW_STR_Label PW_STR_Value</Pieces>
    
    <StaticAnimation item="PW_STR_Icon">
      <ScreenID>PW_STR_Icon</ScreenID>
      <RelativePosition>true</RelativePosition>
      <Location><X>0</X><Y>0</Y></Location>
      <Animation>ICON_STR</Animation>
    </StaticAnimation>
    
    <Label item="PW_STR_Label">
      <ScreenID>PW_STR_Label</ScreenID>
      <RelativePosition>true</RelativePosition>
      <Location><X>18</X><Y>0</Y></Location> <!-- Offset from icon -->
      <Size><CX>30</CX><CY>14</CY></Size>
      <Text>STR</Text>
      <Font>3</Font>
      <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
    </Label>
    
    <Label item="PW_STR_Value">
      <ScreenID>PW_STR_Value</ScreenID>
      <EQType>5</EQType> <!-- STR stat -->
      <RelativePosition>true</RelativePosition>
      <Location><X>50</X><Y>0</Y></Location>
      <Size><CX>40</CX><CY>14</CY></Size>
      <Font>3</Font>
      <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
      <AlignRight>true</AlignRight>
    </Label>
  </Screen>
  
</XML>
```

### Pattern 2: Icons Only (No Text Labels)

For a more visual, icon-heavy approach:

```xml
<StaticAnimation item="PW_STR_Icon">
  <ScreenID>PW_STR_Icon</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>0</X><Y>0</Y></Location>
  <Animation>ICON_STR</Animation>
  <TooltipReference>STR</TooltipReference> <!-- Tooltip shows "STR" on hover -->
</StaticAnimation>

<Label item="PW_STR_Value">
  <ScreenID>PW_STR_Value</ScreenID>
  <EQType>5</EQType>
  <RelativePosition>true</RelativePosition>
  <Location><X>18</X><Y>1</Y></Location> <!-- Right next to icon -->
  <Size><CX>40</CX><CY>14</CY></Size>
  <Font>3</Font>
  <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
</Label>
```

---

## 📁 File Organization

### Required Files

**1. Copy Texture Assets to thorne_drak/**

```bash
# Copy stat icon texture file(s) to thorne_drak
cp duxaUI/window_pieces22.tga thorne_drak/stat_icons.tga

# Alternative: Use original filename to maintain consistency
cp duxaUI/window_pieces22.tga thorne_drak/window_pieces22.tga
```

**Recommendation**: Rename to `stat_icons.tga` for clarity and to avoid confusion with window border textures.

**2. Modify Window .xml Files**

Each window that uses stat icons should:
1. Define `TextureInfo` for the stat icons texture
2. Define `Ui2DAnimation` elements for each stat icon
3. Use `StaticAnimation` elements in the layout to display icons

**Target Windows for Stat Icons**:
- `EQUI_Inventory.xml` - **PRIMARY TARGET** (shows all stats, most space available)
- `EQUI_PlayerWindow.xml` - Secondary (compact layout, may use icon+value only)
- `EQUI_ActionsWindow.xml` - Secondary (Player Info tab, assess space constraints)
- `EQUI_MerchantWnd.xml` - Secondary (Player Info tab if applicable, assess space)

**3. Create Options Variants**

```
thorne_drak/Options/Inventory/
├── Default/                    # Text labels only (current - no icons)
├── Icons and Labels/           # [Icon] Text Value format (new default after implementation)
├── Icons Only/                 # [Icon] Value format (compact, no text labels)
└── README.md

thorne_drak/Options/Player/
├── Default/                    # Current text-only version
├── With Stat Icons/            # [Icon] Value format (compact for player window)
└── README.md

# Similar structure for Actions, Merchant windows as needed
```

**Format Guidelines by Window:**
- **Inventory**: [Icon] Text Value (e.g., `[STR Icon] STR  150`) - most space, clearest display
- **Player**: [Icon] Value or [Icon] Text Value (decide during implementation based on layout)
- **Actions/Merchant**: [Icon] Value (compact, save space) or provide both as variants

---

## 🧪 Testing Strategy

### Phase 1: Single Window Prototype

1. **Choose Inventory Window** as initial implementation target (most space, clearest use case)
2. **Copy texture file** to thorne_drak/
3. **Add texture definitions** at top of EQUI_Inventory.xml
4. **Implement one stat icon** (e.g., STR) with [Icon] Text Value format as proof of concept
5. **Test in-game** to verify:
   - Icon displays correctly
   - Icon position is accurate
   - Text label displays properly
   - Value label still works with EQType binding
   - No texture loading errors
   - Visual spacing looks good with all three elements

### Phase 2: Complete Stat Set

1. Map all 7 stat icons (STR, STA, AGI, DEX, WIS, INT, CHA)
2. Implement all icons in Player Window
3. Adjust spacing/alignment for visual balance
4. Test with different stat values (low/high numbers)

### Phase 3: Multi-Window Rollout

1. Assess Inventory Window results - determine what worked well
2. Apply to Player Window with format decision based on space constraints
   - Try [Icon] Value format (no text label) and compare
3. Apply to Actions Window (Player Info tab)
   - Choose format based on available space
4. Apply to Merchant Window (Player Info tab if applicable)
   - Choose format based on available space
5. Verify consistency where applicable, allow variation where it makes sense
6. Document format decisions for each window

### Phase 4: Options Variants

1. Create "Icons Only" variant
2. Create "Icons and Labels" variant
3. Document each variant with screenshots
4. Test switching between variants

---

## 🎨 Design Considerations

### Layout Patterns

**Format 1: [Icon] Text Value** (Inventory Window - PRIMARY):
```
[Icon] STR  150
[Icon] STA  130
[Icon] AGI  120
[Icon] DEX  110
[Icon] WIS  140
[Icon] INT  160
[Icon] CHA  100
```
- Most comprehensive display
- Clear for all users
- Requires more horizontal space (~80-100px)

**Format 2: [Icon] Value** (Compact Windows - Player/Actions/Merchant):
```
[Icon] 150
[Icon] 130
[Icon] 120
[Icon] 110
[Icon] 140
[Icon] 160
[Icon] 100
```
- Space-efficient
- Icons provide visual identification
- Requires ~40-50px horizontal space
- Similar to duxaUI and vert approach

**Vertical Stack** (Common in most windows):
```
[Icon] STR  150
[Icon] STA  130
[Icon] AGI  120
[Icon] DEX  110
[Icon] WIS  140
[Icon] INT  160
[Icon] CHA  100
```

**Horizontal Compact** (Very space-constrained windows):
```
[Icon]150  [Icon]130  [Icon]120  [Icon]110
```

**Grid Layout** (If larger displays warrant it):
```
[Icon] STR 150    [Icon] WIS 140
[Icon] STA 130    [Icon] INT 160
[Icon] AGI 120    [Icon] CHA 100
[Icon] DEX 110
```

### Spacing Guidelines

- **Icon to Text**: 2-4px gap minimum
- **Icon to Value**: 8-12px gap for readability
- **Vertical Spacing**: Match existing label spacing (14-16px per row)
- **Icon Alignment**: Top-align icons with text baselines

### Color Coordination

- Consider tinting icons to match stat type (blue for mental stats, red for physical, etc.)
- Use `<FillTint>` on StaticAnimation if texture supports it
- Maintain consistency with gauge colors and existing theme

---

## 📊 Success Criteria

### Must Have
- ✅ Icons display correctly in at least one window (Player Window)
- ✅ No texture loading errors in logs
- ✅ Stat values still update correctly (EQType bindings intact)
- ✅ Visual alignment is clean and readable
- ✅ Texture file is properly sized and optimized

### Should Have
- ✅ Icons implemented in 3+ windows (Player, Inventory, Actions)
- ✅ At least one Options variant created (Icons Only or Icons+Labels)
- ✅ Documentation includes icon map with coordinates
- ✅ README.md files for each variant explain icon usage

### Nice to Have
- ✅ Custom tooltips on hover showing full stat name
- ✅ Consistent icon styling across all windows
- ✅ Variants for different icon preferences
- ✅ Icon size variants (16x16, 20x20, 24x24 if textures allow)

---

## 🚧 Known Limitations

1. **Texture File Size**: 256×256 textures are relatively large; consider impact on UI load times
2. **Icon Quality**: Source icons from duxaUI may not match Thorne UI visual style
3. **Stat Coverage**: Ensure all 7 primary stats have icons; AC/ATK may not have icons
4. **Screen Space**: Icons require more horizontal space than text-only labels

---

## 📝 Next Steps

### Immediate Actions

1. **Extract and examine texture files**
   - Open window_pieces22.tga in image viewer
   - Map icon locations and dimensions
   - Document in ICON-MAP.md in this directory

2. **Create prototype in Inventory Window**
   - Copy texture file to thorne_drak/
   - Add TextureInfo and Ui2DAnimation definitions to EQUI_Inventory.xml
   - Implement one stat icon (STR) with [Icon] Text Value format
   - Test in-game to verify icon displays, text label works, value binding works

3. **Expand to full stat set in Inventory**
   - Implement all 7 stat icons with [Icon] Text Value format
   - Adjust layout and spacing for visual balance
   - Verify all EQType bindings work correctly

4. **Create Inventory Options variants**
   - Default (text only - current baseline)
   - Icons and Labels (new implementation with [Icon] Text Value)
   - Icons Only ([Icon] Value format, no text labels)
   - Document each variant with README.md

5. **Assess and expand to other windows**
   - Review Inventory implementation results
   - Decide on format for Player Window ([Icon] Value vs [Icon] Text Value)
   - Apply to Actions Window with chosen format
   - Apply to Merchant Window if applicable
   - Create Options variants for each window as needed

### Long-Term

- Update `.docs/STANDARDS.md` with stat icon guidelines
- Document format decision rationale for each window
- Create reusable patterns for future icon integration

---

## 📚 Related Work

### TODO.md Items

This work relates to:
- **Stat Icons Integration** section in TODO.md
- Future work on visual polish and consistency
- Options variant system expansion

### Standards Documentation

Update `.docs/STANDARDS.md` with:
- Stat icon usage guidelines
- Icon sizing standards
- Layout patterns for icon + text displays
- Self-contained window resource guidelines

---

## 🔗 References

- `.docs/STANDARDS.md` - UI standards and patterns
- `.docs/technical/EQTYPES.md` - EQType reference (stat bindings)
- Community UIs: duxaUI, vert (source assets)
- Default EQ UI (baseline patterns)

---

**Maintainer**: Draknare Thorne  
**Repository**: draknarethorne/thorne-ui
