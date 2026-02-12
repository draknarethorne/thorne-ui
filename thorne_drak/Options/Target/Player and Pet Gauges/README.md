# Target Window - Player and Pet Gauges Variant

**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)  
**Version**: 1.0.0  
**Last Updated**: 2026-02-10
**Status**: ✅ Active - Dual Information Display  
**Author**: Draknare Thorne

---
## Purpose

The "Player and Pet Gauges" Target Window variant provides comprehensive information display by combining **player vitals, pet health, and target status** in a single efficient window. This allows players to monitor their own resources while actively targeting, improving situational awareness during group and solo play.

**Key Features**:

- **Player HP Gauge**: 8px red gauge showing current health status (EQType 1)
- **Player Mana Gauge**: 8px blue gauge with mana regeneration ticks (EQType 2/24)
- **Pet Health Display**: 8px purple gauge for summoned pet tracking (EQType 16)
- **Weight Indicator**: Compact weight display (current/max) for inventory management
- **Target Information**: Full target HP/Mana gauges and percentage values
- **Multi-Resource View**: See player, pet, and target vitals simultaneously
- **Color-Coded**: Red (HP), Blue (Mana), Purple (Pet), Cyan (Ticks), Yellow (Target)

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 260 × 76+ pixels |
| **Layout Type** | Stacked gauge display (player/pet/target info) |
| **Resizable** | Yes |
| **Player Gauges** | 3 (HP, Mana, Pet Health) @ 8px height |
| **Target Gauges** | 2 (HP, Mana) @ standard height |
| **Weight Display** | Centered at Y=18 (Font 2) |
| **Mana Ticks** | Tick gauge indicator (EQType 24) |
| **Fonts** | Font 2-5 (varies by element) |
| **Color Scheme** | RGB palette: Red/Blue/Purple/Cyan/Yellow |
| **Columns** | Player (X=2-147), Target (right side) |

---

## Overview

This Target Window variant displays player and pet health gauges alongside target information, providing at-a-glance visibility of your character status while targeting.

## Features

- **Player HP Gauge** - Red gauge showing current player health (EQType 1), X=2, Y=16 (8px height)
- **Player Mana Gauge** - Blue gauge showing current player mana (EQType 2), X=148, Y=16 (8px height)
- **Pet Health Gauge** - Purple gauge showing current pet health (EQType 16), X=2, Y=24 (8px height)
- **Mana Tick Display** - Cyan line gauge showing mana regeneration ticks (EQType 24), X=148, Y=21 (8px height)
- **Player Weight Display** - Compact weight indicator (current/max), Font 2, centered, X=99-147, Y=18
- **Target HP/Mana Gauges** - Full-size target information display (standard Target Window)
- **Target Percentage Values** - HP%/Mana% with Font 5 labels

## Layout

```
Window: 260×76px

Row 1 (Y=16): Player HP | Mana Tick Gauge
Row 2 (Y=18): [Weight Display]
Row 3 (Y=24): [Pet Health]
Rows 4-6: Target Gauges and Info
```

## Color Scheme

- **Player HP**: Red RGB(255,0,0)
- **Player Mana**: Blue RGB(30,30,255)  
- **Pet Health**: Purple RGB(200,80,200)
- **Mana Ticks**: Cyan RGB(0,220,220)
- **Target HP**: Yellow RGB(240,0,0)
- **Target Mana**: Magenta RGB(240,0,240)

## Font Sizes

- Weight fields: Font 2 (minimal/compact)
- Player/Target HP/Mana values: Font 4
- Percentage indicators: Font 5

---

## Element Inventory - Comprehensive Triple-Gauge System

### Player Status Gauges (Top Section, Y=16-40)

| Element | ScreenID | Position | Size (px) | EQType | Color | Function |
|---------|----------|----------|-----------|--------|-------|----------|
| Player HP Gauge | TW_PlayerHPGauge | X=2, Y=16 | 142×8 | 1 | Red (255,0,0) | Current player health visualization |
| Player HP Value | TW_PlayerHPValue | X=2, Y=25 | 45×12 | 70 | White | Current/Max HP numeric (e.g., "875/1200") |
| Player HP Percent | TW_PlayerHPPercent | X=50, Y=25 | 30×12 | 19 | White | HP percentage (e.g., "73%") |
| Player Mana Gauge | TW_PlayerManaGauge | X=148, Y=16 | 108×8 | 2 | Blue (30,30,255) | Current player mana bar |
| Player Mana Value | TW_PlayerManaValue | X=148, Y=25 | 45×12 | 80 | White | Current/Max Mana numeric |
| Player Mana Percent | TW_PlayerManaPercent | X=196, Y=25 | 30×12 | 20 | White | Mana percentage display |
| Mana Tick Gauge | TW_ManaTickGauge | X=148, Y=21 | 108×8 | 24 | Cyan (0,220,220) | Mana regeneration tick counter |
| Weight Display | TW_PlayerWeight | X=99, Y=18 | 45×12 | 25 | White | Current/Max inventory weight |

