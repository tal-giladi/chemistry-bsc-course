"""Lesson 28.1 - stationary points and the minimum-energy path on a model surface.

Fill in the functions marked TODO, then run:  py lesson01_pes.py
Reference solution: lesson01_pes_solution.py
Writes runs/lesson01_pes.png.
The Mueller-Brown surface (K. Mueller and L. D. Brown, Theor. Chim. Acta 53, 75 (1979)) is a standard
two-coordinate test surface with three minima and two saddle points. Its energy unit is arbitrary;
read it as kJ/mol to get a feel for the numbers.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, root

from sr28 import runs_dir

A = np.array([-200.0, -100.0, -170.0, 15.0])
a = np.array([-1.0, -1.0, -6.5, 0.7])
b = np.array([0.0, 0.0, 11.0, 0.6])
c = np.array([-10.0, -10.0, -6.5, 0.7])
x0 = np.array([1.0, 0.0, -0.5, -1.0])
y0 = np.array([0.0, 0.5, 1.5, 1.0])


def energy(p):
    x, y = p
    dx, dy = x - x0, y - y0
    return float(np.sum(A * np.exp(a * dx ** 2 + b * dx * dy + c * dy ** 2)))


def gradient(p):
    x, y = p
    dx, dy = x - x0, y - y0
    e = A * np.exp(a * dx ** 2 + b * dx * dy + c * dy ** 2)
    return np.array([np.sum(e * (2 * a * dx + b * dy)), np.sum(e * (b * dx + 2 * c * dy))])


def hessian(p, h=1e-5):
    """Matrix of second derivatives by central differences of the analytic gradient."""
    Hm = np.zeros((2, 2))
    for i in range(2):
        step = np.zeros(2)
        step[i] = h
        Hm[:, i] = (gradient(p + step) - gradient(p - step)) / (2 * h)
    return 0.5 * (Hm + Hm.T)


def classify(p):
    """'minimum' if both Hessian eigenvalues are positive, 'saddle' if exactly one is negative."""
    # TODO: ev = np.linalg.eigvalsh(hessian(p))   (eigenvalues = curvatures along the two principal directions)
    # TODO: return ("minimum", ev) if all are > 0, ("saddle", ev) if exactly one is < 0, else ("maximum", ev)
    raise NotImplementedError("TODO: write classify() first (see the hints in the code).")


def find_minimum(guess):
    return minimize(energy, guess, jac=gradient, method="BFGS", options={"gtol": 1e-8}).x


def find_stationary(guess):
    """Any stationary point (gradient = 0) near the guess, including saddle points."""
    # TODO: a minimiser cannot find a saddle (it rolls downhill). Solve gradient(p) = 0 instead:
    # TODO: return root(gradient, guess, jac=hessian, tol=1e-12).x
    raise NotImplementedError("TODO: write find_stationary() first (see the hints in the code).")


def steepest_descent(start, step=1e-3, n_max=20000):
    """Follow -gradient from start until the gradient is tiny. Returns an (n, 2) path."""
    path = [np.array(start, float)]
    for _ in range(n_max):
        g = gradient(path[-1])
        norm = np.linalg.norm(g)
        new = path[-1] - step * g / norm
        if norm < 1e-3 or energy(new) >= energy(path[-1]):
            break                      # at the bottom: a further step would go uphill
        path.append(new)
    return np.array(path)


def mep_from_saddle(ts, delta=1e-2):
    """Minimum-energy path: step off the saddle both ways along the negative-curvature eigenvector."""
    # TODO: ev, vec = np.linalg.eigh(hessian(ts)); v = vec[:, np.argmin(ev)]  (the downhill direction at the pass)
    # TODO: back = steepest_descent(ts - delta * v)[::-1]; forward = steepest_descent(ts + delta * v)
    # TODO: return np.vstack([back, ts, forward])
    raise NotImplementedError("TODO: write mep_from_saddle() first (see the hints in the code).")


def arc_length(path):
    return np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])


def main():
    minima = [find_minimum(g) for g in ([-0.5, 1.5], [0.6, 0.0], [-0.05, 0.5])]
    saddles = [find_stationary(g) for g in ([-0.8, 0.6], [0.2, 0.3])]
    print("Stationary points (x, y, E, type, Hessian eigenvalues):")
    for p in minima + saddles:
        kind, ev = classify(p)
        print(f"  ({p[0]:7.3f}, {p[1]:6.3f})  E = {energy(p):8.2f}  {kind:8s} {ev[0]:9.1f} {ev[1]:9.1f}")

    MA, MB, MC = minima
    path1 = mep_from_saddle(saddles[0])
    path2 = mep_from_saddle(saddles[1])
    if np.linalg.norm(path1[0] - MA) > np.linalg.norm(path1[-1] - MA):
        path1 = path1[::-1]            # run the first path from A to C
    if np.linalg.norm(path2[0] - MC) > np.linalg.norm(path2[-1] - MC):
        path2 = path2[::-1]            # and the second from C to B
    print(f"Barrier A -> C via saddle 1: {energy(saddles[0]) - energy(MA):.2f}")
    print(f"Barrier C -> B via saddle 2: {energy(saddles[1]) - energy(MC):.2f}")
    print(f"Overall A -> B: dE = {energy(MB) - energy(MA):.2f}; highest point on the path "
          f"{energy(saddles[0]) - energy(MA):.2f} above A")
    print(f"Straight-line A -> B: highest energy {max(energy(p) for p in np.linspace(MA, MB, 400)) - energy(MA):.2f} "
          f"above A (a path through a hill, not the pass)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    X, Y = np.meshgrid(np.linspace(-1.5, 1.2, 300), np.linspace(-0.4, 2.0, 300))
    Z = np.vectorize(lambda x, y: energy((x, y)))(X, Y)
    ax1.contourf(X, Y, np.minimum(Z, 100), levels=40, cmap="viridis")
    for path in (path1, path2):
        ax1.plot(path[:, 0], path[:, 1], "w-", lw=2)
    for p, lab in zip(minima + saddles, ["A", "B", "C", "TS1", "TS2"]):
        ax1.plot(*p, "ro" if lab.startswith("TS") else "wo")
        ax1.annotate(lab, p, color="w", xytext=(5, 5), textcoords="offset points")
    ax1.set(xlabel="coordinate x", ylabel="coordinate y", title="Mueller-Brown surface and MEP")

    s1, s2 = arc_length(path1), arc_length(path2)
    E1 = [energy(p) for p in path1]
    E2 = [energy(p) for p in path2]
    ax2.plot(s1, E1, label="A - TS1 - C")
    ax2.plot(s2 + s1[-1], E2, label="C - TS2 - B")
    ax2.set(xlabel="distance along the path (reaction coordinate)", ylabel="energy",
            title="Energy profile along the minimum-energy path")
    ax2.legend()
    fig.tight_layout()
    out = runs_dir() / "lesson01_pes.png"
    fig.savefig(out, dpi=120)
    print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
