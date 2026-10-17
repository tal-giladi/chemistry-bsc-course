"""Lesson 31.6 Part C exercise - module practical: calculated versus measured IR.

Six small molecules (H2O, NH3, CH4, CO2, H2CO, HCN). For each level of theory:
  1. optimise + harmonic frequencies (xtb --ohess here; ORCA r2SCAN-3c from orca/06_ir_*.inp if you ran it),
  2. check there are no imaginary frequencies,
  3. pair every calculated mode with an experimental fundamental (exp_fundamentals.csv),
  4. fit one least-squares scale factor for the whole set and report the RMS error before and after,
  5. list the worst modes and plot calculated against experimental wavenumbers.

Run from this folder:  py lesson06_practical.py     (about 15 s with xtb)
Writes runs/31.6-practical/ and runs/lesson06_practical.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comp31 as c

SET = {"water": "H2O", "ammonia": "NH3", "methane": "CH4", "co2": "CO2", "formaldehyde": "H2CO", "hcn": "HCN"}


def xtb_wavenumbers(name):
    work = c.RUNS / "31.6-practical" / name
    c.run_xtb(c.MOLECULES / f"{name}.xyz", ["--ohess", "tight"], work, "ohess.out")
    return [w for w, _, _ in c.vibrations(c.read_vibspectrum(work / "vibspectrum"))]


def orca_wavenumbers(name):
    out = c.HERE / "orca" / f"06_ir_{name}.out"
    if not out.exists():
        return None
    return [w for w in c.orca_frequencies(out) if abs(w) > 20]


def collect(get):
    """{formula: [(calc, exp), ...]} for every molecule `get` can supply; None if none."""
    data = {}
    for name, formula in SET.items():
        w = get(name)
        if w is None:
            continue
        if any(x < 0 for x in w):
            print(f"  WARNING {name}: imaginary frequency {min(w):.0f} cm-1 - not a minimum, fix before use")
        data[formula] = c.match_sorted(w, c.experimental_fundamentals(formula))
    return data or None


def summarise(level, data):
    # TODO: write this function (see the lesson's Hands-on and the docstring).
    raise NotImplementedError("summarise")


def main():
    results = [("GFN2-xTB", collect(xtb_wavenumbers))]
    orca = collect(orca_wavenumbers)
    if orca:
        results.append(("ORCA r2SCAN-3c (your runs)", orca))
    else:
        print("(no orca/06_ir_*.out files yet - run the six ORCA inputs to add r2SCAN-3c)")
    fig, ax = plt.subplots(figsize=(5, 5))
    for level, data in results:
        pairs, s = summarise(level, data)
        ax.plot([e for _, e in pairs], [s * w for w, _ in pairs], "o", ms=4, label=f"{level} x {s:.3f}")
    ax.plot([400, 4400], [400, 4400], "k-", lw=0.8)
    ax.set_xlabel("experimental fundamental (cm-1)")
    ax.set_ylabel("scaled calculated (cm-1)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(c.RUNS / "lesson06_practical.png", dpi=120)
    print("\nplot: runs/lesson06_practical.png")


if __name__ == "__main__":
    main()
