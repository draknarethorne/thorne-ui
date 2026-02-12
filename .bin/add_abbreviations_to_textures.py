#!/usr/bin/env python3
"""
Add abbreviation text labels to stat icon texture files.

This script reads the stat-icons-coordinates.json file and renders
abbreviation text to the right of each icon in the .tga texture files.

Purpose: When manually editing textures, labels make it easy to identify
what each icon represents without cross-referencing the JSON file.

Usage:
    python add_abbreviations_to_textures.py
    python add_abbreviations_to_textures.py --output modified/
    python add_abbreviations_to_textures.py --font-size 10 --text-color 0,0,0

Options:
    --output DIR        Output directory for modified textures (default: thorne_drak/)
    --font-size SIZE    Font size for text labels (default: 10)
    --text-color RGB    RGB color for text (default: black 0,0,0)
    --dry-run          Show what would be done without modifying files
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: PIL not found. Install with: pip install Pillow")
    sys.exit(1)


class AbbreviationTextRenderer:
    """Renders abbreviation labels onto stat icon texture files."""
    
    def __init__(self, font_size=10, text_color=(0, 0, 0), dry_run=False):
        """
        Initialize the renderer.
        
        Args:
            font_size: Font size for text labels
            text_color: RGB tuple for text color (default: black)
            dry_run: If True, don't actually modify files
        """
        self.font_size = font_size
        self.text_color = text_color
        self.dry_run = dry_run
        self.coordinates = None
        self.textures_dir = None
        self.modified_count = 0
        self.font = None
        
    def load_coordinates(self):
        """Load the stat icons coordinates JSON file."""
        coord_path = Path(__file__).parent.parent / ".development" / "stat-icons-coordinates.json"
        
        if not coord_path.exists():
            print(f"ERROR: Coordinates file not found: {coord_path}")
            return False
        
        try:
            with open(coord_path, 'r') as f:
                self.coordinates = json.load(f)
            print(f"✓ Loaded coordinates from {coord_path.name}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to load coordinates: {e}")
            return False
    
    def setup_font(self):
        """Try to load a system font, prefer bold variant, fall back to default."""
        # Try common font locations - prefer bold variants
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux bold
            "C:\\Windows\\Fonts\\arialbd.ttf",  # Windows bold
            "/Library/Fonts/Arial Bold.ttf",  # macOS bold
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux regular
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows regular
            "/Library/Fonts/Arial.ttf",  # macOS regular
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.font = ImageFont.truetype(font_path, self.font_size)
                    is_bold = "bold" in font_path.lower() or "bd" in font_path.lower()
                    font_type = "Bold" if is_bold else "Regular"
                    print(f"✓ Loaded {font_type} font: {font_path}")
                    return True
                except Exception:
                    continue
        
        # Fall back to default font
        try:
            self.font = ImageFont.load_default()
            print("⚠ Using default font (smaller text)")
            return True
        except Exception as e:
            print(f"ERROR: Failed to load any font: {e}")
            return False
    
    def get_texture_files(self, textures_dir):
        """Get list of texture files to process."""
        tga_files = []
        
        for file_name in self.coordinates.get('files', {}).keys():
            file_path = Path(textures_dir) / file_name
            if file_path.exists():
                tga_files.append((file_name, file_path))
            else:
                print(f"⚠ Texture not found: {file_name}")
        
        return tga_files
    
    def render_abbreviations_on_texture(self, image_path, file_data):
        """
        Render abbreviation labels onto a single texture file.
        
        Args:
            image_path: Path to the .tga file
            file_data: Icon data from coordinates JSON
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Open the texture
            image = Image.open(image_path).convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # Process each icon in this texture file
            icons = file_data.get('icons', {})
            for icon_name, icon_data in icons.items():
                abbr = icon_data.get('abbr')
                if not abbr:
                    continue
                
                # Get position (text goes to the right of the icon)
                x = icon_data.get('position', {}).get('x', 0)
                y = icon_data.get('position', {}).get('y', 0)
                
                # Icon is 22x22, so text starts at x + 24 (22 + 2px spacing)
                text_x = x + 24
                text_y = y + 6  # Vertically align approximately to center
                
                # Render text
                draw.text(
                    (text_x, text_y),
                    abbr,
                    fill=self.text_color,
                    font=self.font
                )
            
            return True, image
            
        except Exception as e:
            print(f"  ERROR processing {image_path.name}: {e}")
            return False, None
    
    def process_textures(self, textures_dir):
        """
        Process all texture files and add abbreviation labels.
        
        Args:
            textures_dir: Directory containing .tga files
        
        Returns:
            Number of successfully modified textures
        """
        self.textures_dir = textures_dir
        
        if not self.load_coordinates():
            return 0
        
        if not self.setup_font():
            return 0
        
        tga_files = self.get_texture_files(textures_dir)
        
        if not tga_files:
            print("✗ No texture files found to process")
            return 0
        
        print(f"\n{'=' * 60}")
        print(f"Processing {len(tga_files)} texture file(s)")
        print(f"{'=' * 60}\n")
        
        for file_name, file_path in tga_files:
            file_data = self.coordinates.get('files', {}).get(file_name, {})
            if not file_data.get('icons'):
                print(f"⚠ No icon data for {file_name}")
                continue
            
            success, modified_image = self.render_abbreviations_on_texture(
                file_path, file_data
            )
            
            if success and modified_image:
                if self.dry_run:
                    print(f"  [DRY RUN] Would modify: {file_name}")
                    icon_count = len(file_data.get('icons', {}))
                    print(f"    Labels to add: {icon_count} icons")
                else:
                    # Save the modified image
                    modified_image.save(file_path)
                    icon_count = len(file_data.get('icons', {}))
                    print(f"✓ {file_name}")
                    print(f"  Added {icon_count} abbreviation labels")
                    self.modified_count += 1
            else:
                print(f"✗ Failed to process {file_name}")
        
        return self.modified_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add abbreviation labels to stat icon texture files"
    )
    parser.add_argument(
        "--output",
        default="thorne_drak",
        help="Directory containing textures (default: thorne_drak/)"
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=10,
        help="Font size for labels (default: 10)"
    )
    parser.add_argument(
        "--text-color",
        default="0,0,0",
        help="RGB color for text (default: 0,0,0 = black)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without modifying files"
    )
    parser.add_argument(
        "--append-backup",
        action="store_true",
        help="Backup original files with .bak extension before modifying"
    )
    
    args = parser.parse_args()
    
    # Parse color
    try:
        text_color = tuple(map(int, args.text_color.split(',')))
        if len(text_color) != 3 or any(c > 255 for c in text_color):
            raise ValueError("Invalid RGB values")
    except (ValueError, IndexError):
        print(f"ERROR: Invalid color format. Use 'R,G,B' (e.g., '255,255,255')")
        return 1
    
    # Verify textures directory
    textures_dir = Path(args.output)
    if not textures_dir.exists():
        print(f"ERROR: Textures directory not found: {args.output}")
        return 1
    
    # Create backups if requested
    if args.append_backup and not args.dry_run:
        print("Creating backups...")
        for tga_file in textures_dir.glob("stat_icon_pieces*.tga"):
            backup_path = tga_file.with_suffix('.bak')
            if not backup_path.exists():
                import shutil
                shutil.copy2(tga_file, backup_path)
                print(f"  ✓ {tga_file.name} → {backup_path.name}")
    
    # Process textures
    renderer = AbbreviationTextRenderer(
        font_size=args.font_size,
        text_color=text_color,
        dry_run=args.dry_run
    )
    
    modified = renderer.process_textures(args.output)
    
    # Summary
    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"DRY RUN: Would modify {modified} texture file(s)")
    else:
        print(f"✓ Successfully modified {modified} texture file(s)")
    print(f"{'=' * 60}\n")
    
    if args.dry_run:
        print("Run without --dry-run to actually modify the files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
