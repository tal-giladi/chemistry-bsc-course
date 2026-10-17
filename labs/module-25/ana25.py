"""Shared helpers for the Module 25 labs: a CSV reader, the calibration maths of Lesson 09.4,
standard addition, the sRGB linearisation of Lesson 09.6 and a plot saver."""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
DOWNLOADED = HERE / "data" / "downloaded"


def read_csv(path):
    """Read a CSV with one header line (lines starting with # are skipped). Returns a dict of columns.
    Numeric columns become float arrays (empty cells become nan); text columns stay arrays of str."""
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    head = lines[0].split(",")
    rows = [r.split(",") for r in lines[1:]]
    cols = {}
    for j, name in enumerate(head):
        vals = [r[j] if j < len(r) else "" for r in rows]
        try:
            cols[name] = np.array([float(v) if v != "" else np.nan for v in vals])
        except ValueError:
            cols[name] = np.array(vals)
    return cols


def line_fit(x, y):
    """Ordinary least squares y = b + m x. Returns m, b, residual standard deviation s_r, residuals."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m, b = np.polyfit(x, y, 1)
    res = y - (b + m * x)
    s_r = np.sqrt(np.sum(res ** 2) / (x.size - 2))
    return m, b, s_r, res


def conc_from_line(y_unk, x, y, m, b, s_r):
    """Concentration of an unknown read k times and its standard deviation (Harvey eq. 5.12, Lesson 09.4)."""
    y_unk = np.atleast_1d(np.asarray(y_unk, float))
    x, y = np.asarray(x, float), np.asarray(y, float)
    k, n = y_unk.size, x.size
    c = (y_unk.mean() - b) / m
    s_c = s_r / m * np.sqrt(1 / k + 1 / n + (y_unk.mean() - y.mean()) ** 2 / (m ** 2 * np.sum((x - x.mean()) ** 2)))
    return c, abs(s_c)


def standard_addition(added, signal):
    """Standard addition with equal final volumes: fit signal = b + m * added and extrapolate to signal 0.
    Returns the concentration in the measured solution, its standard deviation, and m, b.
    s from Harvey eq. 5.13: s = s_r/|m| * sqrt(1/n + ybar^2 / (m^2 * sum (x - xbar)^2))."""
    x, y = np.asarray(added, float), np.asarray(signal, float)
    m, b, s_r, _ = line_fit(x, y)
    c = b / m
    s_c = s_r / abs(m) * np.sqrt(1 / x.size + y.mean() ** 2 / (m ** 2 * np.sum((x - x.mean()) ** 2)))
    return c, s_c, m, b


def srgb_to_linear(v):
    """Undo the sRGB transfer curve (IEC 61966-2-1). v in 0..255 (or 0..1 if all values <= 1)."""
    v = np.asarray(v, float)
    if v.max() > 1.0:
        v = v / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def save(fig, name):
    RUNS.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(RUNS / name, dpi=120)
    print(f"plot written to runs/{name}")
