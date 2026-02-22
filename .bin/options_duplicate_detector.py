#!/usr/bin/env python3
"""
Duplicate Variant Detector - Identify redundant UI variants in Options directory.

Scans all variants within each window directory to find:
1. Functionally identical files (same content as Thorne or other variants)
2. Near-identical files (very similar content, likely duplicates)
3. Suggestions for consolidation
4. Variants that could be removed/archived

Compares files using:
- MD5 checksum for exact matches
- Line-by-line diff for similarity detection

Usage:
    python duplicate_detector.py [--similarity PERCENT] [--detailed] [--remove-candidates]
    
Options:
    --similarity N   Set similarity threshold 0-100 (default 95)
    --detailed       Show detailed diff information
    --remove-candidates  List variants recommended for removal
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import difflib

class DuplicateDetector:
    def __init__(self, options_root, similarity_threshold=95):
        self.options_root = Path(options_root)
        self.similarity_threshold = similarity_threshold
        self.results = {
            "scan_timestamp": datetime.now().isoformat(),
            "windows": {},
            "duplicates_found": 0,
            "similar_sets": 0,
            "candidates_for_removal": []
        }
    
    def calculate_checksum(self, file_path):
        """Calculate MD5 checksum of file."""
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return None
    
    def read_file_lines(self, file_path):
        """Read file into list of lines."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.readlines()
        except:
            return []
    
    def calculate_similarity(self, lines1, lines2):
        """Calculate similarity percentage between two file line lists."""
        if not lines1 or not lines2:
            return 0
        
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        ratio = matcher.ratio()
        return int(ratio * 100)
    
    def get_xml_files(self, directory):
        """Get all EQUI_*.xml files in directory."""
        xml_files = {}
        for file in directory.iterdir():
            if file.name.startswith('EQUI') and file.suffix == '.xml':
                checksum = self.calculate_checksum(file)
                xml_files[file.name] = {
                    "path": file,
                    "checksum": checksum,
                    "size": file.stat().st_size,
                    "mtime": file.stat().st_mtime
                }
        return xml_files
    
    def scan_window(self, window_dir):
        """Scan a single window directory for duplicate variants."""
        window_name = window_dir.name
        variants = defaultdict(list)
        
        # Collect all variants and their XMLs
        for item in window_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                variant_name = item.name
                xml_files = self.get_xml_files(item)
                if xml_files:
                    for xml_name, xml_info in xml_files.items():
                        variants[xml_name].append({
                            "variant": variant_name,
                            "path": item,
                            **xml_info
                        })
        
        # Analyze each XML type for duplicates
        window_results = {
            "exact_duplicates": [],
            "similar_groups": [],
            "total_variants": len(list(window_dir.glob('*/**/EQUI*.xml')))
        }
        
        for xml_name, locations in variants.items():
            if len(locations) <= 1:
                continue
            
            # Check for exact duplicates
            checksums = {}
            for loc in locations:
                checksum = loc['checksum']
                if checksum not in checksums:
                    checksums[checksum] = []
                checksums[checksum].append(loc)
            
            # Report exact duplicates
            for checksum, dupes in checksums.items():
                if len(dupes) > 1:
                    window_results["exact_duplicates"].append({
                        "xml_file": xml_name,
                        "count": len(dupes),
                        "variants": [d['variant'] for d in dupes],
                        "checksum": checksum,
                        "size": dupes[0]['size']
                    })
            
            # Check for similar variants
            if len(locations) > 1:
                lines_cache = {}
                for i, loc1 in enumerate(locations):
                    for loc2 in locations[i+1:]:
                        if loc1['path'] == loc2['path']:
                            continue
                        
                        # Get cached lines or read
                        path1_str = str(loc1['path'] / loc1['path'].name)
                        path2_str = str(loc2['path'] / loc2['path'].name)
                        
                        if path1_str not in lines_cache:
                            lines_cache[path1_str] = self.read_file_lines(loc1['path'] / xml_name)
                        if path2_str not in lines_cache:
                            lines_cache[path2_str] = self.read_file_lines(loc2['path'] / xml_name)
                        
                        lines1 = lines_cache[path1_str]
                        lines2 = lines_cache[path2_str]
                        similarity = self.calculate_similarity(lines1, lines2)
                        
                        if similarity >= self.similarity_threshold:
                            window_results["similar_groups"].append({
                                "xml_file": xml_name,
                                "variant1": loc1['variant'],
                                "variant2": loc2['variant'],
                                "similarity": similarity,
                                "size1": loc1['size'],
                                "size2": loc2['size']
                            })
        
        return window_results
    
    def scan(self):
        """Scan all windows in Options directory."""
        # Get all window directories
        window_dirs = [d for d in self.options_root.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        
        duplicate_count = 0
        similar_count = 0
        
        for window_dir in sorted(window_dirs):
            results = self.scan_window(window_dir)
            if results['exact_duplicates'] or results['similar_groups']:
                self.results['windows'][window_dir.name] = results
                duplicate_count += len(results['exact_duplicates'])
                similar_count += len(results['similar_groups'])
        
        self.results['duplicates_found'] = duplicate_count
        self.results['similar_sets'] = similar_count
    
    def print_report(self, detailed=False, show_removals=False):
        """Print formatted report."""
        print("\n" + "="*70)
        print("DUPLICATE VARIANT DETECTOR REPORT")
        print("="*70)
        print(f"Scan Timestamp: {self.results['scan_timestamp']}")
        print(f"Exact Duplicates Found: {self.results['duplicates_found']}")
        print(f"Similar Sets Found: {self.results['similar_sets']}\n")
        
        if not self.results['windows']:
            print("[OK] No duplicates detected!\n")
            return
        
        # Report by window
        for window_name, window_data in sorted(self.results['windows'].items()):
            has_issues = (len(window_data['exact_duplicates']) > 0 or 
                         len(window_data['similar_groups']) > 0)
            
            if not has_issues:
                continue
            
            print(f"\n[DIR] {window_name}")
            print("   " + "-"*65)
            
            # Exact duplicates
            if window_data['exact_duplicates']:
                print(f"   [DUP] EXACT DUPLICATES ({len(window_data['exact_duplicates'])})")
                for dup in window_data['exact_duplicates']:
                    print(f"      {dup['xml_file']}")
                    print(f"        Variants: {', '.join(dup['variants'])}")
                    print(f"        Size: {dup['size']} bytes (appears {dup['count']} times)")
                    print(f"        -> Consider keeping one, remove others")
            
            # Similar groups
            if window_data['similar_groups']:
                print(f"   [SIM] SIMILAR VARIANTS ({len(window_data['similar_groups'])})")
                for sim in window_data['similar_groups']:
                    print(f"      {sim['xml_file']}")
                    print(f"        • {sim['variant1']} <-> {sim['variant2']}")
                    print(f"        • Similarity: {sim['similarity']}%")
                    print(f"        • Sizes: {sim['size1']} vs {sim['size2']} bytes")
        
        # Removal candidates
        if show_removals:
            print("\n" + "="*70)
            print("REMOVAL CANDIDATES")
            print("="*70)
            candidates = self._identify_removal_candidates()
            if candidates:
                for window, variants in candidates.items():
                    print(f"\n{window}:")
                    for variant in variants:
                        print(f"  -> {variant}")
            else:
                print("No clear removal candidates identified.")
        
        print("\n" + "="*70 + "\n")
    
    def _identify_removal_candidates(self):
        """Identify variants that could be safely removed."""
        candidates = {}
        
        for window_name, window_data in self.results['windows'].items():
            removal_list = []
            
            # Exact duplicates: recommend removing non-Thorne variants
            for dup in window_data['exact_duplicates']:
                variants = dup['variants']
                if 'Thorne' in variants and len(variants) > 1:
                    removal_list.extend([v for v in variants if v != 'Thorne'])
            
            if removal_list:
                candidates[window_name] = removal_list
        
        return candidates
    
    def save_report(self, output_file):
        """Save report to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Detailed report saved to: {output_file}")
    
    def get_summary(self):
        """Return summary for other tools."""
        return {
            "total_duplicates": self.results['duplicates_found'],
            "total_similar": self.results['similar_sets'],
            "affected_windows": list(self.results['windows'].keys()),
            "duplicate_data": self.results['windows']
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="options_duplicate_detector.py",
        description="""
Detect Duplicate UI Variant Files in Options/

Scans Options/ directory structure to find identical or similar variant files
within the same window. Uses similarity threshold for fuzzy matching.

FEATURES:
  ✓ Exact duplicate detection (100% match)
  ✓ Fuzzy matching with configurable similarity threshold
  ✓ Window-level analysis with variant grouping
  ✓ Removal candidates report (safe to delete)
  ✓ Detailed hash-based comparison
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # Quick scan - find exact duplicates
  python .bin/options_duplicate_detector.py

  # Detailed output showing all similar variants
  python .bin/options_duplicate_detector.py --detailed

  # Show removal candidates with fuzzy matching (95% similarity)
  python .bin/options_duplicate_detector.py --remove-candidates

  # Custom similarity threshold (85% = more lenient matching)
  python .bin/options_duplicate_detector.py --similarity 85 --detailed

SIMILARITY THRESHOLD:
  - 100 = Exact match only
  - 95  = Allow small differences (default)
  - 85  = Allow moderate differences
  - 70  = Allow major differences (rarely useful)

OUTPUT:
  - Console: Duplicate report with statistics
  - .reports/duplicate_detection_report.json: Full audit data
"""
    )
    
    parser.add_argument(
        "--similarity", "-s",
        type=int,
        default=95,
        metavar="PERCENT",
        help="Similarity threshold (0-100, default: 95)"
    )
    parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed variant information and hash comparisons"
    )
    parser.add_argument(
        "--remove-candidates",
        action="store_true",
        help="Show variants safe to remove (duplicates)"
    )
    
    args = parser.parse_args()
    
    # Validate similarity argument
    if not 0 <= args.similarity <= 100:
        parser.error("--similarity must be between 0 and 100")
    
    # Determine Options path
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    options_dir = root_dir / "thorne_drak" / "Options"
    
    if not options_dir.exists():
        print(f"ERROR: Options directory not found at {options_dir}")
        sys.exit(1)
    
    # Run detector
    detector = DuplicateDetector(options_dir, similarity_threshold=args.similarity)
    print(f"Scanning {options_dir}...")
    detector.scan()
    
    # Print report
    detector.print_report(detailed=args.detailed, show_removals=args.remove_candidates)
    
    # Save JSON report
    report_file = root_dir / ".reports" / "duplicate_detection_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    detector.save_report(report_file)
    
    return detector.get_summary()


if __name__ == "__main__":
    main()
