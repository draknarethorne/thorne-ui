# v0.5.0 Release: Complete Guide for You

**Created:** February 3, 2026  
**Status:** ✅ Ready for Release  
**Your Next Action:** Follow the checklist below

---

## 🎯 What You Need to Know

### The Bottom Line
- **v0.5.0 is ready to release**
- **The process is simple: 4 git commands + wait 3 minutes**
- **You don't need extensive documentation like v0.4.0 had**
- **All future releases (v0.6.0+) will be even simpler**

### What's in v0.5.0
Phase 5 Target Window enhancements that merged on February 3:
- Target of Target window (Zeal support)
- Player HP/Mana gauges in Target window
- Pet dismiss button
- Loot window height fix
- Attribution headers (38 files)
- New Options variants with full documentation

---

## 📋 The Exact Process (Do This)

### Step 1: Update Version in README (5 minutes)

```bash
# Open README.md in your editor
vim README.md
# or use VS Code, Notepad++, etc.
```

**Find this section (currently in README.md):**
```markdown
## Version History

**v0.4.0** (February 2, 2026)
- Release infrastructure setup
```

**Add v0.5.0 ABOVE it (at the top):**
```markdown
## Version History

**v0.5.0** (February 3, 2026)
- Phase 5: Target Window enhancements (ToT, player gauges, target info)
- Pet window improvements (dismiss button, color updates RGB(100,150,255))
- Comprehensive XML attribution headers (38 files)
- Loot window bug fix (proper 4×5 grid, 420px height)
- Enhanced Options documentation and variants

**v0.4.0** (February 2, 2026)
- Release infrastructure setup
```

**Save the file and exit**

### Step 2: Commit Version Update (2 minutes)

```bash
# Stage README
git add README.md

# Commit with message
git commit -m "chore: Update version history for v0.5.0 release"

#Push to origin/main
git push origin main
```

### Step 3: Create Release Tag (1 minute)

```bash
# Create annotated tag
git tag -a v0.5.0 -m "Release v0.5.0: Phase 5 Target Window enhancements (ToT, player gauges, pet improvements)"

# Push tag to GitHub (THIS TRIGGERS EVERYTHING)
git push origin v0.5.0
```

### Step 4: Wait & Monitor (3 minutes)

**GitHub Actions automatically:**
1. Detects the v0.5.0 tag
2. Creates ZIP files (~2.4 MB + ~2.8 MB)
3. Generates changelog
4. Publishes release
5. Makes files downloadable

**Monitor progress:**
- Go to: https://github.com/draknarethorne/thorne-ui/actions
- Look for "Create Release" workflow
- Should finish in 2-3 minutes with green checkmark

**Verify completion:**
- Go to: https://github.com/draknarethorne/thorne-ui/releases
- You should see "Thorne UI v0.5.0" with downloadable ZIPs

**Total Time: ~10 minutes**

---

## 📚 Documentation Organization (How It Works)

### For v0.5.0 Release Right Now

Start with this:
1. **[.docs/releases/v0.5.0/RELEASE-CHECKLIST.md](../../../.docs/releases/v0.5.0/RELEASE-CHECKLIST.md)**
   - Detailed step-by-step instructions
   - Troubleshooting section
   - Command reference

2. **[.docs/releases/v0.5.0/v0.5.0-CHANGES.md](../../../.docs/releases/v0.5.0/v0.5.0-CHANGES.md)**
   - What changed in this release
   - Files modified list
   - Statistics

3. **[.docs/releases/v0.5.0/README.md](../../../.docs/releases/v0.5.0/README.md)**
   - Overview of v0.5.0
   - What features are included
   - Quick start reference

### For v0.6.0 and Beyond

Use the template:
- **[.docs/releases/RELEASE-TEMPLATE.md](../../../.docs/releases/RELEASE-TEMPLATE.md)**
  - Copy and customize for each release
  - Takes 15-20 minutes to prepare docs
  - Takes 5 minutes to execute

### Historical Reference

v0.4.0 documentation (for reference only):
- **[.docs/releases/v0.4.0/](../../../.docs/releases/v0.4.0/)**
  - This was the first release (infrastructure setup)
  - Much more extensive than v0.5.0
  - You don't need to do this for future releases!

---

## ❓ Key Insights

### Why is v0.5.0 Documentation Shorter?

**v0.4.0 Problem:**
- Release infrastructure didn't exist
- Had to build everything from scratch
- Documentation needed to explain the entire workflow
- Resulted in 2+ hours of prep work
- But you only do this ONCE

**v0.5.0 Achievement:**
- Infrastructure is now in place
- Process is proven and automated
- Documentation just needs to guide you through it
- Takes 15-20 minutes of prep work
- Same simple process for all future releases

### Why Not as Much Documentation Needed?

`.docs/releases/` now contains:

**Generic (reusable for all releases):**
- `.docs/RELEASES.md` - Complete guide
- `.docs/RELEASES-FAQ.md` - Common questions
- `.docs/releases-quickstart.md` - Quick reference
- `RELEASE-TEMPLATE.md` - Template for v0.6.0+
- `.docs/TESTING-RELEASES.md` - Testing guide

**Version-specific (one per release):**
- `v0.5.0/RELEASE-CHECKLIST.md` - ~150 lines
- `v0.5.0/v0.5.0-CHANGES.md` - ~200 lines
- `v0.5.0/README.md` - ~60 lines

