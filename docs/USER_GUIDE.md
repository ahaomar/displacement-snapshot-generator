# User Guide — Displacement Snapshot Generator

Plain language, no technical background needed.

## What this does

You type one sentence, like:

> "Build a displacement profile for Sudan, focus on movement into Chad"

and your AI assistant gives you back a professional 2–5 page brief (PDF and
Word) with real, cited numbers about displacement in that country.

## What you need

- An AI tool that can run Python (Claude Code, Codex CLI, ZCode, etc.)
- The `displacement-snapshot-generator` folder copied into that tool's
  skills folder
- Internet connection (the tool fetches public data — no accounts, no API
  keys)

## How to use it

1. **Copy the folder** `displacement-snapshot-generator` into your AI
   tool's skills directory (same place you'd put the climate tool).
2. **Ask for a brief.** Say the country, and optionally a focus country
   for cross-border movement: "Build a displacement profile for Myanmar,
   focus on Bangladesh."
3. **Wait ~2 minutes.** The assistant fetches the data, draws charts, and
   writes the brief.
4. **Get your files.** PDF (for sharing) and Word (for editing) appear in
   the `output/` folder.

## How to read it

- **Stat cards** at the top give the three headline numbers, each labelled
  with its year and source.
- **Figures 1 and 2** show the trend over time.
- **Sources annex** at the end lists where every number came from, with a
  retrieval date.
- If something was unavailable, the brief says so in the annex — the tool
  never guesses a number.

## Good to know

- UNHCR numbers count displaced people *in* a country (who that country
  hosts or tracks), not by where people came from.
- IDMC internal-displacement totals combine conflict and disaster
  displacement — the brief will not invent a split.
- This tool is deliberately not UN-branded and is not an official UN
  product. Always verify critical figures against the cited primary source
  before formal use.
