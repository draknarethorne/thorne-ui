# Quick Start: Creating a Release

**🎯 TL;DR: Push a tag, GitHub does the rest automatically!**

```bash
git push origin v0.6.4
# That's it! GitHub Actions creates ZIPs and publishes the release.
```

**View releases:** https://github.com/draknarethorne/thorne-ui/releases

---

This is a quick reference for creating releases. For detailed information, see [RELEASES.md](RELEASES.md).

## 💡 Key Points

- ✅ **ZIP creation is automated** - runs on GitHub's servers
- ✅ **No local tools needed** - just git commands
- ✅ **Release page is public** - `/releases` URL
- ✅ **Takes 2-3 minutes** - from tag push to published release

---

## Pre-Release Checklist

```bash
# 1. Update version in README.md Version History
vim README.md
# Add: **v0.6.4** (February 15, 2026) with changes

# 2. Test thorne_drak in-game
/loadskin thorne_drak

# 3. Commit all changes
git add .
git commit -m "docs: Update version history for v0.6.4 release"
git push origin main
```

## Create Release

```bash
# 1. Create annotated tag
git tag -a v0.6.4 -m "Release v0.6.4: Brief description of changes"

# 2. Push tag to trigger workflow
git push origin v0.6.4

# 3. Monitor workflow
# Go to: https://github.com/draknarethorne/thorne-ui/actions

# 4. Check release
# Go to: https://github.com/draknarethorne/thorne-ui/releases
```

## What Happens Automatically

**🤖 GitHub Actions runs on GitHub's servers (not your computer!):**

1. ✅ Extract version from tag (e.g., `v0.6.4` → `0.6.4`)
2. ✅ Generate changelog from commits since last release
3. ✅ **Package thorne_drak as ZIP:** `thorne_drak-v0.6.4.zip` (~2.4 MB)
4. ✅ **Create complete package:** `thorne-ui-v0.6.4.zip` (thorne_drak + docs, ~2.8 MB)
5. ✅ Create release notes with installation instructions
6. ✅ **Publish to Releases page:** https://github.com/draknarethorne/thorne-ui/releases
7. ✅ **Attach ZIP files** - users can download immediately

**You don't:**
- ❌ Create ZIPs locally
- ❌ Run any build scripts
- ❌ Upload files manually
- ❌ Write release notes manually (auto-generated)

**The workflow does everything!** Just push the tag and wait 2-3 minutes.

> **Note**: Only thorne_drak is included in releases. Other variants are available in the source repository.

## Version Numbering

- **v1.0.0** - Major release (breaking changes, complete redesign)
- **v0.6.4** - Patch release (bug fixes, small improvements)
- **v0.3.1** - Patch release (bug fixes, small tweaks)

## Troubleshooting

### Workflow didn't trigger
```bash
# Verify tag was pushed
git ls-remote --tags origin

# Tag must start with 'v'
git tag v0.6.4  # ✓ Correct
git tag 0.6.4   # ✗ Won't trigger workflow
```

### Need to redo a tag
```bash
# Delete local and remote tag
git tag -d v0.6.4
git push origin :refs/tags/v0.6.4

# Create new tag
git tag -a v0.6.4 -m "Release v0.6.4"
git push origin v0.6.4
```

### Check workflow logs
1. Go to: https://github.com/draknarethorne/thorne-ui/actions
2. Click on "Create Release" workflow
3. Click on the latest run
4. Review step-by-step logs

## After Release

- [ ] Test download the thorne_drak ZIP
- [ ] Verify ZIP contains correct files
- [ ] Edit release notes on GitHub if needed
- [ ] Announce to TAKP community

---

**Full Documentation**: [RELEASES.md](RELEASES.md)
