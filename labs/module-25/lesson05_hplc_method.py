"""Lesson 25.5 HPLC method thinking for a painkiller tablet (paracetamol, caffeine,
aspirin and its breakdown product salicylic acid).
Part 1: two isocratic scouting runs -> linear-solvent-strength model log k = log kw - S phi for each compound
-> predicted resolution map -> the best isocratic mobile phase.
Part 2: system-suitability test from six replicate injections, on a new and on a worn column.

Fill in the two TODOs, then run (from this folder):
    py lesson05_hplc_method.py
Reference solution: lesson05_hplc_method_solution.py
Data: hplc_scouting.csv and hplc_sst.csv (simulated).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana25 import HERE, read_csv, save

T0 = 1.00          # min, dead time (uracil)
N_COL = 10000      # plates of the 150 x 4.6 mm, 5 um column
MAX_TIME = 15.0    # min, longest acceptable isocratic run
SST = {"min_Rs": 2.0, "max_tailing": 2.0, "max_area_rsd_percent": 2.0, "min_plates": 5000}


def lss_from_two_runs(phi1, k1, phi2, k2):
    """Linear solvent strength: log10 k = log10 kw - S phi. Returns (log10 kw, S) from two isocratic runs."""
    # TODO 1: two points define the straight line log10 k against phi; S is minus its slope.
    S = 0.0
    return np.log10(k1), S


def resolution(k1, k2, N):
    """Purnell equation (Lesson 19.3) for neighbours with k2 > k1: Rs = sqrt(N)/4 (alpha-1)/alpha k2/(1+k2)."""
    alpha = k2 / k1
    # TODO 2: the Purnell equation in one line.
    return 0.0


def worst_pair(ks, names, N):
    order = np.argsort(ks)
    rs = [(resolution(ks[a], ks[b], N), names[a], names[b]) for a, b in zip(order, order[1:])]
    return min(rs)


def main():
    d = read_csv(HERE / "hplc_scouting.csv")
    names = list(dict.fromkeys(d["compound"]))
    model = {}
    print("Linear-solvent-strength fit from the two scouting runs:")
    for n in names:
        sel = d["compound"] == n
        phi, tR = d["phi_MeCN"][sel], d["t_R_min"][sel]
        k = (tR - T0) / T0
        model[n] = lss_from_two_runs(phi[0], k[0], phi[1], k[1])
        print(f"   {n:15s} k = {k[0]:6.2f} at {phi[0]:.2f}, {k[1]:5.2f} at {phi[1]:.2f}  ->  log kw = {model[n][0]:.2f}, S = {model[n][1]:.2f}")

    if all(model[n][1] == 0 for n in names):
        print("Complete TODO 1 (and TODO 2) first.")
        return
    phis = np.round(np.arange(0.10, 0.451, 0.01), 2)
    best = None
    print("phi   worst pair                         Rs    run time (min)")
    rows = []
    for phi in phis:
        ks = np.array([10 ** (lkw - S * phi) for lkw, S in (model[n] for n in names)])
        rs, a, b = worst_pair(ks, names, N_COL)
        t_run = T0 * (1 + ks.max())
        rows.append((phi, rs, t_run))
        if abs(phi * 100 % 5) < 1e-6:
            print(f"{phi:.2f}  {a + ' / ' + b:34s} {rs:5.2f}  {t_run:6.1f}")
        if t_run <= MAX_TIME and (best is None or rs > best[1]):
            best = (phi, rs, t_run, a, b)
    print(f"Best isocratic choice within {MAX_TIME:.0f} min: {100 * best[0]:.0f} % MeCN, worst pair {best[3]} / {best[4]}, "
          f"Rs = {best[1]:.2f}, run {best[2]:.1f} min")
    cross = [phi for phi, rs, _ in rows if rs < 0.5]
    if cross:
        print(f"   paracetamol and caffeine swap order near {100 * np.mean(cross):.0f} % MeCN (Rs falls to zero there)")

    s = read_csv(HERE / "hplc_sst.csv")
    for state in dict.fromkeys(s["column_state"]):
        sel = s["column_state"] == state
        print(f"System suitability, {state}:")
        tr_mean, n_mean, fails = {}, {}, []
        for n in names:
            m = sel & (s["compound"] == n)
            area, tR = s["area"][m], s["t_R_min"][m]
            rsd = 100 * area.std(ddof=1) / area.mean()
            tail, N = s["tailing"][m].mean(), s["plates"][m].mean()
            tr_mean[n], n_mean[n] = tR.mean(), N
            print(f"   {n:15s} tR {tR.mean():6.3f} min (RSD {100 * tR.std(ddof=1) / tR.mean():.2f} %), area RSD {rsd:.2f} %, "
                  f"tailing {tail:.2f}, N {N:.0f}")
            if rsd > SST["max_area_rsd_percent"]:
                fails.append(f"area RSD of {n}")
            if tail > SST["max_tailing"]:
                fails.append(f"tailing of {n}")
            if N < SST["min_plates"]:
                fails.append(f"plates of {n}")
        order = sorted(names, key=lambda n: tr_mean[n])
        rs_pairs = []
        for a, b in zip(order, order[1:]):
            wa, wb = 4 * tr_mean[a] / np.sqrt(n_mean[a]), 4 * tr_mean[b] / np.sqrt(n_mean[b])
            rs_pairs.append((2 * (tr_mean[b] - tr_mean[a]) / (wa + wb), a, b))
        rs, a, b = min(rs_pairs)
        if rs < SST["min_Rs"]:
            fails.append(f"Rs {a}/{b}")
        print(f"   critical pair {a} / {b}: Rs = {rs:.2f}")
        print("   PASS" if not fails else "   FAIL: " + ", ".join(fails))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot([100 * r[0] for r in rows], [r[1] for r in rows], "-o", ms=3)
    ax.axhline(1.5, color="grey", ls=":")
    ax.axvline(100 * best[0], color="C1", ls="--")
    ax.set(xlabel="acetonitrile (%)", ylabel="Rs of the worst pair", title="Resolution map (isocratic, pH 2.5)")
    save(fig, "lesson05_hplc_method.png")


if __name__ == "__main__":
    main()
