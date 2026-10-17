"""Lesson 07.7: uncertainty budget for a salt standard and a serial dilution.

Fill in the two TODOs, then run (from this folder):
    py lesson07_solutions.py                                   # example data
    py lesson07_solutions.py my_salt.csv my_dilution.csv       # your data
Reference solution: lesson07_solutions_solution.py
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U_MASS = 0.1 / math.sqrt(6)    # g, difference of two readings on a 0.1 g scale (Lesson 01.5)


def read_rows(path):
    """Return the CSV rows (after the header) as lists of strings, skipping # comments."""
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    return [r.split(",") for r in lines[1:]]


def salt_standard(path):
    """Mass fraction w = m_salt * purity / m_solution and concentration c = w * rho / M.
    For a product or quotient, relative standard uncertainties add in quadrature."""
    q = {r[0]: (float(r[1]), float(r[2])) for r in read_rows(path)}
    m_s, m_sol, p, rho, M = (q[k][0] for k in ("m_salt", "m_solution", "purity", "density", "M_NaCl"))
    w = m_s * p / m_sol
    c = w * rho * 1000 / M                       # mol/L (rho in g/mL -> g/L)
    budget = {k: q[k][1] / q[k][0] for k in q}   # relative uncertainty of each input
    # TODO 1: combine the relative uncertainties in budget (add their squares, then take the square root).
    u_rel = None
    return w, c, u_rel, budget


def dilution_factor_u(a, w, ua, uw):
    """Dilution factor f = a / (a + w) and its standard uncertainty.
    Partial derivatives: df/da = w/(a+w)^2, df/dw = -a/(a+w)^2 (Lesson 02.5)."""
    f = a / (a + w)
    # TODO 2: u = sqrt((df/da * ua)^2 + (df/dw * uw)^2) with the derivatives in the docstring.
    u = None
    return f, u


def main():
    salt = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "salt_standard_example.csv"
    dil = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "dilution_example.csv"

    w, c, u_rel, budget = salt_standard(salt)
    if u_rel is None or dilution_factor_u(10, 10, U_MASS, U_MASS)[1] is None:
        print("TODO: complete salt_standard() and dilution_factor_u() first.")
        return
    print("Salt standard")
    print(f"  mass fraction w = {100 * w:.3f} %   concentration c = {c:.4f} mol/L")
    print(f"  standard uncertainty: {100 * u_rel:.2f} % -> c = {c:.4f} +/- {c * u_rel:.4f} mol/L")
    print("  budget (share of the variance):")
    total = sum(v ** 2 for v in budget.values())
    for k, v in sorted(budget.items(), key=lambda kv: -kv[1]):
        print(f"    {k:<11} u_rel = {100 * v:5.2f} %   share = {100 * v ** 2 / total:5.1f} %")

    print("\nSerial dilution (weighed)")
    print(f"  {'step':>4} {'factor':>8} {'u_rel step':>11} {'cumulative':>11} {'u_rel cum':>10}")
    cum, cum_u2 = 1.0, 0.0
    for r in read_rows(dil):
        a, wat = float(r[1]), float(r[2])
        f, u = dilution_factor_u(a, wat, U_MASS, U_MASS)
        cum *= f
        cum_u2 += (u / f) ** 2                   # relative uncertainties of a product add in quadrature
        print(f"  {r[0]:>4} {f:>8.4f} {100 * u / f:>10.2f}% {cum:>11.5f} {100 * math.sqrt(cum_u2):>9.2f}%")

    total_mass = 20.0
    a_direct = cum * total_mass
    f_d, u_d = dilution_factor_u(a_direct, total_mass - a_direct, U_MASS, U_MASS)
    print(f"\nDirect dilution to the same factor in one step ({a_direct:.2f} g stock in {total_mass:.0f} g):")
    print(f"  u_rel = {100 * u_d / f_d:.1f} %  against {100 * math.sqrt(cum_u2):.2f} % for the serial route")


if __name__ == "__main__":
    main()
