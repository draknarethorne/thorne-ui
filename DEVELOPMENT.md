# 🛠️ Thorne UI Development Guide

Implementation details, architecture decisions, and development roadmap for the Thorne UI project.

**Version**: 0.6.5  
**Last Updated**: February 18, 2026  
**Maintainer**: Draknare Thorne

**Quick Links**: [Standards](.docs/STANDARDS.md) | [Phases](.development/initial-phases/) | [Technical References](.docs/technical/) | [TODO](TODO.md) | [Releases Guide](.docs/releases/RELEASES.md)

---

## 🎯 Project Vision & Goals

### Design Philosophy

Thorne UI is built on a foundation of **player choice, flexibility, and accessibility**. Our mission is to create a truly player-friendly experience that empowers users to customize their interface to match their playstyle while working within TAKP's P2002 client limitations.

**Core Principles**:

- **🎨 Player Choice Over Designer Control**
  - Multiple windows display the same stats (HP/Mana in Player, Group, Pet, Actions)
  - Players choose what to show and where based on their preferences
  - No "correct" way to play - support all playstyles equally

- **📑 Flexibility Through Options**
  - Standard + Options variants for most windows
  - Tab-based designs provide contextual organization (Actions, Merchant)
  - Modular approach - mix and match window styles
  - Options directory structure preserves player autonomy

- **📊 Information When Needed**
  - Stats visible in multiple contexts (combat, trading, exploring)
  - Self-sufficient windows reduce need to juggle multiple interfaces
  - Redundant information is intentional - players decide what to use

- **🔧 Customization Within Customization**
  - Options folders provide pre-built alternatives (Tall Gauge pet, Wide Merchant, etc.)
  - Players can further modify any variant to suit their needs
  - Documentation supports confident experimentation

### Technical Goals

Create a streamlined, modern UI experience:

- **Horizontal inventory access** - Quick access to all 29 inventory slots
- **Multi-row hotbars** - Expandable hotbar system for abilities/items
- **Persistent player stats** - Always-visible HP/Mana/Level display
- **No fading windows** - Use only windows immune to client-enforced transparency
- **Clean visual design** - Modern aesthetics with consistent color scheme
- **Self-sufficient merchant window** - Shop without opening separate inventory/stats windows
- **Tab-based organization** - Logical grouping reduces window clutter

### Long-Term Vision

As we continue expanding Thorne UI, we're committed to:

- **🌟 Enhancing Player Experience**
  - Continual refinements based on actual gameplay needs
  - Quality-of-life improvements that reduce friction
  - Visual polish that maintains readability and immersion

- **📚 Comprehensive Documentation**
  - Clear installation and customization guides
  - Technical references for advanced users
  - Development standards that ensure consistency

- **🔄 Iterative Improvement**
  - Quick Hits for rapid minor enhancements
  - Phased development for major features
  - Community feedback integration

**Bottom Line**: Thorne UI exists to serve players, not constrain them. Every design decision asks "Does this give players more control?" rather than "What do I think looks best?"

---

## 🚀 Quick Start

### Installation

```bash
# Copy thorne_drak folder to your TAKP UI directory
# Typical path: C:\Program Files (x86)\EverQuest\uifiles\

# In-game, load the UI
/loadskin thorne_drak
```

### Testing Individual Windows

- **Actions Window**: `/actions` (contains hotbar + inventory tabs)
- **Merchant Window**: Talk to any merchant NPC
- **Hotbar**: `/hotbutton` (4-row hybrid layout)
- **Character Info**: `/charinfo`

---

## 🛠️ Development Workflow

### File Modification Principle

**Always use existing thorne_drak files as the basis** - never overwrite with default files.

### Standard Workflow

1. **Check if file exists in thorne_drak**
   ```bash
   ls thorne_drak/EQUI_*.xml
   ```

2. **If file exists**: Modify it directly
   - Preserves existing customizations
   - Maintains visual consistency
   - Prevents loss of prior work

