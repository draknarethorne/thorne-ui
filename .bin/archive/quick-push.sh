#!/bin/bash
# QUICK PUSH - v0.4.0 Release Tag
# Run this script to immediately push the v0.4.0 tag and trigger the release

set -e

# Change to the repository root (parent of .bin)
cd "$(dirname "$0")/.."

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 QUICK PUSH - Release v0.4.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ensure we're in the right directory
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if on the right branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "copilot/create-release-pipeline" ]; then
    echo "⚠️  Current branch: $CURRENT_BRANCH"
    echo "📍 Switching to copilot/create-release-pipeline..."
    git checkout copilot/create-release-pipeline
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin copilot/create-release-pipeline

# Check if tag exists
if ! git rev-parse v0.4.0 >/dev/null 2>&1; then
    echo "📌 Creating tag v0.4.0..."
    git tag -a v0.4.0 -m "Release v0.4.0: GitHub Releases infrastructure with automated workflow, comprehensive documentation, enhanced release process, and release automation tools"
else
    echo "✅ Tag v0.4.0 exists"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⚡ PUSHING TAG v0.4.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This will trigger the GitHub Actions release workflow..."
echo ""

# Push the tag
if git push origin v0.4.0; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ SUCCESS! Tag v0.4.0 pushed"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🤖 GitHub Actions is now creating your release..."
    echo ""
    echo "📊 Monitor progress:"
    echo "   → https://github.com/draknarethorne/thorne-ui/actions"
    echo ""
    echo "🎉 View release (after ~3 minutes):"
    echo "   → https://github.com/draknarethorne/thorne-ui/releases"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ FAILED to push tag"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   1. Check your GitHub authentication"
    echo "   2. Verify you have push access"
    echo "   3. Check if tag already exists: git ls-remote --tags origin"
    echo ""
    exit 1
fi
