# Inventory Analysis Project - Execution Roadmap

**Date**: February 4, 2026  
**Project**: Comprehensive inventory window analysis across all community UI variants  
**Status**: RESEARCH PHASE STARTING

---

## Task Execution Order (Optimized for Impact)

### Phase 1: Quick Research (1 hour total)

**TASK 1A: Stat Icons - Identify Examples**
- [ ] Locate stat icon files in duxaUI directory
- [ ] List all found .tga texture files for icons
- [ ] Note file naming convention and size
- [ ] Document which windows use icons (Inventory, Player, Actions, etc.)
- [ ] Determine if icon graphics are standardized across mods

**TASK 1B: Stat Icons - Texture Loading Method**
- [ ] Read Target window XML (EQUI_TargetWindow.xml in default)
- [ ] Find oval gauge .tga texture loading pattern
- [ ] Compare to Animations.xml (global vs. embedded)
- [ ] Document the method for direct .tga loading
- [ ] Create reusable code template

**TASK 2: Race EQType Verification**
- [ ] Scan EQTYPES.md for Race references (likely none)
- [ ] Grep all non-thorne_ EQUI_*.xml files for "Race" text
- [ ] Check if any EQType is bound to race display
- [ ] Document findings
- [ ] Propose solution if EQType not available

**TASK 3: Tribute Display Research**
- [ ] Grep all directories for "Tribute" implementations
- [ ] Look for EQType 121-123 usage in existing files
- [ ] Check if any mod displays Tribute as gauge
- [ ] Find if Tribute has associated EQType
- [ ] Document typical formatting/placement

**Deliverable**: Research summary memo with code examples

---

### Phase 2: Directory Analysis Template (1-2 hours)

**Create INVENTORY-ANALYSIS template**:
- [ ] Design consistent document format
- [ ] Create reusable sections for all directories
- [ ] Include visual layout diagrams
- [ ] Add comparison matrix fields
- [ ] Create example with 1-2 directories first

**Output**: Template + 1-2 example analysis documents

---

### Phase 3: Deep Analysis (2-3 hours)

**Analyze Each Directory**:
- [ ] default/ - baseline/reference implementation
- [ ] duxaUI/ - community variant
- [ ] Infiniti-Blue/ - specific design approach
- [ ] QQ/ - alternative layout
- [ ] vert/ - vertical variant specifics
- [ ] zeal/ - Zeal-specific features

**Per Directory**:
- Read EQUI_Inventory.xml (note window size, element count)
- Identify subwindow usage patterns
- Map equipment layout (anatomical vs. scattered)
- Document stat display approach
- Note icon usage (yes/no/partial)
- Check gauge implementations
- Find unique features

**Deliverable**: 6 consistent analysis documents

---

### Phase 4: Synthesis (1 hour)

**Create Recommendations Document**:
- [ ] Synthesize findings from all 6 directories
- [ ] Identify best practices
- [ ] Highlight unique innovations
- [ ] Assess implementation complexity
- [ ] Create priority matrix

**Deliverable**: INVENTORY-REDESIGN-RECOMMENDATIONS.md

---

### Phase 5: Agent Documentation (30 min)

**Update ThorneUI.agent.md**:
- [ ] Add "Community Resources" section
- [ ] Document icon implementations patterns
- [ ] Add comparative analysis guidance
- [ ] Include texture loading method
- [ ] Reference all UI variants
- [ ] Add tool capabilities (pylance, github)

**Deliverable**: Enhanced agent.md with cross-references

---

## Quick Research Starting Points

**For TASK 1 (Stat Icons)**:
```bash
# Find .tga files in duxaUI
find c:\TAKP\uifiles\duxaUI -name "*icon*" -o -name "*stat*"

# Check Target window method
grep -n "tga\|Texture" c:\TAKP\uifiles\default\EQUI_TargetWindow.xml | head -20

# Find stat icon references
grep -r "Icon" c:\TAKP\uifiles\default\EQUI_Inventory.xml
grep -r "Icon" c:\TAKP\uifiles\default\EQUI_PlayerWindow.xml
```

**For TASK 2 (Race EQType)**:
```bash
# Search for Race in all XMLs
grep -r "Race" c:\TAKP\uifiles\default --include="*.xml"

# Search EQTYPES.md
grep -i "race" c:\TAKP\uifiles\.docs\technical\EQTYPES.md
```