3. **If file does NOT exist**: Copy from default and modify
   ```bash
   cp default/EQUI_WindowName.xml thorne_drak/
   ```
   - Add to `EQUI.xml` include list if needed

4. **Test in-game**
   ```bash
   /loadskin thorne_drak
   ```

5. **Commit to git** with descriptive message

### Why This Matters

- ✅ Preserves all prior customizations and color schemes
- ✅ Maintains consistency across thorne UI
- ✅ Prevents accidental loss of work
- ✅ Builds incrementally on existing foundation

### Task Tracking

**All task tracking is now in [TODO.md](TODO.md)**. The TODO includes:

- **⚡ Quick Wins**: Small improvements that take < 30 minutes
- **Component Sections**: Tasks organized by window (Group, Pet, Player, Actions, etc.)
- **Quick Hit Guidelines**: What qualifies as a quick hit vs. a phase

For small changes (color adjustments, minor layout tweaks, small bug fixes), add them to the **Quick Wins** section of TODO.md with:
- **Description**: What needs to change
- **Reason**: Why this improves the UI
- **Affected Files**: Which EQUI_*.xml files need updates
- **Testing**: How to verify the change

**When to use Quick Wins**: If it takes < 30 minutes to implement, it's a quick win, not a phase.

---

## ⚖️ Known Limitations & Constraints

### Client-Enforced Fading

**Problem**: Certain window types participate in client-controlled transparency/fading.

**Windows that FADE** (avoid for critical UI):
- ✗ ActionsWindow (includes buttons/slots with items)
- ✗ MerchantWnd (item slots fade)
- ✗ Container windows (bags)

**Windows that DON'T FADE** (safe for core UI):
- ✓ HotButtonWnd (Hotbar)
- ✓ PotionBeltWnd
- ✓ PlayerWindow
- ✓ TargetWindow
- ✓ GroupWindow
- ✓ BuffWindow
- ✓ Inventory (main window only)
- ✓ SpellBookWnd
- ✓ CompassWnd

**Workaround**: Use `/viewport` to position and size windows; use `Alt+Shift+T` to control transparency globally.

### Keybinding Limitations

- **Cannot bind custom windows to keys via XML** - keybindings are client-side only
- **Workaround**: Use slash commands in hotkey macros
  - Example: `/potionbelt` in an F-key macro
  - Works for all built-in slash commands

### Button Click Limitations

- **Custom buttons cannot execute slash commands** - only hardcoded ScreenIDs work
- **Examples of what works**: Sit, Stand, Camp, Melee Attack, Range Attack
- **Example of what doesn't work**: `/potionbelt`, `/inventory` from custom buttons
- **Workaround**: Use buttons as visual reminders; create hotkey macros for commands

### Window Structure

- **Resizable windows**: Use `Style_Sizable=true`
- **Resize behavior**: Both axes scale when dragging; be careful with horizontal limits
- **Global positioning**: UI elements are positioned globally; same element name = same position across all tabs

---

## 🎨 Architecture Decisions & Lessons Learned

Comprehensive architectural patterns and implementation guidance are documented in [.docs/STANDARDS.md](.docs/STANDARDS.md).

### Key Discoveries

#### Global UI Element Positioning

**Discovery**: UI elements are positioned globally. If the same `item=` name appears in multiple Page `<Pieces>` lists, the element displays at the SAME position on all those pages.

**Impact**: Cannot reuse InvSlot/Label across tabs if different positions are needed.

**Solution**: Duplicate elements with unique names
- Example: `MW_Primary` (Equipment tab) vs `MW_Bags_Primary` (Bags tab)
- Allows independent positioning per tab

### Style_Sizable Behavior

**Discovery**: `Style_Sizable=true` allows resizing in BOTH axes simultaneously.

**Problem**: Users could accidentally shrink window horizontally, causing cutoffs and overlaps.

