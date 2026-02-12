# Player Window Analysis: Nillipuss vs. Thorne

## Summary
The `EQUI_PlayerWindow.xml` shows **major differences** between Nillipuss and thorne_drak. Nillipuss features a highly complex, multi-colored animated HP bar and defines a 6-segment timer system. Thorne_drak uses a more standard, simplified gauge system but includes Zeal tick display and expanded XP/AA rate labels. For the current authoritative analysis, see `PLAYERWINDOW-analysis.md`.

## Window Size & Layout
- **Nillipuss**: `288x107`
- **thorne_drak**: `226x118`

Thorne_drak's window is narrower and slightly taller, reflecting a more compact design.

## Element Inventory

### Gauges (EQType-validated)
**In Both:**
- **Mana Gauge**: `Player_Mana` (N) / `PW_Gauge_Mana` (T) - EQType **2**
- **Stamina/Fatigue Gauge**: `Player_Fatigue` (N) / `PW_Gauge_Stamina` (T) - EQType **3** (same stat, different naming)
- **XP Gauge**: `PW_ExpGauge` (N) / `PW_Gauge_XP` (T) - EQType **4**
- **AA XP Gauge**: `PW_AAExpGauge` (N) / `PW_Gauge_AAXP` (T) - EQType **5**
- **Mana Tick**: `Zeal_Tick` (N) / `PW_Mana_Tick` (T) - EQType **24** (same data source; different visuals)

**Nillipuss Only:**
- **Multi-Color HP Bar**: A system of layered gauges (`Player_HP_*`, EQType **1**) that change color with health.
- **Timer System**: Six gauges (`PW_Timer_1` to `PW_Timer_6`, EQType **2**), **not referenced by any Screen/Page pieces** (hidden/inactive by default).

**Thorne Only:**
- **HP Gauge**: `PW_Gauge_HP` (EQType **1**) - A single, simple red gauge replacing the Nillipuss multi-layer system.

### Labels
**In Both:**
- Player Name, Class, Level, Weight
- HP/Mana/Stamina Percentages
- Current/Max HP and Mana values
- XP and AA Percentage
- XP per Hour (`PW_ExpPerHour_Percentage` / `PW_XP_per_Hour`)
- AA per Hour (`PW_AAHR_Percentage` / `PW_AA_per_Hour`)

**Nillipuss Only:**
- Numerous redundant labels with `BG` suffixes for text shadow effects (e.g., `Player_NameTextBG`).

**Thorne Only:**
- XP/AA rate labels use EQType **81** (XP per hour) and related labels. Nillipuss has **AA per hour** via EQType **86**, which Thorne does not display in this layout.

### Buttons
**Nillipuss Only:**
- **Marker Buttons**: `PW_Marker1_Button` through `PW_Marker7_Button`. Used in conjunction with the timer system. - **MISSING from Thorne**

### Other Elements (Animations)
**Nillipuss Only:**
- `PW_GaugeFill1` to `PW_GaugeFill4`: Custom animations for the multi-color HP bar.
- `A_PlayerWindow_Timer_1` to `A_PlayerWindow_Timer_6`: Animations for the timer gauges.

## Functional Differences
- **HP Bar:** Nillipuss provides immediate visual feedback on health status through color changes, a significant functional advantage in combat. Thorne's is a basic bar.
- **Timers:** Nillipuss includes a fully functional, built-in timer system within the player window, allowing users to track multiple short-term events without a separate window. Thorne lacks this completely.

## What Thorne is Missing from Nillipuss
1. **Multi-Color HP Bar** - High Priority
   - **What it does:** Changes the HP bar color based on the player's health percentage (e.g., green > yellow > orange > red).
   - **Why it matters:** Provides at-a-glance assessment of health status, which is critical for survivability. It's a major quality-of-life feature.
   - **Complexity to add:** High. Requires re-implementing the multi-gauge and animation system from the Nillipuss file.

2. **Integrated Timer System** - Medium Priority
   - **What it does:** Provides six configurable timers with visual indicators directly in the player window.
   - **Why it matters:** Extremely useful for classes that need to track short-duration buffs, debuffs, or spell cycles.
   - **Complexity to add:** High. Requires adding multiple gauges, buttons, and animations.

## What Thorne Added Beyond Nillipuss
- **XP Rate Modifier (`PW_XP_Rate`)**: A small but useful label that shows if an experience bonus is active. This is a nice-to-have feature that provides clear feedback on XP gain.

## Recommendations
Thorne should strongly consider porting the **Multi-Color HP Bar** from Nillipuss. It is a significant functional and visual upgrade that directly impacts gameplay awareness. The complexity is high, but the value justifies the effort.

The **Integrated Timer System** is also a powerful feature, but its priority is lower as dedicated timer windows exist. It would be a valuable addition for players who prefer a minimalist UI setup, but it's not as critical as the HP bar.
