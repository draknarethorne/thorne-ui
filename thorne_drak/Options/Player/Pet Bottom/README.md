# Player Window - Pet Bottom Variant

**File**: [EQUI_PlayerWindow.xml](./EQUI_PlayerWindow.xml)
**Version**: 1.1.0  
**Last Updated**: 2026-02-17
**Status**: ✅ Enhanced with improved pet gauge styling  
**Author**: Draknare Thorne

---
## Purpose

The "Pet Bottom" Player Window variant displays comprehensive character stats with the pet HP gauge positioned at the bottom of the window. This layout prioritizes player statistics while maintaining persistent pet health awareness during active play.

**Key Features**:

- **Full Player Stats**: HP, Mana, Stamina, Experience, AA Points with gauges and percentages
- **Pet HP Gauge**: Tall 15px gauge at bottom with white pet name text
- **Consistent Positioning**: Pet stats aligned with Pet Window and Group Window layouts
- **Status Indicators**: Breath meter, spell casting progress, threat level
- **Level & Class Display**: Character name, level, and class information
- **Buff Window Integration**: Shows active buffs in separate panel area
- **Clean Layout**: Organized vertical layout with clear visual hierarchy

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 224 × 560 pixels (approximate) |
| Resizable | Yes |
| Fadeable | Yes |
| Screen ID | CharacterWindow |
| DrawTemplate | WDT_RoundedNoTitle |
| Titlebar | No |
| Closebox | Yes |
| Minimizebox | Yes |
| Pet Gauge Position | Bottom section (Y≈111) |
| Pet Gauge Height | 15 pixels (tall variant) |

---

## Key Modifications (v1.1.0 - Feb 3, 2026)

### Visual Improvements
- **Pet Name Color**: Changed from green (0,240,0) to white (255,255,255)
- **Text Offset Standardization**: Synchronized with Pet Window (TextOffsetY: 1→0)
- **Consistency**: Pet gauge styling now matches Player/Target/Group layouts

### Position Alignment
- Pet HP numeric values positioned at X=82 (consistent with Group Window)
- Pet HP percentage positioned at X=142 (standard across all windows)
- Allows seamless visual flow when referencing pet health across different UI panels

---

## Pet Gauge Details

### Position & Sizing

| Element | Position | Size | Type | EQType |
|---------|----------|------|------|--------|
| Pet Label | (2, 111) | 120×15 | Gauge | 16 |
| Pet HP Numeric | (168, 111) | 27×12 | Value | N/A |
| Pet HP Percent | (196, 111) | - | Value | N/A |
| Pet HP % Sign | (218, 111) | 8×12 | Text | N/A |

### Gauge Specifications

- **Height**: 15 pixels (tall variant for readability)
- **Width**: 120 pixels
- **Background**: A_GaugeBackground_Tall template
- **Fill Color**: Purple (RGB 200,80,200)
- **Text Color**: White (RGB 255,255,255) - high contrast
- **Border**: Black outline
- **Text Offset**: X=4, Y=0 (matches Pet Window and Target Window)

---

## Color Scheme

| Element | RGB Values | Usage |
|---------|-----------|-------|
| HP Bar | (255, 0, 0) | Red health bar |
| Mana Bar | (100, 150, 255) | Thorne blue |
| Stamina Bar | (200, 100, 0) | Orange |
| XP Bar | (0, 100, 200) | Blue |
| AA Bar | (200, 200, 0) | Gold |
| Pet HP Bar | (200, 80, 200) | Purple |
| Pet Name Text | (255, 255, 255) | White (HIGH CONTRAST) |
| Text Labels | (240, 240, 240) | Light gray |
| Bar Borders | (0, 0, 0) | Black |

---

## Element Inventory - Pet Status Section

### Pet Gauge Elements

| Element | ScreenID | EQType | Position | Size | Color | Function |
|---------|----------|--------|----------|------|-------|----------|
| Pet Name Gauge | PW_Gauge_PetHP | 16 | (2, 111) | 120×15 | Purple (200, 80, 200) | Pet HP visualization |
| Pet HP Value | PW_Pet_HPValues | N/A | (82, 111) | 27×12 | White | Current/Max HP display |
| Pet HP Percent | PW_Pet_HPPct | N/A | (142, 111) | 30×12 | White | HP percentage indicator |
| Pet Name Text | PW_PetName | N/A | (4, 111) | 70×12 | White | Pet name display (overlaid) |

