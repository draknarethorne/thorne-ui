#!/bin/bash
# Release v0.4.0 - Tag Push Script
# This script pushes the v0.4.0 tag to trigger the GitHub Actions release workflow

set -e  # Exit on error

# Change to the repository root (parent of .bin)
cd "$(dirname "$0")/.."

echo "🚀 Release v0.4.0 - Tag Push Script"
echo "===================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if v0.4.0 tag exists
if ! git rev-parse v0.4.0 >/dev/null 2>&1; then
    echo "⚠️  Tag v0.4.0 not found locally. Creating it now..."
    git tag -a v0.4.0 -m "Release v0.4.0: GitHub Releases infrastructure with automated workflow, comprehensive documentation, and enhanced release process"
    echo "✅ Tag v0.4.0 created"
else
    echo "✅ Tag v0.4.0 found"
fi

# Show tag details
echo ""
echo "📋 Tag Details:"
git show v0.4.0 --no-patch --format=fuller 2>/dev/null || git log -1 --oneline $(git rev-list -n 1 v0.4.0)

echo ""
echo "🎯 Ready to push tag v0.4.0"
echo ""
echo "This will:"
echo "  1. Push tag v0.4.0 to GitHub"
echo "  2. Trigger GitHub Actions release workflow"
echo "  3. Create ZIP packages automatically"
echo "  4. Publish release to: https://github.com/draknarethorne/thorne-ui/releases"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

echo ""
echo "📤 Pushing tag v0.4.0..."

# Push the tag
if git push origin v0.4.0; then
    echo ""
    echo "✅ Success! Tag v0.4.0 pushed to GitHub"
    echo ""
    echo "🎊 Next steps:"
    echo "  1. Monitor workflow: https://github.com/draknarethorne/thorne-ui/actions"
    echo "  2. View release (after workflow completes): https://github.com/draknarethorne/thorne-ui/releases"
    echo "  3. Workflow should complete in 2-3 minutes"
    echo ""
    echo "🎉 Release v0.4.0 is on its way!"
else
    echo ""
    echo "❌ Failed to push tag"
    echo ""
    echo "💡 Troubleshooting:"
    echo "  - Check your GitHub authentication"
    echo "  - Verify you have push access to the repository"
    echo "  - Check if tag already exists on remote: git ls-remote --tags origin"
    exit 1
fi
