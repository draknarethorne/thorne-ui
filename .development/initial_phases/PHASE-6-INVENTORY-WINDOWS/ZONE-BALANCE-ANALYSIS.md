# Zone Height Balance Analysis - CRITICAL DESIGN DECISION

**Date**: February 4, 2026  
**Status**: DETAILED CALCULATIONS FOR 4 LAYOUT OPTIONS  
**Issue**: Current 5-zone design has vertical imbalance - Stats zone (240px tall) cannot accommodate all stat items (504px content)

---

## 1. Current Design Problem: Height Mismatch

### Component Height Inventory

**LEFT ZONE (IW_LeftZone) - Specified: 85×350px**

```
Items:
├─ IW_Name             (Label) - ~14px (height)
├─ IW_Level            (Label) - ~14px
├─ IW_Class            (Label) - ~14px
├─ IW_Deity            (Label) - ~14px
├─ IW_Race             (Label, future) - ~14px
├─ IW_CharacterView    (Screen, ClassAnim) - 74×138px
├─ IW_Weight           (Label) - ~14px
├─ IW_CurrentWeight    (Label) - ~14px
└─ IW_FacePick         (Button) - 20px

TOTAL CONTENT HEIGHT: 14+14+14+14+14+138+14+14+20 = 256px
ZONE SIZE: 350px
AVAILABLE MARGIN: 350 - 256 = 94px EXTRA ✅ (33% unused)
```

**EQUIPMENT GRID (IW_EquipmentGrid) - Specified: 215×300px**

```
Items:
├─ ROW 1 (HEAD): Y=5
│  ├─ InvSlot1 [L.EAR]    (45×45)
│  ├─ InvSlot5 [NECK]     (45×45)
│  ├─ InvSlot3 [FACE]     (45×45)
│  ├─ InvSlot2 [HEAD]     (45×45)
│  └─ InvSlot4 [R.EAR]    (45×45)
│  Total height: 45px
│
├─ ROW 2 (ARMS): Y=52 (47px gap)
│  ├─ InvSlot15 [L.RING]  (45×45)
│  ├─ InvSlot9 [L.WRIST]  (45×45)
│  ├─ InvSlot7 [ARMS]     (45×45)
│  ├─ InvSlot12 [HANDS]   (45×45)
│  ├─ InvSlot10 [R.WRIST] (45×45)
│  └─ InvSlot16 [R.RING]  (45×45)
│  Total height: 45px
│
├─ ROW 3 (TORSO): Y=99 (47px gap)
│  ├─ InvSlot6 [SHOULDERS] (45×45)
│  ├─ InvSlot17 [CHEST]    (45×45)
│  ├─ InvSlot8 [BACK]      (45×45)
│  ├─ InvSlot20 [WAIST]    (45×45)
│  ├─ InvSlot18 [LEGS]     (45×45)
│  └─ InvSlot19 [FEET]     (45×45)
│  Total height: 45px
│
├─ ROW 4 (WEAPONS): Y=146 (47px gap)
│  ├─ InvSlot13 [PRIMARY]  (45×45)
│  ├─ InvSlot14 [SECONDARY] (45×45)
│  ├─ InvSlot11 [RANGE]    (45×45)
│  └─ InvSlot21 [AMMO]     (45×45)
│  Total height: 45px
│
└─ CURRENCY: Y=200 (54px gap)
   ├─ IW_Money0 [PLATINUM]  (70×24)
   ├─ IW_Money1 [GOLD]      (70×24)  
   ├─ IW_Money2 [SILVER]    (70×24)
   └─ IW_Money3 [COPPER]    (70×24)
   Total height: ~96px (4 coins, 24px each, possibly 2 columns)

TOTAL CONTENT HEIGHT: 4 rows (180px) + currency (96px) = 276px
ZONE SIZE: 300px
AVAILABLE MARGIN: 300 - 276 = 24px ✅ (8% unused)
```

**STATS ZONE (IW_StatsZone) - Specified: 80×240px**

