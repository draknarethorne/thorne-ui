# Multi-Color Gauge Experiment — HP Side-by-Side Test

> **ARCHIVED**: This was the original 4-row experiment plan. Current testing
> uses `build_mpw_test2.py` with a composite + A|B piece layout. See
> [README.md](README.md) for current approach and tooling.

**Date**: March 4, 2026  
**Author**: Draknare Thorne  
**Status**: Archived — superseded by build_mpw_test2.py approach  
**Purpose**: Compare all three multi-color gauge approaches side-by-side using HP (EQType=1)

---

## Table of Contents

- [Multi-Color Gauge Experiment — HP Side-by-Side Test](#multi-color-gauge-experiment--hp-side-by-side-test)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Test Setup: Expanded Stats Window](#test-setup-expanded-stats-window)
  - [The Four Test Rows](#the-four-test-rows)
  - [Color Palettes](#color-palettes)
  - [Required Animation Definitions](#required-animation-definitions)
  - [Complete Test XML](#complete-test-xml)
    - [How to Apply](#how-to-apply)
    - [What to Look For](#what-to-look-for)
  - [Testing Procedure](#testing-procedure)
  - [Expected Results at Different HP Levels](#expected-results-at-different-hp-levels)
  - [Decision Criteria](#decision-criteria)

---

## Overview

This experiment places 4 HP gauge variants on the expanded MusicPlayerWnd (stats window) so they can be compared in real-time as HP changes. All gauges track EQType=1 (player HP), so they move together.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [AC][ATK][STR][STA][AGI][DEX][WIS][INT][CHA][MR][FR][CR][DR][PR]          │
│ (existing stats row — unchanged)                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ROW A: Current Single-Color (Red)                                           │
│  [████████████████████████████████████████]  Label: "Current (Single Red)"   │
│                                                                              │
│  ROW B: Rainbow Clipping — Classic GYOR                                      │
│  [████████████████████████████████████████]  Label: "Rainbow (GYOR Clip)"    │
│                                                                              │
│  ROW C: Rainbow Clipping — Red Tones                                         │
│  [████████████████████████████████████████]  Label: "Rainbow (Red Tones)"    │
│                                                                              │
│  ROW D: Hybrid Stretch — Classic GYOR                                        │
│  [████████████████████████████████████████]  Label: "Hybrid 4× (GYOR)"      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Test Setup: Expanded Stats Window

**Changes to MusicPlayerWnd Screen definition:**

- CY expanded from `42` to `168` (adds 126px for 4 gauge rows)
- New Pieces added for all test gauge elements
- Stats row unchanged at top
- All hidden client-required pieces preserved

**Layout math:**

| Element | Y position | Height | Notes |
|---------|-----------|--------|-------|
| Stats row | Y=2 | 36px | Existing (icon + label) |
| Separator | Y=42 | 4px | Visual spacer |
| Row A label | Y=48 | 12px | "Current (Single Red)" |
| Row A gauge | Y=60 | 16px | Single-color HP |
| Row B label | Y=80 | 12px | "Rainbow (GYOR Clip)" |
| Row B gauge | Y=92 | 16px | Clipping rainbow |
| Row C label | Y=112 | 12px | "Rainbow (Red Tones)" |
| Row C gauge | Y=124 | 16px | Clipping red palette |
| Row D label | Y=144 | 12px | "Hybrid 4× (GYOR)" |
| Row D gauge | Y=156 | 16px | Hybrid stretch |

Total height needed: ~176px. Using CY=180 with 4px bottom padding.

---

## The Four Test Rows

### Row A: Current Single-Color (Baseline)

Exact reproduction of the current PlayerWindow HP gauge. One gauge, red fill, native 120px width. This is the control.

### Row B: Rainbow Clipping — Classic GYOR

Uses the clipping approach from [gauges-clipping-design.md](gauges-clipping-design.md). Four adjacent Screen containers, each clipping a native-resolution gauge to show only its band segment. Colors: Green → Yellow → Orange → Red (left-to-right, high→low HP).

**Behavior**: Always shows all 4 color bands proportional to fill level. "Rainbow bar."

### Row C: Rainbow Clipping — Red Tones

Same clipping technique as Row B, but using a red-themed palette instead of GYOR. This tests whether a monochromatic palette works for multi-band gauges.

### Row D: Hybrid Stretch — Classic GYOR

Uses the hybrid approach from [gauges-hybrid-design.md](gauges-hybrid-design.md). A/B gauge pairs with CX=480 (4× stretch). Colors: GYOR with solid-color-that-changes behavior.

**Behavior**: Shows one dominant color based on HP level. Color changes as HP drops.

---

## Color Palettes

### Classic GYOR (Rows B and D)

| Band | HP Range | Color Name | RGB |
|------|----------|-----------|-----|
| 4 (leftmost) | 75-100% | Green | (0, 220, 0) |
| 3 | 50-75% | Yellow | (240, 240, 0) |
| 2 | 25-50% | Orange | (240, 120, 0) |
| 1 (rightmost) | 0-25% | Red | (255, 0, 0) |

### Red Tones (Row C)

| Band | HP Range | Color Name | RGB |
|------|----------|-----------|-----|
| 4 (leftmost) | 75-100% | Amber Gold | (220, 160, 30) |
| 3 | 50-75% | Flame Orange | (220, 80, 10) |
| 2 | 25-50% | Crimson | (180, 20, 20) |
| 1 (rightmost) | 0-25% | Blood Red | (120, 0, 0) |

---

## Required Animation Definitions

Add these to `EQUI_Animations.xml` for the hybrid test (Row D only). Rows A-C use existing `A_GaugeFill_120t` at native resolution.

```xml
<!-- ========================================================== -->
<!-- EXPERIMENT: Hybrid 4x stretch fills for gauge comparison    -->
<!-- ========================================================== -->
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

---

## Complete Test XML

The sections below contain the complete XML elements needed for the experiment. These go into the MusicPlayerWnd XML file and Animations XML file.

### New Elements for EQUI_MusicPlayerWnd.xml

Insert these elements **before** the Screen definition (between the last hidden client piece and the Screen). Then add the new Pieces references to the Screen.

```xml
<!-- ============================================================== -->
<!-- GAUGE EXPERIMENT: Side-by-side multi-color HP gauge comparison  -->
<!-- ============================================================== -->

<!-- ======================== ROW A: Current Single-Color ======================== -->

<Label item="EXP_LabelA">
    <ScreenID>EXP_LabelA</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>48</Y>
    </Location>
    <Size>
        <CX>140</CX>
        <CY>12</CY>
    </Size>
    <Text>Current (Single Red)</Text>
    <Font>3</Font>
    <TextColor>
        <R>200</R>
        <G>200</G>
        <B>200</B>
    </TextColor>
    <NoWrap>true</NoWrap>
</Label>

<Gauge item="EXP_A_HP">
    <ScreenID>EXP_A_HP</ScreenID>
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>60</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetY>-250</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>255</R>
        <G>0</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground_120t</Background>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>

<Label item="EXP_A_HPText">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>136</X>
        <Y>62</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>12</CY>
    </Size>
    <EQType>1</EQType>
    <Font>3</Font>
    <TextColor>
        <R>180</R>
        <G>180</G>
        <B>180</B>
    </TextColor>
    <NoWrap>true</NoWrap>
</Label>

<!-- ======================== ROW B: Rainbow Clipping (GYOR) ======================== -->

<Label item="EXP_LabelB">
    <ScreenID>EXP_LabelB</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>80</Y>
    </Location>
    <Size>
        <CX>140</CX>
        <CY>12</CY>
    </Size>
    <Text>Rainbow (GYOR Clip)</Text>
    <Font>3</Font>
    <TextColor>
        <R>200</R>
        <G>200</G>
        <B>200</B>
    </TextColor>
    <NoWrap>true</NoWrap>
</Label>

<!-- Row B Background (full width) -->
<Gauge item="EXP_B_BG">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>92</Y>
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

<!-- Row B Band 1: Green (leftmost, 75-100%) -->
<Gauge item="EXP_B_Band1_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_B_Band1_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>92</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_B_Band1_Fill</Pieces>
</Screen>

<!-- Row B Band 2: Yellow (50-75%) -->
<Gauge item="EXP_B_Band2_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-30</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_B_Band2_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>38</X>
        <Y>92</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_B_Band2_Fill</Pieces>
</Screen>

<!-- Row B Band 3: Orange (25-50%) -->
<Gauge item="EXP_B_Band3_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-60</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_B_Band3_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>68</X>
        <Y>92</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_B_Band3_Fill</Pieces>
</Screen>

<!-- Row B Band 4: Red (0-25%) -->
<Gauge item="EXP_B_Band4_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-90</X>
        <Y>0</Y>
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
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="EXP_B_Band4_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>98</X>
        <Y>92</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_B_Band4_Fill</Pieces>
</Screen>

<!-- Row B overlay (text/tooltip) -->
<Gauge item="EXP_B_Overlay">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>92</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetY>-250</TextOffsetY>
    <Style_Transparent>true</Style_Transparent>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate/>
</Gauge>

<!-- ======================== ROW C: Rainbow Clipping (Red Tones) ======================== -->

<Label item="EXP_LabelC">
    <ScreenID>EXP_LabelC</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>112</Y>
    </Location>
    <Size>
        <CX>160</CX>
        <CY>12</CY>
    </Size>
    <Text>Rainbow (Red Tones Clip)</Text>
    <Font>3</Font>
    <TextColor>
        <R>200</R>
        <G>200</G>
        <B>200</B>
    </TextColor>
    <NoWrap>true</NoWrap>
</Label>

<!-- Row C Background -->
<Gauge item="EXP_C_BG">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>124</Y>
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

<!-- Row C Band 1: Amber Gold (leftmost, 75-100%) -->
<Gauge item="EXP_C_Band1_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>220</R>
        <G>160</G>
        <B>30</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="EXP_C_Band1_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>124</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_C_Band1_Fill</Pieces>
</Screen>

<!-- Row C Band 2: Flame Orange (50-75%) -->
<Gauge item="EXP_C_Band2_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-30</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>220</R>
        <G>80</G>
        <B>10</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="EXP_C_Band2_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>38</X>
        <Y>124</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_C_Band2_Fill</Pieces>
</Screen>

<!-- Row C Band 3: Crimson (25-50%) -->
<Gauge item="EXP_C_Band3_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-60</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>180</R>
        <G>20</G>
        <B>20</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="EXP_C_Band3_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>68</X>
        <Y>124</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_C_Band3_Fill</Pieces>
</Screen>

<!-- Row C Band 4: Blood Red (0-25%) -->
<Gauge item="EXP_C_Band4_Fill">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>-90</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
    <TextOffsetY>8000</TextOffsetY>
    <Style_Transparent>false</Style_Transparent>
    <FillTint>
        <R>120</R>
        <G>0</G>
        <B>0</B>
    </FillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate>
        <Fill>A_GaugeFill_120t</Fill>
    </GaugeDrawTemplate>
</Gauge>
<Screen item="EXP_C_Band4_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>98</X>
        <Y>124</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_C_Band4_Fill</Pieces>
</Screen>

<!-- Row C overlay -->
<Gauge item="EXP_C_Overlay">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>124</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetY>-250</TextOffsetY>
    <Style_Transparent>true</Style_Transparent>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate/>
</Gauge>

<!-- ======================== ROW D: Hybrid Stretch (GYOR, 4×) ======================== -->

<Label item="EXP_LabelD">
    <ScreenID>EXP_LabelD</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>144</Y>
    </Location>
    <Size>
        <CX>160</CX>
        <CY>12</CY>
    </Size>
    <Text>Hybrid 4x (GYOR Stretch)</Text>
    <Font>3</Font>
    <TextColor>
        <R>200</R>
        <G>200</G>
        <B>200</B>
    </TextColor>
    <NoWrap>true</NoWrap>
</Label>

<!-- Row D Background -->
<Gauge item="EXP_D_BG">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
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

<!-- Row D Band 0: Base Red (always active) -->
<Gauge item="EXP_D_Band0">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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

<!-- Row D Band 1A: Orange threshold (activates >25% HP) -->
<Gauge item="EXP_D_Band1A">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_D_Band1A_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_D_Band1A</Pieces>
</Screen>
<!-- Row D Band 1B: Orange continuation -->
<Gauge item="EXP_D_Band1B">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>38</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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

<!-- Row D Band 2A: Yellow threshold (activates >50% HP) -->
<Gauge item="EXP_D_Band2A">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_D_Band2A_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_D_Band2A</Pieces>
</Screen>
<!-- Row D Band 2B: Yellow continuation -->
<Gauge item="EXP_D_Band2B">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>68</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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

<!-- Row D Band 3A: Green threshold (activates >75% HP) -->
<Gauge item="EXP_D_Band3A">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>0</X>
        <Y>0</Y>
    </Location>
    <Size>
        <CX>480</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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
<Screen item="EXP_D_Band3A_Clip">
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>16</CY>
    </Size>
    <Style_Transparent>true</Style_Transparent>
    <Pieces>EXP_D_Band3A</Pieces>
</Screen>
<!-- Row D Band 3B: Green continuation -->
<Gauge item="EXP_D_Band3B">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>98</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetX>8000</TextOffsetX>
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

<!-- Row D overlay (text/tooltip) -->
<Gauge item="EXP_D_Overlay">
    <EQType>1</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>8</X>
        <Y>156</Y>
    </Location>
    <Size>
        <CX>120</CX>
        <CY>16</CY>
    </Size>
    <TextOffsetY>-250</TextOffsetY>
    <Style_Transparent>true</Style_Transparent>
    <DrawLinesFill>false</DrawLinesFill>
    <GaugeDrawTemplate/>
</Gauge>
```

### Pieces to Add to MusicPlayerWnd Screen

Add these Pieces lines **before** the client-required hidden children comment:

```xml
<!-- Gauge experiment elements -->
<Pieces>EXP_LabelA</Pieces>
<Pieces>EXP_A_HP</Pieces>
<Pieces>EXP_A_HPText</Pieces>
<Pieces>EXP_LabelB</Pieces>
<Pieces>EXP_B_BG</Pieces>
<Pieces>EXP_B_Band1_Clip</Pieces>
<Pieces>EXP_B_Band2_Clip</Pieces>
<Pieces>EXP_B_Band3_Clip</Pieces>
<Pieces>EXP_B_Band4_Clip</Pieces>
<Pieces>EXP_B_Overlay</Pieces>
<Pieces>EXP_LabelC</Pieces>
<Pieces>EXP_C_BG</Pieces>
<Pieces>EXP_C_Band1_Clip</Pieces>
<Pieces>EXP_C_Band2_Clip</Pieces>
<Pieces>EXP_C_Band3_Clip</Pieces>
<Pieces>EXP_C_Band4_Clip</Pieces>
<Pieces>EXP_C_Overlay</Pieces>
<Pieces>EXP_LabelD</Pieces>
<Pieces>EXP_D_BG</Pieces>
<Pieces>EXP_D_Band0</Pieces>
<Pieces>EXP_D_Band1A_Clip</Pieces>
<Pieces>EXP_D_Band1B</Pieces>
<Pieces>EXP_D_Band2A_Clip</Pieces>
<Pieces>EXP_D_Band2B</Pieces>
<Pieces>EXP_D_Band3A_Clip</Pieces>
<Pieces>EXP_D_Band3B</Pieces>
<Pieces>EXP_D_Overlay</Pieces>
```

### Screen Definition Change

```xml
<!-- Before: -->
<Size>
    <CX>426</CX>
    <CY>42</CY>
</Size>

<!-- After: -->
<Size>
    <CX>426</CX>
    <CY>180</CY>
</Size>
```

---

### How to Apply

1. **Add hybrid animations** to `EQUI_Animations.xml` (the 4 `A_HybridFill_120t_Band*` definitions above)
2. **Add experiment elements** to `EQUI_MusicPlayerWnd.xml` (before the Screen definition)
3. **Add Pieces references** to the MusicPlayerWnd Screen (before the hidden client pieces)
4. **Change CY** from 42 to 180 in the MusicPlayerWnd Screen Size
5. **Sync**: `.bin\sync-thorne-ui.bat`
6. **Test**: `/loadskin thorne_dev` in-game

### What to Look For

| Check | What to Observe |
|-------|----------------|
| **Row A** | Should look identical to current PlayerWindow HP gauge |
| **Row B** | Should show 4 colored segments (GYOR) — all filling proportionally |
| **Row C** | Same as Row B but in graduated red tones (amber → blood) |
| **Row D** | Should show single dominant color that changes with HP level |
| **Fill pattern** | Compare Row A (native) vs Row D (4× stretch) — is pattern visible? |
| **Clipping** | Do Rows B/C show seams between band segments? |
| **Negative X** | Do the clip containers work with negative child Location X? |
| **Band transitions** | At 75%, 50%, 25% — do colors transition cleanly in Row D? |

---

## Testing Procedure

### Step 1: Full HP (100%)

- Row A: Full red fill
- Row B: All 4 bands fully filled (rainbow GYOR)
- Row C: All 4 bands fully filled (rainbow reds)
- Row D: Full green fill (band 4 covers everything)

### Step 2: Take Damage to ~60% HP

- Row A: 60% red fill
- Row B: Green full, Yellow partial, Orange unfilled, Red unfilled
- Row C: Amber full, Flame partial, Crimson unfilled, Blood unfilled
- Row D: Yellow fill (bands 1-3 active, yellow on top) — ~60% filled

### Step 3: Continue to ~35% HP

- Row A: 35% red fill
- Row B: Green full, Yellow full, Orange partial, Red unfilled
- Row C: Amber full, Flame full, Crimson partial, Blood unfilled
- Row D: Orange fill (bands 1-2 active) — ~35% filled

### Step 4: Critical HP (~10%)

- Row A: 10% red fill
- Row B: Only red band partially filled (other bands have trailing fill)
- Row C: Only blood band partially filled
- Row D: Red fill (only band 0 active) — ~10% filled

### Step 5: Full Heal

- All rows return to Step 1 appearance

---

## Expected Results at Different HP Levels

```
100% HP:
  A: [████████████████████████████████████████]  solid red
  B: [▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓]  G-Y-O-R all full
  C: [▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓]  amber-flame-crim-blood
  D: [████████████████████████████████████████]  solid green

 50% HP:
  A: [████████████████████░░░░░░░░░░░░░░░░░░░░]  half red
  B: [▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|░░░░░░░░░░|░░░░░░░░░░]  G full, Y full, O+R empty
  C: [▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓▓|░░░░░░░░░░|░░░░░░░░░░]  amber+flame full, rest empty
  D: [████████████████████░░░░░░░░░░░░░░░░░░░░]  half yellow

 15% HP:
  A: [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  sliver red
  B: [▓▓░░░░░░░░|░░░░░░░░░░|░░░░░░░░░░|░░░░░░░░░░]  G partial, rest empty
  C: [▓▓░░░░░░░░|░░░░░░░░░░|░░░░░░░░░░|░░░░░░░░░░]  amber partial, rest empty
  D: [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  sliver red
```

---

## Decision Criteria

After testing, evaluate based on:

1. **Readability**: Which variant communicates HP level fastest at a glance?
2. **Aesthetic**: Which looks best with Thorne's fill pattern and overall UI style?
3. **Pattern impact**: Is the 4× stretch pattern degradation noticeable or acceptable?
4. **Clipping quality**: Do the rainbow variants render cleanly without seams?
5. **Red tones**: Does the monochromatic palette work, or does it need more contrast?
6. **Technical viability**: Does negative Location X work in Screen containers?

Based on findings, the winning approach will be documented in the main [gauges-analysis.md](gauges-analysis.md) and scheduled for implementation across all gauge windows.
