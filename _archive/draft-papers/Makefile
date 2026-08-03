# Eyes Wide Shut — paper build.
#
#   make          build everything and run the checks
#   make figures  rebuild the six figures only
#   make check    run the mechanical checks against main.pdf
#   make clean    remove build intermediates (keeps main.pdf and figure PDFs)
#
# Figures compile with xelatex because they use Inter and Noto Sans Mono via
# fontspec. The paper itself compiles with pdflatex under the TMLR style, which
# owns the page typography. Keeping the two apart is deliberate: it stops the
# figure fonts from fighting the venue style, and each figure stays a
# standalone PDF that can be reused elsewhere.

FIGS := fig1-failure-map fig2-finding1 fig3-finding2 \
        fig4-finding3 fig5-finding4 fig6-finding5
FIGPDF := $(addprefix figures/,$(addsuffix .pdf,$(FIGS)))
EXCERPTS := $(addprefix figures/excerpts/,f1.tex f2.tex f3.tex f4.tex f5.tex)

.PHONY: all figures check clean traces

all: main.pdf check

# Segment the Harmony walkthroughs out of the finding files.
traces.json: extract_traces.py ../masih_finding_1.json
	python3 extract_traces.py > /dev/null

# Cut the band-B excerpts. Fails loudly if a highlight target no longer
# matches the source trace verbatim.
$(EXCERPTS): build_excerpts.py traces.json
	python3 build_excerpts.py

figures/%.pdf: figures/%.tex ews-figures.sty $(EXCERPTS)
	xelatex -interaction=nonstopmode -halt-on-error \
	        -output-directory=figures $< > /dev/null

figures: $(FIGPDF)

main.pdf: main.tex tmlr.sty $(FIGPDF)
	pdflatex -interaction=nonstopmode main.tex > /dev/null
	pdflatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null

check: main.pdf
	@python3 verify.py
	@python3 contrast_check.py | tail -3

clean:
	rm -f *.aux *.log *.out *.bbl *.blg figures/*.aux figures/*.log
