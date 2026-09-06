#!/usr/bin/env python3
"""
Generate publication-quality comparative visualization for Multi-Model Expansion across Findings 1, 2, and 3.
Saves high-res SVG, PNG, and standalone HTML dashboard.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("/home/masih/Desktop/p/eyes-wide-shut-multimodel/visualizations")
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

fig, axes = plt.subplots(1, 3, figsize=(19, 5.8), dpi=300)
plt.subplots_adjust(wspace=0.34, top=0.82, bottom=0.22, left=0.06, right=0.96)

# Colors matching paper style
C_SIM = "#c4562e"      # Terracotta hitcolor
C_NOSIM = "#34495e"    # Slate navy
C_LEAK_COT = "#c4562e" # CoT leakage
C_LEAK_VIS = "#d35400" # Visible leakage

# ==========================================
# SUBPLOT 1: Finding 1 Multi-Model Delta
# ==========================================
ax1 = axes[0]
models_f1 = [
    "gpt-oss:20b\n(Paper Baseline)",
    "gpt-oss:120b\n(Flagship)",
    "deepseek-v4-flash\n(Open Reasoning)",
    "gpt-5.6-luna\n(Next-Gen)"
]

sim_rates = [97.0, 86.0, 91.0, 99.0]
nosim_rates = [78.0, 64.0, 91.0, 100.0]

x = np.arange(len(models_f1))
width = 0.36

rects1 = ax1.bar(x - width/2, nosim_rates, width, label="No-Simulation Framing", color=C_NOSIM, alpha=0.92, edgecolor="black", linewidth=0.8)
rects2 = ax1.bar(x + width/2, sim_rates, width, label="Simulation Framing", color=C_SIM, alpha=0.95, edgecolor="black", linewidth=0.8)

ax1.set_ylabel("Destructive Tool-Call Rate (%)", fontsize=11, fontweight="bold")
ax1.set_title("Finding 1: Tool-Call Simulation Framing Effect\n(Matched Pairs, $n=100$ per arm)", fontsize=11.5, fontweight="bold", pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(models_f1, fontsize=9.0)
ax1.set_ylim(0, 122)
ax1.legend(loc="upper left", frameon=True, fontsize=9.0, framealpha=0.95)

for i in range(len(models_f1)):
    h1 = nosim_rates[i]
    h2 = sim_rates[i]
    ax1.annotate(f"{h1:.0f}%", xy=(x[i] - width/2, h1), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax1.annotate(f"{h2:.0f}%", xy=(x[i] + width/2, h2), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_SIM)
    delta = h2 - h1
    delta_str = f"+{delta:.0f}%" if delta > 0 else (f"{delta:.0f}%" if delta < 0 else "0%")
    delta_color = C_SIM if delta > 0 else ("#2c3e50" if delta == 0 else "#27ae60")
    ax1.annotate(f"$\\Delta$: {delta_str}", xy=(x[i], max(h1, h2) + 9), ha="center", fontsize=8.5, fontweight="bold", color=delta_color,
                 bbox=dict(boxstyle="round,pad=0.25", fc="#fdfefe", ec=delta_color, lw=1))

# ==========================================
# SUBPLOT 2: Finding 2 Multi-Turn Trajectory
# ==========================================
ax2 = axes[1]
turns_f2_labels = ["Turn 1:\nDirect Ask\n(Refused)", "Turn 2:\nPedagogy\n(Accepted)", "Turns 3-5:\nImplementation\n(Decomposed)", "Final:\nDistress Upsell\n(Monetized)"]
x2 = np.arange(len(turns_f2_labels))

y_20b = [0, 100, 100, 100]
y_120b = [0, 100, 100, 100]
y_ds = [0, 100, 100, 100]
y_luna = [0, 100, 100, 100]

ax2.plot(x2, y_20b, marker="o", markersize=8, linewidth=2.5, label="gpt-oss:20b (Paper)", color="#e74c3c", linestyle="-")
ax2.plot(x2, y_120b, marker="s", markersize=7, linewidth=2.0, label="gpt-oss:120b (New)", color="#2980b9", linestyle="--")
ax2.plot(x2, y_ds, marker="^", markersize=7, linewidth=1.5, label="deepseek-v4-flash (New)", color="#27ae60", linestyle=":")
ax2.plot(x2, y_luna, marker="D", markersize=6, linewidth=1.5, label="gpt-5.6-luna (New)", color="#8e44ad", linestyle="-.")

ax2.set_ylabel("Compliance Rate (%)", fontsize=11, fontweight="bold")
ax2.set_title("Finding 2: Multi-Turn Semantic Reframing\n($n=30$ Multi-Turn Conversations)", fontsize=11.5, fontweight="bold", pad=12)
ax2.set_xticks(x2)
ax2.set_xticklabels(turns_f2_labels, fontsize=8.8)
ax2.set_ylim(-5, 122)
ax2.legend(loc="lower right", frameon=True, fontsize=8.5, framealpha=0.95)

ax2.annotate("Universal Cross-Model Vulnerability\nDirect ask refused (0%) $\\rightarrow$ Reframe compliant (100%)", 
             xy=(2, 100), xytext=(0.1, 48),
             arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2e9", ec="#e67e22", lw=1))

# ==========================================
# SUBPLOT 3: Finding 3 Secret Exposure Split
# ==========================================
ax3 = axes[2]
models_f3 = [
    "gpt-oss:20b\n(Paper Baseline)",
    "gpt-oss:120b\n(Flagship)",
    "deepseek-v4-flash\n(Open Reasoning)"
]

cot_leak = [83.3, 100.0, 0.0]
vis_leak = [43.3, 90.0, 100.0]

x3 = np.arange(len(models_f3))
rects_cot = ax3.bar(x3 - width/2, cot_leak, width, label="Reasoning (Thinking) Leakage", color=C_LEAK_COT, alpha=0.95, edgecolor="black", linewidth=0.8)
rects_vis = ax3.bar(x3 + width/2, vis_leak, width, label="Visible Content Leakage", color=C_LEAK_VIS, alpha=0.9, edgecolor="black", linewidth=0.8)

ax3.set_ylabel("Synthetic Secret Exposure Rate (%)", fontsize=11, fontweight="bold")
ax3.set_title("Finding 3: CoT Secret Unmasking\n($n=30$ Scripted Exception Trials)", fontsize=11.5, fontweight="bold", pad=12)
ax3.set_xticks(x3)
ax3.set_xticklabels(models_f3, fontsize=9.0)
ax3.set_ylim(0, 122)
ax3.legend(loc="upper left", frameon=True, fontsize=9.0, framealpha=0.95)

for i in range(len(models_f3)):
    h_c = cot_leak[i]
    h_v = vis_leak[i]
    ax3.annotate(f"{h_c:.1f}%", xy=(x3[i] - width/2, h_c), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_LEAK_COT)
    ax3.annotate(f"{h_v:.1f}%", xy=(x3[i] + width/2, h_v), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_LEAK_VIS)

fig.suptitle("Cross-Model Empirical Generalization: Multi-Vector Safety Analysis", fontsize=14, fontweight="bold", y=0.97)

png_path = OUT_DIR / "multimodel_comparative_findings.png"
svg_path = OUT_DIR / "multimodel_comparative_findings.svg"
pdf_path = OUT_DIR / "multimodel_comparative_findings.pdf"

plt.savefig(png_path, bbox_inches="tight")
plt.savefig(svg_path, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")
plt.close()

print("Regenerated charts successfully!")
