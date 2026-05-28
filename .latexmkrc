# LaTeX build config — plain pdflatex (robust, synctex-correct).
# Shared preamble: ~/university/preamble.tex
# Output (pdf/aux/synctex) lands in the course directory; aux is gitignored
# and removable via `acad course cleanup`. Inherited by subdirs lacking their own.

$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 %O %S';

ensure_path('TEXINPUTS', './/:');

@generated_exts = (@generated_exts, 'synctex.gz', 'run.xml', 'bbl', 'bcf');
$clean_ext = 'aux bbl bcf blg fdb_latexmk fls log out run.xml synctex.gz toc nav snm';
