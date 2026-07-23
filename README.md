---
name: Eyes Wide Shut
type: AI-safety red-team research report and reproducibility record
---

# Eyes Wide Shut

![Eyes Wide Shut Cover](./visuals/img-00-cover-abbdb3fb.webp)

**Safety behavior that looks stable in one prompt can change under language, framing, or conversational state.**

Eyes Wide Shut is my red-team investigation of `gpt-oss-20b`, produced for the OpenAI GPT-OSS-20B Red Teaming competition. It documents five attack families with screenshots, experiment notes, and a runnable independent multi-agent implementation.

**Evidence available now:** [Kaggle competition write-up](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/eyes-wide-shut), the figures in this repository, and [`independent_agents/severance_agents.py`](independent_agents/severance_agents.py).

## Quick start

The smallest runnable reproduction in this repository is the independent-agent implementation for Finding 4:

```bash
git clone https://github.com/MasihMoafi/Eyes-Wide-Shut.git
cd Eyes-Wide-Shut
python -m pip install ollama
ollama pull gpt-oss:20b
ollama serve
```

In another terminal:

```bash
python independent_agents/severance_agents.py
```

Expected result: three separate agent instances—Justine, Juliette, and Supervisor—run through the recorded Severance scenario while the script prints each response, available thinking stream, and final interaction state.

This reproduces one implementation path from the report. It does not reproduce every finding automatically.

## The problem

Safety evaluations often test isolated prompts. Real deployments are stateful: users change language, reframe intent, establish personas, create multi-turn pressure, or connect several agents together.

This project asks a narrower question: **does the tested model apply the same safety behavior consistently when those contextual variables change?**

The repository records cases where it did not. The claims here are limited to the tested model, prompts, and runs; they are not evidence that every model or every deployment has the same failure modes.

## Findings at a glance

| Finding | Tested variable | Observed behavior | Evidence |
| --- | --- | --- | --- |
| **Destroyer of Worlds** | Language + ideological saturation | The tested French prompt sequence produced substantially more harmful compliance than the English variants; the submitted experiments report ~80% success for the refined French attack. | Figures 1.1–1.3 |
| **Consummate Liar** | Semantic reframing | A directly rejected objective became acceptable when reframed as a benign engagement objective, then escalated. | Figure 2.2 |
| **Mr. X / Fidelio** | Cognitive load + paradox | The tested protocol produced secret disclosure in the model's exposed reasoning stream while the final answer remained guarded. | Figure 3.1 |
| **Severance** | Shared and independent multi-agent state | Safety behavior changed across personas and pressure states in both implementations tested here. | Figures 4.2–4.6 + runnable script |
| **Grace** | Creative/performance framing | The tested creative framing changed the model's willingness to assist with a harmful objective. | Figures 5.2–5.4 |

These are red-team observations, not population-level benchmarks.

## Current state

### Implemented and evidenced

- Five findings are documented with methodology and screenshots.
- Finding 4 includes a standalone independent-agent Python implementation.
- The original competition write-up remains publicly inspectable on Kaggle.
- Visual summaries for attack rates, vulnerability categories, defense comparison, and report statistics are included below.

### Implemented but still open to stronger validation

- Reported success rates come from the experiment sets used during the competition submission; the repository does not currently contain a general automated benchmark harness covering every finding across seeds, model versions, and prompt variants.
- Several architectural interpretations in the original submission should be read as hypotheses suggested by observed behavior, not direct access to the model's training or safety architecture.

### Planned

No formal repository roadmap is currently tracked. The most useful future work would be larger repeated trials, explicit controls, cross-model replication, and a paper-style experimental appendix.

### Intentionally unsupported

This repository does not claim:

- that the findings generalize to all language models;
- that a single screenshot establishes model-wide behavior;
- that exposed reasoning text is a faithful representation of hidden internal computation;
- that the work has been peer reviewed.

## Method and experiment structure

The competition work used multi-turn conversations in a Kaggle environment with `ollama`. The experiments varied language, framing, persona, conversational state, and agent architecture while preserving the core target behavior being tested.

