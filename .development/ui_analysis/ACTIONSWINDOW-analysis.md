# Actions Window Analysis: Nillipuss vs. Thorne

## Summary

**Nillipuss has RESISTANCE ICONS** that Thorne lacks! Both windows display extensive stats (STR, STA, AGI, DEX, INT, WIS, CHA, AC, ATK, resistances), but Nillipuss uses ICONS for resistances while Thorne uses text-only. This is **directly relevant** to the stat-icons implementation plan.

---

## EQType Validation (Stats & Resists)

**Thorne (Label EQTypes):**
- STR **5**, STA **6**, DEX **7**, AGI **8**, WIS **9**, INT **10**, CHA **11**
- Poison **12**, Disease **13**, Fire **14**, Cold **15**, Magic **16**
- AC **22**, ATK **23**, Weight **24/25**
- HP values **70**, Mana values **80**, AA current/total **36/37**

**Nillipuss (Label EQTypes):**
- Uses the **same EQTypes** for stats and resistances (e.g., CR **15**, DR **13**, FR **14**, MR **16**, PR **12**)
- Includes additional label elements (e.g., `STR`, `STA`, `FR`, `CR`, etc.) that are **label-only** and share the same EQTypes

**Important**: Resistance icons are **StaticAnimation** elements and **do not use EQType**. The EQType is still carried by the numeric labels (e.g., `SvCnum`, `SvFnum`, etc.).

### Hidden/Unreferenced EQType Elements (Nillipuss)
The following numeric labels are **not referenced by any Screen/Page pieces** and appear unused/legacy:
`STRnum`, `STAnum`, `AGInum`, `DEXnum`, `WISnum`, `CHAnum`, `INTnum`, `SvPnum`, `SvMnum`, `SvDnum`, `SvFnum`, `SvCnum`, `ATKnum`, `ACnum`, `WGT`.

## Window Files
- Nillipuss: `EQUI_ActionsWindow.xml` (63,842 bytes - very large!)
- Thorne: `EQUI_ActionsWindow.xml` (estimated ~40-50KB)

## Element Inventory Comparison

### Common Elements (In Both)
**Character Stats (ALL in both, text format):**
- `STRnum`, `STRtxt` - Strength display
- `STAnum`, `STAtxt` - Stamina display
- `AGInum`, `AGItxt` - Agility display
- `DEXnum`, `DEXtxt` - Dexterity display
- `INTnum`, `INTtxt` - Intelligence display
- `WISnum`, `WIStxt` - Wisdom display
- `CHAnum`, `CHAtxt` - Charisma display
- `ACnum`, `ACtxt` - Armor Class display
- `ATKnum`, `ATKtxt` - Attack display
- `SvCnum`, `SvCtxt` - Save vs. Cold
- `SvDnum`, `SvDtxt` - Save vs. Disease
- `SvFnum`, `SvFtxt` - Save vs. Fire
- `SvMnum`, `SvMtxt` - Save vs. Magic
- `SvPnum`, `SvPtxt` - Save vs. Poison

**Ability Buttons (In Both):**
- `AAP_FirstAbilityButton` through `AAP_SixthAbilityButton` - AA abilities (6 buttons)
- `ACP_FirstAbilityButton` through `ACP_FourthAbilityButton` - Combat abilities (4 buttons)
- `ACP_MeleeAttackButton`, `ACP_RangeAttackButton` - Attack mode buttons

**Movement Buttons (In Both):**
- `AMP_SitButton`, `AMP_StandButton` - Sit/Stand
- `AMP_WalkButton`, `AMP_RunButton` - Walk/Run toggle
- `AMP_CampButton` - Camp/return to bind
- `AMP_InviteButton`, `AMP_DisbandButton`, `AMP_FollowButton`, `AMP_WhoButton` - Group commands

**Social Buttons (In Both):**
- `ASP_SocialButton1` through `ASP_SocialButton12` - 12 social buttons
- `ASP_SocialPageLeftButton`, `ASP_SocialPageRightButton` - Page navigation
- `ASP_CurrentSocialPageLabel` - Page indicator

### Elements in Nillipuss ONLY ⭐

**CRITICAL MISSING FEATURES IN THORNE:**

1. **`CRIcon`, `DRIcon`, `FRIcon`, `MRIcon`, `PRIcon`** (StaticAnimation or similar)
   - **What**: RESISTANCE ICONS for Cold, Disease, Fire, Magic, Poison
   - **Why It Matters**: 🔴 **HIGHEST PRIORITY** - This is EXACTLY what user wants for stat-icons!
   - **User Request**: YES - stat-icons implementation
   - **Complexity**: LOW - icons already exist in shared textures
   - **Implementation**: Port resistance icon display logic from Nillipuss

2. **Resistance Display Method:**
   - `CR`, `DR`, `FR`, `MR`, `PR` - Likely Screen pieces containing resistances
   - `CRIcon` through `PRIcon` - Icon graphics
   - Nillipuss shows ICON + VALUE for each resistance

