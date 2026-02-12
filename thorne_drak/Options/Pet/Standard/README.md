# Pet Window - Standard Variant

**File:** [EQUI_PetInfoWindow.xml](./EQUI_PetInfoWindow.xml)  
**Version:** 1.0.0  
**Last Updated:** February 1, 2026  
**Status:** ✅ Active - Taller HP Gauge Variant  
**Author:** Draknare Thorne

---

## Purpose
Standard pet window variant with a **taller HP gauge (24px)** for easier readability and a compact mana bar. This layout provides better visibility of pet health percentage at a glance while maintaining a clean, minimal footprint.

### Key Features:
- **Taller HP Gauge** - 24px height with percentage display and numeric HP value
- **Compact Mana Bar** - 2px thin line indicator below HP gauge
- **Full Pet Commands** - Attack, Follow, Taunt, Guard, Back, Sit, and Dismiss buttons
- **HP Value Display** - Right-aligned numeric HP and percentage labels
- **Dismiss Button** - Red "X" button to dismiss pet (Thorne UI addition)
- **Clean Layout** - Compact 160×125px window with no title bar

---

## Specifications

| Property | Value | Description |
|----------|-------|-------------|
| **Window Size** | 160 × 125px | Compact pet control window |
| **Window Position** | X=1, Y=1 | Default spawn position |
| **Title Bar** | No | Clean, borderless design |
| **Sizable** | No | Fixed dimensions |
| **Border** | Yes | Rounded border style |
| **DrawTemplate** | WDT_RoundedNoTitle | Rounded corners, no title |
| **HP Gauge Height** | 24px | **Taller** for better readability |
| **Mana Gauge Height** | 2px | Thin compact indicator |
| **Total Buttons** | 7 | Attack, Follow, Taunt, Guard, Back, Sit, Dismiss |

---

## Layout Overview

### Component Hierarchy
```
PetInfoWindow (160×125px)
├── PIW_PetHPGauge (128×24px at X=3, Y=3)
│   └── HP text overlay + fill bar
├── PIW_PetManaGauge (128×2px at X=3, Y=27)
│   └── Thin mana indicator
├── PIW_Pet_HPLabel (60×12px at X=74, Y=16)
│   └── Numeric HP value (right-aligned)
├── PIW_Pet_HPPercLabel (16×12px at X=136, Y=16)
│   └── "%" symbol
├── PIW_LostButton (28×6px at X=130, Y=23)
│   └── Red "X" dismiss button
├── PIW_AttackButton (154×20px at X=2, Y=32)
├── PIW_FollowButton (77×20px at X=2, Y=53)
├── PIW_TauntButton (77×20px at X=79, Y=53)
├── PIW_GuardButton (77×20px at X=2, Y=74)
├── PIW_BackButton (77×20px at X=79, Y=74)
└── PIW_SitButton (154×20px at X=2, Y=95)
```

### Visual Layout (Standard - Tall Gauge)
```
┌──────────────────────────────────────┐
│  ┌──────────────────────────┐     X │  ← Dismiss (130,23)
│  │  Pet Name / HP Gauge     │  999% │  ← HP Gauge (3,3) 128×24px
│  │  ▓▓▓▓▓▓▓▓▓▓▓░░░░         │       │
│  └──────────────────────────┘       │
│  ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░                │  ← Mana (3,27) 128×2px
│                                      │
│  ┌────────── Attack ────────────┐   │  ← (2,32) 154×20px
│                                      │
│  ┌─── Follow ───┐ ┌─── Taunt ───┐   │  ← (2,53) & (79,53)
│                                      │
│  ┌─── Guard ────┐ ┌─── Back ────┐   │  ← (2,74) & (79,74)
│                                      │
│  ┌──────────── Sit ─────────────┐   │  ← (2,95) 154×20px
│                                      │
└──────────────────────────────────────┘
```

---

## Key Elements

### Gauges

| Element | Position | Size | EQType | FillTint (RGB) | Template |
|---------|----------|------|--------|----------------|----------|
| **HP Gauge** | X=3, Y=3 | 128×24px | 16 | (200,0,200) | A_GaugeBackground |
| **Mana Gauge** | X=3, Y=27 | 128×2px | 17 | (0,0,240) | A_GaugeBackground |

**HP Gauge Details:**
- **Text:** "No Pet" (bright green RGB 0,240,0)
- **TextOffset:** X=4, Y=1 (positioned in gauge)
- **GaugeOffset:** X=3, Y=0
- **FillTint:** Magenta RGB(200,0,200)
- **Template:** Standard gauge (A_GaugeBackground, A_GaugeFill, A_GaugeLines)

**Mana Gauge Details:**
- **Size:** Very thin 2px indicator
- **TextOffset:** Y=-50 (hidden text)
- **GaugeOffset:** X=3, Y=-2
- **FillTint:** Blue RGB(0,0,240)
- **LinesFillTint:** Cyan RGB(0,220,220)
- **Template:** Standard gauge (A_GaugeBackground, A_GaugeFill)

### HP Value Labels

| Element | Position | Size | Font | Alignment | Purpose |
|---------|----------|------|------|-----------|---------|
| **PIW_Pet_HPLabel** | X=74, Y=16 | 60×12px | 2 | Right-aligned | Numeric HP value |
| **PIW_Pet_HPPercLabel** | X=136, Y=16 | 16×12px | 2 | Left-aligned | "%" symbol |

**Added by Brujoloco** - Provides numeric HP readout alongside percentage in gauge.

### Control Buttons

