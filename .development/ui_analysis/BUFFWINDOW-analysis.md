# BuffWindow Analysis (EQUI_BuffWindow.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Both UIs show standard buff duration labels (EQTypes **45–59**). Thorne additionally includes **ShortDurationBuffWindow** with EQTypes **135–149**. Nillipuss defines extra long-range labels (EQTypes **515–524**) that are **not referenced** by any Screen/Page pieces.

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- **BuffWindow**: `BW_Buff0`–`BW_Buff14` (Labels, **EQType 45–59**)
- **ShortDurationBuffWindow**: `SDB_Buff0_label`–`SDB_Buff14_label` (Labels, **EQType 135–149**)

### Nillipuss
- **BuffWindow**: `BW_Buff0_Label`–`BW_Buff14_Label` (Labels, **EQType 45–59**)
- Includes paired shadow labels (`BW_Buff*_LabelBG`) using the same EQType for readability

---

## Hidden/Unreferenced EQType Elements (Nillipuss)

These elements exist but are **not referenced by any Screen/Page pieces**:
- `BW_Buff15_Label`–`BW_Buff24_Label` (Labels, **EQType 515–524**)

**Interpretation**: Defined for extended buff slots but currently inactive/hidden.

---

## Structural Differences

### Thorne
- Defines **two screens** in one file: `BuffWindow` and `ShortDurationBuffWindow`
- Uses separate EQType ranges for short duration buffs (**135–149**)
- No unused EQType labels detected

### Nillipuss
- Defines **only** `BuffWindow`
- Uses paired label + background label for text shadow
- Defines extra label slots (EQType **515–524**) but they are unused

---

## Recommendations

1. **Keep Thorne’s ShortDurationBuffWindow** (EQTypes 135–149) as a distinct feature not present in Nillipuss.
2. **Optional visual enhancement**: If desired, adopt the Nillipuss shadow-label pattern for readability (BG labels with +1 offset).
3. **Do not port unused EQType 515–524 labels** unless the client actually supports those buff slots in your target environment.

---

## Notes

- This window is now fully EQType-validated and in sync with the analysis standards established for other major windows.
