# Final Class-Type Slot System Architecture

**Document**: Final organizational structure for class-aware slot generation system
**Date**: February 22, 2026
**Status**: Ready for Review & Implementation

---

## Executive Summary

This document defines the complete directory structure and data flow for the Thorne UI slot generation system with class-specific item overrides, centralized theme definitions, and organized source assets.

**Key Principles**:
- **Single Source of Truth**: Master configs in `.Master/` directory
- **Inheritance Model**: Class overrides patch base configs (only modified items)
- **Theme Sharing**: Color/gradient themes used across all classes
- **Clean Asset Organization**: Source items in `.Items/` subdirectory
- **Generated Output**: Separate by class+theme combination

---

## Complete Directory Structure

```
Options/Slots/
├── .Master/                          # ← All configuration and source assets
│   ├── .regen_slots.json             # Master layout: slot map + base gradients
│   ├── .Items/                       # Source dragitem texture files
│   │   ├── dragitem001.tga
│   │   ├── dragitem002.tga
│   │   ├── dragitem003.tga
│   │   ├── dragitem004.tga
│   │   ├── dragitem005.tga
│   │   ├── dragitem006.tga
│   │   ├── dragitem007.tga
│   │   ├── dragitem008.tga
│   │   └── ... (dragitem009-dragitem036.tga)
│   │
│   ├── .Themes/                      # Theme variations (colors, gradients)
   │   ├── Thorne/                   # Default theme (personal preference for copy-back)
   │   │   └── .regen_slots.json     # Thorne theme gradient overrides
│   │   │
│   │   ├── Gold/
│   │   │   └── .regen_slots.json     # Gold gradient overrides
│   │   │
│   │   ├── Silver/
│   │   │   └── .regen_slots.json     # Silver gradient overrides
│   │   │
│   │   ├── Patriot/
│   │   │   └── .regen_slots.json     # Patriot (red/white/blue) overrides
│   │   │
│   │   ├── Bronze/
│   │   │   └── .regen_slots.json     # Bronze overrides
│   │   │
│   │   ├── Transparent/
│   │   │   └── .regen_slots.json     # Transparent background overrides
│   │   │
│   │   └── Texture/
│   │       └── .regen_slots.json     # Textured background overrides
│   │
│   └── .Classes/                     # Class-specific item overrides (patch model)
│       ├── Caster/
│       │   └── .regen_thorne.json    # Caster armor/weapon/spell items override
│       │
│       ├── Melee/
│       │   └── .regen_thorne.json    # Melee armor/weapon override
│       │
│       ├── Hybrid/
│       │   └── .regen_thorne.json    # Hybrid armor/weapon override
│       │
│       └── Thorne/
│           └── .regen_thorne.json    # Thorne variant (optional custom items)
│
├── Caster/                           # ← Generated output (per class)
│   ├── Thorne/
│   │   └── item_slots_thorne01.tga   # Caster + Thorne theme output
│   ├── Gold/
│   │   └── item_slots_thorne01.tga   # Caster + Gold theme output
│   ├── Silver/
│   │   └── item_slots_thorne01.tga   # Caster + Silver theme output
│   ├── Patriot/
│   │   └── item_slots_thorne01.tga   # Caster + Patriot theme output
│   ├── Bronze/
│   │   └── item_slots_thorne01.tga   # Caster + Bronze theme output
│   ├── Transparent/
│   │   └── item_slots_thorne01.tga   # Caster + Transparent theme output
│   └── Texture/
│       └── item_slots_thorne01.tga   # Caster + Texture theme output
│
├── Melee/                            # ← Generated output (per class)
│   ├── Thorne/
│   │   └── item_slots_thorne01.tga   # Melee + Thorne theme output
│   └── ... (Gold, Silver, Patriot, etc.)
│
├── Hybrid/                           # ← Generated output (per class)
│   ├── Thorne/
│   │   └── item_slots_thorne01.tga   # Hybrid + Thorne theme output
│   └── ... (Gold, Silver, Patriot, etc.)
│
└── Thorne/                           # ← Generated output (per class)
    ├── Thorne/
    │   └── item_slots_thorne01.tga   # Thorne + Thorne theme output [PREFERRED]
    └── ... (Gold, Silver, Patriot, etc.)
```

