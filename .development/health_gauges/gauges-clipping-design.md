# Multi-Color Gauges via Clipping — Design Document

> **ARCHIVED**: This approach (rainbow bar clipping) was explored but **not
> adopted**. Thorne uses the oversized A/B split pattern instead. See
> [README.md](README.md) for the implemented system.

**Date**: March 4, 2026  
**Author**: Draknare Thorne  
**Status**: Archived — approach not adopted (rainbow bar, not threshold)  
**Prerequisite**: [gauges-analysis.md](gauges-analysis.md) (core technique reference)

---

## Table of Contents

- [Multi-Color Gauges via Clipping — Design Document](#multi-color-gauges-via-clipping--design-document)
  - [Table of Contents](#table-of-contents)
  - [The Problem with Stretching](#the-problem-with-stretching)
  - [How Thorne's Gauge Textures Work Today](#how-thornes-gauge-textures-work-today)
    - [The Four-Section Layout](#the-four-section-layout)
    - [How Background and Fill Interact](#how-background-and-fill-interact)
    - [The Four Texture Family Patterns](#the-four-texture-family-patterns)
      - [Family 1: Show-Through Structural (Thorne, Grid, Thorne 7, Basic)](#family-1-show-through-structural-thorne-grid-thorne-7-basic)
      - [Family 2: Opaque Gradient (Bars, Oval)](#family-2-opaque-gradient-bars-oval)
      - [Family 3: Bubble/Organic Texture (Bubbles, Light Bubbles)](#family-3-bubbleorganic-texture-bubbles-light-bubbles)
      - [Family 4: Tall Variant Alpha Patterns (All variants at 120t)](#family-4-tall-variant-alpha-patterns-all-variants-at-120t)
  - [Why Stretching Destroys The Pattern](#why-stretching-destroys-the-pattern)
  - [The Clipping Approach](#the-clipping-approach)
    - [Core Idea](#core-idea)
    - [How It Works — Step by Step](#how-it-works--step-by-step)
    - [Why The Pattern Survives](#why-the-pattern-survives)
  - [Layer Architecture](#layer-architecture)
    - [Current Single-Color Stack](#current-single-color-stack)
    - [Proposed Multi-Color Stack](#proposed-multi-color-stack)
    - [Z-Order and Rendering](#z-order-and-rendering)
  - [Concrete Example: HP Gauge (120px, 4 Bands)](#concrete-example-hp-gauge-120px-4-bands)
    - [Band Layout](#band-layout)
    - [Full XML](#full-xml)
    - [How It Renders at Different HP Levels](#how-it-renders-at-different-hp-levels)
  - [Animation Requirements](#animation-requirements)
    - [Reuse Existing Animations](#reuse-existing-animations)
    - [No New Animations Needed](#no-new-animations-needed)
  - [How EQType Sharing Works](#how-eqtype-sharing-works)
  - [Handling the Background](#handling-the-background)
    - [Approach A: Single Background Gauge (Simplest)](#approach-a-single-background-gauge-simplest)
    - [Approach B: Static Background Animation](#approach-b-static-background-animation)
  - [Applying to All Gauge Sizes](#applying-to-all-gauge-sizes)
    - [Tall Gauges (16px) — HP, Mana, XP, AAXP, PetHP](#tall-gauges-16px--hp-mana-xp-aaxp-pethp)
    - [Standard Gauges (8px) — Target bars, Stamina](#standard-gauges-8px--target-bars-stamina)
    - [Thin/Tick Gauges — PetGauge, GlobalRecast](#thintick-gauges--petgauge-globalrecast)
  - [Palette Configuration](#palette-configuration)
  - [Comparing the Two Approaches](#comparing-the-two-approaches)
    - [Key Risk: Negative Location in Screen](#key-risk-negative-location-in-screen)
  - [Implementation Roadmap](#implementation-roadmap)
    - [Phase 1: Proof of Concept (test one gauge)](#phase-1-proof-of-concept-test-one-gauge)
    - [Phase 2: Validate Edge Cases](#phase-2-validate-edge-cases)
    - [Phase 3: Roll Out to Key Gauges](#phase-3-roll-out-to-key-gauges)
    - [Phase 4: Options Integration](#phase-4-options-integration)
  - [Open Questions for Testing](#open-questions-for-testing)

---

## The Problem with Stretching

The [gauges-analysis.md](gauges-analysis.md) documents the technique used by Nillipuss and DuxaUI: make gauges 8000–10000px wide, use `GaugeOffsetX` thresholds to control when each color band becomes visible, and clip the result through a Screen container.

The fill animations that power those oversized gauges reference the same small source texture (100–120px) but declare `CX=10000`. The EQ client **stretches** the source to fill that virtual space. A 120px texture stretched to 10000px means each source pixel covers ~83 display pixels. Any gradient, pattern, or alpha variation in the source fill is obliterated — the visible 30px band sees effectively flat color.

**This is acceptable for Nillipuss and DuxaUI** because their fill textures are simple flat or near-flat patterns. Their visual identity doesn't depend on fill texture detail.

**This is NOT acceptable for Thorne** because Thorne's fill textures contain deliberate alpha gradients, show-through gaps, and pattern work that interact with the background to create dimensional depth. Stretching destroys the signature look.

---

## How Thorne's Gauge Textures Work Today

### The Four-Section Layout

Each gauge `.tga` has four vertically stacked sections:

```
┌─────────────────────────────────┐  Y=0
│         Background              │  Opaque base with line/pattern art
├─────────────────────────────────┤  Y=H
│         Fill                    │  Colorized fill with alpha gaps
├─────────────────────────────────┤  Y=2H
│         Lines                   │  XP progress line overlay
├─────────────────────────────────┤  Y=3H
│         LinesFill               │  XP progress fill overlay
└─────────────────────────────────┘  Y=4H

Standard: H=8px (103px wide)
Tall:     H=16px (120px wide)
```

The EQ client renders them as layers:

1. **Background** renders first (always, full width)
2. **Fill** renders on top, clipped to the fill percentage (HP%, Mana%, etc.)
3. **Lines** renders on top (divider marks, e.g. 10% ticks on XP)
4. **LinesFill** renders on top of Lines, clipped to fill percentage

### How Background and Fill Interact

The critical design principle: **Fill has deliberate transparent gaps that let the Background show through**. This creates the distinctive Thorne gauge look — the fill isn't a flat bar, it's a patterned overlay that reveals the background's line work.

Pixel analysis of the center row for each standard gauge (first 30 columns shown):

**Thorne** — Fill has isolated transparent columns at tick positions:
```
BG alpha: 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 ...  (all opaque)
Fill  a :   0 255 255 255 255 255 255 255 255 255 255 255 255 255 255 ... 255   0 255 ...
Lines a : 255   0   0   0   0   0 255   0   0   0   0   0 255   0   0 ...   0 255   0 ...
             ↑                       ↑                       ↑           ↑
          show-through            show-through            show-through   show-through
```

Where Fill alpha=0 and BG alpha=255: the background line/pattern shows through the fill gap.
Where Lines alpha=255: the XP tick marks overlay everything (only relevant if DrawLinesFill=true).

**Grid** — Same tick pattern as Thorne, more evenly spaced:
```
Fill  a :   0 255 255 255 255 255   0 255 255 255 255 255   0 255 255 255 255 255   0 ...
Lines a : 255   0   0   0   0   0 255   0   0   0   0   0 255   0   0   0   0   0 255 ...
```
Fill and Lines are exact inverses — every 6th pixel is a show-through column.

**Bars** / **Bubbles** / **Oval** / **Light Bubbles** — Fill has no transparent gaps:
```
Fill  a : 255 255 255 255 255 255 255 255 255 255 255 255 255 ...  (all opaque)
```
These rely on RGB gradient variation for their visual texture rather than show-through.

### The Four Texture Family Patterns

Analysis of all 8 gauge variants reveals four distinct design strategies:

#### Family 1: Show-Through Structural (Thorne, Grid, Thorne 7, Basic)

```
Background:  Opaque with rich patterns (20-41 shades in tall)
Fill:        Alpha gaps at regular intervals → BG peeks through
Lines:       Tick marks at show-through positions (or empty)
LinesFill:   Empty
```

- The visual identity comes from **Background + Fill alpha gap alignment**
- Fill color comes from `FillTint` multiplied against gray fill pixels (~198 gray)
- The pattern must render at native resolution to preserve the gap alignment

#### Family 2: Opaque Gradient (Bars, Oval)

```
Background:  Opaque with subtle shading
Fill:        Fully opaque with RGB gradient (4-23 shades)
Lines:       Semi-transparent or empty
LinesFill:   Semi-transparent or empty
```

- The visual identity comes from **Fill RGB variation** (subtle shading within the bar)
- `FillTint` multiplies against the existing gradient
- Tolerates slight stretching better, but still loses gradient detail

#### Family 3: Bubble/Organic Texture (Bubbles, Light Bubbles)

```
Background:  Opaque (flat or gentle gradient)
Fill:        Fully opaque with gentle gradient (8-16 shades)
Lines:       Alpha-varied overlay (sparse accents)
LinesFill:   Alpha-varied overlay (sparse accents)
```

- Visual identity from **Fill gradient + Lines accent overlay**
- The subtle gradient in Fill creates organic dimensional depth
- Stretching would flatten the bubble contours

#### Family 4: Tall Variant Alpha Patterns (All variants at 120t)

```
120t Fill:   6 distinct alpha levels (0, 40, 98, 178, 255)
             Row 0 and 15: fully transparent border
             Rows 1-14: repeating column alpha pattern
```

Example Thorne tall fill alpha (sampled every 8px):
```
[0, 255, 255, 98, 255, 255, 40, 255, 255, 178, 255, 255, 255, 255, 255]
```

This columnar alpha gradient is what HP/Mana gauges actually use. The varying alpha creates the dimensional depth when `FillTint` colorizes it — semi-transparent columns (40, 98, 178) let the rich Background partially show through, creating the signature gauged look.

---

## Why Stretching Destroys The Pattern

When `A_GaugeFill_120t` (CX=120, from a 120px source) fills a standard gauge:

```
Source: [0, 255, 255, 98, 255, 255, 40, 255, 255, 178, ...]  (120 alpha values)
        ↓ 1:1 mapping
Display: identical pattern, perfect fidelity
```

When a proposed `A_MCFill_Band` (CX=10000, from the same 120px source) fills an oversized gauge:

```
Source: [0, 255, 255, 98, 255, 255, 40, 255, 255, 178, ...]  (120 alpha values)
        ↓ stretched 83x
Display: each value spans ~83 pixels. In any 30px band you see at most
         1-2 alpha transitions. The pattern is gone.
```

For **Family 1** (show-through structural): The 1px transparent gaps become 83px transparent bands or disappear entirely. The signature line show-through effect is destroyed.

For **Family 4** (tall alpha columns): The subtle graduated transparency (40→98→178→255) that creates depth becomes a 300+ pixel wide flat zone. No dimensional quality survives.

---

## The Clipping Approach

### Core Idea

Instead of making gauges absurdly wide and stretching, **keep gauges at their native size** and use Screen containers to show only the relevant segment of each band. The fill texture renders at native resolution — zero stretching, zero pattern loss.

```
┌──────────────────────────────────────────────────────────┐
│  STRETCHING (Nillipuss/DuxaUI):                          │
│    Animation CX=10000 → texture stretched ~83x → flat    │
│                                                          │
│  CLIPPING (proposed):                                    │
│    Animation CX=120 → texture at 1:1 → pattern intact   │
│    Screen clips to the visible band → color from Tint    │
└──────────────────────────────────────────────────────────┘
```

### How It Works — Step by Step

For an HP gauge that is 120px wide with 4 color bands of 30px each:

**Step 1**: Create 4 Screen containers, each 30px wide, tiled across the gauge's position:

```
 ←30px→ ←30px→ ←30px→ ←30px→
┌──────┬──────┬──────┬──────┐
│ Scr1 │ Scr2 │ Scr3 │ Scr4 │
│ red  │orange│yellow│green │
└──────┴──────┴──────┴──────┘
  X=0    X=30   X=60   X=90
```

**Step 2**: Inside each Screen, place a full-width gauge (CX=120) with a negative X offset so the correct portion of the fill is visible through the Screen's clip window:

```
Screen 1 (X=0, CX=30):
  └─ Gauge (Location X=0, CX=120, FillTint=red)
     Fill renders 0 to 120×HP%. Screen shows columns 0-29.

Screen 2 (X=30, CX=30):
  └─ Gauge (Location X=-30, CX=120, FillTint=orange)
     Fill renders 0 to 120×HP%. Screen shows columns 30-59.

Screen 3 (X=60, CX=30):
  └─ Gauge (Location X=-60, CX=120, FillTint=yellow)
     Fill renders 0 to 120×HP%. Screen shows columns 60-89.

Screen 4 (X=90, CX=30):
  └─ Gauge (Location X=-90, CX=120, FillTint=green)
     Fill renders 0 to 120×HP%. Screen shows columns 90-119.
```

**Step 3**: Each gauge shares the same EQType (1=HP) so they all track the same value. They all use the same fill animation (`A_GaugeFill_120t`). Only `FillTint` differs.

### Why The Pattern Survives

The key: each band's gauge is CX=120 using animation `A_GaugeFill_120t` (also CX=120). It's a 1:1 pixel mapping. The Screen container simply masks which 30px segment you see.

```
Full gauge fill at 60% HP (72px filled):
  pixel: 0    10   20   30   40   50   60   70   80   90   100  110  120
  alpha: 0 255 255 98 255 255 40 255 255 178 255 255 ...  (native pattern)
         ↑←  Screen 1  →↑←  Screen 2  →↑←  Screen 3  →↑←  Screen 4  →↑
         red (filled)    orange (filled)  yellow (part)  green (empty)
```

Every pixel retains its original alpha value. The show-through gaps align with the background exactly as they do today. The dimensional depth from the tall alpha gradient columns (40, 98, 178, 255) is perfectly preserved.

The only difference from today's single-color gauge: each 30px segment is tinted a different color.

---

## Layer Architecture

### Current Single-Color Stack

Today, your HP gauge is a single element:

```xml
<Gauge item="PW_Gauge_HP">
    <!-- EQType=1, CX=120, CY=16 -->
    <FillTint><R>255</R><G>0</G><B>0</B></FillTint>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
```

Layer stack (bottom to top):
```
┌──────────────────────────────────┐
│  Background (120px, full width)  │  gauge_inlay120t: Y=0-15, rich pattern
├──────────────────────────────────┤
│  Fill (120×HP%, tinted red)      │  gauge_inlay120t: Y=16-31, alpha gradient
└──────────────────────────────────┘
```

### Proposed Multi-Color Stack

```
┌──────────────────────────────────────────────────────┐
│  Layer 0: Background gauge (full width, EQType=1)    │  Same as today
├──────────┬──────────┬──────────┬─────────────────────┤
│  Layer 1 │  Layer 2 │  Layer 3 │  Layer 4            │  Band fills
│  Band 1  │  Band 2  │  Band 3  │  Band 4             │  (Screens with
│  Red     │  Orange  │  Yellow  │  Green               │   clipped gauges)
│  0-30px  │  30-60px │  60-90px │  90-120px            │
├──────────┴──────────┴──────────┴─────────────────────┤
│  Layer 5: Overlay gauge (transparent, text/tooltip)   │  Optional: ScreenID
└──────────────────────────────────────────────────────┘
```

### Z-Order and Rendering

XML elements are rendered in declaration order (later = on top). The sequence:

1. **Background gauge**: renders the full background pattern, always visible
2. **Band screens**: each clips a fill gauge to its 30px zone, each with its own FillTint
3. **Overlay gauge** (optional): transparent, no fill, carries the ScreenID for EQ client interaction (tooltip, click-through, HP text display)

The fill in each band renders with the same native animation. The alpha patterns in the fill interact with the background below exactly as they do today. The only difference is color per segment.

---

## Concrete Example: HP Gauge (120px, 4 Bands)

### Band Layout

| Band | HP Range | Screen Position | Screen Width | Gauge X Offset | FillTint |
|------|----------|----------------|-------------|----------------|----------|
| 1 | 0–25% | X=2, Y=26 | CX=30 | X=0 | Red (255,0,0) |
| 2 | 25–50% | X=32, Y=26 | CX=30 | X=-30 | Orange (240,120,0) |
| 3 | 50–75% | X=62, Y=26 | CX=30 | X=-60 | Yellow (240,240,0) |
| 4 | 75–100% | X=92, Y=26 | CX=30 | X=-90 | Green (0,220,0) |

### Full XML

```xml
<!-- ====================================================================== -->
<!-- HP GAUGE — Multi-Color via Clipping -->
<!-- ====================================================================== -->

<!-- Layer 0: Background (full width, always visible) -->
<Gauge item="PW_HP_BG">
    <ScreenID>PlayerHP</ScreenID>
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>255</R>
        <G>0</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
    </GaugeDrawTemplate>
</Gauge>

<!-- Layer 1: Band 1 — Red (0-25%) -->
<Gauge item="PW_HP_Band1">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>255</R>
        <G>0</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band1_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band1</Pieces>
</Screen>

<!-- Layer 2: Band 2 — Orange (25-50%) -->
<Gauge item="PW_HP_Band2">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-30</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>240</R>
        <G>120</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band2_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>32</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band2</Pieces>
</Screen>

<!-- Layer 3: Band 3 — Yellow (50-75%) -->
<Gauge item="PW_HP_Band3">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-60</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>240</R>
        <G>240</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band3_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>62</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band3</Pieces>
</Screen>

<!-- Layer 4: Band 4 — Green (75-100%) -->
<Gauge item="PW_HP_Band4">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-90</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>0</R>
        <G>220</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band4_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>92</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band4</Pieces>
</Screen>

<!-- Layer 5: Overlay — Transparent for ScreenID/Tooltip -->
<Gauge item="PW_Gauge_HP">
    <ScreenID>PW_Gauge_HP</ScreenID>
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetY>-250</TextOffsetY>
    <Style_Transparent>true</Style_Transparent>
    <FillTint>
        <R>0</R>
        <G>0</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate />
</Gauge>
```

### How It Renders at Different HP Levels

**At 100% HP (120px fill):**
```
 ← Band 1 → ← Band 2 → ← Band 3 → ← Band 4 →
┌──────────┬──────────┬──────────┬──────────┐
│▓▓▓▓▓▓▓▓▓▓│▓▓▓▓▓▓▓▓▓▓│▓▓▓▓▓▓▓▓▓▓│▓▓▓▓▓▓▓▓▓▓│  all bands filled
│   RED    │  ORANGE  │  YELLOW  │  GREEN   │
└──────────┴──────────┴──────────┴──────────┘
   30px       30px       30px       30px
```

**At 60% HP (72px fill):**
```
 ← Band 1 → ← Band 2 → ← Band 3 → ← Band 4 →
┌──────────┬──────────┬──────────┬──────────┐
│▓▓▓▓▓▓▓▓▓▓│▓▓▓▓▓▓▓▓▓▓│▓▓▓▓▓▓░░░░│          │
│   RED    │  ORANGE  │ YELLOW   │   (bg)   │
│  (full)  │  (full)  │ (12/30)  │          │
└──────────┴──────────┴──────────┴──────────┘
```

**At 20% HP (24px fill):**
```
 ← Band 1 → ← Band 2 → ← Band 3 → ← Band 4 →
┌──────────┬──────────┬──────────┬──────────┐
│▓▓▓▓▓▓▓▓░░│          │          │          │
│   RED    │   (bg)   │   (bg)   │   (bg)   │
│  (24/30) │          │          │          │
└──────────┴──────────┴──────────┴──────────┘
```

In every case, the filled area uses the fill texture at 1:1 pixel resolution. The alpha gradient columns (40, 98, 178, 255) create the same depth effect as today, and the show-through gaps reveal the background pattern exactly as they do in single-color mode.

---

## Animation Requirements

### Reuse Existing Animations

The clipping approach uses **the exact same animations** defined today:

| Animation | Source | Section | Used By |
|-----------|--------|---------|---------|
| `A_GaugeBackground_120t` | `gauge_inlay120t_thorne01.tga` | Y=0, CX=120, CY=16 | Background layer |
| `A_GaugeFill_120t` | `gauge_inlay120t_thorne01.tga` | Y=16, CX=120, CY=16 | All band fills |
| `A_GaugeLines_120t` | `gauge_inlay120t_thorne01.tga` | Y=32, CX=120, CY=16 | XP Lines overlay |
| `A_GaugeLinesFill_120t` | `gauge_inlay120t_thorne01.tga` | Y=48, CX=120, CY=16 | XP LinesFill |

### No New Animations Needed

Unlike the stretching approach (which requires 4 new oversized `A_MCFill_Band1-4` animations), the clipping approach needs **zero** new animation definitions. Color changes come entirely from `FillTint` on the gauge elements.

This also means:
- No changes to `EQUI_Animations.xml`
- All existing gauge style variants (Thorne, Bars, Bubbles, etc.) work automatically
- Switching gauge styles via Options still works — swap the texture file, same animations

---

## How EQType Sharing Works

All band gauges share the same `<EQType>1</EQType>` (HP). The EQ client binds each gauge to the player's HP percentage independently. When HP changes, all band gauges in the window update simultaneously to the same fill level.

Since each gauge is positioned at a different offset within its Screen clip, they collectively render as a single multi-color bar despite being independent gauge elements.

**Important**: Only ONE gauge should have the real `<ScreenID>PlayerHP</ScreenID>` (or `PW_Gauge_HP` for Thorne's current naming). This is the gauge the EQ client uses for interaction (tooltip, text display). The band gauges should omit ScreenID or use non-conflicting identifiers.

---

## Handling the Background

### Approach A: Single Background Gauge (Simplest)

Use a standard gauge with only `<Background>` in the draw template. No fill, no lines. This renders the full background pattern across the entire gauge width regardless of HP percentage.

```xml
<Gauge item="PW_HP_BG">
    <ScreenID>PlayerHP</ScreenID>
    <EQType>1</EQType>
    <Size><CX>120</CX><CY>16</CY></Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
    </GaugeDrawTemplate>
</Gauge>
```

The background renders at full width because `<Background>` is not clipped to fill percentage — it draws the entire background animation regardless of the gauge value. This is exactly how DuxaUI's `PW_Guage_BlackBgd` works.

### Approach B: Static Background Animation

Alternatively, use a `<StaticAnimation>` for the background (non-gauge rendering):

```xml
<StaticAnimation item="PW_HP_BG_Static">
    <RelativePosition>true</RelativePosition>
    <Location><X>2</X><Y>26</Y></Location>
    <Size><CX>120</CX><CY>16</CY></Size>
    <Animation>A_GaugeBackground_120t</Animation>
</StaticAnimation>
```

This is simpler but doesn't participate in gauge ScreenID binding. **Approach A is recommended** because it keeps the ScreenID on a gauge element, which the EQ client expects.

---

## Applying to All Gauge Sizes

### Tall Gauges (16px) — HP, Mana, XP, AAXP, PetHP

These are the prime candidates for multi-color. They use `A_GaugeFill_120t` and have the richest fill patterns (6 alpha levels in the tall texture).

| Gauge | CX | Bands | Band Width | Animation |
|-------|----|-------|-----------|-----------|
| HP | 120 | 4 | 30px | A_GaugeFill_120t |
| Mana | 120 | 4 | 30px | A_GaugeFill_120t |
| PetHP | 120 | 4 | 30px | A_GaugeFill_120t |
| TargetHP | 250 | 4 | ~62px | A_GaugeFill_250t |

For XP and AAXP: multi-color is less useful (XP doesn't represent "health urgency"). These can stay single-color.

**Band formula**: For N bands on a CX-wide gauge:
```
Band_Width = CX / N
Screen_i.X = gauge_start_X + (i-1) × Band_Width
Gauge_i.Location.X = -(i-1) × Band_Width
```

### Standard Gauges (8px) — Target bars, Stamina

These use `A_GaugeFill` (103px) or `A_GaugeFill_120` (120px wide). Same clipping approach, just thinner.

| Gauge | CX | Bands | Band Width | Animation |
|-------|----|-------|-----------|-----------|
| PlayerHP (target) | 103 | 4 | ~26px | A_GaugeFill |
| PlayerMana (target) | 103 | 4 | ~26px | A_GaugeFill |
| Stamina | 120 | 3 | 40px | A_GaugeFill_120 |

For 103px gauges with uneven division: use bands of 26+26+26+25 (or 25+26+26+26).

### Thin/Tick Gauges — PetGauge, GlobalRecast

2–4px thin gauges. Multi-color is visually negligible at this height. **Not worth the complexity** — keep single-color.

---

## Palette Configuration

Colors are defined entirely in XML `<FillTint>` elements — no texture changes required. Switching color palettes means editing only the RGB values in each band gauge.

Example palettes (from [gauges-analysis.md](gauges-analysis.md)):

| Palette | Band 1 (low) | Band 2 | Band 3 | Band 4 (high) |
|---------|-------------|--------|--------|---------------|
| **Classic** | Red (255,0,0) | Orange (240,120,0) | Yellow (240,240,0) | Green (0,220,0) |
| **Warm** | Deep Red (180,0,0) | Red (240,40,0) | Orange (240,160,0) | Gold (220,200,0) |
| **Cool** | Purple (160,0,200) | Blue (40,80,240) | Cyan (0,200,220) | Teal (0,220,160) |
| **Ember** | Dark Red (140,0,0) | Crimson (200,30,0) | Flame (240,80,0) | Amber (240,200,40) |

Each palette is just 4 sets of RGB values in the window XML. No animation changes, no texture changes.

---

## Comparing the Two Approaches

| Aspect | Stretching (Nillipuss/DuxaUI) | Clipping (proposed) |
|--------|-------------------------------|---------------------|
| **Fill pattern fidelity** | Destroyed (83x stretch) | Perfect (1:1 pixels) |
| **New animations needed** | 4+ oversized fills per size class | None |
| **EQUI_Animations.xml changes** | Yes (significant additions) | No |
| **Gauge elements per bar** | 9+ (BG + 4×A + 4×B) | 6 (BG + 4 bands + overlay) |
| **XML complexity** | High (A/B split, GaugeOffsetX math) | Moderate (Screen+Gauge pairs) |
| **Works with gauge style Options** | Partially (B gauges keep pattern) | Fully (all bands keep pattern) |
| **Color palette changes** | FillTint only | FillTint only |
| **Proven in production** | Yes (Nillipuss, DuxaUI) | No (needs testing) |
| **Risk** | None (known technique) | Negative gauge Location needs validation |

### Key Risk: Negative Location in Screen

The clipping approach relies on placing a gauge at a **negative X offset** inside a Screen container (e.g., `Location X=-30`). This positions the gauge so the Screen's clip window shows a middle segment of the fill.

**This needs in-game testing.** The EQ client should support negative coordinates since elements are positioned relative to their parent container, and the Screen is what clips. But the TAKP client has quirks — this must be verified before committing to this approach.

**Fallback**: If negative Location inside Screen doesn't work, the stretching approach remains available. The approaches aren't mutually exclusive — you could even use clipping for tall gauges (where pattern matters most) and stretching for standard gauges (where pattern is simpler).

---

## Implementation Roadmap

### Phase 1: Proof of Concept (test one gauge)

1. Modify `EQUI_PlayerWindow.xml` — replace the single HP gauge with the multi-color clipped version (XML from [Concrete Example](#full-xml) above)
2. Sync to `thorne_dev`
3. Test in-game with `/loadskin thorne_dev`
4. Verify:
   - [ ] Fill pattern displays correctly in each band
   - [ ] Color transitions visible at correct HP thresholds
   - [ ] Negative Location X works inside Screen container
   - [ ] Background renders full-width behind all bands
   - [ ] Overlay gauge receives tooltip / text correctly
   - [ ] No visual artifacts at band boundaries
   - [ ] All gauge styles (Thorne, Bars, Bubbles...) render correctly

### Phase 2: Validate Edge Cases

5. Test at various HP percentages: 100%, 75% (band boundary), 50%, 25%, 1%
6. Test gauge style switching (swap `gauge_inlay120t_*.tga` files)
7. Test different band counts (3 bands, 5 bands)

### Phase 3: Roll Out to Key Gauges

8. Apply to Mana gauge (same 120px tall pattern)
9. Apply to TargetHP (250px tall — wider bands)
10. Apply to PlayerHP/PlayerMana in TargetWindow (103px standard)
11. Apply to GroupWindow gauges (114px standard)

### Phase 4: Options Integration

12. Document multi-color as a gauge Option variant
13. Provide single-color and multi-color variants in Options
14. Update palette configurations per user preference

---

## Open Questions for Testing

1. **Negative Location X**: Does the TAKP client honor negative `<X>` values for gauge elements inside Screen containers? This is the fundamental requirement.

2. **Fill Clipping Direction**: The fill always grows left-to-right. Does moving the gauge left (negative X) correctly shift which pixels are visible through the screen? Or does the fill's clip calculation change relative to the screen rather than the gauge?

3. **Band Boundary Seams**: At exactly 25%/50%/75% HP, the fill edge lands at a band boundary. Is there a 1px rendering seam or gap visible?

4. **Performance**: 4 gauge elements + 4 screens per bar vs. 1 gauge. Is there measurable frame impact? (Likely negligible, but worth confirming.)

5. **GaugeOffsetX Alternative**: If negative Location doesn't work, can `GaugeOffsetX` achieve the same effect? E.g., `<GaugeOffsetX>-30</GaugeOffsetX>` on a gauge positioned at the Screen's origin to shift which fill pixels are visible.

6. **Background as Gauge vs StaticAnimation**: Does the ScreenID binding work correctly when the background gauge has `<Background>` only and no `<Fill>`?
