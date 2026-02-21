# Thorne Slots Proof of Concept (Rebaseline)

Maintainer: Draknare Thorne  
Date: 2026-02-20

## Goal of this analysis

Create a clean inventory of existing `.bin` scripts that currently process or support Thorne texture workflows (especially `thorne_*.tga`), then classify each as:
- **Keep as-is**
- **Adapt to new `.Master` workflow**
- **Archive / replace**

Target direction: shift generation roots into:
- `C:\Thorne-UI\thorne_drak\Options\Slots\.Master`

and generate option-ready outputs from master files.

---

## Scripts directly tied to `thorne_*.tga`

### 1) `.bin/generate_thorne_buttons_transparent.py`

**Current purpose**
- Reads `thorne_drak/thorne_buttons01.tga`
- Detects source buttons in row 1
- Generates 5 alpha rows (95/90/85/75/50)
- Preserves 3px border, changes inner alpha only
- Writes back to the same `thorne_buttons01.tga`

**Inputs**
- `thorne_drak/thorne_buttons01.tga`

**Outputs**
- `thorne_drak/thorne_buttons01.tga` (in-place rewrite)

**Current assumptions**
- 255x255 atlas
- 40x40 buttons
- 2px row spacing

**Recommendation**
- **Adapt** to read/write from `Options/Slots/.Master` path.
- Keep logic; parameterize source/output paths.

---

### 2) `.bin/generate_thorne_icons_master.py`

**Current purpose**
- Reads one source icon from `thorne_drak/thorne_icon.tga` at `(2,2)`
- Produces `thorne_drak/thorne_icons01.tga`
- Top-row layout: 4x 40px + 4x 20px copies (2px spacing)
- Includes 20px sharpening pass

**Inputs**
- `thorne_drak/thorne_icon.tga`

**Outputs**
- `thorne_drak/thorne_icons01.tga`

**Recommendation**
- **Adapt** to `.Master` location and keep as first-stage icon seeding script.
- Add configurable icon source slots (future: multiple source icons in row 1).

---

### 3) `.bin/generate_thorne_slot_variants.py`

**Current purpose**
- Monolithic prototype script combining multiple concerns:
  1. Builds icon tonal variants (silver/gold/hybrid)
  2. Reads button variants from `thorne_buttons01.tga`
  3. Composites icon+button outputs into preview atlases
- Writes:
  - `thorne_drak/thorne_icons_slots01.tga`
  - `thorne_drak/thorne_icons_slots02.tga`
  - `thorne_drak/thorne_icons_slots03.tga`

**Inputs**
- `thorne_drak/thorne_icon.tga`
- `thorne_drak/thorne_buttons01.tga`

**Outputs**
- `thorne_drak/thorne_icons_slots0{1,2,3}.tga`

**Recommendation**
- **Split/replace** into pipeline stages:
  - Stage A: icon master + color rows (`thorne_icons01.tga` in `.Master`)
  - Stage B: button alpha rows (`thorne_buttons01.tga` in `.Master`)
  - Stage C: compositor that only assembles from masters into option outputs
- This script should become the **compositor only** (long-run).

---

### 4) `.bin/generate_thorne_icons_collage.py`

**Current purpose**
- Legacy proof/collage script from old `thorne_drak01.jpg/.tga` workflow
- Produces a visual sample atlas in `thorne_icons01.tga`

**Recommendation**
- **Archive** (historical prototype).
- Do not use for new `.Master` pipeline.

---

## Adjacent scripts that affect icon texture workflows (non-`thorne_*.tga` naming)

### 5) `.bin/regen_icons.py`

**Purpose**
- Rebuilds `staticons01.tga` from `Options/Icons/<Variant>/` sources using JSON mapping.

**Why relevant**
- Already demonstrates option-oriented generation and smart copy/deploy behavior.

**Recommendation**
- **Reference pattern** for argument design, variant discovery, copyback logic.

---

### 6) `.bin/regen_gems.py`

**Purpose**
- Generates `gemiconsXX.tga` + `spelliconsXX.tga` from `spellsXX.tga`, then triggers staticon regeneration.

**Why relevant**
- Demonstrates staged pipeline and multi-output generation from one source family.

**Recommendation**
- **Reference pattern** for staged orchestration and output packaging.

---

### 7) `.bin/fix_tga_files.py`

**Purpose**
- Scan/fix mislabeled PNG-as-TGA files.

**Why relevant**
- Useful QA guardrail for any generated masters/options.

**Recommendation**
- **Keep** and run in validation steps.

---

### 8) `.bin/sync_option.py` and `.bin/options_thorne_sync.py`

**Purpose**
- Sync option variants to test target and update sync metadata.

**Why relevant**
- End-of-pipeline deployment tools once slot options are generated.

**Recommendation**
- **Keep**, likely expand once Slots option tree is formalized.

---

## Proposed new Slots architecture (baseline)

## `.Master` (authoritative source + generated masters)

