# GitHub Releases Guide

This guide explains how to create and manage releases for the Thorne UI project on GitHub.

## 🎯 Quick Answers

**Q: Do I need to create ZIPs locally?**  
**A: No! GitHub Actions creates them automatically when you push a tag. You don't run anything locally.**

**Q: Where do I find releases?**  
**A: https://github.com/draknarethorne/thorne-ui/releases** (or click "Releases" in the right sidebar)

**Q: What do I need to do?**  
**A: Just push a git tag:** `git push origin v0.6.4` **- everything else is automatic!**

See [RELEASES-FAQ.md](RELEASES-FAQ.md) for more common questions.

---

## Overview

GitHub Releases provide a way to package and distribute versions of the Thorne UI with:
- **Automatic ZIP creation** - No manual packaging needed!
- **Downloadable packages** - ZIP files created by GitHub Actions
- **Version-tagged releases** - Organized by semantic version
- **Auto-generated changelogs** - From git commit history
- **Public download page** - Accessible at `/releases` URL

## What Gets Released

Each release includes:
1. **thorne_drak package** - The primary UI variant (`thorne_drak-v{VERSION}.zip`)
2. **Complete package** - thorne_drak with all documentation (`thorne-ui-v{VERSION}.zip`)
3. **Release notes** - Auto-generated from git commits since the last release
4. **Version tag** - Git tag marking the specific commit (e.g., `v0.3.0`)

> **Note**: Only thorne_drak is included in releases. For reference implementations, see the community UIs in the repository: duxaUI, Infiniti-Blue, QQQuarm.

## Creating a Release

### Method 1: Automated Release (Recommended)

**🎯 Everything happens automatically on GitHub's servers - no local work needed!**

The automated workflow creates releases when you push a version tag:

1. **Ensure all changes are committed and pushed to main:**
   ```bash
   git add .
   git commit -m "Prepare for release v0.6.4"
   git push origin main
   ```

2. **Create and push a version tag:**
   ```bash
   # Create an annotated tag with release notes
   git tag -a v0.6.4 -m "Release v0.6.4: Brief description of major changes"
   
   # Push the tag to trigger the release workflow
   git push origin v0.6.4
   ```

3. **GitHub Actions automatically:**
   - ✅ Creates ZIP packages (thorne_drak and complete)
   - ✅ Generates changelog from commits
   - ✅ Creates release notes
   - ✅ Publishes to Releases page
   - ✅ Makes downloads available

4. **View your release:**
   - **Releases page:** https://github.com/draknarethorne/thorne-ui/releases
   - Or click "Releases" in the right sidebar of your repository
   - Your new release will be at the top with download links

**No manual ZIP creation, no local packaging - it's all automated!**

### Method 2: Manual Release (Alternative)

You can also create releases manually through the GitHub web interface:

1. Go to your repository on GitHub
2. Click "Releases" in the right sidebar
3. Click "Draft a new release"
4. Click "Choose a tag" and create a new tag (e.g., `v0.6.4`)
5. Fill in the release title and description
6. Manually upload ZIP files (if not using the workflow)
7. Click "Publish release"

---

## 📍 Where to Find Releases

### For You (Repository Owner)

**Direct URL:**
```
https://github.com/draknarethorne/thorne-ui/releases
```

**Navigation paths:**
1. From repository homepage → Click "Releases" in right sidebar
2. From repository homepage → Click on the releases badge/number
3. From top menu → Repository → Releases section

### For Users (Downloads)

Users can access releases without navigating through your repository:

**Share this URL for downloads:**
```
https://github.com/draknarethorne/thorne-ui/releases
```

**What users see:**
- List of all releases (newest first)
- Version numbers and dates
- Release notes with what's new
- Download buttons for ZIP files
- Installation instructions

**Advantages:**
- Direct link to downloads
- No need to browse repository structure
- Bookmark-able URL
- Shareable in Discord, forums, documentation

---

## Version Numbering

Follow semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v1.0.0) - Major changes, breaking compatibility, complete redesigns
- **MINOR** (v0.3.0) - New features, significant window additions, new variants
- **PATCH** (v0.3.1) - Bug fixes, small tweaks, documentation updates

### Examples:
- `v0.6.4` - Current patch release (gauge overhaul + target window updates)
- `v0.7.0` - Next minor version with new features
- `v1.0.0` - First major stable release
- `v0.3.1` - Patch release fixing bugs in v0.3.0

## Release Checklist

Before creating a release:

