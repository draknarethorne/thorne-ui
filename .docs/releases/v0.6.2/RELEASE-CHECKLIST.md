# v0.6.2 Release Checklist

**Status:** Ready for Release  
**Release Date:** February 9, 2026  
**Previous Release:** v0.6.1 (February 7, 2026)  
**Commits Since v0.6.1:** TBD

---

## Pre-Release Tasks

Use this checklist before creating the v0.6.2 release tag.

### ✅ Code & Testing
- [ ] Inventory window loads without UI errors
- [ ] Equipment grid layout matches 6-row anatomical “paper doll” arrangement
- [ ] Hands slot visible and clickable
- [ ] Class animation and progression layout display correctly
- [ ] Loadskin window width and controls align properly

### ✅ Documentation
- [ ] README.md Version History updated for v0.6.2
- [ ] Release docs created under `.docs/releases/v0.6.2/`
- [ ] All changes committed to main branch

### ✅ Version Preparation

**Current Status:**
```
Branch: main
Latest Commit: TBD
Tag History: v0.6.1 exists
README.md Version: ✅ Updated
VERSION file: ✅ Updated to 0.6.2
```

**Version History Entry (README.md):**
```
**v0.6.2** (February 9, 2026)
- Inventory equipment grid refinements
  - Restored Hands slot visibility and sizing
  - Converted layout to 6-row anatomical “paper doll” arrangement
  - Centered 3-slot rows for cleaner alignment
- Class animation and progression layout tuning
  - ClassAnim window repositioned and resized with preserved aspect ratio
  - Progression window height reduced to balance layout
- Loadskin window width expansion (+32px)
- New Options variants for Inventory (Default + Enhanced No Hands Bug)
```

---

## Release Steps (Follow in Order)

### Step 1: Verify Version Updates (LOCAL)
- Confirm `README.md` includes the v0.6.2 entry.
- Confirm `VERSION` is set to `0.6.2`.

### Step 2: Commit Version Updates
```bash
# Stage version updates
git add README.md VERSION .docs/releases/v0.6.2

# Commit with release message
git commit -m "chore: Prepare v0.6.2 release"

# Push to main
git push origin main
```

### Step 3: Create Release Tag
```bash
# Create annotated tag with version and description
git tag -a v0.6.2 -m "Release v0.6.2: Inventory layout fixes and Loadskin width update"

# Push tag to GitHub (TRIGGERS release workflow!)
git push origin v0.6.2
```

### Step 4: Monitor Workflow
```
✨ GitHub Actions automatically:
1. Detects v0.6.2 tag
2. Extracts version: v0.6.2 → 0.6.2
3. Generates changelog from commits
4. Creates thorne_drak-v0.6.2.zip
5. Creates thorne-ui-v0.6.2.zip
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
   - thorne_drak-v0.6.2.zip
   - thorne-ui-v0.6.2.zip
4. Release notes auto-generated from commits
5. Downloads available to users
```

---

## Troubleshooting

### "Workflow didn't trigger"
```bash
# Verify tag was pushed
git ls-remote --tags origin | grep v0.6.2

# Tag must start with 'v' and match v*.*.*
# e.g., v0.6.2 ✓ or v1.2.3 ✓ but not 0.6.2 ✗
```

### "Need to redo the tag"
```bash
# Delete local and remote tag
git tag -d v0.6.2
git push origin :refs/tags/v0.6.2

# Start over from Step 3
```

### "Release notes look wrong"
Edit after creation:
1. Go to Releases page: https://github.com/draknarethorne/thorne-ui/releases
2. Click the pencil icon on v0.6.2 release
3. Edit release notes
4. Click "Update release"

---

## After Release

- [ ] Test download the `thorne_drak-v0.6.2.zip` file
- [ ] Verify ZIP contains correct files
- [ ] Announce v0.6.2 to TAKP community (Discord, forums, etc.)
- [ ] Update project documentation with new UI changes

---

**Questions?** See [.docs/releases/INDEX.md](../INDEX.md)
