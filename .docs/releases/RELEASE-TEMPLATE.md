# Release Template - Use for Future Releases (v0.6.0+)

This template is for **creating releases after v0.5.0**. The process becomes simple and repeatable.

---

## For v0.6.0 and Beyond: Simple 5-Minute Process

### 1. Create Release Directory
```bash
# When you're ready to create v0.6.0:
mkdir -p .docs/releases/v0.6.0
```

### 2. Copy Template Files
```bash
# Copy this template and the checklist template into v0.6.0
cp .docs/releases/RELEASE-TEMPLATE.md .docs/releases/v0.6.0/
cp .development/releases/archive/v0.5.0/RELEASE-CHECKLIST.md .docs/releases/v0.6.0/RELEASE-CHECKLIST.md
```

### 3. Update Checklist for Your Release

Edit `.docs/releases/v0.6.0/RELEASE-CHECKLIST.md`:

**Change:**
```bash
# At the top, update:
Release Date: February 3, 2026     -> Release Date: February [XX], 2026
Previous Release: v0.4.0           -> Previous Release: v0.5.0
Commits Since v0.4.0: 1            -> Commits Since v0.5.0: [X]

# Update Version History section:
**v0.6.0** (February [XX], 2026)
- [Your phase description here]
- [New features added]
- [Bug fixes]
```

### 4. Update Change Summary

Create `.docs/releases/v0.6.0/v0.6.0-CHANGES.md`:

Edit the sections:
- Major Features
- Technical Improvements
- Files Modified
- Testing Completed

### 5. Create README.md

Create `.docs/releases/v0.6.0/README.md`:

```markdown
# Thorne UI v0.6.0 Release

This directory contains documentation for the v0.6.0 release.

## 📋 What's Included in v0.6.0

**[List your phases/features here]**
- Phase X: [Description]
- Bug fixes
- Documentation updates

## 📚 Release Documentation

- **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** - Step-by-step release process
- **[v0.6.0-CHANGES.md](v0.6.0-CHANGES.md)** - Detailed changes

## ⚡ Quick Start

```bash
# 1. Update README.md version (see RELEASE-CHECKLIST.md)
# 2. Commit and push
git add README.md
git commit -m "chore: Prepare for v0.6.0 release"
git push origin main

# 3. Create and push tag
git tag -a v0.6.0 -m "Release v0.6.0: [Your description]"
git push origin v0.6.0

# GitHub Actions does the rest automatically!
```
```

---

## Key Points for All Releases (v0.5.0+)

### ✅ Process is Always the Same

1. **Update README.md** Version History
2. **Commit** version update to main
3. **Push** to origin/main
4. **Create tag:** `git tag -a v0.6.0 -m "Release v0.6.0: Description"`
5. **Push tag:** `git push origin v0.6.0`
6. **Wait 2-3 minutes** - GitHub Actions handles everything!

### ✅ What You DON'T Need to Do

- ❌ Create ZIP files locally
- ❌ Write complex release instructions (use template!)
- ❌ Manually upload files
- ❌ Manage changelog (auto-generated from commits)
- ❌ Create extensive v0.4.0-style documentation

### ✅ What Happens Automatically

GitHub Actions workflow (`.github/workflows/release.yml`):
1. Detects new `v*.*.*` tag
2. Extracts version number
3. Generates changelog from commits since last tag
4. Creates ZIP packages
5. Publishes release with notes
6. Makes downloads available

**Time:** ~2-3 minutes | **Your effort:** ~5 minutes total

---

## File Organization

```
.docs/releases/
├── INDEX.md                       ← Index (points to versions)
├── RELEASE-TEMPLATE.md            ← This file
├── RELEASES.md                    ← Generic workflow reference
└── v0.6.0/                        ← Your next release (follow this pattern)
    ├── README.md
    ├── RELEASE-CHECKLIST.md
    └── v0.6.0-CHANGES.md

.development/releases/archive/
├── v0.4.0/                        ← First release (historical)
└── v0.5.0/                        ← Second release (historical)
```

---

## Copy-Paste Commands for Next Release

```bash
# When ready for v0.6.0:

# 1. Create directory
mkdir -p .docs/releases/v0.6.0

# 2. Copy checklist template
cp .development/releases/archive/v0.5.0/RELEASE-CHECKLIST.md .docs/releases/v0.6.0/

# 3. Edit the checklist (update version numbers, date, changes)
vim .docs/releases/v0.6.0/RELEASE-CHECKLIST.md

# 4. Follow the checklist to complete release
# (It's all in there - just follow the steps!)
```

---

## Release Cadence

- **v0.4.0** - First release infrastructure (Feb 2, 2026)
- **v0.5.0** - Phase 5 enhancements (Feb 3, 2026)
- **v0.6.0** - Next phase ([date])
- **v0.7.0** - Future phase

**Naming:** `v[major].[minor].[patch]`
- **v0.4.0** → **v0.5.0** = minor version bump (new features)
- **v0.5.0** → **v0.5.1** = patch version bump (bug fixes only)
- **v1.0.0** = major version bump (breaking changes)

---

## Minimal Release Documentation Needed

### For Every Release, Create

1. **RELEASE-CHECKLIST.md** (copy from v0.5.0 archive, change dates/version)
   - Copy from previous release
   - Update version numbers
   - Update feature list
   - Update "Version History" section in README.md with new items
   - **Time: 5-10 minutes**

2. **v0.X.0-CHANGES.md** (copy from v0.5.0 archive, update sections)
   - List major features
   - List bug fixes
   - Update file count/statistics
   - **Time: 5-10 minutes**

3. **README.md** (copy from v0.5.0 archive, change version)
   - Update version number (3 places)
   - Update feature list
   - **Time: 2-3 minutes**

### Total Time: 15-20 minutes to prepare documentation
### Release Execution: 5-10 minutes (all automatic!)

---

## Questions?

- **How to release?** → See `.development/releases/archive/v0.5.0/RELEASE-CHECKLIST.md`
- **What changed?** → See `.development/releases/archive/v0.5.0/v0.5.0-CHANGES.md`
- **Detailed info?** → See `.docs/releases/RELEASES-QUICKSTART.md` or `.docs/releases/RELEASES.md`

---

**Remember:** v0.4.0 was setup infrastructure. Starting with v0.5.0, releases are simple!

Use this template for v0.6.0, v0.7.0, and all future releases.

---

*Template Version: 1.0*
*Based on: v0.5.0 release pattern*
*Last Updated: February 3, 2026*
