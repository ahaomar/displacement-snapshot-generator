---
name: displacement-snapshot
description: >
  Generate a cited, UN-style displacement brief (PDF + Word) for any country
  from keyless public data. Use when the user asks for a displacement
  profile, displacement snapshot, refugee/IDP country brief, or displacement
  context for a proposal - e.g. "build a displacement profile for Sudan,
  focus on movement into Chad".
---

# Displacement Snapshot Generator

Produce a finished, professional displacement brief for one country. The
brief is evidence-first: every number comes from the fetched data file and
carries a citation. You never invent a number (principle P5).

## Pipeline (run in order)

1. **Resolve inputs.** From the user's request extract: country (required),
   focus host country for cross-border movement (optional, e.g. "Chad"),
   any format preference (default: PDF + Word). If the country name is
   ambiguous, pick the most common interpretation and state it.

2. **Fetch data.** Run:
   `python3 scripts/fetch_displacement.py "<Country>" ["<Focus country>"]`
   This writes `output/<ISO3>_data.json` and prints the datasets fetched and
   any gaps. NEVER skip this step and NEVER hand-write data values.

3. **Render charts.** Run:
   `python3 scripts/make_charts.py output/<ISO3>_data.json`
   This writes `output/charts/chart_displacement.png` and
   `output/charts/chart_new_displacement.png` (requires matplotlib).

4. **Write the brief** in JSON following `references/report-template.md`
   exactly (structure, cards, sections, tone). Save as
   `output/Displacement_Snapshot_<Country>_brief.json`. Numbers come ONLY
   from the data JSON:
   - persons of concern by year (refugees hosted, asylum-seekers, IDPs,
     returned) → `datasets.unhcr`
   - internal displacement totals and new displacements →
     `datasets.idmc_totals`
   - population, GDP, GDP per capita, poverty → `datasets.world_bank`
   - focus-country hosting figures → `datasets.focus_unhcr`

5. **Render documents.** Produce PDF and DOCX:
   - `python3 scripts/render_pdf.py --brief output/Displacement_Snapshot_<Country>_brief.json -o output/Displacement_Snapshot_<Country>.pdf`
   - `python3 scripts/render_docx.py --brief output/Displacement_Snapshot_<Country>_brief.json -o output/Displacement_Snapshot_<Country>.docx`
   Both ship fonts in `fonts/` and need only reportlab/python-docx + pillow.
   If a renderer is unavailable, deliver the brief JSON + charts and say so
   plainly. Visual standard: `examples/mockup_displacement_snapshot.pdf`.

6. **Report to the user**: file paths, datasets used, and any gaps
   (see gap language below).

## Gap handling (principle P5)

If `gaps[]` in the data JSON is non-empty, the corresponding section or
number is OMITTED and the brief includes, in its Sources annex:
> "<dataset> was unavailable at generation time (<reason>)."

Never substitute literature values, model guesses, or "approximately"
numbers for a missing dataset. Missing data is a result, not an error to
hide.

## Writing rules

- Tone: neutral, factual, institutional. No adjectives like "devastating" or
  "alarming" - let numbers carry the weight (UN editorial style).
- People-first language: "displaced people", "refugees", "host communities" -
  never "the displaced" as a noun phrase, never dehumanising labels.
- Short paragraphs (2-4 sentences). Every figure footnoted: superscript index
  in text, full source name + URL in the Sources annex.
- State the observation window of every trend (e.g. "2019-2025").
- Data caveats to state once where relevant: UNHCR figures cover persons of
  concern in the country of asylum; IDMC totals are country-year aggregates
  (conflict and disaster combined) and undercount where access is limited.
- Drivers of displacement: describe only what the sources support (IDMC
  aggregates do not split conflict vs disaster - do not estimate a split).
  Qualitative context (conflict events, disasters) may be described without
  figures, clearly attributed to public reporting generally, or omitted.
- Length: 2-5 rendered pages. Do not pad.

## Design standard (locked)

Corporate Navy palette (NOT UN blue - this is not a UN entity):
masthead `#24356B`, headings `#1F3A7A`, charts navy `#24356B` + blue
`#2E86AB`, fills `#EEF1F8`. Font: Roboto Condensed (ships in `fonts/`,
embedded in PDFs). Masthead: "Displacement Snapshot" + country + focus line.
Footer: "Built by Omar Farooq |
github.com/ahaomar/displacement-snapshot-generator" and
"Generated <date, time> | Page X of Y". Reference rendering:
`examples/mockup_displacement_snapshot.pdf`.