**Solution**: Set `Style_Sizable=false` for windows that must maintain fixed width; enable only on windows designed for resizing.

### Class Animation Implementation

**Correct Pattern**:
```xml
<StaticAnimation item="ClassAnim">
  <Animation>A_ClassAnim01</Animation>
  <!-- other properties -->
</StaticAnimation>
```

**Invalid**: Don't use `RelativePosition` or `EQType` attributes with StaticAnimation.

### Target of Target (ToT) Window Requirement

**Discovery**: EQTypes 27 and 120 (Target of Target HP) **ONLY work in a window named "TargetOfTargetWindow"**. They cannot be embedded in the regular TargetWindow.

**Impact**: ToT display requires a separate `EQUI_TargetOfTargetWindow.xml` file AND EQUI.xml modification.

**Solution**: Create dedicated ToT window file:
- File: `EQUI_TargetOfTargetWindow.xml`
- Screen item: `<Screen item="TargetOfTargetWindow">`
- EQType 27: ToT HP Gauge
- EQType 120: ToT HP numeric/percentage display
- **CRITICAL**: Modify EQUI.xml to include: `<Include>EQUI_TargetOfTargetWindow.xml</Include>`
  - Default EQUI.xml does NOT include this file
  - Custom UI folders need their own EQUI.xml to load ToT window
- Independent window - can be positioned/hidden separately

**See**: [EQUI_TargetOfTargetWindow.xml](thorne_drak/EQUI_TargetOfTargetWindow.xml) and [EQUI.xml](thorne_drak/EQUI.xml) for implementation example.

