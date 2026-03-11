# Thorne UI v0.7.5 Roadmap

**Version:** 0.7.5
**Status:** ✅ Shipped (March 10, 2026)
**Branch:** `feature/class-slot-images-v0.7.5` (merged to `main`)
**Previous:** [ROADMAP-v0.7.0.md](ROADMAP-v0.7.0.md) (shipped)

---

## Vision

v0.7.5 extends the art system and asset pipelines introduced in v0.7.0 — expanding slot art, logo branding, and visual polish across the UI. The milestone culminates with class-specific slot item overrides.

---

## ✅ Shipped (v0.7.1–v0.7.3)

### v0.7.1 — HotButton Polish & Post-v0.7.0 Iteration

- Expanded `EQUI_HotButtonWnd.xml` utility row into a full 14-stat trial layout (MusicPlayer-style icon/value spacing)
- Preserved stacked bag/weapon utility arrangement while improving under-hotbar information density
- Synced Hotbutton option variant files and metadata with current live layout

### v0.7.2 — Slot Art System Expansion

- Repurposed Actions window Info tab as Worn equipment mini-slots (28×28, 5-row anatomical grid)
- Redesigned Inspect window with full 6-row anatomical layout (40×40, Inventory-matching)
- Migrated all slot backgrounds to `A_Slot_*` art system across both windows
- Added `A_Slot_Logo5` branding element to Inspect window
- Added Thorne Classic option variant for Actions window

### v0.7.3 — Logo Atlas & Branding

- Built `generate_thorne_logo_atlas.py` with 7 lighting modes (source, flat, radial_glow, radial_top_bias, bottom_light, top_light, rim_light)
- JSON-driven config for atlas layout, transparency rows, and icon generation
- Created `logo_atlas_thorne01.tga` (256×256, 6 columns × 6 transparency rows)
- Tab icon branding for Actions window (18×18 icon atlas with LANCZOS downscale, gold-tinted active variant)
- Casting gauge and group pet HP color standardization
- Slot background migration to `A_Slot_*` art system across key windows
- Comprehensive gauge color audit and multi-color design documentation

---

## ✅ Shipped (v0.7.5)

### Slot Class Item Overrides

**Priority:** ✅ Complete | **Effort:** Medium | **Branch:** `feature/class-slot-images-v0.7.5`

Built an automated icon scoring pipeline to select class-appropriate item icons for 15 EQ classes, then generated all slot atlas combinations.

**What was built:**
- `pick_class_icons.py` — Stat-weighted scoring with class specificity, exclusivity, and confidence penalties
- Per-class `weapon_hints` for archetype-typical item types (Bard instruments, Cleric maces, etc.)
- Cross-slot deduplication across primary/secondary/range/ammo
- Class-restricted item filtering on all equipment slots
- Auto-tone gamma correction targeting luminance 85–175 for icon readability
- `generate_regen_json.py` — Compact Master-style JSON formatter
- `regen_thorne.py` — Config-level `auto_tone` default with per-item override priority
- 112 slot combos generated (16 classes × 7 themes)
- 15 class atlases promoted from `.Research/` to `.Classes/` (production-ready)

### Final Polish

- Options README accuracy pass for new v0.7.1–v0.7.3 content
- Sync metadata (`.sync-status.json`) updates where applicable

---

## Timeline

| Milestone             | Target         | Status |
| --------------------- | -------------- | ------ |
| v0.7.1–v0.7.3 Polish | Mar 2–4, 2026  | ✅     |
| v0.7.4 Container/Logo | Mar 6, 2026    | ✅     |
| Class Slot Overrides  | Mar 10, 2026   | ✅     |
| v0.7.5 Release        | Mar 10, 2026   | ✅     |

---

## Related Documentation

- [ROADMAP-v0.7.0.md](ROADMAP-v0.7.0.md) — Previous milestone (shipped)
- [ROADMAP-v0.8.0.md](ROADMAP-v0.8.0.md) — Next milestone
- [item_slots/README.md](../.development/item_slots/README.md) — Slot system documentation
- [STANDARDS.md](STANDARDS.md) — UI design standards

---

**Maintained by:** Draknare Thorne
**Last Updated:** March 2026
