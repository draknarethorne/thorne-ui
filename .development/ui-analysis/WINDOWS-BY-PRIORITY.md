# Windows Analysis: Prioritized by Feature Differences

**Master Document**: Systematically analyze windows ordered by impact (largest feature differences first).

## 🔴 CRITICAL PRIORITY (Massive Features Missing in Thorne)

### 1. EQUI_PlayerWindow (+1857 lines in Nillipuss = **195% larger**)
**File sizes**: Nillipuss 2808 lines | Thorne 951 lines

**Verified Major Differences (EQType-validated):**
- Color-changing HP gauge (multi-layer EQType 1)
- Zeal tick visuals differ (EQType 24 present in both)
- Additional labels and layout differences
- Enhanced gauge styling

**Estimated v0.8.0 Impact**: HIGH - Core gameplay feature (deferred from v0.7.0)
**Complexity**: MEDIUM-HIGH (color gradient gauge system)

**Status**: ✅ ANALYZED (EQType-validated)

---

### 2. EQUI_GroupWindow (+1972 lines in Nillipuss = **174% larger**)
**File sizes**: Nillipuss 3103 lines | Thorne 1131 lines

**Verified Major Differences (EQType-validated):**
- Multi-layer group HP gauges (EQTypes 11–15)
- Pet HP gauges (EQTypes 17–21)
- Hidden unused labels in Nillipuss (EQTypes 2,3,4,70,128)

**Estimated v0.8.0 Impact**: MEDIUM-HIGH (group/raid gameplay)
**Complexity**: MEDIUM

**Status**: ✅ ANALYZED (EQType-validated)

---

### 3. EQUI_HotButtonWnd (+1642 lines in Nillipuss = **169% larger**)
**File sizes**: Nillipuss 4012 lines | Thorne 2370 lines

**Verified Major Differences (EQType-validated):**
- Additional hotbar layouts and equipment slot variants
- Hidden/unreferenced equipment invslots in Nillipuss

**Estimated v0.8.0 Impact**: MEDIUM (QoL improvement)
**Complexity**: LOW-MEDIUM (mostly layout/styling)

**Status**: ✅ ANALYZED (EQType-validated)

---

## 🟢 MEDIUM PRIORITY (Opportunity Windows from Comprehensive Scan)

### 5. EQUI_BazaarSearchWnd (431 vs 411 lines = **+20 lines, 5% larger**)
**File sizes**: Nillipuss 431 lines | Thorne 411 lines

**Differences**:
- Advanced search and filtering options
- Improved UI controls for merchant searches

**Estimated Impact**: MEDIUM (Merchant quality of life)
**Complexity**: MEDIUM (8-12 hours)

**Status**: ✅ ANALYZED (Comprehensive Scan)
**Recommendation**: v0.8.1 or v0.9.0 (polish phase)

---

### 6. EQUI_TradeskillWnd (165 vs 155 lines = **+10 lines, 6% larger**)
**File sizes**: Nillipuss 165 lines | Thorne 155 lines

**Differences**:
- Organized layout with improved grouping
- Recipe search functionality
- Better visual presentation

**Estimated Impact**: MEDIUM (Crafting quality of life)
**Complexity**: MEDIUM (6-10 hours)

**Status**: ✅ ANALYZED (Comprehensive Scan)
**Recommendation**: v0.8.1 or v0.9.0 (polish phase)

---

## 🔵 NILLIPUSS-ONLY (Strategic Additions)

### 7. EQUI_GuildManagementWnd (Nillipuss-only, 531 lines)
**Nillipuss**: 531 lines | Thorne: NOT PRESENT

**Description**: Comprehensive guild management interface including:
- Guild member management
- Permission controls
- Guild bank access
- Member chat/communication

**Estimated Impact**: HIGH (Core guild functionality)
**Complexity**: HIGH (20-25 hours)

**Status**: ✅ ANALYZED (Comprehensive Scan)
**Recommendation**: v0.9.0+ (Post-v0.8.0 stabilization phase)

---

### 8. EQUI_CharacterCreate (Nillipuss-only, 631 lines)
**Nillipuss**: 631 lines | Thorne: NOT PRESENT

**Description**: Modern character creation interface:
- Streamlined character creation flow
- Better visual presentation
- Improved user guidance

**Estimated Impact**: MEDIUM (New player experience)
**Complexity**: MEDIUM (10-15 hours)

**Status**: ✅ ANALYZED (Comprehensive Scan)
**Recommendation**: v0.9.0+ (Polish/enhancement phase)

---

### 4. EQUI_CastSpellWnd (**CONFIRMED**: Spell Recast Timers Missing)
**File sizes**: Nillipuss 941 lines | Thorne 799 lines (+142 lines = **18% larger**)

**Confirmed Missing Features:**
- ✅ `CSPW_Spell0_Recast` through `CSPW_Spell7_Recast` (individual spell recast timers)
- ✅ `CSPW_Global_Recast` (global cooldown indicator)

