# Link Scanner Configuration

The link scanner (`.bin/scan_links.py`) uses `.scan_linksrc.json` for directory exclusion configuration.

## Configuration File

**Location:** `.scan_linksrc.json` (repository root, follows standard config naming like `.eslintrc.json`)

**Example:**
```json
{
  "exclude_dirs": [
    ".git",
    ".tmp",
    "node_modules",
    "default"
  ]
}
```

## excluded_dirs

List of directory names to exclude from scanning. Directories matching any name in this list will be skipped, regardless of where they appear in the file path.

**Default exclusions** (always applied):
- `.git` — Git metadata
- `.tmp` — Temporary build outputs
- `.archive` — Archive directories
- `.reports` — Report outputs  
- `.venv`, `venv` — Python virtual environments
- `__pycache__` — Python cache

**Configured exclusions** (in `.linkscanconfig.json`):
- `node_modules` — NPM dependencies
- `default` — Default EverQuest UI files (reference, not part of Thorne UI)
- `*.code-search` — VS Code search cache

## Running the Scanner

```bash
# Scan all markdown files (respects .linkscanconfig.json)
python .bin/scan_links.py

# Specify custom root directory
python .bin/scan_links.py --root /path/to/repo

# Apply automatic fixes
python .bin/scan_links.py --fix

# Specify output report location
python .bin/scan_links.py --output custom/path/report.json
```

## Output Report

The scanner generates `.tmp/scan_links.json` with:
- Summary statistics (files scanned, links scanned, broken links)
- Detailed list of broken links with file, line number, and suggestions

## How Configuration Priority Works

1. **Load defaults** — Always includes core exclusions
2. **Load config file** — `.scan_linksrc.json` merged with defaults
3. **Apply filtering** — Both sets of exclusions applied during scan

If `.scan_linksrc.json` is missing, the scanner uses defaults only.

## Common Exclusions to Consider

**Development/Build Files:**
```json
{
  "exclude_dirs": [
    "node_modules",
    ".venv",
    "__pycache__",
    "build",
    "dist"
  ]
}
```

**Third-Party UI References:**
```json
{
  "exclude_dirs": [
    "default",
    "duxaUI",
    "Infiniti-Blue",
    "community-ui-variants"
  ]
}
```

**Large Static Directories:**
```json
{
  "exclude_dirs": [
    "assets",
    "media",
    "archives"
  ]
}
```

## Notes

- Exclusions are matched against directory names in the full path
- Pattern matching uses simple string comparison (e.g., `node_modules` matches any directory named `node_modules`)
- For glob patterns, upgrade `.linkscanconfig.json` with `exclude_patterns` field (future feature)
- Configuration is optional — scanner works with defaults if file missing
