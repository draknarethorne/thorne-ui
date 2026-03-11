# Inventory Window Redesign - MODULAR LEGO BLOCK ARCHITECTURE

**Date**: February 4, 2026  
**Branch**: feature/v0.6.0-inventory-and-windows  
**Status**: ✅ READY FOR IMPLEMENTATION (User-Approved Modular Design)  
**Philosophy**: Subwindows as "Lego Blocks" - Mix and match to create variants

---

## User Requirements Summary

Based on user feedback:

✅ **Window can be wider AND taller** - no strict size constraint  
✅ **Do NOT stack character info on single lines** - prefer vertical layout  
✅ **Progression HIGH in window** (upper left area)  
✅ **ClassAnim can be pushed down** - treat as its own subwindow  
✅ **Left zone order**: Player Info → Progression → ClassAnim → Weight (bottom)  
✅ **More granular subwindows** = easier to create variants  
✅ **Stats display**: ICON + Label + Value (maintains consistency with other windows)  
✅ **Equipment layout**: Flexible - offer both 3-column and 4-column anatomical variants  
✅ **Current likes**: Groupings on right side, bags across bottom, buttons below bags  
✅ **Current dislikes**: Armor/weapons are messy (QQ style), bag flow not great  
✅ **Vision**: Player info + progression LEFT, Full stats with icons RIGHT, Equipment CENTER  
✅ **HP/Mana consideration**: Could be on left with player info, may include gauges in variant  
✅ **Modularity goal**: Create subwindow grouping system for easy reorganization

---

## Modular Subwindow Architecture (9 Zones = Maximum Flexibility)

### Window Overview: 420×440px (Expanded for Comfort)

```
┌──────────────────────────────────────────────────────────────────────┐
│ INVENTORY WINDOW (420×440px)                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ ┌───────────┬─────────────────────────────┬──────────────────────┐  │
│ │ ZONE 1    │ ZONE 4: EQUIPMENT GRID      │ ZONE 7: STATS        │  │
│ │ Player    │ (110,4) 215×300             │ (330,4) 85×360       │  │
│ │ Info      │                             │                      │  │
│ │ (5,4)     │ • ROW 1 (HEAD)             │ • COMBAT STATS       │  │
│ │ 100×60    │ • ROW 2 (ARMS)             │   AC: 1250   🛡️     │  │
│ │           │ • ROW 3 (TORSO)             │   ATK: 950   ⚔️     │  │
│ │ Name      │ • ROW 4 (WEAPONS)           │                      │  │
│ │ Level     │                             │ • VITALS             │  │
│ │ Class     │ ┌─────────────────────────┐ │   HP🔴: 1200/1200  │  │
│ │ Deity     │ │ ZONE 5: CURRENCY        │ │   Mana🔵: 800/800  │  │
│ ├───────────┤ │ (110,210) 215×90        │ │   Stam🟡: 100%     │  │
│ │ ZONE 2    │ │ [Plat] [Gold]           │ │                      │  │
│ │ Progress  │ │ [Silv] [Copp]           │ │ • ATTRIBUTES         │  │
│ │ (5,68)    │ └─────────────────────────┘ │   🔶STR: 180        │  │
│ │ 100×70    │                             │   🔶STA: 175        │  │
│ │           │                             │   🔶AGI: 110        │  │
│ │ XP:████85%│                             │   🔶DEX: 115        │  │
│ │ AA:████12pt│                            │   🔶WIS: 95         │  │
│ ├───────────┤                             │   🔶INT: 90         │  │
│ │ ZONE 3    │                             │   🔶CHA: 85         │  │
│ │ ClassAnim │                             │                      │  │
│ │ (5,142)   │                             │ • RESISTANCES        │  │
│ │ 100×160   │                             │   🟣MR: 100         │  │
│ │           │                             │   🔴FR: 100         │  │
│ │ ⬟ 74×138  │                             │   🔵CR: 100         │  │
│ │  model    │                             │   🟢DR: 100         │  │
│ │           │                             │   🟡PR: 100         │  │
│ ├───────────┤                             │                      │  │
│ │ ZONE 6    │                             │ • MISC               │  │
│ │ Weight    │                             │   Tribute: 450       │  │
│ │ (5,306)   │                             │   AA Avail: 12/50   │  │
│ │ 100×58    │                             │                      │  │
│ │           │                             │                      │  │
│ │ Weight:   │                             │                      │  │
│ │ 85/300    │                             │                      │  │
│ └───────────┴─────────────────────────────┴──────────────────────┘  │
│ ┌────────────────────────────────────────────────────────────────┐  │
│ │ ZONE 8: BAG ZONE (Full width)                                  │  │
│ │ (5,370) 410×45                                                 │  │
│ │ [Bag1][Bag2][Bag3][Bag4][Bag5][Bag6][Bag7][Bag8]              │  │
│ └────────────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────────────┐  │
│ │ ZONE 9: BUTTONS                                                │  │
│ │ (5,420) 410×20                                                 │  │
│ │ [Skills] [Alt Adv]              [Face] [Destroy] [Done]       │  │
│ └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## The 9 Modular "Lego Block" Subwindows

### **ZONE 1: Player Identity (IW_PlayerInfo)**
```xml
Location: (5, 4)
Size: 100×60px
DrawTemplate: WDT_Inner

