# Configuration Defaults Reference

Centralized documentation for all `.regen_*.json` configuration defaults. This file explains what each setting means — refer to it from variant config files rather than repeating explanations.

---

## Slots Configuration

### `button_grid` (Regen Slots)

Controls button background positioning and spacing on the composite texture.

- **`origin_x`**: Left edge position of the button grid (pixels from left)
- **`origin_y`**: Top edge position of the button grid (pixels from top)
- **`sep_x`**: Horizontal spacing between buttons (pixels)
- **`sep_y`**: Vertical spacing between buttons (pixels)

**Example:** `origin_x: 0, origin_y: 0, sep_x: 2, sep_y: 2` places the grid at top-left with 2px gaps.

---

### `default_button` (Regen Slots)

Specifies which button texture from `button_atlas_thorne01.tga` to use as the default background.

- **`button_row`**: Row number in button atlas (1-based)
- **`button_col`**: Column number in button atlas (1-based)
- **`gradient`**: Optional gradient preset name to tint the button (e.g., `"gold"`, `"silver"`, `"none"`)

**Example:** `button_row: 1, button_col: 1, gradient: "gold"` uses first button with gold tint.

---

### `default_item` (Regen Slots)

Controls how item icons are rendered onto buttons.

- **`fit_mode`**: How the icon fills available space
  - `"scale"` — Scale to fit (preserves aspect ratio, may add empty space)
  - `"tile"` — Tile/repeat the icon (fills entire available space)
  - `"stretch"` — Stretch to fill (may distort if icon isn't square)
  
- **`fit_size`**: Pixel size of the rendered icon (affects final size on button; grid is 40×40, typical is 28-36)

- **`offset_x`**: Horizontal offset of icon from button top-left (pixels)
- **`offset_y`**: Vertical offset of icon from button top-left (pixels)

- **`item_opacity`**: Alpha blending of the icon (0.0-1.0; 1.0 = fully opaque, 0.5 = 50% transparent)

**Example:** `fit_mode: "tile", fit_size: 28, offset_x: 1, offset_y: 1, item_opacity: 0.92` tiles a 28px icon with slight transparency.

---

### `item_overrides` (Regen Slots)

Per-item customizations that override defaults for specific items.

Each key is an item name (e.g., `"ear"`, `"logo_1"`), and the value is an object containing any of:
- `"gradient"`: Override gradient for this item
- `"button_row"` / `"button_col"`: Override button source
- `"fit_mode"`, `"fit_size"`, `"offset_x"`, `"offset_y"`, `"item_opacity"`: Override rendering

All unspecified properties fall back to `default_item` or `default_button`.

**Example:**
```json
"item_overrides": {
  "logo_1": { "gradient": "none" },
  "primary": { "fit_size": 32, "item_opacity": 0.95 }
}
```

---

## Thorne Atlas Configuration

### `default_tone` (Regen Thorne)

Tone controls adjust the appearance of rendered item icons in the atlas.

- **`contrast`**: Controls vividity of colors
  - `1.0` = Unchanged
  - `> 1.0` = More vivid/rich (bright colors brighter, dark colors darker; example: 1.10)
  - `< 1.0` = Flatter (less contrast; example: 0.90)
  
  **Combined with brightness** (e.g., `contrast: 1.10 + brightness: 0.95`) creates a richer appearance at slightly darker tones.

- **`brightness`**: Adjusts overall lightness
  - `1.0` = Unchanged
  - `> 1.0` = Lighter/brighter (example: 1.05)
  - `< 1.0` = Darker/dimmer (example: 0.95)

**Typical values:** `contrast: 1.10, brightness: 0.95` for richer, slightly darker icons.

---

### `output_file` (Regen Thorne)

Target filename for generated atlas. Stored in variant's `.Master/` directory.

- **Master atlases:**
  - `"item_atlas_thorne01.tga"` — 40px item icons (primary)
  - `"item_icons_thorne01.tga"` — 20px variant (compact)
  
- **Configured via `variants` array** — Each variant can output to a different file.

---

## Gradient Presets (Shared)

Preset color gradients defined in `.bin/regen_slots.json` and auto-merged into all variants. Add `"gradient_presets"` block in a variant config to introduce new presets or override base ones.

### Common Presets

| Name | Type | Description |
|------|------|-------------|
| `gold` | vertical | Warm classic gold (top to bottom) |
| `silver` | vertical | Cool silver gradient |
| `bronze` | vertical | Warm bronze/copper |
| `logo` | vertical | Subtle tinted gold |
| `none` | (special) | No tint — item as-is |
| `patriot` | vertical | Red-white-blue 3-stop gradient |
| `shadow` | vertical | Dark desaturated fade |
| `gold_h` | horizontal | Gold left to right |
| `dawn` | diagonal | Warm sunrise diagonal |

**Reference in config:**
```json
"default_button": { "gradient": "gold" },
"item_overrides": { "special_slot": { "gradient": "custom" } }
```

**Define new preset in variant:**
```json
"gradient_presets": {
  "custom": {
    "type": "vertical",
    "top_color": [255, 100, 100],
    "bottom_color": [100, 50, 50]
  }
}
```

---

## Types of Config Files

### Master Configs (`.bin/`)

- **`regen_slots.json`** — Item layout & button grid, shared gradient presets
- **`regen_icons.json`** — Stat icon coordinate mappings
- **`.Master/.regen_thorne.json`** — Item atlas configuration (items 1-36, tone controls)

### Variant Configs (`Options/<Category>/<Variant>/`)

- **`.regen_slots.json`** — Per-variant button styling, gradients, overrides
- **`.regen_gauges-stats.json`** (generated) — Output metadata
- **`.regen_gems-stats.json`** (generated) — Output metadata
- **`.regen_icons-stats.json`** (generated) — Output metadata
- **`.regen_thorne-stats.json`** (generated) — Output metadata

Variant configs merge with their corresponding master configs at runtime.

---

## See Also

- `.bin/regen_slots.md` — Slots script documentation
- `.bin/regen_gauges.md` — Gauges script documentation
- `.bin/regen_gems.md` — Gems script documentation
- `.bin/regen_icons.md` — Icons script documentation
- `.docs/STANDARDS.md` — UI development standards
