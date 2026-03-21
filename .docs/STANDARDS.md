# 📐 Thorne UI Development Standards

Complete guidelines for maintaining consistency across all Thorne UI variants and ongoing development.

**Quick Links**: [Development Guide](DEVELOPMENT.md) | [Phases](../.development/initial_phases/README.md) | [Technical References](technical/README.md) | [Releases](releases/RELEASES.md)

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

| EQType | Purpose         | Color (RGB)                  |
| ------ | --------------- | ---------------------------- |
| 1      | Player HP       | 255, 0, 0 (Red)              |
| 2      | Player Mana     | 30, 30, 255 (Deep Blue fill) |
| 16     | Pet HP          | 200, 80, 200 (Purple)        |
| 17     | Pet Mana        | 100, 150, 255 (Bright Blue)  |
| 11-21  | Group Member HP | Consistent across members    |

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

### Subwindow Transparency Behavior (Critical)

> **Verified February 2026** - Inventory/MusicPlayer crash-fade investigation

For TAKP/P2002 UI behavior in this project, transparency on a parent `<Screen>` affects all child pieces in ways that matter for usability and stability.

**Observed rules:**

- **Transparent parent screen (`Style_Transparent=true`) can cause child elements to appear dim/faded.**
- Applies to `InvSlot` children even when the `InvSlot` itself has `<Style_Transparent>false</Style_Transparent>`.
- Also observed with other child controls (for example, button visuals in Actions-related layouts).

- **Non-transparent subwindow wrappers (`Style_Transparent=false`) may be unsafe in some contexts.**
- During controlled testing, enabling an opaque wrapper subwindow in repurposed `MusicPlayerWnd` caused client instability/crash.
- Treat opaque wrapper usage as **high-risk** unless validated in that exact window/context.

**Design decision standard:**

- ✅ **If you want non-faded slot rendering:** prefer placing slots directly in the main window’s `<Pieces>` (no wrapper screen).
- ⚠️ **If you intentionally want faded/dimmed rendering:** place controls inside a transparent subwindow wrapper.
- ❌ **Do not assume child `InvSlot` transparency settings override parent screen transparency behavior.**

**Practical guidance:**

- Keep wrapper screens for logical grouping only when visual side-effects are acceptable.
- For critical visibility (inventory/bag interactions), default to direct placement.
- When experimenting with wrapper transparency behavior, test in a sandbox window first (e.g., `EQUI_MusicPlayerWnd.xml`) before touching canonical windows like Inventory.

### Flattening Subwindows: Relative Position Rule (Critical)

When removing a wrapper `<Screen>` and moving its child controls into the parent window's `<Pieces>`, preserve movement behavior deliberately:

- ✅ **Use `<RelativePosition>true</RelativePosition>`** for controls that should move with the parent window (default for Inventory/Actions content).
- ⚠️ **Use `<RelativePosition>false</RelativePosition>` only** for intentionally screen-anchored elements or temporary off-screen parking.
- ❌ Do not switch to absolute positioning by default during flattening; this can make controls appear fixed to the main screen instead of the window.

**Example implication:**

- Flattening `IW_ButtonBar_Wnd` into `InventoryWindow` should keep button controls
  (`IW_DoneButton`, `IW_Skills`, `IW_AltAdvBtn`, `IW_Destroy`) as
  relative-positioned so they follow `InventoryWindow` movement.

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

| Purpose         | Fill RGB      | LinesFill RGB | Notes                                     |
| --------------- | ------------- | ------------- | ----------------------------------------- |
| Player HP       | 255, 0, 0     | 220, 220, 0   | Red fill, gold line tint                  |
| Player Mana     | 30, 30, 255   | 0, 220, 220   | Deep blue fill, cyan line tint            |
| Pet HP          | 200, 80, 200  | 0, 0, 0       | Purple fill (PlayerWindow implementation) |
| Pet Mana        | 100, 150, 255 | 70, 105, 180  | Bright blue gauge                         |
| Stamina/Breath  | 240, 240, 0   | 0, 220, 0     | Yellow fill, green line tint              |
| XP Progress     | 220, 150, 0   | 100, 160, 255 | Orange fill, blue line tint               |
| AA Progress     | 220, 200, 0   | 0, 220, 220   | Yellow fill, cyan line tint               |
| Group Member HP | 255, 0, 0     | 180, 0, 0     | Red (legacy/group variants)               |

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

