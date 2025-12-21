# Global LaTeX build configuration for ~/university
# Uses precompiled format for fast compilation (~0.5s vs ~2s for package loading)
#
# SETUP (run once, and whenever preamble.tex changes):
#   cd ~/university && ./build-format.sh
#
# This config is inherited by all subdirectories without their own .latexmkrc

$pdf_mode = 1;
$pdflatex = '/Users/stephens1/university/scripts/pdflatex-fast -interaction=nonstopmode -synctex=1 -shell-escape %O %S';

# Ensure output dirs exist
ensure_path('TEXINPUTS', './/:');

# Clean up extra files
@generated_exts = (@generated_exts, 'synctex.gz', 'run.xml', 'bbl', 'bcf');
$clean_ext = 'aux bbl bcf blg fdb_latexmk fls log out run.xml synctex.gz toc nav snm';
