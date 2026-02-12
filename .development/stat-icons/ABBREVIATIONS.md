# Stat Icon Abbreviations Reference

**Document Version:** 1.0  
**Last Updated:** 2026-02-15  
**Purpose:** Define standardized abbreviations for all stat icons used in Thorne UI

---

## Overview

This guide defines the abbreviated names for stat icons, designed for UI implementations where space is limited. Each abbreviation is optimized for readability while maintaining clarity about the represented stat.

### Three-Level Abbreviation Hierarchy

1. **Full Names**: Complete icon identifier (e.g., "MANA", "Weight")
2. **Short Abbreviations**: 1-3 character codes for compact display (e.g., "MP", "WT")
3. **Visual Icons**: Icon graphics themselves (no text needed)

---

## Player Stats (Column 1)

These represent core character mechanics.

| Full Name | Abbreviation | Length | Display Example | Purpose |
|-----------|--------------|--------|-----------------|---------|
| AC | AC | 2 | AC 25 | Armor Class rating |
| ATK | ATK | 3 | ATK 245 | Attack power/damage |
| HP | HP | 2 | HP 575 | Hit Points (health) |
| MANA | MP | 2 | MP 350 | Mana resource pool |
| STA | ST | 2 | ST 100 | Stamina/endurance |
| Weight | WT | 2 | WT 40.5 | Carried weight |

**Usage Notes:**
- AC, ATK, HP: Universal gaming abbreviations, need no explanation
- MANA → MP: Industry standard abbreviation for Mana Points
- STA → ST: Matches expected stat abbreviation pattern
- Weight → WT: Compact representation following standard conventions

---

## Resistances (Column 2)

These represent defensive capabilities against specific damage types.

| Full Name | Abbreviation | Length | Display Example | Purpose |
|-----------|--------------|--------|-----------------|---------|
| Fire | FR | 2 | FR 45 | Fire damage resistance |
| Cold | CR | 2 | CR 40 | Cold damage resistance |
| Magic | MR | 2 | MR 35 | Magic damage resistance |
| Poison | PR | 2 | PR 30 | Poison damage resistance |
| Disease | DR | 2 | DR 25 | Disease damage resistance |
| Reserve | RV | 2 | RV — | Reserved/future use |

**Usage Notes:**
- All resistances use 2-character format for visual consistency
- Reserve (RV) is a placeholder for future resistance types
- Abbreviations follow pattern: First letter of damage type + R for Resistance

**Mnemonic Pattern:**
- **FR** = Fire Resistance
- **CR** = Cold Resistance
- **MR** = Magic Resistance
- **PR** = Poison Resistance
- **DR** = Disease Resistance

---

## Attribute Stats (Column 3)

These represent character abilities and personality traits.

| Full Name | Abbreviation | Length | Display Example | Purpose |
|-----------|--------------|--------|-----------------|---------|
| STR | STR | 3 | STR 18 | Strength (melee power) |
| INT | INT | 3 | INT 14 | Intelligence (mental acuity) |
| WIS | WIS | 3 | WIS 15 | Wisdom (awareness) |
| AGI | AGI | 3 | AGI 16 | Agility (reflexes) |
| DEX | DEX | 3 | DEX 17 | Dexterity (hand-eye coord) |
| CHA | CHA | 3 | CHA 12 | Charisma (force of will) |

**Usage Notes:**
- Three-character abbreviations matching standard stat abbreviations
- Clear and unambiguous (no confusion with other systems)
- Consistent with gaming industry standards (STR, INT, WIS, etc.)
- Players instantly recognize these abbreviations from countless RPGs

---

## Implementation Guidelines

### When to Use Each Abbreviation Type

**Full Names (AC, ATK, HP, etc.):**
- Primary stat displays with plenty of space
- Tooltip text and descriptions
- Documentation and help files
- Default UI variant for clarity

**Short Abbreviations (AC, ATK, HP, MP, ST, WT, FR, CR, MR, PR, DR, RV, STR, INT, WIS, AGI, DEX, CHA):**
- Primary and recommended compact display option
- Works in all UI layouts
- Equipment windows and character sheets
- Inventory displays and status bars
- Hotbar badges and tooltips
- Industry standard - players instantly recognize them

**Icons Only (No Text):**
- Icon-only compact layouts
- Visual stat displays (stat block icons)
- UI frames where icon is self-explanatory
- Hover tooltip provides full name

### Display Format Recommendations

```
Format: [Icon] Abbreviation Value
Example: [STR Icon] S 18/00

Format with full name: [Icon] Full Name Value
Example: [STR Icon] Strength 18/00

Format compact: [Icon] Value
Example: [STR Icon] 18/00
```

---

## Abbreviation Rationale

