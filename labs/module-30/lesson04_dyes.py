"""Lesson 30.4 (exercise: fill in the two TODO functions): conjugated dyes as particles in a box (module practical).

Run from this folder:
    py lesson04_dyes.py
    py lesson04_dyes.py my_dyes.csv      (same columns as cyanine_dyes.csv)
File: cyanine_dyes.csv (published lambda_max values with their sources; NOT generated).
Model (Kuhn 1949): N = p + 3 pi electrons in a box of length L = (p + 3 + alpha) l, where p is the number of
carbons on the conjugated path between the nitrogens, l the bond length and alpha an end extension in bonds.
HOMO -> LUMO: lambda = 8 m_e c L^2 / (h (N + 1)).
Part 1: l = 0.139 nm, alpha = 0. Part 2: alpha calibrated on one dye. Part 3: l and alpha fitted to the
2,2' series. Part 4: blind test on the 4,4' dye. Part 5: the polyene (beta-carotene) and Kuhn's
alternation term. Writes runs/lesson04_dyes.png.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

from pc30 import HERE, H, C, M_E, read_csv, column, todo, save_plot, pyplot

HC_EV_NM = 1239.84198      # h c in eV nm


def lambda_box(p, l_nm, alpha):
    """HOMO-LUMO wavelength (nm) of a cyanine with p chain carbons: N = p + 3 electrons,
    L = (p + 3 + alpha) l. Works on numbers or numpy arrays.
    TODO: three lines (use np.asarray(p, float); M_E, C and H are imported; return nm)."""
    return None  # TODO


def polyene_V0(N, l_nm, lam_obs):
    """Kuhn's correction for a polyene with N pi electrons in a box L = N l: the bond alternation adds a gap
    V0 (1 - 1/N) to the box gap. Return the V0 (eV) that reproduces the observed wavelength.
    TODO: the box gap in eV is HC_EV_NM / lambda_box(N - 3, l_nm, 0) (L = N l); two lines."""
    return None  # TODO


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cyanine_dyes.csv"
    rows = read_csv(path)
    fam = np.array([r["family"] for r in rows])
    p, lam = column(rows, "p"), column(rows, "lambda_nm")
    names = [r["dye"] for r in rows]
    s22, s44, spoly = fam == "22-cyanine", fam == "44-cyanine", fam == "polyene"

    test = lambda_box(3, 0.139, 0.0)
    if todo(test, polyene_V0(22, 0.139, 451.0)):
        return
    print("Part 1: bare box, l = 0.139 nm, alpha = 0")
    for nm, pp, lo in zip(np.array(names)[s22], p[s22], lam[s22]):
        print(f"  {nm:52s} p = {pp:.0f}: model {float(lambda_box(pp, 0.139, 0)):5.0f} nm, measured {lo:.0f} nm")

    a1 = brentq(lambda a: float(lambda_box(p[s22][0], 0.139, a)) - lam[s22][0], 0, 6)
    pred = lambda_box(p[s22], 0.139, a1)
    print(f"Part 2: alpha calibrated on the first dye = {a1:.2f} bonds; predictions "
          f"{', '.join(f'{x:.0f}' for x in pred)} nm vs {', '.join(f'{x:.0f}' for x in lam[s22])}")

    fit = least_squares(lambda x: lambda_box(p[s22], x[0], x[1]) - lam[s22], [0.139, 1.0])
    l_fit, a_fit = fit.x
    dof = max(1, s22.sum() - 2)
    cov = np.linalg.inv(fit.jac.T @ fit.jac) * np.sum(fit.fun**2) / dof
    sl, sa = np.sqrt(np.diag(cov))
    corr = cov[0, 1] / (sl * sa)
    print(f"Part 3: fitted l = {l_fit:.4f} +/- {sl:.4f} nm, alpha = {a_fit:.2f} +/- {sa:.2f} bonds, "
          f"correlation {corr:+.3f}")
    print(f"  residuals (model - measured): {', '.join(f'{x:+.1f}' for x in fit.fun)} nm")

    if s44.any():
        pp, lo = p[s44][0], lam[s44][0]
        pr = float(lambda_box(pp, l_fit, a_fit))
        p_eff = brentq(lambda q: float(lambda_box(q, l_fit, a_fit)) - lo, 1, 20)
        print(f"Part 4: blind test, 4,4'-carbocyanine (p = {pp:.0f} on the path): predicted {pr:.0f} nm, "
              f"measured {lo:.0f} nm ({(pr - lo) / lo * 100:+.0f} %); it behaves as if p = {p_eff:.1f}")

    if spoly.any():
        N, lo = p[spoly][0], lam[spoly][0]
        box = float(lambda_box(N - 3, 0.139, 0.0))
        V0 = polyene_V0(N, 0.139, lo)
        print(f"Part 5: beta-carotene, {N:.0f} pi electrons, box L = N x 0.139 nm: {box:.0f} nm vs {lo:.0f} nm; "
              f"Kuhn's alternation gap V0 = {V0:.2f} eV")

    plt = pyplot()
    if plt is None:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    pp = np.linspace(2, 10, 50)
    ax.plot(pp, lambda_box(pp, 0.139, 0), ":", label="bare box, l = 0.139 nm")
    ax.plot(pp, lambda_box(pp, 0.139, a1), "--", label=f"alpha = {a1:.2f} (one dye)")
    ax.plot(pp, lambda_box(pp, l_fit, a_fit), "-", label=f"fit l = {l_fit:.3f} nm, alpha = {a_fit:.2f}")
    ax.plot(p[s22], lam[s22], "ko", label="2,2' series")
    if s44.any():
        ax.plot(p[s44], lam[s44], "rs", label="4,4'-carbocyanine")
    ax.set_xlabel("p (carbons on the path)")
    ax.set_ylabel(r"$\lambda_{max}$ (nm)")
    ax.legend(fontsize=8)
    save_plot(fig, "lesson04_dyes.png")


if __name__ == "__main__":
    main()
