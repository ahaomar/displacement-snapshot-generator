#!/usr/bin/env python3
"""displacement-snapshot-generator / Phase 2: charts.

Reads output/<iso3>_data.json and renders two charts into output/charts/:
  chart_displacement.png  - stacked bars: IDPs + refugees hosted, per year
  chart_new_displacement.png - new internal displacements per year

Usage:
    python3 scripts/make_charts.py output/SDN_data.json
"""
import json
import sys
from pathlib import Path

NAVY = "#24356B"
BLUE = "#2E86AB"
STRIPE = "#EEF1F8"
TEXT = "#20201d"


def render(data_path, out_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(Path(data_path).read_text())
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []

    unhcr = d["datasets"].get("unhcr", {})
    years = sorted(int(y) for y in unhcr if int(y) >= max(int(y) for y in unhcr) - 5)
    if years:
        idps = [unhcr[str(y)]["idps"] / 1e6 for y in years]
        ref = [(unhcr[str(y)]["refugees_hosted"] + unhcr[str(y)]["asylum_seekers"]) / 1e6
               for y in years]
        fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
        ax.bar([str(y) for y in years], idps, 0.62, label="IDPs (UNHCR)", color=NAVY)
        ax.bar([str(y) for y in years], ref, 0.62, bottom=idps,
               label="Refugees & asylum-seekers hosted (UNHCR)", color=BLUE)
        for i, y in enumerate(years):
            tot = idps[i] + ref[i]
            ax.text(i, tot + max(idps + ref) * 0.03, "%.1fM" % tot, ha="center",
                    fontsize=8.5, color=NAVY, fontweight="bold")
        ax.set_ylabel("Persons of concern (millions)", fontsize=9, color=TEXT)
        ax.set_ylim(0, max(idps[i] + ref[i] for i in range(len(years))) * 1.18)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9, colors=TEXT)
        ax.yaxis.grid(True, color=STRIPE, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.legend(fontsize=8.5, frameon=False, loc="upper left")
        ax.set_title("UNHCR persons of concern by year, %s" % d["country"],
                     fontsize=10, color=NAVY, fontweight="bold", loc="left", pad=10)
        fig.tight_layout()
        p = out_dir / "chart_displacement.png"
        fig.savefig(p, bbox_inches="tight")
        plt.close(fig)
        made.append(p)

    idmc = d["datasets"].get("idmc_totals", {})
    yrs = sorted(int(y) for y in idmc
                 if idmc[y].get("new_displacement") is not None
                 and int(y) >= 2015)
    # trim low early years (noise) - keep from first year >= 5% of the peak,
    # always showing at least the most recent 5 years
    vals_all = [idmc[str(y)]["new_displacement"] or 0 for y in yrs]
    threshold = 0.05 * max(vals_all, default=0)
    first = next((i for i, v in enumerate(vals_all) if v >= threshold),
                 max(0, len(yrs) - 5))
    first = min(first, max(0, len(yrs) - 5))
    yrs = yrs[first:]
    if yrs:
        vals = [idmc[str(y)]["new_displacement"] / 1e6 for y in yrs]
        fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
        ax.bar([str(y) for y in yrs], vals, 0.55, color=NAVY)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.02, "%.1fM" % v, ha="center",
                    fontsize=8.5, color=NAVY, fontweight="bold")
        ax.set_ylabel("New displacements (millions)", fontsize=9, color=TEXT)
        ax.set_ylim(0, max(vals) * 1.18)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9, colors=TEXT)
        ax.yaxis.grid(True, color=STRIPE, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_title("New internal displacements per year (IDMC), %s" % d["country"],
                     fontsize=10, color=NAVY, fontweight="bold", loc="left", pad=10)
        fig.tight_layout()
        p = out_dir / "chart_new_displacement.png"
        fig.savefig(p, bbox_inches="tight")
        plt.close(fig)
        made.append(p)

    print("charts written:", ", ".join(str(p) for p in made) or "none")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    data_path = Path(sys.argv[1])
    render(data_path, data_path.parent / "charts")
