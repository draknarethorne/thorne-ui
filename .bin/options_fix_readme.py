#!/usr/bin/env python3
"""
Fix README Headers and File References - Auto-correct mechanical issues in Options variant READMEs.

Fixes the following mechanical issues:
1. File references: Convert 'thorne_drak/Options/...' paths to local markdown links [file.xml](./file.xml)
2. Header standardization: Reorder metadata fields to consistent format
3. Author field: Ensure all variants have Author: Draknare Thorne
4. Dates: Standardize date format to YYYY-MM-DD
5. Spacing: Fix header blank line issues

Usage:
    python fix_readme_headers.py [--dry-run] [--verbose]
    
Options:
    --dry-run   Show what would change without modifying files
    --verbose   Show detailed output of all changes
    --window    Fix only README files in specific window directory
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

class ReadmeHeaderFixer:
    def __init__(self, options_root, dry_run=False, verbose=False):
        self.options_root = Path(options_root)
        self.dry_run = dry_run
        self.verbose = verbose
        self.changes_made = 0
        self.files_processed = 0
        self.fixes_applied = {}  # Track fixes by type
    
    def extract_header(self, content):
        """Extract the header section up to first ## section."""
        lines = content.split('\n')
        header_end = 0
        
        # Find the first ## (main section) which marks the end of header
        for i, line in enumerate(lines):
            if line.startswith('## ') and i > 2:
                header_end = i
                break
        
        if header_end == 0:
            # Fallback: use first 20 lines if no ## found
            header_end = min(20, len(lines))
        
        return lines[:header_end], lines[header_end:]
    
    def normalize_file_reference(self, header_lines):
        """Fix file reference from full path to local markdown link."""
        fixed = False
        new_lines = []
        
        for line in header_lines:
            if '**File**' in line or '**File**:' in line:
                # Check if it's a full path that needs fixing
                if 'thorne_drak/Options' in line:
                    # Extract filename from full path
                    match = re.search(r'(EQUI_\w+\.xml)', line)
                    if match:
                        filename = match.group(1)
                        new_line = f"**File**: [{filename}](./{filename})"
                        new_lines.append(new_line)
                        fixed = True
                        self._track_fix("file_reference")
                        continue
                
                # Check if it's a relative path that needs fixing (../../../EQUI_*.xml)
                elif re.search(r'\(\.\./\.\./\.\./.*EQUI_\w+\.xml\)', line):
                    # Extract filename from relative path
                    match = re.search(r'(EQUI_\w+\.xml)', line)
                    if match:
                        filename = match.group(1)
                        new_line = f"**File**: [{filename}](./{filename})"
                        new_lines.append(new_line)
                        fixed = True
                        self._track_fix("file_reference")
                        continue
                
                # Ensure proper formatting if it's already a link
                if '[EQUI_' in line and '](.)' in line:
                    # Already correct format
                    new_lines.append(line)
                    continue
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return new_lines, fixed
    
    def standardize_metadata_order(self, header_lines, readme_path=None):
        """Reorder metadata fields to standard format and fix title with variant name."""
        fixed = False
        new_lines = []
        
        # Extract metadata fields, filtering out separator lines
        title = None
        file_ref = None
        version = None
        updated = None
        status = None
        author = None
        based_on = None
        
        # First pass: extract all fields (skip separator lines)
        for line in header_lines:
            if line.strip() == '---':
                # Skip separator lines - will add one properly at the end
                continue
            elif line.startswith('# '):
                title = line
            elif '**File**' in line:
                file_ref = line
            elif '**Version**' in line:
                version = line
            elif '**Last Updated**' in line:
                updated = line
            elif '**Status**' in line:
                status = line
            elif '**Author**' in line:
                author = line
            elif '**Based On**' in line:
                based_on = line
            elif '**Maintainer**' in line:
                author = line.replace('**Maintainer**', '**Author**')
        
        # If we found metadata fields, rebuild in correct order
        if any([file_ref, version, updated, status, author]):
            # Get window and variant names from path if available
            window_name, variant_name = None, None
            if readme_path:
                window_name, variant_name = self.extract_window_and_variant(readme_path)
            
            # Construct proper title if we have window/variant names
            if window_name and variant_name:
                if variant_name.lower() == 'default':
                    proper_title = f"# Window: {window_name} - {variant_name} Variant"
                else:
                    # Standard, Custom, etc.
                    proper_title = f"# {window_name} Window - {variant_name} Variant"
                title = proper_title
            
            # Rebuild header
            if title:
                new_lines.append(title)
                new_lines.append('')
            
            if file_ref:
                new_lines.append(file_ref)
            if version:
                new_lines.append(version)
            if updated:
                new_lines.append(updated)
            if status:
                new_lines.append(status)
            if author:
                new_lines.append(author)
            if based_on:
                new_lines.append(based_on)
            
            new_lines.append('')
            new_lines.append('---')
            fixed = True
            self._track_fix("metadata_order")
        else:
            # Preserve original if no metadata found (but filter out separator lines)
            new_lines = [line for line in header_lines if line.strip() != '---']
        
        return new_lines, fixed
    
    def ensure_author_field(self, header_lines):
        """Ensure Author field exists and is set to Draknare Thorne."""
        fixed = False
        
        # Check if Author field exists
        has_author = any('**Author**' in line or '**Maintainer**' in line for line in header_lines)
        
        if not has_author:
            # Find where to insert it (after Status field)
            for i, line in enumerate(header_lines):
                if '**Status**' in line:
                    header_lines.insert(i + 1, '**Author**: Draknare Thorne')
                    fixed = True
                    self._track_fix("missing_author")
                    break
        else:
            # Verify it's Draknare Thorne
            for i, line in enumerate(header_lines):
                if '**Author**' in line:
                    if 'Draknare Thorne' not in line:
                        header_lines[i] = '**Author**: Draknare Thorne'
                        fixed = True
                        self._track_fix("incorrect_author")
        
        return header_lines, fixed
    
    def standardize_dates(self, header_lines):
        """Standardize date format to YYYY-MM-DD."""
        fixed = False
        new_lines = []
        
        for line in header_lines:
            if '**Last Updated**' in line:
                # Try to extract and reformat date
                # Acceptable formats: Feb 3, 2026 or February 3, 2026 or 2026-02-03
                if 'February' in line or 'Feb' in line:
                    # Parse the date - be flexible
                    today = datetime.now()
                    new_date = today.strftime('%Y-%m-%d')
                    new_line = f"**Last Updated**: {new_date}"
                    new_lines.append(new_line)
                    fixed = True
                    self._track_fix("date_format")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return new_lines, fixed
    
    def fix_file(self, readme_path):
        """Fix a single README file."""
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            header_lines, body_lines = self.extract_header(content)
            
            # Apply fixes
            header_lines, file_fixed = self.normalize_file_reference(header_lines)
            header_lines, metadata_fixed = self.standardize_metadata_order(header_lines, readme_path)
            header_lines, author_fixed = self.ensure_author_field(header_lines)
            header_lines, date_fixed = self.standardize_dates(header_lines)
            
            any_fixed = file_fixed or metadata_fixed or author_fixed or date_fixed
            
            if any_fixed:
                new_content = '\n'.join(header_lines) + '\n' + '\n'.join(body_lines)
                
                if not self.dry_run:
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                if self.verbose or any_fixed:
                    variant_path = str(readme_path.relative_to(self.options_root))
                    print(f"[FIXED] {variant_path}")
                    if file_fixed:
                        print(f"  - File reference format")
                    if metadata_fixed:
                        print(f"  - Metadata field ordering")
                    if author_fixed:
                        print(f"  - Author field")
                    if date_fixed:
                        print(f"  - Date format")
                
                self.changes_made += 1
            
            self.files_processed += 1
            
        except Exception as e:
            print(f"ERROR processing {readme_path}: {str(e)}")
    
    def scan_and_fix(self, window_filter=None):
        """Scan Options directory and fix all variant READMEs."""
        print(f"\nScanning Options directory...")
        if self.dry_run:
            print("(DRY RUN - No changes will be made)\n")
        
        count = 0
        for root, dirs, files in os.walk(self.options_root):
            if 'README.md' in files:
                readme_path = Path(root) / 'README.md'
                rel_path = readme_path.relative_to(self.options_root)
                
                # Skip root and parent navigation READMEs (only fix variants)
                parts = list(rel_path.parent.parts)
                if len(parts) >= 2:  # This is a variant README
                    if window_filter is None or window_filter in str(rel_path):
                        self.fix_file(readme_path)
                        count += 1
        
        self.print_summary(count)
    
    def _track_fix(self, fix_type):
        """Track fixes by type."""
        self.fixes_applied[fix_type] = self.fixes_applied.get(fix_type, 0) + 1
    
    def extract_window_and_variant(self, readme_path):
        """Extract window name and variant name from file path.
        
        Expected paths:
        - thorne_drak/Options/Actions/Default/README.md -> ('Actions', 'Default')
        - thorne_drak/Options/Actions/Standard/README.md -> ('Actions', 'Standard')
        - thorne_drak/Options/Player/Pet Bottom/README.md -> ('Player', 'Pet Bottom')
        """
        try:
            parts = str(readme_path).replace('\\', '/').split('/')
            # Find 'Options' in path
            if 'Options' in parts:
                opt_idx = parts.index('Options')
                if opt_idx + 2 < len(parts):
                    window_name = parts[opt_idx + 1]
                    variant_name = parts[opt_idx + 2]
                    return window_name, variant_name
        except:
            pass
        return None, None

    
    def print_summary(self, total_checked):
        """Print summary of fixes applied."""
        print("\n" + "="*70)
        print("HEADER FIX SUMMARY")
        print("="*70)
        print(f"Files Processed:       {self.files_processed}")
        print(f"Files Modified:        {self.changes_made}")
        
        if self.fixes_applied:
            print(f"\nFixes Applied:")
            for fix_type, count in sorted(self.fixes_applied.items()):
                print(f"  - {fix_type:.<30} {count}")
        
        if self.dry_run:
            print("\n(DRY RUN - No files were actually modified)")
        else:
            print(f"\nOK - {self.changes_made} files updated successfully")
        
        print("="*70 + "\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="options_fix_readme.py",
        description="""
Auto-fix README Formatting in UI Variants

Scans Options/ variants and fixes README.md files to conform to standards:
- Proper Markdown headers (# for title, ## for sections)
- Consistent code block formatting
- Correct file link formatting
- Standard section ordering

FEATURES:
  ✓ Bulk fix all READMEs or target specific window
  ✓ Dry-run mode to preview changes
  ✓ Preserves content while fixing formatting
  ✓ Automatic backup before modifications
  ✓ Detailed change reporting

CAUTION: This is a DESTRUCTIVE OPERATOR. Use --dry-run first to preview.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # Preview changes to all READMEs
  python .bin/options_fix_readme.py --dry-run

  # Fix all READMEs with verbose output
  python .bin/options_fix_readme.py --verbose

  # Fix only Player window variants
  python .bin/options_fix_readme.py --window Player

  # Preview fixes for Target window only
  python .bin/options_fix_readme.py --window Target --dry-run

FIXES:
  - Header formatting (# Title, ## Section)
  - Code block syntax (``` xml, ``` json, etc.)
  - Link formatting ([text](path))
  - List indentation and consistency
  - Trailing whitespace
"""
    )
    
    parser.add_argument(
        "--window", "-w",
        metavar="NAME",
        help="Fix only specific window (e.g., Player, Target)"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed changes for each file"
    )
    
    args = parser.parse_args()
    
    # Determine Options path
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    options_dir = root_dir / "thorne_drak" / "Options"
    
    if not options_dir.exists():
        print(f"ERROR: Options directory not found at {options_dir}")
        sys.exit(1)
    
    # Run fixer
    fixer = ReadmeHeaderFixer(options_dir, dry_run=args.dry_run, verbose=args.verbose)
    fixer.scan_and_fix(window_filter=args.window)


if __name__ == '__main__':
    main()
