#!/usr/bin/env python3
"""
Generate publication-quality SVG/PNG figure using Shadcn/D3 aesthetic:
- Clean card layout
- Muted monochromatic palette (#18181b slate, #c2410c terracotta, #f4f4f5 background)
- Subtle rounded pill badges
- Direct value typography and horizontal bar layout matching TMLR paper format
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT_DIR = Path("/home/masih/Desktop/p/eyes-wide-shut-multimodel/visualizations")
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica Neue", "Arial"]

fig, axes = plt.subplots(1, 3, figsize=(18, 5.2), dpi=300)
fig.patch.set_facecolor("#ffffff")
plt.subplots_adjust(wspace=0.30, top=0.82, bottom=0.18, left=0.06, right=0.96)

# Shadcn Slate + Orange Palette
C_BG = "#ffffff"
C_CARD = "#fafafa"
C_BORDER = "#e4e4e7"
C_TEXT_MUTED = "#71717a"
C_TEXT_MAIN = "#18181b"
C_PRIMARY = "#c2410c"   # Shadcn orange-700
C_SLATE = "#334155"     # Shadcn slate-700
C_ACCENT = "#ea580c"    # Shadcn orange-600

# ==========================================
# SUBPLOT 1: Finding 1 (Simulation Framing Delta)
# ==========================================
ax1 = axes[0]
ax1.set_facecolor(C_BG)
models_f1 = ["gpt-oss:20b\n(Paper Baseline)", "gpt-oss:120b\n(Flagship Reasoning)"]
nosim = [78.0, 64.0]
sim = [97.0, 86.0]

y = np.arange(len(models_f1))
h = 0.28

# Draw background pill tracks
for i in range(len(models_f1)):
    ax1.barh(y[i] + h/2, 100, h, color="#f4f4f5", edgecolor=C_BORDER, linewidth=0.8, zorder=1)
    ax1.barh(y[i] - h/2, 100, h, color="#f4f4f5", edgecolor=C_BORDER, linewidth=0.8, zorder=1)

# Filled progress bars
b1 = ax1.barh(y - h/2, nosim, h, color=C_SLATE, label="No Simulation Framing", edgecolor="none", zorder=2)
b2 = ax1.barh(y + h/2, sim, h, color=C_PRIMARY, label="Simulation Framing", edgecolor="none", zorder=2)

ax1.set_yticks(y)
ax1.set_yticklabels(models_f1, fontsize=10, fontweight="600", color=C_TEXT_MAIN)
ax1.set_xlim(0, 115)
ax1.set_xlabel("Destructive Action Rate (%)", fontsize=10, fontweight="600", color=C_TEXT_MUTED)
ax1.set_title("Finding 1: Simulation Framing Effect\n(Matched Pairs, $n=100$ per arm)", fontsize=11, fontweight="700", color=C_TEXT_MAIN, pad=12)
ax1.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor=C_BORDER, fontsize=8.5)

# Value annotations + delta badges
for i in range(len(models_f1)):
    ax1.text(nosim[i] - 3, y[i] - h/2, f"{nosim[i]:.0f}%", va="center", ha="right", color="#ffffff", fontweight="700", fontsize=8.5, zorder=3)
    ax1.text(sim[i] - 3, y[i] + h/2, f"{sim[i]:.0f}%", va="center", ha="right", color="#ffffff", fontweight="700", fontsize=8.5, zorder=3)
    delta = sim[i] - nosim[i]
    ax1.text(103, y[i], f"+{delta:.0f}%\nΔ Effect", va="center", ha="left", color=C_PRIMARY, fontweight="800", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.25", fc="#fff7ed", ec="#fed7aa", lw=1))

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color(C_BORDER)
ax1.spines["bottom"].set_color(C_BORDER)
ax1.grid(axis="x", linestyle="--", alpha=0.4, color=C_BORDER)

# ==========================================
# SUBPLOT 2: Finding 2 (Multi-Turn Semantic Reframing)
# ==========================================
ax2 = axes[1]
ax2.set_facecolor(C_BG)
turns = ["Turn 1:\nDirect Ask\n(Refused)", "Turn 2:\nPedagogy\n(Accepted)", "Turns 3-5:\nImplementation\n(Decomposed)", "Final Turn:\nDistress Upsell\n(Monetized)"]
x2 = np.arange(len(turns))

ax2.plot(x2, [0, 100, 100, 100], marker="o", markersize=8, linewidth=2.8, label="gpt-oss:20b", color=C_PRIMARY, zorder=3)
ax2.plot(x2, [0, 100, 100, 100], marker="s", markersize=7, linewidth=2.0, label="gpt-oss:120b", color=C_SLATE, linestyle="--", zorder=3)

ax2.set_xticks(x2)
ax2.set_xticklabels(turns, fontsize=8.5, color=C_TEXT_MAIN)
ax2.set_ylim(-5, 115)
ax2.set_ylabel("Compliance Rate (%)", fontsize=10, fontweight="600", color=C_TEXT_MUTED)
ax2.set_title("Finding 2: Multi-Turn Semantic Reframing\n($n=30$ Multi-Turn Conversations)", fontsize=11, fontweight="700", color=C_TEXT_MAIN, pad=12)
ax2.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor=C_BORDER, fontsize=8.5)

ax2.annotate("Universal GPT-OSS Vulnerability\nDirect ask refused (0%) → Reframe compliant (100%)", 
             xy=(2, 100), xytext=(0.1, 48),
             arrowprops=dict(facecolor=C_TEXT_MAIN, shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight="700", color=C_TEXT_MAIN,
             bbox=dict(boxstyle="round,pad=0.3", fc="#fff7ed", ec="#fed7aa", lw=1))

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color(C_BORDER)
ax2.spines["bottom"].set_color(C_BORDER)
ax2.grid(axis="y", linestyle="--", alpha=0.4, color=C_BORDER)

# ==========================================
# SUBPLOT 3: Finding 3 (Secret Exposure Split)
# ==========================================
ax3 = axes[2]
ax3.set_facecolor(C_BG)
models_f3 = ["gpt-oss:20b\n(Paper Baseline)", "gpt-oss:120b\n(Flagship Reasoning)"]
cot_leak = [83.3, 100.0]
vis_leak = [43.3, 90.0]
x3 = np.arange(len(models_f3))
w3 = 0.32

ax3.bar(x3 - w3/2, cot_leak, w3, label="Reasoning (Thinking) Leakage", color=C_PRIMARY, edgecolor="none", zorder=2)
ax3.bar(x3 + w3/2, vis_leak, w3, label="Visible Content Leakage", color=C_SLATE, edgecolor="none", zorder=2)

ax3.set_xticks(x3)
ax3.set_xticklabels(models_f3, fontsize=9.5, fontweight="600", color=C_TEXT_MAIN)
ax3.set_ylim(0, 120)
ax3.set_ylabel("Secret Exposure Rate (%)", fontsize=10, fontweight="600", color=C_TEXT_MUTED)
ax3.set_title("Finding 3: CoT Secret Unmasking\n($n=30$ Scripted Exception Trials)", fontsize=11, fontweight="700", color=C_TEXT_MAIN, pad=12)
ax3.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor=C_BORDER, fontsize=8.5)

for i in range(len(models_f3)):
    ax3.text(x3[i] - w3/2, cot_leak[i] + 2, f"{cot_leak[i]:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="700", color=C_PRIMARY)
    ax3.text(x3[i] + w3/2, vis_leak[i] + 2, f"{vis_leak[i]:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="700", color=C_SLATE)

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_color(C_BORDER)
ax3.spines["bottom"].set_color(C_BORDER)
ax3.grid(axis="y", linestyle="--", alpha=0.4, color=C_BORDER)

fig.suptitle("GPT-OSS Model Family Multi-Vector Safety Analysis", fontsize=13, fontweight="800", color=C_TEXT_MAIN, y=0.98)

png_path = OUT_DIR / "shadcn_gpt_oss_findings.png"
svg_path = OUT_DIR / "shadcn_gpt_oss_findings.svg"
pdf_path = OUT_DIR / "shadcn_gpt_oss_findings.pdf"

plt.savefig(png_path, bbox_inches="tight")
plt.savefig(svg_path, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")
plt.close()

print("Generated Shadcn-style SVG/PNG figures successfully!")
