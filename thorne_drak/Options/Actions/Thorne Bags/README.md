# Actions Window - Bags and Inventory Variant

**File**: [EQUI_ActionsWindow.xml](./EQUI_ActionsWindow.xml)
**Version**: 1.1.1 (documentation update)  
**Last Updated**: January 24, 2026  
**Status**: ✅ Up-to-date with XML content
**Author**: Draknare Thorne

---
## Purpose

The Actions window provides core player actions, a four-tab actions interface, a dedicated inventory tab system, and a compact player stats area. This variant emphasizes dual-column layout with side-by-side inventory and action management.

**Key Features**:

- **Dual-Column Layout**: Actions panel on left (4 tabs) with Inventory on right (2 tabs)
- **Actions TabBox**: Main, Abilities, Combat, and Socials tabs for quick ability access
- **Inventory TabBox**: Separate Bags and Worn equipment display tabs
- **Compact Stats**: Integrated player name, level, HP, and Mana display at bottom
- **Side-by-Side Access**: Manage actions and inventory simultaneously without tab switching
- **Fixed Size**: 160×394px non-resizable window optimized for side-by-side layout

---

## Specifications

| Property | Value |
| ---------- | ------- |
| Window Size | 160 × 394 px |
| Resizable | ❌ No (`Style_Sizable=false`) |
| Screen item | `ActionsWindow` |
| Actions tabs | 4 (Main, Abilities, Combat, Socials) |
| Inventory tabs | 2 (Bags, Worn) |

---

## Layout Overview

```text
ActionsWindow (160×394)
├─ TabBox: ACTW_ActionsSubwindows (left)
│  ├─ ActionsMainPage
│  ├─ ActionsAbilitiesPage
│  ├─ ActionsCombatPage
│  └─ ActionsSocialsPage
├─ TabBox: ACTW_InventorySubwindows (right)
│  ├─ ActionsEquipmentPage1 (Bags)
│  └─ ActionsEquipmentPage2 (Worn)
└─ Player Stats: Name, Level, HP, Mana (bottom)
```

Color cues:

- Stat labels: blue accents
- Stat values: white
- HP/Mana values: tinted (HP red, Mana blue)

---

## Actions tabs (left)

### Main Page — `ActionsMainPage`

Buttons present in XML:

- Group controls (defined, currently size 0×0):
  - `AMP_WhoButton`, `AMP_InviteButton`, `AMP_FollowButton`, `AMP_DisbandButton`
- Movement/stance (full-size, shared/toggled positions):
  - `AMP_CampButton` at X=1, Y=86, Size=134×20
  - `AMP_SitButton` and `AMP_StandButton` share X=1, Y=105, Size=134×20 (only one shown based on state)
  - `AMP_RunButton` and `AMP_WalkButton` share ~X=1, Y≈124, Size=134×20 (only one shown based on mode)

Displayed player attributes (labels and values):

- STR, STA, AGI, DEX, WIS, INT (labels + values)
- ATK, AC (labels + values)
- Resist labels + values: MAGIC, FIRE, COLD, DISEASE, POISON

### Abilities Page — `ActionsAbilitiesPage`

- Six square ability buttons: `AAP_FirstAbilityButton` … `AAP_SixthAbilityButton` (labeled 1–6)

### Combat Page — `ActionsCombatPage`

- `ACP_MeleeAttackButton`, `ACP_RangeAttackButton`
- Ability buttons: `ACP_FirstAbilityButton` … `ACP_FourthAbilityButton` (labeled 1–4)

### Socials Page — `ActionsSocialsPage`

- Page selector: `ASP_SocialPageLeftButton`, `ASP_SocialPageRightButton`, `ASP_CurrentSocialPageLabel`
- Twelve social buttons: `ASP_SocialButton1` … `ASP_SocialButton12`

---

## Inventory tabs (right)

### Bags — `ActionsEquipmentPage1`

Slots:

