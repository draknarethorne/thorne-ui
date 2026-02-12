#!/usr/bin/env python3
"""
Convert gauge_pieces PNG files (mislabeled as .tga) to proper TGA format
"""

from PIL import Image
import os

# Files to convert
files_to_fix = [
    r"c:\TAKP\uifiles\thorne_drak\gauge_pieces01.tga",
    r"c:\TAKP\uifiles\thorne_drak\gauge_pieces01_tall.tga",
    r"c:\TAKP\uifiles\thorne_drak\Options\Gauges\gauge_pieces01.tga",
    r"c:\TAKP\uifiles\thorne_drak\Options\Gauges\gauge_pieces01_tall.tga",
]

def convert_to_tga(file_path):
    """Convert PNG file (mislabeled as .tga) to proper TGA format"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Open the PNG data (even though it has .tga extension)
        img = Image.open(file_path)
        
        # Convert to RGBA if needed (TGA supports RGBA)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Save as proper TGA format
        img.save(file_path, format='TGA')
        
        print(f"✓ Successfully converted: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error converting {file_path}: {e}")
        return False

def main():
    print("=" * 60)
    print("TGA File Converter - PNG to TGA Format")
    print("=" * 60)
    
    success_count = 0
    for file_path in files_to_fix:
        if convert_to_tga(file_path):
            success_count += 1
    
    print("=" * 60)
    print(f"Conversion complete: {success_count}/{len(files_to_fix)} files fixed")
    print("=" * 60)

if __name__ == "__main__":
    main()
