# Item Icon Catalog — Workflow Guide

The item catalog system identifies and classifies all 1,224 icons across 34 dragitem TGA sprite sheets. Each sheet is a 256×256 image containing a 6×6 grid of 40×40 pixel icons.

## Directory Layout

```
.Items/
  dragitem1.tga … dragitem34.tga   # Source sprite sheets
  item_catalog.json                 # Single source of truth (catalog + slot map)
  item_catalog.md                   # Generated markdown summary
  README.md                         # This file
  .cache/
    dragitem1/ … dragitem34/        # Extracted cell PNGs (40×40 → r1c1.png…r6c6.png)
    clip_refs.npz                   # CLIP reference centroids (from confirmed items)
    features.json                   # HOG feature cache (legacy)
    *.html                          # HTML contact sheets
```

## Scripts

Both scripts live in `.bin/` at the repo root.

### vision_classify.py — Primary Classification Engine

AI-powered classification using CLIP (image embeddings) and Ollama (vision LLM).

```bash
# Classify one file with hybrid mode (CLIP + Ollama descriptions)
python .bin/vision_classify.py --hybrid dragitem3

# Classify all unprocessed files
python .bin/vision_classify.py --hybrid

# Re-classify even confirmed items
python .bin/vision_classify.py --hybrid --force dragitem1

# Build CLIP reference centroids from confirmed items (do this after confirming)
python .bin/vision_classify.py --build-refs

# Run Ollama description pass on confirmed items
python .bin/vision_classify.py --describe dragitem1

# Test accuracy against confirmed items
python .bin/vision_classify.py --test
```

**Modes:**

| Flag | Backend | Purpose |
|------|---------|---------|
| `--hybrid` | CLIP + Ollama | **Recommended.** CLIP classifies, Ollama describes. Uses ref centroids when available. |
| `--clip` | CLIP only | Fast text-based zero-shot classification (~50% accuracy without refs) |
| `--ollama` | Ollama only | Vision LLM classification (slow, standalone accuracy is low) |
| `--hog` | scikit-image | Legacy HOG + color heuristic (poor accuracy) |
| `--describe` | Ollama | Description-only pass — adds `desc` field to confirmed items |
| `--build-refs` | CLIP | Builds reference centroids from confirmed items, then runs accuracy test |
| `--test` | varies | Tests all available backends against confirmed ground truth |

### generate_catalog.py — Utility & Output Generation

Handles PNG extraction, markdown generation, HTML contact sheets, and statistics.

```bash
# Extract cell PNGs from all TGA sheets (required before vision_classify)
python .bin/generate_catalog.py --png

# Extract PNGs for one file only
python .bin/generate_catalog.py --png dragitem3

# Regenerate markdown summary from JSON
python .bin/generate_catalog.py --md

# Show catalog statistics
python .bin/generate_catalog.py --stats

# Generate HTML contact sheets for visual review
python .bin/generate_catalog.py --html
```

**Superseded modes** (still functional but inferior to vision_classify):

| Flag | Purpose | Why superseded |
|------|---------|----------------|
| `dragitem1` | Heuristic pixel analysis | CLIP hybrid is far more accurate |
| `--all` | Batch heuristic analysis | Use `vision_classify.py --hybrid` instead |
| `--learn` | Re-score from confirmed refs | CLIP ref system (`--build-refs`) is superior |
| `--force` | Re-analyze with heuristic | Use `vision_classify.py --hybrid --force` |

## The Learning Loop

Classification improves iteratively as you confirm more items:

```
1. Extract PNGs    →  python .bin/generate_catalog.py --png
2. Classify        →  python .bin/vision_classify.py --hybrid dragitem1
3. Review & edit   →  Edit item_catalog.json, set "status": "confirmed"
4. Build refs      →  python .bin/vision_classify.py --build-refs
5. Classify next   →  python .bin/vision_classify.py --hybrid dragitem2
                      (now uses centroids from step 4 for better accuracy)
6. Repeat steps 3-5
```

**Accuracy progression:**
- Text-only CLIP: ~50%
- With 43 confirmed items (19 centroids): **97.7%**

## Data Governance — `_slot_map` Is the Master

The `_slot_map` field in `item_catalog.json` is the **single source of truth** for:
- **Categories** (armor, jewelry, weapon, container, misc, empty)
- **Subcategories** (helm, bracer, ring, sword_long, bag, scroll, etc.)
- **Equipment slot assignments** (head, chest, wrist, primary, etc.)

Both scripts derive their internal category lists from `_slot_map` at startup:
- `vision_classify.py` calls `load_valid_subs()` → builds `{sub: cat}` dict
- `generate_catalog.py` calls `load_master_categories()` → builds `{cat: [sub, ...]}` and `{sub: cat}` dicts

**Unknown subcategory warnings:** If any cell entry in the catalog has a `sub` value not present in `_slot_map`, both scripts print a warning at startup. To fix: either correct the cell entry or add the new subcategory to `_slot_map`.

### Adding a New Subcategory

1. Open `item_catalog.json`
2. Add the entry under the appropriate category in `_slot_map`:
   ```json
   "_slot_map": {
     "armor": {
       "helm": "head",
       "new_type": "slot_name"
     }
   }
   ```
3. The scripts will pick it up automatically on next run

## JSON Catalog Structure

```json
{
  "_meta": { "version": "2.0", "updated": "...", "confirmed": 76, ... },
  "_slot_map": {
    "armor": { "helm": "head", "bracer": "wrist", ... },
    "jewelry": { "ring": "fingers", "earring": "ear", ... },
    ...
  },
  "dragitem1": {
    "[1,1]": {
      "cat": "jewelry",
      "sub": "necklace",
      "status": "confirmed",
      "desc": "semi-hollow circular",
      "notes": ""
    },
    ...
  }
}
```

**Cell entry fields:**

| Field | Values | Meaning |
|-------|--------|---------|
| `cat` | armor, jewelry, weapon, container, misc, empty | Top-level category |
| `sub` | helm, ring, sword_long, bag, scroll, etc. | Specific subcategory |
| `status` | confirmed, high, guess, vision | Confidence level |
| `desc` | free text | Ollama-generated description of the icon |
| `notes` | free text | Script-generated metadata (e.g. "hybrid (0.95)") |

**Status levels:**
- `confirmed` — Human-verified ground truth. Used to build CLIP reference centroids.
- `high` — High-confidence machine classification
- `vision` — AI-classified but not yet verified
- `guess` — Low-confidence or heuristic guess

## Dependencies

- **Python 3.10+**
- **Pillow** — TGA/PNG image handling
- **open-clip-torch** — CLIP model (ViT-B-32, loaded on CPU)
- **torch** — PyTorch backend for CLIP
- **scikit-image** — HOG features (legacy, optional)
- **Ollama** — Local LLM server at `localhost:11434` with `gemma3:4b` model

Install with:
```bash
pip install Pillow open-clip-torch torch scikit-image
```

Ollama must be running separately (`ollama serve`).
