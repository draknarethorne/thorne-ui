# README Standards Analysis - 15+ Variant Sample

## Sample Coverage

Reviewed **17 variant README files** across **10 different window categories**:

- Actions: 2 variants (Standard, Bags and Inventory)
- Group: 1 variant (Standard)
- Hotbutton: 2 variants (Standard, Four Rows Inventory and Bags)
- Inventory: 1 variant (Standard)
- Loot: 1 variant (Standard)
- Merchant: 3 variants (Standard, Large Inventory, Large Inventory and Bags)
- Pet: 2 variants (Standard, Tall Gauge)
- Selector: 2 variants (Standard, Vertical)
- Skin: 1 variant (Slightly Taller and Wider)
- Spellbook: 1 variant (Standard)
- Target: 4 variants (Standard, Player and Pet Gauges, Player Gauges and Weight, Player HP and Mana Gauges)
- Animations: 1 variant (Drak Theme Gauges - special case)
- Player: 2 variants (Standard, AA and XP Bottom)

---

## Header Format Analysis

### Pattern 1: Standard Modern Format (MOST COMMON)
**Used in: 12+ files**

```markdown
# [Window Name] - [Variant Name] Variant

**File**: `thorne_drak/Options/[Window]/[Variant]/EQUI_*.xml`  
**Version**: 1.0.0  
**Last Updated**: February 3, 2026  
**Status**: ✅ Status description  
**Author**: Draknare Thorne
```

**Examples:**
- Actions/Standard/README.md
- Merchant/Standard/README.md
- Target/Player Gauges and Weight/README.md
- Hotbutton/Standard/README.md

---

### Pattern 2: Asset Documentation Format (UNIQUE)
**Used in: Animations/Drak Theme Gauges/README.md**

```markdown
# [Asset Type] — [Description]

**Document**: [Description]  
**Status**: ACTIVE  
**Last Updated**: January 25, 2026  
**Author**: Draknare Thorne
```

Special case for texture/asset documentation vs window documentation.

---

### Pattern 3: Minimal/Skeleton Format
**Used in: 2 files**

Examples:
- Target/Player and Pet Gauges/README.md (35 lines, minimal)
- Pet/Tall Gauge/README.md (shortened version)

```markdown
# [Window Name] - [Variant Name] Variant

**File**: `thorne_drak/Options/[Path]/EQUI_*.xml`  
**Version**: X.Y.Z  
**Last Updated**: [Date]  
**Status**: ✅ [Status]  
**Author**: [Author] (if applicable: based on/modified from original by [Original Author])
```

---

### Pattern 4: Full Path Reference (PROBLEMATIC)
**Used in: 3 files**

```markdown
**File**: `thorne_drak/EQUI_MerchantWnd.xml`
```

**Occurrences:**
- Hotbutton/Four Rows Inventory and Bags/README.md
- Merchant/Large Inventory and Bags/README.md

**Problem**: References full `thorne_drak/` path instead of local directory. Confusing when file is in `Options/Merchant/[Variant]/`.

---

## Content Structure Analysis

### Section Headings Present (Ranked by Frequency)

1. **Purpose** (16/17 files) - Universal section
   - Describes what the variant is for
   - Content ranges 5-15 lines
   - Often includes key features in separate subsection

2. **Key Features** (15/17 files) - Core content
   - Bulleted list of 5-10 features
   - Some use "Features", some use "Key Features"
   - Content ranges 10-25 lines

3. **Specifications** (14/17 files) - Technical details
   - Formatted as markdown table
   - Properties: Window Size, Resizable, Fadeable, etc.
   - 8-20 rows per table

4. **Layout Overview** (12/17 files) - Visual documentation
   - ASCII diagrams or text-based visualizations
   - Window hierarchy trees OR layout diagrams
   - Some very detailed (100+ lines), some minimal

5. **Modifications** (4/17 files) - Change history
   - Version-specific updates (v1.1.0 changes)
   - Recent edits documented
   - Example: Mana color changes, positioning adjustments

6. **See Also** / Cross-references (3/17 files)
   - Links to related windows
   - Example: Pet Window references Group/Target windows

7. **Color Scheme** (2/17 files)
   - RGB values for gauges/elements
   - Example: "HP: Red RGB(255,0,0)"

---

