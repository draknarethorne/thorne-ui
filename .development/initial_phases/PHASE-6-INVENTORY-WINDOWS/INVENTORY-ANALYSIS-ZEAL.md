# Inventory Analysis: Zeal UI (Inherited from Default)

## Executive Summary
- **Source File**: `default/EQUI_Inventory.xml`
- **Analysis Date**: February 4, 2026

The Zeal UI modification does not provide a custom `EQUI_Inventory.xml`. It inherits this window entirely from the `default` UI files. This analysis, therefore, focuses on proposing enhancements to the default inventory layout by integrating powerful, data-rich EQTypes exclusive to the Zeal client.

The default layout is functional but lacks detailed, at-a-glance information that modern players expect. By strategically adding new labels tied to Zeal's custom EQTypes, we can significantly improve the window's utility without altering its core structure. The primary opportunities lie in displaying precise HP/Mana values, tracking XP/AA progression rates, and providing an inventory slot counter.

This document provides a roadmap for creating a "Zeal-enhanced" version of the default inventory window.

## Layout Architecture (Reference: `default/EQUI_Inventory.xml`)

The default inventory window uses a standard three-column layout.
- **Left Column**: Character info (Name, Level, Class, Deity), core stats (HP, AC, ATK), primary stats (STR, STA, etc.), and resistances.
- **Center Column**: Anatomical equipment slots.
- **Right Column**: Main inventory bag slots.

There is sufficient empty space to add new informational labels, particularly below the primary stats and near the bottom of the window.

**ASCII Art Layout (from INVENTORY-ANALYSIS-DEFAULT.md)**
```
┌───────────────────────────────────────────────────────────┐
│ INVENTORY                                                 │
├───────────────────────────────────────────────────────────┤
│ ┌───────────┬──────────────────────┬────────────────────┐ │
│ │ LEFT      │ CENTER               │ RIGHT              │ │
│ │ (0,0)     │ (120,0)              │ (330,160)          │ │
│ │ 120x330   │ 210x330              │ 80x160             │ │
│ │           │                      │                    │ │
│ │ Name/Class│ ┌─Ear──Neck──Face──Head──Ear─┐ │ ┌─Bag1──Bag2─┐ │
│ │ HP/AC/ATK │ │ Chest Arms  Back Shoulders│ │ │ Bag3  Bag4 │ │
│ │ XP Gauge  │ │ Wrist Waist Wrist  Hands │ │ │ Bag5  Bag6 │ │
│ │ Stats     │ │ Ring       Ring         │ │ │ Bag7  Bag8 │ │
│ │ Resists   │ │ └─Legs──Feet──Primary/Sec/Range/Ammo┘ │ │ └────────────┘ │
│ │           │                      │                    │ │
│ └───────────┴──────────────────────┴────────────────────┘ │
├───────────────────────────────────────────────────────────┤
│ [Done] [Alt Storage] [Skills] [Dye] [Face]                │
└───────────────────────────────────────────────────────────┘
```

## Zeal-Specific EQType Enhancements

The following sections detail how to leverage Zeal's custom EQTypes to enhance the default inventory window.

### 1. Consolidated HP and Mana Readouts

The default UI uses separate labels for `CurrentHP`/`MaxHP` and has no display for Mana values in the inventory. Zeal's EQTypes can display this information in a more compact `Current/Max` format.

**Proposed Implementation:**

- **HP Display:** Replace the three separate labels for HP with a single, more efficient label.
- **Mana Display:** Add a new label for Mana, mirroring the HP display format.

**XML Snippets:**

```xml
<!-- ** ENHANCEMENT: Consolidated HP Label ** -->
<!-- Remove IW_HP, IW_CurrentHP, IW_HPDivider, IW_MaxHP -->
<Label item ="IW_HP_Zeal">
    <ScreenID>HPLabel</ScreenID>
    <EQType>70</EQType> <!-- Zeal: HP Current/Max -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>14</X>
        <Y>50</Y>
    </Location>
    <Size>
        <CX>106</CX>
        <CY>14</CY>
    </Size>
    <Text>HP: 1234/1234</Text>
    <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
    <NoWrap>true</NoWrap>
</Label>

<!-- ** ENHANCEMENT: Consolidated Mana Label ** -->
<Label item ="IW_Mana_Zeal">
    <ScreenID>ManaLabel</ScreenID>
    <EQType>80</EQType> <!-- Zeal: Mana Current/Max -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>14</X>
        <Y>64</Y> <!-- Positioned below new HP label -->
    </Location>
    <Size>
        <CX>106</CX>
        <CY>14</CY>
    </Size>
    <Text>Mana: 1234/1234</Text>
    <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
    <NoWrap>true</NoWrap>
</Label>
```
**Value Proposition:** Provides clear, consolidated HP and Mana values directly in the inventory, a crucial feature missing from the default UI.

### 2. XP and AA Rate Tracking

Players often rely on external tools or manual calculations to track their experience gain rate. Zeal provides EQTypes to display this information directly.

**Proposed Implementation:**

- Add labels below the existing XP gauge to show XP/hour and AA/hour percentages.

**XML Snippets:**