```
COMBAT STATS:
├─ IW_AC_Label        (Label) "AC:" - ~14px
├─ IW_AC_Value        (Label, EQType 22) - ~14px
├─ IW_ATK_Label       (Label) "ATK:" - ~14px
└─ IW_ATK_Value       (Label, EQType 23) - ~14px
Subtotal: 56px

VITALS:
├─ IW_HP_Label        (Label) "HP:" - ~14px
├─ IW_HP_Value        (Label, EQType 70/18) - ~14px
├─ IW_Mana_Label      (Label) "Mana:" - ~14px
└─ IW_Mana_Value      (Label, EQType 80/20) - ~14px
Subtotal: 56px

ATTRIBUTES (7 stats, each with label + value = 14 items):
├─ IW_STR_Label       (Label) "STR:" - ~14px
├─ IW_STR_Value       (Label, EQType 5) - ~14px
├─ IW_STA_Label/Value - ~28px
├─ IW_AGI_Label/Value - ~28px
├─ IW_DEX_Label/Value - ~28px
├─ IW_WIS_Label/Value - ~28px
├─ IW_INT_Label/Value - ~28px
└─ IW_CHA_Label/Value - ~28px
Subtotal: 7 stats × 2 items × 14px = 196px

RESISTANCES (5 types, each with label + value = 10 items):
├─ IW_Poison_Label/Value - ~28px
├─ IW_Fire_Label/Value   - ~28px
├─ IW_Cold_Label/Value   - ~28px
├─ IW_Disease_Label/Value - ~28px
└─ IW_Magic_Label/Value  - ~28px
Subtotal: 5 resists × 2 items × 14px = 140px

MISC:
├─ IW_Tribute_Label   (Label) "Tribute:" - ~14px
├─ IW_Tribute_Value   (Label, EQType 121) - ~14px
└─ IW_AA_Available    (Label, EQType 72) - ~14px
Subtotal: 42px

TOTAL CONTENT HEIGHT: 56 + 56 + 196 + 140 + 42 = 490px ❌ OVERFLOW!
ZONE SIZE: 240px
CONTENT OVERFLOW: 490 - 240 = 250px OVER! ❌ (204% of zone size needed!)
```

**PROGRESSION ZONE (IW_ProgressionZone) - Specified: 80×60px**

```
Items:
├─ IW_ExpGauge       (Gauge, 116×8) - 8px height
├─ IW_EXP_Percentage (Label) "85%" - ~14px height  
├─ IW_AltAdvGauge    (Gauge, 116×8) - 8px height
├─ IW_AltAdv_Label   (Label) "AA:" - ~14px height
└─ IW_AltAdv_Points  (Label, EQType 71) - ~14px height

TOTAL CONTENT HEIGHT: 8 + 14 + 8 + 14 + 14 = 58px ✅ (fits in 60px with 2px margin)
ZONE SIZE: 60px
```

**BAG ZONE (IW_BagZone) - Specified: 300×45px**

```
Items:
├─ InvSlot22 [BAG1]  (45×45) - single row
├─ InvSlot23 [BAG2]  (45×45)
├─ InvSlot24 [BAG3]  (45×45)
├─ InvSlot25 [BAG4]  (45×45)
├─ InvSlot26 [BAG5]  (45×45)
├─ InvSlot27 [BAG6]  (45×45)
├─ InvSlot28 [BAG7]  (45×45)
└─ InvSlot29 [BAG8]  (45×45)

TOTAL HEIGHT: 45px ✅ (fits in 45px exactly, width might need adjustment)
```

### Summary of Current Design Balance

| Zone | Width | Height | Content | Usage | Balance |
|------|-------|--------|---------|-------|---------|
| **LeftZone** | 85px | 350px | 256px | 73% | ✅ Good |
| **EquipmentGrid** | 215px | 300px | 276px | 92% | ✅ Good |
| **StatsZone** | 80px | 240px | 490px | 204% | ❌ **CRITICAL** |
| **ProgressionZone** | 80px | 60px | 58px | 97% | ✅ Good |
| **BagZone** | 300px | 45px | 45px | 100% | ✅ Good |
| **Window Total** | 400px | 410px | --- | --- | ❌ Imbalanced |

---

## 2. THE CORE PROBLEM

