# 📐 Thorne UI Development Standards

Complete guidelines for maintaining consistency across all Thorne UI variants and ongoing development.

**Quick Links**: [Development Guide](../DEVELOPMENT.md) | [Phases](phases/) | [Technical References](technical/) | [Quick Hits](QUICK-HITS.md) | [Releases](releases/RELEASES.md)

---

## 📋 Why Standards Matter

Consistent standards ensure the UI remains:

- **Maintainable** - New contributors understand existing patterns
- **Scalable** - New features integrate smoothly with existing design
- **Professional** - Cohesive appearance users expect from quality UI
- **Accessible** - Clear conventions reduce learning curve

---

## 🎨 Core Standards

### Window Sizing

Standardized window widths for consistent layout:

- **Primary windows**: 160px (Actions, Group, Pet windows)
- **Merchant/Loot windows**: 315-330px
- **Player window**: Variable content width (~130px)

### Button Layout

**Full-width buttons** (spanning entire window):

- Position: `X=2, CX=154` (ends at X=156)
- Creates 2px left, 4px right borders
- Examples: Attack/Back buttons in Pet window

**Paired buttons** (two columns):

- Left: `X=2, CX=77`
- Right: `X=79, CX=77`
- Both end at X=156, creates 1px center gap
- Examples: Follow/Guard (left), Taunt/Sit (right) in Pet window

### Gauge Styling

**Position & Sizing:**

- Default X position: `X=3`
- Default height: `CY=24`
- Width for 160px window: `CX=128`
- Template: Use only `Background`, `Fill`, `Lines` (no end caps)

**Color Standards:**

| EQType | Purpose | Color (RGB) |
|--------|---------|------------|
| 1 | Player HP | 255, 0, 0 (Red) |
| 2 | Player Mana | 100, 150, 255 (Bright Blue) |
| 16 | Pet HP | 200, 0, 200 (Purple) |
| 17 | Pet Mana | 100, 150, 255 (Bright Blue) |
| 11-21 | Group Member HP | Consistent across members |

### Label Display

**Health/Mana Labels:**

- HP value labels use EQType binding to display current/max
- Percent labels: Static `<Text>%</Text>` for alignment
- Position: Overlap gauge with `AlignRight=true`
- Standard sizing: `X=74, CX=60` (HP), `X=136, CX=16` (Percent)

**Placeholder Text Convention:**

Empty-state elements should display helpful placeholder text:

```xml
<Text>No Pet</Text>     <!-- displays when no pet active -->
<Text>No Target</Text>  <!-- displays when no target selected -->
```

Game client dynamically replaces with real data when available.

### Spacing & Borders

- **Left border minimum**: 2px
- **Right border minimum**: 4px
- **Text offsets**: Use `TextOffsetX`, `TextOffsetY` to position text
- **Hidden text**: `TextOffsetY="-250"` or similar to move off-screen

