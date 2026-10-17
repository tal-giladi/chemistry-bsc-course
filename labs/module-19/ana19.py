"""Shared helpers for the Module 19 labs: a small CSV reader and the calibration maths of Lesson 09.4."""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def read_csv(path):
    """Read a CSV with one header line (lines starting with # are skipped). Returns a dict of columns.
    Numeric columns become float arrays (empty cells become nan); text columns stay lists of str."""
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    head = lines[0].split(",")
    rows = [r.split(",") for r in lines[1:]]
    cols = {}
    for j, name in enumerate(head):
        vals = [r[j] for r in rows]
        try:
            cols[name] = np.array([float(v) if v != "" else np.nan for v in vals])
        except ValueError:
            cols[name] = np.array(vals)
    return cols


def line_fit(x, y):
    """Ordinary least squares y = b + m x. Returns m, b, residual standard deviation s_r, residuals."""
    m, b = np.polyfit(x, y, 1)
    res = y - (b + m * x)
    s_r = np.sqrt(np.sum(res ** 2) / (x.size - 2))
    return m, b, s_r, res


def conc_from_line(y_unk, x, y, m, b, s_r):
    """Concentration of an unknown read k times and its standard deviation (Harvey eq. 5.12, Lesson 09.4)."""
    y_unk = np.atleast_1d(y_unk)
    k, n = y_unk.size, x.size
    c = (y_unk.mean() - b) / m
    s_c = s_r / m * np.sqrt(1 / k + 1 / n + (y_unk.mean() - y.mean()) ** 2 / (m ** 2 * np.sum((x - x.mean()) ** 2)))
    return c, s_c


def save(fig, name):
    RUNS.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(RUNS / name, dpi=120)
    print(f"plot written to runs/{name}")