### Spacing & Alignment

| Measurement | Value | Notes |
|-------------|-------|-------|
| Pet Gauge Y-Position | 111px | Positions pet stats at bottom |
| Pet Label Offset | X=4, Y=0 | Matches Target/Group window standards |
| Pet HP Value X-Position | 82px | Aligns with Player/Target/Group windows |
| Pet Percentage X-Position | 142px | Standard percentage column across UI |
| Gauge Height | 15px | Tall variant for visibility |

---

## Variant Comparison - Player Window Layouts

| Feature | Default | Standard | Pet Bottom | AA & XP Bottom |
|---------|---------|----------|-----------|-----------------|
| **Primary Gauges** | HP/Mana/Stamina/XP | HP/Mana/Stamina/XP | HP/Mana/Stamina/XP/AA | HP/Mana/Stamina/AA+XP |
| **Pet Gauge** | Small separate | None | Bottom focus (15px tall) | None |
| **Pet Priority** | Low | None | ✅ High | None |
| **Layout Version** | Balanced | Standard | Pet-focused | AA-focused |
| **Typical Height** | 70px | 120px | 560px (with buffbox) | Similar |
| **Primary Use** | General | All-purpose | Pet classes | AA builders |
| **Window Height Adjustment** | Fixed | Fixed | Resizable | Resizable |

---

## Technical Implementation

### Pet Gauge Integration

- **EQType 16**: Drives pet HP gauge fill based on current pet health
- **Dynamic Updates**: Gauge refreshes instantly as pet takes/heals damage
- **Name Rendering**: Pet name displays white text overlaid on gauge
- **Off-Focus Opacity**: Gauges dim when window loses focus (optional styling)
- **Relative Positioning**: Pet gauge uses relative positioning for window scaling

### Cross-Window Consistency

This variant achieves UI cohesion by maintaining:
- **Identical metric positioning** across Player, Target, Group, and Pet windows
- **Standard gauge heights** (15px for primary, 8px for secondary)
- **Consistent text colors** (white for readability against purple gauge)
- **Aligned value columns** (HP values at X=82, percentages at X=142)

---

## Alignment with Other Windows

This variant maintains consistent positioning with:

- **Pet Window (Tall Gauge)**: Identical pet gauge height (15px) and text offset
- **Target Window**: Pet gauge styling (white text, purple fill)
- **Group Window (Standard)**: HP/percentage label positions (X=82, X=142)

**Pet Stats Consistency**:
```
Layout across all windows:
[Pet Name Gauge (120px wide, 15px tall)]
[HP Value (82,Y)]  [HP % (142,Y)]
```

---

## Configuration

To use this variant, place this folder's files in your EverQuest UI directory:

```bash
EverQuest/
├── UIFILES/
│   └── thorne_drak/
│       ├── Options/
│       │   └── Player/
│       │       └── Pet Bottom/
│       │           ├── EQUI_PlayerWindow.xml
│       │           └── README.md
```

Then load with:
```
/loadskin thorne_drak
```

---

## Testing Recommendations

1. Load UI: `/loadskin thorne_drak`
2. Summon a pet and verify:
   - Pet name displays in white on purple gauge
   - HP value shows correctly aligned
   - Percentage displays properly
3. Check visual consistency across:
   - Pet Window (Tall Gauge variant)
   - Target Window (if targeting pet owner)
   - Group Window (if grouped with pet user)
4. Verify no text overlap or positioning issues

---

## Modification History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | Feb 3, 2026 | White pet name text, standardized text offset |
| 1.0.0 | Feb 1, 2026 | Initial Pet Bottom variant |

---

## See Also

- [Pet Window - Tall Gauge](../../Pet/Tall%20Gauge/README.md)
- [Group Window - Standard](../../Group/Standard/README.md)
- [Player Window - AA and XP Bottom](../AA%20and%20XP%20Bottom/README.md)
- [Target Window - Player Gauges and Weight](../../Target/Player%20Gauges%20and%20Weight/README.md)
