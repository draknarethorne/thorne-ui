# Player Window - Standard Variant

**File**: [EQUI_PlayerWindow.xml](./EQUI_PlayerWindow.xml)
**Version**: 1.0.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Standard - Balanced player stats layout  
**Author**: Draknare Thorne

---
## Purpose

The "Standard" Player Window variant displays core character statistics (HP, Mana, Stamina, XP) in a balanced, vertically-stacked gauge layout. This is the foundational Player window layout, optimized for consistent information display without specialized focus on pet or AA stats.

**Key Features**:

- **Quad-Gauge Primary Display**: HP (Red), Mana (Blue), Stamina (Yellow), XP (Green)
- **Full Player Info**: Character name, class, and level display
- **Percentage Indicators**: Real-time percentage displays for all major gauges
- **Mana Regeneration Display**: Cyan tick counter for meditation tracking
- **Compact Footprint**: Optimized for sidebar or bottom placement
- **Attack Indicator**: Visual border changes during combat engagement
- **Auto-Update**: EQType-driven gauge updates (no manual refresh needed)

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 224 × 120 pixels (typical, non-resizable) |
| Layout Type | Vertical gauge stack (Cornerstone design) |
| Resizable | No |
| Sizable | No |
| Titlebar | Hidden (WDT_RoundedNoTitle) |
| Closebox | Yes (collapsing to hide) |
| Minimizebox | Optional |
| Default Position | X=50, Y=100 |
| Gauge Count | 4 primary (HP, Mana, Stamina, XP) |
| Text Color (Primary) | RGB(255, 255, 255) - White |
| Font | Font 2 (consistent with Actions/Group) |
| Attack Border | Black outline during combat (visual indicator) |

---

## Visual Layout - Standard Configuration

```
┌──────────────────────────────────────┐
│ Player Name        Class      Lv60   │  Y=0px
├──────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░    100%        │  Y=18px (HP Gauge, Red)
│ HP: 1,234 / 1,234                    │
├──────────────────────────────────────┤
│ ▓▓▓▓▓░░░░░░░░░░░░░░░     80%        │  Y=35px (Mana Gauge, Blue)
│ Mana: 987 / 1,100                    │
├──────────────────────────────────────┤
│ ▓▓░░░░░░░░░░░░░░░░░░░░    15%       │  Y=52px (Stamina, Yellow)
├──────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░     65%       │  Y=69px (XP, Green)
│ [Mana Tick: ✓✓✓░░] Regen: 12s       │
└──────────────────────────────────────┘
```

---

## Element Inventory

### Header Section

| Element | ScreenID | Type | Position | Size | Purpose |
|---------|----------|------|----------|------|---------|
| Player Name | PW_PlayerName | Label | (5, 3) | 90×12px | Character name (white, left-aligned) |
| Player Class | PW_PlayerClass | Label | (97, 3) | 60×12px | Class name display |
| Player Level | PW_PlayerLevel | Label | (160, 3) | 30×12px | Level number (right-aligned, e.g., "60") |

### Primary Gauges (Standard Stack)

| Element | ScreenID | EQType | Position | Size | Fill Color | Purpose |
|---------|----------|--------|----------|------|------------|---------|
| HP Gauge | PW_Gauge_HP | 1 | (2, 18) | 160×15px | Red (255, 0, 0) | Health progression (primary) |
| HP Percent | PW_HP_Pct | 19 | (165, 18) | 30×12px | White | HP as percentage |
| HP Values | PW_HP_Values | 70 | (2, 29) | 100×10px | Red-tinted (255, 100, 100) | Current/Max HP display |
| Mana Gauge | PW_Gauge_Mana | 2 | (2, 35) | 160×15px | Blue (30, 30, 255) | Mana progression |
| Mana Percent | PW_Mana_Pct | 20 | (165, 35) | 30×12px | White | Mana as percentage |
| Mana Values | PW_Mana_Values | 80 | (2, 46) | 100×10px | Blue-tinted (100, 150, 255) | Current/Max Mana display |
| Stamina Gauge | PW_Gauge_Stamina | 3 | (2, 52) | 160×15px | Yellow (255, 255, 0) | Stamina depletion indicator |
| Stamina Pct | PW_Stamina_Pct | (calc) | (165, 52) | 30×12px | White | Stamina percentage |
| XP Gauge | PW_Gauge_XP | 4 | (2, 69) | 160×12px | Green (0, 200, 0) | Experience progression |
| XP Percent | PW_XP_Pct | (calc) | (165, 69) | 30×12px | White | XP as percentage to level |

### Support Elements

| Element | ScreenID | EQType | Position | Size | Purpose |
|---------|----------|--------|----------|------|---------|
| Mana Tick Display | ManaTick | 24 | (2, 62) | 160×8px | Cyan indicator ticks (regen) |
| Mana Regen Label | PW_Value_ManaTick | — | (2, 73) | 200×8px | Text: "Regen: XXs" |

---

## Color Scheme - Standardized Across UI