| Button | Position | Size | Tooltip | Description |
|--------|----------|------|---------|-------------|
| **Attack** | X=2, Y=32 | 154×20px | "Pet Attack" | Attack current target |
| **Follow** | X=2, Y=53 | 77×20px | "Pet Follow Me" | Follow player |
| **Taunt** | X=79, Y=53 | 77×20px | "Pet Taunt" | Toggle taunt |
| **Guard** | X=2, Y=74 | 77×20px | "Pet Guard Here" | Guard location |
| **Back** | X=79, Y=74 | 77×20px | "Pet Back Off" | Stop attack, return |
| **Sit** | X=2, Y=95 | 154×20px | "Pet Sit Down" | Sit/stand toggle |
| **Dismiss** | X=130, Y=23 | 28×6px | "Pet Get Lost (Dismiss)" | Dismiss pet |

**Button Layout Pattern:**
- **Full-width buttons:** 154px (Attack, Sit)
- **Half-width buttons:** 77px (Follow/Taunt, Guard/Back)
- **Standard height:** 20px (all except Dismiss)
- **Dismiss button:** 28×6px, Font 1, Red text RGB(240,100,100)

### Dismiss Button (Thorne UI Addition)
- **Position:** X=130, Y=23 (top right corner)
- **Size:** 28×6px (small, intentional design)
- **Text:** "X" in red RGB(240,100,100)
- **Font:** 1 (small font)
- **Purpose:** Provides quick pet dismissal while being positioned away from Attack button to avoid accidental clicks
- **Tooltip:** "Pet Get Lost (Dismiss)"
- **Recent Change:** Moved up 2px (Y=25 → Y=23) to increase separation from Attack button

---

## Color Scheme

### HP Gauge
- **Fill Color:** Magenta RGB(200,0,200) - Bright purple-magenta
- **Text Color:** Bright Green RGB(0,240,0) - High contrast for "No Pet" message
- **Background:** Standard gauge background template

### Mana Gauge
- **Fill Color:** Blue RGB(0,0,240) - Standard blue mana
- **Lines Fill:** Cyan RGB(0,220,220) - Accent lines
- **Background:** Standard gauge background template

### Buttons
- **Text Color:** White RGB(255,255,255)
- **Templates:** Standard button states (Normal, Pressed, Flyby, Disabled, PressedFlyby)
- **Dismiss Button:** Red RGB(240,100,100) - Warning color for destructive action

### Labels
- **HP Value Labels:** White RGB(255,255,255)

---

## Behavior Notes

### Gauge Characteristics
- **HP Gauge:** Tall 24px height provides excellent readability
- **Mana Gauge:** Ultra-thin 2px line keeps window compact
- **Gauge Templates:** Uses standard templates (A_GaugeBackground, A_GaugeFill)
- **HP Display:** Shows both text percentage in gauge AND numeric value/percentage labels

### Button Layout
- **Two-column design:** Half-width buttons arranged in pairs
- **Full-width actions:** Attack (primary) and Sit at top and bottom
- **Dismiss button:** Small, top-right corner placement reduces accidental activation
- **Button separation:** 2px gap between Dismiss and Attack buttons (increased from previous 0px)

---

## Differences from Tall Gauge Variant

The **Standard** variant uses:
- **Taller HP Gauge:** 24px vs 15px (Tall Gauge)
- **Thinner Mana Gauge:** 2px vs 4px (Tall Gauge)
- **Different Gauge Y-positions:** HP at Y=3 (vs Y=4), Mana at Y=27 (vs Y=20)
- **Different Label Positions:** HP labels at Y=16 (vs Y=5 in Tall Gauge)
- **Standard Gauge Templates:** A_GaugeBackground (vs A_GaugeBackground_Tall)
- **Brighter HP Color:** RGB(200,0,200) (vs RGB(200,80,200) - darker in Tall Gauge)
- **Button X-positions:** Slightly offset (X=2 vs X=0 in Tall Gauge)

**When to use Standard vs Tall Gauge:**
- **Standard:** Prefer easier HP readability with larger gauge height
- **Tall Gauge:** Prefer consistent window aesthetic with target window (both use _Tall templates)

---

## Installation

1. **Backup existing pet window:** Copy current `EQUI_PetInfoWindow.xml` to safe location
2. **Copy this variant:**
   ```
   cp EQUI_PetInfoWindow.xml ../../
   ```
3. **Reload UI:** `/loadskin thorne_drak` or restart EverQuest
4. **Test all buttons:** Verify Attack, Follow, Taunt, Guard, Back, Sit, and Dismiss all function
5. **Check dismiss position:** Verify dismiss button is separated from Attack button

---

## Credits

- **Original Design:** ODAKU Pet Window
- **QQQuarm Conversion:** Brujoloco (November 6, 2023)
- **Editing & Layout:** Nanan (Order of the Phoenix, Saryrn server)
- **Thorne UI Enhancements:** 
  - Added dismiss button functionality
  - Adjusted dismiss button position for UX (Y=23)
  - Standard gauge variant configuration

---

## Technical Details

**EQTypes Used:**
- `16` - HP Gauge
- `17` - Mana Gauge  
- `69` - HP Label (numeric value)

**Key XML Properties:**
- `RelativePosition: true` - All child elements positioned relative to parent window
- `Style_Titlebar: false` - No title bar (clean look)
- `Style_Border: true` - Maintains window border
- `Style_Sizable: false` - Fixed dimensions, not resizable
- `WDT_RoundedNoTitle` - Rounded corners without title bar

**Gauge Offsets:**
- HP Gauge text aligned with left edge (TextOffsetX=4)
- HP Gauge fill offset right (GaugeOffsetX=3)
- Mana Gauge slight offset adjustment (GaugeOffsetY=-2)

---

**Last Updated:** February 1, 2026  
**Maintainer:** Draknare Thorne
