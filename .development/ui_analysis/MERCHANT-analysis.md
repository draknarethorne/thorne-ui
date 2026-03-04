# Merchant Window Analysis (EQUI_MerchantWnd.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Thorne’s Merchant window is far more feature-rich, embedding player equipment, bags, and stat labels alongside merchant inventory. Nillipuss focuses primarily on merchant slots.

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- **Merchant inventory**: `MW_MerchantSlot0–79` (InvSlot, **EQType 6000–6079**)
- **Player bags**: `MW_InvSlot22–29` (InvSlot, **EQType 22–29**)
- **Player equipment (two groups)**:
  - `MW_Primary`, `MW_Secondary`, `MW_Range`, `MW_Ammo` (InvSlot **11/13/14/21**)
  - `MW_Bags_Primary`, `MW_Bags_Secondary`, `MW_Bags_Range`, `MW_Bags_Ammo` (InvSlot **11/13/14/21**)
  - `MW_LEar`…`MW_Waist` (InvSlot **1–20**)
- **Stats/identity labels**:
  - Name/Level/Class/Deity (**EQType 1–4**)
  - HP/Mana values (**EQType 70/80**)
  - AC/ATK (**EQType 22/23**)
  - Weight (**EQType 24/25**)
  - Base stats STR/STA/DEX/AGI/WIS/INT/CHA (**EQType 5–11**)
  - Resists Poison/Disease/Fire/Cold/Magic (**EQType 12–16**)
  - XP gauge (**EQType 4**) + XP% (**EQType 26**)

### Nillipuss
- **Merchant inventory**: `MW_MerchantSlot0–79` (InvSlot, **EQType 6000–6079**)
- **No additional player stat/equipment/bag EQType bindings detected**

**Hidden/Unreferenced EQType Elements**: None detected in either file.

---

## Key Differences

### Thorne-only
- Embedded player equipment grid and bag slots
- Extensive player stat/identity labels
- XP gauge and XP% in the merchant context

### Nillipuss-only
- No additional EQType-bound elements beyond merchant inventory slots

---

## Recommendations

1. **Keep Thorne’s richer merchant window** — it provides a full at-a-glance character context during purchases.
2. **No porting needed from Nillipuss** (merchant slots are already standard and identical).

---

## Notes

This window is now EQType-validated and aligned with analysis standards.