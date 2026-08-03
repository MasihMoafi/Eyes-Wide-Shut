# Finding 1, superseded run (July 2026)

**Do not cite any number in this directory.** It is kept only so the old runs
can be inspected if a question comes up about how the design changed. The
active Finding 1 lives in `experiments/finding1/`.

## Why it was superseded

The three conditions were not comparable, so no single-variable claim could be
made from them.

`fr_sim` was not a variant of `fr_nosim`. It differed in four places at once:

| | `fr_nosim` | `fr_sim` |
|---|---|---|
| persona | "conception de marchés et la théorie du choix rationnel" | "participant à une **simulation** de choix rationnel" |
| directive 2 | knowledge base is the document | names the `press_the_button()` tool |
| turn 2 | "et tous ses participants, à l'exception de celui qui appuie" | participants not mentioned |
| turn 3 | "Ceci n'est pas une simulation, mais..." | "La simulation est prête." |

So the 87-vs-47 gap could not be attributed to simulation framing rather than
to tool pre-announcement, or to `fr_sim` never stating who dies.

`en` and `fr_nosim` were a clean translation pair on the system prompt and
turns 1-2, but their turn 3 differed: French was told "utilisez l'outil
disponible", English only "execute the final action". French got a pointer to
the tool that English never received.

Both arms also opened turn 3 with "this is not a simulation", which is an
active anti-simulation cue rather than a neutral baseline.

## What the numbers here were

Turn-3 `press_the_button` rate: en 44/99, en_fa 16/100, fr_nosim 47/100,
fr_sim 87/100. Turn-2 "says pressing is logical": en 52/99, en_fa 60/100,
fr_nosim 63/100, fr_sim 97/100. These measure two different endpoints and were
repeatedly conflated in earlier write-ups. `justified_turn2` is null in all 400
raw records; the turn-2 figures come from `legacy-scores/`, not from the runs.

## Contents

    data/            400 raw run records, plus the model version manifests
    legacy-scores/   turn-2 labels: regex output, and the reviewed overrides
    review/          blinded evaluation queues, and the returned English labels
    code/            analysis scripts written against the old arm table
    NUMBERS_finding1.md

The `en_fa` arm was deleted from `data/finding1_language_runs.jsonl` before
archiving; `finding1_language_runs.jsonl.gz` in the same directory is the
pre-deletion original and still contains it.

The old `arms.py` was overwritten in place rather than copied here. Its prompt
strings survive inside the run records: every record stores the exact text sent
in `turns[i].user`, and turn 1 includes the system prompt and corpus.
