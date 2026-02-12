# Options Sync System

## Complete Documentation for Long-Term Maintenance (6-8+ months)

---

## üìö Documentation

**Choose based on your need:**

### Quick Reference

### Tool Reference
- **[TOOLS.md](TOOLS.md)** Ì¥ß Complete guide to all 6 options tools with examples and use cases

- **[CHEAT-SHEET.md](CHEAT-SHEET.md)** ‚≠ê Command reference and common tasks (2 min bookmark this!)

### Complete Operations Guide
- **[OPERATIONS-GUIDE.md](OPERATIONS-GUIDE.md)** üìñ How to run all scripts and operations:
  - All 6 scripts with examples
  - Team workflows and responsibilities
  - Daily/weekly/monthly maintenance tasks
  - Pre-release checklist
  - Troubleshooting guide
  - (30-60 min read)

### This Guide
- Full architecture, directory structure, how the system works, and component details

---

## Overview

The Options Sync System is a comprehensive toolkit for managing UI window variants, backups, documentation, and synchronization across the Thorne UI repository. This system ensures that working window files are properly tracked, documented, and backed up with metadata.

## Purpose

The Options Sync System solves several key challenges:

1. **Version Tracking**: Know which Options variant represents the current working version
2. **Backup Safety**: Maintain `Default/` copies of all finalized window configurations
3. **Documentation Quality**: Track which variants have proper documentation vs. skeletal placeholders
4. **Duplicate Detection**: Identify redundant variants for consolidation
5. **Metadata Management**: Keep sync status, dates, and git commits synchronized

## Directory Structure

```
thorne_drak/
  Options/
    [WindowName]/               # e.g., Target, Player, Group
      .sync-status.json         # Metadata tracking sync status
      Default/                  # Backup of current working configuration
        EQUI_*.xml              # Window file
        README.md               # Documentation (when Default is a variant)
      [VariantName]/            # Custom variants (e.g., "Player Gauges and Weight")
        EQUI_*.xml              # Variant window file
        README.md               # Variant documentation
      [VariantName2]/
        ...
```

### Key Components

#### `.sync-status.json`
Metadata file tracking the synchronization state between main working file and Default backup.

**Structure:**
```json
{
  "window": "Target",
  "filename": "EQUI_TargetWindow.xml",
  "description": "Target window default configuration",
  "last_sync_date": "2026-02-03T22:00:00.000000",
  "last_sync_commit": "ac7a1c4",
  "in_sync": true
}
```

#### `Default/` Directory
Stores the backup copy of the current working window file from `thorne_drak/`. This serves as:
- A known-good backup
- A reference version for comparison
- A sync target for ongoing development

**Important:** `Default/` may or may not contain a README.md depending on whether it's also a usable variant or just a backup copy.

#### Variant Directories
Custom window variations stored in subdirectories with descriptive names. Each should contain:
- The variant XML file
- A comprehensive README.md documenting the variant's purpose, features, and specifications

## Available Tools

All scripts are located in `.bin/` directory and save reports to `.reports/` directory.

### 1. Sync Window to Default

**Script:** `.bin/options_default_sync.py`

**Purpose:** Copy finalized working window files from `thorne_drak/` to their `Options/[Window]/Default/` backup and update metadata.

**Usage:**
```bash
# Sync a specific window
python .bin/options_default_sync.py --window Target

# Sync all 13 configured windows
python .bin/options_default_sync.py --all

# Preview changes without modifying files
python .bin/options_default_sync.py --all --dry-run

# Show detailed file operations
python .bin/options_default_sync.py --window Player --verbose
```

**What it does:**
1. Compares `thorne_drak/EQUI_*.xml` with `Options/[Window]/Default/EQUI_*.xml`
2. If files differ, copies the working file to Default
3. Updates `.sync-status.json` with:
   - Current timestamp
   - Current git commit hash
   - Sets `in_sync: true`
4. Reports skipped (already identical), synced, or error states
5. Saves detailed report to `.reports/sync_report.json`

**When to use:**
- After finalizing changes to a window in `thorne_drak/`
- Before committing window changes
- During release preparation to ensure all backups are current

**Configured Windows (13 total):**
- Actions, Animations, Group, Hotbutton, Inventory
- Loot, Merchant, Pet, Player, Selector
- Skin, Spellbook, Target

---

### 2. Options README Checker

**Script:** `.bin/options_readme_checker.py`

**Purpose:** Audit README.md files across all Options variants for placement issues, sync status, completeness, and documentation depth.

**Usage:**
```bash
# Standard audit
python .bin/options_readme_checker.py

# Show all properly documented variants (verbose)
python .bin/options_readme_checker.py --verbose
```

