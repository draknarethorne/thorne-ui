#!/usr/bin/env python3
"""
extract_gemicon_coordinates.py - Analyze and document gemicon coordinates from EverQuest UI files

This tool searches through multiple UI variant directories and extracts all Ui2DAnimation
definitions that reference gemicons01.tga, gemicons02.tga, and gemicons03.tga files.

It documents icon coordinates, sizes, and locations across different UI variants.

MASTER LAYOUT INTEGRATION:
--------------------------
When extracting resist icons from gemicons01.tga, they should be placed at these 
positions in the stat_icon_pieces master layout (256×256 RGBA):

  Fire:    Column 2, Row 1 → (90, 10)   22×22
  Cold:    Column 2, Row 2 → (90, 40)   22×22
  Magic:   Column 2, Row 3 → (90, 70)   22×22
  Poison:  Column 2, Row 4 → (90, 100)  22×22
  Disease: Column 2, Row 5 → (90, 130)  22×22

EXTRACTION EXAMPLE:
------------------
If extracting from vert-blue/gemicons01.tga:
  Source Fire icon at (48, 120) 24×24 → Resize to 22×22 → Place at (90, 10)
  Source Cold icon at (168, 120) 24×24 → Resize to 22×22 → Place at (90, 40)
  ... etc.

All other positions (13 slots) get dark placeholder boxes.
See generate_master_stat_icons.py for the complete implementation.

Usage:
    python .bin/extract_gemicon_coordinates.py
    
Outputs:
    - Console output with discovered icons
    - .docs/GEMICON-COORDINATES.json - Comprehensive JSON mapping
    - .docs/GEMICON-REFERENCE.md - Human-readable reference guide
"""

import os
import re
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from collections import defaultdict


# Master Layout Constants (from generate_master_stat_icons.py)
# These coordinates define where icons should be placed in stat_icon_pieces files
MASTER_LAYOUT_RESIST_POSITIONS = {
    "Fire":     {"x": 90, "y": 10,  "col": 2, "row": 1},
    "Cold":     {"x": 90, "y": 40,  "col": 2, "row": 2},
    "Magic":    {"x": 90, "y": 70,  "col": 2, "row": 3},
    "Poison":   {"x": 90, "y": 100, "col": 2, "row": 4},
    "Disease":  {"x": 90, "y": 130, "col": 2, "row": 5},
}

# UI variant directories to search
SEARCH_DIRS = [
    'default',
    'vert',
    'vert-blue', 
    'duxaUI',
    'QQ',
    'thorne_drak'
]

# XML files to analyze
TARGET_FILES = [
    'EQUI_Animations.xml',
    'EQUI_PlayerWindow.xml',
    'EQUI_HotButtonWnd.xml',
    'EQUI_Inventory.xml',
    'EQUI_BuffWindow.xml',
    'EQUI_CastSpellWnd.xml',
    'EQUI_TargetWindow.xml'
]

# Gemicon texture files to search for
GEMICON_FILES = ['gemicons01.tga', 'gemicons02.tga', 'gemicons03.tga']


