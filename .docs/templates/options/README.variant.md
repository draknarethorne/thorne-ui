# Thorne UI Options Variant README Template

This template defines the standard structure for variant documentation within the Options system.
Use this as a reference when creating or updating variant README files.

---

## REQUIRED STRUCTURE

### Header Section (REQUIRED - MUST INCLUDE ALL FIELDS)

```markdown
# [Window Name] - [Variant Name] Variant

**File**: [EQUI_WindowName.xml](./EQUI_WindowName.xml)  
**Version**: X.Y.Z  
**Last Updated**: YYYY-MM-DD  
**Status**: ✅ [Status description]  
**Author**: Draknare Thorne
[OPTIONAL]: **Based On**: [Original authors/sources if derived]

---
```

**Header Field Requirements:**

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| Title | YES | `# [Window] - [Variant] Variant` | `# Player Window - AA and XP Bottom Variant` |
| File | YES | Markdown link to local XML: `[Name](./Name.xml)` | `[EQUI_PlayerWindow.xml](./EQUI_PlayerWindow.xml)` |
| Version | YES | SemVer format X.Y.Z | `1.0.0` or `1.1.2` |
| Last Updated | YES | YYYY-MM-DD format | `2026-02-03` |
| Status | YES | Start with emoji + description | `✅ Active variant` or `⚠️ Experimental` |
| Author | YES | Always "Draknare Thorne" (current maintainer) | `Draknare Thorne` |
| Based On | CONDITIONAL | Include if derived from other work | `Based on ODAKU original by Nanan, modified by Brujoloco` |

**Important Notes:**
- File reference MUST be local markdown link, NOT full path
- NEVER use: `thorne_drak/Options/Merchant/Large Inventory/EQUI_MerchantWnd.xml`
- ALWAYS use: `[EQUI_MerchantWnd.xml](./EQUI_MerchantWnd.xml)`
- Variant directory location is understood from file path; no need to repeat it
- If file was created by adapting another author's work, give credit in "Based On"

---

### Purpose Section (REQUIRED)

```markdown
## Purpose

[1-2 sentence overview of what this variant does]

[Key differentiators from Standard variant]

**Key Features**:

- [Feature 1 with brief explanation]
- [Feature 2 - major differentiator]
- [Feature 3 - what makes this variant unique]
- [Feature 4 - functionality or visual change]
- [Feature 5 - optional advanced feature]

[Optional: Design philosophy or use cases if relevant]
```

**Requirements:**
- Start with clear, concise purpose statement
- Explain why/when to use this variant
- List 5-10 bullet-point features
- Each feature should explain WHAT it does, not just name it
- Can include sub-items with `- -` if nested structure helps

**Example (Good):**
```markdown
## Purpose

The "Large Inventory Variant" Merchant window provides an expanded vendor interface with more items visible at once without integrated player inventory display. Use this variant when trading frequently with merchants and want to minimize scrolling.

**Key Features**:

- **Expanded Merchant Display**: 2-column grid showing 80+ items without excessive scrolling
- **Large Window Height**: 600+ pixels of merchant slot visibility
- **Vertically Resizable**: Drag bottom edge to show even more items
- **Tab System**: Separate Items/Buy/Sell tabs for organized workflow
- **Compact Width**: Only 125px wide to leave screen space for other windows
```

---

### Specifications Section (REQUIRED)

```markdown
## Specifications

| Property | Value |
|----------|-------|
| Window Size | [Width] × [Height] pixels (fixed/resizable) |
| Resizable | Yes/No (`Style_Sizable=true/false`) |
| Fadeable | Yes/No (`Style_Transparent=true/false`) |
| Screen ID | [SCREENID] |
| DrawTemplate | [WDT_Template] |
| Default Position | X=[num], Y=[num] |
| Titlebar | Yes/No (`Style_Titlebar=true/false`) |
| Closebox | Yes/No (`Style_Closebox=true/false`) |
| Minimizebox | Yes/No (`Style_Minimizebox=true/false`) |
| Border | Yes/No (`Style_Border=true/false`) |
| [Custom Property 1] | [Value] |
| [Custom Property 2] | [Value] |
```

**Requirements:**
- Extract technical properties directly from XML Screen definition
- Include window size (CX/CY) or note if dynamic
- Document resize capability
- Include all Style_* properties as Yes/No with XML value for reference
- Add window-specific properties (e.g., "Group Member Count: 5", "Merchant Slot Count: 80")
- Use markdown table format
- Values should be verifiable from XML file

**Data Sources:**
- Look at XML `<Screen>` tag attributes
- Look at Style definitions
- Look at major ScreenPiece definitions for dimensions

---

### Layout Overview Section (REQUIRED for variants >100 lines)

```markdown
## Layout Overview

### Window Hierarchy

[ASCII tree diagram or text description of element organization]

Example format:
```
WindowName (WidthxHeight)
├── Element1 (type, position, size)
│   ├── SubElement1a
│   └── SubElement1b
├── Element2 (type, position, size)
└── Element3 (type, position, size)
```

### Visual Diagram (Optional but Recommended)

[ASCII-art diagram showing window appearance]

Example:
```
┌─────────────────────────────────┐
│  Window Title                   │
├─────────────────────────────────┤
│ [Item 1] [Item 2] [Item 3]      │
│ [Item 4] [Item 5] [Item 6]      │
├─────────────────────────────────┤
│ [Button1] [Button2] [Button3]   │
└─────────────────────────────────┘
```
```

**Requirements:**
- Describe element positioning and nesting
- Include X/Y coordinates for major elements if important for layout
- Include dimensions if non-obvious
- Visual ASCII diagram strongly recommended
- Helps future developers understand structure without reading XML

