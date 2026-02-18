# Options Scripts Deep Analysis & Consolidation Recommendations

**Analysis Date:** February 13, 2026

---

## Current Options Scripts (6 total)

### Script Breakdown by Function

#### 1. **options_thorne_compare.py** - Auditor

**Purpose:** Analyzes current state of Options directory

**What it does:**
- Scans all window variants
- Compares each variant to their "Default" baseline
- Identifies which variants are identical to Default (redundant)
- Identifies which variants differ from Default (custom)
- Reports structure consistency

**Output:** Console report + `.reports/options_default_compare.json`

**Typical use case:** "Are we keeping duplicate variants unnecessarily?"

---

#### 2. **options_thorne_sync.py** - Operator

**Purpose:** Backup/sync working files to Options/Thorne/ directory

**What it does:**
- Copies main EQUI_*.xml files from `thorne_drak/` to `Options/[Window]/Thorne/`
- Updates `.sync-status.json` metadata (timestamp, git commit)
- Tracks which windows have been synced and when

**Operations:**
- `--window TARGET` - Sync single window
- `--all` - Sync all 13 windows
- `--dry-run` - Preview changes
- `--verbose` - Detailed output

**Output:** Copies files + metadata JSON

**Typical use case:** "Save current working version as baseline"

---

#### 3. **options_duplicate_detector.py** - Auditor

**Purpose:** Find duplicate and similar variants

**What it does:**
- Scans all window variants
- Calculates MD5 checksums (exact matches)
- Compares file similarity (near-duplicates)
- Suggests consolidation candidates
- Lists variants safe to remove/archive

**Parameters:**
- `--similarity N` - Set threshold (0-100, default 95)
- `--detailed` - Show line-by-line diffs
- `--remove-candidates` - List removal suggestions

**Output:** Console report + identifies redundant variants

**Typical use case:** "Which variants are just copies that we don't need?"

---

#### 4. **options_generate_readme.py** - Operator

**Purpose:** Create skeletal README templates for new variants

**What it does:**
- Generates basic README.md template structure
- Fills in window name, variant name, XML file, date
- Includes placeholder sections for agent to expand

**Output:** New README.md file

**Typical use case:** "I added a new variant, generate starter docs"

---

#### 5. **options_fix_readme.py** - Operator

**Purpose:** Auto-correct mechanical issues in existing READMEs

**What it does:**
- Fixes file path references (thorne_drak/... → [file.xml](./file.xml))
- Standardizes headers and metadata
- Sets Author: Draknare Thorne consistently
- Standardizes date format (YYYY-MM-DD)
- Fixes spacing and formatting

**Operations:**
- `--dry-run` - Preview changes
- `--verbose` - Detailed output
- `--window` - Fix only specific window

**Output:** Modified README files

**Typical use case:** "My READMEs have inconsistent formatting, fix them all"

---

#### 6. **options_readme_checker.py** - Auditor

**Purpose:** Quality audit of README documentation

**What it does:**
- Finds orphaned/improperly placed README files
- Identifies out-of-sync READMEs (older than XML)
- Detects incomplete documentation (<80 lines = skeletal)
- Finds missing READMEs in variant directories
- Checks for format issues (links, headers, sections)
- Identifies files needing deep analysis

**Operations:**
- `--fix` - Auto-move orphaned files
- `--verbose` - Detailed listings

**Output:** Audit report identifying all issues

**Typical use case:** "Are my READMEs in good shape? What needs work?"

---

## Cross-Script Relationship Analysis

```
AUDITORS (Read-only, generate reports):      OPERATORS (Modify files):
├── options_thorne_compare.py               ├── options_thorne_sync.py
├── options_duplicate_detector.py            ├── options_generate_readme.py
└── options_readme_checker.py                └── options_fix_readme.py
```

### Potential Consolidations

#### **Group A: README Management (generate, fix, check)**

Could these 3 be consolidated?

```
Current:
  options_generate_readme.py   → Create template
  options_fix_readme.py        → Fix existing
  options_readme_checker.py    → Audit quality

Proposed merged script: options_readme_manager.py
  python options_readme_manager.py --generate --window Player --variant "Custom"
  python options_readme_manager.py --fix --dry-run
  python options_readme_manager.py --check [--fix]
```