class GemiconExtractor:
    """Extract and document gemicon coordinates from EQ UI XML files"""
    
    def __init__(self, workspace_root):
        self.workspace_root = Path(workspace_root)
        self.gemicon_data = defaultdict(lambda: defaultdict(list))
        self.all_icons = []
        
    def extract_coordinates_from_animation(self, animation_elem, item_name, file_path, variant):
        """Extract coordinates from a single Ui2DAnimation element"""
        try:
            # Check if this animation uses Grid (sprite sheet)
            grid_elem = animation_elem.find('Grid')
            is_grid = grid_elem is not None and grid_elem.text.lower() == 'true'
            
            cell_width = None
            cell_height = None
            
            if is_grid:
                cw_elem = animation_elem.find('CellWidth')
                ch_elem = animation_elem.find('CellHeight')
                if cw_elem is not None:
                    cell_width = int(cw_elem.text)
                if ch_elem is not None:
                    cell_height = int(ch_elem.text)
            
            # Process each frame
            for frame in animation_elem.findall('Frames'):
                texture_elem = frame.find('Texture')
                if texture_elem is None:
                    continue
                    
                texture = texture_elem.text
                
                # Check if this frame uses a gemicon file
                if texture not in GEMICON_FILES:
                    continue
                
                # Extract location coordinates
                location = frame.find('Location')
                size = frame.find('Size')
                
                if location is None or size is None:
                    continue
                
                x_elem = location.find('X')
                y_elem = location.find('Y')
                cx_elem = size.find('CX')
                cy_elem = size.find('CY')
                
                if x_elem is None or y_elem is None or cx_elem is None or cy_elem is None:
                    continue
                
                x = int(x_elem.text)
                y = int(y_elem.text)
                cx = int(cx_elem.text)
                cy = int(cy_elem.text)
                
                icon_info = {
                    'name': item_name,
                    'texture': texture,
                    'x': x,
                    'y': y,
                    'width': cx,
                    'height': cy,
                    'file': str(file_path.relative_to(self.workspace_root)),
                    'variant': variant,
                    'is_grid': is_grid,
                    'cell_width': cell_width,
                    'cell_height': cell_height
                }
                
                self.all_icons.append(icon_info)
                self.gemicon_data[texture][item_name].append(icon_info)
                
                print(f"  + {item_name:30} - {texture:20} ({x:3},{y:3}) {cx}x{cy}")
                if is_grid:
                    print(f"    Grid: {cell_width}x{cell_height} cells")
                
        except Exception as e:
            print(f"    Warning: Error parsing {item_name}: {e}")
    
    def search_xml_file(self, file_path, variant):
        """Search a single XML file for gemicon references"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find all Ui2DAnimation elements
            animations = root.findall('.//Ui2DAnimation')
            
            if not animations:
                return 0
            
            count = 0
            for anim in animations:
                item_attr = anim.get('item')
                if not item_attr:
                    continue
                
                # Check if any frame uses gemicons
                has_gemicon = False
                for frame in anim.findall('Frames'):
                    texture = frame.find('Texture')
                    if texture is not None and texture.text in GEMICON_FILES:
                        has_gemicon = True
                        break
                
                if has_gemicon:
                    self.extract_coordinates_from_animation(anim, item_attr, file_path, variant)
                    count += 1
            
            return count
            
        except ET.ParseError as e:
            print(f"    XML Parse Error: {e}")
            return 0
        except Exception as e:
            print(f"    Error: {e}")
            return 0
    
    def scan_directories(self):
        """Scan all configured directories for gemicon usage"""
        print("\n" + "="*80)
        print("GEMICON COORDINATE EXTRACTOR")
        print("="*80)
        
        total_icons = 0
        
        for variant_dir in SEARCH_DIRS:
            variant_path = self.workspace_root / variant_dir
            
            if not variant_path.exists():
                print(f"\n[{variant_dir}] - Directory not found, skipping")
                continue
            
            print(f"\n[{variant_dir}]")
            variant_found = False
            
            for xml_file in TARGET_FILES:
                file_path = variant_path / xml_file
                
                if not file_path.exists():
                    continue
                
                print(f"\n  Analyzing: {xml_file}")
                count = self.search_xml_file(file_path, variant_dir)
                
                if count > 0:
                    variant_found = True
                    total_icons += count
                    print(f"  Found {count} gemicon animation(s)")
            
            if not variant_found:
                print(f"  No gemicon references found")
        
        print("\n" + "="*80)
        print(f"TOTAL: Found {total_icons} gemicon animation definitions across {len(self.all_icons)} frames")
        print("="*80)
        
        return total_icons
    
    def generate_json_output(self, output_path):
        """Generate comprehensive JSON documentation"""
        output_data = {
            'description': 'Gemicon coordinate mappings extracted from EverQuest UI files',
            'generated_by': 'extract_gemicon_coordinates.py',
            'textures': {}
        }
        
        for texture_name in sorted(self.gemicon_data.keys()):
            texture_animations = self.gemicon_data[texture_name]
            
            output_data['textures'][texture_name] = {
                'description': f'Icons from {texture_name}',
                'dimensions': '256x256',
                'animations': {}
            }
            
            for anim_name in sorted(texture_animations.keys()):
                frames = texture_animations[anim_name]
                
                # Collect unique variants
                variants_used = list(set(f['variant'] for f in frames))
                
                output_data['textures'][texture_name]['animations'][anim_name] = {
                    'variants': variants_used,
                    'frames': [
                        {
                            'variant': f['variant'],
                            'file': f['file'],
                            'x': f['x'],
                            'y': f['y'],
                            'width': f['width'],
                            'height': f['height'],
                            'is_grid': f['is_grid'],
                            'cell_width': f['cell_width'],
                            'cell_height': f['cell_height']
                        }
                        for f in frames
                    ]
                }
        
        # Also include a flat list of all icons for easy reference
        output_data['all_icons'] = sorted(self.all_icons, key=lambda x: (x['texture'], x['name'], x['variant']))
        
        # Write JSON file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            print(f"\n[OK] Generated: {output_path}")
            print(f"  Contains {len(output_data['all_icons'])} icon frame definitions")
            return True
        except Exception as e:
            print(f"\n[ERROR] Error writing JSON: {e}")
            return False
    
    def generate_markdown_output(self, output_path):
        """Generate human-readable markdown reference"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Gemicon Coordinate Reference\n\n")
                f.write("This document provides a comprehensive reference of all gemicon coordinates\n")
                f.write("discovered in EverQuest UI variant directories.\n\n")
                f.write("**Auto-generated by:** `extract_gemicon_coordinates.py`\n\n")
                f.write("---\n\n")
                
                # Table of contents
                f.write("## Table of Contents\n\n")
                for texture in sorted(self.gemicon_data.keys()):
                    anchor = texture.replace('.', '-')
                    f.write(f"- [{texture}](#{anchor})\n")
                f.write("\n---\n\n")
                
                # Details for each texture file
                for texture_name in sorted(self.gemicon_data.keys()):
                    f.write(f"## {texture_name}\n\n")
                    
                    texture_animations = self.gemicon_data[texture_name]
                    f.write(f"**Total animations:** {len(texture_animations)}\n\n")
                    
                    for anim_name in sorted(texture_animations.keys()):
                        frames = texture_animations[anim_name]
                        variants = sorted(set(frame['variant'] for frame in frames))
                        
                        f.write(f"### `{anim_name}`\n\n")
                        f.write(f"**Used in variants:** {', '.join(variants)}\n\n")
                        
                        # Check if it's a grid animation
                        if frames[0]['is_grid']:
                            f.write(f"**Grid Animation:** {frames[0]['cell_width']}×{frames[0]['cell_height']} cells\n\n")
                        
                        # Create table
                        f.write("| Variant | File | X | Y | Width | Height |\n")
                        f.write("|---------|------|--:|--:|------:|-------:|\n")
                        
                        for frame in frames:
                            f.write(f"| {frame['variant']} | {os.path.basename(frame['file'])} | ")
                            f.write(f"{frame['x']} | {frame['y']} | ")
                            f.write(f"{frame['width']} | {frame['height']} |\n")
                        
                        f.write("\n")
                        
                        # Example XML usage
                        sample_frame = frames[0]
                        f.write("**Example XML:**\n\n")
                        f.write("```xml\n")
                        f.write(f'<Ui2DAnimation item="{anim_name}">\n')
                        if sample_frame['is_grid']:
                            f.write(f"  <Grid>true</Grid>\n")
                            f.write(f"  <CellWidth>{sample_frame['cell_width']}</CellWidth>\n")
                            f.write(f"  <CellHeight>{sample_frame['cell_height']}</CellHeight>\n")
                        f.write("  <Frames>\n")
                        f.write(f"    <Texture>{texture_name}</Texture>\n")
                        f.write("    <Location>\n")
                        f.write(f"      <X>{sample_frame['x']}</X>\n")
                        f.write(f"      <Y>{sample_frame['y']}</Y>\n")
                        f.write("    </Location>\n")
                        f.write("    <Size>\n")
                        f.write(f"      <CX>{sample_frame['width']}</CX>\n")
                        f.write(f"      <CY>{sample_frame['height']}</CY>\n")
                        f.write("    </Size>\n")
                        f.write("  </Frames>\n")
                        f.write("</Ui2DAnimation>\n")
                        f.write("```\n\n")
                    
                    f.write("---\n\n")
                
                # Summary section
                f.write("## Summary\n\n")
                f.write(f"**Total gemicon textures found:** {len(self.gemicon_data)}\n\n")
                
                for texture in sorted(self.gemicon_data.keys()):
                    count = len(self.gemicon_data[texture])
                    f.write(f"- `{texture}`: {count} animation(s)\n")
                
                f.write("\n")
            
            print(f"[OK] Generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error writing markdown: {e}")
            return False
    
    def generate_summary(self):
        """Print summary of findings"""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        print(f"\n📊 Gemicon Files Found:")
        for texture in sorted(self.gemicon_data.keys()):
            print(f"\n  {texture}:")
            print(f"    Animations: {len(self.gemicon_data[texture])}")
            
            # Show unique variants using this texture
            variants = set()
            for anim_frames in self.gemicon_data[texture].values():
                for frame in anim_frames:
                    variants.add(frame['variant'])
            
            print(f"    Variants: {', '.join(sorted(variants))}")
            
            # List animations
            print(f"    Animation names:")
            for anim_name in sorted(self.gemicon_data[texture].keys()):
                frames = self.gemicon_data[texture][anim_name]
                if frames[0]['is_grid']:
                    print(f"      - {anim_name} (Grid: {frames[0]['cell_width']}x{frames[0]['cell_height']})")
                else:
                    print(f"      - {anim_name}")
        
        print("\n" + "="*80)
    
    def show_master_layout_mapping(self):
        """Show how extracted resist icons map to master layout positions"""
        print("\n" + "="*80)
        print("MASTER LAYOUT MAPPING FOR RESIST ICONS")
        print("="*80)
        print("\nIf extracting resist icons for stat_icon_pieces files:")
        print("Extract from gemicons01.tga and place at these master positions:\n")
        
        print("  Icon Name │ Master Position │ Size  │ Column │ Row")
        print("  ──────────┼─────────────────┼───────┼────────┼────")
        for icon_name, pos in MASTER_LAYOUT_RESIST_POSITIONS.items():
            print(f"  {icon_name:9} │ ({pos['x']:3}, {pos['y']:3})      │ 22×22 │ Col {pos['col']}  │ {pos['row']}")
        
        print("\nAll other positions (13 slots) should contain dark placeholder boxes.")
        print("See generate_master_stat_icons.py for complete implementation.\n")
        
        # If we found resist icons, show mapping example
        if 'gemicons01.tga' in self.gemicon_data:
            print("\nEXAMPLE: Discovered resist icons in gemicons01.tga:")
            print("-" * 80)
            
            for resist_name in ["Fire", "Cold", "Magic", "Poison", "Disease"]:
                # Look for resist icons in discovered data
                found_in_variants = []
                
                for anim_name, frames in self.gemicon_data['gemicons01.tga'].items():
                    if resist_name.lower() in anim_name.lower():
                        for frame in frames[:1]:  # Show first variant only
                            source_pos = f"({frame['x']}, {frame['y']})"
                            source_size = f"{frame['width']}×{frame['height']}"
                            variant = frame['variant']
                            
                            if resist_name in MASTER_LAYOUT_RESIST_POSITIONS:
                                master = MASTER_LAYOUT_RESIST_POSITIONS[resist_name]
                                master_pos = f"({master['x']}, {master['y']})"
                                
                                print(f"  {resist_name:7} | {variant:12} | Source: {source_pos:10} {source_size:6} → "
                                      f"Master: {master_pos:10} 22×22")
                                found_in_variants.append(variant)
                                break
                
                if not found_in_variants and resist_name in MASTER_LAYOUT_RESIST_POSITIONS:
                    master = MASTER_LAYOUT_RESIST_POSITIONS[resist_name]
                    master_pos = f"({master['x']}, {master['y']})"
                    print(f"  {resist_name:7} | (Not found in variants - use placeholder at {master_pos})")
            
            print("-" * 80)
        
        print("\n💡 To add resist icons from a new UI variant:")
        print("  1. Run this script to find the source coordinates")
        print("  2. Add extraction rules to generate_master_stat_icons.py")
        print("  3. Icons will be auto-resized to 22×22 and placed at master positions")
        print("="*80)