---

## OPTIONAL SECTIONS

### Color Scheme (OPTIONAL - include if custom colors used)

```markdown
## Color Scheme

| Element | Color | RGB |
|---------|-------|-----|
| HP Gauge | Red | RGB(220, 0, 0) |
| Mana Gauge | Blue | RGB(100, 150, 255) |
| Pet Health | Green | RGB(51, 192, 51) |
| Text Labels | White | RGB(255, 255, 255) |
| Background | Dark Gray | RGB(64, 64, 64) |
```

**When to include:**
- Custom gauge colors (not default)
- Non-standard text colors
- Important visual styling choices
- Color consistency across multiple windows
```

---

### Modifications Section (OPTIONAL - include for recent changes)

```markdown
## Modifications

### Version 1.1.0 (February 3, 2026)

**Changes:**
- Updated mana gauge color from RGB(150,150,255) to RGB(100,150,255) for consistency
- Fixed pet gauge X positioning from X=16 to X=11
- Added weight display to header row

**Rationale:**
- Mana color standardization across all windows
- Alignment with Player and Group windows

**Previous Version**: See git commits [link or hash] for details
```

**When to include:**
- Recent version changes
- Major layout modifications
- Bug fixes documented
- Feature additions
- Help future developers understand evolution

---

### See Also / Cross-References (OPTIONAL)

```markdown
## See Also

- [Player Window - Standard](../../Player/Standard/README.md) - Main character stats display
- [Target Window - Player Gauges and Weight](../../Target/Player%20Gauges%20and%20Weight/README.md) - Complementary target display
- [Group Window - Standard](../../Group/Standard/README.md) - Group member monitoring
```

**When to include:**
- Related variant windows
- Complementary views
- Prerequisites or dependencies
- Similar functionality in other windows

---

### Design Philosophy (OPTIONAL - for experimental/unique variants)

```markdown
## Design Philosophy

This variant combines visual elements from:
- **Infiniti-Blue**: Gauge textures and styling
- **duxaUI**: Icon methodology for class/race representation
- **vert**: Vertical stat arrangement and layout approach

Goal: Create information-dense display without overwhelming users.
```

**When to include:**
- Experimental or custom variants
- Multi-source adaptations
- Unusual design decisions needing explanation
- Educational context for contributors

---

## VALIDATION CHECKLIST

When creating/updating a variant README, verify:

### Header (5 fields - ALL REQUIRED)
- [ ] Title: `# [Window] - [Variant] Variant`
- [ ] File: `[EQUI_Name.xml](./EQUI_Name.xml)` (local link)
- [ ] Version: SemVer format (X.Y.Z)
- [ ] Last Updated: YYYY-MM-DD format
- [ ] Status: `✅ Description`
- [ ] Author: `Draknare Thorne`
- [ ] Based On: Present if derived work (CONDITIONAL)

### Content (3 required + optional sections)
- [ ] Purpose: Clear explanation + Key Features bullets
- [ ] Specifications: Complete table with XML-verified properties
- [ ] Layout: Window hierarchy or ASCII diagram
- [ ] Optional sections as appropriate

### Quality Checks
- [ ] File references are local (not full paths)
- [ ] All XML-sourced values match actual file content
- [ ] Links to other variants work (if included)
- [ ] No orphaned sections or incomplete content
- [ ] Grammar and formatting consistent
- [ ] Date is current (not stale)
- [ ] Version number logical (relates to changes)

### Directory Structure
- [ ] README.md is in: `Options/[WindowName]/[VariantName]/`
- [ ] EQUI_*.xml file exists in same directory
- [ ] File path matches directory structure

---

## EXAMPLES BY CONTENT LENGTH

### Short Variant (80-120 lines)
- Simple Purpose + Features (5-10 feature bullets)
- Specifications table (10-12 rows)
- Minimal Layout (just brief description or simple ASCII)

### Standard Variant (120-200 lines)
- Purpose + Key Features (8-12 bullets)
- Full Specifications table (12-15 rows)
- Window Hierarchy tree (20-30 lines)
- Visual ASCII diagram (10-20 lines)

### Comprehensive Variant (200+ lines)
- Detailed Purpose + Design Philosophy
- Key Features (10-15 bullets) with sub-explanations
- Full Specifications table (15-20 rows)
- Detailed window hierarchy with coordinates
- Multiple visual diagrams
- Color scheme if custom
- Modifications history
- Cross-references to related windows

---

## COMMON MISTAKES TO AVOID

❌ **DON'T:**
- Use full `thorne_drak/Options/...` path in File field
- Forget to update Last Updated date
- Omit Author field
- Skip Specifications table
- Use vague feature descriptions ("better interface")
- Mix old version format with new format
- Leave placeholder text or TODOs in published files
- Reference XMLs that don't exist in the directory
- Omit Required sections
- Use absolute paths or file:// URLs in links

✅ **DO:**
- Use local markdown links: `[FileName.xml](./FileName.xml)`
- Update date every time you modify the file
- Always include all 5 header metadata fields
- Create complete Specifications table from XML
- Describe features with implementation details
- Be consistent in formatting and structure
- Verify all content before committing
- Test links work correctly
- Include all Required sections
- Use relative paths for cross-references

---

## UPDATES TO THIS TEMPLATE

This template is maintained at: `.docs/templates/options/README.variant.md`

When the standard changes:
1. Update this template
2. Update the checker validation rules
3. Note when/why in .docs/DEVELOPMENT.md
4. Apply retroactively to existing files over time

**Last Updated**: 2026-02-03  
**Maintainer**: Draknare Thorne (via automated tool development)