3. **Additional Stat Labels:**
   - `STRLabel`, `STALabel`, `AGILabel`, `DEXLabel`, `INTLabel`, `WISLabel`, `CHALabel` - Stat name labels
   - `ACLabel`, `ATKLabel` - AC/ATK labels
   - `WGTLabel` - Weight label
   - Note: Thorne may have equivalent with different naming

4. **`AMP_FindButton`, `AMP_EndFindButton`** (Buttons)
   - **What**: Find/End tracking buttons
   - **Why It Matters**: MEDIUM PRIORITY - Convenience feature
   - **Complexity**: LOW - two buttons

5. **Cosmetic/Branding Elements:**
   - `Harambe`, `RiseApes`, `Rustle2`, `Rustle-logo`, `version` - Likely decorative/branding
   - LOW PRIORITY - Not functional

6. **Other Elements:**
   - `AC`, `AGI`, `ATK`, `CHA`, `DEX`, `INT`, `STA`, `STR`, `WGT`, `WIS` - Likely Screen pieces or additional labels
   - May be duplicates or organizational containers

### Elements in Thorne ONLY

**Additional Features in Thorne:**

1. **`ACTW_*` Prefix Elements** - Thorne uses organized naming convention:
   - `ACTW_AADivider`, `ACTW_AALabel` - AA section headers
   - `ACTW_ACLabel`, `ACTW_ATKLabel` - Stat section labels
   - `ACTW_CurrentAA`, `ACTW_MaxAA` - AA point display
   - `ACTW_CurrentAC`, `ACTW_CurrentATK` - Current stat values
   - `ACTW_CurrentHP`, `ACTW_CurrentMana` - HP/Mana displays
   - `ACTW_CurrentWeight`, `ACTW_MaxWeight`, `ACTW_WeightDivider`, `ACTW_WeightLabel` - Weight display
   - `ACTW_HP`, `ACTW_Mana` - HP/Mana gauges or labels
   - `ACTW_Level`, `ACTW_LevelLabel` - Level display
   - `ACTW_PlayerClass`, `ACTW_PlayerName` - Character info

## Stat Display Comparison

| Stat Type | Nillipuss | Thorne | Display Method |
|---|---|---|---|
| **Primary Stats** (STR, STA, etc.) | Text (num + txt) | Text (num + txt) | Same - text only |
| **Resistances** | 🌟 **ICON + TEXT** | Text only (num + txt) | Nillipuss has icons! |
| **AC / ATK** | Text | Text | Same - text only |
| **HP / Mana** | Likely text | Text + possibly gauges | Similar |
| **AA Points** | Unknown | Text display | Thorne may be more detailed |
| **Weight** | Text (`WGT`) | Text (`ACTW_Weight*`) | Both have |

## Resistance Icon Implementation in Nillipuss

### How Nillipuss Displays Resistance Icons

Based on element names, Nillipuss likely uses a pattern like:
```xml
<!-- Resistance Icon (Static Animation referencing texture) -->
<StaticAnimation item="CRIcon">
  <ScreenID>CRIcon</ScreenID>
  <Animation>ICON_CR</Animation>
  <RelativePosition>true</RelativePosition>
  <Location><X>?</X><Y>?</Y></Location>
  <Size><CX>16</CX><CY>16</CY></Size>
</StaticAnimation>

<!-- Resistance Value (Numeric text) -->
<Label item="SvCnum">
  <ScreenID>SvCnum</ScreenID>
  <Font>2</Font>
  <EQType>?</EQType>  <!-- Resistance EQType -->
  <Text>100</Text>
  <!-- ... positioning next to icon ... -->
</Label>
```

Pattern: ICON + VALUE positioned together for each resistance.

## Recommendations for Thorne Stat-Icons

### User Direction
User stated:
> "I am thinking that I could adjust my Actions window to include the stat-icons instead of the player window (since I already have stats on there)"

### Current Thorne ActionsWindow Layout

Thorne ActionsWindow displays:
- Character name, class, level (top)
- Primary stats: STR, STA, AGI, DEX, INT, WIS, CHA (text labels + values)
- Combat stats: AC, ATK (text labels + values)
- Resistances: SvC, SvD, SvF, SvM, SvP (text labels + values)
- HP, Mana, Weight displays
- AA points (current/max)
- Ability buttons (AA, Combat, Movement, Social)

### Stat-Icons Implementation Strategy

**Phase 1: Add Resistance Icons (v0.7.0)** 🎯

Port the resistance icon display from Nillipuss:
1. Define icon animations (`ICON_CR`, `ICON_DR`, `ICON_FR`, `ICON_MR`, `ICON_PR`)
2. Add `StaticAnimation` elements for each resistance
3. Position icons next to existing resistance text
4. Alternative: Replace text with icon-only or icon+text hybrid

