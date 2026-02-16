# .bin Directory Audit & Cleanup Plan

**Generated:** February 13, 2026  
**Status:** Complete inventory + recommendations

---

## Summary

**Total scripts:** 23 items  
**Categories:**
- ✅ **Active & Needed:** 5 scripts
- 🔄 **Supporting/Specialized:** 5 scripts  
- ⚠️ **Redundant/Legacy:** 6 scripts
- 📦 **Already Archived:** 6 scripts

---

## Active & Essential Scripts ✅

These are core tools you use regularly.

| Script | Purpose | Keep? | Notes |
|--------|---------|-------|-------|
| `regen_gauges.py` | Regenerate all gauge textures | **YES** | PRIMARY GAUGE TOOL - Does tall + wide automatically |
| `generate_stat_icons.py` | Generate stat icon textures | **YES** | PRIMARY ICON TOOL - Complex, needs dedicated .md |
| `fix_tga_files.py` | Convert PNG→TGA format | **YES** | UTILITY - Used by regen_gauges.py automatically |
| `validate_stat_icons.py` | Validate icon texture files | **YES** | QA TOOL - Good to keep for testing |
| `add_abbreviations_to_textures.py` | Add text labels to icons | **YES** | UTILITY - Used by generate_stat_icons.py |

---

## Options Management Scripts (5 total) 🔄

These scripts manage the Options/ directory structure, variants, and documentation. Deep analysis shows they serve distinct purposes:

| Script | Purpose | Type | Keep? |
|--------|---------|------|-------|
| `options_default_compare.py` | Audit which variants differ from Default | Auditor | **YES** |
| `options_default_sync.py` | Backup working files to Default/ | Operator | **YES** |
| `options_duplicate_detector.py` | Find identical/redundant variants | Auditor | **YES** |
| `options_generate_readme.py` | Create skeletal README templates | Operator | **YES** |
| `options_fix_readme.py` | Auto-fix README formatting | Operator | **YES** |
| `options_readme_checker.py` | Audit README quality/placement | Auditor | **YES** |

**Analysis Summary:**
- These scripts fall into two categories: **Auditors** (analyze current state) and **Operators** (modify files)
- Consolidation possible but **not recommended** - each has clear purpose + sync is destructive operation
- Better approach: Document as a group with clear purpose + example workflows

**Recommendation:** Keep all 5, document collectively as "Options Management Tools" group

**References:** See [OPTIONS-ANALYSIS.md](OPTIONS-ANALYSIS.md) for detailed breakdown

---

---

## Redundant/Legacy Scripts ⚠️

These should be moved to archive or deleted.

| Script | Issue | Action |
|--------|-------|--------|
| `generate_tall_gauges.py` | **SUPERSEDED** by `regen_gauges.py` (newer, better, faster) | **MOVE TO ARCHIVE** |
| `push-v0.4.0-tag.sh` | **HARDCODED VERSION** - only works for v0.4.0 release | **DELETE/ARCHIVE** |
| `quick-push.sh` | **HARDCODED VERSION** - only works for v0.4.0 release | **DELETE/ARCHIVE** |
| `test-release-workflow.sh` | **RELEASE-SPECIFIC** - testing script for v0.4.0 pipeline | **DELETE/ARCHIVE** |
| `fix_tga_files.ps1` | **DUPLICATE** - PowerShell version of fix_tga_files.py | **DELETE** (Python version preferred) |
| `fix_tga_files.sh` | **DUPLICATE** - Shell version of fix_tga_files.py | **DELETE** (Python version preferred) |

---

## Already in Archive 📦

These are kept for reference/historical purposes:

```
archive/
├── analyze_gemicons.py            # Old tool for gemicon analysis
├── detect_gemicon_grid.py          # Old grid detection tool
├── extract_gemicon_coordinates.py  # Old coordinate extraction
├── fix_gauge_tga.py                # Superseded by regen_gauges.py
├── generate_abbreviation_reference.py
└── generate_master_stat_icons.py   # Old icon generation (v1)
```

These are correctly archived ✅

---

## Missing/Not Found ✗

| Script | Location | Status |
|--------|----------|--------|
| `cleanup-assistant.bat` | Not in .bin | ✓ Good - doesn't exist |
| `SCRIPTS_README.md` | C:\Thorne-UI\.bin\ | Duplicate/old (rename to README.md) |

---

## Recommended Actions

### IMMEDIATE (Next commit)

1. **Move to archive:**
   ```
   generate_tall_gauges.py     (replaced by regen_gauges.py)
   push-v0.4.0-tag.sh          (hardcoded release script)
   quick-push.sh               (hardcoded release script)
   test-release-workflow.sh    (test for old release pipeline)
   ```

2. **Delete (no longer needed):**
   ```
   fix_tga_files.ps1           (duplicate, use .py version)
   fix_tga_files.sh            (duplicate, use .py version)
   SCRIPTS_README.md           (duplicate, use README.md)
   ```

3. **Document the `options_*` scripts:**
   - Do you actively use these 5 scripts?
   - If YES → Create `options_scripts.md` with brief overview of all 5
   - If NO → Move all 5 to archive

---

## Cleanup Checklist

- [ ] **Confirm:** Are the `options_*.py` scripts still needed?
  - [ ] YES → Move to documentation plan (add to .bin/STANDARDS.md audit)
  - [ ] NO → Move all 5 to archive/

- [ ] Move legacy scripts to archive:
  - `generate_tall_gauges.py` → archive/
  - `push-v0.4.0-tag.sh` → archive/
  - `quick-push.sh` → archive/
  - `test-release-workflow.sh` → archive/

- [ ] Delete duplicate versions:
  - `fix_tga_files.ps1` (keep only .py)
  - `fix_tga_files.sh` (keep only .py)
  - `SCRIPTS_README.md` (keep only README.md)

- [ ] Update `.bin/STANDARDS.md` script audit table with final status

---

## Final Directory Structure (After Cleanup)

```
.bin/
├── README.md                      # Main index
├── STANDARDS.md                   # Documentation standards
├── SCRIPTS_README.md              # Stat icons documentation (legacy)
│
├── regen_gauges.py               # PRIMARY: Gauge generation
├── regen_gauges.md               # Documentation
│
├── generate_stat_icons.py         # PRIMARY: Icon generation
├── add_abbreviations_to_textures.py
├── validate_stat_icons.py
│
├── fix_tga_files.py              # UTILITY: TGA format fixing
│
├── [options_*.py scripts]         # OPTIONAL: If still used
│
└── archive/
    ├── [legacy scripts]
    └── [superseded scripts]
```

---

## Questions for You

1. **Do you use any of these `options_*.py` scripts?**
   - `options_default_sync.py`
   - `options_generate_readme.py`
   - `options_duplicate_detector.py`
   - `options_fix_readme.py`
   - `options_readme_checker.py`
   
   → If no: Move all 5 to archive  
   → If yes: Tell me which ones and I'll document them

2. **Are the push/tag scripts ever used?** (They're hardcoded to v0.4.0)

3. **Should we create a generic tag-push script** for future releases, or is that handled through GitHub web interface?

---

## Next Steps (After You Confirm)

Once you confirm which `options_*` scripts are needed:

1. Move legacy/duplicate scripts to archive/
2. Update .bin/STANDARDS.md with final audit
3. If options_* are needed, create group documentation
4. Clean commit: "chore(.bin): Audit and cleanup, move legacy scripts to archive"

