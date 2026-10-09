# Report Template — Displacement Snapshot Brief

The brief JSON passed to `scripts/render_pdf.py` / `render_docx.py` follows
this structure exactly:

```json
{
  "country": "Sudan",
  "focus": "Cross-border movement into Chad",
  "period_label": "5-year trend",
  "cards": [["4.7M", "people displaced within Sudan (UNHCR, 2025)"],
            ["1.5M", "refugees hosted by Chad (UNHCR, 2025)"],
            ["6.0M", "new internal displacements in 2023 (IDMC)"]],
  "sections": [
    {"heading": "1. Displacement overview",
     "paragraphs": ["..."],
     "figure": {"path": "output/charts/chart_displacement.png",
                "caption": "Figure 1. ..."}},
    {"heading": "2. Recent displacement pressure",
     "paragraphs": ["..."],
     "figure": {"path": "output/charts/chart_new_displacement.png",
                "caption": "Figure 2. ..."}},
    {"heading": "3. Host-country context: Chad",
     "paragraphs": ["..."], "bullets": ["..."]},
    {"heading": "4. Response & frameworks", "paragraphs": ["..."]}
  ],
  "sources": ["1. UNHCR Population of Concern per country ... data.unhcr.org — retrieved <timestamp>", ...]
}
```

Masthead, stat cards, figures, footer and the Sources annex are rendered by
the PDF/DOCX templates - the body only supplies headings, paragraphs,
bullets and figure captions.

---

## Stat cards (3, strongest available numbers)

| Card | Source field |
|------|--------------|
| Latest IDP stock | `datasets.unhcr.<latest-year>.idps` |
| Latest refugees hosted (country or focus country) | `datasets.unhcr.<latest>.refugees_hosted` or `datasets.focus_unhcr.<latest>.refugees_hosted` |
| Peak / latest new displacements (IDMC) | `datasets.idmc_totals.<year>.new_displacement` |
| Fallback: population, GDP per capita, poverty rate | `datasets.world_bank` |

Never leave an empty card and never invent one. Label each card with its
year and source in parentheses.

## Section order (fixed)

1. **Displacement overview** — multi-year UNHCR trend, chart_displacement
   as Figure 1. State the window. Who is displaced (IDPs vs refugees
   hosted), direction of change, notable single-year shifts.
2. **Recent displacement pressure** — IDMC new-displacement series,
   chart_new_displacement as Figure 2. Peak years, latest year vs peak.
3. **Host-country context** — if a focus country was fetched:
   refugees hosted, asylum-seekers, own IDPs; two or three bullets on
   hosting pressure drawn only from these numbers plus neutral framing.
   Without a focus country: the country's hosting role or return dynamics.
4. **Response & frameworks** — one short paragraph: relevant international
   frameworks (Global Compact on Refugees; Global Compact for Migration for
   mixed movements; IASC humanitarian programme cycle) and, where known,
   that a regional refugee response plan exists. No invented planning
   figures; links go in the annex only.

## Sources (annex format)

```
1. UNHCR Population of Concern per country (ArcGIS FeatureServer), <Country>,
   years <min>-<max>. gis.unhcr.org / data.unhcr.org — retrieved <timestamp>
2. IDMC Internal Displacements - country-year totals (HDX).
   data.humdata.org — retrieved <timestamp>
3. World Bank Open Data API, indicators SP.POP.TOTL, NY.GDP.MKTP.CD,
   NY.GDP.PCAP.CD, SI.POV.DDAY. api.worldbank.org — retrieved <timestamp>
```

If any dataset is in `gaps[]`, add: "*<name> was unavailable at generation
time (<reason>).*"

## Writer cautions (not printed)

- UNHCR country rows are persons of concern IN that country (country of
  asylum), not by origin. Do not describe `refugees_hosted` for the affected
  country as "refugees from" it.
- IDMC `total_displacement` and UNHCR `idps` may differ (different mandate
  and cutoff dates). Present one series per chart; note the difference once
  if both appear in text.
- Aggregates do not split conflict vs disaster. Never estimate the split.
- Round to 3 significant figures or whole millions in cards; keep exact
  values in the annex sentences where useful.
