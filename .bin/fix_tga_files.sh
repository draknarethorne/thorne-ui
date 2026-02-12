#!/bin/bash
# fix_tga_files.sh
# Wrapper script for fix_tga_files.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/fix_tga_files.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: fix_tga_files.py not found in $SCRIPT_DIR"
    exit 1
fi

# If no arguments provided, show help
if [ $# -eq 0 ]; then
    python3 "$PYTHON_SCRIPT"
    exit
fi

# Pass arguments to Python script
python3 "$PYTHON_SCRIPT" "$@"
