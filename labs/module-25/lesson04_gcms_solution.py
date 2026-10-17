"""Lesson 25.4 (reference solution): identify the peaks of a lemon-oil GC-MS run by library search
against NIST WebBook spectra, then confirm or reject each hit with the retention index.

First run (once, needs internet):  py get_nist_ms.py
Then (from this folder):            py lesson04_gcms_solution.py
Extension: add "C98555" (alpha-terpineol) to LIBRARY and run again.
"""
import sys

import numpy as np

from ana25 import HERE, DOWNLOADED, read_csv
from get_nist_ms import COMPOUNDS, MS_DIR, read_jcamp_ms

LIBRARY = ["C80568", "C127913", "C123353", "C99876", "C138863", "C99854", "C78706", "C106263", "C141275"]
MZ = np.arange(35, 351)          # the scan range of the run
MF_MIN = 800                     # a "good" match on the 0-999 scale
RI_WINDOW = 10                   # accepted |measured RI - library RI| on the same type of column


def to_vector(spec):
    v = np.zeros(MZ.size)
    for m, i in spec.items():
        if MZ[0] <= m <= MZ[-1]:
            v[m - MZ[0]] = i
    return v


def match_factor(meas, ref):
    """Weighted dot-product (cosine) similarity on a 0-999 scale: intensities are square-rooted and
    multiplied by m/z before comparing, so the few heavy, characteristic ions count more than the
    abundant small fragments (the approach Stein and Scott 1994 found to work best)."""
    a = np.sqrt(meas) * MZ
    b = np.sqrt(ref) * MZ
    return 999 * float(a @ b) / float(np.linalg.norm(a) * np.linalg.norm(b))


def retention_index(t_x, ladder):
    """Linear (van den Dool-Kratz) retention index from an n-alkane ladder {carbon number: time}."""
    ns = sorted(ladder)
    for n, n1 in zip(ns, ns[1:]):
        if ladder[n] <= t_x <= ladder[n1]:
            return 100 * (n + (t_x - ladder[n]) / (ladder[n1] - ladder[n]))
    raise ValueError("peak outside the alkane ladder")


def decide(hits, ri):
    """hits: list of (MF, WebBook ID) sorted best first. Keep hits with MF >= MF_MIN whose library RI is
    within RI_WINDOW of the measured RI. Return (verdict, list of accepted names)."""
    ok = [COMPOUNDS[w][0] for mf, w in hits if mf >= MF_MIN and abs(COMPOUNDS[w][1] - ri) <= RI_WINDOW]
    if len(ok) == 1:
        return "identified", ok
    if len(ok) > 1:
        return "ambiguous", ok
    return "not identified", ok


def residual_search(meas, ref, lib_vec):
    """Subtract the best hit (scaled by least squares) and search what is left: a co-eluting compound?"""
    scale = float(meas @ ref) / float(ref @ ref)
    res = np.clip(meas - scale * ref, 0, None)
    share = res.sum() / meas.sum()
    best = max((match_factor(res, v), w) for w, v in lib_vec.items()) if share > 0.08 else None
    return share, best


def main():
    run_file = DOWNLOADED / "gcms_run.csv"
    if not run_file.exists():
        sys.exit("No GC-MS run yet: run  py get_nist_ms.py  first (needs internet once).")
    lib_vec = {w: to_vector(read_jcamp_ms(MS_DIR / f"{w}.jdx")) for w in LIBRARY}
    a = read_csv(HERE / "gcms_alkanes.csv")
    ladder = {int(n[1:]): t for n, t in zip(a["alkane"], a["t_min"])}
    run = read_csv(run_file)
    print(f"Library: {len(LIBRARY)} NIST spectra. Accept: MF >= {MF_MIN} and |delta RI| <= {RI_WINDOW}.")
    print("peak  t/min  area%    RI   best hit (MF)                    2nd hit (MF)                     verdict")
    for p, t, area, sp in zip(run["peak"], run["t_min"], run["area_percent"], run["spectrum"]):
        meas = to_vector({int(m): float(i) for m, i in (x.split(":") for x in sp.split(";"))})
        ri = retention_index(t, ladder)
        hits = sorted(((match_factor(meas, v), w) for w, v in lib_vec.items()), reverse=True)
        verdict, names = decide(hits, ri)
        h1 = f"{COMPOUNDS[hits[0][1]][0]} ({hits[0][0]:.0f}, RI {COMPOUNDS[hits[0][1]][1]})"
        h2 = f"{COMPOUNDS[hits[1][1]][0]} ({hits[1][0]:.0f}, RI {COMPOUNDS[hits[1][1]][1]})"
        print(f"{p:4s} {t:6.2f} {area:5.1f}  {ri:5.0f}   {h1:32s} {h2:32s} {verdict}: {', '.join(names) or '-'}")
        share, best = residual_search(meas, lib_vec[hits[0][1]], lib_vec)
        if best and best[1] != hits[0][1] and best[0] >= MF_MIN:
            print(f"      {100 * share:.0f} % of the ion current is not explained by the best hit; "
                  f"the residual matches {COMPOUNDS[best[1]][0]} (MF {best[0]:.0f}): co-elution?")


if __name__ == "__main__":
    main()
