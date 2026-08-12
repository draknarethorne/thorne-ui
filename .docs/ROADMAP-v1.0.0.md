# Thorne UI v1.0.0 Roadmap

**Version:** 1.0.0-dev
**Status:** Planning (v0.9.0 bridge + v1.0.0 final release)
**Previous:** [ROADMAP-v0.8.0.md](ROADMAP-v0.8.0.md)

> **Moved from:** `.development/additional-enhancements/additional-enhancements-v1.0.0.md` (March 2026 reorganization)

---

## Vision

v1.0.0 is the **legendary release** — the culmination of branding, documentation, field standardization, and final polish that elevates Thorne UI from a refined custom skin to a fully realized, player-first interface system.

This roadmap tracks items that represent the finishing touches: logo identity across key screens, documentation completeness, code consistency, and creative explorations.

---

## How Thorne UI Modifications Work (TAKP Client Mechanics)

The **TAKP (The Al'Kabor Project)** client is a restored Macintosh-era EverQuest client (circa Planes of Power / Legacy of Ykesha era) that supports custom UI skins through the `uifiles/` directory system.

| Mechanic                    | How It Works                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Gauge colors & textures** | `<FillTint>` RGB values and `<GaugeDrawTemplate>` referencing TGA textures. See [STANDARDS.md](STANDARDS.md). |
| **Window sizing**           | `<Size>` and `<Location>` with inner `<Screen>` containers using `<RelativePosition>`.                        |
| **Logo/branding placement** | `.tga` images via `<StaticAnimation>` positioned with `<Location>` inside the desired window.                 |
| **Slot option themes**      | Organized by archetype × color theme in `Options/Slots/`. Generated via `.bin\regen_slots.bat`.                    |
| **Testing workflow**        | `.bin\sync-thorne-ui.bat` (full) or `.bin\sync-option.bat <path>` (variant) → `/loadskin thorne_dev`.                   |

---

## Feature Summary

| #   | Enhancement                                | Status                             |
| --- | ------------------------------------------ | ---------------------------------- |
| 1   | Logo: Character Select                     | In progress (v0.8.2 implementation)  |
| 2   | Logo: Inventory & Key Screens              | Partial (Inventory done)           |
| 3   | Documentation Consistency Pass             | Ongoing                            |
| 4   | Field Naming Standardization               | Writeup done, implementation partial  |
| 5   | Feature Harvest (Duxa/Nillipuss/Infiniti) | Planned for v0.9.0                |
| 6   | Theme System Foundation                    | Planned for v0.9.0                |
| 7   | Option Screenshot Catalog                  | Planned for v1.0.0                |

> **Context:** Stat icons, gauge refactor, spellbook icon reconciliation,
> slot class overrides, and multi-color gauges are shipped.
> Enhanced Group Displays remains deferred work entering the
> v0.9.0 → v1.0.0 cycle.

---

## v0.9.0 Pre-Release Polish Scope

v0.9.0 is the bridge milestone: lock high-value polish and feature-harvest work before the final 1.0.0 release pass.

### Planned Deliverables (v0.9.0)

1. **Documentation Drift Cleanup (Required)**
Align README, TODO, DEVELOPMENT, STANDARDS, and ROADMAP status language;
remove stale assumptions from older analysis summaries;
validate links and cross-references (`python .bin/scan_links.py`).

1. **Feature Harvest from Community UIs (Targeted)**
Capture practical, low-risk UX improvements inspired by Duxa/Nillipuss/Infiniti;
prioritize items that do not destabilize core window behavior;
track each candidate as: Adopt / Option-only / Defer.

1. **Theme Foundation (Color + Buttons + Window Chrome)**
Define shared theme surface area (button atlases, draw templates, gauge/chrome colors);
establish Theme options structure and naming conventions;
build first set of non-gray baseline variants as proof of pipeline.

1. **Option Screenshot Pipeline (toward v1.0.0 deliverable)**
Standardize screenshot naming, framing, and coverage matrix;
start capture pass for option families and key windows;
prepare final v1.0.0 gallery pass.

---

## Remaining Enhancements

### 1. Thorne Logo Integration: Character Selection Screen

**Objective:** Embed a Thorne logo into the character selection screen for immediate brand recognition on load.

**Approach:**

1. Reuse existing `A_Logo_6` animation from `EQUI_Animations.xml`
1. Add `CS_ThorneLogo` `<StaticAnimation>` in `EQUI_CharacterSelect.xml`
1. Include logo in `CharacterSelectWindow` `<Pieces>` list
1. Validate in-game placement across resolutions (1920×1080 and lower)

**Dependencies:** None (existing logo atlas assets already available).

**Status:** In progress (implemented in branch; pending in-game validation)

---

### 2. Thorne Logo Integration: Inventory & Key Screens

**Objective:** Add Thorne branding to inventory and potentially other core screens.

**Approach:**

1. Reuse the logo TGA from Enhancement #1
2. Add `<StaticAnimation>` logo to `EQUI_Inventory.xml` (e.g., below currency zone or beside equipment grid)
3. Evaluate additional screens: `EQUI_SpellBookWnd.xml`, `EQUI_PlayerWindow.xml`
4. Ensure logo doesn't interfere with functional elements or clickable slots

**Dependencies:** Enhancement #1 (logo asset)
**Status:** Not started

---

### 3. Documentation & Comments: Final Consistency Pass

**Objective:** Ensure all XML files have clear inline comments, all Options directories have accurate READMEs, and documentation cross-references are consistent.

**Scope:**

- Audit all 60 `EQUI_*.xml` files for missing or outdated `<!-- comments -->`
- Verify every `Options/` subdirectory has an accurate `README.md`
- Ensure STANDARDS.md, DEVELOPMENT.md, and TODO.md cross-reference consistently
- Validate all markdown links with `python .bin/scan_links.py`
- Standardize XML comment style (section headers, EQType annotations, layout explanations)
- Create reference docs from [STANDARDIZATION-ROADMAP](../.development/standards/STANDARDIZATION-ROADMAP.md):
  - `WINDOW-REGISTRY.md` — Standard dimensions, default positions, rationale
  - `ANIMATION-REGISTRY.md` — All custom animation definitions and their usage
  - `GAUGE-PROPERTIES-REFERENCE.md` — Gauge standard properties, defaults, copy-paste templates

**Existing Foundation:** v0.5.0 added attribution headers to 38+ files; most Options dirs have READMEs.
**Status:** Ongoing — always applicable as new work lands

---

### 4. Field Naming Standardization Across Windows

**Objective:** Apply consistent field naming conventions so XML is easier to navigate, maintain, and create variants from.

**Scope:** Player Window, Target Window, Pet Window, Actions Window, Merchant Window, Group Window
**Key Fields:** HP, Mana, Level, Class, Race, AC, ATK, Weight, AA labels and values
**Approach:** Apply prefix convention (`PW_`, `TW_`, `GW_`, etc.) documented in the naming writeup.

**Status:** Writeup complete, implementation not started

---

### 5. FriendsWnd Polish

**Objective:** Improve Friends window usability and layout consistency with modern Thorne patterns.

**Scope:** Button sizing/spacing pass, text alignment pass, style consistency pass.

**Status:** Not started

---

### 6. PetInfoWindow Command Surface Review

**Objective:** Re-evaluate pet command and buff-surface UX for optional improvements.

**Scope:** Assess command affordances, optional buff-strip variant feasibility, and click-safety around dismiss/attack controls.

**Status:** Not started

---

## Optional / Experimental

### Mini-Gauges (Potion Bottle Style)

Compact mini-gauges for health and mana — styled as potion bottles or small bars — for quick-glance validation. Place on the hotbutton bar or other window locations.

**Status:** Not started — experimental/creative exploration
**Infrastructure:** 7 gauge variants already ship with size-specific outputs via `.bin\regen_gauges.bat`.

---

## Quality & Polish Items

- [ ] **Button sizing uniformity** — Audit all windows for consistent button dimensions
- [ ] **Window border spacing** — Verify 2px left / 4px right border standard across all windows
- [ ] **Performance review** — Identify texture/animation optimization opportunities
- [ ] **Inventory stat icon alignment** — Revisit positioning on Inventory window

---

## Future / Post-v1.0.0

Items identified during analysis that are too large or speculative for v1.0.0. Tracked here for reference:

| Feature                    | Effort | Source                                |
| -------------------------- | ------ | ------------------------------------- |
| GuildManagementWnd         | 20-25h | Nillipuss-only (~914 lines)           |
| CharacterCreate UI         | 10-15h | Nillipuss-only (~3510 lines)          |
| Spellbook List View option | 5-8h   | Alternative to 2-column page view     |
| Dragitem Icon Set          | 4-6h   | 34 item textures from Nillipuss       |
| Custom Cursor Variants     | 2-3h   | Nillipuss cursor texture set concepts |

**Source:** [MASTER-FEATURE-INDEX](../.development/ui_analysis/MASTER-FEATURE-INDEX.md) and [WINDOWS-BY-PRIORITY](../.development/ui_analysis/WINDOWS-BY-PRIORITY.md)

---

## Asset Pipeline Reference

| Pipeline        | Script                                        | Output Location                       |
| --------------- | --------------------------------------------- | ------------------------------------- |
| Gauge textures  | `.bin\regen_gauges.bat` / `.bin/regen_gauges.py`   | `Options/Gauges/[variant]/`           |
| Spell gem icons | `.bin\regen_gems.bat` / `.bin/regen_gems.py`       | `Options/Icons/[variant]/`            |
| Stat icons      | `.bin\regen_icons.bat` / `.bin/regen_icons.py`     | `thorne_drak/stat_icons_thorne01.tga` |
| Slot textures   | `.bin\regen_slots.bat` / `.bin/regen_slots.py`     | `Options/Slots/[class]/[theme]/`      |
| Button textures | `.bin/generate_thorne_buttons_transparent.py` | `Options/Buttons/[variant]/`          |

---

## Related Documentation

- [ROADMAP-v0.8.0.md](ROADMAP-v0.8.0.md) — Previous milestone
- [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md) — Current active milestone
- [ROADMAP-v0.7.0.md](ROADMAP-v0.7.0.md) — Archived (shipped)
- [STANDARDS.md](STANDARDS.md) — UI design standards
- [README.md](../README.md) — Full version history
- [DEVELOPMENT.md](DEVELOPMENT.md) — Architecture and contribution guide

---

**Maintained by:** Draknare Thorne
**Last Updated:** May 2026

_For the glory of Thorne!_
