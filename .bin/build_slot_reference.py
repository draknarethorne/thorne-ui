#!/usr/bin/env python3
"""Build a class-to-icon reference for equipment slot art selection.

Reads eq_items.csv (produced by extract_eq_items.py) and generates a
reference mapping of which dragitem icons are used by which EQ class
archetypes at each equipment slot.

Output: .master/items/.cache/slot_icon_reference.json
        .master/items/.cache/slot_icon_reference.csv

Usage:
    python .bin/build_slot_reference.py
"""
import csv
import json
import os
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CACHE_DIR = os.path.join(PROJECT_ROOT, '.master', 'items', '.cache')

CSV_IN = os.path.join(CACHE_DIR, 'eq_items.csv')
JSON_OUT = os.path.join(CACHE_DIR, 'slot_icon_reference.json')
CSV_OUT = os.path.join(CACHE_DIR, 'slot_icon_reference.csv')

if not os.path.exists(CSV_IN):
    print("ERROR: eq_items.csv not found. Run extract_eq_items.py first.")
    sys.exit(1)

# ============================================================
# EQ REFERENCE DATA
# ============================================================

CLASS_BITS = {
    1: 'WAR', 2: 'CLR', 4: 'PAL', 8: 'RNG', 16: 'SHD',
    32: 'DRU', 64: 'MNK', 128: 'BRD', 256: 'ROG', 512: 'SHM',
    1024: 'NEC', 2048: 'WIZ', 4096: 'MAG', 8192: 'ENC',
    16384: 'BST', 32768: 'BER',
}

# Thorne UI class archetypes — which EQ classes map to each
# Broad archetypes (active in classes/)
ARCHETYPES = {
    'Caster':  {'NEC', 'WIZ', 'MAG', 'ENC'},
    'Hybrid':  {'PAL', 'RNG', 'SHD', 'BRD', 'BST'},
    'Melee':   {'WAR', 'MNK', 'ROG', 'BER'},
    'Priest':  {'CLR', 'DRU', 'SHM'},
    # Individual class configs (staged in research/)
    'Bard':    {'BRD'},
    'Druid':   {'DRU'},
    'Monk':    {'MNK'},
    'Necro':   {'NEC'},
    'Ranger':  {'RNG'},
}

# Equipment slot bit → name mapping
SLOT_BITS = {
    2: 'ear', 4: 'head', 8: 'face', 32: 'neck',
    64: 'shoulder', 128: 'arms', 256: 'back',
    512: 'wrist',    # L.Wrist — wrists are paired
    4096: 'hands', 8192: 'primary', 16384: 'secondary',
    32768: 'fingers',  # L.Ring — rings are paired
    131072: 'chest', 262144: 'legs', 524288: 'feet',
    1048576: 'waist', 2048: 'range', 2097152: 'ammo',
}

# Canonical slot order matching UI layout
SLOT_ORDER = [
    'ear', 'head', 'face', 'neck',
    'shoulder', 'arms', 'back', 'wrist',
    'hands', 'fingers', 'chest', 'legs', 'feet', 'waist',
    'primary', 'secondary', 'range', 'ammo',
]

ITEMTYPE_NAMES = {
    0: '1H-Slash', 1: '2H-Slash', 2: 'Piercing', 3: '1H-Blunt',
    4: '2H-Blunt', 5: 'Archery', 7: 'Throwing', 8: 'Shield',
    10: 'Armor', 11: 'Tradeskill', 14: 'Food', 15: 'Drink',
    16: 'Light', 17: 'Combinable', 20: 'Alcohol', 21: 'Poison',
    23: 'Wind-Inst', 24: 'String-Inst', 25: 'Brass-Inst',
    26: 'Percussion', 27: 'Arrow', 35: '2H-Pierce', 45: 'H2H',
}


def decode_class_set(bitmask):
    """Convert class bitmask to a set of class abbreviations."""
    classes = set()
    for bit, name in CLASS_BITS.items():
        if bitmask & bit:
            classes.add(name)
    return classes


def archetype_for_classes(class_set):
    """Determine which Thorne archetypes a class bitmask matches."""
    matches = []
    for arch_name, arch_classes in ARCHETYPES.items():
        if class_set & arch_classes:
            matches.append(arch_name)
    return matches


