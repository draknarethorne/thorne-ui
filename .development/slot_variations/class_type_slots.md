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

### Structure

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

### Workflow

- Use a flag to choose master atlas source:
  - `regen_thorne.bat .Master_Caster`
  - `regen_thorne.bat .Master_Melee`
  - `regen_thorne.bat .Master_Hybrid`

### Impact

- **Minimal change** to scripts (already support argument input).
- `regen_slots.bat --all` still works, as it references `item_atlas_thorne01.tga` from the chosen master.
- Each master can share the **same** gradient presets, allowing metal variants to be compared cleanly.

### Pros

- Clear separation of class-type art.
- Preserves existing Options/Slots variants.
- Allows quick comparison via atlas swap.

### Cons

- Multiple atlas files to maintain.
- Requires consistent item layout across master files.

## Option B — Class-Type Variants as Options

### Structure

```
thorne_drak/Options/Slots/
  Caster/
  Melee/
  Hybrid/
```

### Workflow

- Each class type becomes a normal Options variant.
- Atlas remains single master; class differences are achieved through gradient overrides and icon selection.

### Impact

- **Limited** if class types need distinct source art (dragitem set).
- Would require more complex overrides to mimic gear differences.

### Pros

- Simple directory structure.
- No changes to atlas generation.

### Cons

- Not viable if class types need different source images.
- Overload of per-variant overrides.

## Option C — Hybrid Approach (Master + Variant Sub-Options)

### Structure

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

### Workflow

- Swap master atlas for class type.
- Apply metal variants on top (Gold/Silver/Bronze/etc.).

### Impact

- Works cleanly with current scripts.
- Adds more combinations but keeps data in predictable layers.

### Pros

- Best flexibility.
- Keeps class-type art separate from gradient styling.

### Cons

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

## Script Considerations

- `regen_thorne.bat` already supports a master argument; keep using this to pick class type.
- If class-type masters expand, consider adding a selector wrapper:
  - `regen_thorne_class.bat Caster`
- No changes needed in `regen_slots.py` if all masters keep the same slot layout.
- If layouts diverge, `regen_slots.json` would need per-master variants (not recommended).

## Recommended Path Forward

1. Adopt **Option A** (multiple masters) for class-type art.
2. Keep gradient presets centralized until they become too large.
3. Add Option packs for special themes only when needed.
4. Preserve identical slot layouts across masters to avoid script complexity.

## Notes for Future Slot Systems

- Inventory, Loot, Merchant, Bank can reuse this same approach.
- Class-type atlases can be shared across systems for visual consistency.
- Keep gradients subtle to preserve placeholder readability without overpowering item art.