Contents:
├─ IW_Name       (Label, EQType 1) "Draknare" - white, large font
├─ IW_Level      (Label, EQType 2) "Level" label - blue
├─ IW_LevelValue (Label, EQType 2) "60" - white, same line as Level
├─ IW_Class      (Label, EQType 3) "Warrior" - blue
└─ IW_Deity      (Label, EQType 4) "Karana" - white

Vertical spacing: 14px per line
Total height: ~60px (4 items × 14px + margins)

Modular purpose: Identity info that rarely changes
Variant options: 
  - Add Race display
  - Add class icon (32×32)
  - Add deity icon (24×24)
```

### **ZONE 2: Progression (IW_Progression)**
```xml
Location: (5, 68)
Size: 100×70px
DrawTemplate: WDT_Inner

Contents:
├─ IW_ExpGauge       (Gauge, 116×8) - green fill, may overflow zone horizontally
├─ IW_EXP_Label      (Label) "XP:" - blue, before gauge or integrated
├─ IW_EXP_Percentage (Label, EQType 26) "85%" - white, overlay or after gauge
├─ IW_AltAdvGauge    (Gauge, 116×8) - yellow fill
├─ IW_AltAdv_Label   (Label) "AA:" - blue
├─ IW_AltAdv_Points  (Label, EQType 71/72) "12pt" or "12/50" - white
└─ IW_AltAdv_Percent (Label, EQType 73) Optional percentage overlay

Vertical spacing: 
  - XP gauge + label: 28px
  - AA gauge + label: 28px
  - Gap between: 14px
Total height: 70px

Modular purpose: Character advancement tracking
Variant options:
  - Show/hide XP rate (%/hour, EQType 81)
  - Show/hide AA rate (%/hour, EQType 86)
  - Adjust gauge width to fit zone (95px instead of 116px)
  - Combine with HP/Mana gauges in "vitals" variant
```

### **ZONE 3: Character Model (IW_ClassAnim)**
```xml
Location: (5, 142)
Size: 100×160px
DrawTemplate: WDT_Inner

Contents:
└─ IW_CharacterView  (Screen subwindow) - 74×138px actual, centered in zone
    └─ ClassAnim     (StaticAnimation or SubScreen) - 3D class model

Centering calculation:
  X offset: (100 - 74) / 2 = 13px → X=18 (5+13)
  Y offset: (160 - 138) / 2 = 11px → Y=153 (142+11)

Modular purpose: Visual character representation
Variant options:
  - Hide entirely for ultra-compact variant
  - Replace with race graphic
  - Replace with deity graphic
  - Larger zone for bigger model
```

### **ZONE 4: Equipment Grid (IW_EquipmentGrid)**
```xml
Location: (110, 4)
Size: 215×200px
DrawTemplate: WDT_Inner

Contents (4-ROW ANATOMICAL LAYOUT):

ROW 1 - HEAD (Y=5):
├─ InvSlot1   [LEFT_EAR]   (45×45, X=5, EQType 1)
├─ InvSlot5   [NECK]       (45×45, X=52, EQType 5)
├─ InvSlot3   [FACE]       (45×45, X=99, EQType 3)
├─ InvSlot2   [HEAD]       (45×45, X=146, EQType 2)
└─ InvSlot4   [RIGHT_EAR]  (45×45, X=193, EQType 4)