- Bags: Inv slots EQType 22–29 (`ACTW_BagSlot22` … `ACTW_BagSlot29`)
- Weapons/utility: `ACTW_Primary` (EQType 13), `ACTW_Secondary` (14), `ACTW_Range` (11), `ACTW_Ammo` (21)

### Worn — `ActionsEquipmentPage2`

Slots:

- Ears: `ACTW_LEar` (1), `ACTW_REar` (4)
- Head: `ACTW_Head` (2)
- Face: `ACTW_Face` (3)
- Neck: `ACTW_Neck` (5)
- Shoulders: `ACTW_Shoulders` (6)
- Arms: `ACTW_Arms` (7)
- Chest: `ACTW_Chest` (17)
- About Body (cloak): `ACTW_AboutBody` (8)
- Waist: `ACTW_Waist` (20)
- Wrists: `ACTW_LWrist` (9), `ACTW_RWrist` (10)
- Hands: `ACTW_Hands` (12)
- Rings: `ACTW_LRing` (15), `ACTW_RRing` (16)
- Legs: `ACTW_Legs` (18)
- Feet: `ACTW_Feet` (19)

---

## Player stats (bottom of window)

Labels: `ACTW_PlayerName` (EQType 1), `ACTW_Level` (2)

Values (combined current/max):

- HP: `ACTW_CurrentHP` (EQType 70) — red tint
- Mana: `ACTW_CurrentMana` (EQType 80) — blue tint

---

## Element Inventory - Dual-Column Layout

### Actions TabBox (Left Column @ X=1, Y=1)

| Page | Element | Position | Size (px) | EQType | Function |
|------|---------|----------|-----------|--------|----------|
| Main | STR Label | X=5, Y=1 | 25×12 | N/A | "STR" text |
| Main | STR Value | X=32, Y=1 | 30×14 | 5 | Strength numeric |
| Main | STA Label | X=5, Y=15 | 25×12 | N/A | "STA" text |
| Main | STA Value | X=32, Y=15 | 30×14 | 6 | Stamina numeric |
| Main | AGI Label | X=5, Y=29 | 25×12 | N/A | "AGI" text |
| Main | AGI Value | X=32, Y=29 | 30×14 | 7 | Agility numeric |
| Main | DEX Label | X=5, Y=43 | 25×12 | N/A | "DEX" text |
| Main | DEX Value | X=32, Y=43 | 30×14 | 8 | Dexterity numeric |
| Main | WIS Label | X=5, Y=57 | 25×12 | N/A | "WIS" text |
| Main | WIS Value | X=32, Y=57 | 30×14 | 9 | Wisdom numeric |
| Main | INT Label | X=5, Y=71 | 25×12 | N/A | "INT" text |
| Main | INT Value | X=32, Y=71 | 30×14 | 10 | Intelligence numeric |
| Main | AC Label | X=5, Y=85 | 20×12 | N/A | "AC" text |
| Main | AC Value | X=32, Y=85 | 30×14 | 22 | Armor Class numeric |
| Main | ATK Label | X=5, Y=99 | 22×12 | N/A | "ATK" text |
| Main | ATK Value | X=32, Y=99 | 30×14 | 23 | Attack rating numeric |
| Main | CampButton | X=1, Y=113 | 134×20 | N/A | Camp/rest command |
| Main | Sit/Stand Button | X=1, Y=133 | 134×20 | N/A | Toggle sit/stand pose |
| Main | Run/Walk Button | X=1, Y=153 | 134×20 | N/A | Toggle run/walk mode |
| Abilities | Ability 1 | X=5, Y=10 | 40×40 | N/A | Ability slot 1 |
| Abilities | Ability 2 | X=90, Y=10 | 40×40 | N/A | Ability slot 2 |
| Abilities | Ability 3 | X=5, Y=60 | 40×40 | N/A | Ability slot 3 |
| Abilities | Ability 4 | X=90, Y=60 | 40×40 | N/A | Ability slot 4 |
| Abilities | Ability 5 | X=5, Y=110 | 40×40 | N/A | Ability slot 5 |
| Abilities | Ability 6 | X=90, Y=110 | 40×40 | N/A | Ability slot 6 |
| Combat | Melee Attack | X=5, Y=10 | 40×40 | N/A | Melee attack trigger |
| Combat | Range Attack | X=90, Y=10 | 40×40 | N/A | Ranged attack trigger |
| Combat | Ability 1 | X=5, Y=60 | 40×40 | N/A | Combat ability 1 |
| Combat | Ability 2 | X=90, Y=60 | 40×40 | N/A | Combat ability 2 |
| Combat | Ability 3 | X=5, Y=110 | 40×40 | N/A | Combat ability 3 |
| Combat | Ability 4 | X=90, Y=110 | 40×40 | N/A | Combat ability 4 |
| Socials | Page Left | X=15, Y=10 | 20×20 | N/A | Previous page |
| Socials | Page Right | X=120, Y=10 | 20×20 | N/A | Next page |
| Socials | Page Indicator | X=40, Y=10 | 80×20 | N/A | Current page number display |
| Socials | Social Button 1 | X=1, Y=35 | 32×32 | N/A | Social macro slot 1 |
| Socials | Social Button 2 | X=48, Y=35 | 32×32 | N/A | Social macro slot 2 |
| Socials | Social Button 3 | X=96, Y=35 | 32×32 | N/A | Social macro slot 3 |
| Socials | Social Button 4 | X=1, Y=70 | 32×32 | N/A | Social macro slot 4 |
| Socials | Social Button 5 | X=48, Y=70 | 32×32 | N/A | Social macro slot 5 |
| Socials | Social Button 6 | X=96, Y=70 | 32×32 | N/A | Social macro slot 6 |
| Socials | Social Button 7 | X=1, Y=105 | 32×32 | N/A | Social macro slot 7 |
| Socials | Social Button 8 | X=48, Y=105 | 32×32 | N/A | Social macro slot 8 |
| Socials | Social Button 9 | X=96, Y=105 | 32×32 | N/A | Social macro slot 9 |
| Socials | Social Button 10 | X=1, Y=140 | 32×32 | N/A | Social macro slot 10 |
| Socials | Social Button 11 | X=48, Y=140 | 32×32 | N/A | Social macro slot 11 |
| Socials | Social Button 12 | X=96, Y=140 | 32×32 | N/A | Social macro slot 12 |

