TEX = $(wildcard *.tex)
BIB = refs.bib
PAPER = micro23_bitpacker
OPT_PAPER = micro23_bitpacker_opt
#FLAGS = -halt-on-error -mode=batch
FLAGS = -halt-on-error -interaction=batchmode

default: paper

figs:
	make -C tables/
	make -C figures/
	make -C plots/

paper: figs $(TEX) $(BIB)
	date > auto_header.tex
	echo "--- rev" >> auto_header.tex
	python3 scripts/gitver.py >> auto_header.tex
	pdflatex -halt-on-error $(PAPER)
	bibtex -min-crossrefs=30000 $(PAPER)
	pdflatex $(FLAGS) $(PAPER)
	pdflatex $(FLAGS) $(PAPER)
	pdflatex -halt-on-error $(PAPER)
	ps2pdf -dPDFSETTINGS=/prepress -dCompatibilityLevel=1.4 -dEmbedAllFonts=true -dSubsetFonts=true -r600 $(PAPER).pdf $(OPT_PAPER).pdf
	qpdf --linearize $(OPT_PAPER).pdf $(PAPER).pdf

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf

