# Thorne UI v0.6.3 Pre-Release

This directory contains documentation for the v0.6.3 pre-release.

## 📋 What's Included in v0.6.3 (Pre-Release)

- Cast spell window spell-name font adjusted to Font 1

## 📚 Release Documentation

- **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** - Step-by-step pre-release process
- **[v0.6.3-CHANGES.md](v0.6.3-CHANGES.md)** - Detailed changes

## ⚡ Quick Start

```bash
# 1. Update README.md version history (see RELEASE-CHECKLIST.md)
# 2. Commit and push
git add README.md VERSION .docs/releases/v0.6.3
git commit -m "chore: Prepare v0.6.3 pre-release"
git push origin main

# 3. Create and push tag
git tag -a v0_6_3 -m "Pre-release v0.6.3: Cast spell font adjustment"
git push origin v0_6_3

# GitHub Actions does the rest automatically (if tag format is supported)
```

---

**Maintainer:** Draknare Thorne
