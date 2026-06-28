import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the catalog
merged = pd.read_csv("short_period_exoplanets_G.csv", low_memory=False)

# Focus on 0.5–6 R⊕
data = merged["radius"].dropna()
data = data[(data >= 0.5) & (data <= 6.0)]

# Log-spaced bins since x-axis is logarithmic
bins_size = np.logspace(np.log10(0.5), np.log10(6.0), 60)

fig, ax = plt.subplots(figsize=(14, 6))

ax.hist(data, bins=bins_size, color="steelblue", edgecolor="white", linewidth=0.4)

# ── Shaded planet type regions ───────────────────────────────────────────────
ax.axvspan(0.5,  1.25, alpha=0.15, color="green",  label="Earth-size")
ax.axvspan(1.25, 2.0,  alpha=0.15, color="orange", label="Super-Earth")
ax.axvspan(2.0,  4.0,  alpha=0.15, color="red",    label="Sub-Neptune")
ax.axvspan(4.0,  6.0,  alpha=0.15, color="purple", label="Neptune-like")

# ── Planet type boundary lines ───────────────────────────────────────────────
ax.axvline(x=1.25, color="green",  linestyle="--", linewidth=1.5)
ax.axvline(x=4.0,  color="red",    linestyle="--", linewidth=1.5)

# ── Fulton Gap highlighted on top ────────────────────────────────────────────
ax.axvspan(1.5, 2.0, alpha=0.45, color="gray", label="Radius Valley (Fulton Gap)")
ax.axvline(x=1.5, color="black", linestyle="-", linewidth=2)
ax.axvline(x=2.0, color="black", linestyle="-", linewidth=2)

# ── Log x-axis ───────────────────────────────────────────────────────────────
ax.set_xscale("log")

# ── Custom x-axis ticks at meaningful radius values ──────────────────────────
tick_vals = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]
ax.set_xticks(tick_vals)
ax.set_xticklabels([str(t) for t in tick_vals])

# ── Planet type labels ────────────────────────────────────────────────────────
y_label = ax.get_ylim()[1] * 0.85
ax.text(0.58,  y_label, "Earth",        fontsize=9, color="green",  rotation=90, va="top")
ax.text(1.30,  y_label, "Super-Earth",  fontsize=9, color="orange", rotation=90, va="top")
ax.text(2.10,  y_label, "Sub-Neptune",  fontsize=9, color="red",    rotation=90, va="top")
ax.text(4.10,  y_label, "Neptune-like", fontsize=9, color="purple", rotation=90, va="top")

# ── Fulton Gap arrow annotation ───────────────────────────────────────────────
ax.annotate(
    "Fulton Gap\n(1.5–2.0 R⊕)",
    xy=(1.75, 2.5),
    xytext=(2.3, ax.get_ylim()[1] * 0.6),
    fontsize=10, color="black", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="black", lw=1.5)
)

ax.set_title("Distribution of Planet Sizes by Type — Log x-axis\n"
             "(G-type stars, Orbital Period < 100 days)", fontsize=13)
ax.set_xlabel("Planet Radius (Earth radii) — log scale", fontsize=12)
ax.set_ylabel("Number of Planets", fontsize=12)
ax.set_xlim(0.5, 6.0)
ax.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig("fulton_gap_logx.png", dpi=150, bbox_inches="tight")
plt.show()