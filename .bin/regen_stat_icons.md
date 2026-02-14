# Stat Icon Texture Regeneration Guide

**Script:** `regen_stat_icons.py`  
**Purpose:** Generate stat icon texture files from any icon variant  
**Status:** Production-ready

## Quick Start

Extract stat icons from an icon variant and generate texture file:

```bash
# Basic usage (Classic variant, default config)
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Classic \
  --output thorne_drak/stat_icon_pieces01.tga

# With abbreviation labels
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Classic \
  --output thorne_drak/stat_icon_pieces01.tga \
  --add-abbreviations

# Show help
python regen_stat_icons.py --help
```

## What It Does

The script automates the icon extraction and texture generation workflow:

1. **Reads Configuration** - Loads JSON config mapping stat names → icon coordinates
2. **Extracts Icons** - Reads gemicon files from source directory
3. **Resizes** - Scales icons to standard 22×22 pixels
4. **Places** - Positions icons in 256×256 master layout template
5. **Labels** - Adds abbreviation text (if `--add-abbreviations` specified)
6. **Generates Placeholders** - Creates graphics for any missing icons
7. **Saves Output** - Writes final texture + metadata JSON

## Command Reference

### Required Arguments

```
--source-dir DIR, -s DIR    Directory containing gemicon files
                            Example: thorne_drak/Options/Icons/Classic
                            
--output FILE, -o FILE      Output path for generated texture
                            Example: thorne_drak/stat_icon_pieces01.tga
```

### Optional Arguments

```
--config FILE, -c FILE      Config with icon coordinate mappings
                            Default: .development/stat-icons-config.json
                            
--add-abbreviations, -a     Include abbreviation labels on icons
                            Default: No labels
```

## Common Workflows

### 1. Generate Classic Variant with Abbreviations

```bash
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Classic \
  --output thorne_drak/stat_icon_pieces01.tga \
  --add-abbreviations
```

**Output:** `stat_icon_pieces01.tga` (256×256 texture with abbreviation labels)

### 2. Generate Custom Variant (Duxa Icons)

```bash
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Duxa \
  --output thorne_drak/stat_icon_pieces_duxa.tga
```

**Output:** `stat_icon_pieces_duxa.tga` (256×256 texture without labels)

### 3. Use Custom Configuration File

```bash
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Modern \
  --config .development/custom-config.json \
  --output thorne_drak/custom_icons.tga
```

**Output:** Generated from your custom config mapping

### 4. One-Off Test with Labels

```bash
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/Test \
  --output /tmp/test_icons.tga \
  --add-abbreviations
```

**Output:** Test texture (useful for quick validation)

## Understanding the Output

### Main Texture File

Generated at the path you specify (e.g., `stat_icon_pieces01.tga`):

- **Dimensions:** 256×256 pixels
- **Format:** TGA (Truevision Graphics Adapter)
- **Content:** 18 stat icons (1 of each stat stat) arranged in master layout
- **Colors:** Full RGBA (supports transparency)

### Master Layout Grid

Icons positioned in 256×256 output:

```
Column 1        Column 2          Column 3
(x=10)          (x=90)            (x=170)
─────────────────────────────────────────────
AC      (y=10)  Fire    (y=10)   STR    (y=10)
ATK     (y=40)  Cold    (y=40)   INT    (y=40)
HP      (y=70)  Magic   (y=70)   WIS    (y=70)
MANA    (y=100) Poison  (y=100)  AGI    (y=100)
STA     (y=130) Disease (y=130)  DEX    (y=130)
Weight  (y=160) Reserve (y=160)  CHA    (y=160)
```

Each icon: 22×22 pixels (after resizing)

### Metadata File (Automatic)

Generated alongside texture with same base name:

```
stat_icon_pieces01.tga
stat_icon_pieces01-stats.json      ← Automatic metadata file
```

**Stats File Contents:**
```json
{
  "file": "thorne_drak/stat_icon_pieces01.tga",
  "source_dir": "thorne_drak/Options/Icons/Classic",
  "icons": {
    "AC": {
      "source": "gemicons01.tga",
      "coordinates": {"x": 0, "y": 0, "w": 24, "h": 24},
      "extracted": true
    },
    "ATK": { ... },
    ...
  }
}
```

**Use Cases:**
- Debugging: Which icons were extracted vs created as placeholders?
- Validation: Verify all icons extracted correctly
- Auditing: Track which gemicon source was used for each stat

## Configuration File Format

The config JSON maps stat names to source icon coordinates:

```json
{
  "AC": {
    "source": "gemicons01.tga",
    "x": 0,
    "y": 0,
    "w": 24,
    "h": 24
  },
  "ATK": {
    "source": "gemicons01.tga",
    "x": 24,
    "y": 0,
    "w": 24,
    "h": 24
  },
  "HP": {
    "source": "gemicons01.tga",
    "x": 48,
    "y": 0,
    "w": 24,
    "h": 24
  },
  ...
}
```

**Key Notes:**
- `source`: Gemicon filename (searched in `--source-dir`)
- `x, y`: Top-left corner coordinates in source gemicon
- `w, h`: Icon dimensions in source (typically 24×24)
- Each stat requires an entry
- Missing entries → placeholder graphic generated

## Abbreviations Reference

Used when `--add-abbreviations` flag specified:

```
AC         → AC      (Armor Class)
ATK        → ATK     (Attack)
HP         → HP      (Hit Points)
MANA       → MP      (Magic Points)
STA        → ST      (Stamina)
Weight     → WT      (Weight)

Fire       → FR      (Fire Resist)
Cold       → CR      (Cold Resist)
Magic      → MR      (Magic Resist)
Poison     → PR      (Poison Resist)
Disease    → DR      (Disease Resist)
Reserve    → RV      (Reserve Stat)

STR        → STR     (Strength)
INT        → INT     (Intelligence)
WIS        → WIS     (Wisdom)
AGI        → AGI     (Agility)
DEX        → DEX     (Dexterity)
CHA        → CHA     (Charisma)
```

