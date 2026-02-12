# ✅ Thorne UI Development TODO

Planned features, improvements, and work items organized by component.

---

## ⚡ Quick Wins (Low Hanging Fruit)

**Short on time? Pick one of these quick tasks to make progress:**

### Pending Quick Hits

#### Visual & Color Adjustments

- [ ] **Standardize Field Naming Conventions Across Windows** (Priority: High, READY FOR EXECUTION)
  - **Status**: ✅ Writeup completed, ⏳ Implementation pending
  - **Reason**: Inconsistent field naming makes code maintenance difficult and reduces clarity
  - **Scope**: Player Window, Target Window, Pet Window, Actions Window, Merchant Window, Group Window
  - **Key Fields to Standardize**: HP, Mana, Level, Class, Race, AC, ATK, Weight, AA, etc.
  - **Approach**: Apply established naming convention documented in writeup
  - **Impact**: Improves code consistency, aids future development, simplifies XML navigation
  - **Files**: Multiple EQUI_*.xml files across windows
  - **Testing**: Verify all fields still display and update correctly in-game after renaming

- [ ] **Refactor Custom Gauge Definitions to Window Files** (Priority: Medium, ARCHITECTURE)
  - **Status**: ⏳ Planning - part of self-sustainable window initiative
  - **Reason**: Window .xml files should be self-contained and not depend on EQUI_Animations.xml for custom resources
  - **Scope**: Player Window, Pet Window, Target Window (any windows with custom gauge definitions)
  - **Current Problem**: Custom gauge textures/animations defined in EQUI_Animations.xml create cross-file dependencies
  - **Approach**: Move `<Ui2DAnimation>` and `<TextureInfo>` definitions from EQUI_Animations.xml into respective window .xml files
  - **Impact**:
    - ✅ Windows become self-sustainable (all resources in one file)
    - ✅ Easier to create Options variants (no shared animation dependencies)
    - ✅ Better encapsulation (window owns its resources)
    - ✅ Reduces EQUI_Animations.xml bloat
    - ⚠️ Some texture definitions may be duplicated across windows (acceptable trade-off)
  - **Files**: EQUI_PlayerWindow.xml, EQUI_PetInfoWindow.xml, EQUI_TargetWindow.xml, EQUI_Animations.xml
  - **Related**: Stat Icons implementation follows this pattern (see .development/stat-icons/)
  - **Testing**: Verify gauges render correctly, no texture loading errors, all variants work

- [ ] Check button sizing uniformity across windows
- [ ] Review window border spacing standards (2px/4px consistency)

## 📋 Options Sync System (NEW - February 2026)

Comprehensive organization system for all windows

### Structure Overview

Each Options/[Window]/ directory now contains:

```
Options/[Window]/
├── Default/                      ← CURRENT PRODUCTION VERSION (always synced)
│   └── EQUI_*.xml               ← Exact copy of thorne_drak/ version
├── [Variant Name]/              ← Experimental alternatives
│   ├── EQUI_*.xml
│   └── README.md                ← Documents what's different
├── [Another Variant]/
├── .sync-status.json            ← Metadata tracking sync status
└── README.md                    ← Organization & workflow guide
```

### Status: ✅ FULLY IMPLEMENTED (ALL 13 WINDOWS)

**Commits**: 17947d2 (Initial 9 windows) + aa7b6b7 (Remaining 4 windows)  
**Date**: 2026-02-03

**Complete Window Coverage:**
- ✅ Actions Window - EQUI_ActionsWindow.xml
- ✅ Animations Window - EQUI_Animations.xml
- ✅ Group Window - EQUI_GroupWindow.xml
- ✅ Hotbutton Window - EQUI_HotbuttonWnd.xml
- ✅ Inventory Window - EQUI_Inventory.xml
- ✅ Loot Window - EQUI_LootWnd.xml
- ✅ Merchant Window - EQUI_MerchantWnd.xml
- ✅ Pet Window - EQUI_PetInfoWindow.xml
- ✅ Player Window - EQUI_PlayerWindow.xml
- ✅ Selector Window - EQUI_SelectorWnd.xml
- ✅ Skin Window - EQUI_LoadskinWnd.xml
- ✅ Spellbook Window - EQUI_SpellbookWnd.xml
- ✅ Target Window - EQUI_TargetWindow.xml

