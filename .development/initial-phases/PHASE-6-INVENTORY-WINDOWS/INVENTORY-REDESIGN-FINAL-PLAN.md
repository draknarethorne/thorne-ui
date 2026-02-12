# Inventory Window Redesign - FINAL COMPREHENSIVE PLAN

**Date**: February 4, 2026  
**Branch**: feature/v0.6.0-inventory-and-windows  
**Status**: ✅ READY FOR IMPLEMENTATION  
**Designer Decisions**: User input integrated, Standards verified, Missing fields identified

---

## Executive Summary

**Approved Design**:
- Default variant: **Option A** (bottom bags, full width)
- Optional variant: **Option B** (side bags), stored in `Options/Inventory/Compact`
- AA gauge: **Implement immediately** with XP gauge (both EQType 5, but Zeal uses 71-73)
- Button placement: **Bottom row** (consistent with Merchant/Loot windows)
- Stat icons: **Plan included** for visual scanning
- Additional fields: **Tributes, Race, Deity icons** identified for future phases

**Window Dimensions**:
- Option A: 400×410px (height +20px for bottom bags)
- Option B: 400×390px (same as current, bags in 2×4 grid on right)

---

## Missing Fields Analysis & Recommendations

After reviewing STANDARDS.md and EQTYPES.md, here are fields that SHOULD be considered:

### ✅ **Tier 1 - INCLUDE IN PHASE 3.9 (High Value)**

#### 1. **Class Icon** (Visual identifier)
- **Current**: Text "Class: Warrior" at (280, 19)
- **Enhancement**: Add 32×32 class icon left of text
- **EQType**: No EQType (static based on EQType 3 class name)
- **Implementation**: Use existing class texture from game
- **Reason**: Players recognize class at a glance; reduces reading time
- **Files**: Check what class icon textures are available in default UI

