"""Lesson 14.1 reference solution: the force constant of a spring, measured two ways.

Static:  hang known masses, read the spring length; slope of length vs mass is g/k.
Dynamic: time the bounce with phyphox Spring; T^2 = (4 pi^2 / k) (m + m_eff), so the slope gives k
         and the intercept gives the effective mass of the spring itself (about a third of its mass).

Run:   py lesson01_spring_solution.py                              (example data)
       py lesson01_spring_solution.py my_static.csv my_dynamic.csv  (your own data)
Headers: static mass_kg,length_m   dynamic mass_kg,trial,period_s
The plot is saved to runs/lesson01_spring.png next to this file.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
G = 9.795           # m/s^2, local g in Israel (lesson 04.2); use your own value if you measured it
SPRING_MASS = 0.030  # kg, weigh your spring on the kitchen scale and put the value here
K_HCL = 516.0        # N/m, the H-Cl bond (lesson 04.2)


def line_fit(x, y):
    """Straight line y = a x + b. Return a, b and their standard uncertainties."""
    (a, b), cov = np.polyfit(x, y, 1, cov=True)
    return a, b, np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1])


def k_static(mass, length):
    """Force constant from the static stretch: length = L0 + (g/k) m. Return k, u_k, L0."""
    a, b, ua, _ = line_fit(mass, length)
    k = G / a
    return k, k * ua / a, b


def k_dynamic(mass, period):
    """Force constant and effective spring mass from T^2 = (4 pi^2/k) m + (4 pi^2/k) m_eff.
    Return k, u_k, m_eff, u_m_eff (the m_eff uncertainty ignores the slope-intercept correlation)."""
    a, b, ua, ub = line_fit(mass, period ** 2)
    k = 4 * np.pi ** 2 / a
    m_eff = b / a
    u_m = abs(m_eff) * np.sqrt((ua / a) ** 2 + (ub / b) ** 2)
    return k, k * ua / a, m_eff, u_m


def main():
    static = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE / "spring_static_example.csv"
    dynamic = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "spring_dynamic_example.csv"
    ms, Ls = np.loadtxt(static, delimiter=",", skiprows=1, unpack=True)
    md, _, Td = np.loadtxt(dynamic, delimiter=",", skiprows=1, unpack=True)

    ks, uks, L0 = k_static(ms, Ls)
    kd, ukd, m_eff, u_meff = k_dynamic(md, Td)
    print(f"Static:  k = {ks:.2f} +/- {uks:.2f} N/m   (unloaded length {L0 * 100:.1f} cm)")
    print(f"Dynamic: k = {kd:.2f} +/- {ukd:.2f} N/m")
    diff = ks - kd
    print(f"Difference {diff:+.2f} N/m = {diff / np.hypot(uks, ukd):+.1f} combined standard uncertainties")
    print(f"Effective spring mass {m_eff * 1000:.1f} +/- {u_meff * 1000:.1f} g; "
          f"one third of the spring mass = {SPRING_MASS / 3 * 1000:.1f} g")
    f = np.sqrt(kd / 0.300) / (2 * np.pi)
    print(f"With 300 g on it: f = {f:.2f} Hz, period {1 / f:.3f} s")
    print(f"The H-Cl bond (516 N/m) is {K_HCL / kd:.0f} times stiffer than this spring.")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    a1.plot(ms * 1000, Ls * 100, "o")
    a1.plot(ms * 1000, (L0 + G / ks * ms) * 100, "-")
    a1.set_xlabel("added mass (g)")
    a1.set_ylabel("spring length (cm)")
    a1.set_title(f"static: k = {ks:.1f} N/m")
    a2.plot(md * 1000, Td ** 2, "o")
    mm = np.linspace(min(0, -m_eff), md.max(), 50)
    a2.plot(mm * 1000, 4 * np.pi ** 2 / kd * (mm + m_eff), "-")
    a2.set_xlabel("hanging mass (g)")
    a2.set_ylabel("period$^2$ (s$^2$)")
    a2.set_title(f"dynamic: k = {kd:.1f} N/m")
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson01_spring.png", dpi=120)
    print("Plot saved to runs/lesson01_spring.png")


if __name__ == "__main__":
    main()
