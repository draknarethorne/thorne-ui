# GitHub Automation for Thorne UI

Maintainer: Draknare Thorne

This guide explains the repository automation scaffold for issue tracking, PR hygiene, and project intake.

## What was added

- **Issue forms** in `.github/ISSUE_TEMPLATE/`
  - `bug-report.yml`
  - `ui-testing-finding.yml`
  - `feature-request.yml`
  - `config.yml` (disables blank issues)
- **Workflow enforcement**
  - `.github/workflows/issue-governance.yml`
    - Requires linked issue references in PR bodies
    - Auto-labels issues based on form/title/body content
  - `.github/workflows/project-intake.yml`
    - Auto-adds new issues/PRs to your GitHub Project (when configured)
  - `.github/workflows/quick-issue-command.yml`
    - Supports `/issue <summary>` in issue/PR comments to auto-create tracking issues
  - `.github/workflows/label-sync.yml`
    - Syncs repository labels from `.github/labels.yml`
  - `.github/workflows/issue-triage-comment.yml`
    - Posts one triage helper comment on newly opened/reopened issues with suggested labels

- **Label source of truth**
  - `.github/labels.yml`
    - Canonical label names, colors, and descriptions

## Branch protection (recommended)

Enable branch protection on `main` and require this status check:

- `Issue Governance / pr-linked-issue-check`

This enforces issue linkage before merge.

## Required setup for project auto-intake

In GitHub repository settings:

1. Add repository **Variable**:
   - `PROJECT_URL` = full URL to your GitHub Project (v2)

2. Add repository **Secret**:
   - `ADD_TO_PROJECT_PAT` = Personal Access Token with scopes:
     - `repo`
     - `project`

Without these, the workflow prints setup guidance and exits safely.

## Suggested label taxonomy

Labels are now managed by `.github/labels.yml` and synced automatically.

Manual edits are possible in GitHub UI, but the next sync run will restore the canonical values for any labels defined in the file.

Current canonical groups include:

- Core: `bug`, `enhancement`, `testing`, `needs-triage`
- Priority: `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- UI scope: `ui:*` labels for major windows/components
- Maintenance: `automation`, `docs`

### Label sync behavior

- Triggered on:
  - manual run (`workflow_dispatch`)
  - push to `.github/labels.yml` or workflow file
  - weekly schedule (Monday, 13:00 UTC)
- Uses `skip-delete: true` to avoid deleting unmanaged custom labels.

## Fast testing workflow

1. During playtesting, file a **UI testing finding** issue (quick form) or write `/issue <finding summary>` in a PR/issue comment to auto-create one.
2. When reproducible, convert/expand to **Bug report**.
3. Open PR using `Closes #<issue>` in body.
4. Merge: issue auto-closes and traceability is preserved.

## Triage commenter recommendation

Recommended: **enabled**. It is advisory (comment-only), not blocking.

Behavior:

- Triggers on issue `opened` and `reopened`
- Posts one comment with suggested labels (priority + UI scope + type)
- Avoids duplicate triage comments using an internal marker

Why this helps:

- Gives immediate triage direction during fast playtesting cycles
- Reduces manual label guesswork
- Pairs well with issue forms and auto-labeling workflow

## GitHub Agents (Copilot coding agent) for this repo

GitHub's coding agent can take an issue and produce a PR with implementation.
Best use cases in this project:

- XML standardization across multiple windows
- repetitive option sync metadata updates
- documentation/README consistency sweeps
- low-risk refactors in `.bin/` scripts

Recommended safety pattern:

1. Use clear issue acceptance criteria
2. Require PR issue linkage and checklist completion
3. Keep XML validation and in-game testing as human gate
4. Request human review before merge

Agent-friendly issue template tips:

- Include exact files/windows
- Include expected visual result
- Include EQType constraints and references to `.docs/STANDARDS.md`
- Include test commands (`/loadskin thorne_dev 1`)
