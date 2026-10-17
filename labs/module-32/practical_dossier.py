"""Module 32 practical (exercise: fill in the two TODO functions): a materials dossier from real XRD patterns and corrosion data.

Run from this folder:
    py practical_dossier.py
Files: in2o3_xrd.csv, cdo_xrd.csv, cdo_in2o3_xrd.csv (REAL data, Dahiya, Dahiya and Sabarwal 2026, Zenodo
doi:10.5281/zenodo.18522088, CC BY 4.0) and corrosion_steel.csv (GENERATED, make_data.py).
Part 1: index the In2O3 pattern (body-centred cubic, bixbyite), fit a with a zero shift; reference
        COD 2310009, Ia-3, a = 10.117 A (Marezio 1966).
Part 2: crystallite sizes of CdO and In2O3 by the Scherrer equation (lower limits: the instrument profile is
        not known).
Part 3: assign every peak of the CdO-In2O3 composite to CdO, In2O3, a K-beta satellite, or "unassigned".
Part 4: inhibitor efficiency for steel in 1 M HCl from Tafel extrapolation (lesson 32.2).
Uses fit_cubic() from lesson03 and analyse() from lesson02 (the exercise version imports YOUR files).
Writes runs/practical_composite.png.
"""
import numpy as np

from ec32 import (HERE, CU_KA1, bragg_two_theta, d_from_two_theta, find_xrd_peaks, read_xrd, todo,
                  save_plot, pyplot)
from lesson03_xrd import kbeta_partner, fit_cubic, A_COD, FCC, BCC, SC
import lesson02_corrosion as corr

A_IN2O3_COD = 10.117


def index_with_check(tt, max_m=8, max_rms=0.05):
    """Ratio method with a lattice check and a refinement. For m = 1..max_m and each cubic lattice (fcc, bcc,
    sc), and for starting zero shifts z0 from -0.4 to +0.4 deg: start from a = d(first line) sqrt(m), then three
    times snap every line to the nearest allowed N for the current (a, z) and refit (a, z). A zero shift makes
    high-angle lines snap to the wrong N, which is why several z0 are tried. Accept the first m and lattice
    whose best rms residual is below max_rms degrees. Return (N array, m, lattice name, (a, z, sigma_a, rms))."""
    for m in range(1, max_m + 1):
        for name, allowed in (("fcc", FCC), ("bcc", BCC), ("sc", SC)):
            if m not in allowed:
                continue
            al = np.array(allowed)
            best = None
            for z0 in np.arange(-0.4, 0.401, 0.1):
                a, z = float(d_from_two_theta(tt[0] - z0)) * np.sqrt(m), z0
                for _ in range(3):
                    x = (a / d_from_two_theta(tt - z)) ** 2
                    N = al[np.argmin(np.abs(x[:, None] - al[None, :]), axis=1)]
                    a, z, sa, rms = fit_cubic(tt, N)
                if best is None or rms < best[3][3]:
                    best = (N, m, name, (a, z, sa, rms))
            if best[3][3] < max_rms:
                return best
    return None, None, None, None


def scherrer(two_theta, fwhm_deg, lam=CU_KA1, K=0.9):
    """Crystallite size (nm) from the Scherrer equation tau = K lam / (beta cos theta), beta = FWHM in radians.
    lam in angstrom. Without subtracting the instrument width this is a lower limit of the size.
    TODO: three lines; convert both angles to radians (theta is half of 2 theta) and angstrom to nm."""
    return None  # TODO


def assign_phases(peaks, phases, zero, tol=0.15):
    """Label each observed peak (2 theta, deg) with the phase whose predicted K-alpha1 line (plus the zero shift)
    is nearest within tol degrees, else with "K-beta of <phase> <N>" if it matches a K-beta line, else
    "unassigned". phases = {name: (a, allowed N list)}. Return a list of (peak, label) pairs.
    TODO: build a list of (predicted 2 theta, label) for every phase and N, K-alpha1 and K-beta (use
    bragg_two_theta and kbeta_partner, then add zero), and give each peak the nearest label. About twelve lines."""
    return None  # TODO


