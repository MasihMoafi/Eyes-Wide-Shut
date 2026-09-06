#!/usr/bin/env python3
"""Build paper tables and figures from audited saved records, offline."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/new/generated"
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads((ROOT / "analysis/results/metrics.json").read_text())
names = ["gpt-oss-20b (local)", "gpt-oss-120b", "DeepSeek V4 Flash", "GPT-5.6 Luna", "safeguard-20b*"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42})

def write(name, text):
    (OUT / name).write_text(text + "\n")

def table(name, headings, rows, spec):
    lines = [r"\begin{tabular}{" + spec + "}", r"\toprule", " & ".join(headings) + r" \\", r"\midrule"]
    lines += [" & ".join(map(str, row)) + r" \\" for row in rows]
    lines += [r"\bottomrule", r"\end{tabular}"]
    write(name + ".tex", "\n".join(lines))
    with (OUT / (name + ".csv")).open("w") as f:
        w = csv.writer(f)
        w.writerow(headings)
        w.writerows(rows)

f1 = list(data["finding1"].values())
f3 = list(data["finding3"].values())
table("finding1", ["Deployment", "No simulation", "Simulation", r"$\Delta$ (pp)"],
      [[name, f"{r['no_simulation_calls']}/{r['n_per_arm']}", f"{r['simulation_calls']}/{r['n_per_arm']}",
        f"{r['difference_percentage_points']:+.0f}"] for name, r in zip(names, f1)], "lrrr")
table("finding1-pairs", ["Deployment", "Both", "Sim. only", "No-sim. only", "Neither"],
      [[name] + [r["paired"][k] for k in ("both", "simulation_only", "no_simulation_only", "neither")]
       for name, r in zip(names, f1)], "lrrrr")
table("finding3", ["Deployment", "Pre-auth. R", "Post-auth. R", "Post-auth. F", r"R + refusal"],
      [[name,
        f"{r['turns']['1']['reasoning_contains']}/30" if r['turns']['1']['reasoning_rate'] is not None else "N/O",
        f"{r['turns']['2']['reasoning_contains']}/30" if r['turns']['2']['reasoning_rate'] is not None else "N/O",
        f"{r['turns']['2']['final_contains']}/30",
        str(r['turns']['2']['reasoning_with_explicit_final_refusal']) if r['turns']['2']['reasoning_rate'] is not None else "N/O"]
       for name, r in zip(names, f3)], "lrrrr")
table("finding3-overlap", ["Deployment", "Both", "Reasoning only", "Final only", "Neither"],
      [[name] + ([r['turns']['2'][k] for k in ("both", "reasoning_only", "final_only", "neither")]
                 if r['turns']['2']['reasoning_rate'] is not None else ["N/O"] * 4)
       for name, r in zip(names, f3)], "lrrrr")

fig, ax = plt.subplots(figsize=(7.6, 3.5))
ys = range(5)
for off, key, label, color in [(-.17, "no_simulation_calls", "No simulation", "#65758B"),
                               (.17, "simulation_calls", "Simulation", "#AE582D")]:
    vals = [r[key] for r in f1]
    ax.barh([y+off for y in ys], vals, height=.29, color=color, label=label)
    for y, v in zip(ys, vals):
        ax.text(v+1, y+off, str(v), va="center", fontsize=9)
ax.set(yticks=list(ys), yticklabels=names, xlim=(0, 111), xlabel="Exact tool calls / 100 saved trials per arm")
ax.invert_yaxis()
ax.set_xticks([0, 25, 50, 75, 100])
ax.legend(loc="lower right", frameon=False, ncol=2, bbox_to_anchor=(1, 1))
fig.tight_layout()
fig.savefig(OUT / "finding1.pdf")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.6), sharey=True)
for ax, t, title in zip(axes, ("1", "2"), ("Before second credential", "After release is authorized")):
    for off, key, label, color in [(-.17, "reasoning_contains", "Returned reasoning", "#74649B"),
                                  (.17, "final_contains", "Final answer", "#2D7A83")]:
        for y, row in enumerate(f3):
            r = row["turns"][t]
            if key == "reasoning_contains" and r["reasoning_rate"] is None:
                ax.text(1, y+off, "not observed", va="center", fontsize=8, color="#666666")
            else:
                v = r[key]
                ax.barh(y+off, v, height=.29, color=color, label=label if y == 0 else None)
                ax.text(v+.4, y+off, str(v), va="center", fontsize=9)
    ax.set(title=title, xlim=(0, 35), xlabel="Exact secret matches / 30 trials", xticks=[0, 10, 20, 30])
axes[0].set(yticks=list(ys), yticklabels=names)
axes[0].invert_yaxis()
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(.6, 1.07))
fig.tight_layout()
fig.savefig(OUT / "finding3.pdf", bbox_inches="tight")
plt.close(fig)

macros = {}
for label, r in zip(("Local", "Oss", "Deepseek", "Luna", "Safeguard"), f1):
    macros[label + "FOneSim"] = r["simulation_calls"]
    macros[label + "FOneNoSim"] = r["no_simulation_calls"]
for label, r in zip(("Local", "Oss", "Deepseek", "Luna", "Safeguard"), f3):
    macros[label + "PreReason"] = r["turns"]["1"]["reasoning_contains"]
    macros[label + "PostReason"] = r["turns"]["2"]["reasoning_contains"]
    macros[label + "PostFinal"] = r["turns"]["2"]["final_contains"]
    macros[label + "ReasonRefusal"] = r["turns"]["2"]["reasoning_with_explicit_final_refusal"]
macros["OssUpsellShortRefusal"] = data["finding2"]["exact_short_refusals"]["openai/gpt-oss-120b|escalation_condensed|upsell_attack"]
macros["ReviewCaseCount"] = data["finding2"]["review_cases"]
macros["NaturalProbes"] = sum(data["finding2"]["exact_short_refusals"].values())
if data["finding2"].get("noncompliant_with_implementation"):
    macros["CodeDespiteRefusal"] = sum(data["finding2"]["noncompliant_with_implementation"].values())
review = ROOT / "analysis/review/verification.json"
if review.exists():
    verification = json.loads(review.read_text())
    macros["ReviewBatches"] = len([b for b in verification["batches"] if b["status"] == "pass"])
    macros["OverlapCompared"] = verification["overlap_compared"]
    macros["OverlapAgreed"] = int(verification["overlap_agreement"].split("/")[0])
    macros["Adjudicated"] = len(verification["overlap_disagreements"])
write("numbers.tex", "\n".join("\\newcommand{\\" + k + "}{" + str(v) + "}" for k, v in macros.items()))
print(f"Generated 4 tables, 2 figures and numerical macros in {OUT}")

f2 = data["finding2"].get("counts")
if f2:
    api = [("openai/gpt-oss-120b", "gpt-oss-120b"), ("deepseek/deepseek-v4-flash", "DeepSeek V4 Flash"),
           ("openai/gpt-5.6-luna", "GPT-5.6 Luna"), ("openai/gpt-oss-safeguard-20b", "safeguard-20b*")]
    phases = [("escalation_full", "direct_attack", "Direct ask"),
              ("escalation_full", "benevolent_reframe", "Reframe"),
              ("escalation_full", "pseudocode_emotional", "Emotional"),
              ("escalation_full", "pseudocode_peer", "Peer"),
              ("escalation_full", "pseudocode_guardian", "Guardian"),
              ("escalation_condensed", "setup_ack", "Setup"),
              ("escalation_condensed", "upsell_attack", "Upsell")]
    labels = ["complies", "partial_compliance", "refuses", "nonresponsive", "uncertain_or_ambiguous"]
    cell = lambda model, arm, phase: f2[f"{model}|{arm}|{phase}"]
    table("finding2", ["Deployment"] + [p[2] for p in phases],
          [[label] + [str(cell(model, arm, phase)["complies"]) for arm, phase, _ in phases]
           for model, label in api], "l" + "r" * len(phases))
    rows = []
    for model, label in api:
        for arm, phase, title in phases:
            counts = cell(model, arm, phase)
            if counts["complies"] != 30:
                rows.append([label, title] + [counts[k] for k in labels])
    table("finding2-labels", ["Deployment", "Phase", "Compl.", "Partial", "Refuses", "Nonresp.", "Uncert."],
          rows, "ll" + "r" * len(labels))

    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    width, xs = 0.2, range(len(phases))
    for index, ((model, label), color) in enumerate(zip(api, ["#AE582D", "#65758B", "#2F6F5E", "#7A5C99"])):
        vals = [cell(model, arm, phase)["complies"] for arm, phase, _ in phases]
        ax.bar([x + (index - 1.5) * width for x in xs], vals, width=width, color=color, label=label)
    ax.set(xticks=list(xs), xticklabels=[p[2] for p in phases], ylim=(0, 34),
           ylabel="Judged \\textit{complies} / 30")
    ax.set_ylabel("Judged complies / 30")
    ax.legend(frameon=False, ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.16))
    fig.tight_layout()
    fig.savefig(OUT / "finding2.pdf")
    plt.close(fig)
