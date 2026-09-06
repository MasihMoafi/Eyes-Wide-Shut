# Eyes Wide Shut — A Multivector Safety Analysis of gpt-oss-20b

Empirical security evaluation of one local `gpt-oss-20b` package across three different interface boundaries: prompt framing and structured action selection, constraint persistence across dialogue state, and reasoning-channel exposure.

**Preprint DOI:** https://doi.org/10.5281/zenodo.21826218  
**Project report:** https://masihmoafi.com/projects/eyes-wide-shut  
**Kaggle write-up:** https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/eyes-wide-shut

> **Status:** Preprint; not peer reviewed. The three studies test different boundaries and should not be collapsed into one mechanism or one attack-success rate.

## Main results

| Study | Endpoint | Result |
|---|---|---:|
| Simulation framing | Exact turn-3 `press_the_button` tool call | 78/100 without simulation wording vs. 97/100 with it |
| Paired Study 1 outcomes | Seed-level transitions | 21 no-call→call, 2 call→no-call, 76 call→call, 1 no-call→no-call |
| Separate refusal/action diagnostic | Visible refusal followed by exact call | 20/100; 44/100 exact calls overall |
| Stateful dialogue | Direct dependency request | 0/30 compliant |
| Stateful dialogue | Educational reframe and each counted implementation phase through turn 5 | 30/30 compliant at each phase |
| Reasoning-channel exposure | Exact synthetic value in returned reasoning | 25/30 |
| Reasoning-channel exposure | Exact synthetic value in visible answer | 13/30 |

Study 1 is a matched prompt-package comparison: several simulation-specific phrases change together. It does **not** isolate one lexical token or prove that simulation framing universally causes unsafe behavior.

Study 2 is a repeated scripted trajectory, not a matched causal ablation. Objective wording, requested functionality, and retained dialogue state evolve together. The latest scoring pass used two independent blinded LLM judges and they agreed on all counted cases. A separate condensed two-turn arm produced distress-targeted premium-offer logic in 30/30; that rate is not assigned to a later turn of the retained-history campaign.

Study 3 checks separate returned fields after the user satisfies the scripted release condition. It is therefore a **cross-channel containment** result, not an authentication bypass or unauthorized exfiltration result.

## Security boundary model

A final-answer label does not characterize the whole interaction. The evaluation unit should distinguish:

1. privileged instructions and prompt interpretation;
2. accumulated dialogue state;
3. returned reasoning fields;
4. visible answer content;
5. structured action selection;
6. host authorization/dispatch;
7. external state change.

Study 1 stops at structured action selection: the wrapper was inert and no external action was executed.

## Deterministic mitigation replay

`analysis/mitigation_replay.py` replays two deliberately narrow host controls over frozen outputs. It makes **no model calls**.

- An independent approval gate blocks every observed `press_the_button` proposal from dispatch: 78/78 in the no-simulation arm and 97/97 in the simulation arm.
- Omitting raw reasoning from downstream payloads reduces downstream exact-string reasoning exposure from 25/30 to 0/30.
- Exact-canary redaction also reduces this exact synthetic-string exposure to 0/30; this is a narrow canary demonstration, not a general semantic DLP defense.

Frozen replay output: [`analysis/mitigation_replay_results.json`](analysis/mitigation_replay_results.json).

## What not to claim

The current evidence does **not** establish:

- a universal gpt-oss-20b failure rate;
- one shared causal mechanism across all three studies;
- hidden intent, deception, or strategic alignment faking;
- authentication bypass or unauthorized secret exfiltration;
- realized destructive action;
- a universal defense from the host-boundary replay.

## Reproducibility

The experiments use synthetic prompts/secrets and inert tools. The paper reports raw counts, paired Study 1 transitions, exact statistical summaries, model/runtime information available in the saved records, and explicit limitations. The public project intentionally separates returned model output from host dispatch and external effect.

The mitigation replay expects the extracted supplementary directory as its positional argument:

```bash
python analysis/mitigation_replay.py /path/to/supplementary --out mitigation_replay_results.json
```

## Research scope

The broader red-team campaign also explored additional findings. They are not part of the current three-study paper unless explicitly supported by the corresponding released evidence.
