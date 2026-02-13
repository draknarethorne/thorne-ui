#!/usr/bin/env python3
"""
Audit player window label positions across all variants.
Ensures consistent spacing and vertical alignment.
"""

import xml.etree.ElementTree as ET

# Path to player window files
MAIN_WINDOW = r"C:\Thorne-UI\thorne_drak\EQUI_PlayerWindow.xml"
OPTION_DIRS = {
    "Default": r"C:\Thorne-UI\thorne_drak\Options\Player\Default\EQUI_PlayerWindow.xml",
    "Standard": r"C:\Thorne-UI\thorne_drak\Options\Player\Standard\EQUI_PlayerWindow.xml",
    "Pet Bottom": r"C:\Thorne-UI\thorne_drak\Options\Player\Pet Bottom\EQUI_PlayerWindow.xml",
    "AA and XP Bottom": r"C:\Thorne-UI\thorne_drak\Options\Player\AA and XP Bottom\EQUI_PlayerWindow.xml",
}

def get_label_positions(xml_file):
    """Extract all label Y positions from XML file."""
    labels = {}
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all Label elements
        for label in root.findall(".//Label"):
            item = label.get("item")
            if item and item.startswith("PW_"):
                # Look for Location/Y
                location = label.find("Location")
                if location is not None:
                    y_elem = location.find("Y")
                    if y_elem is not None and y_elem.text is not None:
                        try:
                            y_pos = int(y_elem.text)
                            labels[item] = y_pos
                        except ValueError:
                            pass
        
        return labels
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return {}

def main():
    print("=" * 80)
    print("PLAYER WINDOW LABEL POSITION AUDIT")
    print("=" * 80)
    
    # Get main window labels
    main_labels = get_label_positions(MAIN_WINDOW)
    print("\n[MAIN WINDOW] Label Y Positions:")
    print("-" * 80)
    for item in sorted(main_labels.keys()):
        print(f"  {item:<30} Y={main_labels[item]:3d}")
    
    # Check options
    print("\n\n[OPTIONS VARIANTS] Consistency Check:")
    print("-" * 80)
    
    all_consistent = True
    for option_name, option_path in sorted(OPTION_DIRS.items()):
        option_labels = get_label_positions(option_path)
        
        # Compare with main
        mismatches = []
        for item, y_pos in main_labels.items():
            if item in option_labels:
                if option_labels[item] != y_pos:
                    mismatches.append(f"    {item}: Main={y_pos}, {option_name}={option_labels[item]}")
            else:
                mismatches.append(f"    {item}: MISSING in {option_name}")
        
        # Check for extra labels in option
        for item in option_labels:
            if item not in main_labels:
                mismatches.append(f"    {item}: Extra in {option_name} (Y={option_labels[item]})")
        
        if mismatches:
            print(f"\n  [{option_name}] MISMATCHES FOUND:")
            for mismatch in mismatches:
                print(mismatch)
            all_consistent = False
        else:
            print(f"  [{option_name}] ✓ All labels match main window")
    
    # Summary
    print("\n" + "=" * 80)
    if all_consistent:
        print("[OK] All label positions are consistent across all variants!")
    else:
        print("[WARN] Label position inconsistencies detected - see above")
    print("=" * 80)

if __name__ == "__main__":
    main()
