#!/usr/bin/env python3
"""
Analyze gem icon layouts and create searchable reference.

This tool analyzes gemicons*.tga files to understand what icons are available
and their positions. It then creates a reference guide to help identify which
gem/spell icons could be used as substitutes for missing stat icons.

Purpose:
  - Map out gem icon grids (typically 256x256 with small icons)
  - Create searchable reference of available icons
  - Suggest which gems could replace placeholder slots in stat icons
  - Support future expansion of stat_icon_pieces extraction

Usage:
    python analyze_gemicons.py
    python analyze_gemicons.py --source default
    python analyze_gemicons.py --output reference.md

Output:
    - Console display of gem icon analysis
    - JSON mapping files
    - Reference guide for manual selection
"""

import os
import sys
from pathlib import Path
from PIL import Image
import json

class GemiconAnalyzer:
    """Analyze gemicon texture files to map their layout."""
    
    def __init__(self, source_dir="default"):
        """
        Initialize analyzer.
        
        Args:
            source_dir: UI variant directory to analyze (default, duxaUI, etc.)
        """
        self.source_dir = Path(source_dir)
        self.gemicon_files = []
        self.icon_analysis = {}
        self.missing_stat_icons = {
            'HP': 'Hit Points (usually heart icon)',
            'MANA': 'Mana Points (usually blue orb/flask)',
            'STA': 'Stamina (usually circular breath/lung icon)',
            'Weight': 'Character Weight (usually scale icon)',
            'STR': 'Strength (usually fist/sword)',
            'INT': 'Intelligence (usually book/scroll)',
            'WIS': 'Wisdom (usually eye/spirit)',
            'AGI': 'Agility (usually lightning/movement)',
            'DEX': 'Dexterity (usually hand/precision)',
            'CHA': 'Charisma (usually star/force)'
        }
        
    def find_gemicon_files(self):
        """Find all gemicon*.tga files in source directory."""
        if not self.source_dir.exists():
            print(f"ERROR: Source directory not found: {self.source_dir}")
            return False
        
        gemicon_files = list(self.source_dir.glob("gemicons*.tga"))
        if not gemicon_files:
            print(f"No gemicon files found in {self.source_dir}")
            return False
        
        self.gemicon_files = sorted(gemicon_files)
        print(f"[OK] Found {len(self.gemicon_files)} gemicon files:")
        for f in self.gemicon_files:
            print(f"  - {f.name}")
        return True
    
    def analyze_texture(self, texture_path):
        """
        Analyze a texture file to understand its layout.
        
        Args:
            texture_path: Path to .tga file
            
        Returns:
            Dictionary with analysis results
        """
        try:
            img = Image.open(texture_path)
            width, height = img.size
            
            # Analyze color distribution to estimate icon grid
            # Typical patterns:
            # - 256x256 with ~10-15 icons per row suggests 16x16 or 20x20 icons
            # - 512x512 with more icons
            
            analysis = {
                'file': texture_path.name,
                'dimensions': f"{width}x{height}",
                'size_bytes': os.path.getsize(texture_path),
                'format': img.format
            }
            
            # Estimate icon count and size based on typical EQ patterns
            if width == 256 and height == 256:
                # Standard gemicon format: 256x256 with 24x24 icons
                # 256/24 = 10.67, so 10 or 11 icons per row with small spacing
                analysis['estimated_icon_size'] = "24x24"
                analysis['estimated_grid'] = "10-11 columns x 10-11 rows"
                analysis['estimated_icon_count'] = "100-120"
            elif width == 512 and height == 512:
                analysis['estimated_icon_size'] = "48x48 or 32x32"
                analysis['estimated_grid'] = "16x16 grid"
                analysis['estimated_icon_count'] = "200-400"
            
            return analysis
            
        except Exception as e:
            print(f"ERROR analyzing {texture_path}: {e}")
            return None
    
    def extract_gem_icon_analysis(self):
        """
        Extract analysis from all gemicon files.
        
        Returns:
            Dictionary mapping filenames to analysis data
        """
        analysis = {}
        for gemicon_file in self.gemicon_files:
            result = self.analyze_texture(gemicon_file)
            if result:
                analysis[gemicon_file.name] = result
                self.icon_analysis[gemicon_file.name] = result
        
        return analysis
    
    def generate_reference_guide(self):
        """Generate a human-readable reference guide."""
        output = []
        output.append("=" * 70)
        output.append("GEM ICON LAYOUT ANALYSIS & REFERENCE")
        output.append("=" * 70 + "\n")
        
        output.append(f"Source Directory: {self.source_dir}\n")
        output.append("Gemicon Files Analyzed:")
        output.append("-" * 70)
        
        for filename, analysis in self.icon_analysis.items():
            output.append(f"\n{filename}")
            output.append(f"  Dimensions: {analysis['dimensions']}")
            output.append(f"  Size: {analysis['size_bytes']:,} bytes")
            output.append(f"  Est. Icon Size: {analysis['estimated_icon_size']}")
            output.append(f"  Est. Grid: {analysis['estimated_grid']}")
            output.append(f"  Est. Icons: {analysis['estimated_icon_count']}")
        
        output.append("\n" + "-" * 70)
        output.append("\nEXISTING GEM ICON COORDINATES (from gemicons01.tga):")
        output.append("-" * 70)
        output.append("""
These coordinates are from the current gemicon files and are used to extract
resist icons. Each icon is 24×24 pixels and resized to 22×22 for stat_icons:

  Fire:     (48, 120)     24×24 → resize to 22×22 → place at (90, 10)
  Cold:     (168, 120)    24×24 → resize to 22×22 → place at (90, 40)
  Magic:    (216, 144)    24×24 → resize to 22×22 → place at (90, 70)
  Poison:   (24, 144)     24×24 → resize to 22×22 → place at (90, 100)
  Disease:  (120, 144)    24×24 → resize to 22×22 → place at (90, 130)

These locations work across different UI variants (vert-blue, default, etc.)
that have consistent resist icon layouts.
""")
        output.append("-" * 70)
        output.append("\nMISSING STAT ICONS (Need Replacements):")
        output.append("-" * 70)
        
        for stat_name, description in self.missing_stat_icons.items():
            output.append(f"\n{stat_name:10} → {description}")
            output.append(f"           In gemicons files, look for:")
            
            # Suggest what to look for
            suggestions = self.suggest_gem_replacements(stat_name)
            for suggestion in suggestions:
                output.append(f"             • {suggestion}")
        
        output.append("\n" + "-" * 70)
        output.append("\nNEXT STEPS FOR ICON EXTRACTION:")
        output.append("-" * 70)
        output.append("""
1. Analyze gemicon layout using detect_gemicon_grid.py:
   python .bin/detect_gemicon_grid.py --file default/gemicons01.tga \\
                                      --grid-size 24 \\
                                      --export gemicon_grid_map.png
   
   This will create a visual grid overlay showing all icons in 24×24 cells.

2. For each missing stat icon (HP, MANA, STA, Weight, STR, INT, WIS, AGI, DEX, CHA):
   - Open gemicons01.tga, gemicons02.tga, gemicons03.tga in image editor
   - Find a suitable 24×24 gem/spell icon that matches the stat
   - Note its coordinates (e.g., 96, 72 for a 24x24 icon)
   - Use extract_gemicon_coordinates.py to document the finding

3. Update generate_master_stat_icons.py with new extraction rules:
   - Add entry to PIECES01_SOURCES, PIECES02_SOURCES, or PIECES03_SOURCES
   - Icon will be extracted 24×24 and automatically resized to 22×22
   - Placement position is defined in MASTER_LAYOUT

The entire process is compatible with current scripts:
  - extract_gemicon_coordinates.py: Documents where icons are in gemicons
  - generate_master_stat_icons.py: Extracts, resizes, and places them in stat_icons
  - add_abbreviations_to_textures.py: Adds abbreviation labels to final stat_icons files
""")
        
        return "\n".join(output)
    
    def suggest_gem_replacements(self, stat_name):
        """Suggest where to look for gem icons to replace stat icons."""
        suggestions = {
            'HP': ['Red heart icon', 'Healing spell icon', 'Cure spell gem'],
            'MANA': ['Blue orb/sphere', 'Blue flask/potion', 'Wiz or Enc spell gem'],
            'STA': ['Breathing/lungs icon', 'Endurance icon', 'Physical spell icon'],
            'Weight': ['Scale/balance icon', 'Inventory icon', 'Container icon'],
            'STR': ['Sword/weapon icon', 'Fist/punch icon', 'Melee damage gem'],
            'INT': ['Book/scroll icon', 'Mind/brain icon', 'Wiz spell gem'],
            'WIS': ['Eye/vision icon', 'Spirit/aura icon', 'Cleric spell gem'],
            'AGI': ['Lightning/movement icon', 'Speed icon', 'Movement spell gem'],
            'DEX': ['Target/crosshair icon', 'Archer/range icon', 'Range weapon icon'],
            'CHA': ['Star/sparkle icon', 'Charisma/aura icon', 'Social/power icon']
        }
        return suggestions.get(stat_name, ['Look for related icon in gem library'])
    
    def save_json_reference(self, output_file=".development/gemicon-analysis.json"):
        """Save analysis to JSON file."""
        data = {
            'source_directory': str(self.source_dir),
            'gemicon_files': self.icon_analysis,
            'missing_stat_icons': self.missing_stat_icons,
            'stat_icon_positions': {
                'HP': {'x': 10, 'y': 70, 'col': 1, 'row': 3},
                'MANA': {'x': 10, 'y': 100, 'col': 1, 'row': 4},
                'STA': {'x': 10, 'y': 130, 'col': 1, 'row': 5},
                'Weight': {'x': 10, 'y': 160, 'col': 1, 'row': 6},
                'STR': {'x': 170, 'y': 10, 'col': 3, 'row': 1},
                'INT': {'x': 170, 'y': 40, 'col': 3, 'row': 2},
                'WIS': {'x': 170, 'y': 70, 'col': 3, 'row': 3},
                'AGI': {'x': 170, 'y': 100, 'col': 3, 'row': 4},
                'DEX': {'x': 170, 'y': 130, 'col': 3, 'row': 5},
                'CHA': {'x': 170, 'y': 160, 'col': 3, 'row': 6}
            }
        }
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[OK] Saved analysis to {output_file}")
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze gem icon layouts and create reference guides"
    )
    parser.add_argument(
        "--source",
        default="default",
        help="UI variant directory to analyze (default: default)"
    )
    parser.add_argument(
        "--output",
        help="Save reference guide to file"
    )
    
    args = parser.parse_args()
    
    analyzer = GemiconAnalyzer(args.source)
    
    print()
    if not analyzer.find_gemicon_files():
        return 1
    
    print()
    analyzer.extract_gem_icon_analysis()
    
    print()
    reference = analyzer.generate_reference_guide()
    print(reference)
    
    # Save JSON reference
    analyzer.save_json_reference()
    
    # Save markdown reference if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write(reference)
        print(f"\n✓ Saved reference guide to {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
