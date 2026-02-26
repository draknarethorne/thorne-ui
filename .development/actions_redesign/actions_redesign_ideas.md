# Actions Window Redesign Ideas (Research + Proposals)

_Date: 2026-02-26_

## What you asked

You wanted to know whether **other UI files use subwindows for the Actions window**, or whether there are variants that **do not** and instead draw items directly on the main `ActionsWindow` while tabs alone handle visibility.

## Short answer

- In the 53 `EQUI_ActionsWindow.xml` variants scanned in this workspace set, **all 53 use the tabbed subwindow model** (`ACTW_ActionsSubwindows`).
- I did **not** find a variant where action pages are shown/hidden without that tab container.
- However, important nuance: you do **not** need extra wrapper `Screen` containers for slots/buttons once you are on a tab page. You can place controls directly on a `Page` and let the tab system handle visibility.

## Evidence from scan

### Global pattern found in all scanned Actions variants

All found files include a `TabBox` for actions and wire it into the root window via:

- `<TabBox item="ACTW_ActionsSubwindows">`
- `<Pieces>ACTW_ActionsSubwindows</Pieces>` inside `<Screen item="ActionsWindow">`

Examples:

- `c:\TAKP\uifiles\default\EQUI_ActionsWindow.xml`
- `c:\TAKP\uifiles\QQ\EQUI_ActionsWindow.xml`
- `c:\TAKP\uifiles\Nillipuss\EQUI_ActionsWindow.xml`
- `c:\TAKP\uifiles\duxaUI\EQUI_ActionsWindow.xml`
- `c:\Thorne-UI\thorne_drak\EQUI_ActionsWindow.xml`

### Page model is also universal

Scanned variants consistently define pages such as:

- `ActionsMainPage`
- `ActionsCombatPage`
- `ActionsAbilitiesPage`
- `ActionsSocialsPage`

This indicates tabs/pages are the standard Actions architecture, not a custom invention.

## Clarification: “subwindow” types

There are two concepts that get mixed together:

1. **Tab system container (`TabBox` + `Page`)**
   - Needed for tabbed visibility behavior.
   - This is what virtually all Actions windows use.

2. **Extra wrapper `Screen` groups inside pages**
   - Optional.
   - Often used for grouping/layout, but not strictly required.
   - You can place `InvSlot` and buttons directly on `Page` pieces.

So: if your concern is fading/render side-effects from additional wrappers, you can keep tabs while avoiding extra wrapper screens in the hot areas.

## Design proposals

## Proposal A — Single Actions TabBox, direct placement on pages (recommended)

**Goal:** keep standard tab behavior, remove avoidable wrapper complexity.

### Structure

- Keep one `ACTW_ActionsSubwindows` `TabBox`.
- Keep/reorder pages to match gameplay priority.
- Put `InvSlot`/buttons directly on each page’s `<Pieces>` list.
- Avoid transparent wrapper `Screen` layers for slots.

### Suggested page set

1. `ActionsMainPage` (trimmed utility)
2. `ActionsCombatAbilitiesPage` (merged combat + abilities)
3. `ActionsSocialsPage`
4. `ActionsBagsPage` (bag slots)
5. `ActionsWornPage` (worn/equipment slots)

### Why this fits your goals

- Preserves tab UX users already expect.
- Eliminates extra wrapper dependency where fading can happen.
- Frees “Player/Info” real estate for high-value inventory pages.

## Proposal B — Keep dual-tabbox architecture, but direct-slot pages only

**Goal:** lower migration risk while improving rendering confidence.

### Structure

- Keep both existing tab boxes (`ACTW_ActionsSubwindows`, `ACTW_InventorySubwindows`) for compatibility.
- Refactor inventory pages so slot controls are directly listed in page pieces.
- Reduce nested `Screen` usage to non-interactive decoration only.

### Tradeoff

- Safer incremental rollout.
- Slightly more complex XML than Proposal A.

## Proposal C — Aggressive consolidation + priority-first tab order

**Goal:** optimize click-path for frequent combat/inventory actions.

### Structure

- Merge `Combat` + `Abilities` into one page.
- Remove or repurpose low-value page (`Info`/`Player`) into inventory utility.
- Final order example:
  1. Combat+Abilities
  2. Bags
  3. Worn
  4. Socials
  5. Main (utility)

### Tradeoff

- Highest usability upside.
- Largest behavioral change for users accustomed to legacy order.

## Proposal D — Keep baseline architecture, only visual/size improvements

**Goal:** smallest change footprint.

### Structure

- No tab structure changes.
- Keep all pages but enlarge high-value controls and tighten spacing.
- Optionally move one inventory page into Actions with direct page placement.

### Tradeoff

- Lowest risk, fastest ship.
- Doesn’t fully capitalize on available page real estate.

## Recommended next implementation path

1. Start from **Proposal A**.
2. Create merged `Combat+Abilities` page.
3. Repurpose freed page(s) into `Bags` and `Worn` with direct `InvSlot` placement.
4. Keep tabs, avoid extra wrapper screens for slot clusters.
5. Validate in-game focus areas:
   - visibility/no fade on slots
   - click hitbox consistency
   - tab order speed in combat

## Direct answer to your “invented” concern

For Actions specifically: based on scanned variants here, **tabbed subwindow usage is standard across all observed files**. The part you can still simplify is **how much extra wrapping you do inside those pages**.
