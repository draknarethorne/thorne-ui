# Alt Storage Window Analysis (EQUI_AltStorageWnd.xml)

## Summary
- **Status**: ✅ Reviewed (no EQType bindings)
- **Key Finding**: `EQUI_AltStorageWnd.xml` exists only in `default/` and is **missing** from both `thorne_drak` and `Nillipuss` variants.

---

## EQType Validation (Referenced by Screen/Page Pieces)

- **No EQType-bound elements** in the default file.
- Window uses labels, listbox, and buttons only.

---

## Key Differences

- **Not present** in either Thorne or Nillipuss.
- Default window titled “Shroud Bank” with timer + item list UI.

---

## Recommendations

1. **No porting required** unless your server/client relies on Alt Storage (shroud bank) functionality.
2. If needed, consider importing the default window into Thorne’s variant set and styling to match standards.

---

## Notes

This window is documented for completeness; no EQType bindings exist to validate.
