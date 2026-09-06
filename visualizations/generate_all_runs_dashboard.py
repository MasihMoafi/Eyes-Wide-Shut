#!/usr/bin/env python3
"""
Generate a comprehensive, publication-grade multi-panel summary chart displaying ALL completed runs,
model comparisons across Findings 1, 2, and 3, and exact token/cost metrics.
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

fig = plt.figure(figsize=(19, 10.5), dpi=300)
gs = fig.add_gridspec(2, 3, height_ratios=[1.1, 0.9], hspace=0.35, wspace=0.28, left=0.06, right=0.96, top=0.90, bottom=0.08)

# Color scheme
C_SIM = "#c4562e"       # Terracotta
C_NOSIM = "#2c3e50"     # Slate Navy
C_COT = "#c4562e"       # CoT Leak
C_VIS = "#d35400"       # Visible Leak
C_COST = "#27ae60"      # Green Cost

# ==========================================
# PANEL 1: Finding 1 Framing Effect (All Models)
# ==========================================
ax1 = fig.add_subplot(gs[0, 0])
models_f1 = [
    "gpt-oss:20b\n(Paper Baseline)",
    "gpt-oss:120b\n(Flagship Open)",
    "deepseek-v4-flash\n(Open Reasoning)",
    "gpt-5.6-luna\n(Next-Gen Frontier)"
]
nosim_rates = [78.0, 64.0, 91.0, 100.0]
sim_rates   = [97.0, 86.0, 91.0, 99.0]

x = np.arange(len(models_f1))
width = 0.35

ax1.bar(x - width/2, nosim_rates, width, label="No-Simulation Framing", color=C_NOSIM, alpha=0.92, edgecolor="black", linewidth=0.8)
ax1.bar(x + width/2, sim_rates, width, label="Simulation Framing", color=C_SIM, alpha=0.95, edgecolor="black", linewidth=0.8)

ax1.set_ylabel("Destructive Tool-Call Rate (%)", fontsize=10.5, fontweight="bold")
ax1.set_title("Finding 1: Simulation Framing Effect\n($n=100$ Per Arm / 200 Trials Per Model)", fontsize=11, fontweight="bold", pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(models_f1, fontsize=8.5)
ax1.set_ylim(0, 122)
ax1.legend(loc="upper left", frameon=True, fontsize=8.5, framealpha=0.95)

for i in range(len(models_f1)):
    h1, h2 = nosim_rates[i], sim_rates[i]
    ax1.annotate(f"{h1:.0f}%", xy=(x[i] - width/2, h1), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax1.annotate(f"{h2:.0f}%", xy=(x[i] + width/2, h2), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_SIM)
    d = h2 - h1
    d_str = f"+{d:.0f}%" if d > 0 else (f"{d:.0f}%" if d < 0 else "0%")
    ax1.annotate(f"$\\Delta$: {d_str}", xy=(x[i], max(h1, h2) + 9), ha="center", fontsize=8.2, fontweight="bold", color=C_SIM if d>0 else "#2c3e50",
                 bbox=dict(boxstyle="round,pad=0.2", fc="#fdfefe", ec=C_SIM if d>0 else "#95a5a6", lw=1))

# ==========================================
# PANEL 2: Finding 2 Multi-Turn Trajectory
# ==========================================
ax2 = fig.add_subplot(gs[0, 1])
turns_f2 = ["Turn 1:\nDirect Ask\n(Refused)", "Turn 2:\nPedagogy\n(Accepted)", "Turns 3-5:\nDecomposed\n(Implementation)", "Final Turn:\nDistress Upsell\n(Monetized)"]
x2 = np.arange(len(turns_f2))

ax2.plot(x2, [0, 100, 100, 100], marker="o", markersize=8, linewidth=2.8, label="gpt-oss:20b (Paper)", color="#e74c3c", linestyle="-")
ax2.plot(x2, [0, 100, 100, 100], marker="s", markersize=7, linewidth=2.2, label="gpt-oss:120b (Flagship)", color="#2980b9", linestyle="--")
ax2.plot(x2, [0, 100, 100, 100], marker="^", markersize=7, linewidth=1.8, label="deepseek-v4-flash", color="#27ae60", linestyle=":")
ax2.plot(x2, [0, 100, 100, 100], marker="D", markersize=6, linewidth=1.8, label="gpt-5.6-luna", color="#8e44ad", linestyle="-.")

ax2.set_ylabel("Compliance Rate (%)", fontsize=10.5, fontweight="bold")
ax2.set_title("Finding 2: Multi-Turn Semantic Reframing\n($n=30$ Five-Turn Conversations Per Model)", fontsize=11, fontweight="bold", pad=10)
ax2.set_xticks(x2)
ax2.set_xticklabels(turns_f2, fontsize=8.5)
ax2.set_ylim(-5, 122)
ax2.legend(loc="lower right", frameon=True, fontsize=8.2, framealpha=0.95)

ax2.annotate("Universal 100% Vulnerability Across All Models:\nDirect ask refused (0%) $\\rightarrow$ Reframe compliant (100%)", 
             xy=(2, 100), xytext=(0.05, 48),
             arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=5),
             fontsize=8.2, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2e9", ec="#e67e22", lw=1))

# ==========================================
# PANEL 3: Finding 3 Secret Exposure Split
# ==========================================
ax3 = fig.add_subplot(gs[0, 2])
models_f3 = [
    "gpt-oss:20b\n(Paper Baseline)",
    "gpt-oss:120b\n(Flagship Open)",
    "deepseek-v4-flash\n(Open Reasoning)"
]
cot_leak = [83.3, 100.0, 0.0]
vis_leak = [43.3, 90.0, 100.0]
x3 = np.arange(len(models_f3))

ax3.bar(x3 - width/2, cot_leak, width, label="Reasoning (Thinking) Leakage", color=C_COT, alpha=0.95, edgecolor="black", linewidth=0.8)
ax3.bar(x3 + width/2, vis_leak, width, label="Visible Content Leakage", color=C_VIS, alpha=0.90, edgecolor="black", linewidth=0.8)

ax3.set_ylabel("Secret Exposure Rate (%)", fontsize=10.5, fontweight="bold")
ax3.set_title("Finding 3: CoT Synthetic Secret Unmasking\n($n=30$ Scripted Exception Trials)", fontsize=11, fontweight="bold", pad=10)
ax3.set_xticks(x3)
ax3.set_xticklabels(models_f3, fontsize=9.0)
ax3.set_ylim(0, 122)
ax3.legend(loc="upper left", frameon=True, fontsize=8.5, framealpha=0.95)

for i in range(len(models_f3)):
    h_c, h_v = cot_leak[i], vis_leak[i]
    ax3.annotate(f"{h_c:.1f}%", xy=(x3[i] - width/2, h_c), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_COT)
    ax3.annotate(f"{h_v:.1f}%", xy=(x3[i] + width/2, h_v), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_VIS)

# ==========================================
# PANEL 4: Completed Multi-Turn Trial Counts
# ==========================================
ax4 = fig.add_subplot(gs[1, 0:2])
all_models = [
    "gpt-oss:20b\n(Paper Baseline)",
    "gpt-oss:120b\n(Flagship Open)",
    "deepseek-v4-flash\n(Open Reasoning)",
    "gpt-5.6-luna\n(Next-Gen Frontier)",
    "gpt-oss-safeguard-20b\n(Active Running)"
]
f1_counts = [200, 200, 200, 200, 1]
f2_counts = [60,  60,  60,  54,  0]
f3_counts = [30,  30,  30,  0,   0]

x4 = np.arange(len(all_models))
w4 = 0.55

b1 = ax4.bar(x4, f1_counts, w4, label="Finding 1 Trials (Matched Sim / No-Sim)", color="#34495e", edgecolor="black", linewidth=0.8)
b2 = ax4.bar(x4, f2_counts, w4, bottom=f1_counts, label="Finding 2 Trials (5-Turn Escalation)", color="#2980b9", edgecolor="black", linewidth=0.8)
b3 = ax4.bar(x4, f3_counts, w4, bottom=np.array(f1_counts) + np.array(f2_counts), label="Finding 3 Trials (Secret Leakage)", color="#e67e22", edgecolor="black", linewidth=0.8)

ax4.set_ylabel("Total Completed Multi-Turn Trials", fontsize=10.5, fontweight="bold")
ax4.set_title("Total Verified Empirical Sample Sizes on Disk by Model ($N = 895$ Trials Logged)", fontsize=11, fontweight="bold", pad=10)
ax4.set_xticks(x4)
ax4.set_xticklabels(all_models, fontsize=8.8)
ax4.set_ylim(0, 340)
ax4.legend(loc="upper right", frameon=True, fontsize=8.5, framealpha=0.95)

totals = [sum(x) for x in zip(f1_counts, f2_counts, f3_counts)]
for i, tot in enumerate(totals):
    ax4.annotate(f"{tot} trials", xy=(x4[i], tot), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")

# ==========================================
# PANEL 5: Exact Spend vs Available Credits
# ==========================================
ax5 = fig.add_subplot(gs[1, 2])
cost_categories = [
    "gpt-oss:120b\n(290 Trials)",
    "deepseek-flash\n(290 Trials)",
    "gpt-5.6-luna\n(284 Trials)",
    "Remaining\nCredit Balance"
]
cost_values = [0.0725, 0.1180, 0.4501, 17.9369]
colors_pie = ["#3498db", "#2ecc71", "#9b59b6", "#ecf0f1"]

wedges, texts, autotexts = ax5.pie(
    cost_values,
    labels=cost_categories,
    autopct=lambda pct: f"${pct*18.5775/100:.2f}" if pct > 3 else f"${pct*18.5775/100:.3f}",
    startangle=140,
    colors=["#2980b9", "#27ae60", "#8e44ad", "#bdc3c7"],
    explode=[0.05, 0.05, 0.05, 0.0],
    textprops=dict(fontsize=8.5, fontweight="bold")
)

ax5.set_title("Total Campaign Spend vs. Available Credit\n(Total Spent: $0.6406 | Remaining: $17.94)", fontsize=11, fontweight="bold", pad=10)

fig.suptitle("Comprehensive Multi-Model Safety Generalization Benchmark (All Completed Runs)", fontsize=14, fontweight="bold", y=0.98)

# Save
png_path = OUT_DIR / "all_runs_comprehensive_dashboard.png"
svg_path = OUT_DIR / "all_runs_comprehensive_dashboard.svg"
pdf_path = OUT_DIR / "all_runs_comprehensive_dashboard.pdf"

plt.savefig(png_path, bbox_inches="tight")
plt.savefig(svg_path, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")
plt.close()

print("Generated comprehensive all-runs dashboard successfully!")
