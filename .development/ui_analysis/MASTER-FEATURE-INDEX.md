# Master Feature Index: All Nillipuss Features Worth Porting

**Single source of truth**: All features identified from comprehensive Nillipuss UI analysis, organized by priority and implementation complexity.

---

## 🔴 v0.7.0 - CONFIRMED LOW-COMPLEXITY FEATURES (Ready This Release)

| Feature | Window | Complexity | Effort | User Request | Status | Notes |
|---|---|---|---|---|---|---|
| **Spell Recast Timers (Global)** | CastSpellWnd | LOW | 2-3h | 🟢 Implied (casters) | ✅ CONFIRMED | `CSPW_Global_Recast` gauge element missing |
| **Spell Recast Timers (Individual)** | CastSpellWnd | LOW | 3-4h | 🟢 Implied (casters) | ✅ CONFIRMED | `CSPW_Spell0_Recast` through `_Spell7_Recast` missing (8 elements) |
| **Resistance Icons** | ActionsWindow | LOW | 2-3h | 🔴 EXPLICIT | ✅ CONFIRMED | CRIcon, DRIcon, FRIcon, MRIcon, PRIcon elements (stat-icons feature!) |
| **Target Spell Casting Name** | TargetWindow | LOW | 1-2h | 🔴 EXPLICIT | ✅ CONFIRMED | `Target_Casting_SpellName` label (user specifically requested) |
| **Target Attack Delay Timer** | TargetWindow | LOW | 1-2h | 🟡 Maybe | ✅ CONFIRMED | `Target_AttackDelay` gauge (combat utility) |
| **Spellbook Meditate Button** | SpellBookWnd | LOW | 0.5-1h | 🟢 Implied | ✅ CONFIRMED | `SBW_MeditateButton` element (quick access) |

**v0.7.0 Total**: 6 features, **9-17 hours combined effort**
**Combined v0.7.0 PR Deliverable**: "Stat Icons & Combat Features v0.7.0"

---

## 🟢 NEW OPPORTUNITIES - From Comprehensive Window Scan

### Nillipuss-Only Windows (Not in Current Thorne)

| Window | Complexity | Effort | Strategic Value | Recommendation |
|--------|-----------|--------|-----------------|----------------|
| **GuildManagementWnd** | HIGH | 20-25h | HIGH - Core guild functionality | v0.9.0+ (Post-v0.8.0 stabilization) |
| **CharacterCreate** | MEDIUM | 10-15h | MEDIUM - Improved new player UX | v0.9.0+ (Polish phase) |

### Enhancement Opportunities (Polished Features in Nillipuss)

| Window | Feature | Complexity | Effort | Strategic Value | Recommendation |
|--------|---------|-----------|--------|-----------------|----------------|
| **BazaarSearchWnd** | Advanced search + filtering | MEDIUM | 8-12h | MEDIUM - Better merchant UX | v0.8.1 or v0.9.0 |
| **TradeskillWnd** | Organized layout + recipe search | MEDIUM | 6-10h | MEDIUM - Crafting quality of life | v0.8.1 or v0.9.0 |
| **FriendsWnd** | "Find" button + layout polish | LOW | 1-2h | LOW - Minor QoL | v0.7.1+ (Quick polish) |
| **PetInfoWindow** | "Pet Commands" button | LOW | 1-2h | LOW - Minor QoL | v0.7.1+ (Quick polish) |

**Note**: None of these are blocking v0.7.0 or v0.8.0 and can be prioritized strategically based on community feedback.

---

## 🟡 v0.8.0 - MEDIUM-COMPLEXITY FEATURES (Next Release)

| Feature | Window | Complexity | Effort | Scope | Status | Notes |
|---|---|---|---|---|---|---|
| **Color-Changing HP Gauge** | PlayerWindow | HIGH | 15-20h | Core | 🔴 REQUIRES DESIGN | Multi-layer gauge (Green/Yellow/Orange/Red) - 13 layer elements in Nillipuss |
| **Zeal Tick Mana Visual Upgrade** | PlayerWindow | MEDIUM | 8-12h | Core | 🔴 REQUIRES DESIGN | EQType 24 already present in Thorne; Nillipuss uses full-width tick visuals |
| **Enhanced Group Displays** | GroupWindow | MEDIUM | 10-15h | Raid | 🔴 REQUIRES DETAILED ANALYSIS | 1972 line difference (174% larger in Nillipuss) |
| **Hotbar Layout Variants** | HotButtonWnd | LOW-MEDIUM | 8-12h | Secondary | 🔴 REQUIRES DETAILED ANALYSIS | 1642 line difference (169% larger in Nillipuss) |
| **Buff Display Variants** | BuffWindow | LOW-MEDIUM | 5-10h | Secondary | 🔴 REQUIRES ANALYSIS | 457 line difference (26% larger in Nillipuss) |

