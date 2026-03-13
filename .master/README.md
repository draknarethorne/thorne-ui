# .master/ — Thorne UI Slot System Control Center

This directory contains the authoritative source of truth for the Thorne UI slot generation system.

## Directory Structure

```
.master/
├── .regen_slots.json          Master config: slot layout, button styles, all gradient presets
├── items/                     Source dragitem textures (36 files)
├── themes/                    Theme-specific gradient overrides
│   ├── Thorne/               Default personal theme
│   ├── Gold/                 Gold variant
│   ├── Silver/               Silver variant
│   ├── Patriot/              Red/white/blue variant
│   ├── Bronze/               Bronze variant
│   ├── Transparent/          Transparent background variant
│   └── Texture/              Textured background variant
└── classes/                   Class-specific item overrides
    ├── Thorne/               Personal class (mostly mirrors master)
    ├── Caster/               Caster armor/weapon selections
    ├── Melee/                Melee armor/weapon selections
    └── Hybrid/               Hybrid armor/weapon selections
```

## Workflow at a Glance

### Two-Step Generation

**STEP 1 - `regen_thorne.py`**: Generates class-specific item atlases
- Input: `items/dragitem*.tga` (source items)
- Process: Apply class-specific item selections from `classes/<Class>/.regen_thorne.json`
- Output: `classes/<Class>/item_atlas_thorne01.tga` (+ icon variant)

**STEP 2 - `regen_slots.py`**: Composites atlases with buttons and theme gradients
- Input: `classes/<Class>/item_atlas_thorne01.tga` + `themes/<Theme>/.regen_slots.json`
- Process: Apply theme gradients, composite with buttons from master config
- Output: `Options/Slots/<Class>/<Theme>/item_slots_thorne01.tga`

### Configuration Inheritance Model

- **Master Config** (`.regen_slots.json`): Complete slot layout + all gradient presets
- **Class Overrides** (`classes/<Class>/.regen_thorne.json`): Only dragitems that differ from master
- **Theme Overrides** (`themes/<Theme>/.regen_slots.json`): Only gradients that differ from master

## Key Files

### `.regen_slots.json` (Master)

Contains:
- `items` array: 36-item slot mapping (ear, neck, head, ... logo_6)
- `gradient_presets`: All color gradients (gold, silver, bronze, platinum, gleams, etc.)
- `source_items` & `source_buttons`: Atlas source file references

**Do NOT add theme-specific values here.** Theme-specific overrides go in `themes/`.

### `classes/<Class>/.regen_thorne.json`

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

### `themes/<Theme>/.regen_slots.json`

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

## Running the Scripts

### Recommended (Batch Wrappers)

```bash
.bin/regen_thorne.bat --all-classes
```

- Generates **all class atlases**
- Regenerates **all class/theme slot outputs**

```bash
.bin/regen_thorne.bat --class Caster
```

- Generates **Caster** atlas
- Regenerates **Caster + all themes**

```bash
.bin/regen_slots.bat --theme Gold
```

- Regenerates **all classes** with the **Gold** theme only

### Direct Python (Manual Two-Step)

```bash
python .bin/regen_thorne.py --class Caster
python .bin/regen_slots.py --class Caster
```

> Direct `.py` usage does **not** auto-run Step 2. Use the batch scripts if you want the convenience step.

## Workflow Examples

### Generate All Classes + All Themes

```bash
.bin/regen_thorne.bat --all-classes
# Generates all class/theme combos
```

### Generate Specific Class

```bash
.bin/regen_thorne.bat --class Caster
# Generates Caster atlas + all Caster/theme combos
```

### Generate Specific Theme

```bash
.bin/regen_slots.bat --theme Gold
# Generates all class/Gold combos
```

### Test Specific Class + Theme

```bash
regen_slots.py --class Caster --theme Gold
# Generates Caster/Gold only
```

## Adding Classes & Themes (Detailed Guides)

- **Classes** → `README-CLASSES.md`
  - How to pick dragitems
  - How to set `src_row`, `src_col`, `source_file`
  - How to tune contrast/brightness per slot

- **Themes** → `README-THEMES.md`
  - How to define gradients
  - Which gradient types are supported
  - How to override logos and weapons

## Future Themes (Experimental)

- Fire: Warm orange/red color palette
- Blood: Deep red/crimson variants
- Nature: Green/earth tones
- These can be added as new `themes/<Name>/` directories when ready

## Notes for Future Architecture

The theme gradient system is designed to be potentially extracted into a global color library for use across more than just slot definitions. This would allow:
- Consistent color theming across entire UI
- Reusable gradient presets in other UI elements
- Centralized theme management

For now, themes are slot-specific, but the groundwork exists for broader adoption.