### Pet Status Gauge (Middle Section, Y=41-50)

| Element | ScreenID | Position | Size (px) | EQType | Color | Function |
|---------|----------|----------|-----------|--------|-------|----------|
| Pet Name Label | TW_PetName | X=2, Y=33 | 60×10 | 69 | Purple (200,80,200) | "Pet:" prefix + dynamic pet name |
| Pet HP Gauge | TW_PetHPGauge | X=2, Y=41 | 142×8 | 16 | Purple (200,80,200) | Pet health visualization |
| Pet HP Value | TW_PetHPValue | X=2, Y=50 | 45×12 | 69 | White | Current/Max pet HP display |
| Pet HP Percent | TW_PetHPPercent | X=50, Y=50 | 30×12 | 19 | White | Pet HP percentage |
| Pet Status Icon | TW_PetIcon | X=148, Y=41 | 16×16 | N/A | N/A | Pet type/class indicator |
| Pet Mana Gauge | TW_PetManaGauge | X=148, Y=41 | 108×8 | 17 | Blue (100,150,255) | Pet mana bar (if applicable) |

### Target Status Gauges (Bottom Section, Y=51+)

| Element | ScreenID | Position | Size (px) | EQType | Color | Function |
|---------|----------|----------|-----------|--------|-------|----------|
| Target Name | TW_TargetName | X=2, Y=51 | 100×12 | 3 | White | Target character/NPC name |
| Target Level | TW_TargetLevel | X=140, Y=51 | 20×12 | 4 | White | Target level display |
| Target HP Gauge | TW_TargetHPGauge | X=2, Y=63 | 142×12 | 18 | Yellow/Red (240,0,0) | Target health bar |
| Target HP Value | TW_TargetHPValue | X=2, Y=76 | 45×12 | 37 | White | Current/Max target HP |
| Target HP Percent | TW_TargetHPPercent | X=50, Y=76 | 30×12 | 5 | White | Target HP percentage |
| Target Mana Gauge | TW_TargetManaGauge | X=148, Y=63 | 108×12 | 21 | Magenta (240,0,240) | Target mana bar |
| Target Mana Value | TW_TargetManaValue | X=148, Y=76 | 45×12 | 38 | White | Current/Max target mana |
| Target Mana Percent | TW_TargetManaPercent | X=196, Y=76 | 30×12 | 6 | White | Target mana percentage |
| Target Info Label | TW_TargetInfo | X=85, Y=51 | 50×12 | 89 | Yellow | Target type (NPC/PC/Special) |

---

## Technical Specifications - Multi-Gauge Implementation

### Window Layout Architecture

**Total Height Calculation**:
- Player Status: 32px (gauges 8px + labels 12px + padding)
- Pet Status: 26px (label 10px + gauges 8px + labels 12px + padding)
- Target Status: 38px (name 12px + space 2px + gauges 12px + labels 12px)
- **Total**: ~96px (resizable window standardizes to 260×76px minimum, expands with content)

**Three-Column Layout**:
```
┌─────────────────────────┬──────────────────────────┐
│ PLAYER STATUS (Left)    │ MANA/TICK (Right)       │
│ HP + Percent + Value    │ Player Mana + Ticks     │
├─────────────────────────┼──────────────────────────┤
│ PET STATUS (Dual Column)                  │ Icon  │
│ Pet HP + Percent + Name │ Pet Mana (if applicable)│
├─────────────────────────┴──────────────────────────┤
│ TARGET STATUS (Full Width)                         │
│ Target HP Bar + Target Mana Bar                    │
│ Target Info (Name, Level, Class, Type)             │
└────────────────────────────────────────────────────┘
```

### EQType Coverage

