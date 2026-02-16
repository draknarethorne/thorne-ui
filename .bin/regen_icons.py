#!/usr/bin/env python3
"""
Generate Stat Icon Textures from Icon Variants

Complete workflow for creating stat icon texture files from any icon variant
in the Options/Icons directory structure.

Features:
  - Auto-discovers icon variants from thorne_drak/Options/Icons/
  - Reads icon coordinates from JSON config
  - Extracts icons from gemicon files in source directory
  - Resizes to 22x22 pixels
  - Places in 256x256 template at master layout positions
  - Adds abbreviation labels within icons (text overlay)
  - Optionally adds text labels next to icons (--labels flag)
  - Generates placeholder graphics for missing icons
  - Smart copyback (single variant → copy to thorne_drak/, multiple → Thorne only)
  - Automatic deployment to thorne_dev/ for testing

USAGE:
    python regen_icons.py --all                   # Auto-discover all variants
    python regen_icons.py <variant> [variant2 ...]      # Specific variants
    python regen_icons.py Thorne --labels         # With text labels
    python regen_icons.py --help

EXAMPLES:
    # Regenerate ALL variants (auto-discovered from Options/Icons/)
    python regen_icons.py --all
    
    # Single variant - copies to thorne_drak/ and deploys to thorne_dev/
    python regen_icons.py Thorne
    
    # Multiple variants - only Thorne copied to thorne_drak/
    python regen_icons.py Thorne Classic Duxa
    
    # With text labels next to icons (easier to identify during editing)
    python regen_icons.py Thorne --labels
"""

