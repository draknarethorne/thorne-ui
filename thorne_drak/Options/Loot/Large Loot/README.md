# Loot Window - Large Loot Variant

**File**: [EQUI_LootWnd.xml](./EQUI_LootWnd.xml)  
**Version**: 1.1.0  
**Last Updated**: January 27, 2026  
**Status**: ✅ Fixed - Optimized 5-Column Grid Layout  
**Author**: Draknare Thorne

---
## Purpose

The Large Loot variant provides an optimized looting interface for corpses with many items. Instead of the default 2-column layout, this variant uses a **5-column grid** design allowing players to see more items at once (20 visible slots) while maintaining accessibility and Zeal compatibility.

**Key Features**:

- **5-Column Grid Layout**: 5 items wide vs default 2-column (more items visible at once)
- **4-Row Visible Area**: Shows 20 items before scrolling required
- **Large Slots**: 45×45px per item for easier clicking
- **Compact Spacing**: 5px horizontal, 2px vertical gaps (optimized for visibility)
- **Zeal Button Set**: Includes Loot All, Link All, and Done buttons
- **Auto-Anchoring**: Scrollable area adjusts with window resizing
- **Corpse Header**: Centered corpse name at top for context

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 271 × 304 pixels (sizable, resizable) |
| **Layout Type** | Grid-based item display (5 columns × 6 rows) |
| **Visible Grid** | 4 rows × 5 columns = 20 items (scroll for more) |
| **Slot Size** | 45 × 45 pixels per item |
| **Total Slots** | 30 items max (EQTypes 5000-5029) |
| **Column Spacing** | 5px horizontal |
| **Row Spacing** | 2px vertical |
| **Scrollable** | Yes (auto-scroll for rows 5-6) |
| **Button Count** | 3 (Loot All, Link All, Done) |
| **Titlebar** | Hidden (WDT_RoundedNoTitle) |
| **Resizable** | Yes |

---

## Snapshot

- Window size: **271 × 304** (sizable) — ✅ FIXED: Optimized for 4×5 grid (4 rows visible)
- Layout: **5-column item grid** (5 items wide, 4 rows visible with scrolling)
- Item slot size: **45 × 45** per slot
- Spacing: **5px horizontal, 2px vertical** (tighter than original, similar to default)
- Corpse name: Top-centered at **Y=2**, full width (271px)
- Scrollable area: **Auto-stretch** with anchoring (TopAnchorOffset=22, BottomAnchorOffset=28)
- Buttons: **3 buttons** at bottom at **Y=258** - Loot All (X=4), Link All (X=84), Done (X=184)
- Features: Zeal-compatible buttons (Loot All, Link All in addition to Done)
- Visible slots: **20 slots** (4 rows × 5 columns), scroll for remaining 10 slots

### Current Coordinates

| Element | X | Y | Size (CX×CY) | Notes |
| --- | --- | --- | --- | --- |
| **Window** | 0 | 25 | 271×304 | WDT_RoundedNoTitle, sizable (+8px for scrollbar) |
| **Corpse Name** | 0 | 2 | 271×18 | Full width, centered text |
| **LW_LootInvWnd** | — | — | Auto-stretch | Scroll area with anchors |
| **Item Slots (grid)** | — | — | 45×45 each | 5 columns, 30 total (20 visible, 5px H-gap, 2px V-gap) |
| **Loot All Button** | 4 | 258 | 75×20 | Left button |
| **Link All Button** | 84 | 258 | 75×20 | Center button |
| **Done Button** | 184 | 258 | 75×20 | Right button (4px from right edge) |

### Item Grid Layout (5-column pattern)

**Row 0 (Y=5):** — Visible
- Slot 0: X=5, Y=5
- Slot 1: X=55, Y=5
- Slot 2: X=105, Y=5
- Slot 3: X=155, Y=5
- Slot 4: X=205, Y=5

