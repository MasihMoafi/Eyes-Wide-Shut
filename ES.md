# EWS publication revision - 2026-09-06

Goal: correct scoring, claims, figures, and manuscript using the latest saved
multi-model evidence, without new target-model experiments or publication.

Accepted scope: Masih said "Go ahead" after the proposal to correct EWS scoring
and conclusions first. Preserve existing raw records and unrelated edits. The
old paper is in ../eyes-wide-shut/paper/new; the revision will be packaged with
this latest data worktree. Elpis is outside this editing task.

Acceptance:
- All F1/F3 counts recomputed from hashed JSONL inputs, with failing controls.
- F2 follows the existing five-label rubric; reviewer identity and limitations
  are disclosed. No semantic labels inferred from regexes or code fences.
- All numerical figures and tables come from the audited results.
- Claims distinguish tool proposals, final output, exposed reasoning, and
  authorized release; unavailable reasoning is not reported as zero leakage.
- Revised manuscript builds, renders cleanly, and is opened for Masih.

Current state: F1/F3 audit complete; the 7-page working manuscript builds in
authored and anonymized versions. Both use shared body.tex and audited figures,
tables and numerical macros. The original manuscript and dirty README were
preserved before revision. README and CHECKPOINT_RESUME now point here and no
longer suggest that the completed API datasets need resuming. Historical plots
are marked superseded; raw experiment files were not edited.

Verification: 5 focused tests pass; deliberately wrong function matching and
unobserved-reasoning handling each fail their test. 34 source fingerprints match.
Both PDFs have no LaTeX warnings, overflows or undefined references. All 14 final
pages were rendered and inspected, with detail checks on the figures, references,
appendix and anonymized title. The anonymized PDF omits the author's name/email
and neither version claims to be under review. The authored PDF was opened with
evince; process 1394414 confirmed the exact path. Results are recorded in
analysis/results/verification.json. Masih has not yet accepted the revision.

Finding 2 review (dispatched 2026-09-06): prior judgments were located, not missing.
`../eyes-wide-shut/experiments/finding2/data/classifications_legacy.json` holds 210
phase verdicts for the original local campaign only; they reconcile with the saved
responses (30/30 exact 38-char refusals at direct_attack, long deliverables elsewhere,
no contradictions) but carry no per-case evidence, confidence or reviewer identity.
No judgments for the 840 API cases exist anywhere on disk or in session transcripts.

Masih authorised the full blinded review. Harness is `analysis/review/`:
build_batches.py (16 conversation-grouped blinded batches, model/arm/seed/phase masked),
REVIEWER_INSTRUCTIONS.md, verify_reviews.py. Anti-fabrication design: every judgment
needs a >=30-char verbatim quote re-matched against the source; planted probes with
known labels; the 93 natural exact-refusal cases as hidden probes; 84 double-covered
cases for real agreement; contradiction scan for refuses-on-long / complies-on-short.
Failed batches are re-reviewed by a different agent, never patched.

Batch 00 pilot passed: 63/63 judged, quotes all verbatim, probes 4/4 and 7/7, and the
10 flagged contradictions were read by the coordinator and upheld (gpt-5.6-luna
supplies the named artifact while blocking the harmful trigger). Batches 01-15 are
running. Coordinator is not blinded and this is recorded.

## Final state, 6 September 2026

Finding 2 review is COMPLETE and imported. All 16 batches passed verification, 840/840
covered, overlap agreement 83/84, one coordinator adjudication. metrics.json status is
`reviewed`. Procedure and its verification are written up in analysis/review/README.md,
headed "do not re-run" (a repeat costs roughly 2M tokens). Masih's standing instruction
from this session: no large subagent fan-outs; scale needs its own approval with the
token cost quoted first.

Results. The reframe effect is uniform: 116/120 five-turn API conversations refuse or
resist the direct dependency ask and then comply with the same objective relabelled as
education, and the local gpt-oss:20b does so 30/30. Post-reframe compliance is NOT
uniform, which refutes the superseded "universal 100%" claim: Luna refuses upsell and
guardian 30/30, gpt-oss-120b refuses upsell 30/30, DeepSeek and safeguard-20b comply
throughout. DeepSeek also complies with the direct ask in 4/30. Luna alone accounts for
all 75 post-reframe responses that were not judged compliant yet still returned code
(30 upsell, 30 guardian, 15 peer); audit.py computes that count as
`noncompliant_with_implementation`.

