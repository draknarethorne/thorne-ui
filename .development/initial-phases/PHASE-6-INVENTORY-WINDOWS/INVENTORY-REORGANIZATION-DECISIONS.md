# Inventory Window Reorganization - Decision Document

**Date**: February 4, 2026  
**Branch**: feature/v0.6.0-inventory-and-windows  
**Purpose**: Finalize subwindow architecture and element grouping

---

## Current Layout Visual Map (400×390px)

```
┌─────────────────────────────────────────────────────────────────┐
│ [Name: char]         [Level: 60]                                │ Y=4
│ [Class: Warrior]                                                │ Y=19
│ [Deity: Karana]                                                 │ Y=34
├───────────────────────────────────────────────────────────────  │
│ LEFT AREA          │  EQUIPMENT SCATTERED  │  RIGHT AREA        │
│                    │                       │                    │
│ ?                  │  Eq1  Eq5  Eq3  Eq2Eq4│  STR: 180          │ Y=154
│ ?                  │       Eq9  Eq10 Eq20  │  STA: 175          │ Y=169
│ ?                  │            Eq17 Eq8...│  AGI: 110          │ Y=184
│ ?                  │  Eq13Eq14 Eq15...Eq18 │  DEX: 115          │ Y=199
│                    │  (No logical order)   │  WIS: 95           │ Y=214
│ [CharView]         │  Bag22 Bag23          │  INT: 90           │ Y=229
│  74x138            │  Bag24 Bag25          │  CHA: 85           │ Y=244
│  Class Anim        │  Bag26 Bag27          │  AC: 1250          │ Y=259
│  (2, 169)          │  Bag28 Bag29          │  ATK: 950  │ Y=274
│                    │                        │  Poison: 120       │ Y=289
│ [Face Btn]         │  Money0 (Plat) 93,193 │  Magic: 110        │ Y=304
│  (2, 139)          │  Money1 (Gold) 93,219 │  Disease: 100      │ Y=319
│                    │  Money2 (Silv) 93,246 │  Fire: 115         │ Y=334
│                    │  Money3 (Copp) 93,273 │  Cold: 105         │ Y=349
│                    │                        │  Weight: 85/300    │ Y=367
├─────────────────────────────────────────────────────────────────│
│                │         │                [Alt Adv] [Done]      │ Y=358
│                │         │                 101,358   299,358    │
└─────────────────────────────────────────────────────────────────┘
```

**PROBLEM**: Equipment has NO anatomical organization, everything scattered

---

## Proposed Subwindow Architecture

### OPTION A: 3-Zone with Bottom Bags (Recommended)

**Window Size**: 400×410px (height +20px for bottom bags)

```
┌─────────────────────────────────────────────────────────────────┐
│ ┌───────────────┬───────────────────────┬──────────────────────┐│
│ │ LEFT ZONE     │ CENTER ZONE           │ RIGHT ZONE           ││
│ │(5,4) 85x350   │ (95, 4) 215x300       │ (315,4) 80x300       ││
│ │               │                       │                      ││
│ │ Name          │ ┌──HEAD ROW────────┐  │ AC: 1250             ││
│ │ Level         │ │Ear Neck Face H Ear│  │ ATK: 950             ││
│ │ Class         │ └──────────────────┘  │ HP: 1200/1200        ││
│ │ Deity         │                       │ Mana: 800/800        ││
│ │               │ ┌──ARMS ROW────────┐  │                      ││
│ │               │ │Rng Wri A H Wri Rng│  │ STR: 180             ││
│ │ [Class Anim]  │ └──────────────────┘  │ STA: 175             ││
│ │   74x138      │                       │ AGI: 110             ││
│ │   (centered)  │ ┌──TORSO ROW───────┐  │ DEX: 115             ││
│ │               │ │Sho Ch Bk Wa Lg Ft │  │ WIS: 95              ││
│ │               │ └──────────────────┘  │ INT: 90              ││
│ │               │                       │ CHA: 85              ││
│ │ Weight:       │ ┌──WEAPONS ROW────┐   │                      ││
│ │  85/300       │ │Pri Sec Rng Ammo │   │ Poison: 120          ││
│ │               │ └─────────────────┘   │ Magic: 110           ││
│ │               │                       │ Disease: 100         ││
│ │               │ ┌──CURRENCY───────┐   │ Fire: 115            ││
│ │[Face Button]  │ │Plat Gold Silv Cp│   │ Cold: 105            ││
│ │               │ │ (4 buttons)     │   │                      ││
│ │               │ └─────────────────┘   │ ─────────────────    ││
│ │               │                       │ XP Gauge ████▓▓▓▓▓   ││
│ │[Done Button]  │                       │ 85% to 61            ││
│ │               │                       │ AA Gauge ████▓▓▓▓▓   ││
│ │               │                       │ 12 AA (3 available)  ││
│ └───────────────┴───────────────────────┴──────────────────────┘│
│ ┌──BAG ZONE (Full Width Bottom)──────────────────────────────┐  │
│ │ [Bag1] [Bag2] [Bag3] [Bag4] [Bag5] [Bag6] [Bag7] [Bag8]   │  │
│ │  (95,360) → 8 bags × 45px horizontal, single row           │  │
│ └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         Alt Adv button moves to LEFT ZONE (below Done)
```

