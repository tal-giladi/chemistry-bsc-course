"""Lesson 31.5 exercise: transition states and reaction barriers with GFN2-xTB.

Two textbook barriers, each found as a minimum plus a symmetric transition-state structure:
  ammonia inversion (pyramidal minimum, planar D3h transition state; experiment 24.2 kJ/mol)
  ethane rotation   (staggered minimum, eclipsed D3h transition state; experiment 12 kJ/mol)
For each: check the number of imaginary frequencies, the electronic barrier, the zero-point
correction and the Eyring rate constant at 298 K. Adds your ORCA ammonia runs if present.

Run from this folder:  py lesson05_barriers.py     (about 10 s with xtb)"""
import comp31 as c

CM1_KJMOL = 0.01196266     # 1 cm-1 in kJ/mol (h c N_A, CODATA 2022)
EXPERIMENT = {"ammonia inversion": 24.2, "ethane rotation": 12.0}


def n_imaginary(wavenumbers, cutoff=-10.0):
    # TODO: write this function (see the lesson's Hands-on and the docstring).
    raise NotImplementedError("n_imaginary")


def zpe_kj(wavenumbers):
    """Harmonic zero-point energy in kJ/mol: half the sum of the REAL vibrational wavenumbers."""
    # TODO: write this function (see the lesson's Hands-on and the docstring).
    raise NotImplementedError("zpe_kj")


def barrier_kj(e_ts, e_min):
    """Electronic barrier in kJ/mol from two total energies in hartree."""
    # TODO: write this function (see the lesson's Hands-on and the docstring).
    raise NotImplementedError("barrier_kj")


def xtb_min_and_ts(name, min_xyz, ts_xyz):
    base = c.RUNS / "31.5-barriers" / name.replace(" ", "-")
    o_min = c.run_xtb(min_xyz, ["--ohess"], base / "min", "ohess.out")
    # The symmetric start structure has no force along the reaction mode, so a plain optimisation
    # stays on the saddle point; --hess then tells us what kind of stationary point it is.
    c.run_xtb(ts_xyz, ["--opt"], base / "ts", "opt.out")
    o_ts = c.run_xtb(base / "ts" / "xtbopt.xyz", ["--hess"], base / "ts", "hess.out")
    w_min = [w for w, _, _ in c.vibrations(c.read_vibspectrum(base / "min" / "vibspectrum"))]
    w_ts = [w for w, _, _ in c.vibrations(c.read_vibspectrum(base / "ts" / "vibspectrum"))]
    return c.xtb_total_energy(o_min), w_min, c.xtb_total_energy(o_ts), w_ts


def report(name, e_min, w_min, e_ts, w_ts, level):
    dE = barrier_kj(e_ts, e_min)
    dZ = zpe_kj(w_ts) - zpe_kj(w_min)
    imag = [w for w in w_ts if w < -10]
    print(f"{name} ({level})")
    print(f"  imaginary modes: minimum {n_imaginary(w_min)}, transition state {n_imaginary(w_ts)}"
          f" ({', '.join(f'{-w:.0f}i' for w in imag)} cm-1)")
    print(f"  electronic barrier {dE:6.1f} kJ/mol   (experiment {EXPERIMENT[name]} kJ/mol)")
    print(f"  ZPE change {dZ:+5.1f} kJ/mol -> barrier with ZPE {dE + dZ:6.1f} kJ/mol")
    print(f"  Eyring k(298 K) with the ZPE barrier: {c.eyring(dE + dZ):.2e} s-1")


def main():
    report("ammonia inversion", *xtb_min_and_ts("ammonia inversion", c.MOLECULES / "ammonia.xyz",
                                                 c.MOLECULES / "ammonia_planar.xyz"), "GFN2-xTB")
    report("ethane rotation", *xtb_min_and_ts("ethane rotation", c.MOLECULES / "ethane.xyz",
                                               c.MOLECULES / "ethane_eclipsed.xyz"), "GFN2-xTB")
    o_min, o_ts = c.HERE / "orca" / "05_nh3_min.out", c.HERE / "orca" / "05_nh3_ts.out"
    if o_min.exists() and o_ts.exists():
        report("ammonia inversion", c.orca_final_energy(o_min), c.orca_frequencies(o_min)[6:],
               c.orca_final_energy(o_ts), c.orca_frequencies(o_ts)[6:], "ORCA r2SCAN-3c, your run")
    else:
        print("(no orca/05_nh3_min.out and 05_nh3_ts.out yet - run them to add r2SCAN-3c)")


if __name__ == "__main__":
    main()
