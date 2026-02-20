from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps


ROOT = Path("C:/Thorne-UI")
SOURCE_ICON = ROOT / "thorne_drak" / "thorne_drak01.tga"
SOURCE_JPG = ROOT / "thorne_drak" / "thorne_drak01.jpg"
BUTTON_SOURCE = ROOT / "thorne_drak" / "button_clean_from_bow.tga"  # Clean button from window_pieces02
OUT_ATLAS = ROOT / "thorne_drak" / "thorne_icons_slots01.tga"
OUT_ATLAS_GOLD = ROOT / "thorne_drak" / "thorne_icons_slots02.tga"
OUT_ATLAS_HYBRID = ROOT / "thorne_drak" / "thorne_icons_slots03.tga"

# Hand-editable source files for workflow
SOURCE_ICON_FILE = ROOT / "thorne_drak" / "thorne_icon.tga"
SOURCE_BUTTONS_FILE = ROOT / "thorne_drak" / "thorne_buttons01.tga"

# Source file crop positions (where icon and button are located in source files)
ICON_X, ICON_Y = 2, 2
# Button positions in thorne_buttons01.tga (255x255 atlas with 6 rows)
# Row 1: Solid (100% opacity, A=255) @ y=0
BUTTON1_X_SOLID, BUTTON1_Y_SOLID = 0, 0
BUTTON2_X_SOLID, BUTTON2_Y_SOLID = 40, 0
# Row 2: 95% opacity (A=242) @ y=44
BUTTON1_X_95, BUTTON1_Y_95 = 0, 44
BUTTON2_X_95, BUTTON2_Y_95 = 40, 44
# Row 3: 90% opacity (A=230) @ y=88
BUTTON1_X_90, BUTTON1_Y_90 = 0, 88
BUTTON2_X_90, BUTTON2_Y_90 = 40, 88
# Row 4: 85% opacity (A=217) @ y=132
BUTTON1_X_85, BUTTON1_Y_85 = 0, 132
BUTTON2_X_85, BUTTON2_Y_85 = 40, 132
# Row 5: 75% opacity (A=191) @ y=176
BUTTON1_X_75, BUTTON1_Y_75 = 0, 176
BUTTON2_X_75, BUTTON2_Y_75 = 40, 176
# Row 6: 50% opacity (A=128) @ y=220
BUTTON1_X_50, BUTTON1_Y_50 = 0, 220
BUTTON2_X_50, BUTTON2_Y_50 = 40, 220

# Button type selector: "solid", "95", "90", "85", "75", or "50"
BUTTON_TYPE = "solid"

ATLAS_SIZE = 255

# Layout: 6-column comprehensive comparison per row
# Each variant row shows: gray_40, gray_20, btn1_40, btn1_20, btn2_40, btn2_20
# Columns: grayscale (40+20) | button1_blend (40+20) | button2_blend (40+20)
X_GRAY_40 = 2
X_GRAY_20 = 44
X_BTN1_40 = 66
X_BTN1_20 = 108
X_BTN2_40 = 130
X_BTN2_20 = 172
Y_START = 2
GAP = 2

# Icon fit inside button canvases (top-anchored to keep placement "up")
FIT_40 = 39
FIT_20 = 18
FIT_40_Y_OFFSET = -1
FIT_20_Y_OFFSET = 0

# Background extraction thresholds for producing a truly clear icon from JPG
L_LOW, L_HIGH = 165.0, 245.0
S_MAX = 55.0


@dataclass
class Variant:
    name: str
    img40: Image.Image
    img20: Image.Image


def tint_grayscale(icon: Image.Image, dark_rgb: tuple[int, int, int], light_rgb: tuple[int, int, int]) -> Image.Image:
    """Tint a grayscale RGBA icon from dark_rgb -> light_rgb while preserving alpha."""
    rgba = icon.convert("RGBA")
    r, g, b, a = rgba.split()
    # Use red channel as luminance reference (R=G=B for grayscale icons)
    lum = r.load()
    ap = a.load()
    w, h = rgba.size

    out = Image.new("RGBA", (w, h))
    op = out.load()
    dr, dg, db = dark_rgb
    lr, lg, lb = light_rgb

    for y in range(h):
        for x in range(w):
            alpha = ap[x, y]
            if alpha == 0:
                op[x, y] = (0, 0, 0, 0)
                continue
            t = lum[x, y] / 255.0
            rr = int(dr + (lr - dr) * t)
            gg = int(dg + (lg - dg) * t)
            bb = int(db + (lb - db) * t)
            op[x, y] = (rr, gg, bb, alpha)

    return out


