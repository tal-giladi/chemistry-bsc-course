"""Lesson 25.6 a scan-rate study of a quasi-reversible couple.
Peak potentials and currents at six scan rates -> diffusion control (log ip vs log v), D from Randles-Sevcik,
and the standard rate constant k0 from the peak separation (Nicholson's method, Lavagnini's equation).

Fill in the two TODOs, then run (from this folder):
    py lesson06_cv.py
Reference solution: lesson06_cv_solution.py
Data: cv_quasi.csv (simulated).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana25 import HERE, read_csv, line_fit, save

F, R, T = 96485.33212, 8.314462618, 298.15      # CODATA 2022 (NIST); 25 C
N_E = 1
AREA = 0.0707          # cm2, 3 mm disc
C_BULK = 1.0e-6        # mol/cm3 (1.0 mM)
D_KNOWN = 7.0e-6       # cm2/s, measured independently (chronoamperometry, Cottrell equation)
DEP_MAX = 150          # mV: above this the Lavagnini equation drifts from Nicholson's working curve


def psi_from_dEp(dEp_mV, n=N_E):
    """Nicholson's kinetic parameter psi from the peak separation, with the empirical equation of
    Lavagnini et al. (2004), for alpha near 0.5; the authors give it up to about 200 mV, but it agrees
    with Nicholson's tabulated working curve within about 5 % only up to about 150 mV."""
    X = n * dEp_mV
    # TODO 1: psi = (-0.6288 + 0.0021 X) / (1 - 0.017 X), one line.
    return 0.0


def k0_from_psi(psi, v, D, n=N_E):
    """psi = k0 / sqrt(pi D n F v / (R T))  ->  k0 in cm/s (v in V/s, D in cm2/s)."""
    # TODO 2: solve the definition of psi for k0, one line (F, R and T are defined at the top).
    return 0.0


def vertex(E, i, j, w=6):
    """Peak potential and current from a parabola fitted to the points around index j (smooths noise
    and gets below the 2 mV spacing of the data)."""
    sl = slice(max(j - w, 0), j + w + 1)
    a, b, c = np.polyfit(E[sl], i[sl], 2)
    Ep = -b / (2 * a)
    return Ep, np.polyval([a, b, c], Ep)


def peaks(E, i):
    """Cathodic and anodic peaks of one cycle that starts with a negative-going (reduction) sweep.
    Peak currents are measured from the charging-current baseline at the start of the forward sweep."""
    half = np.argmin(E)
    fwd_E, fwd_i = E[:half], i[:half]
    rev_E, rev_i = E[half:], i[half:]
    Epc, ic = vertex(fwd_E, fwd_i, np.argmin(fwd_i))
    Epa, ia = vertex(rev_E, rev_i, np.argmax(rev_i))
    base = fwd_i[:5].mean()
    ipc = ic - base
    # Nicholson's empirical ratio: the anodic peak sits on the decaying cathodic current, so
    # ipa/ipc = (ipa)0/ipc + 0.485 (isp)0/ipc + 0.086, with (ipa)0 and (isp)0 read from zero current
    # and isp the current at the switching potential.
    isp0 = rev_i[0]
    ratio = ia / abs(ipc) + 0.485 * abs(isp0) / abs(ipc) + 0.086
    return Epc, ipc, Epa, ratio


def main():
    d = read_csv(HERE / "cv_quasi.csv")
    vs = np.unique(d["scan_rate_V_per_s"])
    tab = []
    for v in vs:
        sel = d["scan_rate_V_per_s"] == v
        Epc, ipc, Epa, ipa = peaks(d["E_V"][sel], d["i_uA"][sel])
        tab.append((v, Epc, ipc, Epa, ipa))
    tab = np.array(tab)
    v, Epc, ipc, Epa, ipa = tab.T
    dEp = 1000 * (Epa - Epc)

    m_log, b_log, _, _ = line_fit(np.log10(v), np.log10(-ipc))
    print(f"log |ipc| against log v: slope {m_log:.3f} (0.5 = diffusion control, 1.0 = adsorbed species)")
    slow = v <= 0.05
    D_rs = ((-ipc[slow] * 1e-6) / (2.69e5 * N_E ** 1.5 * AREA * C_BULK * np.sqrt(v[slow]))) ** 2
    print(f"Apparent D from Randles-Sevcik at the two slowest scans: {D_rs.mean():.2e} cm2/s "
          f"(low: the reversible equation overestimates the peak of a slow couple)")
    D = D_KNOWN
    print(f"Using D = {D:.1e} cm2/s from an independent chronoamperometry measurement")

    print(" v (V/s)   Epc (V)   Epa (V)   dEp (mV)   E1/2 (V)   ipa/ipc   psi     k0 (cm/s)")
    k0s = []
    for vi, a, c_, e, f_, de in zip(v, Epc, ipc, Epa, ipa, dEp):
        psi = psi_from_dEp(de)
        k0 = k0_from_psi(psi, vi, D)
        if 63 < de <= DEP_MAX:
            k0s.append(k0)
        print(f"{vi:7.2f}  {a:8.3f}  {e:8.3f}  {de:8.1f}   {(a + e) / 2:8.3f}   {f_:6.2f}   {psi:5.3f}   {k0:.4f}")
    print(f"k0 = {np.mean(k0s):.4f} +/- {np.std(k0s, ddof=1):.4f} cm/s (mean and s over scans with 63 < dEp <= {DEP_MAX} mV)")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for vi in vs:
        sel = d["scan_rate_V_per_s"] == vi
        ax[0].plot(d["E_V"][sel], d["i_uA"][sel] / np.sqrt(vi), lw=1, label=f"{vi} V/s")
    ax[0].set(xlabel="E (V vs Ag/AgCl)", ylabel="i / sqrt(v)  (uA s^0.5 V^-0.5)", title="Scan-rate normalised CVs")
    ax[0].legend(fontsize=7)
    ax[1].plot(np.sqrt(v), -ipc, "o", label="cathodic peak")
    ax[1].set(xlabel="sqrt(v)  (V/s)^0.5", ylabel="|ip| (uA)", title="Peak current against sqrt(scan rate)")
    ax[1].legend()
    save(fig, "lesson06_cv.png")


if __name__ == "__main__":
    main()