### Usage: Making Changes

When you modify any main window in `thorne_drak/`:

```
STEP 1: Edit & Test
  └─ thorne_drak/EQUI_*.xml

STEP 2: Verify Works
  └─ Test in-game, confirm changes

STEP 3: Backup to Default
  └─ cp thorne_drak/EQUI_*.xml thorne_drak/Options/[Window]/Default/EQUI_*.xml

STEP 4: Update Metadata
  └─ Edit .sync-status.json:
     - Update last_sync_date
     - Update last_sync_commit  
     - Mark "in_sync": true

STEP 5: Commit Together
  └─ Include main file + Default/ backup + .sync-status.json update
```

### Benefits

✅ **No Confusion** - Always know which version is current  
✅ **Full Backup** - Every change preserved in Options/[Window]/Default/  
✅ **Clear Metadata** - .sync-status.json shows last update + commit  
✅ **Safe Experimentation** - Variants separate from production  
✅ **Easy Verification** - Check sync status: `cat thorne_drak/Options/[Window]/.sync-status.json`

### Checking Sync Status

```bash
# View sync status for any window
cat thorne_drak/Options/Actions/.sync-status.json

# Example output:
{
  "window": "Actions",
  "default_variant": "Default",
  "last_sync_date": "2026-02-03",
  "last_sync_commit": "17947d2",
  "in_sync": true,
  "notes": "Initial sync - Default copy created"
}
```

### For Future Windows

When you start working on a new window:

1. Create `Options/[NewWindow]/Default/` directory
2. Copy main window file into it
3. Create `.sync-status.json` with metadata
4. Create `README.md` explaining the system
5. Commit everything together

**Template for new window setup:**
```bash
mkdir -p "thorne_drak/Options/[NewWindow]/Default"
cp "thorne_drak/EQUI_*.xml" "thorne_drak/Options/[NewWindow]/Default/"
# Create .sync-status.json and README.md (use existing as templates)
```

---

### Completed Quick Hits (Recent)

#### February 2026

- ✅ **v0.6.0 Release** (2026-02-06)
  - Released Phase 3.9 Inventory redesign finalization
  - Resolved all texture-related startup errors (UIError.txt, Texture.txt)
  - Updated VERSION to 0.6.0 and added release notes to README.md
  - Created git tag v0.6.0 for official release
  - Commit: 0ecb51f

- ✅ **Documentation Reorganization** (2026-02-06)
  - Moved SESSION_COMPLETION_REPORT.md to .development/initial-phases/PHASE-6-INVENTORY-WINDOWS/
  - Moved INVENTORY-REDESIGN-FINAL.md to .development/initial-phases/PHASE-6-INVENTORY-WINDOWS/
  - Consolidated Phase 6 inventory redesign documentation
  - Commit: e4325c1

- ✅ **Attack Indicator Texture Fix** (2026-02-06)
  - Added missing AttackIndicator.tga TextureInfo definition (222×34)
  - Fixed in all 5 player window variants:
    - EQUI_PlayerWindow.xml (main)
    - Options/Player/Default
    - Options/Player/Standard
    - Options/Player/AA and XP Bottom
    - Options/Player/Pet Bottom
  - Resolved constant texture loading errors at startup
  - Commit: 111e7f5

- ✅ **Group Window Pet Gauge Alignment Fix** (2026-02-03)
  - Fixed pet gauge horizontal misalignment (X=16→X=11)
  - All 5 pet gauges now aligned with player health gauges
  - Visual consistency improved across all group member bars
  - Updated Options/Group/Standard backup with latest changes
  - Commit: a228f2a, 8340d48

