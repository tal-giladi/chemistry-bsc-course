"""Lesson 09.4 (reference solution): calibration line, unknown with uncertainty, LOD/LOQ and standard additions.

Run (from this folder):
    py lesson04_calibration_solution.py                        # example data
    py lesson04_calibration_solution.py my_calibration.csv     # your data, same columns
Data columns: type,c_mg_per_L,absorbance with type = standard | blank | unknown | addition.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def read_rows(path):
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    rows = [r.split(",") for r in lines[1:]]
    get = lambda t, col: np.array([float(r[col]) for r in rows if r[0] == t])
    return get


def line_fit(x, y):
    """Ordinary least squares y = b + m x. Returns m, b, residual standard deviation s_r, residuals."""
    m, b = np.polyfit(x, y, 1)
    res = y - (b + m * x)
    s_r = np.sqrt(np.sum(res ** 2) / (x.size - 2))
    return m, b, s_r, res


def conc_from_line(y_unk, x, y, m, b, s_r):
    """Concentration of an unknown read k times, and its standard deviation (Harvey eq. 5.12, Lesson 05.3)."""
    k, n = y_unk.size, x.size
    c = (y_unk.mean() - b) / m
    s_c = s_r / m * np.sqrt(1 / k + 1 / n + (y_unk.mean() - y.mean()) ** 2 / (m ** 2 * np.sum((x - x.mean()) ** 2)))
    return c, s_c


def main():
    RUNS.mkdir(exist_ok=True)
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "nitrite_calibration.csv"
    get = read_rows(path)
    x, y = get("standard", 1), get("standard", 2)
    m, b, s_r, res = line_fit(x, y)
    print(f"Calibration ({x.size} standards): A = {b:.4f} + {m:.3f} c   s_r = {s_r:.4f}")
    print("   residuals: " + " ".join(f"{r:+.4f}" for r in res))

    blanks = get("blank", 2)
    s_bl = blanks.std(ddof=1)
    lod = 3 * s_bl / m
    loq = 10 * s_bl / m
    print(f"Blanks: n={blanks.size} mean={blanks.mean():.4f} s={s_bl:.4f}")
    print(f"   LOD = 3 s_blank / m = {lod:.4f} mg/L    LOQ = 10 s_blank / m = {loq:.4f} mg/L")
    print(f"   regression-based (ICH Q2(R2)): DL = 3.3 s_r / m = {3.3 * s_r / m:.4f} mg/L, QL = 10 s_r / m = {10 * s_r / m:.4f} mg/L")

    unk = get("unknown", 2)
    if unk.size:
        c, s_c = conc_from_line(unk, x, y, m, b, s_r)
        note = "above the LOQ" if c > loq else ("between LOD and LOQ: detected, not quantified" if c > lod else "below the LOD")
        print(f"Unknown: c = {c:.4f} +/- {s_c:.4f} mg/L ({note})")

    xa, ya = get("addition", 1), get("addition", 2)
    if xa.size:
        ma, ba, s_ra, _ = line_fit(xa, ya)
        c_sa = ba / ma
        s_sa = s_ra / ma * np.sqrt(1 / xa.size + ya.mean() ** 2 / (ma ** 2 * np.sum((xa - xa.mean()) ** 2)))
        c_ext = (ya[xa == 0].mean() - b) / m
        print(f"Standard additions: slope {ma:.3f} (external {m:.3f}, ratio {ma / m:.2f})")
        print(f"   sample = intercept / slope = {c_sa:.4f} +/- {s_sa:.4f} mg/L; external line would say {c_ext:.4f} mg/L")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    xx = np.linspace(-0.06, x.max(), 50)
    ax[0].plot(x, y, "o", label="standards")
    ax[0].plot(xx[xx >= 0], b + m * xx[xx >= 0], "-", label="external line")
    if xa.size:
        ax[0].plot(xa, ya, "s", label="standard additions")
        ax[0].plot(xx, ba + ma * xx, "--")
        ax[0].axvline(0, color="grey", lw=0.8)
    ax[0].set(xlabel="c or c added (mg/L)", ylabel="absorbance", title="Calibration")
    ax[0].legend()
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].plot(x, res, "o")
    ax[1].set(xlabel="c (mg/L)", ylabel="residual", title="Residuals")
    fig.tight_layout()
    fig.savefig(RUNS / "lesson04_calibration.png", dpi=120)
    print("plot written to runs/lesson04_calibration.png")


if __name__ == "__main__":
    main()
