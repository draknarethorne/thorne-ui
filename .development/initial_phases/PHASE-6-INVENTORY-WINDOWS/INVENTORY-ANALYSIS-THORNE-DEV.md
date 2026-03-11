# Thorne-Dev Inventory Layout Analysis

**Source**: `.archive/thorne_dev/EQUI_Inventory.xml`  
**Context**: Legacy UI from advanced EQ emulator with expanded game systems (now shutdown)  
**Purpose**: Identify layout patterns and features that resonated with user's playstyle

---

## Overview

The archived thorne_dev inventory represents a significantly more feature-rich EQ experience than TAKP. It includes:
- **22 equipment slots + charm** (21 standard + power source not in TAKP)
- **10 root inventory slots** (bag system)
- **Extensive stats panel** (50+ display metrics)
- **Multiple game systems**: Stats, Evolution, Shrouds, Alt. Currency
- **42×42px slot size** (larger/more readable than standard)
- **Asymmetrical equipment layout** (optimized for fast lookup, not pure anatomy)

---

## Equipment Slot Layout (thorne_dev)

### Visual Layout Diagram

```
┌─────────────────────────────────────────────────────┐
│ EQUIPMENT SECTION (Asymmetrical Optimization)       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ DH: CHARM (Y=228,X=210)          [Separators]       │
│                                                     │
│ Y=12:   L Ear (123)   Head (166)   Face (210)  R Ear (253)
│                    ^^ Row 1: Face/Head area          │
│                                                     │
│ Y=55-98:  Chest (123) ─┐                            │
│          About Body (253)                         │
│          Neck (253)    ├─ Torso armor cluster      │
│          Arms (123)    │                            │
│          Shoulders (253)─┐                          │
│                                                     │
│ Y=142:   Waist (123) ├─ Limb/joint cluster         │
│                                                     │
│ Y=185:   L Wrist (123)    ┐                         │
│          R Wrist (253)    ├─ Arm protection        │
│                                                     │
│ Y=228:   Legs (123)  Hands (166)   Feet (253)       │
│          ^^ Row 4: Lower body assembly              │
│                                                     │
│ Y=272:   L Ring (166)  RECLAIM (X=300)  R Ring (210)
│          Power Src (253)                            │
│          ^^ Special items and buttons               │
│                                                     │
│ Y=316:   Primary (123) Secondary (166) Range (210) Ammo (253)
│          ^^ Weapons row                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Equipment Slot Mapping (thorne_dev)

| InvSlot | Item | X  | Y | Notes |
|---------|------|----|----|-------|
| 0 | Charm | 210 | 228 | Special containment slot |
| 1 | L Ear | 123 | 12 | ↓ Head zone |
| 2 | Head | 166 | 12 | |
| 3 | Face | 210 | 12 | |
| 4 | R Ear | 253 | 12 | |
| 5 | Neck | 253 | 55 | ↓ Torso cluster |
| 6 | Shoulders | 253 | 141 | |
| 7 | Arms | 123 | 99 | |
| 8 | About Body (Chest) | 253 | 98 | |
| 9 | L Wrist | 123 | 185 | ↓ Arm/joint zone |
| 10 | R Wrist | 253 | 185 | |
| 11 | Range | 210 | 316 | ↓ Weapons section |
| 12 | Hands | 166 | 228 | Hand protection |
| 13 | Primary | 123 | 316 | Weapon |
| 14 | Secondary | 166 | 316 | Off-hand |
| 15 | L Ring (L Finger) | 166 | 272 | Ring 1 |
| 16 | R Ring (R Finger) | 210 | 272 | Ring 2 |
| 17 | Chest | 123 | 55 | Chest plate |
| 18 | Legs | 123 | 228 | Lower body |
| 19 | Feet | 253 | 228 | Feet protection |
| 20 | Waist | 123 | 142 | Belt/waist |
| 21 | Power Source | 253 | 272 | **Special: No TAKP equiv** |
| 22 | Ammo | 253 | 316 | Projectiles |
| 23-32 | Root Inventory (B1-B10) | — | — | 10 bag slots |

---

## Layout Philosophy

### **Key Design Principle: Functional Clustering**

Rather than pure anatomical ordering, thorne_dev groups equipment by **lookup speed**:

1. **Head Zone** (Y=12): All head/face items in one horizontal row
   - User can scan left-to-right for ear/face/head protection
   - Very efficient for equipping raid loot

2. **Torso Cluster** (Y=55-142): Core armor scattered but proximally grouped
   - Chest, About Body, Neck, Arms, Shoulders, Waist all within ~87px height
   - Reflects where user's eyes gravitate for armor upgrades

3. **Special Items** (Y=228-272): Hands, Legs, Feet, Rings, Power Source all visible
   - Not purely anatomical; functional separation
   - Charm and Power Source (expansion items) isolated together

4. **Weapons Section** (Y=316): All 4 weapon slots in single row
   - Complete visibility of combat readiness
   - Primary, Secondary, Range, Ammo all at same Y level

### **Why User Preferred This Layout**

- **Fast target acquisition**: Items grouped by equip frequency
- **Reduces scrolling**: Most-used items clustered together
- **Expansion-aware**: Power Source slot for higher-level content
- **Clear visual hierarchy**: Armor → Accessories → Weapons
- **42×42 slots**: Much more icon visibility than tiny 40×40

---

## Slot Size Comparison

| Metric | thorne_dev | Current TAKP |
|--------|-----------|-------------|
| **Slot Size** | 42×42px | 40×40px |
| **Icon Clarity** | Good | Tiny |
| **Grid Pattern** | Asymmetrical | Rectangular (proposed) |
| **Equipment Slots** | 23 (0-22) | 21 (1-21) |
| **Special Slots** | Power Source (21) | None |
| **Bag Slots** | 10 root (23-32) | 8 (22-29) |
| **Total Inventory** | 33 slots | 29 slots |

---

## Game Systems in thorne_dev

### **Available in thorne_dev (Expansion Features)**

This inventory was designed for a more advanced emulator supporting:

#### 1. **Evolution System**
- Separate tab with item collection UI
- Displays: Item Name, Level, Progress %, Active toggle
- "Activate All" / "Deactivate All" buttons for batch control
- Indicates game level > ~60+ content

#### 2. **Shrouds System** 
- "Shrouds" tab with Progression tracking
- Lists unlocked progressions and "Next Class" options
- Indicates endgame/alternate advancement system

#### 3. **Alternative Currency**
- Loyalty Tokens tracking
- Loyalty Velocity gauge (0-100% scale)
- "Alt. Currency" tab with Create/Reclaim buttons
- Indicates modern server monetization

#### 4. **Power Source Slot (InvSlot21)**
- Equipment slot for "Power Source" items
- **NOT AVAILABLE IN TAKP**
- Suggests high-end raid/group content extensions

### **Not Available in TAKP**
Power Source items, Evolution system, Shrouds, Loyalty Tokens

---

## Character Information Display

thorne_dev displays character metadata:

```xml
<!-- Title, Name, Last Name (Y=365-393) -->
<Label item="IW_CharTitle">      <!-- Title (if player has one) -->
<Label item="IW_Name">            <!-- Main character name -->
<Label item="IW_LastName">        <!-- Guild/family name (if applicable) -->