**Advantages**:
- ✅ Clean 3-zone separation
- ✅ All 8 bags easily accessible in one row
- ✅ Equipment in center prominently featured
- ✅ Stats never overlap with inventory

**Disadvantages**:
- ❌ Window height increases to ~410px (still fits 800×600)
-❌ Bags separated from equipment conceptually

---

### OPTION B: 3-Zone with Right-Side Bags

**Window Size**: 400×390px (same as current)

```
┌─────────────────────────────────────────────────────────────────┐
│ ┌───────────────┬───────────────────────┬──────────────────────┐│
│ │ LEFT ZONE     │ CENTER ZONE           │ RIGHT ZONE           ││
│ │(5,4) 85x350   │ (95, 4) 215x350       │ (315,4) 80x350       ││
│ │               │                       │                      ││
│ │ Name          │ ┌──HEAD ROW────────┐  │ ┌─STATS──────────┐  ││
│ │ Level         │ │Ear Neck Face H Ear│  │ │AC: 1250        │  ││
│ │ Class         │ └──────────────────┘  │ │ATK: 950        │  ││
│ │ Deity         │                       │ │HP: 1200/1200   │  ││
│ │               │ ┌──ARMS ROW────────┐  │ │Mana: 800/800   │  ││
│ │               │ │Rng Wri A H Wri Rng│  │ │STR-CHA (7 rows)│  ││
│ │ [Class Anim]  │ └──────────────────┘  │ │Resistances (5) │  ││
│ │   74x138      │                       │ └────────────────┘  ││
│ │   (centered)  │ ┌──TORSO ROW───────┐  │                      ││
│ │               │ │Sho Ch Bk Wa Lg Ft │  │ ┌─PROGRESSION────┐  ││
│ │               │ └──────────────────┘  │ │XP: ████▓▓▓▓ 85% │  ││
│ │               │                       │ │AA: ████▓▓▓▓ 12pt│  ││
│ │ Weight:       │ ┌──WEAPONS ROW────┐   │ └─────────────────┘ ││
│ │  85/300       │ │Pri Sec Rng Ammo │   │                      ││
│ │               │ └─────────────────┘   │ ┌─BAG ZONE───────┐  ││
│ │               │                       │ │[Bag1] [Bag2]   │  ││
│ │[Face Button]  │ ┌──CURRENCY───────┐   │ │[Bag3] [Bag4]   │  ││
│ │               │ │Plat Gold Silv Cp│   │ │[Bag5] [Bag6]   │  ││
│ │[Done Button]  │ │ (4 vert buttons)│   │ │[Bag7] [Bag8]   │  ││
│ │[Alt Adv Btn]  │ └─────────────────┘   │ └─────────────────┘ ││
│ └───────────────┴───────────────────────┴──────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Advantages**:
- ✅ No window height increase
- ✅ Bags logically grouped with stats zone
- ✅ Compact design

**Disadvantages**:
- ❌ Bags in 2×4 grid harder to visually scan
- ❌ Right zone becomes cramped (Stats + Progression + Bags)
- ❌ Less breathing room

---

## Recommended Subwindow Definitions

### Subwindow 1: IW_LeftZone
```xml
<Screen item="IW_LeftZone">
  <ScreenID>IW_LeftZone</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>5</X><Y>4</Y></Location>
  <Size><CX>85</CX><CY>350</CY></Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_Transparent>false</Style_Transparent>
  <Pieces>
    IW_Name IW_Level IW_Class IW_Deity
    ClassAnim IW_CharacterView
    IW_Weight IW_CurrentWeight IW_MaxWeight
    IW_FacePick
    IW_DoneButton
    IW_AltAdvBtn
  </Pieces>
