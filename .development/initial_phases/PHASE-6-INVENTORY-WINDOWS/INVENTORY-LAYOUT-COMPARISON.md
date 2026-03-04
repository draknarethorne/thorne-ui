# Inventory Layout Comparison: thorne_dev vs Current TAKP Plan

**Purpose**: Understand what fields/sections thorne_dev included vs what we're planning for TAKP

---

## Window Overview

### **thorne_dev (Archive Legacy)**
```
Window Size:  426×500px
Layout Type:  Tabbed interface (5 tabs)
Main Tab:     Inventory (IW_InvPage)
Other Tabs:   Stats, Evolution, Shrouds, Alt. Currency
Resizable:    No (fixed size)
Border:       Filigree template (ornate)
```

### **TAKP Current Plan**
```
Window Size:  420×470px
Layout Type:  Single unified view (NO tabs)
Structure:    9 zone containers (modular grid)
Resizable:    No (fixed size)
Border:       Standard template (TBD)
```

---

## Main Inventory Tab Structure (thorne_dev)

The **Inventory page (IW_InvPage)** in thorne_dev contains ALL of this content in one panel:

### **SECTION 1: Equipment Grid** (Top-Left, Y=12-316)
- **23 equipment slots** (InvSlot0-22)
- **Asymmetrical layout** (optimized for speed)
- **42×42px slot size** (large, readable)
- 6 visual separator bars (dividers)
- Charm slot (special containment)
- Power Source slot (endgame item)

### **SECTION 2: Character Information** (Top-Right, Y=0-30)
```
Level: 60               ← Player level (EQType 2)
SHD 60 Shadow Knight    ← Class abbreviation + class name (EQType 3,6)
Deity: Mithaniel Marr   ← Character deity (EQType 4)
```
**Space**: ~120×30px right column area

### **SECTION 3: Combat Vitals** (Left sidebar, Y=64-180)
```
HP:   1234 / 1500       ← Current/Max Hit Points  (EQType 17,18)
MP:   450  / 500        ← Current/Max Mana        (EQType 124,125)
EN:   100% / 100%       ← Current/Max Endurance   (EQType 126,127)
AC:   -45               ← Armor Class             (EQType 22)
MIT:  123               ← Mitigation              (EQType 6668)
AVD:  456               ← Avoidance               (EQType 6667)
ATK:  +189              ← Attack Power            (EQType 23)
DMG:  +234              ← Spell Damage            (EQType 226)
HEAL: +567              ← Healing Boost           (EQType 225)
```
**Space**: ~120×120px left sidebar
**Notes**: 
- Each stat is label + number format
- Includes separator dividers (/)
- Left-aligned column

### **SECTION 4: Progression Gauge** (Center, Y=200-230)
```
EXP / AAEXP Label       ← Section header
[====████░░░░░] 45%     ← Experience gauge (dual-color fill)
```
**Space**: ~120×30px
**Colors**: Orange fill for XP, Blue lines for AA progress
**EQType**: 4 (XP gauge)

### **SECTION 5: Core Attributes** (Bottom-Left, Y=242-335)
```
STR  123 / 255 +45      ← Strength with Heroic (EQType 5,264,251)
STA  100 / 255 +0       ← Stamina with Heroic  (EQType 6,265,252)
AGI  189 / 255 +12      ← Agility with Heroic  (EQType 8,267,254)
DEX  156 / 255 +23      ← Dexterity with Heroic (EQType 7,266,253)
WIS  167 / 255 +34      ← Wisdom with Heroic   (EQType 9,268,255)
INT  145 / 255 +5       ← Intelligence with Heroic (EQType 10,269,256)
CHA  128 / 255 +18      ← Charisma with Heroic (EQType 11,270,257)
```
**Space**: ~120×95px bottom-left area
**Format**: Attribute / Max / +Heroic bonus
**Colors**: Yellow/gold at 214,178,40 for heroic values
**Notes**: 7 attributes (not 6) - includes all base stats

---

## Comparison Table: What Each Layout Includes

| Component | thorne_dev | TAKP Current Plan |
|-----------|-----------|------------------|
| **Equipment Slots** | 23 (0-22) | 21 (1-21) |
| **Bag Slots** | 10 root (23-32) | 8 (22-29) |
| **Charm Slot** | Yes (InvSlot0) | No |
| **Power Source** | Yes (InvSlot21) | No |
| **Equipment Layout** | Asymmetrical | 4-column grid (proposed) |
| **Slot Size** | 42×42px | 40×40 (or 45×45px proposed) |
| **Character Name** | Shown (title/name/surname) | Hidden or TBD |
| **Character Class** | Shown (class + abbr) | Hidden or TBD |
| **Character Deity** | Shown | Hidden or TBD |
| **Level Display** | Shown "Level: 60 SK" | Hidden or TBD |
| **HP/MP/Endurance** | Shown with current/max | Hidden or TBD |
| **AC/MIT/AVD** | Shown (3 armor stats) | Hidden or TBD |
| **Attack/Damage** | Shown (ATK + DMG) | Hidden or TBD |
| **Heal Bonus** | Shown | Hidden or TBD |
| **7 Attributes** | Shown with current/max/heroic | Hidden or TBD |
| **XP/AA Gauge** | Single gauge (dual-colored) | Dual gauges (expanded 95px zone) |
| **Heroic Values** | Shown ("+ bonus") | Hidden or TBD |
| **Visual Separators** | 6 divider bars | None (proposed) |
| **Total Data Points** | ~50+ metrics | ~10-15 metrics |
| **Tab System** | 5 tabs (Inv, Stats, Evo, Shrouds, Alt Curr) | None (single view) |

