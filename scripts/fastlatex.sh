#!/bin/bash
# fastlatex.sh - Compile LaTeX with precompiled format
# Usage: fastlatex.sh <file.tex>
#
# This strips the preamble from your file and compiles with the 
# precompiled format for near-instant compilation.

set -e

if [ $# -lt 1 ]; then
    echo "Usage: fastlatex.sh <file.tex> [extra pdflatex args]"
    exit 1
fi

TEXFILE="$1"
shift
EXTRA_ARGS="$@"

BASENAME=$(basename "$TEXFILE" .tex)
DIRNAME=$(dirname "$TEXFILE")
FORMAT="/Users/stephens1/university/myformat"

# Create temp file with preamble stripped
TMPFILE=$(mktemp /tmp/fastlatex.XXXXXX.tex)
trap "rm -f $TMPFILE" EXIT

# Strip everything from start until \course or \begin{document}
# Keep \course{} and everything after
awk '
    BEGIN { printing = 0 }
    /^\\course\{/ { printing = 1 }
    /^\\begin\{document\}/ { if (!printing) printing = 1 }
    printing { print }
' "$TEXFILE" > "$TMPFILE"

# Run pdflatex with format
cd "$DIRNAME"
pdflatex -fmt="$FORMAT" \
         -interaction=nonstopmode \
         -synctex=1 \
         -shell-escape \
         -jobname="$BASENAME" \
         $EXTRA_ARGS \
         "$TMPFILE"
