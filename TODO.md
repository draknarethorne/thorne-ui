# Thorne UI — TODO

Development tracker for Thorne UI. For detailed implementation plans, see the versioned roadmaps in `.docs/`.

**Current Branch:** `main`
**Maintainer:** Draknare Thorne

---

## Roadmaps

| Version | Status      | Focus                               | Link                                      |
| ------- | ----------- | ----------------------------------- | ----------------------------------------- |
| v0.7.0  | ✅ Shipped  | Recast timers, stat icons, options  | [ROADMAP-v0.7.0](.docs/ROADMAP-v0.7.0.md) |
| v0.7.5  | ✅ Shipped  | Slot art expansion, class overrides | [ROADMAP-v0.7.5](.docs/ROADMAP-v0.7.5.md) |
| v0.8.0  | ⏳ Planning | Multi-color gauges, group displays  | [ROADMAP-v0.8.0](.docs/ROADMAP-v0.8.0.md) |
| v1.0.0  | ⏳ Planning | Logo branding, docs, release polish | [ROADMAP-v1.0.0](.docs/ROADMAP-v1.0.0.md) |

---

## What's Been Done (Summary)

### Shipped Releases

| Version | Date       | Highlights                                                                 |
| ------- | ---------- | -------------------------------------------------------------------------- |
| v0.7.5  | 2026-03-10 | Class slot art (15 classes × 7 themes), auto-tone, weapon archetypes      |
| v0.7.3  | 2026-03-04 | Logo atlas (7 lighting modes), tab icon branding, gauge polish             |
| v0.7.2  | 2026-03-03 | Slot art expansion (Actions 28×28, Inspect 40×40), dark rounded templates  |
| v0.7.1  | 2026-03-02 | HotButton 14-stat layout, post-v0.7.0 polish                               |
| v0.7.0  | 2026-02-22 | Spell recast timers, stat icons (18 icons, 6 packs), Options modernization |
| v0.6.5  | 2026-02-15 | Spellbook polish, Thorne-first option sync, 6 spell icon packs             |
| v0.6.4  | 2026-02-12 | Gauge overhaul, target window enhancements                                 |
| v0.6.3  | 2026-02-10 | MusicPlayer stat bar, selector vertical layout, pet window polish          |
| v0.6.2  | 2026-02-08 | Merchant tabbed interface, actions player info tab                         |
| v0.6.1  | 2026-02-07 | Hotbutton bag/weapon layout, actions thorne classic option                 |
| v0.6.0  | 2026-02-06 | Phase 3.9 inventory redesign (anatomical 4-column, 45×45 slots)            |
| v0.5.0  | 2026-01-20 | Foundation release (all core windows, documentation system)                |

### Completed Components (All 100%)

Group Window, Pet Window, Player Window, Inventory (Phase 3.9), Actions Window (tabs, player info), Textures & TGA validation, Stat Icons (18 icons, 3 windows, 6 packs), Title Bars, Selector Window (horizontal + vertical), Action Buttons (investigated — client limitation), HotButton (bag/weapon/armor layout, 14-stat trial), Merchant (tabbed + standard), Target Window (level, class, pet HP, ToT), Open All Bags (researched — not natively possible), Target of Target (Zeal separate window), Spellbook (icon reconciliation, large variant, 6 packs), UI Standards (window drag rejected), Architecture (animation centralization decided)

### Key Decisions

- **Gauge centralization:** All Thorne animations live in `EQUI_Animations.xml`; Options swap TGA files, not definitions
- **Window drag affordances:** Rejected — borders already allow dragging
- **Action buttons:** Not possible — TAKP client limitation (only hardcoded ScreenIDs work)
- **Deity display:** Not possible — no EQType for character deity in TAKP/P2002 client
- **SpellBook meditate:** Hidden — button not functional in TAKP client

---

## Remaining Work

### v0.7.5 — Slot Class Overrides (✅ Shipped)

- [x] Build automated icon scoring pipeline (SQL → stat-weighted scoring → icon picks)
- [x] Per-class weapon archetype hints and cross-slot dedup
- [x] Auto-tone gamma correction for Research icons
- [x] Promote 15 class atlases to .Classes/ (production-ready)
- [x] Run `regen_slots.py --all` for 16 classes × 7 themes (112 combos)
- [x] Visual verification and in-game testing

### v0.8.0 — Advanced Visual Systems

- [ ] Multi-color health gauge experiment (4 variants on MusicPlayerWnd)
- [ ] Select winning gauge approach (Full Stretch / Clipping / Hybrid)
- [ ] Roll out multi-color gauges to Player, Target, Group, Pet (40+ gauges)
- [ ] Enhanced Group Displays analysis and implementation (10-15h)

### v1.0.0 — Logo Branding & Release Polish

- [ ] Thorne logo: Character Select screen
- [ ] Thorne logo: Inventory & key screens
- [ ] Documentation consistency pass (60 XML files, all Options READMEs, registry docs)
- [ ] Field naming standardization (PW*, TW*, GW\_ prefix convention)
- [ ] FriendsWnd "Find" button polish (1-2h)
- [ ] PetInfoWindow "Pet Commands" button (1-2h)

### Quality & Polish (Any Version)

- [ ] **Button sizing uniformity** — Audit all windows for consistent dimensions
- [ ] **Window border spacing** — Verify 2px left / 4px right across all windows
- [ ] **Performance review** — Texture/animation optimization opportunities
- [ ] **Inventory stat icon alignment** — Revisit positioning on Inventory window
- [ ] **UI affordances from variant analysis** — Document patterns from duxaui, vert, Infiniti-Blue

---

## Options Sync System

All 13 primary windows have Options sync with Default backups:

Actions, Animations, Group, Hotbutton, Inventory, Loot, Merchant, Pet, Player, Selector, Skin, Spellbook, Target

**Usage:** See [SYNC-SCRIPTS.md](SYNC-SCRIPTS.md) for sync workflow.

**Checking sync status:**

```bash
cat thorne_drak/Options/[Window]/.sync-status.json
```

---

## Asset Pipelines

| Pipeline | Command                                       | Output                     |
| -------- | --------------------------------------------- | -------------------------- |
| Gauges   | `regen_gauges.bat`                            | `Options/Gauges/[variant]` |
| Gems     | `regen_gems.bat`                              | `Options/Icons/[variant]`  |
| Icons    | `regen_icons.bat`                             | `stat_icons_thorne01.tga`  |
| Slots    | `regen_slots.bat`                             | `Options/Slots/[class]/`   |
| Buttons  | `.bin/generate_thorne_buttons_transparent.py` | `Options/Buttons/`         |

---

## Notes

- Keep track of EQType discoveries for reference
- Document any new gauge templates created
- Maintain consistent naming conventions for variants
- Test all changes in-game before committing

---

**Maintainer:** Draknare Thorne
**License:** Custom UI for personal use with The Al'Kabor Project.
