#!/usr/bin/env python3
"""
Visual grid detector for gemicon texture files.

This tool analyzes gemicon textures to automatically detect:
- Icon grid boundaries and spacing
- Individual icon locations
- Transparent vs opaque pixels (to identify actual icons)
- Creates a visual grid map showing icon positions

This enables automated discovery of where specific icons are located
without manual visual inspection.

Usage:
    python detect_gemicon_grid.py --file default/gemicons01.tga
    python detect_gemicon_grid.py --file default/gemicons01.tga --grid-size 20
    python detect_gemicon_grid.py --file default/gemicons01.tga --export grid_map.png
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

class GemiconGridDetector:
    """Automatically detect icon grid layout in gemicon textures."""
    
    def __init__(self, texture_path):
        """
        Initialize detector.
        
        Args:
            texture_path: Path to gemicon.tga file
        """
        self.texture_path = Path(texture_path)
        self.image = None
        self.width = None
        self.height = None
        self.pixels = None
        self.grid_info = {}
        
    def load_texture(self):
        """Load texture file and convert to RGBA."""
        try:
            self.image = Image.open(self.texture_path).convert('RGBA')
            self.width, self.height = self.image.size
            print(f"[OK] Loaded {self.texture_path.name} ({self.width}x{self.height})")
            return True
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def analyze_transparency(self):
        """
        Analyze transparency patterns to find icon boundaries.
        
        Returns:
            Dictionary with transparency analysis
        """
        # Get pixel data
        pixels = self.image.load()
        
        # Find rows and columns with opaque content
        rows_with_content = []
        cols_with_content = set()
        
        for y in range(self.height):
            row_has_content = False
            for x in range(self.width):
                alpha = pixels[x, y][3] if len(pixels[x, y]) > 3 else 255
                if alpha > 128:
                    row_has_content = True
                    cols_with_content.add(x)
            if row_has_content:
                rows_with_content.append(y)
        
        if not rows_with_content:
            print("WARNING: No opaque pixels found (possibly all transparent texture)")
            return {
                'has_content': False,
                'content_rows': [],
                'content_cols': [],
                'row_count': 0,
                'col_count': 0
            }
        
        cols_with_content = sorted(cols_with_content)
        
        return {
            'has_content': True,
            'content_rows': [rows_with_content[0], rows_with_content[-1]],
            'content_cols': [cols_with_content[0], cols_with_content[-1]],
            'row_count': len(rows_with_content),
            'col_count': len(cols_with_content)
        }
    
    def detect_grid_spacing(self, sample_size=50):
        """
        Detect icon grid spacing by analyzing gap patterns.
        
        Args:
            sample_size: Number of pixels to scan for spacing patterns
            
        Returns:
            Estimated icon size and spacing
        """
        trans_analysis = self.analyze_transparency()
        
        if not trans_analysis['has_content']:
            return None
        
        # Analyze vertical gaps (between row groups)
        pixels = self.image.load()
        
        transitions = []
        prev_has_content = False
        
        for y in range(self.height):
            row_has_content = False
            for x in range(self.width):
                alpha = pixels[x, y][3] if len(pixels[x, y]) > 3 else 255
                if alpha > 128:
                    row_has_content = True
                    break
            
            if prev_has_content != row_has_content:
                transitions.append(y)
            prev_has_content = row_has_content
        
        # Estimate icon size from spacing patterns
        common_gaps = defaultdict(int)
        if len(transitions) > 1:
            for i in range(1, len(transitions)):
                gap = transitions[i] - transitions[i-1]
                if 10 <= gap <= 50:  # Typical icon sizes: 16x16, 20x20, 24x24
                    common_gaps[gap] += 1
        
        if common_gaps:
            estimated_icon_size = max(common_gaps, key=common_gaps.get)
        else:
            # Default estimate for 256x256 texture
            estimated_icon_size = 20
        
        return {
            'estimated_icon_size': estimated_icon_size,
            'common_gaps': dict(common_gaps),
            'spacing_confidence': 'high' if max(common_gaps.values(), default=0) > 5 else 'low'
        }
    
    def create_grid_visualization(self, grid_size=20, export_path=None):
        """
        Create visual grid overlay showing detected icon positions.
        
        Args:
            grid_size: Expected icon size (16, 20, 24, etc.)
            export_path: Optional path to save visualization
            
        Returns:
            PIL Image with grid overlay
        """
        # Create a copy of the texture to draw on
        display_img = self.image.copy()
        draw = ImageDraw.Draw(display_img)
        
        # Draw grid lines
        color = (255, 0, 0, 255)  # Red with full opacity
        
        # Vertical grid lines
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=color, width=1)
        
        # Horizontal grid lines
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=color, width=1)
        
        # Draw corner markers on potential icons
        grid_img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        grid_draw = ImageDraw.Draw(grid_img)
        
        pixels = self.image.load()
        cols = self.width // grid_size
        rows = self.height // grid_size
        
        for row in range(rows):
            for col in range(cols):
                x_start = col * grid_size
                y_start = row * grid_size
                x_end = min(x_start + grid_size, self.width)
                y_end = min(y_start + grid_size, self.height)
                
                # Check if this cell has content
                has_content = False
                for y in range(y_start, y_end):
                    for x in range(x_start, x_end):
                        alpha = pixels[x, y][3] if len(pixels[x, y]) > 3 else 255
                        if alpha > 128:
                            has_content = True
                            break
                    if has_content:
                        break
                
                if has_content:
                    # Draw corner dots for populated cells
                    marker_size = 4
                    marker_color = (0, 255, 0, 200)  # Green
                    grid_draw.ellipse(
                        [(x_start+1, y_start+1), 
                         (x_start+1+marker_size, y_start+1+marker_size)],
                        fill=marker_color
                    )
        
        # Blend grid with original
        display_img.paste(grid_img, (0, 0), grid_img)
        
        if export_path:
            display_img.save(export_path)
            print(f"[OK] Saved grid visualization to {export_path}")
        
        return display_img
    
    def analyze(self, grid_size=24):
        """Run complete analysis."""
        if not self.load_texture():
            return False
        
        print("\nAnalyzing texture...")
        
        # Transparency analysis
        trans = self.analyze_transparency()
        print(f"[OK] Transparency analysis: {trans['row_count']} content rows, {trans['col_count']} content cols")
        
        # Grid detection
        spacing = self.detect_grid_spacing()
        if spacing:
            print(f"[OK] Detected icon size: {spacing['estimated_icon_size']}x{spacing['estimated_icon_size']} pixels")
            print(f"[OK] Spacing confidence: {spacing['spacing_confidence']}")
            if spacing['common_gaps']:
                print(f"[OK] Common gaps detected: {spacing['common_gaps']}")
        else:
            print(f"[OK] Using standard gemicon icon size: 24x24 pixels")
        
        # Create visualization with correct grid size
        if not grid_size:
            grid_size = spacing.get('estimated_icon_size', 24) if spacing else 24
        
        grid_img = self.create_grid_visualization(grid_size)
        
        stats = {
            'file': self.texture_path.name,
            'dimensions': f"{self.width}x{self.height}",
            'grid_size': grid_size,
            'icons_per_row': self.width // grid_size,
            'icons_per_col': self.height // grid_size,
            'total_grid_cells': (self.width // grid_size) * (self.height // grid_size),
            'transparency_analysis': trans,
            'spacing_analysis': spacing,
            'note': 'Gemicon icons are 24x24 pixels. They are resized to 22x22 when extracted to stat_icon_pieces files.'
        }
        
        self.grid_info = stats
        return grid_img


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Detect icon grid layout in gemicon texture files"
    )
    parser.add_argument(
        "--file", "-f",
        required=False,
        help="Path to gemicon.tga file"
    )
    parser.add_argument(
        "--grid-size", "-g",
        type=int,
        default=24,
        help="Grid size in pixels (default: 24 for standard gemicon icons)"
    )
    parser.add_argument(
        "--export", "-e",
        help="Export grid visualization to PNG file"
    )
    
    args = parser.parse_args()
    
    # If no file specified, find default gemicons
    if not args.file:
        files = list(Path("default").glob("gemicons*.tga"))
        if not files:
            print("ERROR: No gemicon files found. Specify with --file or place in default/")
            return 1
        file_path = files[0]
        print(f"Using {file_path}")
    else:
        file_path = args.file
    
    detector = GemiconGridDetector(file_path)
    grid_img = detector.analyze(grid_size=args.grid_size)
    
    if grid_img and args.export:
        grid_img.save(args.export)
        print(f"\n[OK] Saved visualization: {args.export}")
    
    print("\n" + "─" * 70)
    print("Grid Analysis Summary:")
    print("─" * 70)
    for key, value in detector.grid_info.items():
        if key not in ['transparency_analysis', 'spacing_analysis']:
            print(f"{key:25}: {value}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
