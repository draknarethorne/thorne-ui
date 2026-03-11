# Pet Info Window Analysis (EQUI_PetInfoWindow.xml)

## Summary
- **Status**: ✅ EQType-validated
- **Key Finding**: Thorne includes pet HP, pet mana, and HP% label. Nillipuss uses a **multi-layer pet HP gauge** but has no pet mana gauge.

---

## EQType Validation (Referenced by Screen/Page Pieces)

### Thorne
- `PIW_PetHPGauge` (Gauge, **EQType 16**)
- `PIW_PetManaGauge` (Gauge, **EQType 17**)
- `PIW_Pet_HPLabel` (Label, **EQType 69**)

### Nillipuss
- `Pet_HP_BG`, `Pet_HP_0`, `Pet_HP_1A/1B/2A/2B/3A/3B/4A/4B` (Gauge, **EQType 16**)
- `PIW_Pet_HPLabel` (Label, **EQType 69**)

**Hidden/Unreferenced EQType Elements**: None detected.

---

## Key Differences

- **Nillipuss**: Multi-layer pet HP gauge (visual color/gradient system using EQType 16)
- **Thorne**: Single-layer pet HP gauge + **pet mana gauge (EQType 17)**

---

## Recommendations

1. **Keep Thorne’s pet mana gauge** (unique functional addition).
2. If desired, consider porting the **multi-layer pet HP gauge** visuals from Nillipuss for improved at-a-glance health feedback.

---

## Notes

This window is now EQType-validated and aligned with analysis standards.