| EQType | Source | Values | Usage |
|--------|--------|--------|-------|
| 1 | Player | Current HP | Player HP Gauge fill |
| 2 | Player | Current Mana | Player Mana Gauge fill |
| 4 | Target | Level | Target level display |
| 5 | Target | Mana % | Target mana percentage |
| 6 | Target | HP % | Target HP percentage |
| 16 | Pet | Current HP | Pet HP Gauge fill |
| 17 | Pet | Current Mana | Pet Mana Gauge fill (optional) |
| 18 | Target | Current HP | Target HP Gauge fill |
| 19 | Player/Pet | HP % | Percentage calculations |
| 20 | Player | Mana % | Mana percentage calculation |
| 21 | Target | Current Mana | Target Mana Gauge fill |
| 24 | Player | Mana Ticks | Tick counter/visual indicator |
| 25 | Player | Weight | Inventory weight display |
| 37 | Target | Max HP | Target max HP denominator |
| 38 | Target | Max Mana | Target max mana denominator |
| 69 | Pet | Name | Pet name + "Pet:" label |
| 70 | Player | Max HP | Player max HP for value display |
| 80 | Player | Max Mana | Player max mana for value display |
| 89 | Target | Type/Class | Target classification label |

### Gauge Sizing Standards

| Gauge Type | Height | Width | Purpose | EQ Palette |
|------------|--------|-------|---------|-----------|
| Player HP | 8px | 142px | Quick status glance | Red (255,0,0) |
| Player Mana | 8px | 108px | Resource tracking | Blue (30,30,255) |
| Mana Ticks | 8px | 108px | Regen timing | Cyan (0,220,220) |
| Pet HP | 8px | 142px | Companion status | Purple (200,80,200) |
| Pet Mana | 8px | 108px | Pet resource | Blue (100,150,255) |
| Target HP | 12px | 142px | Primary focus | Yellow/Red (240,0,0) |
| Target Mana | 12px | 108px | Secondary focus | Magenta (240,0,240) |

### Font & Text Configuration

| Element | Font | Size | Color | Alignment |
|---------|------|------|-------|-----------|
| Player HP Value | Font 4 | 12px | White | Left |
| Player HP % | Font 5 | 10px | White | Left |
| Player Weight | Font 2 | 9px | White | Center |
| Pet Name | Font 3 | 10px | Purple | Left |
| Pet HP Value | Font 4 | 12px | White | Left |
| Target Name | Font 3 | 11px | White | Left |
| Target Type | Font 2 | 9px | Yellow | Center |
| Target HP % | Font 5 | 10px | White | Left |
| Target Mana % | Font 5 | 10px | White | Left |

---

## Variant Comparison - Target Window Layouts

| Feature | Player & Pet | Standard | Simple | Compact |
|---------|--------------|----------|--------|---------|
| **Player HP Display** | ✅ Yes (8px) | No | No | No |
| **Player Mana Display** | ✅ Yes (8px) | No | No | No |
| **Pet Gauge** | ✅ Yes (8px) | No | No | No |
| **Mana Tick Display** | ✅ Yes (8px) | No | No | No |
| **Weight Display** | ✅ Yes | No | No | No |
| **Target Name/Level** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Target HP Gauge** | ✅ Yes (12px) | ✅ Yes (12px) | ✅ Yes (8px) | ✅ Yes (6px) |
| **Target Mana Gauge** | ✅ Yes (12px) | ✅ Yes (12px) | ✅ Yes (8px) | ✅ Yes (4px) |
| **Use Case** | Pet classes | Solo/general | Minimal | Extreme compact |
| **Minimum Height** | 76px | 40px | 28px | 20px |
| **Information Density** | Maximum | Medium | Low | Minimal |

---

## Status

**Active Development** - This is the primary Target Window variant being refined with precise positioning and sizing adjustments for optimal information density.

## Installation

### Quick Setup
```bash
# Copy to main UI directory
cp EQUI_TargetWindow.xml ../../
```

### Testing
1. Launch EverQuest with thorne_drak UI
2. Target an NPC or player
3. Verify dual-gauge display shows correctly
4. Check weight indicator updates as inventory changes
5. Summon a pet and verify pet health gauge displays

## Best Use Cases

**Excellent For**:
- Group content where you need your own resource visibility
- Solo pet classes (Enchanter, Necromancer, Druid)  
- Coordinating buffs/debuffs while managing personal resources
- Extended battles where mana tick tracking matters

**Alternative If**:
- You prefer dedicated Pet Window elsewhere - use Standard Target Window
- You don't use summoned pets - use simpler Target variant
- Screen space is extremely limited - use minimal Target

---

**Maintainer**: Draknare Thorne  
**Last Updated**: February 2026
