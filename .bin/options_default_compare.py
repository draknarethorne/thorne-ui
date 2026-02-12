#!/usr/bin/env python3
"""
Options Default Variant Comparison Tool

Audits Options/ structure to identify:
- Which windows have Default variants (unified source of truth)
- Which named variants are identical to their Default (redundant duplicates)
- Which named variants differ from Default (intentional custom variants)
- Overall consistency of Options structure

Usage:
    python .bin/options_default_compare.py                    # Full report
    python .bin/options_default_compare.py --verbose          # Detailed output
    python .bin/options_default_compare.py --window "Inventory"  # Specific window

Output:
    - Console: Summary or detailed report
    - .reports/options_default_compare.json: Full audit data
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
        "has_default": False,
        "default_xml": None,
        "default_hash": None,
        "variants": [],
        "duplicate_count": 0,
        "custom_variant_count": 0,
    }
    
    # Find Default variant
    default_path = window_path / "Default"
    if default_path.exists() and default_path.is_dir():
        result["has_default"] = True
        xml_files = list(default_path.glob("EQUI_*.xml"))
        if xml_files:
            default_xml_path = xml_files[0]
            result["default_xml"] = default_xml_path.name
            result["default_hash"] = get_file_hash(default_xml_path)
    else:
        return result
    
    # Scan all other variants
    if result["default_xml"]:
        for variant_path in sorted(window_path.iterdir()):
            if not variant_path.is_dir() or variant_path.name == "Default":
                continue
            
            variant_name = variant_path.name
            variant_xml_path = variant_path / result["default_xml"]
            
            if not variant_xml_path.exists():
                result["variants"].append({
                    "name": variant_name,
                    "status": "missing_xml",
                    "is_identical_to_default": False,
                })
                continue
            
            variant_hash = get_file_hash(variant_xml_path)
            is_identical = variant_hash == result["default_hash"]
            
            result["variants"].append({
                "name": variant_name,
                "hash": variant_hash,
                "is_identical_to_default": is_identical,
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
    print("OPTIONS DEFAULT VARIANT AUDIT REPORT")
    print("=" * 80)
    
    windows_with_default = sum(1 for r in results.values() if r["has_default"])
    windows_without_default = len(results) - windows_with_default
    total_duplicates = sum(r["duplicate_count"] for r in results.values())
    total_custom = sum(r["custom_variant_count"] for r in results.values())
    
    print(f"\nSummary:")
    print(f"  Total windows: {len(results)}")
    print(f"  With Default: {windows_with_default}")
    print(f"  Total duplicate variants: {total_duplicates}")
    print(f"  Total custom variants: {total_custom}")
    
    # Windows WITHOUT Default
    print("\n" + "-" * 80)
    print("WINDOWS WITHOUT DEFAULT:")
    print("-" * 80)
    
    orphan_windows = [k for k, v in results.items() if not v["has_default"]]
    if orphan_windows:
        for name in sorted(orphan_windows):
            print(f"  {name}/ (NO DEFAULT - orphaned variants)")
    else:
        print("  OK: All windows have a Default variant")
    
    # Duplicate variants
    print("\n" + "-" * 80)
    print("DUPLICATE VARIANTS (identical to Default):")
    print("-" * 80)
    
    dup_windows = {k: v for k, v in results.items() 
                   if v["has_default"] and v["duplicate_count"] > 0}
    
    if dup_windows:
        for window, info in sorted(dup_windows.items()):
            dups = [v["name"] for v in info["variants"] if v["is_identical_to_default"]]
            print(f"\n  {window}/")
            print(f"    Duplicates: {', '.join(dups)}")
            print(f"    Action: Consider naming as 'Default - <description>' or removing")
    else:
        print("\n  OK: No duplicate variants")
    
    # Custom variants
    print("\n" + "-" * 80)
    print("CUSTOM VARIANTS (differ from Default):")
    print("-" * 80)
    
    custom_windows = {k: v for k, v in results.items() 
                      if v["has_default"] and v["custom_variant_count"] > 0}
    
    if custom_windows:
        for window, info in sorted(custom_windows.items()):
            custom = [v["name"] for v in info["variants"] 
                     if not v["is_identical_to_default"] and v["status"] != "missing_xml"]
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
        
        if not info["has_default"]:
            print("  NO DEFAULT VARIANT")
            return
        
        print(f"  Default XML: {info['default_xml']}")
        print(f"  Hash: {info['default_hash'][:16]}...")
        print(f"\n  Variants ({len(info['variants'])}):")
        
        if not info["variants"]:
            print("    (Default only - no variants)")
        else:
            for v in sorted(info["variants"], key=lambda x: x["name"]):
                status_icon = "DUPLICATE" if v["is_identical_to_default"] else "CUSTOM"
                if v["status"] == "missing_xml":
                    status_icon = "MISSING"
                
                hash_str = v.get("hash", "")[:16] if v.get("hash") else "N/A"
                print(f"    [{status_icon:10}] {v['name']:45} [{hash_str}]")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audit Options Default variants and identify duplicates"
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
    report_path = Path(".reports/options_default_compare.json")
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nReport saved: {report_path}")

if __name__ == "__main__":
    main()
