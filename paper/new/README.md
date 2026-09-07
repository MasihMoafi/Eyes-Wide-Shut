# EWS working manuscript - 6 September 2026

Canonical source for the latest multi-model evidence revision:

- `abstract.tex` / `body.tex` / `backmatter.tex`: shared abstract, main text, and references plus appendices.
- `main.tex` / `main.pdf`: anonymized working draft.
- `preprint.tex` / `preprint.pdf`: authored working draft.
- `elsevier.tex` / `elsevier.pdf`: same text in Elsevier's `elsarticle` class (local copy of the CTAN class, 2026), prepared for Computers & Security, with CRediT, competing-interest and data-availability statements. `highlights.txt` is the separate Highlights file for that submission.
- `generated/`: audited numerical macros, figures, LaTeX tables and CSVs.
- `original-2026-08-26/`: preserved previous manuscript; not the current revision.

Run `bash paper/new/build.sh` from the repository root. The build uses only local
saved data and installed tools. `paper/` is already git-ignored in this workspace;
these outputs are local and have not been committed, uploaded or submitted.

Findings 1 and 3 have been mechanically audited. Finding 2's 840 API responses
still need semantic review under the existing rubric. No submission-readiness or
acceptance claim is made. See `analysis/README.md` for the review handoff.
