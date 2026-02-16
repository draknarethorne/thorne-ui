# Pre‑commit Strategy (Proposed)

This outlines a staged approach to pre‑commit adoption so the repo can move
toward consistent quality checks without blocking work too early.

## Baseline (current)

The repo now ships a starter `.pre-commit-config.yaml` with:

- **Ruff** lint + format
- **Markdown lint** via `markdownlint-cli2`
- **Markdown link scan** via `.bin/scan_links.py`
- **XML well‑formedness** via `.bin/validate_xml.py`
- **CSpell** (manual stage only)

Line length is set to **180** across Ruff and Markdown linting.

## Phase 1: Optional Hooks (Low Risk)

- Run on demand or locally before commits:
  - `python .bin/scan_links.py`
  - `ruff` (lint + format)

## Phase 2: Default Hooks (Team Ready)

- Add a basic `.pre-commit-config.yaml` with:
  - `ruff` lint
  - `ruff` format
  - Markdown lint
  - XML well‑formedness check (custom or lxml script)

## Phase 3: CI Enforcement

- CI job runs the same hooks on PRs
- Pre‑commit becomes “recommended” for contributors

## Suggested Hook Categories

1. **Docs**
   - scan_links (local path validation)
   - markdownlint or pymarkdown
   - cspell (optional)

2. **Python**
   - ruff (lint + format)
   - pyright or mypy (type check)

3. **XML**
   - lxml-based validation
   - optional rule checks for standards

4. **YAML/JSON**
   - yaml lint
   - json schema validation (if needed)

## Setup Notes

- Install Python tooling from `requirements-dev.txt`.
- Install Node tooling from `package.json`.
- Run `pre-commit install` once per clone to enable hooks.
- Run spellcheck manually with `pre-commit run cspell --all-files`.

---

Maintainer: Draknare Thorne