- [ ] **Update version number** in README.md (Version History section)
- [ ] **Update DEVELOPMENT.md** if version or release date changed
- [ ] **Test all UI variants** in-game to ensure they load correctly
- [ ] **Review documentation** - ensure all docs are up-to-date
- [ ] **Write clear commit messages** - they become part of the changelog
- [ ] **Update TODO.md** - mark completed items, add new planned work
- [ ] **Commit all changes** to main branch
- [ ] **Create the version tag** using the format `v*.*.*`
- [ ] **Push the tag** to trigger the automated release

After release creation:

- [ ] **Verify release on GitHub** - check that all ZIP files are present
- [ ] **Test download** - download and test installation of at least one variant
- [ ] **Review release notes** - edit on GitHub if automated notes need improvement
- [ ] **Announce** - share the release with the TAKP community (forums, Discord, etc.)

## Managing Releases

### Editing a Release

1. Go to the Releases page
2. Find the release you want to edit
3. Click the pencil icon (Edit)
4. Make your changes
5. Click "Update release"

### Deleting a Release

1. Go to the Releases page
2. Find the release you want to delete
3. Click "Delete"
4. Note: This does NOT delete the git tag

### Deleting a Tag

If you need to delete and recreate a tag:

```bash
# Delete local tag
git tag -d v0.6.4

# Delete remote tag
git push origin :refs/tags/v0.6.4

# Create new tag and push
git tag -a v0.6.4 -m "Release v0.6.4"
git push origin v0.6.4
```

## Troubleshooting

### Workflow doesn't trigger

- Verify you pushed a tag starting with `v` (e.g., `v0.4.0`, not `0.4.0`)
- Check that the tag was pushed: `git ls-remote --tags origin`
- Review the Actions tab for error messages

### Missing ZIP files

- Check the workflow logs in the Actions tab
- Verify the thorne_drak directory exists
- Ensure there are no file permission issues

### Changelog is empty

- The workflow compares against the previous tag
- For the first release, it includes all commits
- Write descriptive commit messages for better changelogs

## Best Practices

1. **Regular releases** - Release after completing significant features or phases
2. **Clear commit messages** - They appear in the auto-generated changelog
3. **Test before tagging** - Ensure everything works before creating the tag
4. **Semantic versioning** - Use the version numbering scheme consistently
5. **Document changes** - Update README.md version history before releasing
6. **Keep release notes clean** - Edit auto-generated notes for clarity if needed

## Examples

### Example Release Workflow

```bash
# You've completed Phase 4 work - time for a release!

# 1. Update version in README.md
vim README.md
# Add entry to Version History:
# **v0.6.4** (February 15, 2026)
# - ✅ Group window with raid support
# - ✅ Pet window enhancements
# etc.

# 2. Commit the version update
git add README.md
git commit -m "docs: Update version history for v0.6.4 release"
git push origin main

# 3. Create and push the tag
git tag -a v0.6.4 -m "Release v0.6.4: Gauge overhaul and target window updates"
git push origin v0.6.4

# 4. Wait for workflow (check GitHub Actions tab)
# 5. Review release on GitHub Releases page
# 6. Announce to community!
```

### Example Manual Release (if workflow fails)

```bash
# Create packages manually
zip -r thorne_drak-v0.6.4.zip thorne_drak/ -x "*.git*" "*.md"

# Upload through GitHub web interface
# Go to Releases > Draft a new release
# Upload the ZIP file
# Write release notes manually
# Publish
```

## Testing the Workflow

Before creating your first release, test that the workflow works correctly:

```bash
# Run the automated test script
./.bin/test-release-workflow.sh
```

This validates:
- YAML syntax
- Required files exist
- Package creation
- Release notes generation

For detailed testing instructions, see **[TESTING-RELEASES.md](../../.development/releases/TESTING-RELEASES.md)** (maintainer-only).

---

## Common Questions

See **[RELEASES-FAQ.md](RELEASES-FAQ.md)** for answers to:

- ❓ Do I need to create ZIPs locally? (No - automated!)
- ❓ Where can I find releases on GitHub? (Releases page URL)
- ❓ Can users find releases without navigating the repo? (Yes - direct link)
- ❓ What's the difference between test script and workflow?
- ❓ How do I know the workflow succeeded?
- ❓ What if the workflow fails?
- ❓ And more...

---

## Support

For questions about releases or the release process:
- Test the workflow: [TESTING-RELEASES.md](../../.development/releases/TESTING-RELEASES.md) (maintainer-only)
- Open an issue on GitHub
- Check the [DEVELOPMENT.md](../../DEVELOPMENT.md) guide
- Review existing releases for examples

---

**Last Updated**: February 16, 2026  
**Workflow Version**: 1.0
