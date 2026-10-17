"""Lesson 31.3 reference solution: Hartree-Fock and DFT geometry optimisation.

Part A  water: compare your optimised geometries (GFN2-xTB from xtb, and any ORCA runs you made
        with orca/03_water_*.inp) with experiment and with the reference table reference_water.csv.
Part B  acetone: the MMFF94 start geometry optimises to a stationary point that is NOT a minimum
        (one small imaginary frequency, a methyl rotation). Detect it and fix it.

Run from this folder:  py lesson03_geometry_solution.py     (about 10 s with xtb)"""
from pathlib import Path
import comp31 as c

R_EXP, A_EXP = 0.958, 104.48     # CCCBDB experimental equilibrium geometry of water


def water_geometry(x):
    """Mean O-H distance (Angstrom) and H-O-H angle (degrees); atom 0 is O."""
    r = (c.distance(x, 0, 1) + c.distance(x, 0, 2)) / 2.0
    return r, c.angle(x, 1, 0, 2)


def n_imaginary(modes, cutoff=-10.0):
    """Number of imaginary (negative) wavenumbers below `cutoff` cm-1."""
    return sum(1 for w, *_ in modes if w < cutoff)


def main():
    print("Part A - water geometry (errors relative to experiment r = 0.958 A, angle = 104.48 deg)")
    rows = []
    out = c.run_xtb(c.MOLECULES / "water.xyz", ["--opt", "tight"], c.RUNS / "31.3-water-xtb", "opt.out")
    _, x, _ = c.read_xyz(out.parent / "xtbopt.xyz")
    rows.append(("GFN2-xTB (your run)",) + water_geometry(x))
    for f in sorted((c.HERE / "orca").glob("03_water_*.xyz")):      # final geometries ORCA writes
        _, x, _ = c.read_xyz(f)
        rows.append((f"ORCA {f.stem} (your run)",) + water_geometry(x))
    for r in c.read_csv(c.HERE / "reference_water.csv"):
        if not r["level"].startswith("experiment"):
            rows.append((r["level"] + " (reference)", float(r["r_OH_A"]), float(r["angle_HOH_deg"])))
    print(f"  {'level':34s} {'r(OH)':>7s} {'dr':>7s} {'angle':>7s} {'da':>6s}")
    for name, r, a in rows:
        print(f"  {name:34s} {r:7.4f} {r - R_EXP:+7.4f} {a:7.2f} {a - A_EXP:+6.2f}")

    print("\nPart B - acetone: is the optimised structure a minimum?")
    w1 = c.RUNS / "31.3-acetone" / "first"
    o1 = c.run_xtb(c.MOLECULES / "acetone.xyz", ["--ohess"], w1, "ohess.out")
    m1 = c.vibrations(c.read_vibspectrum(w1 / "vibspectrum"))
    print(f"  first try : E = {c.xtb_total_energy(o1):.6f} Eh, lowest mode {m1[0][0]:7.1f} cm-1, "
          f"imaginary modes: {n_imaginary(m1)}")
    if n_imaginary(m1):
        # xtb wrote xtbhess.xyz: the structure pushed along the imaginary mode. Restart from it, tighter.
        w2 = c.RUNS / "31.3-acetone" / "restart"
        o2 = c.run_xtb(w1 / "xtbhess.xyz", ["--ohess", "vtight"], w2, "ohess.out")
        m2 = c.vibrations(c.read_vibspectrum(w2 / "vibspectrum"))
        e1, e2 = c.xtb_total_energy(o1), c.xtb_total_energy(o2)
        print(f"  restart   : E = {e2:.6f} Eh, lowest mode {m2[0][0]:7.1f} cm-1, "
              f"imaginary modes: {n_imaginary(m2)}")
        print(f"  energy gained by the restart: {(e1 - e2) * c.HARTREE_KJMOL:.2f} kJ/mol")


if __name__ == "__main__":
    main()
