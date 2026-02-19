# Cast Spell Window Analysis: Nillipuss vs. Thorne

## High-Level Differences Summary

Both UIs provide a vertical spell casting window, but they differ significantly in visual presentation and included features.

*   **Nillipuss**: Features a compact, functional design that incorporates **spell recast timers**, a popular feature borrowed from the Zeal UI. It uses standard spell gem elements with custom backgrounds.
*   **Thorne UI**: Focuses on a major visual overhaul, replacing the traditional spell gems with larger, custom-textured **buttons**. This provides a unique aesthetic with better visual contrast but omits the recast timer functionality present in Nillipuss.

## Layout/Positioning Analysis

Both windows are vertical stacks of spell slots. The primary difference is the styling of the slots themselves.

### Nillipuss Layout

A vertical list of spell gems with integrated recast timers below each gem.

```
┌───────────────────┐
│ [Icon] Spell Name [1] │
│  embaixo-recast-bar │
├───────────────────┤
│ [Icon] Spell Name [2] │
│  embaixo-recast-bar │
├───────────────────┤
│ ... (8 slots total) ... │
├───────────────────┤
│   [ Spells Button ]   │
└───────────────────┘
```

### Thorne UI Layout

A vertical list of custom-designed buttons that act as spell gems.

```
┌─────────────────────┐
│ ┌─────────────────┐ │
│ │[Icon][2] Spell Name │ │
│ └─────────────────┘ │
├─────────────────────┤
│ ┌─────────────────┐ │
│ │[Icon][3] Spell Name │ │
│ └─────────────────┘ │
├─────────────────────┤
│ ... (8 slots total) ... │
├─────────────────────┤
│  [ Spellbook Button ] │
└─────────────────────┘
```

## Element-by-Element Comparison

| Feature | Nillipuss | Thorne UI | Analysis |
| :--- | :--- | :--- | :--- |
| **Window Size** | `130x215` | `160x238` | Thorne is wider and taller to fit the custom button style. |
| **Spell Gem Style** | Standard `SpellGem` with custom holder | Custom `Button` with `Ui2DAnimation` | Major visual difference. Thorne's looks like a list of buttons. |
| **Recast Timers** | **Yes** (per-spell and global) | **No** | Major functional difference. Nillipuss provides more casting information. |
| **Spell Numbers** | On the right side | On the left, next to the icon | Different placement to suit the layout. |
| **Custom Textures** | Uses `A_dzSpellBG` | Uses `button-dark-opaque01.tga` and `button_light-opaque01.tga` | Thorne has a completely unique asset for its spell bar. |
| **Spellbook Button**| `120x14` | `144x20` | Thorne's is larger and more prominent. |

---

## EQType Validation (Recast Timers)

**Nillipuss EQType bindings (recast gauges):**
- `CSPW_Global_Recast` (Gauge, **25**)
- `CSPW_Spell0_Recast`–`CSPW_Spell7_Recast` (Gauge, **26–33**)

**Spell name labels (both):**
- `CSPW_Spell0_Name`–`CSPW_Spell7_Name` (Label, **60–67**)
- Thorne also defines `CSPW_Spell8_Name` (Label, **133**) for extended data display

**Thorne missing:** All recast gauges listed above.

## Feature Additions/Removals

*   **Nillipuss Additions**:
    *   **Spell Recast Timers**: Adds `Gauge` elements (`CSPW_Spell0_Recast`, etc.) for each spell slot to show cooldown progress.
    *   **Global Recast Timer**: Includes a `Gauge` (`CSPW_Global_Recast`) to show the global spell cooldown. This is a significant feature for casters.

*   **Thorne UI Additions**:
    *   **Custom Button Gems**: Replaces the entire `SpellGem` presentation with custom-animated buttons (`A_CastBtnNormal`, `A_CastBtnReady`). This is a purely cosmetic but very impactful change.
    *   **Custom Textures**: Introduces new texture files specifically for this window.
    *   The file contains extensive comments detailing the design philosophy and changes, which is a good documentation practice.

## Stat-Icons Relevance

The `EQUI_CastSpellWnd.xml` has minimal relevance to the stat-icons project, as it deals with actions (casting spells) rather than displaying character statistics. The design choices here are focused on usability for casting, not on displaying passive character data.