---

## Data Flow & Configuration Hierarchy

### Two-Step Generation Workflow

**STEP 1: Atlas Generation** (`regen_thorne.py`)
```
.Master/.Items/dragitem*.tga (source items: 36 files)
          ↓
    Load Master Config
    └─ .Master/.regen_thorne.json (base item definitions)
          ↓
    Load Class Override (if specified)
    └─ .Master/.Classes/<Class>/.regen_thorne.json (item patches)
          ↓
    Generate Class Atlas
    └─ .Master/.Classes/<Class>/item_atlas.tga (intermediate)
       Only dragitems for this class, composited together
```

**STEP 2: Final Composite** (`regen_slots.py`)
```
.Master/.Classes/<Class>/item_atlas.tga (from Step 1)
          ↓
    Load Slot Layout & Button Config
    └─ .Master/.regen_slots.json (base layout + button definitions)
          ↓
    Load Theme Overrides (if specified)
    └─ .Master/.Themes/<Theme>/.regen_slots.json (gradient patches)
          ↓
    Composite: Atlas + Buttons + Gradient Tints
    └─ Generate final item_slots_thorne01.tga
              ↓
    Output: Options/Slots/<Class>/<Theme>/item_slots_thorne01.tga
              ↓
    Copy-Back (conditional)
    └─ thorne_drak/item_slots_thorne01.tga (if Thorne/Thorne or specified)
```

### Config Inheritance Model

- **Master Configs** (`.Master/`):
  - `.regen_thorne.json` = Base items + dragitem definitions (shared by all classes)
  - `.regen_slots.json` = Base slot layout + button styles + gradient presets
  
- **Class Overrides** (`.Master/.Classes/<Class>/`):
  - `.regen_thorne.json` = Only items that differ from master (patch model)
  - `.Thorne/` class likely mirrors master, but available for customization
  
- **Theme Overrides** (`.Master/.Themes/<Theme>/`):
  - `.regen_slots.json` = Only gradients that differ from master (patch model)
  - `.Thorne/` theme likely mirrors master, but available for customization

---

## Configuration Files: Content & Purpose

### Master Config: `.Master/.regen_slots.json`

```json
{
  "slot_map": {
    "rows": [
      { "row": 1, "items": ["Head", "Neck", "Shoulders", "Back"] },
      // ... all 9 rows
    ]
  },
  "items": [
    {
      "dragitem": 1,
      "item_name": "Head",
      "fit_size": [30, 30],
      "offset": [0, 0]
    },
    // ... 36 total items including pack/satchel
  ],
  "gradient_presets": {
    "thorne": { "colors": ["#2C3E50", "#3498DB", "#5DADE2"] },
    "gold": { "colors": ["#8B7500", "#FFD700", "#B8860B"] },
    "silver": { /* ... */ },
    // ... all gradient definitions
  },
  "button_backgrounds": {
    "default": { /* button piece definitions */ }
  }
}
```

**Purpose**: Single source of truth for:
- Slot positions (which item goes where)
- All gradient color definitions (including Thorne theme defaults)
- Default button styling
- Item fit sizes and offset adjustments

**Used By**: All class+theme combinations inherit from this

---

### Class Override: `.Classes/<Class>/.regen_thorne.json`

```json
{
  "class_name": "Caster",
  "description": "Caster armor and spell focus items",
  "item_overrides": [
    {
      "dragitem": 3,
      "override_name": "CustomSpellFocus",
      "fit_size": [32, 32],
      "offset": [-1, -1]
    },
    {
      "dragitem": 15,
      "override_name": "CasterRobe",
      "fit_size": [32, 32],
      "offset": [0, 0]
    }
  ],
  "note": "Only includes items that differ from base class"
}
```

