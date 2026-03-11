# Current Inventory Window - Structure Analysis

**Date**: February 4, 2026  
**File**: `thorne_drak/EQUI_Inventory.xml`  
**Purpose**: Deep analysis before Phase 3.9 redesign

---

## Current Window Dimensions

**Main Window (`InventoryWindow`)**:
- **Size**: 400×390 px
- **Location**: (115, 54) - default screen position
- **Template**: WDT_RoundedNoTitle
- **Features**: Closebox ✅, Minimizebox ✅, Not Resizable

---

## Current Subwindows

### IW_CharacterView Subwindow
- **Location**: (2, 169) - left side, mid-height
- **Size**: 74×138 px
- **Template**: WDT_RoundedNoTitle
- **Purpose**: Container for class animation (character model display)
- **Tooltip**: "Drop Item Here to Auto Equip"
- **Note**: This is the ONLY existing subwindow - all other elements are flat in main window

---

## Current Element Organization

### Equipment Slots (InvSlots 1-21)

**Currently NO logical grouping** - traditional EQ slot order with scattered positions:

| Slot# | EQType | Equipment | Current Location (X,Y) | Size |
|-------|--------|-----------|------------------------|------|
| 1 | 1 | Left Ear | (44, -1) | 45×45 |
| 2 | 2 | Head | (178, -1) | 45×45 |
| 3 | 3 | Face | (133, -1) | 45×45 |
| 4 | 4 | Right Ear | (223, -1) | 45×45 |
| 5 | 5 | Neck | (89, -1) | 45×45 |
| 6 | 6 | Shoulders | (267, -1) | 45×45 |
| 7 | 7 | Arms | (267, 46) | 45×45 |
| 8 | 8 | Back (Cloak) | (223, 46) | 45×45 |
| 9 | 9 | Left Wrist | (5, 46) | 45×45 |
| 10 | 10 | Right Wrist | (50, 46) | 45×45 |
| 11 | 11 | Range | (138, 91) | 45×45 |
| 12 | 12 | Hands | (312, 46) | 45×45 |
| 13 | 13 | Primary Weapon | (5, 91) | 45×45 |
| 14 | 14 | Secondary Weapon | (50, 91) | 45×45 |
| 15 | 15 | Left Ring | (95, 91) | 45×45 |
| 16 | 16 | Right Ring | (183, 91) | 45×45 |
| 17 | 17 | Chest | (178, 46) | 45×45 |
| 18 | 18 | Legs | (267, 91) | 45×45 |
| 19 | 19 | Feet | (312, 91) | 45×45 |
| 20 | 20 | Waist | (133, 46) | 45×45 |
| 21 | 21 | Ammo | (228, 91) | 45×45 |

**Observation**: Equipment scattered horizontally with no anatomical organization

---

### Bag Slots (InvSlots 22-29)

**Current Layout**: 2×4 grid (2 columns, 4 rows)

| Slot# | EQType | Location (X,Y) | Row | Column |
|-------|--------|----------------|-----|--------|
| 22 | 22 | (179, 169) | 1 | 1 |
| 23 | 23 | (224, 169) | 1 | 2 |
| 24 | 24 | (179, 214) | 2 | 1 |
| 25 | 25 | (224, 214) | 2 | 2 |
| 26 | 26 | (179, 259) | 3 | 1 |
| 27 | 27 | (224, 259) | 3 | 2 |
| 28 | 28 | (179, 304) | 4 | 1 |
| 29 | 29 | (224, 304) | 4 | 2 |

**Spacing**: 45px vertical between rows, 45px horizontal between columns  
**Position**: Right side overlapping with stats area  
**Size**: Each slot 45×45 px

---

### Stats Display (Current - Right Side)

**XP Gauge**:
- Element: `IW_ExpGauge`
- Location: (279, 138)
- Size: 116×8 px
- EQType: 4 (Experience %)
- Colors: Orange fill (220,150,0), Blue lines (0,80,220)

**AA Gauge**:
- Element: `IW_AltAdvGauge`
- Location: (279, 153) - NOT YET DEFINED IN FILE (placeholder exists)
- EQType: 5 (AA Experience %)
- Status: **MISSING IMPLEMENTATION**

**Character Attributes** (STR-CHA):
- **Starting Location**: (280, 154) - RIGHT SIDE
- **Layout**: Single column, 15px vertical spacing
- **Label Color**: Blue (50, 160, 250)
- **Value Color**: White (255, 255, 255)