**StatsZone is too small for the content:**
- Currently: 240px height with 80px width
- Content: 490px of items (labels + values for combat, vitals, 7 attributes, 5 resistances, tribute)
- **Problem**: Items will overlap, scroll, or stack vertically and break the layout

**LeftZone has excess capacity:**
- Currently: 350px with only 256px content
- Available: 94px unused space
- **Available for reuse**: Could accommodate progression zone (60px) with margin

**Visual Balance Issue:**
- Right column (Stats) appears cramped while Left column appears sparse
- Equipment grid height (300px) is between left (350px) and right (240px)
- Creates visual triangle with point at right - aesthetically unbalanced

---

## 3. VECTOR ANALYSIS: FOUR LAYOUT OPTIONS

### **OPTION A: 3-Column Anatomical (duxaUI Pattern)**

**Concept**: Collapse 5 zones into 3 columns, mimicking duxaUI layout. Equipment and stats share right column space.

**Layout Structure**:
```
Window: 400×410px

┌────────────────────────────────────────┐
│ LEFT: Char Info  │ CENTER: Equipment   │ │ TOP (Y=4):
│ (5,4)            │ + Stats mixed       │ │ LeftZone: 85×280
│ 85×280           │ (95,4)              │ │
│                  │ 215×280             │ │ CenterZone: 215×280
│                  │                     │ │ (equipment rows 1-3)
├────────────────────────────────────────┤ │
│ LEFT CONTINUED   │ CENTER CONTINUED    │ │ MIDDLE:
│ (5,288)          │ (95,288)            │ │ Same zones continue
│ 85×62            │ 215×62              │ │ LeftZone: 85×122
│                  │ (equipment row 4)   │ │ CenterZone: 215×62
├────────────────────────────────────────┤ │
│ Right Column: Combined Stats           │ │ RIGHT SIDE:
│ (305,4)          Equipment Row 4 ROW   │ │ RightZone: 90×350
│ 90×350           (weapons)             │ │
│ • Vitals         Stats: Attributes +   │ │
│ • Attributes     Resistances           │ │
│ • Resistances    + Progression info    │ │
│ • Progression    at very bottom        │ │
│ • Currency       (if space)            │ │
├────────────────────────────────────────┤ │
│ BAGS + BUTTONS (full width)             │ │ BOTTOM:
│ (95, 360) BagZone: 300×45              │ │ BagZone: 300×45
│ Buttons Y=390                           │ │ Buttons: Y=390
└────────────────────────────────────────┘ │
```

**Coordinate Recalculation**:
- Left Char Zone: (5,4) 85×280
- Center Equipment 1-3: (95,4) 215×240 (3 equipment rows)
- Center Equipment 4: (95,244) 215×45 (weapons row)
- Right Stats: (305,4) 90×350 (all stats stacked)
- Bags: (95,360) 300×45
- Buttons: (5,390) and (299,390) Y=390 for 410px window

**Pros ✅**:
- Right column now 350px - matches left column height
- Visual symmetry (left 350, right 350, center 300)
- Equipment and stats logically on right (interactive/read-only split)
- Proven pattern: duxaUI uses similar approach
- Easier item alignment - right column can use single column

