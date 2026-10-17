"""Download the IUPAC Digitized pKa Dataset and extract substituted benzoic acids, phenols and anilinium ions.

Run once (needs internet, about 7 MB):  py fetch_iupac_pka.py
Writes data/downloaded/iupac_high-confidence_v2_4.csv (the full dataset) and
data/downloaded/aromatic_pka.csv (one median pKa per compound), used by lesson03_hammett.py.

The dataset is Copyright 2026 IUPAC and licensed CC BY-NC 4.0: "Reproduced by permission of
International Union of Pure and Applied Chemistry." Citation: J. W. Zheng and O. Lafontant-Joseph,
IUPAC Digitized pKa Dataset, v2.4, https://doi.org/10.5281/zenodo.7236452 (GitHub: IUPAC/Dissociation-Constants).
It is not stored in this repository; data/downloaded/ is ignored by git, so the files stay on your computer.

Selection rules (written down so you can change them): water only (no co-solvent), 25 C, ordinary
pressure, the carboxylic-acid / phenol pKa ("pKa1") or the anilinium pKa ("pKaH1"); values the
compilers marked "Reliable" are used if there are any, otherwise "Approximate" ones; the median is taken.
"""
import csv
import statistics
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "downloaded"
URL = "https://raw.githubusercontent.com/IUPAC/Dissociation-Constants/main/iupac_high-confidence_v2_4.csv"
RAW = OUT / "iupac_high-confidence_v2_4.csv"
TABLE = OUT / "aromatic_pka.csv"

SUBSTITUENTS = {"CH3": "C", "OCH3": "OC", "F": "F", "Cl": "Cl", "Br": "Br", "I": "I", "CF3": "C(F)(F)F",
                "CN": "C#N", "NO2": "[N+](=O)[O-]", "COCH3": "C(C)=O"}
# (series, pK type, SMILES of the parent, meta template, para template)
SERIES = [
    ("benzoic acid", "pKa1", "OC(=O)c1ccccc1", "OC(=O)c1cc({})ccc1", "OC(=O)c1ccc({})cc1"),
    ("phenol", "pKa1", "Oc1ccccc1", "Oc1cc({})ccc1", "Oc1ccc({})cc1"),
    ("anilinium", "pKaH1", "Nc1ccccc1", "Nc1cc({})ccc1", "Nc1ccc({})cc1"),
]


def download():
    OUT.mkdir(parents=True, exist_ok=True)
    if RAW.exists():
        print(f"{RAW.relative_to(HERE)} already exists")
        return
    print(f"Downloading {URL} ...")
    with urllib.request.urlopen(URL, timeout=120) as r:
        RAW.write_bytes(r.read())
    print(f"Saved {RAW.relative_to(HERE)} ({RAW.stat().st_size / 1e6:.1f} MB)")


def targets():
    from rdkit import Chem, RDLogger
    RDLogger.DisableLog("rdApp.*")
    canon = {}
    for series, ptype, parent, meta, para in SERIES:
        canon[Chem.CanonSmiles(parent)] = (series, ptype, "H", "")
        for name, smi in SUBSTITUENTS.items():
            canon[Chem.CanonSmiles(meta.format(smi))] = (series, ptype, name, "m")
            canon[Chem.CanonSmiles(para.format(smi))] = (series, ptype, name, "p")
    return canon


def extract():
    from rdkit import Chem, RDLogger
    RDLogger.DisableLog("rdApp.*")
    canon = targets()
    found = {}
    with open(RAW, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                c = Chem.CanonSmiles(row["SMILES"])
            except Exception:
                continue
            if c not in canon:
                continue
            series, ptype, name, pos = canon[c]
            remarks = row["remarks"] or ""
            if (row["pka_type"] != ptype or row["T"] not in ("25", "25.0") or row["cosolvent"]
                    or row["pressure"] or "P=" in remarks):
                continue
            found.setdefault((series, name, pos), []).append((float(row["pka_value"]), row["assessment"]))
    rows = []
    for (series, name, pos), vals in sorted(found.items()):
        reliable = [v for v, a in vals if a == "Reliable"]
        approx = [v for v, a in vals if a == "Approximate"]
        use, label = (reliable, "Reliable") if reliable else (approx, "Approximate")
        if not use:
            continue
        rows.append({"series": series, "position": pos, "substituent": name, "pKa": f"{statistics.median(use):.3f}",
                     "n_values": len(use), "assessment": label, "spread": f"{max(use) - min(use):.2f}"})
    with open(TABLE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {TABLE.relative_to(HERE)}: {len(rows)} compounds")
    for r in rows:
        print(f"  {r['series']:13s} {r['position'] + '-' if r['position'] else '  '}{r['substituent']:6s} "
              f"pKa {r['pKa']}  ({r['n_values']} {r['assessment']}, spread {r['spread']})")


if __name__ == "__main__":
    try:
        download()
    except OSError as e:
        sys.exit(f"Download failed ({e}). Check your internet connection and try again.")
    extract()
