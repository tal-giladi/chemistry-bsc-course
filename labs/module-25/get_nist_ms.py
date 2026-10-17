"""Download the electron-ionisation mass spectra that Lesson 25.4 matches against, from the NIST
Chemistry WebBook, and build the simulated GC-MS run of a lemon-oil sample from them.

    py get_nist_ms.py

Needs an internet connection once (about 1 minute: the script waits a few seconds between requests to
be polite to the NIST server). Files go to data/downloaded/ (ignored by git). The NIST mass spectra are
copyrighted by the U.S. Secretary of Commerce: download them yourself for your own study and do not
redistribute them. Pages: https://webbook.nist.gov/cgi/cbook.cgi?ID=<ID>&Mask=200
"""
import time
import urllib.error
import urllib.request

import numpy as np

from ana25 import HERE, DOWNLOADED, read_csv

# WebBook ID -> (name, retention index on a 5 % phenyl column). The indices are the medians of the
# DB-5 / HP-5 / DB-5MS / HP-5MS temperature-ramp entries on each compound's WebBook Gas
# Chromatography page (Mask=2000), read 2026-10-17.
COMPOUNDS = {
    "C80568": ("alpha-pinene", 937),
    "C127913": ("beta-pinene", 979),
    "C123353": ("beta-myrcene", 991),
    "C99876": ("p-cymene", 1026),
    "C138863": ("limonene", 1031),
    "C99854": ("gamma-terpinene", 1061),
    "C78706": ("linalool", 1099),
    "C98555": ("alpha-terpineol", 1190),
    "C106263": ("neral (Z-citral)", 1241),
    "C141275": ("geranial (E-citral)", 1270),
}
URL = "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={id}&Index=0&Type=Mass"
MS_DIR = DOWNLOADED / "nist_ms"


def download(wid):
    out = MS_DIR / f"{wid}.jdx"
    if out.exists() and out.stat().st_size > 200:
        return out
    req = urllib.request.Request(URL.format(id=wid), headers={"User-Agent": "chemistry-course-lab-script (personal study)"})
    for attempt in range(5):
        try:
            text = urllib.request.urlopen(req, timeout=30).read().decode("latin-1")
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:                       # too many requests: wait and retry
                time.sleep(10 * (attempt + 1))
                continue
            raise
    else:
        raise RuntimeError(f"NIST did not answer for {wid}; try again later")
    if "##PEAK TABLE" not in text:
        raise RuntimeError(f"no mass spectrum returned for {wid}")
    out.write_text(text, encoding="utf-8", newline="\n")
    time.sleep(4)
    return out


def read_jcamp_ms(path):
    """Return {m/z: relative intensity (0-999)} from a JCAMP-DX mass spectrum peak table."""
    text = path.read_text(encoding="utf-8")
    body = text.split("##PEAK TABLE=(XY..XY)")[1].split("##END")[0]
    pairs = [p.split(",") for p in body.split()]
    spec = {int(round(float(m))): float(i) for m, i in pairs}
    top = max(spec.values())
    return {m: 999 * i / top for m, i in spec.items()}


def time_from_ri(ri, ladder):
    """Inverse of the linear (van den Dool-Kratz) retention index: RI -> retention time."""
    n = int(ri // 100)
    return ladder[n] + (ri - 100 * n) / 100 * (ladder[n + 1] - ladder[n])


def noisy(spec, rng, rel=0.12, floor=15, low_mass=35):
    """Simulate a measured spectrum: scan from m/z 35, multiplicative noise on each ion,
    ions below 1.5 % of the base peak lost."""
    out = {m: i * np.exp(rng.normal(0, rel)) for m, i in spec.items() if m >= low_mass}
    top = max(out.values())
    return {m: round(999 * i / top) for m, i in out.items() if 999 * i / top >= floor}


def build_run(lib):
    rng = np.random.default_rng(2504)
    a = read_csv(HERE / "gcms_alkanes.csv")
    ladder = {int(n[1:]): t for n, t in zip(a["alkane"], a["t_min"])}
    plan = [("C80568", 1.8), ("C127913", 11.5), ("C123353", 1.6), ("C138863", 65.0), ("C99854", 9.5),
            ("C78706", 0.4), ("C98555", 0.5), ("C106263", 1.1), ("C141275", 1.8)]
    rows = []
    for k, (wid, area) in enumerate(plan, start=1):
        ri = COMPOUNDS[wid][1] + rng.normal(0, 2.0)
        spec = dict(lib[wid])
        if wid == "C138863":                       # p-cymene co-elutes with limonene (area 0.9 %)
            ri = 0.9 * COMPOUNDS["C138863"][1] + 0.1 * COMPOUNDS["C99876"][1]
            cym = lib["C99876"]
            spec = {m: 0.82 * spec.get(m, 0) + 0.18 * cym.get(m, 0) for m in set(spec) | set(cym)}
            area = 65.0 + 0.9
        meas = noisy(spec, rng)
        if ri > 1150:                              # column bleed ions in the late part of the run
            meas[207] = meas.get(207, 0) + 25
            meas[281] = meas.get(281, 0) + 18
        t = time_from_ri(ri, ladder)
        sp = ";".join(f"{m}:{meas[m]}" for m in sorted(meas))
        rows.append(f"P{k},{t:.3f},{area:.1f},{sp}")
    out = DOWNLOADED / "gcms_run.csv"
    head = ["# simulated GC-MS run of a lemon essential oil diluted in hexane, 5 % phenyl column, 60 C then 3 K/min,",
            "# EI 70 eV, scan m/z 35-350; spectra built from NIST WebBook reference spectra with noise (see get_nist_ms.py)",
            "peak,t_min,area_percent,spectrum"]
    out.write_text("\n".join(head + rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(HERE)} with {len(rows)} peaks")


def main():
    MS_DIR.mkdir(parents=True, exist_ok=True)
    lib = {}
    for wid, (name, ri) in COMPOUNDS.items():
        p = download(wid)
        lib[wid] = read_jcamp_ms(p)
        print(f"   {wid}  {name:22s} RI {ri}  {len(lib[wid])} ions  ->  {p.relative_to(HERE)}")
    build_run(lib)


if __name__ == "__main__":
    main()
