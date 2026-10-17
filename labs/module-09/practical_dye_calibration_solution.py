"""Module 9 practical (reference solution): a full calibration with detection limit from phone photos of a
blue food-colour dilution series.

The phone stores colours in sRGB, which is not proportional to light intensity. Each red value is first
converted back to linear intensity, then to a pseudo-absorbance A = -log10(I / I_blank). Blue dye absorbs red
light (Brilliant Blue FCF has its maximum near 630 nm), so the red channel carries the signal.

Run (from this folder):
    py practical_dye_calibration_solution.py                 # example data
    py practical_dye_calibration_solution.py my_photos.csv   # your data, same columns
Columns: type,c_percent_stock,R,G,B with type = standard | blank | unknown | check.
"""
import sys
from pathlib import Path

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
MAX_DEV = 0.03          # a standard is "on the line" if it deviates by less than 3 % from the line below it


def srgb_to_linear(v):
    """sRGB value 0-255 -> linear intensity 0-1 (the sRGB transfer function, IEC 61966-2-1)."""
    x = np.asarray(v, float) / 255
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def read(path):
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    rows = [r.split(",") for r in lines[1:]]
    out = {}
    for r in rows:
        c = float(r[1]) if r[1] else np.nan
        out.setdefault(r[0], []).append((c, float(r[2]), float(r[3]), float(r[4])))
    return {k: np.array(v) for k, v in out.items()}


def fit(x, y):
    m, b = np.polyfit(x, y, 1)
    res = y - (b + m * x)
    return m, b, np.sqrt(np.sum(res ** 2) / (x.size - 2)), res


def main():
    RUNS.mkdir(exist_ok=True)
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "dye_photo_example.csv"
    d = read(path)
    i_blank = srgb_to_linear(d["blank"][:, 1]).mean()
    absorb = lambda rows: -np.log10(srgb_to_linear(rows[:, 1]) / i_blank)

    a_bl = absorb(d["blank"])
    s_bl = a_bl.std(ddof=1)
    c, a = d["standard"][:, 0], absorb(d["standard"])
    print(f"Blanks: {a_bl.size} photos, s = {s_bl:.4f} absorbance units")

    # linear range: fit the lowest five standards, then keep adding while the next one stays within MAX_DEV
    order = np.argsort(c)
    c, a = c[order], a[order]
    n_lin = 5
    m0, b0, _, _ = fit(c[:n_lin], a[:n_lin])
    while n_lin < c.size and abs(a[n_lin] - (b0 + m0 * c[n_lin])) / (b0 + m0 * c[n_lin]) < MAX_DEV:
        n_lin += 1
        m0, b0, _, _ = fit(c[:n_lin], a[:n_lin])
    print("Deviation of each standard from the low-range line:")
    for ci, ai in zip(c, a):
        pred = b0 + m0 * ci
        print(f"   {ci:5.1f} %  A = {ai:.4f}  line {pred:.4f}  " + (f"{100 * (ai - pred) / pred:+.1f} %" if ci > 0 else ""))
    c_top = c[n_lin - 1]
    m, b, s_r, res = fit(c[:n_lin], a[:n_lin])
    print(f"Linear range up to {c_top:g} % stock ({n_lin} standards): A = {b:.4f} + {m:.4f} c, s_r = {s_r:.4f}")

    lod, loq = 3 * s_bl / m, 10 * s_bl / m
    print(f"LOD = {lod:.3f} % stock   LOQ = {loq:.3f} % stock   working range {loq:.2f} to {c_top:g} % stock")

    def readback(rows):
        y = absorb(rows)
        k, n, x = y.size, n_lin, c[:n_lin]
        cc = (y.mean() - b) / m
        s_c = s_r / m * np.sqrt(1 / k + 1 / n + (y.mean() - a[:n_lin].mean()) ** 2 / (m ** 2 * np.sum((x - x.mean()) ** 2)))
        return cc, s_c, y

    cu, su, _ = readback(d["unknown"])
    t = stats.t.ppf(0.975, n_lin - 2)
    print(f"Unknown: c = {cu:.2f} +/- {su:.2f} % stock (standard uncertainty); 95 % interval +/- {t * su:.2f}")
    if "check" in d:
        nominal = d["check"][0, 0]
        cc, sc, _ = readback(d["check"])
        z = (cc - nominal) / sc
        print(f"Check standard ({nominal:g} %): found {cc:.2f} +/- {sc:.2f}, recovery {100 * cc / nominal:.1f} %, "
              f"z = {z:+.1f} -> {'no evidence of bias' if abs(z) <= 2 else 'look for a bias'}")

    # what skipping the sRGB linearisation would do: sRGB is roughly intensity^(1/2.2), so the "absorbance"
    # comes out about 2.2 times too small and no longer compares with Beer-Lambert values
    raw = lambda rows: -np.log10(rows[:, 1] / d["blank"][:, 1].mean())
    m_raw = fit(c[:n_lin], raw(d["standard"])[order][:n_lin])[0]
    print(f"Without linearising sRGB the slope would be {m_raw:.4f} instead of {m:.4f} (ratio {m / m_raw:.2f})")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    xx = np.linspace(0, c.max(), 50)
    ax[0].plot(c, a, "o", label="standards")
    ax[0].plot(xx, b + m * xx, "-", label=f"line, 0-{c_top:g} %")
    ax[0].axvline(c_top, color="grey", lw=0.8, ls=":")
    ax[0].set(xlabel="% of stock", ylabel="pseudo-absorbance (red)", title="Calibration from photos")
    ax[0].legend()
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].plot(c, a - (b + m * c), "o")
    ax[1].set(xlabel="% of stock", ylabel="residual", title="Residuals (all standards)")
    fig.tight_layout()
    fig.savefig(RUNS / "practical_dye_calibration.png", dpi=120)
    print("plot written to runs/practical_dye_calibration.png")


if __name__ == "__main__":
    main()