**Verdict:** Possibly consolidatable, but they serve different purposes. Keeping separate might be clearer.

---

#### **Group B: Thorne variant handling (compare, sync)**

Could these be one script with mode flag?

```
Current:
  options_thorne_compare.py   → Analyze current state
  options_thorne_sync.py      → Backup to Thorne/

Proposed merged script: options_default_manager.py
  python options_default_manager.py --compare [--window X]
  python options_default_manager.py --sync --window X
  python options_default_manager.py --sync --all [--dry-run]
```

**Verdict:** Could work, but `sync` is a destructive operation. Keeping separate prevents accidents.

---

#### **Overlap Analysis**

| Comparison | Script A | Script B | Overlap? |
|-----------|----------|----------|----------|
| Compare vs Sync | Read current state | Copy to Default | None - different ops |
| Compare vs Duplicate Detector | Checks vs Default | Finds duplicates | Minor - could inform each other |
| Generate vs Fix README | Creates new | Fixes existing | None - different phases |
| Fix vs Check README | Applies fixes | Audits issues | Moderate - checker could call fixer |
| All Auditors | Report on state | Report on state | Moderate - could be unified report |

---

## Recommendations

### **Keep As-Is** (Clearer workflow)
1. **options_thorne_sync.py** - Dangerous to merge (destructive operation)
2. **options_generate_readme.py** - Specific, single purpose
3. **options_duplicate_detector.py** - Specialized analysis tool

### **Consider Merging** (If used together frequently)

**Options A:** Keep all 5 separate (clear, distinct purposes)

**Options B:** Merge into 3-4
- `options_default_manager.py` - Compare + Sync with careful warnings
- `options_readme_manager.py` - Generate + Fix + Check with subcommands
- Keep: `options_duplicate_detector.py` (specialized analysis)

**Options C:** Create unified wrapper
- `options_tools.py --action [compare|sync|detect-duplicates|readme-generate|readme-fix|readme-check]`

---

## Recommendation: **Keep All 5 Separate**

**Reasons:**
1. **Clarity** - Each script has one clear purpose
2. **Safety** - Sync is destructive, better isolated
3. **Unix philosophy** - Do one thing well
4. **Learning curve** - Easy to understand what each does
5. **Usage** - They're not that frequently combined

**Better approach:** Document each one clearly in README.md so users know what each does.

---

## Documentation Plan for Options Scripts

Since these are specialized but useful, here's how to document them:

### In `.bin/README.md` - Create "Options Management Tools" section:

```markdown
### Options Management Tools

**Purpose:** Manage window variants, defaults, and documentation in the Options/ directory

**Quick Overview Table:**

| Script | Purpose | See: `--help` |
|--------|---------|---------------|
| options_thorne_compare.py | Audit variants vs Default | Analyze current state |
| options_thorne_sync.py | Backup working files to Thorne/ | Sync with metadata tracking |
| options_duplicate_detector.py | Find identical/redundant variants | Identify candidates for removal |
| options_generate_readme.py | Create skeletal README templates | Generate docs for new variants |
| options_fix_readme.py | Auto-fix README formatting | Standardize all documentation |
| options_readme_checker.py | Audit README quality/placement | Identify doc issues |

**Common Workflows:**

1. **Check if my variants are duplicates:**
   ```bash
   python .bin/options_duplicate_detector.py --detailed
   ```

2. **Backup current working files to Options/Default:**
   ```bash
   python .bin/options_thorne_sync.py --all --dry-run
   python .bin/options_thorne_sync.py --all
   ```

3. **Audit README quality:**
   ```bash
   python .bin/options_readme_checker.py --verbose
   ```

4. **Fix README formatting across all variants:**
   ```bash
   python .bin/options_fix_readme.py --dry-run
   python .bin/options_fix_readme.py
   ```

For detailed usage of any script: `python .bin/script_name.py --help`
```

---

## Next Actions

1. **Add --help to all 5 options scripts** (if not already present)
2. **Document in .bin/README.md** with table + example workflows
3. **Update STANDARDS.md** script audit - mark these as "Options Management Group"
4. **Consider creating** `options_scripts.md` if detailed usage needed (probably overkill)