**Row 1 (Y=52):** — Visible
- Slot 5: X=5, Y=52
- Slot 6: X=55, Y=52
- Slot 7: X=105, Y=52
- Slot 8: X=155, Y=52
- Slot 9: X=205, Y=52

**Row 2 (Y=99):** — Visible
**Row 3 (Y=146):** — Visible
**Rows 4-5 (Y=193, Y=240):** — Scroll to view

**Pattern**:
- **Column spacing**: 5px horizontal gap (matching default)
- **Row spacing**: 2px vertical gap (tighter than original 12px)
- **Total slots**: 30 (LW_LootSlot0 through LW_LootSlot29)
- **Visible slots**: 20 (rows 0-3, requiring scroll for rows 4-5)
- **EQTypes**: 5000-5029
- **Content width**: 255px (5 margin + 5×45 slots + 4×5 gaps + 5 margin)
- **Total width**: 263px (255px content + 8px scrollbar)

### Anchoring System

```xml
<AutoStretch>true</AutoStretch>
<LeftAnchorOffset>0</LeftAnchorOffset>
<TopAnchorOffset>22</TopAnchorOffset>
<RightAnchorOffset>0</RightAnchorOffset>
<BottomAnchorOffset>28</BottomAnchorOffset>
```

- **TopAnchorOffset=22**: Positions scroll area below corpse name (2px Y + 18px height + ~2px spacing)
- **BottomAnchorOffset=28**: Reserves space for buttons at bottom (20px height + spacing)
- **Auto-stretch**: Allows window to resize while maintaining proper spacing

### Quick Layout Sketch

```
┌──────────────────────────────────┐
│     Corpse Name (centered)       │ Y=2
├──────────────────────────────────┤
│ ┌──────────────────────────────┐ │
│ │ [0] [1] [2] [3] [4]          │ │ Y=5 (row 0, visible)
│ │ [5] [6] [7] [8] [9]          │ │ Y=52 (row 1, visible)
│ │ [10][11][12][13][14]         │ │ Y=99 (row 2, visible)
│ │ [15][16][17][18][19]         │ │ Y=146 (row 3, visible)
│ │ ─ scroll for rows 4-5 ─      │ │ (5px H-gap, 2px V-gap)
│ └──────────────────────────────┘ │
│ [Loot All][Link All]     [Done]  │ Y=258
└──────────────────────────────────┘
                                     Width: 271px
```

## Behavior Notes

- **Scrollable Content**: LW_LootInvWnd uses vertical scrolling with AutoStretch to accommodate all 30 slots
- **VirtualSize**: Calculated automatically based on slot grid (would be ~456px tall for 8 rows × 57px)
- **Button Spacing**: Loot All (X=4), Link All (X=84), Done (X=184 - right-anchored with 4px margin)
- **Style_Sizable**: Window can be resized by user; anchoring maintains proper layout proportions
- **Zeal Integration**: Link All and Loot All buttons provide enhanced functionality for Zeal client

## Window Sizing Calculation

**Width (271px):**
- Left margin: 5px
- 5 columns × 45px = 225px
- Column gaps: 4 × 5px = 20px
- Right margin: 5px
- Scrollbar: ~8px
- Content: 255px (5 + 225 + 20 + 5)
- **Total**: 271px (content + scrollbar)

**Height (304px):**
- Titlebar: ~16px (title area)
- Corpse name: ~20px (label at Y=2)
- Scroll area: ~230px (4 visible rows + spacing)
- Button area: ~28px (buttons + margin)
- Extra spacing: ~10px
- **Total**: 304px (ensures 4 rows visible with scrolling for remaining slots)


## Issues Fixed (January 27, 2026)

**Before:**

- Corpse name positioned at X=210, Y=180 (middle of window, not visible)
- Window size 315×500px (arbitrary, too large)
- Buttons at Y=464 with inconsistent spacing (X=7, 116, 225)
- Scroll area used fixed Size instead of AutoStretch anchoring
- No proper relationship between window components

