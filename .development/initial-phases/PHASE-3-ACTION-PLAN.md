# Phase 3 Action Plan - README Fixes & Expansion

**Status**: Ready for Execution  
**Date**: February 3, 2026  
**Items**: 9 Format/Content Issues + 13 Deep Analysis files + 2 Missing XML

---

## Quick Issue Summary

### FORMAT/CONTENT ISSUES (Priority: HIGH - 9 items)

These have structural or metadata problems that block proper usage:

| # | File | Issue | Fix Type | Effort |
|---|------|-------|----------|--------|
| 1 | Actions/Bags and Inventory | Missing "Key Features" section | Add section | 15 min |
| 2 | Animations/Drak Theme Gauges | Missing File, Version, all main sections | Rebuild structure | 30 min |
| 3 | Hotbutton/Four Rows | File reference format wrong | Auto-fix + verify | 5 min |
| 4 | Loot/Large Loot | Missing File, Version, sections | Rebuild structure | 30 min |
| 5 | Merchant/Large Inv & Bags | File reference format wrong | Auto-fix + verify | 5 min |
| 6 | Pet/Standard | Full path issue, missing all metadata | Rebuild completely | 30 min |
| 7 | Pet/Tall Gauge | Missing Specifications section | Add section | 15 min |
| 8 | Target/Player & Pet | Missing metadata and sections | Rebuild structure | 30 min |
| 9 | Target/Player HP & Mana | File reference format wrong | Auto-fix + verify | 5 min |

**Subtotal**: ~2.5 hours for all 9 fixes

---

### DEEP ANALYSIS NEEDED (Priority: MEDIUM - 13 items)

Structure is fine, but content is skeletal/generic. These can be improved incrementally:

- Actions/Standard (123 lines)
- Group/Standard (149 lines)
- Hotbutton/Standard (120 lines)
- Hotbutton/Two Rows (138 lines)
- Loot/Standard (129 lines)
- Merchant/Large inventory (124 lines)
- Merchant/Standard (140 lines)
- Player/Default (124 lines)
- Player/Pet Bottom (124 lines)
- Player/Standard (105 lines)
- Selector/Standard (140 lines)
- Skin/Slightly Taller (120 lines)
- Target/Player Gauges & Weight (147 lines)

**Target**: Expand 2-3 per month over next 4 months

---

### MISSING XML (Priority: MEDIUM - 2 items)

Decision needed: Keep as documentation-only or find/restore XML

- Group/Large Gauges (README exists, no XML)
- Inventory/Dark Slots (README exists, no XML)

**Action**: Investigate `.archive/` for missing files

---

## Execution Plan

### Phase 3a: Auto-Fix File References (10 minutes)

Files with format issues can be auto-fixed. Run this to fix 3 files automatically:

```bash
cd /d C:\TAKP\uifiles

# These have file reference format issues that auto-fix can resolve:
# - Hotbutton/Four Rows Inventory and Bags
# - Merchant/Large Inventory and Bags
# - Target/Player HP and Mana Gauges
# - Pet/Standard (partial - has also metadata issues)

python .bin/fix_readme_headers.py --verbose

# Expected output:
# [FIXED] Hotbutton\Four Rows Inventory and Bags\README.md
#   - Metadata field ordering
# [FIXED] Merchant\Large Inventory and Bags\README.md
#   - Metadata field ordering
# [FIXED] Target\Player HP and Mana Gauges\README.md
#   - Metadata field ordering

# Verify
python .bin/options_readme_checker.py | grep "FORMAT/CONTENT" -A 20
```

---

### Phase 3b: Fix Actions/Bags and Inventory (15 minutes)

**File**: `thorne_drak/Options/Actions/Bags and Inventory/README.md`

**Issue**: Missing "Key Features" section

**Fix**:
1. Read current file to understand its content
2. Extract key features from the existing text
3. Create proper "Key Features" bulleted list
4. Run checker to verify

```bash
# Check current structure
code "thorne_drak/Options/Actions/Bags and Inventory/README.md"

# Verify after fix
python .bin/options_readme_checker.py --verbose | grep "Bags and Inventory"
# Should show: [OK] PROPERLY DOCUMENTED
```

---