import os
import sys
import json
import shutil
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
    
    def __init__(self, source_dir, config_path, output_file, add_abbreviations=True, add_labels=False):
        """
        Initialize the generator.
        
        Args:
            source_dir: Directory containing gemicon files (e.g., thorne_drak/Options/Icons/Thorne)
            config_path: Path to JSON config file with icon coordinate mappings
            output_file: Output path for staticons texture file
            add_abbreviations: Whether to add abbreviation labels within icons (default: True)
            add_labels: Whether to add text labels next to icons (default: False)
        """
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.add_abbreviations = add_abbreviations
        self.add_labels = add_labels
        self.config = None
        self.font = None
        self.label_font = None
        self.stats = {
            "file": str(output_file),
            "source_dir": str(source_dir),
            "icons": {}
        }
        
        # Load config
        if not self._load_config(config_path):
            raise ValueError(f"Failed to load config: {config_path}")
        
        # Load fonts if needed
        if add_labels:
            self._setup_fonts()
    
    def _load_config(self, config_path):
        """Load icon coordinate configuration from JSON."""
        config_path = Path(config_path)
        
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
    
    def _setup_fonts(self):
        """Try to load system fonts, prefer bold variants, fall back to default."""
        # Try common font locations - prefer bold variants
        font_paths = [
            "C:\\Windows\\Fonts\\arialbd.ttf",  # Windows bold
            "C:\\Windows\\Fonts\\arial.ttf",    # Windows regular
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux bold
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux regular
            "/Library/Fonts/Arial Bold.ttf",  # macOS bold
            "/Library/Fonts/Arial.ttf",  # macOS regular
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.label_font = ImageFont.truetype(font_path, 9)
                    is_bold = "bold" in font_path.lower() or "bd" in font_path.lower()
                    font_type = "Bold" if is_bold else "Regular"
                    return True
                except Exception:
                    continue
        
        # Fall back to default font
        try:
            self.label_font = ImageFont.load_default()
            return True
        except Exception:
            print(f"WARNING: Could not load font for labels")
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
        print(f"\n{'='*70}")
        print(f"GENERATING: {self.output_file.name}")
        print(f"{'='*70}")
        
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
        
        # Add text labels next to icons if enabled
        if self.add_labels and self.label_font:
            self._add_text_labels(output_img)
        
        # Save output
        output_img.save(self.output_file)
        print(f"\n[OK] Generated: {self.output_file}")
        
        if self.add_abbreviations:
            print("[OK] Abbreviations added within icons")
        
        if self.add_labels:
            print("[OK] Text labels added next to icons")
        
        return True
    
    def _add_text_labels(self, output_img):
        """Render text labels next to each icon in the output image."""
        draw = ImageDraw.Draw(output_img)
        
        for icon_name, layout in self.MASTER_LAYOUT.items():
            x = layout["x"]
            y = layout["y"]
            abbr = self.ABBREVIATIONS.get(icon_name, icon_name[:3])
            
            # Text position: to the right of icon (icon is 22px wide, +2px spacing)
            text_x = x + 24
            text_y = y + 6  # Vertically try to center with icon
            
            # Render text label
            draw.text(
                (text_x, text_y),
                abbr,
                fill=(0, 0, 0, 255),  # Black text
                font=self.label_font
            )
    
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


def regenerate_icons(variant_dir, config_path, root_path, add_labels=False):
    """Regenerate stat icons for a specific variant.
    
    Args:
        variant_dir: Path to variant directory (e.g., thorne_drak/Options/Icons/Thorne)
        config_path: Path to config JSON file
        root_path: Path to root thorne_drak directory
        add_labels: Whether to add text labels next to icons
    
    Returns:
        (success, variant_name, variant_dir) tuple
    """
    variant_name = variant_dir.name
    output_file = variant_dir / 'staticons01.tga'
    
    print(f"\nProcessing {variant_name}...")
    
    try:
        generator = StatIconGenerator(
            variant_dir,
            config_path,
            output_file,
            add_abbreviations=True,
            add_labels=add_labels
        )
        
        if generator.generate():
            generator.save_stats()
            return True, variant_name, variant_dir
        else:
            return False, variant_name, variant_dir
    
    except Exception as e:
        print(f"ERROR: {variant_name}: {e}")
        import traceback
        traceback.print_exc()
        return False, variant_name, variant_dir


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h', 'help'):
        print("""
Icon Texture Regeneration Tool
===============================

Regenerates stat icon textures from icon variants in Options/Icons/ directory.

USAGE:
    python regen_icons.py --all                      # Auto-discover all variants
    python regen_icons.py <variant> [variant2 ...]  # Specific variants
    python regen_icons.py --help

EXAMPLES:
    # Regenerate ALL variants (auto-discovered from Options/Icons/)
    python regen_icons.py --all
    
    # Single variant - copies to thorne_drak/ and deploys to thorne_dev/
    python regen_icons.py Thorne
    
    # Multiple variants - only Thorne copied to thorne_drak/
    python regen_icons.py Thorne Classic Duxa
    
    # With text labels next to icons (easier to identify during editing)
    python regen_icons.py Thorne --labels
    
    # Show this help message
    python regen_icons.py --help
    python regen_icons.py -h

OPTIONS:
    --all               Auto-discover and regenerate all variants from Options/Icons/
    <variant>           Specific variant name (e.g., Thorne, Classic, Duxa)
    --labels            Add text labels next to each icon (for reference/editing)
    root                Direct regeneration of thorne_drak/ directory

AVAILABLE VARIANTS (auto-discovered):
    Thorne              Primary development variant
    Classic, Duxa       Icon style variants
    Modern, etc.        Other community variants

FEATURES:
    ✓ Auto-discovers all icon variants in Options/Icons/
    ✓ Flexible JSON config for icon coordinate mapping
    ✓ Extracts and resizes icons (22×22)
    ✓ Abbreviation labels WITHIN icons (text overlay)
    ✓ Text labels NEXT TO icons (with --labels option)
    ✓ Placeholder generation for missing icons
    ✓ Smart copyback (single→thorne_drak/, multi→Thorne only)
    ✓ Automatic deployment to thorne_dev/ for immediate testing

WORKFLOW:
    1. Edit source icons: thorne_drak/Options/Icons/Thorne/gemicons*.tga
    2. Run: python regen_icons.py --all  (or: python regen_icons.py Thorne)
    3. Test: /loadskin thorne_drak

OPTIONS:
    --all               Auto-discover and regenerate all variants from Options/Icons/
    <variant>           Specific variant name (e.g., Thorne, Classic, Duxa)
    --labels            Add text labels next to each icon (for reference/editing)
    root                Direct regeneration of thorne_drak/ directory

For detailed documentation, see: .bin/regen_icons.md
        """)
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    # Extract options from argv
    add_labels = '--labels' in sys.argv
    if add_labels:
        sys.argv.remove('--labels')
    
    base_path = Path(__file__).parent.parent / 'thorne_drak' / 'Options' / 'Icons'
    root_path = Path(__file__).parent.parent / 'thorne_drak'
    config_path = Path(__file__).parent / 'regen_icons.json'
    
    # Verify config exists
    if not config_path.exists():
        print(f"ERROR: Config file not found at {config_path}")
        sys.exit(1)
    
    # Determine which variants to process
    if '--all' in sys.argv:
        # Auto-discover all variants from Icons directory
        if base_path.exists():
            variant_names = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
            print(f"Auto-discovered {len(variant_names)} variants: {', '.join(variant_names)}\n")
        else:
            print(f"ERROR: Icons directory not found at {base_path}")
            sys.exit(1)
    else:
        # Use explicitly specified variants
        variant_names = sys.argv[1:]
    
    regenerated_variants = []  # Track which variants were successfully regenerated
    success_count = 0
    
    for variant in variant_names:
        if variant.lower() == 'root':
            # Direct regeneration of thorne_drak/ directory
            print(f"\nProcessing root (thorne_drak/)...")
            output_file = root_path / 'staticons01.tga'
            try:
                generator = StatIconGenerator(
                    root_path,
                    config_path,
                    output_file,
                    add_abbreviations=True,
                    add_labels=add_labels
                )
                if generator.generate():
                    generator.save_stats()
                    success_count += 1
            except Exception as e:
                print(f"ERROR: root regeneration failed: {e}")
        else:
            variant_path = base_path / variant
            
            if variant_path.exists():
                success, variant_name, path = regenerate_icons(variant_path, config_path, root_path, add_labels=add_labels)
                if success:
                    success_count += 1
                    regenerated_variants.append((variant_name, path))
            else:
                print(f"ERROR: Variant directory not found: {variant_path}")
    
    # Logic: single variant → copy that one; multiple variants → copy only Thorne
    variants_to_copy = []
    
    if len(regenerated_variants) == 1 and regenerated_variants[0][0].lower() != 'root':
        # Single variant (not root) - copy it
        variants_to_copy = regenerated_variants
    elif len(regenerated_variants) > 1:
        # Multiple variants - only copy Thorne if it was regenerated
        variants_to_copy = [(name, path) for name, path in regenerated_variants if name.lower() == 'thorne']
    
    if variants_to_copy:
        print(f"\n{'='*70}")
        print(f"Copying regenerated files back to thorne_drak/...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            src = variant_path / 'staticons01.tga'
            dst = root_path / 'staticons01.tga'
            
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Copied {variant_name} stat icons to thorne_drak/")
    
    # Also copy to thorne_dev for immediate testing
    thorne_dev_path = Path('C:\\TAKP\\uifiles\\thorne_dev')
    if thorne_dev_path.exists():
        print(f"\n{'='*70}")
        print(f"Deploying to thorne_dev for testing...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            src = variant_path / 'staticons01.tga'
            dst = thorne_dev_path / 'staticons01.tga'
            
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Deployed {variant_name} stat icons to thorne_dev/")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: {success_count}/{len(variant_names)} variant(s) regenerated successfully")
    print(f"{'='*70}")
    
    if variants_to_copy:
        print(f"\nReady to test in-game with: /loadskin thorne_drak")
    else:
        print(f"\nNote: No files copied to thorne_drak/")
        if success_count > 1:
            print(f"(Multiple variants regenerated - only Thorne variant would be copied)")
    
    sys.exit(0)
