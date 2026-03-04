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

## Current Focus: v0.7.0 (March 2026 Release)

**Active Development:**
- 🎯 **Spell recast timers** (CastSpellWnd)
- 🎯 **Target window enhancements** (spell name, attack delay)
- 🎯 **Elemental resistance icons** (ActionsWindow)
- 🎯 **SpellBook meditate button** (SpellBookWnd)

**For v0.7.0 Implementation Details:**
→ See [.docs/ROADMAP-v0.7.0.md](../.docs/ROADMAP-v0.7.0.md)  
→ See [ui-analysis/README.md](./ui_analysis/README.md) (comprehensive feature analysis)

## Directory Structure (Organized by Purpose)

### `ui-analysis/` — **The Research Engine**
Where we decode what makes legendary UIs work:
- **Window-by-window analyses** (17 detailed breakdowns of ActionsWindow, TargetWindow, CastSpellWnd, etc.)
- **MASTER-FEATURE-INDEX.md** - Complete inventory of features to implement (v0.7.0 through v0.8.0+)
- **COMPLETE-COVERAGE.md** - 100% coverage analysis of Thorne vs. community variants
- Cross-window pattern research and opportunity identification

**Active:** Feeding v0.7.0 implementation priorities (6 features, 9-17 hours)

### `stat-icons/` — **Phase 3.9 Icon System**
Implementation research and techniques for integrating stat icons across windows:
- Icon texture strategy and consolidation
- EQType bindings for stat icon displays
- Window-by-window icon implementation notes

**Status:** Informing v0.7.0 resistance icons feature

### `initial-phases/` — **Phase Documentation**
Detailed record of UI development phases (Foundation → Polish):
- **PHASE-1-2** through **PHASE-8** (8 phases, both completed and planned)
- **PHASE-3.9-INVENTORY-REDESIGN** ✅ Completed (shipped v0.6.0)
- **PHASE-6-INVENTORY-WINDOWS/** — Archived research (8 community UI analysis docs)
- **README.md** - Phase index and status tracker

**Key Phases:**
- ✅ Phase 1-2: Foundation (Actions, Hotbar, Inventory tabs)
- ✅ Phase 3: Merchant window
- ✅ Phase 3.5-3.7: Refine infrastructure
- ✅ Phase 3.9: Inventory redesign (v0.6.0)
- 📚 Phase 6: Community UI research (archived, informing current work)
- 📋 Phase 4-8: Planned enhancements

### `releases/` — **Release Management**
Release process utilities and documentation:
- Testing workflows and checklist templates
- Historical release documentation and changelogs
- Workflow implementation notes (maintainer reference)

### `options-sync/` — **Variant Management**
Delivery summaries, sync documentation, and variant deployment planning.



### `readme-sync/` — **Documentation Planning**
README improvement tracking and content expansion planning for Options variants.

### `standards/` — **Architecture & Standards**
Standardization planning, refactoring opportunities, and infrastructure notes.

### `technical/` — **Deep Dives**
Maintainer-only technical explorations, limitations, and edge cases.

### `quality_tools/` — **QA & Validation**
Scripts and utilities for code quality, syntax validation, and testing automation.

### `architecture/` — **Design Decisions**
Architecture decisions, system patterns, and infrastructure evolution record.

---

## How to Navigate

**I want to know what to build next:**  
→ [ui_analysis/MASTER-FEATURE-INDEX.md](ui_analysis/MASTER-FEATURE-INDEX.md)

**I want to see all window analyses:**  
→ [ui_analysis/README.md](ui_analysis/README.md)

**I want to understand current v0.7.0 plans:**  
→ [.docs/ROADMAP-v0.7.0.md](../.docs/ROADMAP-v0.7.0.md)

**I want to see what phase we're on:**  
→ [initial_phases/README.md](initial_phases/README.md)



---

## Key Principles

✅ **Deep Analysis Precedes Implementation** - Research across community variants informs design  
✅ **Decisions Are Documented** - Why we do things matters as much as what  
✅ **History Is Preserved** - Archived research stays accessible for future learning  
✅ **Focus Flows Forward** - Current work (v0.7.0) builds on legendary foundations (v0.6.0/v0.6.5)

---

**Craftship Notes:**
- These files support the visible UI but remain invisible to end users
- What you see in releases is the polished result; what you see here is the forge
- Questions about development direction? Start with ROADMAP-v0.7.0.md or MASTER-FEATURE-INDEX.md

