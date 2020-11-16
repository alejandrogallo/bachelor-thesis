MAIN_SRC  = text.tex
BUILD_DIR = build
# TeX files
SOURCES   = $(MAIN_SRC) $(wildcard *.tex)
PACKAGES  = $(wildcard *.sty)

VIEW      = 1
VIEWER    = xdg-open
BIBTEX    = bibtex
PYTHON    = python3
TEXENGINE = pdflatex
# use color for output
COLOR = 1
