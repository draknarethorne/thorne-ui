from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps


ROOT = Path("C:/Thorne-UI")
SOURCE_ICON = ROOT / "thorne_drak" / "thorne_drak01.tga"
SOURCE_JPG = ROOT / "thorne_drak" / "thorne_drak01.jpg"
BUTTON_SOURCE = ROOT / "thorne_drak" / "button_clean_from_bow.tga"  # Clean button from window_pieces02
OUT_ATLAS = ROOT / "thorne_drak" / "thorne_icons_slots01.tga"

# Hand-editable source files for workflow
SOURCE_ICON_FILE = ROOT / "thorne_drak" / "thorne_icon.tga"
SOURCE_BUTTONS_FILE = ROOT / "thorne_drak" / "thorne_buttons01.tga"

# Source file crop positions (where icon and button are located in source files)
ICON_X, ICON_Y = 2, 2
BUTTON1_X, BUTTON1_Y = 2, 2      # Smooth gradient button
BUTTON2_X, BUTTON2_Y = 48, 2    # Dramatic gradient button

ATLAS_SIZE = 255

# Layout: 3 columns (grayscale | button1_blend | button2_blend), test rows
# Column 1: X=2 (grayscale icon)
# Column 2: X=46 (blended with button1 smooth)
# Column 3: X=90 (blended with button2 dramatic)
X_COL1_GRAY = 2
X_COL2_BTN1 = 46
X_COL3_BTN2 = 90
Y_START = 2
GAP = 2

# Background extraction thresholds for producing a truly clear icon from JPG
L_LOW, L_HIGH = 165.0, 245.0
S_MAX = 55.0


@dataclass
class Variant:
    name: str
    img40: Image.Image
    img20: Image.Image


def make_40_from_source(src: Image.Image) -> Image.Image:
    # Downsample + sharpen for crisper small icon definition
    img = src.resize((40, 40), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=220, threshold=2))

    # Slight alpha tightening for crisper edges
    r, g, b, a = img.split()
    a = ImageEnhance.Contrast(a).enhance(1.2)
    return Image.merge("RGBA", (r, g, b, a))


def load_icon_40(icon_source: Image.Image, x: int, y: int) -> Image.Image:
    """Extract and prepare 40x40 icon from source file."""
    icon = icon_source.crop((x, y, x + 40, y + 40)).convert("RGBA")
    
    # Sharpen for crisper edges
    rgb = icon.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.0, percent=220, threshold=2))
    a = ImageEnhance.Contrast(icon.split()[3]).enhance(1.25)
    return Image.merge("RGBA", (*rgb.split(), a))


def apply_inner_feather_mask(icon: Image.Image, margin: int = 3, feather: int = 1) -> Image.Image:
    """Keep button border visible by tapering icon alpha near outer edge."""
    icon = icon.convert("RGBA")
    w, h = icon.size

    inner = Image.new("L", (w, h), 0)
    # Inner rectangle where icon can remain strongest
    x0, y0 = margin, margin
    x1, y1 = w - margin - 1, h - margin - 1
    for y in range(max(0, y0), min(h, y1 + 1)):
        for x in range(max(0, x0), min(w, x1 + 1)):
            inner.putpixel((x, y), 255)

    if feather > 0:
        inner = inner.filter(ImageFilter.GaussianBlur(radius=feather))

    r, g, b, a = icon.split()
    a = ImageChops.multiply(a, inner)
    return Image.merge("RGBA", (r, g, b, a))


def make_20_from_40(img40: Image.Image) -> Image.Image:
    img20 = img40.resize((20, 20), Image.LANCZOS)
    img20 = img20.filter(ImageFilter.UnsharpMask(radius=0.8, percent=200, threshold=2))
    return img20


def make_gray_lit(icon40: Image.Image, brightness_bias: float = 1.0, enhance_center: bool = False) -> Image.Image:
    """Create grayscale with light source and center-to-edge depth gradient."""
    rgba = icon40.convert("RGBA")
    rgb = rgba.convert("RGB")
    alpha = rgba.split()[3]

    gray = ImageOps.grayscale(rgb)
    w, h = gray.size
    gp = gray.load()
    ap = alpha.load()

    # Normalize grayscale over visible pixels so we can target a stable tonal range
    g_vals = []
    for y in range(h):
        for x in range(w):
            if ap[x, y] > 8:
                g_vals.append(gp[x, y])
    g_min = min(g_vals) if g_vals else 0
    g_max = max(g_vals) if g_vals else 255
    g_span = max(1, g_max - g_min)

    # Light focus mapped from source reference point: (126,132) on 255x255 (dragon eye area)
    lx = ((126.0 / 255.0) * (w - 1))
    ly = ((132.0 / 255.0) * (h - 1))
    max_d = ((w * w + h * h) ** 0.5)

    out = Image.new("RGBA", (w, h))
    op = out.load()

    for y in range(h):
        top_light = 1.0 - (y / max(1, h - 1))  # 1 at top, 0 at bottom
        for x in range(w):
            g = gp[x, y]
            a = ap[x, y]

            dx = x - lx
            dy = y - ly
            d = (dx * dx + dy * dy) ** 0.5
            radial = max(0.0, 1.0 - (d / max_d))

            # tonal shaping toward user-targeted range
            g_norm = (g - g_min) / g_span
            if g_norm < 0.0:
                g_norm = 0.0
            elif g_norm > 1.0:
                g_norm = 1.0
            
            if enhance_center:
                # Pronounced radial gradient: bright center, dark edges (outline effect)
                base = 40.0 + g_norm * 35.0
                lift = 0.8 * top_light + 5.5 * radial  # Strong radial lift for depth
            else:
                # Softer gradient
                base = 47.0 + g_norm * 24.0
                lift = 1.2 * top_light + 2.5 * radial
            
            v = int(max(0, min(255, (base + lift) * brightness_bias)))
            op[x, y] = (v, v, v, a)

    return out


