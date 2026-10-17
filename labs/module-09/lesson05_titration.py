"""Lesson 09.5: titration curves from the charge balance, indicator error and
the end point from noisy pH-meter data.

Fill in the two TODOs, then run (from this folder):
    py lesson05_titration.py                      # example data
    py lesson05_titration.py my_titration.csv     # your data, columns V_NaOH_mL,pH
Reference solution: lesson05_titration_solution.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
KW = 1.0e-14                 # 25 °C
KA_ACETIC = 10 ** -4.757     # Harvey, Analytical Chemistry 2.1, Appendix 11
KA_STRONG = 1.0e8            # a strong acid: fully dissociated for every practical purpose
CA, VA, CB = 0.1000, 25.00, 0.1000      # mol/L, mL, mol/L
INDICATORS = {"methyl orange": 3.8, "bromothymol blue": 7.0, "phenolphthalein": 9.0}  # end-point pH taken


def charge_balance(ph, vb, ka, ca=CA, va=VA, cb=CB):
    """Positive minus negative charge (mol/L) at a trial pH: [Na+] + [H3O+] - [OH-] - [A-].
    Zero at the true pH. [A-] = C_acid * Ka / (Ka + [H3O+])."""
    h = 10.0 ** -ph
    c_acid = ca * va / (va + vb)
    na = cb * vb / (va + vb)
    # TODO 1: return the charge balance [Na+] + [H3O+] - [OH-] - [A-], with [OH-] = KW / h
    # and [A-] = c_acid * ka / (ka + h).
    raise NotImplementedError("TODO 1")


def ph_at(vb, ka):
    return brentq(charge_balance, 0.0, 14.0, args=(vb, ka))


def volume_at_ph(target, ka):
    """Volume of titrant at which the curve reaches a given pH (the indicator's end point)."""
    return brentq(lambda v: ph_at(v, ka) - target, 0.01, 2 * VA * CA / CB - 0.01)


def endpoint_from_data(v, ph):
    """First derivative dpH/dV at interval midpoints; the end point is where it peaks.
    Second derivative: the end point is where it crosses zero (linear interpolation)."""
    vm = (v[1:] + v[:-1]) / 2
    d1 = np.diff(ph) / np.diff(v)
    # TODO 2: the first-derivative end point is the midpoint volume vm where d1 is largest (use np.argmax).
    v_first = None
    vmm = (vm[1:] + vm[:-1]) / 2
    d2 = np.diff(d1) / np.diff(vm)
    # the + to - sign change of the second derivative closest to the first-derivative peak
    cross = [m for m in range(d2.size - 1) if d2[m] > 0 >= d2[m + 1]]
    m = min(cross, key=lambda q: abs(vmm[q] - v_first))
    v_second = vmm[m] + (vmm[m + 1] - vmm[m]) * d2[m] / (d2[m] - d2[m + 1])
    return v_first, v_second, vm, d1


def main():
    RUNS.mkdir(exist_ok=True)
    v_eq = CA * VA / CB
    print(f"25.00 mL of 0.1000 M acid with 0.1000 M NaOH; equivalence at {v_eq:.2f} mL")
    for name, ka in (("HCl (strong)", KA_STRONG), ("acetic acid (pKa 4.757)", KA_ACETIC)):
        pts = {"start": 0.0, "half-equivalence": v_eq / 2, "equivalence": v_eq, "+1.00 mL": v_eq + 1}
        print(f"  {name}: " + ", ".join(f"{k} pH {ph_at(x, ka):.2f}" for k, x in pts.items()))

    print("Indicator error for acetic acid (end point taken at the pH shown):")
    for name, p in INDICATORS.items():
        ve = volume_at_ph(p, KA_ACETIC)
        print(f"  {name:17s} pH {p}: end point {ve:6.2f} mL, error {100 * (ve - v_eq) / v_eq:+.2f} %")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "titration_weak_acid.csv"
    lines = [r for r in path.read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    data = np.array([[float(x) for x in r.split(",")] for r in lines[1:]])
    v, ph = data[:, 0], data[:, 1]
    v1, v2, vm, d1 = endpoint_from_data(v, ph)
    v_half = v1 / 2
    pka_est = np.interp(v_half, v, ph)
    print(f"Data ({path.name}): end point by 1st derivative {v1:.2f} mL, by 2nd derivative {v2:.2f} mL")
    print(f"  pH at half the end-point volume ({v_half:.2f} mL) = {pka_est:.2f}  -> estimate of pKa")

    vv = np.linspace(0, 40, 400)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(vv, [ph_at(x, KA_STRONG) for x in vv], label="HCl")
    ax[0].plot(vv, [ph_at(x, KA_ACETIC) for x in vv], label="acetic acid")
    ax[0].plot(v, ph, ".", label="data")
    for name, p in INDICATORS.items():
        ax[0].axhline(p, ls=":", lw=0.8)
    ax[0].set(xlabel="V NaOH (mL)", ylabel="pH", title="Titration curves")
    ax[0].legend()
    ax[1].plot(vm, d1, "o-")
    ax[1].axvline(v1, color="grey", lw=0.8)
    ax[1].set(xlabel="V NaOH (mL)", ylabel="dpH/dV (per mL)", title="First derivative")
    fig.tight_layout()
    fig.savefig(RUNS / "lesson05_titration.png", dpi=120)
    print("plot written to runs/lesson05_titration.png")


if __name__ == "__main__":
    main()
