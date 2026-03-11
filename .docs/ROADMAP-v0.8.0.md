# Thorne UI v0.8.0 Roadmap

**Version:** 0.8.0-dev
**Status:** 🔨 Active (Q2 2026)
**Branch:** `feature/gauges-v0.8.0`
**Previous:** [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md)

---

## Vision

v0.8.0 introduces advanced visual systems — dynamic multi-color health gauges and enhanced group displays — pushing Thorne UI's combat readability to the next level.

> **Context:** Zeal tick mana visuals, hotbar layout variants, and buff display variants were originally scoped for v0.8.0 but shipped ahead of schedule in v0.7.x releases.

---

## Feature Summary

| Feature                   | Status                     | Effort    |
| ------------------------- | -------------------------- | --------- |
| Multi-Color Health Gauges | Research complete          | Medium-Hi |
| Enhanced Group Displays   | Requires detailed analysis | 10-15h    |

---

## ⏳ Remaining Features

### 1. Multi-Color Health & Mana Gauge System

**Priority:** 🔴 High | **Impact:** Combat readability

Implement dynamic multi-color gauge fills that transition through color bands as HP/Mana changes (green → yellow → orange → red as HP drops), inspired by Nillipuss and DuxaUI implementations.

**Research Status:** Extensive analysis complete in `.development/health_gauges/`:

- [gauges-analysis.md](../.development/health_gauges/gauges-analysis.md) — Full inventory of 40+ gauges across 12 windows, core technique (oversized gauge layering with opaque occlusion)
- [gauges-clipping-design.md](../.development/health_gauges/gauges-clipping-design.md) — Clipping approach preserving Thorne's fill texture patterns
- [gauges-hybrid-design.md](../.development/health_gauges/gauges-hybrid-design.md) — Hybrid 4× stretch approach: solid-color-that-changes with reduced pattern degradation
- [gauges-experiment-plan.md](../.development/health_gauges/gauges-experiment-plan.md) — Side-by-side test plan using MusicPlayerWnd

**Three Approaches Under Consideration:**

1. **Full Stretch** (Nillipuss/DuxaUI style) — CX=10000, solid color that changes. Destroys Thorne fill patterns.
2. **Clipping** — Screen clip containers, perfect pattern fidelity, rainbow bar always visible. Moderate complexity.
3. **Hybrid Stretch** — CX=480 (4× display width), solid color with recognizable patterns. Best of both worlds.

**Next Step:** Run the side-by-side experiment (4 HP gauge variants on expanded MusicPlayerWnd) to visually compare approaches and select the winner.

**Rollout Scope:** Player, Target, Group, and Pet windows (40+ gauges total).

---

### 2. Enhanced Group Displays

**Priority:** 🟡 Medium | **Impact:** Raid/group awareness | **Effort:** 10-15 hours

Enhanced player displays and status indicators for the Group Window, informed by Nillipuss analysis (1972 line difference, 174% larger implementation).

**Current State:** Analysis complete, implementation not started. Requires detailed design work.

**Reference:** [GROUPWINDOW-analysis.md](../.development/ui_analysis/GROUPWINDOW-analysis.md)

---

## Timeline

| Milestone                    | Target  | Status              |
| ---------------------------- | ------- | ------------------- |
| Multi-color gauge experiment | Q2 2026 | ⏳ Ready to execute |
| Gauge rollout (all windows)  | Q2 2026 | ⏳ After experiment |
| Enhanced group displays      | Q2 2026 | 🔴 Needs analysis   |
| v0.8.0 Release               | Q2 2026 | ⏳ Planning         |

---

## Related Documentation

- [ROADMAP-v0.7.5.md](ROADMAP-v0.7.5.md) — Previous milestone
- [ROADMAP-v1.0.0.md](ROADMAP-v1.0.0.md) — Next milestone (release polish)
- [health_gauges/](../.development/health_gauges/) — Gauge research directory
- [MASTER-FEATURE-INDEX.md](../.development/ui_analysis/MASTER-FEATURE-INDEX.md) — Feature analysis source

---

**Maintained by:** Draknare Thorne
**Last Updated:** March 2026
