# Pet Window - Tall Gauge Variant

**File**: [EQUI_PetInfoWindow.xml](./EQUI_PetInfoWindow.xml)
**Version**: 1.1.0  
**Last Updated**: 2026-02-03
**Status**: ✅ Enhanced variant with improved readability  
**Author**: Draknare Thorne (modified from original by Brujoloco)

---
## Purpose

The "Tall Gauge" Pet Window variant provides an enhanced display for your summoned pet with larger, more readable gauges optimized for visibility during active play.

**Key Features**:

- **Tall HP Gauge**: 15px height for enhanced visibility
- **Pet Name Display**: White text for contrast against purple background
- **Quick Commands**: Attack, Follow, Guard, Taunt, Dismiss buttons
- **Consistent Styling**: Matches Player and Target window aesthetics
- **EQType Support**: HP/Mana values (EQTypes 16/17), numeric labels (EQType 69)

---

## Specifications

| Property | Value |
|----------|-------|
| **Window Size** | 160 × 125 pixels (fixed, non-resizable) |
| **Layout Type** | Vertical gauge with button row |
| **Resizable** | No |
| **Titlebar** | No (WDT_NoTitle) |
| **Background** | Dark purple (RGB 32, 16, 64) with rounded corners |
| **HP Gauge Height** | 15px (tall variant) |
| **Mana Bar Height** | 2px (thin line) |
| **Buttons** | 6 (Attack, Follow, Guard, Taunt, Dismiss, Sit) |
| **Pet Name Color** | White (RGB 255, 255, 255) |
| **Font** | Font 3 with TextOffsetX=4, TextOffsetY=0 |
| **EQTypes Used** | 16 (HP), 17 (Mana), 69 (HP Value) |

---

## Modifications (v1.1.0 - Feb 3, 2026)

- **Pet Name Color**: Changed to white (RGB 255,255,255) from green for better contrast
- **Text Offset**: Standardized to TextOffsetX=4, TextOffsetY=0 matching Player Window

---

## Layout Components

### Main Window Structure
The window is composed of two primary sections:

1. **Gauge Area** (top, 160 × 28px)
   - HPGauge: 160 × 15px with percentage display and numeric value
   - ManaGauge: 160 × 2px thin indicator line
   - Pet Name: White text label above gauges

2. **Command Buttons** (bottom, 160 × 97px)
   - Single row of 6 command buttons
   - Each button: ~27px wide × 18px tall
   - Sit button spans full width at bottom

### Color Scheme
- **Background**: Dark purple (RGB 32, 16, 64)
- **Text**: White (RGB 255, 255, 255)
- **HP Bar**: Standard green gradient (standard EQ palette)
- **Mana Bar**: Blue gradient (standard EQ palette)
- **Button Text**: White on teal/blue backgrounds

---

## Element Inventory - Pet Gauge Components

### Gauge Elements (Top 28px)

| Element | ScreenID | Position | Size (px) | EQType | Text Color | Function |
|---------|----------|----------|-----------|--------|-----------|----------|
| Pet Name Label | PetWnd_Label | X=4, Y=2 | 70×12 | 69 | White (255,255,255) | Pet name display with dynamic text |
| HP Gauge | PetWnd_Gauge | X=4, Y=16 | 152×15 | 16 | N/A | Green HP bar visualization (EQType 16 current) |
| HP Value Text | PetWnd_HPValues | X=82, Y=16 | 45×12 | 69+70 | White | Current/Max HP numeric display (e.g., "100/200") |
| HP Percentage | PetWnd_HPPercent | X=130, Y=16 | 25×12 | 19 | White | HP percentage indicator (e.g., "50%") |
| Mana Gauge | PetWnd_ManaGauge | X=4, Y=32 | 152×2 | 17 | N/A | Thin blue mana indicator line |

### Command Button Row (Bottom, Y=41 onwards)