**What it checks:**

1. **Orphaned/Improperly Placed READMEs**
   - ROOT_LEVEL: README in `Options/[Window]/` parent directory
   - ORPHANED_PARENT: README in variant subdirectory (incorrect structure)

2. **Out of Sync**
   - README.md modification date older than corresponding XML file
   - Indicates documentation hasn't been updated after code changes

3. **Incomplete Documentation**
   - READMEs with < 80 lines (configurable threshold)
   - Missing basic content structure

4. **Needs Deep Analysis** ‚≠ê
   - Properly placed READMEs with matching XML files
   - Line count < 150 lines (likely skeletal/template)
   - Ready for agent to perform detailed technical documentation

5. **Missing XML**
   - README exists but no matching EQUI_*.xml file found
   - Indicates orphaned documentation

**Report Output:**
- Terminal summary with categorized issues
- JSON report saved to `.reports/readme_check_report.json`

**When to use:**
- Before creating detailed documentation to identify which files need work
- After adding new variants to verify proper structure
- As part of quality assurance workflow

---

### 3. Duplicate Detector

**Script:** `.bin/options_duplicate_detector.py`

**Purpose:** Identify functionally identical UI variants across windows to prevent redundancy and storage waste.

**Usage:**
```bash
# Standard duplicate detection
python .bin/options_duplicate_detector.py

# Show removal candidates
python .bin/options_duplicate_detector.py --remove-candidates

# Detailed reporting
python .bin/options_duplicate_detector.py --detailed

# Custom similarity threshold (0-100, default 95%)
python .bin/options_duplicate_detector.py --similarity 90
```

**What it detects:**

1. **Exact Duplicates**
   - Files with identical MD5 checksums
   - Byte-for-byte identical content
   - Clear candidates for consolidation

2. **Similar Variants**
   - Files with >= 95% similarity (configurable)
   - Detected via line-by-line diff analysis
   - May indicate incomplete customizations or duplicates

**Report Output:**
- Terminal summary showing duplicates by window
- Suggested removal candidates (non-Default duplicates)
- JSON report saved to `.reports/duplicate_detection_report.json`

**When to use:**
- Periodically to maintain repository hygiene
- Before releases to reduce distribution size
- When consolidating variants or cleaning up experimental work

---

### 4. Generate Skeletal README

**Script:** `.bin/options_generate_readme.py`

**Purpose:** Create starter README.md templates for new window variants with placeholder sections for agent expansion.

**Usage:**
```bash
# Create new variant README
python .bin/options_generate_readme.py --window Target --variant "Custom Layout"

# Specify XML file explicitly
python .bin/options_generate_readme.py --window Inventory --variant "Large Grid" --xml EQUI_Inventory.xml
```

**What it creates:**
- README.md in `Options/[Window]/[VariantName]/`
- Skeletal template (~33 lines) with sections:
  - Overview
  - Key Features (placeholder list)
  - File Information
  - Description (to be added by agent)
  - Configuration (to be added by agent)
  - Element Specifications (to be added by agent)
  - Usage Notes (to be added by agent)

**When to use:**
- When creating a new window variant
- Before performing detailed documentation work
- As a starting point for variant development

**Follow-up Workflow:**
1. Generate skeletal README
2. Run `options_readme_checker.py` to identify it for deep analysis
3. Agent expands README with detailed technical specifications

---

## Comprehensive Workflow

### Workflow 1: Adding a New Variant

**Scenario:** You've created a custom Player window variant with AA/XP bars at the bottom.

**Steps:**

1. **Create the variant XML file**
   ```bash
   # Copy base file and customize
   cp thorne_drak/EQUI_PlayerWindow.xml thorne_drak/Options/Player/"AA and XP Bottom"/EQUI_PlayerWindow.xml
   # Edit the variant XML with your changes
   ```

2. **Generate skeletal README**
   ```bash
   python .bin/options_generate_readme.py --window Player --variant "AA and XP Bottom" --xml EQUI_PlayerWindow.xml
   ```

3. **Verify structure**
   ```bash
   python .bin/options_readme_checker.py
   ```
   Should show variant in "NEEDS DEEP ANALYSIS" section

4. **Expand with detailed documentation**
   - Agent analyzes the XML file
   - Documents element specifications, layout, features
   - Updates README with comprehensive technical details

5. **Commit the new variant**
   ```bash
   git add thorne_drak/Options/Player/"AA and XP Bottom"/
   git commit -m "feat(player): Add AA and XP Bottom variant"
   ```

---

### Workflow 2: Updating Main Window File

**Scenario:** You've refined the Target window gauge positions in the main working file.

**Steps:**

