# Themes Guide (Slots)

This guide explains how to create and tune slot themes for the Thorne UI slot pipeline.

## What a Theme Is

A **theme** is a collection of gradient presets and style overrides used by `regen_slots.py` to tint item icons and choose button styles.
Themes live in:

```
Options/Slots/.Master/.Themes/<Theme>/
```

Each theme provides a `.regen_slots.json` that **overrides** master defaults from:

```
Options/Slots/.Master/.regen_slots.json
```

## Quick Start: Add a New Theme

1. **Create a theme folder** (example: `Ashen`):

```
Options/Slots/.Master/.Themes/Ashen/
```

2. **Create `.regen_slots.json`** in that folder.

3. **Define theme overrides** (you can start minimal):

```json
{
  "_comment": "Ashen theme overrides",
  "default_button": {
    "button_row": 1,
    "button_col": 1,
    "gradient": "ashen"
  },
  "gradient_presets": {
    "ashen": {
      "type": "diagonal_tl",
      "top_color": [40, 45, 50],
      "middle_color": [170, 175, 185],
      "bottom_color": [110, 120, 130]
    }
  }
}
```

4. **Regenerate theme output**:

- For all classes:
  - `regen_slots.bat --theme Ashen`
- For a specific class:
  - `regen_slots.py --class Thorne --theme Ashen`

> Outputs are written to `Options/Slots/<Class>/<Theme>/item_slots_thorne01.tga`.

## Gradient Presets

Gradients are defined in `gradient_presets`. Items reference a preset by name via `gradient`.

Supported `type` values:
- `vertical`
- `horizontal`
- `diagonal_tl` (top-left → bottom-right)
- `diagonal_tr` (top-right → bottom-left)
- `none` (no tint)
- `direct` (same as none)

3-stop gradients are supported by providing `middle_color`.

### Example: 3-stop Necro/Silver Gradient

```json
"gradient_presets": {
  "thorne": {
    "type": "diagonal_tl",
    "top_color": [45, 48, 52],
    "middle_color": [160, 170, 180],
    "bottom_color": [110, 120, 130]
  }
}
```

## Item Overrides

Use `item_overrides` to apply special gradients to specific slots (logos, weapons, etc.):

```json
"item_overrides": {
  "logo_1": { "gradient": "none" },
  "logo_2": { "gradient": "thorne_logo" }
}
```

## Common Theme Patterns

- **Gold/Silver/Bronze**: Use vertical gradients with 3 stops (dark → light → mid).
- **Patriot**: Use `patriot` for most armor, `patriot_weapon` for weapons, mixed accents for logos.
- **Transparent**: Set `default_button.gradient` to `none`, reduce `item_opacity`.

## Troubleshooting

- **Everything is gold** → Theme override file is empty or `default_button.gradient` not set.
- **No visible change** → Regenerate outputs using `regen_slots.py` or `regen_slots.bat`.
- **Wrong direction** → Use `diagonal_tl` or `diagonal_tr` in preset.

## Reference

- Master presets: `Options/Slots/.Master/.regen_slots.json`
- Theme examples: `Options/Slots/.Master/.Themes/Gold/`, `Silver/`, `Bronze/`, `Patriot/`, `Thorne/`
