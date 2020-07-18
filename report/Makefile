DIAGRAMS=uml_class.pdf uml_comm.pdf uml_seq.pdf uml_use_case.pdf uml_state.pdf uml_activity.pdf uml_proxy.pdf
IMAGES=document_recognition_29_1.png mask_description.jpg test_background.jpg test_patente.jpg test_tesserino.jpg test_patente_snapshot.jpg test_tesserino_snapshot.jpg
SOURCES=config.py test_background.py test_patente.py test_tesserino.py via_regions.json

.PHONY: all clean

all: report.pdf

report.pdf: report.tex $(SOURCES) $(IMAGES) $(DIAGRAMS)
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

%.pdf: %.drawio
	rm -f $@
	draw.io --crop -x -o $@ $<

clean:
	rm -rf report.pdf $(DIAGRAMS) *.aux *.log *.out *.lol *.lof *.toc _minted-*