---

## Space Allocation Comparison

### **thorne_dev Window (426×500px)**

```
┌─────────────────────────────────────────────┐  Y=0
│  LEFT COLUMN              │  RIGHT COLUMN   │
│  (Equipment + Stats)      │  (Character)    │
│  ~310px wide              │  ~120px wide    │
├─────────────────────────────────────────────┤  Y=12
│  Equipment Layout (23 slots)                │
│  Asymmetrical positioning                   │
│  X coords: 123, 166, 210, 253              │
│  Y coords: 12-316px range                   │
│  6 divider bars for section clarity         │
│                        │ Level: 60 SK      │
│                        │ Class: Shadow K.  │
│                        │ Deity: Foo Bar    │
├─────────────────────────────────────────────┤  Y=64
│  HP/MP/EN/AC/MIT/AVD/ATK/DMG stats         │
│  (9 combat lines, ~120px tall)             │
│                                            │
├─────────────────────────────────────────────┤  Y=200
│  EXP Gauge (dual-color)                    │
├─────────────────────────────────────────────┤  Y=242
│  Attributes (STR/STA/AGI/DEX/WIS/INT/CHA) │
│  Format: label current/max +heroic        │
│  (~95px tall for all 7)                    │
├─────────────────────────────────────────────┤  Y=365
│  Character name/title text                 │
├─────────────────────────────────────────────┤  Y=400+
│  (Page ends, next tab starts)               │
└─────────────────────────────────────────────┘  Y=500
```

### **TAKP Current Plan (420×470px)**

```
┌─────────────────────────────────────────────┐  Y=0
│  Unified Zone Architecture                  │
├─────────────────────────────────────────────┤  Y=4
│  IW_PlayerInfo_Wnd (100×60)                │
│  - Name, Level, Class, Deity               │
├─────────────────────────────────────────────┤  Y=68
│  IW_Progression_Wnd (100×95)               │
│  - XP gauge, AA gauge (expanded)           │
├─────────────────────────────────────────────┤  Y=167
│  IW_ClassAnim_Wnd (100×160)                │
│  - Character portrait/animation            │
├─────────────────────────────────────────────┤  Y=4
│  IW_EquipmentGrid_Wnd (215×200)            │
│  - 4-column equipment layout (proposed)    │
│  - 45×45px slots, 20 items                 │
├─────────────────────────────────────────────┤  Y=208
│  IW_Currency_Wnd (215×90)                  │
│  - Platinum/Gold/Silver/Copper buttons     │
├─────────────────────────────────────────────┤  Y=331
│  IW_Weight_Wnd (100×58)                    │
│  - Current weight / Max weight display     │
├─────────────────────────────────────────────┤  Y=4
│  IW_Stats_Wnd (109×360)                    │
│  - Combat stats, attributes, resistances  │
├─────────────────────────────────────────────┤  Y=397
│  IW_BagZone_Wnd (410×45)                   │
│  - 8 bag slots (22-29)                     │
├─────────────────────────────────────────────┤  Y=447
│  IW_ButtonBar_Wnd (410×20)                 │
│  - Action buttons                          │
└─────────────────────────────────────────────┘  Y=470
```

---

## Key Architectural Differences

### **thorne_dev: Integrated Single-Tab Design**

**Pros**:
- Everything visible at once (no tab switching)
- Character info always present (quick reference)
- Combat stats always visible for build planning
- More immersive integrated gameplay

**Cons**:
- Packed interface (lots of data competing for space)
- Small font for attributes/stats (readability challenge)
- Fixed window size (limited by content volume)
- Limited expansion room for new systems

### **TAKP: Modular Zone-Based Design**

**Pros**:
- Clear separation of concerns (zones)
- Scalable (can adjust zone sizes independently)
- Tab-extensible (can add Evolution/Shrouds if needed)
- Cleaner visual hierarchy
- Easier to maintain and modify

**Cons**:
- Must switch tabs to see all info (less immersive)
- Character info less "always available"
- Requires more navigation

---

## What We Can Learn From thorne_dev

### **1. Character Context Should Always Be Available**
thorne_dev keeps player name/level/class/deity visible even when scrolling through stats. Consider:
- Adding character display to PlayerInfo zone (already planned)
- Showing level + class abbreviation prominently

### **2. Combat Vitals Are Important for Equipment Planning**
When equipping gear, players need quick reference to:
```
- HP totals (to estimate defense)
- AC/MIT/AVD (to see defense impact)
- ATK/DMG (to see offense impact)
```

