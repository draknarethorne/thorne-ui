# Phase 6: Inventory & Window Enhancements (v0.6.0)

**Status:** In Progress  
**Started:** February 3, 2026  
**Target Release:** v0.6.0  
**Branch:** feature/v0.6.0-inventory-and-windows

**Quick Links:** [Development Guide](../../DEVELOPMENT.md) | [Standards](../STANDARDS.md) | [TODO](../../TODO.md)

---

## 🎯 Phase Overview

This phase focuses on comprehensive inventory window improvements, title bar standardization, and experimental quality-of-life features to enhance the overall UI experience.

**Key Objectives:**
1. **Target Window Enhancement** - Add player weight display (experimental)
2. **Loot Window Enhancement** - Add destroy button functionality (experimental)
3. **Title Bar Standardization** - Replace WDT_DEF with custom rounded title bars
4. **Inventory Window Overhaul** - Complete redesign with logical grouping
5. **Minor Cleanup** - Address accumulated quick-hit items

---

## 📋 Work Items

### 1. Target Window - Weight Display (Experimental)

**Goal:** Test adding player current/max weight between HP and mana gauges.

**Requirements:**
- Weight display format: `999/999` (cur/max)
- Font size: Match player window HP/Mana fields
- Position: Centered in middle area between HP and Mana
- Vertical adjustment: Down slightly from default center

**Files to Modify:**
- `thorne_drak/EQUI_TargetWindow.xml`

**EQTypes:**
- Current Weight: EQType 24
- Max Weight: EQType 25

**Implementation Notes:**
- This is a test feature - may or may not be included in final release
- Need to verify layout doesn't feel cluttered
- Consider if this duplicates information already visible in Player window

**Testing Checklist:**
- [ ] Weight values display correctly
- [ ] Font size matches Player window
- [ ] Position feels balanced
- [ ] Doesn't interfere with target name/level/class
- [ ] In-game usability test

---

### 2. Loot Window - Destroy Button (Experimental)

**Goal:** Add a destroy button to loot window for quick item deletion.

**Requirements:**
- Button similar to Inventory window destroy button
- Check if destroy functionality works on loot items
- Position logically within existing loot window layout

**Files to Modify:**
- `thorne_drak/EQUI_LootWnd.xml`
- Potentially: `thorne_drak/Options/Loot/Standard/EQUI_LootWnd.xml`

**Implementation Notes:**
- **Experimental** - May not work due to client limitations
- If functional, could be a significant QoL improvement
- Research: Does EQ client allow destroy from loot context?
- Fallback: Document limitation if not functional

**Testing Checklist:**
- [ ] Button appears in correct location
- [ ] Button visual style matches window
- [ ] Destroy functionality works on looted items
- [ ] No crashes or errors when used
- [ ] Tooltip displays correctly

---

### 3. Title Bar Standardization

**Goal:** Replace all WDT_DEF title bar definitions with custom rounded variants.

**Current State:**
- Many windows use default `WDT_DEF` title bar
- Some windows have custom title bars
- Inconsistent visual appearance across UI

**Target State:**
- All windows use custom rounded title bar design
- Two variants:
  1. **With Title Bar** - Windows that need close button and title text
  2. **Without Title Bar** - Frameless windows with drag affordance only

**Files to Audit:**
- All `EQUI_*.xml` files in `thorne_drak/`
- Check for `WDT_DEF` references
- Replace with custom title bar definition

**Custom Title Bar Specifications:**
```xml
<!-- Rounded Title Bar Template - TO BE DEFINED -->
<!-- Review existing custom title bars for style -->
<!-- Ensure consistent styling across all windows -->
```

**Implementation Steps:**
1. [ ] Audit all XML files for WDT_DEF usage
2. [ ] Define standard rounded title bar template
3. [ ] Create variant for windows without close button
4. [ ] Document in STANDARDS.md
5. [ ] Apply to all windows systematically
6. [ ] Test each window for proper display

**Testing Checklist:**
- [ ] All windows display consistent title bar style
- [ ] Close buttons work where present
- [ ] Window dragging works correctly
- [ ] Rounded corners render properly
- [ ] No visual artifacts or overlap issues

---

### 4. Inventory Window Overhaul

**Goal:** Complete redesign with logical grouping, AA gauge, and improved layout.

**Scope:**

#### A. Armor & Weapon Alignment
**Current Issues:**
- Armor slots not logically grouped
- Weapons mixed with armor
- Inconsistent spacing

**Target Layout:**
- Logical grouping: Head → Feet sequence
- Clear visual separation of armor vs weapons
- Consistent slot spacing

**Implementation:**
- [ ] Design new armor layout (sketch/mockup)
- [ ] Group equipment by body region
- [ ] Separate primary/secondary weapons
- [ ] Update slot positions in XML
- [ ] Test alignment and spacing

#### B. Bag Slot Organization
**Current Issues:**
- Bags positioned inconsistently
- Relationship to armor unclear

**Target Layout:**
- Logical bag positioning relative to armor
- Clear visual hierarchy
- Easy access to all 8 bag slots

**Implementation:**
- [ ] Determine optimal bag slot locations
- [ ] Adjust positions relative to new armor layout
- [ ] Ensure proper spacing
- [ ] Test bag opening/closing

#### C. AA Gauge & Display
**Goal:** Add AA experience gauge and current/max AA display near XP gauge.