- ✅ **Standardize Mana Label Colors in All Windows** (2026-02-03)
  - Standardized mana labels in all main thorne_drak files: RGB(150,150,255) → RGB(100,150,255)
  - Updated mana colors in 10 Options variants (Target, Actions, Merchant, Player windows)
  - Commit: 5ebf3df (main files), d7c0008 (Options files)
  - All mana labels now consistently bright blue RGB(100,150,255) for improved readability
  - **Files Updated**: 14 total files across main and Options variants

- ✅ **Group Window Player Bars Alignment Verification** (2026-02-03)
  - Verified all 5 player health gauges (GW_Gauge1-5) are properly aligned
  - Confirmed 28px vertical spacing throughout: gauges, F-labels, dividers, HP labels
  - All player bars horizontally aligned at X=11 (health) and X=82-142 (HP display)
  - Note: Group Window does not contain mana gauges (only player health status)
  - Alignment Status: ✅ ALL CONSISTENT

- ✅ **Test F2-F6 Keyboard Label Positioning on Group Window** (2026-02-03)
  - Verified F2-F6 labels are properly positioned with 28px vertical spacing
  - Confirmed no overlap with player health gauges (GW_Gauge1-5)
  - Label Y positions: 13, 41, 69, 97, 125 (consistent 28px spacing)
  - No adjustment needed - labels verified fine

- ✅ **Brighten Mana Label Color Standardization** (2026-02-03)
  - Updated Player Window: PW_Mana_Values from RGB(150,150,255) to RGB(100,150,255)
  - Updated Actions Window: ACTW_CurrentMana from RGB(150,150,255) to RGB(100,150,255)
  - Updated Merchant Window: MW_MANANumber from RGB(150,150,255) to RGB(100,150,255)
  - Already completed for Pet and Target windows in prior sessions
  - All mana labels now consistently bright blue RGB(100,150,255) for improved readability

- ✅ **PlayerWindow Name/Class Overlap Fix** (2026-02-03)
  - Moved Player Class from X=91 to X=130, reduced width from 56px to 50px
  - Removed redundant "Level" label (max level 60 makes it unnecessary)
  - Moved level value from X=200 to X=185 for better spacing
  - Fixes Shadow Knight and other long class names overlapping with player name

- ✅ **Vertical Selector Window Layout** (2026-02-03)
  - Created vertical selector window (38×278px) from horizontal layout (278×50px)
  - Repositioned all 9 buttons from X-axis to Y-axis layout  
  - Removed titlebar (WDT_RoundedNoTitle) for streamlined narrow design
  - Created Options/Selector/Standard (horizontal) and Vertical variants with documentation

- ✅ **Phase 5: Target Window Enhancements**
  - Created separate EQUI_TargetOfTargetWindow.xml for ToT display (Zeal)
  - Created EQUI.xml to load ToT window (not in default EQUI.xml)
  - Added Target Level (EQType 2) and Class (EQType 3) to Target Window
  - Resized Target Window from 50px to 60px height
  - ToT window: compact 182×18px design with HP gauge and label
  - Key discovery: ToT requires separate window file AND EQUI.xml modification

- ✅ **Pet Dismiss Button Added**
  - Enabled hidden PIW_LostButton as small clickable bar
  - Position: X=130, Y=25 (just below HP percentage display)
  - Size: 28×6 pixels (thin bar with "X")
  - Tooltip: "Pet Get Lost (Dismiss)"
  - Allows dismissing pet when /pet commands fail

- ✅ **Mana Color Updated in Pet Window**
  - Updated pet mana gauge from RGB(0,0,240) to RGB(100,150,255)
  - Better visibility and consistency with STANDARDS.md

- ✅ **Mana Color Updated in Target Window**
  - Updated player mana display from RGB(150,150,255) to RGB(100,150,255)
  - Part of Phase 5 Target Window implementation

- ✅ **Weight Display Added to Player Window** (Commit: 2e7d647)
  - Added weight cur/max display to Player window cornerstone
  - Format: "WT: cur/max"
  - EQTypes: 24 (current), 25 (max)

