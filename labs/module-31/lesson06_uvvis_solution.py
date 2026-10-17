"""Lesson 31.6 Parts A-B reference solution: excited states with TD-DFT.

Part A  GFN2-xTB geometries (with a frequency check) of all-trans butadiene, hexatriene and
        octatetraene and of formaldehyde, written to runs/31.6-polyenes/<name>/xtbopt.xyz, the
        files the ORCA inputs orca/06_*_tddft.inp read.
Part B  For each polyene: the brightest excited state from your ORCA TD-DFT output
        (orca/06_<name>_tddft.out) if it exists, otherwise from the reference values in
        polyenes_uv.csv; comparison with the measured lambda_max; Gaussian-broadened spectra.

Run from this folder:  py lesson06_uvvis_solution.py     (about 10 s with xtb)
Writes runs/31.6-polyenes/ and runs/lesson06_uvvis.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comp31 as c

POLYENES = ["butadiene", "hexatriene", "octatetraene"]


def ev_to_nm(e_ev):
    """Photon wavelength in nm for an energy in eV (lambda = h c / E)."""
    return c.HC_EV_NM / e_ev


def brightest(states):
    """The (energy_eV, wavelength_nm, f) tuple with the largest oscillator strength."""
    return max(states, key=lambda s: s[2])


def spectrum_nm(states, grid_nm, fwhm_ev=0.35):
    """Gaussian-broadened absorption on a wavelength grid, broadened in energy (f as peak height)."""
    e_grid = c.HC_EV_NM / grid_nm
    return c.gaussian(e_grid, [s[0] for s in states], [s[2] for s in states], fwhm_ev)


def reference_states(name, level):
    rows = [r for r in c.read_csv(c.HERE / "polyenes_uv.csv") if r["molecule"] == name and r["level"] == level]
    return [(float(r["E_eV"]), ev_to_nm(float(r["E_eV"])), float(r["f"])) for r in rows]


def main():
    print("Part A - GFN2-xTB geometries for the TD-DFT inputs")
    for name in POLYENES + ["formaldehyde"]:
        work = c.RUNS / "31.6-polyenes" / name
        c.run_xtb(c.MOLECULES / f"{name}.xyz", ["--ohess"], work, "ohess.out")
        modes = c.vibrations(c.read_vibspectrum(work / "vibspectrum"))
        n_imag = sum(1 for w, _, _ in modes if w < -10)
        print(f"  {name:13s} lowest mode {modes[0][0]:7.1f} cm-1, imaginary modes {n_imag}  -> {work.name}/xtbopt.xyz")

    print("\nPart B - brightest pi -> pi* state against the measured lambda_max")
    exp = {r["molecule"]: float(r["lambda_exp_nm"]) for r in c.read_csv(c.HERE / "polyenes_uv.csv")
           if r["level"] == "experiment"}
    levels = sorted({r["level"] for r in c.read_csv(c.HERE / "polyenes_uv.csv") if r["level"] != "experiment"})
    grid = np.linspace(150, 400, 501)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for name in POLYENES:
        own = c.HERE / "orca" / f"06_{name}_tddft.out"
        sets = []
        if own.exists():
            sets.append(("your ORCA run", c.orca_tddft(own)))
        sets += [(lv + " (reference)", reference_states(name, lv)) for lv in levels]
        for label, states in sets:
            if not states:
                continue
            e, lam, f = brightest(states)
            e_exp = c.HC_EV_NM / exp[name]
            print(f"  {name:13s} {label:38s} {e:5.2f} eV {lam:6.1f} nm  f = {f:5.3f}   "
                  f"exp {exp[name]:.0f} nm ({e_exp:.2f} eV)  error {e - e_exp:+5.2f} eV")
        label, states = sets[0]
        line, = ax.plot(grid, spectrum_nm(states, grid), label=f"{name} ({label})")
        ax.axvline(exp[name], color=line.get_color(), ls=":", lw=1)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("oscillator strength (broadened)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(c.RUNS / "lesson06_uvvis.png", dpi=120)
    print("  dotted lines: measured lambda_max.  plot: runs/lesson06_uvvis.png")


if __name__ == "__main__":
    main()
