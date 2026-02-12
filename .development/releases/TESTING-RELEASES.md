# Testing the GitHub Releases Workflow

This document explains how to test the GitHub Releases workflow to ensure it works correctly.

## Testing Approaches

There are three levels of testing available:

### 1. Local Validation (Automated) ✅ RECOMMENDED

Run the automated test script that validates all workflow steps locally:

```bash
./.bin/test-release-workflow.sh
```

**What it tests:**
- ✓ YAML syntax validation
- ✓ Required files and directories exist
- ✓ Version extraction logic
- ✓ Changelog generation
- ✓ ZIP package creation
- ✓ Package contents verification
- ✓ Release notes generation

**Output:**
- Test ZIP files created in `/tmp/test-releases/`
- Release notes preview in `/tmp/release_notes.md`
- Detailed step-by-step validation results

**Time:** ~30 seconds

**Risk:** None - completely safe, no changes to repository

---

### 2. Dry Run with Test Tag (Safe)

Create a test tag to trigger the workflow without creating a real release:

```bash
# 1. Create a test tag
git tag -a v0.99.0-test -m "Test release workflow"

# 2. Push the test tag to trigger workflow
git push origin v0.99.0-test

# 3. Monitor the workflow
# Go to: https://github.com/draknarethorne/thorne-ui/actions
# Watch the "Create Release" workflow run

# 4. Clean up test tag and release
# Delete the release on GitHub (via web interface)
# Delete the tag:
git tag -d v0.99.0-test
git push origin :refs/tags/v0.99.0-test
```

**What it tests:**
- ✓ Complete workflow execution in GitHub Actions
- ✓ Actual ZIP file creation on GitHub
- ✓ Release notes generation
- ✓ Release publishing

**Time:** 2-3 minutes (workflow execution time)

**Risk:** Low - creates a temporary release that can be deleted

---

### 3. Production Release (Real Release)

Create an actual release for distribution:

```bash
# 1. Update version in README.md
vim README.md
# Add version entry to "Version History" section

# 2. Commit version update
git add README.md
git commit -m "docs: Update version history for v0.4.0 release"
git push origin main

# 3. Create release tag
git tag -a v0.4.0 -m "Release v0.4.0: Brief description of changes"

# 4. Push tag to trigger workflow
git push origin v0.4.0

# 5. Monitor and verify
# Go to: https://github.com/draknarethorne/thorne-ui/actions
# Then: https://github.com/draknarethorne/thorne-ui/releases
```

**What it does:**
- Creates a permanent release
- Packages and distributes thorne_drak
- Publishes to GitHub Releases page
- Makes it available for users to download

**Time:** 2-3 minutes

**Risk:** None for well-tested workflows - creates permanent release

---

## Test Results

### Local Test Results (Automated Script)

When you run `./.bin/test-release-workflow.sh`, you should see:

```
==========================================
Testing GitHub Releases Workflow
==========================================

Test Version: v0.99.0-test

Step 1: Validating workflow YAML syntax...
✓ YAML syntax is valid

Step 2: Checking required directories and files exist...
✓ Directory exists: thorne_drak
✓ Directory exists: docs
✓ File exists: README.md
✓ File exists: DEVELOPMENT.md
✓ File exists: STANDARDS.md

Step 3: Simulating version extraction...
VERSION=0.99.0-test
TAG=v0.99.0-test
✓ Version extraction works

Step 4: Simulating changelog generation...
✓ Changelog generated (X commits)

Step 5: Creating test packages...
✓ Created thorne_drak-v0.99.0-test.zip (2.4M)
✓ Created thorne-ui-v0.99.0-test.zip (2.8M)

Step 6: Verifying ZIP contents...
✓ ZIP files contain expected content

Step 7: Creating test release notes...
✓ Release notes created (XX lines)

==========================================
All Tests Passed!
==========================================
```

### Expected ZIP Contents

**thorne_drak-v{VERSION}.zip should contain:**
- `thorne_drak/` directory with all UI files
- All `.xml`, `.tga`, `.bmp`, `.txt` files
- NO `.md` markdown files (excluded)
- NO `.git` files (excluded)