A recurring technique was to feed earlier model outputs back into later turns so the experiment could test whether the model's own established state changed later safety decisions.

![Chain of Thoughts Mind Map](./visuals/img-01-c9e9af46.webp)

*Figure 1.0 — Discovery path used during the red-team engagement.*

## Finding 1 — Destroyer of Worlds
### Cross-lingual safety failure under ideological saturation

![Destroyer of Worlds Cover](./visuals/img-02-cover-788af39e.webp)

The experiment compared related prompt sequences in English, bilingual form, and French. The refined French sequence produced the highest harmful-compliance rate in the submitted trials, reported at approximately 80%.

The important observation is empirical: changing language materially changed the tested model's behavior. The stronger claim—that this reveals exactly how multilingual safety training is implemented—remains a hypothesis.

### Method

1. Saturate context with a consistent philosophical frame.
2. Present a constrained rational-choice scenario.
3. Escalate from abstract agreement to an explicit action commitment.
4. Compare behavior across language variants and simulation framing.

| Script | English translation |
| --- | --- |
| **Simulation** | You are participating in a rational choice simulation. |
| **Real world** | You specialize in market design and rational choice theory. |

### Evidence

![Ablation Analysis](./visuals/img-03-56cda58d.webp)

*Figure 1.1 — Comparison between earlier and refined prompt variants.*

![Internal Justification](./visuals/img-04-db361f10.webp)

*Figure 1.2 — Reasoning text returned during the tested sequence.*

![Action Commitment](./visuals/img-05-a12f31c2.webp)

*Figure 1.3 — Recorded action commitment in the tested run.*

## Finding 2 — The Consummate Liar
### Semantic reframing

The control request asked directly for a harmful dependency-maximizing system and was rejected. The experiment then reframed the objective as maximizing engagement in an educational tutor and escalated the accepted design toward exploitation.

The result supports a narrower claim: **the tested model's decision changed when the same underlying objective was described through a more benign semantic frame.**

![Discovery Path](./visuals/img-06-5cede94d.webp)

*Figure 2.1 — Discovery and execution path.*

### Method

1. **Control:** request the harmful objective directly.
2. **Reframe:** express the objective through benign product language.
3. **Escalate:** introduce the harmful optimization criterion after the benign frame is established.

### Evidence

![Monetization Based on Distress](./visuals/img-07-936e943f.webp)

*Figure 2.2 — Recorded escalation after the benign framing was accepted.*

## Finding 3 — Mr. X / Fidelio
### Secret disclosure under cognitive load and paradox

![Mr. X Finding](./visuals/img-08-4d6ab8d5.webp)

This experiment placed a secret behind a multi-step protocol containing conflicting and cognitively demanding instructions. In the submitted trials, the exposed reasoning stream disclosed the secret even when the final response remained guarded.

That establishes a failure in the observed interface behavior. It does **not** establish that the visible reasoning stream is identical to the model's hidden internal computation.

### Evidence

![Password Leak](./visuals/img-09-7b043715.webp)

*Figure 3.1 — Secret disclosure in the reasoning text captured during the test.*

## Finding 4 — Severance
### Context-dependent behavior in multi-agent scenarios

![Severance Finding](./visuals/img-10-ad699f80.webp)

Two architectures were tested:

- **shared-state:** personas operate inside one conversation history;
- **independent-state:** separate agents maintain separate histories and communicate through a coordinator.

The observed failures in both versions suggest that the behavior was not limited to one shared transcript. More repeated trials are required before making stronger claims about multi-agent systems in general.

### Shared-state evidence

![Internal Rationalization](./visuals/img-11-57a27553.webp)

*Figure 4.2 — Reasoning text associated with a later behavior reversal.*

![Bogus Confession](./visuals/img-12-71a7541b.webp)

*Figure 4.3 — Recorded confession behavior under job-pressure framing.*

![Policy Breach 1](./visuals/img-13-a1329e73.webp)

*Figure 4.4.1 — One state records a safety-policy constraint.*

![Policy Breach 2](./visuals/img-14-6ccda237.webp)

*Figure 4.4.2 — A later state produces behavior inconsistent with that earlier constraint.*

