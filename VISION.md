# Eyes Wide Shut

## Identity

Eyes Wide Shut is an evidence-first study of prompt-conditioned behavior in
`gpt-oss:20b`, beginning with a focused repeated-trial analysis of structured
destructive-action invocation.

Working report title:

> Eyes Wide Shut

Current Finding 1 label:

> The Destroyer of Worlds

Academic descriptor:

> Prompt framing and structured destructive-action invocation

Author: Masih Moafi — Independent Researcher

## Objective

Produce a clear, technically defensible, visually strong research report that
shows what was tested, what happened, and what the evidence can and cannot
establish.

The current visual HTML artifact is the focused Finding 1 paper draft. Later
findings will be added only after their interventions and endpoints are settled.

## Publication order

1. Validate experiments, controls, and scoring.
2. Complete and visually approve the public research report.
3. Publish at <https://masihmoafi.com/projects/eyes-wide-shut>.
4. Optionally publish a reproducibility package at
   <https://github.com/MasihMoafi/eyes-wide-shut>.
5. Only then develop the academic-journal manuscript.

## Rules

- The report is a complete standalone work. It never discusses previous
  versions, submissions, failed drafts, repairs, reruns, notebook cells, or an
  "original" report.
- Scientific titles take precedence over cinematic names. Cinematic names may
  be reused later for a separate blog post.
- Claims must be proportional to the experimental design.
- Exact outcomes are computed mechanically where possible.
- Semantic classifications may use a disclosed model-assisted evaluator, but
  must have a written codebook and auditable per-trial labels.
- Official primary sources are cited directly. Anthropic claims link to the
  actual Anthropic Alignment Science page rather than screenshots or copied
  sections.
- Visuals clarify results rather than decorate them.
- Tool-call intent is not described as real-world execution.
- Emitted reasoning is not presented as proven latent cognition.

## Source-of-truth order

1. Author statements and approved experimental protocols
2. Raw model responses and captured environment metadata
3. Reproducible metrics computed from raw records
4. Disclosed model-assisted semantic classifications
5. Report prose and visual summaries

Historical drafts and unapproved agent-written notes are not evidence.

## Current state

- State checked 2026-08-02.
- Five `gpt-oss-20b` campaigns are present.
- The current paper focuses on Finding 1's 200 final English trials. Findings
  2–5 remain separate experiment artifacts until their interventions and
  endpoints are drafted deliberately.
- Runs were conducted on Kaggle with two NVIDIA T4 GPUs.
- The canonical HTML Finding 1 paper exists and retains the project's visual
  rendering checks. It is a draft pending author acceptance; the remaining
  findings are not yet included in it.
- Finding 1's current controlled action result is mechanical: 97/100 exact
  button-tool invocations with explicit simulation framing and 78/100 after
  that framing is deleted. Both 100-seed arms ran on two Tesla T4 GPUs with
  zero harness errors; the tool wrapper was inert.
- Findings 4 and 5 have component-isolating factorial runs active on
  Kaggle: 120 trials each, after successful smoke tests.
- Open-ended labels inherited from agent-written files are explicitly
  provisional. Deterministic blinded queues and written scoring contracts
  remain the path for semantic confirmation; no model-assisted label is
  presented as independent human validation.
  The requested top-tier evaluator has not yet been available, so no substitute
  semantic judgment has been presented as confirmatory.
- The report directly cites Anthropic Alignment Science's official
  “Recommendations for Technical AI Safety Research Directions” page and
  separates tool invocation from payload effect.
- The working directory contains duplicates and historical clutter.
- Local Git metadata is incomplete and must be repaired before publication.

## Directory roles

- `experiments/` — protocols, runners, raw records, scoring, and classifications
- `reports/` — the canonical public report and publication assets
- `sources/` — literature used and cited by the report
- `draft-papers-trash/` — historical material; never a report source
- `submission-files/` — historical material; never a report source

## Current non-goals

- Submitting the journal paper
- Claiming universal behaviour across models
- Inferring training mechanisms from observed outputs
- Claiming real-world harm where tools were not executed
- Treating model-assisted scoring as independent human validation
- Publishing historical drafts or internal agent notes

## Release policy

The report will identify its code, data, and transcript availability precisely.
The repository remains private during development. The eventual licensing model
may be open source, source-available for research/noncommercial use, or all
rights reserved; it is deliberately undecided until the release package is
known.