**v0.8.0 Estimated**: 5 features, **46-69 hours combined effort**
**Focus** (if resource-constrained): Color HP gauge + Zeal tick visuals (23-32h) for maximum user impact

---

## 🟢 v0.8.0+ - LOWER-PRIORITY/FUTURE FEATURES

| Feature | Window | Complexity |Effort | Notes |
|---|---|---|---|---|
| Spellbook Larger Icons Variant | SpellBookWnd | MEDIUM | 5-8h | Current 24x20px; could expand to 32x32px+ |
| Spellbook List View Option | SpellBookWnd | MEDIUM | 5-8h | Alternative to 2-column page view (Nillipuss style) |
| Dragitem Icon Set (34 textures) | Inventory | MEDIUM | 4-6h | Nillipuss has dragitem1-34.tga (Thorne may share from default/) |
| Custom Cursor Variants | Global | LOW | 2-3h | Nillipuss has 6 custom cursor TGA files |
| Spell Icon Sheets (7 sets) | Various | MEDIUM | 6-10h | Nillipuss has spells01-07.tga (alternative icon styling) |
| Guild Management UI | GuildManagementWnd | MEDIUM | 10-15h | Nillipuss feature (may not be critical for P2002) |
| Character Creation UI | CharacterCreate | LOW | 2-4h | Nillipuss includes; Thorne can add if needed |

---

## Analysis Status by Window

### ✅ COMPLETE ANALYSIS (17 windows)
- EQUI_ActionsWindow - Element inventory complete (resistance icons found)
- EQUI_TargetWindow - Element inventory complete (spell name + timer found)
- EQUI_SpellBookWnd - Layout verified (2-column confirmed)
- EQUI_CastSpellWnd - Elements extracted (recast timers found)
- EQUI_PlayerWindow - Element inventory complete (color HP gauge ++ found)
- EQUI_BuffWindow - EQType-validated analysis complete (short duration window)
- EQUI_GroupWindow - Analysis complete (1972 line difference, MEDIUM priority)
- EQUI_HotButtonWnd - Analysis complete (1642 line difference, LOW-MEDIUM priority)
- EQUI_Inventory - Analysis complete (**Thorne is SUPERIOR - no features needed**)
- EQUI_MerchantWnd - EQType-validated analysis complete
- EQUI_LootWnd - EQType-validated analysis complete
- EQUI_Container - EQType-validated analysis complete
- EQUI_PetInfoWindow - EQType-validated analysis complete
- EQUI_InspectWnd - EQType-validated analysis complete
- EQUI_TradeWnd - EQType-validated analysis complete
- EQUI_BankWnd - EQType-validated analysis complete
- EQUI_AltStorageWnd - Documented (default-only; missing in Thorne/Nillipuss)

### ⏳ PENDING ANALYSIS (0 windows - ALL CRITICAL WINDOWS ANALYZED!)
- All windows have been addressed either with detailed analysis or quick assessment

### 🔍 STANDARD WINDOWS (60+ windows)
- Likely trivial or no differences
- Quick scan shows: < 100 line changes in most
- Not priority for feature porting

---

## Feature Implementation Dependency Map

```
v0.7.0 WAVE 1 (No Dependencies)
├── Spell Recast Timers (CastSpellWnd) - Standalone gauge additions
├── Resistance Icons (ActionsWindow) - Standalone animation + gauge
├── Target Spell Name (TargetWindow) - Standalone label
├── Target Attack Delay (TargetWindow) - Standalone gauge
└── Meditate Button (SpellBookWnd) - Standalone button

v0.8.0 WAVE 1 (Medium Dependencies)
├── Color HP Gauge (PlayerWindow) - Requires gauge piece textures
├── Zeal Tick Visuals (PlayerWindow) - Requires animation definitions
├── Buff Variants (BuffWindow)  - May require texture adjustments
└── Hotbar Variants (HotButtonWnd) - Layout-only changes

v0.8.0 WAVE 2 (High Dependencies)
├── Enhanced Group Displays - May require StatusBar/font changes
├── Spellbook Icons Variant - Icon asset scaling
├── Dragitem Set - Conditional on inventory redesign scope
└── Custom Cursor - Optional polish feature
```