### Phase 3c: Fix Pet/Tall Gauge (15 minutes)

**File**: `thorne_drak/Options/Pet/Tall Gauge/README.md`

**Issue**: Missing "Specifications" section

**Fix**:
1. Read XML to extract specification details
2. Create specifications table
3. Add to README between Key Features and Visual Layout

```bash
# Examine XML structure
code thorne_drak/Options/Pet/Tall\ Gauge/EQUI_PetInfoWindow.xml

# Update README
code "thorne_drak/Options/Pet/Tall Gauge/README.md"
# Add specifications table after Key Features

# Verify
python .bin/options_readme_checker.py --verbose | grep "Tall Gauge"
```

---

### Phase 3d: Rebuild Animations/Drak Theme Gauges (30 minutes)

**File**: `thorne_drak/Options/Animations/Drak Theme Gauges/README.md`

**Issues**: 
- Missing metadata (File, Version)
- Missing Purpose, Key Features, Specifications sections

**Fix Approach**:

```bash
# 1. Check current content length
wc -l "thorne_drak/Options/Animations/Drak Theme Gauges/README.md"

# 2. Read the file to see what's there
code "thorne_drak/Options/Animations/Drak Theme Gauges/README.md"

# 3. Examine corresponding XML
code thorne_drak/Options/Animations/Drak\ Theme\ Gauges/EQUI_Animations.xml

# 4a. Option A: Use auto-generator to create skeleton
python .bin/generate_skeletal_readme.py --window Animations --variant "Drak Theme Gauges" --xml EQUI_Animations.xml --dry-run

# (Review output, decide if fully replace or merge)

# 4b. Option B: Manually add missing sections to existing file
# Keep useful content, add missing metadata and sections

# 5. Verify
python .bin/options_readme_checker.py --verbose | grep "Drak Theme"
```

---

### Phase 3e: Rebuild Loot/Large Loot (30 minutes)

**File**: `thorne_drak/Options/Loot/Large Loot/README.md`

**Issues**:
- Missing File, Version metadata
- Missing Purpose, Key Features, Specifications sections

**Same process as Phase 3d**:

```bash
# 1. Read current file
code "thorne_drak/Options/Loot/Large Loot/README.md"

# 2. Read XML to understand it
code thorne_drak/Options/Loot/Large\ Loot/EQUI_LootWnd.xml

# 3. Either regenerate with skeleton or manually add sections
python .bin/generate_skeletal_readme.py --window Loot --variant "Large Loot" --xml EQUI_LootWnd.xml --dry-run

# 4. Verify
python .bin/options_readme_checker.py --verbose | grep "Large Loot"
```

---

### Phase 3f: Fix Merchant/Large Inventory and Bags (30 minutes)

**File**: `thorne_drak/Options/Merchant/Large Inventory and Bags/README.md`

**Issues**:
- Missing File, Version metadata
- Missing Key Features, Specifications sections

**Same approach**: Manually add or regenerate

```bash
# Read and understand
code "thorne_drak/Options/Merchant/Large Inventory and Bags/README.md"
code thorne_drak/Options/Merchant/Large\ Inventory\ and\ Bags/EQUI_MerchantWnd.xml

# Fix
python .bin/generate_skeletal_readme.py --window Merchant --variant "Large Inventory and Bags" --xml EQUI_MerchantWnd.xml --dry-run

# Verify
python .bin/options_readme_checker.py --verbose | grep "Large Inventory"
```

---

### Phase 3g: Fix Pet/Standard (30 minutes)

**File**: `thorne_drak/Options/Pet/Standard/README.md`

**Issues**:
- Uses full path instead of local link
- Missing all metadata fields (File, Version, Last Updated, Status, Author)

**Fix Approach**:

```bash
# 1. Check current state
code "thorne_drak/Options/Pet/Standard/README.md"

# 2. Complete rebuild might be needed
python .bin/generate_skeletal_readme.py --window Pet --variant "Standard" --xml EQUI_PetInfoWindow.xml --dry-run

# 3. Option: If current content is valuable, manually fix
#    - Update file reference to [EQUI_PetInfoWindow.xml](./EQUI_PetInfoWindow.xml)
#    - Add metadata fields (Version, Last Updated, Status, Author)

# 4. Verify + read XML to ensure content accuracy
python .bin/options_readme_checker.py --verbose | grep "Pet/Standard"
```

