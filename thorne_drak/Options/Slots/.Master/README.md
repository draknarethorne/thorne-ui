# .Master Directory - Thorne UI Slot System Control Center

This directory contains the authoritative source of truth for the Thorne UI slot generation system.

## Directory Structure

```
.Master/
├── .regen_slots.json          Master config: slot layout, button styles, all gradient presets
├── .Items/                    Source dragitem textures (36 files)
├── .Themes/                   Theme-specific gradient overrides
│   ├── Thorne/               Default personal theme
│   ├── Gold/                 Gold variant
│   ├── Silver/               Silver variant
│   ├── Patriot/              Red/white/blue variant
│   ├── Metal/                Multi-metal variant
│   ├── Transparent/          Transparent background variant
│   └── Texture/              Textured background variant
└── .Classes/                  Class-specific item overrides
    ├── Thorne/               Personal class (mostly mirrors master)
    ├── Caster/               Caster armor/weapon selections
    ├── Melee/                Melee armor/weapon selections
    └── Hybrid/               Hybrid armor/weapon selections
```

## How It Works

### Two-Step Generation

**STEP 1 - `regen_thorne.py`**: Generates class-specific item atlases
- Input: `.Items/dragitem*.tga` (source items)
- Process: Apply class-specific item selections from `.Classes/<Class>/.regen_thorne.json`
- Output: `.Classes/<Class>/item_atlas.tga` (class-specific atlas)

**STEP 2 - `regen_slots.py`**: Composites atlases with buttons and theme gradients
- Input: `.Classes/<Class>/item_atlas.tga` + `.Themes/<Theme>/.regen_slots.json`
- Process: Apply theme gradients, composite with buttons from master config
- Output: `Options/Slots/<Class>/<Theme>/item_slots_thorne01.tga`

### Configuration Inheritance Model

- **Master Config** (`.regen_slots.json`): Complete slot layout + all gradient presets
- **Class Overrides** (`.Classes/<Class>/.regen_thorne.json`): Only dragitems that differ from master
- **Theme Overrides** (`.Themes/<Theme>/.regen_slots.json`): Only gradients that differ from master

## Key Files

### `.regen_slots.json` (Master)

Contains:
- `items` array: 36-item slot mapping (ear, neck, head, ... logo_6)
- `gradient_presets`: All color gradients (gold, silver, bronze, platinum, gleams, etc.)
- `source_items` & `source_buttons`: Atlas source file references

**Do NOT add theme-specific values here.** Theme-specific overrides go in `.Themes/`.

### `.Classes/<Class>/.regen_thorne.json`

Example structure:
```json
{
  "class_name": "Caster",
  "item_overrides": [
    {
      "item_name": "chest",
      "dragitem_index": 42,
      "brightness": 1.1,
      "contrast": 1.05
    }
  ]
}
```

**Only add items that differ from the master.**
- Master items: All armor from a general dragitem file
- Caster overrides: Caster-specific robes, spell focus items

### `.Themes/<Theme>/.regen_slots.json`

Example structure:
```json
{
  "_comment": "Gold theme overrides",
  "gradient_presets": {
    "custom_gold": {
      "type": "vertical",
      "top_color": [150, 120, 60],
      "middle_color": [230, 210, 130],
      "bottom_color": [180, 150, 80]
    }
  }
}
```

**Only override gradients that should differ from master.**
- Empty file: Theme uses all master gradients as-is

## Workflow Examples

### Generate All Classes + All Themes

```bash
regen_thorne.bat --all-classes
# Generates all class/theme combos
# Copies Thorne/Thorne to thorne_drak/item_slots_thorne01.tga (your personal preference)
```

### Generate Specific Class

```bash
regen_thorne.bat --class Caster
# Generates Caster atlas + all Caster/theme combos
# Copies Caster/Thorne to thorne_drak/ (Caster with default theme active)
```

### Generate Specific Theme

```bash
regen_slots.bat --theme Gold
# Generates all class/Gold combos
# Does NOT copy-back (exploring variants)
```

### Test Specific Class + Theme

```bash
regen_slots.py --class Caster --theme Gold --verbose
# Generates Caster/Gold only
# Does NOT copy-back (testing mode)
```

## Next Steps: Adding Class-Specific Items

When ready to customize per-class armor/weapons:

1. Identify which dragitem files contain the items you want for each class
2. In `.Classes/<Class>/.regen_thorne.json`, add `item_overrides` entries
3. Specify dragitem index, and optionally apply brightness/contrast
4. Run `regen_thorne.bat --class <Class>` to generate and test
5. Use `--verbose` flag to see which items are being selected

**Future Themes (Experimental)**
- Fire: Warm orange/red color palette
- Blood: Deep red/crimson variants
- Nature: Green/earth tones
- These can be added as new `.Themes/<Name>/` directories when ready

## Notes for Future Architecture

The theme gradient system is designed to be potentially extracted into a global color library for use across more than just slot definitions. This would allow:
- Consistent color theming across entire UI
- Reusable gradient presets in other UI elements
- Centralized theme management

For now, themes are slot-specific, but the groundwork exists for broader adoption.