**thorne-ui-v{VERSION}.zip should contain:**
- `thorne_drak/` directory (complete UI)
- `README.md`
- `DEVELOPMENT.md`
- `STANDARDS.md`
- `.docs/` directory with all documentation
- NO `TODO.md` (excluded)

---

## Troubleshooting Tests

### Test Script Fails

**Issue:** Script exits with error

**Solutions:**
1. Check that you're in the repository root: `cd /path/to/thorne-ui`
2. Ensure script is executable: `chmod +x test-release-workflow.sh`
3. Verify Python3 is available: `python3 --version`
4. Check that `thorne_drak` directory exists

---

### YAML Validation Fails

**Issue:** "YAML syntax is invalid"

**Solutions:**
1. Check workflow file: `.github/workflows/release.yml`
2. Validate indentation (YAML is indent-sensitive)
3. Use online YAML validator: https://www.yamllint.com/
4. Fix any syntax errors reported

---

### Missing Files/Directories

**Issue:** "Directory missing" or "File missing"

**Solutions:**
1. Ensure you're in the repository root
2. Verify `thorne_drak` directory exists: `ls -la thorne_drak`
3. Check documentation exists: `ls -la .docs/`
4. Pull latest changes: `git pull origin main`

---

### ZIP Files Too Small/Large

**Expected sizes:**
- `thorne_drak-v*.zip`: ~2-3 MB
- `thorne-ui-v*.zip`: ~2.5-3.5 MB

**If sizes are wrong:**
1. Extract and inspect contents: `unzip -l /tmp/test-releases/*.zip`
2. Check for missing files
3. Verify exclude patterns in workflow

---

### GitHub Actions Workflow Fails

**Issue:** Workflow fails when pushing tag

**Check workflow logs:**
1. Go to: https://github.com/draknarethorne/thorne-ui/actions
2. Click on failed workflow run
3. Expand each step to see errors
4. Common issues:
   - Missing `thorne_drak` directory
   - Permissions error (shouldn't happen on GitHub)
   - Invalid YAML syntax
   - Network issues (rare)

---

## Verification Checklist

Before creating a production release, verify:

- [ ] Local test script passes (`./.bin/test-release-workflow.sh`)
- [ ] YAML syntax is valid
- [ ] All required files exist (thorne_drak, docs, README, etc.)
- [ ] ZIP files created successfully
- [ ] ZIP contents look correct
- [ ] Release notes are properly formatted
- [ ] Version number follows semantic versioning (vX.Y.Z)
- [ ] README.md version history is updated
- [ ] All changes are committed and pushed

---

## What Gets Tested

### Workflow Steps Validated

1. **Checkout** - Repository is cloned
2. **Version Extraction** - Tag is parsed correctly (v0.4.0 → 0.4.0)
3. **Changelog Generation** - Commits are collected and formatted
4. **Package Creation** - ZIP files are created with correct contents
5. **Release Notes** - Markdown file is generated with proper formatting
6. **Release Publishing** - Release is created on GitHub (test tag only)

### Files Validated

- `.github/workflows/release.yml` - Workflow syntax
- `thorne_drak/` - UI files directory
- `.docs/` - Documentation directory
- `README.md` - Project readme
- `DEVELOPMENT.md` - Development guide
- `STANDARDS.md` - Standards document

---

## Next Steps After Testing

### If All Tests Pass

1. ✓ Workflow is ready to use
2. ✓ You can create releases anytime by pushing tags
3. ✓ Users can download from GitHub Releases page

### Create Your First Release

When ready:

```bash
# Update version in README.md
git tag -a v0.4.0 -m "Release v0.4.0: Description"
git push origin v0.4.0
```

Visit: https://github.com/draknarethorne/thorne-ui/releases

---

## Support

If you encounter issues:

1. Run the local test script first: `./.bin/test-release-workflow.sh`
2. Review this testing guide
3. Check workflow logs on GitHub Actions
4. Review the detailed guide: [RELEASES.md](../../.docs/releases/RELEASES.md)

---

**Last Updated:** February 2, 2026  
**Test Script:** `test-release-workflow.sh`  
**Status:** All tests passing ✓
