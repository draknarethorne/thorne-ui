[← Back to Development Guide](../../DEVELOPMENT.md#development-phases)

# Phase 7: Integration & Asset Consolidation

**Status**: NOT PLANNED  
**Priority**: Low (post-Phase 6)  
**Target Completion**: TBD

## Objectives

- Consolidate icon assets (reduce duplication)
- Standardize button templates across windows
- Create reusable UI component library

## Planned Improvements

### Asset Consolidation

- **Central Assets Folder**: Create shared graphics directory
- **Icon Modernization**: Audit and optimize all icon assets
- **TGA Optimization**: Review file sizes, compression, dimensions
- **Remove Duplicates**: Identify identical assets across Options variants
- **Texture Atlas**: Consider consolidating small icons into single texture sheet

### Template Standardization

- **Button Templates**: Document all button types (A_BtnNormal, A_BtnPressed, A_BtnFlyby)
- **Gauge Templates**: Consolidate tall/short gauge variants
- **Window Frames**: Standardize WDT_Rounded and other frame templates
- **Animation Library**: Create central animation definition reference

### Component Library

- **Reusable Patterns**: Document subwindow patterns (Stats Zone, Equipment Grid, etc.)
- **Layout Utilities**: Create template snippets for common layouts
- **Color Palette**: Formalize color scheme with hex/RGB values
- **Spacing Guide**: Document standard spacing units (14px, 17px, 42px, etc.)

### Build/Validation Scripts

- **Asset Reference Validator**: Check all XML texture references resolve to existing TGA files
- **Template Validator**: Verify all DrawTemplate references exist in animations
- **Color Consistency Checker**: Flag colors outside canonical palette
- **Dead Code Detector**: Identify unused elements in XML files

---

## Technical Approach

### Asset Audit Process

1. Scan all .tga files across main directory and Options variants
2. Generate MD5 checksums to identify duplicates
3. Create asset inventory spreadsheet (name, size, usage count, locations)
4. Prioritize consolidation based on file size × usage count
5. Move shared assets to central directory
6. Update XML references across all affected files

### Template Documentation

1. Extract all `<Animation>` definitions from EQUI_Animations.xml
2. Categorize by type (gauges, buttons, frames, icons)
3. Create Markdown reference with screenshots/examples
4. Document required textures and properties for each template
5. Add usage examples and best practices

### Build Automation

**Python Scripts**:
- `validate_assets.py`: Check TGA references, report missing files
- `consolidate_duplicates.py`: Identify and merge duplicate assets
- `generate_docs.py`: Auto-generate template documentation from XML
- `check_color_palette.py`: Flag non-standard colors in XML files

---

## Success Criteria

- ✅ Asset duplication reduced by >50% (measured by total MB)
- ✅ All template types documented with usage examples
- ✅ Build scripts validate 100% of asset references
- ✅ Component library enables rapid Options variant creation
- ✅ Visual consistency maintained across all windows

---

## Dependencies

- **Phase 3.7**: Template standardization foundation
- **Phase 3.9**: Inventory redesign patterns (subwindows, zones)
- **Phase 6**: Container variant implementation (Options pattern maturity)

---

[← Back to Phases](README.md) | [Development Guide](../../DEVELOPMENT.md) | [Standards](../../.docs/STANDARDS.md)
