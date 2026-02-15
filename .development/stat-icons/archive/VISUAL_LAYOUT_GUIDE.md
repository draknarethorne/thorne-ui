bre# Stat Icon Master Template - Visual Layout Guide

**Generated:** 2026-02-10  
**Format:** All files use 256×256 RGBA, 22×22 icons

---

## Visual Grid Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│  STAT ICON MASTER TEMPLATE - 256×256 RGBA                                 │
│  All three files (pieces01, pieces02, pieces03) use this layout           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│    COLUMN 1 (X=10)      COLUMN 2 (X=90)      COLUMN 3 (X=170)            │
│    Player/Combat        Resistances          Character Attrs              │
│    ═══════════════      ═══════════════      ═══════════════             │
│                                                                            │
│ Row 1 (Y=10):                                                             │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │    AC    │          │   FIRE   │          │   STR    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Armor Class           Fire Resist          Strength                   │
│                                                                            │
│ Row 2 (Y=40):                                                             │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │   ATK    │          │   COLD   │          │   INT    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Attack                Cold Resist          Intelligence               │
│                                                                            │
│ Row 3 (Y=70):                                                             │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │    HP    │          │  MAGIC   │          │   WIS    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Hit Points            Magic Resist         Wisdom                     │
│                                                                            │
│ Row 4 (Y=100):                                                            │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │   MANA   │          │  POISON  │          │   AGI    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Mana Points           Poison Resist        Agility                    │
│                                                                            │
│ Row 5 (Y=130):                                                            │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │   STA    │          │ DISEASE  │          │   DEX    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Stamina               Disease Resist       Dexterity                  │
│                                                                            │
│ Row 6 (Y=160):                                                            │
│    ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│    │  WEIGHT  │          │ RESERVE  │          │   CHA    │              │
│    │  22×22   │          │  22×22   │          │  22×22   │              │
│    └──────────┘          └──────────┘          └──────────┘              │
│    Character Weight      Future Use           Charisma                   │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Coordinate Quick Reference

### Column 1: Player/Combat Stats (X=10)
| Row | Y   | Icon   | Label            |
|-----|-----|--------|------------------|
| 1   | 10  | AC     | Armor Class      |
| 2   | 40  | ATK    | Attack           |
| 3   | 70  | HP     | Hit Points       |
| 4   | 100 | MANA   | Mana             |
| 5   | 130 | STA    | Stamina          |
| 6   | 160 | Weight | Character Weight |

### Column 2: Resistances (X=90)
| Row | Y   | Icon    | Label             |
|-----|-----|---------|-------------------|
| 1   | 10  | Fire    | Fire Resistance   |
| 2   | 40  | Cold    | Cold Resistance   |
| 3   | 70  | Magic   | Magic Resistance  |
| 4   | 100 | Poison  | Poison Resistance |
| 5   | 130 | Disease | Disease Resist.   |
| 6   | 160 | Reserve | Future/Reserved   |

### Column 3: Character Attributes (X=170)
| Row | Y   | Icon | Label        |
|-----|-----|------|--------------|
| 1   | 10  | STR  | Strength     |
| 2   | 40  | INT  | Intelligence |
| 3   | 70  | WIS  | Wisdom       |
| 4   | 100 | AGI  | Agility      |
| 5   | 130 | DEX  | Dexterity    |
| 6   | 160 | CHA  | Charisma     |

---

## File Content Comparison

### Legend
- ✅ **Real Icon** - Extracted from source texture
- ○ **Placeholder** - Subtle gray box with X mark

### stat_icon_pieces01.tga (Vert Icons)

```
    COL 1       COL 2       COL 3
    ─────       ─────       ─────
R1  ✅ AC       ✅ Fire     ✅ STR
R2  ✅ ATK      ✅ Cold     ✅ INT
R3  ○ HP        ✅ Magic    ✅ WIS
R4  ○ MANA      ✅ Poison   ○ AGI
R5  ○ STA       ✅ Disease  ○ DEX
R6  ○ Weight    ○ Reserve   ○ CHA

Real Icons: 10/18
Source: vert/window_pieces06.tga
```

### stat_icon_pieces02.tga (Vert-Blue Resists)

```
    COL 1       COL 2       COL 3
    ─────       ─────       ─────
R1  ○ AC        ✅ Fire     ○ STR
R2  ○ ATK       ✅ Cold     ○ INT
R3  ○ HP        ✅ Magic    ○ WIS
R4  ○ MANA      ✅ Poison   ○ AGI
R5  ○ STA       ✅ Disease  ○ DEX
R6  ○ Weight    ○ Reserve   ○ CHA

Real Icons: 5/18 (Column 2 only)
Source: vert-blue/gemicons01.tga (24×24→22×22)
```

### stat_icon_pieces03.tga (Default Resists)

```
    COL 1       COL 2       COL 3
    ─────       ─────       ─────
R1  ○ AC        ✅ Fire     ○ STR
R2  ○ ATK       ✅ Cold     ○ INT
R3  ○ HP        ✅ Magic    ○ WIS
R4  ○ MANA      ✅ Poison   ○ AGI
R5  ○ STA       ✅ Disease  ○ DEX
R6  ○ Weight    ○ Reserve   ○ CHA

Real Icons: 5/18 (Column 2 only)
Source: default/gemicons01.tga (24×24→22×22)
```