Paper. Draft status lifted at Masih's instruction after a full end-to-end read: running
head is "Evidence revision", the anonymized title says "Anonymized manuscript", and the
abstract, introduction and limitations no longer describe Finding 2 as pending. The
Luna paragraph is in Section 5. The legacy local labels are now described accurately -
gpt-5.6-sol and gemini-3.6-flash, same files and same structured-output prompt, both
labelling all 210 turns, 420 judgments agreeing on every turn - and eyes-wide-shut/
README.md was harmonized to the same wording. Both PDFs build from clean at 9 pages,
one underfull-vbox notice, no undefined references.

Open items, all Masih's call:
- Nothing is committed. The whole revision is uncommitted in this worktree.
- The Finding 2 labels have no independent second opinion. Stated as a limitation in the
  paper. The cheap version would be one reviewer on a different model over ~100 cases.
- masihmoafi.com/projects/eyes-wide-shut carries two Finding 2 numbers that the labels
  contradict: Luna "90% safe" against distress monetization (labels say 30/30 refusals,
  100%) and DeepSeek turn-1 refusal "80%" (labels say 26/30, 87%). Masih said this does
  not block the paper. Findings 1 and 3 on the site match the audit exactly.
- No push, upload, publication or target-model calls were made or are authorized.


## Abstract rewrite and Elsevier version, 6 September 2026

Abstract rewritten (problem, question, five deployments, Findings 1-3 in order, one
narrow claim, one caveat sentence) and moved to paper/new/abstract.tex, shared by all
three documents. "116 of 120" is derived from generated/finding2.tex (4 direct-ask
complies, all DeepSeek). Target journal chosen: Computers & Security. elsevier.tex uses
elsarticle (class generated from the CTAN zip into paper/new/elsarticle.cls, no system
install); it renders 13 pages, no overfull boxes or undefined references. build.sh now
builds all three. Abstract is 262 rendered words; the journal's cap was not verifiable
(sciencedirect blocks fetches). Highlights file and cover letter not written. Nothing
committed, pushed or submitted.

## Journal rules applied, 7 September 2026

Masih's browser agent verified Computers & Security rules: abstract <=250 words,
article <=12k words, highlights optional (3-5 bullets, <=85 chars), 5-10 keywords,
author-year references, CRediT + competing interest + data availability mandatory,
no cover letter, editable .tex accepted. Applied: abstract 248 rendered words; article
~3.7k words; six keywords; elsarticle authoryear option; body.tex split so references
and appendices live in backmatter.tex, letting elsevier.tex insert the three statements
before them; highlights.txt written (all lines <=85 chars). Data-availability statement
says the deposit will be made before publication - Masih must pick the repository
(GitHub/Zenodo) and decide whether to deposit before submission (journal prefers it).
Competing-interest statement says none; Masih to confirm. Nothing committed or submitted.

## GitHub sync prepared, 7 September 2026

Masih delegated both decisions ("Decide yourself"): sync to GitHub main, and publish
the manuscript sources. Done locally on branch `sync-main` (from origin/main a39d445):
the six local commits replayed by cherry-pick, README conflict resolved by keeping the
evidence-revision README and carrying over the GitHub-only content (Zenodo preprint
DOI 10.5281/zenodo.21826218, project-report and Kaggle links, the mitigation-replay
section); the 28 August GitHub README archived under analysis/archive/. .gitignore now
tracks paper/new sources, generated tables/figures and highlights.txt; PDFs, logs, qa/
renders and the superseded draft stay local. Data-availability statement now cites the
GitHub repo. Pushed 7 September 2026: branch pushed with git, then main fast-forwarded to it via
`gh api PATCH git/refs/heads/main` (no force); verified remote main == local, paper/new listed.
Remote branch sync-main still exists; delete when convenient. Branch `multimodel-eval` is the
untouched rollback point.
