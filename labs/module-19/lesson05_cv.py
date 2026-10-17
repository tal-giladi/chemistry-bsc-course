"""Lesson 19.5: read peak potentials and currents from cyclic voltammograms, test reversibility,
and get the diffusion coefficient from the Randles-Sevcik equation.

Fill in the two TODOs, then run (from this folder):
    py lesson05_cv.py
Reference solution: lesson05_cv_solution.py
Data: cv_ferricyanide.csv (simulated by finite differences in make_data.py). Sign convention:
IUPAC, oxidation current positive. The scan starts at +0.50 V, goes down to -0.10 V and back.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana19 import HERE, read_csv, save

F, R, T = 96485.33212, 8.314462618, 298.15      # CODATA 2022 (NIST)
N_E, AREA_CM2, C_MOL_PER_CM3 = 1, 0.0707, 2.0e-6  # one electron, 3 mm disc, 2.0 mM
RS_CONST = 2.69e5                                # Randles-Sevcik constant at 25 C (A s V^-1/2 mol^-1)


def peaks(E, i):
    """Cathodic and anodic peaks of one cycle. The anodic peak is measured from the decaying cathodic
    current with Nicholson's empirical rule, not from zero."""
    n = E.size // 2
    jc = np.argmin(i[:n])
    ja = n + np.argmax(i[n:])
    ipc = -i[jc]                                 # magnitude, from the zero-current baseline
    ipa0 = i[ja]                                 # anodic peak measured from zero
    isp = -i[n]                                  # current at the switching potential (magnitude)
    ratio = ipa0 / ipc + 0.485 * isp / ipc + 0.086
    return E[jc], ipc, E[ja], ipa0, ratio


def delta_and_half(Epc, Epa):
    """Peak separation (mV) and half-wave potential (V)."""
    # TODO 1: dEp = Epa - Epc (convert V to mV) and E1/2 = the mean of the two peak potentials.
    return None, None


def D_from_slope(slope_A_per_sqrtV):
    """Diffusion coefficient (cm2/s) from the slope of ip against sqrt(scan rate)."""
    # TODO 2: rearrange ip = 2.69e5 n^(3/2) A C D^(1/2) v^(1/2): the slope is 2.69e5 n^(3/2) A C D^(1/2),
    # so D = (slope / (RS_CONST * N_E**1.5 * AREA_CM2 * C_MOL_PER_CM3))**2.
    return None


def main():
    d = read_csv(HERE / "cv_ferricyanide.csv")
    rates = np.unique(d["scan_rate_V_per_s"])
    print(f"Reversible limit at 25 C: about {1000 * 2.218 * R * T / (N_E * F):.0f} mV (textbooks often round to 59 mV)")
    print(" v (V/s)  Epc (V)  Epa (V)  dEp (mV)  E1/2 (V)  ipc (uA)  ipa0 (uA)  ipa/ipc")
    ipcs = []
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for v in rates:
        s = d["scan_rate_V_per_s"] == v
        E, i = d["E_V"][s], d["i_uA"][s] * 1e-6
        Epc, ipc, Epa, ipa0, ratio = peaks(E, i)
        dEp, E_half = delta_and_half(Epc, Epa)
        ipcs.append(ipc)
        print(f" {v:6.3f}  {Epc:7.3f}  {Epa:7.3f}  {dEp:7.0f}   {E_half:7.3f}  {1e6 * ipc:7.2f}   {1e6 * ipa0:7.2f}    {ratio:5.2f}")
        ax[0].plot(E, 1e6 * i, label=f"{1000 * v:.0f} mV/s")
    ipcs = np.array(ipcs)
    x = np.sqrt(rates)
    slope, icpt = np.polyfit(x, ipcs, 1)
    print(f"ipc = {1e6 * icpt:.2f} uA + {1e6 * slope:.2f} uA (V/s)^-1/2 * sqrt(v)   (a diffusion-controlled peak is a line through 0)")
    print(f"   D from the slope of all five points: {D_from_slope(slope):.2e} cm2/s")
    for v, ip in zip(rates, ipcs):
        print(f"   v = {v:5.3f} V/s: ipc/sqrt(v) = {1e6 * ip / np.sqrt(v):6.1f} uA (V/s)^-1/2  ->  D = {D_from_slope(ip / np.sqrt(v)):.2e} cm2/s")
    ax[0].set(xlabel="E vs Ag/AgCl (V)", ylabel="i (uA), oxidation positive", title="CV, 2.0 mM ferricyanide")
    ax[0].invert_xaxis()
    ax[0].legend(fontsize=8)
    ax[1].plot(x, 1e6 * ipcs, "o")
    xx = np.linspace(0, x.max(), 20)
    ax[1].plot(xx, 1e6 * (icpt + slope * xx), "-")
    ax[1].set(xlabel="sqrt(v) ((V/s)^1/2)", ylabel="ipc (uA)", title="Randles-Sevcik test")
    save(fig, "lesson05_cv.png")


if __name__ == "__main__":
    main()