ROW 2 - ARMS (Y=52):
├─ InvSlot15  [LEFT_RING]  (45×45, X=5, EQType 15)
├─ InvSlot9   [LEFT_WRIST] (45×45, X=52, EQType 9)
├─ InvSlot7   [ARMS]       (45×45, X=99, EQType 7)
├─ InvSlot12  [HANDS]      (45×45, X=146, EQType 12)
├─ InvSlot10  [RIGHT_WRIST](45×45, X=169, EQType 10)
└─ InvSlot16  [RIGHT_RING] (45×45, X=193, EQType 16)

ROW 3 - TORSO (Y=99):
├─ InvSlot6   [SHOULDERS]  (45×45, X=5, EQType 6)
├─ InvSlot17  [CHEST]      (45×45, X=52, EQType 17)
├─ InvSlot8   [BACK]       (45×45, X=99, EQType 8)
├─ InvSlot20  [WAIST]      (45×45, X=146, EQType 20)
├─ InvSlot18  [LEGS]       (45×45, X=169, EQType 18)
└─ InvSlot19  [FEET]       (45×45, X=193, EQType 19)

ROW 4 - WEAPONS (Y=146):
├─ InvSlot13  [PRIMARY]    (45×45, X=52, EQType 13)
├─ InvSlot14  [SECONDARY]  (45×45, X=99, EQType 14)
├─ InvSlot11  [RANGE]      (45×45, X=146, EQType 11)
└─ InvSlot21  [AMMO]       (45×45, X=193, EQType 21)

Total: 4 rows × 45px + 3 gaps × 7px = 180 + 21 = 201px ✅ Fits in 200px

Modular purpose: Core equipment management
Variant options:
  - 3-COLUMN variant: Split Row 2 into 3 columns (narrower, 7 rows total)
  - 6-COLUMN variant: Compress slot size to 40×40 (denser)
  - Alternative row orders (weapons at top for combat classes)
```

### **ZONE 5: Currency (IW_Currency)**
```xml
Location: (110, 210)
Size: 215×90px
DrawTemplate: WDT_Inner

Contents (2×2 grid):
├─ IW_Money0 [PLATINUM] (70×24, X=5, Y=5)
├─ IW_Money1 [GOLD]     (70×24, X=80, Y=5)
├─ IW_Money2 [SILVER]   (70×24, X=5, Y=35)
└─ IW_Money3 [COPPER]   (70×24, X=80, Y=35)

Layout: Two columns, two rows
Column width: 70px + 10px gap = 80px
Row height: 24px + 11px gap = 35px

Modular purpose: Currency display
Variant options:
  - Vertical stack (single column, 4 rows)
  - Horizontal row (single row, 4 columns)
  - Integrate into stats zone instead
  - Add inventory slot counter (EQType 83/84 Zeal)
```

### **ZONE 6: Weight/Encumbrance (IW_Weight)**
```xml
Location: (5, 306)
Size: 100×58px
DrawTemplate: WDT_Inner

Contents:
├─ IW_Weight        (Label) "Weight:" - blue label
├─ IW_CurrentWeight (Label, EQType 24) "85" - white value
├─ IW_WeightDivider (Label) "/" - white separator
└─ IW_MaxWeight     (Label, EQType 25) "300" - white value

Optional additions:
├─ IW_InventorySlotCount (Label, EQType 83/84) "Slots: 12/80" - Zeal client
└─ IW_Weight_Gauge       (Gauge) Optional visual weight bar

Vertical layout:
  Line 1: "Weight:" label
  Line 2: "85/300" value
  Line 3: Optional "Slots: 12/80"
Total height: ~58px

Modular purpose: Inventory capacity tracking
Variant options:
  - Add weight gauge
  - Show only percentage
  - Combine with currency
  - Add breathing meter (underwater)
```

### **ZONE 7: Stats (IW_Stats)**
```xml
Location: (330, 4)
Size: 85×360px
DrawTemplate: WDT_Inner

Contents (ICON + Label + Value format):