**Primary Gauge Colors** (consistent with all Thorne UI windows):
- **HP**: RED RGB(255, 0, 0) - Highest priority alert
- **Mana**: THORNE BLUE RGB(30, 30, 255) or RGB(100, 150, 255) - Secondary resource
- **Stamina**: YELLOW RGB(255, 255, 0) - Endurance tracking
- **XP**: Green RGB(0, 200, 0) - Progression indicator
- **Mana Tick**: Cyan RGB(0, 220, 220) - Regen timer visual

**Text Colors**:
- Primary labels: White RGB(255, 255, 255)
- HP values: Red-tinted RGB(255, 100, 100)
- Mana values: Blue-tinted RGB(100, 150, 255)
- Status text: Light gray RGB(200, 200, 200)

---

## Technical Details

### EQType Mappings

- **1**: Player HP (current/max, triggers PW_Gauge_HP fill)
- **2**: Player Mana (current/max, triggers PW_Gauge_Mana fill)
- **3**: Stamina (current/max, triggers PW_Gauge_Stamina fill)
- **4**: Experience (current/next level, triggers PW_Gauge_XP fill)
- **19**: HP percentage (calculated, displays in PW_HP_Pct)
- **20**: Mana percentage (calculated, displays in PW_Mana_Pct)
- **24**: Mana regen ticks / countdown timer (updated each regen pulse)
- **70**: HP value display (e.g., "1234/1234")
- **80**: Mana value display (e.g., "987/1100")

### Gauge Draw System

All gauges use Thorne standardized draw templates:
- **Background**: Recessed groove effect (A_GaugeBackground_Tall for 15px, shorter for others)
- **Fill Animation**: Color-filled portion proportional to current/max ratio
- **No Overlay Lines**: Smooth appearance (grid lines disabled)

### Attack Border Behavior

- When engaged in combat, window border changes to darker color
- Indicates active threat level via DrawTemplate state
- Returns to normal upon combat disengagement

---

## Comparison with Other Player Variants

| Feature | Standard | Pet Bottom | AA and XP Bottom | Default |
|---------|----------|-----------|------------------|---------|
| **Gauges** | HP/Mana/Stamina/XP | All 4 + Pet HP | HP/Mana/Stamina + AA/XP (dual) | All 5 (compact) |
| **Pet Display** | None | Bottom, tall (15px) | None | Small (3px bottom) |
| **AA Display** | None | None | Separate gauge section | Integrated (small) |
| **Window Height** | ~85px | ~140px | ~150px | ~95px |
| **Best For** | General play | Pet classes | AA grinders | Minimal footprint |

---

## Modifications & Customization

### V1.0.0 Baseline (Current)
- Established standard quad-gauge layout
- Synchronized colors with Actions/Target/Group windows
- Implemented EQType-driven auto-update

### Future Enhancement Ideas
- Optional buff/debuff panel integration
- Customizable gauge order (drag-and-drop)
- Expandable sections for situational displays
- Pet/Target mini-gauges (if summoned/targeted)

---

## Installation

1. Copy `EQUI_PlayerWindow.xml` from this directory
2. Paste to `thorne_drak/` main directory (replacing existing)
3. Restart EverQuest or run `/loadskin thorne_drak`

**Backup Existing Config:**
```bash
# From within Options/Player/Standard directory:
cp EQUI_PlayerWindow.xml EQUI_PlayerWindow.xml.backup
cp EQUI_PlayerWindow.xml ../../
```

---

## Usage & Testing

1. **Verify Display**: Check that all 4 gauges show current values
2. **Combat Test**: Engage enemy, verify border darkens
3. **Regen Display**: Cast spell, verify Mana:Tick counter counts down
4. **Consistency**: Compare gauge colors with Actions/Target windows

---

## Integration Notes

**Coordinates with:**
- Actions Window (EQUI_ActionsWindow.xml) - can dock to same edge
- Target Window (EQUI_TargetWindow.xml) - mirrors player gauge colors
- Group Window (EQUI_GroupWindow.xml) - consistent layout philosophy

**Cross-Reference**:
- For Pet-focused variant, see [Pet Bottom](../Pet%20Bottom/README.md)
- For AA-grinding focus, see [AA and XP Bottom](../AA%20and%20XP%20Bottom/README.md)
- For ultra-compact view, see [Default](../Default/README.md)

---

**Version**: 1.0.0 | **Last Updated**: February 3, 2026 | **Status**: ✅ Active
## Reverting

To revert the Player Notes window to default, replace with the original `EQUI_PlayerNotesWindow.xml` from the base UI.

**For Main Player Window Variants**: See other Options/Player subdirectories:
- [Pet Bottom](../Pet%20Bottom/README.md)
- [AA and XP Bottom](../AA%20and%20XP%20Bottom/README.md)

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Pet Bottom](../Pet%20Bottom/README.md), [AA and XP Bottom](../AA%20and%20XP%20Bottom/README.md)  
**Note**: This variant contains the Player **Notes** window, not the main Player window