def main():
    if todo(fit_cubic(np.array([30.0, 40.0, 50.0]), np.array([3, 4, 8])), corr.corrosion_rate(1e-6),
            scherrer(30.0, 0.3), assign_phases([30.0], {"X": (4.0, [3])}, 0.0)):
        print("This practical also uses your fit_cubic() from lesson 32.3 and corrosion_rate() and "
              "stern_geary() from lesson 32.2: complete those first.")
        return
    # Part 1: In2O3
    tt, y = read_xrd(HERE / "in2o3_xrd.csv")
    pk, h, w = find_xrd_peaks(tt, y)
    strong = h > 0.03 * h.max()
    kb = []
    for parent, hp in zip(pk, h):          # a K-beta line is near the predicted position AND much weaker
        near = (np.abs(pk - kbeta_partner(parent)) < 0.15) & (h < 0.10 * hp) & strong
        kb += list(pk[near])
    main_pk = np.array([p for p in pk[strong] if p not in kb])
    N, m, lat, fit = index_with_check(main_pk)
    if fit is None:
        print("Part 1: no cubic cell found")
        return
    a, z, sa, rms = fit
    print(f"Part 1 In2O3: K-beta lines {', '.join(f'{p:.2f}' for p in kb)}; multiplier {m}, "
          f"N = {[int(n) for n in N]} -> {lat}")
    print(f"   a = {a:.4f} +- {sa:.4f} A, zero shift {z:+.3f} deg, rms {rms:.3f} deg; "
          f"COD 2310009: {A_IN2O3_COD} A ({(a - A_IN2O3_COD) / A_IN2O3_COD * 100:+.2f} %)")
    # Part 2: Scherrer
    sizes = {}
    for name, f in (("CdO", "cdo_xrd.csv"), ("In2O3", "in2o3_xrd.csv")):
        t2, y2 = read_xrd(HERE / f)
        p2, h2, w2 = find_xrd_peaks(t2, y2)
        top = np.argsort(h2)[-3:]
        s = scherrer(p2[top], w2[top])
        sizes[name] = s
        print(f"Part 2 {name}: FWHM {', '.join(f'{x:.3f}' for x in w2[top])} deg at "
              f"{', '.join(f'{x:.1f}' for x in p2[top])} deg -> sizes >= {', '.join(f'{x:.0f}' for x in s)} nm")
    # Part 3: composite
    t3, y3 = read_xrd(HERE / "cdo_in2o3_xrd.csv")
    p3, h3, w3 = find_xrd_peaks(t3, y3)
    keep = h3 > 0.03 * h3.max()
    phases = {"CdO": (A_COD, [3, 4, 8, 11, 12, 16]), "In2O3": (a, sorted(set(int(n) for n in N)))}
    # reference lines = the lines actually seen in the pure samples (32.3 and Part 1), not every allowed N:
    # bixbyite (Ia-3) has extra absences that a plain bcc list would miss. Zero shift: the value that
    # matches the most peaks.
    best_z, best_n = 0.0, -1
    for zz in np.arange(-0.4, 0.401, 0.01):
        lab = assign_phases(p3[keep], phases, zz, tol=0.06)
        n_ok = sum(1 for _, s in lab if s != "unassigned")
        if n_ok > best_n:
            best_z, best_n = zz, n_ok
    labels = assign_phases(p3[keep], phases, best_z)
    print(f"Part 3 composite: zero shift {best_z:+.2f} deg; {len(labels)} peaks")
    for (p, s), hh in zip(labels, h3[keep]):
        print(f"   {p:7.2f} deg  {hh:6.0f}  {s}")
    un = [p for p, s in labels if s == "unassigned"]
    print(f"   unassigned: {len(un)} peaks ({', '.join(f'{p:.2f}' for p in un)})")
    # Part 4: inhibitor
    bare = corr.analyse("bare", 1.0, plot=False)
    inh = corr.analyse("inhibited", 1.0, plot=False)
    eff = 1 - inh["icorr"] / bare["icorr"]
    print(f"Part 4: inhibition efficiency {eff * 100:.1f} % (Tafel), "
          f"{(1 - inh['icorr_sg'] / bare['icorr_sg']) * 100:.1f} % (Stern-Geary); "
          f"rate {corr.corrosion_rate(bare['icorr']):.2f} -> {corr.corrosion_rate(inh['icorr']):.2f} mm/y")
    plt = pyplot()
    if plt:
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(t3, y3, lw=0.8, color="0.2")
        colours = {"CdO": "tab:red", "In2O3": "tab:blue", "K-beta": "tab:orange", "unassigned": "tab:green"}
        for p, s in labels:
            key = "K-beta" if s.startswith("K-beta") else s.split()[0]
            ax.axvline(p, color=colours.get(key, "k"), lw=0.8, ls="--")
        ax.set_xlabel("2θ / degrees (Cu Kα)")
        ax.set_ylabel("counts")
        ax.set_title("CdO-In2O3 composite: red CdO, blue In2O3, orange Kβ, green unassigned")
        save_plot(fig, "practical_composite.png")


if __name__ == "__main__":
    main()
