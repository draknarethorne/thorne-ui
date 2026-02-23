[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 3.7: UI Infrastructure & Template Standardization ✅

**Status**: COMPLETED  
**Priority**: High (Supporting infrastructure for all windows)  
**Completion Date**: January 16-30, 2026

## Objectives

- Fix corrupted and malformed UI assets (TGA files)
- Standardize window templates across Options variants
- Enhance core windows with improved layouts and stats
- Expand Options directory with additional window variants
- Ensure consistent title bar rendering and styling

## TGA/Asset Fixes (Jan 29, 2026)

### Problem Statement

Several texture assets were corrupted or in incorrect formats:
- `wnd_bg_light_rock.tga` was corrupted, causing transparent title bars
- `classic_pieces01.tga` had incorrect TGA type (needed type 10 RLE format)
- Custom texture references needed cleanup

### Solution Implemented

**1. Title Bar Fix** (Commit 6966aeb):
- Replaced corrupted `wnd_bg_light_rock.tga` references with `wnd_bg_dark_rock.tga`
- Updated rounded frame title animations in EQUI_Animations.xml
- Fixed transparency issues across all windows using rounded templates

**2. Classic Pieces Restoration** (Commit daba5b7, a7dceeb):
- Restored `classic_pieces01.tga` to proper TGA format (type 10, RLE compression)
- Added to Options/Inventory/Dark Slots and Color Weapons variants
- Created Python script (`.bin/fix_tga_files.py`) with improved validation and verbose output

**3. Asset Cleanup** (Commit 46c6982, eddd78d):
- Removed obsolete `custom_pieces_01.tga` from thorne_drak
- Cleaned up documentation references to removed assets
- Standardized on `classic_pieces01.tga` for gauge textures

### Files Affected

- `thorne_drak/EQUI_Animations.xml`
- `thorne_drak/Options/Inventory/Dark Slots/classic_pieces01.tga`
- `.bin/fix_tga_files.py` (utility script)

### Impact

Fixed visual glitches across all windows using rounded templates and gauge animations.

---

## Template Standardization (Jan 29, 2026)

### Goal

Ensure consistent title bar appearance and window styling across all Options variants.

### Changes Implemented (Commits 155062a, 46f5446, 962474d)

**1. OptionsWindow Template Update**:
- Changed from `WDT_RoundedNoTitle` to `WDT_Rounded` for proper titlebar integration
- Added Font element to match HotButtonWnd title bar rendering
- Ensures consistent appearance with other UI windows

**2. Options Directory Template Rollout**:
- Applied `WDT_Rounded` template to all Options window variants
- Standardized rounded styling across:
  - Hotbutton variants
  - Merchant variants
  - Loot variants
  - Player variants
  - Pet variants
  - Group variants
  - Actions variants
  - Spellbook variants
  - Inventory variants
  - Skin variants
- Ensures visual consistency when users swap between variants

### Files Affected

- `thorne_drak/EQUI_OptionsWindow.xml`
- All Options subdirectory XML files (Hotbutton, Merchant, Loot, Player, Pet, Group, Actions, Spellbook, Inventory, Skin)

### Impact

Unified window styling across UI, professional appearance, easier variant swapping.

---

## Window Enhancements & Standardization (Jan 30, 2026)

### Major Windows Updated (Commits d243c70, 940c90a)

### 1. Actions Window (ActionsWindow.xml)

**Enhancements**:
- **Added Stats**: AC (Armor Class) and ATK (Attack) displays
- **Layout Improvements**: Stat lines swapped, centered, and color-coded
- **Options Variant Created**: Options/Actions/Standard/ with full stat layout
- **Purpose**: Provides critical combat stats at-a-glance for melee/tank classes

**Impact**: Enhanced combat awareness without opening separate windows

### 2. Inventory Window (Inventory.xml)

**Enhancements**:
- **Tab Removal**: Removed tab controls for cleaner, simpler UI
- **AA Button Addition**: Quick-access Alternate Advancement button
- **Button Reorganization**: Swapped button positions for better flow
- **Pieces Cleanup**: Streamlined texture references
- **Purpose**: Simplified standard variant; tabs remain in Options/Inventory variants

**Impact**: Clean, minimal standard layout with feature-rich Options alternatives

### 3. Merchant Window (MerchantWnd.xml)

**Enhancements**:
- **Standardization**: Aligned with Actions window layout principles
- **Options Variants Created**:
  - Large Inventory variant with tabbed interface
  - Bags variant with expanded slots
- **Purpose**: Standard no-tabs layout in main directory; feature-rich tabs in Options

**Impact**: Consistent with Phase 3 merchant enhancements, better variant management

### 4. LoadskinWnd (Skin Selection)

**Enhancements**:
- **Infiniti-Blue Port**: Imported layout from Infiniti-Blue UI variant
- **Window Resize**: Adjusted dimensions for better fit
- **Button Re-alignment**: Fixed button positioning after resize
- **Options Variants Created**:
  - Standard layout
  - Slightly Taller and Wider variant
- **Purpose**: Improved UI skin selector with better button placement

**Impact**: Better user experience when swapping UI skins

### 5. Spellbook Window (SpellBookWnd.xml)

**Enhancements**:
- **Documentation Sync**: Added comprehensive layout documentation
- **Minor Layout Tweaks**: Aligned with PlayerNotesWindow consistency
- **Options Variant Created**: Options/Spellbook/Standard/ variant

**Impact**: Consistent documentation and layout standards

### Files Affected

- `thorne_drak/EQUI_ActionsWindow.xml`
- `thorne_drak/EQUI_Inventory.xml`
- `thorne_drak/EQUI_MerchantWnd.xml`
- `thorne_drak/EQUI_LoadskinWnd.xml`
- `thorne_drak/Options/Actions/Standard/EQUI_ActionsWindow.xml`
- `thorne_drak/Options/Merchant/Large Inventory/EQUI_MerchantWnd.xml`
- `thorne_drak/Options/Merchant/Bags/EQUI_MerchantWnd.xml`
- `thorne_drak/Options/Skin/Standard/EQUI_LoadskinWnd.xml`
- `thorne_drak/Options/Skin/Slightly Taller and Wider/EQUI_LoadskinWnd.xml`
- `thorne_drak/Options/Spellbook/Standard/EQUI_SpellBookWnd.xml`

---

## Options Directory Expansion (Jan 30, 2026)

### New Options Variants Created (Commit c0f871f)

**Loot Window**:
- **Created**: `Options/Loot/Standard/EQUI_LootWnd.xml`
- **Purpose**: Provides user-selectable loot window variant
- **Lines**: 724 lines of SIDL XML

**Merchant Window**:
- **Created**: `Options/Merchant/Standard/EQUI_MerchantWnd.xml`
- **Purpose**: Feature-rich merchant interface with tabs
- **Lines**: 1676 lines of SIDL XML
- **Additional Variants**: Large Inventory and Bags (created in commit 940c90a)

**Supporting Assets**:
- **Added**: `classic_pieces01.tga` to Dark Slots and Color Weapons variant directories
- **Purpose**: Gauge texture assets for inventory variants

**Documentation**:
- Created window-specific markdown documentation in respective Options directories
- Added README.md files explaining variant purposes and selection

### Impact

Users now have 11 Options subdirectories (Actions, Animations, Group, Hotbutton, Inventory, Loot, Merchant, Pet, Player, Skin, Spellbook) with multiple variant choices.

---

## Bulk Window Standardization (Jan 16, 2026)

**Mass Update** (Commit b6111a8):
- **Files Affected**: 40+ EQUI_*.xml files
- **Scope**: AAWindow, BankWnd, BuffWindow, BugReportWnd, CastSpellWnd, ChatWindow, Container, and more
- **Changes**: Standardized window templates, title bar styles, and rounded frame animations
- **Purpose**: Ensure visual consistency across all thorne_drak windows

---

## Learnings

### TGA File Format Requirements

**Discovery**: EverQuest client requires specific TGA format for texture assets
- **Type 10**: RLE (Run-Length Encoded) compression required for compatibility
- **Type 2**: Uncompressed format causes rendering issues
- **Corruption Detection**: Files with incorrect headers cause transparent/missing textures
- **Validation Script**: Created `.bin/fix_tga_files.py` for automated format checking and repair

### Custom Texture Asset Management

**Best Practice**: Keep custom textures in Options variants only
- Main directory uses standard EverQuest textures (`classic_pieces01.tga`, `wnd_bg_dark_rock.tga`)
- Options variants can include custom assets for specialized layouts
- Reduces maintenance burden and simplifies troubleshooting

### Template Standardization Impact

**Before**: Inconsistent window styling across Options variants
- Some used `WDT_RoundedNoTitle` (no title bar)
- Some used `WDT_Rounded` (proper title bar)
- Font element missing in some variants

**After**: Unified `WDT_Rounded` template across all Options
- Professional appearance with consistent title bars
- Easy variant swapping without visual discontinuity
- Reduced user confusion when testing different layouts

### Window Width Calculation

**Standard Pattern**: Window width = content width + border margins
- Content area typically 310-320px for merchant/loot windows
- Add 10-15px for left/right borders and padding
- Total: 325-335px typical merchant window width

## Challenges

### TGA Corruption Root Cause

**Problem**: `wnd_bg_light_rock.tga` was corrupted in repository
- Caused transparent title bars across multiple windows
- Difficultto diagnose (no obvious error messages)
- Required visual inspection to identify issue

**Solution**: Replaced with known-good `wnd_bg_dark_rock.tga`
- Updated all animations referencing corrupted file
- Verified all windows render correctly after change

### Bulk Template Updates

**Challenge**: Updating 40+ XML files consistently
- Risk of introducing typos or missing files
- Need to verify each file after modification
- Time-consuming manual validation process

**Solution**: Search/replace with verification
- Used grep to find all files needing updates
- Batch replaced template references
- Tested representative sample in-game to verify correctness

## Technical Notes

### TGA Format Specifications

**RLE Compression (Type 10)**:
- Reduces file size for textures with repeated colors
- Required by EverQuest client for proper rendering
- Created with image editing tools (GIMP, Photoshop, etc.)

**Validation Script** ([.bin/fix_tga_files.py](../../.bin/fix_tga_files.py)):
```python
# Checks TGA header for correct type (10 = RLE)
# Repairs incorrect formats by converting to Type 10
# Provides verbose output for troubleshooting
```

### Window Template Hierarchy

**Available Templates** (See [EQUI_Animations.xml](../../thorne_drak/EQUI_Animations.xml)):
- `WDT_Rounded`: Standard rounded frame with title bar
- `WDT_RoundedNoTitle`: Rounded frame without title bar
- `WDT_Square`: Square frame with sharp corners
- Custom templates: Can be defined for specialized windows

**Template Selection Guide**:
- Use `WDT_Rounded` for most windows (consistent appearance)
- Use `WDT_RoundedNoTitle` only when title bar interferes with layout
- Avoid custom templates unless absolutely necessary (maintenance burden)

### Before/After Comparison

**Title Bar Fix**:
```xml
<!-- BEFORE (corrupted texture) -->
<Animation>A_RoundedFrameTitle</Animation>
  <Texture>wnd_bg_light_rock.tga</Texture>  <!-- CORRUPTED -->

<!-- AFTER (working texture) -->
<Animation>A_RoundedFrameTitle</Animation>
  <Texture>wnd_bg_dark_rock.tga</Texture>  <!-- VERIFIED WORKING -->
```

**Template Standardization**:
```xml
<!-- BEFORE (inconsistent) -->
<Screen item="OptionsWindow" Template="WDT_RoundedNoTitle">
  <!-- Missing Font element, no title bar -->

<!-- AFTER (standardized) -->
<Screen item="OptionsWindow" Template="WDT_Rounded">
  <Font>3</Font>  <!-- Matches HotButtonWnd title bar rendering -->
```

## Impact

- Professional, polished appearance across all thorne_drak windows
- Eliminated visual glitches caused by corrupted texture assets
- Established template standards for future window development
- Created validation tools for maintaining asset quality
- Simplified variant management through consistent styling

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Technical References](../../.docs/technical/EQTYPES.md)
