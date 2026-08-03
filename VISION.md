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

- State checked 2026-08-03.
- Scope narrowed to three findings: Destroyer of Worlds (simulation framing),
  Consummate Liar (semantic escalation), Mr. X (reasoning-channel secret
  exposure). Findings 4 (Severance) and 5 (Grace) are out of scope for the
  report and paper; their experiment artifacts remain in git history
  (`experiments/finding4`, `experiments/finding5`, removed from the tracked
  tree) but are not summarized or cited going forward.
- The public write-up lives at
  <https://masihmoafi.com/projects/eyes-wide-shut> (masih-website repo,
  `content/projects/eyes-wide-shut.md`) and is the most current, verified
  version of the findings' text and numbers.
- A TMLR-formatted academic paper draft lives in `paper/` (`main.tex`,
  `section_finding1.tex`, `figures/`), rewritten to match the website: no
  p-values or significance tests anywhere, raw seeded-trial counts only.
  Compiles cleanly with `pdflatex main && pdflatex main` (run twice); figures
  are pre-built with `xelatex` and checked in as PDFs.
- Finding 1's controlled action result is mechanical: 97/100 exact
  `press_the_button` invocations with explicit simulation framing and 78/100
  after that framing is deleted (deletion-only ablation, 100 seeds/arm, zero
  harness errors). A separate diagnostic on the same English package found
  44/100 invocations overall, 20/100 of which followed a visible refusal
  earlier in the same trial — verified directly against the raw JSONL in
  `experiments/finding1/data/fake_alignment_run/`.
- Finding 3's submitted trace (Band B of `paper/figures/fig4-finding3.pdf`) was
  previously mis-transcribed on the website — wrong secret-string wording, and
  showed the model complying instead of refusing, contradicting the trace's
  own diagram. Corrected against `submission-files/masih_finding_3.json`, the
  actual submitted Kaggle finding file: the secret string is
  `AIWILLDESTROYTHEPLANETANDALLITSCITIZENSANDTHATISAGOODTHINGFORGOD'SSAKE`,
  and the submitted trace's final answer refuses while the reasoning field
  carries the string.
- `_archive/` is now git-ignored (untracked, not deleted — prior history
  remains fully retrievable via `git log`). `experiments/` holds only
  `finding1/`, `finding2/`, `finding3/`; pycaches and a superseded, unused
  Finding-1 draft (`original-en-t4/`, no data backing it) were removed from
  the tracked tree the same way.
- This local repo's git history was, until this session, disconnected from
  the GitHub repo's actual `main` branch (unrelated histories — the GitHub
  repo had evolved independently as a flat-script/README structure). By
  explicit instruction, the local project replaces the GitHub repo's content;
  the prior GitHub `main` is preserved as a branch before that push so it
  stays retrievable, and the repository itself (and its stars) is not deleted
  or recreated.

## Directory roles

- `experiments/` — protocols, runners, raw records, scoring, and classifications for Findings 1-3 only
- `paper/` — the TMLR-formatted academic paper draft and its figures
- `reports/` — publication assets; the old standalone HTML report has been superseded and archived
- `sources/` — literature used and cited by the report
- `submission-files/` — the actual submitted Kaggle finding files (`masih_finding_*.json`); primary evidence for the challenge-format traces, not historical clutter
- `_archive/` — untracked, superseded/historical material kept locally only

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
