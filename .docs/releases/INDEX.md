# Thorne UI Release Documentation Index

## 📌 CURRENT RELEASE: v0.6.2 ✅

**Status:** Patch release (Inventory layout fixes + Loadskin width expansion)  
**Release Date:** February 9, 2026  
**Ready for Production:** Yes!

### For Creating New Releases (v0.6.0+)

**Quick Reference:**
1. **[RELEASES-QUICKSTART.md](RELEASES-QUICKSTART.md)** - TL;DR (push tag, GitHub does the rest)
2. **[RELEASE-TEMPLATE.md](RELEASE-TEMPLATE.md)** - Use as template for next release prep
3. **[RELEASES.md](RELEASES.md)** - Complete reference guide

Estimated time: 15-20 minutes prep + 5 minutes release (fully automated on GitHub)

### Detailed Guides

- **[RELEASES.md](RELEASES.md)** - Comprehensive guide with architecture & workflow details
- **[RELEASES-QUICKSTART.md](RELEASES-QUICKSTART.md)** - Quick reference (push tag → GitHub handles it)
- **[RELEASES-FAQ.md](RELEASES-FAQ.md)** - Common questions and troubleshooting
- **[RELEASES-IMPLEMENTATION.md](../../.development/releases/RELEASES-IMPLEMENTATION.md)** - Technical implementation details (maintainer-only)
- **[TESTING-RELEASES.md](../../.development/releases/TESTING-RELEASES.md)** - Testing the release workflow locally (maintainer-only)

### Templates

- **[RELEASE-TEMPLATE.md](RELEASE-TEMPLATE.md)** - Template for preparing releases
- **[RELEASE-NOTES-TEMPLATE.md](RELEASE-NOTES-TEMPLATE.md)** - Template for release notes

---

## 📜 Historical Release Archives

Historical release archives are stored in `.development/releases/archive/` (repository-only; not shipped in release packages).

---

## 🧪 Current Pre-Release

**v0.6.3 (pre-release)** — Cast spell window spell-name font adjusted to Font 1  
**Tag format:** `v0_6_3`

---

## 🚀 The Release Process (TL;DR)

```bash
# 1. Update version in README.md (Version History section)
# 2. Commit and push to main
git add README.md
git commit -m "chore: Update version history for v0.6.2"
git push origin main

# 3. Create and push a version tag (triggers GitHub Actions)
git tag -a v0.6.2 -m "Release v0.6.2: Description of changes"
git push origin v0.6.2

# ✨ GitHub Actions handles everything:
# - Creates ZIP packages automatically
# - Generates release notes from commits
# - Publishes to Releases page
# - Takes 2-3 minutes
```

**That's it!** Visit the [Releases page](https://github.com/draknarethorne/thorne-ui/releases) when complete.

---

## 📊 Document Selection Guide

| Need | Read |
|------|------|
| **Prepare v0.6.0+** | [releases/RELEASE-TEMPLATE.md](releases/RELEASE-TEMPLATE.md) |
| **Just want to create a release** | [RELEASES-QUICKSTART.md](RELEASES-QUICKSTART.md) |
| **What changed recently?** | [../README.md](../README.md) |
| **Questions about the process** | [RELEASES-FAQ.md](RELEASES-FAQ.md) |
| **How the workflow was built** | [../../.development/releases/RELEASES-IMPLEMENTATION.md](../../.development/releases/RELEASES-IMPLEMENTATION.md) |
| **Complete reference guide** | [RELEASES.md](RELEASES.md) |
| **Testing locally before release** | [../../.development/releases/TESTING-RELEASES.md](../../.development/releases/TESTING-RELEASES.md) |

---

## ✅ Checklist: Release Readiness

**For any release, you need to:**

- [ ] Review [RELEASE-TEMPLATE.md](RELEASE-TEMPLATE.md)
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
- [Phases](../../.development/initial-phases/) - Development phases (maintainer-only)

---

**Status:** v0.6.2 released ✅

**Last Updated:** February 9, 2026
