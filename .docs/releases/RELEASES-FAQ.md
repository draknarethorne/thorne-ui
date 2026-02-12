# Release Process FAQ

## Common Questions About GitHub Releases

### Q: Do I need to create ZIP files locally or does it happen automatically?

**A: It happens automatically in GitHub Actions - you don't need to run anything locally!**

When you push a version tag (e.g., `v0.4.0`), GitHub Actions automatically:
1. Creates the ZIP packages for you
2. Generates release notes
3. Publishes the release
4. Makes download links available

**You only need to:**
- Push a git tag: `git push origin v0.4.0`
- Wait 2-3 minutes for the workflow to complete
- That's it! The ZIPs are created automatically

**No local ZIP creation needed!** The entire packaging process runs on GitHub's servers.

---

### Q: Where can I find releases on GitHub?

**A: GitHub has a dedicated Releases page for every repository.**

**Direct URL:**
```
https://github.com/draknarethorne/thorne-ui/releases
```

**How to navigate to it:**

1. **From the repository homepage:**
   - Look at the right sidebar
   - Click on "Releases" (shows release count)
   - Or click on the release number badge

2. **From the top navigation:**
   - Go to your repository
   - Releases are listed in the right sidebar
   - Click to see all releases

3. **Direct link in README:**
   - The README.md has a direct link to the Releases page
   - Look for "From GitHub Releases (Recommended)" in Installation

**What you'll see on the Releases page:**
- List of all published releases (newest first)
- Version tags (v0.4.0, v0.3.0, etc.)
- Release notes with what's new
- Download links for ZIP files
- Release date and author
- Commit hash for each release

---

### Q: Can users find releases without navigating through my repo?

**A: Yes! Share the direct Releases page URL:**

```
https://github.com/draknarethorne/thorne-ui/releases
```

This URL goes directly to your releases and can be:
- Shared in Discord, forums, or social media
- Bookmarked by users
- Added to your project documentation
- Used in download instructions

Users don't need to navigate through the repository structure - they can go straight to downloads.

---

### Q: What's the difference between the test script and the automated workflow?

**A: The test script is for validation, the workflow creates real releases.**

**Test Script (`./.bin/test-release-workflow.sh`):**
- Runs locally on your machine
- Tests that the workflow WILL work
- Creates test ZIPs in `/tmp/` (not published)
- Takes ~30 seconds
- Use this to verify before creating a real release

**GitHub Actions Workflow:**
- Runs automatically on GitHub's servers
- Triggered by pushing a version tag
- Creates real ZIPs and publishes release
- Takes 2-3 minutes
- Users can download the results

**Workflow:**
1. Test locally first: `./.bin/test-release-workflow.sh`
2. When ready, push tag: `git push origin v0.4.0`
3. GitHub Actions runs automatically
4. Release appears on Releases page

---

### Q: Do I need to manually upload ZIP files to GitHub?

**A: No! The workflow automatically attaches them to the release.**

The workflow:
1. Creates ZIP files
2. Uploads them to the GitHub Release
3. Makes them available for download

You never touch the ZIP files manually.

---

### Q: How do users download releases?

**A: They visit the Releases page and click the ZIP file they want.**

**User workflow:**
1. Go to: https://github.com/draknarethorne/thorne-ui/releases
2. Find the version they want (latest is at the top)
3. Click on the ZIP file in the "Assets" section:
   - `thorne_drak-v0.4.0.zip` - Just the UI
   - `thorne-ui-v0.4.0.zip` - UI + documentation
4. Download starts automatically
5. Extract and install

---

### Q: Can I edit release notes after publishing?

**A: Yes! You can edit releases at any time.**

**How to edit:**
1. Go to the Releases page
2. Find the release you want to edit
3. Click the pencil/edit icon
4. Make your changes
5. Click "Update release"

The ZIP files stay the same, but you can update:
- Release title
- Release description/notes
- Mark as pre-release or draft

---

### Q: How do I know the workflow succeeded?

**A: Check the Actions tab or Releases page.**

**Option 1 - Check Actions:**
1. Go to: https://github.com/draknarethorne/thorne-ui/actions
2. Look for "Create Release" workflow
3. Green checkmark = success
4. Red X = failed (click to see logs)

**Option 2 - Check Releases:**
1. Go to: https://github.com/draknarethorne/thorne-ui/releases
2. Your new release should appear at the top
3. ZIP files should be in "Assets" section

**You'll know it worked when:**
- Release appears on the Releases page
- Both ZIP files are attached
- Release notes are populated
- Download links work

---

### Q: What happens if the workflow fails?

**A: Check the Actions tab for error logs.**

**Troubleshooting steps:**
1. Go to: https://github.com/draknarethorne/thorne-ui/actions
2. Click on the failed workflow run
3. Expand each step to see what failed
4. Common issues:
   - Missing `thorne_drak` directory
   - Invalid YAML syntax
   - Network/GitHub issues (rare)

**Fix and retry:**
1. Fix the issue
2. Delete the tag: `git push origin :refs/tags/v0.4.0`
3. Delete local tag: `git tag -d v0.4.0`
4. Create and push tag again

---

### Q: How much does this cost?

**A: GitHub Actions and Releases are free for public repositories!**

- GitHub Actions: 2,000 minutes/month free for public repos
- Releases: Unlimited releases and downloads
- Storage: No limits for release assets in public repos

This workflow uses ~2-3 minutes per release, so you can create many releases within the free tier.

---

### Q: Can I create a release without using a tag?

**A: Not with the automated workflow. Tags trigger the automation.**

**Why tags?**
- Tags mark specific versions in git history
- Users can checkout specific versions
- Follows semantic versioning (v1.0.0, v1.1.0, etc.)
- Standard practice for releases

**Manual alternative:**
You can create releases manually through the GitHub web interface, but you'll need to create and upload ZIP files yourself.

---

### Q: What if I want to change what gets included in the ZIP?

**A: Edit the workflow file: `.github/workflows/release.yml`**

Look for the "Create UI package" step and modify:
- What directories to include
- What files to exclude
- Additional packages to create

After editing, test with `./.bin/test-release-workflow.sh` before creating a real release.

---

## Quick Reference

| Task | Command/URL |
|------|-------------|
| Test locally | `./.bin/test-release-workflow.sh` |
| Create release | `git push origin v0.X.Y` |
| View releases | <https://github.com/draknarethorne/thorne-ui/releases> |
| Monitor workflow | <https://github.com/draknarethorne/thorne-ui/actions> |
| Edit release | Click pencil icon on Releases page |

---

**Still have questions?**
- Review: [RELEASES.md](RELEASES.md) for complete guide
- Review: [TESTING-RELEASES.md](../../.development/releases/TESTING-RELEASES.md) for testing info (maintainer-only)
- Open an issue on GitHub

---

**Last Updated:** February 2, 2026