**See**: [Color Palette & Text Styling](#color-palette--text-styling) for comprehensive color reference.

### Asset File Standards

**TGA Texture Files:**

- **Format**: Targa RGBA (proper binary format)
- **Not acceptable**: PNG data saved with `.tga` extension
- **Conversion**: Use PIL/Python to ensure proper RGBA Targa format
- **Consistency**: All gauge pieces must use same format
- **Type 10 RLE**: Recommended for gauge textures (32x256px classic_pieces01.tga)
- **Alpha Channel**: Required for transparency effects

**Window Templates:**

- **WDT_Rounded**: Standard rounded window frame with integrated title bar
  - Requires: `wnd_bg_dark_rock.tga` for title bar texture
  - Requires: `Font` element (typically Font 3) for title text rendering
  - Use for: All main windows, Options variants
- **WDT_Inner**: Inner frame template for subwindows/containers
  - Use for: Grouping elements, creating visual zones
- **WDT_RoundedNoTitle**: Avoid in new development (replaced by WDT_Rounded in Phase 3.7)

**Template Usage Pattern**:
```xml
<Screen item="WindowName">
    <DrawTemplate>WDT_Rounded</DrawTemplate>
    <Font>3</Font>
    <Style_Titlebar>true</Style_Titlebar>
    <!-- window contents -->
</Screen>
```

---

## 🏗️ Layout & Organization Standards

> **Added January 2026** - Phase 3.7/3.9 learnings

### Subwindow/Inner Screen Pattern

**When to Use Inner `<Screen>` Containers**:

Use inner `<Screen>` elements to create **logical groupings** of related UI elements:

✅ **Recommended Use Cases**:
- Equipment slot grids (all 21 worn slots together)
- Stat display sections (AC, ATK, HP, Mana, Resistances grouped)
- Progression displays (XP gauge + AA gauge + labels)
- Button clusters (action buttons, navigation buttons)
- Currency displays (Platinum/Gold/Silver/Copper grouping)
- Player info sections (name, level, class, deity)

**Benefits**:
1. **Group Movement**: Change one `Location` to move entire cluster
2. **Relative Positioning**: Child elements use coords relative to parent
3. **Logical Code Structure**: XML hierarchy mirrors visual hierarchy
4. **Variant Creation**: Swap entire subwindows between Options variants
5. **Collision/Bounds**: Inner Screen provides bounding box for layout
6. **Visual Debugging**: Can add temporary borders to see groupings

**Implementation Pattern**:

```xml
<!-- Parent window -->
<Screen item="InventoryWindow">
    <Size><CX>450</CX><CY>400</CY></Size>
    
    <!-- Inner Screen: Equipment Grid Zone -->
    <Screen item="IW_EquipmentGrid">
        <ScreenID>IW_EquipmentGrid</ScreenID>
        <RelativePosition>true</RelativePosition>
        <Location><X>50</X><Y>10</Y></Location>
        <Size><CX>260</CX><CY>200</CY></Size>
        <DrawTemplate>WDT_Inner</DrawTemplate>
        <Pieces>InvSlot1</Pieces>
        <Pieces>InvSlot2</Pieces>
        <Pieces>InvSlot3</Pieces>
        <!-- ... more slot pieces ... -->
        <Pieces>InvSlot21</Pieces>
    </Screen>
    
    <!-- Inner Screen: Stats Zone -->
    <Screen item="IW_StatsZone">
        <ScreenID>IW_StatsZone</ScreenID>
        <RelativePosition>true</RelativePosition>
        <Location><X>320</X><Y>10</Y></Location>
        <Size><CX>120</CX><CY>150</CY></Size>
        <Pieces>Label_AC</Pieces>
        <Pieces>Label_ATK</Pieces>
        <Pieces>Label_HP</Pieces>
        <Pieces>Label_Mana</Pieces>
    </Screen>
</Screen>

<!-- Child elements use relative coordinates within parent Screen -->
<Label item="Label_AC">
    <ScreenID>Label_AC</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>5</X>   <!-- 5px from left edge of IW_StatsZone, NOT main window -->
        <Y>10</Y>
    </Location>
    <Text>AC:</Text>
</Label>
```

**Naming Convention for Subwindows**:
- Prefix with parent window acronym: `IW_` for InventoryWindow, `PW_` for PlayerWindow
- Descriptive name: `EquipmentGrid`, `StatsZone`, `ProgressionZone`
- Full example: `IW_EquipmentGrid`, `PW_GaugeCluster`, `GW_MemberList`

**When NOT to Use Inner Screens**:
- Single standalone elements (one label, one button)
- Elements that need independent absolute positioning
- Very simple windows with <5 elements total

---

### Anatomical Layout Pattern

> **Established in Phase 3.9** - Inventory Window redesign

**Equipment Slot Sequencing**:

When displaying equipment slots, use **anatomical ordering** (head-to-toe, left-to-right):

**Standard Sequence** (21 worn equipment slots):

1. **Row 1 - HEAD LEVEL**: Left Ear, Neck, Face, Head, Right Ear (EQTypes 1, 5, 3, 2, 4)
2. **Row 2 - ARM LEVEL**: Left Ring, Left Wrist, Arms, Hands, Right Wrist, Right Ring (EQTypes 15, 9, 7, 12, 10, 16)
3. **Row 3 - TORSO LEVEL**: Shoulders, Chest, Back, Waist, Legs, Feet (EQTypes 6, 17, 8, 20, 18, 19)
4. **Row 4 - WEAPONS LEVEL**: Primary, Secondary, Range, Ammo (EQTypes 13, 14, 11, 21)

**Rationale**:
- Mirrors how players naturally think about gear (top to bottom)
- Symmetric layout (left/right equipment mirrored around center)
- Logical grouping by body region
- Consistent across all windows displaying equipment

**Application**:
- **Inventory Window**: Full 21-slot anatomical grid
- **Actions Window**: Partial display maintains same sequence/grouping
- **Hotbar Window**: Inventory quick-access follows same pattern
- **Any window showing equipment**: Use canonical ordering

**Consistency Rule**: Once a player learns slot positions in Inventory, they should find the same relative positions in Actions, Hotbar, etc.

---

### Gauge Templates & Styling

> **Refined in Phase 3.5** - Player/Pet/Group window work

**Tall Gauge Pattern** (14px height, uniform width):

Use for: HP, Mana, Stamina, XP, AA gauges requiring vertical stacking

**Template Structure**:
```xml
<Gauge item="HP_Gauge">
    <EQType>1</EQType>
    <Size><CX>150</CX><CY>14</CY></Size>
    <GaugeDrawTemplate>
        <Background>A_TallGaugeBG</Background>
        <Fill>A_TallGaugeFill</Fill>
        <Lines>A_TallGaugeLines</Lines>
    </GaugeDrawTemplate>
    <FillTint><R>255</R><G>0</G><B>0</B></FillTint>  <!-- Red for HP -->
    <LinesFillTint><R>180</R><G>0</G><B>0</B></LinesFillTint>
    <DrawLinesFill>true</DrawLinesFill>
</Gauge>
```

**Gauge Color Standards** (Expanded):

| Purpose | Fill RGB | LinesFill RGB | Notes |
|---------|----------|---------------|-------|
| Player HP | 255, 0, 0 | 180, 0, 0 | Red gauge |
| Player Mana | 100, 150, 255 | 70, 105, 180 | Bright blue gauge |
| Pet HP | 200, 0, 200 | 140, 0, 140 | Purple gauge (Phase 3.5) |
| Pet Mana | 100, 150, 255 | 70, 105, 180 | Bright blue gauge |
| Stamina/Breath | 205, 205, 0 | 144, 144, 0 | Yellow gauge |
| XP Progress | 0, 205, 0 | 0, 144, 0 | Green gauge |
| AA Progress | 205, 205, 0 | 144, 144, 0 | Yellow gauge |
| Group Member HP | 255, 0, 0 | 180, 0, 0 | Red (consistent) |

**Vertical Spacing**:
- **14px gauges**: Use 17px vertical spacing (14px gauge + 3px gap)
- **24px gauges**: Use 27px vertical spacing (24px gauge + 3px gap)
- Maintains consistent rhythm across window

**Label Overlay Pattern**:
```xml
<Label item="HP_Value">
    <RelativePosition>true</RelativePosition>
    <Location><X>5</X><Y>0</Y></Location>  <!-- Overlays gauge -->
    <Size><CX>60</CX><CY>14</CY></Size>
    <EQType>70</EQType>  <!-- HP current/max -->
    <AlignCenter>true</AlignCenter>
    <NoWrap>true</NoWrap>  <!-- Prevents truncation -->
    <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
</Label>
```

---

### XML Organization Best Practices

**File Structure Order**:

1. **XML Declaration**: `<?xml version="1.0" encoding="us-ascii"?>`
2. **Schema**: `<Schema xmlns="EverQuestData" ...>`
3. **Standalone Elements**: InvSlots, Gauges, Labels, Buttons (elements without parents)
4. **Main Window Screen**: Primary `<Screen item="WindowName">` container
5. **Inner Screens**: Subwindow containers (EquipmentGrid, StatsZone, etc.)
6. **Animations**: StaticAnimation definitions
7. **Templates**: Reusable template pieces
8. **Comments**: Section dividers, explanations

**Section Comments**:
```xml
<!-- ========================================== -->
<!-- LEFT ZONE: Character Identity & Info      -->
<!-- ========================================== -->

<Screen item="IW_LeftZone">
    <!-- Player name, level, class labels -->
    <Pieces>PlayerName</Pieces>
    <Pieces>PlayerLevel</Pieces>
    <Pieces>PlayerClass</Pieces>
    <Pieces>ClassAnim</Pieces>
    <Pieces>DoneButton</Pieces>
</Screen>

<!-- ========================================== -->
<!-- CENTER ZONE: Equipment Grid               -->
<!-- ========================================== -->
```

**Element Naming**:
- **ScreenID**: Always set for debugging (`<ScreenID>IW_EquipmentGrid</ScreenID>`)
- **Item Attribute**: Descriptive, unique (`item="Label_AC"`, `item="HP_Gauge"`)
- **Prefix Convention**: `IW_` (InventoryWindow), `PW_` (PlayerWindow), `GW_` (GroupWindow)

**RelativePosition**:
- Set `<RelativePosition>true</RelativePosition>` for ALL child elements within Screens
- Enables repositioning parent without recalculating all children
- Exception: Top-level window Screen (no parent, uses absolute positioning)

---

### Options Directory Variant Pattern

> **Established in Phase 3.7** - Infrastructure standardization

**Directory Structure**:

```
thorne_drak/
├── EQUI_WindowName.xml          # Standard/minimal variant (main directory)
└── Options/
    └── WindowName/
        ├── README.md            # Variant documentation
        ├── Standard/
        │   └── EQUI_WindowName.xml   # Feature-rich standard variant
        ├── Variant1/
        │   └── EQUI_WindowName.xml   # Alternative layout/feature set
        └── Variant2/
            └── EQUI_WindowName.xml   # Another alternative
```

**Pattern Purpose**:

1. **Main Directory**: Contains **standard/minimal** variant
   - Clean, simple layout
   - No tabs or complex features (where applicable)
   - Baseline for all users
   
2. **Options Directory**: Contains **feature-rich variants**
   - Tabbed interfaces (Merchant, Inventory)
   - Expanded stat displays (Actions, Player)
   - Alternative layouts (Hotbutton vertical, LoadskinWnd sizes)
   - User-selectable via `/loadskin` or manual file copy

**When to Create Options Variants**:

✅ **Create variant when**:
- Adding features some users may not want (tabs, extra stats)
- Providing alternative layouts (vertical vs horizontal)
- Offering different information density levels (minimal vs detailed)
- Supporting different play styles (raid-focused vs solo-focused)

❌ **Don't create variant for**:
- Minor tweaks (change one color, move one label slightly)
- Bug fixes (fix should go in both main and Options variants)
- Template updates (WDT_Rounded adoption should be universal)

**Naming Convention**:
- **README.md**: Explain purpose of each variant, installation instructions
- **Standard**: Feature-complete variant (may have tabs, stats, etc.)
- **Descriptive Names**: "Dark Slots", "Vertical Bags", "Large Inventory", "Pet Bottom"
- **Avoid**: "v1", "v2", "new", "test" (use descriptive purpose-driven names)

---

### Implementation Patterns

> **See [DEVELOPMENT.md - Architecture Decisions](../DEVELOPMENT.md#architecture-decisions--lessons-learned) for detailed implementation guidance**

**Key Architectural Patterns**:

1. **Global UI Element Positioning**: Elements with same `item=` name display at same position across all pages/tabs
   - Solution: Use unique names per tab (e.g., `MW_Primary` vs `MW_Bags_Primary`)

2. **Style_Sizable Behavior**: Set to `false` for fixed-width windows to prevent accidental horizontal shrinking

3. **StaticAnimation**: Use `<Animation>` tag only, never use `RelativePosition` or `EQType` with animations

4. **Inventory Window Reference**: Use Inventory window as canonical source for label colors, stat patterns, spacing

---

### Color Palette & Text Styling

> **Canonical Inventory Window Color Scheme** - Reference standard

**Label Colors** (for stats, attributes, resistances):

| Label Type | RGB Value | Hex | Usage |
|------------|-----------|-----|-------|
| **White** | 255, 255, 255 | #FFFFFF | Default text, player name, stat values |
| **Blue (Attributes)** | 50, 160, 250 | #32A0FA | Attribute labels (STR, STA, AGI, DEX, WIS, INT, CHA) |
| **Pink/Rose** | 200, 120, 145 | #C87891 | HP/Mana labels (alternate to white) |
| **Orange** | 255, 165, 0 | #FFA500 | ATK label, FIRE resist |
| **Cyan** | 0, 165, 255 | #00A5FF | COLD resist |
| **Purple** | 195, 0, 185 | #C300B9 | MAGIC resist |
| **Yellow** | 205, 205, 0 | #CDCD00 | DISEASE resist |
| **Teal** | 0, 130, 100 | #008264 | POISON resist |
| **Green** | 0, 205, 0 | #00CD00 | XP gauge, positive indicators |

**Gauge Fill Colors**:

> **Standard Gauge RGB Values** - Use these exact values across all windows for consistency

| Gauge Type | Fill RGB | LinesFill RGB | Hex (Fill) | EQType | Notes |
|------------|----------|---------------|------------|--------|-------|
| **Player HP** | 255, 0, 0 | 180, 70, 70 | #FF0000 | 1 | Bright red for health |
| **Player Mana** | 100, 150, 255 | 70, 105, 180 | #6496FF | 2 | "Thorne blue" - signature color |
| **Pet Health** | 200, 80, 200 | 150, 60, 150 | #C850C8 | 9 | Purple to differentiate from player |
| **Pet Mana** | 100, 150, 255 | 70, 105, 180 | #6496FF | 17 | Same blue as player mana |
| **Stamina** | 205, 205, 0 | 144, 144, 0 | #CDCD00 | 4 | Yellow for stamina/endurance |
| **Experience (XP)** | 0, 205, 0 | 0, 144, 0 | #00CD00 | 5 | Green for progression |
| **AA Points** | 205, 205, 0 | 144, 144, 0 | #CDCD00 | 10 | Yellow (same as XP in some UIs) |
| **Breath Meter** | 0, 240, 240 | 0, 0, 0 | #00F0F0 | 8 | Cyan for underwater breathing |
| **Mana Tick (Standard)** | 0, 220, 220 | 0, 220, 220 | #00DCDC | 24 | LinesFill only, 103px wide (compact windows) |
| **Mana Tick (Tall)** | 0, 220, 220 | 0, 220, 220 | #00DCDC | 24 | LinesFill only, 120px wide (Player/Pet windows) |
| **Target HP** | 240, 0, 0 | 220, 220, 0 | #F00000 | 6 | Oval gauge style |
| **Casting Bar** | 240, 0, 240 | 220, 220, 0 | #F000F0 | 7 | Magenta for spell casting |

**Standard Gauge Sizes**:

| Gauge Style | Width (CX) | Height (CY) | LinesFill Animation | Usage |
|-------------|------------|-------------|---------------------|-------|
| **Standard** | 103px | 8px | A_GaugeLinesFill | Compact windows (Target, Breath) |
| **Tall** | 120px | 15px | A_GaugeLinesFill_Tall | Player/Pet windows (more visible) |
| **Wide** | 250px | 15px | (uses oval animations) | Target oval gauges (horizontal emphasis) |

**Gauge XML Template**:

```xml
<!-- Standard HP Gauge Example -->
<Gauge item="ExampleHP_Gauge">
  <ScreenID>ExampleHP</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>2</X><Y>16</Y></Location>
  <Size><CX>122</CX><CY>8</CY></Size>
  <GaugeOffsetX>0</GaugeOffsetX>
  <GaugeOffsetY>0</GaugeOffsetY>
  <TextOffsetY>-50</TextOffsetY>  <!-- Hide text if not needed -->
  <Style_VScroll>false</Style_VScroll>
  <Style_HScroll>false</Style_HScroll>
  <Style_Transparent>false</Style_Transparent>
  <FillTint>
    <R>255</R><G>0</G><B>0</B>  <!-- Standard HP red -->
  </FillTint>
  <LinesFillTint>
    <R>180</R><G>70</G><B>70</B>
  </LinesFillTint>
  <DrawLinesFill>false</DrawLinesFill>
  <EQType>1</EQType>  <!-- Player HP -->
  <GaugeDrawTemplate>
    <Background>A_GaugeBackground</Background>
    <Fill>A_GaugeFill</Fill>
  </GaugeDrawTemplate>
</Gauge>

<!-- Mana Tick Gauge (LinesFill only - STANDARD 103px for compact windows) -->
<Gauge item="ExampleManaTick_Gauge">
  <ScreenID>ManaTick</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>148</X><Y>23</Y></Location>
  <Size><CX>103</CX><CY>8</CY></Size>
  <GaugeOffsetX>0</GaugeOffsetX>
  <GaugeOffsetY>0</GaugeOffsetY>
  <TextOffsetY>-50</TextOffsetY>
  <Style_VScroll>false</Style_VScroll>
  <Style_HScroll>false</Style_HScroll>
  <Style_Transparent>true</Style_Transparent>  <!-- Transparent for line-only -->
  <FillTint>
    <R>0</R><G>220</G><B>220</B>  <!-- Cyan mana tick -->
  </FillTint>
  <LinesFillTint>
    <R>0</R><G>220</G><B>220</B>
  </LinesFillTint>
  <DrawLinesFill>false</DrawLinesFill>
  <EQType>24</EQType>  <!-- Mana tick indicator -->
  <GaugeDrawTemplate>
    <Fill>A_GaugeLinesFill</Fill>  <!-- Standard width (103px) -->
  </GaugeDrawTemplate>
</Gauge>

<!-- Mana Tick Gauge (LinesFill only - TALL 120px for Player/Pet windows) -->
<!-- Available via Zeal addon/helper feature -->
<Gauge item="Mana_Tick">
  <ScreenID>ManaTick</ScreenID>
  <RelativePosition>true</RelativePosition>
  <Location><X>5</X><Y>52</Y></Location>
  <Size><CX>120</CX><CY>8</CY></Size>
  <GaugeOffsetX>0</GaugeOffsetX>
  <GaugeOffsetY>0</GaugeOffsetY>
  <TextOffsetY>-50</TextOffsetY>
  <Style_VScroll>false</Style_VScroll>
  <Style_HScroll>false</Style_HScroll>
  <Style_Transparent>true</Style_Transparent>
  <FillTint>
    <R>0</R><G>220</G><B>220</B>  <!-- Cyan mana tick -->
  </FillTint>
  <LinesFillTint>
    <R>0</R><G>220</G><B>220</B>
  </LinesFillTint>
  <DrawLinesFill>false</DrawLinesFill>
  <EQType>24</EQType>  <!-- Mana tick indicator -->
  <GaugeDrawTemplate>
    <Fill>A_GaugeLinesFill_Tall</Fill>  <!-- Tall width (120px) -->
  </GaugeDrawTemplate>
</Gauge>
```

**Color Override Guidelines**:

- ✅ **Use standard colors** for consistency across windows
- ✅ **Document deviations** in window-specific comments if you change a color
- ⚠️ **Valid exceptions**: Themed variants, accessibility needs, special UI modes
- ❌ **Avoid**: Random RGB values without documentation

**Text Alignment Standards**:

```xml
<!-- Numeric Values: Right-align for tabular appearance -->
<Label item="AC_Value">
    <AlignRight>true</AlignRight>
    <NoWrap>true</NoWrap>
</Label>

<!-- Labels: Left-align for readability -->
<Label item="AC_Label">
    <AlignLeft>true</AlignLeft>
    <Text>AC:</Text>
</Label>

<!-- Centered Text: For gauges, symmetric layouts -->
<Label item="HP_Value">
    <AlignCenter>true</AlignCenter>
    <NoWrap>true</NoWrap>
</Label>
```

**Font Standards**:

| Font ID | Size (approx) | Usage |
|---------|---------------|-------|
| 0 | Small | Tooltips, secondary info |
| 1 | Small | Compact labels |
| 2 | Medium | Standard labels |
| 3 | Medium | **Default for most UI elements** |
| 4 | Large | Button text, section headers |
| 5 | Large | Title bars, window names |

**NoWrap Property**:
- **Always use** `<NoWrap>true</NoWrap>` for numeric values
- Prevents truncation when values exceed expected width
- Examples: HP/Mana current/max, AC, ATK, Weight displays

---

### Cross-Window Consistency Rules

**Equipment Slot Ordering**:
- ALL windows displaying equipment slots MUST use anatomical pattern
- Applies to: Inventory, Actions, Hotbar, Inspect, any custom windows
- No exceptions unless functionally impossible

**Gauge Vertical Spacing**:
- 14px gauges: 17px spacing (3px gap)
- 24px gauges: 27px spacing (3px gap)
- Consistent rhythm across all windows with stacked gauges

**Stat Display Order** (when showing multiple stats):
1. AC (Armor Class)
2. ATK (Attack)
3. HP (current or current/max)
4. Mana (current or current/max)
5. Attributes (STR, STA, AGI, DEX, WIS, INT, CHA)
6. Resistances (Poison, Disease, Fire, Cold, Magic)
7. Weight (Current/Max)

**Color Consistency**:
- Pet elements: Always purple (`200, 0, 200`)
- Player HP: Always red (`255, 0, 0`)
- Player Mana: Always bright blue (`100, 150, 255`)
- No custom colors unless documented in this standard

---

## 📚 Documentation Organization Standards

> **Recommended as of February 2026** - Managing growing documentation complexity

### When to Split DEVELOPMENT.md

Consider restructuring when documentation exceeds **2000 lines** or **8+ major phases**.

**Proposed Structure**:
```
.docs/
├── STANDARDS.md                 # This file
├── technical/
│   ├── EQTYPES.md
│   ├── ZEAL-FEATURES.md
│   └── templates.md

.development/
├── phases/
│   ├── PHASE-3.9-INVENTORY-REDESIGN.md
│   ├── PHASE-4-ACTIONS.md
│   └── PHASE-6-CONTAINERS.md
└── architecture/
  ├── decisions.md
  ├── options-pattern.md
  └── subwindow-pattern.md
```

**Cross-Linking Pattern**:
```markdown
<!-- Master index -->
### [Phase 3.9](phases/PHASE-3.9-INVENTORY-REDESIGN.md)
**Status**: PLANNED | [Full Documentation →](phases/PHASE-3.9-INVENTORY-REDESIGN.md)

<!-- Phase file -->
# Phase 3.9: Inventory Window Redesign
[← Back to Development Guide](../DEVELOPMENT.md#phases)
```

**Benefits**: Easier navigation, focused docs, better GitHub UI  
**Drawbacks**: More files, link maintenance, git history fragmentation

**Current Status**: ✅ **Completed February 2026** - DEVELOPMENT.md reorganized from 1961 → 412 lines (79% reduction). Documentation now modular with user-facing docs in `.docs/` and working docs in `.development/`.

---

## 📊 EQType Reference

Bindings discovered and verified for TAKP:

| EQType | Binding | Notes |
|--------|---------|-------|
| 1 | Player HP | Red gauge, displays health |
| 2 | Player Mana | Blue gauge, displays mana/power |
| 11-21 | Group Member HP | One per group member slot |
| 35-39 | Group HP Labels | Current/max health text display |
| 16 | Pet HP | Pet health, purple color |
| 17 | Pet Mana | Pet stamina/mana, blue color |
| 69 | Pet HP Label | Pet health value display |

---

## ✅ Contributing Guidelines

### Before Committing

- ✅ Test all changes in-game
- ✅ Verify no overlapping elements or visual glitches
- ✅ Maintain consistent spacing and alignment
- ✅ Follow established color/sizing standards
- ✅ Add comments for non-obvious decisions
- ✅ Document changes in commit message

### Common Tasks

**Adding a new window variant:**

1. Create new subdirectory under `thorne_drak/Options/<WindowType>/`
2. Copy relevant XML file and customize
3. Update group/section documentation
4. Test with `/loadskin` command

**Modifying gauge appearance:**

1. Check EQType reference above
2. Ensure color matches established palette
3. Update scaling proportionally across all variants
4. Test in multiple window contexts

**Creating alternate sizing:**

1. Calculate proportional adjustments (not random pixel changes)
2. Update all dependent elements (labels, buttons, spacing)
3. Test both collapsed and expanded states
4. Document the variant purpose

---

## � Standards Under Investigation

### Window Drag Affordances

Research needed on how to allow dragging of windows without visible title bars. Observations from other EverQuest UI variants:

- Some windows use dummy UI elements in upper-left corners as drag targets
- Allows moving windows that lack visible title bars (Pet, Actions, Merchant windows)
- Questions to resolve:
  - Which window types benefit most from visible drag affordances?
  - Should this be standardized across all thorne_drak windows?
  - Implementation: dummy colored element vs. transparent placeholder vs. other approach?
  - Usability impact: does visibility improve or hinder user experience?

**Status**: Investigation pending (See TODO.md → UI Standards Investigation)

---

## �📚 Related Documentation

- **README.md** - Project vision, philosophy, and variants overview
- **DEVELOPMENT.md** - Implementation details, architecture decisions, and roadmap
- **TODO.md** - Planned features and work items

---

## 📜 Version History

**v1.0.0** (February 1, 2026)
- ✅ Comprehensive standards documentation created
- ✅ Layout & Organization Standards (subwindow pattern, anatomical layout)
- ✅ Gauge Templates & Styling (6 gauge template definitions)
- ✅ XML Organization Best Practices
- ✅ Options Directory Variant Pattern
- ✅ Color Palette & Text Styling (canonical Inventory color scheme)
- ✅ Cross-Window Consistency Rules
- ✅ Documentation Organization Standards
- ✅ Implementation Patterns summary

---

**Maintainer**: Draknare Thorne  
**Repository**: [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)