- ✅ **Weight Display Added to Actions Window** (Commit: ae6c629)
  - Added weight display to Actions window Player Info tab
  - Prevents over-encumbrance during combat/inventory management

- ✅ **AA Points Display Added to Actions Window** (Commit: 6ad9ef2)
  - Added AA points display to Actions window Player Info tab
  - Allows monitoring AA progress without opening separate window

#### January 2026

- ✅ **Documentation Reorganization**
  - Created modular .docs/ directory structure
  - Extracted 9 phase files from DEVELOPMENT.md (79% reduction)
  - Created technical references (EQTypes, Zeal features)
  - Enhanced STANDARDS.md with comprehensive patterns

- ✅ **README Enhancements**
  - Added comprehensive Option variant README files
  - Standardized naming (EQUI_*.md → README.md)
  - Added technical specifications to all variants

### Quick Hit Guidelines

**What Qualifies as a Quick Hit?**

✅ **Yes - Add Here**:
- Color/contrast adjustments (< 5 RGB values changed)
- Single label position tweaks (< 10px movement)
- Text alignment or font size changes
- Small button additions (using existing templates)
- Tooltip additions or corrections
- Minor spacing/padding adjustments
- Bug fixes (< 20 lines of code)

❌ **No - Create Phase Instead**:
- New window layouts or major refactors
- Multi-window coordination changes
- New feature implementations (gauges, tabs, etc.)
- Changes requiring > 100 lines of XML
- Changes affecting multiple interconnected systems
- Architectural decisions or pattern changes

**When in Doubt**: If it takes > 30 minutes to implement, it's probably a phase, not a quick hit.

---

## 👥 Group Window

- [x] **Review and verify F2-F6 keyboard label positioning** (COMPLETED - 2026-02-03)
  - [x] Verified F2-F6 labels positioned correctly with no gauge overlap
  - [x] Confirmed consistent 28px vertical spacing throughout window
  - [x] No adjustment needed - labels verified fine

- [x] **Verify player bars alignment** (COMPLETED - 2026-02-03)
  - [x] Verified all 5 player health gauges properly aligned
  - [x] Confirmed proper spacing between all elements
  - [x] All player bars horizontally and vertically consistent
  - [x] Note: Group Window contains only health gauges, not mana

- [x] **Align pet gauges to match player gauges** (COMPLETED - 2026-02-03)
  - [x] Fixed pet gauge X positions from 16 to 11 (matching player health gauges)
  - [x] All GW_PetGauge1-5 now aligned with GW_Gauge1-5
  - [x] Ensures consistent visual alignment across all 5 group member bars
  - [x] Commit: a228f2a

## 🐾 Pet Window

- [x] **Redesign Pet Health Gauge Layout**
  - [x] Convert pet health gauge to tall vertical bar (matching new Player window pet gauge style)
  - [x] Shift all buttons down to accommodate taller gauge
  - [x] Reposition percentage labels to align with new gauge height
  - [x] Adjust overall window alignment to ensure all elements fit properly
  - [x] Change pet health gauge color to be more red (currently too purple)
  - [x] Test gauge scaling and button functionality with new layout
  - [x] Verify visual consistency with redesigned Player window pet gauge

- [x] **Restore and Display Hidden Buttons**
  - [x] Show "go away" button on pet window
  - [x] Display other hidden pet window buttons (currently suppressed)
  - [x] Verify button positioning and sizing consistency
  - [x] Test button functionality in-game
- [x] Review pet window layout for consistency with other windows
- [x] Quick win items from above: "Display 'go away' button", "Show hidden pet window buttons"

## 🧙 Player Window

- [x] **Add weight display to lower right corner** (COMPLETED - commit 2e7d647)
  - [x] Positioned on same line as pet HP labels (Y=96)
  - [x] Right-aligned with 3px margin matching XP/H standard above
  - [x] Format: "999/999" (cur/max using EQType 24 & 25)
  - [x] Follows established positioning standards