| Button | ScreenID | Position | Size (px) | Command | Function |
|--------|----------|----------|-----------|---------|----------|
| Attack Button | PetWnd_AttackButton | X=4, Y=41 | 27×18 | /pet attack | Order pet to attack target |
| Follow Button | PetWnd_FollowButton | X=32, Y=41 | 27×18 | /pet follow | Order pet to follow player |
| Guard Button | PetWnd_GuardButton | X=60, Y=41 | 27×18 | /pet guard me | Order pet to guard player |
| Taunt Button | PetWnd_TauntButton | X=88, Y=41 | 27×18 | /pet taunt on/off | Toggle pet taunt mode |
| Dismiss Button | PetWnd_DismissButton | X=116, Y=41 | 27×18 | /pet release | Dismiss or release pet |
| Focus Button | PetWnd_FocusButton | X=144, Y=41 | 13×18 | (reserved) | Future focus control |
| Sit Button | PetWnd_SitButton | X=4, Y=60 | 153×18 | /pet sit | Toggle pet sit/stand pose |

### Text Labels & Stat Display

| Element | Position | Size (px) | Font | EQType | Usage |
|---------|----------|-----------|------|--------|-------|
| HP Label | (dynamic) | 20×12 | Font 3 | 69 | "HP" prefix for HP Value display |
| Percent Label | (dynamic) | 15×12 | Font 3 | 19 | "%" suffix appended to percentage value |
| Attack Icon | X=5, Y=42 | 12×12 | Icon | N/A | A icon representing attack command |
| Follow Icon | X=33, Y=42 | 12×12 | Icon | N/A | F icon representing follow command |
| Guard Icon | X=61, Y=42 | 12×12 | Icon | N/A | G icon representing guard command |
| Taunt Icon | X=89, Y=42 | 12×12 | Icon | N/A | T icon representing taunt command |
| Release Icon | X=117, Y=42 | 12×12 | Icon | N/A | R icon representing release command |

---

## Technical Specifications - Tall Gauge Implementation

### EQType Coverage

| EQType | Purpose | Value | Used In |
|--------|---------|-------|---------|
| 16 | Pet HP (Current) | Dynamic | HPGauge fill, HP Value display |
| 17 | Pet Mana (Current) | Dynamic | ManaGauge fill indicator |
| 19 | HP Percentage | Calculated | Percentage display label |
| 69 | Pet Name / HP Label | Dynamic | Name text + "HP" prefix |
| 70 | HP Max Value | Static | HP Value denominator |

### Gauge Draw Templates

- **HPGauge**: Uses green fill (standard EverQuest palette)
  - Background: Recessed/inset appearance
  - Fill: Proportional to current HP (EQType 16 / EQType 70)
  - Height: 15px (tall variant, vs 24px in other variants)
  - Border: Dark gray/black outline

- **ManaGauge**: Minimal blue indicator
  - Height: 2px (thin line)
  - Visibility: Subtle indicator only
  - Position: Directly below HP gauge (Y=32)

### Window Properties & Rendering

| Property | Value | Notes |
|----------|-------|-------|
| DrawTemplate | WDT_NoTitle | No window title/decorations |
| ScreenPiece Opacity | 255 | Fully opaque elements |
| Location | User-configurable | Stored in defaults.ini |
| BGColor | RGB(32, 16, 64) | Dark purple background |
| BGType | 2 (rounded rectangle) | Styled frame borders |
| RelativePosition | true | Elements scale with window |
| TextFont | Font 3 | Consistent with Player/Target windows |

### Compatibility & Consistency

- **Metric Alignment**: Pet gauge X-positions match Player/Target/Group windows (X=4 left margin)
- **Text Styling**: White text (255,255,255) matches Player Name styling for UI consistency
- **Height**: 15px gauge height matches Player/Default pet gauge sizing
- **Button Standards**: 27×18 buttons match Action window quick-command buttons
- **EQType Parity**: HP/Mana types (16/17) synchronized with all character windows

---

## Buff/Debuff Icon Display (Reserve Space)

| Position | Size | Purpose | Status |
|----------|------|---------|--------|
| X=4, Y=80 (optional) | 12×12 × 8 | Buff icon slots | Not currently implemented |
| X=4, Y=100 (optional) | 12×12 × 8 | Debuff icon slots | Not currently implemented |

