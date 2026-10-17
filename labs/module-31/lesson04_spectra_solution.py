"""Lesson 31.4 reference solution: calculated IR and NMR spectra versus experiment.

Part A  formaldehyde IR: GFN2-xTB harmonic frequencies and intensities (xtb --ohess), matched to the
        experimental gas-phase fundamentals in exp_fundamentals.csv; best scale factor and RMS error;
        broadened spectrum plot. Adds your ORCA run (orca/04_formaldehyde_ir.out) if it exists.
Part B  acetone NMR: chemical shifts from your ORCA GIAO shieldings (orca/04_acetone_nmr.out and
        orca/04_tms_nmr.out), delta = sigma(TMS) - sigma, compared with measured shifts in CDCl3.

Run from this folder:  py lesson04_spectra_solution.py     (a few seconds with xtb)
Writes runs/31.4-*/ and runs/lesson04_ir.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comp31 as c

# Measured acetone shifts in CDCl3 (Fulmer et al., Organometallics 29, 2176, 2010)
ACETONE_EXP = {"C=O carbon": 207.07, "CH3 carbon": 30.92, "CH3 hydrogen": 2.17}


def table(pairs, s):
    """Print calculated, scaled and experimental wavenumbers side by side."""
    print(f"  {'calc':>8s} {'scaled':>8s} {'exp':>6s} {'error':>6s}")
    for w, e in pairs:
        print(f"  {w:8.1f} {s * w:8.1f} {e:6.0f} {s * w - e:+6.0f}")


def scale_factor(pairs):
    """Least-squares scale factor s that minimises the sum of (s * calc - exp)^2 over (calc, exp) pairs."""
    num = sum(w * e for w, e in pairs)
    den = sum(w * w for w, _ in pairs)
    return num / den


def shift(sigma_ref, sigma):
    """Chemical shift in ppm from isotropic shieldings: delta = sigma_ref - sigma."""
    return sigma_ref - sigma


def mean_shielding(shieldings, element, indices=None):
    """Average isotropic shielding of one element, optionally only over the given atom indices."""
    vals = [v for (i, el), v in shieldings.items() if el == element and (indices is None or i in indices)]
    return sum(vals) / len(vals)


def main():
    print("Part A - formaldehyde IR, GFN2-xTB")
    out = c.run_xtb(c.MOLECULES / "formaldehyde.xyz", ["--ohess"], c.RUNS / "31.4-formaldehyde", "ohess.out")
    modes = c.vibrations(c.read_vibspectrum(out.parent / "vibspectrum"))
    exp = c.experimental_fundamentals("H2CO")
    pairs = c.match_sorted([w for w, _, _ in modes], exp)
    s = scale_factor(pairs)
    table(pairs, s)
    print(f"  scale factor {s:.4f}; RMS error {c.rms(pairs):.0f} cm-1 unscaled, {c.rms(pairs, s):.0f} cm-1 scaled")

    grid = np.linspace(500, 3500, 3001)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(grid, c.lorentzian(grid, [s * w for w, _, _ in modes], [i for _, i, _ in modes], 15.0),
            label=f"GFN2-xTB x {s:.3f}")
    orca_out = c.HERE / "orca" / "04_formaldehyde_ir.out"
    if orca_out.exists():
        ir = [(w, i) for w, i in c.orca_ir(orca_out) if w > 20]
        po = c.match_sorted([w for w, _ in ir], exp)
        so = scale_factor(po)
        print(f"  ORCA r2SCAN-3c: scale {so:.4f}; RMS {c.rms(po):.0f} cm-1 unscaled, {c.rms(po, so):.0f} scaled")
        ax.plot(grid, c.lorentzian(grid, [so * w for w, _ in ir], [i for _, i in ir], 15.0),
                label=f"r2SCAN-3c x {so:.3f}")
    else:
        print("  (no orca/04_formaldehyde_ir.out yet - run it to add the r2SCAN-3c spectrum)")
    rows = [r for r in c.read_csv(c.HERE / "exp_fundamentals.csv") if r["molecule"] == "H2CO"]
    ax.vlines([float(r["wavenumber_cm1"]) for r in rows], 0, [float(r["ir_intensity_km_mol"]) for r in rows],
              colors="k", label="experiment (CCCBDB)")
    ax.set_xlabel("wavenumber (cm-1)")
    ax.set_ylabel("intensity (km/mol, peak height)")
    ax.invert_xaxis()
    ax.legend()
    fig.tight_layout()
    fig.savefig(c.RUNS / "lesson04_ir.png", dpi=120)
    print("  plot: runs/lesson04_ir.png")

    print("\nPart B - acetone NMR from ORCA shieldings")
    a_out, t_out = c.HERE / "orca" / "04_acetone_nmr.out", c.HERE / "orca" / "04_tms_nmr.out"
    if not (a_out.exists() and t_out.exists()):
        print("  ORCA outputs not found: run orca/04_acetone_opt.inp, 04_acetone_nmr.inp, 04_tms_opt.inp "
              "and 04_tms_nmr.inp first (README.md).")
        return
    sa, st = c.orca_nmr_shieldings(a_out), c.orca_nmr_shieldings(t_out)
    ref_c, ref_h = mean_shielding(st, "C"), mean_shielding(st, "H")
    calc = {"C=O carbon": shift(ref_c, mean_shielding(sa, "C", [1])),
            "CH3 carbon": shift(ref_c, mean_shielding(sa, "C", [0, 2])),
            "CH3 hydrogen": shift(ref_h, mean_shielding(sa, "H"))}
    print(f"  sigma(TMS): C {ref_c:.2f} ppm, H {ref_h:.2f} ppm")
    for k, v in calc.items():
        print(f"  {k:13s} calc {v:7.2f} ppm   exp {ACETONE_EXP[k]:7.2f} ppm   error {v - ACETONE_EXP[k]:+6.2f}")


if __name__ == "__main__":
    main()
