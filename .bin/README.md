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
- `options_thorne_compare.py` - Show which variants differ from Default
- `options_duplicate_detector.py` - Find identical/redundant variant files
- `options_readme_checker.py` - Validate README documentation quality

**Operators** (modify files, use with care):
- `options_thorne_sync.py` - Backup working files to Thorne/ directory
- `options_generate_readme.py` - Auto-generate README templates for variants
- `options_fix_readme.py` - Auto-fix README formatting and structure

#### Typical Workflow

1. **Audit first** (read-only, safe):
   ```bash
   python .bin/options_thorne_compare.py     # See which files differ
   python .bin/options_duplicate_detector.py  # Find redundant variants
   python .bin/options_readme_checker.py      # Check documentation
   ```

2. **Operate with caution** (modifying):
   ```bash
   python .bin/options_thorne_sync.py        # Backup to Thorne/
   python .bin/options_generate_readme.py     # Create README templates
   python .bin/options_fix_readme.py          # Fix existing READMEs
   ```

#### Running Options Tools

All tools support `--help`:
```bash
python .bin/options_thorne_compare.py --help
python .bin/options_thorne_sync.py --help
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

Syncs entire `thorne_drak/` to `<TAKP>\uifiles\thorne_dev\` for in-game testing.

**Use when:** Testing full UI changes, ready to commit to git

**Don't use when:** Making quick gauge tweaks (use `regen_gauges.py` instead)

---

## Documentation Standards

All scripts follow the pattern defined in [STANDARDS.md](../.docs/STANDARDS.md):

- **Simple scripts**: One-liner + `--help` in README.md
- **Complex scripts**: Individual `.md` file + `--help` in script
- **Tool categories**: Grouped by function with cross-references

---

### Item Data Pipeline

Scripts for extracting EQ item stats from the Quarm SQL dump and generating
class-specific icon recommendations for equipment slot art.

**Run order matters** — each step depends on the previous:

```bash
python .bin/extract_eq_items.py      # Step 1: SQL → .Items/.cache/eq_items.*
python .bin/build_slot_reference.py  # Step 2: CSV → .Items/.cache/slot_icon_reference.*
python .bin/pick_class_icons.py      # Step 3: CSV → .Items/.cache/class_icon_picks.* + HTML
```

- **extract_eq_items.py** — Parses Quarm SQL dump (from `.tmp/`) into item CSV/JSON with stats and dragitem mapping
- **build_slot_reference.py** — Groups items by archetype and slot, counts icon frequency
- **pick_class_icons.py** — Scores icons for 15 individual EQ classes using stat-priority weights, generates visual HTML

**Prerequisite:** Quarm SQL dump in `.tmp/quarm_*.sql` (see [ITEM-DATA-PIPELINE.md](../.development/item_slots/ITEM-DATA-PIPELINE.md))

📖 **For full pipeline documentation, see [.development/item_slots/ITEM-DATA-PIPELINE.md](../.development/item_slots/ITEM-DATA-PIPELINE.md)**

---

## Quick Reference

| Task | Command |
|------|---------|
| Regen all gauges (auto-discover) | `python .bin/regen_gauges.py --all` |
| Regen single gauge + test | `python .bin/regen_gauges.py Thorne` |
| Regen all stat icons | `python .bin/regen_icons.py --all` |
| Regen stat icons with labels | `python .bin/regen_icons.py --all --labels` |
| Extract items from SQL dump | `python .bin/extract_eq_items.py` |
| Build slot icon reference | `python .bin/build_slot_reference.py` |
| Pick class icons + HTML | `python .bin/pick_class_icons.py` |
| Full sync to TAKP | `.\sync-thorne-ui.bat` |
| Fix TGA files | `python .bin/fix_tga_files.py <dir>` |
| Get help | `python .bin/<script>.py --help` |

