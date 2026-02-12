# Bank Window Analysis (EQUI_BankWnd.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Thorne and Nillipuss have identical functional EQType coverage for main bank, expanded bank bags, and shared bank. Differences are primarily cosmetic (background textures).

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- **Main bank slots**: `BW_BankSlot0–29` (InvSlot, **EQType 2000–2029**)
- **Bank bag expansions**: `BW_Bag0Slot0–BW_Bag29Slot9` (InvSlot, **EQType 2030–2329**)
- **Shared bank**: `BW_SharedBankSlot0–9` (InvSlot, **EQType 2500–2509**)

### Nillipuss
- **Main bank slots**: `BW_BankSlot0–29` (InvSlot, **EQType 2000–2029**)
- **Bank bag expansions**: `BW_Bag0Slot0–BW_Bag29Slot9` (InvSlot, **EQType 2030–2329**)
- **Shared bank**: `BW_SharedBankSlot0–9` (InvSlot, **EQType 2500–2509**)

**Hidden/Unreferenced EQType Elements**: None detected in either file.

---

## Key Differences

- **Cosmetic only**: Nillipuss uses custom bag textures (`A_dzBag`, `A_dzS1–A_dzS10`, `Nilli_Bag`) while Thorne uses `A_RecessedBox`.
- **Functionality and slot coverage are identical**.

---

## Recommendations

1. **No porting required** — feature parity already achieved.
2. **Optional**: If desired, review texture aesthetics for a unified bank visual theme, but no EQType work is needed.

---

## Notes

This window is EQType-validated and aligned with current analysis standards.
