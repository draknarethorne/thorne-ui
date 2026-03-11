"""vision_classify.py -- DEPRECATED / EXPERIMENTAL

This script was the AI-powered icon classification system using multiple
backends (HOG, CLIP, Ollama). It is preserved as a reference for the AI
techniques used (CLIP zero-shot, HOG feature matching, Ollama vision LLM)
but is NO LONGER USED in the active pipeline.

Replaced by:
  - extract_eq_items.py   (Quarm SQL database → real item data)
  - pick_class_icons.py   (stat-weighted scoring per class + slot)

Those scripts use actual game item data rather than visual classification.

Original description follows:
---
AI-powered icon classification for EQ dragitem sprites.

Three classification backends (tiers), each with different tradeoffs:

  Tier 1: HOG    -- Shape-based features (HOG + color histogram + contours)
                    Fast, local, no model download. Best for --learn similarity.
  Tier 2: CLIP   -- Zero-shot text-image matching (OpenAI CLIP)
                    Excellent accuracy, local, needs ~600MB model download.
  Tier 3: Ollama -- Local vision LLM (gemma3:4b or similar)
                    Most accurate, free, needs Ollama installed + model pulled.

Usage:
    python .bin/vision_classify.py --hog                 # Tier 1: all files
    python .bin/vision_classify.py --hog dragitem1       # Tier 1: one file
    python .bin/vision_classify.py --clip                # Tier 2: all files
    python .bin/vision_classify.py --clip dragitem1      # Tier 2: one file
    python .bin/vision_classify.py --ollama              # Tier 3: all files
    python .bin/vision_classify.py --ollama dragitem1    # Tier 3: one file
    python .bin/vision_classify.py --hybrid              # CLIP classify + Ollama describe
    python .bin/vision_classify.py --hybrid dragitem1    # Hybrid: one file
    python .bin/vision_classify.py --describe             # Update descriptions via Ollama
    python .bin/vision_classify.py --describe dragitem1   # Describe one file
    python .bin/vision_classify.py --build-refs           # Build CLIP reference centroids
    python .bin/vision_classify.py --test                # Test all tiers on dragitem1

Options:
    --force       Re-classify confirmed items too (for testing only)
                  For --describe: overwrite existing descriptions
    --dry-run     Show results without writing to catalog
    --model NAME  Override default model (clip: model name, ollama: model tag)

Status written: "vision" (new tier between "high" and "confirmed")
  - Never overwrites "confirmed" entries (unless --force)
  - Overwrites "guess" and "high" entries
  - "desc" field is NEVER overwritten (user-owned) except by --describe --force
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

# ─── Paths ───────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO / ".master" / "items"
CATALOG_JSON = ITEMS_DIR / "item_catalog.json"
CACHE_DIR = ITEMS_DIR / ".cache"

CELL = 40
GRID = 6
CLIP_REFS_PATH = CACHE_DIR / "clip_refs.npz"

# ─── Valid subcategories (loaded from _slot_map in item_catalog.json) ─
# The _slot_map is the single source of truth for categories, subcategories,
# and equipment slot assignments. Populated at startup by load_valid_subs().

VALID_SUBS: dict[str, str] = {}  # sub -> cat (populated at runtime)


def load_valid_subs(catalog: dict) -> dict[str, str]:
    """Build flat {sub: cat} dict from _slot_map in catalog."""
    subs: dict[str, str] = {}
    for cat, cat_subs in catalog.get("_slot_map", {}).items():
        if isinstance(cat_subs, dict):
            for sub in cat_subs:
                subs[sub] = cat
    return subs


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
    return warnings


# ─── Catalog I/O ─────────────────────────────────────────────────────

def load_catalog() -> dict:
    if CATALOG_JSON.exists():
        return json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    return {"_meta": {}, "_slot_map": {}}



def save_catalog(catalog: dict) -> None:
    """Save catalog in compact format (one item per line, slot_map pretty-printed)."""
    from datetime import datetime

    # Update meta stats
    stats = {"confirmed": 0, "high": 0, "guess": 0, "vision": 0, "total": 0}
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

    lines = ["{"]

    # Meta block
    lines.append(f'  "_meta": {json.dumps(catalog["_meta"])},') 

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

    # File data blocks
    file_keys = sorted(
        (k for k in catalog if not k.startswith("_")),
        key=lambda k: int(k.replace("dragitem", "")),
    )
    for i, fk in enumerate(file_keys):
        cells = catalog[fk]
        lines.append(f'  "{fk}": {{')
        cell_keys = sorted(cells.keys(), key=lambda ck: tuple(
            int(x) for x in ck.strip("[]").split(",")
        ))
        for j, ck in enumerate(cell_keys):
            entry = cells[ck]
            comma = "," if j < len(cell_keys) - 1 else ""
            lines.append(f'    "{ck}": {json.dumps(entry, separators=(",", ":"))}{comma}')
        trail = "," if i < len(file_keys) - 1 else ""
        lines.append(f"  }}{trail}")

    lines.append("}")
    CATALOG_JSON.write_text("\n".join(lines) + "\n", encoding="utf-8")


def png_path(file_key: str, row: int, col: int) -> Path:
    return CACHE_DIR / file_key / f"r{row}c{col}.png"


def load_png(path: Path, upscale: int = 4, bg_color: tuple = (0, 0, 0),
             resample: int | None = None) -> Image.Image:
    """Load a PNG and upscale for better model input.
    
    Args:
        bg_color: Background RGB tuple. (0,0,0)=black, (255,255,255)=white.
        resample: PIL resample filter. None defaults to NEAREST.
    """
    img = Image.open(path).convert("RGBA")
    bg = Image.new("RGB", img.size, bg_color)
    bg.paste(img, mask=img.split()[3])
    if upscale > 1:
        w, h = bg.size
        filt = resample if resample is not None else Image.Resampling.NEAREST
        bg = bg.resize((w * upscale, h * upscale), filt)
    return bg


def img_to_base64(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ─── Label Maps ──────────────────────────────────────────────────────

# CLIP text prompts — consolidated to reduce confusion between near-synonyms.
# Each key is a "CLIP group" that maps to one or more catalog subcategories.
# After CLIP picks a group, we map it back to the best catalog sub via CLIP_TO_SUB.
CLIP_LABELS = {
    # Armor — head
    "helm": "a small pixel art icon of a metal helmet or helm headgear",
    "crown": "a small pixel art icon of a crown circlet or tiara headpiece",
    "face": "a small pixel art icon of a face mask or visor",
    # Armor — hands/wrists
    "gloves": "a small pixel art icon of gloves gauntlets or hand armor",
    "bracer": "a small pixel art icon of a wrist bracer or arm guard",
    # Armor — body
    "tunic": "a small pixel art icon of armor tunic vest breastplate or robe",
    "cape": "a small pixel art icon of a cape cloak or mantle worn on back",
    "belt": "a small pixel art icon of a belt sash or waistband",
    "boots": "a small pixel art icon of boots greaves or foot armor",
    "pauldrons": "a small pixel art icon of shoulder armor or pauldrons",
    # Armor — shield
    "shield": "a small pixel art icon of a shield",
    # Jewelry
    "necklace": "a small pixel art icon of a necklace pendant or chain",
    "bracelet": "a small pixel art icon of a bracelet or bangle wristband",
    "ring": "a small pixel art icon of a finger ring or band",
    "earring": "a small pixel art icon of an earring or ear stud",
    "charm": "a small pixel art icon of a talisman charm idol or amulet",
    # Weapons
    "sword": "a small pixel art icon of a sword or blade weapon",
    "dagger": "a small pixel art icon of a dagger or small knife",
    "axe": "a small pixel art icon of an axe weapon",
    "mace": "a small pixel art icon of a mace club or hammer weapon",
    "spear": "a small pixel art icon of a spear lance or polearm",
    "staff": "a small pixel art icon of a staff or walking stick",
    "bow": "a small pixel art icon of a bow or ranged weapon",
    # Containers
    "bag": "a small pixel art icon of a bag sack or container",
    "box": "a small pixel art icon of a box chest or crate",
    # Misc
    "scroll": "a small pixel art icon of a scroll page spell or parchment",
    "potion": "a small pixel art icon of a potion bottle or flask",
    "food": "a small pixel art icon of food drink or consumable item",
    "gem": "a small pixel art icon of a gemstone jewel or crystal",
    "lightstone": "a small pixel art icon of a glowing stone or light source",
    "instrument": "a small pixel art icon of a musical instrument",
    "other": "a small pixel art icon of a miscellaneous fantasy item",
}

# Map CLIP group → default catalog subcategory.
# Some groups collapse multiple subs (e.g. CLIP "gloves" handles gauntlets too).
# The hybrid pipeline can later refine via Ollama description.
CLIP_TO_SUB = {
    "helm": "helm",
    "crown": "crown",
    "face": "face",
    "gloves": "gloves",
    "bracer": "bracer",
    "tunic": "tunic",
    "cape": "cape",
    "belt": "belt",
    "boots": "boots",
    "pauldrons": "pauldrons",
    "shield": "shield_round",
    "necklace": "necklace",
    "bracelet": "bracelet",
    "ring": "ring",
    "earring": "earring",
    "charm": "charm",
    "sword": "sword_long",
    "dagger": "dagger",
    "axe": "axe",
    "mace": "mace",
    "spear": "spear",
    "staff": "staff",
    "bow": "bow",
    "bag": "bag",
    "box": "box",
    "scroll": "scroll",
    "potion": "potion",
    "food": "food",
    "gem": "gem",
    "lightstone": "lightstone",
    "instrument": "instrument",
    "other": "other",
}

# For accuracy testing: CLIP groups that should match each catalog sub.
# e.g. "gauntlets" in catalog → CLIP "gloves" group counts as correct.
SUB_TO_CLIP_GROUP = {
    "helm": "helm", "cap": "helm",
    "crown": "crown",
    "face": "face",
    "gloves": "gloves", "gauntlets": "gloves",
    "bracer": "bracer",
    "breastplate": "tunic", "tunic": "tunic", "robe": "tunic",
    "cape": "cape", "cloak": "cape",
    "belt": "belt",
    "boots": "boots", "greaves": "boots",
    "pauldrons": "pauldrons",
    "shield_round": "shield", "shield_kite": "shield",
    "shield_tower": "shield", "shield_ornate": "shield",
    "necklace": "necklace",
    "bracelet": "bracelet",
    "ring": "ring",
    "earring": "earring",
    "charm": "charm",
    "sword_long": "sword", "sword_short": "sword",
    "sword_2h": "sword", "katana": "sword",
    "dagger": "dagger",
    "axe": "axe",
    "mace": "mace",
    "spear": "spear",
    "staff": "staff",
    "bow": "bow", "arrow": "bow",
    "bag": "bag", "box": "box",
    "scroll": "scroll", "spell": "scroll",
    "potion": "potion",
    "food": "food",
    "gem": "gem",
    "lightstone": "lightstone",
    "instrument": "instrument",
    "spellbook": "scroll", "lantern": "lightstone",
    "fishing": "other", "other": "other",
}

# Ollama prompt — classify + describe (two lines)
OLLAMA_PROMPT = """This is a 40x40 pixel art icon from the classic MMORPG EverQuest (1999).
It depicts an inventory item. Classify it as ONE of these types:
helm, cap, breastplate, tunic, robe, shield_round, shield_kite, shield_tower,
gauntlets, gloves, bracer, pauldrons, greaves, boots, cloak, cape, belt, face,
ring, earring, necklace, bracelet, charm, crown,
sword_long, sword_short, sword_2h, katana, dagger, axe, mace, spear, staff, bow, arrow,
bag, box, scroll, spell, potion, food, instrument, gem, lightstone, spellbook, lantern, fishing, other.

