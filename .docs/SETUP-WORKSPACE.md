# Workspace Setup

This guide covers setting up the Thorne UI workspace for running scripts and
quality tools (Python + Node).

## Prerequisites

- **Python 3.13+** (configured to use `.venv`)
- **Node.js 20+** (includes `npm`)

## 1) Python environment

Create or activate the virtual environment, then install dev tools:

- `requirements-dev.txt` contains all Python tooling and script dependencies.

## 2) Node tooling

Install Node-based tools for Markdown linting, spellcheck, and type checking:

- `package.json` contains devDependencies for `markdownlint-cli2`, `cspell`, and
  `pyright`.

### Installing Node.js on Windows

**Option A (recommended):** Official LTS installer

1. Download the LTS installer: https://nodejs.org/en/download/
2. Run the installer (keep defaults — it installs Node.js + npm).
3. Close and reopen your terminal so PATH updates.
4. Verify with `node --version` and `npm --version`.

**Option B:** winget

- `winget install OpenJS.NodeJS.LTS`
- Restart your terminal, then verify versions as above.

## 3) Pre-commit (optional but recommended)

Install git hooks once per clone:

- `pre-commit install`

You can run a manual spellcheck with:

- `pre-commit run cspell --all-files`

## Common tool commands

### Markdown links

- `python .bin/scan_links.py`
- Report: `.tmp/scan_links.json`

### XML well-formedness

- `python .bin/validate_xml.py --report .tmp/xml_wellformed.json`

### Ruff

- `ruff check .`
- `ruff format .`

### Markdown lint

- `npm run lint:md`

### Spellcheck

- `npm run spell`

### Type checking (optional)

- `npm run typecheck`

## Troubleshooting

- **`npm` not found**: Install Node.js from https://nodejs.org/ and restart your
  terminal.
- **Wrong Python**: Ensure VS Code is using the workspace `.venv` interpreter.
- **Reports location**: All tool outputs should go to `.tmp/` (gitignored).

---

Maintainer: Draknare Thorne
