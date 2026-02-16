[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 5: Target Window Enhancements

**Status**: ✅ COMPLETE  
**Priority**: Medium  
**Completion Date**: February 1, 2026

## Implementation Summary

**What Was Implemented:**
1. Created separate `EQUI_TargetOfTargetWindow.xml` for ToT display (Zeal client)
2. Added Target Level and Class display to Target Window
3. Compact design maintaining thorne UI aesthetic

**Key Discovery:** ToT (Target of Target) requires a **separate window file** (`EQUI_TargetOfTargetWindow.xml`) - EQType 27/120 cannot be embedded in TargetWindow. Additionally, **EQUI.xml must be created/modified** to include the ToT window file, as the default EQUI.xml does not reference it.

## Final Implementation

### Target Window (EQUI_TargetWindow.xml)

**Window Specifications:**
- Size: 260×60 pixels (increased from 50px to 60px)
- Layout: Player HP/Mana at top, target casting gauge, level/class info at bottom
- Components:
  - Y=0-15: Player HP/Mana display (EQTypes 70, 80)
  - Y=1-40: Target casting gauge with HP% (EQType 29)
  - Y=42-57: **NEW** Target Level (EQType 2) and Class (EQType 3) display

**New Features:**
- Target level display for quick con checking
- Target class display for PvP/raid awareness  
- Compact layout - only 10px height increase from original

### Target of Target Window (EQUI_TargetOfTargetWindow.xml)

**Window Specifications:**
- Size: 182×18 pixels (ultra-compact)
- Position: Default X=516, Y=319 (below target window)
- Frameless design (WDT_RoundedNoTitle)
- Components:
  - ToT HP Gauge (EQType 27 - Zeal required)
  - ToT HP Label (EQType 120 - Zeal required)
  - "ToT:" prefix label

**Design Notes:**
- Matches thorne UI red HP gauge colors (255,100,100 fill)
- Transparent gauge background for clean look
- Single-row compact design
- Independent window - can be positioned/hidden separately

## Objectives - Completed

- Add Target of Target (ToT) display for improved raid awareness
- Enhance target information display (level, class, guild, HP%)
- Improve visual hierarchy and readability
- Maintain compact footprint while adding functionality

## Planned Enhancements

### Target of Target (ToT) Display

- Show who/what your target is currently targeting
- Essential for raid awareness (is boss targeting MT or someone else?)
- **EQType 27**: Target of Target HP Gauge (Zeal client required)
- Potential layout: Small ToT gauge below main target HP

### Enhanced Target Info

Current default/duxaUI implementations show:
- Target name (typically in title bar or overlaid on gauge)
- Target HP percentage (EQType 29 as Label)
- Target HP gauge (EQType 6 as Gauge)

**Potential additions**:
- Target's target (ToT) - EQType 27 (Zeal-only)
- Guild affiliation display for PvP awareness
- HP percentage display (numeric - EQType 29)
- Class icon or text indicator (if EQType available)
- Level display with color coding (con colors)

### Layout Improvements

**Current thorne_drak implementation**:
- Window size: 124×50 px
- Style_Transparent: true (frameless design)
- Custom TargetBox.tga texture for background
- HP gauge at X=3, Y=0, Size=108×24
- Compact design with minimal chrome

**Planned improvements**:
- Add ToT gauge below main target (would increase window height to ~75-80px)
- Reorganize elements for better visual hierarchy
- Consider gauge templates matching Player window style (15px tall gauges)
- Ensure ToT display doesn't clutter main target info
- Maintain consistent color scheme with rest of UI

## Research Findings

### Current Target Window Implementations

**default/EQUI_TargetWindow.xml**:
- Simple 124×50 window with single HP gauge (EQType 6)
- HP percentage label (EQType 29)
- Minimal design, no ToT

**duxaUI/EQUI_TargetWindow.xml**:
- Similar minimalist approach (124×50)
- Single HP gauge with percentage display
- Uses custom TargetBox.tga texture
- No ToT implementation

**thorne_drak/EQUI_TargetWindow.xml** (current):
- Enhanced with Player HP/Mana display at top (EQTypes 70, 80)
- Target HP gauge below (EQType 6)
- Window size: 232×50 (wider to accommodate player stats)
- Style_Transparent: true (frameless)
- Custom gauge styling matching thorne UI aesthetic
- **No ToT currently implemented**

### Available EQTypes for Target Window

| EQType | Data Field | Element Type | Notes |
|--------|------------|--------------|-------|
| 6 | Target HP | Gauge | Primary target health gauge |
| 27 | Target of Target HP | Gauge | **Zeal client required** |
| 29 | Target HP % | Label | Numeric percentage display |
| 1 | Target Name | Label | Character/NPC name (context-dependent) |

**Missing EQTypes** (not available in P2002 client):
- Target Level (would need confirmation if available)
- Target Class (likely not exposed)
- Target Guild (likely not exposed)

### Zeal Client Dependency

**EQType 27** (ToT HP Gauge) requires:
- Zeal client with ToT features enabled
- Will display 0% or empty if using vanilla P2002 client
- Consider graceful degradation (ToT visible only when data available)

## Constraints

- Must remain non-fadeable (TargetWindow is safe from client fading)
- Cannot script conditional logic (SIDL limitation)
- Limited by available EQTypes for target information
- EQType 27 (ToT) only works with Zeal client
- Must maintain compact footprint for screen real estate
- Style_Transparent design requires careful layering of elements

## Implementation Plan

### Phase 5.1: Research & Planning
- ✅ Document current target window implementations
- ✅ Identify available EQTypes for target data
- ✅ Confirm Zeal client requirement for ToT (EQType 27)
- [ ] Design mockup for enhanced target window layout

### Phase 5.2: Basic ToT Integration
- [ ] Add ToT gauge (EQType 27) below main target HP
- [ ] Increase window height to accommodate ToT (75-80px)
- [ ] Add "ToT:" label for clarity
- [ ] Style ToT gauge to match player window aesthetic
- [ ] Test with Zeal client and vanilla client

### Phase 5.3: Enhanced Information Display
- [ ] Add target HP percentage display (EQType 29)
- [ ] Position percentage next to or below HP gauge
- [ ] Ensure text is readable against gauge background
- [ ] Consider adding target name display if space permits

### Phase 5.4: Visual Refinement
- [ ] Apply gauge templates matching Player window (15px tall)
- [ ] Ensure color consistency with thorne UI theme
- [ ] Optimize spacing and alignment
- [ ] Update TargetBox.tga texture if needed
- [ ] Test with various target types (players, NPCs, bosses)

## Success Criteria

- ✅ ToT display functional and clearly visible (Zeal client)
- ✅ Enhanced target info improves situational awareness
- ✅ Layout maintains compact footprint (~75-80px height max)
- ✅ Visual consistency with Player/Group windows
- ✅ Tested in raid scenarios for usability
- ✅ Graceful degradation on vanilla client (no errors)
- ✅ No interference with targeting mechanics

## Notes

- Target window does NOT fade (safe for critical UI elements)
- Consider future integration with Group window (unified design language)
- ToT feature primarily benefits tanks and raid leaders
- Compact design philosophy: prioritize essential information only

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Standards](../../.docs/STANDARDS.md)
