# Target Window Analysis: Nillipuss vs. Thorne

## Summary

**Major Functional Differences Found**: Nillipuss includes combat-specific features (spell casting display, attack delay timer) that Thorne lacks. Thorne instead adds player gauges and weight display to the target window, repurposing it as a combined info panel.

## Window Files
- Nillipuss: `EQUI_TargetWindow.xml` (327 lines)
- Thorne: `EQUI_TargetWindow.xml` (621 lines)

## Element Inventory Comparison

### Elements in BOTH
- `TargetWindow` - Main window container

### Elements in Nillipuss ONLY (Missing from Thorne) ⚠️

**CRITICAL MISSING FEATURES:**

1. **`Target_Casting_SpellName` & `Target_Casting_SpellNameBG`** (Labels)
   - **What**: Displays the name of the spell the target is casting
   - **Why It Matters**: HIGH PRIORITY - Essential combat awareness feature
   - **User Request**: Specifically mentioned wanting this feature
   - **EQType**: **134** (Target spell name label)
   - **Implementation**: Simple label with EQType for target cast name
   - **Complexity**: LOW

2. **`Target_AttackDelay` (Gauge)**
   - **What**: Visual timer showing when the target will swing/attack next
   - **Why It Matters**: MEDIUM PRIORITY - Useful for tanks and melee timing
   - **User Request**: Mentioned "melee tick on target window"
   - **EQType**: **34** (Attack Delay)
   - **Implementation**: Single gauge element
   - **Complexity**: LOW

3. **`HPLabel` & `HPLabelBG`** (Labels)
   - **What**: Numeric HP percentage display (e.g., "100")
   - **EQType**: **29** (Target HP %)
   - **Why It Matters**: LOW PRIORITY - Thorne already shows target HP % via `TW_TargetHP_Pct` (EQType 29)

4. **`A_TargetBox` & `A_TargetBoxStaticAnim`** (Screen + Animation)
   - **What**: Decorative target box background
   - **Why It Matters**: LOW PRIORITY - Visual styling only

5. **`TW_CastGauge` (Gauge)**
   - **What**: Target casting progress bar (separate from spell name)
   - **Why It Matters**: MEDIUM PRIORITY - Shows cast progress visually
   - **EQType**: **7** (Casting bar)
   - **Note**: Thorne has `TW_TargetCasting_Gauge` (also EQType 7)

6. **`Target_HP` (Gauge)**
   - **What**: Target HP bar
   - **EQType**: **6** (Target HP)
   - **Why It Matters**: Essential - Thorne has equivalent: `TW_TargetHP_Gauge` (EQType 6)

### Elements in Thorne ONLY (Not in Nillipuss) ✨

**THORNE-SPECIFIC ADDITIONS:**

1. **`TW_PlayerHP_Gauge` & `TW_PlayerMana_Gauge`** (Gauges)
   - **What**: Player HP and Mana gauges displayed in target window
   - **EQTypes**: **1** (Player HP), **2** (Player Mana)
   - **Note**: Thorne repurposes target window as info panel
   - **Keep**: YES - Thorne-specific design choice

2. **`TW_PetHealth_Gauge`** (Gauge)
   - **What**: Pet health display in target window
   - **Note**: Useful for pet classes
   - **Keep**: YES - Added functionality

3. **`TW_Weight_Current`, `TW_Weight_Max`, `TW_Weight_Divider`** (Labels)
   - **What**: Player weight display (999/999 format)
   - **EQTypes**: **24/25** (Weight)
   - **Note**: Marked as "EXPERIMENTAL" in comments
   - **Keep**: MAYBE - Test for usefulness

4. **`TW_HP_Pct`, `TW_Mana_Pct`, `TW_TargetHP_Pct`** (Labels)  
   - **What**: Percentage displays for HP/Mana
   - **EQTypes**: **19** (Player HP%), **20** (Player Mana%), **29** (Target HP%)
   - **Keep**: YES - Core Thorne functionality

5. **`TW_ManaTick_Gauge`** (Gauge)
   - **What**: Likely a mana tick timer (similar to "Zeal Tick" in Nillipuss PlayerWindow)
   - **EQType**: **24** (Mana tick)
   - **Keep**: YES - Useful combat timer

6. **`A_OvalTarBG` & `A_OvalTarFill`** (Animations)
   - **What**: Oval-shaped target box styling (vs. rectangular in Nillipuss)
   - **Keep**: YES - Thorne visual identity

## Functional Comparison

