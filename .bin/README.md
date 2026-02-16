# Thorne UI Build Scripts

Central index of all build and utility scripts for Thorne UI development.

## Scripts Overview

### Gauge Management

**[regen_gauges.py](regen_gauges.md)** - Gauge texture generation and deployment

- Regenerates tall (120×64) and wide (120×32) gauge textures
- Automatic TGA format fixing (PNG→TGA conversion)
- Smart deployment (copies to thorne_drak/ and thorne_dev/)
- Auto-discover mode (--all) or specific variants

```bash
python .bin/regen_gauges.py --all              # Auto-discover all variants
python .bin/regen_gauges.py Thorne             # Single variant deployment
python .bin/regen_gauges.py Bars Basic Thorne  # Multiple specific variants
python .bin/regen_gauges.py --help             # Usage help
```

📖 **For comprehensive usage guide, see [regen_gauges.md](regen_gauges.md)**

---

### Stat Icon Management

**[regen_icons.py](regen_icons.md)** - Generate stat icon textures with abbreviations and labels

- Auto-discovers icon variants from Options/Icons/
- Extracts icons from gemicon files
- Flexible JSON configuration for icon coordinates
- Abbreviation labels within icons (in-game display)
- Optional text labels next to icons (editing reference)
- Integrated label rendering (no separate tool needed)
- Smart deployment (copies to thorne_drak/ and thorne_dev/)

```bash
python .bin/regen_icons.py --all                      # Auto-discover all variants
python .bin/regen_icons.py Thorne                     # Single variant
python .bin/regen_icons.py Thorne --labels            # With reference labels
python .bin/regen_icons.py Thorne Classic Duxa        # Multiple variants
python .bin/regen_icons.py --help                     # Usage help
```

📖 **For comprehensive usage guide, see [regen_icons.md](regen_icons.md)**

---

### Texture Utilities

**fix_tga_files.py** - Convert mislabeled PNG files to proper TGA format

```bash
python .bin/fix_tga_files.py <directory>     # Fix all .tga files in directory
python .bin/fix_tga_files.py --help          # Show options
```

---

### Options Management Tools

Advanced utilities for managing UI variants in the `Options/` directory. These tools fall into two categories:

**Auditors** (read-only, analyze current state):
- `options_default_compare.py` - Show which variants differ from Default
- `options_duplicate_detector.py` - Find identical/redundant variant files
- `options_readme_checker.py` - Validate README documentation quality

**Operators** (modify files, use with care):
- `options_default_sync.py` - Backup working files to Default/ directory
- `options_generate_readme.py` - Auto-generate README templates for variants
- `options_fix_readme.py` - Auto-fix README formatting and structure

#### Typical Workflow

1. **Audit first** (read-only, safe):
   ```bash
   python .bin/options_default_compare.py     # See which files differ
   python .bin/options_duplicate_detector.py  # Find redundant variants
   python .bin/options_readme_checker.py      # Check documentation
   ```

2. **Operate with caution** (modifying):
   ```bash
   python .bin/options_default_sync.py        # Backup to Default/
   python .bin/options_generate_readme.py     # Create README templates
   python .bin/options_fix_readme.py          # Fix existing READMEs
   ```

#### Running Options Tools

All tools support `--help`:
```bash
python .bin/options_default_compare.py --help
python .bin/options_default_sync.py --help
python .bin/options_duplicate_detector.py --help
python .bin/options_generate_readme.py --help
python .bin/options_fix_readme.py --help
python .bin/options_readme_checker.py --help
```

**Note:** Each tool serves a specific purpose. They are kept separate (not consolidated) for safety and clarity - particularly the destructive `sync` operation.

---

## Batch Deployment

**sync-thorne-ui.bat** - Full UI sync from source to TAKP testing directory

```bash
.\sync-thorne-ui.bat
```

Syncs entire `thorne_drak/` to `C:\TAKP\uifiles\thorne_dev\` for in-game testing.

**Use when:** Testing full UI changes, ready to commit to git

**Don't use when:** Making quick gauge tweaks (use `regen_gauges.py` instead)

---

## Documentation Standards

All scripts follow the pattern defined in [STANDARDS.md](STANDARDS.md):

- **Simple scripts**: One-liner + `--help` in README.md
- **Complex scripts**: Individual `.md` file + `--help` in script
- **Tool categories**: Grouped by function with cross-references

---

## Quick Reference

| Task | Command |
|------|---------|
| Regen all gauges (auto-discover) | `python .bin/regen_gauges.py --all` |
| Regen single gauge + test | `python .bin/regen_gauges.py Thorne` |
| Regen all stat icons | `python .bin/regen_icons.py --all` |
| Regen stat icons with labels | `python .bin/regen_icons.py --all --labels` |
| Full sync to TAKP | `.\sync-thorne-ui.bat` |
| Fix TGA files | `python .bin/fix_tga_files.py <dir>` |
| Get help | `python .bin/<script>.py --help` |

