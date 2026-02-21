# Thorne Slots Rebuild Plan

Maintainer: Draknare Thorne

This folder is the planning hub for the Slots pipeline redesign.

## Working docs

- `proof_of_concept.md` — current state analysis of existing `.bin` scripts and recommended split

## Baseline objective

Migrate from monolithic generation in `thorne_drak/` to a master-driven pipeline rooted in:

- `thorne_drak/Options/Slots/.Master/`

Then generate option-ready outputs from master assets.

## Target end-state (current direction)

- Final swappable textures:
  - `thorne_slots01.tga` → inventory/dedicated equipment and utility slots
  - `thorne_slots02.tga` → logo-driven branded slot/button family
- Generated from `.Master` assets and published into option variants (later: `Options/Slots/Gold`, `Silver`, `Metal`, etc.)
- Long-run: update animation references away from `window_pieces01/02.tga` to Thorne slot atlases where appropriate.

## Planned phases

1. Rebaseline + path migration to `.Master`
2. Define exact `thorne_slots01/02` atlas contracts (required cells, coordinates, size families)
3. Split script responsibilities (buttons, icons, colorizer, compositor)
4. Generate option variant outputs (`Gold`, `Silver`, `Metal`, etc.)
5. Integrate with Options sync/deploy workflow

## Confirmed slot animation universe (from current `EQUI_Animations.xml`)

Primary slot animations currently in play:

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

Related inventory button/tab animations:

- `A_InventoryBtnNormal`
- `A_InventoryBtnFlyby`
- `A_InventoryBtnPressed`
- `A_InventoryBtnPressedFlyby`
- `A_BagsTabIcon`
- `A_BagsTabActiveIcon`

These 24 entries are the minimum baseline set to account for in the first atlas contract draft.

## Status

- Script inventory + rebaseline analysis complete in `proof_of_concept.md`
- Slot animation baseline extracted (24 items) and added here
- Next: draft concrete coordinate map for `thorne_slots01.tga` and `thorne_slots02.tga`
