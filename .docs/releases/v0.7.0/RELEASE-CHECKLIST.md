# v0.7.0 Release Checklist

**Status:** Ready to Publish  
**Release Date:** February 22, 2026  
**Previous Release:** v0.6.5

---

## ✅ Release Prep

- [x] Update `VERSION` to `0.7.0`
- [x] Add `v0.7.0` entry in `README.md` Version History
- [x] Update release references in docs (`.docs/releases/INDEX.md`)
- [x] Create release notes folder `.docs/releases/v0.7.0/`
- [ ] Run markdown link scan (`python .bin/scan_links.py`)
- [ ] Confirm clean git status (only intended files changed)
- [ ] Commit release prep changes
- [ ] Push release-prep branch updates
- [ ] Prepare PR merge into `main`
- [ ] Tag release (`v0.7.0`) after merge to `main`
- [ ] Push tag and verify GitHub Actions release workflow
- [ ] Verify assets and notes in GitHub Releases

---

## 🔁 Canonical Release Commands

```bash
# 1) Commit release prep
git add VERSION README.md .docs/releases/INDEX.md .docs/releases/v0.7.0
git commit -m "chore(release): prepare v0.7.0"

# 2) Push branch commit
git push origin feature/stat-icons-v0.7.0

# 3) Merge to main (PR or direct, per policy)
# 4) Tag and push from main tip
git tag -a v0.7.0 -m "Release v0.7.0: options modernization, slot pipeline foundation, and core thorne_drak consistency updates"
git push origin v0.7.0
```

---

## 📌 Notes

- This release intentionally centers **actual `thorne_drak` shipped output changes**.
- Slot/scripting foundation work is included to support long-term Options management and future releases.
