#!/usr/bin/env python3
"""Extract EverQuest item data from the Quarm SQL dump into a clean CSV.

Parses INSERT INTO `items` VALUES(...) statements and outputs a CSV with
all columns relevant to class-specific slot art mapping.

Source: SecretsOTheP/EQMacEmu Quarm database dump
Output: .cache/eq_items.csv  (+ .cache/eq_items.json for programmatic use)

Usage:
    python .bin/extract_eq_items.py
"""
import csv
import glob
import json
import os
import sys
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TMP_DIR = os.path.join(PROJECT_ROOT, '.tmp')
CACHE_DIR = os.path.join(PROJECT_ROOT, '.cache')

# Find the main SQL file (colon in filename gets mangled on Windows)
sql_files = glob.glob(os.path.join(TMP_DIR, 'quarm_*.sql'))
SQL_FILE = next((f for f in sql_files if os.path.getsize(f) > 10_000_000), None)
if not SQL_FILE:
    print("ERROR: Could not find the main quarm SQL file in .tmp/")
    print("  Download from: SecretsOTheP/EQMacEmu → utils/sql/database_full/")
    sys.exit(1)

os.makedirs(CACHE_DIR, exist_ok=True)

CSV_OUT = os.path.join(CACHE_DIR, 'eq_items.csv')
JSON_OUT = os.path.join(CACHE_DIR, 'eq_items.json')

# ============================================================
# COLUMN INDICES (0-based from CREATE TABLE `items`)
# ============================================================
# These map to the position of each column in the INSERT VALUES tuples.
COLUMNS = {
    'id':         0,
    'Name':       2,
    'aagi':       3,
    'ac':         4,
    'acha':       5,
    'adex':       6,
    'aint':       7,
    'asta':       8,
    'astr':       9,
    'awis':      10,
    'bagsize':   11,
    'bagslots':  12,
    'bagtype':   13,
    'classes':   23,
    'cr':        26,
    'damage':    27,
    'delay':     29,
    'dr':        30,
    'fr':        45,
    'hp':        48,
    'icon':      49,
    'idfile':    50,
    'itemclass': 51,
    'itemtype':  52,
    'light':     53,
    'lore':      54,
    'magic':     55,
    'mana':      56,
    'material':  57,
    'mr':        59,
    'nodrop':    60,
    'pr':        62,
    'races':     64,
    'reclevel':  66,
    'reqlevel':  68,
    'size':      70,
    'slots':     73,
    'weight':    76,
}

# Max column index we need to read
MAX_COL = max(COLUMNS.values())

# ============================================================
# EQ REFERENCE DATA
# ============================================================

CLASS_BITS = {
    1: 'WAR', 2: 'CLR', 4: 'PAL', 8: 'RNG', 16: 'SHD',
    32: 'DRU', 64: 'MNK', 128: 'BRD', 256: 'ROG', 512: 'SHM',
    1024: 'NEC', 2048: 'WIZ', 4096: 'MAG', 8192: 'ENC',
    16384: 'BST', 32768: 'BER',
}
ALL_CLASSES = sum(CLASS_BITS.keys())  # 65535

SLOT_BITS = {
    1: 'Charm', 2: 'L.Ear', 4: 'Head', 8: 'Face', 16: 'R.Ear',
    32: 'Neck', 64: 'Shoulder', 128: 'Arms', 256: 'Back',
    512: 'L.Wrist', 1024: 'R.Wrist', 2048: 'Range', 4096: 'Hands',
    8192: 'Primary', 16384: 'Secondary', 32768: 'L.Ring', 65536: 'R.Ring',
    131072: 'Chest', 262144: 'Legs', 524288: 'Feet',
    1048576: 'Waist', 2097152: 'Ammo',
}

ITEMTYPE_NAMES = {
    0: '1H-Slash', 1: '2H-Slash', 2: 'Piercing', 3: '1H-Blunt',
    4: '2H-Blunt', 5: 'Archery', 7: 'Throwing', 8: 'Shield',
    10: 'Armor', 11: 'Tradeskill', 12: 'Lockpick', 14: 'Food',
    15: 'Drink', 16: 'Light', 17: 'Combinable', 18: 'Stackable',
    19: 'Scroll', 20: 'Alcohol', 21: 'Poison', 23: 'Wind-Inst',
    24: 'String-Inst', 25: 'Brass-Inst', 26: 'Percussion', 27: 'Arrow',
    28: 'Jewelry', 29: 'Skull', 30: 'Tome', 31: 'Note', 32: 'Key',
    33: 'Coin', 34: 'Aug-2H', 35: '2H-Pierce', 36: 'Fish-Pole',
    37: 'Fish-Bait', 38: 'Alcohol2', 39: 'Misc-Ammo', 40: 'Potion',
    42: 'Aug', 45: 'H2H', 52: 'Charm',
}

ITEMCLASS_NAMES = {0: 'Common', 1: 'Container', 2: 'Book'}


