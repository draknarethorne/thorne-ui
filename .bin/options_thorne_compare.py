#!/usr/bin/env python3
"""
Options Thorne Variant Comparison Tool

Audits Options/ structure to identify:
- Which windows have Thorne variants (preferred source of truth)
- Which named variants are identical to Thorne (redundant duplicates)
- Which named variants differ from Thorne (intentional custom variants)
- Overall consistency of Options structure

Usage:
    python .bin/options_thorne_compare.py                    # Full report
    python .bin/options_thorne_compare.py --verbose          # Detailed output
    python .bin/options_thorne_compare.py --window "Inventory"  # Specific window

Output:
    - Console: Summary or detailed report
    - .reports/options_thorne_compare.json: Full audit data
"""

import json
import hashlib
import sys
from pathlib import Path

OPTIONS_DIR = Path("thorne_drak/Options")

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def scan_window(window_name):
    """Scan a single window's Options structure."""
    window_path = OPTIONS_DIR / window_name
    if not window_path.exists():
        return None
    
    result = {
        "window_name": window_name,
        "has_thorne": False,
        "thorne_xml": None,
        "thorne_hash": None,
        "variants": [],
        "duplicate_count": 0,
        "custom_variant_count": 0,
    }
    
    # Find Thorne variant
    thorne_path = window_path / "Thorne"
    if thorne_path.exists() and thorne_path.is_dir():
        result["has_thorne"] = True
        xml_files = list(thorne_path.glob("EQUI_*.xml"))
        if xml_files:
            thorne_xml_path = xml_files[0]
            result["thorne_xml"] = thorne_xml_path.name
            result["thorne_hash"] = get_file_hash(thorne_xml_path)
    else:
        return result
    
    # Scan all other variants
    if result["thorne_xml"]:
        for variant_path in sorted(window_path.iterdir()):
            if not variant_path.is_dir() or variant_path.name == "Thorne":
                continue
            
            variant_name = variant_path.name
            variant_xml_path = variant_path / result["thorne_xml"]
            
            if not variant_xml_path.exists():
                result["variants"].append({
                    "name": variant_name,
                    "status": "missing_xml",
                    "is_identical_to_thorne": False,
                })
                continue
            
            variant_hash = get_file_hash(variant_xml_path)
            is_identical = variant_hash == result["thorne_hash"]
            
            result["variants"].append({
                "name": variant_name,
                "hash": variant_hash,
                "is_identical_to_thorne": is_identical,
                "status": "identical" if is_identical else "custom",
            })
            
            if is_identical:
                result["duplicate_count"] += 1
            else:
                result["custom_variant_count"] += 1
    
    return result

def scan_all_windows():
    """Scan all Options windows."""
    if not OPTIONS_DIR.exists():
        print(f"Error: {OPTIONS_DIR} not found")
        sys.exit(1)
    
    results = {}
    for window_path in sorted(OPTIONS_DIR.iterdir()):
        if not window_path.is_dir() or window_path.name.startswith("."):
            continue
        result = scan_window(window_path.name)
        if result:
            results[window_path.name] = result
    
    return results

def print_summary(results):
    """Print human-readable summary report."""
    print("\n" + "=" * 80)
    print("OPTIONS THORNE VARIANT AUDIT REPORT")
    print("=" * 80)
    
    windows_with_thorne = sum(1 for r in results.values() if r["has_thorne"])
    windows_without_thorne = len(results) - windows_with_thorne
    total_duplicates = sum(r["duplicate_count"] for r in results.values())
    total_custom = sum(r["custom_variant_count"] for r in results.values())
    
    print(f"\nSummary:")
    print(f"  Total windows: {len(results)}")
    print(f"  With Thorne: {windows_with_thorne}")
    print(f"  Total duplicate variants: {total_duplicates}")
    print(f"  Total custom variants: {total_custom}")
    
    # Windows WITHOUT Default
    print("\n" + "-" * 80)
    print("WINDOWS WITHOUT THORNE:")
    print("-" * 80)
    
    orphan_windows = [k for k, v in results.items() if not v["has_thorne"]]
    if orphan_windows:
        for name in sorted(orphan_windows):
            print(f"  {name}/ (NO THORNE - orphaned variants)")
    else:
        print("  OK: All windows have a Thorne variant")
    
    # Duplicate variants
    print("\n" + "-" * 80)
    print("DUPLICATE VARIANTS (identical to Thorne):")
    print("-" * 80)
    
    dup_windows = {k: v for k, v in results.items() 
                   if v["has_thorne"] and v["duplicate_count"] > 0}
    
    if dup_windows:
        for window, info in sorted(dup_windows.items()):
            dups = [v["name"] for v in info["variants"] if v["is_identical_to_thorne"]]
            print(f"\n  {window}/")
            print(f"    Duplicates: {', '.join(dups)}")
            print(f"    Action: Consider naming as 'Thorne - <description>' or removing")
    else:
        print("\n  OK: No duplicate variants")
    
    # Custom variants
    print("\n" + "-" * 80)
    print("CUSTOM VARIANTS (differ from Thorne):")
    print("-" * 80)
    
    custom_windows = {k: v for k, v in results.items() 
                      if v["has_thorne"] and v["custom_variant_count"] > 0}
    
    if custom_windows:
        for window, info in sorted(custom_windows.items()):
            custom = [v["name"] for v in info["variants"] 
                     if not v["is_identical_to_thorne"] and v["status"] != "missing_xml"]
            if custom:
                print(f"\n  {window}/")
                print(f"    Variants: {', '.join(custom)}")
    else:
        print("\n  (None)")
    
    print("\n" + "=" * 80)

def print_detailed(results, window_name=None):
    """Print detailed output for specific window or all."""
    if window_name:
        if window_name not in results:
            print(f"Window '{window_name}' not found")
            return
        windows = {window_name: results[window_name]}
    else:
        windows = results
    
    for wname, info in sorted(windows.items()):
        print(f"\n{'=' * 80}")
        print(f"{wname}")
        print(f"{'=' * 80}")
        
        if not info["has_thorne"]:
            print("  NO THORNE VARIANT")
            return
        
        print(f"  Thorne XML: {info['thorne_xml']}")
        print(f"  Hash: {info['thorne_hash'][:16]}...")
        print(f"\n  Variants ({len(info['variants'])}):")
        
        if not info["variants"]:
            print("    (Thorne only - no variants)")
        else:
            for v in sorted(info["variants"], key=lambda x: x["name"]):
                status_icon = "DUPLICATE" if v["is_identical_to_thorne"] else "CUSTOM"
                if v["status"] == "missing_xml":
                    status_icon = "MISSING"
                
                hash_str = v.get("hash", "")[:16] if v.get("hash") else "N/A"
                print(f"    [{status_icon:10}] {v['name']:45} [{hash_str}]")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audit Options Thorne variants and identify duplicates"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed variant hashes")
    parser.add_argument("--window", "-w", type=str,
                       help="Audit specific window")
    parser.add_argument("--all", action="store_true",
                       help="Verbose output for all windows")
    
    args = parser.parse_args()
    results = scan_all_windows()
    
    if args.all:
        args.verbose = True
    
    # Display report
    if args.verbose or args.window:
        print_detailed(results, args.window)
    else:
        print_summary(results)
    
    # Save JSON report
    report_path = Path(".reports/options_thorne_compare.json")
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nReport saved: {report_path}")

if __name__ == "__main__":
    main()
