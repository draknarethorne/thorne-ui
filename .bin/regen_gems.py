#!/usr/bin/env python3
"""
Generate Gemicons and Spellicons from Spell Icon Sources + Auto-regenerate Staticons

Complete icon pipeline: spells (40×40) → gemicons (24×24) + spellicons (22×22) → staticons (22×22)

Features:
  - Reads spellsXX.tga files (40×40 icons, 6 rows × 6 columns)
    - Scales to gemiconsXX.tga (24×24 icons, 10 rows × 10 columns)
        - Default: transparent 1px border (22×22 icon inset at 1,1)
  - Scales to spelliconsXX.tga (22×22 icons, 10 rows × 10 columns) - clean, no borders
  - Auto-regenerates staticons01.tga from new spellicons
    - Optional --border mode for gemicons ONLY: transparent (default), black, blend
  - High-quality LANCZOS resampling + SHARPEN filter
  - Supports all icon variants (Classic, Duxa, Infiniti, Steamworks, Thorne, WoW)
  - Smart copyback: single variant → copy to thorne_drak/, multiple → Thorne only
  - Automatic deployment to thorne_dev/ for immediate testing

USAGE:
    python regen_gems.py --all                    # All variants
    python regen_gems.py Thorne                   # Single variant  
    python regen_gems.py Thorne Classic           # Multiple variants
    python regen_gems.py --all --border blend     # All variants with blended borders on gemicons
    python regen_gems.py --help

EXAMPLES:
    # Regenerate all variants with blended borders on gemicons only, auto-copy to thorne_drak and thorne_dev
    python regen_gems.py --all --border blend
    
    # Just Thorne variant with borders on gemicons
    python regen_gems.py Thorne --border blend
"""

import sys
import json
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageFilter


