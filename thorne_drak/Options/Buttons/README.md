# 🔘 Button Texture Options

**Version**: 0.7.2  
**Last Updated**: March 4, 2026  
**Author**: Draknare Thorne

---

## Overview

Button texture variants control the visual appearance of hotbar and action buttons. Each variant provides three texture files that define button states (normal, pressed, hover).

## Variants

| Variant | Description |
|---------|-------------|
| **Ghost** | Semi-transparent buttons — subtle presence, minimal visual weight |
| **Phantom** | Near-invisible buttons — maximum screen clarity, buttons appear on hover |
| **Thorne** | Standard visibility — balanced between form and function *(default)* |

## Files

Each variant contains:
- `buttons_dark_thorne01.tga` — Dark button state texture
- `buttons_eclipse_thorne01.tga` — Eclipse/hover state texture
- `buttons_light_thorne01.tga` — Light/pressed state texture

## Usage

Copy all three `.tga` files from the desired variant to `thorne_drak/` root:

```bash
sync-option.bat Buttons/Ghost
```

Or manually copy files and reload with `/loadskin thorne_drak 1`.

---

**Maintainer**: Draknare Thorne
