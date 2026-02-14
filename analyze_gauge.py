from PIL import Image

gauge_path = r'c:\Thorne-UI\thorne_drak\Options\Gauges\Thorne\gauge_pieces01.tga'
img = Image.open(gauge_path)

print(f"Source gauge dimensions: {img.size}")
print(f"Format: {img.format}, Mode: {img.mode}")

# Crop and examine the lines section (Y:16-23, which is row 3)
lines_section = img.crop((0, 16, img.size[0], 24))
print(f"\nLines section: {lines_section.size}")

# Save a zoomed view for analysis
lines_section.save(r'c:\Thorne-UI\gauge_lines_original.tga')
print("Saved original lines section to gauge_lines_original.tga")

# Now check what it looks like when scaled to 250px with NEAREST
scaled_nearest = lines_section.resize((250, 8), Image.Resampling.NEAREST)
scaled_nearest.save(r'c:\Thorne-UI\gauge_lines_scaled_nearest.tga')
print("Saved scaled (NEAREST) to gauge_lines_scaled_nearest.tga")

# Try with LANCZOS
scaled_lanczos = lines_section.resize((250, 8), Image.Resampling.LANCZOS)
scaled_lanczos.save(r'c:\Thorne-UI\gauge_lines_scaled_lanczos.tga')
print("Saved scaled (LANCZOS) to gauge_lines_scaled_lanczos.tga")

# Print pixel analysis of original lines at specific positions
print("\nPixel analysis of original lines section (sampling middle row):")
pixels = lines_section.load()
width, height = lines_section.size

# Sample positions to see the line structure
sample_positions = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, width-1]
for x in sample_positions:
    if x < width:
        color = pixels[x, 4]  # Sample middle row of lines section
        print(f"  X={x:3d}: {color}")

print("\nAnalyzing consecutive pixels to find line patterns:")
# Look for black vertical lines
consecutive_blacks = 0
last_black_x = -1
for x in range(width):
    color = pixels[x, 4]
    if color[2] == 0 and color[1] == 0 and color[0] == 0 and color[3] == 255:  # Black and opaque
        if consecutive_blacks == 0:
            print(f"  Black line starts at X={x}")
        consecutive_blacks += 1
        last_black_x = x
    elif consecutive_blacks > 0:
        print(f"    Black line: X={x-consecutive_blacks} to X={last_black_x} (width: {consecutive_blacks}px)")
        consecutive_blacks = 0

print("\n[Analysis complete - check the saved .tga files to compare original vs scaled]")
