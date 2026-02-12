# Window: Actions - Default Variant

**File**: [EQUI_ActionsWindow.xml](./EQUI_ActionsWindow.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Active - Comprehensive Tabbed Interface  
**Author**: Draknare Thorne

---
## Purpose

The Actions Window provides a comprehensive tabbed interface for accessing player abilities, social commands, information windows, and combat features. Organized across four main tabs (Socials/Info/Abilities/Combat), this window integrates player stats, potion belt reminders, and ability management into a single resizable interface.

**Key Features**:
- **4-Tab Tabbed Interface**: Socials, Info, Abilities, Combat tabs
- **Social Commands Hub**: Organized social emote buttons with pagination
- **Information Access**: Quick links to game information windows
- **Combat Abilities**: Organized combat skill buttons and toggles
- **Integrated Player Stats**: HP, Mana, AC, ATK, Weight, AA display
- **Potion Belt Reminder**: Main tab features belt status on designated button
- **Resizable Design**: Collapses to minimal footprint when needed
- **Multi-Page Support**: Pagination controls for social command sets

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 150 × 300 pixels (typical, resizable) |
| **Layout Type** | Tabbed multi-section (Cornerstone, dockable) |
| **Resizable** | Yes (collapsible design) |
| **Sizable** | Yes |
| **Titlebar** | Yes - "Actions" |
| **Closebox** | Yes |
| **Minimizebox** | Yes |
| **Draw Template** | WDT_RoundedStandard |
| **Default Position** | X=200, Y=300 |
| **Tab Count** | 4 main tabs |
| **Buttons per Tab** | 8-20 variable |
| **Font** | Font 2-3 (size varies) |

---

## Visual Layout - Socials Tab (Active)

```
┌─────────────────────────────────────────┐
│ [◄ 1 ►]  Socials    Info  Abilities    │  Tab bar (Y=0-22px)
├─────────────────────────────────────────┤
│ [  Sit      ] [  Down      ]           │  Y=20-40px
│ [  Stand    ] [  Afk       ]           │  Y=40-60px
│ [  Bow      ] [  Cheer     ]           │  Y=60-80px
│ [  Laugh    ] [  Wave      ]           │  Y=80-100px
│ [  Dance    ] [  Emote1    ]           │  Button grid continues
│ [  Salute   ] [  Emote2    ]           │
│                                         │
└─────────────────────────────────────────┘
```

---

## Element Inventory

### Tab Navigation Bar

| Element | ScreenID | Position | Size | Purpose |
|---------|----------|----------|------|---------|
| Socials Tab Left | ASP_SocialPageLeftButton | (16, 3) | 22×12px | Previous page arrows |
| Tab Count Label | ASP_CurrentSocialPageLabel | (50, 1) | 36×22px | "1" (current page indicator) |
| Socials Tab Right | ASP_SocialPageRightButton | (97, 3) | 22×12px | Next page arrows |
| Info Tab Button | ASP_InfoTabButton | (varies) | ~50×20px | Info tab toggle |
| Abilities Tab Button | ASP_AbilitiesTabButton | (varies) | ~50×20px | Abilities tab toggle |
| Combat Tab Button | ASP_CombatTabButton | (varies) | ~50×20px | Combat tab toggle |

### Social Buttons (Repeating Grid - Socials Tab)

| Button | ScreenID | Position | Size | Purpose |
|--------|----------|----------|------|---------|
| Social 1 | ASP_SocialButton1 | (7, 20) | 64×20px | Social command button 1 |
| Social 2 | ASP_SocialButton2 | (7, 40) | 64×20px | Social command button 2 |
| Social 3 | ASP_SocialButton3 | (7, 60) | 64×20px | Social command button 3 |
| Social 4 | ASP_SocialButton4 | (7, 80) | 64×20px | Social command button 4 |
| Social 7 | ASP_SocialButton7 | (74, 20) | 64×20px | Social command button 5 (offset) |
| Social 8 | ASP_SocialButton8 | (74, 40) | 64×20px | Social command button 6 (offset) |
| Social 9 | ASP_SocialButton9 | (74, 60) | 64×20px | Social command button 7 (offset) |
| Social 10 | ASP_SocialButton10 | (74, 80) | 64×20px | Social command button 8 (offset) |

**Grid Layout**:
- Left column: X=7, buttons at 20px intervals vertically
- Right column (offset): X=74, mirrors left column layout
- 2×4 grid configuration (8 visible buttons per page)

### Player Stats Section (Info Tab - Integrated)

| Element | ScreenID | EQType | Purpose |
|---------|----------|--------|---------|
| HP Display | ASP_PlayerHP | 1 | Current/Max health |
| Mana Display | ASP_PlayerMana | 2 | Current/Max mana |
| AC Value | ASP_PlayerAC | 60 | Armor Class indicator |
| ATK Value | ASP_PlayerATK | 61 | Attack power |
| Weight Display | ASP_PlayerWeight | 24/25 | Current/Max burden |
| AA Points | ASP_PlayerAA | 71 | Alternate Advancement counter |

### Potion Belt Reminder (Main/Socials Tab)

| Element | ScreenID | Position | Size | Purpose |
|---------|----------|----------|------|---------|
| Belt Reminder | ASP_BeltReminderButton | (varies) | 50×20px | Visual indicator for belt status |
| Belt Tooltip | — | — | — | Reminds to use belt items |

---

## Color Reference

**Button States**:
- **Normal**: Dark gray background, white text
- **Pressed**: Inverse colors, indicates active state
- **Flyby**: Highlight on hover (gold/yellow tint)
- **Disabled**: Grayed out (unavailable while in-combat or specific game state)

**Text Colors**:
- Tab labels: RGB(255, 255, 255) - White
- Button text: RGB(255, 255, 255) - White
- Stat values: RGB(100, 200, 100) - Green for "in-range" values

---

## Technical Details

### Tab System Architecture

**Draw Templates** (per tab):
- Each tab button uses ButtonDrawTemplate with Normal/Pressed/Flyby/Disabled states
- Tab content swaps on button press (game client handles logic)
- All tabs share same screen space (272×280px content area)

### EQType Integration

- **EQType 1-5**: Primary stats (HP, Mana, AC, ATK, Weight)
- **EQType 60**: AC specialized display
- **EQType 61**: Attack power specialized display
- **EQType 71**: AA point counter

### Button Grid Configuration

**RelativePosition Strategy**:
- `RelativePosition=true` on all action buttons
- X-position determines column (7px for left, 74px for right)
- Y-position determines row (20px intervals)
- Relative positioning within tab container enables clean layouts

### Pagination System

**Socials Tab Navigation**:
- Left/Right arrow buttons scroll through social command pages
- Label displays current page number (e.g., "1", "2", "3")
- Game client manages page data loading
- Client limitation: Buttons 11-30 don't respond (hardcoded limitation)

---

## Related Windows & Dependencies

### Connected Windows
- **Player Window** (EQUI_PlayerWindow.xml): Provides player stat data source
- **Inventory Window** (EQUI_Inventory.xml): Tab system moved from inventory (Phase 3 refactor)
- **Merchant Window** (EQUI_MerchantWnd.xml): May reference actions for trading

### Standards References
- See STANDARDS.md for tabbed interface best practices
- See EQTYPES.md for EQType stat mappings
- Part of "Phase 1" and "Phase 3" Actions window development

---

## Recent Updates (v1.0.0)

**January-February 2026**:
- ✅ Comprehensive tabbed interface development (Socials/Info/Abilities/Combat)
- ✅ Integrated player stats display on Info tab
- ✅ Resizable design for flexible UI layouts
- ✅ Potion Belt reminder button on Main tab
- ✅ Standardized layout replacing inventory tab functionality
- ✅ Part of Phase 1 and Phase 3 Actions window development

**Known Limitations**:
- Client hardcoding limitation: Buttons 11-30 don't function
- Tab switching may have delay on lower-bandwidth connections
- Social commands limited to available player commands

---

## Developer Notes

**Modular Approach**: The Actions Window consolidates features previously scattered across multiple windows (Inventory tabs, Socials, Combat abilities). This centralization reduces UI clutter and improves discoverability.

**Pagination**: Socials tab pagination enables access to all social commands without massive window size. Players can page through command sets with arrow buttons.

**Future Enhancements**:
- Keyboard shortcuts for tab switching (Alt+1/2/3/4)
- Customizable button contexts
- Drag-and-drop ability binding
- Macro recording integration

---

**Version**: 1.0.0 | **Last Updated**: February 3, 2026 | **Status**: ✅ Active
