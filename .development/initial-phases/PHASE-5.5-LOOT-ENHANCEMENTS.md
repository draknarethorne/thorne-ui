[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 5.5: Loot Window Enhancements

**Status**: PLANNED  
**Priority**: Medium  
**Target Completion**: March 2026

## Objectives

- Add Destroy button to Loot window for quick item deletion from corpse loot
- Add weight cur/max display to prevent over-encumbrance while looting
- Improve looting workflow and inventory management
- Maintain current 4-column layout and functionality

## Planned Enhancements

### Destroy Button

**Purpose**: Destroy unwanted items directly from corpse loot without picking them up

**Workflow improvement**:
- Current: Loot item → Open inventory → Find item → Destroy
- Proposed: Select item in loot window → Click Destroy → Confirm

**Research findings**: 
- Destroy button (`IW_Destroy`) exists in Inventory window implementations
- Found in `QQQuarm/EQUI_Inventory.xml` and `duxaUI/EQUI_Inventory.xml` community variants
- Button uses standard Button element with "Destroy" text
- **Unknown**: Whether Destroy button can function in LootWnd context
- **Needs testing**: Does client support destroy action from loot window?

**Implementation considerations**:
- May be window-specific (Inventory vs. Loot context)
- Could require item to be in player inventory first
- Need to verify EQType or special button mechanism
- Zeal client feature ("Fast Item Destroy") exists but is separate

---

## Bug Fixes

### Window Height Fix (v0.4.0 - February 2, 2026)

**Issue**: Large Loot window too short, cutting off bottom 5 rows of loot slots

**Symptoms**:
- Tester reported loot window "doesn't have as many slots as default"
- Player corpses with full inventory couldn't show all items
- Scrolling didn't reach slots 25-29 (last 5 rows cut off)

**Root Cause Analysis**:
- Window height: 360px
- Scrollable area: ~310px (after top/bottom margins)
- Last slot (slot 29): Y=290, extends to Y=335
- **Problem**: Slots needed 335px but only 310px available

**Investigation**:
- Default loot window: 420px height (60px taller)
- Both windows have identical 30 slots (LW_LootSlot0-29) ✓
- Issue was VISIBILITY not QUANTITY
- thorne_drak uses larger slots (45×45 vs 40×40) + 4-column layout

**Fix**:
1. Increased window height: 360px → **420px** (matches default)
2. Moved all buttons down: Y=302 → **Y=362** (+60px)
3. New scrollable area: **370px** (sufficient for all slots)

**Verification**:
- Slot layout: 6 rows × 5 columns = 30 slots
- Last slot ends at Y=335
- Available scroll area: 370px ✓
- All 30 slots now accessible with scrolling ✓

**Files Modified**:
- `thorne_drak/EQUI_LootWnd.xml` (main window)
- `thorne_drak/Options/Loot/Large Loot/EQUI_LootWnd.xml` (options variant)
- `thorne_drak/Options/Loot/Large Loot/README.md` (documentation)

**Lesson**: Always verify complete slot accessibility in scrollable areas, especially with larger slot sizes.

---


**Available EQTypes**:
- **EQType 24** (Label): Current character weight
- **EQType 25** (Label): Maximum weight capacity

**Proposed format**:
- "WT: 45 / 100" (current / max)
- Alternative: "Weight: 45/100 lbs"
- Color coding: Green (safe), Yellow (75%+), Red (90%+)

**Placement options**:
1. **Bottom of window** (below buttons) - Most visible, requires height increase
2. **Top title area** (near corpse name) - Non-intrusive but smaller space
3. **Above buttons** (Y=~295) - Compromises between visibility and space

**Current loot window layout**:
- Window: 246×360 px (sizable)
- Corpse name: Y=2, full width (246px)
- Scroll area: Auto-stretch with TopAnchorOffset=22, BottomAnchorOffset=28
- Buttons at Y=302: [Loot All][Link All][Done] (3 buttons, 75px each)

### Layout Adjustments

**Current button layout** (Y=302):
- Loot All: X=4, CX=75
- Link All: X=84, CX=75
- Done: X=164, CX=75

**Proposed Destroy button placement**:
- **Option A**: Add 4th button in row (shrink existing buttons to 55px each)
  - [Loot All][Link All][Destroy][Done]
  - Buttons: 4×55px = 220px (fits in 246px width with margins)
- **Option B**: Replace Link All with Destroy (less ideal - removes Zeal feature)
  - [Loot All][Destroy][Done]
- **Option C**: Two-row button layout (increases window height)
  - Row 1: [Loot All][Link All]
  - Row 2: [Destroy][Done]

**Weight display placement**:
- Add Label at Y=285 (above buttons): "WT: 24 / 25"
- Size: CX=100, CY=12
- Center-aligned at X=73
- Requires adjusting BottomAnchorOffset from 28 to 40

## Research Findings

### Destroy Button Investigation

**Inventory Window Implementation** (QQQuarm/EQUI_Inventory.xml reference):
```xml
<Button item="IW_Destroy">
  <ScreenID>IW_Destroy</ScreenID>
  <Text>Destroy</Text>
  <!-- Standard button properties -->
</Button>
```

**Key questions**:
1. Does `IW_Destroy` ScreenID work in LootWnd context?
2. Is destroy action tied to Inventory window specifically?
3. Does it require item to be in player inventory first?
4. Can we use custom ScreenID like `LW_DestroyButton`?

**Zeal "Fast Item Destroy" feature**:
- Checkbox in EQUI_OptionsWindow.xml (`OGP_FastItemDestroyCheckbox`)
- Removes confirmation dialog when destroying items
- Separate from adding Destroy button to windows
- Would complement LootWnd Destroy button if implemented

**Action required**:
- Test Destroy button in LootWnd with temporary XML modification
- Verify client accepts destroy command from loot window
- Document whether feature is window-specific or universal

### Weight EQTypes

Confirmed available (from .docs/technical/eqtypes.md):

| EQType | Data Field | Element Type | Format | Usage |
|--------|------------|--------------|--------|-------|
| 24 | Current Weight | Label | Number | Current character weight |
| 25 | Maximum Weight | Label | Number | Max carrying capacity |

**Note**: EQType 24 is context-dependent:
- As **Label**: Current weight (standard)
- As **Gauge** in PlayerWindow (Zeal): Mana tick timer
- Must use as Label in LootWnd to display weight

**Implementation**: Straightforward - add two Labels with EQTypes 24 and 25

## Constraints

- Loot window DOES fade (client-enforced transparency)
  - Weight display may not always be visible when window fades
  - Not critical - users typically have window focused when looting
- Destroy button may be window-specific (needs testing)
- Must maintain 4-column item grid layout (current design)
- Window is sizable - layout must scale properly with anchoring
- Button bar has limited space (246px width, 3 existing buttons)
- Adding weight display reduces scroll area height slightly

## Implementation Plan

### Phase 5.5.1: Research & Testing
- [ ] Test Destroy button in LootWnd (create test XML)
- [ ] Verify client accepts destroy action from loot window
- [ ] Document ScreenID requirements (IW_Destroy vs LW_DestroyButton)
- [ ] Design button layout mockup (4-button vs 2-row)

### Phase 5.5.2: Weight Display Implementation
- [ ] Add weight labels (EQTypes 24, 25) above buttons
- [ ] Format: "WT: cur / max"
- [ ] Position at Y=285, centered
- [ ] Adjust BottomAnchorOffset to accommodate weight display
- [ ] Test with various weight loads and window sizes

### Phase 5.5.3: Destroy Button Implementation (if feasible)
- [ ] Add Destroy button to button row
- [ ] Resize existing buttons to fit 4 buttons (55px each)
- [ ] Configure button draw template and styling
- [ ] Test destroy functionality in-game
- [ ] Add confirmation dialog if needed
- [ ] Document limitations if feature is restricted

### Phase 5.5.4: Layout Refinement
- [ ] Ensure 4-column grid layout maintained
- [ ] Verify auto-stretch and anchoring with new elements
- [ ] Test window resizing behavior
- [ ] Optimize spacing and alignment
- [ ] Update README documentation

## Success Criteria

- ✅ Weight display accurate and clearly visible
- ✅ Weight format easy to read at a glance
- ✅ Layout maintains 4-column loot grid
- ✅ No interference with existing Loot All/Link All/Done buttons
- ✅ Window remains sizable without layout issues
- ✅ Destroy button functional (if technically feasible)
- ✅ Workflow improvement validated through testing

## Alternative Approaches

If Destroy button is NOT feasible:
1. Focus solely on weight display enhancement
2. Add "Quick Destroy" keybind documentation (if available)
3. Document Zeal "Fast Item Destroy" feature as workaround
4. Consider auto-loot filters as alternative QoL improvement

If button space is too constrained:
1. Use 2-row button layout (increases window height ~20px)
2. Add dropdown menu for secondary actions
3. Implement right-click context menu on items (if client supports)

## Notes

- Loot window fading is acceptable (weight display useful when looting)
- Zeal client's "Fast Item Destroy" complements this feature
- Current 4-column layout is optimal for item visibility
- Workflow improvements benefit all players (raid looting, camp cleanup)
- Weight display prevents embarrassing over-encumbrance during raids

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Standards](../STANDARDS.md)
