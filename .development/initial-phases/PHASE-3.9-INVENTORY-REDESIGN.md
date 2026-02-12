[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 3.9: Inventory Window Character Sheet Redesign

**Status**: PLANNED  
**Priority**: High (Core window transformation)  
**Target Completion**: February 2026

## Vision

Transform the Inventory window from a simple equipment/storage interface into a comprehensive **character sheet** that serves as the primary hub for viewing character state, equipped gear, stats, and progression.

---

## Design Objectives

### Primary Goals

1. **Add Character Stats Display**: Integrate AC, ATK, resistances, and other key stats directly into Inventory window
2. **Add AA Gauge**: Display Alternate Advancement progress alongside standard XP gauge
3. **Anatomical Equipment Layout**: Reorganize equipment slots to mirror natural character anatomy (head-to-toe, left-to-right)
4. **Three-Zone Layout**: Create distinct visual zones for class identity (left), equipped gear (center), and character stats (right)
5. **Cross-Window Consistency**: Standardize equipment slot sequence across ALL windows displaying inventory (Inventory, Actions, Hotbar)
6. **Optimized Window Dimensions**: Resize and reorganize window to accommodate new layout efficiently

### Secondary Goals

- Make Inventory window feel like a "character window" rather than just storage
- Improve visual hierarchy and information scanning
- Reduce cognitive load when checking character state
- Maintain or improve current bag slot accessibility

---

## Equipment Slot Anatomical Layout

### Inspiration

DuxaUI's anatomical 3-column grid pattern (see `duxaUI/EQUI_Inventory.xml`)

### Proposed Layout Pattern (Head-to-Toe, Left-to-Right)

**Row 1 - HEAD LEVEL (Y=4)**:  
Position (X): `[47] [89] [131] [173] [215]`  
Equipment:   `[Left Ear] [Neck] [Face] [Head] [Right Ear]`  
EQTypes:     `[1] [5] [3] [2] [4]`

**Row 2 - ARM LEVEL (Y=47)**:  
Position (X): `[5] [47] [89] [131] [173] [215]`  
Equipment:   `[Left Ring] [Left Wrist] [Arms] [Hands] [Right Wrist] [Right Ring]`  
EQTypes:     `[15] [9] [7] [12] [10] [16]`

**Row 3 - TORSO LEVEL (Y=90)**:  
Position (X): `[5] [47] [89] [131] [173] [215]`  
Equipment:   `[Shoulders] [Chest] [Back] [Waist] [Legs] [Feet]`  
EQTypes:     `[6] [17] [8] [20] [18] [19]`

**Row 4 - WEAPONS LEVEL (Y=133)**:  
Position (X): `[89] [131] [173] [215]`  
Equipment:   `[Primary] [Secondary] [Range] [Ammo]`  
EQTypes:     `[13] [14] [11] [21]`

### Rationale

- Mirrors how a player naturally thinks about gear (top to bottom)
- Symmetric layout (left/right equipment mirrored around center)
- Logical grouping by body region
- Weapons at bottom separate from armor
- Standard 40x40px slot size, 42-43px horizontal spacing, 43px vertical spacing
- Equipment grid occupies center zone of window

### Current State for Comparison

Current thorne_drak/EQUI_Inventory.xml uses traditional EQ layout (slots 0-21 in default order), which doesn't create anatomical visual grouping.

---

## Three-Zone Layout Architecture

### Zone 1: LEFT - Character Identity & Info

**Position**: X=5, top-to-bottom  
**Implementation**: Inner `<Screen item="LeftZone">` container

**Contents**:
- **Class Animation** (Y=133): Visual character class representation (64x128px)
  - Displays race/class combination graphic
  - Tooltip: "Drop Item Here to Auto Equip"
  - Existing element to preserve
- **Player Information** (above class animation, Y=TBD):
  - Character name label
  - Level display
  - Class text
  - Deity (if space permits)
  - Potentially weight display (Current/Max)
  - Color-coded labels (Blue for attribute labels, White for values)
- **Done Button** (Y=298): Window close button (82x46px)

**Subwindow Pattern**:
```xml
<Screen item="IW_LeftZone">
    <ScreenID>IW_LeftZone</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location><X>5</X><Y>4</Y></Location>
    <Size><CX>87</CX><CY>340</CY></Size>
    <DrawTemplate>WDT_Inner</DrawTemplate>
    <Pieces>PlayerName PlayerLevel PlayerClass ClassAnim DoneButton</Pieces>
</Screen>
```

**Benefits**: Move entire left zone by changing single Location; create variants by swapping entire subwindow.

**Zone Constraints**:
- Width: ~82-87px (constrained by class animation + border)
- Must not interfere with equipment slots starting at X=47

---

### Zone 2: CENTER - Equipment Slots

**Position**: Starting X=47 (or adjusted based on left zone width)  
**Implementation**: Inner `<Screen item="EquipmentGrid">` container

**Contents**:
- **Equipment Grid**: All 21 worn equipment slots in anatomical layout (see above)
  - 4 rows of slots (head, arms, torso, weapons)
  - Symmetric arrangement around vertical centerline
  - 40x40px slots with consistent spacing
- **Currency Display** (below equipment, Y=176):
  - Platinum, Gold, Silver, Copper buttons
  - Traditional coin box layout
  - 82x22px per coin type
  - Potentially rearrange horizontally for width optimization

**Subwindow Pattern**:
```xml
<Screen item="IW_EquipmentGrid">
    <ScreenID>IW_EquipmentGrid</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location><X>47</X><Y>4</Y></Location>
    <Size><CX>260</CX><CY>270</CY></Size>
    <Pieces>InvSlot1 InvSlot2 ... InvSlot21 Money0 Money1 Money2 Money3</Pieces>
</Screen>
```

**Benefits**: All equipment slots use relative positioning within grid; move entire grid without recalculating 21 individual coordinates.

**Zone Constraints**:
- Width: ~260px (5 columns × 42px spacing + slot widths + margins)
- Height: ~173px for equipment grid + ~90px for currency = ~263px
- Centered horizontally in window

---

### Zone 3: RIGHT - Character Stats & Progression

**Position**: Right side of window, aligned with equipment grid  
**Implementation**: Two inner `<Screen>` containers (Stats + Progression)

**Contents**:

**Stats Display Subwindow**:
```xml
<Screen item="IW_StatsZone">
    <ScreenID>IW_StatsZone</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location><X>310</X><Y>4</Y></Location>
    <Size><CX>110</CX><CY>150</CY></Size>
    <Pieces>Label_AC Label_ATK Label_HP ... ResistPoison ResistDisease ...</Pieces>
</Screen>
```

- **Primary Stats**:
  - AC (Armor Class) - Orange label
  - ATK (Attack) - Orange label  
  - HP current/max - White or Rose label
  - Mana current/max - White or Rose label
- **Attributes** (if space permits):
  - STR, STA, AGI, DEX, WIS, INT, CHA
  - Blue labels, white values
  - 2-column layout to save vertical space
- **Resistances**:
  - Poison (Teal), Disease (Yellow), Fire (Orange), Cold (Cyan), Magic (Purple)
  - Single-line compact display or icon-based
- **Weight**:
  - Current / Max weight
  - Color change if approaching encumbrance limit

**Progression Display Subwindow** (below stats):
```xml
<Screen item="IW_ProgressionZone">
    <ScreenID>IW_ProgressionZone</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location><X>310</X><Y>160</Y></Location>
    <Size><CX>110</CX><CY>60</CY></Size>
    <Pieces>XPGauge XPLabel AAGauge AALabel</Pieces>
</Screen>
```

- **XP Gauge**: Standard experience progress bar
  - EQType 4 (Experience %)
  - Orange/green gauge
  - Numeric label showing % to next level
- **AA Gauge**: Alternate Advancement progress
  - EQType 5 (AA Experience %)
  - Yellow gauge
  - Numeric label showing AA % or points available
  - Aligned vertically with XP gauge (17px spacing)
  - Same width and styling as XP gauge for visual consistency

**Benefits**: Stats and progression are logically separated; can show/hide entire sections; easier to create stat-focused vs minimal variants.

**Zone Constraints**:
- Width: ~90-120px (sufficient for stat labels + values)
- Height: Must align with equipment grid top/bottom
- Right-aligned against window edge

---

## Bag Slots Configuration

### Decision Point

Single-row vs. double-row layout depends on final window width after three-zone layout implementation.

### Option A: Single Row (8 bags horizontal)

- **Requirements**: Window width ≥ 360px
- **Position**: Y=346 (below currency/XP gauges)
- **Layout**: All 8 bag slots (EQTypes 22-29) in single horizontal row
- **Spacing**: 42px horizontal spacing
- **Advantages**: Clean, reduces vertical window height
- **Disadvantages**: Wider window footprint

### Option B: Double Row (4 bags × 2 rows)

- **Requirements**: Window width ≥ 220px (allows narrower window)
- **Position**: Y=346 and Y=389 (two rows stacked)
- **Layout**: Bags 1-4 on top row, Bags 5-8 on bottom row
- **Spacing**: 42px horizontal, 43px vertical
- **Advantages**: Narrower window, more compact footprint
- **Disadvantages**: Taller window

**Current State**: thorne_drak uses 2-row bag layout  
**Recommendation**: Test both; choose based on overall window dimensions after layout implementation

---

## Cross-Window Equipment Sequence Alignment

### Problem

Equipment slots appear in multiple windows but with inconsistent ordering:
- **Inventory Window**: Traditional slot sequence (0-21)
- **Actions Window**: Partial equipment display (unknown current sequence)
- **Hotbar Window**: Inventory slot quick-access (unknown current sequence)

### Goal

Standardize equipment slot display sequence across ALL windows to match anatomical pattern

### Implementation Tasks

1. **Inventory Window** (Primary):
   - Implement full anatomical layout (Phase 3.9 core work)
   - Document canonical slot sequence
   - Create Options variants if needed

2. **Actions Window** (Alignment):
   - **Audit**: Identify which equipment slots are currently displayed
   - **Redesign**: Reorder slots to match Inventory anatomical sequence
   - **Visual Check**: Ensure slots appear in same relative positions as Inventory
   - **Test**: Verify intuitive scanning between Actions and Inventory windows

3. **Hotbar Window** (Alignment):
   - **Audit**: Document current inventory slot layout in hotbar tabs/pages
   - **Redesign**: Reorganize inventory slots to match anatomical pattern
   - **Sequence**: If showing partial equipment, use same left-to-right, top-to-bottom order
   - **Grouping**: Consider grouping slots by body region (head, arms, torso, weapons)

4. **Any Other Windows** (Discovery & Alignment):
   - **Audit**: Search for other windows displaying InvSlots (Inspect, Trade, etc.)
   - **Evaluate**: Determine if alignment needed (context-dependent)
   - **Implement**: Apply anatomical pattern where sensible

### Consistency Rules

- **Head slots**: Always appears top/first
- **Weapon slots**: Always appears bottom/last
- **Left-to-right**: Symmetric pairs (ears, wrists, rings) maintain left-before-right order
- **Top-to-bottom**: Head → Arms → Torso → Weapons

### Expected Benefit

Players develop muscle memory for slot positions, reducing time spent searching for specific equipment across different windows.

---

## Window Dimensions & Layout Integration

### Current Inventory Window (thorne_drak)

- **Size**: Unknown (to be measured)
- **Layout**: Traditional EQ 2-column equipment grid
- **Stats**: No stats displayed (stats in Actions window instead)
- **AA Gauge**: Not present

### Proposed New Dimensions (Estimated)

**Width Calculation**:
- Left zone: ~87px (class animation + margins)
- Center zone: ~260px (5-column equipment grid + spacing)
- Right zone: ~110px (stats + gauges)
- Borders/padding: ~20px
- **Total Width**: ~477px (or narrower if optimized)

**Height Calculation**:
- Title bar: ~18px
- Equipment grid: ~173px (4 rows × 43px spacing)
- Currency display: ~90px (4 rows of coins)
- XP/AA gauges: ~44px (2 gauges × 17px + spacing + labels)
- Bag slots: ~43px (single row) or ~86px (double row)
- Margins/spacing: ~40px
- **Total Height**: ~408px (single-row bags) or ~451px (double-row bags)

### Constraints

- Must fit on 800x600 minimum resolution (standard for P2002)
- Should not exceed ~500px width to leave room for other windows
- Bag slots must remain easily accessible (not buried at bottom)
- Stats zone must have sufficient space for readable text

### Layout Flexibility

- Exact dimensions TBD during implementation
- May require iterative adjustments to balance zones
- Options variants can explore different width/height ratios

---

## Implementation Phases

### Phase 3.9.1: Research & Planning

- [x] Document duxaUI anatomical layout pattern
- [ ] Measure current thorne_drak Inventory window dimensions
- [ ] Create mockup/wireframe of three-zone layout
- [ ] Calculate exact coordinates for all elements
- [ ] Decide bag slot configuration (1-row vs 2-row)
- [ ] Audit Actions and Hotbar windows for current equipment sequences

### Phase 3.9.2: Equipment Grid Redesign

- [ ] Reposition all 21 equipment slots to anatomical pattern
- [ ] Verify slot backgrounds (icons) match new positions
- [ ] Test slot spacing and alignment
- [ ] Ensure tooltips display correctly
- [ ] Validate drop-to-equip functionality

### Phase 3.9.3: Stats & Progression Integration

- [ ] Add right zone stat labels (AC, ATK, HP, Mana, Resistances, Weight)
- [ ] Position and style stat value labels (colors, fonts, alignment)
- [ ] Add XP gauge (existing EQType 4)
- [ ] Add AA gauge (EQType 5) with matching styling
- [ ] Align gauges vertically with 17px spacing
- [ ] Add AA numeric label (EQType 72 or 73 for unspent/percentage)

### Phase 3.9.4: Left Zone Character Info

- [ ] Preserve class animation positioning
- [ ] Add character name label (EQType 1)
- [ ] Add level display (EQType 2)
- [ ] Add class label (EQType 3)
- [ ] Add deity label (EQType 4, if space permits)
- [ ] Add weight display (EQTypes 24, 25)
- [ ] Adjust Done button position

### Phase 3.9.5: Window Resize & Polish

- [ ] Adjust overall window Size (width, height)
- [ ] Reposition currency buttons
- [ ] Configure bag slots (finalize 1-row or 2-row)
- [ ] Verify all elements fit within window bounds
- [ ] Test window positioning on 800x600 resolution
- [ ] Add/adjust borders, spacing, padding

### Phase 3.9.6: Cross-Window Alignment

- [ ] Audit Actions window equipment slot sequence
- [ ] Reorder Actions slots to match anatomical pattern
- [ ] Audit Hotbar inventory slot sequence
- [ ] Reorganize Hotbar slots to match anatomical pattern
- [ ] Document canonical sequence in DEVELOPMENT.md
- [ ] Create visual alignment test (open Inventory + Actions + Hotbar simultaneously)

### Phase 3.9.7: Options Variants

- [ ] Create Options/Inventory/Character Sheet variant (new layout)
- [ ] Create Options/Inventory/Standard variant (preserve current simple layout)
- [ ] Document differences between variants
- [ ] Test variant swapping functionality

### Phase 3.9.8: Testing & Validation

- [ ] Test all equipment slots (equip/unequip items)
- [ ] Verify stats update dynamically
- [ ] Test XP and AA gauges update correctly
- [ ] Test bag slots (open bags, close bags)
- [ ] Test currency display
- [ ] Test window resizing behavior (if Style_Sizable enabled)
- [ ] Test across different character classes
- [ ] Test across different screen resolutions (800x600, 1024x768, 1920x1080)

---

## Technical Considerations

### EQTypes Required

**Stats Display**:
- EQType 22 (Label): Armor Class (AC)
- EQType 23 (Label): Attack (ATK)
- EQType 18 (Label): Current HP
- EQType 19 (Label): HP Percentage
- EQType 20 (Label): Mana Percentage
- EQType 21 (Label): Maximum Mana
- EQType 70 (Label, Zeal): HP current/max format
- EQType 80 (Label, Zeal): Mana current/max or percentage
- EQTypes 5-11 (Label): STR, STA, AGI, DEX, WIS, INT, CHA
- EQTypes 12-16 (Label): Resistances (Poison, Disease, Fire, Cold, Magic)
- EQTypes 24-25 (Label): Current/Max Weight

**Progression Display**:
- EQType 4 (Gauge): Experience percentage
- EQType 26 (Label): Experience percentage (numeric)
- EQType 5 (Gauge): AA Experience percentage
- EQType 71 (Label, Zeal): AA Points Total
- EQType 72 (Label, Zeal): AA Points Available
- EQType 73 (Label, Zeal): AA Percentage

**Character Info**:
- EQType 1 (Label): Character Name
- EQType 2 (Label): Level
- EQType 3 (Label): Class
- EQType 4 (Label): Deity

**Equipment Slots**:
- EQTypes 0-21 (InvSlot): All worn equipment (repositioned)
- EQTypes 22-29 (InvSlot): Bag slots

### Zeal Client Considerations

- AA gauge (EQType 5) works on standard P2002 client
- Extended AA labels (71, 72, 73) require Zeal client
- HP/Mana value labels (70, 80) require Zeal client
- Provide fallback layout/labels for non-Zeal users if needed

### Color Palette (from canonical Inventory scheme)

- White (255, 255, 255): Default text, values
- Blue (50, 160, 250): Attribute labels (STR, STA, etc.)
- Pink/Rose (200, 120, 145): HP/Mana labels
- Orange (255, 165, 0): ATK, FIRE resist
- Cyan (0, 165, 255): COLD resist
- Purple (195, 0, 185): MAGIC resist
- Yellow (205, 205, 0): DISEASE resist
- Teal (0, 130, 100): POISON resist

### Templates & Styling

- **Window Template**: WDT_Rounded (consistent with Phase 3.7 standardization)
- **Gauge Templates**: Use tall gauge templates from Phase 3.5 (A_TallGaugeBG, A_TallGaugeFill, A_TallGaugeLines)
- **Slot Backgrounds**: Existing A_Inv* animations (A_InvHead, A_InvChest, etc.)
- **Button Templates**: A_BtnNormal, A_BtnPressed, A_BtnFlyby (standard buttons)

### XML Structure Best Practices

- Use ScreenID for all elements (enables easier debugging)
- Set RelativePosition=true for all child elements
- Comment sections clearly (<!-- LEFT ZONE -->, <!-- CENTER ZONE -->, etc.)
- Group related elements together in XML (all stats labels together, all slots together)
- Use consistent naming: IW_ prefix for Inventory Window elements

---

## Risks & Mitigation

**Risk 1: Window Too Wide**  
- **Impact**: Doesn't fit on lower resolutions, overlaps other windows
- **Mitigation**: Test on 800x600 resolution early, adjust zone widths, consider collapsible sections

**Risk 2: Information Overload**  
- **Impact**: Too many stats make window cluttered and hard to scan
- **Mitigation**: Prioritize most important stats (AC, ATK, HP, Mana), use color coding, consider Optional stats section

**Risk 3: Equipment Slot Confusion**  
- **Impact**: Users can't find familiar slots in new anatomical layout
- **Mitigation**: Provide Options variant with traditional layout, create visual guide, use clear tooltips

**Risk 4: Cross-Window Alignment Breaks**  
- **Impact**: Changing one window requires updating others, maintenance burden
- **Mitigation**: Document canonical sequence clearly, create alignment validation checklist, test thoroughly

**Risk 5: Bag Slots Inaccessible**  
- **Impact**: Bags at bottom of tall window are off-screen on low resolutions
- **Mitigation**: Test bag positioning on 800x600, consider fixed bag row at specific Y position, use double-row if needed

**Risk 6: Zeal vs Non-Zeal Compatibility**  
- **Impact**: Advanced EQTypes (AA labels, HP/Mana values) don't work without Zeal
- **Mitigation**: Design layout to work with basic EQTypes, treat Zeal features as enhancements, test on both clients

---

## Success Criteria

### Functional Requirements

- ✅ All 21 equipment slots function correctly (equip, unequip, tooltips)
- ✅ All 8 bag slots accessible and functional
- ✅ Stats update dynamically when gear changes
- ✅ XP and AA gauges display correctly
- ✅ Currency buttons work (withdraw, deposit)
- ✅ Class animation displays character's class
- ✅ Window fits on 800x600 resolution without clipping

### Visual/UX Requirements

- ✅ Equipment slots follow logical anatomical pattern (head-to-toe)
- ✅ Three zones visually distinct and well-organized
- ✅ Stats are readable and color-coded appropriately
- ✅ Gauges aligned and styled consistently
- ✅ No overlapping elements or visual glitches
- ✅ Window feels like a "character sheet" rather than just storage

### Consistency Requirements

- ✅ Equipment slot sequence matches across Inventory, Actions, Hotbar windows
- ✅ Zeal-specific features degrade gracefully on standard client
- ✅ Layout follows WDT_Rounded template standard (Phase 3.7)
- ✅ Color palette matches canonical Inventory scheme

### Maintenance Requirements

- ✅ XML well-commented and organized
- ✅ Canonical sequence documented in DEVELOPMENT.md
- ✅ Options variants created for user choice (Character Sheet vs Standard)
- ✅ Window dimensions and element coordinates documented

---

## Related Work & Dependencies

### Dependencies

- **Phase 3.5**: Tall gauge templates and AA gauge styling (reference implementation)
- **Phase 3.7**: WDT_Rounded template standardization, TGA asset fixes
- **Phase 2**: Merchant window tab removal pattern (inform inventory tab decisions)

### Related Future Work

- **Phase 4**: Actions Window Simplification (may reduce stats duplication)
- **Phase 7**: Asset Consolidation (optimize equipment slot icon assets)

### Inspirations

- **duxaUI**: Anatomical equipment layout pattern (duxaUI/EQUI_Inventory.xml)
- **Infiniti-Blue**: Potential stat display patterns (to be researched)
- **Standard EQ Client**: Traditional equipment sequence (baseline for comparison)

---

## Learnings (To Be Captured Post-Implementation)

- Anatomical layout vs traditional slot order usability comparison
- Optimal stat density for readable character sheet
- Single-row vs double-row bag slot user preference
- Cross-window sequence consistency maintenance effort
- Window dimension trade-offs (width vs height)

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Technical References](../technical/eqtypes.md)
