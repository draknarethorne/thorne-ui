#!/usr/bin/env python3
"""
Generate Master Template Stat Icons
====================================
Creates three stat_icon_pieces files with IDENTICAL layouts:
- pieces01: Icons from vert/window_pieces06.tga + placeholders
- pieces02: Resists from vert-blue/gemicons01.tga (24×24→22×22) + placeholders
- pieces03: Resists from default/gemicons01.tga (24×24→22×22) + placeholders

All files use 256×256 RGBA format with icons at identical coordinates.
This ensures files are swappable without XML coordinate changes.

PLACEHOLDER DESIGN (Vert-Inspired):
-----------------------------------
Placeholders use a dark, subtle design inspired by vert UI:
  - Size: 22×22 pixels (matching icon size)
  - Outer border: 2px solid black (#000000)
  - Fill: Dark gray (#2B2B2B) - matches vert's dark color scheme
  - Inner accent line: 1px mid-gray (#444444) at 1px inset
  - Center: Small hollow square to indicate empty/reserved slot
  - Overall appearance: Looks like a reserved slot in the vert UI style

This design is intentionally visible (not subtle) to help identify which
icons still need to be created/extracted.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json

# Master Template Layout (identical for ALL files)
MASTER_LAYOUT = {
    # Column 1: Player/Combat Stats (X=10)
    "AC":       {"col": 1, "x": 10,  "y": 10,  "row": 1},
    "ATK":      {"col": 1, "x": 10,  "y": 40,  "row": 2},
    "HP":       {"col": 1, "x": 10,  "y": 70,  "row": 3},
    "MANA":     {"col": 1, "x": 10,  "y": 100, "row": 4},
    "STA":      {"col": 1, "x": 10,  "y": 130, "row": 5},
    "Weight":   {"col": 1, "x": 10,  "y": 160, "row": 6},
    
    # Column 2: Resistance Icons (X=90)
    "Fire":     {"col": 2, "x": 90,  "y": 10,  "row": 1},
    "Cold":     {"col": 2, "x": 90,  "y": 40,  "row": 2},
    "Magic":    {"col": 2, "x": 90,  "y": 70,  "row": 3},
    "Poison":   {"col": 2, "x": 90,  "y": 100, "row": 4},
    "Disease":  {"col": 2, "x": 90,  "y": 130, "row": 5},
    "Reserve":  {"col": 2, "x": 90,  "y": 160, "row": 6},
    
    # Column 3: Character Attributes (X=170)
    "STR":      {"col": 3, "x": 170, "y": 10,  "row": 1},
    "INT":      {"col": 3, "x": 170, "y": 40,  "row": 2},
    "WIS":      {"col": 3, "x": 170, "y": 70,  "row": 3},
    "AGI":      {"col": 3, "x": 170, "y": 100, "row": 4},
    "DEX":      {"col": 3, "x": 170, "y": 130, "row": 5},
    "CHA":      {"col": 3, "x": 170, "y": 160, "row": 6},
}

# Source extraction rules for pieces01 (vert icons)
PIECES01_SOURCES = {
    "AC":       {"file": "vert/window_pieces06.tga", "x": 205, "y": 85,  "w": 22, "h": 22},
    "ATK":      {"file": "vert/window_pieces06.tga", "x": 231, "y": 85,  "w": 22, "h": 22},
    "STR":      {"file": "vert/window_pieces06.tga", "x": 179, "y": 85,  "w": 22, "h": 22},
    "WIS":      {"file": "vert/window_pieces06.tga", "x": 205, "y": 111, "w": 22, "h": 22},
    "INT":      {"file": "vert/window_pieces06.tga", "x": 179, "y": 137, "w": 22, "h": 22},
    "Fire":     {"file": "vert/window_pieces06.tga", "x": 231, "y": 137, "w": 22, "h": 22},
    "Cold":     {"file": "vert/window_pieces06.tga", "x": 231, "y": 111, "w": 22, "h": 22},
    "Magic":    {"file": "vert/window_pieces06.tga", "x": 231, "y": 189, "w": 22, "h": 22},
    "Poison":   {"file": "vert/window_pieces06.tga", "x": 231, "y": 215, "w": 22, "h": 22},
    "Disease":  {"file": "vert/window_pieces06.tga", "x": 231, "y": 163, "w": 22, "h": 22},
}

# Source extraction rules for pieces02 (vert-blue gemicons)
PIECES02_SOURCES = {
    "Fire":     {"file": "vert-blue/gemicons01.tga", "x": 48,  "y": 120, "w": 24, "h": 24},
    "Cold":     {"file": "vert-blue/gemicons01.tga", "x": 168, "y": 120, "w": 24, "h": 24},
    "Magic":    {"file": "vert-blue/gemicons01.tga", "x": 216, "y": 144, "w": 24, "h": 24},
    "Poison":   {"file": "vert-blue/gemicons01.tga", "x": 24,  "y": 144, "w": 24, "h": 24},
    "Disease":  {"file": "vert-blue/gemicons01.tga", "x": 120, "y": 144, "w": 24, "h": 24},
}

# Source extraction rules for pieces03 (default gemicons)
PIECES03_SOURCES = {
    "Fire":     {"file": "default/gemicons01.tga", "x": 48,  "y": 120, "w": 24, "h": 24},
    "Cold":     {"file": "default/gemicons01.tga", "x": 168, "y": 120, "w": 24, "h": 24},
    "Magic":    {"file": "default/gemicons01.tga", "x": 216, "y": 144, "w": 24, "h": 24},
    "Poison":   {"file": "default/gemicons01.tga", "x": 24,  "y": 144, "w": 24, "h": 24},
    "Disease":  {"file": "default/gemicons01.tga", "x": 120, "y": 144, "w": 24, "h": 24},
}

def create_placeholder(size=22):
    """Create a dark placeholder icon inspired by vert UI aesthetic"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer border: 2px solid black
    border_color = (0, 0, 0, 255)  # Solid black
    draw.rectangle([0, 0, size-1, size-1], outline=border_color, width=2)
    
    # Fill: Dark gray (#2B2B2B)
    fill_color = (43, 43, 43, 255)  # Dark gray matching vert aesthetic
    draw.rectangle([2, 2, size-3, size-3], fill=fill_color)
    
    # Inner accent line: 1px mid-gray at 1px inset
    accent_color = (68, 68, 68, 255)  # Mid-gray #444444
    draw.rectangle([3, 3, size-4, size-4], outline=accent_color, width=1)
    
    # Center: Small hollow square to show it's a placeholder
    center = size // 2
    box_size = 6
    box_color = (32, 32, 32, 255)  # Slightly darker than fill
    draw.rectangle([center-box_size//2, center-box_size//2, 
                    center+box_size//2, center+box_size//2], 
                   outline=accent_color, width=1)
    
    return img

def extract_and_resize_icon(source_file, x, y, w, h, target_size=22):
    """Extract icon from source and resize to target size if needed"""
    try:
        # Load source file
        full_path = os.path.join(os.path.dirname(__file__), "..", source_file)
        source_img = Image.open(full_path).convert("RGBA")
        
        # Extract icon region
        icon = source_img.crop((x, y, x + w, y + h))
        
        # Resize if needed
        if w != target_size or h != target_size:
            icon = icon.resize((target_size, target_size), Image.Resampling.LANCZOS)
        
        return icon
    except Exception as e:
        print(f"  ⚠ Failed to extract from {source_file} at ({x},{y}): {e}")
        return create_placeholder(target_size)

def generate_stat_icon_file(output_name, sources_dict, description):
    """Generate a single stat icon file using master layout"""
    print(f"\n{'='*70}")
    print(f"Generating: {output_name}")
    print(f"Description: {description}")
    print(f"{'='*70}")
    
    # Create blank 256×256 RGBA template
    output_img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    
    stats = {
        "file": output_name,
        "description": description,
        "size": "256×256 RGBA",
        "icons": {}
    }
    
    # Place all icons according to master layout
    for icon_name, layout in MASTER_LAYOUT.items():
        x = layout["x"]
        y = layout["y"]
        col = layout["col"]
        row = layout["row"]
        
        # Get icon (from source or placeholder)
        if icon_name in sources_dict:
            source = sources_dict[icon_name]
            icon = extract_and_resize_icon(
                source["file"], 
                source["x"], 
                source["y"], 
                source["w"], 
                source["h"]
            )
            icon_type = "extracted"
            source_info = {
                "file": source["file"],
                "original_x": source["x"],
                "original_y": source["y"],
                "original_size": f"{source['w']}×{source['h']}"
            }
            print(f"  ✓ {icon_name:8} at ({x:3},{y:3}) - extracted from {source['file']}")
        else:
            icon = create_placeholder()
            icon_type = "placeholder"
            source_info = None
            print(f"  ○ {icon_name:8} at ({x:3},{y:3}) - PLACEHOLDER")
        
        # Paste icon at master layout position
        output_img.paste(icon, (x, y), icon)
        
        # Record in stats
        stats["icons"][icon_name] = {
            "position": {"x": x, "y": y},
            "column": col,
            "row": row,
            "size": "22×22",
            "type": icon_type,
            "source": source_info
        }
    
    # Save output file
    output_path = os.path.join(os.path.dirname(__file__), "..", "thorne_drak", output_name)
    output_img.save(output_path)
    print(f"\n  ✅ Saved: {output_path}")
    
    return stats

def generate_all_files():
    """Generate all three stat icon files"""
    print("\n" + "="*70)
    print("MASTER STAT ICON TEMPLATE GENERATOR")
    print("="*70)
    print("\nThis script creates THREE stat icon files with IDENTICAL layouts:")
    print("  - stat_icon_pieces01.tga (vert icons)")
    print("  - stat_icon_pieces02.tga (vert-blue resist icons)")
    print("  - stat_icon_pieces03.tga (default resist icons)")
    print("\nAll files share the same coordinate system, making them swappable.")
    print("="*70)
    
    all_stats = {}
    
    # Generate pieces01 (vert icons)
    stats01 = generate_stat_icon_file(
        "stat_icon_pieces01.tga",
        PIECES01_SOURCES,
        "Icons from vert/window_pieces06.tga (22×22 native size)"
    )
    all_stats["stat_icon_pieces01.tga"] = stats01
    
    # Generate pieces02 (vert-blue gemicons)
    stats02 = generate_stat_icon_file(
        "stat_icon_pieces02.tga",
        PIECES02_SOURCES,
        "Resist icons from vert-blue/gemicons01.tga (24×24 resized to 22×22)"
    )
    all_stats["stat_icon_pieces02.tga"] = stats02
    
    # Generate pieces03 (default gemicons)
    stats03 = generate_stat_icon_file(
        "stat_icon_pieces03.tga",
        PIECES03_SOURCES,
        "Resist icons from default/gemicons01.tga (24×24 resized to 22×22)"
    )
    all_stats["stat_icon_pieces03.tga"] = stats03
    
    # Save master coordinates JSON
    json_path = os.path.join(os.path.dirname(__file__), "..", ".development", "stat-icons-coordinates.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, "w") as f:
        json.dump({
            "description": "Master stat icon coordinate mapping",
            "template_size": "256×256 RGBA",
            "icon_size": "22×22",
            "layout": MASTER_LAYOUT,
            "files": all_stats
        }, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Master coordinates saved: {json_path}")
    print(f"{'='*70}")
    
    # Print summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)
    print("\nFiles created:")
    print("  ✓ thorne_drak/stat_icon_pieces01.tga")
    print("  ✓ thorne_drak/stat_icon_pieces02.tga")
    print("  ✓ thorne_drak/stat_icon_pieces03.tga")
    print("  ✓ .development/stat-icons-coordinates.json")
    
    # Count real vs placeholder icons
    for filename, stats in all_stats.items():
        real_count = sum(1 for icon in stats["icons"].values() if icon["type"] == "extracted")
        placeholder_count = sum(1 for icon in stats["icons"].values() if icon["type"] == "placeholder")
        print(f"\n{filename}:")
        print(f"  - Real icons: {real_count}")
        print(f"  - Placeholders: {placeholder_count}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    generate_all_files()
