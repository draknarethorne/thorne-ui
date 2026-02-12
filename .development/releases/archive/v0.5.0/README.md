# Thorne UI v0.5.0 Release

This directory contains documentation for the v0.5.0 release.

## 📋 What's Included in v0.5.0

**Phase 5 - Target Window Enhancements** ✅ (Merged February 3, 2026)
- Target of Target (ToT) window for Zeal client (182×18px)
- Target Level and Class display
- Player HP/Mana gauges in Target window
- Pet Window improvements:
  - Dismiss button enabled
  - Mana color updates (RGB(100,150,255))
  - Standard and Tall Gauge variants

**Additional Features:**
- Comprehensive XML attribution headers (38 files)
- New Options variants with full documentation
- Loot window bug fix (420px height for proper 4×5 grid)

## 📚 Release Documentation

- **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** - Step-by-step release process (START HERE)
- **[v0.5.0-CHANGES.md](v0.5.0-CHANGES.md)** - Detailed list of what changed

## ⚡ Quick Start

```bash
# 1. Verify version in README.md is updated to v0.5.0
# 2. Commit any final changes
git add .
git commit -m "chore: Prepare for v0.5.0 release"
git push origin main

# 3. Create and push the tag (GitHub Actions does the rest!)
git tag -a v0.5.0 -m "Release v0.5.0: Phase 5 Target Window enhancements and improvements"
git push origin v0.5.0

# 4. Monitor at: https://github.com/draknarethorne/thorne-ui/actions
# 5. View release at: https://github.com/draknarethorne/thorne-ui/releases
```

**That's it!** GitHub Actions automatically:
- Creates ZIP packages
- Generates changelog
- Publishes release
- Takes 2-3 minutes

## 📖 For More Details

- **[.docs/releases/RELEASES-QUICKSTART.md](../../../.docs/releases/RELEASES-QUICKSTART.md)** - Full quickstart guide
- **[.docs/releases/RELEASES.md](../../../.docs/releases/RELEASES.md)** - Complete reference
- **[.docs/releases/INDEX.md](../../../.docs/releases/INDEX.md)** - Documentation index

---

Last updated: February 3, 2026
