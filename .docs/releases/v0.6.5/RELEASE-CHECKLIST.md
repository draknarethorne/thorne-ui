# v0.6.5 Release Checklist

**Status:** In Progress  
**Release Date:** February 18, 2026  
**Previous Release:** v0.6.4

---

## ✅ Release Prep

- [x] Update `VERSION` to `0.6.5`
- [x] Add `v0.6.5` entry in `README.md` Version History
- [x] Update release references in docs (`.docs/releases/*`, `.docs/VERSION-MANAGEMENT.md`)
- [x] Create release notes folder `.docs/releases/v0.6.5/`
- [ ] Run markdown link scan (`python .bin/scan_links.py`)
- [ ] Confirm clean git status (only intended files changed)
- [ ] Commit release prep changes
- [ ] Tag release (`v0.6.5`)
- [ ] Push branch + tag
- [ ] Verify release workflow in GitHub Actions
- [ ] Verify assets and notes in GitHub Releases

---

## 🔁 Canonical Release Commands

```bash
# 1) Commit release prep
git add VERSION README.md DEVELOPMENT.md .docs/VERSION-MANAGEMENT.md .docs/releases
git commit -m "chore(release): prepare v0.6.5"

# 2) Push branch commit
git push origin feature/stat-icons-v0.7.0

# 3) Tag and push
git tag -a v0.6.5 -m "Release v0.6.5: Spellbook/cast polish, Thorne options sync workflow, and icon variant refresh"
git push origin v0.6.5
```

---

## 📌 Notes

- This release is intentionally based on the current feature branch per maintainer request.
- `v0.6.4` comments are explicitly preserved and referenced in v0.6.5 notes.
