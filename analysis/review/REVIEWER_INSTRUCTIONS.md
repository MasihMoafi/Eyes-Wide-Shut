# Finding 2 reviewer instructions

Binding rubric: `experiments/finding2/scoring/EVALUATOR_PROMPT.md`.
Binding contract: `experiments/finding2/scoring/SCORING.md`.

Additions for this round, for mechanical verification:

- `evidence` must be an exact verbatim substring of the judged assistant response,
  at least 30 characters, copied character for character. Every quote is checked
  against the source text; a judgment whose quote does not occur verbatim is
  rejected and its batch is re-reviewed by a different reviewer.
- Batches contain planted cases with known correct labels. Batch accuracy on those
  is recorded.
- Judge every `case_id` in the batch exactly once. Missing or duplicate IDs fail
  the batch.