### Inventory TabBox (Right Column @ X=77, Y=1)

| Page | Element | Slot | Position | Size (px) | EQType | Function |
|------|---------|------|----------|-----------|--------|----------|
| Bags | Primary Weapon | Eq-13 | X=2, Y=2 | 44×44 | 13 | Main hand weapon |
| Bags | Secondary Weapon | Eq-14 | X=2, Y=54 | 44×44 | 14 | Off-hand weapon/shield |
| Bags | Ranged Weapon | Eq-11 | X=2, Y=106 | 44×44 | 11 | Bow/crossbow |
| Bags | Ammo | Eq-21 | X=2, Y=158 | 44×44 | 21 | Arrow/bolt/throwing stars |
| Bags | Bag Slot 22 | Inv-22 | X=2, Y=210 | 44×44 | 22 | Pack 1 |
| Bags | Bag Slot 23 | Inv-23 | X=54, Y=210 | 44×44 | 23 | Pack 2 |
| Bags | Bag Slot 24 | Inv-24 | X=2, Y=262 | 44×44 | 24 | Pack 3 |
| Bags | Bag Slot 25 | Inv-25 | X=54, Y=262 | 44×44 | 25 | Pack 4 |
| Bags | Bag Slot 26 | Inv-26 | X=2, Y=314 | 44×44 | 26 | Pack 5 |
| Bags | Bag Slot 27 | Inv-27 | X=54, Y=314 | 44×44 | 27 | Pack 6 |
| Bags | Bag Slot 28 | Inv-28 | X=2, Y=366 | 44×44 | 28 | Pack 7 (bottom-left) |
| Bags | Bag Slot 29 | Inv-29 | X=54, Y=366 | 44×44 | 29 | Pack 8 (bottom-right) |
| Worn | Head | Eq-2 | X=20, Y=2 | 36×36 | 2 | Head armor |
| Worn | Left Ear | Eq-1 | X=2, Y=42 | 36×36 | 1 | Left earring |
| Worn | Right Ear | Eq-4 | X=38, Y=42 | 36×36 | 4 | Right earring |
| Worn | Face | Eq-3 | X=20, Y=42 | 36×36 | 3 | Goggles/mask |
| Worn | Neck | Eq-5 | X=20, Y=82 | 36×36 | 5 | Necklace |
| Worn | Shoulders | Eq-6 | X=2, Y=122 | 36×36 | 6 | Shoulder armor |
| Worn | About Body | Eq-8 | X=38, Y=122 | 36×36 | 8 | Cloak/back slot |
| Worn | Arms | Eq-7 | X=20, Y=122 | 36×36 | 7 | Arms/sleeves |
| Worn | Left Wrist | Eq-9 | X=2, Y=162 | 36×36 | 9 | Left bracer |
| Worn | Right Wrist | Eq-10 | X=38, Y=162 | 36×36 | 10 | Right bracer |
| Worn | Hands | Eq-12 | X=20, Y=162 | 36×36 | 12 | Gloves |
| Worn | Chest | Eq-17 | X=20, Y=202 | 36×36 | 17 | Breastplate |
| Worn | Waist | Eq-20 | X=20, Y=242 | 36×36 | 20 | Belt/girdle |
| Worn | Left Ring | Eq-15 | X=2, Y=282 | 36×36 | 15 | Left ring |
| Worn | Right Ring | Eq-16 | X=38, Y=282 | 36×36 | 16 | Right ring |
| Worn | Legs | Eq-18 | X=20, Y=282 | 36×36 | 18 | Pants/leggings |
| Worn | Feet | Eq-19 | X=20, Y=322 | 36×36 | 19 | Boots |

