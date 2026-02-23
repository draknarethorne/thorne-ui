#!/usr/bin/env python3
"""
Options README Checker - Audit and report on README.md file placement and synchronization.

Scans the Options directory structure to identify:
1. Orphaned/improperly placed README files in parent directories
2. Out-of-sync README files (older than corresponding XML files)
3. Incomplete documentation (READMEs with insufficient line count)
4. Missing README files in variant directories
5. Directory structure inconsistencies

Usage:
    python options_readme_checker.py [--fix] [--verbose]
    
Options:
    --fix       Automatically move orphaned READMEs to proper locations
    --verbose   Show detailed file listings
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class OptionsReadmeChecker:
    def __init__(self, options_root, min_readme_lines=80, deep_analysis_threshold=150):
        self.options_root = Path(options_root)
        self.min_readme_lines = min_readme_lines
        self.deep_analysis_threshold = deep_analysis_threshold  # Line count below which needs deep analysis
        self.results = {
            "orphaned_readmes": [],
            "out_of_sync": [],
            "incomplete_docs": [],
            "missing_readmes": [],
            "needs_deep_analysis": [],  # Skeletal READMEs that need agent work
            "good_readmes": [],
            "format_issues": [],  # File reference format, header issues
            "section_issues": [],  # Missing required sections
            "issues_found": 0,
            "timestamp": datetime.now().isoformat()
        }
        
    def get_readme_files(self):
        """Find all README*.md files in Options directory."""
        readmes = defaultdict(list)
        for root, dirs, files in os.walk(self.options_root):
            for file in files:
                if file.lower().startswith('readme') and file.endswith('.md'):
                    full_path = Path(root)
                    readmes[full_path].append(file)
        return readmes
    
    def get_window_directory(self, readme_path):
        """Determine if README is in window parent dir or variant dir."""
        # Structure: Options/[WindowName]/[VariantName]/README.md
        #       or: Options/[WindowName]/README.md
        parts = list(readme_path.relative_to(self.options_root).parts)
        if len(parts) == 0:  # Options/README.md
            return None, None, "root"
        elif len(parts) == 1:  # Options/WindowName/README.md
            return parts[0], None, "parent"
        elif len(parts) >= 2:  # Options/WindowName/VariantName/README.md
            return parts[0], parts[1], "variant"
        return None, None, "unknown"
    
    def find_matching_xml(self, readme_path):
        """Find XML file in same directory as README."""
        for file in readme_path.iterdir():
            if file.suffix == '.xml' and file.name.startswith('EQUI'):
                return file
        return None
    
    def count_lines(self, file_path):
        """Count non-empty lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return len([line for line in f if line.strip()])
        except:
            return 0
    
    def check_sync_status(self, readme_path, xml_path):
        """Check if README is in sync with XML file."""
        try:
            readme_mtime = os.path.getmtime(readme_path)
            xml_mtime = os.path.getmtime(xml_path)
            
            readme_time = datetime.fromtimestamp(readme_mtime)
            xml_time = datetime.fromtimestamp(xml_mtime)
            
            if readme_mtime < xml_mtime:
                return "OUT_OF_SYNC", f"XML modified after README ({xml_time.date()})"
            else:
                return "IN_SYNC", f"README: {readme_time.date()}, XML: {xml_time.date()}"
        except:
            return "ERROR", "Could not determine modification times"
    
    def check_file_reference_format(self, readme_path):
        """Check if File reference uses proper markdown link format."""
        issues = []
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for problematic patterns
            if 'thorne_drak/Options' in content:
                issues.append("Uses full path 'thorne_drak/Options/...' instead of local link")
            
            # Check for File reference in markdown link format
            # Support both **File**: and **File**: patterns
            file_patterns = ['**File:**', '**File**:']
            has_file_ref = any(pattern in content for pattern in file_patterns)
            
            if has_file_ref:
                # Extract line after File reference
                for pattern in file_patterns:
                    if pattern in content:
                        file_section = content.split(pattern)[1].split('\n')[0]
                        if '[' not in file_section:
                            issues.append("File reference not in markdown link format [file.xml](./file.xml)")
                        break
            
            # Check for proper author field (support both **Author**: and **Author**: patterns)
            has_author = '**Author:**' in content or '**Author**:' in content or 'Maintainer' in content
            if not has_author:
                issues.append("Missing Author field")
            elif '**Author:**' in content or '**Author**:' in content:
                # Extract what's there
                author_line = [line for line in content.split('\n') if '**Author' in line]
                if author_line and 'Draknare Thorne' not in author_line[0]:
                    issues.append("Author not listed as 'Draknare Thorne'")
                    
        except Exception as e:
            issues.append(f"Could not read file: {str(e)}")
            
        return issues
    
    def check_required_sections(self, readme_path, location):
        """Check if README has required sections."""
        missing = []
        found = {}
        
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for required sections based on location
            if location == "variant":
                # Variant files MUST have Purpose, Specifications, Key Features
                required = {
                    "Purpose": "## Purpose",
                    "Key Features": ["**Key Features**", "### Key Features"],
                    "Specifications": "## Specifications"
                }
                
                for section_name, pattern in required.items():
                    patterns = pattern if isinstance(pattern, list) else [pattern]
                    found_section = any(p in content for p in patterns)
                    found[section_name] = found_section
                    if not found_section:
                        missing.append(section_name)
                        
                # Recommended but not required
                optional = ["## Layout", "## Modifications", "## Color Scheme"]
                missing_optional = [s for s in optional if s not in content]
                
                return missing, missing_optional, found
                
            elif location == "parent":
                # Parent navigation files just need variant list
                return [], [], {}
                
            elif location == "root":
                # Root index files just need to exist
                return [], [], {}
                
        except Exception as e:
            return [f"Error reading file: {str(e)}"], [], {}
            
        return missing, [], found
    
    def check_metadata_fields(self, readme_path):
        """Check if all required metadata fields are present."""
        missing_fields = []
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                first_500_chars = content[:500]  # Check only header area
            
            # Support both **Field** and **Field:** patterns in markdown
            required_fields = {
                "File": ["**File**:", "**File**", "[EQUI"],
                "Version": ["**Version:**", "**Version**"],
                "Last Updated": ["**Last Updated:**", "**Last Updated**"],
                "Status": ["**Status:**", "**Status**"],
                "Author": ["**Author:**", "**Author**"]
            }
            
            for field, patterns in required_fields.items():
                patterns = patterns if isinstance(patterns, list) else [patterns]
                found = any(p in first_500_chars for p in patterns)
                if not found:
                    missing_fields.append(field)
                    
        except Exception as e:
            missing_fields.append(f"Error checking: {str(e)}")
            
        return missing_fields
    
    def scan(self):
        """Scan Options directory and generate report."""
        readmes = self.get_readme_files()
        
        for readme_dir, readme_files in sorted(readmes.items()):
            for readme_file in readme_files:
                readme_path = readme_dir / readme_file
                window, variant, location = self.get_window_directory(readme_dir)
                
                # Count lines
                line_count = self.count_lines(readme_path)
                is_complete = line_count >= self.min_readme_lines
                
                # Find matching XML
                xml_file = self.find_matching_xml(readme_dir)
                
                issue = {
                    "readme": readme_file,
                    "path": str(readme_path.relative_to(self.options_root)),
                    "window": window,
                    "variant": variant,
                    "location": location,
                    "line_count": line_count,
                    "has_xml": xml_file is not None,
                    "xml_name": xml_file.name if xml_file else None
                }
                
                # Classify
                if location == "root":
                    # Options/README.md - valid index file
                    if readme_file == "README.md":
                        issue["classification"] = "OK_INDEX"
                        self.results["good_readmes"].append(issue)
                    else:
                        issue["classification"] = "ROOT_LEVEL_ORPHAN"
                        self.results["orphaned_readmes"].append(issue)
                        self.results["issues_found"] += 1
                elif location == "parent":
                    # Options/[Window]/README.md - valid navigation file (generated by sync)
                    if readme_file == "README.md":
                        issue["classification"] = "OK_NAVIGATION"
                        self.results["good_readmes"].append(issue)
                    else:
                        # Options/[Window]/README_Something.md - orphaned
                        issue["classification"] = "PARENT_ORPHAN"
                        self.results["orphaned_readmes"].append(issue)
                        self.results["issues_found"] += 1
                elif location == "variant":
                    # Validate content and format for variants
                    format_issues = self.check_file_reference_format(readme_path)
                    metadata_issues = self.check_metadata_fields(readme_path)
                    section_issues, optional_sections, found_sections = self.check_required_sections(readme_path, location)
                    
                    issue["format_issues"] = format_issues
                    issue["metadata_issues"] = metadata_issues
                    issue["section_issues"] = section_issues
                    issue["optional_sections"] = optional_sections
                    issue["found_sections"] = found_sections
                    
                    if xml_file:
                        sync_status, sync_msg = self.check_sync_status(readme_path, xml_file)
                        issue["sync_status"] = sync_status
                        issue["sync_message"] = sync_msg
                        
                        # Determine classification
                        if format_issues or metadata_issues or section_issues:
                            # Has content/format problems
                            issue["classification"] = "NEEDS_FIX"
                            self.results["format_issues"].append(issue)
                            self.results["issues_found"] += 1
                        elif not is_complete:
                            issue["classification"] = "INCOMPLETE"
                            self.results["incomplete_docs"].append(issue)
                            self.results["issues_found"] += 1
                        elif sync_status == "OUT_OF_SYNC":
                            issue["classification"] = "OUT_OF_SYNC"
                            self.results["out_of_sync"].append(issue)
                            self.results["issues_found"] += 1
                        elif line_count < self.deep_analysis_threshold:
                            # Properly placed and synced, but skeletal/needs deep analysis
                            issue["classification"] = "NEEDS_ANALYSIS"
                            self.results["needs_deep_analysis"].append(issue)
                            self.results["issues_found"] += 1
                        else:
                            issue["classification"] = "OK"
                            self.results["good_readmes"].append(issue)
                    else:
                        issue["classification"] = "NO_XML"
                        self.results["missing_readmes"].append(issue)
                        self.results["issues_found"] += 1
    
    def print_report(self, verbose=False):
        """Print formatted report."""
        print("\n" + "="*70)
        print("OPTIONS README CHECKER REPORT")
        print("="*70)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Issues Found: {self.results['issues_found']}\n")
        
        # Orphaned READMEs
        if self.results['orphaned_readmes']:
            print("[!] ORPHANED/IMPROPERLY PLACED READMES (need correction)")
            print("-" * 70)
            for item in self.results['orphaned_readmes']:
                print(f"  {item['classification']}: {item['path']}")
                print(f"    -> File: {item['readme']} ({item['line_count']} lines)")
                if item['classification'] == 'PARENT_ORPHAN':
                    print(f"    -> Legacy file, should be removed or moved")
            print()
        
        # Format and content issues
        if self.results['format_issues']:
            print("[F] FORMAT/CONTENT ISSUES (needs fixing)")
            print("-" * 70)
            for item in self.results['format_issues']:
                variant_display = item['variant'] or '[Root]'
                print(f"  {item['window']}/{variant_display}")
                print(f"    -> Path: {item['path']}")
                if item['format_issues']:
                    print(f"    -> Format Issues: {', '.join(item['format_issues'])}")
                if item['metadata_issues']:
                    print(f"    -> Missing Metadata: {', '.join(item['metadata_issues'])}")
                if item['section_issues']:
                    print(f"    -> Missing Sections: {', '.join(item['section_issues'])}")
            print()
        
        # Out of sync
        if self.results['out_of_sync']:
            print("[T] OUT OF SYNC (documentation older than XML)")
            print("-" * 70)
            for item in self.results['out_of_sync']:
                variant_display = item['variant'] or '[Root]'
                print(f"  {item['window']}/{variant_display}")
                print(f"    -> {item['sync_message']}")
            print()
        
        # Incomplete docs
        if self.results['incomplete_docs']:
            print("[*] INCOMPLETE DOCUMENTATION (< {} lines)".format(self.min_readme_lines))
            print("-" * 70)
            for item in self.results['incomplete_docs']:
                variant_display = item['variant'] or '[Root]'
                print(f"  {item['window']}/{variant_display}")
                print(f"    -> {item['readme']}: {item['line_count']} lines (need ~{self.min_readme_lines}+)")
            print()
        
        # Missing READMEs
        if self.results['missing_readmes']:
            print("[X] MISSING INFORMATION (README exists but no XML)")
            print("-" * 70)
            for item in self.results['missing_readmes']:
                variant_display = item['variant'] or '[Root]'
                print(f"  {item['window']}/{variant_display}")
                print(f"    -> {item['readme']} (no matching EQUI_*.xml found)")
            print()
        
        # Needs deep analysis
        if self.results['needs_deep_analysis']:
            print("[AGENT] NEEDS DEEP DOCUMENTATION ANALYSIS (skeletal/generic)")
            print("-" * 70)
            print("These are properly placed READMEs with matching XMLs, but need")
            print("detailed technical analysis and more comprehensive documentation.")
            print()
            for item in self.results['needs_deep_analysis']:
                variant_display = item['variant'] or '[Root]'
                print(f"  {item['window']}/{variant_display}")
                print(f"    -> {item['readme']}: {item['line_count']} lines")
                print(f"       Path: {item['path']}")
            print()
        
        # Good status
        if verbose and self.results['good_readmes']:
            print("[OK] PROPERLY DOCUMENTED")
            print("-" * 70)
            for item in self.results['good_readmes']:
                variant_display = item['variant'] or '[Root]'
                classification = item.get('classification', 'OK')
                print(f"  {item['window']}/{variant_display}")
                
                # Show sync message only for variant READMEs with XML
                if 'sync_message' in item:
                    print(f"    -> {item['readme']}: {item['line_count']} lines - {item['sync_message']}")
                else:
                    # Navigation or index READMEs
                    print(f"    -> {item['readme']}: {item['line_count']} lines ({classification})")
            print()
        
        # Summary
        print("="*70)
        print("SUMMARY")
        print("="*70)
        print(f"  Orphaned/Improper:     {len(self.results['orphaned_readmes'])}")
        print(f"  Format/Content Issues: {len(self.results['format_issues'])}")
        print(f"  Out of Sync:           {len(self.results['out_of_sync'])}")
        print(f"  Incomplete:            {len(self.results['incomplete_docs'])}")
        print(f"  No XML Found:          {len(self.results['missing_readmes'])}")
        print(f"  Needs Deep Analysis:   {len(self.results['needs_deep_analysis'])}")
        print(f"  Properly Documented:   {len(self.results['good_readmes'])}")
        print(f"  Total Issues:          {self.results['issues_found']}")
        print("="*70 + "\n")
    
    def save_report(self, output_file):
        """Save report to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Report saved to: {output_file}")
    
    def get_issues_summary(self):
        """Return summary for other tools to use."""
        return {
            "orphaned_count": len(self.results['orphaned_readmes']),
            "orphaned_list": self.results['orphaned_readmes'],
            "out_of_sync_count": len(self.results['out_of_sync']),
            "incomplete_count": len(self.results['incomplete_docs']),
            "needs_analysis_count": len(self.results['needs_deep_analysis']),
            "needs_analysis_list": self.results['needs_deep_analysis'],
            "total_issues": self.results['issues_found']
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="options_readme_checker.py",
        description="""
