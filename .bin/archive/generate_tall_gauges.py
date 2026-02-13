"""
Generalized Tall Gauge Generator

Generates tall gauge textures (120x64, 15px slices) from standard gauge 
textures (103x32 or 100x32, 8px slices).

Can process:
- Single gauge_pieces01.tga file
- All variants in a directory (e.g., Options/Gauges/)
- Recursively scan for missing tall gauges

Standard layout:  103x32 or 100x32 with 4x 8px slices at Y=0,8,16,24
Tall layout:      120x64 with 4x 15px slices at Y=0,16,31,47

Usage:
    python generate_tall_gauges.py                          # Process default Options/Gauges
    python generate_tall_gauges.py -d path/to/gauges        # Process specific directory
    python generate_tall_gauges.py -f gauge_pieces01.tga    # Process single file
    python generate_tall_gauges.py --recursive              # Scan recursively
    python generate_tall_gauges.py --check                  # Check for missing tall gauges
"""

import argparse
import sys
from PIL import Image
from pathlib import Path

# Target dimensions for tall gauges
TALL_WIDTH = 120
TALL_HEIGHT = 64

# Default base directory (relative to script location)
DEFAULT_GAUGES_DIR = Path(__file__).parent.parent / "thorne_drak" / "Options" / "Gauges"