def blend_on_button(icon: Image.Image, button40: Image.Image, icon_opacity: float, darken_bg: float = 1.0) -> Image.Image:
    base = button40.convert("RGBA")

    if abs(darken_bg - 1.0) > 1e-6:
        rgb = base.convert("RGB")
        rgb = ImageEnhance.Brightness(rgb).enhance(darken_bg)
        a = base.split()[3]
        base = Image.merge("RGBA", (*rgb.split(), a))

    ico = icon.convert("RGBA")
    ir, ig, ib, ia = ico.split()
    ia = ia.point(lambda v: int(v * icon_opacity))
    ico = Image.merge("RGBA", (ir, ig, ib, ia))

    out = base.copy()
    out.alpha_composite(ico, (0, 0))
    return out


def build_variants(icon40: Image.Image) -> list[Variant]:
    # Pipeline: source icon -> grayscale light variants
    clear40 = icon40

    # Start with just one variant for testing
    gray_dim = make_gray_lit(clear40, brightness_bias=1.12, enhance_center=False)

    # Build 20px versions
    gray_dim_20 = make_20_from_40(gray_dim)

    v = [
        Variant("gray_dim", gray_dim, gray_dim_20),
    ]
    return v


def render_atlas(variants: list[Variant], button1_40: Image.Image, button2_40: Image.Image) -> list[tuple[str, int, int, int, int]]:
    # Layout: grayscale | button1_blend | button2_blend (side-by-side comparison)
    atlas = Image.new("RGBA", (ATLAS_SIZE, ATLAS_SIZE), (71, 71, 71, 0))
    placements: list[tuple[str, int, int, int, int]] = []

    y = Y_START
    for v in variants:
        # Col 1: raw grayscale icon
        atlas.alpha_composite(v.img40, (X_COL1_GRAY, y))
        placements.append((f"{v.name}_gray", X_COL1_GRAY, y, 40, 40))
        
        # Col 2: blended with button1 (smooth gradient)
        blended_btn1 = blend_on_button(v.img40, button1_40, icon_opacity=0.50, darken_bg=1.00)
        atlas.alpha_composite(blended_btn1, (X_COL2_BTN1, y))
        placements.append((f"{v.name}_btn1", X_COL2_BTN1, y, 40, 40))
        
        # Col 3: blended with button2 (dramatic gradient)
        blended_btn2 = blend_on_button(v.img40, button2_40, icon_opacity=0.50, darken_bg=1.00)
        atlas.alpha_composite(blended_btn2, (X_COL3_BTN2, y))
        placements.append((f"{v.name}_btn2", X_COL3_BTN2, y, 40, 40))
        
        y += 40 + GAP

    atlas.save(OUT_ATLAS, format="TGA")
    return placements


def main() -> None:
    if not SOURCE_ICON_FILE.exists():
        raise FileNotFoundError(f"Missing source icon: {SOURCE_ICON_FILE}")
    if not SOURCE_BUTTONS_FILE.exists():
        raise FileNotFoundError(f"Missing source buttons: {SOURCE_BUTTONS_FILE}")

    # Load source files
    icon_source = Image.open(SOURCE_ICON_FILE).convert("RGBA")
    button_source = Image.open(SOURCE_BUTTONS_FILE).convert("RGBA")
    
    # Extract icon and both buttons
    icon40 = load_icon_40(icon_source, ICON_X, ICON_Y)
    button1_40 = button_source.crop((BUTTON1_X, BUTTON1_Y, BUTTON1_X + 40, BUTTON1_Y + 40)).convert("RGBA")
    button2_40 = button_source.crop((BUTTON2_X, BUTTON2_Y, BUTTON2_X + 40, BUTTON2_Y + 40)).convert("RGBA")

    variants = build_variants(icon40)
    placements = render_atlas(variants, button1_40, button2_40)

    print(f"Created: {OUT_ATLAS}")
    print("Placements (Side-by-Side Comparison):")
    print("  Columns: grayscale | button1_smooth | button2_dramatic")
    print()
    for name, x, y, w, h in placements:
        if x == X_COL1_GRAY:
            pos = "grayscale"
        elif x == X_COL2_BTN1:
            pos = "button1_smooth"
        else:
            pos = "button2_dramatic"
        print(f"  {name:20s} @ ({x:3d},{y:3d}) {pos:16s} size {w}x{h}")


if __name__ == "__main__":
    main()
