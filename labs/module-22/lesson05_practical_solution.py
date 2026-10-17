"""Lesson 22.5 - reference solution. Module practical: fit the 1913 invertase data end to end.

Run:  py lesson05_practical_solution.py      Writes runs/lesson05_practical.png.
Part 1: Michaelis-Menten fit of the seven initial rates (nonlinear and Lineweaver-Burk).
Part 2: global fit of the five time courses by numerical integration, with and without
competitive product inhibition (KS, KF, KG from Michaelis & Menten 1913).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit, least_squares

from kin22 import KF_MM, KG_MM, KS_MM, read_csv, runs_dir


def michaelis_menten(S, V, K):
    """Initial rate v = V S / (K + S)."""
    return V * S / (K + S)


def fit_mm(S, v):
    """Nonlinear least-squares fit of michaelis_menten. Returns (V, K) and their standard errors."""
    popt, pcov = curve_fit(michaelis_menten, S, v, p0=(v.max(), np.median(S)))
    return popt, np.sqrt(np.diag(pcov))


def lineweaver_burk(S, v):
    """Straight line 1/v = 1/V + (K/V)(1/S). Returns V, K."""
    slope, intercept = np.polyfit(1.0 / S, 1.0 / v, 1)
    return 1.0 / intercept, slope / intercept


def rate(S, S0, V, inhibition):
    """-dS/dt for invertase: V (S/KS) / (1 + S/KS + P/KF + P/KG), P = S0 - S (fructose = glucose)."""
    P = (S0 - S) if inhibition else 0.0
    return V * (S / KS_MM) / (1 + S / KS_MM + P / KF_MM + P / KG_MM)


def fraction_converted(V, S0, t, inhibition):
    """Integrate dS/dt = -rate and return 1 - S/S0 at the times t (minutes)."""
    sol = solve_ivp(lambda _t, y: [-rate(y[0], S0, V, inhibition)], (0, t.max()), [S0],
                    t_eval=t, rtol=1e-9, atol=1e-12)
    return 1 - sol.y[0] / S0


def global_fit(courses, inhibition):
    """Fit one V (mM/min) to all time courses. Returns V, its standard error and the RMS residual."""
    def resid(p):
        return np.concatenate([fraction_converted(p[0], S0, t, inhibition) - x for S0, (t, x) in courses.items()])
    fit = least_squares(resid, [0.5])
    dof = fit.fun.size - 1
    s2 = np.sum(fit.fun**2) / dof
    se = np.sqrt(s2 / (fit.jac.T @ fit.jac)[0, 0])
    return fit.x[0], se, np.sqrt(np.mean(fit.fun**2))


def load_courses():
    courses = {}
    for r in read_csv("invertase_timecourse.csv"):
        if r["used_in_MM_constant"] != "1":
            continue
        S0 = float(r["sucrose_mM"])
        t, x = courses.setdefault(S0, ([], []))
        t.append(float(r["t_min"])); x.append(float(r["fraction_converted"]))
    return {S0: (np.array(t), np.array(x)) for S0, (t, x) in courses.items()}


def main():
    rows = read_csv("invertase_initial_rates.csv")
    S = np.array([float(r["sucrose_M"]) for r in rows]) * 1000
    v = np.array([float(r["initial_rate_arb"]) for r in rows])
    (V, K), (sV, sK) = fit_mm(S, v)
    print(f"Part 1 nonlinear fit: V = {V:.2f} +/- {sV:.2f} (arb.), Km = {K:.1f} +/- {sK:.1f} mM  (1913: 16.7 mM)")
    Vlb, Klb = lineweaver_burk(S, v)
    print(f"Part 1 Lineweaver-Burk: V = {Vlb:.2f}, Km = {Klb:.1f} mM")

    courses = load_courses()
    results = {}
    for inhibition in (True, False):
        Vg, sVg, rms = global_fit(courses, inhibition)
        results[inhibition] = Vg
        label = "with product inhibition" if inhibition else "without inhibition    "
        print(f"Part 2 {label}: Vmax = {Vg:.3f} +/- {sVg:.3f} mM/min, RMS residual = {rms:.4f}")
    print(f"  Vmax/Km = {results[True] / KS_MM:.4f} min^-1  (1913 global constant 0.0454 +/- 0.0032 min^-1)")
    print("  Johnson & Goody (2011) global fit: kcat E0 = 0.80 +/- 0.02 mM/min; 1913 value 0.76 +/- 0.05")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ss = np.linspace(0, S.max(), 200)
    ax[0].plot(S, v, "o", label="Michaelis & Menten 1913")
    ax[0].plot(ss, michaelis_menten(ss, V, K), "-", label=f"fit, Km = {K:.1f} mM")
    ax[0].set_xlabel("[sucrose] / mM"); ax[0].set_ylabel("initial rate (arb.)"); ax[0].legend()
    for S0, (t, x) in courses.items():
        tt = np.linspace(0, t.max(), 100)
        line, = ax[1].plot(t, x, "o", label=f"{S0:g} mM")
        ax[1].plot(tt, fraction_converted(results[True], S0, tt, True), "-", c=line.get_color())
        ax[1].plot(tt, fraction_converted(results[False], S0, tt, False), ":", c=line.get_color())
    ax[1].set_xlabel("t / min"); ax[1].set_ylabel("fraction converted"); ax[1].legend(fontsize=8)
    ax[1].set_title("solid: with product inhibition; dotted: without", fontsize=9)
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson05_practical.png", dpi=120)
    print("saved runs/lesson05_practical.png")


if __name__ == "__main__":
    main()
