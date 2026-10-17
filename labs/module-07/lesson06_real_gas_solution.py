"""Lesson 07.6 reference solution: ideal gas, van der Waals and real CO2 at 320 K.

Run (from this folder):
    py lesson06_real_gas_solution.py        # prints Z = PVm/RT for each model, saves runs/co2_z.png
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = 0.08314462618          # L bar / (mol K), CODATA 2022 (exact)
A_CO2, B_CO2 = 3.658, 0.04286   # van der Waals a (bar L^2/mol^2) and b (L/mol), LibreTexts table A8
T = 320.0                  # K


def load(path=HERE / "co2_320K_nist.csv"):
    """Return arrays (P in bar, Vm in L/mol) from the NIST isotherm file."""
    lines = [r for r in path.read_text(encoding="utf-8").splitlines() if r and not r.startswith("#")]
    data = np.array([[float(v) for v in r.split(",")] for r in lines[1:]])
    return data[:, 0], data[:, 2]


def vdw_molar_volume(P, T, a, b):
    """Molar volume from the van der Waals equation (P + a/Vm^2)(Vm - b) = RT.
    Multiplied out it is a cubic in Vm:  P Vm^3 - (P b + R T) Vm^2 + a Vm - a b = 0.
    Above the critical temperature it has one real root; below it, take the largest (the gas)."""
    roots = np.roots([P, -(P * b + R * T), a, -a * b])
    real = roots[np.abs(roots.imag) < 1e-9].real
    return real.max()


def main():
    P, vm_nist = load()
    z_nist = P * vm_nist / (R * T)
    vm_vdw = np.array([vdw_molar_volume(p, T, A_CO2, B_CO2) for p in P])
    z_vdw = P * vm_vdw / (R * T)
    print(f"{'P/bar':>7} {'Vm ideal':>9} {'Vm vdW':>9} {'Vm NIST':>9} {'Z vdW':>7} {'Z NIST':>7}   (Vm in L/mol)")
    for p, vv, vn, zv, zn in zip(P, vm_vdw, vm_nist, z_vdw, z_nist):
        print(f"{p:>7.0f} {R * T / p:>9.4f} {vv:>9.4f} {vn:>9.4f} {zv:>7.3f} {zn:>7.3f}")
    i = int(np.argmin(z_nist))
    print(f"\nminimum Z (NIST) = {z_nist[i]:.3f} at {P[i]:.0f} bar: the ideal gas law overestimates Vm there by "
          f"{100 * (1 / z_nist[i] - 1):.0f} %")
    err = np.abs(z_vdw - z_nist)
    print(f"largest |Z vdW - Z NIST| = {err.max():.3f} at {P[np.argmax(err)]:.0f} bar")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    pp = np.linspace(1, P.max(), 300)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(1.0, color="grey", ls=":", label="ideal gas")
    ax.plot(pp, [p * vdw_molar_volume(p, T, A_CO2, B_CO2) / (R * T) for p in pp], "-", label="van der Waals")
    ax.plot(P, z_nist, "o", label="NIST (reference data)")
    ax.set_xlabel("pressure / bar")
    ax.set_ylabel("compressibility factor Z = PVm/RT")
    ax.set_title("CO2 at 320 K")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "co2_z.png", dpi=120)
    print(f"\nPlot saved to {out / 'co2_z.png'}")


if __name__ == "__main__":
    main()
