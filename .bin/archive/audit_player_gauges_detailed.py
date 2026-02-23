#!/usr/bin/env python3
"""
Enhanced audit: Check gauge positioning AND sizes.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def get_gauge_details(file_path):
    """Extract gauge name, Y position, and CY size."""
    try:
        tree = ET.parse(str(file_path))
        root = tree.getroot()
        
        gauges = {}
        for gauge in root.findall(".//Gauge"):
            item_name = gauge.get('item')
            if item_name and 'Gauge' in item_name:
                location = gauge.find("Location")
                size = gauge.find("Size")
                cy = None
                y = None
                
                if location is not None:
                    y_elem = location.find("Y")
                    if y_elem is not None and y_elem.text:
                        try:
                            y = int(y_elem.text)
                        except ValueError:
                            pass
                
                if size is not None:
                    cy_elem = size.find("CY")
                    if cy_elem is not None and cy_elem.text:
                        try:
                            cy = int(cy_elem.text)
                        except ValueError:
                            pass
                
                if y is not None and cy is not None:
                    gauges[item_name] = {'y': y, 'cy': cy}
        
        return gauges
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return {}

# Main analysis
print("="*100)
print("PLAYER WINDOW GAUGE POSITIONING & SIZING AUDIT")
print("="*100)

# Analyze main window
print("\n[MAIN] thorne_drak/EQUI_PlayerWindow.xml")
print("-" * 100)
main_gauges = get_gauge_details(Path("thorne_drak/EQUI_PlayerWindow.xml"))
if main_gauges:
    print("Gauge Details (sorted by Y):")
    print(f"{'Gauge Name':<30} {'Y':<5} {'CY':<5} {'Type':<15}")
    print("-" * 100)
    for name, y_pos in sorted(main_gauges.items(), key=lambda x: x[1]['y']):
        cy = main_gauges[name]['cy']
        gauge_type = "Tall (16px)" if cy == 16 else f"Wide/Other ({cy}px)"
        print(f"{name:<30} {main_gauges[name]['y']:<5} {cy:<5} {gauge_type:<15}")

# Analyze options
options_base = Path("thorne_drak/Options/Player")
print("\n\n" + "="*100)
print("PLAYER WINDOW OPTIONS")
print("="*100)

variants = sorted([d for d in options_base.iterdir() if d.is_dir()])
for variant in variants:
    player_file = variant / "EQUI_PlayerWindow.xml"
    if player_file.exists():
        gauges = get_gauge_details(player_file)
        if gauges:
            print(f"\n[OPTION] {variant.name}")
            print("-" * 100)
            print(f"{'Gauge Name':<30} {'Y':<5} {'CY':<5} {'Type':<15}")
            print("-" * 100)
            for name, y_pos in sorted(gauges.items(), key=lambda x: x[1]['y']):
                cy = gauges[name]['cy']
                gauge_type = "Tall (16px)" if cy == 16 else f"Wide/Other ({cy}px)"
                print(f"{name:<30} {gauges[name]['y']:<5} {cy:<5} {gauge_type:<15}")

print("\n\n" + "="*100)
print("FINDINGS")
print("="*100)
print("""
Tall gauges (CY=16):
- Use gauge_pieces01_tall.tga (120×64)
- Typically HP, Mana, XP, AA (AAIcon), Pet HP

Wide gauges (CY=8):
- Use gauge_pieces01_wide.tga (120×32)
- Typically Stamina

ACTION ITEMS:
1. Identify which variants have tall gauges that need Y adjustment
2. Move Stamina Y from 63 to 64 (and adjust elements below accordingly)
3. Ensure all other gauges remain consistently spaced
4. Test alignment across all variants
""")
