"""generate_catalog.py -- DEPRECATED / EXPERIMENTAL

This script was the original AI-powered icon catalog builder using pixel
feature analysis and iterative learning. It is preserved as a reference for
the AI classification techniques used (HOG features, exemplar learning,
confidence scoring) but is NO LONGER USED in the active pipeline.

Replaced by:
  - extract_eq_items.py   (Quarm SQL database → real item data)
  - pick_class_icons.py   (stat-weighted scoring per class + slot)

Those scripts use actual game item data rather than visual classification.

Original description follows:
---
Iterative EQ dragitem icon catalog with learning.

Identifies items in dragitem*.tga sprite sheets by analyzing pixel features,
then improves classifications over time as items are confirmed by the user.

Workflow:
  1. Run on a file:    python .bin/generate_catalog.py dragitem1
  2. Agent reviews ASCII output + recommendations, updates JSON status
  3. User confirms entries → status set to "confirmed"
  4. Re-run with --learn to improve unconfirmed items using confirmed references
  5. Repeat per file until catalog is complete

Usage:
    python .bin/generate_catalog.py dragitem1        # Analyze single file
    python .bin/generate_catalog.py --all            # Analyze all files (skip confirmed)
    python .bin/generate_catalog.py --md             # Regenerate markdown from JSON
    python .bin/generate_catalog.py --learn          # Re-score unconfirmed using confirmed
    python .bin/generate_catalog.py --stats          # Show catalog statistics
    python .bin/generate_catalog.py --force dragitem1  # Re-analyze even high-status items
    python .bin/generate_catalog.py --png            # Extract 40x40 cell PNGs from all TGAs
    python .bin/generate_catalog.py --png dragitem1  # Extract PNGs for one file
    python .bin/generate_catalog.py --html           # Generate HTML contact sheets (all)
    python .bin/generate_catalog.py --html dragitem1 # Generate HTML contact sheet (one)

Status Levels:
    guess     — auto-classified, needs review
    high      — agent-reviewed, likely correct
    confirmed — human verified, NEVER overwritten

Files:
    .Master/.Items/item_catalog.json   — Source of truth (compact, one item/line)
    .Master/.Items/item_catalog.md     — Regenerated readable view
    .Master/.Items/.cache/             — Feature cache and ASCII renders
    .Master/.Items/.cache/dragitemN/   — Per-file extracted cell PNGs
    .Master/.Items/.cache/dragitemN.html — Per-file visual contact sheet
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import math
import sys
import textwrap
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image

# ─── Paths ───────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO / "thorne_drak" / "Options" / "Slots" / ".Master" / ".Items"
CATALOG_JSON = ITEMS_DIR / "item_catalog.json"
CATALOG_MD = ITEMS_DIR / "item_catalog.md"
CACHE_DIR = ITEMS_DIR / ".cache"

CELL = 40
GRID = 6
ALPHA_THRESH = 30

# ─── Master Categories (loaded from _slot_map in item_catalog.json) ──
# The _slot_map is the single source of truth for categories, subcategories,
# and equipment slot assignments. These are populated at startup by
# load_master_categories().

MASTER_CATEGORIES: dict[str, list[str]] = {}  # cat -> [sub, ...]
VALID_SUBS: dict[str, str] = {}               # sub -> cat


def load_master_categories(catalog: dict) -> None:
    """Populate MASTER_CATEGORIES and VALID_SUBS from _slot_map in catalog."""
    global MASTER_CATEGORIES, VALID_SUBS
    slot_map = catalog.get("_slot_map", {})
    MASTER_CATEGORIES = {cat: list(subs.keys()) for cat, subs in slot_map.items()}
    VALID_SUBS = {}
    for cat, subs in slot_map.items():
        for sub in subs:
            VALID_SUBS[sub] = cat


def validate_catalog_subs(catalog: dict) -> list[str]:
    """Check all cell entries for subcategories not in _slot_map.
    Returns list of warning strings. Prints them too."""
    warnings = []
    for file_key, cells in catalog.items():
        if file_key.startswith("_"):
            continue
        for ck, entry in cells.items():
            sub = entry.get("sub", "")
            if sub and sub not in VALID_SUBS:
                msg = f"  WARNING: {file_key} {ck} has sub '{sub}' not in _slot_map"
                warnings.append(msg)
    if warnings:
        print(f"\n  === {len(warnings)} unknown subcategories ===")
        for w in warnings:
            print(w)
        print("  Add them to _slot_map in item_catalog.json or fix the cell entry.\n")
    return warnings


# ─── Feature Extraction ─────────────────────────────────────────────

def extract_cell(img: Image.Image, row: int, col: int) -> np.ndarray:
    """Extract a single 40x40 cell from a sprite sheet."""
    x0 = (col - 1) * CELL
    y0 = (row - 1) * CELL
    return np.array(img.crop((x0, y0, x0 + CELL, y0 + CELL)).convert("RGBA"))


def get_features(cell: np.ndarray) -> dict | None:
    """Extract classification features from a cell. Returns None if empty."""
    alpha = cell[:, :, 3]
    rgb = cell[:, :, :3]
    mask = alpha >= ALPHA_THRESH
    opaque = int(mask.sum())
    total = CELL * CELL

    if opaque < total * 0.02:
        return None

    fill = opaque / total

    # Bounding box
    rows_any = np.any(mask, axis=1)
    cols_any = np.any(mask, axis=0)
    rmin, rmax = np.where(rows_any)[0][[0, -1]]
    cmin, cmax = np.where(cols_any)[0][[0, -1]]
    bh = int(rmax - rmin + 1)
    bw = int(cmax - cmin + 1)
    aspect = bw / max(bh, 1)

    # Center of mass
    ys, xs = np.where(mask)
    cx = float(xs.mean()) / CELL
    cy = float(ys.mean()) / CELL

    # Quadrant distribution
    q = [
        mask[:20, :20].sum(),
        mask[:20, 20:].sum(),
        mask[20:, :20].sum(),
        mask[20:, 20:].sum(),
    ]
    qt = max(opaque, 1)
    qn = [x / qt for x in q]

    # Diagonal bias (top-left+bottom-right vs top-right+bottom-left)
    diag = (qn[0] + qn[3]) - (qn[1] + qn[2])

    # Symmetry (horizontal and vertical)
    h_sym = np.sum(mask[:, :20] & mask[:, 39:19:-1]) / max(mask[:, :20].sum(), 1)
    v_sym = np.sum(mask[:20, :] & mask[39:19:-1, :]) / max(mask[:20, :].sum(), 1)

    # Hollowness (edge vs center fill)
    cm = mask[10:30, 10:30]
    cf = cm.sum() / max(cm.size, 1)
    ef = (opaque - cm.sum()) / max(total - cm.size, 1)
    hollow = max(0, ef - cf) if ef > 0 else 0

    # Principal axis angle
    if opaque > 10:
        xs_c = xs - xs.mean()
        ys_c = ys - ys.mean()
        mxx = (xs_c ** 2).mean()
        myy = (ys_c ** 2).mean()
        mxy = (xs_c * ys_c).mean()
        angle = 0.5 * math.degrees(math.atan2(2 * mxy, mxx - myy))
    else:
        angle = 0

    # Color
    opaque_rgb = rgb[mask]
    avg = opaque_rgb.mean(axis=0).astype(int).tolist()
    brightness = sum(avg) / 3
    r, g, b = avg
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    sat = (max_c - min_c) / max(max_c, 1)

    # Vertical profile (5 zones)
    vp = []
    for i in range(5):
        s = i * 8
        vp.append(mask[s:s + 8, :].sum() / (8 * CELL))

    # Width at different heights
    top_w = mask[:10, :].sum() / max(mask[:10, :].any(axis=1).sum() * CELL, 1)
    mid_w = mask[15:25, :].sum() / max(mask[15:25, :].any(axis=1).sum() * CELL, 1)
    bot_w = mask[30:, :].sum() / max(mask[30:, :].any(axis=1).sum() * CELL, 1)

    # Edge ratio
    edge = (
        mask[:, :5].sum() + mask[:, 35:].sum() +
        mask[:5, :].sum() + mask[35:, :].sum()
    )
    edge_ratio = edge / max(opaque, 1)

    return {
        "fill": round(fill, 3), "bw": bw, "bh": bh, "aspect": round(aspect, 2),
        "cx": round(cx, 2), "cy": round(cy, 2),
        "diag": round(diag, 2), "hollow": round(hollow, 2),
        "h_sym": round(float(h_sym), 2), "v_sym": round(float(v_sym), 2),
        "angle": round(angle, 1),
        "rgb": avg, "brightness": round(brightness, 1), "sat": round(sat, 2),
        "vp": [round(x, 2) for x in vp],
        "top_w": round(top_w, 2), "mid_w": round(mid_w, 2), "bot_w": round(bot_w, 2),
        "edge_ratio": round(edge_ratio, 2),
    }


def feature_vector(f: dict) -> list[float]:
    """Convert features dict to a numeric vector for similarity comparison."""
    return [
        f["fill"], f["aspect"], f["hollow"], f["diag"],
        f["h_sym"], f["v_sym"], f["angle"] / 90.0,
        f["brightness"] / 255.0, f["sat"],
        f["top_w"], f["mid_w"], f["bot_w"],
        f["edge_ratio"], f["cx"], f["cy"],
    ]


def render_ascii(cell: np.ndarray) -> list[str]:
    """Render a cell as 10x10 ASCII art."""
    chars = " .:-=+*#%@"
    lines = []
    for yr in range(0, CELL, 4):
        line = ""
        for xr in range(0, CELL, 4):
            blk = cell[yr:yr + 4, xr:xr + 4]
            a = blk[:, :, 3].mean()
            if a < ALPHA_THRESH:
                line += " "
            else:
                br = blk[:, :, :3].mean()
                idx = min(int(br / 256 * len(chars)), len(chars) - 1)
                line += chars[idx]
        lines.append(line)
    return lines


# ─── Heuristic Classifier ───────────────────────────────────────────

def classify_heuristic(f: dict) -> tuple[str, str, str]:
    """Classify by pixel features. Returns (cat, sub, notes)."""
    fill = f["fill"]
    aspect = f["aspect"]
    bw, bh = f["bw"], f["bh"]
    hollow = f["hollow"]
    diag = f["diag"]
    angle = f["angle"]
    h_sym = f["h_sym"]
    v_sym = f["v_sym"]
    vp = f["vp"]
    brightness = f["brightness"]
    sat = f["sat"]
    top_w = f["top_w"]
    mid_w = f["mid_w"]
    bot_w = f["bot_w"]

    # Rings & Jewelry — hollow circles
    if hollow > 0.20 and fill < 0.35 and 0.6 < aspect < 1.6:
        return ("jewelry", "ring", "hollow circular shape")

    if hollow > 0.12 and fill < 0.30 and 0.7 < aspect < 1.4:
        return ("jewelry", "ring", "semi-hollow circular")

    # Weapons — strong diagonal
    if abs(diag) > 0.65 and fill < 0.25:
        if bh > 35 or bw > 35:
            return ("weapon", "sword_long", "strong diagonal, tall")
        return ("weapon", "dagger", "strong diagonal, short")

    if abs(diag) > 0.40 and fill < 0.30 and abs(angle) > 30:
        if fill < 0.12:
            return ("weapon", "arrow", "thin diagonal")
        if fill < 0.20:
            return ("weapon", "sword_long", "diagonal blade")
        return ("weapon", "axe", "diagonal, wider blade")

    if abs(angle) > 35 and fill < 0.25 and (aspect > 1.3 or aspect < 0.75):
        return ("weapon", "sword_long", "angled elongated")

    # Staves — tall and thin
    if aspect < 0.35 and bh > 30 and fill < 0.25:
        return ("weapon", "staff", "tall thin")

    # Bows — wide horizontal curve
    if aspect > 2.0 and hollow > 0.05 and 0.3 < fill < 0.5:
        return ("weapon", "bow", "wide curved")

    # Shields — large, filled, symmetric
    if fill > 0.60 and h_sym > 0.6 and bw > 30 and bh > 30:
        if aspect < 0.85:
            return ("armor", "shield_kite", "tall large filled")
        if aspect > 1.15:
            return ("armor", "shield_round", "wide large filled")
        return ("armor", "shield_round", "large filled symmetric")

    if fill > 0.50 and h_sym > 0.5 and bw > 25 and bh > 25:
        return ("armor", "shield_round", "medium filled symmetric")

    # Breastplate — tall, symmetric, medium-high fill
    if 0.35 < fill < 0.60 and aspect < 0.85 and h_sym > 0.35 and bh > 30:
        if brightness > 130:
            return ("armor", "breastplate", "bright tall symmetric")
        return ("armor", "breastplate", "tall symmetric torso")

    if 0.30 < fill < 0.55 and 0.6 < aspect < 0.9 and bh > 28:
        if sat < 0.15 and brightness > 100:
            return ("armor", "tunic", "neutral tall armor")
        return ("armor", "tunic", "medium tall")

    # Helms — top-heavy, dome-shaped
    if vp[0] + vp[1] > vp[3] + vp[4] and fill > 0.25 and h_sym > 0.35:
        if fill > 0.45 and brightness > 130:
            return ("armor", "helm", "bright dome top-heavy")
        if fill > 0.40:
            return ("armor", "helm", "dome-shaped top-heavy")
        if aspect > 1.3:
            return ("armor", "cap", "wide horizontal headband")
        return ("armor", "cap", "light top-heavy")

    # Crown/Circlet — wide horizontal
    if aspect > 1.5 and bh < 25 and fill > 0.20 and h_sym > 0.5:
        return ("armor", "cap", "wide horizontal piece")

    # Boots — bottom-heavy
    if vp[3] + vp[4] > vp[0] + vp[1] + 0.1 and fill > 0.20:
        return ("armor", "boots", "bottom-heavy shape")

    # Belts — wide and thin
    if aspect > 2.0 and bh < 15 and fill < 0.20:
        return ("armor", "belt", "wide thin band")

    # Containers — low fill scattered
    if fill < 0.12:
        return ("misc", "other", "faint scattered shape")

    # Cloaks — widening downward
    if top_w < mid_w < bot_w and fill > 0.25 and h_sym > 0.3:
        return ("armor", "cloak", "widening downward")

    # Pendants/Amulets — hanging, center-weighted
    if f["cy"] > 0.55 and fill < 0.30 and h_sym > 0.25:
        return ("jewelry", "necklace", "hanging bottom-weighted")

    if fill < 0.25 and h_sym > 0.3 and vp[1] + vp[2] > vp[0] + vp[4]:
        return ("jewelry", "charm", "mid-weighted symmetric")

    # Generic armor
    if 0.25 < fill < 0.55 and h_sym > 0.35:
        if brightness > 130:
            return ("armor", "breastplate", "bright symmetric")
        if sat > 0.3:
            return ("armor", "tunic", "colored symmetric")
        return ("armor", "breastplate", "generic symmetric")

    if 0.20 < fill < 0.50:
        return ("misc", "other", "unclassified shape")

    if fill > 0.50:
        return ("misc", "other", "high fill unclassified")

    return ("misc", "other", "insufficient features")


# ─── Reference-Based Learning ───────────────────────────────────────

def build_references(catalog: dict) -> dict[str, list[list[float]]]:
    """Build feature reference vectors from confirmed items in the cache."""
    refs = defaultdict(list)
    cache_features = load_feature_cache()

    for file_key, cells in catalog.items():
        if file_key.startswith("_"):
            continue
        for cell_key, entry in cells.items():
            if entry.get("status") != "confirmed":
                continue
            feat_key = f"{file_key}/{cell_key}"
            if feat_key in cache_features:
                cat_sub = f"{entry['cat']}/{entry['sub']}"
                refs[cat_sub].append(cache_features[feat_key])

    return dict(refs)


def classify_by_reference(fvec: list[float], refs: dict) -> tuple[str, str, float] | None:
    """Classify a feature vector by similarity to confirmed references.

    Returns (cat, sub, similarity) or None if no references exist.
    """
    if not refs:
        return None

    best_cat_sub = None
    best_sim = -1.0

    fv = np.array(fvec)
    fv_norm = np.linalg.norm(fv)
    if fv_norm < 1e-6:
        return None

    for cat_sub, ref_vectors in refs.items():
        for rv in ref_vectors:
            rv = np.array(rv)
            rv_norm = np.linalg.norm(rv)
            if rv_norm < 1e-6:
                continue
            sim = float(np.dot(fv, rv) / (fv_norm * rv_norm))
            if sim > best_sim:
                best_sim = sim
                best_cat_sub = cat_sub

    if best_cat_sub and best_sim > 0.90:
        cat, sub = best_cat_sub.split("/", 1)
        return (cat, sub, best_sim)

    return None


# ─── Feature Cache ───────────────────────────────────────────────────

def feature_cache_path() -> Path:
    return CACHE_DIR / "features.json"


def load_feature_cache() -> dict[str, list[float]]:
    """Load cached feature vectors. Key format: 'dragitemN/[r,c]'."""
    path = feature_cache_path()
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_feature_cache(cache: dict[str, list[float]]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(feature_cache_path(), "w", encoding="utf-8") as f:
        json.dump(cache, f)


# ─── Catalog JSON I/O ───────────────────────────────────────────────

def load_catalog() -> dict:
    """Load existing catalog, populate globals from _slot_map, and validate."""
    if CATALOG_JSON.exists():
        with open(CATALOG_JSON, encoding="utf-8") as f:
            catalog = json.load(f)
    else:
        catalog = {"_meta": {"version": "2.0"}}
    load_master_categories(catalog)
    validate_catalog_subs(catalog)
    return catalog


def flatten_slot_map(catalog: dict) -> dict[str, list[str]]:
    """Flatten nested _slot_map {cat: {sub: slot_str}} → {sub: [slot, ...]}.

    Slot values may be comma-separated for multi-slot items
    (e.g. "primary, secondary" → ["primary", "secondary"]).
    """
    flat: dict[str, list[str]] = {}
    for cat_subs in catalog.get("_slot_map", {}).values():
        if isinstance(cat_subs, dict):
            for sub, slot_str in cat_subs.items():
                flat[sub] = [s.strip() for s in slot_str.split(",")]
        else:
            # Backward compat with old flat format
            for sub, slot_str in catalog.get("_slot_map", {}).items():
                if isinstance(slot_str, str):
                    flat[sub] = [s.strip() for s in slot_str.split(",")]
            break
    return flat


def save_catalog(catalog: dict) -> None:
    """Save catalog with compact formatting (one item per line)."""
    # Update meta stats
    stats = {"confirmed": 0, "high": 0, "guess": 0, "total": 0}
    for key, cells in catalog.items():
        if key.startswith("_"):
            continue
        for entry in cells.values():
            s = entry.get("status", "guess")
            stats[s] = stats.get(s, 0) + 1
            stats["total"] += 1
    catalog["_meta"] = {
        "version": "2.0",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        **stats,
    }

    # Custom compact formatting: each cell entry on one line
    lines = ["{"]

    # Meta block
    meta = catalog["_meta"]
    lines.append(f'  "_meta": {json.dumps(meta)},')

    # Slot map block (nested by category, pretty-printed)
    slot_map = catalog.get("_slot_map", {})
    if slot_map:
        lines.append('  "_slot_map": {')
        cat_keys = list(slot_map.keys())
        for ci, cat_name in enumerate(cat_keys):
            subs = slot_map[cat_name]
            lines.append(f'    "{cat_name}": {{')
            sub_items = list(subs.items())
            for si, (sub, slot) in enumerate(sub_items):
                comma = "," if si < len(sub_items) - 1 else ""
                lines.append(f'      "{sub}": "{slot}"{comma}')
            comma = "," if ci < len(cat_keys) - 1 else ""
            lines.append(f"    }}{comma}")
        lines.append("  },")

    file_keys = sorted(
        (k for k in catalog if not k.startswith("_")),
        key=lambda k: int(k.replace("dragitem", "")),
    )

    for i, fk in enumerate(file_keys):
        cells = catalog[fk]
        lines.append(f'  "{fk}": {{')

        cell_keys = sorted(cells.keys(), key=_cell_sort_key)
        for j, ck in enumerate(cell_keys):
            entry = cells[ck]
            comma = "," if j < len(cell_keys) - 1 else ""
            lines.append(f'    "{ck}": {json.dumps(entry, separators=(",", ":"))}{comma}')

        trail = "," if i < len(file_keys) - 1 else ""
        lines.append(f"  }}{trail}")

    lines.append("}")

    CATALOG_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _cell_sort_key(ck: str) -> tuple[int, int]:
    """Sort [r,c] keys numerically."""
    parts = ck.strip("[]").split(",")
    return (int(parts[0]), int(parts[1]))


# ─── Markdown Generation ────────────────────────────────────────────

STATUS_ICON = {"confirmed": "confirmed", "high": "high", "guess": "guess"}


def generate_markdown(catalog: dict) -> None:
    """Regenerate item_catalog.md from the JSON source of truth."""
    meta = catalog.get("_meta", {})
    lines = []

    # Header
    lines.append("# Dragitem Cell Catalog")
    lines.append("")
    lines.append(f"**Updated:** {meta.get('updated', 'unknown')}")
    lines.append(f"**Total:** {meta.get('total', 0)} cells across 34 files")
    lines.append(
        f"**Status:** {meta.get('confirmed', 0)} confirmed, "
        f"{meta.get('high', 0)} high, {meta.get('guess', 0)} guess"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Master categories reference
    lines.append("## Master Categories")
    lines.append("")
    lines.append("| Category | Subcategories |")
    lines.append("|----------|---------------|")
    for cat, subs in MASTER_CATEGORIES.items():
        lines.append(f"| {cat} | {', '.join(subs)} |")
    lines.append("")

    # Slot mapping reference (nested format: cat → {sub → slot})
    slot_map = catalog.get("_slot_map", {})
    if slot_map:
        lines.append("## Slot Mapping (subcat → regen slot)")
        lines.append("")
        lines.append("| Category | Subcategory | Regen Slot |")
        lines.append("|----------|-------------|------------|")
        for cat_name, subs in slot_map.items():
            for sub, slot in subs.items():
                lines.append(f"| {cat_name} | {sub} | {slot} |")
        lines.append("")

    # Per-file tables
    lines.append("## Per-File Catalog")
    lines.append("")

    file_keys = sorted(
        (k for k in catalog if not k.startswith("_")),
        key=lambda k: int(k.replace("dragitem", "")),
    )

    for fk in file_keys:
        cells = catalog[fk]
        lines.append(f"### {fk}.tga")
        lines.append("")
        lines.append("| Cell | Category | Sub | Status | Description | Notes |")
        lines.append("|------|----------|-----|--------|-------------|-------|")

        for ck in sorted(cells.keys(), key=_cell_sort_key):
            e = cells[ck]
            lines.append(
                f"| {ck} | {e['cat']} | {e['sub']} "
                f"| {STATUS_ICON.get(e.get('status', 'guess'), 'guess')} "
                f"| {e.get('desc', '')} | {e.get('notes', '')} |"
            )

        lines.append("")

    CATALOG_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Markdown: {CATALOG_MD}")


# ─── Core Analysis ──────────────────────────────────────────────────

def analyze_file(
    file_num: int,
    catalog: dict,
    feature_cache: dict,
    refs: dict,
    force: bool = False,
) -> int:
    """Analyze a single dragitem file. Returns count of cells processed."""
    fname = f"dragitem{file_num}"
    tga_path = ITEMS_DIR / f"{fname}.tga"

    if not tga_path.exists():
        print(f"  SKIP: {tga_path} not found")
        return 0

    img = Image.open(tga_path)
    file_data = catalog.get(fname, {})
    processed = 0
    ascii_lines = []

    ascii_lines.append(f"{'=' * 60}")
    ascii_lines.append(f"  {fname}.tga")
    ascii_lines.append(f"{'=' * 60}")
    ascii_lines.append("")

    for row in range(1, GRID + 1):
        for col in range(1, GRID + 1):
            ck = f"[{row},{col}]"
            existing = file_data.get(ck)

            # Skip confirmed items (and high unless --force)
            if existing:
                status = existing.get("status", "guess")
                if status == "confirmed":
                    continue
                if status == "high" and not force:
                    continue

            # Extract features
            cell = extract_cell(img, row, col)
            feats = get_features(cell)

            if feats is None:
                file_data[ck] = {
                    "cat": "empty", "sub": "empty",
                    "status": "confirmed", "desc": "", "notes": "transparent",
                }
                processed += 1
                continue

            # Cache feature vector
            fvec = feature_vector(feats)
            cache_key = f"{fname}/{ck}"
            feature_cache[cache_key] = fvec

            # Classify: try reference-based first, fall back to heuristic
            ref_result = classify_by_reference(fvec, refs) if refs else None
            if ref_result:
                cat, sub, sim = ref_result
                notes = f"ref-match ({sim:.2f})"
                status = "high" if sim > 0.95 else "guess"
            else:
                cat, sub, notes = classify_heuristic(feats)
                status = "guess"

            # Preserve user description if re-analyzing
            desc = existing.get("desc", "") if existing else ""

            file_data[ck] = {
                "cat": cat, "sub": sub,
                "status": status, "desc": desc, "notes": notes,
            }
            processed += 1

            # Generate ASCII for this cell
            art = render_ascii(cell)
            r, g, b = feats["rgb"]
            color = _color_name(r, g, b, feats["sat"])
            ascii_lines.append(f"  {ck}  {cat}/{sub}  [{status}]  fill={feats['fill']:.2f}  {color}  br={feats['brightness']:.0f}")
            ascii_lines.append(f"         {notes}")
            for al in art:
                ascii_lines.append(f"         |{al}|")
            ascii_lines.append("")

    catalog[fname] = file_data

    # Save ASCII to cache
    if ascii_lines:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        ascii_path = CACHE_DIR / f"{fname}_ascii.txt"
        with open(ascii_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ascii_lines))

    # Print ASCII to terminal
    for line in ascii_lines:
        print(line)

    return processed


def _color_name(r: int, g: int, b: int, sat: float) -> str:
    if sat < 0.2:
        return "gray"
    if r > g and r > b:
        return "red/brown"
    if g > r and g > b:
        return "green"
    if b > r and b > g:
        return "blue"
    if r > 150 and g > 150:
        return "gold"
    return "colored"


# ─── CLI Commands ────────────────────────────────────────────────────

def cmd_analyze(args):
    """Analyze one or all dragitem files."""
    catalog = load_catalog()
    feature_cache = load_feature_cache()

    # Build references from confirmed items
    refs = build_references(catalog) if not args.force else {}
    if refs:
        total_refs = sum(len(v) for v in refs.values())
        print(f"  References: {total_refs} confirmed items across {len(refs)} types")

    total = 0
    if args.all:
        files = sorted(
            ITEMS_DIR.glob("dragitem*.tga"),
            key=lambda p: int(p.stem.replace("dragitem", "")),
        )
        for fpath in files:
            fnum = int(fpath.stem.replace("dragitem", ""))
            n = analyze_file(fnum, catalog, feature_cache, refs, args.force)
            total += n
            if n > 0:
                print(f"  {fpath.name}: {n} cells analyzed")
    else:
        # Parse file argument: "dragitem1", "dragitem1.tga", or "1"
        name = args.file.replace(".tga", "").replace("dragitem", "")
        try:
            fnum = int(name)
        except ValueError:
            print(f"ERROR: Cannot parse file number from '{args.file}'")
            sys.exit(1)
        total = analyze_file(fnum, catalog, feature_cache, refs, args.force)

    if total > 0:
        save_catalog(catalog)
        save_feature_cache(feature_cache)
        generate_markdown(catalog)
        print(f"\n  Done: {total} cells analyzed")
    else:
        print("\n  No cells needed analysis (all confirmed/high)")


def cmd_learn(args):
    """Re-score unconfirmed items using confirmed references."""
    catalog = load_catalog()
    feature_cache = load_feature_cache()
    refs = build_references(catalog)

    if not refs:
        print("  No confirmed items to learn from yet.")
        return

    total_refs = sum(len(v) for v in refs.values())
    print(f"  Learning from {total_refs} confirmed items across {len(refs)} types")

    updated = 0
    for file_key in sorted(k for k in catalog if not k.startswith("_")):
        cells = catalog[file_key]
        for ck, entry in cells.items():
            if entry.get("status") == "confirmed":
                continue

            cache_key = f"{file_key}/{ck}"
            fvec = feature_cache.get(cache_key)
            if fvec is None:
                continue

            result = classify_by_reference(fvec, refs)
            if result:
                cat, sub, sim = result
                old_cat = entry["cat"]
                old_sub = entry["sub"]
                if cat != old_cat or sub != old_sub:
                    entry["cat"] = cat
                    entry["sub"] = sub
                    entry["notes"] = f"ref-match ({sim:.2f})"
                    # desc is never overwritten by learning
                    if sim > 0.95:
                        entry["status"] = "high"
                    updated += 1

    if updated > 0:
        save_catalog(catalog)
        generate_markdown(catalog)
        print(f"  Updated {updated} items from references")
    else:
        print("  No items updated (references didn't improve classifications)")


def cmd_md(args):
    """Regenerate markdown from JSON."""
    catalog = load_catalog()
    generate_markdown(catalog)


def cmd_stats(args):
    """Show catalog statistics."""
    catalog = load_catalog()
    meta = catalog.get("_meta", {})

    by_status = defaultdict(int)
    by_cat = defaultdict(int)
    by_sub = defaultdict(int)

    for file_key in sorted(k for k in catalog if not k.startswith("_")):
        cells = catalog[file_key]
        for entry in cells.values():
            by_status[entry.get("status", "guess")] += 1
            cat_sub = f"{entry['cat']}/{entry['sub']}"
            by_cat[entry["cat"]] += 1
            by_sub[cat_sub] += 1

    total = sum(by_status.values())
    print(f"\n  Catalog Statistics")
    print(f"  {'=' * 40}")
    print(f"  Total cells:  {total}")
    print(f"  Confirmed:    {by_status.get('confirmed', 0)}")
    print(f"  High:         {by_status.get('high', 0)}")
    print(f"  Guess:        {by_status.get('guess', 0)}")
    print()

    print(f"  By Category:")
    for cat in sorted(by_cat):
        print(f"    {cat:12s}  {by_cat[cat]}")
    print()

    print(f"  Top Subcategories:")
    for cat_sub in sorted(by_sub, key=lambda k: -by_sub[k])[:15]:
        print(f"    {cat_sub:30s}  {by_sub[cat_sub]}")


# ─── PNG Extraction ─────────────────────────────────────────────────

def extract_pngs(file_num: int) -> int:
    """Extract all 40x40 cells from a dragitem TGA as individual PNGs.

    Output: .cache/dragitemN/rRcC.png for each cell.
    Returns count of PNGs written.
    """
    fname = f"dragitem{file_num}"
    tga_path = ITEMS_DIR / f"{fname}.tga"
    if not tga_path.exists():
        print(f"  SKIP: {tga_path} not found")
        return 0

    out_dir = CACHE_DIR / fname
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(tga_path).convert("RGBA")
    count = 0
    for row in range(1, GRID + 1):
        for col in range(1, GRID + 1):
            x0 = (col - 1) * CELL
            y0 = (row - 1) * CELL
            cell = img.crop((x0, y0, x0 + CELL, y0 + CELL))
            png_path = out_dir / f"r{row}c{col}.png"
            cell.save(png_path, "PNG")
            count += 1

    print(f"  {fname}: {count} PNGs → {out_dir}")
    return count


def cmd_png(args):
    """Extract cell PNGs from TGA sprite sheets."""
    total = 0
    if args.file:
        name = args.file.replace(".tga", "").replace("dragitem", "")
        try:
            fnum = int(name)
        except ValueError:
            print(f"ERROR: Cannot parse file number from '{args.file}'")
            sys.exit(1)
        total = extract_pngs(fnum)
    else:
        files = sorted(
            ITEMS_DIR.glob("dragitem*.tga"),
            key=lambda p: int(p.stem.replace("dragitem", "")),
        )
        for fpath in files:
            fnum = int(fpath.stem.replace("dragitem", ""))
            total += extract_pngs(fnum)

    print(f"\n  Done: {total} PNGs extracted")


# ─── HTML Contact Sheet ─────────────────────────────────────────────

STATUS_COLORS = {
    "confirmed": "#69db7c",
    "high": "#ffd43b",
    "guess": "#ff8787",
}


def _cell_png_to_data_uri(file_num: int, row: int, col: int) -> str:
    """Get a base64 data URI for a cell PNG, extracting on-the-fly if needed."""
    fname = f"dragitem{file_num}"
    png_path = CACHE_DIR / fname / f"r{row}c{col}.png"

    if png_path.exists():
        data = png_path.read_bytes()
    else:
        # Extract directly from TGA
        tga_path = ITEMS_DIR / f"{fname}.tga"
        if not tga_path.exists():
            return ""
        img = Image.open(tga_path).convert("RGBA")
        x0 = (col - 1) * CELL
        y0 = (row - 1) * CELL
        cell = img.crop((x0, y0, x0 + CELL, y0 + CELL))
        buf = io.BytesIO()
        cell.save(buf, "PNG")
        data = buf.getvalue()

    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


def generate_html(file_num: int, catalog: dict) -> Path:
    """Generate an HTML contact sheet for one dragitem file."""
    fname = f"dragitem{file_num}"
    cells = catalog.get(fname, {})
    html_path = CACHE_DIR / f"{fname}.html"

    parts = [f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{fname}.tga — Thorne UI Icon Catalog</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #e0e0e0;
         margin: 20px; }}
  h1 {{ color: #c9a84c; border-bottom: 2px solid #c9a84c; padding-bottom: 8px; }}
  .grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px;
           max-width: 960px; }}
  .cell {{ background: #16213e; border: 2px solid #333; border-radius: 6px;
           padding: 6px; text-align: center; }}
  .cell:hover {{ border-color: #c9a84c; }}
  .cell img {{ width: 80px; height: 80px; image-rendering: pixelated;
              border: 1px solid #444; background: #000; display: block;
              margin: 0 auto 4px auto; }}
  .coord {{ font-size: 11px; color: #888; font-family: monospace; }}
  .cat {{ font-size: 12px; font-weight: bold; margin: 2px 0; }}
  .status {{ font-size: 10px; font-weight: bold; padding: 1px 6px;
            border-radius: 3px; display: inline-block; }}
  .name {{ font-size: 11px; color: #aaa; font-style: italic; }}
  .notes {{ font-size: 10px; color: #666; }}
  .legend {{ margin: 12px 0; font-size: 13px; }}
  .legend span {{ padding: 2px 8px; border-radius: 3px; margin-right: 10px; }}
  .empty-cell {{ opacity: 0.3; }}
</style></head><body>
<h1>{fname}.tga</h1>
<div class="legend">
  <span style="background:#69db7c;color:#000">confirmed</span>
  <span style="background:#ffd43b;color:#000">high</span>
  <span style="background:#ff8787;color:#000">guess</span>
</div>
<div class="grid">
"""]

    for row in range(1, GRID + 1):
        for col in range(1, GRID + 1):
            ck = f"[{row},{col}]"
            entry = cells.get(ck, {})
            cat = entry.get("cat", "?")
            sub = entry.get("sub", "?")
            status = entry.get("status", "guess")
            desc = entry.get("desc", "")
            notes = entry.get("notes", "")
            is_empty = cat == "empty"

            data_uri = _cell_png_to_data_uri(file_num, row, col)
            scolor = STATUS_COLORS.get(status, "#888")
            empty_cls = ' class="cell empty-cell"' if is_empty else ' class="cell"'

            parts.append(f'<div{empty_cls}>')
            if data_uri:
                parts.append(f'  <img src="{data_uri}" alt="{ck}">')
            parts.append(f'  <div class="coord">{ck}</div>')
            parts.append(f'  <div class="cat">{cat}/{sub}</div>')
            parts.append(f'  <span class="status" style="background:{scolor};color:#000">{status}</span>')
            if desc:
                parts.append(f'  <div class="name">{desc}</div>')
            if notes and not is_empty:
                parts.append(f'  <div class="notes">{notes}</div>')
            parts.append('</div>')

    parts.append("</div></body></html>")

    html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"  {fname}.html → {html_path}")
    return html_path