def main():
    """Main execution function"""
    # Get workspace root (parent of .bin directory)
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    print(f"Workspace: {workspace_root}")
    
    # Create extractor and scan
    extractor = GemiconExtractor(workspace_root)
    total_found = extractor.scan_directories()
    
    if total_found == 0:
        print("\n[WARNING] No gemicon references found in any UI variant!")
        print("    This could mean:")
        print("    - The UI variants use different texture files")
        print("    - Icons are defined inline in individual window files")
        print("    - The search directories or file names need adjustment")
        return 1
    
    # Generate output files
    docs_dir = workspace_root / '.docs'
    docs_dir.mkdir(exist_ok=True)
    
    json_path = docs_dir / 'GEMICON-COORDINATES.json'
    md_path = docs_dir / 'GEMICON-REFERENCE.md'
    
    print("\n" + "="*80)
    print("GENERATING OUTPUT FILES")
    print("="*80)
    
    extractor.generate_json_output(json_path)
    extractor.generate_markdown_output(md_path)
    
    # Show summary
    extractor.generate_summary()
    
    # Show master layout mapping for resist icons
    extractor.show_master_layout_mapping()
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS FOR THORNE UI:\n")
    
    if 'gemicons01.tga' in extractor.gemicon_data:
        print("  1. gemicons01.tga contains grid-based icons")
        print("     - Can be used for stat/resist icons")
        print("     - Reference the Grid animation coordinates")
    
    if 'gemicons02.tga' in extractor.gemicon_data:
        print("  2. gemicons02.tga provides additional icon sets")
        print("     - Check for alternative or supplemental icons")
    
    print("  3. Review generated documentation:")
    print(f"     - JSON: {json_path.relative_to(workspace_root)}")
    print(f"     - MD:   {md_path.relative_to(workspace_root)}")
    
    print("\n[SUCCESS] Extraction complete!\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
