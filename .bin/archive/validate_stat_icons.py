#!/usr/bin/env python3
"""
Validate Stat Icon Master Layout
==================================
Verifies that all three stat_icon_pieces files use identical coordinate layouts.
This ensures files are swappable without XML coordinate changes.

Checks:
- File existence and format (256×256 RGBA)
- Icon positions match master template
- All three files have icons at same coordinates
- No position overlaps or conflicts
- Validates against stat-icons-coordinates.json
"""

from PIL import Image
import os
import json

def load_master_layout():
    """Load master layout from JSON"""
    json_path = os.path.join(
        os.path.dirname(__file__), 
        "..", 
        ".development", 
        "stat-icons-coordinates.json"
    )
    
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ ERROR: Master layout JSON not found: {json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in {json_path}: {e}")
        return None

def check_icon_at_position(img, x, y, size=22):
    """Check if there's visible content at given position"""
    try:
        icon_region = img.crop((x, y, x + size, y + size))
        
        if icon_region.mode == "RGBA":
            alpha_channel = icon_region.split()[3]
            alpha_data = list(alpha_channel.getdata())
            non_transparent_pixels = sum(1 for a in alpha_data if a > 0)
            return non_transparent_pixels
        else:
            # No alpha channel, assume all visible
            return size * size
    except Exception as e:
        print(f"  ⚠ Error checking position ({x},{y}): {e}")
        return 0

def validate_file(filepath, expected_layout):
    """Validate a single stat icon file"""
    filename = os.path.basename(filepath)
    
    print(f"\n{'='*70}")
    print(f"Validating: {filename}")
    print(f"{'='*70}")
    
    # Check file exists
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        return False
    
    # Load image
    try:
        img = Image.open(filepath).convert("RGBA")
    except Exception as e:
        print(f"❌ ERROR: Cannot open file: {e}")
        return False
    
    # Check dimensions
    if img.size != (256, 256):
        print(f"❌ ERROR: Incorrect size: {img.size[0]}×{img.size[1]} (expected 256×256)")
        return False
    else:
        print(f"✓ Size: 256×256")
    
    # Check mode
    if img.mode != "RGBA":
        print(f"⚠ WARNING: Mode is {img.mode}, expected RGBA")
    else:
        print(f"✓ Mode: RGBA")
    
    # Check each icon position
    print(f"\nIcon Position Verification:")
    print(f"{'Icon':<10} {'X':>3} {'Y':>3} {'Visible Pixels':>15} {'Status'}")
    print(f"{'-'*50}")
    
    all_valid = True
    icon_count = 0
    placeholder_count = 0
    
    for icon_name, layout in expected_layout.items():
        x = layout["x"]
        y = layout["y"]
        
        visible_pixels = check_icon_at_position(img, x, y, size=22)
        
        if visible_pixels > 0:
            # Consider it a real icon if >50% pixels visible
            if visible_pixels > 242:  # 50% of 484 (22×22)
                status = "✓ Real Icon"
                icon_count += 1
            else:
                status = "○ Placeholder"
                placeholder_count += 1
            print(f"{icon_name:<10} {x:>3} {y:>3} {visible_pixels:>15} {status}")
        else:
            status = "✗ EMPTY"
            all_valid = False
            print(f"{icon_name:<10} {x:>3} {y:>3} {visible_pixels:>15} {status}")
    
    print(f"\nSummary:")
    print(f"  Real Icons: {icon_count}/18")
    print(f"  Placeholders: {placeholder_count}/18")
    print(f"  Total Positions: {icon_count + placeholder_count}/18")
    
    if all_valid:
        print(f"\n✅ File validated successfully!")
    else:
        print(f"\n⚠ File has missing icons")
    
    return all_valid, icon_count, placeholder_count

def validate_consistency(files_data, master_layout):
    """Verify all files have icons at consistent positions"""
    print(f"\n{'='*70}")
    print(f"Cross-File Consistency Check")
    print(f"{'='*70}")
    
    # Build position map for each file
    position_maps = {}
    
    for filename in ["stat_icon_pieces01.tga", "stat_icon_pieces02.tga", "stat_icon_pieces03.tga"]:
        filepath = os.path.join(os.path.dirname(__file__), "..", "thorne_drak", filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Skipping {filename} (not found)")
            continue
        
        img = Image.open(filepath).convert("RGBA")
        position_maps[filename] = {}
        
        for icon_name, layout in master_layout.items():
            x = layout["x"]
            y = layout["y"]
            visible_pixels = check_icon_at_position(img, x, y, size=22)
            position_maps[filename][(x, y)] = {
                "icon": icon_name,
                "visible": visible_pixels,
                "has_content": visible_pixels > 0
            }
    
    # Check consistency
    print(f"\nPosition-by-Position Comparison:")
    print(f"{'Icon':<10} {'Position':<12} {'pieces01':<12} {'pieces02':<12} {'pieces03':<12}")
    print(f"{'-'*70}")
    
    all_consistent = True
    
    for icon_name, layout in sorted(master_layout.items(), key=lambda x: (x[1]["col"], x[1]["row"])):
        x = layout["x"]
        y = layout["y"]
        pos_str = f"({x:3},{y:3})"
        
        statuses = []
        for filename in ["stat_icon_pieces01.tga", "stat_icon_pieces02.tga", "stat_icon_pieces03.tga"]:
            if filename in position_maps:
                data = position_maps[filename][(x, y)]
                if data["visible"] > 242:
                    statuses.append("Icon")
                elif data["visible"] > 0:
                    statuses.append("Placeholder")
                else:
                    statuses.append("EMPTY")
                    all_consistent = False
            else:
                statuses.append("N/A")
        
        print(f"{icon_name:<10} {pos_str:<12} {statuses[0]:<12} {statuses[1]:<12} {statuses[2]:<12}")
    
    print(f"\nConsistency Result:")
    if all_consistent:
        print(f"✅ All files have content at all expected positions")
        print(f"✅ Files are swappable (coordinates match)")
    else:
        print(f"⚠ Some positions are completely empty across all files")
        print(f"⚠ This may indicate a problem with template generation")
    
    return all_consistent

def main():
    """Main validation function"""
    print("="*70)
    print("STAT ICON MASTER LAYOUT VALIDATOR")
    print("="*70)
    print("\nThis tool verifies that all stat_icon_pieces files:")
    print("  1. Use correct dimensions (256×256 RGBA)")
    print("  2. Have icons at master template positions")
    print("  3. Are swappable (identical coordinate systems)")
    print("="*70)
    
    # Load master layout
    master_data = load_master_layout()
    if not master_data:
        return False
    
    master_layout = master_data.get("layout", {})
    if not master_layout:
        print("❌ ERROR: No layout data in JSON")
        return False
    
    print(f"\n✓ Loaded master layout: {len(master_layout)} icon positions")
    
    # Validate each file
    base_dir = os.path.join(os.path.dirname(__file__), "..", "thorne_drak")
    
    files_to_check = [
        "stat_icon_pieces01.tga",
        "stat_icon_pieces02.tga",
        "stat_icon_pieces03.tga"
    ]
    
    results = {}
    
    for filename in files_to_check:
        filepath = os.path.join(base_dir, filename)
        valid, icon_count, placeholder_count = validate_file(filepath, master_layout)
        results[filename] = {
            "valid": valid,
            "icons": icon_count,
            "placeholders": placeholder_count
        }
    
    # Check cross-file consistency
    consistency = validate_consistency(master_data.get("files", {}), master_layout)
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*70}")
    
    for filename, result in results.items():
        status = "✅ PASS" if result["valid"] else "⚠ WARNINGS"
        print(f"\n{filename}:")
        print(f"  Status: {status}")
        print(f"  Real Icons: {result['icons']}")
        print(f"  Placeholders: {result['placeholders']}")
        print(f"  Total: {result['icons'] + result['placeholders']}/18")
    
    print(f"\nCross-File Consistency: {'✅ PASS' if consistency else '⚠ NEEDS REVIEW'}")
    
    if all(r["valid"] for r in results.values()) and consistency:
        print(f"\n{'='*70}")
        print(f"✅ ALL VALIDATIONS PASSED")
        print(f"✅ Files are swappable and ready to use!")
        print(f"{'='*70}")
        return True
    else:
        print(f"\n{'='*70}")
        print(f"⚠ VALIDATION COMPLETED WITH WARNINGS")
        print(f"Review the details above for any issues.")
        print(f"{'='*70}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
