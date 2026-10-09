#!/usr/bin/env python3
"""displacement-snapshot-generator / Phase 1: data layer.

Fetches public, keyless displacement + context data for one country and
writes a single JSON file the report pipeline consumes.

Usage:
    python3 scripts/fetch_displacement.py "Sudan" ["Chad"]

    Second (optional) argument is a focus host country, e.g. the main
    cross-border destination.

Output:
    output/<iso3>_data.json   containing datasets + sources[] + gaps[]

Principles: stdlib only, zero API keys, never fabricate - anything
unavailable is recorded in gaps[].

Sources:
    UNHCR   - Population of Concern per country (ArcGIS FeatureServer,
              same figures as data.unhcr.org, keyless REST queries)
    IDMC    - country-year internal displacement totals incl. new
              displacements (HDX-hosted CSV)
    World Bank Open Data - context indicators (population, GDP, poverty)
"""
import csv
import io
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TIMEOUT = 25
RETRIES = 2
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

UNHCR_LAYER = ("https://gis.unhcr.org/arcgis/rest/services/population/"
               "wrl_polbnd_int_population_p_unhcr_all/FeatureServer/0")
IDMC_CSV = ("https://data.humdata.org/dataset/459fc96c-f196-44c1-a0a5-1b5a7b3592dd"
            "/resource/0fb4e415-abdb-481a-a3c6-8821e79919be/download/"
            "internal-displacements-new-displacements-idps.csv")
WB_BASE = "https://api.worldbank.org/v2"

ISO3_TABLE = {
    "afghanistan": "AFG", "albania": "ALB", "algeria": "DZA", "angola": "AGO",
    "armenia": "ARM", "azerbaijan": "AZE", "bangladesh": "BGD", "belarus": "BLR",
    "benin": "BEN", "bolivia": "BOL", "bosnia and herzegovina": "BIH",
    "botswana": "BWA", "brazil": "BRA", "bulgaria": "BGR", "burkina faso": "BFA",
    "burundi": "BDI", "cambodia": "KHM", "cameroon": "CMR",
    "central african republic": "CAF", "chad": "TCD", "chile": "CHL",
    "china": "CHN", "colombia": "COL", "comoros": "COM",
    "congo, democratic republic": "COD", "congo, republic": "COG",
    "costa rica": "CRI", "cote d'ivoire": "CIV", "ivory coast": "CIV",
    "croatia": "HRV", "cuba": "CUB", "cyprus": "CYP", "czechia": "CZE",
    "djibouti": "DJI", "dominican republic": "DOM", "ecuador": "ECU",
    "egypt": "EGY", "el salvador": "SLV", "eritrea": "ERI", "estonia": "EST",
    "ethiopia": "ETH", "fiji": "FJI", "gabon": "GAB", "gambia": "GMB",
    "georgia": "GEO", "ghana": "GHA", "greece": "GRC", "guatemala": "GTM",
    "guinea": "GIN", "guinea-bissau": "GNB", "haiti": "HTI", "honduras": "HND",
    "india": "IND", "indonesia": "IDN", "iran": "IRN", "iraq": "IRQ",
    "jordan": "JOR", "kenya": "KEN", "kyrgyzstan": "KGZ", "lebanon": "LBN",
    "lesotho": "LSO", "liberia": "LBR", "libya": "LBY", "madagascar": "MDG",
    "malawi": "MWI", "mali": "MLI", "mauritania": "MRT", "mexico": "MEX",
    "moldova": "MDA", "mongolia": "MNG", "morocco": "MAR", "mozambique": "MOZ",
    "myanmar": "MMR", "namibia": "NAM", "nepal": "NPL", "nicaragua": "NIC",
    "niger": "NER", "nigeria": "NGA", "pakistan": "PAK", "palestine": "PSE",
    "papua new guinea": "PNG", "paraguay": "PRY", "peru": "PER",
    "philippines": "PHL", "russia": "RUS", "rwanda": "RWA", "senegal": "SEN",
    "somalia": "SOM", "south africa": "ZAF", "south sudan": "SSD",
    "sri lanka": "LKA", "sudan": "SDN", "syria": "SYR", "tajikistan": "TJK",
    "tanzania": "TZA", "thailand": "THA", "togo": "TGO", "tunisia": "TUN",
    "turkiye": "TUR", "turkey": "TUR", "turkmenistan": "TKM", "uganda": "UGA",
    "ukraine": "UKR", "venezuela": "VEN", "yemen": "YEM", "zambia": "ZMB",
    "zimbabwe": "ZWE",
}

WB_INDICATORS = {
    "SP.POP.TOTL": "Population, total",
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "SI.POV.DDAY": "Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)",
}


def resolve_iso3(name):
    key = name.strip().lower()
    if key in ISO3_TABLE:
        return ISO3_TABLE[key]
    for k, v in ISO3_TABLE.items():
        if k in key or key in k:
            return v
    raise SystemExit("Country '%s' not in bundled lookup table. Add it to ISO3_TABLE." % name)


