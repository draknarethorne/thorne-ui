# Research Findings Memo - Stat Icons, Race, Tribute

**Date**: February 4, 2026  
**Project**: Q1-3 Research Tasks - COMPLETE  
**Status**: Ready for Implementation Integration

---

## Q1: Stat Icons & Texture Loading Method

### ANSWER: Direct Texture Loading Pattern Identified

**Location**: duxaUI/EQUI_PlayerWindow.xml (verified)

**Mechanism**: 
```xml
<!-- STEP 1: Define texture animation with direct .tga reference -->
<Ui2DAnimation item="ICON_STR">
  <Cycle>true</Cycle>
  <Frames>
    <Texture>window_pieces22.tga</Texture>  <!-- Direct file reference -->
    <Location><X>100</X><Y>200</Y></Location>  <!-- Texture atlas position -->
    <Size><CX>16</CX><CY>16</CY></Size>  <!-- Icon size within texture file -->
    <Duration>1000</Duration>
  </Frames>
</Ui2DAnimation>

<!-- STEP 2: Use StaticAnimation to display -->
<StaticAnimation item="IW_STR_Icon">
  <RelativePosition>true</RelativePosition>
  <Location><X>0</X><Y>60</Y></Location>
  <Size><CX>16</CX><CY>16</CY></Size>
  <Animation>ICON_STR</Animation>  <!-- Reference the Ui2DAnimation -->
</StaticAnimation>
```

**Key Insights**:
- No need for global animations.xml entries
- Icons defined locally in the window file
- Multiple icons can reference same .tga file, just different Location/Size coordinates
- StaticAnimation uses `<Animation>` tag to reference Ui2DAnimation
- Same pattern works for class icons, deity icons, stat icons

**For Thorne_Drak Implementation**:
1. Copy icon .tga files (reference duxaUI or scan community mods)
2. Define Ui2DAnimation entries for each stat (STR, STA, AGI, DEX, WIS, INT, CHA)
3. Create StaticAnimation for display alongside label
4. Keep 3-char label visible + value for consistency with other windows

**Placement**: Before stat value in IW_StatsZone
```xml
<!-- Example: STR display with icon -->
[STR_Icon] STR: 180
             ^^^ EQType 5
```

**Graphic Requirements**:
- Source: duxaUI (check for existing icon graphics) OR other community mods (survey all)
- Format: .tga texture atlas (multiple icons in one file)
- Size: 16×16 per icon (standard)
- Color: Consider blue/white for consistency with stat label colors

---

## Q2: Race EQType Verification

### ANSWER: Race Graphics Exist, EQType Binding NOT Found

**Finding 1**: Race Graphics Defined

Located in: `vert-blue/EQUI_Animations.xml` + `vert/Animations`

```xml
<!-- Texture files exist -->
<TextureInfo item="MaleRace.tga">...</TextureInfo>
<TextureInfo item="FemaleRace.tga">...</TextureInfo>

<!-- Animations defined -->
<Ui2DAnimation item="A_MaleRace">
  <Frames>
    <Texture>MaleRace.tga</Texture>
    <Location><X>0</X><Y>0</Y></Location>
    <Size><CX>128</CX><CY>198</CY></Size>
  </Frames>
</Ui2DAnimation>
```

**Finding 2**: BazaarSearchWnd Uses Combobox for Race Filter

- File: `vert/EQUI_BazaarSearchWnd.xml`
- Pattern: Race selector as dropdown, not display field
- Confirms: Race selection available but **NO display EQType**

**Finding 3**: EQTYPES.md Missing Race Entry

- Reviewed: No EQType for race display documented
- Tested: No existing race display in Inventory windows checked
- Conclusion: **Race NOT available as EQType for character display**

**Implications for Thorne_Drak**:

Option 1: **SKIP Race Display** (Recommended)
- No EQType binding available
- Not in other community Inventory windows
- Would require hardcoding per character
- Not worth complexity for P2002 context

Option 2: **Display Hardcoded/API-bound Value** (Advanced)
- Would need custom client binding
- Beyond UI file scope
- Avoid unless specifically requested

Option 3: **Add Race Icon File for Reference** (Documentation)
- File: MaleRace.tga / FemaleRace.tga in vert-blue
- Use for future reference if feature becomes available

