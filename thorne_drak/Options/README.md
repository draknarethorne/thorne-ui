# UI Window Options Directory

**Location**: `thorne_drak/Options/`  
**Version**: 1.1.0  
**Last Updated**: February 3, 2026  
**Status**: ✅ Complete with 6 synchronized window options and dual toolbar layouts  
**Author**: Draknare Thorne

---

## Overview

The Options directory contains curated UI variants for core player-facing windows. Each option combines consistent styling, positioning, and color schemes while allowing players to choose layouts that best suit their playstyle and screen real estate constraints.

**Included Options**:
- 4 player-focused stat/status windows (Group, Target, Pet, Player)
- Window Selector toolbar with 2 layout variants (Standard horizontal, Vertical)

**Design Philosophy**: All window options share common visual language (colors, text offsets, gauge heights) to ensure seamless integration while providing meaningful layout alternatives for different player preferences.

---

## Available Window Options

### 1. **Group Window - Standard**

**Directory**: `thorne_drak/Options/Group/Standard/`

Display real-time health and mana information for 5-member groups (F2-F6 raid targets).

**Key Specifications**:
- **Group Gauge Positions**: X=11 (left-aligned for compact layout)
- **Health Value Position**: X=82 (consistent across all windows)
- **Percentage Position**: X=142 (standard alignment)
- **Gauge Heights**: 24px (full-height for clear visibility at group distances)
- **Styling**: Dark green group borders with red HP gauges

**Use Case**:
- Primary group window for all playstyles
- Recommended as standard baseline configuration
- Optimal for raid/group play with consistent health monitoring

**Files**:
- `EQUI_GroupWindow.xml` - Main window definition
- `README.md` - Detailed specifications

**Status**: ✅ v1.1.0 (Feb 3, 2026)

---

### 2. **Target Window - Player Gauges and Weight**

**Directory**: `thorne_drak/Options/Target/Player Gauges and Weight/`

Display comprehensive target information with player stats overlay and **EXPERIMENTAL** weight display feature.

**Key Specifications**:
- **Player HP Gauge**: Red bar at Y=16, 122×15px (EQType 1)
- **Player Mana Gauge**: Blue bar at Y=16, 122×15px (EQType 2)
- **Weight Display** (EXPERIMENTAL): 
  - Current: X=99, Y=12, Font 2, AlignRight (EQType 24)
  - Divider: "/" at X=123, Y=12, centered
  - Max: X=129, Y=12, Font 2, AlignLeft (EQType 25)
  - **Note**: Requires testing to determine utility/UX impact
- **Window Size**: 260px wide (accommodates weight display)
- **Styling**: Player stats overlay with dual gauges for HP/Mana tracking

**Use Case**:
- Combat targeting with real-time player resource visibility
- **EXPERIMENTAL FEATURE**: Weight display pending community feedback
- Ideal for tanks, melee DPS, and control-focused casters

**Files**:
- `EQUI_TargetWindow.xml` - Main window definition
- `README.md` - Comprehensive specifications including experimental features

**Status**: ✅ v1.1.0 (Feb 3, 2026 - NEW)
**Note**: Weight display is experimental. Decision on inclusion pending v0.6.0 testing.

---

### 3. **Pet Window - Tall Gauge**

**Directory**: `thorne_drak/Options/Pet/Tall Gauge/`

Display active pet hitpoints with large, readable HP gauge and white pet name text.

**Key Specifications**:
- **Pet HP Gauge**: Purple, 15px tall (EQType 16)
- **Pet Name Text**: White (RGB 255,255,255) - high contrast
- **Text Offset**: X=4, Y=0 (standardized across pet implementations)
- **Gauge Fill Color**: Purple (RGB 200,80,200)
- **Window Size**: Compact design suitable for hotbar integration
- **Styling**: Clean, minimal, pet-focused information display

**Use Case**:
- Primary pet control window for all pet classes
- High visibility for pet health during combat
- Recommended for actual pets (not just mercs)

**Files**:
- `EQUI_PetInfoWindow.xml` - Main window definition
- `README.md` - Detailed specifications

**Status**: ✅ v1.1.0 (Feb 3, 2026)

---

### 4. **Player Window - Pet Bottom**

**Directory**: `thorne_drak/Options/Player/Pet Bottom/`

Display character stats with pet health gauge positioned at window bottom.

**Key Specifications**:
- **Player Gauges**: HP, Mana, Stamina, XP (standard positions)
- **Pet HP Gauge**: Bottom position (Y≈111), purple, 15px tall
- **Pet Name Text**: White (RGB 255,255,255)
- **Text Offset**: X=4, Y=0 (matches Pet Window)
- **Alignment**: Pet gauge positions match Group/Target windows for consistency
  - HP values: X=82
  - Percentages: X=142
- **Window Type**: Full character stats view with pet integration

**Use Case**:
- Primary player stats window for all playstyles
- Recommended for pet classes to monitor pet health without separate window
- Maintains main player stat visibility while tracking pet health

