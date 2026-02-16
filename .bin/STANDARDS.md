# Script Documentation Standards

Documentation pattern for all build and utility scripts in `.bin/`

---

## Guiding Principles

1. **Discoverability:** User can find what they need without extensive searching
2. **Scalability:** Easy to add new scripts and maintain existing ones
3. **Consistency:** Predictable structure across all scripts
4. **Maintenance:** Clear patterns prevent forgotten or undocumented scripts

---

## Classification

Scripts are classified by complexity:

### ✅ Simple Scripts

**Definition:**
- Single, well-defined purpose
- Few command-line options
- Straightforward setup/execution
- No complex workflows

**Examples:**
- `fix_tga_files.py` - Convert PNG files to TGA format
- `validate_stat_icons.py` - Validate texture files

**Documentation:**
```
Location: .bin/README.md
Format:
    **script_name.py** - Brief description
    
    Quick reference → Command examples
    
    For options: `python .bin/script_name.py --help`
```

### 📖 Complex Scripts

**Definition:**
- Multiple use cases or workflows
- Sophisticated command-line options
- Requires understanding of setup/process
- Important for development workflow

**Examples:**
- `regen_gauges.py` - Gauge texture generation + deployment
- `regen_icons.py` - Icon extraction + processing + abbreviations

**Documentation:**
```
Location: .bin/<script_name>.md
Format:
    1. Overview (purpose, features)
    2. Quick Start (most common workflow)
    3. Usage Patterns (different scenarios)
    4. Command-Line Options (complete reference)
    5. How It Works (technical details)
    6. Troubleshooting (common issues)
```

---

## Template: Simple Script

**In .bin/README.md:**

```markdown
**script_name.py** - One-sentence description

```bash
python .bin/script_name.py <required_arg> [--option]
```

Quick notes if needed. For options:

```bash
python .bin/script_name.py --help
```
```

---

## Template: Complex Script

**Create .bin/script_name.md with structure:**

```markdown
# Script Name (script_name.py)

One-paragraph overview explaining purpose.

## Overview
- Bullet point features
- What it does
- When to use it

## Quick Start
Most common usage example

## Usage Patterns
Alternative workflows

## Command-Line Options
Full reference

## How It Works
Technical implementation details

## Troubleshooting
Common issues and solutions
```

**In .bin/README.md:**

```markdown
**[script_name.py](script_name.md)** - Brief description

- Bullet point features
- Bullet point features

```bash
python .bin/script_name.py <example>
```

📖 **For comprehensive usage guide, see [script_name.md](script_name.md)**
```

---

## Help Text in Scripts

All scripts must support `--help` and `-h` flags:

```python
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print("""
Script Name - Brief description
=============================

USAGE:
    python script.py <required_arg> [optional]
    python script.py --help

EXAMPLES:
    Example 1 command
    Example 2 command

For detailed documentation, see: .bin/script_name.md
        """)
        sys.exit(0)
```

---

## README.md Structure

### For .bin/README.md:

```markdown
# Thorne UI Build Scripts

Index of all scripts

## Scripts Overview

### Category Name

**[script_name.py](script_name.md)** - Description

- Feature bullets
- Feature bullets

```bash
python .bin/script_name.py example
```

📖 **For comprehensive guide, see [script_name.md](script_name.md)**

### Simple Scripts (Section)

Group of simple scripts with brief descriptions in a table.

| Script | Purpose | Quick Command |
|--------|---------|---------------|
| script1.py | Does X | `python .bin/script1.py --help` |
| script2.py | Does Y | `python .bin/script2.py --help` |

```

---

## Script Audit & Documentation Plan

### Current Scripts to Document

| Script | Status | Type | Notes |
|--------|--------|------|-------|
| regen_gauges.py | ✅ **DONE** | Complex | Complete with .md file + --help |
| regen_icons.py | ✅ **DONE** | Complex | Complete with .md file + --help |
| fix_tga_files.py | ⏳ TODO | Simple | Used by regen_gauges.py automatically |
| add_abbreviations_to_textures.py | ⏳ TODO | Simple | Icon utility, consider group with stat icons |
| validate_stat_icons.py | ⏳ TODO | Simple | Icon QA tool, consider group with stat icons |
| **options_*.py (6 scripts)** | ⏳ TODO | Group | See OPTIONS-ANALYSIS.md - kept as separate tools for clarity + safety |
| scripts_readme.md | ✅ **KEEP** | Ref | Stat icons documentation (legacy, keep) |

**Legend:**
- ✅ DONE: Already documented
- ⏳ TODO: Needs documentation
- ✅ KEEP: No changes needed
- **GROUP**: Related scripts that benefit from overview together

### Next Steps

1. **regen_icons.py** (Complex)
    - Keep `.bin/regen_icons.md` in sync with script behavior
    - Ensure `--help` output matches documentation

2. **Simple scripts** (fix_tga_files.py, etc.)
   - Add --help to each
   - Create summary table in .bin/README.md
   - Point to --help for detailed options

3. **Archive scripts**
   - Document in separate "Archive Tools" section
   - Reference from README.md with note: "For reference only"

4. **Batch scripts** (sync-thorne-ui.bat, etc.)
   - Document workflow and when to use
   - Include in main README.md

---

## Maintenance Checklist

- [ ] **New script created?** Add to Script Audit table
- [ ] **Simple script?** Add --help and update README.md
- [ ] **Complex script?** Create .md file, add --help, reference from README.md
- [ ] **Modified script?** Update corresponding .md file
- [ ] **Behavior changed?** Update examples in documentation
- [ ] **New option added?** Document in both --help and .md file

---

## Example: Current State

### ✅ Correctly Documented

**regen_gauges.py**
- Complex script
- Has `.bin/regen_gauges.md` with full documentation
- Has --help in script
- Referenced in `.bin/README.md` with link

### ✅ Correctly Documented (Icons)

**regen_icons.py**
- Complex script
- Has `.bin/regen_icons.md` with full documentation
- Has --help in script
- Referenced in `.bin/README.md` with link

**fix_tga_files.py**
- Exists and works
- **Missing:** --help, documentation in README.md

### Archive

**analyze_gemicons.py, detect_gemicon_grid.py, etc.**
- Tools used for development
- Kept for reference
- Should be listed in "Archive Tools" section of README.md

---

## Quick Reference

**To add a new script:**

1. Is it simple (single purpose, few options)?
   - Yes → Add --help + add to table in README.md
   - No → Create script_name.md + add --help + reference in README.md

2. Add entry to Script Audit table (in this file)

3. Test that `python script.py --help` works

4. Update `.bin/README.md` with appropriate section

5. Commit with clear message mentioning documentation