## Author Attribution Patterns

### Format Variations:

**Simple:**
```markdown
**Author**: Draknare Thorne
```

**With Credit:**
```markdown
**Author**: Draknare Thorne (based on Daciana/Brujoloco mods)
**Author**: Draknare Thorne (modified from original by Brujoloco)
```

**Legacy (2 files):**
```markdown
**Author**: Draknare Thorne (original variant by Nanan)
**Based on**: ODAKU Pet Window, modified by Brujoloco for QQQuarm (Nov 6, 2023)
```

**Earliest examples** (Files from Jan 24, 2026):
- Hotbutton/Four Rows: References it as general EQUI_HotButtonWnd.xml
- Merchant/Large Inventory and Bags: References general MerchantWnd.xml
- These seem to be from a different generation before variant-specific docs

---

## File Reference Issues (Critical)

### Issue 1: Inconsistent File Path References

**Current approach in newer files (CORRECT):**
```markdown
**File**: `thorne_drak/Options/Target/Player Gauges and Weight/EQUI_TargetWindow.xml`
```

**Older approach (CONFUSING):**
```markdown
**File**: `thorne_drak/EQUI_MerchantWnd.xml`
```
When file is actually in: `Options/Merchant/Large Inventory and Bags/`

**Local reference (IDEAL):**
```markdown
**File**: [EQUI_TargetWindow.xml](./EQUI_TargetWindow.xml)
```

### Issue 2: Wrong XML References

