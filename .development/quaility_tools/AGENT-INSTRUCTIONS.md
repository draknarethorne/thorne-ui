# Agent Quality Check Guidance (Proposed)

These instructions are intended to be embedded into the `.github/agents/*.agent.md` files to ensure agents consistently use the same quality checks.

## Core Expectations

When an agent modifies files:

1. **Run link checks for docs**
   - `python .bin/scan_links.py` (or scoped run)
   - Review `.tmp/scan_links.json`

2. **Run Python lint/format** (if Python changed)
   - `ruff` lint + format

3. **Validate XML** (if XML changed)
   - Well‑formedness check via lxml or xmllint

4. **Record outputs**
   - Keep reports in `.tmp/` when possible

## Suggested Wording for Agent Files

> When you edit Markdown files, run `python .bin/scan_links.py` and ensure any broken links are captured in `.tmp/scan_links.json`.

> When you edit Python files, run `ruff` and fix any issues it reports.

> When you edit XML, validate well‑formedness using the agreed XML checker.

---

Maintainer: Draknare Thorne