</Screen>
```

**Contents**:
- Character name, level, class, deity labels
- Class animation subwindow (nested)
- Weight display
- Face button
- Done button
- Alt Adv button (relocated from bottom)

---

### Subwindow 2: IW_EquipmentGrid
```xml
<Screen item="IW_EquipmentGrid">
  <ScreenID>IW_EquipmentGrid</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>95</X><Y>4</Y></Location>
  <Size><CX>215</CX><CY>350</CY></Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_Transparent>false</Style_Transparent>
  <Pieces>
    InvSlot1 InvSlot2 InvSlot3 InvSlot4 InvSlot5
    InvSlot6 InvSlot7 InvSlot8 InvSlot9 InvSlot10
    InvSlot11 InvSlot12 InvSlot13 InvSlot14 InvSlot15
    InvSlot16 InvSlot17 InvSlot18 InvSlot19 InvSlot20
    InvSlot21
    IW_Money0 IW_Money1 IW_Money2 IW_Money3
  </Pieces>
</Screen>
```

**Contents**:
- All 21 equipment slots in anatomical layout
- Currency buttons (Plat, Gold, Silver, Copper)

---

### Subwindow 3: IW_StatsZone
```xml
<Screen item="IW_StatsZone">
  <ScreenID>IW_StatsZone</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>315</X><Y>4</Y></Location>
  <Size><CX>80</CX><CY>240</CY></Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_Transparent>false</Style_Transparent>
  <Pieces>
    IW_AC IW_ACNumber
    IW_ATK IW_ATKNumber
    IW_HP IW_CurrentHP
    IW_Mana IW_CurrentMana
    IW_STR IW_STRNumber
    IW_STA IW_STANumber
    IW_AGI IW_AGINumber
    IW_DEX IW_DEXNumber
    IW_WIS IW_WISNumber
    IW_INT IW_INTNumber
    IW_CHA IW_CHANumber
    IW_Poison IW_PoisonNumber
    IW_Magic IW_MagicNumber
    IW_Disease IW_DiseaseNumber
    IW_Fire IW_FireNumber
    IW_Cold IW_ColdNumber
  </Pieces>
</Screen>
```

**Contents**:
- AC, ATK
- HP, Mana (current/max)
- All 7 base attributes (STR-CHA)
- All 5 resistances

---

### Subwindow 4: IW_ProgressionZone
```xml
<Screen item="IW_ProgressionZone">
  <ScreenID>IW_ProgressionZone</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>315</X><Y>250</Y></Location>
  <Size><CX>80</CX><CY>60</CY></Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_Transparent>false</Style_Transparent>
  <Pieces>
    IW_ExpGauge IW_EXP_Percentage IW_NextLevel
    IW_AltAdvGauge IW_AltAdv
  </Pieces>
