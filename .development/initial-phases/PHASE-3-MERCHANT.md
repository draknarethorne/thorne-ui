[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 3: Merchant Window Enhancements ✅

**Status**: COMPLETE (v0.3.0)  
**Priority**: High  
**Completion Date**: December 2025

## Objectives

- ✅ Make Merchant window self-sufficient during shopping
- ✅ Eliminate need to open separate Inventory/Stats windows
- ✅ Match visual aesthetics of Inventory window
- ✅ Verify alignment and spacing under all conditions

## Deliverables

- ✅ Merchant window redesigned (3 tabs: Bags/Equipment/Stats)
- ✅ Bags tab: Full inventory display + weapon slots + EXP/XP/WEIGHT blocks
- ✅ Equipment tab: Armor grid + weapon slots
- ✅ Stats tab: Comprehensive 3-column HUD (HP/Mana/AC/ATK, Attributes, Resists)
- ✅ All colors match Inventory window standard
- ✅ Two variants provided:
  - **Standard** (main directory): Classic merchant without tabs
  - **Large Inventory and Bags** (Options/Merchant): Full tabbed implementation
- ✅ Tab definitions preserved in main XML for easy variant creation
- ✅ Potion Belt reminder button added to Actions Main tab
- ✅ XML validation passing on all files
- ✅ Documentation updated with discoveries and decisions

## Implementation Details

### File Structure

**Main Variant**: [thorne_drak/EQUI_MerchantWnd.xml](../../thorne_drak/EQUI_MerchantWnd.xml)
- Standard merchant layout without tabs (classic design)
- Compact footprint for minimal screen usage
- Compatible with separate Inventory/Stats windows

**Options Variant**: [thorne_drak/Options/Merchant/Large Inventory and Bags/EQUI_MerchantWnd.xml](../../thorne_drak/Options/Merchant/Large%20Inventory%20and%20Bags/EQUI_MerchantWnd.xml)
- 3-tab comprehensive interface (Bags/Equipment/Stats)
- 1676 lines of SIDL XML
- Self-sufficient shopping experience

**Documentation**: [Options/Merchant/Large Inventory and Bags/README.md](../../thorne_drak/Options/Merchant/Large%20Inventory%20and%20Bags/README.md)
- Installation instructions
- Tab descriptions
- Feature overview

### Tab Structure

**Bags Tab**:
- Complete inventory bag grid display (29 slots)
- Weapon slots (Primary, Secondary, Range, Ammo)
- Experience/XP/Weight status blocks
- Self-sufficient shopping experience
- EQType bindings: InvSlot0-InvSlot28 for bags, InvSlot13-21 for weapons
- Layout: Horizontal bag arrangement matching Inventory window

**Equipment Tab**:
- Armor slot grid layout (slots 0-21)
- Weapon slots integration
- Quick gear reference while shopping
- EQType bindings: InvSlot0-21 for all equipment slots
- Layout: Anatomical organization (head, torso, arms, legs, hands, feet)

**Stats Tab**:
- HP/Mana/AC/ATK combat stats
- Attribute display (STR, STA, AGI, DEX, WIS, INT, CHA)
- Resistance values (Poison, Disease, Fire, Cold, Magic)
- Three-column HUD layout
- EQType bindings: HP, Mana, AC, Attack, STR, STA, AGI, DEX, WIS, INT, CHA, ResistPoison, ResistDisease, ResistFire, ResistCold, ResistMagic
- Layout: Left (HP/Mana/AC/ATK), Center (Attributes), Right (Resistances)

### Color Scheme Standardization

All labels and values use canonical Inventory window color palette:
- White (255, 255, 255): Default text, values
- Blue (50, 160, 250): Attribute labels
- Pink/Rose (200, 120, 145): HP/Mana labels
- Orange (255, 165, 0): ATK, Fire resist
- Cyan (0, 165, 255): Cold resist
- Purple (195, 0, 185): Magic resist
- Yellow (205, 205, 0): Disease resist
- Teal (0, 130, 100): Poison resist

## Options Directory Pattern

**Innovation**: Established Options directory structure for variant management
- **Standard variant**: Main directory contains classic no-tabs merchant
- **Feature-rich variants**: Options/Merchant contains tabbed implementations
- **Variant preservation**: Unused element definitions kept in XML for easy variant creation
- **User choice**: Players can swap variants by copying files from Options subdirectories

## Learnings

- **Global UI Positioning**: Requires element duplication for per-tab customization
  - Same element name = same position across all tabs
  - Solution: Duplicate elements with unique names (e.g., `MW_Bags_Primary` vs `MW_Equipment_Primary`)
- **Client API Limitations**: Cannot execute slash commands from custom buttons
  - Custom buttons only work with hardcoded ScreenIDs (Inventory, AA, etc.)
  - Workaround: Use buttons as visual reminders + hotkey macros for commands
- **Fading Windows**: Identified fade-safe materials for future window designs
  - MerchantWnd participates in client-controlled transparency
  - UI must account for `/viewport` transparency settings
- **Color Standardization**: Inventory window established as canonical color reference
  - All labels/values use [Inventory color palette](../STANDARDS.md#color-palette)
  - Consistency improves recognition across different windows
- **Options Pattern**: Directory structure allows multiple variants without code duplication
  - Main directory: Standard/minimal variant
  - Options/Merchant: Feature-rich variants
  - Users swap by copying files from Options subdirectories
- **XML Preservation**: Keeping unused definitions simplifies creating new variants
  - Tab definitions remain in XML even when main variant doesn't use tabs
  - Enables quick variant creation by copying/uncommenting code blocks
  - Reduces technical debt and maintenance burden

## Challenges

- **Tab State Management**: No built-in state persistence across `/loadskin` commands
  - User must manually switch back to desired tab after UI reload
  - Cannot save "last used tab" preference in XML
- **Element Naming**: Required careful planning to avoid naming conflicts
  - Created naming convention: `MW_[TabName]_[ElementName]`
  - Example: `MW_Bags_InvSlot0`, `MW_Equipment_InvSlot0`, `MW_Stats_HP`
- **Testing Complexity**: Three tabs mean 3x validation effort
  - Each tab needed thorough testing for alignment, color, EQType bindings
  - Required vendor visits, inventory manipulation, stat changes to verify correctness

## Technical Notes

**Window Dimensions**:
- Width: 330px (accommodates merchant list + tabs)
- Height: ~345px (includes tab content area)
- Template: `WDT_Rounded` for title bar integration

**Tab Implementation**:
```xml
<Page item="MW_Page_Bags">
  <ScreenID>MW_Bags_Screen</ScreenID>
  <!-- Bag grid, weapon slots, status blocks -->
</Page>
```

**EQType Bindings** (See [Technical References](../technical/eqtypes.md) for complete list):
- Inventory slots: `InvSlot0` through `InvSlot28`
- Weapon slots: `InvSlot13` (Primary), `InvSlot14` (Secondary), `InvSlot11` (Range), `InvSlot21` (Ammo)
- Stats: `HP`, `Mana`, `AC`, `Attack`, `STR`, `STA`, `AGI`, `DEX`, `WIS`, `INT`, `CHA`
- Resists: `ResistPoison`, `ResistDisease`, `ResistFire`, `ResistCold`, `ResistMagic`

## Impact

- Self-sufficient merchant shopping experience
- Reduced window clutter (no need for separate Stats/Inventory windows)
- Established Options directory pattern used in all subsequent phases
- Created color palette standard applied across entire UI

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Technical References](../technical/eqtypes.md)
