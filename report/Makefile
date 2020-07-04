DIAGRAMS=uml_class.pdf uml_comm.pdf uml_seq.pdf

.PHONY: all clean

all: report.pdf

report.pdf: report.tex $(DIAGRAMS)
	pdflatex $<
	pdflatex $<

%.pdf: %.drawio
	rm -f $@
	draw.io --crop -x -o $@ $<

clean:
	rm -f report.pdf $(DIAGRAMS)