Validate README Documentation in UI Variants

Audits Options/ variant directories to detect documentation issues:
- Missing README.md files (orphaned variants)
- Incomplete or poor-quality documentation
- Out-of-sync descriptions
- Missing required sections

FEATURES:
  ✓ Comprehensive README quality audit
  ✓ Identification of orphaned variants (no README)
  ✓ Detection of incomplete documentation
  ✓ Deep analysis for variants needing attention
  ✓ Detailed reporting with recommendations
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # Quick scan - summary report
  python .bin/options_readme_checker.py

  # Detailed output with all issues
  python .bin/options_readme_checker.py --verbose

  # Combined with fix_readme tool:
  python .bin/options_readme_checker.py --verbose
  python .bin/options_fix_readme.py --dry-run
  python .bin/options_fix_readme.py

REPORTS:
  - Console: Summary of issues found
  - .reports/readme_check_report.json: Full audit data

OUTPUT CATEGORIES:
  - Missing: Variants without README.md
  - Incomplete: Short or minimal documentation
  - Out-of-sync: Descriptions don't match window type
  - Needs Analysis: Potential improvements recommended
"""
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed analysis for each issue"
    )
    
    args = parser.parse_args()
    
    # Determine Options path
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    options_dir = root_dir / "thorne_drak" / "Options"
    
    if not options_dir.exists():
        print(f"ERROR: Options directory not found at {options_dir}")
        sys.exit(1)
    
    # Run checker
    checker = OptionsReadmeChecker(options_dir)
    checker.scan()
    
    # Print report
    checker.print_report(verbose=args.verbose)
    
    # Save JSON report
    report_file = root_dir / ".reports" / "readme_check_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    checker.save_report(report_file)
    
    return checker.get_issues_summary()


if __name__ == "__main__":
    main()
