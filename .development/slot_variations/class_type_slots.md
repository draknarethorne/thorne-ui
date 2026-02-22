# Class-Type Slot Variations (Caster / Melee / Hybrid)

Author: Draknare Thorne

## Goals

- Provide class-type-specific slot artwork (e.g., Caster/Melee/Hybrid) while preserving metal gradient options.
- Keep gradient testing flexible (vertical and diagonal variants).
- Avoid breaking existing workflows and UI options.
- Prepare for additional slot consumers (Inventory, Loot, Merchant, Bank, etc.).

## Current Layout (Baseline)

- **Master layout:** `.bin/regen_slots.json` (slot map + base gradients).
- **Atlas generation:** `regen_thorne.bat` → `.bin/regen_thorne.py` → `.Master` atlases.
- **Variants:** `thorne_drak/Options/Slots/<Variant>/.regen_slots.json` (gradient overrides).

## Option A — Multiple Master Atlases by Class Type (Recommended)

### A Structure

```
thorne_drak/Options/Slots/
  .Master/
    .regen_thorne.json
  .Master_Caster/
    .regen_thorne.json
  .Master_Melee/
    .regen_thorne.json
  .Master_Hybrid/
    .regen_thorne.json
```

### A Workflow

- Use a flag to choose master atlas source:
  - `regen_thorne.bat .Master_Caster`
  - `regen_thorne.bat .Master_Melee`
  - `regen_thorne.bat .Master_Hybrid`

### A Impact

- **Minimal change** to scripts (already support argument input).
- `regen_slots.bat --all` still works, as it references `item_atlas_thorne01.tga` from the chosen master.
- Each master can share the **same** gradient presets, allowing metal variants to be compared cleanly.

### A Pros

- Clear separation of class-type art.
- Preserves existing Options/Slots variants.
- Allows quick comparison via atlas swap.

### A Cons

- Multiple atlas files to maintain.
- Requires consistent item layout across master files.

## Option A2 — Layered Overrides (No Duplicated .json per Class)

This extends Option A with **shared theme configs** and **class-specific output folders**.
You get class-specific atlases and class-specific outputs **without** duplicating
Gold/Silver/etc. config files in every class folder.

### A2 Structure (recommended)

```
thorne_drak/Options/Slots/
  .Master/
  .Master_Caster/
  .Master_Melee/
  .Master_Hybrid/

  Themes/
    Gold/.regen_slots.json
    Silver/.regen_slots.json
    Bronze/.regen_slots.json
    Platinum/.regen_slots.json
    Thorne/.regen_slots.json

  Output/
    Caster/Gold/item_slots_thorne01.tga
    Caster/Silver/item_slots_thorne01.tga
    Melee/Gold/item_slots_thorne01.tga
    Hybrid/Thorne/item_slots_thorne01.tga
```

### A2 How it works

**Layered config resolution** (no duplication):

1. Base layout + base gradients: `.bin/regen_slots.json`
2. Theme overrides: `Options/Slots/Themes/<Theme>/.regen_slots.json`
3. Class overrides (optional): `Options/Slots/.Master_<Class>/.regen_thorne.json`

The **class** only affects the atlas (source art). The **theme** only affects gradients. Output is written to `Options/Slots/Output/<Class>/<Theme>/`.

### A2 Script impact

- Add an optional flag to `regen_slots.py` for **output folder** and **theme path**.
- Example usage:
  - `regen_thorne.bat .Master_Caster`
  - `regen_slots.bat --theme Themes/Gold --out Output/Caster/Gold`

### A2 Pros

- No duplicated `.json` configs per class.
- All theme edits happen in one place.
- Class-specific outputs remain clean and organized.

### A2 Cons

- Requires a small script update to accept theme path + output folder.

## Option A3 — Nested Master Layout (Class Overrides Under .Master)

This matches your proposed structure: class overrides live under `.Master/<Class>` and
themes live under `.Master/.Themes`. The scripts use `.Master` as the base, apply class
overrides, then apply the theme, and finally emit outputs into `Options/Slots/<Class>`.

### A3 Structure (your proposal)

```
thorne_drak/Options/Slots/
  .Master/
    .regen_thorne.json
    .Themes/
      Gold/.regen_slots.json
      Silver/.regen_slots.json
      Bronze/.regen_slots.json
      Platinum/.regen_slots.json
      Thorne/.regen_slots.json
    Caster/
      .regen_thorne.json
    Melee/
      .regen_thorne.json
    Hybrid/
      .regen_thorne.json

  Caster/
    Gold/item_slots_thorne01.tga
    Silver/item_slots_thorne01.tga
  Melee/
    Gold/item_slots_thorne01.tga
  Hybrid/
    Thorne/item_slots_thorne01.tga
```

