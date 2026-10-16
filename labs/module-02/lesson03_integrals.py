"""Lesson 02.3 hands-on: integrals as accumulated change.

Three jobs: (1) work of an isothermal gas expansion, (2) heat to warm N2 from NIST Shomate Cp(T),
(3) amount of reactant used up, from the rate data of lesson 02.2.
Fill in the three TODO functions, then run:   py lesson03_integrals.py
Reference solution: lesson03_integrals_solution.py
"""
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

HERE = Path(__file__).resolve().parent
R = 8.314462618  # J/(mol K), CODATA 2022 (exact)

# NIST Chemistry WebBook, nitrogen (CAS 7727-37-9), gas-phase Shomate coefficients, 100-500 K.
# Cp in J/(mol K) with t = T / 1000. https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=1
N2 = dict(A=28.98641, B=1.853978, C=-9.647459, D=16.63537, E=0.000117, F=-8.671914, H=0.0)


def trapezoid(y, x):
    """Trapezoid rule: sum over intervals of (x[i+1] - x[i]) * (y[i] + y[i+1]) / 2.
    TODO: write it with np.diff and array slicing (no loops needed)."""
    return None


def cp_n2(T):
    """Cp of N2 in J/(mol K): A + B t + C t^2 + D t^3 + E / t^2 with t = T / 1000.
    TODO: return the Shomate polynomial using the N2 dict."""
    return None


def enthalpy_change_exact(T1, T2, c=N2):
    """H(T2) - H(T1) in J/mol from the integrated Shomate form (NIST, kJ/mol):
    H - H298 = A t + B t^2/2 + C t^3/3 + D t^4/4 - E/t + F - H. Given, nothing to do."""
    def h(T):
        t = T / 1000.0
        return (c["A"] * t + c["B"] * t**2 / 2 + c["C"] * t**3 / 3 + c["D"] * t**4 / 4
                - c["E"] / t + c["F"] - c["H"])
    return (h(T2) - h(T1)) * 1000.0


def amount_used(t, rate):
    """Integral of the rate over time = concentration used up (mol/L).
    TODO: use scipy's simpson(rate, x=t)."""
    return None


def main():
    # 1. Work done BY 1.00 mol ideal gas expanding at 298.15 K from 10.0 L to 25.0 L
    n, T = 1.00, 298.15
    exact = n * R * T * np.log(25.0 / 10.0)
    print(f"1. exact work by gas = nRT ln(V2/V1) = {exact:.1f} J")
    for npts in (5, 11, 101):
        V = np.linspace(10.0, 25.0, npts)          # L
        p = n * R * T / V                           # J/L (1 J/L = 1 kPa)
        w = trapezoid(p, V)
        if w is None:
            print("TODO: write trapezoid() first.")
            return
        print(f"   {npts - 1:3d} intervals: trapezoid {w:8.1f} J, simpson {simpson(p, x=V):8.1f} J")

    # 2. Heat to warm 1 mol N2 at constant pressure from 298.15 K to 500 K
    Ts = np.linspace(298.15, 500.0, 21)
    cp = cp_n2(Ts)
    if cp is None:
        print("TODO: write cp_n2() next.")
        return
    print(f"2. Cp(N2) at 298.15 K = {cp[0]:.2f} J/(mol K), at 500 K = {cp[-1]:.2f} J/(mol K)")
    print(f"   dH by simpson      = {simpson(cp, x=Ts):.0f} J/mol")
    print(f"   dH from NIST form  = {enthalpy_change_exact(298.15, 500.0):.0f} J/mol")
    print(f"   dH with constant Cp(298) = {cp[0] * (500.0 - 298.15):.0f} J/mol")

    # 3. Integrate the rate from lesson 02.2 to get the amount used up
    t, c = np.loadtxt(HERE / "decay_concentration.csv", delimiter=",", skiprows=1, unpack=True)
    rate = -np.gradient(c, t)
    used = amount_used(t, rate)
    if used is None:
        print("TODO: write amount_used() last.")
        return
    print(f"3. integral of rate = {used:.5f} mol/L; c(0) - c(end) = {c[0] - c[-1]:.5f} mol/L")


if __name__ == "__main__":
    main()