**Texture Requirements:**
- Resistance icons likely in shared textures (window_pieces or classic_pieces01.tga)
- May need to check Nillipuss texture usage or create new icons in `stat_icon_pieces01.tga`

Example implementation:
```xml
<!-- Cold Resistance Icon -->
<StaticAnimation item="ACTW_CRIcon">
  <Animation>ICON_RESIST_COLD</Animation>
  <Location><X>10</X><Y>120</Y></Location>
  <Size><CX>16</CX><CY>16</CY></Size>
</StaticAnimation>

<!-- Cold Resistance Value -->
<Label item="SvCnum">
  <Location><X>28</X><Y>122</Y></Location> <!-- Next to icon -->
  <Size><CX>30</CX><CY>12</CY></Size>
  <!-- ... -->
</Label>
```

**Phase 2: Add Primary Stat Icons (v0.7.0 or v0.8.0)**

After resistance icons proven successful, add icons for:
- STR, STA, AGI, DEX, INT, WIS, CHA
- AC, ATK

**Layout Options:**

**Option A: Icon + Text (Hybrid)**
```
[STR Icon] 185  [DEX Icon] 120
[STA Icon] 150  [AGI Icon] 110
[INT Icon] 200  [WIS Icon] 195
[CHA Icon] 100
```

**Option B: Icons Only (Compact)**
```
[STR:185] [DEX:120] [AGI:110]
[STA:150] [INT:200] [WIS:195]
[CHA:100] [AC:1200] [ATK:850]
```

**Option C: Separate Variants**
Create `Options/Actions/` variants:
- `Default` - Current text-only (existing)
- `With Stat Icons` - Icons + text
- `Icons Only` - Compact icon-based

### Space Analysis

**Current Thorne ActionsWindow:**
- Multiple stat display areas
- Social buttons section
- Ability buttons section
- Movement buttons section

**Space Available for Icons:**
- User mentioned: "might mean I need to increase the height and re-organize my stats or have smaller icons"
- Options:
  1. **Smaller icons** (12x12px or 14x14px instead of 16x16px)
  2. **Increase window height** (add 20-40px)
  3. **Reorganize layout** (more compact stat grid)

**Recommended Approach:**
Start with resistance icons (easiest, most impactful). If successful and space allows, expand to primary stats.

## Missing Feature Priority for Stat-Icons

| Feature | Priority | Complexity | v0.7.0? |
|---|---|---|---|
| **Resistance Icons (CR, DR, FR, MR, PR)** | 🔴 **HIGHEST** | LOW | ✅ YES |
| **Primary Stat Icons (STR, DEX, etc.)** | 🟡 MEDIUM | MEDIUM | Maybe |
| **AC/ATK Icons** | 🟢 LOW | LOW | Maybe |
| **Find/EndFind buttons** | 🟢 LOW | LOW | Optional |

## Implementation Plan for v0.7.0

### Step 1: Research & Texture Preparation
1. Read Nillipuss `EQUI_ActionsWindow.xml` to find icon definitions
2. Identify texture file(s) containing resistance icons
3. Add resistance icons to `stat_icon_pieces01.tga` (or use existing textures)
4. Create animation definitions in `EQUI_Animations.xml`

### Step 2: Add Resistance Icons to Thorne ActionsWindow
1. Define `ACTW_CRIcon` through `ACTW_PRIcon` StaticAnimation elements
2. Position icons next to existing resistance values
3. Test layout and adjust spacing
4. Create variant with icon+text hybrid

### Step 3: Create Options Variants
1. `Options/Actions/Default/` - Current text-only (copy existing)
2. `Options/Actions/With Resistance Icons/` - Add resistance icons
3. `Options/Actions/Full Stat Icons/` - All stats with icons (stretch goal)

### Step 4: Documentation
1. Update `Options/Actions/README.md` with variant descriptions
2. Add screenshots showing icon layouts
3. Document in stat-icons plan

## Conclusion

Nillipuss ActionsWindow provides the **perfect reference implementation** for stat-icons in Thorne! The resistance icons (`CRIcon`, `DRIcon`, `FRIcon`, `MRIcon`, `PRIcon`) are exactly what the user wants.

**Key Findings:**
✅ Nillipuss HAS resistance icons (Thorne doesn't)  
✅ User wants stat-icons on ActionsWindow (this is the right target!)  
✅ Resistance icons are LOW complexity to add  
✅ Can expand to primary stats (STR, DEX, etc.) if space allows  

**Immediate Action for v0.7.0:**
1. Port resistance icon implementation from Nillipuss
2. Add as ActionsWindow variant (icon+text hybrid)
3. Test and refine layout
4. Expand to full stat icons if successful

This aligns PERFECTLY with the user's stated goal of making "thorne_drak BETTER than Nilli" by combining Nillipuss's icon approach with Thorne's organized architecture!
