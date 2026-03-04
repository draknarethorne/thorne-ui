# Trade Window Analysis (EQUI_TradeWnd.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Thorne and Nillipuss Trade windows are functionally identical. EQTypes cover 16 trade slots total.

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- `TRDW_TradeSlot0–15` (InvSlot, **EQType 3000–3015**) — 8 “my” + 8 “their” trade slots

### Nillipuss
- `TRDW_TradeSlot0–15` (InvSlot, **EQType 3000–3015**) — 8 “my” + 8 “their” trade slots

**Hidden/Unreferenced EQType Elements**: None detected in either file.

> **Note**: Coin buttons (platinum/gold/silver/copper) are client-bound and do **not** use EQTypes.

---

## Key Differences

- **None detected**. Layout, bindings, and button set are the same.

---

## Recommendations

1. **No porting required** — this window is already equivalent.

---

## Notes

This window is EQType-validated and aligned with current analysis standards.