**After:**

- Corpse name at top (Y=2, full width, centered)
- Window size 271×304px (optimized for 4-row visible 5-column grid with titlebar clearance)
- Buttons spaced at bottom (Y=258): Loot All (X=4), Link All (X=84), Done (X=184 - right-anchored)
- Scroll area uses AutoStretch with proper TopAnchorOffset/BottomAnchorOffset
- Clean separation: header → scrollable items → action buttons
- Tight spacing: 5px horizontal, 2px vertical gaps (matching default standards)


## Changelog

- **Feb 1, 2026** — Final refinements: increased window to 271×304px, moved buttons to Y=258, anchored Done button to right at X=184 (4px margin), tightened slot spacing to 5px H / 2px V (matching default standards).
- **Jan 27, 2026** — Complete layout overhaul: fixed corpse name positioning, corrected window size, repositioned buttons with proper spacing, added AutoStretch anchoring to scroll area.
- **May 24, 2025** — Initial implementation by Brujoloco: Modified Calmethar loot window with Zeal Loot/Link All buttons.

## What we borrowed

- **Calmethar UI**: Base loot window structure and scrolling mechanics
- **Zeal Client**: Loot All and Link All button functionality
- **thorne_drak patterns**: Button styling (A_BtnNormal/Pressed/Flyby templates), rounded window frame (WDT_RoundedNoTitle)
- **default**: Item slot EQTypes (5000-5029) and grid positioning concept

## Next thoughts

- Consider adding item count indicator or total weight display
- Potential currency display area if Zeal exposes loot gold/platinum
- Alternative layout option: 3-column for wider items visualization
- Optional: platinum/gold/silver/copper readout in corpse name area

---

## Technical Reference

### Item Slot Template

```xml
<InvSlot item="LW_LootSlot0">
    <ScreenID>LW_LootSlot0</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>10</X>
        <Y>5</Y>
    </Location>
    <Size>
        <CX>45</CX>
        <CY>45</CY>
    </Size>
    <Background>A_RecessedBox</Background>
    <EQType>5000</EQType>
    <ItemOffsetX>2</ItemOffsetX>
    <ItemOffsetY>2</ItemOffsetY>
</InvSlot>
```

### Button Template

```xml
<Button item="LW_LootAllButton">
    <ScreenID>LootAllButton</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>4</X>
        <Y>295</Y>
    </Location>
    <Size>
        <CX>75</CX>
        <CY>20</CY>
    </Size>
    <Text>Loot All</Text>
    <ButtonDrawTemplate>
        <Normal>A_BtnNormal</Normal>
        <Pressed>A_BtnPressed</Pressed>
        <Flyby>A_BtnFlyby</Flyby>
        <Disabled>A_BtnDisabled</Disabled>
        <PressedFlyby>A_BtnPressedFlyby</PressedFlyby>
    </ButtonDrawTemplate>
</Button>
```

### Scroll Area Configuration

```xml
<Screen item="LW_LootInvWnd">
    <ScreenID>LootInvWnd</ScreenID>
    <RelativePosition>true</RelativePosition>
    <AutoStretch>true</AutoStretch>
    <LeftAnchorOffset>0</LeftAnchorOffset>
    <TopAnchorOffset>22</TopAnchorOffset>
    <RightAnchorOffset>0</RightAnchorOffset>
    <BottomAnchorOffset>28</BottomAnchorOffset>
    <RightAnchorToLeft>false</RightAnchorToLeft>
    <BottomAnchorToTop>false</BottomAnchorToTop>
    <Style_VScroll>true</Style_VScroll>
    <Style_Transparent>true</Style_Transparent>
    <DrawTemplate>WDT_Inner</DrawTemplate>
    <!-- Pieces: LW_LootSlot0 through LW_LootSlot29 -->
</Screen>
```