COMBAT (Y=5):
├─ IW_AC_Icon      (StaticAnimation, 16×16) Optional shield icon
├─ IW_AC_Label     (Label) "AC:" - blue
├─ IW_AC_Value     (Label, EQType 22) "1250" - white, right-aligned
├─ IW_ATK_Icon     (StaticAnimation, 16×16) Optional sword icon
├─ IW_ATK_Label    (Label) "ATK:" - orange
└─ IW_ATK_Value    (Label, EQType 23) "950" - white, right-aligned
Subtotal: ~40px (2 stats × 18px per stat + spacing)

VITALS (Y=45):
├─ IW_HP_Icon      (StaticAnimation, 16×16) Heart icon
├─ IW_HP_Label     (Label) "HP:" - red
├─ IW_HP_Value     (Label, EQType 70 or 18) "1200/1200" or "1200" - white
├─ IW_Mana_Icon    (StaticAnimation, 16×16) Mana crystal icon
├─ IW_Mana_Label   (Label) "Mana:" - blue
├─ IW_Mana_Value   (Label, EQType 80 or 20) "800/800" or "800" - white
├─ IW_Stamina_Icon (StaticAnimation, 16×16) Optional stamina icon
├─ IW_Stamina_Label(Label) "Stam:" - yellow
└─ IW_Stamina_Value(Label) "100%" - white
Subtotal: ~60px (3 vitals × 18px per stat + spacing)

ATTRIBUTES (Y=105):
├─ IW_STR_Icon     (StaticAnimation, 16×16) Strength icon (from duxaUI pattern)
├─ IW_STR_Label    (Label) "STR:" - blue
├─ IW_STR_Value    (Label, EQType 5) "180" - white, right-aligned
├─ IW_STA_Icon/Label/Value (EQType 6) - Same pattern
├─ IW_AGI_Icon/Label/Value (EQType 7)
├─ IW_DEX_Icon/Label/Value (EQType 8)
├─ IW_WIS_Icon/Label/Value (EQType 9)
├─ IW_INT_Icon/Label/Value (EQType 10)
└─ IW_CHA_Icon/Label/Value (EQType 11)
Subtotal: ~126px (7 stats × 18px per stat)

RESISTANCES (Y=231):
├─ IW_MR_Icon/Label/Value (EQType 16) Magic resist - purple
├─ IW_FR_Icon/Label/Value (EQType 14) Fire resist - orange
├─ IW_CR_Icon/Label/Value (EQType 15) Cold resist - cyan
├─ IW_DR_Icon/Label/Value (EQType 13) Disease resist - yellow
└─ IW_PR_Icon/Label/Value (EQType 12) Poison resist - teal
Subtotal: ~90px (5 resists × 18px per resist)

MISC (Y=321):
├─ IW_Tribute_Label (Label) "Tribute:" - blue
├─ IW_Tribute_Value (Label, EQType 121-123) "450" - white
├─ IW_AA_Available  (Label) "AA Avail:" - blue
└─ IW_AA_AvailValue (Label, EQType 72) "12/50" - white
Subtotal: ~39px (2 items × 18px + spacing)

TOTAL HEIGHT: 40 + 60 + 126 + 90 + 39 = 355px ✅ Fits in 360px with 5px margin!

Layout per stat line:
  Icon (16×16) at X=0
  Label at X=20 (after icon + 4px gap)
  Value at X=65 (right-aligned within 85px zone)

Modular purpose: Complete character stats display
Variant options:
  - Remove icons (saves 16px width)
  - Abbreviate labels ("ST" instead of "STR:")
  - Show only top 3-4 resistances
  - Move HP/Mana to vitals zone instead
  - Add pet HP gauge (EQType 69 Zeal)
```

### **ZONE 8: Bags (IW_BagZone)**
```xml
Location: (5, 370)
Size: 410×45px
DrawTemplate: WDT_Inner

Contents (8 bags horizontal):
├─ InvSlot22 [BAG1] (45×45, X=5)
├─ InvSlot23 [BAG2] (45×45, X=52)
├─ InvSlot24 [BAG3] (45×45, X=99)
├─ InvSlot25 [BAG4] (45×45, X=146)
├─ InvSlot26 [BAG5] (45×45, X=193)
├─ InvSlot27 [BAG6] (45×45, X=240)
├─ InvSlot28 [BAG7] (45×45, X=287)
└─ InvSlot29 [BAG8] (45×45, X=334)

Spacing: 45px slot + 7px gap = 52px per bag
Total width: 8 bags × 52px - 7px (last gap) = 409px ✅ Fits in 410px

