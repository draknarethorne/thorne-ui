#!/usr/bin/env python3
"""
Generalized TGA File Converter - PNG to TGA Format

Converts mislabeled PNG files (with .tga extension) to proper TGA format.
Can process individual files or scan directories recursively.
"""

from PIL import Image
import os
import sys
import argparse
from pathlib import Path


def is_png_file(file_path):
    """Check if a .tga file is actually PNG format"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            # PNG signature: 89 50 4E 47 0D 0A 1A 0A
            return header.startswith(b'\x89PNG\r\n\x1a\n')
    except Exception:
        return False


def convert_to_tga(file_path, check_only=False):
    """Convert PNG file (mislabeled as .tga) to proper TGA format or just check"""
    if not os.path.exists(file_path):
        if not check_only:
            print(f"[ERROR] File not found: {file_path}")
        return False
    
    if not file_path.endswith('.tga'):
        if not check_only:
            print(f"[SKIP] Non-.tga file: {file_path}")
        return False
    
    is_png = is_png_file(file_path)
    
    # Check-only mode: just report status
    if check_only:
        if is_png:
            print(f"[BAD] PNG mislabeled as TGA: {file_path}")
            return True
        else:
            print(f"[ OK] Valid TGA: {file_path}")
            return False
    
    # Fix mode: only process PNG files
    if not is_png:
        # Already a valid TGA, nothing to do
        return False
    
    # Convert PNG to TGA
    try:
        # Open the PNG data (even though it has .tga extension)
        img = Image.open(file_path)
        
        # Convert to RGBA if needed (TGA supports RGBA)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Save as proper TGA format
        img.save(file_path, format='TGA')
        
        print(f"[FIXED] Successfully converted: {file_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Conversion failed for {file_path}: {e}")
        return False


def process_directory(directory, recursive=False, check_only=False):
    """Process all .tga files in a directory"""
    if not os.path.isdir(directory):
        if not check_only:
            print(f"[ERROR] Directory not found: {directory}")
        return {'fixed': 0, 'bad': [], 'total': 0}
    
    results = {'fixed': 0, 'bad': [], 'total': 0}
    
    if recursive:
        # Recursive scan
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.tga'):
                    file_path = os.path.join(root, file)
                    results['total'] += 1
                    needs_fix = convert_to_tga(file_path, check_only=check_only)
                    if needs_fix:
                        if check_only:
                            results['bad'].append(file_path)
                        results['fixed'] += 1
    else:
        # Non-recursive scan
        for file in os.listdir(directory):
            if file.endswith('.tga'):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    results['total'] += 1
                    needs_fix = convert_to_tga(file_path, check_only=check_only)
                    if needs_fix:
                        if check_only:
                            results['bad'].append(file_path)
                        results['fixed'] += 1
    
    return results


def main():
    parser = argparse.ArgumentParser(
        prog='fix_tga_files',
        description='Convert mislabeled PNG files (with .tga extension) to proper TGA format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix a single file
  python fix_tga_files.py gauge_inlay_thorne01.tga
  
  # Fix all .tga files in a directory (non-recursive)
  python fix_tga_files.py ./thorne_drak/Options/Gauges
  
  # Recursively scan and fix all .tga files from current directory
  python fix_tga_files.py --scan .
  
  # Check which files need fixing without converting
  python fix_tga_files.py --check gauge_inlay_thorne01.tga
  
  # Check all files that need fixing recursively
  python fix_tga_files.py --check --scan .
        """
    )
    
    parser.add_argument(
        'targets',
        nargs='*',
        metavar='PATH',
        help='File or directory to process (can specify multiple)'
    )
    
    parser.add_argument(
        '--scan',
        action='store_true',
        help='Recursively scan directory instead of processing single file/directory'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check mode: only list files that need fixing, do not convert'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.targets and not args.scan:
        parser.print_help()
        return
    
    if args.scan and not args.targets:
        print("[ERROR] --scan requires at least one directory target")
        return
    
    print("=" * 70)
    print("TGA File Converter - PNG to TGA Format")
    print("=" * 70)
    
    mode_label = "(CHECK MODE)" if args.check else "(FIX MODE)"
    print(f"\n{mode_label}\n")
    
    total_results = {'fixed': 0, 'bad': [], 'total': 0}
    
    if args.scan:
        # Recursive scan mode
        for target in args.targets:
            print(f"Scanning directory recursively: {target}\n")
            results = process_directory(target, recursive=True, check_only=args.check)
            total_results['fixed'] += results['fixed']
            total_results['bad'].extend(results['bad'])
            total_results['total'] += results['total']
    else:
        # File/directory processing mode
        for target in args.targets:
            if os.path.isfile(target):
                if not args.check:
                    print(f"Processing file: {target}")
                total_results['total'] += 1
                needs_fix = convert_to_tga(target, check_only=args.check)
                if needs_fix and args.check:
                    total_results['bad'].append(target)
                total_results['fixed'] += 1 if needs_fix else 0
            elif os.path.isdir(target):
                if not args.check:
                    print(f"Processing directory: {target}")
                results = process_directory(target, recursive=False, check_only=args.check)
                total_results['fixed'] += results['fixed']
                total_results['bad'].extend(results['bad'])
                total_results['total'] += results['total']
            else:
                if not args.check:
                    print(f"[ERROR] Path not found: {target}")
    
    print("\n" + "=" * 70)
    
    if args.check:
        total_count = total_results['fixed']
        total_files = total_results['total']
        print(f"Check complete: {total_count} files need fixing out of {total_files} total .tga files\n")
        
        if total_results['bad']:
            print("Files that need conversion (PNG mislabeled as TGA):")
            print("-" * 70)
            for bad_file in sorted(total_results['bad']):
                print(f"  {bad_file}")
    else:
        total_files = total_results['total']
        print(f"Conversion complete: {total_results['fixed']} files fixed out of {total_files} processed")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
