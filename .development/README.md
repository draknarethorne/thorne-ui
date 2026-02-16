# .development Directory

**Purpose**: Internal working documents, planning, and analysis files - NOT included in published releases

This directory contains:
- Session logs and tracking documents
- Problem analysis and research
- Development planning and roadmaps
- Working notes and temporary documentation
- Scripts and utilities for development workflow

**Important**: Files here are for internal development use only. They are not published in releases or included in distribution ZIPs.

## Directory Structure

### `initial-phases/`
Phase-by-phase development documentation:
- `PHASE-*.md` - Individual phase documentation (completed and planned)
- `PHASE-6-INVENTORY-WINDOWS/` - Detailed research and analysis for inventory redesign
- `README.md` - Phase index and navigation

### `readme-sync/`
README improvement tracking and planning:
- `OPTIONS_README_IMPROVEMENT_STATUS.md` - Current status of Options variant documentation
- `CONTENT_EXPANSION_PLAN.md` - Plan for expanding variant docs
- `GAP_ANALYSIS_FOR_150_LINE_THRESHOLD.md` - Analysis of documentation gaps
- `WORKLOAD_ASSESSMENT.md` - Development workload planning

### `releases/`
Release management documentation:
- `QUICK-PUSH.md` - Helper for pushing releases

### `standards/`
Standardization planning and roadmaps:
- `STANDARDIZATION-ROADMAP.md` - UI refactoring opportunities and planning

### `options-sync/`
Options variant synchronization documentation:
- Delivery summaries and sync documentation

### `ui-analysis/`
Analysis and research for specific UI windows and features:
- `README.md` - Index and navigation
- Window-specific analyses (e.g., `PLAYERWINDOW-analysis.md`)
- Cross-window coverage and priority indexes

### `architecture/`
Architecture decisions and infrastructure notes.

### `stat-icons/`
Stat icon redesign working notes and archives.

### `technical/`
Maintainer-only technical notes and limitations.

---

**Note**: If updating these files, remember they won't reach users. For user-facing documentation, use `.docs/` directory instead.