Modular purpose: Primary container access
Variant options:
  - 2×4 grid on side (compact variant)
  - 2 rows × 4 columns (taller, narrower)
  - Integrate into center column below currency
```

### **ZONE 9: Buttons (IW_ButtonBar)**
```xml
Location: (5, 420)
Size: 410×20px
DrawTemplate: None (transparent background)

Contents:
├─ IW_Skills      (Button, 70×20, X=5) "Skills"
├─ IW_AltAdvBtn   (Button, 70×20, X=82) "Alt Adv"
├─ IW_FacePick    (Button, 70×20, X=250) "Face" - right cluster
├─ IW_Destroy     (Button, 70×20, X=327) "Destroy" - right cluster
└─ IW_DoneButton  (Button, 70×20, X=397) "Done" - far right edge (410-70=340, but 397 for margin)

Layout: Left cluster (Skills, Alt Adv), gap, Right cluster (Face, Destroy, Done)
Gap: 327 - 82 - 70 = 175px center gap

Modular purpose: Window actions
Variant options:
  - Add more buttons (Tinting, Tribute, etc.)
  - Reorder buttons by frequency of use
  - Hide less-used buttons in compact variant
```

---

## Variant Design Matrix (Using Lego Blocks)

### **VARIANT A: Standard (Full-Featured, User's Preferred Vision)**

**Window**: 420×440px  
**Layout**: LEFT (Player + Progression + ClassAnim + Weight) | CENTER (Equipment + Currency) | RIGHT (Stats)

```xml
Zones used:
✅ Zone 1: Player Info (5,4) 100×60
✅ Zone 2: Progression (5,68) 100×70
✅ Zone 3: ClassAnim (5,142) 100×160
✅ Zone 4: Equipment 4-row (110,4) 215×200
✅ Zone 5: Currency (110,210) 215×90
✅ Zone 6: Weight (5,306) 100×58
✅ Zone 7: Stats (330,4) 85×360
✅ Zone 8: Bags (5,370) 410×45
✅ Zone 9: Buttons (5,420) 410×20

Features:
- Full player identity
- XP/AA progression at top
- ClassAnim visual
- 4-row anatomical equipment
- Icon + Label + Value stats
- All 5 resistances
- Tribute display
- 8 bags across bottom
```

### **VARIANT B: Compact (Smaller Footprint, Side Bags)**

**Window**: 420×390px  
**Layout**: Same as Variant A but bags move to right side 2×4 grid

```xml
Zones modified:
✅ Zone 1-7: Same positions (adjust Y coordinates down by 30px)
🔄 Zone 8: REMOVED (bags integrated into right column)
✅ Zone 9: Buttons (5,370) - moved up from Y=420 to Y=370

New zone:
✅ Zone 8b: Bags Side Grid (240,210) 90×180
   - 2×4 grid, each bag 45×45
   - Positioned below currency, beside stats bottom

Window height: 420×390 (saves 50px compared to Variant A)
```

### **VARIANT C: Vitals Left (HP/Mana with Player Info)**

**Window**: 420×440px  
**Layout**: LEFT (Player + Vitals + Progression) | CENTER | RIGHT (Stats minus vitals)

```xml
Zones modified:
✅ Zone 1: EXPANDED to 100×110 (add HP/Mana/Stamina gauges)
   - Contents: Name, Level, Class, Deity, HP gauge, Mana gauge, Stamina gauge
🔄 Zone 2: Progression moves to (5,118) - shifted down 50px
🔄 Zone 3: ClassAnim moves to (5,192) - shifted down 50px
✅ Zone 7: Stats REDUCED - remove vitals section
   - Only: Combat (AC/ATK), Attributes, Resistances, Misc
   - New height: 85×320 (40px shorter)

Philosophy: All "life force" info on left (HP, Mana, XP, AA)
Target user: Players who want vitals near identity info
```

### **VARIANT D: 3-Column Equipment (Vertical Dense)**

**Window**: 360×480px (narrower, taller)  
**Layout**: Same structure but equipment uses 3-column vertical layout (vert pattern)

```xml
Zones modified:
🔄 Zone 4: Equipment 3-column (110,4) 130×280
   - 21 slots in 7 rows × 3 columns
   - Slot size: 40×40 (smaller for density)
   - Equipment organized vertically not anatomically