| Feature | Nillipuss | Thorne | Priority to Port |
|---|---|---|---|
| **Target spell name display** | ✅ YES (Label) | ❌ NO | 🔴 **HIGH** - User requested |
| **Target attack delay timer** | ✅ YES (Gauge) | ❌ NO | 🟡 **MEDIUM** - Combat utility |
| **Target HP bar** | ✅ YES | ✅ YES | N/A - Both have |
| **Target casting progress bar** | ✅ YES | ✅ YES (different name) | N/A - Both have |
| **Player HP gauge in target window** | ❌ NO | ✅ YES | N/A - Thorne addition |
| **Player Mana gauge in target window** | ❌ NO | ✅ YES | N/A - Thorne addition |
| **Pet health in target window** | ❌ NO | ✅ YES | N/A - Thorne addition |
| **Weight display** | ❌ NO | ✅ (experimental) | N/A - Thorne addition |

## Layout Differences

**Nillipuss Layout:**
- Compact, focused on target information only
- Window size: ~280x50px (estimated)
- Target name at top
- HP bar with percentage
- Casting spell name display (when target casting)
- Attack delay timer below HP

**Thorne Layout:**
- Larger, multi-purpose info panel
- Window size: 270x70px
- Oval-shaped target box (visual style)
- Player HP/Mana gauges included
- Weight display (experimental)
- Pet health gauge
- No spell name or attack delay info

## Recommendations for Thorne

### Must-Have (HIGH Priority)
1. **Add Target Spell Casting Name Display** 
   - Port `Target_Casting_SpellName` label from Nillipuss
   - Position above or below target casting gauge
   - Font 2, white text with black shadow
   - **User specifically requested this feature**
   - Complexity: LOW - just add 2 label elements

### Should-Have (MEDIUM Priority)
2. **Add Target Attack Delay Timer**
   - Port `Target_AttackDelay` gauge from Nillipuss
   - Small gauge below target HP (or near other timers)
   - EQType 34
   - **User mentioned "melee tick on target window"**
   - Complexity: LOW - single gauge element

### Consider (LOW Priority)
3. **Review weight display usefulness**
   - Marked as "experimental" in Thorne code
   - May be removed if too cluttered
   - Test in-game before keeping

## Implementation Plan

### Phase 1: Add Target Spell Name (v0.7.0)
```xml
<!-- Add to thorne_drak/EQUI_TargetWindow.xml -->
<Label item="TW_TargetCasting_SpellName">
  <ScreenID>TW_TargetCasting_SpellName</ScreenID>
  <Font>2</Font>
   <EQType>134</EQType>
  <RelativePosition>true</RelativePosition>
  <Location><X>?</X><Y>?</Y></Location>
  <Size><CX>200</CX><CY>14</CY></Size>
  <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
  <NoWrap>true</NoWrap>
  <AlignCenter>true</AlignCenter>
</Label>

<!-- Shadow label for readability -->
<Label item="TW_TargetCasting_SpellNameBG">
  [Same as above with black color and +1 offset]
</Label>
```

**EQType verified**: 134 for target spell name label in Nillipuss.

### Phase 2: Add Attack Delay Timer (v0.7.0 or v0.8.0)
```xml
<Gauge item="TW_TargetAttackDelay">
  <ScreenID>TW_TargetAttackDelay</ScreenID>
  <EQType>34</EQType>
  <RelativePosition>true</RelativePosition>
  <Location><X>?</X><Y>?</Y></Location>
  <Size><CX>120</CX><CY>4</CY></Size>
  <GaugeDrawTemplate>
    <Background>gauge_background</Background>
    <Fill>gauge_fill_red</Fill>
  </GaugeDrawTemplate>
</Gauge>
```

## Line Count Stats
- Nillipuss: 327 lines (simpler, focused)
- Thorne: 621 lines (complex, feature-rich)
- Difference: Thorne has 294 more lines (almost double)

## Conclusion

Thorne's TargetWindow has evolved into a multi-purpose information display with player gauges and pet health, diverging from the traditional target-only focus. However, it's **missing critical combat awareness features** that Nillipuss has:

✅ **Must add**: Target spell casting name (HIGH priority user request)  
✅ **Should add**: Target attack delay timer (MEDIUM priority combat utility)  
✅ **Keep**: Thorne's player gauge additions (unique design choice)  
⚠️ **Evaluate**: Weight display usefulness (experimental feature)

**Priority for v0.7.0**: Add target spell casting name display - this is a quick, high-value addition explicitly requested by the user.