class GemIconGenerator:
    """Generate gemicons and tinyicons from spell icon sources."""
    
    # Spell file layout: 40×40 icons, 6 rows × 6 columns in 256×256 image
    SPELL_ICON_SIZE = 40
    SPELL_GRID_SIZE = 6  # 6×6 grid
    SPELL_ICONS_PER_FILE = 36  # 6×6
    
    # Gemicon output: 24×24 icons, 10 rows × 10 columns in 256×256 image  
    GEM_ICON_SIZE = 24
    GEM_GRID_SIZE = 10  # 10×10 grid
    GEM_ICONS_PER_FILE = 100  # 10×10
    
    # Spellicon output: 22×22 icons, 10 rows × 10 columns in 256×256 image
    SMALL_ICON_SIZE = 22
    SMALL_GRID_SIZE = 10  # 10×10 grid
    SMALL_ICONS_PER_FILE = 100  # 10×10
    
    # Output image size
    OUTPUT_SIZE = 256
    
    def __init__(self, variant_dir, border_mode="transparent"):
        """
        Initialize the generator.
        
        Args:
            variant_dir: Path to icon variant directory (e.g., thorne_drak/Options/Icons/Thorne)
            border_mode: transparent (default), black, or blend
        """
        self.variant_dir = Path(variant_dir)
        self.variant_name = self.variant_dir.name
        self.border_mode = border_mode
        self.stats = {
            "variant": self.variant_name,
            "spell_files_processed": 0,
            "gemicon_files_created": 0,
            "spellicon_files_created": 0,
            "icons_scaled": 0,
            "border_mode": border_mode
        }
    
    def _calculate_spell_positions(self):
        """Calculate icon positions in spell files (6×6 grid, 40×40 icons)."""
        positions = []
        # Icons start at (0,0) with buffer on right and bottom
        # 6×40 = 240, leaving 16 pixels buffer on right/bottom in 256×256 image
        
        for row in range(self.SPELL_GRID_SIZE):
            for col in range(self.SPELL_GRID_SIZE):
                x = col * self.SPELL_ICON_SIZE
                y = row * self.SPELL_ICON_SIZE
                positions.append((x, y))
        
        return positions
    
    def _calculate_gem_positions(self, icon_size, grid_size):
        """Calculate icon positions for output files (10×10 grid)."""
        positions = []
        # Icons start at (0,0) with buffer on right and bottom
        # 10×24 = 240, leaving 16 pixels buffer on right/bottom in 256×256 image
        # 10×22 = 220, leaving 36 pixels buffer on right/bottom in 256×256 image
        
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * icon_size
                y = row * icon_size
                positions.append((x, y))
        
        return positions
    
    def _find_spell_files(self):
        """Find all spellsXX.tga files in variant directory."""
        spell_files = sorted(self.variant_dir.glob("spells*.tga"))
        return spell_files
    
    def _extract_icons_from_spell(self, spell_file):
        """Extract all 36 icons from a spell file."""
        icons = []
        positions = self._calculate_spell_positions()
        
        try:
            img = Image.open(spell_file).convert("RGBA")
            
            for x, y in positions:
                icon = img.crop((x, y, x + self.SPELL_ICON_SIZE, y + self.SPELL_ICON_SIZE))
                icons.append(icon)
            
            return icons
        except Exception as e:
            print(f"  ERROR: Failed to extract icons from {spell_file.name}: {e}")
            return []
    
    def _add_blended_border_to_icon(self, icon):
        """Add 1px darkened border around an icon (blends with existing colors)."""
        width, height = icon.size
        pixels = icon.load()
        
        # Darken factor (0.6 = darken to 60% of original brightness)
        darken_factor = 0.6
        
        # Darken top and bottom edges
        for x in range(width):
            # Top edge (y=0)
            r, g, b, a = pixels[x, 0]
            pixels[x, 0] = (int(r * darken_factor), int(g * darken_factor), 
                           int(b * darken_factor), a)
            # Bottom edge (y=height-1)
            r, g, b, a = pixels[x, height-1]
            pixels[x, height-1] = (int(r * darken_factor), int(g * darken_factor), 
                                  int(b * darken_factor), a)
        
        # Darken left and right edges
        for y in range(height):
            # Left edge (x=0)
            r, g, b, a = pixels[0, y]
            pixels[0, y] = (int(r * darken_factor), int(g * darken_factor), 
                           int(b * darken_factor), a)
            # Right edge (x=width-1)
            r, g, b, a = pixels[width-1, y]
            pixels[width-1, y] = (int(r * darken_factor), int(g * darken_factor), 
                                 int(b * darken_factor), a)
        
        return icon

    def _add_black_border_to_icon(self, icon):
        """Add 1px solid black border around an icon."""
        width, height = icon.size
        pixels = icon.load()
        for x in range(width):
            pixels[x, 0] = (0, 0, 0, 255)
            pixels[x, height - 1] = (0, 0, 0, 255)
        for y in range(height):
            pixels[0, y] = (0, 0, 0, 255)
            pixels[width - 1, y] = (0, 0, 0, 255)
        return icon

    def _create_gem_icon(self, icon):
        """Create a 24×24 gem icon with a 1px transparent border (22×22 content)."""
        # Scale to 22×22 (24 minus 2px for border)
        scaled_icon = icon.resize((self.GEM_ICON_SIZE - 2, self.GEM_ICON_SIZE - 2), Image.Resampling.LANCZOS)
        scaled_icon = scaled_icon.filter(ImageFilter.SHARPEN)

        # Apply optional border to the icon content (not the transparent border)
        if self.border_mode == "blend":
            scaled_icon = self._add_blended_border_to_icon(scaled_icon)
        elif self.border_mode == "black":
            scaled_icon = self._add_black_border_to_icon(scaled_icon)

        # Create 24×24 with transparent border, paste at (1,1)
        output_icon = Image.new("RGBA", (self.GEM_ICON_SIZE, self.GEM_ICON_SIZE), (0, 0, 0, 0))
        output_icon.paste(scaled_icon, (1, 1))
        return output_icon
    
    def _scale_icons(self, icons, target_size, add_border=False):
        """Scale icons to target size using high-quality resampling with sharpening."""
        scaled = []
        for icon in icons:
            # Scale using LANCZOS for high quality
            scaled_icon = icon.resize((target_size, target_size), Image.Resampling.LANCZOS)
            # Apply sharpening to compensate for downscaling blur
            scaled_icon = scaled_icon.filter(ImageFilter.SHARPEN)
            # Optionally add blended border
            if add_border:
                scaled_icon = self._add_blended_border_to_icon(scaled_icon)
            scaled.append(scaled_icon)
        return scaled
    
    def _create_output_file(self, icons, output_path, icon_size, grid_size):
        """Create output file from scaled icons."""
        # Create blank output image
        output_img = Image.new("RGBA", (self.OUTPUT_SIZE, self.OUTPUT_SIZE), (0, 0, 0, 0))
        
        # Calculate positions
        positions = self._calculate_gem_positions(icon_size, grid_size)
        
        # Place icons
        for i, icon in enumerate(icons):
            if i >= len(positions):
                break
            x, y = positions[i]
            output_img.paste(icon, (x, y))
        
        # Save
        output_img.save(output_path, format="TGA")
    
    def _group_icons_for_output(self, all_icons, icons_per_file):
        """Group icons into chunks for output files."""
        grouped = []
        for i in range(0, len(all_icons), icons_per_file):
            chunk = all_icons[i:i + icons_per_file]
            grouped.append(chunk)
        return grouped
    
    def generate(self):
        """Generate gemicons and tinyicons from spell sources."""
        print(f"\n{'='*70}")
        print(f"GENERATING ICONS FROM SPELLS: {self.variant_name}")
        print(f"{'='*70}")
        
        # Find spell files
        spell_files = self._find_spell_files()
        if not spell_files:
            print(f"  ERROR: No spell files found in {self.variant_dir}")
            return False
        
        print(f"  Found {len(spell_files)} spell files")
        
        # Extract all icons from all spell files
        all_icons = []
        for spell_file in spell_files:
            print(f"  Processing {spell_file.name}...")
            icons = self._extract_icons_from_spell(spell_file)
            if icons:
                all_icons.extend(icons)
                self.stats["spell_files_processed"] += 1
        
        total_icons = len(all_icons)
        print(f"  Extracted {total_icons} icons total")
        
        if not all_icons:
            print("  ERROR: No icons extracted")
            return False
        
        # Generate gemicons (24×24)
        border_msg = " with transparent border" if self.border_mode == "transparent" else f" with {self.border_mode} border"
        print(f"\n  Scaling to gemicons (24×24){border_msg}...")
        gem_icons = [self._create_gem_icon(icon) for icon in all_icons]
        gem_groups = self._group_icons_for_output(gem_icons, self.GEM_ICONS_PER_FILE)
        
        for i, icons in enumerate(gem_groups, start=1):
            output_file = self.variant_dir / f"gemicons{i:02d}.tga"
            self._create_output_file(icons, output_file, self.GEM_ICON_SIZE, self.GEM_GRID_SIZE)
            print(f"    Created {output_file.name} ({len(icons)} icons)")
            self.stats["gemicon_files_created"] += 1
        
        # Generate spellicons (22×22)
        print("\n  Scaling to spellicons (22×22)...")
        spell_icons = self._scale_icons(all_icons, self.SMALL_ICON_SIZE)
        spell_groups = self._group_icons_for_output(spell_icons, self.SMALL_ICONS_PER_FILE)
        
        for i, icons in enumerate(spell_groups, start=1):
            output_file = self.variant_dir / f"spellicons{i:02d}.tga"
            self._create_output_file(icons, output_file, self.SMALL_ICON_SIZE, self.SMALL_GRID_SIZE)
            print(f"    Created {output_file.name} ({len(icons)} icons)")
            self.stats["spellicon_files_created"] += 1
        
        self.stats["icons_scaled"] = total_icons
        
        # Save stats
        stats_file = self.variant_dir / "regen_gems_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\n  Statistics saved to {stats_file.name}")
        print(f"  [OK] Gemicons complete: {self.variant_name}")
        
        return True
    
    def regenerate_staticons(self, script_dir):
        """Regenerate staticons from the newly created gemicons."""
        print(f"\n  Regenerating staticons for {self.variant_name}...")
        
        regen_icons_script = script_dir / "regen_icons.py"
        if not regen_icons_script.exists():
            print(f"  WARNING: {regen_icons_script.name} not found, skipping staticons")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, str(regen_icons_script), self.variant_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"  [OK] Staticons complete: {self.variant_name}")
                return True
            else:
                print("  ERROR: Staticon generation failed")
                if result.stderr:
                    print(f"  {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("  ERROR: Staticon generation timed out")
            return False
        except Exception as e:
            print(f"  ERROR: Failed to run staticon generation: {e}")
            return False


def discover_variants(base_dir):
    """Auto-discover icon variants from Options/Icons directory."""
    variants = []
    icons_dir = Path(base_dir) / "thorne_drak" / "Options" / "Icons"
    
    if not icons_dir.exists():
        return variants
    
    for item in sorted(icons_dir.iterdir()):
        if item.is_dir():
            # Check if it has spell files
            if list(item.glob("spells*.tga")):
                variants.append(item.name)
    
    return variants


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate gemicons and tinyicons from spell icon sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python regen_gems.py --all              # All variants
  python regen_gems.py Thorne             # Single variant
  python regen_gems.py Thorne Classic     # Multiple variants
        """
    )
    
    parser.add_argument(
        "variants",
        nargs="*",
        help="Icon variant names (e.g., Thorne, Classic, Duxa)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all discovered variants"
    )
    
    parser.add_argument(
        "--border",
        nargs="?",
        const="blend",
        default="transparent",
        choices=["transparent", "black", "blend"],
        help="Gemicon border mode: transparent (default), black, blend. Use --border for blend."
    )
    
    args = parser.parse_args()
    
    # Determine base directory
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    # Discover or use specified variants
    if args.all:
        variants = discover_variants(base_dir)
        if not variants:
            print("ERROR: No variants discovered in thorne_drak/Options/Icons/")
            return 1
        print(f"Auto-discovered {len(variants)} variants: {', '.join(variants)}")
    elif args.variants:
        variants = args.variants
    else:
        parser.print_help()
        return 1
    
    # Process each variant
    success_count = 0
    total_count = len(variants)
    regenerated_variants = []  # Track which variants were successfully regenerated
    
    for variant in variants:
        variant_dir = base_dir / "thorne_drak" / "Options" / "Icons" / variant
        
        if not variant_dir.exists():
            print(f"\nERROR: Variant directory not found: {variant_dir}")
            continue
        
        generator = GemIconGenerator(variant_dir, border_mode=args.border)
        if generator.generate():
            # Also regenerate staticons from the new gemicons
            generator.regenerate_staticons(script_dir)
            success_count += 1
            regenerated_variants.append((variant, variant_dir))
    
    # Logic: single variant → copy that one; multiple variants → copy only Thorne
    variants_to_copy = []
    root_path = base_dir / "thorne_drak"
    
    if len(regenerated_variants) == 1:
        # Single variant - copy it
        variants_to_copy = regenerated_variants
    elif len(regenerated_variants) > 1:
        # Multiple variants - only copy Thorne if it was regenerated
        for name, path in regenerated_variants:
            if name.lower() == 'thorne':
                variants_to_copy = [(name, path)]
                break  # Only select first match
    
    if variants_to_copy:
        print(f"\n{'='*70}")
        print("Copying regenerated files back to thorne_drak/...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            # Copy gemicons and spellicons only
            for i in range(1, 4):
                src = variant_path / f"gemicons{i:02d}.tga"
                dst = root_path / f"gemicons{i:02d}.tga"
                if src.exists():
                    shutil.copy2(src, dst)
                src = variant_path / f"spellicons{i:02d}.tga"
                dst = root_path / f"spellicons{i:02d}.tga"
                if src.exists():
                    shutil.copy2(src, dst)
            print(f"  Copied {variant_name} gemicons/spellicons to thorne_drak/")
    
    # Also copy to thorne_dev for immediate testing
    thorne_dev_path = Path('C:\\TAKP\\uifiles\\thorne_dev')
    if thorne_dev_path.exists() and variants_to_copy:
        print(f"\n{'='*70}")
        print("Deploying to thorne_dev for testing...")
        print(f"{'='*70}")
        for variant_name, variant_path in variants_to_copy:
            # Copy gemicons and spellicons only
            for i in range(1, 4):
                src = variant_path / f"gemicons{i:02d}.tga"
                dst = thorne_dev_path / f"gemicons{i:02d}.tga"
                if src.exists():
                    shutil.copy2(src, dst)
                src = variant_path / f"spellicons{i:02d}.tga"
                dst = thorne_dev_path / f"spellicons{i:02d}.tga"
                if src.exists():
                    shutil.copy2(src, dst)
            print(f"  Deployed {variant_name} gemicons/spellicons to thorne_dev/")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: {success_count}/{total_count} variants processed successfully")
    print(f"{'='*70}\n")
    
    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