**These show visual progress bars under each spell gem indicating recast time.**

**Estimated v0.7.0 Impact**: HIGH - Essential for casters/raiders
**Complexity**: LOW (just adding gauge elements + EQType bindings)

**Status**: ✅ ANALYZED (EQType-validated)

---

### 5. EQUI_BuffWindow (+457 lines = **26% larger**)
**File sizes**: Nillipuss 2209 lines | Thorne 1752 lines

**Verified Features (EQType-validated):**
- Buff duration labels (EQTypes 45–59)
- ShortDurationBuffWindow labels in Thorne (EQTypes 135–149)
- Nillipuss defines unused labels (EQTypes 515–524)

**Estimated v0.7.0 Impact**: LOW-MEDIUM
**Complexity**: LOW-MEDIUM

**Status**: ✅ ANALYZED (EQType-validated)

---

 

### 8. EQUI_Inventory (Thorne is **15% LARGER** = THORNE WINS!)
**File sizes**: Nillipuss 2164 lines | Thorne 2546 lines (+382 lines in Thorne)

**Result**: **NO FEATURES TO PORT - Thorne's implementation is SUPERIOR!**

Thorne's Phase 3.9 Inventory Redesign succeeded. Thorne's modular, 382-line larger implementation defeats Nillipuss's all-in-one approach.

**Status**: ✅ ANALYZED - NO ACTION NEEDED (Thorne already ahead)

---

## 🟢 Core Features Already Analyzed

### EQUI_ActionsWindow (RESISTANCE ICONS)
- ✅ **Confirmed**: Nillipuss has CRIcon, DRIcon, FRIcon, MRIcon, PRIcon elements
- ✅ **v0.7.0 DELIVERABLE**: Port resistance icons to ActionsWindow

### EQUI_TargetWindow (SPELL NAME + DELAY TIMER)
- ✅ **Confirmed**: Nillipuss has Target_Casting_SpellName + Target_AttackDelay
- ✅ **v0.7.0 DELIVERABLE**: Add spell name display (user explicitly requested)

### EQUI_SpellBookWnd (MEDITATE BUTTON)
- ✅ **Confirmed**: 2-column layout already good in Thorne
- ✅ **v0.7.0 DELIVERABLE**: Add SBW_MeditateButton

---

## 📊 Feature Count by Priority

### v0.7.0 Confirmed Deliverables (HIGH Certainty)
1. Resistance icons on ActionsWindow (LOW complexity)
2. Target spell casting name (LOW complexity)
3. Spell recast timers on CastSpellWnd (LOW-MEDIUM complexity)
4. Spellbook Meditate button (LOW complexity)

**Total estimated v0.7.0 effort**: 9-17 hours (6 features, low complexity)

### v0.8.0 Probable Deliverables (EQType-validated)
1. Color-changing HP gauge (PlayerWindow) - HIGH complexity
2. Zeal tick visuals upgrade (PlayerWindow) - MEDIUM complexity
3. Enhanced group displays (GroupWindow) - MEDIUM complexity
4. Hotbar layout variants (HotButtonWnd) - LOW-MEDIUM complexity
5. Enhanced buff displays (BuffWindow) - LOW-MEDIUM complexity

**Total estimated v0.8.0 effort**: 46-69 hours (5 features, medium complexity)

---

## Analysis Roadmap (EQType-Validated)

### Phase 1: HIGH-Priority Core Windows (Complete)
1. ✅ EQUI_CastSpellWnd - Spell recast timers (EQType-validated)
2. ✅ EQUI_PlayerWindow - Color HP gauge + Zeal tick visuals (EQType-validated)
3. ✅ EQUI_GroupWindow - Group HP layers (EQType-validated)
4. ✅ EQUI_HotButtonWnd - Layout variants (EQType-validated)

### Phase 2: MEDIUM-Priority Windows
5. ✅ EQUI_BuffWindow - Buff display variants (EQType-validated)
6. ✅ EQUI_MerchantWnd - Merchant stats/equipment panel (EQType-validated)
7. ✅ EQUI_LootWnd - Loot slot count differences (EQType-validated)
8. ✅ EQUI_Container - Container slots identical (EQType-validated)
9. ✅ EQUI_PetInfoWindow - Pet mana vs multi-layer HP (EQType-validated)

### Phase 3: Standard/Utility Windows
- 15+ remaining windows (likely trivial differences)

---

## Next Steps

1. **Continue EQType-validated batches for remaining windows**
   - Merchant, Loot, Container, Pet, and other medium-impact windows
2. **Create analysis files for any referenced windows that are missing**
3. **Keep MASTER-FEATURE-INDEX, COMPLETE-COVERAGE, and README in sync after each batch**

---

**Goal**: Complete EQType-validated coverage of remaining windows, then lock v0.7.0 implementation scope.
