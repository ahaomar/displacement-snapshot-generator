# Displacement Snapshot Generator

Turns a one-sentence request into a finished, fully cited displacement
brief (PDF + Word) in about two minutes. The migration twin of
[climate-profile-generator](https://github.com/ahaomar/climate-profile-generator).

> "Build a displacement profile for Sudan, focus on movement into Chad"
> → a 2–5 page brief with stat cards, displacement trend charts, recent
> displacement pressure, host-country context, and a cited sources annex.

## Who it's for

UN staff, consultants, researchers — anyone who needs a defensible,
neutral displacement snapshot without hunting through portals.

## Install (no API keys, ever)

Copy the folder into your AI tool's skills directory (Claude Code, Codex
CLI, ZCode, or any agent harness that reads SKILL.md). Requirements:
Python 3.10+, `matplotlib`, `reportlab`, `python-docx`, `pillow`.

## Data sources (all keyless, all public)

| Source | What it provides |
|---|---|
| UNHCR Population of Concern per country | Refugees hosted, asylum-seekers, IDPs, returns — by year |
| IDMC (via HDX) | Internal displacement totals & new displacements, 2009–latest |
| World Bank Open Data | Population, GDP, GDP per capita, poverty rate |

**Honest data rule:** every figure is cited with source, URL and retrieval
timestamp. Missing datasets are flagged as unavailable — never guessed.

## Usage

Ask your AI agent, or run manually:

```bash
python3 scripts/fetch_displacement.py "Sudan" "Chad"
python3 scripts/make_charts.py output/SDN_data.json
# then follow SKILL.md to write the brief JSON and render:
python3 scripts/render_pdf.py  --brief output/..._brief.json -o output/brief.pdf
python3 scripts/render_docx.py --brief output/..._brief.json -o output/brief.docx
```

See `docs/USER_GUIDE.md` for the plain-language guide.

## Design

Corporate Navy palette (deliberately not UN-branded), Roboto Condensed
fonts (included), reference layout in `examples/mockup_displacement_snapshot.pdf`.

MIT-licensed code; data licenses belong to their publishers.
