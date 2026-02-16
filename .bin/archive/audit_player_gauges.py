#!/usr/bin/env python3
"""
Audit player window gauge positioning across all variants.
Identifies spacing patterns and alignment issues.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def get_gauges_from_file(file_path):
    """Extract gauge name and Y position from player window XML."""
    try:
        tree = ET.parse(str(file_path))
        root = tree.getroot()
        
        gauges = {}
        for gauge in root.findall(".//Gauge"):
            item_name = gauge.get('item')
            if item_name:
                location = gauge.find("Location")
                if location is not None:
                    y_elem = location.find("Y")
                    if y_elem is not None and y_elem.text:
                        try:
                            gauges[item_name] = int(y_elem.text)
                        except ValueError:
                            pass
        
        return gauges
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return {}

def analyze_file(variant_path):
    """Analyze a player window variant."""
    player_file = variant_path / "EQUI_PlayerWindow.xml"
    if not player_file.exists():
        return None
    
    gauges = get_gauges_from_file(player_file)
    if not gauges:
        return None
    
    # Sort by Y position
    sorted_gauges = sorted(gauges.items(), key=lambda x: x[1])
    
    return {
        'path': variant_path,
        'sorted_gauges': sorted_gauges,
        'gauge_dict': gauges
    }

# Main analysis
main_player = Path("thorne_drak/EQUI_PlayerWindow.xml")
options_base = Path("thorne_drak/Options/Player")

print("="*80)
print("PLAYER WINDOW GAUGE POSITIONING AUDIT")
print("="*80)

# Analyze main window
print("\n[MAIN] thorne_drak/EQUI_PlayerWindow.xml")
print("-" * 80)
main_data = analyze_file(Path("thorne_drak"))
if main_data:
    print("Gauge Positions (sorted by Y):")
    for gauge_name, y_pos in main_data['sorted_gauges']:
        print(f"  {gauge_name:30} Y={y_pos:3}")
    
    # Calculate spacing
    print("\nSpacing Pattern:")
    for i in range(len(main_data['sorted_gauges']) - 1):
        name1, y1 = main_data['sorted_gauges'][i]
        name2, y2 = main_data['sorted_gauges'][i + 1]
        spacing = y2 - y1
        print(f"  {name1:30} (Y={y1:3}) → {name2:30} (Y={y2:3}) = +{spacing}px")

# Analyze options
print("\n\n" + "="*80)
print("PLAYER WINDOW OPTIONS")
print("="*80)

variants = sorted([d for d in options_base.iterdir() if d.is_dir()])
for variant in variants:
    variant_data = analyze_file(variant)
    if variant_data:
        print(f"\n[OPTION] {variant.name}")
        print("-" * 80)
        print("Gauge Positions (sorted by Y):")
        for gauge_name, y_pos in variant_data['sorted_gauges']:
            print(f"  {gauge_name:30} Y={y_pos:3}")

print("\n\n" + "="*80)
print("RECOMMENDATIONS")
print("="*80)
print("""
1. Compare spacing patterns between main and each option
2. Identify which options use tall gauges (120x64) vs standard
3. Determine if stamina Y position needs adjustment (currently checking)
4. Align all tall gauge options to use consistent spacing from main window
5. Document the official spacing pattern for future variants
""")
