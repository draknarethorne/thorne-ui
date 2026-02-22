# Version Management

**Maintainer:** Draknare Thorne  
**Repository:** draknarethorne/thorne-ui

---

## Overview

This project follows **Semantic Versioning (SemVer)** with a simplified approach tailored for UI mod projects.

---

## Version Format

```
MAJOR.MINOR.PATCH
```

**Examples:** `0.6.5`, `1.0.0`, `1.2.3`

### What Each Number Means

- **MAJOR** (e.g., `1.0.0`): Major UI overhaul, breaking changes, or significant redesigns
- **MINOR** (e.g., `0.5.0`): New features, new windows, or significant enhancements
- **PATCH** (e.g., `0.5.1`): Bug fixes, small tweaks, or documentation updates

---

## Version Sources of Truth

### 1. `VERSION` File (Primary Reference)

Located at repository root: `/VERSION`

**Purpose:**
- Single source of truth for current development version
- Machine-readable (one line, plain text)
- Used for validation and automation

**Format:**
```
0.6.5
```

**Rules:**
- NO `v` prefix
- NO newline at end
- ONLY the version number

### 2. Git Tags (Release Markers)

**Format:** `vMAJOR.MINOR.PATCH` (e.g., `v0.6.4`)

**Purpose:**
- Mark specific commits as releases
- Trigger automated release workflows
- Create downloadable release packages

### 3. README.md Version History (Changelog)

**Purpose:**
- Human-readable changelog
- Release notes and feature descriptions
- Historical record of project evolution

---

## Release Workflow

### Step-by-Step Process

#### 1. **Update VERSION File**

```bash
# Example: Updating to v0.6.4
echo "0.6.4" > VERSION
git add VERSION
```

#### 2. **Update README.md Version History**

Add new entry at the **top** of the Version History section:

```markdown
## 📋 Version History

**v0.6.4** (YYYY-MM-DD)
- ✅ Feature 1
- ✅ Feature 2
- ✅ Enhancement 3

**v0.6.3** (February 9, 2026)
...
```

#### 3. **Commit Version Updates**

```bash
git add VERSION README.md
git commit -m "chore(release): Prepare for release v0.6.4"
```

#### 4. **Create Annotated Tag**

```bash
git tag -a v0.6.4 -m "Release v0.6.4: Brief description"
```

#### 5. **Push Tag to Trigger Release**

```bash
git push origin main
git push origin v0.6.4
```

**Result:** GitHub Actions workflow automatically:
- Builds ZIP packages
- Creates GitHub Release
- Generates changelog
- Publishes release assets

---

## Version Validation

### Pre-Release Checks

Before tagging a release, verify:

```bash
# 1. Check current VERSION file
cat VERSION

# 2. Verify it matches intended release
# Should display: 0.6.4 (without 'v' prefix)

# 3. Verify README.md has matching entry
grep "v0.6.4" README.md

# 4. Ensure you're on correct branch
git branch

# 5. Verify no uncommitted changes
git status
```

### Minimal Release File Set (Recommended)

To keep release commits focused and avoid noisy documentation churn:

- **Always update:**
  - `VERSION`
  - `README.md` (Version History)

- **Update only if content actually changed:**
  - `DEVELOPMENT.md`
  - `.docs/VERSION-MANAGEMENT.md`
  - `.docs/releases/*` guides, templates, and index files

This keeps each release commit small, reviewable, and accurate.

---

## Automation & Scripts

### Current Automation

**GitHub Actions Workflow:** `.github/workflows/release.yml`

- **Trigger:** Push of tag matching `v*.*.*`
- **Actions:**
  - Extract version from tag
  - Generate changelog from commits
  - Package `thorne_drak/` as ZIP
  - Create GitHub Release
  - Upload release assets

### Future Enhancements

Potential automation improvements:

1. **Version Validation Script**
   ```bash
   # .bin/validate-version.sh
   # - Check VERSION matches tag
   # - Verify README.md updated
   # - Lint release checklist
   ```

2. **Auto-Increment Script**
   ```bash
   # .bin/bump-version.sh [major|minor|patch]
   # - Update VERSION file
   # - Create placeholder in README
   # - Optionally commit
   ```

3. **Release Prep Script**
   ```bash
   # .bin/prepare-release.sh v0.6.4
   # - Update VERSION
   # - Update README.md template
   # - Run validation
   # - Provide next steps
   ```