def main():
    # Load items
    items = []
    with open(CSV_IN, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)

    print(f"Loaded {len(items)} items from eq_items.csv")

    # Filter to equippable items (slots > 0, itemclass=0 Common)
    equippable = [
        i for i in items
        if int(i['slots']) > 0 and int(i['itemclass']) == 0
    ]
    print(f"Equippable items: {len(equippable)}")

    # ============================================================
    # BUILD: slot → icon → class data
    # ============================================================
    # For each slot, collect icons and which classes use them
    # Structure: slot_data[slot_name][icon_id] = {
    #   'classes': set of class abbreviations,
    #   'archetypes': set of archetype names,
    #   'item_count': int,
    #   'itemtypes': set of itemtype values,
    #   'example_names': list of item names,
    #   'dragitem_file': int,
    #   'dragitem_row': int,
    #   'dragitem_col': int,
    # }
    slot_data = defaultdict(lambda: defaultdict(lambda: {
        'classes': set(),
        'archetypes': set(),
        'itemtypes': set(),
        'example_names': [],
        'item_count': 0,
        'dragitem_file': 0,
        'dragitem_row': 0,
        'dragitem_col': 0,
    }))

    for item in equippable:
        slots_bitmask = int(item['slots'])
        classes_bitmask = int(item['classes'])
        icon = int(item['icon'])
        class_set = decode_class_set(classes_bitmask)
        archetypes = archetype_for_classes(class_set)
        itemtype = int(item['itemtype'])

        for slot_bit, slot_name in SLOT_BITS.items():
            if slots_bitmask & slot_bit:
                entry = slot_data[slot_name][icon]
                entry['classes'].update(class_set)
                entry['archetypes'].update(archetypes)
                entry['itemtypes'].add(itemtype)
                entry['item_count'] += 1
                entry['dragitem_file'] = int(item['dragitem_file'])
                entry['dragitem_row'] = int(item['dragitem_row'])
                entry['dragitem_col'] = int(item['dragitem_col'])
                if len(entry['example_names']) < 5:
                    entry['example_names'].append(item['Name'])

    # ============================================================
    # BUILD: archetype → slot → ranked icons
    # ============================================================
    # For each archetype+slot, rank icons by how many items use them
    # (more items = more representative of that class/slot combo)
    arch_slot_icons = defaultdict(lambda: defaultdict(list))

    for slot_name in SLOT_ORDER:
        if slot_name not in slot_data:
            continue
        for icon, data in slot_data[slot_name].items():
            for arch in data['archetypes']:
                arch_slot_icons[arch][slot_name].append({
                    'icon': icon,
                    'item_count': data['item_count'],
                    'dragitem_file': data['dragitem_file'],
                    'dragitem_row': data['dragitem_row'],
                    'dragitem_col': data['dragitem_col'],
                    'itemtypes': sorted(data['itemtypes']),
                    'example_names': data['example_names'][:3],
                })

    # Sort each list by item_count descending
    for arch in arch_slot_icons:
        for slot_name in arch_slot_icons[arch]:
            arch_slot_icons[arch][slot_name].sort(
                key=lambda x: -x['item_count']
            )

    # ============================================================
    # FIND ARCHETYPE-EXCLUSIVE ICONS
    # ============================================================
    # Icons that are ONLY usable by one archetype at a given slot
    # (these are the best candidates for class-specific slot art)
    exclusive_icons = defaultdict(lambda: defaultdict(list))

    for slot_name in SLOT_ORDER:
        if slot_name not in slot_data:
            continue
        for icon, data in slot_data[slot_name].items():
            archs = data['archetypes']
            if len(archs) == 1:
                arch = list(archs)[0]
                exclusive_icons[arch][slot_name].append({
                    'icon': icon,
                    'item_count': data['item_count'],
                    'dragitem_file': data['dragitem_file'],
                    'dragitem_row': data['dragitem_row'],
                    'dragitem_col': data['dragitem_col'],
                    'classes': sorted(data['classes']),
                    'itemtypes': sorted(data['itemtypes']),
                    'example_names': data['example_names'][:3],
                })

    for arch in exclusive_icons:
        for slot_name in exclusive_icons[arch]:
            exclusive_icons[arch][slot_name].sort(
                key=lambda x: -x['item_count']
            )

    # ============================================================
    # WRITE JSON
    # ============================================================
    output = {
        '_meta': {
            'description': 'Icon reference for Thorne UI class-specific slot art',
            'source': 'eq_items.csv (Quarm database)',
            'total_equippable': len(equippable),
            'archetypes': {k: sorted(v) for k, v in ARCHETYPES.items()},
            'slot_order': SLOT_ORDER,
        },
        'by_archetype': {},
        'exclusive_by_archetype': {},
        'by_slot': {},
    }

    # by_archetype: arch → slot → top icons
    for arch in sorted(ARCHETYPES.keys()):
        output['by_archetype'][arch] = {}
        for slot_name in SLOT_ORDER:
            icons = arch_slot_icons.get(arch, {}).get(slot_name, [])
            output['by_archetype'][arch][slot_name] = icons[:10]  # top 10

    # exclusive_by_archetype: arch → slot → exclusive icons
    for arch in sorted(ARCHETYPES.keys()):
        output['exclusive_by_archetype'][arch] = {}
        for slot_name in SLOT_ORDER:
            icons = exclusive_icons.get(arch, {}).get(slot_name, [])
            output['exclusive_by_archetype'][arch][slot_name] = icons[:10]

    # by_slot: slot → all icons grouped by archetype coverage
    for slot_name in SLOT_ORDER:
        if slot_name not in slot_data:
            output['by_slot'][slot_name] = {}
            continue

        slot_icons = []
        for icon, data in slot_data[slot_name].items():
            slot_icons.append({
                'icon': icon,
                'item_count': data['item_count'],
                'dragitem_file': data['dragitem_file'],
                'dragitem_row': data['dragitem_row'],
                'dragitem_col': data['dragitem_col'],
                'classes': sorted(data['classes']),
                'archetypes': sorted(data['archetypes']),
                'itemtypes': sorted(data['itemtypes']),
                'example_names': data['example_names'][:3],
            })
        slot_icons.sort(key=lambda x: -x['item_count'])
        output['by_slot'][slot_name] = slot_icons

    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=1)

    # ============================================================
    # WRITE FLAT CSV SUMMARY
    # ============================================================
    csv_rows = []
    for slot_name in SLOT_ORDER:
        if slot_name not in slot_data:
            continue
        for icon, data in sorted(slot_data[slot_name].items(), key=lambda x: -x[1]['item_count']):
            csv_rows.append({
                'slot': slot_name,
                'icon': icon,
                'dragitem': f"dragitem{data['dragitem_file']}",
                'row': data['dragitem_row'],
                'col': data['dragitem_col'],
                'item_count': data['item_count'],
                'archetypes': '/'.join(sorted(data['archetypes'])),
                'classes': '/'.join(sorted(data['classes'])),
                'itemtypes': '/'.join(str(t) for t in sorted(data['itemtypes'])),
                'examples': ' | '.join(data['example_names'][:3]),
            })

    with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'slot', 'icon', 'dragitem', 'row', 'col', 'item_count',
            'archetypes', 'classes', 'itemtypes', 'examples',
        ])
        writer.writeheader()
        writer.writerows(csv_rows)

    json_size = os.path.getsize(JSON_OUT)
    csv_size = os.path.getsize(CSV_OUT)
    print(f"\nWrote {JSON_OUT} ({json_size / 1000:.0f} KB)")
    print(f"Wrote {CSV_OUT} ({csv_size / 1000:.0f} KB)")

    # ============================================================
    # PRINT ANALYSIS
    # ============================================================
    print("\n" + "=" * 80)
    print("ARCHETYPE ICON SUMMARY")
    print("=" * 80)

    for arch in sorted(ARCHETYPES.keys()):
        print(f"\n  -- {arch.upper()} ({'/'.join(sorted(ARCHETYPES[arch]))}) --")
        for slot_name in SLOT_ORDER:
            icons = arch_slot_icons.get(arch, {}).get(slot_name, [])
            excl = exclusive_icons.get(arch, {}).get(slot_name, [])
            if not icons:
                continue

            top = icons[0]
            di = f"dragitem{top['dragitem_file']} r{top['dragitem_row']}c{top['dragitem_col']}"
            names = ', '.join(top['example_names'][:2])
            excl_count = len(excl)
            total_icons = len(icons)

            print(f"    {slot_name:12s}: {total_icons:3d} icons ({excl_count:2d} exclusive) "
                  f"| top: icon {top['icon']:4d} ({di}) {top['item_count']:3d} items — {names}")

    # Show the exclusive icons per archetype — these are the best for class art
    print("\n" + "=" * 80)
    print("BEST EXCLUSIVE ICONS (unique to one archetype)")
    print("=" * 80)

    for arch in sorted(ARCHETYPES.keys()):
        print(f"\n  -- {arch.upper()} --")
        for slot_name in SLOT_ORDER:
            excl = exclusive_icons.get(arch, {}).get(slot_name, [])
            if not excl:
                continue
            top3 = excl[:3]
            descs = []
            for e in top3:
                di = f"di{e['dragitem_file']} r{e['dragitem_row']}c{e['dragitem_col']}"
                descs.append(f"icon {e['icon']:4d} ({di}, {e['item_count']} items)")
            print(f"    {slot_name:12s}: {' | '.join(descs)}")


if __name__ == '__main__':
    main()
