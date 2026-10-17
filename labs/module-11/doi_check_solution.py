"""Lesson 11.2 — check a list of DOIs against Crossref (reference solution).

For each DOI: does it exist, what is it (title, journal, year, publisher), is it open (licence),
and has it been retracted or corrected (Crossref 'updated-by', which includes Retraction Watch data).

Usage (from this folder):
    py doi_check_solution.py                 # DOIs from dois.txt, live Crossref API, cache as fallback
    py doi_check_solution.py my_dois.txt     # your own list, one DOI per line
    py doi_check_solution.py --offline       # use doi_cache.json only (no network)
    py doi_check_solution.py --refresh       # live API, then rewrite doi_cache.json

Optional: set the environment variable CROSSREF_MAILTO to your e-mail address. Crossref then serves
you from its "polite pool" (https://www.crossref.org/documentation/retrieve-metadata/rest-api/).
Standard library only (urllib, json). Checked against the Crossref REST API on 2026-10-17.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "doi_cache.json"
API = "https://api.crossref.org/works/"
OPEN_LICENCES = ("creativecommons.org",)


def fetch(doi):
    """Return a small record for one DOI from the live Crossref API, or {'found': False}."""
    url = API + urllib.parse.quote(doi, safe="/:().;")
    mailto = os.environ.get("CROSSREF_MAILTO")
    if mailto:
        url += "?mailto=" + urllib.parse.quote(mailto)
    req = urllib.request.Request(url, headers={"User-Agent": "chemistry-bsc-course-lab/1.0 (doi_check.py)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            m = json.load(r)["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"doi": doi, "found": False}
        raise
    issued = (m.get("issued", {}).get("date-parts") or [[None]])[0]
    return {
        "doi": doi,
        "found": True,
        "title": (m.get("title") or [""])[0],
        "journal": (m.get("container-title") or [""])[0],
        "year": issued[0],
        "publisher": m.get("publisher", ""),
        "type": m.get("type", ""),
        "licences": sorted({lic.get("URL", "") for lic in m.get("license", [])}),
        "cited_by": m.get("is-referenced-by-count"),
        "updates": [
            {"type": u.get("type"), "notice": u.get("DOI"), "date": "-".join(f"{x:02d}" for x in u["updated"]["date-parts"][0]),
             "source": u.get("source")}
            for u in m.get("updated-by", [])
        ],
    }


def is_open(rec):
    """True if any licence is a Creative Commons licence."""
    return any(any(o in lic for o in OPEN_LICENCES) for lic in rec.get("licences", []))


def verdict(rec):
    """One word per DOI: NOT-FOUND, RETRACTED, CORRECTED or OK."""
    if not rec.get("found"):
        return "NOT-FOUND"
    kinds = {u["type"] for u in rec.get("updates", [])}
    if "retraction" in kinds or "withdrawal" in kinds:
        return "RETRACTED"
    if kinds & {"correction", "erratum", "expression_of_concern", "addendum"}:
        return "CORRECTED"
    return "OK"


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def main(argv):
    offline = "--offline" in argv
    refresh = "--refresh" in argv
    files = [a for a in argv if not a.startswith("--")]
    doi_file = Path(files[0]) if files else HERE / "dois.txt"
    dois = [line.split("#")[0].strip() for line in doi_file.read_text(encoding="utf-8").splitlines()]
    dois = [d for d in dois if d]
    cache = load_cache()
    records = []
    for doi in dois:
        rec = None
        if not offline:
            try:
                rec = fetch(doi)
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                print(f"  (network problem for {doi}: {e}; using the cache)")
        if rec is None:
            rec = cache.get(doi.lower())
            if rec is None:
                print(f"  {doi}: not in cache and no network, skipped")
                continue
        records.append(rec)
    for rec in records:
        v = verdict(rec)
        print(f"\n{rec['doi']}  ->  {v}")
        if not rec.get("found"):
            print("  Crossref has no record of this DOI. Check for a typo; if there is none, the reference may be invented.")
            continue
        print(f"  {rec['title'][:90]}")
        print(f"  {rec['journal']} ({rec['year']}), {rec['publisher']}; type {rec['type']}")
        print(f"  open licence: {'yes' if is_open(rec) else 'no / not stated'}   cited by: {rec['cited_by']}")
        for u in rec["updates"]:
            print(f"  update: {u['type']} on {u['date']} (notice {u['notice']}, source {u['source']})")
    if refresh and not offline:
        new = {r["doi"].lower(): r for r in records}
        CACHE.write_text(json.dumps(new, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(f"\nCache rewritten: {CACHE.name} ({len(new)} records)")
    counts = {}
    for rec in records:
        counts[verdict(rec)] = counts.get(verdict(rec), 0) + 1
    print("\nSummary:", ", ".join(f"{k} {n}" for k, n in sorted(counts.items())))


if __name__ == "__main__":
    main(sys.argv[1:])