*Note*: Currently no dedicated buff display. Possible future expansion to match Player Window immunities/buffs display.

---

## Variant Comparison - Pet Window Layouts

| Feature | Tall Gauge (This) | Standard | Large Pet |
|---------|------------------|----------|-----------|
| **Window Height** | 125px | 125px | 160px+ |
| **HP Gauge Height** | 15px | 24px | 32px |
| **Mana Display** | 2px line | 2px line | 8px bar |
| **Button Count** | 7 (6 + sit) | 7 (6 + sit) | 10+ |
| **Command Layout** | 6-wide + sit | 6-wide + sit | 2-column |
| **Pet Name Visibility** | Good | Excellent | Excellent |
| **Screen Real Estate** | Compact | Balanced | Expansive |
| **Use Case** | Central placement | Side monitoring | Dedicated window |

---

## Color Scheme Reference

| Element | RGB Values | Usage |
|---------|-----------|-------|
| Background | (32, 16, 64) | Dark purple frame |
| Pet Name Text | (255, 255, 255) | White label for contrast |
| HP Gauge Fill | (0, 200, 0) | Standard green (EQ palette) |
| Mana Gauge Fill | (100, 150, 255) | Light blue indicator |
| HP Bar Border | (0, 0, 0) | Black outline definition |
| Button Background | (64, 64, 128) | Teal-purple button face |
| Button Text | (200, 200, 255) | Light blue button labels |
| Percentage Text | (200, 200, 200) | Light gray numeric display |

---

## Installation & Configuration

1. Copy `EQUI_PetInfoWindow.xml` from this directory to `thorne_drak/` (replacing existing file)
2. Run `/loadskin thorne_drak` in-game
3. Open Pet window with `/pet` or summon a pet
4. Window docks to configured location (stored in defaults.ini)

## Reverting to Standard Variant

- Copy `EQUI_PetInfoWindow.xml` from `Options/Pet/Standard/` directory
- Run `/loadskin thorne_drak` to reload

---

## Modification History

### v1.1.0 (Feb 3, 2026)
- Pet name color changed to white (255,255,255) for better contrast
- Text offset standardized to match Player Window (X=4, Y=0)
- Comparison table added vs Standard variant
- Documentation expanded with full element inventory

### v1.0.0 (Original)
- Initial Tall Gauge variant implementation
- 15px HP gauge height optimized for central UI placement
- 6 command buttons + sit toggle

---

## Comparison with Standard Variant

| Feature | Tall Gauge | Standard |
|---------|-----------|----------|
| **HP Gauge Height** | 15px | 24px |
| **Mana Indicator** | 2px line | 2px line |
| **Total Height** | 125px | 125px |
| **Best For** | Central UI placement | Dedicated monitoring |
| **Readability** | Good compromise | Maximum clarity |

The Tall Gauge variant sacrifices some HP gauge height compared to the Standard variant to provide better overall window proportions when placed in the center of your UI, while the Standard variant is better for dedicated placement on the side or for players who want a larger health indicator.

---

## Usage Recommendations

- **Solo Play**: Use Tall Gauge for compact, unobtrusive pet monitoring
- **Group Play**: Tall Gauge works well alongside group window display
- **Pet Classes**: Recommended for enchanters, necromancers, druids, and magicians

The taller HP gauge (15px vs 24px in Standard) provides a good balance between visibility and compact sizing, making it ideal for keeping your pet status visible without occupying too much screen real estate.

---

## Installation

### Quick Setup
```bash
# Copy to main UI directory
cp EQUI_PetInfoWindow.xml ../../
```

### Testing
1. Start EverQuest with your thorne_drak UI profile
2. Summon a pet
3. Verify taller HP gauge displays correctly
4. Check button layout and positioning

---

## See Also

- [Player Window - Pet Bottom](../../Player/Pet%20Bottom/README.md)
- [Group Window - Standard](../../Group/Standard/README.md)
- [Target Window - Player Gauges and Weight](../../Target/Player%20Gauges%20and%20Weight/README.md)
- [Pet Window - Standard](../Standard/README.md) - Shorter gauge variant