> **See [DEVELOPMENT.md - Architecture Decisions](DEVELOPMENT.md#architecture-decisions--lessons-learned) for detailed implementation guidance**

**Key Architectural Patterns**:

1. **Global UI Element Positioning**: Elements with same `item=` name display at same position across all pages/tabs
   - Solution: Use unique names per tab (e.g., `MW_Primary` vs `MW_Bags_Primary`)

2. **Style_Sizable Behavior**: Set to `false` for fixed-width windows to prevent accidental horizontal shrinking

3. **StaticAnimation**: Use `<Animation>` tag only, never use `RelativePosition` or `EQType` with animations

4. **Inventory Window Reference**: Use Inventory window as canonical source for label colors, stat patterns, spacing

### Note Window Constraint (Do Not Repurpose)

> **Verified February 2026** - client behavior validation

`NoteWindow` has client-specific logic and expected child bindings that are not safe to repurpose for custom UI experiments in this project.

**Rules:**

- ✅ Keep `thorne_drak/EQUI_NoteWindow.xml` aligned to the standard Note implementation.
- ❌ Do not repurpose `NoteWindow` for stats, bags, or experimental custom controls.
- ❌ Do not maintain `Options/Note` variants.

If temporary testing is needed, use a non-critical sandbox window instead (for example `EQUI_MusicPlayerWnd.xml`) and remove test scaffolding after validation.

---

### Color Palette & Text Styling

> **Canonical Inventory Window Color Scheme** - Reference standard

**Label Colors** (for stats, attributes, resistances):

| Label Type       | Color Name       | RGB           | Hex     | Usage                                    |
| ---------------- | ---------------- | ------------- | ------- | ---------------------------------------- |
| **Default Text** | White            | 255, 255, 255 | #FFFFFF | Player name, stat values                 |
| **Attributes**   | Sky Blue         | 70, 180, 255  | #46B4FF | STR, STA, AGI, DEX, WIS, INT, CHA       |
| **HP Value**     | Heated Blush     | 255, 100, 100 | #FF6464 | HP current/max text                      |
| **Mana Value**   | Crystal Blue     | 100, 150, 255 | #6496FF | Mana current/max text                    |
| **AC / ATK**     | Amber            | 255, 185, 30  | #FFB91E | AC label, ATK label                      |
| **FIRE Resist**  | Fire Red         | 255, 113, 46  | #FF712E | FIRE resist value                        |
| **COLD Resist**  | Frost Blue       | 15, 182, 240  | #0FB6F0 | COLD resist value                        |
| **MAGIC Resist** | Arcane Violet    | 255, 113, 255 | #FF71FF | MAGIC resist value                       |
| **DISEASE Resist** | Plague Yellow  | 230, 230, 0   | #E6E600 | DISEASE resist value                     |
| **POISON Resist** | Venom Green     | 0, 220, 0     | #00DC00 | POISON resist value                      |
| **Positive**     | Verdant          | 0, 205, 0     | #00CD00 | XP gauge text, positive indicators       |

**Gauge Fill Colors**:

> **Standard Gauge RGB Values** — Use these exact values across all windows for consistency

| Gauge Type          | Color Name      | Fill RGB      | Lines RGB     | Hex     | EQType | Description                          |
| ------------------- | --------------- | ------------- | ------------- | ------- | ------ | ------------------------------------ |
| **Player HP**       | Blood Red       | 255, 0, 0     | 220, 220, 0   | #FF0000 | 1      | Standard Player/Target windows       |
| **Player Mana**     | Tidal Blue      | 30, 30, 255   | 0, 220, 220   | #1E1EFF | 2      | Text labels use RGB(100,150,255)     |
| **Pet Health**      | Conjured Violet | 200, 80, 200  | 0, 0, 0       | #C850C8 | 16     | LinesFill varies by window           |
| **Pet Mana**        | Crystal Blue    | 100, 150, 255 | 70, 105, 180  | #6496FF | 17     | Also group pet HP in GroupWindow     |
| **Stamina**         | Sunburst        | 240, 240, 0   | 0, 220, 0     | #F0F000 | 3      | Yellow fill, green line tint         |
| **Experience (XP)** | Ember Amber     | 220, 150, 0   | 100, 160, 255 | #DC9600 | 4      | Orange fill, blue line tint          |
| **AA Points**       | Golden Aura     | 220, 200, 0   | 0, 220, 220   | #DCC800 | 5      | Yellow fill, cyan line tint          |
| **Breath Meter**    | Aqua            | 0, 240, 240   | 0, 0, 0       | #00F0F0 | 8      | Underwater breathing                 |
| **Mana Tick**       | Cyan Pulse      | 0, 220, 220   | 0, 220, 220   | #00DCDC | 24     | LinesFill only; 103px or 120px wide  |
| **Target HP**       | Sanguine        | 240, 0, 0     | 220, 220, 0   | #F00000 | 6      | Oval gauge style                     |
| **Casting Bar**     | Arcane Surge    | 240, 0, 240   | 220, 220, 0   | #F000F0 | 7      | Magenta spell casting                |
| **Global Recast**   | Fading Rose     | 255, 210, 250 | 255, 235, 255 | #FFD2FA | 25     | Thin 3px bar (CastSpell, Target)     |
| **Spell Recast**    | Dark Orchid     | 200, 0, 200   | 0, 220, 220   | #C800C8 | 26–33  | Per-spell cooldown bars              |
| **Attack Timer**    | Burnished Gold  | 220, 180, 0   | 220, 180, 0   | #DCB400 | 34     | Tick bar (TargetWindow)              |

**Window-Specific Gauge Colors**:

> Some gauges use intentionally different colors depending on window context.
> These are **not** overrides — they reflect the design intent for each window.

| Gauge Type          | Color Name    | Fill RGB     | Lines RGB    | Hex     | EQType | Window      | Description                         |
| ------------------- | ------------- | ------------ | ------------ | ------- | ------ | ----------- | ----------------------------------- |
| **Group Member HP** | Tempered Red  | 220, 0, 0    | 220, 220, 0  | #DC0000 | 11–15  | GroupWindow | Darker than Player HP (220 vs 255)  |
| **Group Pet HP**    | Shadow Orchid | 170, 60, 170 | 220, 220, 0  | #AA3CAA | 17–21  | GroupWindow | Thin 2px bars under group HP gauges |

**Standard Gauge Sizes**:

| Gauge Style  | Width (CX) | Height (CY) | LinesFill Animation    | Usage                                    |
| ------------ | ---------- | ----------- | ---------------------- | ---------------------------------------- |
| **Standard** | 103px      | 8px         | A_GaugeLinesFill       | Compact windows (Target, Breath)         |
| **Tall**     | 120px      | 15px        | A_GaugeLinesFill_Tall  | Player/Pet windows (more visible)        |
| **Wide**     | 250px      | 15px        | (uses oval animations) | Target oval gauges (horizontal emphasis) |

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

### Composite Gauge System (Multi-Color Veil Technique)

> **5-band layered gauges** — Each gauge uses oversized A-parts with `GaugeOffsetX` thresholds
> to create multi-color gradients. Band 4 (top layer) drops first at 80%, revealing
> progressive bands as value decreases.

#### Technique Variants

- **Veil** — Linear fade from saturated (Band 4, full) toward white/pastel (Band 0, critical).
  Clean, readable gradient. Used for all production gauges.
- **Arc** — Bright peak in the middle bands (Band 2 is brightest), with dark ends.
  More dramatic but less readable. Available as Player Options only.
- **Nillipuss Classic** — Traffic-light green→yellow→red. Community-inspired.
  Available as a Player Option only (not available for other windows).

#### Composite Structure (XML Layer Order)

Every composite gauge replaces a single `<Gauge>` with this layered structure:

```
BG gauge        — Background texture only (no Fill), hides text offscreen
Band 0 gauge    — Base color (GridFill), always visible, hides text
Band 1A gauge   — Oversized A-part (GaugeOffsetX=-2000), hides text
  Screen clip   — Crops 1A to clip width
  Band 1B gauge — GridFill continuation, hides text
Band 2A gauge   — Oversized A-part (GaugeOffsetX=-4000)
  Screen clip   — Crops 2A to clip width
  Band 2B gauge — GridFill continuation
Band 3A/clip/3B — Same pattern (GaugeOffsetX=-6000)
Band 4A/clip/4B — Same pattern (GaugeOffsetX=-8000)
Text overlay    — Original ScreenID preserved for client binding, no Fill/Background
```

**Key rules:**
- The **text overlay** gauge keeps the original `ScreenID` (e.g., `TargetHP`, `Gauge1`) so the
  client binds the EQType correctly. All other layers use unique ScreenIDs.
- All layers except BG use `Style_Transparent=true` to stack properly.
- Text is hidden on all layers except the overlay via `TextOffsetX/Y` pushed offscreen.
- BG uses `<Background>` only. Band 0 uses `<Fill>` with GridFill. Bands 1-4 A-parts use
  Oversized animations; B-parts use GridFill.

#### Band Threshold Tables

**120px gauge (120t, grid-aligned):**

| Band | Threshold | GaugeOffsetX | A-Part Size | Clip Width | B-Part Remainder |
| ---- | --------- | ------------ | ----------- | ---------- | ---------------- |
| 0    | 0% (base) | 0            | Full gauge  | —          | —                |
| 1    | 20%       | -2000        | 8000        | 24px       | 96px             |
| 2    | 40%       | -4000        | 6000        | 48px       | 72px             |
| 3    | 60%       | -6000        | 4000        | **71px**   | **49px**         |
| 4    | 80%       | -8000        | 2000        | **94px**   | **26px**         |

> Grid positions (120px): 0, 24, 48, **71**, **94**, 119.
> Bands 3-4 are adjusted 1-2px from formula values to land on texture grid lines.

**105px gauge (105t, grid-aligned):**

| Band | Threshold | GaugeOffsetX | A-Part Size | Clip Width | B-Part Remainder |
| ---- | --------- | ------------ | ----------- | ---------- | ---------------- |
| 0    | 0% (base) | 0            | Full gauge  | —          | —                |
| 1    | 20%       | -2000        | 8000        | 21px       | 84px             |
| 2    | 40%       | -4000        | 6000        | 42px       | 63px             |
| 3    | 60%       | -6000        | 4000        | **62px**   | **43px**         |
| 4    | 80%       | -8000        | 2000        | **82px**   | **23px**         |

> Grid positions (105px): 0, 21, 42, **62**, **82**, 104.

**250px gauge (250t, even spacing):**

| Band | Threshold | GaugeOffsetX | A-Part Size | Clip Width | B-Part Remainder |
| ---- | --------- | ------------ | ----------- | ---------- | ---------------- |
| 0    | 0% (base) | 0            | Full gauge  | —          | —                |
| 1    | 20%       | -2000        | 8000        | 50px       | 200px            |
| 2    | 40%       | -4000        | 6000        | 100px      | 150px            |
| 3    | 60%       | -6000        | 4000        | 150px      | 100px            |
| 4    | 80%       | -8000        | 2000        | 200px      | 50px             |

> 250px divides evenly into 50px bands — no grid adjustment needed.

#### Oversized Animation Naming

All Oversized animations follow the pattern: `A_Oversized{Type}_{size}_Band{n}`

| Type           | Texture Source | Row (Y offset) | Purpose                    |
| -------------- | -------------- | -------------- | -------------------------- |
| `Fill`         | thorne01       | Y=0 (16px)     | A-part fill for Veil bands |
| `SolidFill`    | thorne02       | Y=0 (16px)     | A-part solid fill variant  |
| `GridFill`     | thorne02       | Y=16 (32px)    | A-part grid fill variant   |

Sizes with full Oversized animation sets: `105t`, `120t`, `250t`.

> **Missing:** No Oversized animations exist for standard 103x8px gauges. The `gauge_inlay_thorne02.tga`
> texture does not exist yet. This blocks composite treatment of 8px gauges (Target player HP/Mana, Pet HP).

#### Player HP: Fire Arc (Blood Red)

The signature HP palette. At full health: Blood Red. Depleting reveals warm colors through an ember arc.

| Band | Color Name    | RGB           | Hex     | Description                |
| ---- | ------------- | ------------- | ------- | -------------------------- |
| 4    | Blood Red     | 255, 0, 0     | #FF0000 | Full HP — drops first      |
| 3    | Ember Glow    | 255, 60, 10   | #FF3C0A | 60% — hot ember            |
| 2    | Forge Fire    | 240, 85, 25   | #F05519 | 40% — peak brightness      |
| 1    | Smolder       | 200, 40, 80   | #C82850 | 20% — cooling              |
| 0    | Vein          | 175, 25, 120  | #AF1978 | Critical — always visible  |

**Gradient choice: Red Veil** (linear fade to white)

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Crimson           | 255, 0, 0     | #FF0000 | Full HP — drops first      |
| 3    | Scorched Rose     | 255, 50, 50   | #FF3232 | 60%                        |
| 2    | Heated Blush      | 255, 100, 100 | #FF6464 | 40%                        |
| 1    | Fading Wound      | 255, 160, 160 | #FFA0A0 | 20%                        |
| 0    | White-hot Ember   | 255, 210, 210 | #FFD2D2 | Critical — always visible  |

#### Player Mana: Ocean Arc (Tidal Blue)

The signature Mana palette. At full mana: Tidal Blue. Depleting reveals deep-sea colors through an ocean arc.

| Band | Color Name    | RGB           | Hex     | Description                |
| ---- | ------------- | ------------- | ------- | -------------------------- |
| 4    | Tidal Blue    | 30, 30, 255   | #1E1EFF | Full Mana — drops first    |
| 3    | Ocean Current | 40, 80, 252   | #2850FC | 60% — deep flow            |
| 2    | Wave Crest    | 55, 120, 250  | #3778FA | 40% — peak brightness      |
| 1    | Deep Sea      | 80, 55, 220   | #5037DC | 20% — depth                |
| 0    | Abyss         | 125, 30, 190  | #7D1EBE | Critical — always visible  |

**Gradient choice: Blue Veil** (linear fade to white)

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Sapphire          | 0, 0, 255     | #0000FF | Full Mana — drops first    |
| 3    | Frozen Azure      | 50, 50, 255   | #3232FF | 60%                        |
| 2    | Starlit Pool      | 100, 100, 255 | #6464FF | 40%                        |
| 1    | Pale Ether        | 160, 160, 255 | #A0A0FF | 20%                        |
| 0    | Icebloom          | 210, 210, 255 | #D2D2FF | Critical — always visible  |

#### Pet HP: Purple Veil (linear fade to white)

Purple Veil Pet HP palette. At full pet health: Conjured Violet. Depleting lightens toward spectral wisp.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Conjured Violet   | 200, 0, 200   | #C800C8 | Full Pet HP — drops first  |
| 3    | Enchanted Orchid  | 210, 50, 210  | #D232D2 | 60%                        |
| 2    | Mystic Haze       | 220, 100, 220 | #DC64DC | 40%                        |
| 1    | Faded Familiar    | 230, 160, 230 | #E6A0E6 | 20%                        |
| 0    | Spectral Wisp     | 240, 210, 240 | #F0D2F0 | Critical — always visible  |

#### Pet HP: Amethyst V-Arc (bright peak)

Amethyst Arc Pet HP palette. At full pet health: Conjured Violet. Depleting arcs through bright Arcane Bloom then fades dark.

| Band | Color Name        | RGB           | Hex     | Description                    |
| ---- | ----------------- | ------------- | ------- | ------------------------------ |
| 4    | Conjured Violet   | 200, 0, 200   | #C800C8 | Full Pet HP — drops first      |
| 3    | Spirit Amethyst   | 180, 60, 200  | #B43CC8 | 60% — settling                 |
| 2    | Arcane Bloom      | 220, 100, 240 | #DC64F0 | 40% — luminous peak            |
| 1    | Twilight Shade    | 170, 50, 180  | #AA32B4 | 20% — dimming                  |
| 0    | Deep Grape        | 120, 20, 120  | #781478 | Critical — dark, always visible|

#### Group HP: Tempered Red Veil (linear fade to white, dimmed)

Tempered variant of Red Veil for group member HP. Uses R=220 (vs 255 for player) to
visually distinguish group members from the player's own HP gauge.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Tempered Red      | 220, 0, 0     | #DC0000 | Full HP — drops first      |
| 3    | Smoldering Red    | 220, 50, 50   | #DC3232 | 60%                        |
| 2    | Warming Red       | 220, 100, 100 | #DC6464 | 40%                        |
| 1    | Fading Red        | 220, 160, 160 | #DCA0A0 | 20%                        |
| 0    | Ashen Red         | 220, 210, 210 | #DCD2D2 | Critical — always visible  |

#### Breath: Cyan Veil (linear fade to white)

Breath meter palette. At full breath: Deep Aqua. Depleting lightens toward Frost Spray.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Deep Aqua         | 0, 240, 240   | #00F0F0 | Full breath — drops first  |
| 3    | Shallow Aqua      | 50, 240, 240  | #32F0F0 | 60%                        |
| 2    | Tidal Aqua        | 100, 240, 240 | #64F0F0 | 40%                        |
| 1    | Sea Mist          | 160, 240, 240 | #A0F0F0 | 20%                        |
| 0    | Frost Spray       | 210, 240, 240 | #D2F0F0 | Critical — always visible  |

#### SpellBook Scribe: Gold Veil (linear fade to white)

SpellBook scribe progress gauge. At full: Ancient Gold. Depleting lightens toward Aureate Glow.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Ancient Gold      | 210, 110, 0   | #D26E00 | Full scribe — drops first  |
| 3    | Molten Script     | 240, 140, 0   | #F08C00 | 60%                        |
| 2    | Gilded Quill      | 255, 170, 40  | #FFAA28 | 40%                        |
| 1    | Sunlit Parchment  | 255, 200, 100 | #FFC864 | 20%                        |
| 0    | Aureate Glow      | 255, 230, 160 | #FFE6A0 | Starting — always visible  |

#### SpellBook Memorize: Sapphire Veil (cool blue gradient)

SpellBook memorize progress gauge. At full: Abyssal Cyan. Depleting lightens toward Frostlight.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Abyssal Cyan      | 0, 120, 210   | #0078D2 | Full memorize — drops first|
| 3    | Deep Tide         | 0, 150, 240   | #0096F0 | 60%                        |
| 2    | Crystal Current   | 40, 180, 255  | #28B4FF | 40%                        |
| 1    | Arctic Glow       | 100, 210, 255 | #64D2FF | 20%                        |
| 0    | Frostlight        | 170, 235, 255 | #AAEBFF | Starting — always visible  |

#### Nillipuss Classic (Green-Yellow-Red)

The original Nillipuss community palette. Traffic-light inspired: green at full, red at critical.
Available as **Player Option only** — not used in other windows.

| Band | Color Name        | RGB           | Hex     | Description                |
| ---- | ----------------- | ------------- | ------- | -------------------------- |
| 4    | Verdant           | 0, 240, 0     | #00F000 | Full — drops first         |
| 3    | Greenleaf Gold    | 173, 255, 47  | #ADFF2F | 60%                        |
| 2    | Sunstone          | 240, 240, 0   | #F0F000 | 40%                        |
| 1    | Pyre Orange       | 240, 102, 0   | #F06600 | 20%                        |
| 0    | Bloodfire         | 240, 0, 0     | #F00000 | Critical — always visible  |

> **Band 4 identity rule**: Both palette variants for the same EQType MUST share the same Band 4 color.
> Band 4 represents "full value" — the visual identity of the gauge at 100%. When comparing
> Purple Veil vs Amethyst Arc, both use Conjured Violet (200,0,200) for Band 4.

#### Composite Gauge Deployment

| Window         | Gauge        | Palette           | Size  | EQType | Texture Set |
| -------------- | ------------ | ----------------- | ----- | ------ | ----------- |
| PlayerWindow   | Player HP    | Red Veil          | 120t  | 1      | 120t        |
| PlayerWindow   | Player Mana  | Blue Veil         | 120t  | 2      | 120t        |
| PlayerWindow   | Pet HP       | Purple Veil       | 120t  | 16     | 120t        |
| TargetWindow   | Target HP    | Red Veil          | 250t  | 6      | 250t        |
| GroupWindow     | Member 1-5   | Tempered Red Veil | 120t  | 11-15  | 120t        |
| PetInfoWindow  | Pet HP       | Purple Veil       | 120t  | 16     | 120t        |
| BreathWindow   | Breath       | Cyan Veil         | 120t  | 8      | 120t        |
| SpellBookWnd   | Scribe       | Gold Veil         | 105t  | 10     | 105t        |
| SpellBookWnd   | Memorize     | Sapphire Veil     | 105t  | 9      | 105t        |

> **Options variants** (Player Options only): Fire Arc (HP), Ocean Arc (Mana),
> Amethyst Arc (Pet HP), Nillipuss Classic (HP). These are alternatives to the
> standard Veil palettes, selectable per-player via Options directory.

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

| Font ID | Size (approx) | Usage                            |
| ------- | ------------- | -------------------------------- |
| 0       | Small         | Tooltips, secondary info         |
| 1       | Small         | Compact labels                   |
| 2       | Medium        | Standard labels                  |
| 3       | Medium        | **Default for most UI elements** |
| 4       | Large         | Button text, section headers     |
| 5       | Large         | Title bars, window names         |

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

- Pet elements: Purple family (`200, 80, 200`)
- Player HP: Always red (`255, 0, 0`)
- Player Mana gauge fill: `30, 30, 255` (value text remains `100, 150, 255`)
- No custom colors unless documented in this standard

---

## 📚 Documentation Organization Standards

> **Recommended as of February 2026** - Managing growing documentation complexity

### When to Split DEVELOPMENT.md

Consider restructuring when documentation exceeds **2000 lines** or **8+ major phases**.

**Current Structure (February 2026)**:

```
.docs/
├── STANDARDS.md                 # This file
├── technical/
│   ├── EQTYPES.md
│   ├── ZEAL-FEATURES.md
│   └── README.md

.development/
├── initial_phases/
│   ├── PHASE-3.9-INVENTORY-REDESIGN.md
│   └── PHASE-5-TARGET-WINDOW.md
├── archive/              # Archived phase docs
└── README.md
```

**Cross-Linking Pattern**:

```markdown
<!-- Master index -->

### [Phase 3.9](../.development/initial_phases/PHASE-3.9-INVENTORY-REDESIGN.md)

**Status**: PLANNED | [Full Documentation →](../.development/initial_phases/PHASE-3.9-INVENTORY-REDESIGN.md)

<!-- Phase file -->

# Phase 3.9: Inventory Window Redesign

[← Back to Development Guide](DEVELOPMENT.md#phases)
```

**Benefits**: Easier navigation, focused docs, better GitHub UI  
**Drawbacks**: More files, link maintenance, git history fragmentation

**Current Status**: ✅ **Completed February 2026** - DEVELOPMENT.md reorganized
from 1961 → 412 lines (79% reduction). Documentation now modular with
user-facing docs in `.docs/` and working docs in `.development/`.

---

## 📊 EQType Reference

Bindings discovered and verified for TAKP:

| EQType | Binding         | Notes                           |
| ------ | --------------- | ------------------------------- |
| 1      | Player HP       | Red gauge, displays health      |
| 2      | Player Mana     | Blue gauge, displays mana/power |
| 11-21  | Group Member HP | One per group member slot       |
| 35-39  | Group HP Labels | Current/max health text display |
| 16     | Pet HP          | Pet health, purple color        |
| 17     | Pet Mana        | Pet stamina/mana, blue color    |
| 69     | Pet HP Label    | Pet health value display        |

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