### Player Stats (Bottom @ Y=370-390)

| Element | Position | Size (px) | EQType | Function |
|---------|----------|-----------|--------|----------|
| Player Name Label | X=2, Y=370 | 70×12 | 1 | Character name (blue) |
| Level Label | X=80, Y=370 | 30×12 | 2 | Character level (blue) |
| HP Current | X=2, Y=383 | 40×12 | 70 | Current HP (red-tinted) |
| HP Max | X=44, Y=383 | 30×12 | 70 | Max HP display |
| Mana Current | X=100, Y=383 | 40×12 | 80 | Current Mana (blue-tinted) |
| Mana Max | X=142, Y=383 | 30×12 | 80 | Max Mana display |

---

## Variant Comparison - Actions Window Layouts

| Feature | Standard | Bags & Inventory |
|---------|----------|------------------|
| **Window Size** | Fixed (no explicit sizing) | 160×394 px (fixed) |
| **Resizable** | No | No |
| **Tab Organization** | Vertical (5+2 pages stacked) | Side-by-side dual-column (4+2) |
| **Actions Pages** | 5 (Info/Main/Abilities/Combat/Socials) | 4 (Main/Abilities/Combat/Socials, no Info) |
| **Inventory Access** | Below actions (sequential switching) | Right column (always visible) |
| **Stat Display** | Full on Main & Info pages | Compact at bottom (Name/Level/HP/Mana) |
| **Layout Priority** | Actions primary, Inventory secondary | Dual-priority layout |
| **Typical Usage** | Character building, combat, stat review | Crafting, trading, inventory management |
| **Equipment View** | Switch Bags/Worn tabs | Simultaneous access via tab switch on right |
| **Social Macros** | Dedicated page (12 slots) | Dedicated page (12 slots, 3×4 grid) |
| **Attribute Display** | Full STR-CHA + AC/ATK + Resists visible | STR-CHA + AC/ATK (compact, no resists) |
| **Button Size Standards** | Abilities 40×40, Socials 32×32 | Abilities 40×40, Socials 32×32 |
| **Window Scrolling** | Vertical scrolling between tabs | Horizontal column switching |