| Attribute | Label Location | Value Location | EQType |
|-----------|----------------|----------------|--------|
| STR | (280, 154) | (361, 154) | 5 |
| STA | (280, 169) | (361, 169) | 6 |
| AGI | (280, 184) | (361, 184) | 7 |
| DEX | (280, 199) | (361, 199) | 8 |
| WIS | (280, 214) | (361, 214) | 9 |
| INT | (280, 229) | (361, 229) | 10 |
| CHA | (280, 244) | (361, 244) | 11 |

**Combat Stats** (AC, ATK):
- **AC Label**: (280, 259), Value: (361, 259), EQType: 22
- **ATK Label**: (280, 274), Value: (361, 274), EQType: 23

**Resistances**:
- **Poison**: Label (280, 289), Value (361, 289), EQType: 12, Color: Teal (0,130,100)
- **Magic**: Label (280, 304), Value (361, 304), EQType: 16, Color: Purple (195,0,185)
- **Disease**: Label (280, 319), Value (361, 319), EQType: 13, Color: Yellow (205,205,0)
- **Fire**: Label (280, 334), Value (361, 334), EQType: 14, Color: Orange (255,165,0)
- **Cold**: Label (280, 349), Value (361, 349), EQType: 15, Color: Cyan (0,165,255)

**Weight**:
- Current Weight: (280, 367), EQType: 24
- Max Weight: (361, 367), EQType: 25

---

### Character Info (Current - Left Side)

**Name, Level, Class, Deity**:
- All currently positioned in LEFT section
- Specific coordinates TBD (need to grep for IW_Name, IW_Level, etc.)

**Class Animation**:
- Within `IW_CharacterView` subwindow at (2, 169)
- Element: `ClassAnim`

---

### Currency (Money) Buttons

**Layout**: Vertical stack in left-center area

| Element | Position | Size | Decal | Purpose |
|---------|----------|------|-------|---------|
| IW_Money0 (Platinum) | (93, 193) | 70×24 | PlatinumCoin (18×18) | Display PP |
| IW_Money1 (Gold) | (93, 219) | 70×24 | GoldCoin (18×18) | Display GP |
| IW_Money2 (Silver) | (93, 246) | 70×24 | SilverCoin (18×18) | Display SP |
| IW_Money3 (Copper) | (93, 273) | 70×24 | CopperCoin (18×18) | Display CP |

**Pattern**:
- All at X=93 (left-center alignment)
- Vertical spacing: 26-27px between buttons
- Right-aligned numeric text
- Coin icon on left side of each button

---

### Action Buttons

**Done Button**:
- `IW_DoneButton`
- Location: (299, 358)
- Size: 84×20 px
- Purpose: Close window

**Alt Adv Button**:
- `IW_AltAdvBtn`
- Location: (101, 358)
- Size: 84×20 px
- Purpose: Open AA window

**Face Button**:
- `IW_FacePick`
- Location: (2, 139)
- Size: 84×20 px
- Purpose: Character customization

---

## Key Problems with Current Layout

### 1. **No Anatomical Equipment Organization**
- Equipment slots scattered without logical body-part grouping
- Hard to visually scan for specific slot types
- No left/right symmetry for paired items

### 2. **Bag Slots Conflict with Stats**
- Bags at (179, 169) overlap conceptually with stats at (280+, 154+)
- Creates visual clutter in right section
- No clear separation between inventory and stats

### 3. **Missing AA Gauge Implementation**
- Placeholder exists but gauge not fully configured
- No visual alignment with XP gauge

### 4. **Flat Structure - No Zone Grouping**
- Only 1 subwindow (IW_CharacterView)
- All stats, gauges, info labels directly in main window
- Hard to move sections as cohesive units
- Variant creation would require editing 50+ individual positions

### 5. **Inefficient Space Usage**
- 400px width could accommodate better 3-zone layout
- Stats crammed on right without visual breathing room
- Equipment doesn't leverage horizontal space effectively

---

## Proposed Subwindow Architecture (Phase 3.9)

### LEFT ZONE - Character Identity
**Subwindow**: `<Screen item="IW_LeftZone">`
- Location: (5, 4)
- Size: ~85×340 px
- Contents:
  - Character Name (EQType 1)
  - Level (EQType 2)
  - Class (EQType 3)
  - Deity (EQType 4)
  - Class Animation (existing ClassAnim)
  - Weight (Current/Max, EQTypes 24/25)
  - Face Button
  - Done Button (relocate here)

