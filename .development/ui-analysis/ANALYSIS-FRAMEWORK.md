# Comprehensive UI Analysis Framework

## Project Scope

**Objective**: Perform 100% element-level analysis of all windows in Nillipuss UI to identify features that would improve thorne_drak, organized cohesively in a single documentation structure.

**Goal**: Make thorne_drak BETTER than Nillipuss by:
1. Porting best features from Nillipuss
2. Maintaining Thorne's superior organization  
3. Combining both UIs' strengths
4. Creating detailed implementation plans

## Documentation Structure

All analysis files organized in `.development/ui-analysis/`:

```
.development/ui-analysis/
├── ANALYSIS-FRAMEWORK.md (THIS FILE - master plan)
├── WINDOWS-BY-CATEGORY/
│   ├── CORE-WINDOWS.md (Player, Inventory, Spells, Buffs, Target, etc.)
│   ├── COMBAT-WINDOWS.md (Actions, CastSpell, Hotbutton, etc.)
│   ├── TRADING-WINDOWS.md (Merchant, Barter, Bazaar, Trade, etc.)
│   ├── UTILITY-WINDOWS.md (Chat, Tracking, Notes, Group, etc.)
│   └── DIALOGS-WINDOWS.md (Trivial dialogs, standard UI)
├── COMPLETE-COVERAGE.md (Master 100% file inventory with texture analysis)
├── MISSING-FEATURES-PRIORITY-MATRIX.md (All features ranked by value & complexity)
├── IMPLEMENTATION-ROADMAP.md (v0.7.0, v0.8.0+ phase planning)
├── MASTER-FEATURE-INDEX.md (Alphabetical feature catalog with implementation details)
└── [Individual window analyses] (TARGETWINDOW, SPELLBOOK, ACTIONSWINDOW, etc.)
```

## Window Analysis Categories

### 1. CORE-WINDOWS (12 windows - Critical gameplay)
- ✅ EQUI_PlayerWindow (analyzed - Phase analysis doc exists)
- ✅ EQUI_Inventory (analyzed - Phase analysis doc exists) 
- ✅ EQUI_SpellBookWnd (being corrected - 2-column, NOT book view)
- ✅ EQUI_TargetWindow (analyzed - missing spell name + delay timer)
- ✅ EQUI_BuffWindow (analyzed - Phase analysis doc exists)
- ✅ EQUI_ActionsWindow (analyzed - missing resistance icons)
- ⏳ EQUI_CastSpellWnd (HIGH priority - spell recast timers)
- ⏳ EQUI_CastingWindow (casting bar display)
- ⏳ EQUI_GroupWindow (group member display)
- ⏳ EQUI_PetInfoWindow (pet health and info)
- ⏳ EQUI_ItemDisplay (item tooltips/display)
- ⏳ EQUI_HotButtonWnd (hotbar/ability bars)

### 2. COMBAT-WINDOWS (8 windows)
- EQUI_CombatAbilityWnd
- EQUI_MeleeBuffWindow
- EQUI_CombatSkillsSelectWindow
- EQUI_RaidWindow
- EQUI_RaidOptionsWindow
- EQUI_GroupSearchWnd
- EQUI_RaidOptionsWindow
- EQUI_AAWindow

### 3. TRADING/MERCHANT WINDOWS (10 windows)
- EQUI_MerchantWnd
- EQUI_BarterWnd
- EQUI_BarterSearchWnd
- EQUI_BazaarWnd
- EQUI_BazaarSearchWnd
- EQUI_TradeWnd
- EQUI_GiveWnd
- EQUI_Container/Bags
- EQUI_BankWnd
- EQUI_GuildBankWnd

### 4. UTILITY/INFO WINDOWS (20+ windows)
- EQUI_ChatWindow
- EQUI_GroupWindow
- EQUI_FriendsWnd
- EQUI_TrackingWnd
- EQUI_CompassWnd
- EQUI_BookWindow
- EQUI_SkillsWindow
- EQUI_AAWindow
- EQUI_AlarmWnd
- EQUI_NoteWindow
- EQUI_PlayerNotesWindow
- EQUI_BreathWindow
- EQUI_DynamicZoneWnd
- EQUI_AdventureStatsWnd
- etc.

### 5. DIALOG/STANDARD WINDOWS (15+ windows - likely trivial differences)
- EQUI_Animations.xml
- EQUI_Templates.xml
- Various dialog windows
- Character creation/selection

## Analysis Methodology

For each window, analyze:

1. **Element Inventory**
   - Extract all UI elements (Gauge, Label, Button, Screen, Page, ListBox, etc.)
   - Count elements in each UI
   - Identify element naming patterns

2. **Functional Comparison**
   - What features does Nillipuss have?
   - What features does Thorne have?
   - What's missing in either direction?

3. **Visual/Layout Differences**
   - Window size differences
   - Element positioning patterns
   - Spacing and alignment

4. **Feature Impact**
   - How valuable is the missing feature?
   - How complex to implement?
   - Dependencies on textures or animations?

5. **Implementation Notes**
   - Required texture changes
   - Animation definitions needed
   - EQType requirements
   - Code snippets for reference

## Priority Feature Categories