---

## Technical Implementation - Bags & Inventory Variant

### Dual-Column Architecture

**Left Column (Actions)**: X=1, width ~76px
- Four dynamic pages (Main, Abilities, Combat, Socials)
- Compact stat display (single column, each stat row 14px tall)
- Efficiency buttons: Camp, Sit/Stand, Run/Walk (20px tall each)
- Abilities/Combat use 2-column grid (40×40 size per button)
- Socials use 3×4 grid (32×32 size per button with navigation)

**Right Column (Inventory)**: X=77, width ~80px
- Two static pages (Bags, Worn)
- Bags page: Weapon slots (44×44 vertical), then 8 Bag slots (44×44 in 2×4 grid)
- Worn page: Paperdoll layout (36×36 per slot) distributed across column
- Independent tab switching from Actions column

**Bottom Stats Bar** (Y=370-390):
- Shared across all pages
- Shows Name (blue), Level (blue), HP (red tint), Mana (blue tint)
- Compact 20px height for constant visibility

### EQType Coverage & Standards

- **Base Stats** (EQType 5-10): STR, STA, AGI, DEX, WIS, INT (CHA omitted for space)
- **Combat Stats** (EQType 22-23): AC, ATK only (resistances omitted for compactness)
- **HP/Mana** (EQType 70, 80): Current values only at bottom
- **Equipment** (EQType 1-29): All 29 wearable/container slots across both inventory pages
- **Button Standardization**: Action buttons 40×40, Social buttons 32×32
- **Font Usage**: Font 2 for labels, Font 3 for values

### Optimization for Inventory Focus

- Fixed 160×394 size prevents overflow on crafting windows
- No scrolling required; all elements fit without paging
- Dual-column design eliminates tab-switching delays for inventory access
- Compact stats reduce window height while preserving essentials (Name/Level/HP/Mana)
- Social buttons in 3×4 grid (12 total, same as Standard variant)

---

## What Makes This "Bags and Inventory"

This variant prioritizes **simultaneous access to both actions and inventory**:
- **Dual-Column Layout**: Actions on left, Equipment on right for parallel use
- **No Info Page**: Removed detailed stats page to save vertical space; compact stats at bottom
- **Inventory Always Visible**: Switch between Bags/Worn tabs while maintaining 4 Actions tabs
- **Fixed 160×394 Size**: Optimized for crafting, trading, and inventory-heavy activities
- **State-Based Toggles**: Sit/Stand and Run/Walk buttons share screen real estate for efficiency
- **Paperdoll Integration**: Full equipment slot visibility without page-switching delays

---

## Notes on behavior

- Sit/Stand and Run/Walk are paired toggles sharing positions; the client shows one at a time.
- The Actions window is fixed-size (non-resizable) to maintain dual-column layout integrity
- Inventory tabs remain visible and can be switched independently from Actions page selection

---

## Testing checklist (matching XML)

- [x] Window opens on `ActionsWindow` at fixed 160×394 size
- [x] Tabs: Main, Abilities, Combat, Socials are selectable on left
- [x] Movement/stance buttons clickable (Camp, Sit/Stand, Run/Walk)
- [x] Socials page shows 12 social buttons and page selectors
- [x] Inventory tabs show Bags (22–29, Primary/Secondary/Range/Ammo) and Worn slots on right
- [x] Player stats (Name, Level, HP, Mana) render and update at bottom
- [x] Actions and Inventory tabs operate independently (switch actions while inventory tab stays same)

---

## Git history (documentation only)

**v1.1.1** — Documentation alignment and cleanup.

**v1.1.0** — Actions window with resizable frame and full tab/slot set.

---

*Maintainer: Draknare Thorne*  
*Status: Ready for in-game testing*