**Files**:
- `EQUI_PlayerWindow.xml` - Main window definition
- `README.md` - Detailed specifications

**Status**: ✅ v1.1.0 (Feb 3, 2026)

---

### 5. **Window Selector - Standard**

**Directory**: `thorne_drak/Options/Selector/Standard/`

Quick-access toolbar for toggling major UI windows (Actions, Inventory, Options, Friends, Hotbuttons, Spells, Pet Info, Effects, Help).

**Key Specifications**:
- **Layout**: Horizontal (9 buttons left-to-right)
- **Window Size**: 278×50 pixels
- **Button Size**: 26×26 pixels each
- **Button Spacing**: 30 pixels (6px gap)
- **Position**: Top-center of screen (X=135, Y=0)
- **Button Order**: Actions → Inventory → Options → Friends → Hotbuttons → Spells → Pet Info → Buffs → Help

**Use Case**:
- Quick window access during gameplay
- Alternative to keyboard hotkeys
- Persistent toolbar on top of screen

**Files**:
- `EQUI_SelectorWnd.xml` - Main window definition
- `README.md` - Complete specifications and future vertical variant plans

**Status**: ✅ v1.0.0 (Feb 3, 2026 - Horizontal baseline)

---

### 6. **Window Selector - Vertical**

**Directory**: `thorne_drak/Options/Selector/Vertical/`

Vertical quick-access toolbar for toggling major UI windows with compact, space-efficient design.

**Key Specifications**:
- **Layout**: Vertical (9 buttons top-to-bottom)
- **Window Size**: 38×278 pixels (narrow and tall)
- **Button Size**: 26×26 pixels each
- **Button Spacing**: 30 pixels vertical (4px gap)
- **Button Inset**: 2px from left and top edges
- **Position**: X=100, Y=100 (adjustable)
- **Titlebar**: None (WDT_RoundedNoTitle)
- **Closebox**: Yes
- **Button Order**: Actions → Inventory → Options → Friends → Hotbuttons → Spells → Pet Info → Buffs → Help (top to bottom)

**Use Case**:
- Vertical UI layouts with limited horizontal space
- Sidebar placement alongside Group/Pet/Actions windows
- Compact toolbar for narrow screen arrangements

**Files**:
- `EQUI_SelectorWnd.xml` - Main window definition
- `README.md` - Complete vertical layout specifications

**Status**: ✅ v1.1.0 (Feb 3, 2026 - Vertical implementation)

---

## Cross-Window Consistency

### Shared Visual Language (v1.1.0)

All four window options maintain consistent styling to provide cohesive UI experience:

| Property | Standard Value | Windows |
|----------|-----------------|---------|
| **Pet Gauge Color** | Purple RGB(200,80,200) | Pet, Player, Target (if pet) |
| **Pet Name Text Color** | White RGB(255,255,255) | All pet gauges |
| **Pet Text Offset** | X=4, Y=0 | Pet, Player |
| **HP Value Position** | X=82 | Group, Player, Target |
| **Percentage Position** | X=142 | Group, Player, Target |
| **HP Bar Color** | Red RGB(255,0,0) | All windows |
| **Mana Bar Color** | Blue RGB(100,150,255) | Player, Target |

### Positioning Alignment

```
Across Player/Target/Group/Pet Windows:
┌─────────────────────────────────┐
│ [Pet Gauge 120px wide, 15px high]
│ [HP Value X=82] [HP% X=142]
└─────────────────────────────────┘
```

### Synchronized Updates (v1.1.0)

All windows updated simultaneously to ensure consistency:

1. **Feb 3, 2026**: Pet name text color standardized to white across all implementations
2. **Feb 3, 2026**: Text offset standardized (TextOffsetY: 1→0 in all pet gauges)
3. **Feb 3, 2026**: Target window weight display added (experimental)
4. **Feb 3, 2026**: Group window positioning optimized (gauges X=11, labels X=82/142)

---

## How Options Work

### Directory Structure

```
thorne_drak/
├── Options/
│   ├── Group/
│   │   └── Standard/
│   │       ├── EQUI_GroupWindow.xml
│   │       └── README.md
│   ├── Target/
│   │   ├── Standard/
│   │   │   ├── EQUI_TargetWindow.xml
│   │   │   └── README.md
│   │   └── Player Gauges and Weight/       (NEW in v1.1.0)
│   │       ├── EQUI_TargetWindow.xml
│   │       └── README.md
│   ├── Pet/
│   │   ├── Standard/
│   │   │   ├── EQUI_PetInfoWindow.xml
│   │   │   └── README.md
│   │   └── Tall Gauge/
│   │       ├── EQUI_PetInfoWindow.xml
│   │       └── README.md
│   ├── Player/
│   │   ├── AA and XP Bottom/
│   │   │   ├── EQUI_PlayerWindow.xml
│   │   │   └── README.md
│   │   └── Pet Bottom/
│   │       ├── EQUI_PlayerWindow.xml
│   │       └── README.md
│   └── Selector/                            (NEW in v1.1.0)
│       ├── Standard/                        (Horizontal layout)
│       │   ├── EQUI_SelectorWnd.xml
│       │   └── README.md
│       └── Vertical/                        (Vertical layout)
│           ├── EQUI_SelectorWnd.xml
│           └── README.md
└── README.md                                (this file)
```

