# Loot Window Analysis (EQUI_LootWnd.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Both UIs use standard loot slots (EQType 5000+). Nillipuss exposes **32 slots**, Thorne exposes **30 slots**.

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- `LW_LootSlot0–29` (InvSlot, **EQType 5000–5029**)

### Nillipuss
- `LW_LootSlot0–31` (InvSlot, **EQType 5000–5031**)

**Hidden/Unreferenced EQType Elements**: None detected.

---

## Key Differences

- **Nillipuss**: 32 visible loot slots (5000–5031)
- **Thorne**: 30 visible loot slots (5000–5029)

---

## Recommendations

1. **Decide on desired slot count**. If the client supports 32 slots reliably, consider matching Nillipuss for parity.
2. Otherwise, keep Thorne’s 30-slot layout as a stable baseline.

---

## Notes

This window is now EQType-validated and aligned with analysis standards.