**Suggestion**: Could add a small combat stats summary to EquipmentGrid zone for quick reference while equipping

### **3. Visual Separators Help Readability**
The 6 divider bars in thorne_dev prevent scanning errors. Consider:
- Adding separator lines between your zone sections
- Using StaticAnimation dividers (same pattern as thorne_dev)

### **4. Attributes Benefit from "Current/Max/Heroic" Format**
Shows player their heroic bonus at a glance (gold-colored):
```
STR  123 / 255 +45              ← Clearly shows +45 heroic bonus
```

**Suggestion**: If IW_Stats_Wnd shows attributes, use this format

### **5. Dual-Color Gauge for XP/AA**
Instead of separate sequential gauges, thorne_dev uses:
- Solid color fill for current progress
- Overlay lines for secondary progress
- Does this with EQType: 4 and DrawLinesFill: true

**Current Status**: Your plan has separate gauges (XP, then AA below)
- ✅ More readable than overlaid
- ❌ Takes more vertical space

### **6. Equipment Layout Optimization**
thorne_dev's asymmetrical layout clusters items by lookup frequency:
- Head zone top (fastest access)
- Armor scattered but grouped (modification zone)
- Weapons section bottom (combat readiness)

**Your Plan**: Anatomical 4-column grid is more logical but less "optimized"
- ✅ Easy to remember systematically
- ✅ Clear Row 2 armor grouping (user request)
- ❌ Not as "fast" as asymmetrical

---

## Data Volume Comparison

### **Visible on thorne_dev Inventory Tab: ~50 data points**

```
Equipment:
  - 23 equipment slots with icons
  - 6 divider bars

Character Info:
  - Title, Name, Last Name
  - Level, Class, Class abbreviation
  - Deity

Combat Stats:
  - HP (current/max)
  - Mana (current/max)
  - Endurance (current/max)
  - AC (single number)
  - MIT (mitigation)
  - AVD (avoidance)
  - ATK (attack)
  - DMG (spell damage)
  - HEAL (heal amount)

Progression:
  - EXP Gauge (visual + %)

Attributes:
  - STR current/max/heroic = 3
  - STA current/max/heroic = 3
  - AGI current/max/heroic = 3
  - DEX current/max/heroic = 3
  - WIS current/max/heroic = 3
  - INT current/max/heroic = 3
  - CHA current/max/heroic = 3
  
Total: 23 slots + 6 dividers + 3 info + 9 combat + 1 gauge + 21 attribute = 63 elements
```

### **Planned in TAKP Single View: ~30-40 data points** (TBD based on what we decide to show)

```
Player Info: Title/Name/Level/Class/Deity (5)
Progression: XP gauge + AA gauge (2)
Equipment: 20 slots (20)
Currency: Platinum/Gold/Silver/Copper buttons (4)
Weight: Current/Max (2)
Stats: Combat + Attributes + Resistances (15+)
Bags: 8 slots (8)
Buttons: Action buttons (variable)

Total: ~50-65 elements (depending on stats detail level)
```

---

## Recommendations for TAKP Design

### **Short-term (Keep Current Plan)**
✅ Proceed with 4-column anatomical grid  
✅ 45×45px slot size (better readability)  
✅ 420×470px window accommodates all zones  
✅ No tabs (simpler for TAKP classic)

### **Enhancements to Consider**
1. **Add visual separator bars** (like thorne_dev)
   - Between equipment and currency zones
   - Between currency and specs zones
   - Simple StaticAnimation dividers

2. **Ensure character context stays visible**
   - PlayerInfo zone already planned (good!)
   - Consider highlighting level near equipment

3. **When showing stats in IW_Stats_Wnd**
   - Use "current / max" format for attributes
   - Show only most-relevant combat stats
   - Consider heroic bonuses if supported

4. **Quick-reference combat summary**
   - Add AC/MIT/AVD to equipment zone?
   - Or keep in stats zone only (cleaner)

### **Not Recommended (TAKP Differences)**
❌ Power Source slot (no equivalent in TAKP)  
❌ Evolution/Shrouds tabs (not in TAKP game systems)  
❌ Alt. Currency tracking (not in TAKP)  
❌ Full 50+ stat display (too much for classic feel)

---

## Summary

**thorne_dev represents an "everything visible" design philosophy** - all character data in one tab, optimized for quick decisions during gameplay.

**Your TAKP plan represents a "focused and modular" approach** - separate zones that can be used independently, cleaner visual hierarchy, easier to extend.

**thorne_dev teaches us about readability and user patterns**, but TAKP's simpler game systems (no Evolution, no Power Source, no Loyalty Tokens) mean you don't need the full complexity.

**Hybrid recommendation**: Keep your zone architecture, but borrow visual refinements:
- Add separator bars for clarity
- Use "current/max" format for stats
- Ensure character context always visible
- Consider function-based equipment clustering if anatomical grid feels wrong in-game

Your layout plan is solid. The 4-column anatomical grid with Row 2 armor grouping (Neck/Chest/Back/Shoulders) is good for classic TAKP playstyle.

