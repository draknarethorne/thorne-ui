# Multi-Color Gauge System — Holistic Analysis

**Date**: March 4, 2026 (revised March 5, 2026)  
**Author**: Draknare Thorne  
**Status**: Research — Pre-Implementation Analysis  
**Sources**: Nillipuss, DuxaUI, Thorne codebase audit (40+ gauges across 12 windows)

---

## Table of Contents

- [Multi-Color Gauge System — Holistic Analysis](#multi-color-gauge-system--holistic-analysis)
  - [Table of Contents](#table-of-contents)
  - [Executive Summary](#executive-summary)
    - [Core Findings](#core-findings)
    - [Key Design Principles](#key-design-principles)
    - [Scope](#scope)
  - [Complete Gauge Inventory](#complete-gauge-inventory)
    - [Inventory Table](#inventory-table)
    - [Tier Classification](#tier-classification)
    - [Gauge Size Classes](#gauge-size-classes)
    - [Anomalies Found](#anomalies-found)
  - [The Core Technique](#the-core-technique)
    - [How EQ Gauges Work](#how-eq-gauges-work)
    - [GaugeOffsetX and Thresholds](#gaugeoffsetx-and-thresholds)
    - [The A/B Split Pattern](#the-ab-split-pattern)
    - [Generic N-Band Mathematics](#generic-n-band-mathematics)
  - [Reference Implementations](#reference-implementations)
    - [Nillipuss (240px, 5-band)](#nillipuss-240px-5-band)
    - [DuxaUI (100px, 5-band)](#duxaui-100px-5-band)
    - [Key Architectural Insights](#key-architectural-insights)
  - [Size-Agnostic Animation Design](#size-agnostic-animation-design)
    - [Why One Set of Animations Serves All Sizes](#why-one-set-of-animations-serves-all-sizes)
    - [Shared Multi-Color Animations](#shared-multi-color-animations)
    - [Per-Window Adaptation](#per-window-adaptation)
    - [Calculation Template](#calculation-template)
  - [Flexible Color Palettes](#flexible-color-palettes)
    - [Palette Independence from Animations](#palette-independence-from-animations)
    - [Example Palettes](#example-palettes)
    - [Per-Purpose Color Strategies](#per-purpose-color-strategies)
    - [Band Count Flexibility](#band-count-flexibility)
  - [Thorne's Current Gauge System](#thornes-current-gauge-system)
    - [Single-Color Architecture](#single-color-architecture)
    - [Swappable Gauge Options](#swappable-gauge-options)
    - [Integration Compatibility](#integration-compatibility)
  - [Per-Window Implementation Plans](#per-window-implementation-plans)
    - [PlayerWindow (7 gauges)](#playerwindow-7-gauges)
    - [TargetWindow (8 gauges)](#targetwindow-8-gauges)
    - [GroupWindow (10 gauges)](#groupwindow-10-gauges)
    - [PetInfoWindow (2 gauges)](#petinfowindow-2-gauges)
    - [Other Windows (single-color)](#other-windows-single-color)
  - [Implementation Roadmap](#implementation-roadmap)
    - [Phase 1: Prototype \& Verify (Single Gauge)](#phase-1-prototype--verify-single-gauge)
    - [Phase 2: PlayerWindow Complete](#phase-2-playerwindow-complete)
    - [Phase 3: TargetWindow](#phase-3-targetwindow)
    - [Phase 4: Group \& Pet Windows](#phase-4-group--pet-windows)
    - [Phase 5: Polish \& Options](#phase-5-polish--options)

---

## Executive Summary

This analysis covers **every gauge across the entire Thorne UI** — 40+ gauge elements in 12+ windows — and presents a holistic plan for adding multi-color fill transitions to any gauge, at any size, with any color palette.

### Core Findings

Both Nillipuss and DuxaUI achieve multi-color gauges using the same technique: **oversized gauge layering with opaque occlusion**. Multiple gauge elements stack on one value (e.g., HP%), each with a different `FillTint` color, clipped by viewport containers so each color band appears only within its designated threshold range. When HP drops, higher layers lose fill first, revealing lower colors underneath. **This is not transparency blending** — it is purely opaque layer occlusion.

### Key Design Principles

1. **Size-agnostic animations**: Define 4 oversized fill animations **once** in `EQUI_Animations.xml`. These same animations work for 103px, 120px, 128px, 250px — any gauge width. Only the per-window layout math changes (Screen clip widths, B gauge positions).

2. **Palette-independent architecture**: Colors come entirely from `FillTint` values in the window XML, not from animations. The oversized fills stretch textures beyond recognition — `FillTint` is the sole color determinant. Switching palettes means changing only FillTint RGB values. The animations never change.

3. **Flexible color palettes**: No palette is hardcoded into the system. The document presents multiple palette examples (classic red→green, ember glow, ocean depths, monochrome intensity), but any combination of RGB values works. Palettes can vary by gauge purpose (HP vs Mana vs XP) and by number of color bands (3, 4, or 5).

4. **Full Options compatibility**: The multi-color fills are independent of Thorne's swappable gauge style system (Bubbles, Grid, Oval, etc.). Gauge Options continue controlling background/overlay appearance; multi-color fills provide the dynamic color transitions within any style.

### Scope

| Category | Gauges | Multi-Color? | Action |
|----------|--------|-------------|--------|
| HP gauges | 8 across 4 windows | **Yes — Tier 1** | Full multi-color layering |
| Resource gauges | 5 (Mana, Stamina, Breath) | **Optional — Tier 2** | Multi-color if desired |
| Progress gauges | 7 (XP, AAXP) | Single-color preferred | No change |
| Timer gauges | 15 (ticks, recasts, casting) | Single-color | No change |
| Activity gauges | 3 (memorize, scribe, song) | Single-color | No change |

---

## Complete Gauge Inventory

### Inventory Table

Every gauge element in the Thorne UI, audited from source XML:

| Window | Gauge ID | EQType | Size (CX×CY) | FillTint RGB | Animation Ref | Notes |
|--------|----------|--------|---------------|-------------|---------------|-------|
| **PlayerWindow** | `PW_Gauge_HP` | 1 (HP%) | 120×16 | 255,0,0 (red) | `A_GaugeFill_120t` | Tall gauge |
| | `PW_Gauge_Mana` | 2 (Mana%) | 120×16 | 30,30,255 (blue) | `A_GaugeFill_120t` | Tall gauge |
| | `PW_Mana_Tick` | 24 (ManaTick) | 120×9 | 0,220,220 (cyan) | `A_GaugeLinesFill_120t` | Transparent, tick only |
| | `PW_Gauge_Stamina` | 3 (Stam%) | 120×8 | 240,240,0 (yellow) | `A_GaugeFill_120` | Wide gauge |
| | `PW_Gauge_XP` | 4 (XP%) | 120×16 | 220,150,0 (gold) | `A_GaugeFill_120t` | Lines+LinesFill |
| | `PW_Gauge_AAXP` | 5 (AAXP%) | 120×16 | 220,200,0 (gold) | `A_GaugeFill_120t` | Lines+LinesFill |
| | `PW_Gauge_PetHP` | 16 (PetHP%) | 120×16 | 200,80,200 (purple) | `A_GaugeFill_120t` | Tall gauge |
| **TargetWindow** | `TW_PlayerHP_Gauge` | 1 (HP%) | 103×8 | 255,0,0 (red) | `A_GaugeFill` | Standard gauge |
| | `TW_PlayerMana_Gauge` | 2 (Mana%) | 103×8 | 30,30,255 (blue) | `A_GaugeFill` | ⚠ CX has typo "103i" |
| | `TW_PetHealth_Gauge` | 16 (PetHP%) | 103×8 | 200,80,200 (purple) | `A_GaugeFill` | Standard gauge |
| | `TW_TargetHP_Gauge` | 6 (TgtHP%) | 250×16 | 240,0,0 (red) | `A_GaugeFill_250t` | Tall, with BG StaticAnim |
| | `TW_Casting_Gauge` | 7 (Cast%) | 250×16 | 240,0,240 (magenta) | `A_GaugeFill_250t` | With spell name overlay |
| | `TW_ManaTick_Gauge` | 24 (ManaTick) | 103×8 | 0,220,220 (cyan) | `A_GaugeLinesFill` | Transparent, tick only |
| | `TW_AttackTick_Gauge` | 34 (AtkTick) | 250×4 | 220,180,0 (gold) | `A_GaugeTick_250t` | Transparent, thin |
| | `TW_Global_Recast_Gauge` | 25 (GCD) | 250×3 | 255,210,250 (pink) | `A_GaugeTick_250t` | Transparent, thin |
| **GroupWindow** | `GW_Gauge1–5` | 11–15 (Grp HP) | 114×24 | 220,0,0 (red) | `A_GaugeFill` | ×5, GaugeOffsetX=3 |
| | `GW_PetGauge1–5` | 17 (GrpPet%) | 114×2 | 51,192,51 (green) | `A_GaugeFill` | ×5, decorative thin |
| **PetInfoWindow** | `PIW_PetHPGauge` | 16 (PetHP%) | 128×15 | 200,80,200 (purple) | `A_GaugeFill_120t` | Unique 128px width |
| | `PIW_PetManaGauge` | 17 (PetMana%) | 120×4 | 100,150,255 (blue) | `A_GaugeFill_120t` | Thin mana bar |
| **CastSpellWnd** | `CSPW_Global_Recast` | 25 (GCD) | 146×3 | 255,210,250 (pink) | `A_CastRecastBarFill` | Transparent |
| | `CSPW_Spell0–7_Recast` | 26–33 | 146×3 | 200,0,200 (purple) | `A_CastRecastBarFill` | ×8, transparent |
| **BreathWindow** | `BREATH_Gauge` | 8 (Breath%) | 116×8 | 0,240,240 (cyan) | `A_GaugeFill` | With EndCaps |
| **CastingWindow** | `Casting_Gauge` | — | 0×0 | — | — | Hidden (0×0) |
| **Inventory** | `IW_ExpGauge` | 4 (XP%) | 102×8 | 220,150,0 (gold) | `A_GaugeFill` | Lines+LinesFill |
| | `IW_AltAdvGauge` | 5 (AAXP%) | 102×8 | 220,200,0 (gold) | `A_GaugeFill` | Lines+LinesFill |
| | `IW_AltAdvGauge_Dummy` | 5 | 102×8 | 220,200,0 | `A_GaugeFill` | ScreenID: "AltAdvGauge" |
| **MerchantWnd** | `MW_ExpGauge` | 4 (XP%) | 111×8 | 220,150,0 (gold) | `A_GaugeFill` | Lines+LinesFill |
| **AAWindow** | `AAW_ExpGauge` | 5 (AAXP%) | 108×28 | 240,240,0 (yellow) | `A_GaugeFill` | Tall, with EndCaps |
| **TrainWindow** | `TRNW_ExpGauge` | 4 (XP%) | 0×0 | 240,240,0 (yellow) | `A_GaugeFill` | Hidden (0×0) |
| **MusicPlayer** | `MPW_SongTimer` | 22 (Song) | 0×0 | 220,220,0 (yellow) | `A_GaugeFill` | Hidden (0×0) |
| **SpellBook** | `SBW_Memorize_Gauge` | 9 (Mem%) | 102×8 | 200,0,200 (purple) | `A_GaugeFill` | Standard |
| | `SBW_Scribe_Gauge` | 10 (Scribe%) | 102×8 | 200,0,200 (purple) | `A_GaugeFill` | Standard |

### Tier Classification

**Tier 1 — Strong multi-color candidates** (HP-type gauges where threshold urgency matters):

| Gauge | Window | Width | Priority |
|-------|--------|-------|----------|
| `PW_Gauge_HP` | PlayerWindow | 120px | Highest — primary feedback |
| `TW_TargetHP_Gauge` | TargetWindow | 250px | High — combat focus |
| `PW_Gauge_PetHP` | PlayerWindow | 120px | High — pet management |
| `PIW_PetHPGauge` | PetInfoWindow | 128px | High — pet management |
| `TW_PlayerHP_Gauge` | TargetWindow | 103px | Medium — self-awareness |
| `TW_PetHealth_Gauge` | TargetWindow | 103px | Medium — pet awareness |
| `GW_Gauge1–5` | GroupWindow | 114px | Medium — group healing |
| `BREATH_Gauge` | BreathWindow | 116px | Lower — situational |

**Tier 2 — Optional multi-color** (resource gauges where depletion has urgency):

| Gauge | Window | Width | Notes |
|-------|--------|-------|-------|
| `PW_Gauge_Mana` | PlayerWindow | 120px | Low mana = danger for casters |
| `TW_PlayerMana_Gauge` | TargetWindow | 103px | Mana awareness |
| `PIW_PetManaGauge` | PetInfoWindow | 120px | Only 4px tall — maybe too thin |
| `PW_Gauge_Stamina` | PlayerWindow | 120px | Running matters in PvP/raids |

**Tier 3 — Single-color preferred** (no urgency-based color transitions needed):

All XP/AAXP gauges, timer/tick gauges, recast bars, casting bars, memorize/scribe gauges, group pet gauges (2px thin), song timer. These stay as-is.

### Gauge Size Classes

Distinct gauge widths currently in use:

| Width | Height | Count | Windows | Animation Suffix |
|-------|--------|-------|---------|-----------------|
| 102–103px | 8px | 7 | Target, Inventory, SpellBook | (standard) |
| 108px | 28px | 1 | AAWindow | (standard, oversized) |
| 111px | 8px | 1 | MerchantWnd | (standard) |
| 114px | 24px | 5 | GroupWindow | (standard) |
| 114px | 2px | 5 | GroupWindow (pet) | (standard, decorative) |
| 116px | 8px | 1 | BreathWindow | (standard) |
| 120px | 8–16px | 7 | PlayerWindow | `_120` / `_120t` |
| 128px | 15px | 1 | PetInfoWindow | Uses `_120t` (mismatched) |
| 146px | 3px | 9 | CastSpellWnd | (recast-specific) |
| 250px | 3–16px | 4 | TargetWindow | `_250t` |

### Anomalies Found

During the audit, these issues were noted:

1. **TargetWindow `TW_PlayerMana_Gauge`**: `<CX>103i</CX>` — trailing "i" is a typo, should be `103`
2. **TargetWindow `TW_TargetHP_Gauge`**: `<TextOffsetY>-1z</TextOffsetY>` — trailing "z" is a typo
3. **PetInfoWindow `PIW_PetHPGauge`**: CX=128 but uses `A_GaugeFill_120t` (120px animation for 128px gauge — 8px shortfall)
4. **GroupWindow `GW_Gauge1–5`**: CX=114 with GaugeOffsetX=3 — effective fill area is 111px, using 103px standard animations (stretched)

---

## The Core Technique

### How EQ Gauges Work

A standard EQ `<Gauge>` element:
1. Binds to a value via `<EQType>` (e.g., `1` = HP percentage)
2. Fills left-to-right proportionally (0% = empty, 100% = full)
3. Draws via `<GaugeDrawTemplate>` (Background, Fill, Lines, LinesFill textures)
4. Colors the fill via `<FillTint>` RGB values

The EQ client has **no built-in support** for changing color based on percentage. Multi-color requires creative XML layering.

### GaugeOffsetX and Thresholds

`GaugeOffsetX` creates a **dead zone** at the start of the gauge fill. The fill must grow past `|GaugeOffsetX|` pixels before becoming visible:

```
effective_width = gauge_CX + |GaugeOffsetX|
visible_fill    = (fill% × effective_width) − |GaugeOffsetX|
threshold_%     = |GaugeOffsetX| / effective_width
```

> **Verification note**: This formula (Model B) assumes the EQ client treats the effective range as `CX + |GaugeOffsetX|`. Nillipuss's 5 equal 20% bands on a 240px bar with GaugeOffsetX values of -2000/-4000/-6000/-8000 and CX values of 8000/6000/4000/2000 yield consistent 20% thresholds under this model. The alternative (Model A: `threshold = |GaugeOffsetX| / CX`) yields 25% thresholds, which doesn't match the implementation intent. **In-game testing is needed to confirm which model the client uses.**

### The A/B Split Pattern

Each color band requires two gauge elements:

- **"A" gauge** (oversized, in a Screen container): Uses massive `CX` and large negative `GaugeOffsetX` to create threshold behavior. The `Screen` clips the oversized fill to the band's visible zone.

- **"B" gauge** (normal size, right of A): Covers the bar from the band boundary to the right edge. Uses a standard fill with `GaugeOffsetX` matching the cumulative band width.

**Why the split?** The Screen clips the A gauge's oversized fill to prevent it from covering the entire bar. The B gauge fills the rest with the same color at normal dimensions.

### Generic N-Band Mathematics

For **N color levels** (1 base + N−1 additional bands) on a bar of width **W** pixels, with equal threshold spacing:

```
effective_width  = chosen constant >> W  (e.g., 10000)
band_width       = W / N
threshold[i]     = i / N                          (for band i, where i = 1..N-1)
GaugeOffsetX[i]  = −(threshold[i] × effective_width)
A_gauge_CX[i]    = effective_width − |GaugeOffsetX[i]|
Screen_CX[i]     = i × band_width
B_start_X[i]     = parent_X + Screen_CX[i]
B_gauge_CX[i]    = W − Screen_CX[i]
B_GaugeOffsetX[i]= −Screen_CX[i]
```

**Example for 5 bands on W=120, effective_width=10000:**

| Band | i | Threshold | GaugeOffsetX | A CX | Screen CX | B CX | B GaugeOffsetX |
|------|---|-----------|-------------|------|-----------|------|----------------|
| Base (0) | 0 | 0% | 0 | 120 | 120 | — | — |
| Band 1 | 1 | 20% | −2000 | 8000 | 24 | 96 | −24 |
| Band 2 | 2 | 40% | −4000 | 6000 | 48 | 72 | −48 |
| Band 3 | 3 | 60% | −6000 | 4000 | **71** | **49** | **−71** |
| Band 4 | 4 | 80% | −8000 | 2000 | **94** | **26** | **−94** |

> Grid-aligned: Bands 3–4 adjusted to match Thorne texture grid lines (0, 24, 48, 71, 94, 119).

**Same formula for W=250 (TargetWindow):**

| Band | Threshold | GaugeOffsetX | A CX | Screen CX | B CX | B GaugeOffsetX |
|------|-----------|-------------|------|-----------|------|----------------|
| Base | 0% | 0 | 250 | 250 | — | — |
| Band 1 | 20% | −2000 | 8000 | 50 | 200 | −50 |
| Band 2 | 40% | −4000 | 6000 | 100 | 150 | −100 |
| Band 3 | 60% | −6000 | 4000 | 150 | 100 | −150 |
| Band 4 | 80% | −8000 | 2000 | 200 | 50 | −200 |

Notice: The **A gauge values are identical** for both sizes (same CX, same GaugeOffsetX). Only the Screen/B gauge values change. This is the foundation of the size-agnostic animation system.

**Unequal band spacing** is also possible. For example, to make the critical zone wider:

| Band | Threshold | Effect |
|------|-----------|--------|
| Base | 0% | Shows below 30% — wider critical zone |
| Band 1 | 30% | Shows 30–50% |
| Band 2 | 50% | Shows 50–70% |
| Band 3 | 70% | Shows 70–90% |
| Band 4 | 90% | Shows above 90% — narrow "full health" zone |

---

## Reference Implementations

### Nillipuss (240px, 5-band)

**Bar**: 240×20px | **Texture**: `dzbars.png` (dedicated 256×256 atlas) | **Elements**: 10

Architecture: 1 background + 1 base red fill + 4 A/B band pairs. Colors: red(240,0,0) → orange(240,102,0) → yellow(240,240,0) → greenyellow(173,255,47) → green(0,240,0) at 20% thresholds.

Oversized fills (`PW_GaugeFill1–4`): CX=10000, Location X = −2000/−4000/−6000/−8000 from `dzbars.png` Y=120 row. Standard fills: `A_dzLongFill` (CX=240) for base and B gauges.

**Key insight**: `FillTint` provides ALL color — the oversized textures are stretched so far beyond recognition that the source art is irrelevant. `Style_Transparent=false` on all layers means pure opaque occlusion, not blending.

### DuxaUI (100px, 5-band)

**Bar**: 100×8px | **Texture**: `window_pieces01.tga` (shared atlas) | **Elements**: 12

Same A/B layering as Nillipuss, plus two refinements:

1. **Transparent overlay gauge** (`Player_HP`): `Style_Transparent=true`, renders only Lines/LinesFill/EndCap *on top* of all color layers. Provides consistent decorative overlay regardless of current color band.

2. **Decorative vertical bar framing**: StaticAnimation pieces (`PW_V_bartop`, `PW_V_barmiddle`, `PW_V_barbottom`) from `window_pieces22.tga` create rounded column frames beside gauges.

### Key Architectural Insights

1. **Both UIs use identical core technique** — only visual polish differs
2. **Colors come from FillTint, not textures** — palettes are fully configurable
3. **Oversized fills are style-independent** — they work with any gauge background art
4. **DuxaUI's overlay separation** is a clean pattern worth adopting

---

## Size-Agnostic Animation Design

### Why One Set of Animations Serves All Sizes

The oversized A gauge fills have CX values of 2000–8000 with GaugeOffsetX values of −8000 to −2000. These values depend only on the chosen **effective_width** and **threshold percentages** — not on the visible bar width. A gauge configured for 20% threshold with effective_width=10000 has CX=8000, GaugeOffsetX=−2000, regardless of whether the visible bar is 103px, 120px, or 250px.

The Screen container clips the oversized fill to the visible band width. The B gauge fills the remainder. Only these per-window elements change with gauge size.

**This means**: Define 4 threshold fill animations once → use them in every window.

### Shared Multi-Color Animations

Add to `EQUI_Animations.xml` — **4 new animations total** (plus 1 optional generic base):

```xml
<!-- ================================================================== -->
<!-- MULTI-COLOR THRESHOLD FILLS                                         -->
<!-- Size-agnostic: same animations work for ANY gauge width.            -->
<!-- Colors come from FillTint in each window XML, not from these fills. -->
<!-- ================================================================== -->

<!-- Band 1 fill (20% threshold, effective_width=10000) -->
<Ui2DAnimation item="A_MCFill_Band1">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay_thorne01.tga</Texture>
        <Location><X>-2000</X><Y>8</Y></Location>
        <Size><CX>10000</CX><CY>8</CY></Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<!-- Band 2 fill (40% threshold) -->
<Ui2DAnimation item="A_MCFill_Band2">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay_thorne01.tga</Texture>
        <Location><X>-4000</X><Y>8</Y></Location>
        <Size><CX>10000</CX><CY>8</CY></Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<!-- Band 3 fill (60% threshold) -->
<Ui2DAnimation item="A_MCFill_Band3">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay_thorne01.tga</Texture>
        <Location><X>-6000</X><Y>8</Y></Location>
        <Size><CX>10000</CX><CY>8</CY></Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<!-- Band 4 fill (80% threshold) -->
<Ui2DAnimation item="A_MCFill_Band4">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay_thorne01.tga</Texture>
        <Location><X>-8000</X><Y>8</Y></Location>
        <Size><CX>10000</CX><CY>8</CY></Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<!-- Generic wide base fill (for B gauges at any width ≤ 300px) -->
<Ui2DAnimation item="A_MCFill_Base">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay_thorne01.tga</Texture>
        <Location><X>0</X><Y>8</Y></Location>
        <Size><CX>300</CX><CY>8</CY></Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>
```

**Notes:**
- The texture reference (`gauge_inlay_thorne01.tga`) is arbitrary — at 10000× stretch, any opaque texture becomes a uniform fill. The color is entirely from `FillTint`.
- The `gauge_inlay_thorne01.tga` file is always present (it's the default standard gauge art), making these animations independent of which gauge Options variant is active.
- CY=8 works for all gauges — the EQ client stretches the fill to match the gauge element's CY.
- `A_MCFill_Base` (CX=300) covers the widest Thorne gauge (250px) with margin. Used for all base fills and B continuation fills.

### Per-Window Adaptation

When implementing multi-color for a specific gauge, only these per-window values change:

```
Given: W = visible bar width, parent_X = gauge X position in parent, parent_Y = gauge Y

Screen_CX[i] = i × (W / N)      ← clip width for band i
B_start_X[i] = parent_X + Screen_CX[i]
B_CX[i]      = W − Screen_CX[i]
B_OffsetX[i] = −Screen_CX[i]
```

Everything else (A gauge CX, A gauge GaugeOffsetX, fill animation names) stays the same across all windows.

### Calculation Template

For any gauge at width **W** with **5 bands** (base + 4 colored):

```
┌─────────────────────────────────────────────────┐
│  Gauge Width: W = ___px                         │
│  Band Width:  W/5 = ___px  (approximate)        │
│                                                 │
│  Band 1: Screen CX = W/5     B CX = 4×W/5      │
│  Band 2: Screen CX = 2×W/5   B CX = 3×W/5      │
│  Band 3: Screen CX = 3×W/5   B CX = 2×W/5      │
│  Band 4: Screen CX = 4×W/5   B CX = W/5         │
│                                                 │
│  NOTE: Adjust to grid-line positions in Thorne  │
│  textures. W/5 multiples may be 1-2px off.      │
│                                                 │
│  All A gauges use: A_MCFill_Band1–4             │
│  All B gauges use: A_MCFill_Base                │
│  Base gauge uses:  existing A_GaugeFill_{size}  │
│  Background uses:  existing A_GaugeBG_{size}    │
└─────────────────────────────────────────────────┘
```

**Quick reference for current Thorne gauge widths:**

| Width | Band (W/5) | Screen CX 1/2/3/4 | B CX 1/2/3/4 |
|-------|-----------|-------------------|--------------|
| 103px | 20.6px | 21 / 41 / 62 / 82 | 82 / 62 / 41 / 21 |
| 114px | 22.8px | 23 / 46 / 68 / 91 | 91 / 68 / 46 / 23 |
| 120px | 24px | 24 / 48 / 72 / 96 | 96 / 72 / 48 / 24 |
| 128px | 25.6px | 26 / 51 / 77 / 102 | 102 / 77 / 51 / 26 |
| 250px | 50px | 50 / 100 / 150 / 200 | 200 / 150 / 100 / 50 |

---

## Flexible Color Palettes

### Palette Independence from Animations

The color of each band comes **entirely** from `<FillTint>` in the window XML:

```xml
<FillTint><R>240</R><G>102</G><B>0</B></FillTint>  <!-- This is the ONLY thing that determines color -->
```

The oversized fill animations (`A_MCFill_Band1–4`) reference a texture stretched to 10,000px — any source texture pattern is obliterated. `FillTint` acts as a color multiplier on what is effectively a uniform white fill. **Changing FillTint = changing color. No animation changes needed.**

This means:
- Palettes are defined by **FillTint values in window XML files**
- Switching palettes = editing FillTint RGB on each band's gauge elements
- The same `A_MCFill_Band1–4` animations serve all palettes forever
- Different gauges can use different palettes simultaneously

### Example Palettes

Each palette defines N RGB values, one per band (base through highest). These are starting points — any RGB combination works.

**Classic (Red → Green):**
Traditional EQ health color language. Universally recognized.

| Band | Name | RGB | Hex |
|------|------|-----|-----|
| 0 (Base) | Red | 240, 0, 0 | `#F00000` |
| 1 (20%) | Orange | 240, 102, 0 | `#F06600` |
| 2 (40%) | Yellow | 240, 240, 0 | `#F0F000` |
| 3 (60%) | Green-Yellow | 173, 255, 47 | `#ADFF2F` |
| 4 (80%) | Green | 0, 240, 0 | `#00F000` |

**Ember Glow (Warm Spectrum):**
Stays within warm tones. Less jarring visually — no green at full HP.

| Band | Name | RGB | Hex |
|------|------|-----|-----|
| 0 | Dark Crimson | 140, 20, 20 | `#8C1414` |
| 1 | Burning Orange | 200, 80, 20 | `#C85014` |
| 2 | Warm Gold | 230, 170, 30 | `#E6AA1E` |
| 3 | Pale Gold | 240, 220, 100 | `#F0DC64` |
| 4 | Bright White-Gold | 255, 245, 180 | `#FFF5B4` |

**Ocean Depths (Cool Spectrum):**
Cool-toned progression. Distinctive from classic health bars.

| Band | Name | RGB | Hex |
|------|------|-----|-----|
| 0 | Deep Plum | 100, 20, 60 | `#64143C` |
| 1 | Dark Blue | 40, 60, 160 | `#283CA0` |
| 2 | Ocean | 30, 140, 200 | `#1E8CC8` |
| 3 | Teal | 20, 200, 180 | `#14C8B4` |
| 4 | Seafoam | 120, 240, 200 | `#78F0C8` |

**Monochrome Red (Single Hue, Varying Intensity):**
Uses brightness progression within one color family. Subtle but effective.

| Band | Name | RGB | Hex |
|------|------|-----|-----|
| 0 | Dark Red | 80, 0, 0 | `#500000` |
| 1 | Medium Red | 140, 20, 20 | `#8C1414` |
| 2 | Bright Red | 200, 40, 40 | `#C82828` |
| 3 | Light Rose | 230, 100, 100 | `#E66464` |
| 4 | Pale Pink | 255, 170, 170 | `#FFAAAA` |

**Frostbite (Cold Danger):**
Inverts the typical warm=danger association. Blue = cold = dangerous.

| Band | Name | RGB | Hex |
|------|------|-----|-----|
| 0 | Ice Blue | 100, 180, 255 | `#64B4FF` |
| 1 | Steel Blue | 80, 130, 200 | `#5082C8` |
| 2 | Dusk Purple | 100, 80, 160 | `#6450A0` |
| 3 | Warm Amber | 200, 150, 60 | `#C8963C` |
| 4 | Hearthfire | 240, 200, 100 | `#F0C864` |

### Per-Purpose Color Strategies

Different gauge types can use different palettes or different numbers of bands:

| Gauge Purpose | Palette Approach | Rationale |
|---------------|-----------------|-----------|
| **HP** | 5-band color transition | Health urgency requires maximum visual feedback |
| **Target HP** | Same as player HP or contrasting | Consistent combat feedback |
| **Pet HP** | Match player HP or use purple shading | Pet uses purple in current Thorne scheme |
| **Group HP** | Simplified 3-band (red/yellow/green) | 5× members × 10 elements = heavy; fewer bands reduce load |
| **Mana** | 3-band blue shading (dark→medium→bright) | Mana depletion is important but less urgent than HP |
| **Stamina** | Single-color or 2-band | Stamina is rarely critical |
| **Breath** | 2-band (red/cyan) or single-color | Only visible during underwater emergency |
| **XP/AAXP** | Single-color (gold) | XP only goes up; no urgency feedback needed |
| **Timers** | Single-color | Transient bars; multi-color adds no value |

### Band Count Flexibility

The system supports any number of bands. Fewer bands = fewer elements per gauge = better performance:

| Bands | Elements per Gauge | Use Case |
|-------|--------------------|----------|
| 2 | 1 BG + 2 fills + 1 Screen | Simple "OK/danger" split |
| 3 | 1 BG + 3 fills + 2 Screens + 2 B fills | Red/yellow/green classic |
| 4 | 1 BG + 4 fills + 3 Screens + 3 B fills | More gradual transitions |
| 5 | 1 BG + 5 fills + 4 Screens + 4 B fills | Full Nillipuss/DuxaUI style |

**For GroupWindow** (5 members × HP gauge): Using 5 bands means 11 elements × 5 = **55 elements** just for group HP. A 3-band approach (7 elements × 5 = 35) may be more practical.

**Total element formula**: `1 + N + (N-1) × 2 = 3N - 1` elements per multi-color gauge (background + base + N-1 A gauges + N-1 Screens + N-1 B gauges). With overlay: `3N`.

---

## Thorne's Current Gauge System

### Single-Color Architecture

Each gauge uses one element with style-specific textures:

```xml
<Gauge item="PW_Gauge_HP">
    <EQType>1</EQType>
    <Size><CX>120</CX><CY>16</CY></Size>
    <FillTint><R>255</R><G>0</G><B>0</B></FillTint>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
```

Animations in `EQUI_Animations.xml` reference size-specific textures:
- Standard (103px): `A_GaugeFill` → `gauge_inlay_thorne01.tga`
- Wide (120, 150): `A_GaugeFill_120` → `gauge_inlay120_thorne01.tga`
- Tall (120t, 150t, 230t–260t): `A_GaugeFill_120t` → `gauge_inlay120t_thorne01.tga`

Each texture has 4 stacked sections: Background (Y=0), Fill, Lines, LinesFill.

### Swappable Gauge Options

8 visual styles generated by `regen_gauges.py` from a source texture. Switching styles = copying `.tga` files + reloading UI. No XML changes required.

### Integration Compatibility

**Multi-color fills are fully independent of gauge style options:**

- ✅ `A_MCFill_Band1–4` reference the always-present default `gauge_inlay_thorne01.tga`
- ✅ At 10000× stretch, the texture pattern is irrelevant — `FillTint` determines all color
- ✅ Gauge style options continue controlling Background/Lines appearance
- ✅ No changes needed to `regen_gauges.py` or the Options pipeline
- ✅ The base fill gauge (Band 0) still uses the style-specific fill animation for visual consistency

---

## Per-Window Implementation Plans

### PlayerWindow (7 gauges)

**Multi-color candidates**: HP, Mana, PetHP  
**Single-color**: Stamina, XP, AAXP, ManaTick  
**Gauge width**: 120px (all)

**HP Gauge — 5-band implementation (11 elements replacing 1):**

Current: 1 gauge (`PW_Gauge_HP`, 120×16, red, `A_GaugeFill_120t`)

Proposed structure:
```
PW_HP_BG         Background only (A_GaugeBackground_120t)
PW_HP_0          Base fill (A_GaugeFill_120t, palette band 0)
PW_HP_1A_X       Screen CX=24 clipping PW_HP_1A
  PW_HP_1A       A gauge CX=8000, GaugeOffsetX=-2000, A_MCFill_Band1
PW_HP_1B         B gauge CX=96, GaugeOffsetX=-24, A_MCFill_Base
PW_HP_2A_X       Screen CX=48 clipping PW_HP_2A
  PW_HP_2A       A gauge CX=6000, GaugeOffsetX=-4000, A_MCFill_Band2
PW_HP_2B         B gauge CX=72, GaugeOffsetX=-48, A_MCFill_Base
PW_HP_3A_X       Screen CX=71 clipping PW_HP_3A    (grid-aligned: 71, not 72)
  PW_HP_3A       A gauge CX=4000, GaugeOffsetX=-6000, A_MCFill_Band3
PW_HP_3B         B gauge CX=49, GaugeOffsetX=-71, A_MCFill_Base
PW_HP_4A_X       Screen CX=94 clipping PW_HP_4A    (grid-aligned: 94, not 96)
  PW_HP_4A       A gauge CX=2000, GaugeOffsetX=-8000, A_MCFill_Band4
PW_HP_4B         B gauge CX=26, GaugeOffsetX=-94, A_MCFill_Base
```

**All A gauges reference the shared `A_MCFill_Band1–4` — same as every other window.**

**Mana Gauge** — same pattern if desired. Consider 3-band blue palette:
- Band 0: dark blue (30,30,180), Band 1: medium blue (60,100,220), Band 2: bright blue (100,180,255)
- 7 elements instead of 11 (fewer bands = lighter)

**PetHP Gauge** — same 120px pattern. Could use purple palette or match player HP palette.

### TargetWindow (8 gauges)

**Multi-color candidates**: TargetHP (250px), PlayerHP (103px), PetHealth (103px)  
**Single-color**: PlayerMana, Casting, ManaTick, AttackTick, GlobalRecast

**Target HP — 5-band at 250px (11 elements replacing 1):**

```
TW_TgtHP_BG      Background (A_GaugeBackground_250t)
TW_TgtHP_0       Base fill (A_GaugeFill_250t, palette band 0)
TW_TgtHP_1A_X    Screen CX=50
  TW_TgtHP_1A    A gauge CX=8000, GaugeOffsetX=-2000, A_MCFill_Band1   ← SAME animations
TW_TgtHP_1B      B gauge CX=200, GaugeOffsetX=-50, A_MCFill_Base
...               (bands 2-4 follow same pattern)
TW_TgtHP_4A_X    Screen CX=200
  TW_TgtHP_4A    A gauge CX=2000, GaugeOffsetX=-8000, A_MCFill_Band4   ← SAME animations
TW_TgtHP_4B      B gauge CX=50, GaugeOffsetX=-200, A_MCFill_Base
```

The A gauge animations are **identical** to PlayerWindow — `A_MCFill_Band1–4`. Only Screen CX and B gauge dimensions differ.

**Player HP on Target (103px)** — same A gauges, Screen CX = 21/41/62/82px.

### GroupWindow (10 gauges)

**Multi-color candidates**: GW_Gauge1–5 (114×24, member HP)  
**Single-color**: GW_PetGauge1–5 (114×2, too thin for multi-color)

**Recommendation: 3-band for performance** (red/yellow/green)

Each member's HP: 7 elements × 5 members = **35 elements** (vs 55 for 5-band).

3-band thresholds at 33%/67%:
```
GaugeOffsetX: -3333, -6667  (with effective_width 10000)
Screen CX:    38, 76  (114px ÷ 3 ≈ 38px bands)
```

This requires 2 additional shared animations:
```xml
<Ui2DAnimation item="A_MCFill_Third1">  <!-- 33% threshold -->
    <Location><X>-3333</X><Y>8</Y></Location>
    <Size><CX>10000</CX><CY>8</CY></Size>
</Ui2DAnimation>
<Ui2DAnimation item="A_MCFill_Third2">  <!-- 67% threshold -->
    <Location><X>-6667</X><Y>8</Y></Location>
    <Size><CX>10000</CX><CY>8</CY></Size>
</Ui2DAnimation>
```

Or reuse `A_MCFill_Band2` (40% threshold) and `A_MCFill_Band4` (80% threshold) for a less even but animation-reusing 3-band approach.

### PetInfoWindow (2 gauges)

**Multi-color candidate**: PIW_PetHPGauge (128×15)  
**Single-color**: PIW_PetManaGauge (120×4, too thin)

PetHP at 128px: Screen CX = 26/51/77/102 for 5 bands (same `A_MCFill_Band1–4`).

Note the anomaly: current gauge uses `A_GaugeFill_120t` for a 128px-wide element — 8px shortfall. The multi-color A gauges don't have this problem (oversized by design). The base fill and B gauges should use `A_MCFill_Base` (CX=300) which covers 128px comfortably.

### Other Windows (single-color)

These windows keep their current single-color gauges unchanged:

| Window | Gauges | Reason |
|--------|--------|--------|
| CastSpellWnd | 9 recast bars (146×3) | Timer gauges — no urgency color needed |
| Inventory | 3 XP/AAXP (102×8) | Progress only goes up |
| MerchantWnd | 1 XP (111×8) | Progress only goes up |
| AAWindow | 1 AAXP (108×28) | Progress only goes up |
| SpellBookWnd | 2 (memorize/scribe, 102×8) | Short-lived progress bars |
| CastingWindow | 1 (0×0, hidden) | Not visible |
| TrainWindow | 1 (0×0, hidden) | Not visible |
| MusicPlayer | 1 (0×0, hidden) | Not visible |
| BreathWindow | 1 (116×8) | Could be 2-band (future) |

---

## Implementation Roadmap

### Phase 1: Prototype & Verify (Single Gauge)

**Goal**: Confirm the GaugeOffsetX model works as expected in TAKP.

1. Add `A_MCFill_Band1–4` and `A_MCFill_Base` to `EQUI_Animations.xml` (5 new animations)
2. Implement 5-band multi-color on `PW_Gauge_HP` (120px) in `EQUI_PlayerWindow.xml`
3. Use Classic palette (red→green) for initial testing
4. Test in-game: verify thresholds activate at ~20/40/60/80% HP
5. If Model B is wrong (thresholds are off), adjust formula and re-derive offsets

**Deliverable**: One working multi-color HP gauge, validated threshold formula.

### Phase 2: PlayerWindow Complete

**Goal**: Multi-color on all Tier 1 PlayerWindow gauges.

1. Apply same pattern to `PW_Gauge_PetHP` (120px, purple or shared palette)
2. Optionally apply to `PW_Gauge_Mana` (120px, blue palette, possibly 3-band)
3. Add DuxaUI-style transparent overlay for Lines consistency (if desired)
4. Test all gauges at various HP/Mana levels

### Phase 3: TargetWindow

**Goal**: Multi-color on target and self HP gauges.

1. `TW_TargetHP_Gauge` (250px) — highest combat value
2. `TW_PlayerHP_Gauge` (103px)
3. `TW_PetHealth_Gauge` (103px)
4. Same shared `A_MCFill_Band1–4` — only layout math changes

### Phase 4: Group & Pet Windows

**Goal**: Multi-color for group healing feedback.

1. `GW_Gauge1–5` (114px) — recommend 3-band for performance
2. `PIW_PetHPGauge` (128px) — 5-band
3. Performance test with all group gauges active (35–55 new elements)

### Phase 5: Polish & Options

**Goal**: Palette selection and visual refinement.

1. Document palette options for users (Classic, Ember Glow, Ocean, etc.)
2. Consider palette as a gauge Option alongside gauge style variants
3. Add EndCap icons (DuxaUI-style) if desired
4. Add transparent overlay for Lines consistency across windows

---

*This analysis documents the technique and architecture. Implementation requires in-game testing to verify the GaugeOffsetX threshold model. The size-agnostic animation system and flexible palette architecture ensure that once the core is proven, extending to any gauge in any window is pure layout math — no new animations needed.*
