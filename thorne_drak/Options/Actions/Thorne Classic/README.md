# Window: Actions - Thorne Classic Variant

**File**: [EQUI_ActionsWindow.xml](./EQUI_ActionsWindow.xml)  
**Version**: 0.8.0  
**Last Updated**: 2026-02-10  
**Status**: ✅ Active  
**Author**: Draknare Thorne

---

## Purpose

The Thorne Classic Actions Window variant organizes the Actions interface using a **dual-TabBox layout**:
one TabBox for the five action pages (Info, Main, Abilities, Combat, Socials) and a second TabBox
for two equipment/inventory pages. This replaces the main variant's inline equipment layout with a
more compact tabbed approach.

**Key Features**:

- **Dual TabBox System**: Separate tab groups for actions (5 tabs) and equipment (2 tabs)
- **Compact Window**: 160×188px with no titlebar — minimal screen footprint
- **Social Button Grid**: 12 social buttons (2×6 grid) with page navigation arrows
- **Equipment Tabs**: Bags (EQType 22-29), weapons (Primary, Secondary, Range), and full armor set across two paginated tabs

**Key Differentiator from Main**: The main variant uses an inline equipment layout with rows
(LEar, Face, Head, REar, etc.). This Classic variant consolidates equipment into a separate
tabbed section below the action tabs.

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 160 × 188 pixels |
| Resizable | No (`Style_Sizable=false`) |
| Titlebar | No (`Style_Titlebar=false`) |
| Closebox | Yes |
| Minimizebox | No |
| Border | Yes |
| DrawTemplate | WDT_RoundedNoTitle |
| Default Position | X=516, Y=292 |
| Actions TabBox | ACTW_ActionsSubwindows (145×170px) |
| Actions Tab Count | 5 (Info, Main, Abilities, Combat, Socials) |
| Inventory TabBox | ACTW_InventorySubwindows (145×203px) |
| Inventory Tab Count | 2 (Equipment Page 1, Equipment Page 2) |
| Social Buttons | 12 per page (2 columns × 6 rows) |
| Social Button Size | 64 × 20 pixels |
| Equipment Slot Size | 44 × 44 pixels |

---

## Layout Overview

### Window Structure

```text
ActionsWindow (160×188px, no titlebar)
├── ACTW_ActionsSubwindows TabBox (145×170px, Y=8)
│   ├── ActionsInfoPage
│   ├── ActionsMainPage
│   ├── ActionsAbilitiesPage
│   ├── ActionsCombatPage
│   └── ActionsSocialsPage
│       ├── Page navigation: Left/Right arrows + page label
│       └── Social buttons 1-12 (2×6 grid)
│
└── ACTW_InventorySubwindows TabBox (145×203px, Y=180)
    ├── ActionsEquipmentPage1 (Bags + Weapons)
    │   ├── Primary (EQType 13), Range (EQType 11)
    │   └── Bag slots 22-29 (EQTypes 22-29)
    └── ActionsEquipmentPage2 (Armor)
```

### Socials Tab Layout

```text
┌─────────────────────────────────────┐
│ [◄]  Page#  [►]                     │  Navigation (Y=0-15)
├─────────────────────────────────────┤
│ [Social 1 ] [Social 7 ]            │  Y=20   (X=7, X=74)
│ [Social 2 ] [Social 8 ]            │  Y=40
│ [Social 3 ] [Social 9 ]            │  Y=60
│ [Social 4 ] [Social 10]            │  Y=80
│ [Social 5 ] [Social 11]            │  Y=100
│ [Social 6 ] [Social 12]            │  Y=120
└─────────────────────────────────────┘
```

---

## Element Inventory

### Social Page Navigation

| Element | ScreenID | Position | Size |
|---------|----------|----------|------|
| Page Left | ASP_SocialPageLeftButton | (16, 3) | 22×12px |
| Page Label | ASP_CurrentSocialPageLabel | (50, 1) | 36×22px |
| Page Right | ASP_SocialPageRightButton | (97, 3) | 22×12px |

### Social Buttons (2×6 Grid)

| Button | ScreenID | Position | Size |
|--------|----------|----------|------|
| Social 1 | ASP_SocialButton1 | (7, 20) | 64×20px |
| Social 2 | ASP_SocialButton2 | (7, 40) | 64×20px |
| Social 3 | ASP_SocialButton3 | (7, 60) | 64×20px |
| Social 4 | ASP_SocialButton4 | (7, 80) | 64×20px |
| Social 5 | ASP_SocialButton5 | (7, 100) | 64×20px |
| Social 6 | ASP_SocialButton6 | (7, 120) | 64×20px |
| Social 7 | ASP_SocialButton7 | (74, 20) | 64×20px |
| Social 8 | ASP_SocialButton8 | (74, 40) | 64×20px |
| Social 9 | ASP_SocialButton9 | (74, 60) | 64×20px |
| Social 10 | ASP_SocialButton10 | (74, 80) | 64×20px |
| Social 11 | ASP_SocialButton11 | (74, 100) | 64×20px |
| Social 12 | ASP_SocialButton12 | (74, 120) | 64×20px |

### Equipment Slots (Page 1 — Bags + Weapons)

| Slot | ScreenID | EQType | Size |
|------|----------|--------|------|
| Primary | ACTW_Primary | 13 | 44×44px |
| Range | ACTW_Range | 11 | 44×44px |
| Bag 1 | ACTW_BagSlot22 | 22 | 44×44px |
| Bag 2 | ACTW_BagSlot23 | 23 | 44×44px |
| Bag 3 | ACTW_BagSlot24 | 24 | 44×44px |
| Bag 4 | ACTW_BagSlot25 | 25 | 44×44px |
| Bag 5 | ACTW_BagSlot26 | 26 | 44×44px |
| Bag 6 | ACTW_BagSlot27 | 27 | 44×44px |
| Bag 7 | ACTW_BagSlot28 | 28 | 44×44px |
| Bag 8 | ACTW_BagSlot29 | 29 | 44×44px |

---

## Design Notes

The dual-TabBox approach uses `FT_DefTabBorder` and `FT_DefPageBorder` templates for both
tab groups. The Actions TabBox sits at Y=8 with the Inventory TabBox directly below at Y=180,
creating a vertically stacked dual-purpose window within the compact 160×188px frame.

Social buttons use `RelativePosition=true` with 20px vertical intervals. Left column buttons
(1-6) are at X=7, right column (7-12) at X=74, each 64×20px.

---

## Known Limitations

- **Buttons 11-30**: Client hardcoding prevents these from functioning (P2002 limitation)
- **No Titlebar**: Window uses close button only — no drag-by-title (drag by content area)
- **Tab switching**: Managed by the EQ client TabBox system; no custom behavior

---

## Cross-References

- **Main Variant**: `thorne_drak/EQUI_ActionsWindow.xml` — inline equipment layout (no equipment tabs)
- **EQTYPES.md**: See `.docs/technical/EQTYPES.md` for InvSlot EQType mappings
- **STANDARDS.md**: See `.docs/STANDARDS.md` for window sizing and layout conventions
