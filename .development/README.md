# .development Directory

## Behind the Legend: Draknare Thorne's Workshop

This directory is the **craftsman's workshop** for Thorne UI—where legendary interfaces are born. Here lies the research, planning, analysis, and working documents that fuel development.

**Not for Public Consumption:** Files here are internal development notes, explorations, and work-in-progress documents. They are not published in releases and are excluded from distribution ZIPs.

**What's Here:**

- Deep analysis of EverQuest UI patterns (community variants, window architecture)
- Implementation research and feature feasibility studies
- Development phase documentation and progress tracking
- v0.7.0+ planning, timelines, and decision records
- Technical experiments and architecture notes
- Utility scripts and development workflow helpers

## Current Focus: v0.7.5 (March 2026)

**Active Development:**

- 🎯 **Slot class item overrides** — Populate `item_overrides` in class configs, regenerate atlases
- ✅ ~~v0.7.0 features~~ (spell recast timers, stat icons, target enhancements) — SHIPPED
- ✅ ~~v0.7.1–v0.7.3~~ (HotButton layout, slot art expansion, logo atlas, tab branding) — SHIPPED
- ⚫ **SpellBook meditate button** — Hidden (TAKP client limitation, not functional)

**For Implementation Details:**
→ See [.docs/ROADMAP-v0.7.5.md](../.docs/ROADMAP-v0.7.5.md) (current milestone)  
→ See [.docs/ROADMAP-v0.8.0.md](../.docs/ROADMAP-v0.8.0.md) (next: gauges & group)  
→ See [.docs/ROADMAP-v1.0.0.md](../.docs/ROADMAP-v1.0.0.md) (release polish)  
→ See [ui_analysis/README.md](./ui_analysis/README.md) (comprehensive feature analysis)

## Directory Structure (Organized by Purpose)

### `ui-analysis/` — **The Research Engine**

Where we decode what makes legendary UIs work:

- **Window-by-window analyses** (17 detailed breakdowns of ActionsWindow, TargetWindow, CastSpellWnd, etc.)
- **MASTER-FEATURE-INDEX.md** - Complete inventory of features to implement (v0.7.0 through v0.8.0+)
- **COMPLETE-COVERAGE.md** - 100% coverage analysis of Thorne vs. community variants
- Cross-window pattern research and opportunity identification

**Active:** Feeding v0.7.0 implementation priorities (6 features, 9-17 hours)

### `stat-icons/` — **Stat Icon System** ✅ COMPLETE

Complete stat icon generation, deployment, and window integration:

- 18 standardized icon textures (player stats, resistances, attributes)
- Automated pipeline (`regen_icons.py`) with 6 icon pack variants
- Integrated into HotButton window, Stat Icon Bar (MusicPlayerWnd), and Inventory

**Status:** Complete — shipped in v0.7.0

### `initial_phases/` — **Phase Documentation**

Detailed record of UI development phases (Foundation → Polish):

- **PHASE-1-2** through **PHASE-5** (all completed and shipped)
- **PHASE-3.9-INVENTORY-REDESIGN** ✅ Completed (shipped v0.6.0)
- **PHASE-5-TARGET-WINDOW** ✅ Completed (shipped v0.6.4)
- **PHASE-6-INVENTORY-WINDOWS/** — Archived research (20 community UI analysis docs)
- **README.md** - Phase index and status tracker

**Key Phases:**

- ✅ Phase 1-2: Foundation (Actions, Hotbar, Inventory tabs)
- ✅ Phase 3: Merchant window
- ✅ Phase 3.5-3.7: Refine infrastructure
- ✅ Phase 3.9: Inventory redesign (v0.6.0)
- ✅ Phase 5: Target window (v0.6.4)
- 📚 Phase 6: Community UI research (informing current work)

### `standards/` — **Architecture & Standards**

Standardization planning, refactoring opportunities, and infrastructure notes.

### `archive/` — **Stale & Superseded**

Documents moved out of active development. Preserved for git history:

- Phase docs that were never started (Phases 4, 5.5, 6-Containers, 7, 8)
- One-time delivery artifacts (options sync, release implementation)
- Superseded planning docs (MCP limitations, class-type ideas)

---

## How to Navigate

**I want to know what to build next:**  
→ [ui_analysis/MASTER-FEATURE-INDEX.md](ui_analysis/MASTER-FEATURE-INDEX.md)

**I want to see all window analyses:**  
→ [ui_analysis/README.md](ui_analysis/README.md)

**I want to see current plans:**  
→ [.docs/ROADMAP-v0.7.5.md](../.docs/ROADMAP-v0.7.5.md) (active)  
→ [.docs/ROADMAP-v0.8.0.md](../.docs/ROADMAP-v0.8.0.md) (next)  
→ [.docs/ROADMAP-v1.0.0.md](../.docs/ROADMAP-v1.0.0.md) (release)

**I want to see what phase we're on:**  
→ [initial_phases/README.md](initial_phases/README.md)

---

## Key Principles

✅ **Deep Analysis Precedes Implementation** - Research across community variants informs design  
✅ **Decisions Are Documented** - Why we do things matters as much as what  
✅ **History Is Preserved** - Archived research stays accessible for future learning  
✅ **Focus Flows Forward** - Current work (v0.7.5) builds on legendary foundations (v0.7.0)

---

**Craftship Notes:**

- These files support the visible UI but remain invisible to end users
- What you see in releases is the polished result; what you see here is the forge
- Questions about development direction? Start with the versioned roadmaps in `.docs/` or MASTER-FEATURE-INDEX.md