**For TASK 3 (Tribute)**:
```bash
# Find Tribute references
grep -r "Tribute" c:\TAKP\uifiles\default --include="*.xml"

# Check EQType 121-123 usage
grep -r "EQType>121\|EQType>122\|EQType>123" c:\TAKP\uifiles --include="*.xml"
```

---

## Analysis Document Template

**Each INVENTORY-ANALYSIS-[NAME].md will include**:

```markdown
# Inventory Window Analysis: [UI Name]

## Quick Reference
- **Directory**: [path]
- **Window Size**: WxH px
- **Template Used**: [template name]
- **Total Elements**: [count]
- **Subwindows**: [yes/no, count]
- **Unique Features**: [list]

## Layout Architecture
- Visual diagram
- Subwindow organization
- Zone definitions
- Element positioning summary

## Equipment Display
- Layout pattern (anatomical/scattered/other)
- Slot ordering
- Spacing and alignment
- Background styling

## Stat Display
- AC/ATK placement
- Attribute layout (column/grid/other)
- Resistance display
- HP/Mana format
- Gauge styling

## Icons & Visuals
- Uses stat icons? (yes/no)
- Icon location and size
- Icon source/naming
- Texture loading method
- Class/Deity/Race icons present?

## Gauge Implementations
- XP gauge (present/missing, styling)
- AA gauge (present/missing, styling)
- Tribute gauge (present/missing)
- Colors and dimensions
- Animation templates used

## Unique Features
- Features not in other mods
- Innovative layouts
- Special integrations
- Clever problem solutions

## Comparison to Thorne_Drak
- Similarities
- Differences
- Learnings to adopt
- Incompatibilities to avoid

## Recommendations for Thorne_Drak
- 3-5 key insights from this mod
- Priority (high/medium/low)
- Implementation complexity
- Expected benefits
```

---

## Directory Scanning Checklist

**Before Deep Analysis**:

- [ ] Identify which directories have Inventory windows
- [ ] Count files per directory
- [ ] Note any directory structure variations (Options/, variants/)
- [ ] Check if directories are duplicates (skip thorne_*)
- [ ] Verify each has unique design or just variant of default

**Expected Findings**:
- default/ = baseline reference
- duxaUI = community design example
- Others = variant implementations
- thorne_* = skip (our own work)

---

## Integration With Phase 3.9a

**How Research Feeds Implementation**:

1. **Stat Icons** → Implement texture loading method from research
2. **Race EQType** → Add if found, skip if not available
3. **Tribute** → Place in XP/AA zone based on community patterns
4. **Layout Innovations** → Consider adoption in core redesign
5. **Best Practices** → Ensure alignment where beneficial

---

## Memory Checkpoints

Save progress to memory at:
- ✅ Task 1-3 research complete
- [ ] 2-3 directories analyzed
- [ ] Recommendations skeleton created
- [ ] ThorneUI.agent.md outline done
- [ ] Full analysis documents provided

---

## Estimated Timeline

| Phase | Task | Time | Deliverable |
|-------|------|------|-------------|
| 1 | Research Q1-3 | 1 hr | Research memo + code samples |
| 2 | Create template | 30 min | INVENTORY-ANALYSIS template |
| 3a | Analyze 3 dirs | 1.5 hrs | 3 analysis documents |
| Break | | | Review findings |
| 3b | Analyze 3 more dirs | 1.5 hrs | 3 more analysis documents |
| 4 | Synthesize | 1 hr | RECOMMENDATIONS.md |
| 5 | Update agent.md | 30 min | Enhanced agent.md |
| | **TOTAL** | **5.5-6 hrs** | **Complete analysis suite** |

**Realistic Evening Goal**: Tasks 1-3 + 1-2 analysis templates + agent.md structure  
**Morning Goal**: Complete all analysis docs + recommendations + implementation integration

---

## Success Indicators

**By end of Phase 1-2**:
- ✓ Know how Target window loads textures
- ✓ Know if Race EQType exists
- ✓ Know Tribute display options
- ✓ Have analysis template ready

**By end of Phase 3-4**:
- ✓ 6 analysis documents complete
- ✓ Synthesis document with 10+ recommendations
- ✓ Priority matrix for Phase 3.9b+

**By end of Phase 5**:
- ✓ ThorneUI.agent.md reflects community knowledge
- ✓ Entire analysis suite in `.development/session-logs/phases/`
- ✓ All findings in memory for next session

---

**Status**: READY TO EXECUTE  
**Next Step**: Begin Task 1 research (stat icons from duxaUI)

