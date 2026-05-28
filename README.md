# University

Terminal-based academic workflow. `acad` (Python CLI at `scripts/academic_cli.py`) unifies course management, lecture/pset scaffolding, grade tracking, an Ipe figure-insertion pipeline, and a status dashboard; a `uni` fish wrapper and a neovim layer (vimtex + custom keymaps) drive it from terminal and editor. LaTeX compiles with plain `pdflatex` via `latexmk` — robust, synctex-correct — against a shared `preamble.tex`. Notes and metadata as JSON under git.

Inspired by the late Gilles Castel.