Proposed root:
- `thorne_drak/Options/Slots/.Master/`

Proposed files:
- `thorne_buttons01.tga` (master button atlas: source row + alpha rows)
- `thorne_icon.tga` (single icon seed and/or icon source cells)
- `thorne_icons01.tga` (master icon atlas: 40/20 rows + future color rows)
- future: optional template/compositor config JSON(s)

## Option outputs (consumer-ready variants)

Proposed examples:
- `thorne_drak/Options/Slots/Gold/`
- `thorne_drak/Options/Slots/Silver/`
- `thorne_drak/Options/Slots/Metal/`
- future: texture/transparent/opaque families

Each option directory eventually receives generated production textures (for inventory/look/containers/hotbuttons as applicable).

---

## Recommended script split for revised approach

1. **Master Buttons Generator**
   - Input: `.Master/thorne_buttons01.tga` source row
   - Output: `.Master/thorne_buttons01.tga` full rows
   - Status: adapt current `generate_thorne_buttons_transparent.py`

2. **Master Icons Seeder**
   - Input: `.Master/thorne_icon.tga`
   - Output: `.Master/thorne_icons01.tga` base rows
   - Status: adapt current `generate_thorne_icons_master.py`

3. **Master Icon Colorizer** *(new)*
   - Input: `.Master/thorne_icons01.tga` base rows
   - Output: `.Master/thorne_icons01.tga` color rows (silver/gold/metal/etc)
   - Status: extract logic from `generate_thorne_slot_variants.py`

4. **Slots Compositor** *(refactor)*
   - Input: `.Master/thorne_buttons01.tga` + `.Master/thorne_icons01.tga`
   - Output: option-target textures (by variant set)
   - Status: refactor current `generate_thorne_slot_variants.py` into compositor-only

5. **Options Packager/Sync**
   - Input: generated outputs
   - Output: `Options/Slots/<Variant>/...` + optional deployment to `thorne_dev`

---

## What to archive soon

- `.bin/generate_thorne_icons_collage.py` (legacy prototype)
- Any transitional one-off scripts that still read `thorne_drak/thorne_drak01.*` directly

---

## Key rebaseline decisions to lock before implementation

1. Exact file names in `.Master` (confirm canonical names)
2. Row/column coordinate contract for both master atlases
3. Whether color rows include both 40 and 20, or only 40 then derive 20 at compose time
4. Output naming convention replacing `*slots*` if desired (e.g., `emblems`, `frames`, `tiles`)
5. Which production texture files are in phase 1 (inventory/look/container/hotbutton list)

---

## Suggested naming alternatives to "slots"

If you want something clearer than "slots":
- **frames** (UI framing-centric)
- **emblems** (brand-centric, thematic)
- **tiles** (texture-atlas centric)

For now, `Slots` is still acceptable and already aligns with your Option folder concept.

---

## Updated end-state definition (2026-02-20)

User direction has shifted from proof atlases toward production-ready slot atlases:

- `thorne_slots01.tga`
  - Intended for inventory/equipment and other dedicated utility slots
  - Candidate place for embossed inventory-type source set (including new `thorne_inventory01.tga` concept)
- `thorne_slots02.tga`
  - Intended for logo-based/branded slot/button set
  - Candidate place for embossed Thorne-head and branded blank variants

The immediate design task is to lock final coordinate contracts for these two atlases before script refactors.

---

## Confirmed slot scope to plan against (current XML reality)

Extracted from current `thorne_drak/EQUI_Animations.xml` and references across `EQUI_*.xml`.

### Equipment/Inventory slot animations (18)

- `A_InvEar`
- `A_InvNeck`
- `A_InvHead`
- `A_InvFace`
- `A_InvChest`
- `A_InvAboutBody`
- `A_InvArms`
- `A_InvShoulders`
- `A_InvWrist`
- `A_InvWaist`
- `A_InvHands`
- `A_InvRing`
- `A_InvLegs`
- `A_InvFeet`
- `A_InvPrimary`
- `A_InvSecondary`
- `A_InvRange`
- `A_InvAmmo`

### Related inventory/bag UI controls (6)

- `A_InventoryBtnNormal`
- `A_InventoryBtnFlyby`
- `A_InventoryBtnPressed`
- `A_InventoryBtnPressedFlyby`
- `A_BagsTabIcon`
- `A_BagsTabActiveIcon`

Total current slot-adjacent animation set: **24**

---

## Practical implication for atlas planning

Before code changes, define a coordinate table for:

1. `thorne_slots01.tga`:
   - Required 40x40 slot cells for all 18 equipment/inventory slot animations
   - Any additional dedicated slots (bag/blank/utility) you want in phase 1

2. `thorne_slots02.tga`:
   - Branded/logo slot/button cells
   - State variants (opaque/transparent/metal/gold/silver families later)

3. Optional 20x20 strategy:
   - Either pre-baked 20x20 cells in atlas, or derived at compose time

Once these tables are locked, script work is straightforward path + compositor refactor.
