# Options Sync System - Operations Guide

**Last Updated**: February 3, 2026  
**Maintainer**: Draknare Thorne  
**Scope**: Long-term operational procedures (6-8 months+)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Team Roles](#team-roles)
3. [Daily Operations](#daily-operations)
4. [Pre-Release Checklist](#pre-release-checklist)
5. [Maintenance Tasks](#maintenance-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Scripts Reference](#scripts-reference)
8. [Common Workflows](#common-workflows)

---

## Introduction

The Options Sync System manages 13 core UI windows across the Thorne UI repository with:
- **46 README files** (1 root index + 4 window navigation files + 41 variant documentations)
- **3 backup systems** (Thorne/ directories with .sync-status.json metadata)
- **4 Python scripts** for validation, synchronization, and error detection
- **Automated reports** for tracking documentation quality and variant redundancy

This guide covers how to use, maintain, and scale the system for the next 6-8 months.

---

## Team Roles

### UI Developer
**Primary Tools**: `options_thorne_sync.py`, `options_generate_readme.py`

**Responsibilities**:
1. Modify window XML files in `thorne_drak/EQUI_*.xml`
2. Sync changes to backups when ready to commit
3. Create variant directories when needed
4. Add basic README placeholders for new variants

**Daily Workflow**:
```bash
# Edit your window file
nano thorne_drak/EQUI_TargetWindow.xml

# Sync to backup when ready
python .bin/options_thorne_sync.py --window Target

# Commit both main and backup
git add thorne_drak/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/Thorne/
git commit -m "fix(target): Update target window layout"
```

### Documentation Reviewer
**Primary Tools**: `options_readme_checker.py`

**Responsibilities**:
1. Monitor documentation quality with regular checker runs
2. Expand skeletal READMEs with detailed technical content
3. Ensure file references and metadata are correct
4. Validate XML matches documentation claims

**Weekly Task**:
```bash
# Check status
python .bin/options_readme_checker.py

# Track improvements over time
# Save reports weekly to track progress
```

### Release Manager
**Primary Tools**: All scripts

**Responsibilities**:
1. Pre-release validation (sync all + check all)
2. Duplicate detection and cleanup
3. Final documentation audit
4. Coordinate fixes before release

**Pre-Release Tasks** (see [Pre-Release Checklist](#pre-release-checklist))

---

## Daily Operations

### Task 1: Modify a Window File

**Scenario**: You've updated `EQUI_TargetWindow.xml` in `thorne_drak/`

```bash
cd /d C:\TAKP\uifiles

# 1. Edit the window file
# (make your changes in the XML)

# 2. Sync to Thorne backup
python .bin/options_thorne_sync.py --window Target --verbose

# 3. Expected output:
# [SYNC] Target: Copying EQUI_TargetWindow.xml...
# [SYNC] Target: Updated .sync-status.json
# Files Modified: 1

# 4. Stage and commit
git add thorne_drak/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/.sync-status.json
git commit -m "fix(target): Update gauge styling"
```

**What Happens**:
- `.bin/options_thorne_sync.py` copies modified file to `Options/Target/Thorne/`
- Updates `.sync-status.json` with current date and git commit hash
- Sets `in_sync: true` flag
- Creates JSON report in `.reports/sync_report.json`

**Verification**:
```bash
# Check that files match (should show identical)
git diff --stat thorne_drak/EQUI_TargetWindow.xml thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml
# (no output = files identical ✓)
```

---

### Task 2: Check Documentation Status

**Scenario**: Weekly documentation health check

```bash
cd /d C:\TAKP\uifiles

# Quick overview
python .bin/options_readme_checker.py

# Expected output shows:
# - Orphaned/Improper: 0
# - Format/Content Issues: [number to fix]
# - Properly Documented: [number complete]
# - Total: 46 files
```

**What to Look For**:
- Format/Content Issues should stay low
- Properly Documented should gradually increase
- No orphaned files should appear
- Missing XML count should stay at 0 (or be resolved)

**Detailed Review** (for documentation specialists):
```bash
# Verbose output shows file-by-file status
python .bin/options_readme_checker.py --verbose

# Save report for tracking
python .bin/options_readme_checker.py > weekly_status_$(date +%Y%m%d).txt
```

---

### Task 3: Create a New Window Variant

**Scenario**: You want to create a new Player window variant with custom layout

```bash
cd /d C:\TAKP\uifiles

# 1. Create variant directory
mkdir "thorne_drak/Options/Player/Custom AA Layout"

# 2. Copy the base window file
copy thorne_drak/EQUI_PlayerWindow.xml "thorne_drak/Options/Player/Custom AA Layout/EQUI_PlayerWindow.xml"

# 3. Edit the variant
# (make your customizations to the variant file)

# 4. Generate skeletal README
python .bin/options_generate_readme.py --window Player --variant "Custom AA Layout" --xml EQUI_PlayerWindow.xml

# Expected output:
# [CREATE] Player/Custom AA Layout/README.md
# Created skeleton with required metadata and sections

# 5. Expand documentation (optional, for detailed docs)
# - Edit the newly created README.md
# - Add more comprehensive descriptions
# - Include layout diagrams if needed

# 6. Verify structure
python .bin/options_readme_checker.py | grep "Custom AA"
# Should show as "Properly Documented" or "Needs Deep Analysis"

# 7. Commit
git add "thorne_drak/Options/Player/Custom AA Layout/"
git commit -m "feat(player): Add Custom AA Layout variant"
```

---

## Pre-Release Checklist

**Timing**: Run 1-2 weeks before release  
**Estimated Duration**: 30-45 minutes  
**Required**: Release Manager access

### Step 1: Synchronize All Windows (15 min)

```bash
cd /d C:\TAKP\uifiles

# Preview changes without modifying
python .bin/options_thorne_sync.py --all --dry-run

# Example output:
# [DRY-RUN] Would sync: Target
# [DRY-RUN] Would sync: Player
# [DRY-RUN] Already synced: Actions
# ...

# If happy with preview, apply for real
python .bin/options_thorne_sync.py --all --verbose

# Save report
copy .reports\sync_report.json .reports\sync_report_prerelease_v0.7.0.json
```

### Step 2: Documentation Audit (15 min)

```bash
# Full documentation check
python .bin/options_readme_checker.py --verbose > .tmp/documentation_audit_prerelease.txt

# Review output:
# - Any FORMAT/CONTENT ISSUES? Fix before release
# - Any orphaned files? Investigate and resolve
# - PROPERLY DOCUMENTED count should be high (>20)
```

### Step 3: Duplicate Detection (10 min)

```bash
# Find and report near-duplicates
python .bin/options_duplicate_detector.py --verbose

# Expected output shows:
# [ANALYSIS] Comparing variant XML files
# [DUPLICATE] Variants with >95% match rate

# Review candidates, optionally remove:
python .bin/options_duplicate_detector.py --remove-candidates --dry-run

# If approved, apply:
python .bin/options_duplicate_detector.py --remove-candidates --verbose
```

### Step 4: Final Sign-Off

```bash
# Create release notes section
cat > .tmp/v0.7.0_OPTIONS_STATUS.md << EOF
# Options Sync Status - v0.7.0
Generated: $(date)
Sync Files: All 13 windows synchronized
Documentation: [X] Complete (24/24 properly documented)
Duplicates: [X] None found
Ready for Release: [X] YES
EOF

git add .reports/sync_report_prerelease_v0.7.0.json
git add .tmp/documentation_audit_prerelease.txt
git add .tmp/v0.7.0_OPTIONS_STATUS.md
git commit -m "chore(release): Pre-release options sync validation"
```

---

## Maintenance Tasks

### Weekly (30 minutes)
1. **Documentation Health Check**
   ```bash
   python .bin/options_readme_checker.py
   # Track trend of format/content issues
   ```

2. **Sync Status Review**
   ```bash
   # Check if any windows are out of sync
   python .bin/options_thorne_sync.py --all --dry-run
   # Should show "Already synced" for all
   ```

### Monthly (1-2 hours)
1. **Expand Skeletal Documentation**
   - Pick 1-2 files from "Needs Deep Analysis" category
   - Read the actual XML file
   - Expand README with detailed technical content
   - Example files for next month: Player/Standard, Target/Standard

2. **Update Maintenance Logs**
   ```bash
   # Create monthly status report
  python .bin/options_readme_checker.py --verbose > .tmp/monthly_status_$(date +%Y%m).txt
   
   # Commit to repository
  git add .tmp/monthly_status_*.txt
   git commit -m "docs(options): Monthly documentation status $(date +%Y-%m)"
   ```

### Quarterly (4-6 hours)
1. **Deep Archive Review**
   - Review `.archive/` directory
   - Identify unused variants for removal
   - Clean up redundant XML files

2. **Script Performance Review**
   - Check `.reports/` directory for error patterns
   - Optimize scripts if issues found
   - Update documentation if workflows changed

---

## Troubleshooting

### Issue 1: File Not Syncing

**Problem**: `options_thorne_sync.py` says "Already synced" but files are different

**Solution**:
```bash
# 1. Verify the actual difference
diff thorne_drak/EQUI_TargetWindow.xml thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml

# 2. Force resync
python .bin/options_thorne_sync.py --window Target --verbose --force

# 3. Check sync status metadata
cat thorne_drak/Options/Target/.sync-status.json | grep in_sync
# Should show "true" after successful sync
```

### Issue 2: README Checker Reports Format Issue

**Problem**: Checker says file reference is broken but it looks correct

**Solution**:
```bash
# Run with verbose to see exact issue
python .bin/options_readme_checker.py --verbose | grep -A 2 "YourFile"

# Common issues:
# 1. Path uses full ../../../ instead of ./
# 2. Missing markdown link syntax []()
# 3. Filename doesn't match actual EQUI_*.xml in directory

# Fix with auto-closer:
python .bin/options_fix_readme.py --window YourWindow

# Or manually edit the README line that should be:
# **File**: [EQUI_WindowName.xml](./EQUI_WindowName.xml)
```

### Issue 3: Sync Status Metadata Corrupted

**Problem**: `.sync-status.json` has invalid JSON

**Solution**:
```bash
# Check JSON validity
python -m json.tool thorne_drak/Options/Target/.sync-status.json

# If invalid, regenerate it
python .bin/options_thorne_sync.py --window Target --force --verbose

# Or manually recreate with this template:
cat > thorne_drak/Options/Target/.sync-status.json << EOF
{
  "window": "Target",
  "filename": "EQUI_TargetWindow.xml",
  "description": "Target window Thorne configuration",
  "last_sync_date": "$(date -u +'%Y-%m-%dT%H:%M:%S.000000')",
  "last_sync_commit": "$(git rev-parse --short HEAD)",
  "in_sync": true
}
EOF

# Verify
python .bin/options_thorne_sync.py --window Target --dry-run
```

### Issue 4: Too Many Format Issues to Fix Manually

**Problem**: 8+ files have format issues and need quick fixing

**Solution**: Use the auto-fix script
```bash
# Dry-run preview
python .bin/options_fix_readme.py --dry-run --verbose

# Apply fixes
python .bin/options_fix_readme.py --verbose

# Verify results
python .bin/options_readme_checker.py
```

---

## Scripts Reference

### `options_thorne_sync.py`

**Location**: `.bin/options_thorne_sync.py`

**Purpose**: Backup working window files and update metadata

**Commands**:
```bash
# Sync single window
python .bin/options_thorne_sync.py --window Target

# Sync all 13 configured windows
python .bin/options_thorne_sync.py --all

# Dry-run preview
python .bin/options_thorne_sync.py --all --dry-run

# Verbose output with file details
python .bin/options_thorne_sync.py --all --verbose

# Force resync even if already matching
python .bin/options_thorne_sync.py --window Target --force
```

**Output**: `.reports/sync_report.json` with:
- Sync status per window (synced, skipped, error)
- File sizes and modification times
- Metadata updates applied
- Any warnings or issues

---

### `options_readme_checker.py`

**Location**: `.bin/options_readme_checker.py`

**Purpose**: Validate README quality and detect issues

**Commands**:
```bash
# Basic summary
python .bin/options_readme_checker.py

# Detailed output with all file info
python .bin/options_readme_checker.py --verbose

# Save to file for archiving
python .bin/options_readme_checker.py --verbose > status.txt

# Check specific window only
python .bin/options_readme_checker.py --window Player
```

**Output**: 
- Console summary with issue counts
- Detailed categorized listing
- `.reports/readme_check_report.json` with full details

**Categories**:
- **Orphaned/Improper**: Files without matching XML
- **Format/Content Issues**: Metadata/syntax problems (actionable)
- **Needs Deep Analysis**: Good structure but sparse content
- **Properly Documented**: Complete and ready
- **Out of Sync**: Should not normally occur
- **No XML Found**: README without matching window file

---

### `options_fix_readme.py`

**Location**: `.bin/options_fix_readme.py`

**Purpose**: Auto-correct common README formatting issues

**Commands**:
```bash
# Preview changes
python .bin/options_fix_readme.py --dry-run

# Apply fixes
python .bin/options_fix_readme.py

# Verbose output showing what was fixed
python .bin/options_fix_readme.py --verbose --dry-run

# Fix single window
python .bin/options_fix_readme.py --window Player --verbose
```

**Fixes Applied**:
- File references: `../../../file` → `[file.xml](./file.xml)`
- Title formatting: Extracts variant names from paths
- Metadata ordering: Standardizes field order
- Author field: Ensures "Draknare Thorne" present
- Date format: Converts to YYYY-MM-DD
- Duplicate separators: Removes extra `---` lines

---

### `options_generate_readme.py`

**Location**: `.bin/options_generate_readme.py`

**Purpose**: Create boilerplate README for new variants

**Commands**:
```bash
# Create skeleton for new variant
python .bin/options_generate_readme.py --window Player --variant "Custom Layout" --xml EQUI_PlayerWindow.xml

# List available windows
python .bin/options_generate_readme.py --list-windows

# Dry-run preview
python .bin/options_generate_readme.py --window Player --variant "Test" --xml EQUI_PlayerWindow.xml --dry-run
```

**Generated Content**:
- Header with metadata fields
- Purpose section (empty for expansion)
- Key Features section (empty list)
- Specifications section (empty table)
- Layout diagrams (empty)
- Ready for human expansion

---

## Common Workflows

### Workflow 1: Quick Hotfix Before Release

**Scenario**: Found a bug 2 days before release, need to ship fix

```bash
# 1. Make the fix
nano thorne_drak/EQUI_TargetWindow.xml
# (edit the bug fix)

# 2. Sync backup
python .bin/options_thorne_sync.py --window Target

# 3. Commit
git add thorne_drak/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/Thorne/EQUI_TargetWindow.xml
git add thorne_drak/Options/Target/.sync-status.json
git commit -m "hotfix(target): Fix gauge rendering issue"

# 4. Run final check
python .bin/options_readme_checker.py | grep Target
# (verify no documentation issues introduced)
```

---

### Workflow 2: Consolidate Duplicate Variants

**Scenario**: "Player Tall" and "Player Tall Gauges" are 95% identical

```bash
# 1. Detect duplicates
python .bin/options_duplicate_detector.py --verbose

# Expected output:
# [DUPLICATE] Player/Tall (95% match with Player/Tall Gauges)

# 2. Manually review both:
diff "thorne_drak/Options/Player/Tall/EQUI_PlayerWindow.xml" \
     "thorne_drak/Options/Player/Tall Gauges/EQUI_PlayerWindow.xml"

# 3. Decide: keep one, delete the other (or merge changes)

# 4. Remove the redundant variant:
rm -r "thorne_drak/Options/Player/Tall"

# 5. Verify with checker
python .bin/options_readme_checker.py | grep "Player/"
# (verify count decreased)

# 6. Commit deletion
git rm -r "thorne_drak/Options/Player/Tall"
git commit -m "refactor(player): Remove duplicate Tall variant"
```

---

### Workflow 3: Quarterly Documentation Expansion

**Scenario**: Pick 2 files from "Needs Deep Analysis" and improve them

```bash
# 1. Identify candidates
python .bin/options_readme_checker.py --verbose | grep "NEEDS DEEP" -A 30

# 2. Pick one file, e.g., Player/Standard
# 3. Read the actual XML to understand the structure
code thorne_drak/Options/Player/Standard/EQUI_PlayerWindow.xml
# (study the XML while README is in split view)

# 4. Improve the README with detailed analysis:
code "thorne_drak/Options/Player/Standard/README.md"
# (add detailed sections, fix sparse areas)

# 5. Run checker to verify improvements
python .bin/options_readme_checker.py --verbose | grep "Player/Standard"

# 6. Commit
git add "thorne_drak/Options/Player/Standard/README.md"
git commit -m "docs(player): Expand Standard variant documentation"

# 7. Repeat with another file
```

---

## Key Statistics to Track

Add these to your monthly reports to monitor system health:

```
Month: YYYY-MM
Date: YYYY-MM-DD
Maintainer: [Name]

Windows: 13 total
  - All 13 configured: ✓

Files: 46 total
  - Root index: 1
  - Window navigation: 13
  - Variant documentation: 32

Documentation Status:
  - Properly Documented: [X]/46
  - Needs Deep Analysis: [X]/46
  - Format/Content Issues: [X]/46
  - Orphaned Files: [X]/46
  - Missing XML: [X]/46

Sync Status:
  - All Windows In Sync: [yes/no]
  - Last Full Sync: YYYY-MM-DD
  - Files Since Last Sync: [count]

Duplicates:
  - Total Found: [count]
  - High Match (>95%): [count]
  - Candidates for Removal: [count]

Action Items Next Month:
  1. [task]
  2. [task]
  3. [task]
```

---

**End of Operations Guide**
