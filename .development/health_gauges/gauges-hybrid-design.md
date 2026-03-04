# Multi-Color Gauges via Hybrid Stretch — Design Document

**Date**: March 4, 2026  
**Author**: Draknare Thorne  
**Status**: Research — Third Approach to Multi-Color Gauges  
**Prerequisites**:

- [gauges-analysis.md](gauges-analysis.md) (core technique, full inventory)
- [gauges-clipping-design.md](gauges-clipping-design.md) (clipping approach, texture analysis)

---

## Table of Contents

- [Multi-Color Gauges via Hybrid Stretch — Design Document](#multi-color-gauges-via-hybrid-stretch--design-document)
  - [Table of Contents](#table-of-contents)
  - [Summary of the Three Approaches](#summary-of-the-three-approaches)
  - [The Hybrid Concept](#the-hybrid-concept)
    - [Why Scale Matters](#why-scale-matters)
    - [Choosing the Stretch Factor](#choosing-the-stretch-factor)
  - [Visual Behavior: Solid Color That Changes](#visual-behavior-solid-color-that-changes)
    - [How the Threshold Mechanic Works](#how-the-threshold-mechanic-works)
    - [HP Level Visual Walkthrough](#hp-level-visual-walkthrough)
  - [Hybrid Mathematics for 120px Gauge](#hybrid-mathematics-for-120px-gauge)
    - [4-Band Layout (30px bands)](#4-band-layout-30px-bands)
    - [A Gauge Calculations](#a-gauge-calculations)
    - [B Gauge Calculations](#b-gauge-calculations)
  - [Stretch Factor Impact on Fill Patterns](#stretch-factor-impact-on-fill-patterns)
    - [Pattern Fidelity at Different Stretch Factors](#pattern-fidelity-at-different-stretch-factors)
    - [Per-Family Analysis](#per-family-analysis)
  - [Animation Definitions (New)](#animation-definitions-new)
    - [Hybrid Fill Animations for 120t](#hybrid-fill-animations-for-120t)
  - [Concrete Example: HP Gauge (120px, 4 Bands)](#concrete-example-hp-gauge-120px-4-bands)
    - [Full XML](#full-xml)
  - [Comparing All Three Approaches](#comparing-all-three-approaches)
  - [When to Use Which Approach](#when-to-use-which-approach)

---

## Summary of the Three Approaches

| Approach | Visual Behavior | Pattern Fidelity | Complexity |
|----------|----------------|-------------------|------------|
| **Full Stretch** (Nillipuss/DuxaUI) | Solid color that changes | Destroyed | High (A/B pairs, CX=10000) |
| **Clipping** (gauges-clipping-design) | Rainbow bar always | Perfect | Moderate (Screen clips) |
| **Hybrid Stretch** (this document) | Solid color that changes | Degraded but recognizable | High (A/B pairs, CX=480) |

The hybrid approach preserves the **solid-color-that-changes behavior** of the Nillipuss/DuxaUI technique while reducing the stretch factor from ~83× to ~4×, keeping fill patterns partially recognizable.

---

## The Hybrid Concept

### Why Scale Matters

The full stretch technique uses CX=10000 for gauges that display in a 120px window, creating an 83× stretch that obliterates any source pattern. But the stretching isn't the point — the **oversized offset thresholds** are the point. The question: how oversized do the gauges really need to be?

The answer: they only need to be large enough that the `GaugeOffsetX` thresholds create the correct activation points.

### Choosing the Stretch Factor

For a 120px gauge with 4 equal bands of 30px each, the threshold offsets are:

```
Band 1 threshold: GaugeOffsetX = 0        (always visible when any HP)
Band 2 threshold: GaugeOffsetX = -offset₂  (visible when HP > 25%)
Band 3 threshold: GaugeOffsetX = -offset₃  (visible when HP > 50%)
Band 4 threshold: GaugeOffsetX = -offset₄  (visible when HP > 75%)
```

The formula is: `offset_n = (band_boundary / gauge_width) × gauge_CX`

If we set `gauge_CX = 480` (4× the display width of 120):

```
Band 2: offset = (30/120) × 480 = 120
Band 3: offset = (60/120) × 480 = 240
Band 4: offset = (90/120) × 480 = 360
```

The fill animation also needs CX=480, stretching 120px source to 480px — a **4× stretch** instead of 83×.

**Why 4× specifically?** It's the ratio of total gauge width to display width. Smaller ratios mean the A gauge (which activates at the threshold) must fit within a tighter clip window. At 4×, the A gauge is 480px wide and the clip screen shows 30px — a 6.25% window. This is tight but functional.

The ratio can be increased for more headroom. Some options:

| Stretch Factor | Gauge CX | Pattern Impact | Headroom |
|----------------|----------|---------------|----------|
| 4× | 480 | Mild blur, pattern visible | Tight |
| 6× | 720 | Noticeable blur, pattern fading | Comfortable |
| 8× | 960 | Significant blur | Generous |
| 10× | 1200 | Heavy blur | Very generous |
| 83× | 10000 | Destroyed (Nillipuss/DuxaUI) | Excessive |

**Recommendation**: Start with 4× (480px) for testing. If visual artifacts appear at band boundaries, increase to 6× (720px).

---

## Visual Behavior: Solid Color That Changes

### How the Threshold Mechanic Works

Unlike the clipping approach (which always shows all colors as segments), the stretching approach layers bands **on top of each other** across the full width. Higher-HP bands occlude lower-HP bands:

```
Z-order (bottom to top):
  Band 1 (red)     — always visible when any HP
  Band 2 (orange)  — paints over entire width, activates at 25%
  Band 3 (yellow)  — paints over entire width, activates at 50%
  Band 4 (green)   — paints over entire width, activates at 75%
```

At 100% HP, the green band covers everything — the bar looks solid green.
At 40% HP, only bands 1 and 2 are active — band 2 (orange) covers band 1 — solid orange.

### HP Level Visual Walkthrough

```
100% HP:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   GREEN (bands 1-4 active, 4 on top)
 90% HP:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░   GREEN edge receding
 75% HP:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░   GREEN/YELLOW transition
 60% HP:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   YELLOW (bands 1-3 active, 3 on top)
 50% HP:  ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░   YELLOW/ORANGE transition
 35% HP:  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░   ORANGE (bands 1-2 active, 2 on top)
 25% HP:  ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░   ORANGE/RED transition
 10% HP:  ▓▓░░░░░░░░░░░░░░░░░░░░░░   RED (only band 1 active)
```

This is the behavior players expect from a health bar — visual urgency that matches danger level.

---

## Hybrid Mathematics for 120px Gauge

### 4-Band Layout (30px bands)

With stretch factor = 4 (gauge CX = 480):

| Band | HP Threshold | Color | GaugeOffsetX |
|------|-------------|-------|-------------|
| 1 | 0% | Red | 0 |
| 2 | 25% | Orange | -120 |
| 3 | 50% | Yellow | -240 |
| 4 | 75% | Green | -360 |

### A Gauge Calculations

Each A gauge activates at its threshold. It's oversized (CX=480) and clipped by a Screen container.

```
A gauge (oversized, threshold trigger):
  Gauge CX = 480 (4× stretch)
  Screen CX = band_width = 30px
  Screen X = gauge_start_X + (band-1) × band_width
  GaugeOffsetX = -(band-1) × (480/4) = -(band-1) × 120
  Fill animation = A_HybridFill_120t_Band{n}
```

The A gauge animation uses `Location X = -(band-1) × 120` to offset within the oversized fill, ensuring the band's visible portion through the Screen clip shows the right fill segment.

### B Gauge Calculations

Each B gauge is the continuation fill — standard size, native resolution. It covers the remaining width after its band position.

```
B gauge (standard size, continuation):
  Gauge CX = display_width - (band-1) × band_width
  Location X = gauge_start_X + (band-1) × band_width
  GaugeOffsetX = -(band-1) × band_width
  Fill animation = A_GaugeFill_120t (native, no stretch)
```

**The B gauges render at 1:1** — they use the existing native-resolution fill animation. This is where pattern fidelity is preserved even in the full-stretch approach. In the hybrid approach, even the A gauges retain most of the pattern.

---

## Stretch Factor Impact on Fill Patterns

### Pattern Fidelity at Different Stretch Factors

At 4× stretch, a 120px source becomes 480 virtual pixels. Each source pixel covers 4 display pixels. Here's what happens to the Thorne tall fill alpha pattern:

```
Source columns: [0, 255, 255, 98, 255, 255, 40, 255, 255, 178, 255, 255, ...]

At 1× (native): [0, 255, 255, 98, 255, 255, 40, 255, 255, 178, ...]
                  ↑ sharp transitions, full depth

At 4× stretch:   [0, 0, 0, 0, 128, 255, 255, 255, 255, 255, 176, 98, 98, ...]
                  ↑ smoothed transitions, some depth preserved

At 83× stretch:  [127, 127, 127, 127, 127, 127, 127, ...]
                  ↑ averaged to flat uniform value
```

The 1px show-through gaps (alpha=0) in Family 1 (Thorne, Grid) become ~4px gaps at 4× stretch. Blurred but still recognizable as the "gapped fill with background showing through" pattern.

### Per-Family Analysis

| Family | At 1× (native) | At 4× (hybrid) | At 83× (full stretch) |
|--------|----------------|-----------------|----------------------|
| **Show-Through** (Thorne, Grid) | Sharp 1px gaps | ~4px soft gaps, still visible | Flat, gaps gone |
| **Opaque Gradient** (Bars, Oval) | Subtle shading | Smoother shading | Flat |
| **Bubble/Organic** (Bubbles, Light Bubbles) | Gentle gradient | Slightly smoother | Flat |
| **Tall Alpha** (120t columns) | 6 alpha levels | Smoothed alpha ramp | Flat |

At 4×, the pattern is "softened" rather than "destroyed." The visual signature is recognizable.

---

## Animation Definitions (New)

### Hybrid Fill Animations for 120t

These animations stretch the 120px fill source to 480px, with band-specific X offsets.

```xml
<!-- Hybrid multi-color fills for 120t tall gauges (4x stretch) -->
<Ui2DAnimation item="A_HybridFill_120t_Band1">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay120t_thorne01.tga</Texture>
        <Location>
            <X>0</X>
            <Y>16</Y>
        </Location>
        <Size>
            <CX>480</CX>
            <CY>16</CY>
        </Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<Ui2DAnimation item="A_HybridFill_120t_Band2">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay120t_thorne01.tga</Texture>
        <Location>
            <X>-120</X>
            <Y>16</Y>
        </Location>
        <Size>
            <CX>480</CX>
            <CY>16</CY>
        </Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<Ui2DAnimation item="A_HybridFill_120t_Band3">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay120t_thorne01.tga</Texture>
        <Location>
            <X>-240</X>
            <Y>16</Y>
        </Location>
        <Size>
            <CX>480</CX>
            <CY>16</CY>
        </Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>

<Ui2DAnimation item="A_HybridFill_120t_Band4">
    <Cycle>true</Cycle>
    <Frames>
        <Texture>gauge_inlay120t_thorne01.tga</Texture>
        <Location>
            <X>-360</X>
            <Y>16</Y>
        </Location>
        <Size>
            <CX>480</CX>
            <CY>16</CY>
        </Size>
        <Hotspot><X>0</X><Y>0</Y></Hotspot>
        <Duration>1000</Duration>
    </Frames>
</Ui2DAnimation>
```

These are the only new animations needed — 4 definitions. The B gauges reuse the existing `A_GaugeFill_120t` at native resolution.

---

## Concrete Example: HP Gauge (120px, 4 Bands)

### Full XML

```xml
<!-- ====================================================================== -->
<!-- HP GAUGE — Hybrid Multi-Color (4x stretch, solid-color-that-changes) -->
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
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
    </GaugeDrawTemplate>
</Gauge>

<!-- Band 0: Base fill — Red (always active when any HP) -->
<Gauge item="PW_HP_Band0">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>0</GaugeOffsetX>
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

<!-- Band 1A: Orange threshold (activates >25% HP) -->
<Gauge item="PW_HP_Band1A">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-120</GaugeOffsetX>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>240</R>
        <G>120</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_HybridFill_120t_Band2</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band1A_Clip">
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
    <Pieces>PW_HP_Band1A</Pieces>
</Screen>
<!-- Band 1B: Orange continuation (native resolution) -->
<Gauge item="PW_HP_Band1B">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>32</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-30</GaugeOffsetX>
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

<!-- Band 2A: Yellow threshold (activates >50% HP) -->
<Gauge item="PW_HP_Band2A">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-240</GaugeOffsetX>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>240</R>
        <G>240</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_HybridFill_120t_Band3</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band2A_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band2A</Pieces>
</Screen>
<!-- Band 2B: Yellow continuation (native resolution) -->
<Gauge item="PW_HP_Band2B">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>62</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-60</GaugeOffsetX>
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

<!-- Band 3A: Green threshold (activates >75% HP) -->
<Gauge item="PW_HP_Band3A">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-360</GaugeOffsetX>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>0</R>
        <G>220</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_HybridFill_120t_Band4</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="PW_HP_Band3A_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>PW_HP_Band3A</Pieces>
</Screen>
<!-- Band 3B: Green continuation (native resolution) -->
<Gauge item="PW_HP_Band3B">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>92</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <EQType>1</EQType>
    <Text />
    <TextOffsetY>8000</TextOffsetY>
    <GaugeOffsetX>-90</GaugeOffsetX>
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

<!-- Layer Top: Overlay — Transparent for text/tooltip -->
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
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate />
</Gauge>
```

---

## Comparing All Three Approaches

| Aspect | Full Stretch | Clipping | Hybrid |
|--------|-------------|----------|--------|
| **Visual behavior** | Solid color changes | Rainbow always | Solid color changes |
| **Pattern fidelity (A gauges)** | Destroyed (83×) | Perfect (1×) | Softened (4×) |
| **Pattern fidelity (B gauges)** | Perfect (1×) | N/A (no B) | Perfect (1×) |
| **New animations needed** | 4 (CX=10000) | 0 | 4 (CX=480) |
| **Gauge elements per bar** | 9+ (BG + 4A + 4B) | 6 (BG + 4band + overlay) | 10+ (BG + 4A + 4B + overlay) |
| **Color palette changes** | FillTint only | FillTint only | FillTint only |
| **Key risk** | None (proven) | Negative Location | 4× stretch quality |
| **Player experience** | Intuitive (green=safe) | Decorative | Intuitive (green=safe) |

---

## When to Use Which Approach

- **Hybrid**: Best for HP, Mana, PetHP — gauges where "solid color that changes" communicates urgency and fill pattern detail matters for Thorne's visual identity.
- **Clipping**: Best if rainbow-always is a desired aesthetic, or for gauges where urgency isn't semantic (decorative bars).
- **Full Stretch**: Best if pattern fidelity isn't a concern (simple flat fills) and maximum compatibility is wanted.
- **Single Color**: Best for XP, AAXP, thin tick gauges, recast bars — where multi-color adds no value.

The experiment in the stats window will let you compare all three side-by-side to make the final call.