---

### Phase 3h: Fix Target/Player and Pet Gauges (30 minutes)

**File**: `thorne_drak/Options/Target/Player and Pet Gauges/README.md`

**Issues**:
- Missing all metadata (File, Version, Last Updated, Status, Author)
- Missing Purpose, Key Features, Specifications sections

```bash
# Read current
code "thorne_drak/Options/Target/Player and Pet Gauges/README.md"

# Read XML
code thorne_drak/Options/Target/Player\ and\ Pet\ Gauges/EQUI_TargetWindow.xml

# Regenerate or manually fix
python .bin/generate_skeletal_readme.py --window Target --variant "Player and Pet Gauges" --xml EQUI_TargetWindow.xml --dry-run

# Verify
python .bin/options_readme_checker.py --verbose | grep "Player and Pet"
```

---

### Phase 3i: Investigate Missing XML Files (20 minutes)

**Files**:
- Group/Large Gauges (README exists, no XML)
- Inventory/Dark Slots and Color Weapons (README exists, no XML)

**Investigation**:

```bash
# 1. Search .archive for possibly deleted files
ls -la C:\TAKP\uifiles\.archive\ | grep -i "group\|inventory"

# 2. Search git history
git log --all --diff-filter=D --summary | grep -i "Large Gauges\|Dark Slots"

# 3. Decide:
#    a) If XML can be recovered: restore from archive/git
#    b) If XML is gone: Keep README as variant reference (mark as documentation-only)
#    c) If not needed: Remove README to clean up repo

# 4. If keeping as documentation-only, add note to README:
#    "**Status**: Documentation-only reference (XML variant not currently maintained)"

# 5. Update checker to recognize this state
```

---

## Execution Order

**Recommended Sequence** (for efficiency):

1. **Day 1 - Automatics (10 min)**
   - Phase 3a: Auto-fix file references (3 files)
   - Done: Hotbutton/4 Rows, Merchant/Large Inv, Target/HP-Mana

2. **Day 2 - Quick Wins (30 min)**
   - Phase 3b: Actions/Bags (15 min)
   - Phase 3c: Pet/Tall (15 min)
   - Done: 2 files properly documented

3. **Day 3 - XML Review & Rebuild (2 hours)**
   - Phase 3d: Animations (30 min)
   - Phase 3e: Loot/Large (30 min)
   - Phase 3f: Merchant/Large (30 min)
   - Phase 3g: Pet/Standard (30 min)

4. **Day 4 - Final Rebuild (30 min)**
   - Phase 3h: Target/Player & Pet (30 min)
   - Phase 3i: Missing XML Investigation (20 min)

**Total Time**: ~5 hours spread over 4 days

---

## Verification Checklist

After each phase, run:

```bash
# Check status
python .bin/options_readme_checker.py

# Should see improvement in counts:
# Before: Format/Content Issues: 9
# After each phase, count should decrease
```

**Expected Final State** (after all 9 fixes):
```
Orphaned/Improper:     0
Format/Content Issues: 0  ← Down from 9
Out of Sync:           0
Incomplete:            0
No XML Found:          0 or 2 (depending on missing XML decision)
Needs Deep Analysis:   13
Properly Documented:   24+ ← Up from 22
Total Issues:          46
```

---

## Next: Deep Analysis Phase (Month 2+)

After fixing all 9 issues, attack the 13 "Needs Deep Analysis" files:

**Monthly Goals**:
- Expand 2-3 files per month
- Target: Complete all 46 by Month 4

**Expansion Process**:
1. Read actual XML in detail
2. Extract technical specifications from XML attributes
3. Document actual behavior and features observed
4. Add detailed layout diagrams or tables
5. Note any quirks or special handling

**High-Value Targets** (start here):
- Player/Standard (core window, used everywhere)
- Target/Standard (core window, used everywhere)
- Group/Standard (core window, used everywhere)
- Hotbutton/Standard (core functionality)

---

**Next Step**: Ready to execute Phase 3a (auto-fix) whenever you confirm.
