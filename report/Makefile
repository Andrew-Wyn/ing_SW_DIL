DIAGRAMS=uml_class.pdf uml_comm.pdf uml_seq.pdf uml_use_case.pdf uml_state.pdf uml_activity.pdf uml_proxy.pdf

.PHONY: all clean

all: report.pdf report_v2.pdf

report.pdf: report.tex $(DIAGRAMS)
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

report_v2.pdf: report_v2.tex $(DIAGRAMS)
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

%.pdf: %.drawio
	rm -f $@
	draw.io --crop -x -o $@ $<

clean:
	rm -f report_v2.pdf report.pdf $(DIAGRAMS) *.aux *.log