- [x] **Reorganize Pet Health Gauge and Stat Bars**
  - [x] Convert pet health to tall vertical bar gauge (similar to HP/Mana style)
  - [x] Move pet health gauge UP to current Stamina bar position
  - [x] Shift Stamina and other bars DOWN to accommodate tall pet health gauge
  - [x] Remove "PT:" label to allow taller pet health gauge
  - [x] Overlay pet's name on the pet health gauge itself
  - [x] Reposition right-side labels (%, XP/H, WEIGHT) to align with shifted bars
  - [x] Adjust all percentage field positions to match new bar layout
  - [x] Change pet health gauge color to be more red (currently too purple)
  - [x] Test all gauge scaling and label positioning
  - [x] Verify visual balance and readability with new layout

## 📦 Inventory Layout Consistency

- [x] **Phase 3.9: Inventory System Redesign** (COMPLETED - v0.6.0, February 6, 2026)
  - [x] Implemented anatomical 4-column equipment layout (21 armor slots)
  - [x] Unified slot sizing to 45x45px for consistency and easier clicking
  - [x] Implemented 2px gap spacing throughout equipment grid
  - [x] Organized equipment slots by body location:
    - [x] Row 1: Head level (Ears, Neck, Face, Head)
    - [x] Row 2: Arm level (Rings, Wrists, Arms, Hands)
    - [x] Row 3: Torso level (Shoulders, Chest, Back, Waist, Legs, Feet)
    - [x] Row 4: Weapons level (Primary, Secondary, Range, Ammo)
  - [x] Repositioned currency zone with proper spacing (Y=253)
  - [x] Grid dimensions: 166×208px equipment grid in 215×210px zone
  - [x] All backgrounds using icon-specific animations from window_pieces02.tga
  - [x] Updated Options/Inventory variants (Standard, Enhanced)
  - [x] Comprehensive documentation in .development/initial-phases/PHASE-6-INVENTORY-WINDOWS/
  - [x] Commits: 074c6ae, 8e29cad, 1fbce3c, cdacd9c, ef53083, b236e93, 7a1c076, c49212b, f5476b7, e785cb0

- [x] **Texture Fixes and Validation** (COMPLETED - v0.6.0, February 6, 2026)
  - [x] Fixed scrollbar_gutter.tga dimensions (0x0 → 16x16)
  - [x] Converted classic_pieces01.tga from PNG to proper TGA format
  - [x] Converted window_pieces01.tga from PNG to proper TGA format
  - [x] Fixed UTF-8 character encoding in XML files (replaced × with x)
  - [x] Added missing AttackIndicator.tga TextureInfo definition (222x34)
  - [x] Validated all 45 .tga files (proper format and file sizes)
  - [x] Resolved UIError.txt and Texture.txt startup errors
  - [x] Commits: 035bae3, 111e7f5

- [x] **Add AA stats to Inventory window** (COMPLETED - v0.6.0, February 2026)
  - [x] Added AA label, current AA (EQType 36), and max AA (EQType 37) fields to Inventory window
  - [x] Established standard field grouping organization for Inventory window
  - [x] Positioned AA fields alongside existing player stat fields (Level, Class, Weight, HP, Mana)
  - [x] Implemented field clustering pattern: Character Identity (Name/Level/Class/Deity) + Stat Metrics (HP/Mana/AC/ATK/EXP/AA)
  - [x] Included AA gauge (EQType 5) and percentage display (EQType 27)

- [x] **Major Revision: Armor Layout Consolidation** (COMPLETED as Phase 3.9)
  - [x] Redesigned inventory armor/equip display with logical anatomical grouping
  - [x] Organized equipment slots by body location (head → feet)
  - [x] Adjusted equipment grid positioning relative to currency zone
  - [x] Reviewed and reorganized all inventory slot positioning
  - [x] Ensured armor display visually groups related items by body location
  - [x] Tested spacing and alignment with armor groupings