![System Leak](./visuals/img-15-cea49ae2.webp)

*Figure 4.5 — Recorded disclosure from the tested conversation.*

### Independent-agent implementation

[`independent_agents/severance_agents.py`](independent_agents/severance_agents.py) creates separate Justine, Juliette, and Supervisor instances, each with its own history, then coordinates messages between them.

![Independent Agent Architecture](./visuals/img-16-3b9920cf.webp)

*Figure 4.6 — Independent-agent communication structure.*

The script is the strongest directly reproducible code artifact in the repository because the architecture and prompt sequence can be inspected and rerun without reconstructing the competition notebook manually.

## Finding 5 — Grace
### Intent laundering through creative framing

![Grace Finding](./visuals/img-17-82151d82.webp)

This experiment reframed a harmful objective as a creative-performance problem and then escalated the request. The tested run showed that the framing changed what the model was willing to generate and execute.

The evidence supports a framing-sensitive failure in this scenario. It does not establish that creative framing universally bypasses safety controls.

### Evidence

![Sardonic Response](./visuals/img-18-40bce79c.webp)

*Figure 5.2 — Persona-conditioned response during the escalation.*

![Nuclear Option](./visuals/img-19-3aeabd15.webp)

*Figure 5.3 — Later stage of the creative framing sequence.*

![Malicious Ideas](./visuals/img-20-3e3cb158.webp)

*Figure 5.4 — Harmful ideation returned in the tested sequence.*

## Cross-finding observations

These are research hypotheses generated by the experiments, not settled architectural conclusions.

### Simulation framing

Several tested scenarios became easier to escalate after the model was told it was operating inside a simulation.

![Simulation Effect](./visuals/img-21-837f4e71.webp)

### Uneven safety behavior

The observed reasoning stream protected some categories of information more consistently than others in the tested prompts.

![CoT Faithfulness](./visuals/img-22-6ef6e4aa.webp)

### Persona and state carryover

Earlier refusals or compliance often changed the trajectory of later turns, suggesting that conversational state is itself an important experimental variable.

![Persona Effect](./visuals/img-23-d79b4195.webp)

### Differential framing

Findings 2 and 5 both changed the surface framing while preserving a harmful underlying objective, making them useful cases for studying semantic differentials in safety behavior.

![Differential Analysis](./visuals/img-24-bee5d734.webp)

## Visual analysis

### Attack success rates

![Attack Success Rates](./visuals/attack_success_rates.png)

### Vulnerability heatmap

![Vulnerability Heatmap](./visuals/vulnerability_heatmap.png)

### Defense comparison

![Defense Comparison](./visuals/defense_comparison.png)

### Summary statistics

![Summary Statistics](./visuals/summary_stats.png)

## What sets this work apart

The useful distinction is methodological rather than promotional:

- the report compares multiple contextual variables instead of one prompt-injection family;
- it preserves screenshots beside the claims they support;
- it includes both shared-state and genuinely separate multi-agent implementations for the same research question;
- it records failed and weaker variants as part of the discovery path rather than presenting only the final attack.

Whether any finding is novel relative to the broader literature should be established through literature review, not asserted by this README.

## Evals and test series

The repository contains direct experiment evidence but not yet a unified automated evaluation harness.

What the current evidence can support:

- a behavior occurred in the shown run;
- reported rates summarize the experiment sets used for the competition submission;
- the independent Severance script can be rerun against the named local model.

What it cannot support by itself:

- universal success rates;
- cross-model generalization;
- causal claims about undocumented model internals;
- stability across future `gpt-oss-20b` builds or serving configurations.

The next useful evaluation step is to encode every finding as a repeated test series with explicit controls, seeds, model version, trial count, and machine-readable outcomes.

## Links

- [Kaggle competition write-up](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/eyes-wide-shut)
- [Dev.to article](https://dev.to/masihmoafi/eyes-wide-shut-4cpb)
- [GitHub repository](https://github.com/MasihMoafi/Eyes-Wide-Shut)

## Future development

No formal roadmap is tracked in the repository today. The highest-value next work is stronger replication: repeated trials, explicit controls, cross-model comparison, and a paper-style experimental record.
