# v0.5.0 Release Checklist

**Status:** Ready for Release
**Release Date:** February 3, 2026
**Previous Release:** v0.4.0 (February 2, 2026)
**Commits Since v0.4.0:** 1 merge commit (Phase 5 enhancements)

---

## Pre-Release Tasks

Use this checklist before creating the v0.5.0 release tag.

### ✅ Code & Testing
- [x] Phase 5 Target Window enhancements merged to main
- [x] In-game testing completed and verified
- [x] All XML files validated (no syntax errors)
- [x] Attribution headers complete on all files

### ✅ Documentation
- [x] Phase 5 documentation updated
- [x] Options variants documented with README files
- [x] Technical documentation (EQTypes, Zeal features) updated
- [x] All changes committed to main branch

### ✅ Version Preparation

**Current Status:**
```
Branch: main
Latest Commit: a013039 (Phase 5 Target Window enhancements)
Tag History: v0.4.0 exists
README.md Version: ❓ NEEDS UPDATE (see below)
```

**TODO - Update Version Information:**

```bash
# 1. Open README.md and add v0.5.0 to Version History section
# Add this entry at the TOP of Version History (most recent first):

**v0.5.0** (February 3, 2026)
- Phase 5: Target Window enhancements (ToT, player gauges, target info)
- Pet window improvements (dismiss button, color updates)
- Comprehensive XML attribution headers (38 files)
- Loot window bug fix (proper 4×5 grid height)
- Enhanced Options documentation and variants
```

---

## Release Steps (Follow in Order)

### Step 1: Update Version (LOCAL)
```bash
# Open README.md and update the Version History section
vim README.md

# 🔍 FIND THIS SECTION:

## Version History

**v0.4.0** (February 2, 2026)
- Release infrastructure setup...

# 🔧 ADD v0.5.0 ABOVE IT (at the top):

## Version History

**v0.5.0** (February 3, 2026)
- Phase 5: Target Window enhancements (ToT, player gauges, target info)
- Pet window improvements (dismiss button, color updates)
- Comprehensive XML attribution headers (38 files)
- Loot window bug fix (proper 4×5 grid height)
- Enhanced Options documentation and variants

**v0.4.0** (February 2, 2026)
- Release infrastructure setup...

# ✅ Save the file (Ctrl+S or :wq in vim)
```

### Step 2: Commit Version Update
```bash
# Stage the updated README
git add README.md

# Commit with release message
git commit -m "chore: Update version history for v0.5.0 release"

# Push to main
git push origin main
```

### Step 3: Create Release Tag
```bash
# Create annotated tag with version and description
git tag -a v0.5.0 -m "Release v0.5.0: Phase 5 Target Window enhancements (ToT, player gauges, pet improvements)"

# Push tag to GitHub (TRIGGERS release workflow!)
git push origin v0.5.0
```

### Step 4: Monitor Workflow
```
✨ GitHub Actions automatically:
1. Detects v0.5.0 tag
2. Extracts version: v0.5.0 → 0.5.0
3. Generates changelog from commits
4. Creates thorne_drak-v0.5.0.zip (~2.4 MB)
5. Creates thorne-ui-v0.5.0.zip (~2.8 MB)
6. Publishes release to: https://github.com/draknarethorne/thorne-ui/releases

⏱️  Takes 2-3 minutes total
```

**Monitor Progress:**
- Actions Tab: https://github.com/draknarethorne/thorne-ui/actions
- Look for "Create Release" workflow
- Should complete with green checkmark

### Step 5: Verify Release
```
✅ Release is complete when you see:

1. Green checkmark in Actions tab
2. Release appears at: https://github.com/draknarethorne/thorne-ui/releases
3. Both ZIP files attached:
   - thorne_drak-v0.5.0.zip
   - thorne-ui-v0.5.0.zip
4. Release notes auto-generated from commits
5. Downloads available to users
```

---

## Troubleshooting

### "Workflow didn't trigger"
```bash
# Verify tag was pushed
git ls-remote --tags origin | grep v0.5.0

# Tag must start with 'v' and match v*.*.*
# e.g., v0.5.0 ✓ or v1.2.3 ✓ but not 0.5.0 ✗
```

### "Need to redo the tag"
```bash
# Delete local and remote tag
git tag -d v0.5.0
git push origin :refs/tags/v0.5.0

# Start over from Step 3
```

### "Release notes look wrong"
Edit after creation:
1. Go to Releases page: https://github.com/draknarethorne/thorne-ui/releases
2. Click the pencil icon on v0.5.0 release
3. Edit release notes
4. Click "Update release"

---

## After Release

- [ ] Test download the `thorne_drak-v0.5.0.zip` file
- [ ] Verify ZIP contains correct files
- [ ] Announce v0.5.0 to TAKP community (Discord, forums, etc.)
- [ ] Update project documentation with new UI changes

---

## Quick Command Reference

```bash
# Check version info
git describe --tags
git tag -l

# View release checklist
cat .docs/releases/v0.5.0/RELEASE-CHECKLIST.md

# For next release (v0.6.0)
# Just follow "Release Steps" section above!
```

---

**Next Steps After v0.5.0:**
1. Continue development work (new features, phases)
2. For v0.6.0, follow this same checklist
3. Copy this template for each release

---

**Questions?** See [.docs/releases/INDEX.md](../../../.docs/releases/INDEX.md)
