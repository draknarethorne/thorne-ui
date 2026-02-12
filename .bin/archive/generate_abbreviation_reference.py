#!/usr/bin/env python3
"""
Generate a visual reference guide for stat icon abbreviations.

Creates a text-based or image-based reference showing all icons with their
abbreviations laid out in the master layout grid.

This is useful for quick reference when manually editing textures.

Usage:
    python generate_abbreviation_reference.py          # Show in terminal
    python generate_abbreviation_reference.py --save   # Save as PNG
    python generate_abbreviation_reference.py --format text
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class AbbreviationReferenceGenerator:
    """Generate visual reference guides for stat icon abbreviations."""
    
    def __init__(self):
        """Initialize the generator."""
        self.coordinates = None
        self.abbreviations = None
        
    def load_coordinates(self):
        """Load the coordinates JSON file."""
        coord_path = Path(__file__).parent.parent / ".development" / "stat-icons-coordinates.json"
        
        if not coord_path.exists():
            print(f"ERROR: Coordinates file not found: {coord_path}")
            return False
        
        try:
            with open(coord_path, 'r') as f:
                self.coordinates = json.load(f)
            self.abbreviations = self.coordinates.get('abbreviations', {})
            return True
        except Exception as e:
            print(f"ERROR: Failed to load coordinates: {e}")
            return False
    
    def generate_text_reference(self):
        """Generate a text-based reference guide."""
        if not self.abbreviations:
            print("No abbreviations found")
            return
        
        output = []
        output.append("╔═══════════════════════════════════════════════════════════════╗")
        output.append("║          STAT ICON ABBREVIATIONS QUICK REFERENCE              ║")
        output.append("╚═══════════════════════════════════════════════════════════════╝\n")
        
        # Stats section
        output.append("📊 STATS (Column 1) - Player Core Stats")
        output.append("─" * 60)
        stats = self.abbreviations.get('stats', {})
        for abbr in ['AC', 'ATK', 'HP', 'MP', 'ST', 'WT']:
            if abbr in stats:
                full_name = stats[abbr]
                output.append(f"  {abbr:4} → {full_name}")
        
        output.append("\n🛡️  RESISTANCES (Column 2) - Damage Resistances")
        output.append("─" * 60)
        resistances = self.abbreviations.get('resistances', {})
        for abbr in ['FR', 'CR', 'MR', 'PR', 'DR', 'RV']:
            if abbr in resistances:
                full_name = resistances[abbr]
                output.append(f"  {abbr:4} → {full_name}")
        
        output.append("\n⚔️  ATTRIBUTES (Column 3) - Character Traits")
        output.append("─" * 60)
        attributes = self.abbreviations.get('attributes', {})
        for abbr in ['STR', 'INT', 'WIS', 'AGI', 'DEX', 'CHA']:
            if abbr in attributes:
                full_name = attributes[abbr]
                output.append(f"  {abbr:4} → {full_name}")
        
        output.append("\n" + "─" * 60)
        output.append(f"Total: {len(stats)} stats + {len(resistances)} resistances + {len(attributes)} attributes")
        
        text_output = "\n".join(output)
        print(text_output)
        return text_output
    
    def generate_master_layout_reference(self):
        """Generate reference showing the master layout grid."""
        layout = self.coordinates.get('layout', {})
        
        # Organize by position (column, row)
        positions = defaultdict(dict)
        for icon_name, icon_data in layout.items():
            col = icon_data.get('col', 0)
            row = icon_data.get('row', 0)
            positions[(col, row)] = {
                'name': icon_name,
                'abbr': icon_data.get('abbr', '?'),
                'desc': icon_data.get('description', '')
            }
        
        output = []
        output.append("╔═══════════════════════════════════════════════════════════════╗")
        output.append("║          MASTER LAYOUT GRID WITH ABBREVIATIONS                ║")
        output.append("╚═══════════════════════════════════════════════════════════════╝\n")
        
        output.append("Column 1 (Stats)      Column 2 (Resist)      Column 3 (Attrib)")
        output.append("─" * 65)
        
        # Display 6 rows
        for row in range(1, 7):
            col1 = positions.get((1, row), {})
            col2 = positions.get((2, row), {})
            col3 = positions.get((3, row), {})
            
            c1_str = f"{col1.get('abbr', '-'):3} {col1.get('name', ''):6}" if col1 else "      "
            c2_str = f"{col2.get('abbr', '-'):3} {col2.get('name', ''):7}" if col2 else "        "
            c3_str = f"{col3.get('abbr', '-'):3} {col3.get('name', ''):6}" if col3 else "      "
            
            row_str = f"Row {row}  {c1_str}        {c2_str}        {c3_str}"
            output.append(row_str)
        
        text_output = "\n".join(output)
        print(text_output)
        return text_output
    
    def generate_png_reference(self, output_path="abbreviation_reference.png"):
        """Generate a PNG image with the reference guide."""
        if not HAS_PIL:
            print("ERROR: PIL/Pillow not available for image generation")
            print("Install with: pip install Pillow")
            return False
        
        # Create image
        width = 600
        height = 400
        image = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(image)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 12)
                title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 16)
            except:
                font = ImageFont.load_default()
                title_font = font
        
        y = 20
        x_start = 20
        
        # Title
        draw.text((x_start, y), "Stat Icon Abbreviations Reference", fill=(0, 0, 0), font=title_font)
        y += 40
        
        # Stats section
        draw.text((x_start, y), "STATS (Column 1)", fill=(0, 0, 100), font=font)
        y += 20
        stats = self.abbreviations.get('stats', {})
        for abbr in ['AC', 'ATK', 'HP', 'MP', 'ST', 'WT']:
            if abbr in stats:
                text = f"  {abbr} = {stats[abbr]}"
                draw.text((x_start, y), text, fill=(0, 0, 0), font=font)
                y += 18
        
        # Save the image
        output_file = Path(output_path)
        image.save(output_file)
        print(f"✓ Generated reference image: {output_file}")
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate abbreviation reference guides"
    )
    parser.add_argument(
        "--format",
        choices=['text', 'layout', 'png'],
        default='text',
        help="Reference format (default: text)"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save PNG reference (if format=png)"
    )
    
    args = parser.parse_args()
    
    generator = AbbreviationReferenceGenerator()
    
    if not generator.load_coordinates():
        return 1
    
    print()
    
    if args.format == 'layout':
        generator.generate_master_layout_reference()
    elif args.format == 'png':
        if args.save:
            generator.generate_png_reference()
        else:
            print("Use --save to generate PNG file")
            return 1
    else:  # text
        generator.generate_text_reference()
    
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