---

## Common Scenarios

### Scenario 1: Feature Release (Minor Version)

**Context:** New window added (e.g., Group Window enhancements)

```bash
# Current: v0.6.3 → Target: v0.6.4

# 1. Update VERSION
echo "0.6.4" > VERSION

# 2. Update README.md (add new section at top)
# ... edit manually ...

# 3. Commit and tag
git add VERSION README.md
git commit -m "chore(release): Prepare for release v0.6.4"
git tag -a v0.6.4 -m "Release v0.6.4: Gauge system overhaul"
git push origin main
git push origin v0.6.4
```

### Scenario 2: Bug Fix (Patch Version)

**Context:** Fixed gauge height issue in Loot Window

```bash
# Current: v0.6.4 → Target: v0.6.5

# 1. Update VERSION
echo "0.6.5" > VERSION

# 2. Update README.md
# Add v0.6.5 entry (brief, focused on fix)

# 3. Commit and tag
git add VERSION README.md
git commit -m "chore(release): Prepare for release v0.6.5"
git tag -a v0.6.5 -m "Release v0.6.5: Fix loot window gauge height"
git push origin main
git push origin v0.6.5
```

### Scenario 3: Major Overhaul (Major Version)

**Context:** Complete UI redesign for v1.0.0 release

```bash
# Current: v0.9.0 → Target: v1.0.0

# 1. Update VERSION
echo "1.0.0" > VERSION

# 2. Update README.md (comprehensive changelog)
# Include all breaking changes, new features, migration notes

# 3. Commit and tag
git add VERSION README.md
git commit -m "chore(release): Prepare for release v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0: Complete UI redesign"
git push origin main
git push origin v1.0.0
```

---

## Version History Archive

Historic versions and their significance:

- **v0.6.5** (February 18, 2026): Spellbook/cast polish, Thorne options sync workflow, icon variant refresh
- **v0.6.4** (February 15, 2026): Gauge system overhaul, target window improvements
- **v0.6.3** (February 9, 2026): Cast spell window spell-name font adjustment
- **v0.5.0** (February 3, 2026): Phase 5 Target Window, documentation reorganization
- **v0.4.0** (February 2, 2026): Release infrastructure, automated workflows
- **v0.3.0** (February 1, 2026): Documentation overhaul, merchant window redesign
- **v0.2.0** (January 2026): Hybrid hotbar, Actions window
- **v0.1.0** (January 2026): Initial Actions window, player stats

---

## Best Practices

### DO:
✅ Update VERSION file every release  
✅ Use annotated tags (`git tag -a`)  
✅ Write descriptive commit messages  
✅ Follow SemVer guidelines  
✅ Keep README.md version history current  
✅ Test before tagging  

### DON'T:
❌ Skip VERSION file updates  
❌ Use lightweight tags  
❌ Tag without testing  
❌ Push tags before commits  
❌ Delete tags from remote (causes workflow issues)  
❌ Reuse version numbers  

---

## Troubleshooting

### Issue: "Tag already exists"

```bash
# Delete local tag
git tag -d v0.6.4

# Delete remote tag (use with caution!)
git push origin :refs/tags/v0.6.4

# Recreate tag
git tag -a v0.6.4 -m "Release v0.6.4: Description"
git push origin v0.6.4
```

### Issue: "VERSION file out of sync"

```bash
# Check current VERSION
cat VERSION

# Check latest tag
git describe --tags --abbrev=0

# If mismatch, update VERSION to match latest release
echo "0.6.4" > VERSION
git add VERSION
git commit -m "chore: Sync VERSION file with latest release"
```

### Issue: "Release workflow didn't trigger"

**Possible causes:**
1. Tag doesn't match pattern `v*.*.*`
2. Tag pushed before commit
3. Workflow file has syntax errors

**Solution:**
```bash
# Verify tag format
git tag -l

# Re-push tag
git push origin v0.6.4

# Check GitHub Actions logs for errors
```

---

## References

- **Semantic Versioning:** https://semver.org/
- **Git Tagging:** https://git-scm.com/book/en/v2/Git-Basics-Tagging
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github

---

## Maintenance Notes

**Last Updated:** February 18, 2026  
**Maintained By:** Draknare Thorne  
**Status:** Active process, subject to refinement