**Purpose**: 
- Override only the dragitem IDs that differ per class
- Define custom names for class-specific items
- Patch model: only changed items, rest inherited from master
- Keep file size minimal (only 3-5 items typically differ)

**Used By**: regen_slots.py when generating class-specific variants

---

### Theme Override: `.Themes/<Theme>/.regen_slots.json`

```json
{
  "theme_name": "Gold",
  "description": "Gold-themed slot borders and indicators",
  "gradient_overrides": {
    "gold": { "colors": ["#8B7500", "#FFD700", "#B8860B"] },
    "gold_gleam": { "colors": ["#5C4A00", "#FFE34D", "#8B7500"], "direction": "diagonal" }
  },
  "button_overrides": {
    "default": { /* gold-themed button piece definitions */ }
  },
  "note": "Only includes gradients/buttons that differ from master"
}
```

**Purpose**:
- Override color/gradient values per theme
- Apply themed button styling
- Keep configuration modular and reusable
- Used across all class variants without duplication

**Special Note on Thorne Theme**:
- `.Themes/Thorne/` is the default user theme and personal preference
- When both --all-classes and --all-themes are used, Thorne/Thorne combo is copied back to thorne_drak/
- This preserves your personal theme as the active UI while keeping alternatives available

**Used By**: regen_slots.py when generating theme-specific output

---

## Copy-Back Logic: Preserving Your Personal Theme

### When Copy-Back Happens

The **copy-back step** only occurs when `regen_slots.py` completes successfully. It copies the
final `item_slots_thorne01.tga` from `Options/Slots/<Class>/<Theme>/` back to `thorne_drak/`
to activate it in your UI.

### Copy-Back Rules

#### Rule 1: Full Workflow (both steps)

```bash
.bin/regen_thorne.bat --all-classes
# STEP 1: Generates all class atlases in .Master/.Classes/
# STEP 2: Triggers regen_slots with --all-combos
#         Generates all class/theme combinations
#         Copy-back: Thorne/Thorne → thorne_drak/   ← Your personal preference
```

#### Rule 2: Specific Class (both steps)

```bash
.bin/regen_thorne.bat --class Caster
# STEP 1: Generates Caster atlas in .Master/.Classes/Caster/
# STEP 2: Triggers regen_slots with --class Caster
#         Generates all Caster/theme combinations
#         Copy-back: Caster/Thorne → thorne_drak/   ← Default Thorne theme active
```

#### Rule 3: Specific Theme (STEP 2 only)

```bash
.bin/regen_slots.bat --theme Gold
# Generates all class/Gold combinations
# Copy-back: NONE   ← Exploring variants, not changing active UI
```

#### Rule 4: Specific Class + Theme (STEP 2 only)

```bash
regen_slots.py --class Caster --theme Gold
# Generates Caster/Gold combination only
# Copy-back: NONE   ← You're testing a variant
#           (use --copy-back flag to force activation if desired)
```

### Example Batch Workflow

```bash
# Create all variants while keeping Thorne/Thorne active
.bin/regen_thorne.bat --all-classes
# All class/theme combos generated
# thorne_drak/item_slots_thorne01.tga now has Thorne/Thorne

# Test a new theme without changing active UI
regen_slots.py --class Caster --theme Gold
# Generates Options/Slots/Caster/Gold/item_slots_thorne01.tga
# Does NOT copy back (still have Thorne/Thorne active)

# Try a different class
.bin/regen_thorne.bat --class Melee
# Generates Melee atlas + all Melee/theme combos
# Copies Melee/Thorne to thorne_drak/ (now Melee is active)

# Test theme on new class, then activate it
regen_slots.py --class Melee --theme Patriot
# Generates Melee/Patriot but doesn't copy back

# When ready, activate the Patriot theme
cp Options/Slots/Melee/Patriot/item_slots_thorne01.tga thorne_drak/item_slots_thorne01.tga
# Or add --copy-back flag to regen_slots.py command
```

---

## Script Changes & Command Usage