Window adjustments:
- Overall width: 420 → 360px (saves 60px)
- Equipment height: 200 → 280px (adds 80px)
- Stats zone width: 85 → 85px (same)
- Left zones: 100 → 90px (saves 10px)

Target user: Players with limited horizontal screen space
```

### **VARIANT E: Zeal Enhanced (Client-Specific Features)**

**Window**: 420×440px  
**Layout**: Same as Variant A but adds Zeal EQTypes

```xml
Zones modified:
✅ Zone 2: Progression EXPANDED
   - Add XP %/hour rate (EQType 81)
   - Add AA %/hour rate (EQType 86)
   - New size: 100×90 (adds 20px)

✅ Zone 6: Weight EXPANDED
   - Add inventory slot counter (EQType 83/84)
   - "Slots: 12/80"
   - New size: 100×70 (adds 12px)

✅ Zone 7: Stats EXPANDED
   - Add consolidated HP/Mana displays (EQType 70/80)
   - "HP: 1200/1400" instead of separate cur/max
   - Add Pet HP gauge (EQType 69) if applicable
   - New size: 85×380 (adds 20px)

Window adjustment: Increase to 420×460px to accommodate

Features: All Zeal client enhancements activated
Target user: Zeal client users wanting performance metrics
```

---

## Implementation Strategy: Phased Approach

### **Phase 3.9a - Core Modular Structure (THIS SESSION)**

**Goal**: Build the 9-zone subwindow architecture

Tasks:
1. Create all 9 subwindow zones with proper sizing and positioning
2. Move existing pieces into appropriate zones
3. Implement 4-row anatomical equipment layout
4. Add progression gauges (XP/AA) with percentage labels
5. Organize stats with ICON placeholders + Label + Value
6. Test in-game: Ensure all EQTypes bind correctly
7. Verify no overlapping elements, proper spacing

**Estimated time**: 4-5 hours

**Deliverable**: Variant A (Standard) fully functional

---

### **Phase 3.9b - Graphics and Icon Implementation**

**Goal**: Add visual polish with stat/resist icons

Tasks:
1. Create or source stat icon graphics (16×16 for 7 attributes)
2. Create resist icon graphics (16×16 for 5 resist types)
3. Implement duxaUI icon pattern (Ui2DAnimation + StaticAnimation)
4. Add class icon (32×32) in Zone 1
5. Add deity icon (24×24) in Zone 1 (optional)
6. Test all icon rendering in-game

**Estimated time**: 2-3 hours

**Deliverable**: Icons integrated into Variant A

---

### **Phase 3.9c - Variant Creation**

**Goal**: Create 3-4 additional variants using lego block rearrangement

Tasks:
1. Create Variant B (Compact) - adjust bag zone
2. Create Variant C (Vitals Left) - split HP/Mana to left
3. Create Variant D (3-Column Equipment) - vertical dense layout
4. Create Variant E (Zeal Enhanced) - add Zeal EQTypes
5. Document all variants in Options/Inventory/ directory
6. Create README explaining variant differences

**Estimated time**: 3-4 hours

**Deliverable**: 4-5 unique variants ready for testing

---

### **Phase 3.9d - Testing and Refinement**

**Goal**: In-game validation and user feedback integration

Tasks:
1. Test all variants in-game across different classes
2. Verify EQType bindings for all stats/gauges
3. Test drag/drop functionality for equipment/bags
4. Check window positioning and resizing behavior
5. Gather user feedback on layout preferences
6. Refine spacing, colors, alignment based on testing

**Estimated time**: 2-3 hours

**Deliverable**: Production-ready variant files

---

## XML Structure Example (Zone Implementation Pattern)

### Example: Zone 1 (Player Info) Subwindow

```xml
<!-- ZONE 1: Player Identity -->
<Screen item="IW_PlayerInfo">
  <ScreenID>PlayerInfo</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location>
    <X>5</X>
    <Y>4</Y>
  </Location>
  <Size>
    <CX>100</CX>
    <CY>60</CY>
  </Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_VScroll>false</Style_VScroll>
  <Style_HScroll>false</Style_HScroll>
  <Style_Transparent>false</Style_Transparent>
  
  <!-- Player identity elements (RelativePosition coordinates within this zone) -->
  <Pieces>IW_Name</Pieces>
  <Pieces>IW_Level</Pieces>
  <Pieces>IW_LevelValue</Pieces>
  <Pieces>IW_Class</Pieces>
  <Pieces>IW_Deity</Pieces>