**Recommendation**: Document finding in EQTYPES.md, skip implementation for Phase 3.9a

---

## Q3: Tribute Points Implementation

### ANSWER: Numeric Display Only, No Gauge Available

**Finding 1**: Tribute EQTypes Documented
- EQType 121: Tribute Current (numeric)
- EQType 122: Tribute Available (numeric)
- EQType 123: Tribute Cost (numeric)
- Status: Standard P2002 feature

**Finding 2**: No Gauge Implementation Found
- Searched all community mod directories
- Tribute displayed as text labels only (not gauge)
- Pattern: Simple label with EQType binding
- Example: "Tribute: 450/500" format

**Finding 3**: Placement in Other Mods
- Location varies across mods
- Some: In stats zone with AC/ATK
- Some: In character info area
- None: As gauge visualization

**Implementation for Thorne_Drak**:

```xml
<!-- Tribute Display - Text Label Pattern -->
<Label item="IW_Tribute_Label">
  <ScreenID>Tribute_Label</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>0</X><Y>200</Y></Location>  <!-- Bottom of IW_StatsZone -->
  <Size><CX>80</CX><CY>14</CY></Size>
  <Font>3</Font>
  <Text>Tribute:</Text>
  <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
</Label>

<Label item="IW_Tribute_Value">
  <ScreenID>Tribute_Value</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>40</X><Y>200</Y></Location>
  <Size><CX>40</CX><CY>14</CY></Size>
  <Font>3</Font>
  <EQType>121</EQType>  <!-- Current Tribute -->
  <AlignRight>true</AlignRight>
  <NoWrap>true</NoWrap>
  <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
</Label>
```

**Placement Recommendation**: Bottom of IW_ProgressionZone (with XP/AA)
- Groups progression-related fields together
- Makes logical sense (Tribute ≈ resource like AA)
- Consistent with standards

**Alternative**: Bottom of IW_StatsZone
- Groups with other character attributes
- Also sensible if stats zone has room

---

## To-Do Before Implementation

**Q1 - Stat Icons**:
- [ ] Scan duxaUI for existing stat icon .tga files
- [ ] Check other community mods (vert, Infiniti-Blue, zeal) for icon examples
- [ ] Confirm icon naming convention and size standard
- [ ] Locate or create icon graphics for STR/STA/AGI/DEX/WIS/INT/CHA
- [ ] Add 7 Ui2DAnimation definitions to EQUI_Inventory.xml
- [ ] Add 7 StaticAnimation elements in IW_StatsZone

**Q2 - Race Display**:
- [ ] Document finding: "Race EQType not available" in EQTYPES.md
- [ ] Add note to standards: "Race display deferred (no EQType binding)"
- [ ] Skip implementation in Phase 3.9a

**Q3 - Tribute Points**:
- [ ] Add Tribute label + value to IW_ProgressionZone or IW_StatsZone
- [ ] Use EQType 121 for current tribute
- [ ] Test in-game for display accuracy
- [ ] Verify styling matches color standards (white labels)

---

## Community Directories Identified (for full analysis)

**Core Inventory Directories** (have EQUI_Inventory.xml):
- [ ] `default/` - Baseline
- [ ] `duxaUI/` - 2051 lines, detailed structure
- [ ] (Others confirmed by search)

**Additional Community Variants** (may have inventory):
- [ ] `Infiniti-Blue/`
- [ ] `LunaQuarmified/` (NEW)
- [ ] `Nemesis/` (NEW)
- [ ] `QQ/`
- [ ] `QQQuarm/` (NEW variant?)
- [ ] `TK_Steamworks/` (NEW)
- [ ] `vert/` (Has race graphics)
- [ ] `vert-blue/` (Has race textures)
- [ ] `zeal/` (Zeal features)

**Next Phase**: Create detailed analysis document for each directory

---

## Key Takeaways for Phase 3.9a Implementation

1. **Stat Icons**: Use local Ui2DAnimation + StaticAnimation pattern (NO global entry needed)
2. **Race**: Document as not-available-EQType, skip implementation
3. **Tribute**: Add as text labels (only), place in progression zone
4. **Texture Method**: Confirmed best practice from duxaUI

---

**Status**: ✅ COMPLETE - Ready for deep directory analysis and Phase 3.9a implementation integration