def tint_vertical_hybrid(
    icon: Image.Image,
    gold_dark: tuple[int, int, int],
    gold_light: tuple[int, int, int],
    silver_dark: tuple[int, int, int],
    silver_light: tuple[int, int, int],
) -> Image.Image:
    """Tint grayscale icon with vertical metal gradient: bright gold top -> silver bottom.

    Keeps luminance detail while shifting hue by Y position.
    """
    rgba = icon.convert("RGBA")
    r, g, b, a = rgba.split()
    lum = r.load()  # grayscale source so R=G=B
    ap = a.load()
    w, h = rgba.size

    out = Image.new("RGBA", (w, h))
    op = out.load()

    gd_r, gd_g, gd_b = gold_dark
    gl_r, gl_g, gl_b = gold_light
    sd_r, sd_g, sd_b = silver_dark
    sl_r, sl_g, sl_b = silver_light

    for y in range(h):
        y_norm = y / max(1, h - 1)
        # Keep gold dominant longer, then transition toward silver near lower half.
        silver_mix = y_norm ** 1.25
        top_gold_boost = 1.10 - 0.10 * y_norm  # brightest at top

        for x in range(w):
            alpha = ap[x, y]
            if alpha == 0:
                op[x, y] = (0, 0, 0, 0)
                continue

            t = lum[x, y] / 255.0

            # Per-row gold and silver colors from luminance
            g_r = gd_r + (gl_r - gd_r) * t
            g_g = gd_g + (gl_g - gd_g) * t
            g_b = gd_b + (gl_b - gd_b) * t

            s_r = sd_r + (sl_r - sd_r) * t
            s_g = sd_g + (sl_g - sd_g) * t
            s_b = sd_b + (sl_b - sd_b) * t

            # Vertical blend: top gold -> bottom silver
            rr = g_r * (1.0 - silver_mix) + s_r * silver_mix
            gg = g_g * (1.0 - silver_mix) + s_g * silver_mix
            bb = g_b * (1.0 - silver_mix) + s_b * silver_mix

            # Top highlight emphasis for "brighter gold at top"
            rr *= top_gold_boost
            gg *= top_gold_boost
            bb *= top_gold_boost

            op[x, y] = (
                int(max(0, min(255, rr))),
                int(max(0, min(255, gg))),
                int(max(0, min(255, bb))),
                alpha,
            )

    return out


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


def fit_icon_to_button_canvas(icon: Image.Image, canvas_size: int, fit_size: int, y_offset: int = 0) -> Image.Image:
    """Resize icon to fit_size x fit_size and place in canvas_size square, top-anchored.

    This preserves a bottom buffer so icon doesn't bleed into lower button border.
    """
    src = icon.convert("RGBA")
    fit_size = max(1, min(canvas_size, fit_size))
    resized = src.resize((fit_size, fit_size), Image.LANCZOS)

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    x = (canvas_size - fit_size) // 2
    y = y_offset  # allows per-size vertical nudges
    canvas.alpha_composite(resized, (x, y))
    return canvas


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


def make_inverted_impression(icon40: Image.Image, mid_tone: int = 128, contrast: float = 0.6, depth_gradient: bool = True) -> Image.Image:
    """Create inverted grayscale impression effect - like icon is pressed into button.
    
    Args:
        icon40: Source icon
        mid_tone: Center gray value (lower = darker impression)
        contrast: Contrast multiplier (0.6 = subtle, 1.0 = full range)
        depth_gradient: Apply vertical gradient (darker top/bottom, brighter middle)
    """
    rgba = icon40.convert("RGBA")
    rgb = rgba.convert("RGB")
    alpha = rgba.split()[3]

    # Convert to grayscale
    gray = ImageOps.grayscale(rgb)
    
    # Invert: 255 - value (light becomes dark, dark becomes light)
    inverted = ImageOps.invert(gray)
    
    # Normalize to mid-tone range for subtle impression
    inv_array = inverted.load()
    w, h = inverted.size
    
    out = Image.new("RGBA", (w, h))
    op = out.load()
    ap = alpha.load()
    
    for y in range(h):
        for x in range(w):
            a = ap[x, y]
            if a > 0:
                # Normalize inverted value to 0-1 range
                norm = inv_array[x, y] / 255.0
                # Map to mid-tone ± contrast range
                val = mid_tone + (norm - 0.5) * contrast * 255
                
                # Apply vertical depth gradient if enabled
                if depth_gradient:
                    # Darker at top (y=0) and bottom (y=h-1), brighter in middle
                    y_norm = y / (h - 1) if h > 1 else 0.5
                    # Parabolic gradient: 0 at edges, 1.0 at center (y=0.5)
                    gradient = 1.0 - 4 * (y_norm - 0.5) ** 2  # Peak at middle
                    # Apply gradient: multiply by 0.85-1.0 range (15% darkening at edges)
                    gradient_mult = 0.85 + gradient * 0.15
                    val *= gradient_mult
                
                val = int(max(0, min(255, val)))
                op[x, y] = (val, val, val, a)
            else:
                op[x, y] = (0, 0, 0, 0)
    
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