1. **Make changes to working file**
   ```
   # Edit thorne_drak/EQUI_TargetWindow.xml
   ```

2. **Test changes in-game**
   - Load the UI
   - Verify gauge positions
   - Confirm functionality

3. **Sync to Default backup**
   ```bash
   python .bin/options_default_sync.py --window Target --verbose
   ```
   Output shows:
   ```
   [SYNCED] 1 window(s)
     Target
       thorne_drak/EQUI_TargetWindow.xml -> Options/Target/Default/EQUI_TargetWindow.xml
   ```

4. **Update related variants (if needed)**
   - If changes affect other Target variants, update those manually
   - Or regenerate variants based on new Default

5. **Commit changes**
   ```bash
   git add thorne_drak/EQUI_TargetWindow.xml
   git add thorne_drak/Options/Target/.sync-status.json
   git add thorne_drak/Options/Target/Default/EQUI_TargetWindow.xml
   git commit -m "fix(target): Adjust gauge positions for better alignment"
   ```

---

### Workflow 3: Quality Assurance Before Release

**Scenario:** Preparing for v0.6.0 release and need to ensure all documentation is current.

**Steps:**

1. **Check README status**
   ```bash
   python .bin/options_readme_checker.py --verbose
   ```

2. **Address issues:**
   - **Orphaned READMEs**: Move to proper locations or delete
   - **Out of Sync**: Update documentation to match current XML
   - **Incomplete**: Expand thin documentation
   - **Needs Deep Analysis**: Use agent to create detailed docs

3. **Check for duplicates**
   ```bash
   python .bin/options_duplicate_detector.py --remove-candidates
   ```

4. **Remove/consolidate duplicates:**
   - Verify duplicates are truly identical
   - Keep the best-documented version
   - Remove redundant variants

5. **Sync all windows to Default**
   ```bash
   python .bin/options_default_sync.py --all --verbose
   ```

6. **Verify all backups current:**
   ```bash
   python .bin/options_default_sync.py --all --dry-run
   ```
   Should show all windows skipped (already identical)

7. **Commit cleanup and proceed with release**

---

### Workflow 4: Expanding Skeletal Documentation

**Scenario:** You have a skeletal README identified by the checker that needs detailed technical docs.

**Steps:**

1. **Identify files needing work**
   ```bash
   python .bin/options_readme_checker.py
   ```
   Output shows:
   ```
   [AGENT] NEEDS DEEP DOCUMENTATION ANALYSIS (skeletal/generic)
     Inventory/Large Grid
       -> README.md: 33 lines
          Path: Inventory/Large Grid/README.md
   ```

2. **Feed to agent for expansion**
   ```
   "Analyze thorne_drak/Options/Inventory/Large Grid/EQUI_Inventory.xml
   and expand the skeletal README with detailed technical documentation
   including element specifications, layout details, and comprehensive
   feature descriptions."
   ```

3. **Agent performs analysis:**
   - Reads XML structure
   - Extracts element specifications (positions, sizes, types)
   - Documents unique features
   - Creates comprehensive README (150+ lines)

4. **Verify completion**
   ```bash
   python .bin/options_readme_checker.py
   ```
   File now appears in "PROPERLY DOCUMENTED" section

5. **Commit enhanced documentation**
   ```bash
   git add thorne_drak/Options/Inventory/"Large Grid"/README.md
   git commit -m "docs(inventory): Add comprehensive technical documentation for Large Grid variant"
   ```

---

## Best Practices

### 1. Regular Sync Discipline

**DO:**
- Run sync after finalizing window changes
- Sync before commits involving window files
- Use `--dry-run` to preview changes

**DON'T:**
- Manually copy files between directories
- Skip metadata updates
- Forget to commit `.sync-status.json` changes

### 2. Documentation Standards

**DO:**
- Use skeletal README generator for new variants
- Expand skeletal READMEs with agent-performed analysis
- Aim for 150+ lines for comprehensive documentation
- Include element specifications, layouts, and features

**DON'T:**
- Leave skeletal placeholders indefinitely
- Create variants without documentation
- Mix documentation styles across variants

### 3. Variant Management

**DO:**
- Use descriptive variant names ("AA and XP Bottom", "Large Grid")
- Check for duplicates before creating new variants
- Consolidate redundant variants periodically

**DON'T:**
- Create near-duplicate variants without differentiation
- Use vague names ("Variant1", "Test", "New")
- Keep experimental/abandoned variants without documentation

### 4. Quality Assurance

**DO:**
- Run all three checker scripts before releases
- Address "Needs Deep Analysis" items systematically
- Verify sync status before major changes

**DON'T:**
- Ignore checker warnings
- Skip documentation updates
- Leave orphaned/misplaced files