**Cons ❌**:
- Moves away from 5-subwindow architecture we designed
- Equipment becomes 2D (rows 1-3 in one zone, row 4 separate)
- Stats column becomes 350px wide at minimum (90px × items won't fit comfortably)
- Requires stat label rewording to fit narrower column
- Less modular/maintainable than 5-subwindow design

**Height Math**:
```
Left Zone: 256px content (fits 280px) ✅
Center Zone: 240px + 45px = 285px content (fits 285px) ✅✅
Right Zone: 490px content (fits 350px) ❌ Still too small!

Option A VERDICT: Still doesn't fully solve stats overflow!
```

---

### **OPTION B: Move Progression Under Player Info Zone**

**Concept**: Keep 5-zone architecture but relocate progression under player info in left zone, freeing up right column for more stats.

**Layout Structure**:
```
Window: 400×410px

┌────────────────────────────────────────┐
│ LEFT ZONE (5,4)  │ EQUIPMENT  │ STATS  │
│ 85×350           │ (95,4)     │ (315,4)
│                  │ 215×300    │ 80×240
│
│ • Name           │ • 4 Rows   │ • AC
│ • Level          │   Equipment│ • ATK
│ • Class          │ • Currency │ • Vitals
│ • Deity          │            │ • Attributes
│ • Race*          │ ┌──────────┤ • Resistances
│
│ • ClassAnim      │ │          ├──────────────
│   74×138         │ │          │
│                  │ │          │ PROGRESSION
│ • Weight         │ │          │ (315,250)
│                  │ │          │ 80×60
│                  │ │          │
│ • PROGRESSION    │ │          │ • XP Gauge
│   (NEW!)         │ │          │ • AA Gauge
│   5,256→       │ │          │
│   80×80        │ │          │
│                  │ │          │
│   • XP Bar       │ │          │
│   • AA Bar       │ │          │
└────────────────────────────────────────┘
│ BAGS + BUTTONS                          │
└────────────────────────────────────────┘
```

**Coordinate Changes**:
- IW_LeftZone: (5,4) 85×350 - **KEEP** (same size)
  - Add progression elements at Y=256 (below weight)
  - IW_ExpGauge: (Y=256) within left zone
  - IW_AltAdvGauge: (Y=276) within left zone
- IW_EquipmentGrid: (95,4) 215×300 - **KEEP** (same)
- IW_StatsZone: (315,4) 80×320 - **EXPAND HEIGHT TO 320px**
  - Now has 320px instead of 240px
  - Can accommodate stat items better: 320 vs 490 = 65% (better than 50%)
- IW_ProgressionZone: **DELETE/MERGE** into LeftZone
- IW_BagZone: (95,360) 300×45 - **KEEP** (same)

**Revised Space Usage**:
```
LeftZone: 256px (content) + 60px (progression) = 316px content
          Fits in 350px with 34px margin ✅

StatsZone: 490px content (fits 320px) - Better! But still overflows by 170px ❌
           (34% overflow instead of 204% overflow)
```

**Critical Question**: **Will the ClassAnim (74×138) interfere with progression gauges below?**
- ClassAnim: Y position TBD, estimated around Y=70-100
- ClassAnim: 74×138, so bottom = Y+138 = 208-238
- Current weight display: ~Y=220
- Proposed progression: Y=256+
- **Gap between ClassAnim and progression: ~20px** - TIGHT but might work

**Pros ✅**:
- Keeps 5-zone subwindow architecture (what we designed)
- Right column visually shorter (250px shows) vs left (350px)
- Progression and character info logically grouped
- Solves the "zones stacked vertically" visual problem
- Frees right column for additional stats content
- ClassAnim can be repositioned if needed

**Cons ❌**:
- Requires moving relational positioning of ClassAnim, Weight, Progression items
- Progression gauges (116px wide) might not fit in 85px zone width!
  - **MAJOR ISSUE**: XP Gauge is 116px wide, zone is only 85px
  - Would cause horizontal overflow/clipping
- Creates mixed stat display: top items in left zone (progression), rest in right
- **Breaks the functional separation** of stats vs progression

**Height Math - Final**:
```
LeftZone: 316px content in 350px ✅
StatsZone: 490px content in 320px ❌ (170px overflow)
Result: Better but not solved. Still need to reduce stats items.
```

---

### **OPTION C: Swap Stats and Progression Zones, Adjust Bag Zone**

**Concept**: Progression at top (small, Y=4), Stats at middle (larger), Bags take remaining space or move to side. Pushes all content down to gain stats space.

**Layout Structure**:
```
Window: 400×410px

TOP (Y=4):
┌────────────────────────────────────────┐
│ LEFT CHAR  │ LEFTMID EQUIP  │ STATS  │ TOP ZONE (4-64):
│ (5,4)      │ (95,4)         │ (315,4)│ • Progression
│ 85×60      │ 215×110        │ 80×60  │   gauges here
│ • Name     │ ROW 1-2 equip  │ Quick  │
│ • Level    │            (110px only) │  Stats subset
│ • Class    │                │ AC/ATK │
│            │                │ HP/Mana│
├────────────────────────────────────────┤ MIDDLE (Y=70):
│ LEFT INFO  │ EQUIPMENT      │ STATS  │ • Full stats here
│ (5,70)     │ CONTINUES      │ ZONE   │ • Attributes
│ 85×280     │ (95,110)       │ (315,70)
│ • Deity    │ ROW 3-4 equip  │ 80×280 │
│ • CharAnim │ • Currency     │ • All stats
│ • Weight   │                │ (490px content)
│            │                │        │
│            │ Total: 215×280│ Total: 80×280
├────────────────────────────────────────┤ BOTTOM:
│ BAGS + BUTTONS                          │ • Full width
│ 8 bags (95,360) + buttons Y=390        │
└────────────────────────────────────────┘
```

**Coordinate Changes**:
- IW_ProgressionZone: (315,4) 80×60 - **MOVE TO TOP** (was at Y=250)
- IW_EquipmentGrid: (95,4) 215×280 - **SHRINK HEIGHT** (was 300)
  - Split equipment: Row 1-2 in top part, Row 3-4 in middle
  - This fragments the equipment grid - BAD DESIGN
- IW_StatsZone: (315,70) 80×280 - **MOVE DOWN, EXPAND HEIGHT** (was at Y=4, height 240)
  - Now more space for stats items
- IW_LeftZone: Keep (5,4) 85×350 but reorganize items vertically
- IW_BagZone: (95,360) 300×45 - **KEEP** (same)

**Revised Space Usage**:
```
StatsZone: 490px content in 280px ❌ (210px overflow, worse!)
EquipmentGrid: Now split/fragmented ❌ (poor design)
Result: Makes things worse! Equipment becomes 2-part zone with stats in between.
```

**Pros ✅**:
- Moves progression out of large zone (since it's small)
- Theoretically creates more vertical space

**Cons ❌** (MAJOR):
- Equipment grid split into two zones separated by stats (poor UX)
- Equipment coordinates change - Row 3-4 move to different parent zone
- **Most confusing architecture** - equipment not together
- Reduces equipment grid height to 280px (still 276px content fits, but fragmentation is terrible)
- No real benefit - stats still overflow
- Violates our 5-subwindow architectural principle

**VERDICT**: ❌ **Not recommended** - creates fragmented, poor-UX design

---

### **OPTION D: Move Bags to Left Side, Free Right Column**

**Concept**: Vertical 2×4 bag grid on far left (replaces LeftZone), move character info to center-left, stats get full right column plus expanded below bags.

**Layout Structure**:
```
Window: 420×410px (needs expansion for side bag layout!)

┌───────────────────────────────────────────┐
│ BAGS   │ LEFT CHAR  │ EQUIPMENT  │ STATS  │
│(5,4)   │ (55,4)     │ (125,4)    │(315,4) │
│2×4     │ 60×350     │ 185×300    │80×340  │
│45×180  │            │            │        │
│        │ • Name     │ • ROW 1-4  │ • ALL  │
│        │ • Level    │   Equipment│  Stats │
│        │ • Class    │ • Currency │ (350px │
│        │ • Deity    │            │  for   │
│        │ • Race     │            │ 490px) │
│        │ • ClassAnim│            │  ❌    │
│        │ • Weight   │            │        │
│        │            │            │        │
├────────┼────────────┼────────────┼────────┤
│ BAG    │   CONTINUATION...   │ PROG ZONE
│ CONTD  │                     │ (315,300)
│        │                     │ 80×60
│        │                     │
├────────────────────────────────────────┤
│ BUTTONS: Y=390                          │
│ [Domain] [Alt Adv Button] [Done]       │
└───────────────────────────────────────┘
```

**Coordinate Changes**:
- IW_LeftZone: **REMOVED/REPLACED**
- IW_BagZone: (5,4) 45×180 - **MOVE TO LEFT, MAKE 2×4 VERTICAL**
  - InvSlot22-25: Column 1 (Y=4,51,98,145)
  - InvSlot26-29: Column 2 (X=46, Y=4,51,98,145)
  - Zone size: 96×184 (actual) vs 45×190 (reserved)
  - **Problem: 96px width extends bag zone out!**
- IW_LeftZone: (55,4) 60×350 - **COMPRESS WIDTH FOR CHARACTER INFO ONLY**
  - Only Name/Level/Class/Deity/Race/Weight/Buttons
  - ClassAnim removed or minimized
  - **Problem: Where does 74×138 ClassAnim go?**
- IW_EquipmentGrid: (125,4) 185×300 - **REDUCE WIDTH**
  - All equipment still fits in 185px (currently 215px)
- IW_StatsZone: (315,4) 80×340 - **EXPAND HEIGHT TO 340px**
  - Stats content: 490px in 340px = 144% overflow ❌ (still doesn't fit)
- IW_ProgressionZone: (315,350) 80×60 - **MOVE TO BOTTOM** (below stats)

**Revised Space Usage**:
```
Window width: Needs increase to 420px from 400px (to accommodate side bag grid properly)
BagZone: Takes 96px width on left
LeftCharZone: 60px width (very cramped for ClassAnim!)
EquipmentGrid: 185px width (tight squeeze)
StatsZone: 340px height ❌ Still overflows (490-340=150px over)

ClassAnim: 74×138 - DOESN'T FIT in 60px wide zone!
Result: Would require removing ClassAnim or massive redesign.
```

**Pros ✅**:
- Frees right column for more stats space (340px vs 240px)
- Visual symmetry: bags left, stats right

**Cons ❌** (MAJOR):
- Requires window width expansion to 420px+ (loses screen space benefit)
- ClassAnim (74px wide) doesn't fit in 60px column
- Character info zone becomes claustrophobic
- 490px stats content still overflows 340px space (only 69% utilization)
- Loses the visual "zones stacked vertically" improvement of current design
- More complex coordinate recalculation

**VERDICT**: ❌ **Not recommended** - doesn't solve stats overflow, breaks ClassAnim display, requires window expansion

---

## 4. ROOT CAUSE: TOO MANY STATS ITEMS

All four options struggle with the same core issue: **We have 490px of stats content in a space that realistically only supports 240-340px.**

### What Causes the Overflow?

```
Optimal stat layout (from community UIs):
- Combat stats (AC, ATK, HP, Mana): ~56px
- Attributes (7 stats): ~84px (if condensed)
- Resistances (5 types): ~84px (if condensed)
Total: ~224px ✅

Our current design:
- Combat stats: 56px
- Vitals: 56px (separate from stats)
- Attributes: 196px (label + value per stat)
- Resistances: 140px (label + value per resist)
- Misc (Tribute, AA): 42px
Total: 490px ❌

Where's the bloat?
1. **Duplicate HP/Mana displays**: Combat section AND Vitals section?
2. **Full label+value per stat**: "STR:" + "180" = 28px per stat
3. **Every resistance gets pair**: Poison label + value, Fire label + value, etc.
```

---

## 5. RECOMMENDATION: OPTIMIZED OPTION B+ (HYBRID SOLUTION)

**Hybrid Approach**: Combine best of Options B and community patterns.

### Design Philosophy
1. **Keep 5-subwindow architecture** (good design)
2. **Move progression to left zone** (frees right column height)
3. **Condense stats display** (reduce content overflow)
4. **Use community patterns** (duxaUI stat icons, QQQuarm percentages)

### New Proposed Layout

```
Window: 400×440px (add 30px for stats comfort)
OR Window: 420×410px (wider instead of taller)

OPTION B+ VARIANT 1 - Taller Window (400×440px):
┌────────────────────────────────────────┐
│ LEFT         │ EQUIPMENT  │ STATS      │
│ (5,4)        │ (95,4)     │ (315,4)    │
│ 85×350       │ 215×300    │ 80×300     │ INCREASED from 240→300
│              │            │            │
│ • Name       │ • ROW 1    │ • AC: 1250 │
│ • Level      │   Equipment│ • ATK: 950 │
│ • Class      │ • ROW 2    │ • HP: 1200 │
│ • Deity      │   Equipment│ • Mana: 800│
│ • Race       │ • ROW 3    │ • STR: 180 │
│              │   Equipment│ • STA: 175 │
│ • ClassAnim  │ • ROW 4    │ • AGI: 110 │
│                           │ • DEX: 115 │
│              │ • Currency │ • WIS: 95  │
│              │            │ • INT: 90  │
│ • PROG ZONE  │ │            │ • CHA: 85  │
│   (256)      │ │            │ • MR: 100  │
│ • XP:████ 85%│ │            │ • FR: 100  │
│ • AA:████ 12pt│ │            │ • CR: 100  │
│              │ │            │ • DR: 100  │
│ • Weight:85/3│ │            │ • PR: 100  │
│              │ │            │ • Tribute: 450
├────────────────────────────────────────┤ (Bag row moved to Y=360)
│ BAGS: [Bag1][Bag2]...[Bag8]             │
│ (95,360) 8×45px                         │
├────────────────────────────────────────┤
│ [Alt Adv Button]     [Done Button]      │  Y=410
└────────────────────────────────────────┘
Total Window: 400×440px
```

**Or OPTION B+ VARIANT 2 - Wider Window (420×410px)**:
```
Window: 420×410px

┌──────────────────────────────────────────┐
│ LEFT (5,4)   │ EQUIPMENT    │ STATS      │
│ 85×350       │ (95,4)       │ (305,4)    │
│              │ 215×300      │ 100×300    │ EXPANDED width to 100px
│              │              │ (from 80px)
│ Same content │              │            │
│ as before    │              │ More room  │
│              │              │ for labels!
│              │              │
│ • XP Prog    │              │ • AC: 1250
│   Y=256      │              │ • ATK: 950
│ • AA Prog    │              │ • HP: 1200
│   Y=276      │              │ • Mana: 800
│              │              │ • STR icon: 180
│              │              │ • STA icon: 175
│              │              │ (etc, with icons)
├──────────────────────────────────────────┤
│ BAGS + BUTTONS as normal                 │
└──────────────────────────────────────────┘
Total Window: 420×410px
```

**Height Math for B+ Variant 1 (400×440px)**:
```
LEFT ZONE: 316px content in 350px ✅
EQUIPMENT: 276px content in 300px ✅
STATS: 490px content in 300px ❌ (190px overflow) - but improved from 204%!

Still needs optimization of stats...
```

### Solution: Compress Stats With Icons/Abbreviations

**Community pattern solutions**:
1. **Use abbreviated labels**: "ST" instead of "STR:" (save 3-4px per line)
2. **Implement stat icons** (duxaUI pattern): 16×16 icon + "180" saves label space
3. **Combine on same line**: "STR 180" instead of "STR:" on one line, "180" on another
4. **Remove some resistances**: Only show top 3-4 most important (MR, FR, CR, DR)
5. **Use percentage format**: Draw progress bar instead of text for secondary stats

**With these optimizations**:
```
Optimized stat layout:
- Top vital info (AC, ATK, HP, Mana): 40px (condensed)
- Attributes with icons (7 stats): 84px (icon + value, no label)
- Key resistances (4 types): 56px (icon + value, no label)
- Progression info: 30px (gauges)
- Tribute: 14px
Total: ~224px ✅ Fits in 240-300px!
```

---

## 6. FINAL RECOMMENDATION: OPTION B+ WITH STATS OPTIMIZATION

### Recommended Path Forward

**Choose ONE of these two**:

### **OPTION B+v1: Taller Window (400×440px)**

```
Pros:
✅ Minimal layout disruption
✅ Keeps 5-subwindow architecture
✅ Progression under player info (logical grouping)
✅ Stats get comfortable space
✅ All equipment together
✅ Progression fits left zone width (if adjusted)
✅ No ClassAnim relocation needed

Cons:
🔶 Window height increases from 410→440px (30px larger)
🔶 Still requires stats optimization (icons/abbrev)
🔶 Progression gauges (116px) still don't fit in left zone (85px)
   → Need to condense progression into 85px or move to right

Action: Expand window to 400×440px, optimize stats with icons, condense progression labels
```

### **OPTION B+v2: Wider Window (420×410px)**

```
Pros:
✅ Keeps 5-subwindow architecture
✅ Progression under player info (logical)
✅ Stats zone expanded to 100px width (better label fit)
✅ Equipment grid has more width (215→215 same, but window wider distributes space)
✅ Progression gauges fit in left zone 85px?
   → No, 116px gauge still overflows! Need separate line or condensed

Cons:
🔶 Window width increases from 400→420px (20px wider, less screen space benefit)
🔶 Still requires stats optimization
🔶 Progression gauges need relocation/resizing

Action: Expand to 420×410px, expand stats zone to 100px, reorganize progression
```

### **MY RECOMMENDATION: OPTION B+v2 (420×410px Wider)**

**Rationale**:
1. Horizontal expansion (420px) has less visual impact than vertical (440px)
2. Stats zone becomes 100px wide - more room for labels/icons
3. Equipment grid maintains 215px (centered between 420px width)
4. Left zone stays 85px (character info), adds progression below
5. Progression gauges need to shrink slightly or stay at 116px with overflow into next row (below stats)

**Final Layout (400×410px BASELINE with Option B+ adjustments)**:

```
KEEP CURRENT BUT:
1. Rename IW_LeftZone → IW_CharacterZone ("player info" zone)
2. Move progression zone items into bottom of character zone (Y=256+)
3. Expand stats zone height 240→300px
4. Reduce stats overflow with:
   - Icon-based stat display (duxaUI pattern)
   - Abbreviated resistance labels
   - Condensed formatting
5. Test: If progression gauges overflow left zone...
   - Option: Wrap to second column in left zone
   - Option: Split labels/gauges vertically
```

### Height Calculations - Final Optimized

**Left Zone (IW_CharacterZone) - Expanded to accommodate progression**:
```
Name: 14px
Level/Class: 14px
Deity/Race: 28px
ClassAnim: 138px
Weight: 28px
─────────
Subtotal: 222px

PROGRESSION:
XP Label/Gauge: 28px
AA Label/Gauge: 28px
─────────
Subtotal: 56px

TOTAL: 278px in 350px ✅ (20% margin)
```

**Equipment Zone (IW_EquipmentGrid) - Same**:
```
4 equipment rows: 180px
Currency: 96px
─────────
TOTAL: 276px in 300px ✅ (8% margin)
```

**Stats Zone (IW_StatsZone) - Optimized with icons**:
```
With icon+value condensation:
- Vital info (AC, ATK, HP, Mana): 40px
- 7 Attributes (icon+value): 84px
- 4 Resistances (MR, FR, CR, DR): 56px
- Tribute/Misc: 28px
─────────
TOTAL: 208px in 240px ✅ (13% margin)
```

**Window Total**: 400×410px ✅ **BALANCED**

---

## NEXT STEPS: APPROVAL DECISION

**User needs to decide which option to proceed with:**

| Option | Size | Left | Equipment | Stats | Window | Status |
|--------|------|------|-----------|-------|--------|--------|
| **Current (Original)** | 400×410 | 350 | 300 | 240 | ❌ Imbalanced |❌ No |
| **OPTION A** (3-Column) | 400×410 | N/A | 300 | 350 | ✅ Balanced | ❌ Complex |
| **OPTION B** (Prog in Left) | 400×410 | 350 | 300 | 240 | ❌ Still overflow | ❌ No |
| **OPTION B+v1** (Taller) | 400×440 | 350 | 300 | 300 | ✅ Balanced | ✅ **GOOD** |
| **OPTION B+v2** (Wider) | 420×410 | 350 | 215 | 100 +margin | ✅Balanced | 🔶 Moderate |
| **OPTION B+Final** (optimized) | 400×410 | 350 | 300 | 240 (optimized) | ✅ Balanced | ✅ **BEST** |

---

**RECOMMENDATION**: **OPTION B+ Final with Stats Icon Optimization**

Keep the 400×410px window size. Implement:
1. Move progression under player info (rename to IW_CharacterZone)
2. Optimize stats display with icon-based layout (duxaUI pattern)
3. Abbreviate resistance labels where needed
4. Test gauge sizing in left zone (may need slight adjustment)

This maintains our current window footprint while solving the balance issue through smart UI optimization rather than window expansion.

