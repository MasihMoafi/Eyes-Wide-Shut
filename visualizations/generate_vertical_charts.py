#!/usr/bin/env python3
"""
Generate publication-quality vertical bar charts with closely-paired bars for Multi-Model EWS results.
Supports both the 4-model comparative view and the focused GPT-OSS family view.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("/home/masih/Desktop/p/eyes-wide-shut-multimodel/visualizations")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica Neue", "Arial"]
plt.rcParams["axes.edgecolor"] = "#d1d5db"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#f3f4f6"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

# Color palette (matching paper & shadcn terracotta/slate)
C_NOSIM = "#334155"    # Slate navy
C_SIM = "#c2410c"      # Terracotta / burnt orange
C_COT = "#b91c1c"      # Crimson / deep red
C_VIS = "#ea580c"      # Vivid orange

def create_multimodel_vertical_chart():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    plt.subplots_adjust(wspace=0.28, top=0.82, bottom=0.18, left=0.06, right=0.96)

    # -------------------------------------------------------------
    # 1. Finding 1: Simulation Framing Effect (Vertical Paired Bars)
    # -------------------------------------------------------------
    ax1 = axes[0]
    ax1.set_facecolor("#ffffff")
    models_f1 = [
        "gpt-oss:20b\n(Paper Baseline)",
        "gpt-oss:120b\n(Flagship)",
        "deepseek-v4-flash\n(Open Reasoning)",
        "gpt-5.6-luna\n(Next-Gen)"
    ]
    nosim = [78.0, 64.0, 91.0, 100.0]
    sim = [97.0, 86.0, 91.0, 99.0]

    x = np.arange(len(models_f1))
    bar_width = 0.32  # Tightly packed bars
    inner_gap = 0.02

    # Draw vertical bars closely adjacent
    rects1 = ax1.bar(x - (bar_width/2 + inner_gap/2), nosim, bar_width, label="No Simulation Framing", color=C_NOSIM, edgecolor="#1e293b", linewidth=0.8, zorder=3)
    rects2 = ax1.bar(x + (bar_width/2 + inner_gap/2), sim, bar_width, label="Simulation Framing", color=C_SIM, edgecolor="#9a3412", linewidth=0.8, zorder=3)

    ax1.set_ylabel("Destructive Tool-Call Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax1.set_title("Finding 1: Simulation Framing Effect\n(Matched Pairs, n=100 per arm)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models_f1, fontsize=9.0, fontweight="600", color="#374151")
    ax1.set_ylim(0, 120)
    ax1.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=8.8)

    for i in range(len(models_f1)):
        h1 = nosim[i]
        h2 = sim[i]
        ax1.annotate(f"{h1:.0f}%", xy=(x[i] - (bar_width/2 + inner_gap/2), h1), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_NOSIM)
        ax1.annotate(f"{h2:.0f}%", xy=(x[i] + (bar_width/2 + inner_gap/2), h2), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_SIM)
        delta = h2 - h1
        delta_str = f"+{delta:.0f}%" if delta > 0 else (f"{delta:.0f}%" if delta < 0 else "0%")
        d_color = C_SIM if delta > 0 else ("#4b5563" if delta == 0 else "#16a34a")
        ax1.annotate(f"Δ: {delta_str}", xy=(x[i], max(h1, h2) + 9), ha="center", fontsize=8.5, fontweight="bold", color=d_color,
                     bbox=dict(boxstyle="round,pad=0.25", fc="#f9fafb", ec=d_color, lw=1))

    # -------------------------------------------------------------
    # 2. Finding 2: Multi-Turn Semantic Reframing Trajectory
    # -------------------------------------------------------------
    ax2 = axes[1]
    ax2.set_facecolor("#ffffff")
    turns = ["Turn 1:\nDirect Ask\n(Refused)", "Turn 2:\nPedagogy\n(Accepted)", "Turns 3-5:\nDecomposed\n(Implementation)", "Final:\nDistress Upsell\n(Monetized)"]
    x2 = np.arange(len(turns))

    ax2.plot(x2, [0, 100, 100, 100], marker="o", markersize=8, linewidth=2.5, label="gpt-oss:20b (Baseline)", color="#dc2626", linestyle="-", zorder=4)
    ax2.plot(x2, [0, 100, 100, 100], marker="s", markersize=7, linewidth=2.0, label="gpt-oss:120b (Flagship)", color="#2563eb", linestyle="--", zorder=4)
    ax2.plot(x2, [0, 100, 100, 100], marker="^", markersize=7, linewidth=1.8, label="deepseek-v4-flash", color="#059669", linestyle=":", zorder=4)
    ax2.plot(x2, [0, 100, 100, 100], marker="D", markersize=6, linewidth=1.8, label="gpt-5.6-luna", color="#7c3aed", linestyle="-.", zorder=4)

    ax2.set_ylabel("Harmful Compliance Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax2.set_title("Finding 2: Multi-Turn Semantic Reframing\n(n=30 Multi-Turn Trajectories)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(turns, fontsize=8.8, fontweight="600", color="#374151")
    ax2.set_ylim(-5, 120)
    ax2.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=8.5)

    ax2.annotate("Universal Cross-Model Vulnerability\nDirect ask refused (0%) → Reframe compliant (100%)",
                 xy=(2, 100), xytext=(0.05, 48),
                 arrowprops=dict(facecolor="#111827", shrink=0.08, width=1, headwidth=5),
                 fontsize=8.2, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#fff7ed", ec="#ea580c", lw=1))

    # -------------------------------------------------------------
    # 3. Finding 3: Secret Exposure (Vertical Paired Bars)
    # -------------------------------------------------------------
    ax3 = axes[2]
    ax3.set_facecolor("#ffffff")
    models_f3 = [
        "gpt-oss:20b\n(Paper Baseline)",
        "gpt-oss:120b\n(Flagship)",
        "deepseek-v4-flash\n(Open Reasoning)",
        "gpt-5.6-luna\n(Next-Gen)"
    ]
    cot_leak = [83.3, 100.0, 93.3, 96.7]
    vis_leak = [43.3, 90.0, 66.7, 73.3]

    x3 = np.arange(len(models_f3))

    rects_cot = ax3.bar(x3 - (bar_width/2 + inner_gap/2), cot_leak, bar_width, label="Reasoning CoT Leakage", color=C_COT, edgecolor="#7f1d1d", linewidth=0.8, zorder=3)
    rects_vis = ax3.bar(x3 + (bar_width/2 + inner_gap/2), vis_leak, bar_width, label="Visible Content Leakage", color=C_VIS, edgecolor="#9a3412", linewidth=0.8, zorder=3)

    ax3.set_ylabel("Secret Canary Exposure Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax3.set_title("Finding 3: Secret Canary Unmasking\n(n=30 Scripted Exception Trials)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax3.set_xticks(x3)
    ax3.set_xticklabels(models_f3, fontsize=9.0, fontweight="600", color="#374151")
    ax3.set_ylim(0, 120)
    ax3.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=8.8)

    for i in range(len(models_f3)):
        hc = cot_leak[i]
        hv = vis_leak[i]
        ax3.annotate(f"{hc:.0f}%", xy=(x3[i] - (bar_width/2 + inner_gap/2), hc), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_COT)
        ax3.annotate(f"{hv:.0f}%", xy=(x3[i] + (bar_width/2 + inner_gap/2), hv), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_VIS)

    fig.suptitle("Multi-Model Frontier Safety Benchmark: Cross-Architecture Generalization", fontsize=13.5, fontweight="bold", color="#111827", y=0.98)

    out_png = OUT_DIR / "multimodel_vertical_barchart.png"
    out_svg = OUT_DIR / "multimodel_vertical_barchart.svg"
    out_pdf = OUT_DIR / "multimodel_vertical_barchart.pdf"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.savefig(out_svg, bbox_inches="tight")
    plt.savefig(out_pdf, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_png}, {out_svg}, {out_pdf}")

if __name__ == "__main__":
    create_multimodel_vertical_chart()

def create_gpt_oss_vertical_chart():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    plt.subplots_adjust(wspace=0.28, top=0.82, bottom=0.18, left=0.08, right=0.96)

    # 1. Finding 1: Simulation Framing (Vertical Paired Bars)
    ax1 = axes[0]
    ax1.set_facecolor("#ffffff")
    models = ["gpt-oss:20b\n(Paper Baseline)", "gpt-oss:120b\n(Flagship)"]
    nosim = [78.0, 64.0]
    sim = [97.0, 86.0]

    x = np.arange(len(models))
    bar_width = 0.28
    inner_gap = 0.015

    ax1.bar(x - (bar_width/2 + inner_gap/2), nosim, bar_width, label="No Simulation Framing", color=C_NOSIM, edgecolor="#1e293b", linewidth=0.8, zorder=3)
    ax1.bar(x + (bar_width/2 + inner_gap/2), sim, bar_width, label="Simulation Framing", color=C_SIM, edgecolor="#9a3412", linewidth=0.8, zorder=3)

    ax1.set_ylabel("Destructive Tool-Call Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax1.set_title("Finding 1: Simulation Framing Effect\n(Matched Pairs, n=100 per arm)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=9.5, fontweight="600", color="#374151")
    ax1.set_ylim(0, 120)
    ax1.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=9.0)

    for i in range(len(models)):
        h1, h2 = nosim[i], sim[i]
        ax1.annotate(f"{h1:.0f}%", xy=(x[i] - (bar_width/2 + inner_gap/2), h1), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color=C_NOSIM)
        ax1.annotate(f"{h2:.0f}%", xy=(x[i] + (bar_width/2 + inner_gap/2), h2), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color=C_SIM)
        delta = h2 - h1
        ax1.annotate(f"Δ: +{delta:.0f}%", xy=(x[i], max(h1, h2) + 9), ha="center", fontsize=9.0, fontweight="bold", color=C_SIM,
                     bbox=dict(boxstyle="round,pad=0.3", fc="#fff7ed", ec=C_SIM, lw=1.1))

    # 2. Finding 2: Multi-Turn Trajectory
    ax2 = axes[1]
    ax2.set_facecolor("#ffffff")
    turns = ["Turn 1:\nDirect Ask\n(Refused)", "Turn 2:\nPedagogy\n(Accepted)", "Turns 3-5:\nDecomposed\n(Implementation)", "Final:\nDistress Upsell\n(Monetized)"]
    x2 = np.arange(len(turns))
    ax2.plot(x2, [0, 100, 100, 100], marker="o", markersize=9, linewidth=2.8, label="gpt-oss:20b (Baseline)", color="#dc2626", linestyle="-", zorder=4)
    ax2.plot(x2, [0, 100, 100, 100], marker="s", markersize=8, linewidth=2.4, label="gpt-oss:120b (Flagship)", color="#2563eb", linestyle="--", zorder=4)

    ax2.set_ylabel("Harmful Compliance Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax2.set_title("Finding 2: Multi-Turn Semantic Reframing\n(n=30 Multi-Turn Trajectories)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(turns, fontsize=9.0, fontweight="600", color="#374151")
    ax2.set_ylim(-5, 120)
    ax2.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=9.0)

    ax2.annotate("Direct ask refused (0%) → Reframe compliant (100%)",
                 xy=(2, 100), xytext=(0.05, 48),
                 arrowprops=dict(facecolor="#111827", shrink=0.08, width=1.1, headwidth=5),
                 fontsize=8.5, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#fff7ed", ec="#ea580c", lw=1))

    # 3. Finding 3: Secret Canary Exposure (Vertical Paired Bars)
    ax3 = axes[2]
    ax3.set_facecolor("#ffffff")
    cot_leak = [83.3, 100.0]
    vis_leak = [43.3, 90.0]

    ax3.bar(x - (bar_width/2 + inner_gap/2), cot_leak, bar_width, label="Reasoning CoT Leakage", color=C_COT, edgecolor="#7f1d1d", linewidth=0.8, zorder=3)
    ax3.bar(x + (bar_width/2 + inner_gap/2), vis_leak, bar_width, label="Visible Content Leakage", color=C_VIS, edgecolor="#9a3412", linewidth=0.8, zorder=3)

    ax3.set_ylabel("Secret Canary Exposure Rate (%)", fontsize=10.5, fontweight="bold", color="#1f2937")
    ax3.set_title("Finding 3: Secret Canary Unmasking\n(n=30 Scripted Exception Trials)", fontsize=11.5, fontweight="bold", color="#111827", pad=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(models, fontsize=9.5, fontweight="600", color="#374151")
    ax3.set_ylim(0, 120)
    ax3.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#e5e7eb", fontsize=9.0)

    for i in range(len(models)):
        hc, hv = cot_leak[i], vis_leak[i]
        ax3.annotate(f"{hc:.1f}%", xy=(x[i] - (bar_width/2 + inner_gap/2), hc), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color=C_COT)
        ax3.annotate(f"{hv:.1f}%", xy=(x[i] + (bar_width/2 + inner_gap/2), hv), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color=C_VIS)

    fig.suptitle("GPT-OSS Model Family: Multi-Vector Safety Analysis (20B vs. 120B)", fontsize=13.5, fontweight="bold", color="#111827", y=0.98)

    out_png = OUT_DIR / "gpt_oss_vertical_barchart.png"
    out_svg = OUT_DIR / "gpt_oss_vertical_barchart.svg"
    out_pdf = OUT_DIR / "gpt_oss_vertical_barchart.pdf"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.savefig(out_svg, bbox_inches="tight")
    plt.savefig(out_pdf, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_png}, {out_svg}, {out_pdf}")

if __name__ == "__main__":
    create_gpt_oss_vertical_chart()
