"""Lesson 03.5 module practical: consecutive first-order reactions A -> B -> C.

Solve the same system three ways (formula, eigenvalues of the rate matrix, solve_ivp), check
they agree, then fit k1 and k2 to measured concentrations and find when B peaks.

Usage (from this folder):
    py lesson05_consecutive_solution.py                    # consecutive_example.csv
    py lesson05_consecutive_solution.py my_data.csv        # CSV with t_min,A_mM,B_mM,C_mM

Reference solution. Run:   py lesson05_consecutive_solution.py
The figure is saved to runs/lesson05_consecutive.png next to this file.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent


def analytic(t, A0, k1, k2):
    """Formula solution with only A present at t = 0. Return (A, B, C).
    A = A0 e^(-k1 t); B = A0 k1/(k2 - k1) (e^(-k1 t) - e^(-k2 t)); C = A0 - A - B.
    If k1 == k2 (= k) the B formula is 0/0; its limit is B = A0 k t e^(-k t)."""
    t = np.asarray(t, dtype=float)
    A = A0 * np.exp(-k1 * t)
    if np.isclose(k1, k2):
        B = A0 * k1 * t * np.exp(-k1 * t)
    else:
        B = A0 * k1 / (k2 - k1) * (np.exp(-k1 * t) - np.exp(-k2 * t))
    return A, B, A0 - A - B


def rate_matrix(k1, k2):
    """The matrix K in dc/dt = K c for c = [A, B, C]:
    dA/dt = -k1 A;  dB/dt = k1 A - k2 B;  dC/dt = k2 B."""
    return np.array([[-k1, 0.0, 0.0],
                     [k1, -k2, 0.0],
                     [0.0, k2, 0.0]])


def eigen_solution(K, c0, t):
    """Solve dc/dt = K c with eigenvalues: K = V diag(lam) V^-1, so
    c(t) = V diag(e^(lam t)) V^-1 c0. Return an array of shape (3, len(t)).
    K is not symmetric, so use np.linalg.eig (not eigh)."""
    lam, V = np.linalg.eig(K)
    a = np.linalg.solve(V, c0)                       # c0 written in eigenvector coordinates
    return np.real(V @ (a[:, None] * np.exp(np.outer(lam, t))))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "consecutive_example.csv"
    t, A, B, C = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    A0 = A[0] + B[0] + C[0]
    print(f"{path.name}: {t.size} times up to {t[-1]:.0f} min, total A+B+C at t=0 = {A0:.2f} mM")

    # 1. Three ways to the same answer, with trial constants
    k1, k2 = 0.15, 0.05
    tt = np.linspace(0, t[-1], 301)
    res = analytic(tt, 10.0, k1, k2)
    if res is None:
        print("TODO: write analytic() first.")
        return
    K = rate_matrix(k1, k2)
    if K is None:
        print("TODO: write rate_matrix() next.")
        return
    lam = np.linalg.eigvals(K)
    print(f"1. rate matrix eigenvalues: {np.array2string(np.sort(lam.real), precision=3)} 1/min "
          "(-k1, -k2 and 0 for the end product)")
    c0 = np.array([10.0, 0.0, 0.0])
    ce = eigen_solution(K, c0, tt)
    if ce is None:
        print("TODO: write eigen_solution() last.")
        return
    num = solve_ivp(lambda _t, c: K @ c, (0, t[-1]), c0, t_eval=tt, rtol=1e-9, atol=1e-12)
    c_expm = expm(K * 20.0) @ c0
    print(f"   max |formula - eigen| = {np.max(np.abs(np.array(res) - ce)):.1e} mM, "
          f"max |formula - solve_ivp| = {np.max(np.abs(np.array(res) - num.y)):.1e} mM")
    print(f"   at 20 min: formula B = {res[1][np.argmin(np.abs(tt - 20.0))]:.4f}, "
          f"expm(K t) c0 gives B = {c_expm[1]:.4f} mM")
    print(f"   mass balance A+B+C stays {np.ptp(ce.sum(axis=0)):.1e} mM from constant")

    # 2. Fit k1 and k2 to all three measured curves at once
    def stacked(tm, k1_, k2_):
        return np.concatenate(analytic(tm, A0, k1_, k2_))

    p, cov = curve_fit(stacked, t, np.concatenate([A, B, C]), p0=[0.1, 0.03])
    (k1f, k2f), (u1, u2) = p, np.sqrt(np.diag(cov))
    t_max = np.log(k1f / k2f) / (k1f - k2f)
    B_max = analytic(t_max, A0, k1f, k2f)[1]
    print(f"2. fit: k1 = {k1f:.4f} +- {u1:.4f} 1/min, k2 = {k2f:.4f} +- {u2:.4f} 1/min")
    print(f"   B peaks at t_max = ln(k1/k2)/(k1-k2) = {t_max:.1f} min with B_max = {B_max:.2f} mM")
    print("   model values used to make the example data: k1 = 0.150, k2 = 0.050 1/min")

    # 3. The trap: B alone, with an unknown scale factor, cannot tell k1 from k2
    def b_scaled(tm, s, k1_, k2_):
        return s * analytic(tm, A0, k1_, k2_)[1]

    pa, _ = curve_fit(b_scaled, t, B, p0=[1.0, 0.2, 0.04])
    pb, _ = curve_fit(b_scaled, t, B, p0=[1.0, 0.04, 0.2])
    for name, q in (("start k1 > k2", pa), ("start k1 < k2", pb)):
        rms = np.sqrt(np.mean((B - b_scaled(t, *q)) ** 2))
        print(f"3. B only, {name}: k1 = {q[1]:.3f}, k2 = {q[2]:.3f}, scale {q[0]:.2f}, rms {rms:.3f} mM")
    print("   Same quality of fit with k1 and k2 swapped: B alone cannot say which step is slow.")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    fit_curves = analytic(tt, A0, k1f, k2f)
    for name, data, curve in zip("ABC", (A, B, C), fit_curves):
        ax.plot(t, data, "o", ms=3, label=f"{name} data")
        ax.plot(tt, curve, "-", label=f"{name} fit")
    ax.axvline(t_max, color="grey", lw=0.8)
    ax.set_xlabel("t (min)")
    ax.set_ylabel("concentration (mM)")
    ax.legend(ncol=3, fontsize=8)
    fig.tight_layout()
    out = HERE / "runs" / "lesson05_consecutive.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