### A3 How it works

1. Load base `.Master/.regen_thorne.json`.
2. Merge class override from `.Master/<Class>/.regen_thorne.json` (only the slots you want to change).
3. Generate class-specific atlases.
4. Apply theme overlays from `.Master/.Themes/<Theme>/.regen_slots.json`.
5. Output to `Options/Slots/<Class>/<Theme>/`.

### A3 Script impact

- `regen_thorne.py` gains `--class <Class>` that loads `.Master/<Class>/.regen_thorne.json` as a patch.
- `regen_slots.py` gains `--theme <Theme>` and `--class <Class>`:
  - Theme path resolves to `.Master/.Themes/<Theme>/.regen_slots.json`.
  - Output path resolves to `Options/Slots/<Class>/<Theme>/`.
- A convenience wrapper could iterate all class/theme combinations.

### A3 Pros

- Exactly matches your desired folder layout.
- No duplicated theme configs.
- Class overrides are minimal and isolated.

### A3 Cons

- Requires script support for class-based patching and class-based output routing.

## Option B — Class-Type Variants as Options

### B Structure

```
thorne_drak/Options/Slots/
  Caster/
  Melee/
  Hybrid/
```

### B Workflow

- Each class type becomes a normal Options variant.
- Atlas remains single master; class differences are achieved through gradient overrides and icon selection.

### B Impact

- **Limited** if class types need distinct source art (dragitem set).
- Would require more complex overrides to mimic gear differences.

### B Pros

- Simple directory structure.
- No changes to atlas generation.

### B Cons

- Not viable if class types need different source images.
- Overload of per-variant overrides.

## Option C — Hybrid Approach (Master + Variant Sub-Options)

### C Structure

```
thorne_drak/Options/Slots/
  .Master/
  .Master_Caster/
  .Master_Melee/
  .Master_Hybrid/
  Gold/
  Silver/
  Bronze/
  Phantom/
  Ghost/
```

### C Workflow

- Swap master atlas for class type.
- Apply metal variants on top (Gold/Silver/Bronze/etc.).

### C Impact

- Works cleanly with current scripts.
- Adds more combinations but keeps data in predictable layers.

### C Pros

- Best flexibility.
- Keeps class-type art separate from gradient styling.

### C Cons

- More combinations to test.

## Gradient Organization Recommendations

- Keep **base metals** in `.bin/regen_slots.json` (Gold/Silver/Bronze/Platinum).
- Add diagonal variants in the same file for consistent testing.
- Move experimental or theme-specific gradients (Phantom, Ghost, Shadow variants) into Option-level configs when they grow.
- Consider separate Option packs if the preset list grows large:

```
thorne_drak/Options/Slots/Phantom/
thorne_drak/Options/Slots/Ghost/
thorne_drak/Options/Slots/MetalTest/
```

## How Class + Theme Combos Would Appear

With Option A2 (Layered Overrides), you can have:

```
Output/
  Caster/Gold/
  Caster/Silver/
  Caster/Thorne/
  Melee/Gold/
  Melee/Silver/
  Melee/Thorne/
  Hybrid/Gold/
  Hybrid/Silver/
  Hybrid/Thorne/
```

Each output folder contains the generated `item_slots_thorne01.tga` and any `.regen_slots-stats.json` artifacts. The **theme config is shared**, the **class master atlas is swapped**.

## Script Considerations

- `regen_thorne.bat` already supports a master argument; keep using this to pick class type.
- If class-type masters expand, consider adding a selector wrapper:
  - `regen_thorne_class.bat Caster`
- No changes needed in `regen_slots.py` if all masters keep the same slot layout.
- If layouts diverge, `regen_slots.json` would need per-master variants (not recommended).

### Minimal Script Extension (for Option A2)

- Add two optional CLI arguments to `regen_slots.py`:
  - `--theme <path>`: Path to shared theme config (e.g., `Themes/Gold`)
  - `--out <path>`: Output folder for generated slots

This keeps the base layout in `.bin/regen_slots.json`, avoids duplicating configs, and still produces class-specific outputs.

## Recommended Path Forward

1. Adopt **Option A3** if you want class overrides under `.Master/` with theme packs in `.Master/.Themes`.
2. Adopt **Option A2** if you prefer themes separated from `.Master`.
3. Keep gradient presets centralized until they become too large.
4. Add Theme packs for special styles only when needed.
5. Preserve identical slot layouts across masters to avoid script complexity.

## Notes for Future Slot Systems

- Inventory, Loot, Merchant, Bank can reuse this same approach.
- Class-type atlases can be shared across systems for visual consistency.
- Keep gradients subtle to preserve placeholder readability without overpowering item art.
