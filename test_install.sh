#!/bin/bash
# Test script to verify ytmp3 installation and basic functionality

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ytmp3 Installation Test                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Create virtual environment
echo "📦 Step 1: Creating virtual environment with uv..."
uv venv .venv-test
echo "✓ Virtual environment created"
echo ""

# Step 2: Activate and install
echo "📦 Step 2: Installing ytmp3..."
source .venv-test/bin/activate
uv pip install -e .
echo "✓ Installation complete"
echo ""

# Step 3: Test command availability
echo "🧪 Step 3: Testing command availability..."
if command -v ytmp3 &> /dev/null; then
    echo "✓ ytmp3 command is available"
else
    echo "✗ ytmp3 command not found"
    exit 1
fi
echo ""

# Step 4: Test help command
echo "🧪 Step 4: Testing --help command..."
ytmp3 --help > /dev/null 2>&1
echo "✓ Help command works"
echo ""

# Step 5: Test version
echo "🧪 Step 5: Testing --version command..."
VERSION=$(ytmp3 --version 2>&1)
echo "✓ Version: $VERSION"
echo ""

# Step 6: Test Python module
echo "🧪 Step 6: Testing Python module import..."
python3 -c "import ytmp3; print('✓ Module imports successfully')"
echo ""

# Cleanup
echo "🧹 Cleaning up test environment..."
deactivate 2>/dev/null || true
rm -rf .venv-test
echo "✓ Cleanup complete"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ✅ All Tests Passed!                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"

