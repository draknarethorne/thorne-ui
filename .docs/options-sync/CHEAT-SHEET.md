# Options Sync - Command Cheat Sheet

Quick reference for common tasks. See [OPERATIONS-GUIDE.md](OPERATIONS-GUIDE.md) for detailed explanations.

---

## 📋 Single-Command Tasks

### Check Documentation Status
```bash
python .bin/options_readme_checker.py
```
Shows overall health: issue counts, properly documented files, missing imports.

### Check Detailed Status

### Compare Defaults vs Variants
```bash
python .bin/options_thorne_compare.py
```
Shows which variants are identical to Default (redundant) vs custom (intentional).

### Compare Specific Window
```bash
python .bin/options_thorne_compare.py --window "Inventory"
```
Detailed view of which variants in a window are identical to Default.

```bash
python .bin/options_readme_checker.py --verbose
```
Shows categorized list with each file's status and specific issues.

### Sync a Single Window
```bash
python .bin/options_thorne_sync.py --window Target
```
Backup `EQUI_TargetWindow.xml` to `Options/Target/Thorne/` and update metadata.

### Sync All Windows (Dry-Run)
```bash
python .bin/options_thorne_sync.py --all --dry-run
```
Preview what would sync without making changes.

### Sync All Windows (Apply)
```bash
python .bin/options_thorne_sync.py --all --verbose
```
Sync all 13 windows and show details.

### Auto-Fix Headers (Dry-Run)
```bash
python .bin/options_fix_readme.py --dry-run
```
Preview what would be fixed without making changes.

### Auto-Fix Headers (Apply)
```bash
python .bin/options_fix_readme.py --verbose
```
Fix file references, metadata ordering, dates, authors across all 41 variant READMEs.

### Find Duplicate Variants
```bash
python .bin/options_duplicate_detector.py
```
List all near-duplicate variants (>95% match).

### Create New Variant README
```bash
python .bin/options_generate_readme.py --window Player --variant "My Layout" --xml EQUI_PlayerWindow.xml
```
Generate boilerplate README in `Options/Player/My Layout/README.md`

---

## 🔧 Common Workflows

### Workflow: Made Changes to a Window File

```bash
# 1. Edit the window file
nano thorne_drak/EQUI_TargetWindow.xml

# 2. Backup to Thorne/
python .bin/options_thorne_sync.py --window Target

# 3. Commit
git add thorne_drak/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/Thorne/
git commit -m "fix(target): Update layout"
```

---

### Workflow: Creating a New Variant

```bash
# 1. Make variant directory and copy file
mkdir -p "thorne_drak/Options/Player/New Variant Name"
cp thorne_drak/EQUI_PlayerWindow.xml "thorne_drak/Options/Player/New Variant Name/"

# 2. Edit the variant
nano "thorne_drak/Options/Player/New Variant Name/EQUI_PlayerWindow.xml"

# 3. Create README
python .bin/options_generate_readme.py --window Player --variant "New Variant Name" --xml EQUI_PlayerWindow.xml

# 4. Expand the README with details
nano "thorne_drak/Options/Player/New Variant Name/README.md"

# 5. Commit
git add "thorne_drak/Options/Player/New Variant Name/"
git commit -m "feat(player): Add New Variant Name"
```

---

### Workflow: Pre-Release Validation

```bash
# 1. Sync all windows
python .bin/options_thorne_sync.py --all --verbose

# 2. Check documentation  
python .bin/options_readme_checker.py --verbose

# 3. Find duplicates
python .bin/options_duplicate_detector.py

# 4. Verify no issues
# (fix any issues that appear)

# 5. Commit validation report
git add .reports/
git commit -m "chore(release): Pre-release validation complete"
```

---

### Workflow: Fix Multiple Format Issues

```bash
# 1. See what needs fixing
python .bin/options_readme_checker.py --verbose | grep "FORMAT"

# 2. Auto-fix file references and metadata
python .bin/options_fix_readme.py --verbose

# 3. Verify results
python .bin/options_readme_checker.py

# 4. Commit
git add thorne_drak/Options/
git commit -m "docs(options): Auto-fix README headers and references"
```

---

### Workflow: Expand Sparse Documentation

