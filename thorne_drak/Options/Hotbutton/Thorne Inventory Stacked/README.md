# Window: Hotbutton - Thorne Inventory Stacked Variant

**File**: [EQUI_HotButtonWnd.xml](./EQUI_HotButtonWnd.xml)  
**Version**: 0.8.0  
**Last Updated**: 2026-02-10  
**Status**: ✅ Active  
**Author**: Draknare Thorne  
**Based On**: Original by Daciana, tweaked by Brujoloco (QQQuarm)

---

## Purpose

The Thorne Inventory Stacked variant combines a standard 10-button hotbar with a full equipment
and inventory slot display in a single 4-row window. All 21 equipment slots plus 8 bag slots are
visible alongside the hotbar, giving players an at-a-glance view of their gear without opening
the Inventory window.

**Key Features**:

- **4-Row Layout**: Row 1 is standard hotbar; Rows 2-4 display all equipment + bag InvSlots
- **Full Equipment Display**: All 21 equipment slots (EQTypes 0-21) across rows 3-4
- **Bag Slot Access**: Primary, Secondary, and Bags 1-8 (EQTypes 13-14, 22-29) in row 2
- **10 Spell Gems**: Integrated spell gem display (HB_SpellGem1-10)
- **Page Navigation**: Left/Right page buttons with page label
- **Always Visible**: HotButtonWnd is non-fadeable — immune to transparency

**Key Differentiator from Main**: The main variant also uses a 4-row hybrid layout, but this
"Inventory Stacked" variant arranges equipment slots in an anatomical equipment order across
rows 2-4 with labeled button overlays showing slot names (Primary, LEar, Waist, etc.).

---

## Specifications

| Property | Value |
|----------|-------|
| Window Size | 440 × 178 pixels |
| Resizable | Yes (`Style_Sizable=true`) |
| Titlebar | Yes — "Hot Buttons" |
| Closebox | Yes |
| Minimizebox | No |
| Border | Yes |
| DrawTemplate | WDT_Rounded |
| Default Position | X=0, Y=230 |
| Fadeable | No (non-fadeable window type) |
| Hotbutton Count | 10 (Row 1 only — HB_Button1-10) |
| Equipment Slots | 30 InvSlots across Rows 2-4 |
| Spell Gems | 10 (HB_SpellGem1-10) |
| Button Size | 40 × 40 pixels |
| Button Spacing | 42px horizontal (40px + 2px gap) |
| Row Spacing | 44px vertical |

---

## Layout Overview

### Window Structure

```text
HotButtonWnd (440×178px)
├── Page Navigation: [◄] Page# [►]  (X=420, Y=2)
│
├── Row 1 (Y=2): Standard Hotbar
│   └── HB_Button1-10 (labeled 1-10) + HB_InvSlot1-10 (EQType -1)
│
├── Spell Gems: HB_SpellGem1-10
│
├── Row 2 (Y=46): Weapons + Bags
│   └── Primary, Secondary, Bag1-Bag8
│
├── Row 3 (Y=90): Head/Upper Body Equipment
│   └── LEar, Head, Face, REar, Neck, Shoulder, Chest, Arms, Hands, Back
│
└── Row 4 (Y=134): Lower Body Equipment
    └── Waist, Legs, Feet, LWrist, RWrist, LFinger, RFinger, Range, Ammo, Charm
```

---

## Element Inventory

### Row 1 — Standard Hotbar (Y=2)

| Col | Button | ScreenID | X | Label | InvSlot EQType |
|-----|--------|----------|---|-------|----------------|
| 1 | HB_Button1 | HB_Button1 | 2 | 1 | -1 |
| 2 | HB_Button2 | HB_Button2 | 44 | 2 | -1 |
| 3 | HB_Button3 | HB_Button3 | 86 | 3 | -1 |
| 4 | HB_Button4 | HB_Button4 | 128 | 4 | -1 |
| 5 | HB_Button5 | HB_Button5 | 170 | 5 | -1 |
| 6 | HB_Button6 | HB_Button6 | 212 | 6 | -1 |
| 7 | HB_Button7 | HB_Button7 | 254 | 7 | -1 |
| 8 | HB_Button8 | HB_Button8 | 296 | 8 | -1 |
| 9 | HB_Button9 | HB_Button9 | 338 | 9 | -1 |
| 10 | HB_Button10 | HB_Button10 | 380 | 10 | -1 |

### Row 2 — Weapons + Bags (Y=46)

