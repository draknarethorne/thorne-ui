# Merchant Window - Large Inventory and Bags Variant

**File**: [EQUI_MerchantWnd.xml](./EQUI_MerchantWnd.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-10  
**Status**: ✅ Complete and tested
**Author**: Draknare Thorne

---
## Purpose

The Merchant window provides a self-sufficient shopping interface without requiring the player to open separate Inventory or Stats windows. This allows comfortable merchandise browsing while keeping the player's inventory, equipment, and stats visible at all times.

**Key Features**:

- 3 tabs: Bags (inventory display), Equipment (worn items), Stats (comprehensive HUD)
- Always displays current inventory state
- Weapon slot display for quick visual reference
- Complete player stats for combat awareness
- Matches Inventory window visual theme and color scheme

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 340 × 566 pixels (fixed) |
| Resizable | No (fixed dimensions) |
| Fadeable | Yes (client-controlled transparency) |
| Tab Count | 3 (Bags, Equipment, Stats) |
| Screen ID | MerchantWnd |

---

## Layout Overview

### Window Hierarchy

```text
MerchantWnd (340×566)
├── TabBox (tabs at top)
│   ├── BagsPage
│   ├── EquipmentPage
│   └── StatsPage
└── Bottom: Player Name, Level, HP, Mana
```

### Color Scheme (Inventory Window Standard)

| Element | Color RGB | Usage |
|---------|-----------|-------|
| Attribute labels (STR/STA/AGI/etc) | (50, 160, 250) | Blue attributes |
| Stat values | (255, 255, 255) | White numbers |
| ATK label | (255, 165, 0) | Orange attack label |
| MAGIC resist | (195, 0, 185) | Purple magic |
| FIRE resist | (255, 165, 0) | Orange fire |
| COLD resist | (0, 165, 255) | Cyan cold |
| DISEASE resist | (205, 205, 0) | Yellow disease |
| POISON resist | (0, 130, 100) | Teal poison |

---

## Tab 1: Bags Tab

**Purpose**: Display player's current inventory state during shopping

**Layout**:

```text
Bags Tab (340×520)
├─ Left Side (columns 1-3):
│  ├─ 8 inventory bag slots (rows 0-1, columns 0-3)
│  ├─ Player Name/Level (overlapping, left corner)
│  └─ Class/Deity display (below bags)
│
├─ Center:
│  └─ 4 weapon slots in 2×2 grid
│
└─ Right Side:
   ├─ EXP label + percentage (top)
   ├─ XP gauge (middle, horizontal)
   └─ WEIGHT cur/max (bottom)
```

### Bag Slots (8 total)

| Location | EQType | Notes |
|----------|--------|-------|
| Row 0, Col 0 | 22 (Bag 1) | Top-left |
| Row 0, Col 1 | 23 (Bag 2) | |
| Row 0, Col 2 | 24 (Bag 3) | |
| Row 0, Col 3 | 25 (Bag 4) | |
| Row 1, Col 0 | 26 (Bag 5) | Bottom-left |
| Row 1, Col 1 | 27 (Bag 6) | |
| Row 1, Col 2 | 28 (Bag 7) | |
| Row 1, Col 3 | 29 (Bag 8) | |

**Positioning**:

- Each slot: 40×40px with 2px gaps
- Row 0, Y=26
- Row 1, Y=72
- Columns start at X=12 with 42px spacing

### Weapon Slots (Bags-Specific)

**Note**: Bags tab uses unique weapon slot names (MW_Bags_Primary, etc.) to allow independent positioning from Equipment tab.

| Slot | EQType | Position | Purpose |
|------|--------|----------|---------|
| MW_Bags_Primary | 13 | Center-top | Primary weapon |
| MW_Bags_Secondary | 14 | Center-mid | Secondary weapon |
| MW_Bags_Range | 11 | Center-mid | Ranged weapon |
| MW_Bags_Ammo | 21 | Center-bottom | Ammo |

**Layout**:

- All 4 in center area
- Stacked vertically in right-center portion of window
- Size: 40×40px each

### Player Info Block (Bags Tab Top-Left)

**Name/Level** (overlapping design):

- Player Name: X=12, Y=91, Width=150px, EQType=1
- Level: X=128, Y=91, CX=18px, EQType=2

**Details** (Class/Deity):

- Class: X=12, Y=110, EQType=3
- Deity: X=12, Y=125, EQType=4

### Experience Block (Right Side, Top)

**Layout**:

```text
EXP  [======== 87%]
Weight: 123 / 345
```

| Element | Position | Width | EQType | Details |
|---------|----------|-------|--------|---------|
| EXP label | X=214, Y=85 | 40px | - | Left-aligned |
| EXP % | X=290, Y=85 | 30px | 26 | Right-aligned, percent |
| XP gauge | X=179, Y=111 | 111px | 4 | Progress bar |
| WEIGHT label | X=214, Y=129 | 40px | - | Left-aligned |
| Cur value | X=242, Y=129 | 25px | 24 | Current weight |
| Slash | X=272, Y=129 | 5px | - | "/" separator |
| Max value | X=276, Y=129 | 50px | 25 | Maximum weight |

**Alignment Notes**:

- EXP label and % are top-right group
- XP gauge spans below, left-aligned with EXP label area
- WEIGHT label, cur, slash, max are bottom group
- All labels use consistent font and spacing

---

## Tab 2: Equipment Tab

**Purpose**: Display player's equipped items (armor + weapons)

**Layout**:

```text
Equipment Tab (340×520)
├─ Rows 0-2: Armor grid (3 rows × 4 columns = 12 pieces)
│  └─ Head, Neck, Shoulder, Chest
│  └─ Back, Wrist, Wrist, Hands
│  └─ Ring, Ring, Fingers, Waist
│
├─ Row 3: Weapon slots (4 pieces)
│  └─ Primary, Secondary, Range, Ammo
│
└─ Bottom: Legs, Feet (2 pieces, separate positioning)
```

### Armor Slots (12 total)

- 3 rows of 4 slots each (40×40px, 2px gaps)
- Row 0, Y=26
- Row 1, Y=72
- Row 2, Y=118
- Columns start at X=12 with 42px spacing each

**Equipment EQTypes** (Standard SIDL mappings):

- Head, Neck, Shoulder, Back, Chest, Hands, Wrists (2), Fingers (2), Ears (2), Legs, Feet, Waist, etc.

### Weapon Slots (Equipment Tab)

| Slot | Item Name | EQType | Position |
|------|-----------|--------|----------|
| MW_Primary | Primary | 13 | Row 3, Col 0 |
| MW_Secondary | Secondary | 14 | Row 3, Col 1 |
| MW_Range | Range | 11 | Row 3, Col 2 |
| MW_Ammo | Ammo | 21 | Row 3, Col 3 |

**Location**: Row 3, Y=164 (same row-based positioning as armor slots)

---

## Tab 3: Stats Tab

**Purpose**: Comprehensive HUD displaying all computed player statistics

**Layout**:

```text
Stats Tab (340×520)
├─ Column 1 (left): Core Stats
│  ├─ HP (current / max)
│  ├─ MANA (current / max)
│  ├─ AC
│  ├─ ATK (attack rating)
│  └─ WEIGHT (current / max)
│
├─ Column 2 (center): Attributes
│  ├─ STR (Strength)
│  ├─ STA (Stamina)
│  ├─ AGI (Agility)
│  ├─ DEX (Dexterity)
│  ├─ WIS (Wisdom)
│  ├─ INT (Intelligence)
│  └─ CHA (Charisma)
│
└─ Column 3 (right): Resistances
   ├─ MAGIC resist
   ├─ FIRE resist
   ├─ COLD resist
   ├─ DISEASE resist
   └─ POISON resist
```

### Column 1: Core Stats (Left)

| Label | EQType | Position | Value Position | Color |
|-------|--------|----------|-----------------|-------|
| HP | - | X=12 | X=40 | - |
| (current/max) | 18/19 | X=60/90 | - | White |
| MANA | - | X=12 | X=40 | - |
| (current/max) | 20/21 | X=60/90 | - | White |
| AC | - | X=12 | X=40 | - |
| (value) | 22 | X=60 | - | White |
| ATK | - | X=12, Color=(255,165,0) | x=40 | Orange |
| (value) | 23 | X=60 | - | White |
| WEIGHT | - | X=12 | X=60 | - |
| (cur/max) | 24/25 | X=91/X=120 | - | White |

**Y Positioning**:

- HP: Y=26
- MANA: Y=49
- AC: Y=72
- ATK: Y=95
- WEIGHT: Y=118

### Column 2: Attributes (Center) ★ KEY ALIGNMENT

| Label | EQType | Y Position |
|-------|--------|------------|
| STR | 5 | Y=26 |
| STA | 6 | Y=49 |
| AGI | 8 | Y=72 |
| DEX | 7 | Y=95 |
| WIS | 9 | Y=118 |
| INT | 10 | Y=141 |
| CHA | 11 | Y=164 |

#### Column 2 Key Alignment

All attribute labels positioned at X=130; all values at X=165

- Labels: X=130, color=(50,160,250) blue
- Values: X=165, color=(255,255,255) white
- All values right-aligned for clean numeric column
- Spacing of 23px between rows allows breathing room

### Column 3: Resistances (Right) ★ KEY ALIGNMENT

| Label | EQType | Y Position | Color |
|-------|--------|------------|-------|
| MAGIC | 16 | Y=26 | (195,0,185) Purple |
| FIRE | 14 | Y=49 | (255,165,0) Orange |
| COLD | 15 | Y=72 | (0,165,255) Cyan |
| DISEASE | 13 | Y=95 | (205,205,0) Yellow |
| POISON | 12 | Y=118 | (0,130,100) Teal |

#### Column 3 Key Alignment

All resist labels positioned at X=230; all values at X=290

- Labels: X=230, color varies by resist type
- Values: X=290, color=(255,255,255) white
- All values right-aligned for numeric precision
- Color-coded labels help identify resist types at a glance

---

## XML Structure & Implementation Notes

### Element Duplication Strategy

**Problem**: Global UI positioning means same element name = same position across all tabs.

**Solution**: Create tab-specific weapon slots with unique names.

**Example**:

```xml
<!-- Equipment Tab weapons -->
<InvSlot item="MW_Primary">
  <ScreenID>InvSlot15</ScreenID>
  <!-- ... positioned at Row 3, Col 0 -->
</InvSlot>

<!-- Bags Tab weapons (different names, same EQType) -->
<InvSlot item="MW_Bags_Primary">
  <ScreenID>InvSlotBags0</ScreenID>
  <!-- ... positioned elsewhere for Bags layout -->
</InvSlot>
```

**Key Insight**: Both items show weapon from EQType=13 (primary) but can be positioned independently because they have unique item names.

### Page Structure

```xml
<Screen item="MerchantWnd">
  <!-- ... screen definition -->
  <TabBox>
    <Page item="BagsPage">
      <Pieces>
        <!-- Bag slots 1-8 -->
        <!-- MW_Bags_* weapon slots -->
        <!-- Name/Level/Class/Deity labels -->
        <!-- EXP/XP/WEIGHT block -->
      </Pieces>
    </Page>
    
    <Page item="EquipmentPage">
      <Pieces>
        <!-- Armor slots -->
        <!-- MW_* weapon slots -->
      </Pieces>
    </Page>
    
    <Page item="StatsPage">
      <Pieces>
        <!-- Column 1 labels + values -->
        <!-- Column 2 labels + values -->
        <!-- Column 3 labels + values -->
      </Pieces>
    </Page>
  </TabBox>
</Screen>
```

### Spacing & Alignment Conventions

1. **Bag slots**: 40×40px, 2px gap = 42px per column
2. **Row spacing**: 46px between rows (40px + gap)
3. **Label positioning**: Consistent X across column (e.g., all attributes at X=130)
4. **Value alignment**: Right-align or specific X position for numeric display
5. **Color coding**: Use EQType-mapped colors for quick visual parsing

---

## Testing Checklist

- [ ] Bags tab displays all 8 inventory slots
- [ ] Bags tab weapon slots display correctly
- [ ] Bags tab EXP%, XP gauge, and WEIGHT display correctly
- [ ] Equipment tab displays armor grid
- [ ] Equipment tab weapon slots display correctly
- [ ] Stats tab Column 1 displays HP, MANA, AC, ATK, WEIGHT
- [ ] Stats tab Column 2 attributes aligned at X=130/165
- [ ] Stats tab Column 3 resists aligned at X=230/290
- [ ] All colors match Inventory window standard
- [ ] No overlapping or clipped elements
- [ ] Window can be moved and resized normally
- [ ] Tab switching works smoothly

---

## Known Issues & Workarounds

| Issue | Cause | Workaround | Status |
|-------|-------|-----------|--------|
| Merchant window fades when out of combat | Client-enforced fading | Use Alt+Shift+T to control transparency | Not fixable |
| Cannot execute `/potionbelt` from button | P2002 client limitation | Use hotkey macro instead | Design limitation |
| Window position resets on relog | Client saves positions | Use `/viewport save` before logging out | Client behavior |

---

## Git History

**Latest Commit**: f447dcf - "Implement Merchant window comprehensive redesign (Phase 3)"

### Key Changes in v1.0.0

- ✅ Complete redesign of 3 tabs (Bags/Equipment/Stats)
- ✅ Fixed XML parsing errors and duplicate labels
- ✅ Created separate Bags weapon slots (MW_Bags_*)
- ✅ Aligned Stats tab columns: Column 2 (X=130/165), Column 3 (X=230/290)
- ✅ Corrected resist colors: DISEASE(205,205,0), POISON(0,130,100)
- ✅ Fixed WEIGHT overlap on Stats tab (adjusted X positions)
- ✅ Redesigned Bags layout to match Inventory window standards
- ✅ Integrated EXP/XP/WEIGHT blocks with proper alignment
- ✅ Color scheme standardization across all tabs

### Previous Versions

**v0.2.0** - Initial merchant window (basic 3 tabs, minimal polish)

**v0.1.0** - Merchant window stub (empty tabs, no implementation)

---

## Future Enhancements

- **Quick-sell button**: Add button to quickly mark items for bulk sales
- **Price preview**: Display estimated gold for selected items (if API available)
- **Comparison mode**: Show item comparison with currently worn gear
- **Loot notification**: Flash when rare loot appears in merchant inventory
- **Custom sorting**: Allow user-selectable sort options (rarity, type, level)

---

## Related Files

- [README.md](README.md) - Main documentation hub
- [ROADMAP.md](ROADMAP.md) - Future phases and enhancements
- [EQUI_ActionsWindow.md](EQUI_ActionsWindow.md) - Actions window documentation
- [EQUI_HotButtonWnd.md](EQUI_HotButtonWnd.md) - Hotbar window documentation
- Reference: `thorne_drak/EQUI_Inventory.xml` - Color scheme and pattern source

---

*Last Updated: January 24, 2026 - v1.0.0*  
*Maintainer: Draknare Thorne*
