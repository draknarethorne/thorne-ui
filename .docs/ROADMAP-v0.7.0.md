# Thorne UI v0.7.0 Roadmap

**Version:** 0.7.0-dev  
**Status:** In Development (February 18, 2026)  
**Target Release:** March 2026  
**Estimated Effort:** 9-17 hours of implementation work

---

## Vision

Thorne UI v0.7.0 carries forward the legendary baseline established in v0.6.0 (inventory redesign) and v0.6.5 (spellbook polish) while adding critical quality-of-life enhancements and visual polish that EverQuest players have long requested.

This release focuses on **actionability and clarity**—bringing real-time combat information directly into the player's visual field and making spell management more intuitive.

---

## ✅ Confirmed Features (v0.7.0)

### 1. Spell Recast Timers (CastSpellWnd)
**Priority:** 🔴 High | **Effort:** 2-3 hours | **Impact:** Essential for combat

Display remaining recast time for each spell gem, allowing casters to see exactly when spells will be available without hovering or checking individual timers.

**What's New:**
- Individual spell gem recast time display
- Global spell recast timer (countdown until ALL spells available)
- Clear visual distinction between gems on cooldown vs. ready
- Reference: [MASTER-FEATURE-INDEX.md](../development/ui-analysis/MASTER-FEATURE-INDEX.md) Spell Recast Timers section

### 2. Target Window Enhancements (TargetWindow)
**Priority:** 🔴 High | **Effort:** 1-2 hours (spell name) + 1-2 hours (attack delay) | **Impact:** Critical information at a glance

Know what spell your target is casting and how fast they attack—essential for both PvP and group play.

**What's New:**
- **Current Casting Spell Display** - Shows name of spell currently being cast by target
- **Attack Delay Timer** - Visual countdown of when target's next attack lands
- **Improved visibility** - Larger, clearer information hierarchy

**Reference:** [TARGETWINDOW-analysis.md](../development/ui-analysis/TARGETWINDOW-analysis.md)

### 3. Actions Window: Elemental Resistance Icons (ActionsWindow)
**Priority:** 🟡 Medium | **Effort:** 2-3 hours | **Impact:** At-a-glance elemental status

Display character's elemental resistance status with stat icons, making it immediately obvious which resists are active and their strength.

**What's New:**
- Fiery Descent, Resolve, Ice, Water, Poison, Disease resistances visualized as icons
- Color-coded strength (gradient or tiers)
- Integrates with stat_icon_pieces texture strategy from Phase 3.9
- Reference: [ACTIONSWINDOW-analysis.md](../development/ui-analysis/ACTIONSWINDOW-analysis.md)

### 4. SpellBook: Meditate Button (SpellBookWnd)
**Priority:** 🟢 Low | **Effort:** 0.5-1 hour | **Impact:** Convenience (saves macro slot)

Add a dedicated meditation button within the SpellBook window, allowing players to meditate directly without a macro.

**What's New:**
- Meditate button in spellbook for Clerics/Shamans/Bards
- Consistent visual style with current spellbook design
- References: [SPELLBOOK-analysis.md](../development/ui-analysis/SPELLBOOK-analysis.md)

### 5. Implementation & Testing
**Effort:** 2-4 hours | **Impact:** Quality assurance

Comprehensive in-game testing, documentation, variant validation, and option sync deployment.

---

## Feature Details Reference

For detailed implementation guidance, analysis, and decision rationale, see:

- **[MASTER-FEATURE-INDEX.md](../development/ui-analysis/MASTER-FEATURE-INDEX.md)** - Comprehensive feature breakdown with code examples
- **[ANALYSIS-COMPLETE.md](../development/ui-analysis/ANALYSIS-COMPLETE.md)** - Full implementation analysis
- **Window-Specific Analysis:**
  - [CASTSPELL-analysis.md](../development/ui-analysis/CASTSPELL-analysis.md) - Spell recast timer implementation
  - [TARGETWINDOW-analysis.md](../development/ui-analysis/TARGETWINDOW-analysis.md) - Target window enhancements
  - [ACTIONSWINDOW-analysis.md](../development/ui-analysis/ACTIONSWINDOW-analysis.md) - Resistance icons

---

## 📊 Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| **Feature Implementation** | Feb 25, 2026 | 🟡 In Progress |
| **In-Game Testing** | Mar 1, 2026 | ⏳ Queued |
| **Variant Sync** | Mar 3, 2026 | ⏳ Queued |
| **v0.7.0 Release** | Mar 7, 2026 | ⏳ Planned |

---

## 🎯 v0.8.0 Preview

Looking ahead: The analysis identified 5 additional features for v0.8.0 (46-69 hours):
- **Buff Window Enhancements** - Duration labels, spell timers, short-buff window
- **Group Window Improvements** - Enhanced player displays and status
- **Hotbar Layout Variants** - Additional button arrangement options
- **Merchant Window Integration** - Character stat/equipment panel in merchant trade view
- **Player Window Polish** - HP gauge colors, Zeal tick visualization

See [MASTER-FEATURE-INDEX.md - v0.8.0 Features](../development/ui-analysis/MASTER-FEATURE-INDEX.md#-v08-medium-complexity-features-extensive-but-targeted) for details.

**Current Focus:** v0.7.0 ships first; v0.8.0 decisions made after v0.7.0 user feedback (Q2 2026).

---

## 📚 Related Documentation

### For Users
- [README.md](../README.md) - Feature overview, installation, support
- [STANDARDS.md](STANDARDS.md) - UI consistency and design guidelines

### For Developers
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Architecture, phases, contribution guide
- [ui-analysis/README.md](../development/ui-analysis/) - Detailed analysis hub (window-by-window breakdowns)
- [stat-icons/README.md](../development/stat-icons/) - Stat icon implementation guide

### Research & Archives
- [Phase 3.9: Inventory Redesign](../development/initial-phases/PHASE-3.9-INVENTORY-REDESIGN.md) - v0.6.0 foundation
- [Phase 6: Inventory Research](../development/archive/initial-phases/phase-6-inventory-research/) - Analysis that informed Phase 3.9
- [ANALYSIS-COMPLETE.md](../development/ui-analysis/ANALYSIS-COMPLETE.md) - Full v0.7.0/v0.8.0 analysis

---

## 🎨 Design Philosophy

v0.7.0 features embody Thorne UI's core values:

✅ **Clarity** - Information the player needs is immediately visible  
✅ **Accessibility** - No macros required for essential actions  
✅ **Consistency** - Features align with existing UI standards  
✅ **Legendary Craftsmanship** - Polish every detail  

---

## Questions & Feedback

- **Technical questions?** See [DEVELOPMENT.md](../DEVELOPMENT.md)
- **Feature requests?** Refer to [MASTER-FEATURE-INDEX.md](../development/ui-analysis/MASTER-FEATURE-INDEX.md)
- **Found a bug?** Open an issue on GitHub
- **Want to contribute?** See [DEVELOPMENT.md#contribution-guide](../DEVELOPMENT.md#contribution-guide)

---

**Maintained by:** Draknare Thorne  
**Last Updated:** February 18, 2026  
**Next Review:** Post v0.7.0 release (March 2026)