```xml
<!-- ** ENHANCEMENT: XP Rate Label ** -->
<Label item ="IW_XPRate_Zeal">
    <ScreenID>XPRateLabel</ScreenID>
    <EQType>81</EQType> <!-- Zeal: XP/Hour % -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>122</Y> <!-- Below the XP Gauge -->
    </Location>
    <Size>
        <CX>116</CX>
        <CY>14</CY>
    </Size>
    <Text>XP/Hr: 12.34%</Text>
    <TextColor><R>220</R><G>150</G><B>0</B></TextColor>
    <NoWrap>true</NoWrap>
    <AlignCenter>true</AlignCenter>
</Label>

<!-- ** ENHANCEMENT: AA Rate Label ** -->
<Label item ="IW_AARate_Zeal">
    <ScreenID>AARateLabel</ScreenID>
    <EQType>86</EQType> <!-- Zeal: AA/Hour % -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>134</Y> <!-- Below the XP Rate Label -->
    </Location>
    <Size>
        <CX>116</CX>
        <CY>14</CY>
    </Size>
    <Text>AA/Hr: 1.23%</Text>
    <TextColor><R>220</R><G>150</G><B>0</B></TextColor>
    <NoWrap>true</NoWrap>
    <AlignCenter>true</AlignCenter>
</Label>
```
**Value Proposition:** Delivers immediate feedback on leveling efficiency, allowing players to optimize their strategies without leaving the game client.

### 3. Inventory Slot Counter

The default UI requires players to manually count free inventory slots. Zeal provides EQTypes to automate this.

**Proposed Implementation:**

- Add a simple text label near the bag slots showing `Free / Total` slots.

**XML Snippets:**

```xml
<!-- ** ENHANCEMENT: Inventory Slot Counter ** -->
<Label item ="IW_InvCount_Zeal">
    <ScreenID>InvCountLabel</ScreenID>
    <EQType>83</EQType> <!-- Zeal: Inventory Slots Free -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>330</X>
        <Y>144</Y> <!-- Above the main bag slots -->
    </Location>
    <Size>
        <CX>80</CX>
        <CY>14</CY>
    </Size>
    <Text>Slots: 12/80</Text>
    <TextColor><R>255</R><G>255</G><B>255</B></TextColor>
    <NoWrap>true</NoWrap>
    <AlignCenter>true</AlignCenter>
    <Template>L_V_Total</Template> <!-- Custom template to combine EQTypes -->
</Label>

<!-- Associated Template needed in EQUI_Templates.xml -->
<Label item = "L_V_Total">
    <ScreenID>L_V_Total</ScreenID>
    <Font>3</Font>
    <Text>Template</Text>
    <NoWrap>true</NoWrap>
    <AlignRight>false</AlignRight>
    <AlignLeft>true</AlignLeft>
    <EQType>84</EQType> <!-- Zeal: Inventory Slots Total -->
    <Combine>true</Combine>
    <Format>/%1.0f</Format>
</Label>
```
**Value Proposition:** A significant quality-of-life improvement that saves time and reduces tedious manual counting, especially during extended farming sessions.

### 4. Pet HP Gauge

For pet classes, tracking a pet's health is critical. Zeal allows for a dedicated pet HP gauge.

**Proposed Implementation:**

- Add a small gauge below the AA gauge to display the pet's current HP percentage.

**XML Snippets:**

```xml
<!-- ** ENHANCEMENT: Pet HP Gauge ** -->
<Gauge item = "IW_PetHPGauge_Zeal">
    <ScreenID>PetHPGauge</ScreenID>
    <EQType>69</EQType> <!-- Zeal: Pet HP % -->
    <RelativePosition>true</RelativePosition>
    <Location>
        <X>2</X>
        <Y>318</Y> <!-- Positioned at the bottom of the left column -->
    </Location>
    <Size>
        <CX>116</CX>
        <CY>8</CY>
    </Size>
    <FillTint><R>200</R><G>20</G><B>20</B></FillTint>
    <GaugeDrawTemplate>
        <Background>A_GaugeBackground</Background>
        <Fill>A_GaugeFill</Fill>
    </GaugeDrawTemplate>
</Gauge>
```
**Value Proposition:** Provides vital, at-a-glance pet status information, allowing pet classes to react more quickly in combat without needing to have the pet targeted.

## Implementation Roadmap

1.  **Create `thorne_zeal` Directory:** If it doesn't exist, create a `thorne_zeal` UI folder to house the modified file.
2.  **Copy `EQUI_Inventory.xml`:** Copy `default/EQUI_Inventory.xml` to `thorne_zeal/EQUI_Inventory.xml`.
3.  **Modify `EQUI_Templates.xml`:** Add the `L_V_Total` label template to `thorne_zeal/EQUI_Templates.xml` (or create the file if it doesn't exist).
4.  **Implement XML Changes:** Add the XML snippets from the sections above into `thorne_zeal/EQUI_Inventory.xml`.
    -   Remove the old HP labels (`IW_HP`, `IW_CurrentHP`, `IW_HPDivider`, `IW_MaxHP`).
    -   Add the new Zeal-specific labels and gauges.
    -   Adjust coordinates of existing elements (like AC/ATK labels) to accommodate the new Mana label.
5.  **Test In-Game:** Load the `thorne_zeal` UI in the EverQuest client and verify that all new elements display correctly and are populated with data.
