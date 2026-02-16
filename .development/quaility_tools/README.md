# Quality Tools Roadmap

This directory captures a proposed **quality toolchain** for Thorne UI, including
linting, formatting, link checks, spell checking, and XML validation. It’s
intentionally scoped as **planning**, so you can decide when/how to adopt it
(e.g., during v0.7.0 or a dedicated follow‑up branch).

## Goals

- **Catch broken links** in Markdown before they land.
- **Standardize Python quality** (lint, format, type checks).
- **Validate XML** for well‑formedness (and optionally deeper rules).
- **Provide consistent, repeatable checks** (local + CI + pre‑commit).

## What’s already included

- **`.bin/scan_links.py`** — scans all `.md` files, reports broken links, and can
   apply safe fixes when a unique target is found.
  - Default report output: `.tmp/scan_links.json`

## Current decisions (February 2026)

- **Toolchain**: Mixed Python + Node.
- **Line length**: 180 characters.
- **Spellcheck**: Enabled via CSpell.
- **XML validation**: Well‑formedness only.

## Baseline configs now in place

- **`pyproject.toml`** — Ruff line length and formatting config.
- **`requirements-dev.txt`** — Python tooling dependencies
   (`ruff`, `lxml`, `pymarkdownlnt`, `yamllint`, `pre-commit`).
- **`package.json`** — Node tooling dependencies (`markdownlint-cli2`, `cspell`, `pyright`).
- **`.cspell.json`** — spelling config and dictionary.
- **`.pre-commit-config.yaml`** — pre‑commit hooks (ruff, markdownlint,
  scan_links, XML validation; cspell on manual stage).
- **`.bin/validate_xml.py`** — XML well‑formedness checker with JSON report output.

## What’s proposed (high‑level)

- **Markdown**: lint and formatting checks
- **Python**: `ruff` (lint + format), optional `mypy` or `pyright` for type checking
- **XML**: well‑formedness validation; optional schema or rule-based checks
- **Spelling**: `cspell`
- **YAML/JSON**: basic validation for config files
- **Pre‑commit**: easy opt‑in “run before commit” guardrail
- **CI**: GitHub Actions job to enforce checks on PRs

## Documents in this folder

- **TOOLING-STACK.md** — suggested tools and what each one does
- **PRE-COMMIT.md** — pre‑commit strategy and staged rollout
- **VSCODE-EXTENSIONS.md** — recommended editor extensions
- **AGENT-INSTRUCTIONS.md** — suggested guidance for agent instructions

## Suggested adoption plan

1. **Minimal (low risk)**
   - Add `scan_links.py` to workflow.
   - Run manually before doc-heavy changes.

2. **Standard (team-ready)**
   - Add `ruff` for Python lint/format.
   - Add Markdown linter (Markdownlint or PyMarkdown).
   - Add XML well‑formedness checker (lxml or xmllint).

3. **Full (CI + pre‑commit)**
   - Pre‑commit hooks to enforce a clean baseline.
   - CI workflow that runs on PRs.
   - Spell checking for docs.

---

Maintainer: Draknare Thorne