Reply in exactly 2 lines:
Line 1: item type (one word from the list above)
Line 2: brief description of the item"""

# Ollama prompt — describe only (given a known classification)
OLLAMA_DESCRIBE_PROMPT = """This is a 40x40 pixel art icon from EverQuest (1999).
I already know this item is a {item_type}.
Describe what this specific {item_type} looks like in 5-10 words.
Focus on materials, colors, and distinguishing features.
Reply with ONLY the description, nothing else."""


# ═════════════════════════════════════════════════════════════════════
# TIER 1: HOG + Color Histogram Features
# ═════════════════════════════════════════════════════════════════════

def classify_hog(img: Image.Image) -> tuple[str, float]:
    """Classify using HOG features + color histogram with KNN against
    confirmed items. Returns (sub, confidence)."""
    from skimage.feature import hog
    import cv2

    # Convert to grayscale numpy
    gray = np.array(img.convert("L"))

    # HOG descriptor — captures shape outlines
    hog_features = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        feature_vector=True,
    )

    # Color histogram (H and S channels from HSV)
    bgr = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hist_h = cv2.calcHist([hsv], [0], None, [18], [0, 180]).flatten()
    hist_s = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()

    # Normalize histograms
    hist_h = hist_h / (hist_h.sum() + 1e-6)
    hist_s = hist_s / (hist_s.sum() + 1e-6)

    # Contour shape features
    gray_cv = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_cv, 15, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circularity = 0.0
    solidity = 0.0
    extent = 0.0
    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        if hull_area > 0:
            solidity = area / hull_area
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 0:
            extent = area / (w * h)

    # Combine into single feature vector
    shape_feats = np.array([circularity, solidity, extent])
    combined = np.concatenate([hog_features, hist_h, hist_s, shape_feats])

    return combined


def build_hog_references(catalog: dict) -> dict[str, list[np.ndarray]]:
    """Build HOG feature vectors from confirmed items."""
    refs: dict[str, list[np.ndarray]] = {}
    for file_key, cells in catalog.items():
        if file_key.startswith("_"):
            continue
        for cell_key, entry in cells.items():
            if entry.get("status") != "confirmed":
                continue
            sub = entry.get("sub", "other")
            if sub == "empty":
                continue
            row, col = parse_cell_key(cell_key)
            p = png_path(file_key, row, col)
            if not p.exists():
                continue
            img = load_png(p, upscale=4)
            fvec = classify_hog(img)
            if sub not in refs:
                refs[sub] = []
            refs[sub].append(fvec)
    return refs


def classify_hog_by_reference(fvec: np.ndarray, refs: dict[str, list[np.ndarray]]) -> tuple[str, float]:
    """Match a HOG feature vector against references using cosine similarity."""
    best_sub = "other"
    best_sim = -1.0
    fv_norm = np.linalg.norm(fvec)
    if fv_norm < 1e-6:
        return ("other", 0.0)

    for sub, ref_vectors in refs.items():
        for rv in ref_vectors:
            rv_norm = np.linalg.norm(rv)
            if rv_norm < 1e-6:
                continue
            sim = float(np.dot(fvec, rv) / (fv_norm * rv_norm))
            if sim > best_sim:
                best_sim = sim
                best_sub = sub
    return (best_sub, best_sim)


def parse_cell_key(ck: str) -> tuple[int, int]:
    """Parse '[row,col]' → (row, col)."""
    inner = ck.strip("[]")
    r, c = inner.split(",")
    return int(r), int(c)


# ═════════════════════════════════════════════════════════════════════
# TIER 2: CLIP Zero-Shot Classification
# ═════════════════════════════════════════════════════════════════════

_clip_model = None
_clip_preprocess = None
_clip_tokenizer = None
_clip_text_features = None
_clip_labels_order = None


def load_clip(model_name: str = "ViT-B-32", pretrained: str = "laion2b_s34b_b79k"):
    """Load CLIP model (cached after first call)."""
    global _clip_model, _clip_preprocess, _clip_tokenizer
    global _clip_text_features, _clip_labels_order

    if _clip_model is not None:
        return

    import open_clip
    import torch

    print(f"  Loading CLIP model {model_name}/{pretrained}...")
    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name, pretrained=pretrained
    )
    tokenizer = open_clip.get_tokenizer(model_name)
    model.eval()

    # Pre-encode all text labels
    labels_order = list(CLIP_LABELS.keys())
    texts = [CLIP_LABELS[k] for k in labels_order]
    text_tokens = tokenizer(texts)

    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    _clip_model = model
    _clip_preprocess = preprocess
    _clip_tokenizer = tokenizer
    _clip_text_features = text_features
    _clip_labels_order = labels_order
    print(f"  CLIP ready ({len(labels_order)} labels encoded)")


def classify_clip(img: Image.Image) -> tuple[str, float]:
    """Classify an image using CLIP. Returns (catalog_sub, confidence).

    CLIP picks from consolidated groups (CLIP_LABELS), then maps
    to catalog subcategories via CLIP_TO_SUB.
    """
    import torch

    load_clip()

    # Preprocess image
    img_rgb = img.convert("RGB")
    img_tensor = _clip_preprocess(img_rgb).unsqueeze(0)

    with torch.no_grad():
        image_features = _clip_model.encode_image(img_tensor)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        # Cosine similarity with all text labels
        similarity = (image_features @ _clip_text_features.T).squeeze(0)
        probs = similarity.softmax(dim=-1)

    best_idx = probs.argmax().item()
    clip_group = _clip_labels_order[best_idx]
    confidence = probs[best_idx].item()

    # Map CLIP group → catalog subcategory
    sub = CLIP_TO_SUB.get(clip_group, clip_group)

    return (sub, confidence)


# ─── CLIP Reference (Exemplar) System ────────────────────────────────

_clip_ref_centroids = None   # dict[sub_name, np.ndarray (512-d)]
_clip_ref_labels = None      # list[str] of sub names matching centroid order
_clip_ref_matrix = None      # np.ndarray shape (N, 512) for fast batch cosine sim


def build_clip_references(catalog: dict) -> dict:
    """Encode all confirmed non-empty cells with CLIP, average by subcategory.

    Saves centroid vectors to clip_refs.npz for fast loading.
    Returns {sub: np.ndarray} centroid dict.
    """
    import torch

    load_clip()

    # Collect confirmed items grouped by sub
    groups: dict[str, list[Path]] = {}
    for file_key, cells in catalog.items():
        if file_key.startswith("_"):
            continue
        for ck, entry in cells.items():
            if entry.get("status") != "confirmed":
                continue
            sub = entry.get("sub", "")
            if not sub or sub == "empty":
                continue
            row, col = parse_cell_key(ck)
            p = png_path(file_key, row, col)
            if p.exists():
                groups.setdefault(sub, []).append(p)

    if not groups:
        print("  No confirmed items found to build references.")
        return {}

    # Encode all images and compute centroids
    centroids = {}
    total_images = sum(len(v) for v in groups.values())
    encoded = 0

    for sub, paths in sorted(groups.items()):
        embeddings = []
        for p in paths:
            img = load_png(p, upscale=4, bg_color=(255, 255, 255),
                           resample=Image.Resampling.LANCZOS)
            img_rgb = img.convert("RGB")
            img_tensor = _clip_preprocess(img_rgb).unsqueeze(0)

            with torch.no_grad():
                feat = _clip_model.encode_image(img_tensor)
                feat /= feat.norm(dim=-1, keepdim=True)
                embeddings.append(feat.squeeze(0).numpy())

            encoded += 1

        # Average and re-normalize
        centroid = np.mean(embeddings, axis=0)
        centroid = centroid / (np.linalg.norm(centroid) + 1e-8)
        centroids[sub] = centroid
        print(f"    {sub:20s}  {len(paths):3d} images -> centroid", flush=True)

    # Save to npz
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    labels = sorted(centroids.keys())
    matrix = np.stack([centroids[s] for s in labels])
    np.savez(CLIP_REFS_PATH, labels=np.array(labels), centroids=matrix)

    print(f"\n  Saved: {len(labels)} centroids ({total_images} images) -> {CLIP_REFS_PATH.name}")
    return centroids


def load_clip_references() -> bool:
    """Load pre-built CLIP reference centroids. Returns True if loaded."""
    global _clip_ref_centroids, _clip_ref_labels, _clip_ref_matrix

    if _clip_ref_matrix is not None:
        return True

    if not CLIP_REFS_PATH.exists():
        return False

    data = np.load(CLIP_REFS_PATH, allow_pickle=False)
    labels = list(data["labels"])
    matrix = data["centroids"]

    _clip_ref_labels = labels
    _clip_ref_matrix = matrix
    _clip_ref_centroids = {l: matrix[i] for i, l in enumerate(labels)}
    return True


def classify_clip_ref(img: Image.Image) -> tuple[str, float]:
    """Classify an image against CLIP reference centroids (exemplar matching).

    Returns (catalog_sub, confidence) where confidence is cosine similarity.
    Much higher confidence spread than text-based CLIP.
    """
    import torch

    load_clip()
    if _clip_ref_matrix is None:
        raise RuntimeError("CLIP references not loaded. Run --build-refs first.")

    img_rgb = img.convert("RGB")
    img_tensor = _clip_preprocess(img_rgb).unsqueeze(0)

    with torch.no_grad():
        feat = _clip_model.encode_image(img_tensor)
        feat /= feat.norm(dim=-1, keepdim=True)
        feat_np = feat.squeeze(0).numpy()

    # Cosine similarity against all centroids (matrix is already normalized)
    sims = _clip_ref_matrix @ feat_np
    best_idx = int(np.argmax(sims))
    best_sub = _clip_ref_labels[best_idx]
    best_conf = float(sims[best_idx])

    return (best_sub, best_conf)


# ═════════════════════════════════════════════════════════════════════
# TIER 3: Ollama Local Vision LLM
# ═════════════════════════════════════════════════════════════════════

OLLAMA_URL = "http://localhost:11434"


def check_ollama() -> bool:
    """Check if Ollama is running."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError):
        return False