**See**: [STANDARDS.md - Implementation Patterns](.docs/STANDARDS.md#implementation-patterns) for comprehensive architectural pattern reference including these discoveries plus Options Directory pattern, color palette, and gauge templates.

---

## 📊 Development Phases

See [.development/initial-phases/](.development/initial-phases/) for detailed phase documentation.

### Phase Status Dashboard

| Phase | Status | Priority | Focus | Documentation |
|-------|--------|----------|-------|---------------|
| 1-2 | ✅ Complete | - | Foundation (Actions, Hotbar, Inventory) | [Details](.development/initial-phases/PHASE-1-2-FOUNDATION.md) |
| 3 | ✅ Complete | - | Merchant Window Enhancements | [Details](.development/initial-phases/PHASE-3-MERCHANT.md) |
| 3.5 | ✅ Complete | - | Player/Pet/Group Window Refinements | [Details](.development/initial-phases/PHASE-3.5-PLAYER-GROUP-REFINEMENTS.md) |
| 3.7 | ✅ Complete | - | UI Infrastructure & Templates | [Details](.development/initial-phases/PHASE-3.7-INFRASTRUCTURE.md) |
| 3.9 | ✅ Complete | - | Inventory Window Character Sheet Redesign (v0.6.0) | [Details](.development/initial-phases/PHASE-3.9-INVENTORY-REDESIGN.md) |
| 4 | 📋 Planned | Medium | Actions Window Simplification | [Details](.development/initial-phases/PHASE-4-ACTIONS-SIMPLIFICATION.md) |
| 5 | ✅ Complete | - | Target Window Enhancements (ToT, Level, Class) | [Details](.development/initial-phases/PHASE-5-TARGET-WINDOW.md) |
| 5.5 | 📋 Planned | Low | Loot Window Enhancements | [Details](.development/initial-phases/PHASE-5.5-LOOT-ENHANCEMENTS.md) |
| 6 | ✅ Complete | - | Research & Analysis (Planning for Phase 3.9) | [Details](.development/initial-phases/PHASE-6-CONTAINERS.md) |
| 7 | 🔮 Future | Low | Integration & Asset Consolidation | [Details](.development/initial-phases/PHASE-7-INTEGRATION.md) |
| 8 | 🔮 Future | Low | Polish & Optimization | [Details](.development/initial-phases/PHASE-8-POLISH.md) |

**Legend**: ✅ Complete | 📋 Planned | 🔬 Research | 🔮 Future

### Phase Summaries

**Phase 1-2: Foundation** ✅  
Established core UI framework with Actions window, multi-row hotbar system, and inventory tabs integration. Discovered and documented critical client limitations.

**Phase 3: Merchant Window Enhancements** ✅  
Redesigned Merchant window with self-sufficient shopping experience. Added tabbed interface (Bags/Equipment/Stats) matching Inventory aesthetics. Implemented Options directory pattern for variant management.

**Phase 3.5: Player/Pet/Group Window Refinements** ✅  
Optimized PlayerWindow layout with extended stats, pet information, and casting indicators. Enhanced GroupWindow with combat states and integrated pet HP tracking. Implemented fade-safe background styling.

**Phase 3.7: UI Infrastructure & Template Standardization** ✅  
Established comprehensive gauge template library, standardized XML organization patterns, and created reusable color schemes. Implemented anatomical layout system for consistent window positioning.

**Phase 3.9: Inventory Window Character Sheet Redesign** ✅  
Completed in v0.6.0: Redesigned Inventory window to integrate character sheet functionality with AA gauge, stat blocks, and equipment grid using subwindow pattern. Features anatomical 4-column equipment layout (45x45px slots) and unified character information display. [Full details →](.development/initial-phases/PHASE-3.9-INVENTORY-REDESIGN.md)

**Phase 4: Actions Window Simplification** 📋  
Streamline Actions window by removing redundant elements, optimizing hotbar layouts, and improving visual hierarchy. [Full details →](.docs/phases/phase-4-actions-simplification.md)

**Phase 5: Target Window Enhancements** ✅  
Added Target Level and Class display to Target Window. Created separate EQUI_TargetOfTargetWindow.xml for Zeal ToT functionality (EQTypes 27/120). Key discovery: ToT requires dedicated window file, cannot be embedded in TargetWindow. [Full details →](.docs/phases/phase-5-target-window.md)

**Phase 5.5: Loot Window Enhancements** 📋  
Add Destroy button for quick item deletion and weight cur/max display to prevent over-encumbrance during looting. ✅ Fixed window height bug (v0.4.0). [Full details →](.docs/phases/phase-5.5-loot-enhancements.md)

**Phase 6: Research & Analysis** ✅  
Completed: Comprehensive multi-window analysis (default, duxaUI, QQ, Infiniti-Blue, vert, zeal, community variants) to identify UI patterns, best practices, and design approaches. Research findings directly informed Phase 3.9 inventory redesign decisions and feature prioritization. [Full details →](.development/initial-phases/PHASE-6-CONTAINERS.md)

**Phase 7: Integration & Asset Consolidation** 🔮  
Unify visual language across all windows, consolidate animation definitions, optimize texture usage.

**Phase 8: Polish & Optimization** 🔮  
Final refinements: performance optimization, accessibility improvements, documentation completion.

---

## 🚀 Future Enhancement Ideas

### Community Features

#### Damage Meter / DPS Tracking
- Parse combat messages for damage calculations
- Display running DPS counter
- Track pet vs. player damage
- Export combat log
- **Status**: Requires DLL injection (Zeal integration)

#### Spell Timers / Buff Tracker
- Track spell recast times visually
- Display buff remaining duration
- Warn on buff expiration
- Recast audio alerts
- **Status**: Possible but requires robust spell parsing

#### Chat Enhancements
- Customizable chat window tabs
- Damage/heal/miss highlighting
- Spell casting notifications
- Join/leave announcements filtering
- **Status**: Might be achievable via existing chat system

#### Loot Log / Drop Tracker
- Track items looted from mobs
- Highlight valuable drops
- Zone-specific drop history
- Rare spawn notifications
- **Status**: Requires extensive logging infrastructure

### Advanced UI Features

#### Raid Awareness HUD
- Frame rate counter, network lag display
- Group member status (HP bars, distance, facing)
- Target threat indicator
- **Status**: Requires Zeal integration; helpful for organized groups

#### Keybind Manager
- Visual UI for rebinding keys
- Macro editor with save/load profiles
- Conflict detection
- **Status**: Would require external tool or DLL modification

---

## 📐 Technical Reference

For comprehensive technical documentation, see:

- **[EQType Values Reference](.docs/technical/eqtypes.md)** - Complete EQType binding guide
  - Gauge EQTypes (HP, Mana, Stamina, XP, AA, Group/Pet gauges)
  - Label EQTypes (Character info, Attributes, Resistances, Buffs)
  - InvSlot EQTypes (Equipment slots, Inventory, Bank, Trading)
  - Context-dependent behavior and important notes
  - Color palette standards

- **[Zeal Client Features](.docs/technical/zeal-features.md)** - Zeal-specific enhancements
  - Zeal-specific EQTypes (24, 27, 69-73, 80-86, 120-123)
  - Client-only features (Map overlay, Camera, Floating damage, Target rings)
  - XML implementation examples
  - Requirements and compatibility

- **[Coding Standards](.docs/STANDARDS.md)** - UI development standards and best practices
  - XML organization patterns
  - Gauge templates and styling
  - Anatomical layout system
  - Subwindow/inner screen patterns

---

## 🐛 Troubleshooting


### UI Not Loading

- **Check**: Is `thorne_drak/EQUI.xml` present?
- **Check**: Are individual files in correct directory?
- **Fix**: `/loadskin thorne_drak 1` to force reload with cache clear

### Windows Positioned Off-Screen

- **Fix**: `/viewport reset` to reset all positions
- **Alternative**: Delete `UI_<ServerName>_<CharacterName>.ini` file and restart client

### Changes Not Appearing

- **Fix**: Use `/loadskin thorne_drak 1` to force reload
- **Verify**: File exists in thorne_drak directory with correct name
- **Note**: File names are case-sensitive on some systems

### Inventory Slots Not Clickable

- **Check**: EQType values are correct (22-29 for bags, 1-21 for worn, etc.)
- **Check**: InvSlot elements have proper `ScreenID`
- **Check**: Sizes and locations don't overlap other elements

---

## 📚 Essential Slash Commands

| Command | Purpose |
|---------|---------|
| `/loadskin thorne_drak` | Reload UI with thorne_drak skin |
| `/loadskin thorne_drak 1` | Force reload (clears cache) |
| `/viewport save` | Save window positions |
| `/viewport load` | Load saved positions |
| `/viewport reset` | Reset all windows to defaults |
| `/hotbutton` | Toggle hotbar window |
| `/potionbelt` | Toggle potion belt window |
| `/inventory` | Toggle inventory window |
| `/charinfo` | Toggle character info (player stats) |
| `/actions` | Toggle actions window |

---

## 🎓 Best Practices

### Code Quality
- ✓ Use `multi_replace_string_in_file` for bulk edits (safer than manual)
- ✓ Always include 3-5 lines of context when editing XML
- ✓ Test with `/loadskin thorne_drak 1` after every change
- ✓ Validate XML: ensure well-formed before committing

### Git Workflow
- ✓ Use feature branches: `feature/window-name-enhancement`
- ✓ Commit frequently with descriptive messages
- ✓ Reference specific changes: files modified, values changed, reasoning
- ✓ Include architectural decisions in commit messages

### Development
- ✓ Reference working UIs (duxa, default, Inventory) for patterns
- ✓ Use consistent naming conventions (e.g., `MW_Bags_*` prefix)
- ✓ Test edge cases: minimum window sizes, max values, text overflow
- ✓ Validate EQType values against current PoP era reference

---

## 📖 Documentation Structure

- **README.md** - Project vision, philosophy, and variants overview
- **.docs/STANDARDS.md** - UI standards and guidelines
- **DEVELOPMENT.md** (this file) - Implementation guide and roadmap
- **TODO.md** - Planned features and work items
- **Individual window docs** - Specific `EQUI_*.md` files with detailed notes

---

## 🤝 Contributing

Have ideas for enhancements? Want to help?

1. **Report Issues**: Use GitHub Issues for bugs or problems
  - Example: [#26](https://github.com/draknarethorne/thorne-ui/issues/26) - MerchantSlotsWnd ScreenID mismatch (uierror.txt)
2. **Suggest Features**: GitHub Discussions or Forums
3. **Submit Code**: Pull requests welcome!
4. **Test & Feedback**: Run latest builds and share results
5. **Documentation**: Help improve guides and examples

---

## 📦 Creating Releases

Thorne UI uses GitHub Releases to distribute packaged versions of thorne_drak. The release process is automated using GitHub Actions.

### Quick Release Process

1. **Prepare for release:**
   - Update version number in README.md Version History section
   - Ensure all changes are committed and pushed to main
   - Test thorne_drak in-game

2. **Create and push a version tag:**
   ```bash
   git tag -a v0.4.0 -m "Release v0.4.0: Brief description"
   git push origin v0.4.0
   ```

3. **Automated workflow:**
   - GitHub Actions automatically creates the release
   - Packages thorne_drak as a ZIP file
   - Generates changelog from commits
   - Publishes release with download links

4. **Review and announce:**
   - Check the release on GitHub Releases page
   - Edit release notes if needed
   - Share with the TAKP community

> **Note**: Only thorne_drak is included in releases. Other variants are available in the source repository.

### Detailed Guide

For complete instructions, troubleshooting, and best practices, see **[Releases Guide](.docs/releases/RELEASES.md)**.

Topics covered:
- Version numbering (semantic versioning)
- Release checklist
- Manual vs. automated releases
- Managing and editing releases
- Troubleshooting workflows

---

## 📜 Version History

**v0.6.5** (February 18, 2026)
- ✅ Spellbook/cast window polish and alignment pass
  - Spellbook Done button standardized to Inventory button height
  - Cast Spellbook button normalized to standard 20px control height
  - Cast window spacing/height adjusted for cleaner bottom control area
- ✅ Options workflow migration to Thorne baselines
  - Added and adopted `options_thorne_sync.py` and `sync-option-thorne.bat`
  - Migrated active option baselines away from `Default/` naming toward `Thorne/`
  - Updated option metadata/readmes and synchronization flows
- ✅ Icon pipeline refresh
  - Regenerated gem icon assets across root and Options icon variant packs

**v0.6.0** (February 6, 2026)
- ✅ **Phase 3.9 Completion**: Inventory window character sheet redesign (FINAL)
  - Anatomical 4-column equipment layout (21 armor slots, 2px spacing)
  - Unified 45x45px slot sizing for consistency across all window sizes
  - Currency zone properly positioned with correct spacing
  - AA gauge integrated with character sheet
  - Phase 3.9 fully tested and stable for production
- ✅ **Critical Texture Fixes**
  - Attack Indicator texture definition added (resolves UIError.txt entries)
  - PNG mislabeling corrected (converted to proper TGA format)
  - UTF-8 character encoding issues fixed in XML files
  - scrollbar_gutter.tga dimensions corrected (0x0 → 16x16)
- ✅ **Player Window Improvements**
  - AttackIndicator animation properly referenced across all 5 variants
  - Gauge animation organization optimized
  - All player window variants validated and tested
- ✅ **Comprehensive Testing & Validation**
  - 45 texture files verified (proper format, dimensions validated)
  - 100 XML files validated for parsing correctness
  - No texture loading errors or missing animations
- ✅ **Documentation & Planning**
  - Phase 6 research archived and summarized
  - Stat icons implementation guide created (.development/stat-icons/)
  - Self-sustainable window architecture philosophy documented
  - Next phase (Stat Icons) fully planned and ready for implementation
- ✅ **Stat Icons System**: File organization and abbreviation enhancements
  - Removed duplicate coordinate files (backed up to .development/archives/)
  - Enhanced master coordinates JSON with 18 icon abbreviations
  - Added comprehensive abbreviation reference guide (.development/stat-icons/ABBREVIATIONS.md)
  - All abbreviations documented with rationale and implementation guidelines
  - Scripts verified working with enhanced metadata structure
- ✅ **Development Setup**: Version management and GitHub Actions
  - VERSION file synchronized with git tags and README
  - Automated release workflow tested and verified
  - Release documentation updated and organized

**v0.5.0** (February 3, 2026)
- ✅ **Phase 5**: Target Window enhancements
  - Target of Target (ToT) window implementation (Zeal compatible)
  - Target Level and Class displays
  - Pet dismiss button enabled with visual improvements
- ✅ **Pet Window**: Enhanced layout and color scheme
  - Pet health gauge improvements (color updated to red)
  - Created Standard and Tall Gauge variants
  - Improved button positioning
- ✅ **Code Quality**: Comprehensive attribution headers
  - Added headers to 38 XML files
  - Credited original authors and documented Thorne UI modifications
- ✅ **Bug Fixes**: Loot window height correction
  - Increased from 360px → 420px for proper 4×5 slot visibility
  - Fixed Large Loot variant matching
- ✅ **Project Infrastructure**: Version management system
  - Created VERSION file (semantic versioning)
  - Multi-source version tracking (VERSION file, git tags, README)
  - Comprehensive VERSION-MANAGEMENT.md guide
- ✅ **Documentation**: Complete reorganization and standardization
  - Renamed all docs to UPPERCASE-WITH-HYPHENS.md convention
  - Moved docs/ → .docs/ (hidden from EQ client)
  - Created version-specific release directories
  - Enhanced ThorneUI agent with GitHub MCP instructions
- ✅ **Development Setup**: Workspace and script improvements
  - Added .bin/ directory for utility scripts
  - Updated workspace PATH configuration for cross-platform support

**v0.4.0** (February 2, 2026)
- ✅ **GitHub Releases**: Complete automated release infrastructure
  - GitHub Actions workflow for automated ZIP packaging
  - Release testing suite with validation script
  - Public Releases page at `/releases` URL
  - Automated changelog generation from commits
- ✅ **Documentation**: Comprehensive releases guides
  - Complete releases guide (RELEASES.md)
  - FAQ covering common questions (RELEASES-FAQ.md)
  - Testing guide (now in .development/releases/TESTING-RELEASES.md)
  - Quick start reference (releases-quickstart.md)

**v0.3.0** (February 1, 2026)
- ✅ **Documentation**: Complete reorganization (79% reduction in main file)
  - Modular structure with `.docs/` directory (15 specialized files)
  - Phase documentation extracted (9 phase files, 1,571 lines)
  - Technical references created (EQTypes 313 lines, Zeal 626 lines)
  - Enhanced STANDARDS.md with comprehensive patterns (629 lines)
- ✅ **Merchant Window**: Comprehensive redesign (3-tab self-sufficient UI)
- ✅ **Actions Window**: Now resizable for collapsing inventory tabs
- ✅ **Potion Belt**: Reminder button added to Actions Main tab
- ✅ **Options Pattern**: Implemented variant directory structure

**v0.2.0** (January 2026)
- ✅ Hybrid hotbar + inventory display (4-row layout)
- ✅ Vertical navigation arrows for multi-row hotbar
- 🔍 Discovered client hardcoding limitations (buttons 11-30 don't function)

**v0.1.0** (January 2026)
- ✅ Initial Actions window with inventory tabs
- ✅ Player stats integration
- ⚠️ Identified window fading limitation

---

**Repository**: [draknarethorne/thorne-ui](https://github.com/draknarethorne/thorne-ui)  
**Maintainer**: Draknare Thorne
