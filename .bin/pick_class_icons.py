#!/usr/bin/env python3
"""Auto-select the best dragitem icon for each EQ class + equipment slot.

Uses per-class stat priorities to score icons and pick the most representative
icon per slot. Reads eq_items.csv and outputs recommendations.

All 15 EQ classes scored individually:
  Warrior, Rogue, Monk, Paladin, Shadowknight, Bard, Ranger, Shaman,
  Beastlord, Cleric, Druid, Necromancer, Wizard, Magician, Enchanter

Scoring:
  1. For each class, define primary/secondary stat weights
  2. For each slot, gather items usable by that class
  3. Group by icon, compute weighted stat score per icon
  4. Apply bonuses: item_count, exclusivity, class-specificity
  5. Rank icons — prefer well-represented, class-distinctive icons

Formula:
  stat_score   = avg(sum(stat * weight) for each statted item)
  spec_mult    = 1.0 + avg(1/n_classes_per_item)  (1.07-2.0x)
  count_bonus  = min(item_count, 20) * 0.5  (caps at 10.0)
  excl_bonus   = stat_score * 0.3 if icon unique to this class
  total_score  = (stat_score * spec_mult) + count_bonus + excl_bonus

  Min 2 items required to be "rank 1" pick (unless no 2+ icon exists).

Output: thorne_drak/Options/Slots/.Master/.Items/.cache/class_icon_picks.csv
        thorne_drak/Options/Slots/.Master/.Items/.cache/class_icon_picks.json
        thorne_drak/Options/Slots/.Master/.Items/.cache/class_icon_picks.html

Usage:
    python .bin/pick_class_icons.py
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CACHE_DIR = os.path.join(PROJECT_ROOT, 'thorne_drak', 'Options', 'Slots',
                        '.Master', '.Items', '.cache')

CSV_IN = os.path.join(CACHE_DIR, 'eq_items.csv')
JSON_OUT = os.path.join(CACHE_DIR, 'class_icon_picks.json')
CSV_OUT = os.path.join(CACHE_DIR, 'class_icon_picks.csv')
HTML_OUT = os.path.join(CACHE_DIR, 'class_icon_picks.html')

if not os.path.exists(CSV_IN):
    print("ERROR: eq_items.csv not found. Run extract_eq_items.py first.")
    sys.exit(1)

# ============================================================
# CLASS DEFINITIONS
# ============================================================

CLASS_BITS = {
    'WAR': 1, 'CLR': 2, 'PAL': 4, 'RNG': 8, 'SHD': 16,
    'DRU': 32, 'MNK': 64, 'BRD': 128, 'ROG': 256, 'SHM': 512,
    'NEC': 1024, 'WIZ': 2048, 'MAG': 4096, 'ENC': 8192,
    'BST': 16384, 'BER': 32768,
}

# All 15 EQ classes with individual stat-priority weights.
# primary=3.0, secondary=2.0, tertiary=1.0-1.5, minor=0.5-0.75
# hp/mana contribute based on class role
# ac scales with armor weight (plate=1.0, chain=0.75, leather=0.5, cloth=0.25)
CLASS_PROFILES = {
    # ── PLATE MELEE ──
    'Warrior': {
        'eq_classes': {'WAR'},
        'weights': {'astr': 3.0, 'asta': 2.0, 'aagi': 1.5, 'adex': 1.0,
                    'hp': 1.0, 'ac': 1.0, 'mana': 0.0},
        'description': 'Plate tank — highest AC, physical stats',
    },
    'Rogue': {
        'eq_classes': {'ROG'},
        'weights': {'aagi': 3.0, 'adex': 2.0, 'astr': 1.5, 'asta': 1.0,
                    'hp': 1.0, 'ac': 0.5, 'mana': 0.0},
        'description': 'Chain DPS — agility, dexterity, backstab',
    },
    # ── LEATHER/CLOTH MELEE ──
    'Monk': {
        'eq_classes': {'MNK'},
        'weights': {'aagi': 3.0, 'asta': 2.0, 'astr': 1.5, 'adex': 1.0,
                    'hp': 1.0, 'ac': 0.75, 'mana': 0.0},
        'description': 'Agility melee — cloth/leather, weight restrictions',
    },
    # ── PLATE HYBRIDS ──
    'Paladin': {
        'eq_classes': {'PAL'},
        'weights': {'asta': 2.5, 'astr': 2.0, 'awis': 1.5, 'acha': 1.0,
                    'hp': 1.0, 'mana': 0.75, 'ac': 1.0},
        'description': 'Plate healer/tank — stamina, wisdom, charisma',
    },
    'Shadowknight': {
        'eq_classes': {'SHD'},
        'weights': {'astr': 2.5, 'asta': 2.0, 'aint': 1.5, 'adex': 0.75,
                    'hp': 1.0, 'mana': 0.75, 'ac': 1.0},
        'description': 'Plate dark knight — strength, intelligence, lifetaps',
    },
    'Bard': {
        'eq_classes': {'BRD'},
        'weights': {'acha': 3.0, 'adex': 1.5, 'asta': 1.0, 'astr': 0.75, 'aagi': 0.75,
                    'hp': 1.0, 'mana': 0.5, 'ac': 0.75},
        'description': 'Plate support — charisma, dexterity, songs',
    },
    # ── CHAIN HYBRIDS ──
    'Ranger': {
        'eq_classes': {'RNG'},
        'weights': {'astr': 2.0, 'asta': 1.5, 'adex': 1.5, 'awis': 1.0, 'aagi': 1.0,
                    'hp': 1.0, 'mana': 0.5, 'ac': 0.75},
        'description': 'Chain melee/caster — bows, dual wield, nature',
    },
    'Shaman': {
        'eq_classes': {'SHM'},
        'weights': {'awis': 3.0, 'asta': 2.0, 'acha': 1.0, 'astr': 0.75,
                    'mana': 1.0, 'hp': 0.75, 'ac': 0.75},
        'description': 'Chain priest — wisdom, slow, buffs, melee hybrid',
    },
    'Beastlord': {
        'eq_classes': {'BST'},
        'weights': {'asta': 2.0, 'astr': 2.0, 'awis': 1.5, 'adex': 1.0, 'aagi': 1.0,
                    'hp': 1.0, 'mana': 0.75, 'ac': 0.75},
        'description': 'Leather melee/priest — balanced physical + wisdom',
    },
    # ── LEATHER/CLOTH PRIESTS ──
    'Cleric': {
        'eq_classes': {'CLR'},
        'weights': {'awis': 3.0, 'asta': 1.5, 'acha': 1.0,
                    'mana': 1.0, 'hp': 0.75, 'ac': 0.75},
        'description': 'Plate priest — wisdom, healing, high AC',
    },
    'Druid': {
        'eq_classes': {'DRU'},
        'weights': {'awis': 3.0, 'asta': 1.5, 'aint': 0.75,
                    'mana': 1.0, 'hp': 0.75, 'ac': 0.5},
        'description': 'Leather priest — wisdom, nature, versatile',
    },
    # ── INTELLIGENCE CASTERS ──
    'Necromancer': {
        'eq_classes': {'NEC'},
        'weights': {'aint': 3.0, 'asta': 1.5, 'astr': 0.5,
                    'mana': 1.0, 'hp': 0.75, 'ac': 0.25},
        'description': 'Cloth caster — intelligence, dark arts, pets',
    },
    'Wizard': {
        'eq_classes': {'WIZ'},
        'weights': {'aint': 3.0, 'asta': 1.5,
                    'mana': 1.0, 'hp': 0.5, 'ac': 0.25},
        'description': 'Cloth caster — intelligence, nukes, evocation',
    },
    'Magician': {
        'eq_classes': {'MAG'},
        'weights': {'aint': 3.0, 'asta': 1.5, 'acha': 0.5,
                    'mana': 1.0, 'hp': 0.5, 'ac': 0.25},
        'description': 'Cloth caster — intelligence, pets, conjuration',
    },
    'Enchanter': {
        'eq_classes': {'ENC'},
        'weights': {'aint': 2.5, 'acha': 2.5, 'asta': 1.0,
                    'mana': 1.0, 'hp': 0.5, 'ac': 0.25},
        'description': 'Cloth caster — intelligence, charisma, crowd control',
    },
}

# Equipment slot bitmasks
SLOT_BITS = {
    2: 'ear', 4: 'head', 8: 'face', 32: 'neck',
    64: 'shoulder', 128: 'arms', 256: 'back',
    512: 'wrist', 4096: 'hands',
    8192: 'primary', 16384: 'secondary',
    32768: 'fingers', 131072: 'chest', 262144: 'legs', 524288: 'feet',
    1048576: 'waist', 2048: 'range', 2097152: 'ammo',
}

SLOT_ORDER = [
    'ear', 'head', 'face', 'neck',
    'shoulder', 'arms', 'back', 'wrist',
    'hands', 'fingers', 'chest', 'legs', 'feet', 'waist',
    'primary', 'secondary', 'range', 'ammo',
]

ALL_STATS = ['astr', 'asta', 'aagi', 'adex', 'aint', 'awis', 'acha', 'hp', 'mana', 'ac',
             'cr', 'dr', 'fr', 'mr', 'pr']

# Filter out GM/test items with absurd stats (Ban Hammer etc.)
MAX_HP = 500
MAX_MANA = 500
MAX_AC = 300

# Armor slots where class-restricted items should be preferred over all-class.
# If enough class-restricted items exist (>=2 icons with 2+ items), use only those.
# Otherwise fall back to the full item pool.
ARMOR_SLOTS = {'head', 'face', 'neck', 'shoulder', 'arms', 'back', 'wrist',
               'hands', 'fingers', 'chest', 'legs', 'feet', 'waist'}

# Bitmask for weapon/shield slots (primary|secondary|range). Items whose icon
# ONLY appears on multi-slot items that also fit a weapon slot get penalised
# when scored for an armor slot — e.g. a shield icon in the 'back' slot.
WEAPON_SLOT_MASK = 8192 | 16384 | 2048  # primary | secondary | range

# Max classes an item can equip and still count as "class-restricted"
MAX_CLASSES_FOR_RESTRICTED = 6


def class_bitmask(eq_classes):
    """Convert a set of class abbreviations to a bitmask."""
    mask = 0
    for cls in eq_classes:
        mask |= CLASS_BITS.get(cls, 0)
    return mask


def score_item(item, weights):
    """Score a single item against stat weights."""
    score = 0.0
    for stat, weight in weights.items():
        val = int(item.get(stat, 0))
        if val > 0:
            score += val * weight
    return score


def class_specificity(items_for_icon, target_class_bit):
    """Compute how class-specific the items behind this icon are.

    Returns a multiplier (0.5 to 2.0):
    - Items worn by 1 class  → 2.0x  (strongly rewarded)
    - Items worn by 3 classes → ~1.3x
    - Items worn by 8 classes → ~0.8x
    - Items worn by 15 classes → 0.5x (heavily penalized)

    Uses log scaling: mult = 2.0 - 1.5 * log(n)/log(15)
    """
    if not items_for_icon:
        return 1.0
    import math
    log15 = math.log(15)
    specificities = []
    for item in items_for_icon:
        class_mask = int(item['classes'])
        n_classes = bin(class_mask).count('1')
        if n_classes == 0:
            continue
        # 2.0 at n=1, 0.5 at n=15
        specificities.append(2.0 - 1.5 * math.log(max(n_classes, 1)) / log15)
    if not specificities:
        return 1.0
    return sum(specificities) / len(specificities)  # range: 0.5 to 2.0


def score_icon_group(items_for_icon, weights, exclusivity=1.0, target_class_bit=0):
    """Score an icon based on the average stat score of its items.

    Returns (stat_score, item_count, total_score).
    - stat_score: average per-item score from stat weights
    - item_count: number of items behind this icon
    - total_score: stat_score + count_bonus + exclusivity_bonus
    - exclusivity: 0.0-1.0, how exclusive this icon is to this class group
    - target_class_bit: bitmask for the target class (for specificity bonus)
    """
    if not items_for_icon:
        return 0.0, 0, 0.0

    # Score items that have any stats at all
    statted_items = [i for i in items_for_icon if any(int(i.get(s, 0)) > 0 for s in ALL_STATS)]

    if not statted_items:
        # No statted items — score by item count alone (very low priority)
        return 0.0, len(items_for_icon), len(items_for_icon) * 0.5

    scores = [score_item(i, weights) for i in statted_items]
    avg_score = sum(scores) / len(scores)

    # Popularity bonus — capped at 20 items (max 10.0 bonus)
    count_bonus = min(len(items_for_icon), 20) * 0.5

    # Exclusivity bonus — reward class-distinctive icons
    excl_bonus = avg_score * 0.3 * exclusivity

    # Class specificity — reward icons whose items are class-restricted
    # Items usable by 1 class get 2x, items usable by all get ~1.07x
    spec_mult = class_specificity(items_for_icon, target_class_bit)

    total = (avg_score * spec_mult) + count_bonus + excl_bonus
    return avg_score, len(items_for_icon), total


def icon_png_path(icon):
    """Return relative path from .cache/ to the icon PNG (1-based row/col)."""
    adjusted = icon - 500
    dragitem_file = adjusted // 36 + 1
    cell = adjusted % 36
    row = cell % 6 + 1   # 1-based, col-major
    col = cell // 6 + 1  # 1-based, col-major
    return f"dragitem{dragitem_file}/r{row}c{col}.png"


def icon_png_exists(icon):
    """Check if the PNG file exists for this icon."""
    adjusted = icon - 500
    dragitem_file = adjusted // 36 + 1
    cell = adjusted % 36
    row = cell % 6 + 1   # 1-based, col-major
    col = cell // 6 + 1  # 1-based, col-major
    path = os.path.join(CACHE_DIR, f"dragitem{dragitem_file}", f"r{row}c{col}.png")
    return os.path.exists(path)


def compute_exclusivity(items, class_profiles):
    """Pre-compute per-icon exclusivity scores for each class group.

    For each icon+slot, count how many of the 9 class groups can use it.
    Exclusivity = 1.0 / num_groups (1.0 = only this group, 0.11 = all 9).
    Returns dict: (icon, slot_name) -> {class_name: exclusivity}.
    """
    # Build: (icon, slot_name) -> set of class_names that have items there
    icon_slot_classes = defaultdict(set)
    for class_name, profile in class_profiles.items():
        mask = class_bitmask(profile['eq_classes'])
        for item in items:
            if int(item['itemclass']) != 0:
                continue
            if not (int(item['classes']) & mask):
                continue
            icon = int(item['icon'])
            slot_val = int(item['slots'])
            for bit, sname in SLOT_BITS.items():
                if slot_val & bit:
                    icon_slot_classes[(icon, sname)].add(class_name)

    result = {}
    for key, groups in icon_slot_classes.items():
        n = len(groups)
        for g in groups:
            result[(*key, g)] = 1.0 / n
    return result


def html_escape(text):
    """Minimal HTML escaping."""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def write_html(results):
    """Generate an HTML visual grid of icon picks with PNG thumbnails."""
    class_order = [
        # Plate melee
        'Warrior', 'Rogue', 'Monk',
        # Plate hybrids
        'Paladin', 'Shadowknight', 'Bard',
        # Chain hybrids
        'Ranger', 'Shaman', 'Beastlord',
        # Priests
        'Cleric', 'Druid',
        # Int casters
        'Necromancer', 'Wizard', 'Magician', 'Enchanter',
    ]

    colors = {
        'Warrior':      '#a83232', 'Rogue':     '#8b7355', 'Monk':      '#8b6914',
        'Paladin':      '#c0c0c0', 'Shadowknight': '#4a3050', 'Bard': '#c4962e',
        'Ranger':       '#4a7c3f', 'Shaman':    '#d4a040', 'Beastlord': '#7a5230',
        'Cleric':       '#3a8fb7', 'Druid':     '#2e8b57',
        'Necromancer':  '#6b3a6b', 'Wizard':    '#5050aa', 'Magician': '#b04040',
        'Enchanter':    '#7b3fa0',
    }

    lines = []
    a = lines.append

    a('<!DOCTYPE html>')
    a('<html lang="en"><head>')
    a('<meta charset="UTF-8">')
    a('<title>Thorne UI -- Class Icon Picks</title>')
    a('<style>')
    a('body { background: #1a1a2e; color: #c8c8d0; font-family: "Segoe UI", Arial, sans-serif; margin: 20px; }')
    a('h1 { color: #d4af37; text-align: center; font-size: 1.8em; }')
    a('h2 { color: #d4af37; border-bottom: 1px solid #333; padding-bottom: 4px; margin-top: 30px; }')
    a('.subtitle { text-align: center; color: #888; font-style: italic; margin-bottom: 20px; }')
    a('.class-section { margin-bottom: 40px; }')
    a('.slot-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; }')
    a('.slot-card { background: #16213e; border: 1px solid #333; border-radius: 6px; padding: 10px; }')
    a('.slot-name { font-weight: bold; color: #e0c872; font-size: 0.95em; text-transform: uppercase; margin-bottom: 6px; }')
    a('.pick { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; padding: 4px; border-radius: 3px; }')
    a('.pick.rank1 { background: rgba(212,175,55,0.12); border: 1px solid #d4af3744; }')
    a('.pick.rank2 { background: rgba(255,255,255,0.03); }')
    a('.pick img { width: 40px; height: 40px; image-rendering: pixelated; border: 1px solid #555; flex-shrink: 0; }')
    a('.pick img.missing { border: 1px dashed #666; opacity: 0.4; }')
    a('.pick-info { font-size: 0.8em; line-height: 1.3; }')
    a('.pick-meta { color: #999; font-size: 0.75em; }')
    a('.pick-stats { color: #8bc8a0; font-size: 0.75em; }')
    a('.pick-examples { color: #777; font-size: 0.7em; font-style: italic; }')
    a('.badge { display: inline-block; padding: 1px 5px; border-radius: 3px; font-size: 0.7em; font-weight: bold; margin-left: 4px; }')
    a('.badge-excl { background: #2e5b3e; color: #8fc; }')
    a('.badge-pop { background: #3a3a5a; color: #aac; }')
    a('.badge-warn { background: #4a2020; color: #e88; }')
    a('.divergence { background: #16213e; border: 1px solid #333; border-radius: 6px; padding: 15px; margin: 20px 0; }')
    a('.div-row { display: flex; align-items: center; gap: 6px; margin: 4px 0; flex-wrap: wrap; }')
    a('.div-slot { font-weight: bold; color: #e0c872; width: 90px; flex-shrink: 0; }')
    a('.div-icon { display: flex; align-items: center; gap: 3px; margin: 2px 4px; }')
    a('.div-icon img { width: 28px; height: 28px; image-rendering: pixelated; border: 1px solid #444; }')
    a('.div-label { font-size: 0.7em; }')
    a('.count-badge { font-size: 0.75em; color: #d4af37; font-weight: bold; }')
    a('</style>')
    a('</head><body>')
    a('<h1>Thorne UI -- Class Icon Picks</h1>')
    a('<p class="subtitle">Auto-selected by stat affinity, item count, and class exclusivity</p>')

    # -- DIVERGENCE OVERVIEW --
    a('<div class="divergence">')
    a('<h2 style="margin-top:0">Class Divergence Overview</h2>')
    a('<p style="color:#888; font-size:0.85em">Where top icon picks differ across classes. More icons = better differentiation.</p>')

    for slot_name in SLOT_ORDER:
        picks_by_class = {}
        for cn in class_order:
            picks = results.get(cn, {}).get('slots', {}).get(slot_name, [])
            if picks:
                picks_by_class[cn] = picks[0]

        if not picks_by_class:
            continue

        unique_icons = set(p['icon'] for p in picks_by_class.values())
        a('<div class="div-row">')
        a(f'  <span class="div-slot">{slot_name}</span>')
        a(f'  <span class="count-badge">{len(unique_icons)} icon{"s" if len(unique_icons) > 1 else ""}</span>')

        for cn in class_order:
            if cn not in picks_by_class:
                continue
            p = picks_by_class[cn]
            img = icon_png_path(p['icon'])
            short = cn[:3]
            col = colors.get(cn, '#aaa')
            a(f'  <span class="div-icon">')
            a(f'    <img src="{img}" alt="icon {p["icon"]}" title="{cn}: icon {p["icon"]}">')
            a(f'    <span class="div-label" style="color:{col}">{short}</span>')
            a(f'  </span>')
        a('</div>')

    a('</div>')

    # -- PER-CLASS SECTIONS --
    for class_name in class_order:
        if class_name not in results:
            continue

        r = results[class_name]
        col = colors.get(class_name, '#d4af37')

        a(f'<div class="class-section">')
        a(f'<h2 style="color:{col}">{html_escape(class_name)} '
          f'<span style="font-size:0.6em;color:#888">({html_escape(r["description"])})</span></h2>')
        a('<div class="slot-grid">')

        for slot_name in SLOT_ORDER:
            picks = r['slots'].get(slot_name, [])
            if not picks:
                continue

            a('<div class="slot-card">')
            a(f'<div class="slot-name">{html_escape(slot_name)}</div>')

            for rank, p in enumerate(picks[:3], 1):
                rank_cls = 'rank1' if rank == 1 else 'rank2'
                img = icon_png_path(p['icon'])
                has_img = icon_png_exists(p['icon'])
                img_cls = ' class="missing"' if not has_img else ''

                badges = ''
                if p['item_count'] >= 5:
                    badges += f' <span class="badge badge-pop">{p["item_count"]} items</span>'
                elif p['item_count'] < 2:
                    badges += ' <span class="badge badge-warn">1 item</span>'
                else:
                    badges += f' <span class="badge badge-pop">{p["item_count"]} items</span>'

                examples = html_escape(', '.join(p['example_names'][:2]))
                top_stats = html_escape(p['top_stats'])
                # 1-based for display
                dr = p['dragitem_row']
                dc = p['dragitem_col']

                a(f'<div class="pick {rank_cls}">')
                a(f'  <img src="{img}"{img_cls} alt="icon {p["icon"]}"'
                  f' title="icon {p["icon"]} - dragitem{p["dragitem_file"]} r{dr}c{dc}">')
                a(f'  <div class="pick-info">')
                a(f'    <div>#{rank} icon {p["icon"]}'
                  f' <span class="pick-meta">di{p["dragitem_file"]} r{dr}c{dc}'
                  f' score={p["total_score"]}</span>{badges}</div>')
                a(f'    <div class="pick-stats">{top_stats}</div>')
                a(f'    <div class="pick-examples">{examples}</div>')
                a(f'  </div>')
                a('</div>')

            a('</div>')

        a('</div>')
        a('</div>')

    a('</body></html>')

    with open(HTML_OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    # Load items
    items = []
    with open(CSV_IN, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            items.append(row)

    print(f"Loaded {len(items)} items from eq_items.csv")
    print(f"Classes to process: {len(CLASS_PROFILES)}")

    # Pre-compute exclusivity
    print("Computing icon exclusivity...")
    excl_map = compute_exclusivity(items, CLASS_PROFILES)
    print()

    # Results structure
    results = {}      # class_name -> slot -> [ranked icon picks]
    csv_rows = []     # flat rows for CSV

    for class_name, profile in sorted(CLASS_PROFILES.items()):
        eq_classes = profile['eq_classes']
        weights = profile['weights']
        class_mask = class_bitmask(eq_classes)

        print(f"  {class_name} ({'/'.join(sorted(eq_classes))})")

        results[class_name] = {
            'description': profile['description'],
            'eq_classes': sorted(eq_classes),
            'weights': weights,
            'slots': {},
        }

        for slot_name in SLOT_ORDER:
            # Find the slot bitmask
            slot_bit = next((bit for bit, name in SLOT_BITS.items() if name == slot_name), None)
            if slot_bit is None:
                continue

            # Filter: items usable by this class at this slot
            slot_items = [
                i for i in items
                if int(i['slots']) & slot_bit
                and int(i['classes']) & class_mask
                and int(i['itemclass']) == 0  # Common items only (not containers/books)
                and int(i['hp']) <= MAX_HP     # Exclude GM items (Ban Hammer etc.)
                and int(i['mana']) <= MAX_MANA
                and int(i['ac']) <= MAX_AC
            ]

            if not slot_items:
                continue

            # For armor slots, try class-restricted items first
            use_restricted = False
            if slot_name in ARMOR_SLOTS:
                restricted = [i for i in slot_items
                              if bin(int(i['classes'])).count('1') <= MAX_CLASSES_FOR_RESTRICTED]
                # Check if restricted pool has enough variety (2+ icons with 2+ items)
                if restricted:
                    icon_counts = Counter(int(i['icon']) for i in restricted)
                    multi_item_icons = sum(1 for c in icon_counts.values() if c >= 2)
                    if multi_item_icons >= 2:
                        slot_items = restricted
                        use_restricted = True

            # Group by icon
            by_icon = defaultdict(list)
            for item in slot_items:
                by_icon[int(item['icon'])].append(item)

            # Score each icon
            scored = []
            for icon, icon_items in by_icon.items():
                excl = excl_map.get((icon, slot_name, class_name), 0.11)
                stat_score, item_count, total_score = score_icon_group(
                    icon_items, weights, exclusivity=excl,
                    target_class_bit=class_mask)

                adjusted = icon - 500
                dragitem_file = adjusted // 36 + 1
                cell = adjusted % 36
                dragitem_row = cell % 6 + 1   # 1-based, col-major
                dragitem_col = cell // 6 + 1  # 1-based, col-major

                # Get top stat contributions for explanation
                stat_avgs = {}
                statted = [i for i in icon_items if any(int(i.get(s, 0)) > 0 for s in ALL_STATS)]
                for stat in ALL_STATS:
                    vals = [int(i.get(stat, 0)) for i in statted if int(i.get(stat, 0)) > 0]
                    if vals:
                        stat_avgs[stat] = sum(vals) / len(vals)

                # Top 3 contributing stats
                top_stats = sorted(
                    ((s, v) for s, v in stat_avgs.items()),
                    key=lambda x: -x[1] * weights.get(x[0], 0)
                )[:3]
                top_stats_str = ', '.join(f"{s}={v:.0f}" for s, v in top_stats)

                example_names = [i['Name'] for i in icon_items[:3]]

                # Penalise icons where ALL items are multi-slot and also
                # equippable in a weapon/shield slot. A shield icon picked
                # for 'back' confuses players — they expect a cloak.
                if slot_name in ARMOR_SLOTS:
                    all_also_weapon = all(
                        int(i['slots']) & WEAPON_SLOT_MASK
                        for i in icon_items
                    )
                    if all_also_weapon:
                        total_score *= 0.3   # heavy penalty

                scored.append({
                    'icon': icon,
                    'stat_score': round(stat_score, 1),
                    'item_count': item_count,
                    'total_score': round(total_score, 1),
                    'dragitem_file': dragitem_file,
                    'dragitem_row': dragitem_row,
                    'dragitem_col': dragitem_col,
                    'top_stats': top_stats_str,
                    'example_names': example_names,
                })

            # Sort: prefer icons with 2+ items first, then by total_score
            representative = [s for s in scored if s['item_count'] >= 2]
            one_offs = [s for s in scored if s['item_count'] < 2]
            representative.sort(key=lambda x: -x['total_score'])
            one_offs.sort(key=lambda x: -x['total_score'])
            # If no representative icons, fall back to one-offs
            ranked = (representative + one_offs) if representative else one_offs

            results[class_name]['slots'][slot_name] = ranked[:10]  # top 10

            # CSV rows — top 5 per class+slot
            for rank, pick in enumerate(ranked[:5], 1):
                csv_rows.append({
                    'class': class_name,
                    'slot': slot_name,
                    'rank': rank,
                    'icon': pick['icon'],
                    'dragitem': f"dragitem{pick['dragitem_file']}",
                    'row': pick['dragitem_row'],
                    'col': pick['dragitem_col'],
                    'total_score': pick['total_score'],
                    'stat_score': pick['stat_score'],
                    'item_count': pick['item_count'],
                    'top_stats': pick['top_stats'],
                    'examples': ' | '.join(pick['example_names']),
                })

        # Print top pick per slot
        for slot_name in SLOT_ORDER:
            picks = results[class_name]['slots'].get(slot_name, [])
            if picks:
                p = picks[0]
                di = f"dragitem{p['dragitem_file']} r{p['dragitem_row']}c{p['dragitem_col']}"
                runner = ""
                if len(picks) > 1:
                    r = picks[1]
                    runner = f"  (runner-up: icon {r['icon']}, score {r['total_score']})"
                print(f"    {slot_name:12s}: icon {p['icon']:4d} ({di}) "
                      f"score={p['total_score']:6.1f} ({p['item_count']:3d} items) "
                      f"[{p['top_stats']}]{runner}")

        print()

    # ============================================================
    # WRITE JSON
    # ============================================================
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=1)

    # ============================================================
    # WRITE CSV
    # ============================================================
    csv_fields = [
        'class', 'slot', 'rank', 'icon', 'dragitem', 'row', 'col',
        'total_score', 'stat_score', 'item_count', 'top_stats', 'examples',
    ]
    with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(csv_rows)

    json_size = os.path.getsize(JSON_OUT)
    csv_size = os.path.getsize(CSV_OUT)
    print(f"Wrote {JSON_OUT} ({json_size / 1000:.0f} KB)")
    print(f"Wrote {CSV_OUT} ({csv_size / 1000:.0f} KB)")

    # ============================================================
    # WRITE HTML
    # ============================================================
    write_html(results)
    html_size = os.path.getsize(HTML_OUT)
    print(f"Wrote {HTML_OUT} ({html_size / 1000:.0f} KB)")

    # ============================================================
    # COMPARISON: Show where classes diverge
    # ============================================================
    print("\n" + "=" * 80)
    print("CLASS DIVERGENCE — Where top picks differ")
    print("=" * 80)

    for slot_name in SLOT_ORDER:
        picks_by_class = {}
        for class_name in sorted(CLASS_PROFILES.keys()):
            picks = results[class_name]['slots'].get(slot_name, [])
            if picks:
                picks_by_class[class_name] = picks[0]['icon']

        if not picks_by_class:
            continue

        unique_icons = set(picks_by_class.values())
        if len(unique_icons) > 1:
            detail = ', '.join(f"{c}={i}" for c, i in sorted(picks_by_class.items()))
            print(f"  {slot_name:12s}: {len(unique_icons)} different icons -- {detail}")
        else:
            icon = list(unique_icons)[0]
            print(f"  {slot_name:12s}: ALL agree on icon {icon}")


if __name__ == '__main__':
    main()
