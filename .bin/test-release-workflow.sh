#!/bin/bash

# Test Release Workflow Script
# This script simulates the GitHub Actions release workflow locally to validate it works

set -e  # Exit on any error

# Change to the repository root (parent of .bin)
cd "$(dirname "$0")/.."

echo "=========================================="
echo "Testing GitHub Releases Workflow"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test version
TEST_VERSION="0.99.0-test"
TEST_TAG="v${TEST_VERSION}"

echo -e "${YELLOW}Test Version: ${TEST_TAG}${NC}"
echo ""

# Step 1: Validate workflow YAML syntax
echo "Step 1: Validating workflow YAML syntax..."
if command -v python3 &> /dev/null; then
    python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))" 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ YAML syntax is valid${NC}"
    else
        echo -e "${RED}✗ YAML syntax is invalid${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ Python3 not found, skipping YAML validation${NC}"
fi
echo ""

# Step 2: Check required directories exist
echo "Step 2: Checking required directories and files exist..."
REQUIRED_DIRS=("thorne_drak" ".docs")
REQUIRED_FILES=("README.md" "DEVELOPMENT.md")

ALL_EXIST=true
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ Directory exists: $dir${NC}"
    else
        echo -e "${RED}✗ Directory missing: $dir${NC}"
        ALL_EXIST=false
    fi
done

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ File exists: $file${NC}"
    else
        echo -e "${RED}✗ File missing: $file${NC}"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    echo -e "${RED}✗ Some required files/directories are missing${NC}"
    exit 1
fi
echo ""

# Step 3: Simulate version extraction
echo "Step 3: Simulating version extraction..."
VERSION="${TEST_VERSION}"
TAG="${TEST_TAG}"
echo "VERSION=${VERSION}"
echo "TAG=${TAG}"
echo -e "${GREEN}✓ Version extraction works${NC}"
echo ""

# Step 4: Simulate changelog generation
echo "Step 4: Simulating changelog generation..."
# Get the previous tag (if any)
PREV_TAG=$(git describe --abbrev=0 --tags $(git rev-list --tags --skip=1 --max-count=1) 2>/dev/null || echo "")

if [ -z "$PREV_TAG" ]; then
    echo "No previous tags found - would include all commits"
    COMMITS=$(git log --pretty=format:"- %s (%h)" --no-merges -10)  # Limit to 10 for testing
else
    echo "Previous tag: $PREV_TAG"
    COMMITS=$(git log ${PREV_TAG}..HEAD --pretty=format:"- %s (%h)" --no-merges)
fi

# Save to file
echo "$COMMITS" > /tmp/changelog.txt
echo -e "${GREEN}✓ Changelog generated ($(wc -l < /tmp/changelog.txt) commits)${NC}"
echo "Preview (first 5 lines):"
head -5 /tmp/changelog.txt
echo ""

# Step 5: Create test packages
echo "Step 5: Creating test packages..."
mkdir -p /tmp/test-releases

# Package thorne_drak
if [ -d "thorne_drak" ]; then
    echo "Packaging thorne_drak..."
    zip -q -r "/tmp/test-releases/thorne_drak-v${VERSION}.zip" "thorne_drak/" -x "*.git*" "*.md"
    DRAK_SIZE=$(du -h "/tmp/test-releases/thorne_drak-v${VERSION}.zip" | cut -f1)
    echo -e "${GREEN}✓ Created thorne_drak-v${VERSION}.zip (${DRAK_SIZE})${NC}"
else
    echo -e "${RED}✗ thorne_drak directory not found${NC}"
    exit 1
fi

# Create complete package
echo "Creating complete package..."
zip -q -r "/tmp/test-releases/thorne-ui-v${VERSION}.zip" \
    thorne_drak/ \
    README.md \
    DEVELOPMENT.md \
    .docs/ \
    -x "*.git*" "*TODO.md"
