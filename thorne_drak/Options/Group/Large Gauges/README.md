# Group Window - Large Gauges Variant

**File**: [EQUI_GroupWindow.xml](./EQUI_GroupWindow.xml)  
**Version**: N/A  
**Last Updated**: 2026-02-03
**Status**: ⚠️ Placeholder variant (XML stub copied from Standard)  
**Author**: Draknare Thorne

---
## Purpose

**Important Note**: This variant directory now contains a **stub XML** copied from the Standard variant so the Options checker is clean. It is **not yet the Large Gauges design**.

**Intended Purpose** (based on variant name):

The Large Gauges variant would feature enlarged HP/Mana gauges for improved visibility during group play, particularly useful for:
- **Raid Healing**: Larger gauges easier to monitor at a distance
- **Main Tank Monitoring**: Enhanced visibility of group member health status
- **Accessibility**: Better readability for players with vision considerations
- **Multi-Monitor Setups**: Larger gauges scale better on high-resolution displays

---

## Current Status

⚠️ **Stub Implementation File**

This directory contains a **copy of Standard** `EQUI_GroupWindow.xml` as a placeholder until large gauges are designed.

**What This Means**:
- This variant **cannot currently be installed**
- The variant is either:
  - **Planned but not yet created**
  - **Moved to main directory** (main `thorne_drak/EQUI_GroupWindow.xml` may be the "large gauge" version)
  - **Deprecated** in favor of other variants

---

## Key Features

**Key Features**:

**Planned Features (not yet implemented)**:

- Enlarged group member HP/Mana gauges for improved visibility
- Increased vertical spacing for clarity in raids
- Larger text labels for name/HP% readability

**Current Stub Behavior**:

- Identical to Standard Group window until the large gauge layout is designed

---

## Specifications

**Planned (Target)**:

| Property | Expected Value |
|----------|----------------|
| Gauge Height | 32–40px (Standard: 24px) |
| Window Width | 170–190px (Standard: 160px) |
| Window Height | 210–240px (Standard: 170px) |
| Gauge Width | 114–130px |
| Member Count | 5 (F2–F6) |

**Current Stub**:

| Property | Value |
|----------|-------|
| Gauge Height | 24px (Standard) |
| Window Width | 160px (Standard) |
| Window Height | 170px (Standard) |

---

## Layout Overview (Planned)

```text
GroupWindow (180×230 approx)
├── GW_Gauge1 (Member 1)  ── HP/Mana bars (larger height)
├── GW_Gauge2 (Member 2)
├── GW_Gauge3 (Member 3)
├── GW_Gauge4 (Member 4)
└── GW_Gauge5 (Member 5)

Each member row increases vertical spacing to prevent overlap.
```

### Spacing Targets

- **Row height**: 40–44px (Standard: ~30–32px)
- **Gauge height**: 32–40px (Standard: 24px)
- **Name label**: same font size, larger vertical padding

---

## Element Inventory (Stub vs Planned)

| Element | Standard | Planned Large Gauges | Notes |
|---------|----------|----------------------|-------|
| GW_Gauge1–5 | 114×24 | 114×32–40 | Increase height, adjust Y positions |
| GW_Name1–5 | 70×12 | 70×12 | Same font, more padding |
| GW_Level1–5 | 24×12 | 24×12 | Same size |
| GW_PetGauge1–5 | 114×12 | 114×16–20 | Optional enlargement |

---

## Comparison to Standard (What Changes)

| Area | Standard | Large Gauges (Planned) |
|------|----------|-------------------------|
| Overall Height | ~170px | ~210–240px |
| Gauge Height | 24px | 32–40px |
| Vertical Spacing | Tight | Relaxed |
| Readability | Medium | High |
| Screen Footprint | Small | Medium |

---

## Implementation Notes (Planned)

