# PlayerWindow Analysis (EQUI_PlayerWindow.xml)

## Summary
- **Lines**: Nillipuss: 2808 | Thorne: 951 (**195% larger in Nillipuss**)
- **Elements**: Nillipuss: 106 | Thorne: 35 (**200% more elements in Nillipuss**)
- **Status**: 🔴 CRITICAL - Massive feature differences

---

## EQType Validation (Key Elements)

**Verified EQType bindings** (Thorne vs Nillipuss):

| Feature | Thorne Element (EQType) | Nillipuss Element (EQType) | Notes |
|---|---|---|---|
| Player HP gauge | `PW_Gauge_HP` (Gauge, **1**) | `Player_HP_*` layers (Gauge, **1**) | Same data, different visual system (single vs multi-layer). |
| HP percent | `PW_HP_Pct` (Label, **19**) | `Player_HPLabel` (Label, **19**) | Same data, different labeling. |
| Mana gauge | `PW_Gauge_Mana` (Gauge, **2**) | `Player_Mana` (Gauge, **2**) | Same data. |
| Mana tick (Zeal) | `PW_Mana_Tick` (Gauge, **24**) | `Zeal_Tick` (Gauge, **24**) | Same data, different visuals/size. |
| Stamina/Fatigue | `PW_Gauge_Stamina` (Gauge, **3**) + `PW_Stamina_Pct` (Label, **21**) | `Player_Fatigue` (Gauge, **3**) + `Player_FatigueLabel` (Label, **21**) | Same data, different naming. |
| XP gauge | `PW_Gauge_XP` (Gauge, **4**) | `PW_ExpGauge` (Gauge, **4**) | Same data. |
| AA gauge | `PW_Gauge_AAXP` (Gauge, **5**) | `PW_AAExpGauge` (Gauge, **5**) | Same data. |
| XP per hour | `PW_XP_PerHour_Value` (Label, **81**) | `PW_ExpPerHour_Percentage` (Label, **81**) | Same data. |
| AA per hour | — | `PW_AAHR_Percentage` (Label, **86**) | Nillipuss-only label. |

**Hidden/unused EQType elements in Nillipuss (not referenced by any Screen/Page pieces):**
`PW_Timer_1`–`PW_Timer_6` (Gauge, **2**), `PW_AAGauge` (Gauge, **5**), `PW_AA_Percentage` (Label, **27**), `PW_BreathGauge` (Gauge, **8**), `Player_HPNumber` (Label, **70**), `Player_ManaNumber` (Label, **128**).

---

## Element Inventory Comparison

### Nillipuss Total Elements (106)
Includes: Color-changing HP gauge layers (13 elements), timer animations, attack indicators, fatigue display, etc.

### Thorne Total Elements (35)
Includes: Single-layer HP gauge, text displays, AA displays, pet health, etc.

---

## CRITICAL DIFFERENCE 1: Color-Changing HP Gauge System

### Nillipuss Implementation (MULTI-LAYER GAUGE)
```
Player_HP_0      - Base HP bar background
Player_HP_1A     - GREEN layer (100-75% health)
Player_HP_1A_X   - GREEN extension/overlay variant
Player_HP_1B     - GREEN variant 2
Player_HP_2A     - YELLOW layer (75-50% health)
Player_HP_2A_X   - YELLOW extension/overlay variant
Player_HP_2B     - YELLOW variant 2
Player_HP_3A     - ORANGE layer (50-25% health)
Player_HP_3A_X   - ORANGE extension/overlay variant
Player_HP_3B     - ORANGE variant 2
Player_HP_4A     - RED layer (25-0% health)
Player_HP_4A_X   - RED extension/overlay variant
Player_HP_4B     - RED variant 2
```

**Total**: 13 separate color layer elements

**Visual Effect**: HP bar smoothly transitions:
- Green at full health
- Yellow as damage increases
- Orange at moderate damage
- Red at critical health

### Thorne Implementation (SINGLE-LAYER GAUGE)
```
PW_Gauge_HP    - Single HP gauge (all states displayed as one color)
PW_HP_Pct      - Percentage text display
PW_HP_PctSign  - Percentage sign
PW_HP_Values   - HP values text
```

**Total**: 4 elements for HP display

**Visual Effect**: Single-color red gauge bar

---

## CRITICAL DIFFERENCE 2: Zeal Tick Mana Regen Timer

### Nillipuss Implementation (EQType-verified)
- **`Zeal_Tick` (Gauge, EQType 24)**
  - Full-width (240x11) visual tick bar using `TickFill`
  - Positioned over the mana row for a prominent pulse

### Thorne Implementation (EQType-verified)
- **`PW_Mana_Tick` (Gauge, EQType 24)**
  - Compact width (120x8) tick bar using `A_GaugeLinesFill_Tall`
  - Positioned under the mana gauge

### Key Difference
Both use **EQType 24**, so the **data source is identical**. The difference is **purely visual/layout**. Nillipuss also defines a **separate 6-segment timer system** (`PW_Timer_1–6`, EQType 2), but those gauges are **not referenced** in any Screen/Page pieces, so they are effectively hidden/inactive.