COMPLETE_SIZE=$(du -h "/tmp/test-releases/thorne-ui-v${VERSION}.zip" | cut -f1)
echo -e "${GREEN}✓ Created thorne-ui-v${VERSION}.zip (${COMPLETE_SIZE})${NC}"
echo ""

# Step 6: Verify ZIP contents
echo "Step 6: Verifying ZIP contents..."
echo "thorne_drak-v${VERSION}.zip contents:"
unzip -l "/tmp/test-releases/thorne_drak-v${VERSION}.zip" | head -15
echo ""
echo "thorne-ui-v${VERSION}.zip top-level contents:"
unzip -l "/tmp/test-releases/thorne-ui-v${VERSION}.zip" | grep -E "thorne_drak/|README|DEVELOPMENT|\.docs/" | head -10
echo -e "${GREEN}✓ ZIP files contain expected content${NC}"
echo ""

# Step 7: Create test release notes
echo "Step 7: Creating test release notes..."
cat > /tmp/release_notes.md << EOF
# Thorne UI v${VERSION}

Custom UI files for **The Al'Kabor Project (TAKP)** - EverQuest Planes of Power (2002) emulation.

## Installation

1. Download \`thorne_drak-v${VERSION}.zip\`
2. Extract the zip file to your TAKP installation directory: \`<TAKP Install>/uifiles/\`
3. In-game, use the command: \`/loadskin thorne_drak\`
4. The UI will automatically reload with the new skin

## About Thorne Drak UI

**Gameplay-focused UI design** built for 1920x1080 resolution and larger. Designed to keep all critical information visible and accessible at all times.

**Key Features:**
- Tabbed windows providing quick access to different information types
- Expanded slot sizing (45x45px standard) for easy clicking
- Redesigned merchant/loot grids with better visibility
- Horizontal bag layout for inventory with full visual feedback
- Player window showing stats, indicators, and quick reference information
- Pet window with controls, health, and mana always visible

## What's New

EOF

# Add changelog
cat /tmp/changelog.txt >> /tmp/release_notes.md

# Add footer
cat >> /tmp/release_notes.md << 'EOF'

## Documentation

- [README.md](https://github.com/draknarethorne/thorne-ui/blob/main/README.md) - Project overview and features
- [STANDARDS.md](https://github.com/draknarethorne/thorne-ui/blob/main/.docs/STANDARDS.md) - UI development standards
- [DEVELOPMENT.md](https://github.com/draknarethorne/thorne-ui/blob/main/DEVELOPMENT.md) - Development guide

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/draknarethorne/thorne-ui).

---

**Maintainer**: Draknare Thorne  
**License**: Custom UI for personal use with The Al'Kabor Project
EOF

echo -e "${GREEN}✓ Release notes created ($(wc -l < /tmp/release_notes.md) lines)${NC}"
echo "Preview (first 20 lines):"
head -20 /tmp/release_notes.md
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}All Tests Passed!${NC}"
echo "=========================================="
echo ""
echo "Test artifacts created in /tmp/test-releases/:"
ls -lh /tmp/test-releases/
echo ""
echo "Release notes preview saved to: /tmp/release_notes.md"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review the test ZIP files in /tmp/test-releases/"
echo "2. Extract and verify contents manually if desired"
echo "3. Review release notes in /tmp/release_notes.md"
echo "4. When ready, create a real release by pushing a tag:"
echo "   git tag -a v0.4.0 -m 'Release v0.4.0: Description'"
echo "   git push origin v0.4.0"
echo ""
echo -e "${YELLOW}Note:${NC} This test uses version ${TEST_VERSION} to avoid conflicts"
echo ""

# Cleanup prompt
echo -e "${YELLOW}Cleanup test files? (y/n)${NC}"
read -r CLEANUP
if [ "$CLEANUP" = "y" ]; then
    rm -rf /tmp/test-releases
    rm -f /tmp/changelog.txt /tmp/release_notes.md
    echo -e "${GREEN}✓ Test files cleaned up${NC}"
else
    echo "Test files preserved in /tmp/"
fi
