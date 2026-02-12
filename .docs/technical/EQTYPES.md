# EQType Reference Guide

[← Back to Development Guide](../../DEVELOPMENT.md#technical-reference)

---

## Overview

**EQTypes** are numeric bindings that connect UI elements (Gauges, Labels, InvSlots) to game data. The same EQType number can mean different things depending on the element type and context.

### Context-Dependent Behavior

The same EQType number has **different meanings** based on the element type:
- **Gauge** (progress bars): EQType 1 = Player HP percentage
- **Label** (text fields): EQType 1 = Character name
- **InvSlot** (equipment): EQType 1 = Left ear equipment slot

Always consider the element type when using EQType values in your XML files.

---

## Gauge EQTypes (Progress Bars / Resource Displays)

### Player Gauges

| EQType | Gauge | Element Type | Window | Notes |
|--------|-------|--------------|--------|-------|
| 1 | Player HP | Gauge | PlayerWindow | Red gauge, health percentage |
| 2 | Player Mana | Gauge | PlayerWindow | Blue gauge, mana percentage |
| 3 | Player Stamina/Fatigue | Gauge | PlayerWindow | Yellow gauge, breath/stamina |
| 4 | Experience % | Gauge | Inventory, AAWindow | Orange/green gauge for XP progress |
| 5 | AA Experience % | Gauge | Inventory, AAWindow | Yellow gauge for AA XP |
| 6 | Target HP | Gauge | TargetWindow | Target's health percentage |

**Validation**: Confirmed in [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml)
- EQType 1 (HP Gauge) - Line 184
- EQType 2 (Mana Gauge) - Line 246
- EQType 3 (Stamina Gauge) - Line 205

### Group Member Gauges

| EQType | Gauge | Element Type | Window | Notes |
|--------|-------|--------------|--------|-------|
| 11 | Group Member 1 HP | Gauge | GroupWindow | First party member HP |
| 12 | Group Member 2 HP | Gauge | GroupWindow | Second party member HP |
| 13 | Group Member 3 HP | Gauge | GroupWindow | Third party member HP |
| 14 | Group Member 4 HP | Gauge | GroupWindow | Fourth party member HP |
| 15 | Group Member 5 HP | Gauge | GroupWindow | Fifth party member HP |

**Validation**: Confirmed in [thorne_drak/EQUI_GroupWindow.xml](../../thorne_drak/EQUI_GroupWindow.xml)
- EQType 11-15 (Group Member HP) - Lines 98, 227, 356, 485, 614

### Pet and Group Pet Gauges

| EQType | Gauge | Element Type | Window | Notes |
|--------|-------|--------------|--------|-------|
| 16 | Pet HP | Gauge | PlayerWindow, PetInfoWindow | Your pet's health (purple gauge) |
| 17 | Group Member 1 Pet HP | Gauge | GroupWindow | First member's pet HP |
| 18 | Group Member 2 Pet HP | Gauge | GroupWindow | Second member's pet HP |
| 19 | Group Member 3 Pet HP | Gauge | GroupWindow | Third member's pet HP |
| 20 | Group Member 4 Pet HP | Gauge | GroupWindow | Fourth member's pet HP |
| 21 | Group Member 5 Pet HP | Gauge | GroupWindow | Fifth member's pet HP |

**Validation**: Confirmed in XML files
- EQType 16 (Pet HP) - [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 896
- EQType 17-21 (Group Pet HP) - [thorne_drak/EQUI_GroupWindow.xml](../../thorne_drak/EQUI_GroupWindow.xml) lines 144, 273, 402, 531, 660

### Special Gauges

| EQType | Gauge | Element Type | Window | Notes |
|--------|-------|--------------|--------|-------|
| 27 | Target of Target HP | Gauge | TargetOfTargetWindow | ToT health (works with Zeal client); **MUST** be in separate EQUI_TargetOfTargetWindow.xml file |
| 76 | Music Track | Label | MusicPlayerWnd | Current track name |
| 77 | Music Album | Label | MusicPlayerWnd | Album name |
| 78 | Music Artist | Label | MusicPlayerWnd | Artist name |
| 79 | Music Genre | Label | MusicPlayerWnd | Genre display |

**Note**: EQType 27 requires the Zeal client. See [Zeal Features](ZEAL-FEATURES.md) for details.

---

## Label EQTypes (Text Fields / Numeric Displays)

### Character Information

| EQType | Data Field | Element Type | Format | Usage |
|--------|------------|--------------|--------|-------|
| 1 | Character Name | Label | Text | Player/target name display |
| 2 | Level | Label | Number | Character level |
| 3 | Class | Label | Text | Class name (Warrior, Cleric, etc.) |
| 4 | Deity | Label | Text | Deity name |
| 18 | Current HP | Label | Number | Numeric HP value |
| 19 | HP Percentage | Label | Percentage | HP % (e.g., "85%") |
| 20 | Mana Percentage | Label | Percentage | Mana % (e.g., "72%") |
| 21 | Maximum Mana | Label | Number | Max mana value |
| 22 | Armor Class (AC) | Label | Number | Total AC |
| 23 | Attack (ATK) | Label | Number | Attack rating |
| 24 | Current Weight | Label | Number | Current character weight |
| 25 | Maximum Weight | Label | Number | Max carrying capacity |
| 26 | Experience % | Label | Percentage | XP percentage to next level |

**Important**: EQType 24 has **context-dependent meaning**:
- As **Label**: Current character weight (standard)
- As **Gauge** in PlayerWindow with Zeal: Mana tick countdown timer (Zeal-only)
- As **InvSlot**: Inventory bag slot 2 (EQType 22-29 = Bag slots 1-8)

### Character Attributes

| EQType | Attribute | Element Type | Usage |
|--------|-----------|--------------|-------|
| 5 | Strength (STR) | Label | Primary melee stat |
| 6 | Stamina (STA) | Label | HP and endurance |
| 7 | Dexterity (DEX) | Label | Avoidance and procs |
| 8 | Agility (AGI) | Label | AC and dodge |
| 9 | Wisdom (WIS) | Label | Cleric/Druid mana |
| 10 | Intelligence (INT) | Label | Wizard/Mage mana |
| 11 | Charisma (CHA) | Label | Faction and pet power |

**Validation**: Confirmed in [thorne_drak/EQUI_Inventory.xml](../../thorne_drak/EQUI_Inventory.xml)
- EQType 1-11 used for InvSlot (equipment slots 0-10: Charm, Ear, Head, Face, etc.)
- Context: Same numbers, different element types (InvSlot vs Label)

### Resistances

| EQType | Resistance | Element Type | Display Color |
|--------|-----------|--------------|---------------|
| 12 | Poison Resist | Label | Teal |
| 13 | Disease Resist | Label | Yellow |
| 14 | Fire Resist | Label | Orange |
| 15 | Cold Resist | Label | Cyan |
| 16 | Magic Resist | Label | Purple |

### Extended Labels

| EQType | Data Field | Element Type | Format | Notes |
|--------|------------|--------------|--------|-------|
| 36 | AA Points Spent | Label | Number | Total AA points spent |
| 37 | AA Points Unspent | Label | Number | Available AA points |
| 45-67 | Buff Duration Timers | Label | Text | Buff slot 0-22 duration text (e.g., "0:45") |
| 69 | Pet HP Percentage | Label | Percentage | Pet health % (Zeal-only) |
| 70 | HP Values (Cur/Max) | Label | Text | "150/200" format (Zeal-only) |
| 71 | AA Points Total | Label | Number | Total AA points available (Zeal-only) |
| 72 | AA Points Available | Label | Number | Current unspent AA points (Zeal-only) |
| 73 | AA Percentage | Label | Percentage | AA progress % (Zeal-only) |
| 76 | Music Track | Label | Text | Current music track name |
| 77 | Music Album | Label | Text | Album name |
| 78 | Music Artist | Label | Text | Artist name |
| 79 | Music Genre | Label | Text | Genre display |
| 80 | Mana Values (Cur/Max) | Label | Text | "400/500" format (Zeal-only) |
| 81 | XP Per Hour % | Label | Percentage | XP/hour rate (Zeal-only) |
| 83 | Inventory Slots Free | Label | Number | Available bag space (Zeal-only) |
| 84 | Inventory Slots Total | Label | Number | Max inventory capacity (Zeal-only) |
| 86 | AA Per Hour | Label | Percentage | AA/hour rate (Zeal-only) |
| 116-119 | Unknown | Label | - | Found in default files, purpose unclear |
| 120 | Target of Target HP Label | Label | Text | ToT HP numeric display (Zeal-only); **MUST** be in separate EQUI_TargetOfTargetWindow.xml file |
| 121 | Tribute Points Current | Label | Number | Tribute system (standard P2002) |
| 122 | Tribute Points Available | Label | Number | Tribute system (standard P2002) |
| 123 | Tribute Points Cost | Label | Number | Tribute system (standard P2002) |
| 124 | Unknown | Label | - | Purpose unclear |
| 128-129 | Unknown | Label | - | Purpose unclear |
| 132 | Task Window Info | Label | Text | Quest/task data |
| 133 | Spell Gem Info | Label | Text | Spell gem 0 data |
| 134-140 | Spell/Buff Data | Label | Text | Additional spell/buff information |

**Validation**: Confirmed Zeal-specific EQTypes in [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml)
- EQType 69 (Pet HP %) - Line 939
- EQType 70 (HP Cur/Max) - Line 303
- EQType 80 (Mana Values) - Line 404

---

## InvSlot EQTypes (Equipment & Inventory)

### Worn Equipment Slots

| EQType | Slot Name | Element Type | Location |
|--------|-----------|--------------|----------|
| 0 | Charm | InvSlot | Worn equipment |
| 1 | Ear (Left) | InvSlot | Worn equipment |
| 2 | Head | InvSlot | Worn equipment |
| 3 | Face | InvSlot | Worn equipment |
| 4 | Ear (Right) | InvSlot | Worn equipment |
| 5 | Neck | InvSlot | Worn equipment |
| 6 | Shoulders | InvSlot | Worn equipment |
| 7 | Arms | InvSlot | Worn equipment |
| 8 | Back | InvSlot | Worn equipment |
| 9 | Wrist (Left) | InvSlot | Worn equipment |
| 10 | Wrist (Right) | InvSlot | Worn equipment |
| 11 | Range | InvSlot | Weapon slot |
| 12 | Hands | InvSlot | Worn equipment |
| 13 | Primary | InvSlot | Weapon slot (main hand) |
| 14 | Secondary | InvSlot | Weapon slot (off-hand) |
| 15 | Finger (Left) | InvSlot | Worn equipment |
| 16 | Finger (Right) | InvSlot | Worn equipment |
| 17 | Chest | InvSlot | Worn equipment |
| 18 | Legs | InvSlot | Worn equipment |
| 19 | Feet | InvSlot | Worn equipment |
| 20 | Waist | InvSlot | Worn equipment |
| 21 | Ammo | InvSlot | Weapon slot |

**Validation**: Confirmed in [thorne_drak/EQUI_Inventory.xml](../../thorne_drak/EQUI_Inventory.xml)
- EQType 1-21 (Equipment slots) - Lines 39-458

### Inventory Bag Slots

| EQType Range | Purpose | Element Type | Notes |
|--------------|---------|--------------|-------|
| 22-29 | Bag Slots 1-8 | InvSlot | Main inventory bags (8 slots) |

**Validation**: Confirmed in [thorne_drak/EQUI_Inventory.xml](../../thorne_drak/EQUI_Inventory.xml)
- EQType 22 (Bag Slot 1) - Line 458

### Container Slots (Currently Open Bag)

| EQType Range | Purpose | Element Type | Notes |
|--------------|---------|--------------|-------|
| 30-39 | Container Slots 1-10 | InvSlot | Currently-open bag contents (10 slots max) |

**Important Limitation**: Unlike bank bags (2030+), inventory bags have **no dedicated expanded EQTypes**. EQTypes 30-39 show **only the currently-open container**. You cannot display multiple bag contents simultaneously in the standard Inventory window.

---

## Bank & Storage EQTypes

| EQType Range | Purpose | Element Type | Notes |
|--------------|---------|--------------|-------|
| 2000-2023 | Bank Slots | InvSlot | Main bank slots (24 slots) |
| 2030-2039 | Bank Bag 0 Expanded | InvSlot | First bank bag contents (slots 0-9) |
| 2040-2049 | Bank Bag 1 Expanded | InvSlot | Second bank bag contents (slots 0-9) |
| 2050-2059 | Bank Bag 2 Expanded | InvSlot | Third bank bag contents (slots 0-9) |
| 2060-2069 | Bank Bag 3 Expanded | InvSlot | Fourth bank bag contents (slots 0-9) |
| 2070-2079 | Bank Bag 4 Expanded | InvSlot | Fifth bank bag contents (slots 0-9) |
| 2080-2089 | Bank Bag 5 Expanded | InvSlot | Sixth bank bag contents (slots 0-9) |
| 2090-2329 | Additional Bank Bags | InvSlot | Continuing pattern for all bank bags |
| 2500-2509 | Shared Bank Slots | InvSlot | Shared bank (10 slots) |

---

## Trading & Commerce EQTypes

| EQType Range | Purpose | Element Type | Window | Notes |
|--------------|---------|--------------|--------|-------|
| 3000-3003 | Give Window Slots | InvSlot | GiveWnd | Quest item turn-in (4 slots) |
| 3008-3015 | Trade Window Slots | InvSlot | TradeWnd | Player-to-player trading (8 slots) |
| 5000-5029 | Loot Slots | InvSlot | LootWnd | Corpse looting (30 slots) |
| 6000-6079 | Merchant Inventory | InvSlot | MerchantWnd | Merchant's items for sale (80 slots) |
| 7000-7079 | Bazaar Trader Slots | InvSlot | BazaarWnd | Player bazaar trader (80 slots) |
| 8001-8021 | Inspect Window Slots | InvSlot | InspectWnd | Viewing another player's gear (21 slots) |

---

## Important Notes on EQTypes

### Context-Dependent Values

The same EQType number means different things for different element types:
- **Gauge**: EQType 1 = Player HP percentage
- **Label**: EQType 1 = Character name
- **InvSlot**: EQType 1 = Left ear equipment slot

Always verify the element type (Gauge, Label, InvSlot) when interpreting EQType values.

### Zeal Client Extensions

Several EQTypes **only work with the Zeal client**:
- EQType 24 (Gauge in PlayerWindow) - Mana tick countdown timer
- EQType 27 (Gauge) - Target of Target HP
- EQTypes 69-73 (Labels) - Extended player/pet/AA stats
- EQTypes 80-86 (Labels) - Mana, XP/AA rates, inventory tracking
- EQType 120 (Label) - Target of Target HP numeric display

Standard P2002 client may not populate these values. See [Zeal Features Guide](ZEAL-FEATURES.md) for comprehensive Zeal documentation.

### No Container Expansion for Inventory Bags

Unlike bank bags (2030+), inventory bags have **no dedicated expanded EQTypes**. EQTypes 30-39 show only the currently-open container. This is a fundamental client limitation.

**Workaround**: If you need to display inventory bag contents, you must rely on the standard container window (30-39) which shows whichever bag is currently open.

### Currency/Coins Display

Platinum, Gold, Silver, Copper displays **do NOT use EQTypes**. They are bound directly via client code to Button text fields in Inventory/Trade windows.

---

## Color Palette

Standard label colors (matching Inventory window canonical scheme):

| Label Type | RGB Value | Hex | Usage |
|------------|-----------|-----|-------|
| **White** | 255, 255, 255 | #FFFFFF | Default text, player name, stat values |
| **Blue (Attributes)** | 50, 160, 250 | #32A0FA | Attribute labels (STR, STA, AGI, etc) |
| **Pink/Rose** | 200, 120, 145 | #C87891 | HP/Mana labels (alternate) |
| **Orange** | 255, 165, 0 | #FFA500 | ATK label, FIRE resist |
| **Cyan** | 0, 165, 255 | #00A5FF | COLD resist |
| **Purple** | 195, 0, 185 | #C300B9 | MAGIC resist |
| **Yellow** | 205, 205, 0 | #CDCD00 | DISEASE resist |
| **Teal** | 0, 130, 100 | #008264 | POISON resist |

---

## Related Documentation

- [Zeal Client Features](ZEAL-FEATURES.md) - Comprehensive guide to Zeal-specific EQTypes and client features
- [Development Guide](../../DEVELOPMENT.md) - Main development documentation
- [Standards Guide](../STANDARDS.md) - UI design standards and best practices

---

**Last Updated**: February 2026  
**Validated Against**: thorne_drak UI files (EQUI_PlayerWindow.xml, EQUI_GroupWindow.xml, EQUI_Inventory.xml)
