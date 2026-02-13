#!/usr/bin/env python3
"""
Generate Stat Icons with Abbreviations

Complete workflow for creating stat_icon_pieces files from any icon variant.

Features:
  - Reads icon coordinates from flexible JSON config
  - Extracts icons from gemicon files in source directory
  - Resizes to 22x22 pixels
  - Places in 256x256 template at master layout positions
  - Adds abbreviation labels (no separate step needed)
  - Generates placeholder graphics for missing icons
  - Works with any icon variant (Classic, Duxa, Modern, etc.)

Usage:
    python generate_stat_icons.py --source-dir thorne_drak/Options/Icons/Classic \
                                  --config stat-icons-config.json \
                                  --output thorne_drak/stat_icon_pieces01.tga

    python generate_stat_icons.py --source-dir thorne_drak/Options/Icons/Duxa \
                                  --config stat-icons-config.json \
                                  --output thorne_drak/stat_icon_pieces_duxa.tga \
                                  --add-abbreviations

The JSON config maps stat names to:
  - Source file (e.g., gemicons01.tga)
  - Coordinates (x, y)
  - Size (w, h - typically 24x24)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class StatIconGenerator:
    """Generate stat icon files with abbreviations."""
    
    # Master layout - where each icon should be placed in 256x256 output
    MASTER_LAYOUT = {
        "AC":       {"x": 10,  "y": 10,  "col": 1, "row": 1},
        "ATK":      {"x": 10,  "y": 40,  "col": 1, "row": 2},
        "HP":       {"x": 10,  "y": 70,  "col": 1, "row": 3},
        "MANA":     {"x": 10,  "y": 100, "col": 1, "row": 4},
        "STA":      {"x": 10,  "y": 130, "col": 1, "row": 5},
        "Weight":   {"x": 10,  "y": 160, "col": 1, "row": 6},
        "Fire":     {"x": 90,  "y": 10,  "col": 2, "row": 1},
        "Cold":     {"x": 90,  "y": 40,  "col": 2, "row": 2},
        "Magic":    {"x": 90,  "y": 70,  "col": 2, "row": 3},
        "Poison":   {"x": 90,  "y": 100, "col": 2, "row": 4},
        "Disease":  {"x": 90,  "y": 130, "col": 2, "row": 5},
        "Reserve":  {"x": 90,  "y": 160, "col": 2, "row": 6},
        "STR":      {"x": 170, "y": 10,  "col": 3, "row": 1},
        "INT":      {"x": 170, "y": 40,  "col": 3, "row": 2},
        "WIS":      {"x": 170, "y": 70,  "col": 3, "row": 3},
        "AGI":      {"x": 170, "y": 100, "col": 3, "row": 4},
        "DEX":      {"x": 170, "y": 130, "col": 3, "row": 5},
        "CHA":      {"x": 170, "y": 160, "col": 3, "row": 6},
    }
    
    # Abbreviations for each icon
    ABBREVIATIONS = {
        "AC": "AC", "ATK": "ATK", "HP": "HP", "MANA": "MP", "STA": "ST", "Weight": "WT",
        "Fire": "FR", "Cold": "CR", "Magic": "MR", "Poison": "PR", "Disease": "DR", "Reserve": "RV",
        "STR": "STR", "INT": "INT", "WIS": "WIS", "AGI": "AGI", "DEX": "DEX", "CHA": "CHA",
    }
    
    def __init__(self, source_dir, config_file, output_file, add_abbreviations=False):
        """
        Initialize the generator.
        
        Args:
            source_dir: Directory containing gemicon files (e.g., thorne_drak/Options/Icons/Classic)
            config_file: JSON file with icon coordinate mappings
            output_file: Output path for stat_icon_pieces file
            add_abbreviations: Whether to add abbreviation labels
        """
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.add_abbreviations = add_abbreviations
        self.config = None
        self.icon_sources = {}
        self.stats = {
            "file": output_file,
            "source_dir": str(source_dir),
            "icons": {}
        }
        
        # Load config
        if not self._load_config(config_file):
            raise ValueError(f"Failed to load config: {config_file}")
    
    def _load_config(self, config_file):
        """Load icon coordinate configuration from JSON."""
        config_path = Path(config_file)
        
        if not config_path.exists():
            print(f"ERROR: Config file not found: {config_path}")
            return False
        
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            print(f"[OK] Loaded config: {config_path}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to load config: {e}")
            return False
    
    def _create_placeholder(self, size=22):
        """Create a dark placeholder icon."""
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Outer border
        draw.rectangle([0, 0, size-1, size-1], outline=(0, 0, 0, 255), width=2)
        
        # Fill
        draw.rectangle([2, 2, size-3, size-3], fill=(43, 43, 43, 255))
        
        # Inner accent line
        draw.rectangle([3, 3, size-4, size-4], outline=(68, 68, 68, 255), width=1)
        
        # Center square
        center = size // 2
        box_size = 6
        draw.rectangle(
            [center-box_size//2, center-box_size//2, center+box_size//2, center+box_size//2],
            outline=(68, 68, 68, 255),
            width=1
        )
        
        return img
    
    def _extract_icon(self, source_file, x, y, w, h, target_size=22):
        """Extract icon from source file and resize."""
        try:
            full_path = self.source_dir / source_file
            
            if not full_path.exists():
                print(f"  WARNING: File not found: {source_file}")
                return self._create_placeholder(target_size)
            
            # Load and extract
            source_img = Image.open(full_path).convert("RGBA")
            icon = source_img.crop((x, y, x + w, y + h))
            
            # Resize if needed
            if w != target_size or h != target_size:
                icon = icon.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            return icon
        except Exception as e:
            print(f"  WARNING: Failed to extract from {source_file}: {e}")
            return self._create_placeholder(target_size)
    
    def _add_abbreviation_label(self, img, text, font_size=8):
        """Add abbreviation text label to icon image."""
        try:
            draw = ImageDraw.Draw(img)
            
            # Try to load a bold font, fall back to default
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("Arial", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Draw text in bottom right
            text_color = (0, 0, 0, 255)  # Black
            draw.text((2, 16), text, fill=text_color, font=font)
            
            return img
        except Exception as e:
            print(f"  WARNING: Failed to add abbreviation: {e}")
            return img
    
    def generate(self):
        """Generate the stat icon file."""
        print("\n" + "="*70)
        print(f"GENERATING: {self.output_file}")
        print("="*70)
        
        # Create blank 256x256 RGBA template
        output_img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        
        # Process each icon in master layout
        for icon_name, layout in self.MASTER_LAYOUT.items():
            x = layout["x"]
            y = layout["y"]
            
            # Get icon from config
            if icon_name in self.config:
                source_info = self.config[icon_name]
                source_file = source_info.get("file")
                src_x = source_info.get("x")
                src_y = source_info.get("y")
                src_w = source_info.get("w", 24)
                src_h = source_info.get("h", 24)
                
                # Extract icon
                icon = self._extract_icon(source_file, src_x, src_y, src_w, src_h)
                
                # Add abbreviation if enabled
                if self.add_abbreviations and icon_name in self.ABBREVIATIONS:
                    abbr = self.ABBREVIATIONS[icon_name]
                    icon = self._add_abbreviation_label(icon, abbr, font_size=7)
                
                icon_type = "extracted"
                source_info_display = f"{source_file} @ ({src_x},{src_y})"
                print(f"  OK {icon_name:8} at ({x:3},{y:3}) <- {source_info_display}")
            else:
                # Create placeholder
                icon = self._create_placeholder()
                icon_type = "placeholder"
                source_info_display = None
                print(f"  -- {icon_name:8} at ({x:3},{y:3}) PLACEHOLDER")
            
            # Paste into output
            output_img.paste(icon, (x, y), icon)
            
            # Record stats
            self.stats["icons"][icon_name] = {
                "position": {"x": x, "y": y},
                "size": "22x22",
                "type": icon_type,
                "source": source_info_display
            }
        
        # Create output directory if needed
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save output
        output_img.save(self.output_file)
        print(f"\n[OK] Generated: {self.output_file}")
        
        if self.add_abbreviations:
            print("[OK] Abbreviations added to texture")
        
        return True
    
    def save_stats(self, stats_file=None):
        """Save generation statistics to JSON."""
        if not stats_file:
            stats_file = self.output_file.stem + "-stats.json"
        
        stats_path = self.output_file.parent / stats_file
        
        try:
            with open(stats_path, 'w') as f:
                json.dump(self.stats, f, indent=2)
            print(f"[OK] Saved stats: {stats_path}")
        except Exception as e:
            print(f"WARNING: Failed to save stats: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="regen_stat_icons.py",
        description="""
