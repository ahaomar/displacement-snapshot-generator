"""MOCKUP CHARTS: Displacement Snapshot layout preview - illustrative data only."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UN_DARK = "#1F3A7A"
NAVY = "#24356B"
STRIPE = "#EEF1F8"
MUTED = "#8b8982"
CONFLICT = "#C0392B"
DISASTER = "#2E86AB"

# ── Chart 1: displaced persons stock, 2019-2024 (illustrative) ──
years = [2019, 2020, 2021, 2022, 2023, 2024]
refugees = [0.78, 0.91, 1.08, 1.24, 1.62, 1.93]   # millions, cross-border
idps = [1.86, 2.31, 2.72, 3.21, 4.14, 4.72]       # millions, internal

fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
ax.bar(years, idps, 0.62, label="IDPs (internal)", color=NAVY)
ax.bar(years, refugees, 0.62, bottom=idps, label="Refugees (cross-border)", color=DISASTER)
for x, (i, r) in zip(years, zip(idps, refugees)):
    ax.text(x, i + r + 0.12, "%.1fM" % (i + r), ha="center", fontsize=8.5,
            color=UN_DARK, fontweight="bold")
ax.set_ylabel("Persons displaced (millions)", fontsize=9, color="#20201d")
ax.set_ylim(0, 7.6)
ax.set_xticks(years)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=9, colors="#20201d")
ax.yaxis.grid(True, color=STRIPE, linewidth=0.8)
ax.set_axisbelow(True)
ax.legend(fontsize=8.5, frameon=False, loc="upper left")
ax.set_title("Total displaced population by year, 2019-2024 (illustrative)",
             fontsize=10, color=UN_DARK, fontweight="bold", loc="left", pad=10)
fig.tight_layout()
fig.savefig("chart_displacement_trend.png", bbox_inches="tight")
plt.close(fig)

# ── Chart 2: new displacements by driver, 2020-2024 (illustrative) ──
years2 = [2020, 2021, 2022, 2023, 2024]
conflict_new = [0.62, 0.71, 0.94, 1.31, 1.12]   # millions
disaster_new = [0.14, 0.19, 0.23, 0.31, 0.42]   # millions

fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
w = 0.36
ax.bar([y - w / 2 for y in years2], conflict_new, w, label="Conflict & violence",
       color=CONFLICT)
ax.bar([y + w / 2 for y in years2], disaster_new, w, label="Disasters (incl. floods & drought)",
       color=DISASTER)
for x, v in zip([y - w / 2 for y in years2], conflict_new):
    ax.text(x, v + 0.03, "%.2f" % v, ha="center", fontsize=8, color=UN_DARK)
for x, v in zip([y + w / 2 for y in years2], disaster_new):
    ax.text(x, v + 0.03, "%.2f" % v, ha="center", fontsize=8, color=UN_DARK)
ax.set_ylabel("New displacements (millions)", fontsize=9, color="#20201d")
ax.set_ylim(0, 1.55)
ax.set_xticks(years2)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=9, colors="#20201d")
ax.yaxis.grid(True, color=STRIPE, linewidth=0.8)
ax.set_axisbelow(True)
ax.legend(fontsize=8.5, frameon=False, loc="upper right")
ax.set_title("New internal displacements by trigger, 2020-2024 (illustrative)",
             fontsize=10, color=UN_DARK, fontweight="bold", loc="left", pad=10)
fig.tight_layout()
fig.savefig("chart_drivers.png", bbox_inches="tight")
plt.close(fig)

print("charts done")