1. **Increase gauge height** for GW_Gauge1–5.
2. **Adjust Y positions** for each row to avoid overlap.
3. **Update window height** to accommodate larger rows.
4. **Evaluate pet gauge visibility** (optional larger pet gauge).
5. **Test in raids** for legibility and spacing comfort.

---

## Testing Checklist (Once Implemented)

- [ ] `/loadskin thorne_drak 1`
- [ ] Verify all 5 member bars render
- [ ] Confirm text labels are aligned and readable
- [ ] Ensure no overlap at 1920×1080
- [ ] Validate pet gauges (if enabled)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-10 | Stub XML copied from Standard; documentation expanded |

---

## Expected Specifications (If Implemented)

Based on the "Large Gauges" name and comparison to the Standard variant, this version would likely feature:

| Property | Expected Value |
|----------|----------------|
| Gauge Height | Larger than Standard (Standard: 24px) - likely 32-40px |
| Window Width | 160-180 pixels (may increase to accommodate larger gauges) |
| Window Height | Increased proportionally (Standard: 170px) - likely 200-240px |
| Gauge Width | 114px (likely maintained) or expanded to 130-140px |
| Member Count | 5 members (F2-F6, same as Standard) |
| Resizable | No (fixed size) |

---

## Comparison to Standard Variant

**Standard Variant** ([see Standard README](../Standard/README.md)):
- Window Size: 160 × 170 pixels
- Gauge Size: 114 × 24 pixels (HP gauges)
- Compact design for minimal screen footprint

**Large Gauges Variant** (expected):
- Window Size: ~180 × 230 pixels (estimated)
- Gauge Size: ~130 × 36 pixels (estimated)
- Enhanced visibility at the cost of screen space

---

## Creating This Variant

If you wish to create the "Large Gauges" variant:

### Steps:

1. **Copy Standard Variant**:
   ```bash
   cp "../Standard/EQUI_GroupWindow.xml" "EQUI_GroupWindow.xml"
   ```

2. **Edit Gauge Sizes** in the new file:
   - Locate `<Gauge item="GW_Gauge1">` through `GW_Gauge5`
   - Increase `<CY>` (height) from 24 to desired size (e.g., 36 or 40)
   - Optionally increase `<CX>` (width) from 114 to desired size

3. **Adjust Window Size**:
   - Locate `<Screen item="GroupWindow">`
   - Increase `<CY>` (window height) proportionally to accommodate larger gauges
   - Formula: New Height = Old Height + (Gauge Height Increase × 5 members)
   - Example: If gauges increase by 12px, add 60px to window height (170 + 60 = 230)

4. **Adjust Element Y-Positions**:
   - Each member slot's Y-position must increase to prevent overlap
   - Space gauges further apart vertically

5. **Test in-game**:
   - Copy to main `thorne_drak/` directory
   - Run `/loadskin thorne_drak`
   - Verify gauges display correctly without overlap

---

## Alternative: Use Main Directory File

The main `thorne_drak/EQUI_GroupWindow.xml` file may already be the "large gauge" version. To check:

1. Compare gauge sizes in `thorne_drak/EQUI_GroupWindow.xml` vs `Options/Group/Standard/EQUI_GroupWindow.xml`
2. If main file has larger gauges, it may serve as this variant
3. The "Standard" variant would then be the compact alternative

---

## Installation

**Currently Not Possible**: No XML file exists to install.

**Once Updated**:
1. Replace `EQUI_GroupWindow.xml` with the large gauge variant
2. Copy to `thorne_drak/` directory
3. Run `/loadskin thorne_drak` in-game

## Reverting

To use the Standard variant instead:
- Copy from `Options/Group/Standard/EQUI_GroupWindow.xml`

---

**Part of**: [Thorne UI](../../../../README.md)  
**Standards**: [Development Standards](../../../../.docs/STANDARDS.md)  
**Related Variants**: [Standard](../Standard/README.md)  
**Status**: ⚠️ Placeholder - XML file not yet implemented