def build_variants(icon40: Image.Image, mode: str = "silver") -> list[Variant]:
    # Pipeline: source icon -> 5 inverted impression variants (darkest to lightest)
    clear40 = icon40

    # 5 inverted impression variants with depth gradient
    # Darkest (top) to lightest (bottom)
    # Row 2 intentionally darker than prior run.
    inv_darkest = make_inverted_impression(clear40, mid_tone=46, contrast=0.6, depth_gradient=True)
    inv_darker = make_inverted_impression(clear40, mid_tone=78, contrast=0.6, depth_gradient=True)
    inv_medium = make_inverted_impression(clear40, mid_tone=96, contrast=0.6, depth_gradient=True)
    inv_lighter = make_inverted_impression(clear40, mid_tone=112, contrast=0.6, depth_gradient=True)
    inv_lightest = make_inverted_impression(clear40, mid_tone=128, contrast=0.6, depth_gradient=True)

    if mode == "gold":
        # Gold ramp (dark antique gold -> bright warm gold)
        dark_gold = (72, 55, 18)
        light_gold = (222, 190, 92)
        inv_darkest = tint_grayscale(inv_darkest, dark_gold, light_gold)
        inv_darker = tint_grayscale(inv_darker, dark_gold, light_gold)
        inv_medium = tint_grayscale(inv_medium, dark_gold, light_gold)
        inv_lighter = tint_grayscale(inv_lighter, dark_gold, light_gold)
        inv_lightest = tint_grayscale(inv_lightest, dark_gold, light_gold)
    elif mode == "hybrid":
        # Vertical hybrid: brighter gold at top, transitioning toward silver at bottom.
        gold_dark = (72, 55, 18)
        gold_light = (222, 190, 92)
        silver_dark = (78, 82, 92)
        silver_light = (208, 214, 224)
        inv_darkest = tint_vertical_hybrid(inv_darkest, gold_dark, gold_light, silver_dark, silver_light)
        inv_darker = tint_vertical_hybrid(inv_darker, gold_dark, gold_light, silver_dark, silver_light)
        inv_medium = tint_vertical_hybrid(inv_medium, gold_dark, gold_light, silver_dark, silver_light)
        inv_lighter = tint_vertical_hybrid(inv_lighter, gold_dark, gold_light, silver_dark, silver_light)
        inv_lightest = tint_vertical_hybrid(inv_lightest, gold_dark, gold_light, silver_dark, silver_light)

    # Build 20px versions
    clear20 = make_20_from_40(clear40)
    inv_darkest_20 = make_20_from_40(inv_darkest)
    inv_darker_20 = make_20_from_40(inv_darker)
    inv_medium_20 = make_20_from_40(inv_medium)
    inv_lighter_20 = make_20_from_40(inv_lighter)
    inv_lightest_20 = make_20_from_40(inv_lightest)

    v = [
        Variant("sharp_clear", clear40, clear20),
        Variant("inv_darkest", inv_darkest, inv_darkest_20),
        Variant("inv_darker", inv_darker, inv_darker_20),
        Variant("inv_medium", inv_medium, inv_medium_20),
        Variant("inv_lighter", inv_lighter, inv_lighter_20),
        Variant("inv_lightest", inv_lightest, inv_lightest_20),
    ]
    return v