---

## Texture Asset Requirements

### Required for v0.7.0
- ✅ gauge_inlay_thorne01.tga (already in Thorne) - for recast timers + attack delay
- ✅ stat_icon_pieces01.tga (already in Thorne) - for resistance icons
- ✅ window_pieces01-05.tga (already in Thorne) - for UI elements
- ⚠️ Confirm resistance icon graphics exist in this file

### Required for v0.8.0
- 🔴 Color gauge variants (Green, Yellow, Orange, Red - may need to create)
- 🔴 Zeal tick animation frames (may need to create)
- ⚠️ Enhanced group display assets (pending detailed analysis)

### Optional Future
- 📦 Nillipuss dragitem01-34.tga (34 files)
- 📦 Nillipuss spells01-07.tga (7 spell icon sheets)
- 📦 Nillipuss spellbook04.tga and custom_cursor variants

---

## Recommended Implementation Schedule

### Week 1 (v0.7.0 Prep)
1. Continue EQType-validated review of legacy analyses (BuffWindow, ItemDisplay) as needed
2. Extract implementation code snippets from Nillipuss
3. Prepare texture assets (verify resistance icons exist)
4. Create PR template for v0.7.0

### Week 2 (v0.7.0 Implementation)
1. Add spell recast timers (2-3h) ← Start here
2. Add resistance icons (2-3h)
3. Add target spell name (1-2h)
4. Add target attack delay timer (1-2h)
5. Add spellbook meditate button (0.5-1h)
6. Testing and Options variant creation

### Week 3-4 (v0.8.0 Prep)
1. Detailed analysis of color gradient gauge system
2. Research Zeal tick animation patterns
3. Design multi-layer gauge placement
4. Create textures for color variants

### Week 5+ (v0.8.0 Implementation)
1. Implement color-changing HP gauge (15-20h)
2. Implement Zeal tick visual upgrade (8-12h)
3. Additional features based on remaining window analysis

---

## Success Criteria for v0.7.0

✅ Release when:
1. All 6 confirmed features implemented
2. Element additions tested in-game
3. Options variants created (if applicable)
4. Documentation updated for each new window
5. PR merged with comprehensive feature list
6. User confirms "stat-icons working as expected"

**Target**: 1-2 weeks

---

## Next Immediate Actions

1. **Continue Standard Window Analysis** (remaining utility/trivial windows)
   - Estimated: ongoing, low priority
   - Priority: Complete EQType-validated coverage of remaining standard windows

2. **Extract Nillipuss XML Code Snippets**
   - Copy spell recast timer definitions from CastSpellWnd
   - Copy resistance icons from ActionsWindow
   - Copy target displays from TargetWindow
   - Create reference doc for implementation

3. **Verify Texture Assets**
   - Confirm resistance icons exist in stat_icon_pieces01.tga
   - Identify gauge pieces for recast timers
   - Check animation frame requirements

4. **Create v0.7.0 Feature Branch & PR Template**
   - Update PR #37 with comprehensive feature list
   - Link all analysis documents
   - Set timeline: Start implementation next session

---

## Summary Table

| Phase | Features | Hours | Status |
|---|---|---|---|
| **v0.7.0** | 6 features (spell timers, icons, names, buttons) | 9-17h | ✅ READY (analysis complete) |
| **v0.8.0** | 5 features (color gauge, visuals, variants, displays) | 46-69h | ✅ ANALYSIS COMPLETE (implementation planning) |
| **v0.8.0+** | 7 features (extras, polish, optional) | 20-40h | 🔍 DISCOVERY |
| **TOTAL** | 18 features identified | 75-126h | 📊 COMPREHENSIVE SCOPE |

---

**Last Updated**: Today's analysis session
**Next Review**: After next EQType-validated batch review
