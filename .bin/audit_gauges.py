#!/usr/bin/env python3
"""
Audit gauge alignment across all composite multi-color gauge files.

Reads EQUI_Animations.xml and all window XMLs to verify that:
  1. Animation X offsets match expected marker×100 values
  2. A-part GaugeOffsetX matches marker×100
  3. B-part GaugeOffsetX = -(marker-1) i.e. -clip
  4. Screen clip CX = clip (marker-1)
  5. No stale pre-snap offset values remain

Usage:
    python .bin/audit_gauges.py              # Report only
    python .bin/audit_gauges.py --verbose    # Show all matched values
    python .bin/audit_gauges.py --json       # Output JSON report to .tmp/

The canonical marker positions come from snap_columns config (exact fifths).
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ============================================================================
# CANONICAL DATA — Single source of truth (matches .regen_gauges.json snap)
# ============================================================================

# Snapped grid marker positions (exact fifths of each width)
GRID_MARKERS = {
    "105t": [21, 42, 63, 84],
    "120t": [24, 48, 72, 96],
    "250t": [50, 100, 150, 200],
}

# Old pre-snap marker positions (for stale value detection)
OLD_MARKERS = {
    "105t": [21, 42, 62, 82],
    "120t": [24, 48, 71, 94],
    "250t": [50, 100, 149, 197],
}

WIDTHS = {"105t": 105, "120t": 120, "250t": 250}


def get_clips(size):
    """Clips = marker - 1 (EQ off-by-one: GaugeOffsetX=-N renders from col N+1)."""
    return [m - 1 for m in GRID_MARKERS[size]]


def get_old_clips(size):
    return [m - 1 for m in OLD_MARKERS[size]]


# Files that contain composite gauges, grouped by size
GAUGE_FILES_BY_SIZE = {
    "105t": [
        "EQUI_SpellBookWnd.xml",
    ],
    "120t": [
        "EQUI_PlayerWindow.xml",
        "EQUI_GroupWindow.xml",
        "EQUI_BreathWindow.xml",
        "EQUI_PetInfoWindow.xml",
        # MusicPlayerWnd: test harness with mixed sizes, audited separately
    ],
    "250t": [
        "EQUI_TargetWindow.xml",
    ],
}

ROOT = Path(__file__).resolve().parent.parent / "thorne_drak"
ANIMS_FILE = ROOT / "EQUI_Animations.xml"


# ============================================================================
# SCANNING
# ============================================================================

def scan_animations(verbose=False):
    """Scan EQUI_Animations.xml for oversized animation offset correctness."""
    issues = []
    ok_count = 0

    with open(ANIMS_FILE, "r", encoding="utf-8-sig") as f:
        content = f.read()

    pattern = re.compile(
        r'<Ui2DAnimation item="(A_Oversized[^"]+)">\s*'
        r"<Cycle>true</Cycle>\s*<Frames>\s*"
        r"<Texture>([^<]+)</Texture>\s*"
        r"<Location>\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*</Location>\s*"
        r"<Size>\s*<CX>([^<]+)</CX>\s*<CY>([^<]+)</CY>"
    )

    for m in pattern.finditer(content):
        name, tex, x_str, y_str, cx_str, cy_str = m.groups()
        x_val = int(x_str)
        cx_val = int(cx_str)

        size_match = re.search(r"(\d+t)", name)
        band_match = re.search(r"Band(\d)", name)
        if not size_match or not band_match:
            continue

        size = size_match.group(1)
        band = int(band_match.group(1))
        if size not in WIDTHS:
            continue

        marker = GRID_MARKERS[size][band - 1]
        width = WIDTHS[size]
        expected_x = -(marker * 100)
        expected_cx = width * 100

        if x_val != expected_x:
            issues.append({
                "type": "anim_x",
                "name": name,
                "actual": x_val,
                "expected": expected_x,
                "band": band,
                "size": size,
            })
        else:
            ok_count += 1

        if cx_val != expected_cx:
            issues.append({
                "type": "anim_cx",
                "name": name,
                "actual": cx_val,
                "expected": expected_cx,
                "size": size,
            })

    return issues, ok_count


def scan_gauge_file(filepath, size, verbose=False):
    """Scan a window XML for gauge offset alignment issues."""
    issues = []
    ok_count = 0
    markers = GRID_MARKERS[size]
    clips = get_clips(size)
    old_markers = OLD_MARKERS[size]
    old_clips = get_old_clips(size)
    width = WIDTHS[size]

    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    rel_path = str(Path(filepath).relative_to(ROOT))

    # ── A-part offsets (×100 scale, negative values > 1000) ──
    a_pattern = re.compile(r"<GaugeOffsetX>(-\d{4,})</GaugeOffsetX>")
    for m in a_pattern.finditer(content):
        offset = int(m.group(1))
        # Check if matches any expected band (marker × 100)
        matched = False
        for i, marker in enumerate(markers):
            if offset == -(marker * 100):
                matched = True
                ok_count += 1
                break

        if not matched:
            # Check if it's a stale old value
            identified = False
            for i, om in enumerate(old_markers):
                if offset == -(om * 100) and om != markers[i]:
                    issues.append({
                        "type": "stale_a_offset",
                        "file": rel_path,
                        "size": size,
                        "band": i + 1,
                        "actual": offset,
                        "expected": -(markers[i] * 100),
                    })
                    identified = True
                    break
            if not identified and abs(offset) > 1000:
                issues.append({
                    "type": "unknown_a_offset",
                    "file": rel_path,
                    "size": size,
                    "actual": offset,
                    "band": "?",
                })

    # ── B-part offsets (pixel scale, small negative 5-300) ──
    b_pattern = re.compile(r"<GaugeOffsetX>(-\d{1,3})</GaugeOffsetX>")
    for m in b_pattern.finditer(content):
        offset = int(m.group(1))
        if abs(offset) < 5:
            continue

        matched = False
        for i, clip in enumerate(clips):
            if offset == -clip:
                matched = True
                ok_count += 1
                break

        if not matched:
            # Check against old clips (marker-1) and old markers
            for i, oc in enumerate(old_clips):
                if offset == -oc and oc != clips[i]:
                    issues.append({
                        "type": "stale_b_offset",
                        "file": rel_path,
                        "size": size,
                        "band": i + 1,
                        "actual": offset,
                        "expected": -clips[i],
                    })
                    break
            else:
                # Also check old markers (pre-OBY1 files used marker-exact)
                for i, om in enumerate(old_markers):
                    if offset == -om and om != clips[i]:
                        issues.append({
                            "type": "stale_b_offset",
                            "file": rel_path,
                            "size": size,
                            "band": i + 1,
                            "actual": offset,
                            "expected": -clips[i],
                        })
                        break

    # ── Screen clip containers (CX = clip value, CY = 16) ──
    # Match Screen elements with Size CX in clip range and CY=16
    screen_pattern = re.compile(
        r"<Size>\s*<CX>(\d+)</CX>\s*<CY>16</CY>\s*</Size>"
    )
    for m in screen_pattern.finditer(content):
        cx_val = int(m.group(1))
        if cx_val < 10 or cx_val > 300 or cx_val == width:
            continue  # Skip full-width or tiny values

        matched = False
        for clip in clips:
            if cx_val == clip:
                matched = True
                ok_count += 1
                break

        if not matched:
            # Check old clips
            for i, oc in enumerate(old_clips):
                if cx_val == oc and oc != clips[i]:
                    issues.append({
                        "type": "stale_screen_clip",
                        "file": rel_path,
                        "size": size,
                        "band": i + 1,
                        "actual": cx_val,
                        "expected": clips[i],
                    })
                    break
            else:
                # Also check old markers (pre-OBY1 files used marker-exact)
                for i, om in enumerate(old_markers):
                    if cx_val == om and om != clips[i]:
                        issues.append({
                            "type": "stale_screen_clip",
                            "file": rel_path,
                            "size": size,
                            "band": i + 1,
                            "actual": cx_val,
                            "expected": clips[i],
                        })
                        break

    return issues, ok_count


def discover_all_files():
    """Find all XML files with composite gauges (main + Options + Testing)."""
    files = []

    # Main files
    for size, fnames in GAUGE_FILES_BY_SIZE.items():
        for fname in fnames:
            path = ROOT / fname
            if path.exists():
                files.append((path, size, "main"))

    # Options variants
    options_dir = ROOT / "Options"
    if options_dir.exists():
        for size, fnames in GAUGE_FILES_BY_SIZE.items():
            for fname in fnames:
                for f in options_dir.rglob(fname):
                    files.append((f, size, "option"))

    # Testing variants
    testing_dir = ROOT / "Testing"
    if testing_dir.exists():
        for size, fnames in GAUGE_FILES_BY_SIZE.items():
            for fname in fnames:
                for f in testing_dir.rglob(fname):
                    files.append((f, size, "testing"))

    return files


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Audit gauge alignment")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true", help="Write JSON to .tmp/")
    args = parser.parse_args()

    print("=" * 65)
    print("  Gauge Alignment Audit (snap_columns edition)")
    print("=" * 65)
    print()

    print("Canonical markers (snapped to exact fifths):")
    for size in sorted(WIDTHS.keys()):
        clips = get_clips(size)
        print(f"  {size}: width={WIDTHS[size]}, markers={GRID_MARKERS[size]}, clips={clips}")
    print()

    # Show what shifted
    print("Changes from old positions:")
    for size in sorted(WIDTHS.keys()):
        old = OLD_MARKERS[size]
        new = GRID_MARKERS[size]
        changes = [f"B{i+1}: {old[i]}->{new[i]}" for i in range(4) if old[i] != new[i]]
        print(f"  {size}: {', '.join(changes) if changes else '(none)'}")
    print()

    all_issues = []

    # ── Layer 1: Animations ──
    print("-" * 65)
    print("Layer 1: Animations (EQUI_Animations.xml)")
    print("-" * 65)
    anim_issues, anim_ok = scan_animations(args.verbose)
    if anim_issues:
        for issue in anim_issues:
            print(f"  ISSUE [{issue['type']}] {issue['name']}: "
                  f"actual={issue['actual']}, expected={issue['expected']}")
        all_issues.extend(anim_issues)
    else:
        print(f"  All oversized animations OK ({anim_ok} checked)")
    print()

    # ── Layer 2: Window XMLs ──
    print("-" * 65)
    print("Layer 2: Gauge Elements (window XMLs)")
    print("-" * 65)
    files = discover_all_files()
    file_ok_count = 0
    file_issue_count = 0

    for filepath, size, source in files:
        rel = filepath.relative_to(ROOT)
        file_issues, file_ok = scan_gauge_file(str(filepath), size, args.verbose)
        if file_issues:
            file_issue_count += 1
            print(f"\n  {rel} ({size}):")
            for issue in file_issues:
                desc = f"    [{issue['type']}] Band {issue.get('band', '?')}: "
                desc += f"actual={issue['actual']}"
                if 'expected' in issue:
                    desc += f", expected={issue['expected']}"
                print(desc)
            all_issues.extend(file_issues)
        else:
            file_ok_count += 1
            if args.verbose:
                print(f"  {rel}: OK ({file_ok} values checked)")

    print()

    # ── Summary ──
    print("=" * 65)
    if all_issues:
        by_type = {}
        for issue in all_issues:
            t = issue["type"]
            by_type.setdefault(t, []).append(issue)

        total = len(all_issues)
        stale_count = sum(len(v) for k, v in by_type.items() if "stale" in k)
        print(f"  ISSUES FOUND: {total} total ({stale_count} stale pre-snap values)")
        print()
        for t, items in sorted(by_type.items()):
            print(f"  {t}: {len(items)}")
        print()
        print(f"  Files with issues: {file_issue_count}")
        print(f"  Files clean: {file_ok_count}")
    else:
        print(f"  ALL CLEAR — no alignment issues found")
        print(f"  Files checked: {file_ok_count}")
    print("=" * 65)

    if args.json:
        tmp_dir = Path(__file__).resolve().parent.parent / ".tmp"
        tmp_dir.mkdir(exist_ok=True)
        report = {
            "markers": GRID_MARKERS,
            "old_markers": OLD_MARKERS,
            "widths": WIDTHS,
            "issues": all_issues,
            "files_checked": file_ok_count + file_issue_count,
            "files_with_issues": file_issue_count,
        }
        out = tmp_dir / "audit_gauges.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nJSON report: {out}")

    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