### Command: Generate All Classes + All Themes (Full Workflow)

```bash
.bin/regen_thorne.bat --all-classes
```

**What it does** (complete pipeline):

**STEP 1** - Atlas Generation:
1. Generates base `.Master/item_atlas.tga` from master config
2. Discovers all classes under `.Master/.Classes/`
3. For each class, generates `.Master/.Classes/<Class>/item_atlas.tga` with config overrides

**STEP 2** - Slot Composition:
4. Triggers `.bin/regen_slots.bat --all-combos`
5. For each class+theme combination:
- Reads class atlas from `.Master/.Classes/<Class>/item_atlas.tga`
- Applies theme gradients from `.Master/.Themes/<Theme>/.regen_slots.json`
- Composites with buttons from `.Master/.regen_slots.json`
- Outputs to `Options/Slots/<Class>/<Theme>/item_slots_thorne01.tga`

**STEP 3** - Copy-Back:
6. Copies `Options/Slots/Thorne/Thorne/item_slots_thorne01.tga` → `thorne_drak/item_slots_thorne01.tga`

**Output**: All class/theme combinations generated + Thorne/Thorne active in UI

---

### Command: Generate Specific Class (Both Steps)

```bash
.bin/regen_thorne.bat --class Caster
```

**What it does**:

**STEP 1** - Atlas Generation:
1. Generates base `.Master/item_atlas.tga`
2. Generates Caster atlas: `.Master/.Classes/Caster/item_atlas.tga` with overrides
   (other class atlases not regenerated)

**STEP 2** - Slot Composition:
3. Triggers `.bin/regen_slots.bat --class Caster`
4. For each Caster+theme combination:
- Reads from `.Master/.Classes/Caster/item_atlas.tga`
- Applies theme from `.Master/.Themes/<Theme>/.regen_slots.json`
- Outputs to `Options/Slots/Caster/<Theme>/item_slots_thorne01.tga`

**STEP 3** - Copy-Back:
5. Copies `Options/Slots/Caster/Thorne/item_slots_thorne01.tga` → `thorne_drak/item_slots_thorne01.tga`
   (Caster class with default Thorne theme becomes active)

### Command: Generate Specific Theme (All Classes)

```bash
.bin/regen_slots.bat --theme Gold
```

**Prerequisites**: Class atlases must already exist in `.Master/.Classes/<Class>/` (run `.bin/regen_thorne.bat --all-classes` first if needed)

**What it does** (STEP 2 only):

1. Discovers all classes under `.Master/.Classes/`
2. For each class, applies Gold theme gradients from `.Master/.Themes/Gold/.regen_slots.json`:
   - Reads existing atlas from `.Master/.Classes/<Class>/item_atlas.tga`
   - Composites with buttons from `.Master/.regen_slots.json`
   - Outputs to `Options/Slots/<Class>/Gold/item_slots_thorne01.tga`