### Usage

Each window option is a complete, standalone variant. To use different options:

1. **Select Desired Windows**: Choose which options best fit your playstyle
2. **Copy Files**: Copy relevant XML files from desired options to your UI folder
3. **Load Skin**: `/loadskin thorne_drak` to apply changes
4. **Test**: Verify positioning and appearance in-game

### Option Combinations

These options are designed to work together seamlessly:

**Recommended Combo for Pet Classes**:
- Group Window: **Standard** - Always use baseline group configuration
- Target Window: **Player Gauges and Weight** - Track target player stats
- Pet Window: **Tall Gauge** - Monitor pet health
- Player Window: **Pet Bottom** - See player stats + pet health in one window

**Recommended Combo for Non-Pet Classes**:
- Group Window: **Standard** - Group health monitoring
- Target Window: **Standard** - Basic target info (no player gauges)
- Player Window: **AA and XP Bottom** - Standard player stats

**Hybrid Setup**:
- Use **Standard** options for group/target windows
- Swap **Pet Bottom** player window when playing pet class
- Return to **AA and XP Bottom** for non-pet classes

---

## Experimental Features

### Target Window Weight Display

**Status**: EXPERIMENTAL (v1.1.0)  
**Location**: `Options/Target/Player Gauges and Weight/`  
**Decision Point**: Remove/redesign before v0.6.0 final release

**Purpose**: Display player weight burden in combat context for inventory awareness.

**Specifications**:
- Current weight: EQType 24, X=99, Y=12, Font 2, AlignRight
- Max weight: EQType 25, X=129, Y=12, Font 2, AlignLeft
- Divider: "/" at X=123, Y=12, centered
- Window width adjusted to 260px to accommodate

**Feedback Criteria**:
- Visual impact on target window usability
- Information usefulness during combat
- Alternative placement/presentation ideas

**Next Steps**:
- Community testing during v0.6.0 development
- Evaluate utility vs. visual clutter
- Decide inclusion in final v0.6.0 release
- Archive experimental feature if not proceeding

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | Feb 3, 2026 | Synchronized pet gauge styling (white text), added Target weight option, added Selector vertical layout, standardized positioning |
---

## Modification & Maintenance

### Adding New Options

To create a new window option variant:

1. **Create Directory**: `Options/<WindowType>/<VariantName>/`
2. **Copy Base File**: Use base `thorne_drak/EQUI_*.xml` as template
3. **Modify XML**: Customize positioning/colors as needed
4. **Create README.md**: Follow [window-specific README format](#readme-template)
5. **Test**: Verify in EverQuest before committing

### Updating Existing Options

When making cross-option updates:

1. **Identify All Affected Options** using file search
2. **Apply Changes** consistently across similar windows
3. **Update Version Number** in each README
4. **Document Changes** in modification history
5. **Test All Variants** before committing

### Color/Position Standardization

Maintain visual consistency by adhering to established values:
- Pet text color: RGB(255,255,255) for all pet gauges
- Pet gauge color: RGB(200,80,200) across all windows
- HP value X position: X=82 (Group, Player, Target)
- Percentage X position: X=142 (Group, Player, Target)

---

## README Template

Each option should include a dedicated README.md following this structure:

```markdown
# [Window Name] - [Variant Name]

**File**: Path and filename  
**Version**: X.Y.Z  
**Last Updated**: Date  
**Status**: ✅ [State]  
**Author**: Draknare Thorne

---

## Purpose
[Brief description of window purpose and use case]

---

## Specifications
[Table of positioning, sizing, colors, EQTypes]

## Key Modifications
[List of changes from base or previous version]

## Configuration
[How to load this option]

## See Also
[Links to related options and windows]
```

---

## Support & Documentation

**Main Documentation**:
- [Thorne UI Project README](../../README.md) - Project overview
- [Roadmap](../../.docs/ROADMAP.md) - Development phases
- [Release Notes](../../.docs/VERSION-MANAGEMENT.md) - Version information

**Window-Specific Docs**:
- [Group Window - Standard](Group/Standard/README.md)
- [Target Window - Player Gauges and Weight](Target/Player%20Gauges%20and%20Weight/README.md)
- [Pet Window - Tall Gauge](Pet/Tall%20Gauge/README.md)
- [Player Window - Pet Bottom](Player/Pet%20Bottom/README.md)
- [Window Selector - Standard](Selector/Standard/README.md)
- [Window Selector - Vertical](Selector/Vertical/README.md)

---

## Contact & Feedback

Options and variants are designed to support diverse playstyles. Feedback on existing options or suggestions for new variants are welcome during the v0.6.0 development cycle.

---

*Last Updated: February 3, 2026*  
*Author: Draknare Thorne*  
*Status: Phase 1 Complete - Ready for v0.6.0 Testing*
