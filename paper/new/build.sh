#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m unittest discover -s analysis -q
python3 analysis/audit.py --reviews analysis/review/reviews.jsonl > analysis/results/build-summary.json
python3 analysis/build_artifacts.py
cd paper/new
for document in main preprint elsevier; do
    for pass_number in 1 2 3; do
        pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
    done
done
printf '%s\n' "Built paper/new/main.pdf, preprint.pdf and elsevier.pdf (working drafts)."