def cmd_html(args):
    """Generate HTML contact sheets for visual review."""
    catalog = load_catalog()
    paths = []

    if args.file:
        name = args.file.replace(".tga", "").replace("dragitem", "")
        try:
            fnum = int(name)
        except ValueError:
            print(f"ERROR: Cannot parse file number from '{args.file}'")
            sys.exit(1)
        paths.append(generate_html(fnum, catalog))
    else:
        files = sorted(
            ITEMS_DIR.glob("dragitem*.tga"),
            key=lambda p: int(p.stem.replace("dragitem", "")),
        )
        for fpath in files:
            fnum = int(fpath.stem.replace("dragitem", ""))
            paths.append(generate_html(fnum, catalog))

    print(f"\n  Done: {len(paths)} HTML contact sheets generated")


# ─── Main ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Iterative EQ dragitem icon catalog with learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python .bin/generate_catalog.py dragitem1        Analyze single file
              python .bin/generate_catalog.py --all            Analyze all files
              python .bin/generate_catalog.py --learn          Re-score from confirmed
              python .bin/generate_catalog.py --md             Regenerate markdown
              python .bin/generate_catalog.py --stats          Show statistics
              python .bin/generate_catalog.py --force dragitem1  Force re-analyze
              python .bin/generate_catalog.py --png            Extract all cell PNGs
              python .bin/generate_catalog.py --png dragitem1  Extract PNGs for one file
              python .bin/generate_catalog.py --html           HTML sheets for all files
              python .bin/generate_catalog.py --html dragitem1 HTML sheet for one file
        """),
    )
    parser.add_argument("file", nargs="?", help="dragitem file to analyze (e.g. dragitem1)")
    parser.add_argument("--all", action="store_true", help="Analyze all dragitem files")
    parser.add_argument("--force", action="store_true", help="Re-analyze even high-status items")
    parser.add_argument("--learn", action="store_true", help="Re-score unconfirmed from confirmed")
    parser.add_argument("--md", action="store_true", help="Regenerate markdown only")
    parser.add_argument("--stats", action="store_true", help="Show catalog statistics")
    parser.add_argument("--png", action="store_true", help="Extract cell PNGs from TGA sheets")
    parser.add_argument("--html", action="store_true", help="Generate HTML contact sheets")

    args = parser.parse_args()

    if args.learn:
        cmd_learn(args)
    elif args.md:
        cmd_md(args)
    elif args.stats:
        cmd_stats(args)
    elif args.png:
        cmd_png(args)
    elif args.html:
        cmd_html(args)
    elif args.file or args.all:
        cmd_analyze(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
