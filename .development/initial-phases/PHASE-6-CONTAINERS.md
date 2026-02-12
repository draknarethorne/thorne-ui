[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 6: Container Window Investigation

**Status**: RESEARCHED  
**Priority**: Medium  
**Last Updated**: February 1, 2026

## Problem Statement

Bags close automatically when zoning, requiring players to repeatedly re-open containers. Users have requested either:
1. A consolidated "all bags expanded" window (like bank window), OR
2. A sizable container with dynamic column layout (1-4 columns based on width)

---

## Research Findings

### Container/Bag EQType Architecture

- **Inventory Bags**: EQTypes 30-39 (10 slots for currently-open container only)
- **Bank Bags**: EQTypes 2030-2039 (Bag 0 expanded), 2040-2049 (Bag 1), continuing pattern
- **Key Limitation**: Inventory bags have NO equivalent expanded EQTypes like bank
- **Client Constraint**: Only currently-open bag contents exposed via EQTypes 30-39

### Zeal Client Extensions

- Zeal provides camera, map, nameplate, floating damage features
- **No Zeal container extensions found** - no EQUI_Container.xml in zeal folder
- **No Zeal merchant extensions** - EQTypes 6000-6079 are standard merchant slots (not Zeal-specific)
- Zeal does NOT extend container or merchant EQType ranges

### SIDL Dynamic Layout Capabilities

- **Anchor Properties**: TopAnchorToTop, BottomAnchorToTop, LeftAnchorToLeft, RightAnchorToLeft with Offset
- **AutoStretch**: Boolean for element auto-sizing when parent resizes
- **Style_Sizable**: Boolean for user-resizable windows
- **Critical Limitation**: NO conditional logic or scripting in SIDL XML
- **Fixed Positioning**: Slots have hardcoded X,Y coordinates that cannot auto-reflow

---

## What is NOT Possible (Without Client Modification)

❌ **Consolidated "All Bags" Window**
- Requires dedicated EQTypes per bag slot (like bank's 2030-2079+ pattern)
- Inventory bags only expose currently-open bag via EQTypes 30-39
- Cannot display multiple bag contents simultaneously

❌ **Dynamic Column Reflow**
- Cannot automatically reposition slots from 2-column → 3-column → 4-column based on window width
- SIDL lacks conditional visibility or scripting logic
- Anchor properties only maintain offsets from edges, don't trigger layout changes

❌ **Client-Side Persistent Bags**
- Bags closing on zone is client behavior, not UI-controllable
- Fading behavior is client-enforced for container windows

---

## What IS Possible (Within SIDL Constraints)

✅ **Sizable Container Window**
```xml
<Style_Sizable>true</Style_Sizable>
```
Window can be resized by user, but slot positions remain fixed.

✅ **Fixed Multi-Column Layouts**
- Create static 3-column or 4-column grid layouts
- Slots positioned at fixed X coordinates (e.g., X=7, 46, 85, 124 for 4-column)
- More horizontal space utilization without scrolling

✅ **Responsive Buttons with Anchors**
- Buttons (Combine, Done) can use AutoStretch + anchors to maintain position when window resizes
- Already implemented in current thorne_drak/EQUI_Container.xml

---

## Recommended Solution

### Fixed 4-Column Sizable Container

**Implementation Status**: NOT YET IMPLEMENTED

**Proposed Changes**:
1. Set `Style_Sizable=true` on ContainerWindow Screen
2. Reposition 10 slots in 4-column grid:
   - Column 1: X=7 (Slots 1, 5, 9)
   - Column 2: X=46 (Slots 2, 6, 10)
   - Column 3: X=85 (Slots 3, 7)
   - Column 4: X=124 (Slots 4, 8)
3. Adjust window Size to accommodate 4 columns (minimum width ~170px)
4. Maintain existing anchors on Combine/Done buttons

**Advantages**:
- All 10 slots visible without scrolling
- User can resize window to preference
- Single file to maintain
- Works within SIDL constraints
- Addresses "bags closing on zone" pain point by reducing clicks needed

**Limitations**:
- Not truly "dynamic" (slots don't reflow based on width)
- Fixed 4-column layout regardless of window size
- Minimum width required to prevent slot overlap

**Implementation Approach**:
Create container variant in Options/Container folder (similar to Merchant variants pattern), allowing users to choose preferred layout manually. Current implementation remains 2-column standard.

---

## Technical Notes

### Current Container State (thorne_drak/EQUI_Container.xml)

- Style_Sizable: false (can be changed to true)
- AutoStretch: true (already configured)
- Combine button: Full anchor framework implemented
- Layout: 2-column (X=7, 46)
- Contains AugmentList listbox with DrawTemplate=WDT_Inner

### Fading Behavior

- Container windows participate in client-controlled transparency/fading
- Cannot be made non-fadeable via UI XML alone
- Workaround: `/viewport` positioning and `Alt+Shift+T` global transparency control

---

## Future Considerations

### Potential Client Modifications (External to UI Work)

If P2002/Zeal client team adds container enhancements:
- **Expanded EQTypes**: Container slots exposed like bank (30-39, 40-49, 50-59, etc.)
- **Persistence API**: UI-controllable bag open/close state across zones
- **Dynamic Layout Events**: Callback/event system for window resize triggers

### Options Variant Strategy

When implementing 4-column variant:
- Create `Options/Container/4-Column/EQUI_Container.xml`
- Document variant in README.md
- Preserve 2-column standard in main directory
- Allow user choice via file copy workflow

---

## Success Criteria (If Implemented)

- ✅ 4-column layout displays all 10 slots without scrolling
- ✅ Window is user-resizable (Style_Sizable=true)
- ✅ Combine and Done buttons maintain proper positioning via anchors
- ✅ Minimum width prevents slot overlap
- ✅ Options variant documented and tested
- ✅ No regression in combine functionality or slot interactions

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Technical References](../technical/eqtypes.md)