| Col | Label | ScreenID | EQType | Slot |
|-----|-------|----------|--------|------|
| 1 | Primary | HB2_Button1 / HB2_InvSlot1 | 13 | Primary weapon |
| 2 | Secondary | HB2_Button2 / HB2_InvSlot2 | 14 | Secondary weapon |
| 3 | Bag1 | HB2_Button3 / HB2_InvSlot3 | 22 | Bag slot 1 |
| 4 | Bag2 | HB2_Button4 / HB2_InvSlot4 | 23 | Bag slot 2 |
| 5 | Bag3 | HB2_Button5 / HB2_InvSlot5 | 24 | Bag slot 3 |
| 6 | Bag4 | HB2_Button6 / HB2_InvSlot6 | 25 | Bag slot 4 |
| 7 | Bag5 | HB2_Button7 / HB2_InvSlot7 | 26 | Bag slot 5 |
| 8 | Bag6 | HB2_Button8 / HB2_InvSlot8 | 27 | Bag slot 6 |
| 9 | Bag7 | HB2_Button9 / HB2_InvSlot9 | 28 | Bag slot 7 |
| 10 | Bag8 | HB2_Button10 / HB2_InvSlot10 | 29 | Bag slot 8 |

### Row 3 — Head/Upper Body (Y=90)

| Col | Label | ScreenID | EQType | Slot |
|-----|-------|----------|--------|------|
| 1 | LEar | HB3_Button1 / HB3_InvSlot1 | 1 | Left Ear |
| 2 | Head | HB3_Button2 / HB3_InvSlot2 | 2 | Head |
| 3 | Face | HB3_Button3 / HB3_InvSlot3 | 3 | Face |
| 4 | REar | HB3_Button4 / HB3_InvSlot4 | 4 | Right Ear |
| 5 | Neck | HB3_Button5 / HB3_InvSlot5 | 5 | Neck |
| 6 | Shoulder | HB3_Button6 / HB3_InvSlot6 | 6 | Shoulders |
| 7 | Chest | HB3_Button7 / HB3_InvSlot7 | 17 | Chest |
| 8 | Arms | HB3_Button8 / HB3_InvSlot8 | 7 | Arms |
| 9 | Hands | HB3_Button9 / HB3_InvSlot9 | 12 | Hands |
| 10 | Back | HB3_Button10 / HB3_InvSlot10 | 8 | Back |

### Row 4 — Lower Body (Y=134)

| Col | Label | ScreenID | EQType | Slot |
|-----|-------|----------|--------|------|
| 1 | Waist | HB4_Button1 / HB4_InvSlot1 | 20 | Waist |
| 2 | Legs | HB4_Button2 / HB4_InvSlot2 | 18 | Legs |
| 3 | Feet | HB4_Button3 / HB4_InvSlot3 | 19 | Feet |
| 4 | LWrist | HB4_Button4 / HB4_InvSlot4 | 9 | Left Wrist |
| 5 | RWrist | HB4_Button5 / HB4_InvSlot5 | 10 | Right Wrist |
| 6 | LFinger | HB4_Button6 / HB4_InvSlot6 | 15 | Left Finger |
| 7 | RFinger | HB4_Button7 / HB4_InvSlot7 | 16 | Right Finger |
| 8 | Range | HB4_Button8 / HB4_InvSlot8 | 11 | Range |
| 9 | Ammo | HB4_Button9 / HB4_InvSlot9 | 21 | Ammo |
| 10 | Charm | HB4_Button10 / HB4_InvSlot10 | 0 | Charm |

### Page Navigation

| Element | ScreenID | Position | Size |
|---------|----------|----------|------|
| Page Left | HB_PageLeftButton | (420, 2) | 12×10px |
| Page Label | HB_CurrentPageLabel | — | — |
| Page Right | HB_PageRightButton | — | — |

---

## Design Notes

Each equipment slot uses a **Button + InvSlot overlay** pattern: the Button provides a text
label (e.g., "LEar", "Bag3") while the InvSlot at the same position handles item display and
interaction. Both share identical X/Y coordinates and 40×40px size.

Row 1 InvSlots use `EQType=-1` (unused/placeholder) since they serve as standard hotbar positions.

---

## Known Limitations

- **Buttons 11-30**: Client hardcoding prevents these from functioning (P2002 limitation).
  Only Row 1 buttons (1-10) execute hotbar actions.
- **Non-fadeable**: HotButtonWnd cannot be made transparent — always fully visible.
  This is a benefit for combat but may occlude other windows.

---

## Cross-References

- **Main Variant**: `thorne_drak/EQUI_HotButtonWnd.xml` — similar 4-row hybrid layout
- **EQTYPES.md**: See `.docs/technical/EQTYPES.md` for InvSlot EQType mappings
- **STANDARDS.md**: See `.docs/STANDARDS.md` for window sizing and layout conventions