## How It Works

### Icon Extraction Process

1. **Load Config** - Read JSON mapping (stat → coordinates)
2. **Scan Source** - Find all gemicon files in source directory
3. **Extract Each Icon:**
   - Open source gemicon file
   - Crop region specified in config (x, y, w, h)
   - Attempt extraction
4. **Placeholder Fallback** - If extraction fails, generate placeholder graphic
5. **Resize** - Scale image to standard 22×22 (preserves aspect ratio)
6. **PNG to TGA** - Handle edge case where .tga is actually PNG format

### Abbreviation Generation (Optional)

If `--add-abbreviations` enabled:

1. **Composite Text** - Add abbreviation text to each icon
2. **Position** - Place text in lower-right corner
3. **Font** - System font, small size
4. **Color** - White text on transparent background
5. **Result** - Labeled 22×22 icons

### Texture Composition

1. **Create Canvas** - 256×256 RGBA image
2. **Base Layer** - Transparent background
3. **Place Icons** - Following master layout coordinates
4. **Save Format** - TGA with RGBA channels

## Troubleshooting

### "Config file not found"
```
ERROR: Failed to load config: .development/stat-icons-config.json
```

**Solution:**
- Verify config file exists at specified path
- Use `--config` to specify custom location
- Check working directory (should be project root)

```bash
# Explicit config path
python regen_stat_icons.py \
  -s thorne_drak/Options/Icons/Classic \
  --config /full/path/to/config.json \
  -o output.tga
```

### "Source directory not found"
```
ERROR: Source directory not found: thorne_drak/Options/Icons/Classic
```

**Solution:**
- Verify icon variant directory exists
- Check variant spelling (case-sensitive)
- Ensure icon files are in correct location

```bash
# Verify directory exists
ls -la thorne_drak/Options/Icons/Classic/

# List available icons
ls thorne_drak/Options/Icons/
```

### "Could not extract icon: AC"
```
WARNING: Could not extract icon AC from gemicons01.tga
```

**Solution:**
- Check config coordinates (x, y, w, h)
- Verify gemicon file exists in source directory
- Icon may be at different coordinates in that variant
- Placeholder graphic will be generated for missing icons

**Debug tip:** Check stats JSON output to see which icons failed extraction:
```json
{
  "AC": {
    "extracted": false,  // ← Failed extraction
    "placeholder": true
  }
}
```

### Output texture appears blank

**Causes:**
1. All icons failed extraction (wrong coordinates)
2. Source directory incorrect
3. Gemicon files not readable

**Solution:**
1. Verify config coordinates match your icon variant
2. Test with known working config
3. Check file permissions on gemicon files

## Advanced Topics

### Custom Icon Variants

Create a new variant with custom icons:

1. Create new directory: `thorne_drak/Options/Icons/MyVariant/`
2. Add gemicon files (with stat icons at specified coordinates)
3. Create or adapt config JSON
4. Run script pointing to new variant:

```bash
python regen_stat_icons.py \
  --source-dir thorne_drak/Options/Icons/MyVariant \
  --config .development/stat-icons-config.json \
  --output thorne_drak/stat_icon_pieces_myvariant.tga
```

### Batch Processing Multiple Variants

Create a batch script to regenerate all variants:

```bash
#!/bin/bash
# Regenerate all icon variants

for variant in Classic Duxa Modern; do
  echo "Processing $variant..."
  python regen_stat_icons.py \
    --source-dir thorne_drak/Options/Icons/$variant \
    --output thorne_drak/stat_icon_pieces_${variant,,}.tga \
    --add-abbreviations
done

echo "All variants regenerated!"
```

### Customizing Master Layout

To change icon positions, modify `MASTER_LAYOUT` in the script:

```python
MASTER_LAYOUT = {
    "AC":       {"x": 10,  "y": 10,  "col": 1, "row": 1},
    "ATK":      {"x": 10,  "y": 40,  "col": 1, "row": 2},
    # ... modify x, y coordinates as needed
}
```

Then regenerate to apply new positions.

## Performance Considerations

- **Speed:** Typically completes in <1 second
- **Memory:** Minimal (single image in memory at a time)
- **Disk I/O:** Limited to reading config + reading source gemicons + writing output
- **No Dependencies:** Only requires PIL/Pillow library

### Optimization Tips

- Use `--add-abbreviations` only when needed (adds processing time)
- Batch process variants outside the script (see Batch Processing section)
- Place source gemicons on fast disk for large operations

## Maintenance Checklist

When maintaining this script:

- [ ] Test with each icon variant (Classic, Duxa, Modern, etc.)
- [ ] Verify abbreviation labels placement and readability
- [ ] Validate output TGA format (should be readable in GIMP, etc.)
- [ ] Keep `--help` documentation up-to-date
- [ ] Update stats.json format if changing output structure
- [ ] Test error handling (missing config, bad coordinates, etc.)
- [ ] Document any new command-line options

## Related Tools

- **[regen_gauges.py](regen_gauges.md)** - Regenerate gauge textures
- **[fix_tga_files.py](README.md)** - Fix TGA format issues
- **[validate_stat_icons.py](README.md)** - Validate icon extraction quality
- **[add_abbreviations_to_textures.py](README.md)** - Add abbreviations to existing textures

## See Also

- `.development/stat-icons-config.json` - Icon coordinate configuration
- `thorne_drak/Options/Icons/` - Available icon variants
- [STANDARDS.md](STANDARDS.md) - Script documentation standards
