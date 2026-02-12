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

### `phases/`
Phase-by-phase development documentation:
- `PHASE-*.md` - Individual phase documentation (completed and planned)
- `PHASE-6-INVENTORY-WINDOWS/` - Detailed research and analysis for inventory redesign
- `README.md` - Phase index and navigation

### `readme/`
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

### `analysis/`
Analysis and research for specific problem areas:
- `README_INCONSISTENCY_ANALYSIS.md` - Analysis of README formatting issues
- `README_STANDARDS_ANALYSIS.md` - Analysis of README standards implementation
- Other technical analysis documents

---

**Note**: If updating these files, remember they won't reach users. For user-facing documentation, use `.docs/` directory instead.