def render_atlas(
    variants: list[Variant],
    button1_40: Image.Image,
    button2_40: Image.Image,
    out_atlas: Path,
) -> list[tuple[str, int, int, int, int]]:
    # Comprehensive layout: Each row shows full variant progression
    # 6 columns per row: gray_40, gray_20, btn1_40, btn1_20, btn2_40, btn2_20
    atlas = Image.new("RGBA", (ATLAS_SIZE, ATLAS_SIZE), (71, 71, 71, 0))
    placements: list[tuple[str, int, int, int, int]] = []

    # Create 20px button versions
    button1_20 = button1_40.resize((20, 20), Image.LANCZOS)
    button2_20 = button2_40.resize((20, 20), Image.LANCZOS)

    y = Y_START
    for i, v in enumerate(variants):
        # Grayscale icons (40px and 20px)
        atlas.alpha_composite(v.img40, (X_GRAY_40, y))
        placements.append((f"{v.name}_gray_40", X_GRAY_40, y, 40, 40))
        
        atlas.alpha_composite(v.img20, (X_GRAY_20, y))
        placements.append((f"{v.name}_gray_20", X_GRAY_20, y, 20, 20))
        
        if i == 0:
            # First row: Show button references only (no icon blending)
            atlas.alpha_composite(button1_40, (X_BTN1_40, y))
            placements.append((f"button1_ref_40", X_BTN1_40, y, 40, 40))
            
            atlas.alpha_composite(button1_20, (X_BTN1_20, y))
            placements.append((f"button1_ref_20", X_BTN1_20, y, 20, 20))
            
            atlas.alpha_composite(button2_40, (X_BTN2_40, y))
            placements.append((f"button2_ref_40", X_BTN2_40, y, 40, 40))
            
            atlas.alpha_composite(button2_20, (X_BTN2_20, y))
            placements.append((f"button2_ref_20", X_BTN2_20, y, 20, 20))
        else:
            # Subsequent rows: Blend icons with buttons
            # Progressive opacity: darkest=0.45, darker=0.50, medium=0.55, lighter=0.60, lightest=0.65
            opacity = 0.45 + (i-1) * 0.05

            # Fit icons per size to preserve button border clearance
            icon40_fit = fit_icon_to_button_canvas(v.img40, 40, FIT_40, FIT_40_Y_OFFSET)
            icon20_fit = fit_icon_to_button_canvas(v.img20, 20, FIT_20, FIT_20_Y_OFFSET)
            
            blended_btn1_40 = blend_on_button(icon40_fit, button1_40, icon_opacity=opacity, darken_bg=1.00)
            atlas.alpha_composite(blended_btn1_40, (X_BTN1_40, y))
            placements.append((f"{v.name}_btn1_40", X_BTN1_40, y, 40, 40))
            
            blended_btn1_20 = blend_on_button(icon20_fit, button1_20, icon_opacity=opacity, darken_bg=1.00)
            atlas.alpha_composite(blended_btn1_20, (X_BTN1_20, y))
            placements.append((f"{v.name}_btn1_20", X_BTN1_20, y, 20, 20))
            
            blended_btn2_40 = blend_on_button(icon40_fit, button2_40, icon_opacity=opacity, darken_bg=1.00)
            atlas.alpha_composite(blended_btn2_40, (X_BTN2_40, y))
            placements.append((f"{v.name}_btn2_40", X_BTN2_40, y, 40, 40))
            
            blended_btn2_20 = blend_on_button(icon20_fit, button2_20, icon_opacity=opacity, darken_bg=1.00)
            atlas.alpha_composite(blended_btn2_20, (X_BTN2_20, y))
            placements.append((f"{v.name}_btn2_20", X_BTN2_20, y, 20, 20))
        
        y += 40 + GAP

    atlas.save(out_atlas, format="TGA")
    return placements


