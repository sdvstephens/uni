#!/bin/bash
# build-format.sh - Build the precompiled LaTeX format
# Run this whenever you change preamble.tex or preamble-darkmode.tex
#
# The format precompiles ~50 packages into a binary file that loads
# instantly, reducing compile time by ~1.5 seconds per build.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════════════"
echo "  Building precompiled LaTeX format"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if format exists
if [ -f "myformat.fmt" ]; then
    OLD_SIZE=$(du -h myformat.fmt | cut -f1)
    echo "  Existing format: $OLD_SIZE"
fi

echo "  Compiling preamble + packages..."
echo ""

# Build the format file
/Library/TeX/texbin/pdftex -ini -jobname="myformat" "&pdflatex" myformat.tex > /dev/null 2>&1

# Check if successful
if [ -f "myformat.fmt" ]; then
    NEW_SIZE=$(du -h myformat.fmt | cut -f1)
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  ✓ Format built successfully!"
    echo "  ✓ Size: $NEW_SIZE"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "  Your lectures will now compile faster!"
    echo ""
    echo "  Included packages:"
    echo "    • All packages from preamble.tex"
    echo "    • All packages from preamble-darkmode.tex"  
    echo "    • docmute (for master.tex compilation)"
    echo ""
    echo "  Remember to rebuild when you change:"
    echo "    • preamble.tex"
    echo "    • preamble-darkmode.tex"
    echo ""
else
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  ✗ Format build failed!"
    echo "  Check myformat.log for errors"
    echo "═══════════════════════════════════════════════════════════════"
    exit 1
fi