---

## Swappability Example

Since all three files use **identical coordinates**, you can swap files without changing XML:

### XML Animation (Works with ANY of the three files)

```xml
<!-- Fire Resist Icon -->
<Ui2DAnimation item="A_FireResistIcon">
  <!-- Try ANY of these three textures: -->
  <Texture>stat_icon_pieces01.tga</Texture>
  <!-- <Texture>stat_icon_pieces02.tga</Texture> -->
  <!-- <Texture>stat_icon_pieces03.tga</Texture> -->
  
  <!-- Coordinates stay the same! -->
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

Simply change the `<Texture>` line to switch icon styles!

---

## Spacing Measurements

```
       10px    22px     58px    22px     58px    22px     34px
    ├────┼────────────┼────┼────────────┼────┼────────────┼────┤
    │    │  Column 1  │    │  Column 2  │    │  Column 3  │    │
    │    │  (X=10)    │    │  (X=90)    │    │  (X=170)   │    │
    ├────┼────────────┼────┼────────────┼────┼────────────┼────┤
    
Vertical spacing:
    Y=10   ─┬─  Row 1 (22px icon)
    Y=32    │ 8px gap
    Y=40   ─┼─  Row 2 (22px icon)
    Y=62    │ 8px gap
    Y=70   ─┼─  Row 3 (22px icon)
    Y=92    │ 8px gap
    Y=100  ─┼─  Row 4 (22px icon)
    Y=122   │ 8px gap
    Y=130  ─┼─  Row 5 (22px icon)
    Y=152   │ 8px gap
    Y=160  ─┴─  Row 6 (22px icon)
    Y=182
    
Total height: 182px (icons + gaps)
Canvas size: 256×256 (lots of space for future expansion)
```

---

## Usage Patterns

### All Stats from pieces01
```xml
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<Ui2DAnimation item="A_ATKIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>40</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<Ui2DAnimation item="A_FireIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

### Mixed: Stats from pieces01, Resists from pieces02
```xml
<!-- Stat icons from pieces01 -->
<Ui2DAnimation item="A_ACIcon">
  <Texture>stat_icon_pieces01.tga</Texture>
  <Location><X>10</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>

<!-- Resist icons from pieces02 (vert-blue style) -->
<Ui2DAnimation item="A_FireIcon">
  <Texture>stat_icon_pieces02.tga</Texture>
  <Location><X>90</X><Y>10</Y></Location>
  <Size><CX>22</CX><CY>22</CY></Size>
</Ui2DAnimation>
```

---

## Master Coordinate Table (Complete Reference)

| Icon    | X   | Y   | Row | Col | pieces01 | pieces02 | pieces03 |
|---------|-----|-----|-----|-----|----------|----------|----------|
| AC      | 10  | 10  | 1   | 1   | ✅       | ○        | ○        |
| ATK     | 10  | 40  | 2   | 1   | ✅       | ○        | ○        |
| HP      | 10  | 70  | 3   | 1   | ○        | ○        | ○        |
| MANA    | 10  | 100 | 4   | 1   | ○        | ○        | ○        |
| STA     | 10  | 130 | 5   | 1   | ○        | ○        | ○        |
| Weight  | 10  | 160 | 6   | 1   | ○        | ○        | ○        |
| Fire    | 90  | 10  | 1   | 2   | ✅       | ✅       | ✅       |
| Cold    | 90  | 40  | 2   | 2   | ✅       | ✅       | ✅       |
| Magic   | 90  | 70  | 3   | 2   | ✅       | ✅       | ✅       |
| Poison  | 90  | 100 | 4   | 2   | ✅       | ✅       | ✅       |
| Disease | 90  | 130 | 5   | 2   | ✅       | ✅       | ✅       |
| Reserve | 90  | 160 | 6   | 2   | ○        | ○        | ○        |
| STR     | 170 | 10  | 1   | 3   | ✅       | ○        | ○        |
| INT     | 170 | 40  | 2   | 3   | ✅       | ○        | ○        |
| WIS     | 170 | 70  | 3   | 3   | ✅       | ○        | ○        |
| AGI     | 170 | 100 | 4   | 3   | ○        | ○        | ○        |
| DEX     | 170 | 130 | 5   | 3   | ○        | ○        | ○        |
| CHA     | 170 | 160 | 6   | 3   | ○        | ○        | ○        |

**Legend:**  
✅ = Real icon extracted from source  
○ = Placeholder (subtle gray box)

---

## Validation Status

```
✅ ALL FILES VALIDATED (2026-02-10)

stat_icon_pieces01.tga: ✅ PASS (18/18 positions)
stat_icon_pieces02.tga: ✅ PASS (18/18 positions)
stat_icon_pieces03.tga: ✅ PASS (18/18 positions)

Cross-File Consistency: ✅ PASS
Swappability Confirmed: ✅ YES
```

Run `python .bin/validate_stat_icons.py` to revalidate anytime.

---

**This is the definitive visual reference for all stat icon positioning.**  
For detailed documentation, see [README.md](README.md) and [stat_icon_MASTER_LAYOUT.md](stat_icon_MASTER_LAYOUT.md)
