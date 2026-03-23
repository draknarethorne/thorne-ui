# Multi-Color Gauge System

**Author**: Draknare Thorne
**Status**: Shipped (v0.8.0)
**Branch**: `feature/gauges-v0.8.0` (PR #68, merged)

---

## How It Works

EverQuest gauges have no built-in multi-color support. We achieve color-band
transitions by **stacking multiple transparent gauge elements on the same
EQType** (e.g., HP%), each with a different `FillTint` color, and using
oversized animations + viewport clipping so each color occupies a specific
fill-percentage range.

When HP drops, higher bands lose their fill first, revealing lower-band colors
underneath. This is **opaque layer occlusion**, not transparency blending.

### The Two-Part (A/B) Architecture

Each color band (except Band 0) is split into two gauge elements:

```
 ┌─── A-part (oversized, Screen-clipped) ───┬─── B-part (native, offset) ──┐
 │  Cols 0..clip-1  (left side of gauge)     │  Cols clip..width-1  (right) │
 │  Uses oversized animation (CX=W×100)      │  Uses normal animation (CX=W)│
 │  GaugeOffsetX = -(clip × 100)             │  GaugeOffsetX = -clip        │
 │  Element CX = (W - clip) × 100            │  Element CX = W - clip       │
 │  Wrapped in <Screen> with CX = clip       │  Location X = base + clip    │
 └───────────────────────────────────────────┴──────────────────────────────┘
```

**Why two parts?** The A-part uses a 100× oversized animation to create a
**threshold effect**: the fill only becomes visible when the gauge value exceeds
the band's percentage threshold. The B-part uses a native-resolution animation
for the continuation — it displays the right side of the texture at 1:1 with no
stretching, preserving texture detail.

### The Nillipuss Invariant

For every band: `Element_CX + |GaugeOffsetX| = Animation_CX`

This must hold for both A-parts (at ×100 scale) and B-parts (at pixel scale).

---

## Layer 1: Animations (EQUI_Animations.xml)

44 oversized animations across 3 gauge sizes and 4 fill styles:

### Animation Name Pattern

```
A_Oversized{FillStyle}_{Size}_Band{N}
```

Fill styles: `Fill`, `SolidFill`, `GridFill`, `LightGridFill`
Sizes: `105t`, `120t`, `250t`
Bands: 1–4

### Animation Parameters

All animations share `CX = width × 100` and `X = -(marker × 100)`:

| Size | CX | Band 1 X | Band 2 X | Band 3 X | Band 4 X |
|------|----|----------|----------|----------|----------|
| 105t | 10500 | -2100 | -4200 | -6300 | -8400 |
| 120t | 12000 | -2400 | -4800 | -7200 | -9600 |
| 250t | 25000 | -5000 | -10000 | -15000 | -20000 |

### Texture References

| Size | Texture File | Row (Y) |
|------|-------------|---------|
| 105t | `gauge_inlay105t_thorne01.tga` (Fill) / `thorne02.tga` (Grid/Solid/LightGrid) | Varies by style |
| 120t | `gauge_inlay120t_thorne01.tga` / `thorne02.tga` | Varies by style |
| 250t | `gauge_inlay250t_thorne01.tga` / `thorne02.tga` | Varies by style |

---

## Layer 2: Gauge Elements (23 Window XMLs)

Each composite gauge has 5 bands (0–4) with the following structure:

- **Band 0**: Full-width gauge, no clip — base color (brightest)
- **Bands 1–4**: A-part + B-part pair split at the clip position

### Marker Positions (Snapped to Exact Fifths)

Grid markers in the thorne02 textures are placed at exact 20% intervals via
the `snap_columns` feature in `regen_gauges.py`. This eliminates BILINEAR
interpolation artifacts that previously spread dark pixels during width-scaling.

| Size | Band 1 | Band 2 | Band 3 | Band 4 |
|------|--------|--------|--------|--------|
| 105t | 21 | 42 | 63 | 84 |
| 120t | 24 | 48 | 72 | 96 |
| 250t | 50 | 100 | 150 | 200 |

### Clip Positions (Marker - 1 for OBY1)

The EQ engine has an **off-by-one** in gauge offset rendering:
`GaugeOffsetX = -N` renders the fill starting at texture column **N+1**, not N.
To align the B-part fill edge with the grid marker, clips use `marker - 1`.

These are the **deployed production values** (verified by `audit_gauges.py`):

| Size | Band 1 | Band 2 | Band 3 | Band 4 |
|------|--------|--------|--------|--------|
| 105t | 20 | 41 | 62 | 83 |
| 120t | 23 | 47 | 71 | 95 |
| 250t | 49 | 99 | 149 | 199 |

### How Values Flow (Cheat Sheet)

Given `marker` (snapped pixel column), `clip = marker - 1`, and `W` (gauge width):

| XML Field | A-part Value | B-part Value |
|-----------|-------------|-------------|
| GaugeOffsetX | `-(marker × 100)` | `-clip` |
| Size CX | `(W - marker) × 100` | `W - clip` |
| Screen CX | `clip` | — |
| Location X | (from Screen) | `base_x + clip` |

The **Animation** X must match the A-part GaugeOffsetX: `-(clip × 100)`.
The Animation CX is always `W × 100`.

---

## Texture Grid Markers

The thorne02 textures embed single-pixel grid marker lines at the band
transition points. These markers appear in two rows:

- **GridFill (Y=32–47)**: Full black lines (brightness 0)
- **LightGridFill (Y=48–63)**: Subtle gray markers (brightness 140 vs 245)

### Marker Positions (from snap_columns pipeline)

| Size | Total Width | Marker Columns | Spacing Pattern |
|------|------------|----------------|-----------------|
| 105t | 105px | 21, 42, 63, 84 | Exact 20% intervals (snap_columns) |
| 120t | 120px | 24, 48, 72, 96 | Exact 20% intervals (snap_columns) |
| 250t | 250px | 50, 100, 150, 200 | Exact 20% intervals (snap_columns) |

Each marker is a **single pixel** surrounded by fill pixels (brightness 245).
Texture col 0 and col (width-1) are transparent/black (padding).
Fill spans cols 1 through width-2.

### The "Last Light Pixel" Rule

The clip boundary should land so that:
- The **A-part's last visible pixel** is the last light pixel before the marker
- The **B-part's first visible pixel** is the dark marker pixel itself

Due to the EQ engine off-by-one, this means `clip = marker_column - 1`.

---

## Color Palettes ("Veils")

All palettes follow a 5-band gradient from light/desaturated (Band 0, critical)
to fully saturated (Band 4, healthy/full). Band 0 is always the "alarm" color
that shows when the gauge is nearly empty.

### Red Veil (HP Gauges)

| Band | Name | RGB | Used In |
|------|------|-----|---------|
| 0 | White-hot Ember | 255,210,210 | Player, Target, Group, Pet |
| 1 | Fading Wound | 255,160,160 | |
| 2 | Heated Blush | 255,100,100 | |
| 3 | Scorched Rose | 255,50,50 | |
| 4 | Crimson | 255,0,0 | |

Group variant uses R=220 base instead of 255 for subtler contrast.

### Ocean Veil (Mana)

| Band | Name | RGB |
|------|------|-----|
| 0 | Icebloom | 210,210,255 |
| 1 | Pale Ether | 160,160,255 |
| 2 | Starlit Pool | 100,100,255 |
| 3 | Frozen Azure | 50,50,255 |
| 4 | Sapphire | 0,0,255 |

### Purple Veil (Pet HP)

| Band | Name | RGB |
|------|------|-----|
| 0 | Spectral Wisp | 240,210,240 |
| 1 | Faded Familiar | 230,160,230 |
| 2 | Mystic Haze | 220,100,220 |
| 3 | Enchanted Orchid | 210,50,210 |
| 4 | Conjured Violet | 200,0,200 |

### Cyan Veil (Breath)

| Band | Name | RGB |
|------|------|-----|
| 0 | Frost Spray | 210,240,240 |
| 1 | Sea Mist | 160,240,240 |
| 2 | Tidal Aqua | 100,240,240 |
| 3 | Shallow Aqua | 50,240,240 |
| 4 | Deep Aqua | 0,240,240 |

### Cyan Veil v2 (Memorize — SpellBook)

| Band | Name | RGB |
|------|------|-----|
| 0 | Frostlight | 170,235,255 |
| 1 | Arctic Glow | 100,210,255 |
| 2 | Crystal Current | 40,180,255 |
| 3 | Deep Tide | 0,150,240 |
| 4 | Abyssal Cyan | 0,120,210 |

### Gold Veil (Scribe — SpellBook)

| Band | Name | RGB |
|------|------|-----|
| 0 | Aureate Glow | 255,230,160 |
| 1 | Sunlit Parchment | 255,200,100 |
| 2 | Molten Script | 255,170,40 |
| 3 | Gilded Quill | 240,140,0 |
| 4 | Ancient Gold | 210,110,0 |

---

## Files Affected

### 23 Window XMLs with Composite Gauges

Grouped by gauge size:

**105t** (SpellBook): `EQUI_SpellBookWnd.xml` + Options variants

**120t** (Player, Group, Breath, Pet, MusicPlayer):
- `EQUI_PlayerWindow.xml` + Options variants
- `EQUI_GroupWindow.xml` + Options variants
- `EQUI_BreathWindow.xml` + Options variants
- `EQUI_PetInfoWindow.xml` + Options variants
- `EQUI_MusicPlayerWnd.xml` (test window)

**250t** (Target): `EQUI_TargetWindow.xml` + Options variants

### Animation File

`EQUI_Animations.xml` — 44 oversized `A_Oversized*` animations

---

## Tooling (`.tmp/` scripts)

### Reusable Tools

| Script | Purpose |
|--------|---------|
| `analyze_tga.py` | Read TGA textures, find grid marker positions by brightness transitions |
| `build_mpw_test2.py` | Generate MusicPlayer test window with composite + A\|B piece layout |
| `build_playerwindow_composites.py` | Generate PlayerWindow composite gauge XML |
| `gen_fire_ocean.py` | Generate Fire HP + Ocean Mana experiment blocks |
| `gen_group.py` | Generate GroupWindow composite gauge XML |
| `gen_target.py` | Generate TargetWindow composite gauge XML |
| `validate_target.py` | Validate Target window XML element counts |

### Archived (one-shot fix scripts, historical reference)

| Script | What it did |
|--------|-------------|
| `fix_oversized_anims.py` | Fixed 44 animation X and CX values in EQUI_Animations.xml |
| `fix_gauge_elements.py` | Fixed A-part GaugeOffsetX and CX across 23 files (424 replacements) |
| `fix_b_parts.py` | Fixed B-part offsets across 20 files (784 replacements) |
| `shift_clips.py` / `shift_clips_utf8.py` / `single_pass_shift.py` | Historical clip shift iterations |
| `insert_anims.py` | Inserted 250t animations into EQUI_Animations.xml |
| `apply_group_composite.py` | Applied composite gauges to GroupWindow |
| `apply_target.py` | Applied composite gauges to TargetWindow |

---

## Related Documents

| File | Contents |
|------|----------|
| [gauges-analysis.md](gauges-analysis.md) | Original research: full gauge inventory, Nillipuss/DuxaUI analysis, A/B split math |
| [gauges-clipping-design.md](gauges-clipping-design.md) | Clipping approach design (rainbow bar, rejected for Thorne) |
| [gauges-hybrid-design.md](gauges-hybrid-design.md) | Hybrid stretch approach design (moderate stretch, evolved into current) |
| [gauges-experiment-plan.md](gauges-experiment-plan.md) | MusicPlayer test layout plan and XML |

---

## Key Lessons Learned

1. **EQ engine off-by-one**: `GaugeOffsetX=-N` renders starting at texture
   column N+1. Set clips to `grid_marker - 1` for correct alignment.

2. **Both layers must agree**: Animation X must equal A-part GaugeOffsetX.
   Animation CX must equal `width × 100`. Element CX + |offset| = Animation CX.

3. **B-parts use pixel scale, A-parts use ×100 scale**: A-part values are
   multiplied by 100 to work with the oversized animation. B-parts are native.

4. **Texture grid markers are truth**: The thorne02 TGA files contain the
   canonical band boundary positions. Use `analyze_tga.py` to verify.

5. **Band 0 has no clip**: It's a simple full-width gauge with the lightest
   color. All clip-based logic starts at Band 1.

6. **Z-order matters**: Band 4 (darkest, full health) is defined LAST so it
   renders on TOP. As the gauge drains, Band 4's fill recedes first, revealing
   Band 3, then 2, then 1, then 0.
