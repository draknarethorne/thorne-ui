# v0.6.3 Pre-Release Checklist

**Status:** Ready for Pre-Release  
**Release Date:** February 9, 2026  
**Previous Release:** v0.6.2 (February 9, 2026)  
**Commits Since v0.6.2:** TBD

---

## Pre-Release Tasks

Use this checklist before creating the v0.6.3 pre-release tag.

### ✅ Code & Testing
- [ ] Cast spell window spell names render correctly with Font 1
- [ ] Window alignment and labels remain readable at the smaller font size

### ✅ Documentation
- [ ] README.md Version History updated for v0.6.3 pre-release
- [ ] Pre-release docs created under `.docs/releases/v0.6.3/`
- [ ] All changes committed to main branch

### ✅ Version Preparation

**Current Status:**
```
Branch: main
Latest Commit: TBD
Tag History: v0.6.2 exists
README.md Version: ✅ Updated
VERSION file: ✅ Updated to 0.6.3-pre
```

**Version History Entry (README.md):**
```
**v0.6.3** (February 9, 2026) _(pre-release)_
- Cast spell window spell-name font adjusted to Font 1
```

---

## Pre-Release Steps (Follow in Order)

### Step 1: Verify Version Updates (LOCAL)
- Confirm `README.md` includes the v0.6.3 pre-release entry.
- Confirm `VERSION` is set to `0.6.3-pre`.

### Step 2: Commit Version Updates
```bash
# Stage version updates
git add README.md VERSION .docs/releases/v0.6.3

# Commit with release message
git commit -m "chore: Prepare v0.6.3 pre-release"

# Push to main
git push origin main
```

### Step 3: Create Pre-Release Tag
```bash
# Create annotated tag with version and description
git tag -a v0_6_3 -m "Pre-release v0.6.3: Cast spell font adjustment"

# Push tag to GitHub (TRIGGERS release workflow if supported)
git push origin v0_6_3
```

### Step 4: Monitor Workflow
```
✨ GitHub Actions automatically:
1. Detects v0_6_3 tag
2. Extracts version
3. Generates changelog from commits
4. Creates ZIP packages
5. Publishes pre-release to: https://github.com/draknarethorne/thorne-ui/releases

⏱️  Takes 2-3 minutes total
```

**Monitor Progress:**
- Actions Tab: https://github.com/draknarethorne/thorne-ui/actions
- Look for "Create Release" workflow
- Should complete with green checkmark

### Step 5: Verify Pre-Release
```
✅ Pre-release is complete when you see:

1. Green checkmark in Actions tab
2. Release appears at: https://github.com/draknarethorne/thorne-ui/releases
3. Both ZIP files attached
4. Release notes auto-generated from commits
```

---

## Troubleshooting

### "Workflow didn't trigger"
```bash
# Verify tag was pushed
git ls-remote --tags origin | grep v0_6_3
```

---

**Questions?** See [.docs/releases/INDEX.md](../INDEX.md)