**Requirements:**
- Position: Near existing XP gauge
- Format: Gauge + `999/999` (cur/max) display
- EQTypes:
  - Current AA: EQType 36
  - Max AA: EQType 37
  - AA Gauge: (Research EQType for AA XP progress)

**Implementation:**
- [ ] Research AA gauge EQType
- [ ] Design gauge visual style
- [ ] Position gauge near XP gauge
- [ ] Add cur/max text labels
- [ ] Test with various AA levels
- [ ] Verify gauge fills correctly

#### D. Sub-Windows
**Goal:** Create logical sub-sections within inventory window.

**Potential Sub-Windows:**
- Character stats cluster
- Equipment/armor section
- Bag management section
- Currency/platinum display

**Implementation:**
- [ ] Define sub-window boundaries
- [ ] Create visual separation (borders, backgrounds)
- [ ] Group related elements
- [ ] Test readability and usability

#### E. Other Cleanup Items
- [ ] Standardize field spacing across inventory
- [ ] Align text labels consistently
- [ ] Update colors to match current palette
- [ ] Add tooltips where helpful
- [ ] Review button sizing uniformity

**Files to Modify:**
- `thorne_drak/EQUI_InventoryWindow.xml`

**Testing Checklist:**
- [ ] All armor slots functional
- [ ] Bag slots open/close properly
- [ ] AA gauge displays correctly
- [ ] Layout feels balanced and organized
- [ ] No overlap or visual artifacts
- [ ] Extensive in-game testing

---

### 5. Minor Cleanup Items

**From TODO.md Quick Wins:**

- [ ] Check button sizing uniformity across windows
- [ ] Review window border spacing standards (2px/4px consistency)
- [ ] Test F2-F6 keyboard label positioning on group window
- [ ] Color palette consistency check
- [ ] Performance optimization opportunities

**Additional Items:**
- [ ] Update any outdated documentation
- [ ] Add attribution headers if missing
- [ ] Verify all Options variants still work

---

## 🔬 Experimental Features Note

**Important:** Items marked "experimental" may not be included in final v0.6.0 release.

**Decision Criteria:**
1. **Functionality** - Does it work as intended?
2. **Usability** - Does it improve player experience?
3. **Stability** - Any bugs or edge cases?
4. **Visual Cohesion** - Fits with overall UI design?

**Experimental Items:**
- Target Window weight display
- Loot Window destroy button

**Process:**
1. Implement and test thoroughly
2. Use in-game for several days
3. Evaluate based on criteria above
4. Document decision in phase notes
5. Either commit to release or remove before v0.6.0 tag

---

## 📐 Design Standards

### Title Bar Specifications

**To Be Defined:**
- Rounded corner radius
- Background color/texture
- Title text font and size
- Close button position and style
- Drag affordance for frameless windows

**Documentation:**
- Update `.docs/STANDARDS.md` with title bar specs
- Include example XML for both variants
- Add visual mockup/screenshot

### Inventory Layout Principles

**Guiding Principles:**
1. **Logical Grouping** - Related items together
2. **Visual Hierarchy** - Important info prominent
3. **Consistent Spacing** - Standard margins/padding
4. **Accessibility** - Easy target sizes for clicks
5. **Information Density** - Balance detail vs clarity

---

## 🧪 Testing Strategy

### Unit Testing (Per Feature)
- Test each feature individually
- Verify XML syntax
- Check EQType bindings
- Test visual rendering

### Integration Testing
- Test features together
- Check for layout conflicts
- Verify window stacking
- Test with various screen resolutions

### In-Game Testing
- Use modified windows in actual gameplay
- Test all interactions (clicks, drags, etc.)
- Verify with full/empty inventory
- Test with different character classes
- Multiple play sessions to identify issues

### Performance Testing
- Check for UI lag
- Monitor memory usage
- Test with multiple windows open
- Verify no frame rate impact

---

## 📊 Success Metrics

**Target Completion:**
- [ ] All experimental features tested and evaluated
- [ ] Title bars standardized across all windows
- [ ] Inventory window redesigned and functional
- [ ] All cleanup items addressed
- [ ] Documentation updated
- [ ] In-game testing completed
- [ ] Options variants verified

**Quality Metrics:**
- Zero XML syntax errors
- No visual artifacts or overlaps
- Consistent styling across all windows
- Positive in-game usability feedback
- No performance degradation

---

## 🚀 Release Decision

**Before Tagging v0.6.0:**

1. **Review experimental features:**
   - Keep or remove target window weight?
   - Keep or remove loot window destroy button?
   - Document decisions in release notes

2. **Verify completeness:**
   - All planned features implemented or explicitly deferred
   - Documentation updated
   - Testing completed
   - No known bugs

3. **Prepare release notes:**
   - List all changes
   - Document any breaking changes
   - Note experimental features included
   - Provide migration guidance if needed

---

## 📝 Notes & Discoveries

*(Document findings, challenges, and decisions made during development)*

### Research Findings
- *To be filled in during development*

### Design Decisions
- *Document why certain approaches were chosen*

### Technical Challenges
- *Note any unexpected issues encountered*

### Future Considerations
- *Ideas for future phases*

---

**Maintainer:** Draknare Thorne  
**Phase Start:** February 3, 2026  
**Estimated Duration:** TBD based on scope