</Screen>

<!-- Name Label (relative to IW_PlayerInfo parent) -->
<Label item="IW_Name">
  <ScreenID>Name</ScreenID>
  <RelativePosition>true</RelativePosition>  <!-- CRITICAL! -->
  <Location>
    <X>5</X>   <!-- 5px from left edge of parent zone -->
    <Y>5</Y>   <!-- 5px from top edge of parent zone -->
  </Location>
  <Size>
    <CX>90</CX>
    <CY>14</CY>
  </Size>
  <Text></Text>
  <TextColor>
    <R>255</R>
    <G>255</G>
    <B>255</B>
  </TextColor>
  <Font>3</Font>
  <EQType>1</EQType>
  <NoWrap>true</NoWrap>
</Label>

<!-- Continue for all pieces in this zone... -->
```

### Main Window Pieces List

```xml
<Screen item="InventoryWindow">
  <ScreenID>InventoryWindow</ScreenID>
  <RelativePosition>false</RelativePosition>
  <Location>
    <X>10</X>
    <Y>10</Y>
  </Location>
  <Size>
    <CX>420</CX>
    <CY>440</CY>
  </Size>
  <Text>Inventory</Text>
  <DrawTemplate>WDT_Rounded</DrawTemplate>
  
  <!-- Subwindow zones (order matters - later = rendered on top) -->
  <Pieces>IW_PlayerInfo</Pieces>      <!-- Zone 1 -->
  <Pieces>IW_Progression</Pieces>     <!-- Zone 2 -->
  <Pieces>IW_ClassAnim</Pieces>       <!-- Zone 3 -->
  <Pieces>IW_EquipmentGrid</Pieces>   <!-- Zone 4 -->
  <Pieces>IW_Currency</Pieces>        <!-- Zone 5 -->
  <Pieces>IW_Weight</Pieces>          <!-- Zone 6 -->
  <Pieces>IW_Stats</Pieces>           <!-- Zone 7 -->
  <Pieces>IW_BagZone</Pieces>         <!-- Zone 8 -->
  <Pieces>IW_ButtonBar</Pieces>       <!-- Zone 9 -->
</Screen>
```

---

## Benefits of Modular "Lego Block" Architecture

### **For Development**:
1. ✅ **Easier debugging**: Each zone is self-contained
2. ✅ **Faster iteration**: Modify one zone without affecting others
3. ✅ **Clear organization**: Logical grouping of related elements
4. ✅ **Reusable patterns**: Copy zone definitions across variants
5. ✅ **Version control**: Git diffs show zone-level changes clearly

### **For Customization**:
1. ✅ **Mix and match**: Swap zones between variants
2. ✅ **User testing**: Enable/disable zones to test preferences
3. ✅ **Incremental changes**: Add new zone without rewriting entire file
4. ✅ **Multiple variants**: Create 10+ variants from same base zones
5. ✅ **Future-proof**: Add new features as new zones

### **For User Experience**:
1. ✅ **Consistent spacing**: Zones enforce internal margins
2. ✅ **Visual hierarchy**: Zones create clear visual blocks
3. ✅ **Flexibility**: Users can choose variant that fits their workflow
4. ✅ **Predictability**: Zones maintain consistent positioning across variants
5. ✅ **Accessibility**: Easier to locate information in organized zones

---

## Next Steps: User Approval Decision Points

---

## Equipment Grid Redesign: 4-Column Anatomical Layout (REVISED)

**Current Status**: 5-column layout doesn't account for EQ's single-item constraints  
**Goal**: 4-column layout respecting actual EQ inventory (only ears, wrists, rings are dual)  
**Constraint**: Keep anatomical ordering (top to bottom)

### **EverQuest Equipment Slots - The Reality**

Single slots (only one in inventory):
- Head, Face, Neck, Chest, Back, Shoulders, Arms, Waist, Legs, Feet
- Primary, Secondary, Range, Ammo

Double slots (left and right):
- Ears (L Ear, R Ear)
- Wrists (L Wrist, R Wrist)  
- Rings (L Ring, R Ring)

**Total**: 20 equipment slots

### **4-Column Anatomical Layout (REVISED)**

```
┌────────────────────────────────────────────────────────┐
│ EQUIPMENT GRID - 4 Column Anatomical Layout            │
├────────────────────────────────────────────────────────┤
│ ROW 1 (Y=0):   L Ear   | Face    | Head    | R Ear    │
│ ROW 2 (Y=47):  Neck    | Chest   | Back    | Shoulders│
│ ROW 3 (Y=94):  L Wrist | Arms    | Waist   | R Wrist  │
│ ROW 4 (Y=141): L Ring  | Legs    | Feet    | R Ring   │
│ ROW 5 (Y=188): Primary | Secondary | Range | Ammo    │
└────────────────────────────────────────────────────────┘