#### 2. **Stat Icons** (User Requested)
- **Current**: Text labels "STR: 180" (blue label, white value)
- **Enhancement**: Small 16×16 icons for each attribute (STR strength symbol, etc.)
- **EQType**: Use same EQTypes 5-11 (values already available)
- **Implementation**: Create/find stat icon graphics
- **Reason**: Visual recognition of stats; aligns with modern UI expectations
- **Location**: Left of each stat label in IW_StatsZone
- **Colors**: Keep blue label color (#32A0FA) per standards

#### 3. **Deity Icon** (Often missing)
- **Current**: Text "Deity: Karana" at (280, 34)
- **Enhancement**: Add 24×24 deity icon with text
- **EQType**: No EQType (static text based on EQType 4)
- **Implementation**: Standard EQ deity textures
- **Reason**: Visual player identity information

#### 4. **Tribute Points Display** (P2002 Standard Feature)
- **Current**: Not displayed
- **Available**: EQTypes 121-123 documented in standards
- **Enhancement**: Add label/display for Tribute Points
- **Location**: Bottom of IW_StatsZone or separate row
- **Format**: "Tribute: 450/500" or similar
- **Colors**: Use standard white (255,255,255) per palette
- **Reason**: Tribute is core P2002 feature, players need quick reference

#### 5. **AA Breakdown** (Split available/total)
- **Current**: Single "AA: 12pt" display
- **Enhancement**: Show "12/45" (available/total) like HP displays
- **EQType**: EQType 71-73 for Zeal, EQType 5 standard
- **Implementation**: Modify IW_AltAdvGauge configuration
- **Reason**: Better visibility of AA investing progress

#### 6. **Race Display** (Identity info)
- **Current**: Not displayed
- **Available**: EQType data in PlayerWindow but not in Inventory
- **Enhancement**: Add "Race: Human" in left zone
- **Location**: Between Class and Deity in IW_LeftZone
- **Reason**: Complete character identity display
- **Note**: May require special handling - verify EQType availability in Inventory context

### ✓ **Tier 2 - CONSIDER FOR LATER PHASE (Medium Value)**

- **Ammo Counter**: Display current ammo in inventory
- **Craft Skill Display**: Quick reference to trade skills
- **Breathing Meter**: For underwater activities (EQType 3)
- **Buff Duration Timers**: Already in separate window, but could integrate top section
- **Current Mana Tick**: Enhanced mana display (Zeal feature, EQType 24)
- **Crafted Item Tracker**: Badges for crafted item counts
- **Skill Points Progress**: Character advancement tracking

### ✗ **Tier 3 - SKIP FOR NOW (Lower Priority)**

- Complex buff management (separate window better)
- Spell gem indicator (separate window better)
- Task/quest display (separate window better)
- Currency conversion rates (static info, not needed real-time)

---

## Recommended Implementation Order

### **Phase 3.9a - Core Redesign** (THIS SESSION)
1. ✅ Restructure into 5 subwindows (LeftZone, EquipmentGrid, StatsZone, ProgressionZone, BagZone)
2. ✅ Reorganize equipment to anatomical layout (4 rows)
3. ✅ Move buttons to bottom (consistent with Merchant/Loot)
4. ✅ Implement AA gauge (fully functional, not placeholder)
5. ✅ Reposition character info (Name/Level/Class/Deity)
6. ✅ Move stats to StatsZone with proper spacing
7. ✅ Add Tribute Points display (new field)
8. ⚠️ Prepare stat icons (graphic files, placeholder implementation)

### **Phase 3.9b - Enhancement** (NEXT SESSION)
1. Implement stat icons (graphics, positioning)
2. Add class icon (graphic, positioning)
3. Add deity icon (graphic, positioning)
4. Add race display (verify EQType availability)
5. Test all equipment drag/drop functionality

### **Phase 3.9c - Options Variants** (FUTURE)
1. Create `Options/Inventory/CompactLayout` with Option B (side bags)
2. Create `Options/Inventory/Standard` with Option A (bottom bags) - new preferred default
3. Documentation and testing

---

## Final Window Architecture

### **OPTION A: DEFAULT VARIANT (Bottom Bags)**

**File Path**: `thorne_drak/EQUI_Inventory.xml`  
**Window Size**: 400×410px  
**Title**: "Inventory"

```
┌────────────────────────────────────────────────────────────────┐
│ ┌──────────────┬──────────────────────────┬──────────────────┐│
│ │ LEFT ZONE    │ CENTER ZONE              │ RIGHT ZONE       ││
│ │ (5,4)        │ (95,4)                   │ (315,4)          ││
│ │ 85×350       │ 215×300                  │ 80×300           ││
│ │              │                          │                  ││
│ │ Name         │ ┌─HEAD ROW────────────┐  │ ┌─STATS────────┐││
│ │ Level        │ │EL Nk Fc H ER        │  ││AC: 1250     ││
│ │ Class        │ └─────────────────────┘  ││ATK: 950    ││
│ │ Deity        │                          ││HP: 1200/1200││
│ │ Race*        │ ┌─ARM ROW─────────────┐  ││Mana: 800/800││
│ │              │ │LR LW Ar Hd RW RR    │  ││STR🔶: 180   ││
│ │ ⬟ClassAnim   │ └─────────────────────┘  ││STA🔶: 175   ││
│ │  74×138      │                          ││AGI🔶: 110   ││
│ │              │ ┌─TORSO ROW─────────────┐││DEX🔶: 115   ││
│ │              │ │Sh Ch Bk Wa Lg Ft     │││WIS🔶: 95    ││
│ │              │ └─────────────────────────┘│INT🔶: 90    ││
│ │ Weight:      │                          │CHA🔶: 85    ││
│ │ 85/300       │ ┌─WEAPONS ROW──────────┐ │├──────────────┤││
│ │              │ │Pr Se Rg Am           │ ││Poison: 120  ││
│ │              │ └──────────────────────┘ ││Disease: 100 ││
│ │              │                          ││Fire: 115    ││
│ │              │ ┌─CURRENCY─────────────┐ ││Cold: 105    ││
│ │              │ │[Plat] [Gold]         │ ││Mag: 110     ││
│ │              │ │[Silv] [Copp]         │ │├──────────────┤││
│ │              │ └──────────────────────┘ ││Tribute: 450 ││
│ │              │                          ││Avail: 50/50 ││
│ │              │                          ││              ││
│ │              │                          │├──PROGRESS────┤││
│ │              │                          ││XP:████▓▓ 85%││
│ │              │                          ││AA:████▓▓ 12pt││
│ └──────────────┴──────────────────────────┴──────────────────┘│
│ ┌─BAG ZONE (Full Width)─────────────────────────────────────┐ │
│ │ [Bag1] [Bag2] [Bag3] [Bag4] [Bag5] [Bag6] [Bag7] [Bag8]  │ │
│ │   (95,360) 8 bags horizontal, 45px each, 1px spacing      │ │
│ └───────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────┤
│ [Alt Adv Button] [Done Button]                                │ Y=390
│    (101,390)        (299,390)  - Both 84×20, 2px gap center   │
└────────────────────────────────────────────────────────────────┘

* Race field implementation pending (verify EQType availability)
🔶 Stat icons added here (16×16, visual indicator only, no EQType change)
```

---

### **OPTION B: COMPACT VARIANT (Side Bags)**

**File Path**: `thorne_drak/Options/Inventory/Compact/EQUI_Inventory.xml`  
**Window Size**: 400×390px (same as original)

```
┌────────────────────────────────────────────────────────────────┐
│ ┌──────────────┬──────────────────────┬──────────────────────┐│
│ │ LEFT ZONE    │ CENTER ZONE          │ RIGHT ZONE           ││
│ │ (5,4)        │ (95,4)               │ (315,4)              ││
│ │ 85×350       │ 215×350              │ 80×350               ││
│ │              │                      │                      ││
│ │ Name         │ ┌─HEAD ROW────────┐  │ ┌─STATS────────────┐││
│ │ Level        │ │EL Nk Fc H ER    │  ││AC: 1250          ││
│ │ Class        │ └─────────────────┘  ││ATK: 950         ││
│ │ Deity        │                      ││HP: 1200/1200     ││
│ │ Race*        │ ┌─ARM ROW─────────┐  ││Mana: 800/800     ││
│ │              │ │LR LW Ar Hd RW RR│  ││STR🔶: 180       ││
│ │ ⬟ClassAnim   │ └─────────────────┘  ││STA🔶: 175       ││
│ │  74×138      │                      ││AGI🔶: 110       ││
│ │              │ ┌─TORSO ROW─────────┐││DEX🔶: 115       ││
│ │              │ │Sh Ch Bk Wa Lg Ft  │││WIS🔶: 95        ││
│ │              │ └───────────────────┘││INT🔶: 90        ││
│ │              │                      ││CHA🔶: 85        ││
│ │ Weight:      │ ┌─WEAPONS ROW────────┐│├─PROGRESS────────┤││
│ │ 85/300       │ │Pr Se Rg Am         │││XP:████▓▓ 85%    ││
│ │              │ └────────────────────┘│AA:████▓▓ 12pt  ││
│ │              │                      │├─BAGS────────────┤││
│ │              │ ┌─CURRENCY──────────┐││[Bg1][Bg2]       ││
│ │              │ │[Plat][Gold]       │││[Bg3][Bg4]       ││
│ │              │ │[Silv][Copp]       │││[Bg5][Bg6]       ││
│ │              │ └────────────────────┘│[Bg7][Bg8]       ││
│ │              │                      │└──────────────────┘││
│ │              │                      │ Tribute: 450     ││
│ │              │                      │ Avail: 50/50     ││
│ │              │                      │                  ││
│ └──────────────┴──────────────────────┴──────────────────────┘│
├────────────────────────────────────────────────────────────────┤
│ [Alt Adv Button] [Done Button]                                │ Y=370
│    (101,370)        (299,370)  - Both 84×20                   │
└────────────────────────────────────────────────────────────────┘

Bags: 2×4 grid (319,300), each 45×45, 1px gaps
No bottom row - bags stack on right side with stats
```

---

## Detailed Subwindow Specifications

### **Subwindow 1: IW_LeftZone**
```
Location: (5, 4)
Size: 85×350px
DrawTemplate: WDT_Inner
RepeativeStyle: false

Contents:
├─ IW_Name              (Label, EQType 1) - Character name, white
├─ IW_Level             (Label, EQType 2) - Level number, right-aligned
├─ IW_Class             (Label, EQType 3) - Class name, blue
├─ [CLASS_ICON*]        (StaticAnimation) - 32×32 class indicator
├─ IW_Deity             (Label, EQType 4) - Deity name, white
├─ [DEITY_ICON*]        (StaticAnimation) - 24×24 deity indicator
├─ [IW_Race*]           (Label) - Race name (EQType TBD)
├─ IW_CharacterView     (Screen subwindow) - Class animation, 74×138
├─ IW_Weight            (Label, EQType 25) - "Weight:"
├─ IW_CurrentWeight     (Label, EQType 24) - Current weight value
├─ IW_MaxWeight         (Label) - "Max weight" or "/" separator
├─ IW_FacePick          (Button, 84×20) - Face customization
└─ Spacer for future fields

Note: All coordinate offsets relative to IW_LeftZone parent
* Future implementation Phase 3.9b
```

---

### **Subwindow 2: IW_EquipmentGrid**
```
Location: (95, 4)
Size: 215×300px
DrawTemplate: WDT_Inner
RepeativeStyle: false

Equipment Layout (Anatomical):

ROW 1 - HEAD (Y=5):
├─ InvSlot1   [LEFT_EAR]   (45×45, X=5)
├─ InvSlot5   [NECK]       (45×45, X=52)
├─ InvSlot3   [FACE]       (45×45, X=99)
├─ InvSlot2   [HEAD]       (45×45, X=146)
└─ InvSlot4   [RIGHT_EAR]  (45×45, X=169)

ROW 2 - ARMS (Y=52):
├─ InvSlot15  [LEFT_RING]  (45×45, X=5)
├─ InvSlot9   [LEFT_WRIST] (45×45, X=52)
├─ InvSlot7   [ARMS]       (45×45, X=99)
├─ InvSlot12  [HANDS]      (45×45, X=146)
├─ InvSlot10  [RIGHT_WRIST](45×45, X=169)
└─ InvSlot16  [RIGHT_RING] (45×45, X=169)

ROW 3 - TORSO (Y=99):
├─ InvSlot6   [SHOULDERS]  (45×45, X=5)
├─ InvSlot17  [CHEST]      (45×45, X=52)
├─ InvSlot8   [BACK]       (45×45, X=99)
├─ InvSlot20  [WAIST]      (45×45, X=146)
├─ InvSlot18  [LEGS]       (45×45, X=169)
└─ InvSlot19  [FEET]       (45×45, X=169)

ROW 4 - WEAPONS (Y=146):
├─ InvSlot13  [PRIMARY]    (45×45, X=5)
├─ InvSlot14  [SECONDARY]  (45×45, X=52)
├─ InvSlot11  [RANGE]      (45×45, X=99)
└─ InvSlot21  [AMMO]       (45×45, X=146)

CURRENCY (Y=200):
├─ IW_Money0 [PLATINUM]    (70×24, X=5)
├─ IW_Money1 [GOLD]        (70×24, X=80)
├─ IW_Money2 [SILVER]      (70×24, X=5)
└─ IW_Money3 [COPPER]      (70×24, X=80)

Spacing: 45px width + 1px gap = 46px per column, 2 rows of 4 coins
Colors: Per standard templates, A_InvSlot backgrounds with appropriate icons
```

---

### **Subwindow 3: IW_StatsZone**
```
Location: (315, 4)
Size: 80×240px
DrawTemplate: WDT_Inner
RepeativeStyle: false

Combat Stats (Y=5):
├─ IW_AC            (Label) - "AC:" blue text
├─ IW_AC_Value      (Label, EQType 22) - AC numeric, right-aligned
├─ IW_ATK           (Label) - "ATK:" orange text
└─ IW_ATK_Value     (Label, EQType 23) - ATK numeric, right-aligned

Vitals (Y=30):
├─ IW_HP_Label      (Label) - "HP:"
├─ IW_HP_Value      (Label, EQType 70/18) - Current/Max or numeric
├─ IW_Mana_Label    (Label) - "Mana:"
└─ IW_Mana_Value    (Label, EQType 80/20) - Current/Max or numeric

Attributes (Y=60, 15px vertical spacing):
├─ IW_STR           (Label, EQType 5) - "STR:" with icon
├─ IW_STR_Value     (Label, EQType 5) - Value, right-aligned
├─ IW_STA           (Label, EQType 6) - "STA:" with icon
├─ IW_STA_Value     (Label, EQType 6) - Value, right-aligned
├─ IW_AGI           (Label, EQType 7) - "AGI:" with icon
├─ IW_AGI_Value     (Label, EQType 7) - Value, right-aligned
├─ [continues for...]
├─ IW_DEX/DEX_Value (EQType 8)
├─ IW_WIS/WIS_Value (EQType 9)
├─ IW_INT/INT_Value (EQType 10)
└─ IW_CHA/CHA_Value (EQType 11)

Resistances (Y=150):
├─ IW_Poison        (Label, EQType 12) - "Poison:" teal text
├─ IW_Poison_Value  (Label, EQType 12) - Value, right-aligned
├─ IW_Magic         (Label, EQType 16) - "Mag:" purple text
├─ IW_Magic_Value   (Label, EQType 16) - Value, right-aligned
├─ IW_Disease       (Label, EQType 13) - "Disease:" yellow text
├─ IW_Disease_Value (Label, EQType 13) - Value, right-aligned
├─ IW_Fire          (Label, EQType 14) - "Fire:" orange text
├─ IW_Fire_Value    (Label, EQType 14) - Value, right-aligned
├─ IW_Cold          (Label, EQType 15) - "Cold:" cyan text
└─ IW_Cold_Value    (Label, EQType 15) - Value, right-aligned

Misc (Y=200):
├─ IW_Tribute_Label (Label) - "Tribute:"
├─ IW_Tribute_Val   (Label, EQType 121) - Current tribute
├─ IW_AA_Available  (Label, EQType 72) - "Avail:" AA points
└─ [Space for future]

Color Standards:
- Labels: Blue (50,160,250) for attributes, specific color for resist type
- Values: White (255,255,255) for all numeric
- Font: 3 (default)
- Alignment: Right-align numerics (AlignRight=true)
```

---

### **Subwindow 4: IW_ProgressionZone**
```
Location: (315, 250)
Size: 80×60px
DrawTemplate: WDT_Inner
RepeativeStyle: false

XP Progress (Y=5):
├─ IW_ExpGauge      (Gauge, EQType 4) - Green progress bar 116×8
│  ├─ FillTint: 0, 205, 0 (green)
│  ├─ LinesFillTint: 0, 144, 0 (darker green)
│  ├─ GaugeDrawTemplate: Background, Fill, Lines
│  └─ Size: 116×8
├─ IW_EXP_Percentage (Label, EQType 26) - "XX%" overlay
└─ IW_NextLevel      (Label) - Next level XP (optional)

AA Progress (Y=20):
├─ IW_AltAdvGauge    (Gauge, EQType 5/71) - Yellow progress bar 116×8
│  ├─ FillTint: 205, 205, 0 (yellow)
│  ├─ LinesFillTint: 144, 144, 0 (darker yellow)
│  ├─ GaugeDrawTemplate: Background, Fill, Lines (FULL IMPLEMENTATION)
│  └─ Size: 116×8 (STANDARD, matching XP gauge)
├─ IW_AltAdv_Label   (Label) - "AA:" text
├─ IW_AltAdv_Points  (Label, EQType 71/72) - "12pt" or "12/45"
└─ IW_AltAdv_Percent (Label, EQType 73) - Optional percentage

Spacing: 15px between gauges (Y offset)
Layout: Gauges side-by-side or stacked? Recommend stacked (vertical) for clarity

Font: 3 (default)
Alignment: Center gauge, numeric label overlay
```

---

### **Subwindow 5: IW_BagZone (OPTION A)**
```
Location: (95, 360)
Size: 300×45px
DrawTemplate: WDT_Inner
RepeativeStyle: false

Single Row, 8 Bags Horizontal:
├─ InvSlot22 [BAG1] (45×45, X=5)
├─ InvSlot23 [BAG2] (45×45, X=52)
├─ InvSlot24 [BAG3] (45×45, X=99)
├─ InvSlot25 [BAG4] (45×45, X=146)
├─ InvSlot26 [BAG5] (45×45, X=193)
├─ InvSlot27 [BAG6] (45×45, X=240)
├─ InvSlot28 [BAG7] (X=287)
└─ InvSlot29 [BAG8] (X=334, extends past zone - will need adjustment)

Note: Adjust zone width or spacing if needed to fit all 8 bags comfortably
Alternative: Use 46px per bag (45+1px gap) = 368px total width
Recommend: Increase IW_BagZone width to 350px, adjust X positions accordingly
```

---

### **Subwindow 5B: IW_BagZone (OPTION B - Compact Variant)**
```
Location: (320, 300)
Size: 75×60px
DrawTemplate: WDT_Inner
RepeativeStyle: false

2×4 Grid, Right Side:
Row 1:
├─ InvSlot22 [BAG1] (45×45, X=5, Y=5)
└─ InvSlot23 [BAG2] (45×45, X=51, Y=5)

Row 2:
├─ InvSlot24 [BAG3] (45×45, X=5, Y=51)
└─ InvSlot25 [BAG4] (45×45, X=51, Y=51)

Row 3:
├─ InvSlot26 [BAG5] (45×45, Y=97)
└─ InvSlot27 [BAG6] (45×45, Y=97)

Row 4:
├─ InvSlot28 [BAG7] (45×45, Y=143)
└─ InvSlot29 [BAG8] (45×45, Y=143)

Spacing: 1px gaps between bags
Total area could be: 96×150px for safe margins on 2×4 grid
```

---

## Button Placement (Bottom Row)

**FINAL DECISION**: Bottom row, consistent with Merchant and Loot windows

```xml
<!-- Buttons in main InventoryWindow, NOT in subwindows -->

<!-- Alt Adv Button -->
<Button item="IW_AltAdvBtn">
  <ScreenID>AltAdvBtn</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>101</X><Y>390</Y></Location>
  <Size><CX>84</CX><CY>20</CY></Size>
  <Text>Alt Adv</Text>
  <OnLeftClick>/alt adv</OnLeftClick>
  <!-- Styling per standards -->
</Button>

<!-- Done Button (Close Window) -->
<Button item="IW_DoneButton">
  <ScreenID>DoneButton</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>299</X><Y>390</Y></Location>
  <Size><CX>84</CX><CY>20</CY></Size>
  <Text>Done</Text>
  <OnLeftClick>/close inventory</OnLeftClick>
  <!-- Styling per standards -->
</Button>

<!-- Face Button (Character Customization) - Relocate to left zone -->
<Button item="IW_FacePick">
  <ScreenID>FaceButton</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>2</X><Y>330</Y></Location>  <!-- In IW_LeftZone -->
  <Size><CX>70</CX><CY>20</CY></Size>
  <Text>Face</Text>
  <OnLeftClick>/face</OnLeftClick>
</Button>

Spacing: Bottom buttons Y=390 for Option A (410px window)
-         Bottom buttons Y=370 for Option B (390px window)
-         Center gap: 299 - 101 - 84 = 114px (visible gap for balance)
-         Left margin: 101 - 2 = 99px (visual balance with left zone)
```

---

## Stat Icons Implementation

**Phase 3.9a Preparation** (defer graphics to Phase 3.9b):

```xml
<!-- Stat Icon Placeholders - Location in IW_StatsZone -->

<!-- STR Icon (strength) -->
<StaticAnimation item="IW_STR_Icon">
  <ScreenID>STR_Icon</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>0</X><Y>60</Y></Location>
  <Size><CX>16</CX><CY>16</CY></Size>
  <TextureInfo Name="A_Icon_STR" U="0" V="0" />
  <!-- 16×16 icon before "STR:" label -->
</StaticAnimation>

<!-- Similar pattern for STA, AGI, DEX, WIS, INT, CHA -->
<!-- One 16×16 icon per attribute in IW_StatsZone -->
```

**Graphics Requirements**:
- Find or create 16×16 attribute icons
- Icons for: Strength, Stamina, Agility, Dexterity, Wisdom, Intelligence, Charisma
- Color: Should match blue label color (#32A0FA) or use neutral gray/white
- File format: .tga in appropriate texture directory
- Consider using existing game textures if available

---

## Color Alignment Verification

**Standards Compliance Check**:

| Element | Color (RGB) | Standard | Status |
|---------|------------|----------|--------|
| Character Name | 255, 255, 255 | White | ✅ Match |
| Level/Stats Value | 255, 255, 255 | White | ✅ Match |
| Attribute Labels | 50, 160, 250 | Blue | ✅ Match |
| Position/Magic | 195, 0, 185 | Purple | ✅ Match |
| Fire | 255, 165, 0 | Orange | ✅ Match |
| Cold | 0, 165, 255 | Cyan | ✅ Match |
| Disease | 205, 205, 0 | Yellow | ✅ Match |
| Poison | 0, 130, 100 | Teal | ✅ Match |
| XP Gauge Fill | 0, 205, 0 | Green | ✅ Match |
| AA Gauge Fill | 205, 205, 0 | Yellow | ✅ Match |

**All colors align with STANDARDS.md canonical Inventory color scheme** ✅

---

## Missing Field Implementation Matrix

| Field | Phase | EQType | Status | Notes |
|-------|-------|--------|--------|-------|
| Equipment Anatomical | 3.9a | 1-21 | ✅ Scheduled | 4-row pattern |
| Class Icon | 3.9b | N/A | 📋 Planned | Visual identifier |
| Stat Icons | 3.9b | N/A | 📋 Planned | 16×16 graphics |
| Deity Icon | 3.9b | N/A | 📋 Planned | 24×24 graphic |
| Tribute Points | 3.9a | 121-123 | ✅ Scheduled | P2002 standard |
| Race Display | 3.9b | TBD | 🔍 Verify | Check EQType availability |
| AA Breakdown | 3.9a | 71-73 | ✅ Scheduled | With AA gauge |
| Breathing Meter | Future | 3 | ⏳ Consider | Underwater activity |
| Ammo Counter | Future | TBD | ⏳ Consider | Item counting |

---

## Implementation Checklist

### **Phase 3.9a (This Session)**

- [ ] Create IW_LeftZone subwindow (85×350)
- [ ] Create IW_EquipmentGrid subwindow (215×300)
- [ ] Create IW_StatsZone subwindow (80×240)
- [ ] Create IW_ProgressionZone subwindow (80×60)
- [ ] Create IW_BagZone subwindow (300×45)
- [ ] Reorganize all 21 equipment slots to anatomical layout
- [ ] Move character info (Name/Level/Class/Deity) to IW_LeftZone
- [ ] Move stats (AC/ATK/STR-CHA/Resistances) to IW_StatsZone
- [ ] Move XP gauge to IW_ProgressionZone
- [ ] **Implement AA gauge** (full size, colors, animations)
- [ ] Move currency buttons to IW_EquipmentGrid
- [ ] Move bag slots to IW_BagZone (bottom row)
- [ ] Move buttons (Alt Adv, Done, Face) to bottom row (consistent with Merchant/Loot)
- [ ] Add Tribute Points display (EQTypes 121-123)
- [ ] Test in-game: Equipment drag/drop, gauge updates, stat displays
- [ ] Commit to feature/v0.6.0-inventory-and-windows branch

### **Phase 3.9b (Next Session)**

- [ ] Create stat icon graphics (6 icons × 16×16)
- [ ] Implement stat icons in XML (placeholder → active)
- [ ] Create class icon graphic (32×32)
- [ ] Implement class icon display
- [ ] Create deity icon graphics (if needed)
- [ ] Implement deity icon display
- [ ] Verify Race field EQType availability
- [ ] Test all new icons in-game
- [ ] Update PHASE-3.9 documentation

### **Phase 3.9c (Options Variants)**

- [ ] Create `Options/Inventory/Compact/` directory
- [ ] Copy and modify EQUI_Inventory.xml with Option B layout
- [ ] Update IW_BagZone for 2×4 grid on right side
- [ ] Adjust window height back to 390px
- [ ] Create README.md explaining both variants
- [ ] Test both variants in-game
- [ ] Commit options variants

---

## Standards Alignment Summary

✅ **All approved by STANDARDS.md**:
- Anatomical equipment layout confirmed in standards
- Subwindow/inner screen pattern recommended and documented
- Color palette verified - all RGB values match canonical scheme
- Gauge styling matches established patterns (14px/8px precedent)
- Button layout consistent with Merchant/Loot windows
- RelativePosition pattern for all child elements
- XML organization follows documented best practices
- Cross-window consistency rules maintained
- Font 3 default confirmed
- NoWrap property for numeric values required
- Stat label colors match established palette

---

## Next Actions

1. **Present comprehensive plan to user** ✅
2. **Get final approval on**:
   - Tribute Points inclusion (EQTypes 121-123)
   - Race display field (if EQType available)
   - Stat icon graphics approach
   - Option B (Compact) variant scope
3. **Begin XML implementation** of subwindows
4. **Test iteratively** as each subwindow is completed
5. **Document progress** in session logs

---

**Status**: ✅ READY FOR IMPLEMENTATION

**Estimated Timeline**:
- Phase 3.9a: 3-4 hours (core redesign)
- Phase 3.9b: 2-3 hours (graphics and icons)
- Phase 3.9c: 1-2 hours (options variant)
- Total: 6-9 hours for complete Inventory redesign

**File to modify**: `thorne_drak/EQUI_Inventory.xml` (2060 lines → estimated 2,500-2,800 lines after expansion)

---

**Prepared by**: Draknare Thorne  
**Date**: February 4, 2026  
**Branch**: feature/v0.6.0-inventory-and-windows