---

## Metadata Schema Reference

### .sync-status.json

**Location:** `thorne_drak/Options/[WindowName]/.sync-status.json`

**Purpose:** Track synchronization state between working file and Default backup

**Schema:**
```json
{
  "window": "string (window name)",
  "filename": "string (EQUI_*.xml filename)",
  "description": "string (human-readable description)",
  "last_sync_date": "string (ISO 8601 timestamp)",
  "last_sync_commit": "string (git short hash)",
  "in_sync": "boolean (true if synced, false if out of sync)"
}
```

**Example:**
```json
{
  "window": "Target",
  "filename": "EQUI_TargetWindow.xml",
  "description": "Target window default configuration",
  "last_sync_date": "2026-02-03T22:00:00.000000",
  "last_sync_commit": "ac7a1c4",
  "in_sync": true
}
```

**Fields:**
- `window`: Window name matching directory (Actions, Target, Player, etc.)
- `filename`: Exact XML filename being tracked
- `description`: Brief description of what this window does
- `last_sync_date`: ISO 8601 timestamp when last synced
- `last_sync_commit`: Git short commit hash at sync time
- `in_sync`: Boolean indicating if Default matches working file

---

## Report Files

All reports are saved to `.reports/` directory (gitignored).

### sync_report.json

Generated by `options_default_sync.py`

**Structure:**
```json
{
  "timestamp": "ISO 8601 timestamp",
  "git_commit": "short hash",
  "synced": [
    {
      "window": "window name",
      "source": "relative path to source",
      "dest": "relative path to destination",
      "commit": "commit hash"
    }
  ],
  "skipped": [
    {
      "window": "window name",
      "reason": "reason for skip"
    }
  ],
  "errors": [
    {
      "window": "window name",
      "error": "error message"
    }
  ],
  "total_synced": 0
}
```

### readme_check_report.json

Generated by `options_readme_checker.py`

**Structure:**
```json
{
  "orphaned_readmes": [...],
  "out_of_sync": [...],
  "incomplete_docs": [...],
  "missing_readmes": [...],
  "needs_deep_analysis": [...],
  "good_readmes": [...],
  "issues_found": 0,
  "timestamp": "ISO 8601 timestamp"
}
```

### duplicate_detection_report.json

Generated by `options_duplicate_detector.py`

**Structure:**
```json
{
  "scan_timestamp": "ISO 8601 timestamp",
  "windows": {
    "WindowName": {
      "exact_duplicates": [...],
      "similar_groups": [...],
      "total_variants": 0
    }
  },
  "duplicates_found": 0,
  "similar_sets": 0,
  "candidates_for_removal": [...]
}
```

---

## Troubleshooting

### Sync fails with "Source file not found"

**Cause:** Window name doesn't match configured mapping in script

**Solution:** Check available windows with:
```bash
python .bin/options_default_sync.py
```

Use exact name from the list (case-sensitive).

---

### README checker shows everything as orphaned

**Cause:** READMEs are in parent directories instead of variant subdirectories

**Solution:** This is expected if you haven't reorganized yet. The checker is identifying the cleanup needed.

---

### Duplicate detector shows unexpected duplicates

**Cause:** Variants that should differ are actually identical (unfinished customizations)

**Solution:**
1. Review the duplicate report
2. Determine if variant was meant to be different
3. Either complete the variant customization or remove it
4. Update documentation to explain the relationship

---

### Sync shows "already identical" every time

**Cause:** Working file and Default are already in sync (this is good!)

**Solution:** No action needed. This confirms backups are current.

---

## Maintenance

### Monthly Tasks

- [ ] Run duplicate detector
- [ ] Review and consolidate redundant variants
- [ ] Check for skeletal READMEs needing expansion

### Pre-Release Tasks

- [ ] Run README checker
- [ ] Sync all windows to Default
- [ ] Address documentation gaps
- [ ] Verify no orphaned files

### After Major Changes

- [ ] Sync affected windows
- [ ] Update variant documentation if affected
- [ ] Verify related variants still work

---

## Version History

**v1.0.0** (2026-02-03)
- Initial Options Sync System documentation
- Three core scripts: sync, checker, generator
- Dual-purpose Default directory (backup + optional variant)
- Comprehensive workflow documentation

---

## Related Documentation

- [VERSION-MANAGEMENT.md](../VERSION-MANAGEMENT.md) - Version control and release processes
- [STANDARDIZATION-ROADMAP.md](../STANDARDIZATION-ROADMAP.md) - Field naming standards
- [technical/EQTYPES.md](../technical/EQTYPES.md) - EverQuest UI element types reference

---

**Maintainer:** Draknare Thorne
**Repository:** [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)