def main() -> None:
    if not SOURCE_ICON_FILE.exists():
        raise FileNotFoundError(f"Missing source icon: {SOURCE_ICON_FILE}")
    if not SOURCE_BUTTONS_FILE.exists():
        raise FileNotFoundError(f"Missing source buttons: {SOURCE_BUTTONS_FILE}")

    # Load source files
    icon_source = Image.open(SOURCE_ICON_FILE).convert("RGBA")
    button_source = Image.open(SOURCE_BUTTONS_FILE).convert("RGBA")
    
    # Extract icon and both buttons based on BUTTON_TYPE
    icon40 = load_icon_40(icon_source, ICON_X, ICON_Y)
    
    if BUTTON_TYPE == "95":
        button1_40 = button_source.crop((BUTTON1_X_95, BUTTON1_Y_95, BUTTON1_X_95 + 40, BUTTON1_Y_95 + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_95, BUTTON2_Y_95, BUTTON2_X_95 + 40, BUTTON2_Y_95 + 40)).convert("RGBA")
        button_label = "95% opacity"
    elif BUTTON_TYPE == "90":
        button1_40 = button_source.crop((BUTTON1_X_90, BUTTON1_Y_90, BUTTON1_X_90 + 40, BUTTON1_Y_90 + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_90, BUTTON2_Y_90, BUTTON2_X_90 + 40, BUTTON2_Y_90 + 40)).convert("RGBA")
        button_label = "90% opacity"
    elif BUTTON_TYPE == "85":
        button1_40 = button_source.crop((BUTTON1_X_85, BUTTON1_Y_85, BUTTON1_X_85 + 40, BUTTON1_Y_85 + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_85, BUTTON2_Y_85, BUTTON2_X_85 + 40, BUTTON2_Y_85 + 40)).convert("RGBA")
        button_label = "85% opacity"
    elif BUTTON_TYPE == "75":
        button1_40 = button_source.crop((BUTTON1_X_75, BUTTON1_Y_75, BUTTON1_X_75 + 40, BUTTON1_Y_75 + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_75, BUTTON2_Y_75, BUTTON2_X_75 + 40, BUTTON2_Y_75 + 40)).convert("RGBA")
        button_label = "75% opacity"
    elif BUTTON_TYPE == "50":
        button1_40 = button_source.crop((BUTTON1_X_50, BUTTON1_Y_50, BUTTON1_X_50 + 40, BUTTON1_Y_50 + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_50, BUTTON2_Y_50, BUTTON2_X_50 + 40, BUTTON2_Y_50 + 40)).convert("RGBA")
        button_label = "50% opacity"
    else:  # solid
        button1_40 = button_source.crop((BUTTON1_X_SOLID, BUTTON1_Y_SOLID, BUTTON1_X_SOLID + 40, BUTTON1_Y_SOLID + 40)).convert("RGBA")
        button2_40 = button_source.crop((BUTTON2_X_SOLID, BUTTON2_Y_SOLID, BUTTON2_X_SOLID + 40, BUTTON2_Y_SOLID + 40)).convert("RGBA")
        button_label = "solid"

    # slots01: Silver/gray atlas
    variants_silver = build_variants(icon40, mode="silver")
    placements = render_atlas(variants_silver, button1_40, button2_40, OUT_ATLAS)

    # slots02: Gold atlas (same layout)
    variants_gold = build_variants(icon40, mode="gold")
    _ = render_atlas(variants_gold, button1_40, button2_40, OUT_ATLAS_GOLD)

    # slots03: Gold/Silver hybrid atlas (same layout)
    variants_hybrid = build_variants(icon40, mode="hybrid")
    _ = render_atlas(variants_hybrid, button1_40, button2_40, OUT_ATLAS_HYBRID)

    print(f"Created: {OUT_ATLAS}")
    print(f"Created: {OUT_ATLAS_GOLD}")
    print(f"Created: {OUT_ATLAS_HYBRID}")
    row_map = {"solid": 1, "95": 2, "90": 3, "85": 4, "75": 5, "50": 6}
    button_row = row_map.get(BUTTON_TYPE, 1)
    print(f"Button type: {button_label} (from thorne_buttons01.tga row {button_row})")
    print("Placements (Inverted Impression Progression):")
    print("  Columns: gray_40, gray_20 | btn1_40, btn1_20 | btn2_40, btn2_20")
    print("  Rows: original -> darkest -> darker -> medium -> lighter -> lightest")
    print("  Each variant: darker top/bottom, brighter middle (depth gradient)")
    print()
    for name, x, y, w, h in placements:
        if x == X_GRAY_40:
            pos = "gray_40"
        elif x == X_GRAY_20:
            pos = "gray_20"
        elif x == X_BTN1_40:
            pos = "btn1_smooth_40"
        elif x == X_BTN1_20:
            pos = "btn1_smooth_20"
        elif x == X_BTN2_40:
            pos = "btn2_dramatic_40"
        else:
            pos = "btn2_dramatic_20"
        print(f"  {name:22s} @ ({x:3d},{y:3d}) {pos:16s} size {w}x{h}")


if __name__ == "__main__":
    main()
