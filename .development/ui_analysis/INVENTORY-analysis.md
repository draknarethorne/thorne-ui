# Inventory Window Analysis: Nillipuss vs. Thorne

## Status: ✅ THORNE IS SUPERIOR
- **Lines**: Nillipuss: 2164 | Thorne: 2546 (**Thorne 15% LARGER - 382 more lines**)
- **Verdict**: NO features to port - Thorne's implementation is better!

## High-Level Differences Summary

The most significant difference is the fundamental purpose of the `EQUI_Inventory.xml` file in each UI.

*   **Nillipuss**: Implements a comprehensive, all-in-one "character sheet" window. It combines equipment, detailed character statistics (base stats and resists), progression gauges, and inventory bag slots into a large, tabbed window.
*   **Thorne UI**: Uses a modular layout with multiple internal screens, but still includes **stats, progression gauges, and weight** in the inventory window. Thorne also adds AA current/total tracking in this window.

**Key Point**: Despite Nillipuss's all-in-one approach, **Thorne's modular 382-line larger implementation is SUPERIOR**. This validates Thorne's Phase 3.9 Inventory Redesign work and the multi-zone screen organization.

This represents a major philosophical divergence in UI design - **Thorne won this one**.

## Layout/Positioning Analysis

### Nillipuss Layout

The Nillipuss inventory is a large, multi-purpose window.

```
┌──────────────────────────────────────────────────────────────┐
│ ┌───────────────┐ ┌──────────────────┐ ┌───────────────────┐ │
│ │               │ │   CHARACTER INFO   │ │    STATS TABS     │ │
│ │  EQUIPMENT    │ │   (Name, Level,    │ │ (Stats, Resists,  │ │
│ │    SLOTS      │ │    HP/Mana/AC)     │ │      Skills)      │ │
│ │ (Anatomical)  │ │                  │ │                   │ │
│ │               │ ├──────────────────┤ ├───────────────────┤ │
│ │               │ │      GAUGES      │ │   INVENTORY BAGS  │ │
│ │               │ │   (XP / AA)      │ │     (8 slots)     │ │
│ └───────────────┘ └──────────────────┘ └───────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│ [ DONE ] [ FACE ] [ BANK ]                                   │
└──────────────────────────────────────────────────────────────┘
```

### Thorne UI Layout

The Thorne UI inventory is a much smaller, focused window for equipment only.

```
┌───────────────────────┐
│ ┌───────────────────┐ │
│ │                   │ │
│ │    EQUIPMENT      │ │
│ │     SLOTS         │ │
│ │  (Anatomical)     │ │
│ │                   │ │
│ │                   │ │
│ │                   │ │
│ └───────────────────┘ │
├───────────────────────┤
│ [ DONE ] [ AA ]       │
└───────────────────────┘
```

## Element-by-Element Comparison

| Feature | Nillipuss | Thorne UI | Analysis |
| :--- | :--- | :--- | :--- |
| **Window Size** | `360x346` | `190x315` | Nillipuss is significantly wider to accommodate stats and bags. |
| **Equipment Slots** | Yes (21 slots) | Yes (21 slots) | Layout is different. Nillipuss is more compact. |
| **Character Stats** | **Yes** (extensive) | **Yes** (extensive) | Both include base stats and resists via EQTypes. |
| **Inventory Bags** | **Yes** (8 slots) | **Yes** (bag slots present) | Both include bag slots; layout differs. |
| **XP/AA Gauges** | Yes | Yes | Thorne includes AA gauge and AA current/total labels. |
| **Tabs (Stats, etc)**| **Yes** | **No** | Nillipuss uses tabs to switch between stat pages. |
| **Buttons** | Done, Face, Bank | Done, AA | Different functionality offered. |

## Feature Additions/Removals

*   **Nillipuss Additions**:
    *   Tab controls to switch between views.
    *   Zeal inventory slot counters (`IW_ZealSlotsTotal` EQType 84, `IW_ZealSlotsFilled` EQType 85).
    *   `Face` and `Bank` buttons.

*   **Thorne UI Additions**:
    *   AA progression labels (`IW_AAPercentage` EQType 27, `IW_AltAdvCurrent` EQType 36, `IW_AltAdvTotal` EQType 37).
    *   Modular screen zones for equipment, stats, progression, and bags.

---

## EQType Validation (Labels & Gauges)

**Thorne (Labels/Gauges):**
- Identity: Name **1**, Level **2**, Class **3**, Deity **4**
- HP/Mana: **70**, **80**
- AC/ATK: **22**, **23**
- Stats: STR **5**, STA **6**, DEX **7**, AGI **8**, WIS **9**, INT **10**, CHA **11**
- Resists: Poison **12**, Disease **13**, Fire **14**, Cold **15**, Magic **16**
- Weight: **24/25**
- XP: `IW_ExpGauge` **4**, `IW_EXPPercentage` **26**
- AA: `IW_AltAdvGauge` **5**, `IW_AAPercentage` **27**, `IW_AltAdvCurrent` **36**, `IW_AltAdvTotal` **37**

**Nillipuss (Labels/Gauges):**
- Same base stat/resist/weight EQTypes as Thorne
- XP gauge **4**, XP % **26**
- Zeal bag counters: **84/85**

## Stat-Icons Relevance

*   Nillipuss provides a clear example of a UI that prioritizes showing a large amount of numerical stat data at once. This is the opposite of the stat-icons goal, which is to use icons to save space.
*   The way Nillipuss groups stats (base stats, resists, skills) could inform how icons are grouped or categorized in the Thorne UI.
*   The sheer number of stats Nillipuss displays reinforces the need for a space-saving solution like icons if Thorne UI were to ever incorporate more stat visibility into its windows.
*   The equipment slot layout in Nillipuss is compact. Thorne's is more spread out, which may offer more room to place stat icons near the relevant equipment.
