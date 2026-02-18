# Sync Scripts for Testing

## Overview

The Thorne UI project uses a **development → testing → release** workflow:

- **Development**: `C:\Thorne-UI\thorne_drak\` (version controlled)
- **Testing**: `C:\TAKP\uifiles\thorne_dev\` (deployed test location)
- **Release**: Changes pushed to GitHub, users install via releases

## Sync Scripts

### Full Development Sync

**`sync-thorne-ui.bat`** - Syncs entire thorne_drak to thorne_dev

```bash
.\sync-thorne-ui.bat
```

**When to use:**
- Starting a testing session after major development work
- Want to test the complete current state of thorne_drak
- Need to deploy all recent changes at once

**What it does:**
- Copies all files from `C:\Thorne-UI\thorne_drak\` to `C:\TAKP\uifiles\thorne_dev\`
- Uses robocopy with mirroring (removes extra files in dest)
- Excludes git, backup, and temporary files
- In-game: `/loadskin thorne_dev`

---

### Option Variant Sync

**`sync-option.bat`** - Copy specific Option variant to thorne_dev for testing

```bash
# Sync specific option directly
.\sync-option.bat spellbook/large

# Show all options in category (numbered selection)
.\sync-option.bat spellbook
.\sync-option.bat inventory

# Sync inventory variant
.\sync-option.bat inventory/enhanced
```

**When to use:**
- Testing alternative window configurations (Options variants)
- Comparing different layout options in-game
- Rapid iteration on specific window variant

**What it does:**
- Copies ALL files (.xml, .tga, etc.) from Option directory to thorne_dev **root** (overwrites main files)
- Excludes: .md files (README.md), hidden files, system files
- Example: `Options/Spellbook/Large Icons/EQUI_SpellBookWnd.xml` → `thorne_dev/EQUI_SpellBookWnd.xml`
- Allows testing variants without modifying main thorne_drak files
- In-game: `/loadskin thorne_dev` (loads with option overrides)

**Directory Structure:**
```
thorne_drak/
├── EQUI_SpellBookWnd.xml          ← Main development file
└── Options/
    └── Spellbook/
        ├── Default/
        │   └── EQUI_SpellBookWnd.xml    ← Original EQ layout
        ├── Large Icons/
        │   └── EQUI_SpellBookWnd.xml    ← 4-column variant
        ├── Medium Icons/
        │   └── EQUI_SpellBookWnd.xml    ← 2-column variant
        └── Small Icons/
            └── EQUI_SpellBookWnd.xml    ← Compact variant
```

**Example Usage:**
```bash
# Test Large Icons spellbook
.\sync-option.bat spellbook/large

# In EQ client
/loadskin thorne_dev

# Verify changes, iterate, re-sync
```

---

## Best Practices

### During Development
- ❌ **Don't sync** - Work stays in `C:\Thorne-UI\` until ready to test
- ✅ **Commit regularly** - Version control main development files
- ✅ **XML validation** - Run validation before syncing

### During Active Testing
- ✅ **Sync after each change** - Rapid iteration with immediate in-game feedback
- ✅ **Use sync-option.bat** - Test specific variants without full sync
- ✅ **Document findings** - Note issues discovered during testing

### After Testing
- ✅ **Review changes** - Present modifications for approval
- ✅ **Update documentation** - Document finalchanges and decisions
- ✅ **Commit approved work** - Version control only after testing/approval

### What NOT to Do
- ❌ Don't edit files in `thorne_dev` directly (not version controlled)
- ❌ Don't commit after every sync (sync is for testing, not release)
- ❌ Don't sync before commits (deployment and commits are separate)

---

## Technical Details

### sync-thorne-ui.bat
- Uses robocopy with `/MIR` (mirror)
- Excludes: `.git`, `__pycache__`, `.vscode`, `*.backup_*`, `*.bak`, `*.old`, `*.tmp`
- Copies: All UI files, textures, animations, configurations

### sync-option.bat

- Python script: `.bin/sync_option.py`
- Uses Python's `shutil.copy2` for file copying (preserves metadata)
- Copies ALL files from option directory (excludes .md files only)
- Non-recursive: only files in the option root, not subdirectories
- Overwrites existing files in thorne_dev
- Interactive numbered selection for ambiguous paths

---

## In-Game Testing Commands

```bash
# Load synced UI
/loadskin thorne_dev

# Reload UI after changes (doesn't work for all changes)
/load

# Return to default UI
/loadskin default

# List available UIs
/loadskin
```

---

## Troubleshooting

**Q: Changes don't appear in-game after sync?**
- A: Try `/loadskin default` then `/loadskin thorne_dev`
- Some changes require full client restart

**Q: Sync script reports "no changes"?**
- A: Files already synced, or working in wrong directory

**Q: Option sync copies too many files?**
- A: It copies ALL files from the selected option directory (.xml, .tga, etc.)
- Excludes only .md files, hidden files, and system files

**Q: Lost work after sync?**
- A: Work should be in `C:\Thorne-UI\` (version controlled)
- `thorne_dev` is a deployment target, not source of truth

---

Maintained by: Draknare Thorne
Repository: draknarethorne/thorne-ui
