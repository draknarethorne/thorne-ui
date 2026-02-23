#!/usr/bin/env python3
"""
Generate Skeletal README - Create starter README.md templates for new window variants.

Generates a basic README.md template when adding a new window variant option.
These skeletal READMEs serve as placeholders until the agent performs deep analysis.

Usage:
    python generate_skeletal_readme.py --window Actions --variant "Custom Layout"
    python generate_skeletal_readme.py --window Target --variant "New Variant"
    
This generates a template that the agent can expand with detailed analysis.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

SKELETAL_TEMPLATE = """# {window_name} - {variant_name}

## Overview

This variant of the {window_name} window provides {description_placeholder}.

## Key Features

- Feature 1
- Feature 2
- Feature 3

## File Information

- **XML File**: {xml_file}
- **Location**: `Options/{window_name}/{variant_name}/`
- **Created**: {created_date}

## Description

[Detailed description to be added by agent analysis]

## Configuration

[Configuration details to be added by agent analysis]

## Element Specifications

[Element table and specifications to be added by agent analysis]

## Usage Notes

[Usage notes to be added by agent analysis]
"""

class SkeletalReadmeGenerator:
    def __init__(self, workspace_root):
        self.workspace_root = Path(workspace_root)
        self.options_root = self.workspace_root / "thorne_drak" / "Options"
    
    def generate(self, window_name, variant_name, xml_file):
        """Generate skeletal README for a variant."""
        # Validate window exists
        window_dir = self.options_root / window_name
        if not window_dir.exists():
            print(f"ERROR: Window directory not found: {window_dir}")
            return False
        
        # Create variant directory
        variant_dir = window_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        
        # Create README
        readme_path = variant_dir / "README.md"
        if readme_path.exists():
            print(f"WARNING: README already exists at {readme_path}")
            return False
        
        # Generate content
        content = SKELETAL_TEMPLATE.format(
            window_name=window_name,
            variant_name=variant_name,
            description_placeholder=f"a custom configuration of the {window_name} window",
            xml_file=xml_file,
            created_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Write file
        try:
            with open(readme_path, 'w') as f:
                f.write(content)
            print(f"[OK] Skeletal README created: {readme_path.relative_to(self.workspace_root)}")
            print(f"     Lines: {len(content.splitlines())}")
            print(f"     Ready for agent deep analysis")
            return True
        except Exception as e:
            print(f"ERROR: Failed to create README: {str(e)}")
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="options_generate_readme.py",
        description="""
Generate Skeletal README Templates for UI Variants

Auto-creates README.md template files for new window variants with standard
sections, descriptions, and metadata. Useful for getting organized documentation
quickly without manual formatting.

FEATURES:
  ✓ Standard README structure with sections for all variants
  ✓ Automatic metadata (window name, variant name, XML file)
  ✓ Ready-to-edit templates with placeholder text
  ✓ Preserves existing files (won't overwrite)
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # Generate for Player window Custom Layout variant
  python .bin/options_generate_readme.py \\
    --window Player \\
    --variant "Custom Layout"

  # With custom XML filename
  python .bin/options_generate_readme.py \\
    --window Target \\
    --variant "Minimal HUD" \\
    --xml EQUI_TargetWindow.xml

  # Generate for Inventory variant
  python .bin/options_generate_readme.py \\
    --window Inventory \\
    --variant "Grid Layout 6x4"

CREATED:\
    <Window>/<Variant>/README.md with:
        - Overview of variant purpose
        - Key modifications from Thorne
        - Customization instructions
        - Usage recommendations
"""
    )
    
    parser.add_argument(
        "--window", "-w",
        required=True,
        metavar="NAME",
        help="Window name (e.g., Player, Target, Inventory)"
    )
    parser.add_argument(
        "--variant", "-v",
        required=True,
        metavar="NAME",
        help="Variant name (e.g., 'Custom Layout', 'Minimal HUD')"
    )
    parser.add_argument(
        "--xml",
        metavar="FILE",
        help="XML filename (default: EQUI_Window.xml)"
    )
    
    args = parser.parse_args()
    
    # Determine workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    # Generate
    generator = SkeletalReadmeGenerator(workspace_root)
    if generator.generate(args.window, args.variant, args.xml or "EQUI_Window.xml"):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
