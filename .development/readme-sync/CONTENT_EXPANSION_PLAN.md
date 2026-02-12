# Options Window Content Expansion Plan (v100% Compliance)

**Status**: After checker fix: 27 Properly Documented, 17 Needs Deep Analysis, 2 No XML  
**Goal**: All 44 variants (46 exclude 2 no-XML) with meaningful XML-specific details  
**Strategy**: High-impact first, systematic expansion with detailed content

---

## Priority 1: High-Impact Windows (18 variants, 8 windows)

These are the most-used UI components. They need comprehensive documentation with XML element inventory,  layout diagrams, color schemes, and usage patterns.

### 1.1 Player Window (4 variants)

**Current Status**: 
- Default (124 lines): Purpose ✓, Features ✓, Specifications ✓, Layout ✗
- Standard (105 lines): Similar basic structure
- Pet Bottom (124 lines): Similar
- [+1 more]: Similar

**What's Needed**:
Each variant needs detailed XML element breakdown showing:
- All EQType references (HP, Mana, AC, Weight, AA, etc.)
- Position/size for major components
- Button grid layout with pagination info
- Color scheme and styling details
- Modifications from base Player window

**Content Template for Each**:
1. Purpose (specific to variant)
2. Key Features (4-6 bullets specific to layout differences)
3. Specifications (gauge sizes, window dimensions, etc.)
4. Visual Layout (ASCII diagram of the layout)
5. Element Inventory (table: Element | ScreenID | EQType | Position | Size | Purpose)
6. Color Scheme (RGB values for health/mana/AC)
7. Modifications (changes from standard)
8. Installation & Usage
9. Comparison with other variants (quick reference table)

**Example Element Inventory Entry**:
```
| HP Gauge | ASP_PlayerHP | 1 | (X=5, Y=18) | 156×12px | Primary health indicator |
| Mana Gauge | ASP_PlayerMana | 2 | (X=5, Y=30) | 156×6px | Mana bar (compact) |
| AC Display | ASP_PlayerAC | 60 | (X=165, Y=20) | 40×12px | Armor Class value |
```

**Effort**: 4-5 hours for all 4 variants with detailed XML cross-reference

---

### 1.2 Target Window (5 variants)

**Current Status**:
- Default (basic): Needs expansion
- Standard (basic): Needs expansion
- Player and Pet Gauges (88 lines): Good structure, add element inventory
- Player Gauges and Weight (147 lines): Already comprehensive
- Player HP and Mana Gauges (needs assessment): Basic?

**What's Needed**:
- Target information display layout (table headers, column widths)
- HP/Mana gauge positioning (different for each variant)
- Target buff/debuff slot layout
- Compare with Player window to show differences
- EQType references for target-specific elements

**Content Priority**: High - Target is critical for gameplay
**Effort**: 3-4 hours for all 5 variants

---

### 1.3 Inventory Window (3 variants)

**Current Status**:
- Default (no assessment yet)
- Standard (no assessment yet)
- Dark Slots and Color Weapons: **NO XML** (keep as-is, reference only)

**What's Needed**:
- Container grid layout (slots × rows × columns)
- Item positioning math
- Equipment slots section
- Stack display details
- Drag-and-drop mechanics documentation

**Content Priority**: High - Inventory is critical
**Effort**: 3 hours for 2 variants

---

### 1.4 Pet Window (3 variants)

**Current Status**:
- Default (needs assessment)
- Standard (250 lines): Comprehensive but needs structuring
- Tall Gauge (94 lines): Good structure, needs more detail

**What's Needed**:
- Gauge height comparison table
- Button layout for attack/follow/guard/dismiss/sit
- Pet name display styling
- Comparison matrix between all 3 variants

**Content Priority**: High - Pet Window commonly used
**Effort**: 2 hours for all 3 variants (mostly restructuring)

---

### 1.5 Actions Window (3 variants)

**Current Status**:
- Default (209 lines): **Excellent** - has element inventory, layout diagram, all details
- Standard (163 lines): Good but less detail than Default
- Bags and Inventory (113 lines): Good structure, less detail

**What's Needed**:
- Port element inventory table from Default to other variants
- Show layout differences between dual-tab vs single-tab
- Show differences in button counts and pagination

**Content Priority**: Medium - Already quite good
**Effort**: 1-2 hours to synchronize detail level

---

### 1.6 Group Window (3 variants)

**Current Status**:
- Default (no assessment)
- Standard (149 lines): Has Purpose, Features, Specifications - good baseline
- Large Gauges: **NO XML** (reference only)

**What's Needed**:
- Member list grid layout (rows × columns)
- HP gauge sizing and positioning for each member
- Class color coding documentation
- Buff slot display

**Content Priority**: Medium - Important for group play
**Effort**: 2 hours for 2 variants

---

### 1.7 Hotbutton Window (4 variants)

**Current Status**:
- All 4: 120-138 lines, basic to good structure
- Four Rows: Fixed path references
- Two Rows: Similar
- Standard: Similar
- Default: Similar

**What's Needed**:
- Button grid layout for each variant (specifically: rows × columns)
- Gem slot positioning (for casters)
- Page count info
- Layout diagram for each variant
- Page vs Page control positioning

**Content Priority**: Medium-High - Used constantly
**Effort**: 2-3 hours for all 4 variants

---

### 1.8 Merchant/Vendor Window (4 variants)

**Current Status**:
- All have basic structure (120-140 lines)
- Mix of good and minimal detail

