"""Lesson 07.2: periodic trends in ionisation energy (NIST ASD data).

Fill in the two functions marked TODO, then run (from this folder):
    py lesson02_ionisation.py           # prints the analysis, saves runs/ie1.png
Reference solution: lesson02_ionisation_solution.py
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NOBLE = {2, 10, 18, 36}


def load(path=HERE / "ionization_energies.csv"):
    """Return Z (int array), symbols (list), IE as an (n, 3) float array with NaN for missing."""
    rows = [r.split(",") for r in path.read_text(encoding="utf-8").splitlines()
            if r and not r.startswith("#")][1:]
    Z = np.array([int(r[0]) for r in rows])
    sym = [r[1] for r in rows]
    ie = np.array([[float(x) if x else np.nan for x in r[2:5]] for r in rows])
    return Z, sym, ie


def dips(Z, ie1):
    """Elements whose IE1 is LOWER than that of the element before them."""
    # TODO: compare each IE1 with the one before it; return the list of Z values where it went down.
    return None


def valence_from_jumps(ie_row):
    """Number of electrons removed before the biggest ratio IE(k+1)/IE(k).
    That count is the number of valence electrons (for main-group atoms with all three IEs known)."""
    # TODO: ratios = IE2/IE1 and IE3/IE2 (array slicing); return the index of the largest ratio + 1.
    #       np.nanargmax ignores missing values.
    return None


def main():
    Z, sym, ie = load()
    ie1 = ie[:, 0]
    d = dips(Z, ie1)
    if d is None:
        print("TODO: write dips() first.")
        return
    print("IE1 lower than the element before:", ", ".join(sym[z - 1] for z in d))
    print("Noble gases (local maxima):", ", ".join(f"{sym[z - 1]} {ie1[z - 1]:.2f} eV" for z in sorted(NOBLE)))
    print("\nValence electrons from the biggest jump in IE1, IE2, IE3:")
    for s in ("Na", "Mg", "K", "Ca"):
        i = sym.index(s)
        print(f"  {s:<3} IE = {ie[i, 0]:7.3f} {ie[i, 1]:7.3f} {ie[i, 2]:8.3f} eV  -> {valence_from_jumps(ie[i])}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(Z, ie1, "o-", ms=4)
    for z in list(NOBLE) + [3, 11, 19] + d:
        ax.annotate(sym[z - 1], (z, ie1[z - 1]), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    ax.set_xlabel("atomic number Z")
    ax.set_ylabel("first ionisation energy / eV")
    ax.set_title("IE1 of H to Kr (NIST ASD)")
    fig.tight_layout()
    fig.savefig(out / "ie1.png", dpi=120)
    print(f"\nPlot saved to {out / 'ie1.png'}")


if __name__ == "__main__":
    main()
