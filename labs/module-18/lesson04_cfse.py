"""Lesson 18.4: crystal-field stabilisation energy and the spin-state decision.

Fill in cfse() and predict_spin() (marked TODO), then run (from this folder):
    py lesson04_cfse.py            # table for complexes.csv, saves runs/lesson04_cfse.png
    py lesson04_cfse.py 1.0        # same, with the free-ion pairing energy (scale factor 1.0)
Data: complexes.csv (sources in its header). Reference solution: lesson04_cfse_solution.py
"""
import sys

from inorg18 import CM_KJ, HERE, d_count, load_csv

P_SCALE = 0.8      # pairing energy in a complex ~ 80 % of the free-ion value (nephelauxetic effect; rule of thumb)


def fill(d, geometry, spin):
    """Occupation of the lower and upper sets: returns (n_low, n_high, unpaired).
    oct: lower = t2g (3 orbitals), upper = eg (2). tet: lower = e (2), upper = t2 (3).
    spin 'HS' follows Hund's rule across both sets; 'LS' fills the lower set completely first."""
    n_low_orb, n_high_orb = (3, 2) if geometry == "oct" else (2, 3)
    orbitals = [0] * n_low_orb + [0] * n_high_orb            # electrons per orbital, lower set first
    if spin == "HS":
        order = list(range(5)) + list(range(5))              # one in each orbital, then pair up
    else:
        order = list(range(n_low_orb)) * 2 + list(range(n_low_orb, 5)) * 2
    for k in range(d):
        orbitals[order[k]] += 1
    n_low = sum(orbitals[:n_low_orb])
    unpaired = sum(1 for x in orbitals if x == 1)
    return n_low, d - n_low, unpaired


def cfse(d, geometry, spin):
    """CFSE in units of the splitting (negative = stabilised).
    oct: t2g -0.4, eg +0.6 per electron. tet: e -0.6, t2 +0.4 per electron (in units of Delta_t)."""
    # TODO: n_low, n_high, _ = fill(d, geometry, spin); weight each electron by its set's energy and
    #       return the sum, rounded to 6 decimals (round(x, 6) + 0.0 avoids printing -0.0).
    #       Checks: cfse(6, "oct", "LS") = -2.4, cfse(6, "oct", "HS") = -0.4, cfse(7, "tet", "HS") = -1.2.
    return None


def predict_spin(d, geometry, delta, p):
    """'HS', 'LS' or '-' (only one arrangement). For octahedral d4-d7, low spin wins when moving an
    electron down into t2g (gain delta) pays for the extra pair it makes (cost P): delta > P.
    Tetrahedral complexes are always high spin (Delta_t is small). 4d/5d ions (no P given) are low spin."""
    # TODO: tetrahedral d3-d6 -> "HS"; any other case with only one arrangement -> "-";
    #       octahedral d4-d7 -> "LS" if p is None (4d/5d metal) or delta > p, else "HS".
    return None


def main():
    scale = float(sys.argv[1]) if len(sys.argv) > 1 else P_SCALE
    rows = load_csv("complexes.csv")
    if cfse(6, "oct", "LS") is None or predict_spin(6, "oct", 20000, 18000) is None:
        print("TODO: write cfse() and predict_spin() first.")
        return
    print(f"Pairing energy in the complex = {scale:.2f} x free-ion value\n")
    print(f"{'complex':<14} {'d':>2} {'geom':<4} {'Delta/cm-1':>10} {'P/cm-1':>7} {'pred':>4} {'obs':>4} "
          f"{'unp':>3} {'CFSE/Delta':>10} {'CFSE/kJ mol-1':>13}")
    right = wrong = 0
    for r in rows:
        d = d_count(r["metal"], int(r["ox"]))
        geom = r["geometry"]
        delta = float(r["delta_cm1"])
        p = float(r["P_free_cm1"]) * scale if r["P_free_cm1"] else None
        spin = predict_spin(d, geom, delta, p)
        use = spin if spin in ("HS", "LS") else "HS"
        c = cfse(d, geom, use)
        unp = fill(d, geom, use)[2]
        obs = r["observed_spin"]
        if obs in ("HS", "LS") and spin in ("HS", "LS"):
            right += spin == obs
            wrong += spin != obs
        mark = "" if obs == "-" or spin == obs else "  <-- wrong"
        p_txt = f"{p:7.0f}" if p else "      -"
        print(f"{r['complex']:<14} {d:>2} {geom:<4} {delta:10.0f} {p_txt} {spin:>4} {obs:>4} {unp:>3} "
              f"{c:10.1f} {c * delta * CM_KJ:13.0f}{mark}")
    print(f"\nSpin states predicted correctly: {right} of {right + wrong}")

    print("\nCFSE (units of Delta_o) for octahedral d0-d10:")
    print("  d   :", " ".join(f"{d:>5}" for d in range(11)))
    print("  HS  :", " ".join(f"{cfse(d, 'oct', 'HS'):5.1f}" for d in range(11)))
    print("  LS  :", " ".join(f"{cfse(d, 'oct', 'LS'):5.1f}" for d in range(11)))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ds = list(range(11))
    ax.plot(ds, [-cfse(d, "oct", "HS") for d in ds], "o-", label="octahedral, high spin (weak field)")
    ax.plot(ds, [-cfse(d, "oct", "LS") for d in ds], "s--", label="octahedral, low spin (strong field)")
    ax.set_xlabel("number of d electrons")
    ax.set_ylabel("stabilisation, -CFSE / Delta_o")
    ax.set_title("Crystal-field stabilisation energy (pairing not included)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "lesson04_cfse.png", dpi=120)
    print(f"\nPlot saved to {out / 'lesson04_cfse.png'}")


if __name__ == "__main__":
    main()
