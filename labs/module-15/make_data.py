"""Generate the example kinetics data for lesson 15.5 (seeded, so the file is reproducible).

    py make_data.py      # writes sn_runs.csv

The data are a MODEL, not measurements: two substitution reactions, each run with two starting
concentrations of nucleophile.
  substrate A, "1-bromobutane + iodide in acetone": rate = k2 [RBr][I-], k2 = 2.0e-3 L/(mol s)
  substrate B, "2-chloro-2-methylpropane in 80 % aqueous ethanol, with added azide": rate = k1 [RCl],
               k1 = 3.0e-4 1/s, independent of the nucleophile
The rate constants are illustrative, chosen to be of a realistic order of magnitude at 25 degC.
Concentrations carry Gaussian noise with a standard deviation of 0.0004 mol/L.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
S0 = 0.050  # mol/L substrate at t = 0


def simulate(kind, nu0, t_end=6000.0, dt=1.0):
    t = np.arange(0.0, t_end + dt, dt)
    s = np.empty_like(t)
    s[0] = S0
    for i in range(1, len(t)):
        nu = nu0 - (S0 - s[i - 1])
        rate = 2.0e-3 * s[i - 1] * nu if kind == "A" else 3.0e-4 * s[i - 1]
        s[i] = s[i - 1] - rate * dt
    return t, s


def main():
    rng = np.random.default_rng(1505)
    rows = ["# Model data for lesson 15.5, made by make_data.py (seed 1505). Not measurements.",
            "substrate,run,nu0_M,t_s,substrate_M"]
    for kind in ("A", "B"):
        for run, nu0 in ((1, 0.10), (2, 0.20)):
            t, s = simulate(kind, nu0)
            for ts in range(0, 6001, 300):
                c = s[ts] + rng.normal(0.0, 0.0004)
                rows.append(f"{kind},{run},{nu0:.2f},{ts},{c:.5f}")
    (HERE / "sn_runs.csv").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote sn_runs.csv ({len(rows) - 2} rows)")


if __name__ == "__main__":
    main()
