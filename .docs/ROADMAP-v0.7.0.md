# Thorne UI v0.7.0 Roadmap — SHIPPED

**Version:** 0.7.0
**Status:** ✅ Shipped (February 22, 2026)
**Tag:** [v0.7.0](https://github.com/draknarethorne/thorne-ui/releases/tag/v0.7.0)

> **Archive Notice:** This roadmap is complete. All v0.7.0 features have shipped. For current work, see [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md) or [ROADMAP-v0.8.0.md](ROADMAP-v0.8.0.md).

---

## What Shipped

### 1. Spell Recast Timers (CastSpellWnd) ✅

- Individual spell gem recast time display
- Global spell recast timer (countdown until all spells available)
- Clear visual distinction between gems on cooldown vs. ready
- Implemented in both Cast window and Target window

### 2. Target Window Enhancements (TargetWindow) ✅

- Current Casting Spell Display — shows name of spell being cast by target
- Attack Delay Timer — visual countdown of target's next attack
- Improved information hierarchy and visibility

### 3. Stat Icons & Elemental Resistances ✅

- 18 stat icons (Player Stats, Resistances, Attributes) across 3 windows (HotButton, Stat Icon Bar, Inventory)
- Stat icon generation pipeline (`regen_icons.py`) with 6 icon pack variants (Classic, Duxa, Infiniti, Steamworks, Thorne, WoW)
- `stat_icons_thorne01.tga` atlas with centralized `<Ui2DAnimation>` definitions in `EQUI_Animations.xml`

### 4. SpellBook Meditate Button — Hidden ⚫

- Meditate button exists visually in spellbook but is **not functional** in the TAKP client
- Confirmed as a client limitation — button will remain hidden in the UI
- Not included as a shipped feature

### 5. Release Infrastructure ✅

- Standardized button, gauge, spell icon, and stat icon naming (Thorne-prefixed conventions)
- Expanded `Options/` organization for gauges, icons, buttons, cast, and animation variants
- Slot system foundation (`.Master/.Classes`, `.Items`, `.Themes`) with scripted generation
- Unified regen tooling and batch wrappers for all asset pipelines

---

## Timeline (Actual)

| Milestone              | Date         | Status |
| ---------------------- | ------------ | ------ |
| Feature Implementation | Feb 22, 2026 | ✅     |
| In-Game Testing        | Feb 22, 2026 | ✅     |
| v0.7.0 Release         | Feb 22, 2026 | ✅     |

---

## Successor Milestones

- **[ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md)** — Art system expansion and slot class overrides
- **[ROADMAP-v0.8.0.md](ROADMAP-v0.8.0.md)** — Multi-color gauges and enhanced group displays
- **[ROADMAP-v1.0.0.md](ROADMAP-v1.0.0.md)** — Logo branding, documentation, and release polish

---

## Reference

- [MASTER-FEATURE-INDEX.md](../.development/ui_analysis/MASTER-FEATURE-INDEX.md) — Feature analysis source
- [STANDARDS.md](STANDARDS.md) — UI design standards
- [README.md](../README.md) — Full version history

---

**Maintained by:** Draknare Thorne
**Last Updated:** March 2026
**Status:** Archived — v0.7.0 shipped