def generate_tall_gauge_from_file(source_file: Path, force: bool = False, check_only: bool = False) -> bool:
    """
    Generate tall gauge texture from a specific source file.
    
    Args:
        source_file: Path to gauge_pieces01.tga or similar
        force: Overwrite existing tall gauge without prompting
        check_only: Only check if tall gauge is missing, don't generate
        
    Returns:
        True if tall gauge was generated (or would be generated in check mode), False otherwise
    """
    source_file = Path(source_file)
    
    if not source_file.exists():
        if not check_only:
            print(f"❌ Source file not found: {source_file}")
        return False
    
    if not source_file.name.endswith('.tga'):
        if not check_only:
            print(f"⚠️  Skipping non-TGA file: {source_file.name}")
        return False
    
    # Determine target filename (add _tall before extension)
    stem = source_file.stem
    if stem.endswith('_tall'):
        if not check_only:
            print(f"⚠️  Already a tall gauge: {source_file.name}")
        return False
    
    target_file = source_file.parent / f"{stem}_tall.tga"
    
    # Check if tall gauge already exists
    if target_file.exists():
        if check_only:
            print(f"[ OK] Tall gauge exists: {source_file.parent.name}/{target_file.name}")
            return False
        elif not force:
            print(f"⚠️  Target already exists: {target_file.name}")
            response = input("   Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("   Skipped")
                return False
    
    # Check-only mode: report missing tall gauge
    if check_only:
        print(f"[MISS] Missing tall gauge: {source_file.parent.name}/{source_file.name}")
        return True
    
    # Generate tall gauge
    try:
        # Load source image
        img = Image.open(source_file)
        source_width, source_height = img.size
        
        print(f"📏 {source_file.parent.name}/{source_file.name}: {source_width}x{source_height} → {TALL_WIDTH}x{TALL_HEIGHT}")
        
        # Resize to tall format using high-quality LANCZOS resampling
        tall_img = img.resize((TALL_WIDTH, TALL_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save as TGA (preserve original format)
        tall_img.save(target_file, format='TGA')
        
        print(f"✅ Generated: {target_file.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {source_file}: {e}")
        return False


def process_directory(directory: Path, recursive: bool = False, force: bool = False, check_only: bool = False) -> dict:
    """
    Process all gauge_pieces*.tga files in a directory.
    
    Args:
        directory: Directory to scan
        recursive: Scan subdirectories recursively
        force: Overwrite existing tall gauges without prompting
        check_only: Only check for missing tall gauges, don't generate
        
    Returns:
        Dictionary with processing statistics
    """
    directory = Path(directory)
    
    if not directory.is_dir():
        print(f"❌ Directory not found: {directory}")
        return {'processed': 0, 'missing': [], 'total': 0}
    
    results = {'processed': 0, 'missing': [], 'total': 0}
    
    # Pattern to match: gauge_pieces*.tga (but not *_tall.tga)
    if recursive:
        # Recursive scan
        for tga_file in directory.rglob('gauge_pieces*.tga'):
            if '_tall' not in tga_file.stem:
                results['total'] += 1
                success = generate_tall_gauge_from_file(tga_file, force=force, check_only=check_only)
                if success:
                    if check_only:
                        results['missing'].append(str(tga_file))
                    results['processed'] += 1
    else:
        # Non-recursive scan - check immediate subdirectories
        for item in directory.iterdir():
            if item.is_dir():
                # Look for gauge_pieces*.tga in subdirectory
                for tga_file in item.glob('gauge_pieces*.tga'):
                    if '_tall' not in tga_file.stem:
                        results['total'] += 1
                        success = generate_tall_gauge_from_file(tga_file, force=force, check_only=check_only)
                        if success:
                            if check_only:
                                results['missing'].append(str(tga_file))
                            results['processed'] += 1
            elif item.name.startswith('gauge_pieces') and item.suffix == '.tga' and '_tall' not in item.stem:
                # Also check files directly in the directory
                results['total'] += 1
                success = generate_tall_gauge_from_file(item, force=force, check_only=check_only)
                if success:
                    if check_only:
                        results['missing'].append(str(item))
                    results['processed'] += 1
    
    return results


def main():
    """Parse arguments and process gauge files."""
    parser = argparse.ArgumentParser(
        description='Generate tall gauge textures from standard gauge files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                               # Process default Options/Gauges directory
  %(prog)s -d thorne_drak/Options        # Process specific directory
  %(prog)s -f gauge_pieces01.tga         # Process single file
  %(prog)s --recursive                   # Scan recursively for missing tall gauges
  %(prog)s --check                       # Check for missing tall gauges only
  %(prog)s --force                       # Overwrite existing without prompting
        """
    )
    
    # Mutually exclusive group: file, directory, or default
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '-f', '--file',
        type=Path,
        help='Process single gauge file'
    )
    input_group.add_argument(
        '-d', '--directory',
        type=Path,
        help='Process directory (default: thorne_drak/Options/Gauges)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Scan directories recursively'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing tall gauges without prompting'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check for missing tall gauges only (no generation)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 70)
    print("Tall Gauge Generator")
    print("=" * 70)
    print()
    
    # Process based on arguments
    if args.file:
        # Single file mode
        print(f"Processing file: {args.file}")
        print()
        success = generate_tall_gauge_from_file(args.file, force=args.force, check_only=args.check)
        
        print()
        print("=" * 70)
        if args.check:
            print("✅ Check complete" if success else "⚠️  No action needed")
        else:
            print("✅ Success" if success else "❌ Failed")
    
    else:
        # Directory mode
        target_dir = args.directory if args.directory else DEFAULT_GAUGES_DIR
        
        if not target_dir.exists():
            print(f"❌ Directory not found: {target_dir}")
            sys.exit(1)
        
        mode_desc = "recursive" if args.recursive else "non-recursive"
        check_desc = " (check only)" if args.check else ""
        print(f"Scanning directory: {target_dir} ({mode_desc}{check_desc})")
        print()
        
        results = process_directory(target_dir, recursive=args.recursive, force=args.force, check_only=args.check)
        
        # Summary
        print()
        print("=" * 70)
        print("Summary")
        print("=" * 70)
        
        if args.check:
            print(f"Total gauge files scanned: {results['total']}")
            print(f"Missing tall gauges: {results['processed']}")
            if results['missing']:
                print()
                print("Files missing tall gauges:")
                for file in results['missing']:
                    print(f"  - {file}")
        else:
            print(f"Total gauge files found: {results['total']}")
            print(f"✅ Tall gauges generated: {results['processed']}")
            
            if results['processed'] > 0:
                print()
                print("Next steps:")
                print("- Test at least one variant in-game to verify rendering")
                print("- Commit changes with: git add <modified files>")
                print("- Include descriptive commit message")

if __name__ == "__main__":
    main()
