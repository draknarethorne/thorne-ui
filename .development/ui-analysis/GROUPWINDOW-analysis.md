# GroupWindow Analysis (EQUI_GroupWindow.xml)

## Summary
- **Lines**: Nillipuss: 3103 | Thorne: 1131 (**174% larger in Nillipuss = 1972 line difference**)
- **Status**: 🔴 SIGNIFICANT DIFFERENCES - Nillipuss has much richer group display
- **Priority**: MEDIUM (affects raid/group gameplay, not as common as solo play)

---

## Key Differences

### Nillipuss Features (EQType-verified)
Nillipuss expands the group display with **multi-layer HP gauges** while keeping the same EQType data bindings:

- **Group Member HP**: EQTypes **11–15** (multiple layered gauges per member)
- **Group Pet HP**: EQTypes **17–21**
- **Group HP Labels**: EQTypes **35–39**

The extra line count is primarily due to layered gauge implementations (`Party*_HP_*` variants) rather than new data fields.

### Thorne Implementation (EQType-verified)
- Single-layer group HP gauges (EQTypes **11–15**)
- Pet HP gauges (EQTypes **17–21**)
- HP labels (EQTypes **35–39**)
- Clean, minimal implementation with fewer layers

### Hidden/Unreferenced EQType Elements (Nillipuss)
The following labels are defined but **not referenced by any Screen/Page pieces**:
`Level` (Label, **2**), `Class` (Label, **3**), `Deity` (Label, **4**), `PlayerHP` (Label, **70**), `PlayerMana` (Label, **128**).

---

## v0.8.0+ Recommendation

**Complexity**: MEDIUM-HIGH
**Value**: MEDIUM (not as essential as solo content features)
**Estimated Effort**: 10-15 hours

**Action**: Detailed analysis deferred to v0.8.0 planning phase. Monitor community requests about group window features to prioritize accordingly.

---

## Notes

- File size suggests Nillipuss version has significantly more sophistication
- Would need element-by-element comparison to identify specific features
- Good candidate for later enhancement if raid/group players request improvements