Total: 20 slots ✓
Height: 235px (fits in expanded window comfortably)
Slot Size: 45×45px (normal, readable)
Column Width: 190px (fits in 215px available space)
```

### **Rationale for Each Row**

**Row 1 (Head Zone)**:
- `L Ear | Face | Head | R Ear`
- Ears frame the face and head naturally
- Left-to-right reading order makes sense

**Row 2 (Torso Armor)** ⭐:
- `Neck | Chest | Back | Shoulders`
- **All core body armor on same line (as requested!)**
- Shoulders caps the shoulder area
- Order: Front center → back → support

**Row 3 (Limbs & Joints)**:
- `L Wrist | Arms | Waist | R Wrist`
- Wrists frame the central arm and waist area
- Natural limb positioning (respects single Arms slot)

**Row 4 (Lower Body & Accessories)**:
- `L Ring | Legs | Feet | R Ring`
- Rings are accessories worn with hands
- Legs and feet together make sense (respects single Legs and Feet slots)
- Creates natural symmetry with Row 3

**Row 5 (Weapons)**:
- `Primary | Secondary | Range | Ammo`
- All combat items together
- Natural weapon progression

### **Layout Calculations**

**Slot Size**: 45×45px + 1px gaps

```
Column 1: X=0    (45px wide)
Column 2: X=46   (45px wide, +1px gap)
Column 3: X=92   (45px wide, +1px gap)
Column 4: X=138  (45px wide, +1px gap)
Total Width: 183px

Row Heights (45px per slot + 1px gaps):
Row 1 (Head):        Y=0,   45px high
Row 2 (Torso):       Y=46,  45px high (+1px gap)
Row 3 (Limbs):       Y=92,  45px high (+1px gap)
Row 4 (Lower):       Y=138, 45px high (+1px gap)
Row 5 (Weapons):     Y=184, 45px high (+1px gap)

Total Height: 229px (fits comfortably in 235px zone)
```

### **Inventory Slot Mapping**

| Row | Col1 | Col2 | Col3 | Col4 | Notes |
|-----|------|------|------|------|-------|
| 1 | L Ear (1) | Face (3) | Head (2) | R Ear (4) | Reordered for layout |
| 2 | Neck (5) | Chest (8) | Back (13) | Shoulders (6) | **All core armor together** |
| 3 | L Wrist (9) | Arms (7) | Waist (20) | R Wrist (10) | Limbs & joints |
| 4 | L Ring | Legs (19) | Feet (15) | R Ring | Lower body + ring accessories |
| 5 | Primary (21) | Secondary (22) | Range (11) | Ammo (12) | Weapons |

### **Why This Works Better**

✅ **Chest and Back together** - Both main torso protection on Row 2 (as requested!)  
✅ **Respects EQ constraints** - Only ears, wrists, rings are dual; everything else is single  
✅ **Dual symmetry** - Ears, Wrists, and Rings naturally frame their respective areas  
✅ **Anatomical flow** - Head → Torso → Limbs → Lower → Weapons  
✅ **45×45px slots** - Much more readable than current tiny slots  
✅ **20 slots exactly** - No gaps or waste  
✅ **5 rows** - Fits in expanded 470px window  

---

## Before Implementation Please Confirm

1. **Layout Approval**: Does this 5-row × 4-column arrangement feel right to you?

2. **Slot Size**: Confirmed 45×45px? (Can adjust to 50×50px if you'd prefer larger)

3. **Window Height**: OK with 470px total? (Current expanded size)

4. **Next Steps**: Ready to start XML refactoring of InvSlot positions with this new layout?


