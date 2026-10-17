"""Lesson 25.3 calcium in mineral water by flame AAS.
Linear range from residuals, the lanthanum releasing agent, spike recovery, check-standard drift and a
detection limit.

Fill in the two TODOs, then run (from this folder):
    py lesson03_aas.py
Reference solution: lesson03_aas_solution.py
Data: aas_calcium.csv (simulated).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana25 import HERE, read_csv, line_fit, conc_from_line, save

DILUTION = 10          # 1 + 9
SPIKE = 2.0            # mg/L Ca added to the diluted water


def recovery(c_spiked, c_unspiked, added):
    """Spike recovery in per cent."""
    # TODO 1: the fraction of the added calcium that the method finds, in per cent (one line).
    return 0.0


def suppression(c_without, c_with):
    """How much lower (per cent) the result is without the releasing agent."""
    # TODO 2: one line; 0 % would mean the matrix has no effect.
    return 0.0


def main():
    d = read_csv(HERE / "aas_calcium.csv")
    t, c, A = d["type"], d["c_mg_per_L"], d["absorbance"]
    std = t == "standard_La"
    m_all, b_all, s_all, res_all = line_fit(c[std], A[std])
    print("All standards 0-10 mg/L, residuals:", np.round(res_all, 4).tolist())
    rng = std & (c <= 6)
    m, b, s_r, res = line_fit(c[rng], A[rng])
    print(f"Linear range 0-6 mg/L: A = {b:.4f} + {m:.5f} c, s_r = {s_r:.4f}; residuals {np.round(res, 4).tolist()}")
    print(f"   detection limit 3.3 s_r / m = {3.3 * s_r / m:.2f} mg/L in the measured solution")

    res_c = {}
    for key in ["water_1to10_noLa", "water_1to10_La", "water_1to10_La_spike2"]:
        cc, sc = conc_from_line(A[t == key], c[rng], A[rng], m, b, s_r)
        res_c[key] = (cc, sc)
        print(f"   {key:22s}: {cc:.3f} +/- {sc:.3f} mg/L measured")
    ca, sca = res_c["water_1to10_La"]
    print(f"Mineral water: {DILUTION * ca:.1f} +/- {DILUTION * sca:.1f} mg/L Ca (s), "
          f"95 % about +/- {2 * DILUTION * sca:.1f} mg/L")
    print(f"Without lanthanum the result is {suppression(res_c['water_1to10_noLa'][0], ca):.0f} % low "
          f"({DILUTION * res_c['water_1to10_noLa'][0]:.1f} mg/L)")
    print(f"Spike recovery: {recovery(res_c['water_1to10_La_spike2'][0], ca, SPIKE):.0f} %")
    q = np.polyfit(c[std], A[std], 2)                 # quadratic calibration over 0-10 mg/L

    def c_quad(a):
        roots = np.roots([q[0], q[1], q[2] - np.mean(a)])
        return float(np.real(roots[(np.isreal(roots)) & (np.real(roots) > -1) & (np.real(roots) < 12)][0]))
    cq0, cq1 = c_quad(A[t == "water_1to10_La"]), c_quad(A[t == "water_1to10_La_spike2"])
    print(f"   the spiked solution ({res_c['water_1to10_La_spike2'][0]:.1f} mg/L) is above the 0-6 mg/L linear range;"
          f" with a quadratic calibration the recovery is {recovery(cq1, cq0, SPIKE):.0f} %")
    checks = [A[t == k][0] for k in ["check_start", "check_middle", "check_end"]]
    drift = 100 * (checks[-1] - checks[0]) / checks[0]
    print(f"Check standard 5.0 mg/L: A = {', '.join(f'{x:.4f}' for x in checks)}; drift {drift:+.1f} % over the run")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(c[std], A[std], "o", label="standards")
    cc = np.linspace(0, 10, 50)
    ax[0].plot(cc, b + m * cc, "-", label="line fitted to 0-6 mg/L")
    ax[0].set(xlabel="Ca (mg/L)", ylabel="absorbance at 422.7 nm", title="Flame AAS calibration")
    ax[0].legend()
    ax[1].plot(c[std], res_all * 1000, "o")
    ax[1].axhline(0, color="grey")
    ax[1].set(xlabel="Ca (mg/L)", ylabel="residual x 1000 (straight line, all points)", title="Curvature shows in the residuals")
    save(fig, "lesson03_aas.png")


if __name__ == "__main__":
    main()