def fetch(url, as_bytes=False):
    """urllib with retries; curl fallback for TLS-hostile hosts."""
    import subprocess
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "displacement-snapshot-generator/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read()
            return data if as_bytes else data.decode("utf-8", errors="replace")
        except Exception as e:
            last = e
            time.sleep(2 * attempt)
    try:
        out = subprocess.run(["curl", "-sL", "--max-time", str(TIMEOUT), url],
                             capture_output=True, check=True)
        return out.stdout if as_bytes else out.stdout.decode("utf-8", errors="replace")
    except Exception:
        raise last


def fetch_unhcr(iso3):
    """Country-of-asylum series for the country (refugees hosted, asylum
    seekers, IDPs) - the same headline figures data.unhcr.org publishes."""
    fields = ("year,refugees,asylum_seekers,returned_refugees,idps,"
              "returned_idps,stateless,ooc")
    url = ("%s/query?f=json&where=coa_iso%%3D%%27%s%%27&outFields=%s"
           "&returnGeometry=false&orderByFields=year%%20DESC&resultRecordCount=80"
           % (UNHCR_LAYER, iso3, fields))
    data = json.loads(fetch(url))
    rows = [f["attributes"] for f in data.get("features", [])]
    rows = [r for r in rows if r.get("year")]
    if not rows:
        raise RuntimeError("no UNHCR rows for coa_iso=%s" % iso3)
    return {str(r["year"]): {
        "refugees_hosted": r.get("refugees") or 0,
        "asylum_seekers": r.get("asylum_seekers") or 0,
        "returned_refugees": r.get("returned_refugees") or 0,
        "idps": r.get("idps") or 0,
        "returned_idps": r.get("returned_idps") or 0,
        "stateless": r.get("stateless") or 0,
        "others_of_concern": r.get("ooc") or 0,
    } for r in rows}


def fetch_idmc_totals(iso3):
    """Country-year internal displacement totals (conflict + disaster combined)."""
    raw = fetch(IDMC_CSV, as_bytes=True)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace")))
    out = {}
    for row in reader:
        if row.get("iso3") != iso3:
            continue
        yr = row.get("year")
        if not (yr and yr.isdigit()):
            continue
        def num(k):
            v = row.get(k, "")
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        out[yr] = {"new_displacement": num("new_displacement"),
                   "total_displacement": num("total_displacement")}
    if not out:
        raise RuntimeError("no IDMC country-year rows for %s" % iso3)
    return out


def fetch_worldbank(iso3):
    out = {}
    for code, label in WB_INDICATORS.items():
        url = "%s/country/%s/indicator/%s?format=json&per_page=60" % (WB_BASE, iso3, code)
        try:
            payload = json.loads(fetch(url))
            series = payload[1] or []
            vals = [(int(d["date"]), d["value"]) for d in series if d["value"] is not None]
            if vals:
                latest = max(vals, key=lambda x: x[0])
                out[code] = {"label": label, "year": latest[0],
                             "value": round(float(latest[1]), 2)}
        except Exception:
            continue
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    name = sys.argv[1].strip()
    focus = sys.argv[2].strip() if len(sys.argv) > 2 else None
    iso3 = resolve_iso3(name)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    result = {"country": name.title(), "iso3": iso3, "generated": now,
              "focus_country": focus.title() if focus else None,
              "datasets": {}, "sources": [], "gaps": []}

    def source(label, url, status):
        result["sources"].append({"name": label, "url": url,
                                  "fetched": now, "status": status})

    try:
        result["datasets"]["unhcr"] = fetch_unhcr(iso3)
        source("UNHCR Population of Concern per country (ArcGIS FeatureServer)",
               UNHCR_LAYER, "ok")
    except Exception as e:
        result["gaps"].append({"dataset": "unhcr", "reason": str(e)[:200]})

    try:
        result["datasets"]["idmc_totals"] = fetch_idmc_totals(iso3)
        source("IDMC Internal Displacements - country-year totals (HDX)",
               IDMC_CSV, "ok")
    except Exception as e:
        result["gaps"].append({"dataset": "idmc_totals", "reason": str(e)[:200]})


    try:
        result["datasets"]["world_bank"] = fetch_worldbank(iso3)
        status = "ok" if result["datasets"]["world_bank"] else "no data"
        source("World Bank Open Data (context indicators)",
               "%s/country/%s/indicator/SP.POP.TOTL?format=json" % (WB_BASE, iso3), status)
        if not result["datasets"]["world_bank"]:
            result["gaps"].append({"dataset": "world_bank", "reason": "no data returned"})
    except Exception as e:
        result["gaps"].append({"dataset": "world_bank", "reason": str(e)[:200]})

    if focus:
        try:
            f_iso3 = resolve_iso3(focus)
            result["datasets"]["focus_unhcr"] = fetch_unhcr(f_iso3)
            source("UNHCR Population of Concern - focus country %s" % f_iso3,
                   UNHCR_LAYER, "ok")
        except Exception as e:
            result["gaps"].append({"dataset": "focus_unhcr", "reason": str(e)[:200]})

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / ("%s_data.json" % iso3)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("wrote %s" % out_path)
    print("datasets: %s" % ", ".join(result["datasets"]))
    if result["gaps"]:
        print("gaps: %s" % "; ".join(g["dataset"] for g in result["gaps"]))
    else:
        print("gaps: none")


if __name__ == "__main__":
    main()
