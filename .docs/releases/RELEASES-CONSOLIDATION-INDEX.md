# Release Documentation Consolidation

**Status:** Completed February 18, 2026 (as part of v0.7.0 documentation audit)

## What Was Consolidated

This index documents the consolidation of redundant release guides (6 documents → 3 core documents + archives).

### Before Consolidation

```
.docs/releases/
├── RELEASES.md ........................ Complete workflow guide (313 lines)
├── RELEASES-QUICKSTART.md ............ TL;DR (124 lines) [REDUNDANT]
├── RELEASES-FAQ.md ................... Q&A format (300+ lines) [REDUNDANT]
├── RELEASE-TEMPLATE.md ............... v0.6.0+ template (220 lines)
├── RELEASE-NOTES-TEMPLATE.md ......... Release notes boilerplate
├── INDEX.md .......................... Navigation guide
├── v0.6.2/ ........................... Release archive [MOVE]
├── v0.6.3/ ........................... Release archive [MOVE]
└── v0.6.5/ ........................... Latest release (current)
```

### After Consolidation

```
.docs/releases/ (Production Documents)
├── RELEASES.md ........................ Primary source of truth
├── RELEASE-NOTES-TEMPLATE.md ......... Template for notes
├── INDEX.md .......................... Updated navigation
└── v0.6.5/ ........................... Latest release reference
```

Older release guides and version archives are preserved in git history (reference via commit tags if needed).

## Why These Changes

### Eliminated Redundancy

**RELEASES-QUICKSTART.md** vs **RELEASES.md**
- Both describe identical automated workflow
- QUICKSTART is lines 1-13 of RELEASES (TL;DR section)
- Solution: Keep RELEASES.md "Quick Answers" section as TL;DR
- Status: Archived

**RELEASES-FAQ.md** vs **RELEASES.md**
- Both cover same topics (ZIP creation, finding releases, workflow status, costs)
- FAQ provides more verbose explanations
- RELEASES.md is the primary reference
- Solution: Keep RELEASES.md with comprehensive coverage
- Status: Archived

**RELEASE-TEMPLATE.md**
- Template for creating release checklists/preparation docs for v0.6.0+
- No longer needed as standard: releases now created via GitHub Actions
- v0.6.5 is latest example; older templates preserved in git history
- Status: In git history

**v0.6.2 & v0.6.3 directories**
- Old releases, v0.6.5 is current; no users on v0.6.2/v0.6.3
- Keep latest (v0.6.5) as reference; older versions in git history
- Status: In git history

### Improved clarity

- **Single source of truth:** RELEASES.md
- **Clearer information hierarchy:** Quick answers → Overview → Detailed process
- **Easier navigation:** INDEX.md references consolidated structure
- **Preserved history:** Old guides preserved in git history for legacy support

## Document Purpose Reference

| Document | Purpose | Audience |
|----------|---------|----------|
| **RELEASES.md** | Primary release workflow guide with examples | Maintainers, advanced users |
| **RELEASE-NOTES-TEMPLATE.md** | Template for GitHub release note body | Maintainers (copy-paste template) |
| **INDEX.md** | Navigation & overview of release docs | Everyone |
| **v0.6.5/** | Latest release reference docs | Reference (pre-release archived in .development/) |

## Archive Contents

Older release guides (RELEASES-QUICKSTART.md, RELEASES-FAQ.md, RELEASE-TEMPLATE.md) and previous releases (v0.6.2, v0.6.3) are preserved in git history via commit tags if needed for legacy reference.

**When to reference git history:**
- Looking for historical release workflow documentation
- Understanding how releases were structured in past versions
- Finding old release notes or checklists

## Navigation

**For creating a release:**
→ See [RELEASES.md](RELEASES.md) sections:
- "Creating a Release" (Automated method recommended)
- "Release Checklist"

**For release notes templates:**
→ See [RELEASE-NOTES-TEMPLATE.md](RELEASE-NOTES-TEMPLATE.md)

**For general info:**
→ See [INDEX.md](INDEX.md)

**For historical processes:**
→ See `.development/archive/releases/RELEASES-QUICKSTART.md` or `RELEASES-FAQ.md`

## Quality Impact

✅ **Reduced cognitive load:** 3 core documents instead of 6 scattered guides  
✅ **Single source of truth:** RELEASES.md authoritative reference  
✅ **Better discoverability:** INDEX.md clearly points to what you need  
✅ **Preserved history:** Archives available for legacy support  

## Backwards Compatibility

- All active URLs remain the same (documents in same locations)
- Older releases can still be found via git history and GitHub Releases page
- No broken links in existing documentation
- Users won't notice the change

---

**Consolidated by:** v0.7.0 documentation audit  
**Date:** February 18, 2026  
**Status:** Released in [DEVELOPMENT.md](../../DEVELOPMENT.md) v0.7.0 update