### CENTER ZONE - Equipment Grid
**Subwindow**: `<Screen item="IW_EquipmentGrid">`
- Location: (95, 4)
- Size: ~215×340 px
- Contents:
  - All 21 equipment slots (InvSlots 1-21) in anatomical layout:
    - **Row 1 (Head)**: Left Ear, Neck, Face, Head, Right Ear
    - **Row 2 (Arms)**: Left Ring, Left Wrist, Arms, Hands, Right Wrist, Right Ring
    - **Row 3 (Torso)**: Shoulders, Chest, Back, Waist, Legs, Feet
    - **Row 4 (Weapons)**: Primary, Secondary, Range, Ammo
  - Currency buttons (Plat/Gold/Silver/Copper)

### RIGHT ZONE - Stats & Progression
**Subwindow 1**: `<Screen item="IW_StatsZone">`
- Location: (315, 4)
- Size: ~80×240 px
- Contents:
  - AC, ATK
  - HP (Current/Max)
  - Mana (Current/Max)
  - STR, STA, AGI, DEX, WIS, INT, CHA
  - Resistances (Poison, Magic, Disease, Fire, Cold)

**Subwindow 2**: `<Screen item="IW_ProgressionZone">`
- Location: (315, 250)
- Size: ~80×90 px
- Contents:
  - XP Gauge (EQType 4)
  - XP Percentage Label (EQType 26)
  - AA Gauge (EQType 5, Zeal)
  - AA Label (EQType 72/73, Zeal)

### BAG ZONE - Inventory Slots
**Decision Needed**: Bottom vs Right Side

**Option A - Bottom Row** (below equipment):
- Location: (95, 350)
- Layout: 8 bags × 1 row horizontal
- Requires window height increase to ~400px

**Option B - Right Side** (alongside stats):
- Location: (315, 4) - shares space with stats zone
- Layout: 2 bags × 4 rows vertical OR 4 bags × 2 rows
- Keeps current window height

**Option C - Split Layout**:
- Bags 1-4: Bottom of equipment zone (95, 350)
- Bags 5-8: Below progression zone (315, 350)
- Balanced distribution

---

## Implementation Questions to Resolve

### Question 1: Bag Slot Positioning
**Where should 8 bag slots go?**
- [ ] Bottom row (all 8 horizontal below equipment)
- [ ] Right side vertical (alongside stats)
- [ ] Split: 4 bottom + 4 right
- [ ] Other configuration?

### Question 2: AA Gauge Status
**Is AA gauge functional now or needs implementation?**
- Current file has `IW_AltAdvGauge` element but appears size 1×1 (hidden/disabled)
- Need to check if Zeal client supports EQType 5 or if we need EQTypes 71-73
- Should AA gauge match XP gauge styling (116×8 px)?

### Question 3: HP/Mana Display
**Use basic EQTypes or Zeal-enhanced values?**
- Basic: EQType 18 (Current HP), separate labels
- Zeal: EQType 70 (HP current/max combined format)
- Similar for Mana (EQType 21 basic vs EQType 80 Zeal)
- Decision impacts layout complexity

### Question 4: Window Dimensions
**Keep 400×390 or adjust?**
- Current: 400×390 px
- Proposed: 400×400 px (accommodate bottom bags)
- OR: 420×390 px (widen for better center zone)
- Must fit 800×600 minimum resolution (safe zone ~500px width max)

### Question 5: Currency Button Position
**Where do Platinum/Gold/Silver/Copper buttons go?**
- Current position unknown (need to grep)
- Options:
  - Bottom of equipment grid
  - Bottom of left zone
  - Dedicated mini-zone
  - Below bag slots

---

## Next Steps

1. **Grep for missing coordinates**: IW_Name, IW_Money0-3, current button positions
2. **Decide bag slot configuration** (bottom vs side vs split)
3. **Confirm AA gauge implementation status** (functional or placeholder?)
4. **Calculate exact coordinates** for 3-zone layout with chosen bag position
5. **Create subwindow structure** in XML
6. **Update PHASE-3.9-INVENTORY-REDESIGN.md** with finalized decisions

---

**Analysis Complete** - Ready for implementation planning discussion.