- [x] **Standardize inventory display order across all windows** (COMPLETED as Phase 3.9)
  - [x] Audited inventory displays in Inventory window
  - [x] Defined logical item sequence (anatomical armor first, then bags/inventory)
  - [x] Consolidated inventory slot display into consistent 45x45px layout
  - [x] Documented standard sequence in STANDARDS.md
  - [x] Re-ordered all equipment slots to match anatomical standard
  - [x] Tested displays with equipped items
  - [x] Verified visual consistency across inventory layout

## ⚔️ Actions Window

- [x] **Player Info Tab Enhancement** (COMPLETED)
  - [x] Reposition Player Level to same line as Name with "Lvl" label (commit ae6c629)
  - [x] Add Player Class display to tab (commit c67bb3f)
  - [x] Add weight display (cur/divider/max format) to Player Info tab (commit ae6c629)
  - [x] Add AA Points display (cur/divider/max format) to Player Info tab (uncommitted, ready for verification)
    - [x] Positioned at Y=94 with proper right-justification alignment
    - [x] Field grouping established: Character Identity Cluster (Name/Level/Class) separated from Stat Metrics Cluster (HP/Mana/Weight/AA)

- [ ] **Player Info Tab - Deity Addition** (NOT POSSIBLE - February 2026)
  - ❌ Cannot add Deity display to Player Info tab
  - ❌ No available EQType for character deity in TAKP/P2002 client
  - ❌ Technical limitation - deity data not exposed to UI layer
  - Note: Character Identity Cluster remains Name/Level/Class only

- [x] Create alternate version without inventory tabs
- [x] Reduce height to accommodate actions-only layout
- [x] Test compatibility with player window stacking

## 🏠 Textures & Visuals

- [x] Revisit classic_pieces01.tga appearance
  - [x] Improve overall visual quality
  - [x] Increase transparency of backgrounds
  - [x] Maintain darker tone/contrast
  - [x] Fix and improve armor slot labels/descriptions

## 🎨 Stat Icons Integration

- [ ] **Explore Stat Type Icons from duxaui and vert variants**
  - [ ] Audit stat icons available in duxaui and vert directories
  - [ ] Document icon set (size, format, stat coverage)
  - [ ] Identify windows where stat icons would enhance visuals (Player, Merchant, Actions, Target)
  - [ ] Create prototype layouts with stat icons vs text labels
  - [ ] Evaluate space/layout trade-offs (icons require more space than text)
  - [ ] Test different presentation approaches:
    - [ ] Text-only (current approach)
    - [ ] Icons-only (duxaui style)
    - [ ] Icons + short labels (hybrid approach)
    - [ ] Tabbed views (if practical)
  - [ ] Determine which approach works best for each window

- [ ] **Create stat icon Options variants**
  - [ ] Design thorne_drak variant with stat icons
  - [ ] Create at least 2 layout options (e.g., "Icons-Heavy" vs "Text-Focused")
  - [ ] Each variant shows stat icons applied consistently
  - [ ] Document design decisions for each variant
  - [ ] Allow users to choose variant based on preference

- [ ] **Document findings and decisions**
  - [ ] Record pros/cons of each icon approach tested
  - [ ] Note space trade-offs discovered
  - [ ] Create guidelines for future stat icon usage
  - [ ] Update STANDARDS.md with stat icon recommendations

## 🖼️ Title Bars

- [x] Review and darken title bar background colors across all windows
  - Related quick win item: "Review and darken title bar background colors"
  - Current colors appear too light
  - Ensure consistent darker theme

## 💬 Selector Window

- [x] **Create Vertical Selector Window Layout** (COMPLETED - Feb 3, 2026)
  - [x] Convert horizontal layout (278×50px) to vertical (38×278px)
  - [x] Reposition all 9 buttons from horizontal to vertical arrangement
  - [x] Remove titlebar for streamlined design (WDT_RoundedNoTitle)
  - [x] Add 2px button inset from top and left edges
  - [x] Create Options/Selector/Vertical variant with README
  - [x] Maintain Standard horizontal variant as baseline
  - [x] Document both layouts in Options master README

## 🗡️ Action Buttons & Social Commands

