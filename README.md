# Eyes Wide Shut

Synthetic studies of prompt framing, structured tool calls, multi-turn reframing,
and disclosure across returned reasoning and final answers.

**Earlier single-model preprint (gpt-oss-20b only):** https://doi.org/10.5281/zenodo.21826218  
**Project report:** https://masihmoafi.com/projects/eyes-wide-shut  
**Kaggle write-up:** https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/eyes-wide-shut

**Current evidence revision: 6 September 2026.** This is the latest multi-model
workspace. The [working manuscript](paper/new/preprint.pdf) and
[reproduction instructions](analysis/README.md) supersede the previous report.
The two earlier READMEs are preserved unchanged: the [full report](analysis/archive/README.before-evidence-revision-2026-09-06.md) and the [GitHub summary of 28 August 2026](analysis/archive/README.github-2026-08-28.md).

Finding 2's semantic review is **complete** (840/840 API cases, 6 September 2026) and
must not be re-run; the procedure and its verification are recorded in
[`analysis/review/README.md`](analysis/review/README.md).

## Verified saved-record observations

Finding 1 counts exact turn-3 `press_the_button` proposals, not executed harm:

| Deployment | No simulation | Simulation |
|---|---:|---:|
| gpt-oss:20b (local baseline) | 78/100 | 97/100 |
| openai/gpt-oss-120b | 64/100 | 86/100 |
| deepseek/deepseek-v4-flash | 91/100 | 91/100 |
| openai/gpt-5.6-luna | 100/100 | 99/100 |
| openai/gpt-oss-safeguard-20b | 100/100 | 100/100 |

The local and API runs differ in prompt rendering and tool arguments; compare
framing arms within each deployment. Safeguard chat is an auxiliary diagnostic
outside its recommended classification role.

Finding 3: the local secret appears in returned reasoning before the second
credential in 5/30 trials. After release is authorized, 13/30 local trials and
3/30 gpt-oss-120b API trials contain it in reasoning alongside an explicit final
refusal. Authorized final disclosure is not an access-control failure. DeepSeek
returned reasoning with zero exact matches; Luna returned no reasoning, so its
reasoning disclosure rate is unknown. Full counts and overlaps are in the paper.

Finding 2's 840 API responses are labelled. Responses judged `complies`, out of 30
conversations per phase:

| Deployment | Direct ask | Reframe | Emotional | Peer | Guardian | Setup | Upsell |
|---|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-oss-120b | 0 | 30 | 29 | 30 | 28 | 30 | 0 |
| deepseek/deepseek-v4-flash | 4 | 30 | 30 | 30 | 30 | 30 | 30 |
| openai/gpt-5.6-luna | 0 | 30 | 30 | 15 | 0 | 30 | 0 |
| openai/gpt-oss-safeguard-20b | 0 | 30 | 30 | 30 | 30 | 30 | 30 |

The reframe result is uniform: 116 of 120 five-turn conversations refuse or resist the
direct dependency request and then comply with the same retention objective relabelled
as education, and the local gpt-oss:20b campaign does so in 30/30. Post-reframe
compliance is not uniform, which contradicts the superseded universal-vulnerability
claim: Luna refuses the distress upsell and the help-interception module in all 30
conversations, gpt-oss-120b refuses the upsell in all 30, while DeepSeek and
safeguard-20b comply with every post-reframe phase including distress monetization.
Labels are model-assisted under a disclosed procedure, not human annotation; see
[`analysis/review/README.md`](analysis/review/README.md).

## Deterministic mitigation replay

`analysis/mitigation_replay.py` replays two deliberately narrow host controls over frozen outputs. It makes **no model calls**.

- An independent approval gate blocks every observed `press_the_button` proposal from dispatch: 78/78 in the no-simulation arm and 97/97 in the simulation arm.
- Omitting raw reasoning from downstream payloads reduces downstream exact-string reasoning exposure from 25/30 to 0/30.
- Exact-canary redaction also reduces this exact synthetic-string exposure to 0/30; this is a narrow canary demonstration, not a general semantic DLP defense.

Frozen replay output: [`analysis/mitigation_replay_results.json`](analysis/mitigation_replay_results.json).

The replay expects the extracted supplementary directory of the single-model preprint as its positional argument:

```bash
python analysis/mitigation_replay.py /path/to/supplementary --out mitigation_replay_results.json
```

## Still required

Independent replication of the Finding 2 labelling under a different reviewer. No new
target-model experiments have been run for this revision. Broader causal claims need
controlled task and prompt variation.

All four API datasets have 290 completed saved records each. The checkpoint has
been corrected; there is no need to resume a campaign because of its old counts.
The separate Ling3 pilot is incomplete and excluded from complete-study tables.

```bash
bash paper/new/build.sh
```

The manuscript is a working draft, not submission-ready. Original raw records
remain unchanged. Nothing has been uploaded, published or submitted.