```bash
# 1. Find sparse files
python .bin/options_readme_checker.py --verbose | grep "NEEDS DEEP"

# 2. Pick one file, e.g., Player/Standard
# 3. Read the XML to understand it
nano thorne_drak/Options/Player/Standard/EQUI_PlayerWindow.xml

# 4. Open README in editor
nano "thorne_drak/Options/Player/Standard/README.md"

# 5. Add more detailed sections:
#    - Expand Purpose from 1 line → full paragraph
#    - Add more Key Features with details
#    - Add Specifications table with X/Y/Width/Height values
#    - Add Style flags, colors, font sizing
#    - Add Layout diagram if helpful

# 6. Verify improved
python .bin/options_readme_checker.py --verbose | grep "Player/Standard"

# 7. Commit
git add "thorne_drak/Options/Player/Standard/README.md"
git commit -m "docs(player): Expand Standard variant documentation"
```

---

### Workflow: Investigate Sync Issue

```bash
# 1. Check what auto-sync says
python .bin/options_thorne_sync.py --window Target --verbose

# 2. Manually compare files
diff thorne_drak/EQUI_TargetWindow.xml thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml

# 3. If they should be same, force resync
python .bin/options_thorne_sync.py --window Target --force --verbose

# 4. Check metadata
cat thorne_drak/Options/Target/.sync-status.json | python -m json.tool

# 5. If metadata corrupted, regenerate
python .bin/options_thorne_sync.py --window Target --force --verbose
```

---

## 📊 Monitoring

### Weekly Check (5 minutes)
```bash
python .bin/options_readme_checker.py
# Just glance at summary - no issues should appear suddenly
```

### Monthly Detailed Audit (15 minutes)
```bash
python .bin/options_readme_checker.py --verbose > .tmp/monthly_status.txt
# Review detailed list, look for trends, pick files to expand
```

### Pre-Release Validation (30 minutes)
```bash
python .bin/options_thorne_sync.py --all --verbose
python .bin/options_readme_checker.py --verbose
python .bin/options_duplicate_detector.py --verbose
# Review all three outputs
```

---

## 🐛 Troubleshooting

### File not syncing?
```bash
# See what script thinks
python .bin/options_thorne_sync.py --window Target --verbose

# Actually check if they match
diff thorne_drak/EQUI_TargetWindow.xml \
     thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml

# Force resync
python .bin/options_thorne_sync.py --window Target --force --verbose
```

### Format issues not auto-fixed?
```bash
# Run the fixer with verbose to see what it finds
python .bin/options_fix_readme.py --dry-run --verbose

# Apply fixes
python .bin/options_fix_readme.py --verbose

# Check result
python .bin/options_readme_checker.py --verbose | grep FORMAT
```

### Checker shows file doesn't exist?
```bash
# Check which files the checker thinks should exist
python .bin/options_readme_checker.py --verbose | grep "No XML Found" -A 5

# Investigate if file really missing or path wrong
ls -la thorne_drak/Options/Target/Player\ and\ Pet\ Gauges/

# If XML truly missing, decide: restore from archive or remove README
```

---

## 📁 File Locations

| Item | Location |
|------|----------|
| Scripts | `.bin/` |
| Documentation | `.docs/options-sync/` |
| Reports | `.reports/` |
| Window files | `thorne_drak/EQUI_*.xml` |
| Variants | `thorne_drak/Options/[Window]/[Variant]/` |
| Backups | `thorne_drak/Options/[Window]/Thorne/` |
| Metadata | `thorne_drak/Options/[Window]/.sync-status.json` |

---

## 📈 Tracking Metrics

Copy & paste these each month to track progress:

```
Date: YYYY-MM-DD
Properly Documented: ___ / 46
Format/Content Issues: ___ / 46
Needs Deep Analysis: ___ / 46
Windows in Sync: ___ / 13
```

---

## 🔐 Important Notes

### Backups Are Sacred
- **Thorne/** directories are your safety net
- Never delete without archive first
- These are committed to git - use them for recovery

### Metadata Tracks Sync State
- `.sync-status.json` is the source of truth
- Last 3 fields reflect when/what was synced
- Corrupted metadata can be regenerated

### README Link Format
Incorrect (use inline code, not links):
```
EQUI_TargetWindow.xml  ❌ (linked to ../../../EQUI_TargetWindow.xml)
EQUI_TargetWindow.xml  ❌ (linked to thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml)
```

Correct (variant README):
```
./EQUI_TargetWindow.xml  ✓
```

---

## 📞 Support

**Questions?** Read detailed docs:
- [OPERATIONS-GUIDE.md](OPERATIONS-GUIDE.md) - Full workflows and explanations
- [README.md](README.md) - System overview and architecture

---

*Last Updated: February 16, 2026*
*Maintained By: Draknare Thorne*