---

## DIFFERENCE 3: Fatigue vs. Stamina Naming

### Nillipuss (Fatigue)
- `Player_Fatigue` (Gauge, **EQType 3**)
- `Player_FatigueLabel` (Label, **EQType 21**)

### Thorne (Stamina)
- `PW_Gauge_Stamina` (Gauge, **EQType 3**)
- `PW_Stamina_Pct` (Label, **EQType 21**)

**Conclusion**: This is the **same stat**, just labeled differently. Thorne already displays the same underlying data.

---

## Feature Impact Assessment

### 🔴 HIGH PRIORITY - v0.8.0+

**1. Color-Changing HP Gauge**
- **Value**: CRITICAL - Essential combat awareness feature
- **User Request**: Multiple users ask for this
- **Complexity**: **HIGH**
  - Requires texture sheets for 4 color states
  - Need multi-layer gauge animations in EQUI_Animations.xml
  - EQType bindings for each layer
  - Gauge piece textures for each color
  - Complex positioning/layering logic
  
- **Estimated Effort**: 15-20 hours design + implementation
- **Dependencies**:
  - gauge_pieces01.tga (Thorne has) + color variants
  - Animation definitions for color transitions
  - EQType system understanding
  - Careful layering to prevent Z-order issues

**2. Zeal Tick Mana Regen Timer**
- **Value**: HIGH - Specialist feature (mainly for certain classes)
- **Complexity**: **MEDIUM**
  - Visual polish (full-width tick, alternate fill, possible marker options)
  - Optional timer segment system (currently defined in Nillipuss but unused)
  
- **Estimated Effort**: 8-12 hours
- **Dependencies**:
  - Animation frame definitions
  - Texture assets for timer marks
  - Custom animation sequencing

### 🟡 MEDIUM PRIORITY - v0.8.0+

**3. Fatigue Display**
- **Status**: Already present in Thorne as Stamina (EQType 3 / 21)
- **Recommendation**: No additional feature needed unless you want different visuals

---

## Implementation Strategy

### Option A: SHORT TERM (v0.7.0) - Focus on High-Value Low-Complexity Features
**Skip color-changing HP gauge for now** (complexity too high for v0.7.0 timeline)
**Instead focus on**:
- Spell recast timers (CastSpellWnd) - DONE complexity
- Resistance icons (ActionsWindow) - LOW complexity  
- Target spell name - LOW complexity
- Spellbook Meditate button - LOW complexity

**Then v0.8.0**: Color-changing HP gauge + Zeal tick (when more design time available)

### Option B: LONG TERM (v0.8.0+) - Full Implementation
Port all PlayerWindow features including color gauge system after analyzing design/implementation requirements more thoroughly.

---

## XML Structure Reference

### How Nillipuss Implements Multi-Layer Gauge

Each color layer is likely defined as:
```xml
<Gauge item="Player_HP_1A">          <!-- GREEN layer -->
  <ScreenID>Player_HP_1A</ScreenID>
  <Location>...</Location>
  <Size>...</Size>
  <Style_TopCap>...</Style_TopCap>
  <Style_BottomCap>...</Style_BottomCap>
  <TextureInfo>
    <Background>gauge_pieces_green.tga</Background>
    <Foreground>gauge_pieces_green_filled.tga</Foreground>
  </TextureInfo>
  <EQType>HP_Percent</EQType>
  <EQType>HP_CriticalCheck</EQType>
  <!-- Logic to show only when 75-50% health -->
</Gauge>
```

The _X and variant elements suggest:
- _X suffix: Extended/wider version for large health values
- _1A vs _1B: Alternative styling variants
- Grouped by percentage ranges (0-25%, 25-50%, etc.)

---

## Questions for User

1. **Is color-changing HP gauge a v0.7.0 requirement or v0.8.0 acceptable?**
   - If v0.7.0: Need significant design+ implementation time
   - If v0.8.0+: Can focus on lower-complexity features first

2. **How important is Zeal tick timer compared to HP gauge?**
   - Developers/optimizers care more about Zeal timing
   - Casual players might prefer simpler HP gauge over timer

3. **Do we want a different visual treatment for Stamina/Fatigue?**
  - Data already present in Thorne (EQType 3 / 21)
  - Only needs visual redesign if desired

---

## Recommendation

**For v0.7.0**: Skip PlayerWindow changes (too complex)
- Focus on confirmed low-complexity features:
  - ✅ Spell recast timers (CastSpellWnd)
  - ✅ Resistance icons (ActionsWindow)
  - ✅ Target spell name (TargetWindow)
  - ✅ Meditate button (SpellBookWnd)

**For v0.8.0**: Tackle PlayerWindow features
- Begin with color-changing HP gauge research
- Parallel: Zeal tick timer research
- Phase in by creating Options variants for different styles

**Benefit**: v0.7.0 delivers quick wins with confirmed features, v0.8.0 focuses on the flagship "color HP bar" that many UIs are known for.
