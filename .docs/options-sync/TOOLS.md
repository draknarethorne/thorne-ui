# Options Tools Reference

Complete guide to all 6 tools in the Options management system.

All tools are located in `.bin/options_*.py`

---

## Quick Tool Selector

| Task | Tool | Command |
|------|------|---------|
| Check which variants are identical to Default | options_default_compare | `python .bin/options_default_compare.py` |
| Sync Default variants from main files | options_default_sync | `python .bin/options_default_sync.py --all` |
| Find duplicate/similar files across ALL variants | options_duplicate_detector | `python .bin/options_duplicate_detector.py` |
| Fix README formatting and metadata | options_fix_readme | `python .bin/options_fix_readme.py --dry-run` |
| Create new variant README template | options_generate_readme | `python .bin/options_generate_readme.py --window Player` |
| Audit README quality and sync status | options_readme_checker | `python .bin/options_readme_checker.py` |

---

## 1. options_default_compare.py

**Purpose:** Audit which Options variants are identical to their Default variant.

**Use when:**
- Checking if variants are duplicates of Default (redundant)
- Understanding variant relationships
- Identifying variants that need renaming or removal

**Usage:**
```bash
python .bin/options_default_compare.py
python .bin/options_default_compare.py --window "Inventory"
python .bin/options_default_compare.py --verbose
```

---

## 2. options_default_sync.py

**Purpose:** Synchronize Default variants with current main thorne_drak files.

**Use when:**
- Main window files have been updated
- Backing up current working versions to Options/*/Default/
- Preparing for release

**ALWAYS use --dry-run first!**

**Usage:**
```bash
python .bin/options_default_sync.py --all --dry-run --verbose
python .bin/options_default_sync.py --window "Player"
python .bin/options_default_sync.py --all --verbose
```

---

## 3. options_duplicate_detector.py

**Purpose:** Find duplicate and near-duplicate files across ALL variants.

**Use when:**
- Identifying redundant variants
- Finding similar files
- Consolidating variants before release

**Usage:**
```bash
python .bin/options_duplicate_detector.py
python .bin/options_duplicate_detector.py --similarity 100
python .bin/options_duplicate_detector.py --detailed
```

---

## 4. options_fix_readme.py

**Purpose:** Auto-standardize README.md formatting and metadata.

**Use when:**
- Maintaining consistent README headers
- Fixing file reference paths
- Updating author field
- Standardizing dates

**Use --dry-run first!**

**Usage:**
```bash
python .bin/options_fix_readme.py --dry-run
python .bin/options_fix_readme.py --verbose
python .bin/options_fix_readme.py --window "Inventory"
```

---

## 5. options_generate_readme.py

**Purpose:** Generate skeleton README.md template for new variants.

**Use when:**
- Creating a new variant
- Need consistent README structure

**Usage:**
```bash
python .bin/options_generate_readme.py --window Player --variant "My Custom Layout" --xml EQUI_PlayerWindow.xml
```

---

## 6. options_readme_checker.py

**Purpose:** Audit README.md quality, sync status, and completeness.

**Use when:**
- Checking overall documentation health
- Pre-release audit
- Finding under-documented variants

**Usage:**
```bash
python .bin/options_readme_checker.py
python .bin/options_readme_checker.py --verbose
python .bin/options_readme_checker.py --window "Player"
```

---

## Recommended Workflows

**Daily: Check Documentation Health**
```bash
python .bin/options_readme_checker.py
```

**Before Editing: Understand Relationships**
```bash
python .bin/options_default_compare.py --window "Inventory"
```

**After Main File Changes: Backup to Default**
```bash
python .bin/options_default_sync.py --all --dry-run
python .bin/options_default_sync.py --all --verbose
```

**Cleanup: Find Duplicates**
```bash
python .bin/options_duplicate_detector.py
```

**Consistency: Fix All READMEs**
```bash
python .bin/options_fix_readme.py --dry-run
python .bin/options_fix_readme.py --verbose
```

---

## Related Documentation

- [CHEAT-SHEET.md](CHEAT-SHEET.md) - Quick command reference
- [OPERATIONS-GUIDE.md](OPERATIONS-GUIDE.md) - Complete workflow guide
- [README.md](README.md) - System overview
- [../STANDARDS.md](../STANDARDS.md) - Documentation standards

Maintainer: Draknare Thorne