**Historical (archive):**
- `v0.4.0/` - Everything from first release

### The Three-Phase Release Evolution

| Phase | Purpose | Prep Time | Per Release | Total Docs |
|-------|---------|-----------|-------------|-----------|
| **v0.4.0** | Build infrastructure | 2+ hours | One-time | 4 large files |
| **v0.5.0** | Prove the system works | 15-20 min | Each release | 3 medium files |
| **v0.6.0+** | Repeatable process | 15-20 min | Each release | Template-based |

---

## 🎓 What You're Actually Doing

### The Philosophy

1. **v0.4.0** was about "How do we release software?"
   - Build the CI/CD workflow
   - Document the process
   - Test everything
   - Result: Fully automated release system

2. **v0.5.0** is about "Now that we have the system, let's use it"
   - Follow the checklist
   - Let automation handle the work
   - Result: Simple, repeatable releases

3. **v0.6.0+** will be about "Copy the template and go"
   - Copy the release template
   - Update 3 small files
   - Push a tag
   - Result: 5 minute releases

### What GitHub Actions Does

When you push the `v0.5.0` tag:

```
You: git push origin v0.5.0   ← Just one command!
       ↓
GitHub: Detects tag
       ↓
GitHub: Runs workflow (.github/workflows/release.yml)
       ↓
GitHub: Extracts version number → "0.5.0"
       ↓ 
GitHub: Generates changelog from git commits
       ↓
GitHub: Creates 2 ZIP files (~2.4 MB + ~2.8 MB)
       ↓
GitHub: Publishes release with all assets
       ↓
Result: Users can download from Releases page!
```

**Your effort:** 1 command + 3 minute wait
**GitHub's effort:** All the complex work!

---

## ✅ Confidence Check

### Before You Release, Verify

- [ ] Phase 5 features are in main (already merged - Feb 3)
- [ ] README version history section ready to add v0.5.0
- [ ] You understand the 4-step process above
- [ ] You have git access and can push tags
- [ ] You know where to monitor: https://github.com/draknarethorne/thorne-ui/actions
- [ ] You know where to verify: https://github.com/draknarethorne/thorne-ui/releases

### What Could Go Wrong? (Nothing!)

| Issue | Solution |
|-------|----------|
| "Tag didn't trigger workflow" | Make sure tag starts with `v` and matches `v*.*.*` format |
| "Workflow took too long" | It shouldn't - max 5 minutes. Check actions tab. |
| "Release notes look wrong" | No problem! Edit them after release on GitHub |
| "Need to redo the tag" | Delete tag, recreate: `git tag -d v0.5.0` then `git push origin :refs/tags/v0.5.0` |

---

## 📊 Current Status

```
Branch: main
Latest Commit: a013039 (Phase 5 Target Window enhancements)
Previous Release: v0.4.0 (February 2, 2026)
Current Release: v0.5.0 (February 3, 2026) ← YOU ARE HERE

Next Steps:
1. Update README version → .docs/releases/v0.5.0/RELEASE-CHECKLIST.md
2. Follow 4-step process above
3. Monitor & celebrate! 🎉
```

---

## 🚀 Quick Commands Reference

```bash
# Update version in README
vim README.md

# Stage and commit
git add README.md
git commit -m "chore: Update version history for v0.5.0 release"
git push origin main

# Create and push tag (RELEASE!)
git tag -a v0.5.0 -m "Release v0.5.0: Phase 5 Target Window enhancements"
git push origin v0.5.0

# Monitor
# Open: https://github.com/draknarethorne/thorne-ui/actions

# Verify
# Open: https://github.com/draknarethorne/thorne-ui/releases
```

**That's it!** Total: ~10 minutes including wait time.

---

## 📖 How to Read the Documentation

### If you want to...

| Goal | Read |
|------|------|
| **Release v0.5.0 RIGHT NOW** | [.docs/releases/v0.5.0/RELEASE-CHECKLIST.md](../../../.docs/releases/v0.5.0/RELEASE-CHECKLIST.md) |
| **Understand what changed** | [.docs/releases/v0.5.0/v0.5.0-CHANGES.md](../../../.docs/releases/v0.5.0/v0.5.0-CHANGES.md) |
| **See all release docs in one place** | [.docs/RELEASES-INDEX.md](../../../.docs/RELEASES-INDEX.md) |
| **Prepare v0.6.0 release** | [.docs/releases/RELEASE-TEMPLATE.md](../../../.docs/releases/RELEASE-TEMPLATE.md) |
| **Understand the system** | [.docs/RELEASES.md](../../../.docs/releases/RELEASES.md) |
| **Answer FAQ** | [.docs/RELEASES-FAQ.md](../../../.docs/releases/RELEASES-FAQ.md) |

---

## 🎉 You're Ready!

**Everything is prepared and waiting.**

When you're ready to release v0.5.0:
1. Follow the 4-step process above
2. Or follow [.docs/releases/v0.5.0/RELEASE-CHECKLIST.md](../../../.docs/releases/v0.5.0/RELEASE-CHECKLIST.md) for more details
3. Wait 3 minutes
4. Your first streamlined release is live!

---

**Questions?** See [.docs/releases/INDEX.md](../../../.docs/releases/INDEX.md) for all documentation.

---

*Created: February 3, 2026*  
*For: v0.5.0 Release Planning*  
*By: Thorne UI Documentation*
