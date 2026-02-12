# Thorne UI v0.6.2 Release

This directory contains documentation for the v0.6.2 release.

## 📋 What's Included in v0.6.2

- Inventory equipment grid refinements (6-row anatomical layout, restored Hands slot)
- Class animation and progression layout tuning
- Loadskin window width expansion
- Inventory Options variants (Default + Enhanced No Hands Bug)

## 📚 Release Documentation

- **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** - Step-by-step release process
- **[v0.6.2-CHANGES.md](v0.6.2-CHANGES.md)** - Detailed changes

## ⚡ Quick Start

```bash
# 1. Update README.md version history (see RELEASE-CHECKLIST.md)
# 2. Commit and push
git add README.md VERSION .docs/releases/v0.6.2
git commit -m "chore: Prepare v0.6.2 release"
git push origin main

# 3. Create and push tag
git tag -a v0.6.2 -m "Release v0.6.2: Inventory layout fixes"
git push origin v0.6.2

# GitHub Actions does the rest automatically!
```

---

**Maintainer:** Draknare Thorne
