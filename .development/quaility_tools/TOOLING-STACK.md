# Tooling Stack Proposal

This document outlines a typical quality toolchain for a mixed
XML/Markdown/Python repository like Thorne UI.

## Chosen defaults (February 2026)

- **Toolchain**: Mixed Python + Node
- **Line length**: 180
- **Markdown lint**: `markdownlint-cli2`
- **Spellcheck**: `cspell`
- **Type checking**: `pyright`
- **XML**: well‑formedness validation only

## Python (Lint + Format + Type Checking)

### Recommended (Python)
- **Ruff** (lint + format) — fast, unified linter + formatter
  - Replaces flake8/black/isort in most setups
- **Type checking (choose one)**
  - **Pyright** (node-based; fast, strong inference)
  - **Mypy** (python-based; stricter with configuration)

### Notes
- Ruff can run in CI and pre‑commit.
- Pyright is typically installed via **npm** or **pipx** (not standard pip), and is
  the same engine behind Pylance.

---

## Markdown (Lint + Format)

### Recommended (Markdown)
- **markdownlint-cli2** (node) — strongest ecosystem, consistent rules
- **OR** **PyMarkdown** (`pymarkdownlnt`) — Python-only alternative

### Optional
- **mdformat** (Python) — autoformatter for Markdown

---

## XML Validation

### Minimal (Well‑formedness)
- **lxml** (Python)
  - Fast parsing and clear errors
  - Easy to script in CI / pre‑commit

### Alternative
- **xmllint** (libxml2) — widely used CLI

### Optional advanced validation
- **xmlschema** (Python) if you want schema validation
- **custom rules** to enforce project-specific structure

---

## Spelling

- **cspell** (node)
  - Works well with Markdown and code
  - Supports custom dictionaries

---

## YAML / JSON

- **yamllint** (Python) or **check-yaml** (pre‑commit)
- **jsonschema** (Python) if structured validation is needed

---

## Link Checking (Docs)

- **`.bin/scan_links.py`** — repo‑aware, path validation
  - Outputs `.tmp/scan_links.json`
  - Includes a `--fix` mode for safe automatic corrections

---

## Typical CI Checks (PR gate)

- `scan_links.py`
- `ruff` (lint + format)
- `pyright` **or** `mypy`
- `markdownlint` (or PyMarkdown)
- XML well‑formedness check
- YAML lint
- optional: cspell

---

## Suggested baseline install set

**Python packages:**
- `ruff`
- `lxml`
- `pymarkdownlnt` (optional)
- `mypy` (optional)
- `yamllint` (optional)

**Node packages:**
- `markdownlint-cli2`
- `pyright`
- `cspell`

---

Maintainer: Draknare Thorne