**What's Needed**:
- Merchant list positioning
- Item grid layout (columns, rows)
- Item slot sizing
- Price display location
- Buy/Sell buttons positioning

**Content Priority**: Medium - Used frequently
**Effort**: 2-3 hours for all 4 variants

---

## Priority 2: Medium-Impact Windows (16 variants, 5 windows)

These are important but less frequently accessed than Priority 1.

### 2.1 Selector Window (3 variants)
- **Content needed**: Spell/combat ability selector grid layout, selection mechanics
- **Effort**: 1.5 hours

### 2.2 Skin/Theme Window (3 variants)
- **Content needed**: Theme preview display, selection grid, color palette display
- **Effort**: 1.5 hours

### 2.3 Spellbook Window (2 variants)
- **Content needed**: Spell grid layout, gem slots, memorization mechanics
- **Effort**: 1 hour

### 2.4 Loot Window (3 variants)
- **Current**: Partially improved, needs consistency
- **Content needed**: Loot list grid, item positioning, expansion options
- **Effort**: 1.5 hours

### 2.5 Animations Window (2 variants)
- **Current**: 1 has good detail, Default is minimal
- **Content needed**: Animation type reference, timing info
- **Effort**: 1 hour

---

## Priority 3: Lower-Impact/Specialized Windows (12 variants, 6+ windows)

Buff, Casting, Combat Skills, and others.

### 3.1 Buff Window
- **Content needed**: Buff/debuff slot layout, duration display, icon positioning

### 3.2 Casting/Progress Windows  
- **Content needed**: Cast bar mechanics, spell name display, progress indicator

### 3.3 Combat Skills Window
- **Content needed**: Command list layout, skill organization

### 3.4+ Others
- Similar approach for remaining windows

---

## Implementation Strategy

### Phase 1: Fix Checker (DONE ✅)
- ✅ Eliminate false positives
- ✅ Establish baseline assessment

### Phase 2: High-Impact Expansion (PRIORITIZED)
1. **Actions** (1-2 hours): Port element inventory to all variants
2. **Player** (4-5 hours): Create detailed element inventory for all 4
3. **Target** (3-4 hours): Cross-reference with Player, detail all 5 variants
4. **Inventory** (3 hours): Detailed grid layout documentation
5. **Pet** (2 hours): Comparison matrix + restructure
6. **Group** (2 hours): Member list and gauge layout
7. **Hotbutton** (2-3 hours): Layout diagrams for each variant
8. **Merchant** (2-3 hours): Grid and button positioning

**Phase 2 Total**: ~30 hours for 33 variants

### Phase 3: Medium-Impact (SCHEDULED)
8 variants × 30-40 min average = 4-5 hours

### Phase 4: Lower-Impact (OPPORTUNISTIC)
Remaining variants, time permitting

---

## Content Quality Standards

### Minimum for "Properly Documented" (100% compliance):
✓ Metadata (File, Version, Last Updated, Status, Author)  
✓ Purpose section (2-4 sentences specific to variant)  
✓ Key Features (4-6 bullets showing variant-specific differences)  
✓ Specifications table (10+ properties)  
✓ One detailed section (layout diagram OR element inventory OR color scheme)  
✓ Installation instructions  
✓ 100+ non-empty lines of meaningful content  

### "Excellent" Content (publication-quality):
✓ All Minimum requirements PLUS:  
✓ Multiple detail sections (element inventory + layout + colors)  
✓ Comparison tables with other variants  
✓ Usage recommendations  
✓ Technical XML depth (EQTypes, ScreenIDs, positioning)  
✓ 150-200+ lines with high information density  

### Target Distribution:
- **Excellent (publication-ready)**: High-impact windows (Priority 1)
- **Good (fully compliant)**: Medium-impact windows (Priority 2)
- **Acceptable (minimum threshold)**: Lower-impact windows (Priority 3)

---

## Content Reference Template

Each variant should have this structure:

```markdown
# [Window Name] - [Variant Name] Variant

**File**: [EQUI_*.xml](./EQUI_*.xml)  
**Version**: X.Y.Z  
**Last Updated**: [Date]  
**Status**: ✅ Active - [Brief description]  
**Author**: Draknare Thorne  

---

## Purpose
[2-4 sentences explaining what this variant does differently/better]

**Key Features**:
- Feature 1 with detail
- Feature 2 with detail
- etc. (4-6 items)

---

## Specifications

| Property | Value |
|----------|-------|
| ... | ... |

---

## Visual Layout / Element Inventory / Color Scheme

[Technical details specific to variant]

---

## Modifications (if variant)
[Changes from base/default variant]

---

## Installation
## Usage / Testing
## See Also
```

---

## Success Criteria for v100% Compliance

- [ ] 0 Format/Content Issues
- [ ] 0 Incomplete Documentation
- [ ] 27+ Properly Documented
- [ ] 17 Needs Deep Analysis → all have clear structure and 100+ lines
- [ ] 2 No XML retained as reference docs
- [ ] All variants have meaningful XML-specific details
- [ ] High-impact windows have element inventory tables
- [ ] Checker validates with no false positives
- [ ] All content aligned with actual XML files
- [ ] Cross-window comparisons documented where applicable

---

## Notes

- Actions/Default is an **excellent example** of desired detail level - use as template
- Pet/Standard and Target windows already have good structure
- Checker fix eliminates false positives - now all flags are real content gaps
- Target: Complete high-priority expansion within one session
- Remaining variants can be refined iteratively