def decode_classes(bitmask):
    """Convert class bitmask to a readable string."""
    if bitmask <= 0:
        return 'NONE'
    if bitmask >= ALL_CLASSES:
        return 'ALL'
    return '/'.join(name for bit, name in sorted(CLASS_BITS.items()) if bitmask & bit)


def decode_slots(bitmask):
    """Convert slot bitmask to a readable string."""
    if bitmask <= 0:
        return 'NONE'
    return '/'.join(name for bit, name in sorted(SLOT_BITS.items()) if bitmask & bit)


# ============================================================
# SQL PARSER
# ============================================================

def parse_row(row_str):
    """Parse a single VALUES tuple into a list of field strings."""
    fields = []
    field = []
    in_q = False
    esc = False
    for c in row_str:
        if esc:
            field.append(c)
            esc = False
        elif c == '\\':
            esc = True
        elif c == "'" and not in_q:
            in_q = True
        elif c == "'" and in_q:
            in_q = False
        elif c == ',' and not in_q:
            fields.append(''.join(field).strip())
            field = []
        else:
            field.append(c)
    fields.append(''.join(field).strip())
    return fields


def extract_tuples(buffer):
    """Extract complete (...) tuples from buffer.

    Returns (list_of_tuple_strings, remaining_buffer).
    """
    tuples = []
    while buffer:
        start = buffer.find('(')
        if start == -1:
            buffer = ""
            break

        i = start + 1
        depth = 1
        in_quote = False
        escaped = False
        while i < len(buffer) and depth > 0:
            c = buffer[i]
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == "'" and not in_quote:
                in_quote = True
            elif c == "'" and in_quote:
                in_quote = False
            elif not in_quote:
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
            i += 1

        if depth > 0:
            break  # incomplete tuple, need more data

        tuples.append(buffer[start + 1:i - 1])
        buffer = buffer[i:].lstrip(' ,;\n\r')

    return tuples, buffer


def extract_item(fields):
    """Extract an item dict from parsed fields, or None if invalid."""
    if len(fields) <= MAX_COL:
        return None

    try:
        item = {}
        for name, idx in COLUMNS.items():
            val = fields[idx]
            if name in ('Name', 'idfile', 'lore'):
                item[name] = val
            elif name == 'icon':
                icon = int(val)
                item['icon'] = icon
                # Derive dragitem file + cell position
                adjusted = icon - 500
                item['dragitem_file'] = adjusted // 36 + 1
                cell = adjusted % 36
                item['dragitem_row'] = cell % 6 + 1   # 1-based, col-major
                item['dragitem_col'] = cell // 6 + 1  # 1-based, col-major
            else:
                item[name] = int(val)

        # Add decoded human-readable fields
        item['classes_str'] = decode_classes(item.get('classes', 0))
        item['slots_str'] = decode_slots(item.get('slots', 0))
        item['itemtype_str'] = ITEMTYPE_NAMES.get(item.get('itemtype', -1), f"unk_{item.get('itemtype', -1)}")
        item['itemclass_str'] = ITEMCLASS_NAMES.get(item.get('itemclass', -1), f"unk_{item.get('itemclass', -1)}")

        return item
    except (ValueError, IndexError):
        return None


# ============================================================
# MAIN
# ============================================================