</Screen>
```

**Contents**:
- XP gauge + percentage label
- AA gauge + AA label (Zeal)
- **NOTE**: Keep progression SEPARATE from main stats for modularity

---

### Subwindow 5: IW_BagZone (OPTION A - Bottom Row)
```xml
<Screen item="IW_BagZone">
  <ScreenID>IW_BagZone</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>95</X><Y>360</Y></Location>
  <Size><CX>300</CX><CY>45</CY></Size>
  <DrawTemplate>WDT_Inner</DrawTemplate>
  <Style_Transparent>false</Style_Transparent>
  <Pieces>
    InvSlot22 InvSlot23 InvSlot24 InvSlot25
    InvSlot26 InvSlot27 InvSlot28 InvSlot29
  </Pieces>
</Screen>
```

**Contents**: All 8 bag slots in single horizontal row

---

## XP/AA Gauge Implementation Status

**Current State**:
- XP Gauge: ✅ Fully implemented (IW_ExpGauge at 279, 138, size 116×8)
- AA Gauge: ⚠️ **PLACEHOLDER ONLY** (IW_AltAdvGauge exists but size 1×1 - effectively hidden)

**Required Work for AA Gauge**:
1. Set proper size (recommend 116×8 to match XP gauge)
2. Set location (recommend 315,270 in new ProgressionZone)
3. Confirm EQType 5 works (standard P2002) or use Zeal EQTypes 71-73
4. Add percentage/points label (IW_AltAdv already exists as label)
5. Match visual styling to XP gauge (colors, templates)

**Test Plan**:
- Verify AA gauge updates on kill
- Test on standard TAKP client (EQType 5)
- Test on Zeal client (EQTypes 71-73 for enhanced labels)

---

## Decision Matrix

| Decision | Option A (Bottom Bags) | Option B (Side Bags) |
|----------|------------------------|----------------------|
| **Window Height** | 410px (+20px) | 390px (same) |
| **Bag Visibility** | ⭐ Excellent (1 row) | Good (2×4 grid) |
| **Stats Density** | ⭐ Spacious | Cramped |
| **Zone Separation** | ⭐ Clear | Stats/Bags mixed |
| **800×600 Compat** | ✅ Yes (~204px margin) | ✅ Yes |
| **Conceptual Logic** | Bags separate from stats | Bags with inventory |
| **Recommendation** | ✅ **RECOMMENDED** | Acceptable fallback |

---

## Implementation Questions - YOUR INPUT NEEDED

### Question 1: Bag Placement
**Which bag layout do you prefer?**
- [ ] **Option A**: Bottom row (8 bags horizontal, window +20px height)
- [ ] **Option B**: Right side (2×4 grid, same window height)
- [ ] **Option C**: Other configuration? (describe)

**My Recommendation**: Option A for better visual clarity

---

### Question 2: Progressi Zone Separation
**Should XP/AA gauges be in separate subwindow from stats?**
- [ ] **Yes** - Keep IW_ProgressionZone separate (modular, easier variants)
- [ ] **No** - Merge into IW_StatsZone (simpler, one zone)

**My Recommendation**: Keep separate for modularity (players may want stats-only variants without gauges)

---

### Question 3: Currency Button Layout
**How should Plat/Gold/Silver/Copper buttons be arranged?**
- [ ] **4 vertical buttons** in center zone (current: 93,193 → 93,273, 26px spacing)
- [ ] **4 horizontal buttons** in one row
- [ ] **2×2 grid** (compact square)

**My Recommendation**: 4 vertical maintains current muscle memory

---

### Question 4: AA Gauge Priority
**When should we implement AA gauge?**
- [ ] **Phase 1** - Implement with initial subwindow reorganization
- [ ] **Phase 2** - After equipment reorganization complete
- [ ] **Phase 3** - Final polish after testing

**My Recommendation**: Phase 2 (focus on equipment layout first, then add gauges)

---

## Next Actions

1. **Get your input on 4 questions above**
2. Update PHASE-3.9-INVENTORY-REDESIGN.md with finalized decisions
3. Calculate exact coordinates for chosen layout
4. Begin XML subwindow implementation
5. Reposition equipment slots to anatomical layout
6. Test and iterate

---

**Status**: Awaiting decision on bag placement and zone architecture
