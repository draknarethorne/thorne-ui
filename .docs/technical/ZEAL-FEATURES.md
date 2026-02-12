# Zeal Client Features Guide

[← Back to Development Guide](../../DEVELOPMENT.md#zeal-client-features)

---

## Overview

**Zeal** is a modified TAKP/P2002 client that provides significant enhancements beyond the standard client. These features fall into two categories:

1. **EQType-based data bindings** - UI XML elements that display game data (covered in this guide)
2. **Client-side functionality** - Built into the Zeal binary, not XML-based (camera, nameplate, map features)

**Important**: All Zeal-specific features **require the Zeal client** to function. They will not work on the vanilla P2002 client.

---

## Zeal-Specific EQTypes

These EQTypes **ONLY work with the Zeal client** and will display no data on vanilla P2002:

| EQType | Element Type | Purpose | Usage Location | Notes |
|--------|--------------|---------|----------------|-------|
| **24** | Gauge | **Mana Tick Countdown** | PlayerWindow | Displays time until next mana tick; must be in PlayerWindow with ScreenID "ZealTick" or similar Zeal-specific naming |
| **27** | Gauge | **Target of Target HP Gauge** | TargetOfTargetWindow | Visual HP bar for what your target is targeting; **REQUIRES** separate EQUI_TargetOfTargetWindow.xml file |
| **69** | Label | **Pet HP Percentage** | PlayerWindow | Displays pet's current HP as percentage (e.g., "95%") |
| **70** | Label | **Player HP (current/max)** | PlayerWindow | Shows current and max HP values (e.g., "1250/1500") |
| **71** | Label | **AA Points Total** | Inventory, TargetWindow | Total AA points available across character |
| **72** | Label | **AA Points Available** | Inventory | Current unspent AA points ready to allocate |
| **73** | Label | **AA Percentage** | Inventory | AA progress percentage toward next point |
| **80** | Label | **Player Mana Values/Percentage** | PlayerWindow, TargetWindow | Displays mana as percentage or current/max values |
| **81** | Label | **XP Per Hour** | PlayerWindow, TargetWindow | Shows experience gain rate per hour (useful for tracking grinding efficiency) |
| **83** | Label | **Inventory Slots (current/free)** | TargetWindow | Displays number of currently used or free inventory slots |
| **84** | Label | **Inventory Slots (max/total)** | TargetWindow | Shows maximum inventory capacity |
| **86** | Label | **AA Per Hour** | TargetWindow | Displays Alternate Advancement point gain rate per hour |
| **120** | Label | **Target of Target HP (numeric)** | TargetOfTargetWindow | Numeric HP display for target's target |
| **121** | Label | Tribute Points (current) | TributeBenefitWnd, GuildTributeMasterWnd | Standard P2002, NOT Zeal-specific |
| **122** | Label | Tribute Points (available) | TributeBenefitWnd, GuildTributeMasterWnd | Standard P2002, NOT Zeal-specific |
| **123** | Label | Tribute Points (cost) | TributeBenefitWnd, GuildTributeMasterWnd | Standard P2002, NOT Zeal-specific |

### Critical Context: EQType 24

**EQType 24 is context-dependent**:
- When used as a **Gauge** in **PlayerWindow** with Zeal-specific naming → **Mana tick countdown timer** ✓ (Zeal-only)
- When used as a **Label** elsewhere → **Current character weight** (standard P2002)
- When used as **InvSlot** elsewhere → **Inventory slot 24** (general inventory bag slot 2) - Standard P2002
- Examples of standard usage: Bank slot 2024, Loot slot 5024, Merchant slot 6024, Bazaar slot 7024

**Validation**: Confirmed in [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 173 - EQType 24 used as Gauge for mana tick timer.

### Usage Notes

**Common EQType Locations**:
- EQTypes **69, 70, 80, 81** are commonly used in **PlayerWindow** for extended player stats
- EQTypes **71, 72, 73** provide **AA (Alternate Advancement) tracking** in Inventory/TargetWindow
- EQTypes **81, 83, 84, 86** are used in **TargetWindow** (LunaQuarmified) for tracking stats/progression
- EQType **80** can display mana as percentage OR current/max values depending on label formatting
- XP/AA per hour rates (**81, 86**) are useful for tracking grinding/leveling efficiency
- AA points display: Use **71** for total available, **72** for unspent/allocatable, **73** for progress %

**Validation Summary**:
- EQType 24 (Mana Tick Gauge) - [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 173
- EQType 69 (Pet HP %) - [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 939
- EQType 70 (HP Cur/Max) - [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 303
- EQType 80 (Mana Values) - [thorne_drak/EQUI_PlayerWindow.xml](../../thorne_drak/EQUI_PlayerWindow.xml) line 404

### Critical Implementation Note: Target of Target (ToT)

**EQTypes 27 and 120 ONLY work in a window named "TargetOfTargetWindow"**. They cannot be embedded in the regular TargetWindow.

**Required Setup**:
1. Create separate file: `EQUI_TargetOfTargetWindow.xml`
2. Define window with `<Screen item="TargetOfTargetWindow">`
3. Add gauge with EQType 27 for ToT HP gauge
4. Add label with EQType 120 for ToT HP numeric/percentage
5. **Create/modify EQUI.xml** to include: `<Include>EQUI_TargetOfTargetWindow.xml</Include>`
   - Add after `<Include>EQUI_TargetWindow.xml</Include>` line
   - Default EQUI.xml does NOT include this - you must add it

**Why This Matters**:
- Default EQUI.xml doesn't reference TargetOfTargetWindow - won't load without explicit include
- Attempting to use EQType 27/120 in TargetWindow will fail silently
- The ToT window is independent - can be positioned/hidden separately
- Graceful degradation: Window appears empty without Zeal, doesn't break UI

**Example Implementation**: See [thorne_drak/EQUI_TargetOfTargetWindow.xml](../../thorne_drak/EQUI_TargetOfTargetWindow.xml) and [thorne_drak/EQUI.xml](../../thorne_drak/EQUI.xml)

---

## Zeal Client-Only Features

These features are **implemented in the Zeal client binary**, not UI XML. They don't use EQTypes but can be configured via Zeal Options.

### General Features (`zeal/EQUI_Tab_General.xml`)

- **Hide Corpse Looted** - Auto-hide corpses after looting
- **Blue Con Color** - Custom blue con color (uses Zeal color #15)
- **Advanced Input** - Modern text editing (Ctrl+C/V, Home/End, Shift+arrows)
- **Show Helm** - Toggle helmet visibility
- **Escape Logic** - ESC drops target without closing windows
- **Raid Escape Lock** - Prevent ESC from closing raid window
- **Container Tooltips** - ALT key shows tooltips for all bag items
- **Spellbook Auto Stand** - Auto-stand when spellbook opens (enables movement keys for page turning)
- **Classic Class Names** - Toggle 50+ class names in /who
- **Tell Windows** - Dedicated windows for private messages
- **Tell Window History** - Keep tell history across sessions
- **Alt LinkAll Delimiter** - Alternative delimiter for item linking
- **Enable Container Lock** - Add lock option to bag context menu
- **Export on /camp** - Save inventory + spellbook data on logout
- **Buff Timers** - Display buff duration timers

### Map Features (`zeal/EQUI_Tab_Map.xml`)

- **Zeal Map** - Overlay map system with customization
- **Background Options** - None, Dark, Light, Tan backgrounds
- **Background Alpha** - Transparency slider for map background
- **Map Position/Size** - Fully customizable map overlay

### Camera Features (`zeal/EQUI_Tab_Cam.xml`)

- **Mouse Look Smoothing** - Smooth camera movement
- **Pan Delay** - Configurable camera pan delay

### Nameplate Features (`zeal/EQUI_Tab_Nameplate.xml`)

- **Nameplate Mana Bars** - Display mana bars on nameplates
  - **REQUIRES**: Zeal fonts (special font system)
  - **Button**: `Zeal_NameplateManaBars`
  - **Tooltip**: "Enable mana bars (zeal fonts only)"

### Floating Damage (`zeal/EQUI_Tab_FloatingDamage.xml`)

- **Floating Combat Numbers** - Display damage numbers above targets
- **Show from me** - Toggle damage from player
- **Show from pets** - Toggle pet damage display
- **Show from other PCs** - Toggle other player damage
- **Show from NPCs** - Toggle NPC damage display

### Target Rings (`zeal/EQUI_Tab_TargetRing.xml`)

- **Target Rings Toggle** - Enable/disable target rings
- **Disable for Self** - Hide ring when self-targeting
- **Attack Indicator** - Visual combat indicator on ring
- **Follow Heading** - Rotate ring with target direction
- **Cone Rendering** - Render as cone instead of circle
- **Target Color** - Match ring color to target con color
- **Hide with GUI** - Auto-hide rings when UI hidden

### Color Customization (`zeal/EQUI_Tab_Colors.xml`)

**Nameplate Color Schemes** - Customizable color palette for nameplates:
- Color 0: AFK
- Color 1: LFG
- Color 2: LD (Link Dead)
- Color 3: MyGuild
- Color 4: Raid
- ...and more (15+ color codes)

---

## Zeal Configuration Files

| File | Purpose |
|------|---------|
| `EQUI_ZealOptions.xml` | Main Zeal options dialog (tabs for all features) |
| `EQUI_Tab_General.xml` | General Zeal settings |
| `EQUI_Tab_Map.xml` | Map overlay configuration |
| `EQUI_Tab_Cam.xml` | Camera smoothing settings |
| `EQUI_Tab_Nameplate.xml` | Nameplate customization (mana bars, etc.) |
| `EQUI_Tab_FloatingDamage.xml` | Floating damage number settings |
| `EQUI_Tab_TargetRing.xml` | Target ring customization |
| `EQUI_Tab_Colors.xml` | Color palette customization |
| `EQUI_ZealMap.xml` | Zeal map window definition |
| `EQUI_ZealButtonWnd.xml` | Zeal button components |
| `EQUI_ZealInputDialog.xml` | Zeal input dialogs |

---

## XML Implementation Examples

### Example 1: Mana Tick Timer in PlayerWindow

```xml
<Gauge item="Zeal_Tick">
    <ScreenID>ZealTick</ScreenID>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>30</X>
        <Y>54</Y>
    </Location>
    <Size>
        <CX>150</CX>
        <CY>27</CY>
    </Size>
    <GaugeOffsetY>0</GaugeOffsetY>
    <TextOffsetX>-500</TextOffsetX>
    <Style_Transparent>true</Style_Transparent>
    <FillTint>
        <R>255</R>
        <G>255</G>
        <B>255</B>
    </FillTint>
    <LinesFillTint>
        <R>0</R>
        <G>220</G>
        <B>220</B>
    </LinesFillTint>
    <DrawLinesFill>false</DrawLinesFill>
    <EQType>24</EQType>
    <GaugeDrawTemplate>
        <Fill>A_GaugeLinesFill</Fill>
    </GaugeDrawTemplate>
</Gauge>
```

**Key Properties**:
- `<EQType>24</EQType>` - Mana tick countdown (context-dependent!)
- `<ScreenID>ZealTick</ScreenID>` - Identifies this as Zeal-specific gauge
- `<TextOffsetX>-500</TextOffsetX>` - Hides default gauge text (optional)
- Must be placed in **PlayerWindow** for EQType 24 to function as mana tick timer

### Example 2: Target of Target HP

```xml
<!-- HP Gauge -->
<Gauge item="TargetOfTarget_HP">
    <ScreenID>TargetOfTarget_HP</ScreenID>
    <EQType>27</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>10</X>
        <Y>40</Y>
    </Location>
    <Size>
        <CX>100</CX>
        <CY>12</CY>
    </Size>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground</Background>
        <Fill>A_GaugeFillRed</Fill>
    </GaugeDrawTemplate>
</Gauge>

<!-- Numeric HP Label -->
<Label item="TargetOfTarget_HPLabel">
    <ScreenID>TargetOfTarget_HPLabel</ScreenID>
    <EQType>120</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>10</X>
        <Y>55</Y>
    </Location>
    <Size>
        <CX>100</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>255</R>
        <G>100</G>
        <B>100</B>
    </TextColor>
    <AlignRight>true</AlignRight>
</Label>
```

**Usage**:
- EQType 27 (Gauge) - Visual HP bar for target's target
- EQType 120 (Label) - Numeric HP display (e.g., "450/1200")
- Both elements work together for comprehensive ToT HP display

### Example 3: Extended Player Stats Display

```xml
<!-- Player HP Values (current/max) -->
<Label item="PW_HP_Values">
    <ScreenID>PW_HP_Values</ScreenID>
    <EQType>70</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>170</X>
        <Y>26</Y>
    </Location>
    <Size>
        <CX>50</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>255</R>
        <G>100</G>
        <B>100</B>
    </TextColor>
    <AlignCenter>true</AlignCenter>
</Label>

<!-- Player Mana Values/Percentage -->
<Label item="PW_Mana_Values">
    <ScreenID>PW_Mana_Values</ScreenID>
    <EQType>80</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>170</X>
        <Y>43</Y>
    </Location>
    <Size>
        <CX>50</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>150</R>
        <G>150</G>
        <B>255</B>
    </TextColor>
    <AlignCenter>true</AlignCenter>
</Label>

<!-- Pet HP Percentage -->
<Label item="PW_Pet_Pct">
    <ScreenID>PW_Pet_Pct</ScreenID>
    <EQType>69</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>123</X>
        <Y>111</Y>
    </Location>
    <Size>
        <CX>25</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>255</R>
        <G>255</G>
        <B>255</B>
    </TextColor>
    <AlignRight>true</AlignRight>
</Label>
```

**Display Output**:
- EQType 70 - HP: "1250/1500" (red text)
- EQType 80 - Mana: "400/500" or "80%" (blue text)
- EQType 69 - Pet HP: "95%" (white text)

**Design Note**: Use consistent TextColor schemes (red for HP, blue for Mana) for visual clarity.

### Example 4: XP and AA Tracking

```xml
<!-- XP Per Hour -->
<Label item="Player_XPHOUR">
    <ScreenID>Player_XPHOUR</ScreenID>
    <EQType>81</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>120</X>
        <Y>101</Y>
    </Location>
    <Size>
        <CX>60</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>240</R>
        <G>240</G>
        <B>240</B>
    </TextColor>
    <AlignLeft>true</AlignLeft>
</Label>

<!-- AA Per Hour -->
<Label item="ZealAA_Hour">
    <ScreenID>ZealAA_Hour</ScreenID>
    <EQType>86</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>109</X>
        <Y>174</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>240</R>
        <G>240</G>
        <B>240</B>
    </TextColor>
    <AlignLeft>true</AlignLeft>
</Label>

<!-- Optional: Static labels for clarity -->
<Label item="Static_XP_Label">
    <Text>XP/hr:</Text>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>80</X>
        <Y>101</Y>
    </Location>
    <Size>
        <CX>35</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>180</R>
        <G>180</G>
        <B>180</B>
    </TextColor>
</Label>

<Label item="Static_AA_Label">
    <Text>AA/hr:</Text>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>70</X>
        <Y>174</Y>
    </Location>
    <Size>
        <CX>35</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>180</R>
        <G>180</G>
        <B>180</B>
    </TextColor>
</Label>
```

**Display Output**:
- XP/hr: 12.5% (showing leveling progress rate)
- AA/hr: 3.2% (showing AA accumulation rate)

**Usage Context**: Useful for grinding/leveling tracking. Place in PlayerWindow or TargetWindow.

### Example 5: Inventory Slot Tracking

```xml
<!-- Free Inventory Slots -->
<Label item="Zeal_INV">
    <ScreenID>Zeal_INV</ScreenID>
    <EQType>83</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>130</X>
        <Y>175</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>200</R>
        <G>255</G>
        <B>100</B>
    </TextColor>
    <AlignLeft>true</AlignLeft>
</Label>

<!-- Total Inventory Slots -->
<Label item="Zeal_INV2">
    <ScreenID>Zeal_INV2</ScreenID>
    <EQType>84</EQType>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>180</X>
        <Y>175</Y>
    </Location>
    <Size>
        <CX>90</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>200</R>
        <G>255</G>
        <B>100</B>
    </TextColor>
    <AlignLeft>true</AlignLeft>
</Label>

<!-- Optional: Static labels for clarity -->
<Label item="Zeal_INV3">
    <Text>Free</Text>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>95</X>
        <Y>175</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>150</R>
        <G>150</G>
        <B>150</B>
    </TextColor>
</Label>

<Label item="Zeal_INV4">
    <Text>Total</Text>
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>145</X>
        <Y>175</Y>
    </Location>
    <Size>
        <CX>30</CX>
        <CY>12</CY>
    </Size>
    <TextColor>
        <R>150</R>
        <G>150</G>
        <B>150</B>
    </TextColor>
</Label>
```

**Display Output**:
- Free: 42 (slots currently available)
- Total: 80 (maximum inventory capacity)

**Usage Context**: Useful for inventory management. Place in TargetWindow or PlayerWindow.

---

## Zeal Requirements & Compatibility

### Installation Requirements

**To use Zeal features:**
1. Install Zeal-modified TAKP client (not vanilla P2002)
2. Include `zeal/` folder files in your UI directory
3. For nameplate mana bars: Install Zeal fonts
4. Test all Zeal features in-game to verify client support

### Fallback for Non-Zeal Clients

**Behavior on vanilla P2002**:
- Zeal EQTypes (24, 27, 69-73, 80-86, 120) will display **no data** on vanilla clients
- UI won't break, but elements using these EQTypes will be empty/blank
- Client-side features (floating damage, map overlay) simply won't be available
- No error messages or crashes - just missing data

**Best Practice**: Test your UI on both Zeal and vanilla clients to ensure graceful degradation.

---

## Real-World Implementations

**Reference UIs with Zeal Integration**:

1. **thorne_drak** - Thorne Blue PlayerWindow with extended stats
   - Location: `thorne_drak/EQUI_PlayerWindow.xml`
   - Uses: EQTypes 24, 69, 70, 80 for mana tick, pet HP, player HP/Mana values
   - Validation: Lines 173 (mana tick), 303 (HP cur/max), 404 (mana values), 939 (pet HP %)

2. **QQQuarm / LunaQuarmified** - Advanced Zeal integration
   - Location: `QQQuarm/EQUI_PlayerWindow.xml`, `LunaQuarmified/EQUI_TargetWindow.xml`
   - Uses: EQTypes 24, 81, 83, 84, 86 for mana tick, XP/hour, AA/hour, inventory tracking
   - Features: Comprehensive stat tracking, progression monitoring

3. **LunaQuarmified/EQUI_TargetWindow.xml** - Advanced target window
   - Uses: EQTypes 81, 83, 84, 86 for XP/AA/inventory tracking
   - Design: Full stats panel for target tracking

**Study These Files**: The best way to learn Zeal integration is to examine working implementations in the reference UIs listed above.

---

## Design Best Practices

### 1. Graceful Degradation

Design UIs to work on both Zeal and vanilla clients:
- Place Zeal-specific elements in non-critical locations
- Don't rely solely on Zeal data for essential functionality
- Test on vanilla client to verify acceptable fallback behavior

### 2. Clear Visual Hierarchy

When adding extended stats:
- Use consistent color schemes (red=HP, blue=Mana, white=general)
- Group related stats together (HP/Mana values near gauges)
- Add static labels for clarity ("XP/hr:", "Free:", etc.)

### 3. Context-Appropriate Usage

Place EQTypes in logical windows:
- **PlayerWindow**: Player stats (HP, Mana, Pet HP, XP/AA tracking)
- **TargetWindow**: Target/ToT stats, progression tracking
- **Inventory**: AA points, inventory slot tracking

### 4. Performance Considerations

Limit excessive label updates:
- XP/AA per hour rates update frequently - use sparingly
- Inventory slot tracking can be CPU-intensive
- Test performance in crowded zones

---

## Troubleshooting

### Zeal EQTypes Not Displaying Data

**Problem**: EQType labels are blank or show no data.

**Solutions**:
1. Verify you're running the Zeal client (not vanilla P2002)
2. Check ScreenID naming - some EQTypes require specific naming conventions
3. Ensure element is in correct window (e.g., EQType 24 must be in PlayerWindow as Gauge)
4. Test with known-working reference UI (thorne_drak, LunaQuarmified)

### Mana Tick Timer (EQType 24) Not Working

**Problem**: EQType 24 gauge displays incorrectly or shows no countdown.

**Solutions**:
1. Must be used as **Gauge** element (not Label or InvSlot)
2. Must be in **PlayerWindow** (not other windows)
3. Use Zeal-specific ScreenID (e.g., "ZealTick")
4. Verify gauge templates are properly defined
5. Check that Zeal client is installed and running

### Target of Target Not Working

**Problem**: EQType 27 (ToT HP gauge) or 120 (ToT HP label) display no data.

**Solutions**:
1. Verify Zeal client is running (not vanilla P2002)
2. Ensure you have a valid target with a target
3. Check window is properly defined (TargetOfTargetWindow)
4. Test with simpler implementation first (just gauge, then add label)

---

## Related Documentation

- [EQType Reference Guide](EQTYPES.md) - Comprehensive EQType tables including standard and Zeal-specific values
- [Development Guide](../../DEVELOPMENT.md) - Main development documentation
- [Standards Guide](../STANDARDS.md) - UI design standards and best practices

---

**Last Updated**: February 2026  
**Validated Against**: thorne_drak UI files, LunaQuarmified implementation  
**Zeal Client Version**: TAKP/P2002 Zeal (2025-2026 builds)