### 🔴 HIGH VALUE, LOW COMPLEXITY (v0.7.0)
- Resistance icons on ActionsWindow
- Target spell casting name display
- Spellbook Meditate button
- Various button/label additions

### 🟡 HIGH VALUE, MEDIUM COMPLEXITY (v0.7.0 or v0.8.0)
- Spellbook list view option variant
- Spell recast timers on CastSpellWnd
- Color-changing HP gauge (multi-layer)
- Target attack delay timer

### 🟢 MEDIUM VALUE, LOW COMPLEXITY (v0.8.0+)
- Additional gauge variants
- Label text format options
- Buff bar layout variants

### ⚪ LOW VALUE OR HIGH COMPLEXITY (Future consideration)
- Dragitem icon sets (Nillipuss has 34 dragitem textures)
- Guild management UI
- Character creation UI
- Custom cursor variants

## documentation Standardization

Each window analysis document follows this structure:

```markdown
# [Window Name] Analysis

## Summary
- Lines: Nillipuss: XXX, Thorne: XXX
- Elements: Nillipuss: XX, Thorne: XX
- Status: MAJOR / MINOR / TRIVIAL

## Element Inventory
### Nillipuss Elements (XX total)
- Element1, Element2, Element3...

### Thorne Elements (XX total)
- Element1, Element2, Element3...

### Differences
- **Only in Nillipuss**: Element1, Element2 (features to port)
- **Only in Thorne**: Element1, Element2 (features to keep)

## Functional Differences
- Feature 1: [Description]
- Feature 2: [Description]

## Implementation Recommendations
### HIGH Priority
- Feature: Description
  - Complexity: LOW/MEDIUM
  - Textures needed: list
  - Implementation notes: details

### MEDIUM Priority
...

## XML Reference
[Code snippets showing key differences]
```

## Current Status

### Completed Analysis
- ✅ COMPLETE-COVERAGE.md (100% file inventory + texture breakdown)
- ✅ TARGETWINDOW-analysis.md (spell name, attack delay missing)
- ✅ ACTIONSWINDOW-analysis.md (resistance icons missing)
- ⏳ SPELLBOOK-analysis.md (needs correction - already 2-column!)
- ✅ PLAYER-analysis.md (from earlier phase analysis)
- ✅ INVENTORY-analysis.md (from earlier phase analysis)
- ✅ ITEMDISPLAY-analysis.md (from earlier phase analysis)
- ✅ CASTSPELL-analysis.md (from earlier phase analysis)
- ✅ BUFFWINDOW-analysis.md (from earlier phase analysis)

### In Progress
- Windows needing systematic analysis: ~55 remaining

### Next Steps (Priority Order)

1. **Correct SPELLBOOK-analysis.md**
   - Fix 2-column layout description
   - Verify against Nillipuss (does it have Meditate button?)
   - Clarify feature differences

2. **Analyze HIGH-Impact Core Windows**
   - EQUI_CastSpellWnd (spell recast timers)
   - EQUI_CastingWindow (casting bar)
   - EQUI_HotButtonWnd (hotbar variants)
   - EQUI_GroupWindow (group display)

3. **Analyze HIGH-Priority Combat Windows**
   - EQUI_BuffWindow (variants)
   - EQUI_RaidWindow (raid display)

4. **Document MEDIUM-Impact Windows**
   - Trading windows (merchant, barter, bazaar)
   - Utility windows (chat, tracking, compass)

5. **Consolidate into Master Index**
   - Create MISSING-FEATURES-PRIORITY-MATRIX.md
   - Create IMPLEMENTATION-ROADMAP.md
   - All features cross-referenced and categorized

## Cohesive Documentation Strategy

**Single Entry Point**: COMPLETE-COVERAGE.md with:
- Executive summary (what we found)
- Window-by-window status table (links to individual analyses)
- Summary of top 20 features to port (with priority ranking)
- Texture strategy
- Implementation roadmap

**Individual Deep Dives**: Category-based window analysis files:
- CORE-WINDOWS.md (unified analysis of 12 core windows)
- COMBAT-WINDOWS.md (combat-related windows)
- TRADING-WINDOWS.md (merchant/bazaar/trade windows)
- DIALOGS-WINDOWS.md (standard dialogs, minor variations)

**Feature Master Index**: MASTER-FEATURE-INDEX.md
- Alphabetical listing of all discovered features
- Which window, priority, complexity
- Implementation details
- Dependencies

**Implementation Guidance**: IMPLEMENTATION-ROADMAP.md
- v0.7.0 deliverables (resistance icons, spell names, etc.)
- v0.8.0 roadmap (list view, recast timers, HP gauge)
- Texture preparation guide
- Phase-by-phase breakdown

## Success Criteria

✅ Complete analysis when:
1. All 71+ core EQUI_*.xml windows analyzed
2. Element inventories created for each
3. Feature differences documented
4. Priority matrix complete (value vs complexity)
5. All documentation cross-referenced
6. Clear implementation roadmap for v0.7.0+
7. Master feature index created
8. No scattered analysis files (everything cohesive)

---

**Current Target**: Complete windows 1-12 (core windows) this week, then move through remaining categories systematically.
