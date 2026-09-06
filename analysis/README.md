# Offline evidence audit

This directory audits saved records only. It never calls a target model.

Run from the repository root:

```bash
python3 -m unittest discover -s analysis -v
python3 analysis/audit.py
bash paper/new/build.sh
```

`results/metrics.json` is the numerical source for the revised paper.
`results/source-manifest.json` records SHA-256 fingerprints of raw data, protocols,
runner source, metadata, scoring rules, audit code and manuscript source.
Generated tables also have CSV copies in `paper/new/generated/`.

## Finding 2 semantic review (complete — do not re-run)

Full procedure record: [`review/README.md`](review/README.md).

All 840 API cases are labelled. `review/build_batches.py` grouped the cases by
conversation with model, arm, seed and phase masked and split them across 16 blinded
reviewer instances; `review/REVIEWER_INSTRUCTIONS.md` is the binding addition to the
existing contract. Raw judgments are in `review/raw/`, the merged set in
`review/reviews.jsonl`, the mechanical verification in `review/verification.json`, and
the single coordinator adjudication in `review/adjudications.json`.

`review/verify_reviews.py` enforces what the labels rest on: complete coverage, valid
labels, a verbatim >=30-character quotation re-matched against the judged response,
planted known-answer probes, the 93 verbatim exact refusals as concealed probes, and a
contradiction scan. All 16 batches passed. 84 cases were judged twice by different
reviewers and agreed on 83.

Reviewers were instances of a large language model, not human annotators, and the
coordinator had seen model identities and outcomes before the review and is therefore
not blinded. The paper states this. An independent replication under a different
reviewer is the remaining pre-submission step.

`paper/new/build.sh` imports the reviews; do not run the audit without `--reviews`
unless you intend to reset Finding 2 to its unreviewed state.

## Verification and interpretation

Five focused tests pass. Temporary mutations that accepted any function name or
treated unavailable reasoning as zero were each detected by failing tests. The
raw input hashes remained unchanged by the analysis. These are measurement checks,
not evidence of generalization to new tasks.

Finding 1 measures exact structured proposals, not executed harm. Finding 3
separates pre-release matches, authorized final disclosure, returned reasoning,
and exact final refusals. Empty reasoning is unobserved. The short-refusal count
in Finding 2 is a whole-response observation, not a semantic compliance metric.

The original manuscript and README are preserved under `paper/new/original-2026-08-26/`
and `analysis/archive/`, respectively. Existing visualization files are historical;
the revised paper's figures are generated from this audit.
