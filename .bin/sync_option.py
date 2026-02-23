#!/usr/bin/env python3
r"""
Sync Option Script - Copy Option variant files to thorne_dev for testing

This script copies all files (.xml, .tga, etc.) from an Options subdirectory
in thorne_drak to the main thorne_dev directory for in-game testing.

Workflow:
  - Development happens in C:\Thorne-UI\thorne_drak (version controlled)
  - Options variants stored in C:\Thorne-UI\thorne_drak\Options\<Category>\<Variant>\
  - Testing happens in C:\TAKP\uifiles\thorne_dev (deployed test location)
  - This script copies option files to thorne_dev root, overwriting main files

Usage:
    python sync_option.py <option_path>
    
Examples:
    python sync_option.py spellbook/large    # Copy Large Icons spellbook variant
    python sync_option.py inventory          # Show all inventory options (numbered)
    python sync_option.py spellbook          # Show all spellbook options (numbered)

Files Copied:
    - All .xml, .tga, and other UI files from selected option
    - Excludes: .md files (README.md), hidden files, system files
"""

import os
import sys
import shutil

def normalize_path(path_str):
    """Normalize path separators and case for searching"""
    return path_str.lower().replace('\\', '/').strip('/')

def find_matching_options(base_path, search_pattern):
    """Find all Options directories matching the search pattern"""
    if not os.path.isdir(base_path):
        return []
    
    normalized_pattern = normalize_path(search_pattern)
    matches = []
    
    # If pattern contains a slash, it's a specific path like "spellbook/large"
    if '/' in search_pattern:
        parts = [p.strip() for p in search_pattern.split('/')]
        # Try to find exact match first
        target_path = os.path.join(base_path, *parts)
        if os.path.isdir(target_path):
            has_xml = any(f.startswith('EQUI_') and f.endswith('.xml') for f in os.listdir(target_path))
            if has_xml:
                return [os.path.relpath(target_path, base_path)]
        
        # Try case-insensitive match
        current = base_path
        for i, part in enumerate(parts):
            matched = False
            if os.path.isdir(current):
                for item in os.listdir(current):
                    if normalize_path(item).startswith(normalize_path(part)):
                        current = os.path.join(current, item)
                        matched = True
                        break
            if not matched:
                break
        
        if matched and os.path.isdir(current):
            has_xml = any(f.startswith('EQUI_') and f.endswith('.xml') for f in os.listdir(current))
            if has_xml:
                return [os.path.relpath(current, base_path)]
    else:
        # Search for a category like "spellbook"
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path) and normalize_path(item).startswith(normalized_pattern):
                # List all subdirectories in this category
                for subitem in sorted(os.listdir(item_path)):
                    subitem_path = os.path.join(item_path, subitem)
                    if os.path.isdir(subitem_path):
                        rel = os.path.relpath(subitem_path, base_path)
                        has_xml = any(f.startswith('EQUI_') and f.endswith('.xml') for f in os.listdir(subitem_path))
                        if has_xml:
                            matches.append(rel)
    
    return sorted(list(set(matches)))

def sync_option(source_dir, dest_dir, option_path):
    """
    Copy all UI files from a specific option directory to main thorne_dev directory.
    This copies the option's files into thorne_dev root for testing.
    """
    source = os.path.join(source_dir, 'Options', option_path)
    dest = dest_dir  # Copy directly to main thorne_dev directory
    
    if not os.path.isdir(source):
        return False, f"Source directory not found: {source}"
    
    # Ensure destination directory exists
    os.makedirs(dest, exist_ok=True)
    
    # Get all files in source directory (not recursive)
    try:
        copied_files = []
        skipped_files = []
        
        for filename in os.listdir(source):
            source_file = os.path.join(source, filename)
            
            # Skip directories
            if os.path.isdir(source_file):
                continue
            
            # Skip .md files (README.md, etc.)
            if filename.lower().endswith('.md'):
                skipped_files.append(filename)
                continue
            
            # Skip hidden files and system files
            if filename.startswith('.') or filename in ['Thumbs.db', '.DS_Store']:
                continue
            
            # Copy the file
            dest_file = os.path.join(dest, filename)
            shutil.copy2(source_file, dest_file)
            copied_files.append(filename)
        
        if copied_files:
            file_list = ', '.join(copied_files) if len(copied_files) <= 5 else f"{', '.join(copied_files[:5])}, ..."
            return True, f"Copied {len(copied_files)} file(s): {file_list}"
        else:
            if skipped_files:
                return True, f"No files to copy (skipped {len(skipped_files)} .md files)"
            else:
                return True, "No files found in option directory"
                
    except Exception as e:
        return False, f"Error during copy: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: sync_option.py <option_path>")
        print("\nExamples:")
        print("  sync_option.py spellbook/large")
        print("  sync_option.py inventory")
        print("  sync_option.py spellbook")
        sys.exit(1)
    
    search_pattern = sys.argv[1]
    
    # Base paths
    source_base = r"C:\Thorne-UI\thorne_drak"
    dest_base = r"C:\TAKP\uifiles\thorne_dev"
    options_dir = os.path.join(source_base, 'Options')
    
    if not os.path.isdir(options_dir):
        print(f"Error: Options directory not found: {options_dir}")
        sys.exit(1)
    
    # Find matching options
    print(f"\nSearching for options matching '{search_pattern}'...\n")
    matches = find_matching_options(options_dir, search_pattern)
    
    if not matches:
        print(f"No options found matching '{search_pattern}'")
        print("\nAvailable Options:")
        for item in sorted(os.listdir(options_dir)):
            item_path = os.path.join(options_dir, item)
            if os.path.isdir(item_path):
                print(f"  {item}/")
                for subitem in sorted(os.listdir(item_path)):
                    if os.path.isdir(os.path.join(item_path, subitem)):
                        print(f"    - {subitem}")
        sys.exit(1)
    
    if len(matches) == 1:
        selected = matches[0]
    else:
        print("Multiple options found:")
        for i, match in enumerate(matches, 1):
            print(f"  {i}. {match}")
        
        while True:
            try:
                selection = input(f"\nSelect option (1-{len(matches)}): ").strip()
                index = int(selection) - 1
                if 0 <= index < len(matches):
                    selected = matches[index]
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(matches)}")
            except ValueError:
                print(f"Invalid input. Please enter a number between 1 and {len(matches)}")
    
    print(f"\nSyncing: {selected}")
    print(f"From: {os.path.join(source_base, 'Options', selected)}")
    print(f"To:   {dest_base} (main directory)")
    print()
    
    success, message = sync_option(source_base, dest_base, selected)
    
    if success:
        print(f"✓ {message}")
        print("\nReady to test in TAKP")
        print("In-game command: /loadskin thorne_dev")
    else:
        print(f"✗ {message}")
        sys.exit(1)

if __name__ == '__main__':
    main()
