# Cast Spell Window Options

## Overview

This directory contains variants for the Cast Spell Window (EQUI_CastSpellWnd.xml).

**Last Synced:** 2026-02-09  
**Git Commit:** TBD

---

## Available Variants

- **[Default/](Default/)**    
  `EQUI_CastSpellWnd.xml` - Custom button-based spell gems with enhanced visibility

- **[Standard/](Standard/)**  📄
  `EQUI_CastSpellWnd.xml` - Original spell gem graphics (compact 140px width)

---

## Variant Comparison

| Feature | Default (Custom Buttons) | Standard (Original Gems) |
|---------|--------------------------|--------------------------|
| **Window Width** | 160px | 140px |
| **Spell Gem Size** | 150×24px (uniform) | Mixed 31×23px and 138×23px |
| **Graphics Style** | Custom button textures | Standard spell gem sprites |
| **Textures Used** | button_pieces01.tga, button_pieces01_light.tga | Standard A_SpellGemHolder/Background |
| **Visibility** | Enhanced (high contrast buttons) | Standard (traditional gem appearance) |
| **Spell Name Display** | Better (wider layout, less truncation) | Standard (may truncate long names) |
| **Use Case** | Preferred for wider spell window visibility | Traditional compact EverQuest appearance |

---

## Default Configuration

The `Default/` directory contains the current synchronized backup of the main working file from `thorne_drak/EQUI_CastSpellWnd.xml`.

**Current Active Variant**: Custom Button-Based Spell Gems (Default)

**Design Philosophy**: The default variant uses custom button-style spell gem graphics to enhance visibility in the cast spell window. The wider layout (160px vs 140px) provides better spell name readability while maintaining the classic vertical spell bar organization.

---

## Metadata

See [.sync-status.json](.sync-status.json) for detailed sync metadata including:
- Last sync date and commit
- Sync status (in_sync: true/false)
- Window description

---

**Part of:** [Thorne UI Options System](../../.docs/options-sync/)