### Stats (Column 1)
- **AC, ATK, HP**: Universal understanding, no change needed
- **MP**: Industry standard abbreviation for "Mana Points" across all games
- **ST**: Standard abbreviation for stamina in gaming contexts
- **WT**: Weight is non-stat and needs distinction, WT is standard abbreviation

### Resistances (Column 2)
- **Pattern**: First letter of damage type + R
- **Consistency**: All same length (2 chars) for alignment
- **Clarity**: FR/CR/MR/PR/DR are immediately recognizable

### Attributes (Column 3)
- **Pattern**: Single first letter of attribute name
- **Simplicity**: Minimal representation for compact spaces
- **Tradition**: Follow D&D/RPG conventions (S=Strength, etc.)
- **Memorability**: Players familiar with these abbreviations from countless RPGs

---

## Code/Script References

### Coordinates File Integration

The `stat-icons-coordinates.json` file includes abbreviation metadata:

```json
{
  "abbreviations": {
    "stats": {
      "AC": "Armor Class",
      "ATK": "Attack Power",
      "HP": "Hit Points",
      "MP": "Mana Points (MANA)",
      "ST": "Stamina (STA)",
      "WT": "Weight"
    },
    "resistances": {
      "FR": "Fire Resistance",
      "CR": "Cold Resistance",
      "MR": "Magic Resistance",
      "PR": "Poison Resistance",
      "DR": "Disease Resistance",
      "RV": "Reserved"
    },
    "attributes": {
      "S": "Strength (STR)",
      "I": "Intelligence (INT)",
      "W": "Wisdom (WIS)",
      "A": "Agility (AGI)",
      "D": "Dexterity (DEX)",
      "C": "Charisma (CHA)"
    }
  },
  "layout": {
    "MANA": {
      "abbr": "MP",
      "description": "Mana Points",
      ...
    },
    ...
  }
}
```

### Using Abbreviations in XML

```xml
<!-- Full name display -->
<Label item="STR_Label">Strength</Label>
<Label item="STR_Abbr">STR</Label>

<!-- Short abbreviation (from coordinates metadata) -->
<Label item="MANA_Abbr">MP</Label>

<!-- Single letter abbreviation (from coordinates metadata) -->
<Label item="STR_Short">S</Label>

<!-- With icon -->
<StaticAnimation item="STR_Icon">
  <Animation>ICON_STR</Animation>
</StaticAnimation>
<Label item="STR_Value">18/00</Label>
```

### Python Script Integration

Scripts can access abbreviation data from the coordinates JSON:

```python
import json

with open('.development/stat-icons-coordinates.json') as f:
    coords = json.load(f)

# Access abbreviations
abbr_stats = coords['abbreviations']['stats']
abbr_resist = coords['abbreviations']['resistances']
abbr_attribs = coords['abbreviations']['attributes']

# Example: Get mana abbreviation
mana_abbr = coords['layout']['MANA']['abbr']  # Returns "MP"
```

---

## Style Guidelines

### Visual Consistency

1. **Abbreviation Capitalization**
   - Stats/Resistances: ALL CAPS (AC, MP, FR)
   - Attributes: Capital letter (S, I, W, A, D, C)
   - Reason: Distinction between category types

2. **Font Selection**
   - Use monospace fonts for stat displays
   - Ensures proper alignment with varying abbreviation lengths
   - Improves readability when mixed with numeric values

3. **Spacing**
   - Abbreviations: Always followed by space before value
   - Example: `MP 350` (not `MP350`)
   - Improves scannability and readability

4. **Alignment**
   - Left-align abbreviations + icons
   - Right-align numeric values with decimal consideration
   - Improves scanning and visual parsing

### Tooltip Text

Always include full name in tooltips:

```
Tooltip for "MP": "Mana Points - Your magical energy resource"
Tooltip for "S": "Strength - Increases melee damage and carrying capacity"
Tooltip for "FR": "Fire Resistance - Reduces fire-based damage taken"
```

---

## Future Considerations

### Extensibility

The abbreviation system is designed to support future additions:

- **New Resistances**: Follow FR/CR/MR/PR/DR pattern
- **New Attributes**: Use first letter pattern (if available)
- **New Stats**: Use 2-letter pattern consistent with existing

### Alternative Abbreviations

If conflicts arise, alternatives are available:

| Original | Alternative | Context |
|----------|-------------|---------|
| MP | MA, MN | If "MP" conflicts arise |
| ST | SM | If "ST" conflicts arise |
| WT | WG | If "WT" causes issues |

---

## Summary

| Category | Icons | Pattern | Length | Example |
|----------|-------|---------|--------|---------|
| **Stats** | 6 | Mixed | 2-3 chars | AC, MP, WT |
| **Resistances** | 6 | X**R** | 2 chars | FR, CR, MR |
| **Attributes** | 6 | Three chars | 3 chars | STR, INT, WIS |

This three-tier abbreviation system provides flexibility for any UI layout while maintaining consistency and clarity across the entire Thorne UI icon system.