Generate Stat Icon Textures with Abbreviations

Extracts stat icons from gemicon files and creates stat_icon_pieces texture files
with abbreviation labels. Supports any icon variant (Classic, Duxa, Modern, etc.).

FEATURES:
  ✓ Flexible JSON config for icon coordinate mapping
  ✓ Automatic icon extraction and resizing (22×22)
  ✓ Master layout positioning in 256×256 output
  ✓ Abbreviation label generation (no separate step)
  ✓ Placeholder graphics for missing icons
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  
  # Generate from Classic variant with default config
  python regen_stat_icons.py \\
    --source-dir thorne_drak/Options/Icons/Classic \\
    --output thorne_drak/stat_icon_pieces01.tga
  
  # Custom output location with abbreviations
  python regen_stat_icons.py \\
    --source-dir thorne_drak/Options/Icons/Duxa \\
    --output thorne_drak/stat_icon_pieces_duxa.tga \\
    --add-abbreviations
  
  # Custom config file
  python regen_stat_icons.py \\
    --source-dir thorne_drak/Options/Icons/Classic \\
    --config .development/custom-icons-config.json \\
    --output thorne_drak/stat_icon_pieces01.tga

CONFIGURATION:
  The config JSON maps stat names to source coordinates:
    {
      "AC": {"source": "gemicons01.tga", "x": 0, "y": 0, "w": 24, "h": 24},
      "ATK": {"source": "gemicons01.tga", "x": 24, "y": 0, "w": 24, "h": 24},
      ...
    }

OUTPUT:
  - Creates main texture file (e.g., stat_icon_pieces01.tga)
  - Generates stats JSON file (e.g., stat_icon_pieces01-stats.json)
  - Stats file tracks extraction metadata for troubleshooting
"""
    )
    parser.add_argument(
        "--source-dir", "-s",
        required=True,
        metavar="DIR",
        help="Source directory containing gemicon files (e.g., thorne_drak/Options/Icons/Classic)"
    )
    parser.add_argument(
        "--config", "-c",
        default=".development/stat-icons-config.json",
        metavar="FILE",
        help="Config file with icon coordinate mappings (default: .development/stat-icons-config.json)"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        metavar="FILE",
        help="Output file path for texture (e.g., thorne_drak/stat_icon_pieces01.tga)"
    )
    parser.add_argument(
        "--add-abbreviations", "-a",
        action="store_true",
        help="Include abbreviation labels on icons (2-3 char labels)"
    )
    
    args = parser.parse_args()
    
    try:
        generator = StatIconGenerator(
            args.source_dir,
            args.config,
            args.output,
            add_abbreviations=args.add_abbreviations
        )
        
        if generator.generate():
            generator.save_stats()
            return 0
        else:
            return 1
    
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