def list_ollama_models() -> list[str]:
    """List available Ollama models."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return [m["name"] for m in data.get("models", [])]
    except (urllib.error.URLError, OSError):
        return []


def classify_ollama(img: Image.Image, model: str = "gemma3:4b") -> tuple[str, float, str]:
    """Classify using Ollama vision API. Returns (sub, confidence, desc)."""
    b64 = img_to_base64(img)

    payload = json.dumps({
        "model": model,
        "prompt": OLLAMA_PROMPT,
        "images": [b64],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 60,
        },
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())

    raw = result.get("response", "").strip()
    lines = [l.strip() for l in raw.split("\n") if l.strip()]

    # Parse line 1: classification
    sub = "other"
    conf = 0.30
    if lines:
        type_line = lines[0].lower().strip(".")
        # Try exact match first
        for word in type_line.split():
            word = word.strip(".,;:!?\"'()")
            if word in VALID_SUBS:
                sub = word
                conf = 0.85
                break
        # Partial match fallback
        if sub == "other":
            for s in VALID_SUBS:
                if s in type_line:
                    sub = s
                    conf = 0.70
                    break

    # Parse line 2: description (if present)
    desc = ""
    if len(lines) >= 2:
        desc = lines[1].strip().strip(".").lower()
        # Clean common LLM prefixes
        for prefix in ["description:", "desc:", "- "]:
            if desc.startswith(prefix):
                desc = desc[len(prefix):].strip()

    return (sub, conf, desc)


def describe_ollama(img: Image.Image, item_type: str, model: str = "gemma3:4b") -> str:
    """Ask Ollama to describe an item we've already classified via CLIP.
    Returns a short description string."""
    b64 = img_to_base64(img)
    prompt = OLLAMA_DESCRIBE_PROMPT.format(item_type=item_type)

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 40,
        },
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        raw = result.get("response", "").strip()
        # Take first line, clean up
        desc = raw.split("\n")[0].strip().strip(".").lower()
        for prefix in ["description:", "desc:", "- ", "the ", "a ", "an "]:
            if desc.startswith(prefix):
                desc = desc[len(prefix):].strip()
        return desc
    except (urllib.error.URLError, OSError, TimeoutError):
        return ""


# ═════════════════════════════════════════════════════════════════════
# Description-Only Pass (for confirmed items)
# ═════════════════════════════════════════════════════════════════════

def describe_file(
    file_key: str,
    catalog: dict,
    model: str | None = None,
    force: bool = False,
) -> dict:
    """Generate/update descriptions for items in a file via Ollama.

    Unlike classify_file, this ONLY touches descriptions:
      - Processes confirmed items (and vision/high/guess)
      - Skips empty cells
      - Only fills empty desc unless --force

    Returns {cell_key: (sub, new_desc)} for items that got descriptions.
    """
    results = {}
    file_data = catalog.get(file_key, {})
    ollama_model = model or "gemma3:4b"

    # Collect work items for progress count
    work_items = []
    for row in range(1, GRID + 1):
        for col in range(1, GRID + 1):
            ck = f"[{row},{col}]"
            existing = file_data.get(ck, {})
            sub = existing.get("sub", "")
            if not sub or sub == "empty":
                continue
            if existing.get("desc") and not force:
                continue
            p = png_path(file_key, row, col)
            if p.exists():
                work_items.append((row, col, ck, existing, sub, p))

    total = len(work_items)
    if total == 0:
        return results

    for idx, (row, col, ck, existing, sub, p) in enumerate(work_items, 1):
            img = load_png(p, upscale=4)
            desc = describe_ollama(img, sub, model=ollama_model)

            if desc:
                results[ck] = (sub, desc)
                print(f"    [{idx}/{total}] {ck} [{sub:15s}] \"{desc}\"", flush=True)
            else:
                print(f"    [{idx}/{total}] {ck} [{sub:15s}] (no description)", flush=True)

    return results


def apply_descriptions(
    catalog: dict,
    file_key: str,
    results: dict,
    force: bool = False,
) -> int:
    """Write Ollama descriptions back to catalog. Never changes cat/sub/status.
    Returns count of descriptions updated."""
    file_data = catalog.get(file_key, {})
    updated = 0

    for ck, (sub, new_desc) in results.items():
        existing = file_data.get(ck, {})
        old_desc = existing.get("desc", "")

        # Only overwrite if empty or forced
        if old_desc and not force:
            continue

        existing["desc"] = new_desc
        file_data[ck] = existing
        updated += 1

    return updated


# ═════════════════════════════════════════════════════════════════════
# Core Classification Engine
# ═════════════════════════════════════════════════════════════════════

def is_empty_cell(path: Path) -> bool:
    """Quick check if a cell PNG is mostly transparent."""
    img = Image.open(path).convert("RGBA")
    alpha = np.array(img)[:, :, 3]
    return int((alpha >= 30).sum()) < (CELL * CELL * 0.02)


def classify_file(
    file_key: str,
    catalog: dict,
    backend: str,
    model: str | None = None,
    force: bool = False,
    dry_run: bool = False,
    hog_refs: dict | None = None,
) -> dict:
    """Classify all cells in a file. Returns {cell_key: (cat, sub, confidence, desc)}."""
    results = {}
    file_data = catalog.get(file_key, {})
    ollama_model = model or "gemma3:4b"
    uses_ollama = backend in ("ollama", "hybrid")

    # Count work items for progress
    work_items = []
    for row in range(1, GRID + 1):
        for col in range(1, GRID + 1):
            ck = f"[{row},{col}]"
            existing = file_data.get(ck, {})
            status = existing.get("status", "guess")
            if status == "confirmed" and not force:
                continue
            p = png_path(file_key, row, col)
            if p.exists():
                work_items.append((row, col, ck, existing))

    total = len(work_items)
    for idx, (row, col, ck, existing) in enumerate(work_items, 1):
            p = png_path(file_key, row, col)

            # Quick empty check
            if is_empty_cell(p):
                results[ck] = ("empty", "empty", 1.0, "")
                if uses_ollama:
                    print(f"    [{idx}/{total}] {ck} -> empty", flush=True)
                continue

            # Load and classify — CLIP uses white bg + LANCZOS, others use black + NEAREST
            desc = ""

            if backend == "hog":
                img = load_png(p, upscale=4)
                fvec = classify_hog(img)
                if hog_refs:
                    sub, conf = classify_hog_by_reference(fvec, hog_refs)
                else:
                    sub, conf = ("other", 0.0)
            elif backend == "clip":
                img = load_png(p, upscale=4, bg_color=(255, 255, 255),
                               resample=Image.Resampling.LANCZOS)
                sub, conf = classify_clip(img)
            elif backend == "ollama":
                img = load_png(p, upscale=4)
                sub, conf, desc = classify_ollama(img, model=ollama_model)
            elif backend == "hybrid":
                # Pass 1: CLIP classifies — use refs if available, else text labels
                img_clip = load_png(p, upscale=4, bg_color=(255, 255, 255),
                                    resample=Image.Resampling.LANCZOS)
                if _clip_ref_matrix is not None:
                    sub, conf = classify_clip_ref(img_clip)
                else:
                    sub, conf = classify_clip(img_clip)
                # Pass 2: Ollama describes (black bg for pixel art LLM)
                if conf > 0.02 and sub != "other":
                    img_ollama = load_png(p, upscale=4)
                    desc = describe_ollama(img_ollama, sub, model=ollama_model)
            else:
                raise ValueError(f"Unknown backend: {backend}")

            cat = VALID_SUBS.get(sub, "misc")
            results[ck] = (cat, sub, conf, desc)

            if uses_ollama:
                desc_tag = f"  \"{desc}\"" if desc else ""
                print(f"    [{idx}/{total}] {ck} -> {cat}/{sub} ({conf:.2f}){desc_tag}", flush=True)

    return results


def apply_results(
    catalog: dict,
    file_key: str,
    results: dict,
    backend: str,
    dry_run: bool = False,
    force: bool = False,
) -> int:
    """Write classification results back to catalog. Returns update count."""
    if file_key not in catalog:
        catalog[file_key] = {}
    file_data = catalog[file_key]
    updated = 0

    for ck, (cat, sub, conf, ai_desc) in results.items():
        existing = file_data.get(ck, {})
        old_status = existing.get("status", "guess")

        # Never overwrite confirmed unless forced
        if old_status == "confirmed" and not force:
            continue

        # Preserve user description; only fill from AI if empty
        desc = existing.get("desc", "")
        if not desc and ai_desc:
            desc = ai_desc

        notes = f"{backend} ({conf:.2f})"
        status = "vision" if conf > 0.5 else "guess"

        # Empty cells auto-confirm
        if sub == "empty":
            status = "confirmed"
            notes = "transparent"

        file_data[ck] = {
            "cat": cat, "sub": sub,
            "status": status, "desc": desc, "notes": notes,
        }
        updated += 1

    return updated


# ═════════════════════════════════════════════════════════════════════
# Test Mode — Accuracy on Confirmed Items
# ═════════════════════════════════════════════════════════════════════

def test_accuracy(catalog: dict, backend: str, model: str | None = None):
    """Test a backend against all confirmed items. Prints accuracy report."""
    print(f"\n  Testing {backend.upper()} accuracy on confirmed items...")

    # Collect ground truth (non-empty confirmed only)
    ground_truth = []
    for file_key, cells in catalog.items():
        if file_key.startswith("_"):
            continue
        for ck, entry in cells.items():
            if entry.get("status") != "confirmed" or entry.get("sub") == "empty":
                continue
            row, col = parse_cell_key(ck)
            p = png_path(file_key, row, col)
            if p.exists():
                ground_truth.append((file_key, ck, entry["sub"], p))

    if not ground_truth:
        print("  No confirmed items found for testing.")
        return

    print(f"  Ground truth: {len(ground_truth)} confirmed items\n")

    # For HOG, build references EXCLUDING current test items (leave-one-out)
    hog_refs = None
    if backend == "hog":
        hog_refs = build_hog_references(catalog)
        if not hog_refs:
            print("  No HOG references available (need confirmed items).")
            return

    correct = 0
    wrong = []
    t0 = time.time()

    for file_key, ck, true_sub, path in ground_truth:
        ollama_model = model or "gemma3:4b"
        ai_desc = ""

        if backend == "hog":
            img = load_png(path, upscale=4)
            fvec = classify_hog(img)
            pred_sub, conf = classify_hog_by_reference(fvec, hog_refs)
        elif backend == "clip":
            img = load_png(path, upscale=4, bg_color=(255, 255, 255),
                           resample=Image.Resampling.LANCZOS)
            pred_sub, conf = classify_clip(img)
        elif backend == "ollama":
            img = load_png(path, upscale=4)
            pred_sub, conf, ai_desc = classify_ollama(img, model=ollama_model)
        elif backend == "clip-ref":
            img = load_png(path, upscale=4, bg_color=(255, 255, 255),
                           resample=Image.Resampling.LANCZOS)
            pred_sub, conf = classify_clip_ref(img)
        elif backend == "hybrid":
            img_clip = load_png(path, upscale=4, bg_color=(255, 255, 255),
                                resample=Image.Resampling.LANCZOS)
            if _clip_ref_matrix is not None:
                pred_sub, conf = classify_clip_ref(img_clip)
            else:
                pred_sub, conf = classify_clip(img_clip)
            img_ollama = load_png(path, upscale=4)
            ai_desc = describe_ollama(img_ollama, pred_sub, model=ollama_model)
        else:
            raise ValueError(f"Unknown backend: {backend}")

        if pred_sub == true_sub:
            correct += 1
            marker = "OK"
        elif backend in ("clip", "clip-ref", "hybrid"):
            # For CLIP-based backends, count as correct if same CLIP group
            true_group = SUB_TO_CLIP_GROUP.get(true_sub, true_sub)
            pred_group = SUB_TO_CLIP_GROUP.get(pred_sub, pred_sub)
            if true_group == pred_group:
                correct += 1
                marker = "~~"  # near-match (same group, different sub)
            else:
                wrong.append((file_key, ck, true_sub, pred_sub, conf))
                marker = "XX"
        else:
            wrong.append((file_key, ck, true_sub, pred_sub, conf))
            marker = "XX"

        desc_tag = f"  \"{ai_desc}\"" if ai_desc else ""
        print(f"    {marker} {file_key} {ck:8s} true={true_sub:15s} pred={pred_sub:15s} conf={conf:.2f}{desc_tag}")

    elapsed = time.time() - t0
    acc = correct / len(ground_truth) * 100

    print(f"\n  {'-' * 50}")
    print(f"  Accuracy: {correct}/{len(ground_truth)} = {acc:.1f}%")
    print(f"  Time: {elapsed:.1f}s ({elapsed/len(ground_truth):.2f}s/item)")

    if wrong:
        print(f"\n  Misclassified ({len(wrong)}):")
        for fk, ck, true, pred, conf in wrong:
            print(f"    {fk} {ck}: {true} -> {pred} ({conf:.2f})")

    return acc


# ═════════════════════════════════════════════════════════════════════
# CLI Entry Point
# ═════════════════════════════════════════════════════════════════════

def find_dragitem_files() -> list[str]:
    """Find all dragitemN keys that have cached PNGs."""
    files = []
    for d in sorted(CACHE_DIR.iterdir()):
        if d.is_dir() and d.name.startswith("dragitem"):
            files.append(d.name)
    return files


def main():
    parser = argparse.ArgumentParser(description="AI vision classification for EQ icons")
    parser.add_argument("file", nargs="?", help="Specific file (e.g. dragitem1)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hog", action="store_true", help="Tier 1: HOG + color features")
    group.add_argument("--clip", action="store_true", help="Tier 2: CLIP zero-shot")
    group.add_argument("--ollama", action="store_true", help="Tier 3: Ollama vision LLM")
    group.add_argument("--hybrid", action="store_true", help="CLIP classify + Ollama describe")
    group.add_argument("--describe", action="store_true", help="Ollama description-only pass")
    group.add_argument("--build-refs", action="store_true", help="Build CLIP reference centroids from confirmed items")
    group.add_argument("--test", action="store_true", help="Test all available backends")

    parser.add_argument("--force", action="store_true", help="Re-classify confirmed items")
    parser.add_argument("--dry-run", action="store_true", help="Don't write results")
    parser.add_argument("--model", help="Override model name")
    args = parser.parse_args()

    catalog = load_catalog()

    # Load valid subcategories from _slot_map (single source of truth)
    global VALID_SUBS
    VALID_SUBS = load_valid_subs(catalog)
    if not VALID_SUBS:
        print("ERROR: _slot_map is empty in item_catalog.json")
        sys.exit(1)

    # Validate all cell subs against _slot_map
    validate_catalog_subs(catalog)

    # ── Build refs mode ──
    if args.build_refs:
        print("\n  Building CLIP reference centroids from confirmed items...")
        refs = build_clip_references(catalog)
        if refs:
            # Run quick accuracy test with the new refs
            print("\n  Quick accuracy test with new references...")
            load_clip_references()
            test_accuracy(catalog, "clip-ref")
        return

    # ── Test mode ──
    if args.test:
        print("=" * 60)
        print("  Vision Classification Accuracy Test")
        print("=" * 60)

        # Always test HOG (fast)
        try:
            test_accuracy(catalog, "hog")
        except Exception as e:
            print(f"  HOG test failed: {e}")

        # Test CLIP if available
        try:
            test_accuracy(catalog, "clip", model=args.model)
        except Exception as e:
            print(f"  CLIP test failed: {e}")

        # Test CLIP-ref if references exist
        if load_clip_references():
            try:
                test_accuracy(catalog, "clip-ref", model=args.model)
            except Exception as e:
                print(f"  CLIP-ref test failed: {e}")

        # Test Hybrid (CLIP + Ollama describe) if Ollama is running
        if check_ollama():
            models = list_ollama_models()
            if models:
                ollama_model = args.model or "gemma3:4b"
                for m in models:
                    if ollama_model in m or m.startswith(ollama_model.split(":")[0]):
                        ollama_model = m
                        break
                try:
                    test_accuracy(catalog, "hybrid", model=ollama_model)
                except Exception as e:
                    print(f"  Hybrid test failed: {e}")

        # Test Ollama standalone if running
        if check_ollama():
            models = list_ollama_models()
            if models:
                ollama_model = args.model or "gemma3:4b"
                # Find closest available model
                for m in models:
                    if ollama_model in m or m.startswith(ollama_model.split(":")[0]):
                        ollama_model = m
                        break
                try:
                    test_accuracy(catalog, "ollama", model=ollama_model)
                except Exception as e:
                    print(f"  Ollama test failed: {e}")
            else:
                print("\n  Ollama: no models pulled yet")
        else:
            print("\n  Ollama: not running (skipped)")

        return

    # ── Determine backend ──
    if args.hog:
        backend = "hog"
    elif args.clip:
        backend = "clip"
    elif args.ollama:
        backend = "ollama"
        if not check_ollama():
            print("ERROR: Ollama is not running. Start it with: ollama serve")
            sys.exit(1)
    elif args.hybrid:
        backend = "hybrid"
        if not check_ollama():
            print("ERROR: Hybrid mode needs Ollama running. Start it with: ollama serve")
            sys.exit(1)
        # Auto-load CLIP refs if available
        if load_clip_references():
            print(f"  CLIP references loaded: {len(_clip_ref_labels)} types")
        else:
            print("  No CLIP references found — using text labels (run --build-refs to improve)")
    elif args.describe:
        backend = "describe"
        if not check_ollama():
            print("ERROR: Describe mode needs Ollama running. Start it with: ollama serve")
            sys.exit(1)

    # ── Determine files ──
    if args.file:
        files = [args.file]
    else:
        files = find_dragitem_files()

    if not files:
        print("No dragitem files found in cache. Run: python .bin/generate_catalog.py --png")
        sys.exit(1)

    # ── Build references for HOG ──
    hog_refs = None
    if backend == "hog":
        print("  Building HOG references from confirmed items...")
        hog_refs = build_hog_references(catalog)
        print(f"  Built references: {sum(len(v) for v in hog_refs.values())} vectors across {len(hog_refs)} types")

    # ── Run ──
    total_updated = 0
    t0 = time.time()

    for file_key in files:
        cache_path = CACHE_DIR / file_key
        if not cache_path.is_dir():
            print(f"  SKIP: {file_key} (no cached PNGs)")
            continue

        if backend == "describe":
            # Description-only pass
            print(f"\n  Describing {file_key}...")
            results = describe_file(
                file_key, catalog,
                model=args.model, force=args.force,
            )

            if not args.dry_run:
                updated = apply_descriptions(
                    catalog, file_key, results, force=args.force,
                )
                total_updated += updated
                print(f"    -> {updated} descriptions updated")
            else:
                for ck in sorted(results.keys(), key=lambda k: parse_cell_key(k)):
                    sub, desc = results[ck]
                    print(f"    {ck:8s} [{sub:15s}] \"{desc}\"")
                total_updated += len(results)

        else:
            # Classification pass
            print(f"\n  Classifying {file_key}...")
            results = classify_file(
                file_key, catalog, backend,
                model=args.model, force=args.force,
                hog_refs=hog_refs,
            )

            if not args.dry_run:
                updated = apply_results(catalog, file_key, results, backend, force=args.force)
                total_updated += updated
                print(f"    -> {updated} cells updated")
            else:
                for ck in sorted(results.keys(), key=lambda k: parse_cell_key(k)):
                    cat, sub, conf, desc = results[ck]
                    desc_tag = f"  \"{desc}\"" if desc else ""
                    print(f"    {ck:8s} -> {cat}/{sub} ({conf:.2f}){desc_tag}")
                total_updated += len(results)

    elapsed = time.time() - t0
    action = "described" if backend == "describe" else f"classified via {backend}"

    if not args.dry_run and total_updated > 0:
        save_catalog(catalog)
        print(f"\n  Done: {total_updated} cells {action} in {elapsed:.1f}s")
        print(f"  Catalog saved: {CATALOG_JSON}")
    else:
        label = "(dry run)" if args.dry_run else ""
        print(f"\n  Done: {total_updated} cells {action} {label} in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
