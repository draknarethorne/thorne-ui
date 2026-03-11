# HotButtonWnd Analysis (EQUI_HotButtonWnd.xml)

## Summary
- **Lines**: Nillipuss: 4012 | Thorne: 2370 (**169% larger in Nillipuss = 1642 line difference**)
- **Status**: 🔴 SIGNIFICANT DIFFERENCES - Nillipuss has more layout variants
- **Priority**: LOW-MEDIUM (hotbars are highly customizable, mostly cosmetic)

---

## Key Differences

### Nillipuss Features (EQType-verified)
Nillipuss defines multiple hotbutton windows (`HotButtonWnd`, `HotButtonWnd2`, `HotButtonWnd3`, `HotButtonWnd4`) with additional invslot bindings:

- **Primary hotbar slots**: `HB_InvSlot1–10` (InvSlot, **-1**) — standard hotbuttons
- **Inventory shortcuts (main screen)**: `Prim` (InvSlot, **13**), `Sec` (InvSlot, **14**), `Newslot1–8` (InvSlot, **22–29**)

**Hidden/Unreferenced EQType Elements (Nillipuss):**
Several equipment invslots are defined but **not referenced by any Screen/Page pieces**:
`Ranged` (11), `Ammo` (21), `Head` (2), `Chest` (17), `Legs` (18), `Boots` (19), `Belt` (20), `Earring1` (1), `Earring2` (4), `Ring1` (15), `Ring2` (16), `Wrist1` (9), `Wrist2` (10), `Face` (3), `Neck` (5), `Back` (8), `Shoulder` (6), `Arms` (7), `Hands` (12).

### Thorne Implementation (EQType-verified)
- **Primary hotbar slots**: `HB_InvSlot1–10` (InvSlot, **-1**)
- **Equipment quick slots**: `HB2_InvSlot1–10` (InvSlot, **13, 14, 22–29**)
- **Additional equipment layouts**: `HB3_InvSlot1–10` (InvSlot, **1,2,3,4,5,6,17,7,12,8**)
- **Additional equipment layouts**: `HB4_InvSlot1–10` (InvSlot, **20,18,19,9,10,15,16,11,21,0**)
- Clean, working implementation with more equipped-slot coverage on the main window

---

## v0.8.0+ Recommendation

**Complexity**: LOW-MEDIUM (mostly layout/styling)
**Value**: MEDIUM (cosmetic, but users care about hotbar customization)
**Estimated Effort**: 8-12 hours

**Action**: Create additional layout variants based on Nillipuss patterns if user community requests specific configurations. Not a priority for current release phase.

---

## Implementation Notes

- Likely candidates: Different row counts, button sizes, layouts (horizontal/vertical)
- Could be added incrementally as Options variants
- Would pair well with other UI customization features in v0.8.0+