- [ ] Investigate adding action buttons (melee attack, ranged attack) to Notes window
- [ ] Investigate adding social commands to Notes window
- [ ] Verify if custom button functionality works on Notes window
- [ ] Consider if Potionbelt window could also support action/social buttons
- [ ] Test interaction with existing hot button features

## � Hot Button Window Layout Redesign

- [x] **Reorganize Bag and Armor Slot Layout**
  - [x] Move bag slots (currently HB2_InvSlot1-8) to the right of the scrollbar
  - [x] Expand default window size to display all bag slots without scrolling
  - [x] Move Primary and Secondary weapon slots to be first TWO bag slot positions
  - [x] Shift remaining bag slots over to accommodate Primary/Secondary relocation
  - [x] Move armor slots (currently HB3/HB4 rows) UP to replace where bags were positioned
  - [x] Ensure proper spacing and alignment after relocation
  - [x] Update window size to accommodate new layout (currently 440x178)
  - [x] Test all slot interactions and verify EQType bindings remain correct
  - [x] Verify proper rendering with scrollbar positioning

- [x] **Visual Polish and Testing**
  - [x] Review button/slot spacing consistency in new layout
  - [x] Test with various screen resolutions
  - [x] Verify sizable window behavior with new default size
  - [x] Ensure hot button pages (HB, HB2, HB3, HB4) still function correctly
  - [x] Document new layout design in STANDARDS.md

## �🏪 Merchant Window

- [x] Create tabbed version with selectable columns
  - [x] Allow user to choose which columns to display
  - [x] Support adjustable slot/item sizes
  - [x] Implement tabs for different display configurations
- [x] Create standard merchant window variant
  - [x] Remove bottom tab section
  - [x] Provide as default "standard" option
  - [x] Ensure both custom and standard versions available

## 🎯 Target Window

- [x] Investigate adding player HP gauge to target window
- [x] Investigate adding player Mana gauge to target window
- [x] Consider positioning and label requirements
- [x] Test for EQType binding compatibility

- [x] **Create Pet-Friendly Target Window Variant** (COMPLETED - v0.6.0, February 2026)
  - [x] Added pet health gauge (TW_PetHealth_Gauge) to main Target Window
  - [x] Positioned directly below player health gauge (Y=24)
  - [x] Standard 122x8 gauge size matching player HP/Mana gauges
  - [x] Purple/magenta fill (R=200, G=80, B=200) for pet health
  - [x] EQType 16 binding for pet health data
  - [x] Integrated into main window (all variants include pet gauge)
  - [x] Vertical spacing maintained with casting gauge and mana tick gauge
  - [x] Use Case: Pet classes (Necromancer, Magician, Beastlord, Druid) can monitor pet HP during combat

## 🧰 Open All Bags Button

- [x] **Research "Open All Bags" Functionality**
  - [x] Search for existing EQType that triggers opening multiple bags
  - [x] Investigate if client supports bulk bag-open command
  - [x] Check if button click event can trigger bag opening
  - [x] Research macro/scripting solutions if EQ UI doesn't support natively
  - [x] Review EQUI_Inventory.xml for bag slot definitions (EQType 22-29)
  - [x] Determine if this is UI-level or requires client support
  - [x] Document findings in technical notes

- [x] **If Not Natively Possible**
  - [x] Document limitations in STANDARDS.md
  - [x] Research third-party solutions (macros, external tools)
  - [x] Provide documentation for users on alternatives

## 🎪 Target of Target (AOE/Aggro Targeting)

- [x] Research available EQTypes for Target of Target data
- [x] Investigate if EQType exists to show who target is targeting
- [x] Test implementation if available
- [x] Consider UI layout if multiple targets need display

## 📚 Spellbook & Spell Gems

- [ ] **Compare Spell Book vs Gem Icon Display**
  - [ ] Document visual discrepancies between spellbook icons and corresponding gem icons
  - [ ] Create comparison list of spells with mismatched visual representation
  - [ ] Determine root cause: Is it texture source, animation, or rendering difference?
  - [ ] Investigate if this is a client-side rendering issue or UI configuration problem