<!-- Level and Class (Y=2) -->
<Label item="IW_Level">           <!-- Numeric level -->
<Label item="IW_LevelLabel">      <!-- "Level: " prefix -->
```

These provide quick character context without opening other windows.

---

## Stats Panel (Advanced)

### **Scope: 50+ Metrics**

thorne_dev's Stats tab displays far more information than TAKP. Organized sections:

#### **Combat Metrics**
- HP, Mana, Endurance (primary)
- Armor Class, Avoidance Class
- Combat HP/Mana/Endurance Regen
- Attack, Haste

#### **Attributes**
- Strength, Stamina, Intelligence, Wisdom, Agility, Dexterity, Charisma
- 7 core stats vs TAKP's typical 6-display

#### **Resistances** (4+)
- Magic, Fire, Cold, Disease, Poison

#### **Combat Modifiers**
- Heal Amount, Spell Damage
- Worn ATK, Combat Effects
- Spell Shield, Shielding, Damage Shield
- DoT Mitigation, Avoidance, Accuracy
- Stun Resist, Strike Through

#### **Critical Rates** (multiple)
- Spell Crit Rate/Ratio
- DoT Crit Rate/Ratio  
- Heal Crit Rate, Melee Crit Rate, Archery Crit Rate

> **Total Coverage**: Player can assess complete class/build viability without external tools

---

## Window Structure

### **Overall Dimensions**
- Width: 426px
- Height: 500px
- DrawTemplate: Filigree (ornate default)
- Resizable: No (fixed size)
- Title bar: Yes ("Inventory")

### **Subwindow Tabs**
1. **Inventory** (IW_InvPage)
   - Equipment grid (slots 0-22)
   - Character portrait/animation area (implied)
   - Character info (Title/Name/Level)

2. **Stats** (IW_StatPage)
   - TileLayoutBox auto-layout (vertical stacking)
   - 40+ stat screens w/ labels
   - Scrollable for high-resolution displays

3. **Alt. Currency** (IW_AltCurrPage)
   - Loyalty Tokens counter
   - Loyalty Velocity gauge
   - Currency item list (scrollable)
   - Create/Reclaim buttons

4. **Evolution** (IW_EIPage) *(May not exist in TAKP)*
   - Item list: Name, Level, Progress %, Active
   - Toggle Selected, Activate All, Deactivate All buttons
   - Indicates game evolution/progression tracking

5. **Shrouds** (IW_AltCharProgPage) *(May not exist in TAKP)*
   - Progression list: Name, Unlocked, Next Class
   - Information panel with details
   - Indicates alternate advancement system

---

## Visual Separators

thorne_dev uses `StaticAnimation` divider bars to visually segment equipment sections:

```
Separator 0: Y=60   (between head and chest)
Separator 1: Y=106  (between chest and arms)
Separator 2: Y=195  (between arms and rings)
Separator 3: Y=239  (between rings and weapons)
Separator 4: Y=332  (between weapons and ??)
Separator 5: Y=400  (very bottom)
```

**Purpose**: Visual clarity when scanning for specific armor pieces

---

## Key Differences from Current TAKP Design

| Aspect | thorne_dev | TAKP (Current) |
|--------|-----------|--------------|
| **Equipment Layout** | Asymmetrical (optimized) | 5-col grid (proposed 4-col) |
| **Slot Size** | 42×42px | 40×40px (proposed 45×45px) |
| **Power Source** | Yes (InvSlot21) | No |
| **Bag Slots** | 10 (InvSlot 23-32) | 8 (proposed) |
| **Character Display** | Title/Name/Level shown | (TBD in redesign) |
| **Stats Tab** | 50+ metrics, auto-layout | ~30 metrics (focused) |
| **Game Systems** | Evolution, Shrouds, Alt Currency | None (TAKP Classic) |
| **Separators** | 6 visual dividers | None (proposed) |
| **Window Size** | 426×500px | 420×470px |

---

## What Made This Layout Work

1. **Fast Equipping**: Items clustered by replacement frequency (head gear together, armor cluster together)
2. **Expansion Ready**: Power Source slot prepared for higher-content raids
3. **Visual Breathing Room**: 42×42px icons are readable at a glance
4. **Tab Organization**: Stats/Evolution/Currency don't clutter main inventory
5. **Character Context**: Quick level/name check without opening character sheet
6. **Visual Guides**: Separator bars prevent scanning errors

---

## User's Take

> "I like this view of the inventory for how I was playing at the time."

**Implication**: The asymmetrical layout *matched user's muscle memory* from active gameplay on that server. Rather than pure anatomy or grid perfection, the layout evolved with how players actually equipped characters during raids and group content.

---

## Considerations for TAKP Redesign

### **Adoptable Features**
✅ **42×42px slots** (proposal: 45×45px) - Better readability  
✅ **Visual separator bars** - Reduce scanning errors  
✅ **Head zone isolation** - Face/Head/Ears on single row  
✅ **Weapons section grouping** - All weapons in one row visibility  
✅ **Character metadata display** - Quick level/name check  

### **Not Adoptable (TAKP Doesn't Support)**
❌ Power Source slot (expansion item)  
❌ Evolution/Shrouds tabs (not in TAKP game systems)  
❌ Alt. Currency tracking (not in TAKP)  
❌ Loyalty Tokens/Velocity (post-2010s feature)  

### **Hybrid Approach**
Could combine:
- **thorne_dev's functional clustering** (asymmetrical efficiency)
- **Anatomical ordering** (user's preferred Row 2: Neck/Chest/Back/Shoulders)
- **TAKP's slot realities** (20 equipment slots, 8 bags)
- **Modern readability** (45×45px, separators)

---

## Next Steps for Consideration

1. **Quick Win**: Increase slot size to 42-45px (better readability)
2. **Visual Clarity**: Add separator bars between armor/limb/weapon sections
3. **Layout Decision**: 
   - Option A: Keep anatomical 4-column grid (current proposal)
   - Option B: Adopt thorne_dev's asymmetrical efficiency
   - Option C: Hybrid (anatomical ROW 2 + optimized placement elsewhere)
4. **Character Context**: Add Title/Name/Level display like thorne_dev (if desired)
5. **Testing**: Load 45×45px layout in-game to verify visual spacing

---

## Summary

The thorne_dev inventory represents a **mature, raid-tested UI** for a more feature-rich EQ expansion. While TAKP can't replicate all systems (Evolution, Shrouds, Alt Currency), it can borrow **design patterns** that made equipping fast and error-free:

- **Functional clustered layout** over pure anatomical symmetry
- **Larger, readable icons** (42-45px vs 40px)
- **Visual separation** between armor classes
- **Quick character context** (level, name visible)

These changes would modernize TAKP's inventory without losing classic gameplay feel.

