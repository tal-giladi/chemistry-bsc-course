"""Lesson 17.3 reference solution: first-order 1H NMR multiplets and proton equivalence.

Run (from this folder):
    py lesson03_nmr1h_solution.py
"""
from math import comb

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from spec17 import need_rdkit, runs_dir  # noqa: E402

need_rdkit()
from rdkit import Chem  # noqa: E402

# Approximate shifts (ppm, CDCl3) and couplings (Hz), rounded textbook values for teaching.
# Check them against the real SDBS spectra in the lesson.
SPECTRA = {
    "bromoethane": [(3.43, 2, [(3, 7.3)]), (1.67, 3, [(2, 7.3)])],
    "2-chloropropane": [(4.14, 1, [(6, 6.5)]), (1.54, 6, [(1, 6.5)])],
    "1-nitropropane": [(4.37, 2, [(2, 7.0)]), (2.03, 2, [(5, 7.2)]), (1.03, 3, [(2, 7.4)])],
}


def multiplet(n_neighbours, j_hz):
    """First-order n+1 rule: offsets (Hz) and relative heights (Pascal's triangle) for n equivalent neighbours."""
    offsets = [(k - n_neighbours / 2) * j_hz for k in range(n_neighbours + 1)]
    heights = [comb(n_neighbours, k) for k in range(n_neighbours + 1)]
    return offsets, heights


def lines_for_signal(shift_ppm, n_h, couplings, mhz):
    """All lines (ppm, intensity) of one signal; each set of neighbours splits every line again."""
    lines = [(0.0, 1.0)]
    for n, j in couplings:
        offs, hts = multiplet(n, j)
        lines = [(x + o, h * w) for x, h in lines for o, w in zip(offs, hts)]
    total = sum(h for _, h in lines)
    return [(shift_ppm + x / mhz, n_h * h / total) for x, h in lines]


def spectrum(signals, mhz, ppm=None, width_hz=0.8):
    """Sum of Lorentzian lines on a ppm axis."""
    ppm = np.linspace(0, 6, 24000) if ppm is None else ppm
    y = np.zeros_like(ppm)
    hw = width_hz / mhz / 2
    for s, n, cpl in signals:
        for x, h in lines_for_signal(s, n, cpl, mhz):
            y += h * hw**2 / ((ppm - x) ** 2 + hw**2)
    return ppm, y


def h_environments(smiles):
    """Number of topologically different H environments (diastereotopic H are not separated)."""
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    ranks = list(Chem.CanonicalRankAtoms(m, breakTies=False))
    return len({ranks[a.GetIdx()] for a in m.GetAtoms() if a.GetSymbol() == "H"})


def main():
    print("Part 1 - Pascal's triangle")
    for n in range(7):
        print(f"  {n} neighbours -> {n + 1} lines, heights {multiplet(n, 7.0)[1]}")

    print("\nPart 2 - proton environments")
    for name, smi in [("bromoethane", "CCBr"), ("2-chloropropane", "CC(C)Cl"), ("1-nitropropane", "CCC[N+](=O)[O-]"),
                      ("2-butanol", "CCC(C)O"), ("tert-butyl methyl ether", "COC(C)(C)C"),
                      ("1,4-dichlorobenzene", "Clc1ccc(Cl)cc1")]:
        print(f"  {name:24s} {h_environments(smi)} signals expected")

    print("\nPart 3 - simulated spectra at 60 and 400 MHz")
    out = runs_dir()
    fig, axes = plt.subplots(len(SPECTRA), 2, figsize=(11, 8))
    for row, (name, sig) in zip(axes, SPECTRA.items()):
        for ax, mhz in zip(row, (60, 400)):
            x, y = spectrum(sig, mhz)
            ax.plot(x, y, color="black", lw=0.8)
            ax.set_xlim(5, 0.5)
            ax.set_title(f"{name}, {mhz} MHz")
            ax.set_yticks([])
        integrals = ", ".join(f"{s} ppm: {n}H" for s, n, _ in sig)
        print(f"  {name}: {integrals}")
    for ax in axes[-1]:
        ax.set_xlabel("chemical shift / ppm")
    fig.tight_layout()
    fig.savefig(out / "lesson03_spectra.png", dpi=120)
    print(f"  plot written to {out / 'lesson03_spectra.png'}")
    j, mhz = 7.3, 60
    dv = (3.43 - 1.67) * mhz
    print(f"\n  bromoethane at {mhz} MHz: delta-nu / J = {dv:.0f} / {j} = {dv / j:.1f} (first order if well above ~10)")


if __name__ == "__main__":
    main()
