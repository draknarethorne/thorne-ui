# Thorne UI Release Documentation Index

## 📌 CURRENT RELEASE: v0.8.0 ✅

**Status:** Feature release (multi-color composite gauges)  
**Release Date:** June 2026  
**Ready for Production:** Yes!

**Release Documentation:** See [ROADMAP-v0.8.0.md](../ROADMAP-v0.8.0.md)

## 📚 Documentation Structure (Updated Feb 18, 2026)

**Core Release Documents:**

- **[RELEASES.md](RELEASES.md)** - Complete guide to creating and managing releases (includes FAQ & quick answers)
- **[RELEASE-NOTES-TEMPLATE.md](RELEASE-NOTES-TEMPLATE.md)** - Template for GitHub release notes

**For Creating New Releases (v0.6.0+):**

See [RELEASES.md](RELEASES.md) for:

1. Quick Answers (TL;DR: push tag, GitHub does the rest)
2. Overview of automated GitHub Actions workflow
3. Step-by-step process for creating releases
4. Release checklist
5. Version numbering guidelines
6. Where to find releases and share with users

Estimated time: 15-20 minutes prep + 5 minutes release (fully automated on GitHub)

---

## 📜 Historical Release Archives

Historical release archives are stored in `.development/archive/` (repository-only; not shipped in release packages).

---

## 🧪 Current Pre-Release

**v0.7.5 (next)** — class-specific slot images and item slot overrides  
**Tag format:** `v0.7.5`

---

## 🚀 The Release Process (TL;DR)

```bash
# 1. Update version in README.md (Version History section)
# 2. Commit and push to main
git add README.md
git commit -m "chore: Update version history for v0.7.0"
git push origin main

# 3. Create and push a version tag (triggers GitHub Actions)
git tag -a v0.7.0 -m "Release v0.7.0: Description of changes"
git push origin v0.7.0

# ✨ GitHub Actions handles everything:
# - Creates ZIP packages automatically
# - Generates release notes from commits
# - Publishes to Releases page
# - Takes 2-3 minutes
```

**That's it!** Visit the [Releases page](https://github.com/draknarethorne/thorne-ui/releases) when complete.

---

## 📊 Document Selection Guide

| Need                               | Read                                                                                                           |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Creating releases (start here)** | [RELEASES.md](RELEASES.md)                                                                                     |
| **GitHub release notes template**  | [RELEASE-NOTES-TEMPLATE.md](RELEASE-NOTES-TEMPLATE.md)                                                         |
| **What changed recently?**         | [../README.md](../README.md)                                                                                   |
| **How the workflow was built**     | [../../.development/archive/RELEASES-IMPLEMENTATION.md](../../.development/archive/RELEASES-IMPLEMENTATION.md) |
| **Testing locally before release** | [../../.development/archive/TESTING-RELEASES.md](../../.development/archive/TESTING-RELEASES.md)               |

---

## ✅ Checklist: Release Readiness

**For any release, you need to:**

- [ ] Review [RELEASES.md](RELEASES.md) (Complete process guide)
- [ ] Update version in README.md (Version History section)
- [ ] Commit version update
- [ ] Create and push the release tag
- [ ] Monitor workflow at GitHub Actions
- [ ] Verify release at Releases page

**Total time:** ~15 minutes

---

## 🎓 Release Strategy

### v0.4.0 (February 2, 2026)

- **Purpose:** Establish release infrastructure
- **Documentation:** Comprehensive (infrastructure setup)
- **Size:** Large (first time setup)

### v0.5.0 (February 3, 2026)

- **Purpose:** Standardize release process
- **Documentation:** Moderate (checklist + changes)
- **Size:** Streamlined

### v0.6.0+ (Future)

- **Purpose:** Simple repeatable releases
- **Documentation:** Template-based (copy, customize, release!)
- **Size:** Minimal prep

---

## 🔗 Quick Links

**Actions & Releases:**

- [GitHub Actions](https://github.com/draknarethorne/thorne-ui/actions) - Monitor workflows
- [GitHub Releases](https://github.com/draknarethorne/thorne-ui/releases) - View all releases
- [Main Repository](https://github.com/draknarethorne/thorne-ui) - Project home

**Documentation:**

- [Main README](../README.md) - Project overview
- [Development Guide](../DEVELOPMENT.md) - Development roadmap
- [Standards](../STANDARDS.md) - Code standards
- [Phases](../../.development/initial_phases/) - Development phases (maintainer-only)

---

**Status:** v0.7.0 released ✅

**Last Updated:** February 22, 2026
