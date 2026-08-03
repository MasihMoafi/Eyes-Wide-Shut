# Finding 1 controlled campaign

This directory is reserved for the corrected French rerun. It is intentionally
empty until the Kaggle campaign is completed.

Expected downloads:

- `finding1_controlled_french.jsonl` — one record for each arm/seed pair;
- `model_version.json` — the exact Ollama model metadata;
- `finding1_controlled_french_summary.json` — the notebook's mechanical endpoint summary.

The campaign has two arms, `fr_nosim` and `fr_sim`, with seeds `0..99` in each
arm. Harness errors remain in the JSONL and are excluded from denominators;
they must be reported, never converted into refusals.

After downloading the JSONL, run:

```text
python experiments/finding1/code/verify_campaign.py \
  experiments/finding1/data/finding1_controlled_french.jsonl
```

Only after that passes should the blind turn-2 review queue be prepared.
