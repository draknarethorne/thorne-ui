# Thorne UI v0.8.0 Roadmap

**Version:** 0.8.0
**Status:** ✅ Shipped (June 2026)
**Branch:** `feature/gauges-v0.8.0` (PR #68)
**Previous:** [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md)

---

## Vision

v0.8.0 delivers advanced visual systems — dynamic multi-color health gauges using a novel A/B composite architecture with oversized animation clipping. This gives Thorne UI color-band health transitions (green → yellow → orange → red as HP drops) while preserving texture detail through the two-part rendering technique.

> **Context:** Zeal tick mana visuals, hotbar layout variants, and buff display variants were originally scoped for v0.8.0 but shipped ahead of schedule in v0.7.x releases. Enhanced Group Displays deferred to a future milestone.

---

## Feature Summary

| Feature                   | Status                     | Effort    |
| ------------------------- | -------------------------- | --------- |
| Multi-Color Health Gauges | ✅ Shipped                  | Medium-Hi |
| Snap-Columns Pipeline     | ✅ Shipped                  | Medium    |
| Gauge Audit Tooling       | ✅ Shipped                  | Medium    |
| Enhanced Group Displays   | ⏳ Deferred (future)        | 10-15h    |

---

## ✅ Shipped Features

### 1. Multi-Color Health & Mana Gauge System

**Priority:** 🔴 High | **Impact:** Combat readability | **Status:** ✅ Shipped

Implemented dynamic multi-color gauge fills that transition through color bands as HP/Mana changes (green → yellow → orange → red as HP drops), using a novel **two-part A/B composite architecture**.

**Architecture:**

- **A-part**: Oversized ×100 animation inside Screen viewport clip — creates threshold visibility effect
- **B-part**: Native-resolution animation with offset — preserves texture detail for the continuation
- **5 color bands** per gauge, stacked via opaque layer occlusion (not transparency blending)
- **Veil palettes**: Red (HP), Blue (Mana) — desaturated alarm → full saturation gradient

**Scope Deployed:**

- 7 production windows: Player, Target, Group, Pet, Breath, Spellbook, MusicPlayer
- 23 XML files total (including Options and Testing variants)
- 48 oversized animations across 3 sizes (105t, 120t, 250t) × 4 fill styles
- All Option variants updated: Bars, Thorne, Thorne Arc, Thorne Veil

**Tooling Built:**

- `regen_gauges.py` enhanced with `snap_columns` for pixel-perfect grid markers at exact fifths
- `audit_gauges.py` — comprehensive audit of all animations + XML files
- `fix_gauge_offsets.py` — bulk correction tool (826 fixes applied across 24 files)

**Research & Design:** `.development/health_gauges/`

- [gauges-analysis.md](../.development/health_gauges/gauges-analysis.md) — Full gauge inventory and technique analysis
- [gauges-clipping-design.md](../.development/health_gauges/gauges-clipping-design.md) — Clipping approach (selected)
- [gauges-hybrid-design.md](../.development/health_gauges/gauges-hybrid-design.md) — Hybrid approach (evaluated)
- [README.md](../.development/health_gauges/README.md) — Technical reference for the composite gauge system

---

### 2. Enhanced Group Displays (⏳ Deferred)

**Priority:** 🟡 Medium | **Impact:** Raid/group awareness | **Effort:** 10-15 hours
**Deferred to:** Future milestone (v1.0.0+)

Enhanced player displays and status indicators for the Group Window, informed by Nillipuss analysis (1972 line difference, 174% larger implementation).

**Current State:** Analysis complete, implementation not started. Requires detailed design work.

**Reference:** [GROUPWINDOW-analysis.md](../.development/ui_analysis/GROUPWINDOW-analysis.md)

---

## Timeline

| Milestone                    | Target  | Status               |
| ---------------------------- | ------- | -------------------- |
| Multi-color gauge experiment | Q2 2026 | ✅ Shipped            |
| Gauge rollout (all windows)  | Q2 2026 | ✅ Shipped            |
| Snap-columns pipeline        | Q2 2026 | ✅ Shipped            |
| Gauge audit tooling          | Q2 2026 | ✅ Shipped            |
| Enhanced group displays      | ---     | ⏳ Deferred           |
| v0.8.0 Release               | Q2 2026 | ✅ Shipped            |

---

## Related Documentation

- [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md) — Previous milestone
- [ROADMAP-v1.0.0.md](ROADMAP-v1.0.0.md) — Next milestone (release polish)
- [health_gauges/](../.development/health_gauges/) — Gauge research directory
- [MASTER-FEATURE-INDEX.md](../.development/ui_analysis/MASTER-FEATURE-INDEX.md) — Feature analysis source

---

**Maintained by:** Draknare Thorne
**Last Updated:** June 2026