def main():
    print(f"Source: {SQL_FILE}")
    print(f"  Size: {os.path.getsize(SQL_FILE) / 1_000_000:.1f} MB")
    print(f"Output: {CSV_OUT}")
    print(f"        {JSON_OUT}")
    print()

    items = []
    in_items = False
    buffer = ""
    insert_count = 0

    with open(SQL_FILE, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith("INSERT INTO `items` VALUES"):
                in_items = True
                insert_count += 1
                buffer = line[len("INSERT INTO `items` VALUES"):].strip()
            elif in_items:
                if (line.startswith("INSERT INTO") or line.startswith("CREATE TABLE")
                        or line.startswith("LOCK TABLES") or line.startswith("UNLOCK TABLES")
                        or line.startswith("/*!") or line.startswith("--")):
                    # Process remaining buffer
                    if buffer:
                        tuples, _ = extract_tuples(buffer)
                        for t in tuples:
                            item = extract_item(parse_row(t))
                            if item:
                                items.append(item)
                    in_items = False
                    buffer = ""
                    continue
                buffer += line.strip()

            if not in_items or not buffer:
                continue

            tuples, buffer = extract_tuples(buffer)
            for t in tuples:
                item = extract_item(parse_row(t))
                if item:
                    items.append(item)

    # Flush remaining
    if buffer:
        tuples, _ = extract_tuples(buffer)
        for t in tuples:
            item = extract_item(parse_row(t))
            if item:
                items.append(item)

    print(f"Processed {insert_count} INSERT statements")
    print(f"Total items extracted: {len(items)}")

    if not items:
        print("ERROR: No items extracted!")
        sys.exit(1)

    # ============================================================
    # WRITE CSV
    # ============================================================
    csv_fields = [
        'id', 'Name', 'icon', 'dragitem_file', 'dragitem_row', 'dragitem_col',
        'itemclass', 'itemclass_str', 'itemtype', 'itemtype_str',
        'classes', 'classes_str', 'slots', 'slots_str',
        'races', 'material',
        'ac', 'hp', 'mana', 'damage', 'delay',
        'astr', 'asta', 'aagi', 'adex', 'aint', 'awis', 'acha',
        'cr', 'dr', 'fr', 'mr', 'pr',
        'magic', 'nodrop', 'size', 'light',
        'reclevel', 'reqlevel', 'weight',
        'bagslots', 'bagsize', 'bagtype',
        'idfile', 'lore',
    ]

    with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction='ignore')
        writer.writeheader()
        for item in sorted(items, key=lambda x: (x['icon'], x['id'])):
            writer.writerow(item)

    # ============================================================
    # WRITE JSON (organized by icon for programmatic access)
    # ============================================================
    by_icon = {}
    for item in items:
        icon = item['icon']
        if icon not in by_icon:
            by_icon[icon] = []
        by_icon[icon].append(item)

    # Sort by icon key for readability
    by_icon_sorted = {k: by_icon[k] for k in sorted(by_icon.keys())}

    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump({
            '_meta': {
                'source': 'SecretsOTheP/EQMacEmu Quarm database dump',
                'extracted_by': 'extract_eq_items.py',
                'total_items': len(items),
                'unique_icons': len(by_icon),
                'icon_range': [min(by_icon.keys()), max(by_icon.keys())],
                'columns': list(COLUMNS.keys()),
            },
            '_class_bits': CLASS_BITS,
            '_slot_bits': SLOT_BITS,
            '_itemtype_names': {str(k): v for k, v in ITEMTYPE_NAMES.items()},
            'items_by_icon': {str(k): v for k, v in by_icon_sorted.items()},
        }, f, indent=1)

    csv_size = os.path.getsize(CSV_OUT)
    json_size = os.path.getsize(JSON_OUT)
    print(f"\nWrote {CSV_OUT} ({csv_size / 1_000_000:.1f} MB)")
    print(f"Wrote {JSON_OUT} ({json_size / 1_000_000:.1f} MB)")

    # ============================================================
    # SUMMARY STATS
    # ============================================================
    icons = set(item['icon'] for item in items)
    print(f"\nUnique icons: {len(icons)} (range {min(icons)}-{max(icons)})")

    # Coverage per dragitem
    print(f"\nDragitem coverage:")
    for file_num in range(1, 35):
        start = (file_num - 1) * 36
        end = file_num * 36
        covered = sum(1 for i in range(start, end) if i in by_icon)
        item_count = sum(len(by_icon.get(i, [])) for i in range(start, end))
        if covered > 0:
            print(f"  dragitem{file_num:2d}: {covered:2d}/36 icons → {item_count:4d} items")

    # Itemtype breakdown
    type_counts = Counter(item['itemtype'] for item in items)
    print(f"\nItem types:")
    for itype, count in type_counts.most_common(15):
        print(f"  {ITEMTYPE_NAMES.get(itype, f'unk_{itype}'):15s} (type {itype:2d}): {count:5d}")

    # Class distribution — how many items per class
    print(f"\nItems per class (equippable, slots > 0):")
    equippable = [item for item in items if item.get('slots', 0) > 0]
    for bit, name in sorted(CLASS_BITS.items()):
        count = sum(1 for item in equippable if item.get('classes', 0) & bit)
        print(f"  {name}: {count:5d}")

    # Armor items per slot
    armor_items = [item for item in items if item['itemtype'] == 10 and item.get('slots', 0) > 0]
    print(f"\nArmor items per equipment slot:")
    for bit, name in sorted(SLOT_BITS.items()):
        count = sum(1 for item in armor_items if item.get('slots', 0) & bit)
        if count > 0:
            print(f"  {name:12s}: {count:4d}")

    # Show example: Head slot armor by class
    print(f"\nExample — HEAD SLOT armor, grouped by class availability:")
    head_armor = [item for item in items if item['itemtype'] == 10 and item.get('slots', 0) & 4]
    head_by_classes = {}
    for item in head_armor:
        cls_str = item['classes_str']
        if cls_str not in head_by_classes:
            head_by_classes[cls_str] = set()
        head_by_classes[cls_str].add(item['icon'])

    for cls_str in sorted(head_by_classes, key=lambda x: -len(head_by_classes[x]))[:15]:
        icons_list = sorted(head_by_classes[cls_str])
        icon_str = ', '.join(str(i) for i in icons_list[:8])
        if len(icons_list) > 8:
            icon_str += f" (+{len(icons_list)-8} more)"
        print(f"  {cls_str:50s}: {len(icons_list):3d} icons — {icon_str}")


if __name__ == '__main__':
    main()