Identified cases where README references wrong XML file:
- **Player/Standard/README.md** - Says `EQUI_PlayerNotesWindow.xml` (it's the notes window, not player window)
- Directory contains BOTH XMLs - documentation unclear which is primary

### Issue 3: Special Cases

**Animations/Drak Theme Gauges:**
- Doesn't document a window, documents texture assets
- Entirely different structure justified
- No EQUI_*.xml file in directory (references external TGA files)

---

## Line Count Distribution

```
File Type              | Count | Avg Lines | Range
─────────────────────────────────────────────────
Detailed Content       | 10    | 200+      | 162-512 lines
Standard Documented    | 4     | 140       | 120-165 lines
Minimal/Skeleton       | 3     | 60        | 35-80 lines
─────────────────────────────────────────────────
TOTAL SAMPLE          | 17    | 165 avg   | 35-512 lines
```

---

## Best Practices Observed

### ✅ Strong Examples (Most consistent & detailed)

1. **Target/Player Gauges and Weight** (194 lines)
   - Clear file reference with options path
   - Detailed Purpose section
   - Comprehensive Specifications table
   - ASCII layout diagram
   - Modification history (v1.1.0)
   - Good cross-window references

2. **Group/Standard** (194 lines)
   - Consistent header format
   - Clear "Key Modifications (v1.1.0)" section
   - Detailed positioning specs
   - Before/after comparison of changes

3. **Hotbutton/Standard** (161 lines)
   - Based on previous authors (Daciana/Brujoloco)
   - Clear hierarchical layout
   - Specification table complete
   - Good ASCII visualization

4. **Merchant/Standard** (185 lines)
   - Compact but complete
   - Clear purpose differentiating from variants
   - Good specifications
   - Simple ASCII layout

5. **Player/AA and XP Bottom** (206 lines)
   - Design philosophy explicitly stated
   - Detailed feature descriptions
   - Clear visual layout diagrams
   - Version/status clearly marked

### ⚠️ Problematic Examples

1. **Hotbutton/Four Rows Inventory and Bags** (512 lines)
   - File reference uses `thorne_drak/EQUI_HotButtonWnd.xml` (full path)
   - Doesn't clearly reference Options path
   - VERY detailed (might be older comprehensive doc)

2. **Merchant/Large Inventory and Bags** (446 lines)
   - File reference uses `thorne_drak/EQUI_MerchantWnd.xml` (full path)
   - Older style - pre-Options organization
   - Tab/feature structure different from newer variants

3. **Target/Player and Pet Gauges** (35 lines - INCOMPLETE)
   - Minimal content
   - Unclear structure
   - Modern Format header but skeleton content

4. **Pet/Tall Gauge** (shortened version)
   - Previously more detailed
   - Now condensed
   - Less layout/visual documentation

---

## Recommendations for Standard Template

### REQUIRED Header Format

```markdown
# [Window Name] - [Variant Name] Variant

**File**: [EQUI_FileName.xml](./EQUI_FileName.xml)  
**Version**: X.Y.Z  
**Last Updated**: YYYY-MM-DD  
**Status**: ✅ [Status description]  
**Author**: Draknare Thorne
[OPTIONAL]: **Based On**: [Original authors/source if applicable]

---
```

### Key Points:

1. **File Reference**: Use markdown link to local file, shows which variant we're documenting
2. **Always include Version & Date**: For tracking changes
3. **Author field**: Always "Draknare Thorne" as current maintainer
4. **Based On**: Add IF file was derived from other authors' work (preserve credit)
5. **Location Reference**: Optional but helpful: "Options/[Window]/[Variant]/" at top or in metadata

---

## REQUIRED Content Sections (Minimum)

1. **Purpose** (required)
   - What this variant is for
   - How it differs from Standard
   - Use cases

2. **Key Features** (required)
   - 5-10 bulleted features
   - Explain differentiators

3. **Specifications** (required)
   - Markdown table format
   - Window size, resizable, adorns, etc.
   - Standard keys allow comparison across variants

4. **Layout Overview** (recommended 100+ lines)
   - ASCII diagrams or text descriptions
   - Window hierarchy if complex
   - Visual reference for development

### OPTIONAL Content Sections

- **Modifications** - Version history of changes
- **Color Scheme** - RGB values for custom colors
- **See Also** - Links to related windows
- **Design Philosophy** - Why designed this way
- **Credits** - Additional contributors

---

## Standards to Enforce

### ✅ DO

- Use local markdown links for XML files: `[EQUI_FileName.xml](./EQUI_FileName.xml)`
- Include "Options/[Window]/[Variant]/" context clearly
- Preserve credit to original authors with "Based On"
- Use standard header with all 5 required metadata fields
- Include Purpose, Key Features, Specifications, Layout sections
- Use version numbers and dates
- Add modification history for recent changes
- Use proper markdown formatting (tables, code blocks, etc.)

### ❌ DON'T

- Don't reference full `thorne_drak/Options/...` paths in File field
- Don't omit Version or Author
- Don't leave out Purpose or Features
- Don't forget to include Options path context
- Don't consolidate all variants into one README
- Don't lose credit to previous authors
- Don't mix old format (full paths) with new format (local links)

---

## Current Status Summary

| Category | Count | Status |
|----------|-------|--------|
| Well-Documented (150+ lines) | 10 | ✅ Good |
| Adequately Documented (80-150) | 4 | ⚠️ Okay |
| Incomplete/Minimal (<80) | 3 | ❌ Needs work |
| **Total Reviewed** | **17** | - |

---

## Implementation Strategy

### Phase 1: Standardize Headers (Quick Fix)
- Update all file references to use local markdown links
- Add missing Version/Author fields
- Add "Based On" where applicable
- Normalize date formats

### Phase 2: Preserve Content
- Keep existing Purpose/Features/Specs sections
- Don't regenerate from scratch
- Just reformat and reorganize into standard structure

### Phase 3: Identify Gaps
- Find incomplete sections (< 80 lines) needing expansion
- Flag sections that need updating (old version dates, obsolete descriptions)
- Identify files needing technical review (older docs that might reference old code)

### Phase 4: Batch Corrections
- Use multi-file replacements for header standardization
- Group similar issues by window type
- Test markdown rendering to verify links work

---

## Specific Files Needing Attention

### HIGH PRIORITY (Wrong/Confusing)
- Hotbutton/Four Rows Inventory and Bags - Full path reference
- Merchant/Large Inventory and Bags - Full path reference
- Player/Standard - References wrong XML (PlayerNotes vs Player)

### MEDIUM PRIORITY (Incomplete)
- Target/Player and Pet Gauges - Only 35 lines, minimal
- Pet/Tall Gauge - Seems cut down from original
- Skin/Standard - NO README (missing entirely)

### LOW PRIORITY (Technical Review)
- Hotbutton/Four Rows - Very long (512 lines), verify accuracy
- Merchant/Large Inventory and Bags - Very long (446 lines), verify accuracy
- Animations/Drak Theme Gauges - Different format (asset doc), verify completeness

---