- [ ] **Investigate Icon Source Mismatch**
  - [ ] Audit EQUI_SpellBookWnd.xml for icon display definitions
  - [ ] Audit EQUI_CastSpellWnd.xml (spell gems) for icon display definitions
  - [ ] Document differences in EQType/AnimLoop references between windows
  - [ ] Determine why same spells show different icons on different windows
  - [ ] Research animation files (EQUI_Animations.xml) for spell icon references
  - [ ] Identify correct/canonical icon source for each spell

- [ ] **Address Spell Gem Display Issues**
  - [ ] Investigate the dual-image overlay on spell gems
  - [ ] Determine if overlay is intentional or display bug
  - [ ] Document root cause (incorrect texture reference, animation issue, etc.)
  - [ ] Test if reconciling icon sources resolves overlay issue

- [ ] **Increase Spellbook Icon Size**
  - [ ] Measure current icon dimensions in spellbook window
  - [ ] Research maximum viable icon size without UI layout breaking
  - [ ] Test scaling up icons while maintaining readability
  - [ ] Consider impact on window sizing/layout requirements
  - [ ] Implement size increase if feasible
  - [ ] Verify functionality (spell selection, drag-and-drop to gems works)

- [ ] **Reconcile Icon Display Approach**
  - [ ] After investigation, document canonical approach
  - [ ] Update STANDARDS.md with spell icon guidelines
  - [ ] Apply reconciliation to spellbook and spell gems
  - [ ] Create testing checklist for spell icon consistency
  - [ ] Test with various spell types (direct damage, buffs, heals, debuffs)

## 🎯 UI Standards Investigation

Research and standardize UI patterns discovered in other EverQuest variants:

- [ ] **Window Drag Affordances (Windowless Title Bars)**
  - [ ] Audit existing UI files (duxaui, vert, Infiniti-Blue) for drag area patterns
  - [ ] Document how drag areas are implemented (dummy elements at top-left of windows)
  - [ ] Determine which window types benefit from visible drag area
  - [ ] Decide if this should be standard for windows without visible title bars
  - [ ] Test usability with/without visible drag affordances
  - [ ] Document standard approach in STANDARDS.md
  - [ ] Apply decision to thorne_drak windows (Pet, Actions, Merchant, etc.)

- [ ] **Other UI Affordances from Variant Analysis**
  - [ ] Document other patterns observed in duxaui, vert, Infiniti-Blue
  - [ ] Evaluate suitability for thorne_drak design philosophy
  - [ ] Document rationale for including/excluding patterns

## 🚀 General Optimizations

- [ ] Review window spacing and alignment standards
  - Related quick win item: "Review window border spacing standards (2px/4px consistency)"
  - Ensure borders are consistently 2px left, 4px right
- [ ] Button sizing uniformity across all windows
  - Related quick win item: "Check button sizing uniformity across windows"
  - Compare all window button sizes for consistency
- [ ] Color palette consistency check
- [ ] Performance optimization opportunities
- [ ] Other improvements discovered during development

## 🏗️ Architecture & Animations

- [ ] **Decouple Options from Global Animation Changes**
  - [ ] Audit current custom animation changes (what was added/modified vs default animations.xml)
  - [ ] Determine which animations should be window-specific vs globally shared
  - [ ] Evaluate feasibility of moving custom animations into individual window XML files
  - [ ] Goal: Make Options self-contained and portable without external animation dependencies
  - [ ] Benefit: Options variants could be deployed independently without assuming prior customizations
  - [ ] Consider approach: Should animations be inline in window files or modular?
  - **Note**: Low priority - strategic architectural decision for future project portability

## 📝 Notes

- Keep track of EQType discoveries for reference
- Document any new gauge templates created
- Maintain consistent naming conventions for variants
- Test all changes in-game before committing

---

## 📝 License

Custom UI for personal use with The Al'Kabor Project.

Maintainer: Draknare Thorne