3. Does NOT copy-back (you're exploring theme variants, not activating one)

---

### Command: Generate Specific Class + Theme

```bash
regen_slots.py --class Caster --theme Gold --verbose
```

**Prerequisites**: Caster atlas must exist in `.Master/.Classes/Caster/` (run `.bin/regen_thorne.bat --class Caster` first if needed)

**What it does** (STEP 2 only):

1. Reads Caster atlas from `.Master/.Classes/Caster/item_atlas.tga`
2. Loads slot layout from `.Master/.regen_slots.json`
3. Applies Gold theme overrides from `.Master/.Themes/Gold/.regen_slots.json`
4. Composites: atlas + buttons + gradient tints
5. Outputs to `Options/Slots/Caster/Gold/item_slots_thorne01.tga`
6. With `--verbose`: Shows config loading and per-item processing details
7. Does NOT copy-back (unless you explicitly want this class/theme active)

---

## Verbosity Modes

### Default (Quiet) Mode

```
Generating slots for Caster + Thorne...
[████████████████████] 36/36 items
✓ Output: Options/Slots/Caster/Thorne/item_slots_thorne01.tga
✓ Copied to: thorne_drak/item_slots_thorne01.tga
```

### Verbose Mode (--verbose flag)

```
Generating slots for Thorne + Thorne...
  Loading base config: Options/Slots/.Master/.regen_slots.json
  Loading class overrides: Options/Slots/.Master/.Classes/Thorne/.regen_thorne.json
    - dragitem 3 (CustomSpellFocus) [32x32 @-1,-1]
    - dragitem 15 (CasterRobe) [32x32 @0,0]
  Loading theme overrides: Options/Slots/.Master/.Themes/Thorne/.regen_slots.json
    - gradient_thorne: #2C3E50 -> #3498DB -> #5DADE2
  Processing items:
    [1/36] Head (dragitem 1) with thorne gradient...
    [2/36] Neck (dragitem 2) with thorne gradient...
    ...
    [36/36] Satchel (dragitem 36) with thorne gradient...
  Composite background and button frames...
  ✓ Output: Options/Slots/Thorne/Thorne/item_slots_thorne01.tga (1024x256, 156KB)
  ✓ Copied to: thorne_drak/item_slots_thorne01.tga (personal preference)
```

---

## Migration & Implementation Steps

### Phase 1: Directory Structure Setup

1. Create `.Master/` directory hierarchy
2. Create `.Master/.Items/` and copy dragitem*.tga files
3. Create `.Master/.Themes/` and `.Master/.Classes/` subdirectories
4. Create theme-specific config files in each `.Themes/<ThemeName>/`

### Phase 2: Configuration Migration

1. Move `.regen_slots.json` from `.bin/` to `Options/Slots/.Master/.regen_slots.json`
2. Copy existing theme configs (Gold, Silver, etc.) to `.Master/.Themes/<ThemeName>/.regen_slots.json`
3. Create initial class override files for Caster, Melee, Hybrid, Thorne

### Phase 3: Script Updates

1. Update `regen_thorne.py` to read source items from `.Master/.Items/`
2. Update `regen_slots.py` to discover themes and classes from `.Master/` structure
3. Add `--verbose` flag support to both scripts
4. Update batch wrappers to use new paths

### Phase 4: Testing

1. Test `.bin/regen_thorne.bat --all-classes`
2. Test `.bin/regen_slots.bat --all-combos`
3. Verify all class+theme combinations generate correctly
4. Test `--verbose` flag output
5. Verify output files in `Options/Slots/<Class>/<Theme>/`

---

## Benefits of This Architecture

| Benefit | How Achieved |
|---------|-------------|
| **Single source of truth** | Master config in `.Master/.regen_slots.json` |
| **Minimal duplication** | Class/theme overrides only contain changes (patch model) |
| **Easy to extend** | Add new class/theme by adding one file + overrides |
| **Clean organization** | Source assets, configs, and output in logical groups |
| **Cross-class consistency** | Shared themes applied uniformly to all classes |
| **Backward compatible** | Old Options/Slots/<Theme>/ style can coexist during transition |
| **Batch automation** | Single command regenerates everything or specific combos |
| **Transparent workflow** | `--verbose` mode shows exactly what's being applied |

---

## Questions for Confirmation

Before implementation, please confirm:

1. ✅ **Directory structure correct?** Should everything under `Options/Slots/.Master/` or split elsewhere?
2. ✅ **Item source location** (`.Master/.Items/`) — good for cleanliness?
3. ✅ **Class override format** — patch model (only changed items) or full item list?
4. ✅ **Verbose output style** — matches the examples above?
5. ✅ **Command syntax** — clear how to generate all/specific class/theme combos?

---

## Summary

This architecture provides:

- **`.Master/` as control center**: All configs and source assets in one place
- **Clean inheritance**: Base → Class → Theme overrides applied in order
- **Organized output**: Generated files sorted by class and theme
- **Automation ready**: Single command can regenerate any combination
- **Human-friendly**: Directory names and structure self-document the system

Ready to proceed with implementation? 🚀
