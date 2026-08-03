# Eyes Wide Shut — TMLR paper

One paper, one visual system, built from the primary evidence.

## Build

```bash
make          # figures + paper + checks
make check    # checks only, against an existing main.pdf
```

Requires `xelatex`, `pdflatex`, Python 3 with PyMuPDF, and the Inter and
Noto Sans Mono fonts.

Output: `main.pdf` (17 pages).

## Why the build is split in two

Figures compile **standalone with xelatex** because they use Inter and Noto Sans
Mono through `fontspec`. The paper compiles with **pdflatex under `tmlr.sty`**,
which owns the page typography and must not be overridden.

Keeping them apart means the figure fonts never fight the venue style, and each
figure stays a self-contained PDF that can be reused on a website or in slides.
Each figure is built at exactly `\ewswidth` = 469.755pt, TMLR's `\textwidth`, so
nothing is ever scaled and 8pt text inside a figure renders at 8pt on the page.

## Files

| File | Role |
|---|---|
| `main.tex` | the paper |
| `tmlr.sty` | venue style, from `JmlrOrg/tmlr-style-file` |
| `ews-figures.sty` | **the single visual system** — palette, panels, trace typography |
| `figures/fig*.tex` | six standalone figures |
| `figures/excerpts/f*.tex` | **generated** band-B trace excerpts — do not edit |
| `extract_traces.py` | segments Harmony walkthroughs out of `../masih_finding_*.json` |
| `build_excerpts.py` | cuts the excerpts and emits LaTeX |
| `verify.py` | type size, font embedding, raster resolution |
| `contrast_check.py` | greyscale and WCAG contrast of the palette |

`ews-figures.sty` is the reason the figures cannot drift apart again: no figure
defines its own colour, type or panel geometry, so a change to the system
changes all six at once.

## Evidence integrity

Band B of every results figure is a **literal slice** of the recorded Harmony
trace. `build_excerpts.py` enforces this:

- text is copied from `traces.json`, never retyped;
- dropping a span is allowed but always marked with an ellipsis;
- a highlight target that no longer matches the source verbatim **aborts the
  build** rather than silently shifting;
- the verbatim command characters (`§ « »`) are asserted absent from every
  excerpt before emission.

One deliberate exception, disclosed in the Figure 6 caption: the Finding 5
tool-call payloads are normalised out of the submission file's extra JSON
escaping layer. The model emitted `{"code": ...}`; the finding file stores
`{\"code\": ...}` with backslash line continuations. Printing those backslashes
would attribute a file-format artifact to the model.

## What the checks enforce

`verify.py` encodes two different promises:

- **Evidence text ≥ 8pt.** The verbatim model output a reviewer must actually
  read. In the drafts this replaces, it ranged 5.2–7.3pt and was raster at
  210–260 ppi. It is now 8pt vector throughout, keyed on the Noto Sans Mono face
  so inline code labels can't mask a regression.
- **All text ≥ 7pt**, the conventional print floor for figure chrome.

Plus: every font embedded, every raster image ≥ 200 ppi.

`contrast_check.py` verifies the palette survives black-and-white printing —
each meaningful colour pair separates in greyscale luma, not only in hue. Colour
in these figures is redundant with the labels, never load-bearing.

## Submission notes

- Target venue is **TMLR**, which needs no arXiv endorser — only a free
  OpenReview account.
- TMLR is **double-blind**. The default build renders "Anonymous authors";
  the author block in `main.tex` appears only when `tmlr` is loaded with
  `[accepted]`.
- Claims are bounded by `../evidence_audit.md`, `../citation_audit.md` and
  `../comparison_audit.md`. Those three files govern what each finding may
  assert; do not strengthen a claim without re-checking them.
