"""Lesson 05.4: reading real instrument data.

Part 1: a UV-Vis export with metadata lines, semicolons and decimal commas (pandas).
Part 2: an IR spectrum in JCAMP-DX AFFN form (X++(Y..Y)), read with a small parser and checked.

Fill in the two functions marked TODO, then run (from this folder):
    py lesson04_reading.py                                  # the example files
    py lesson04_reading.py data/downloaded/ethanol_ir.jdx    # a real NIST spectrum
                                                            # (get it with fetch_nist_ir.py)
Reference solution: lesson04_reading_solution.py
The figure is saved to runs/lesson04_reading.png next to this file.
"""
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

HERE = Path(__file__).resolve().parent
NUMBER = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[Ee][+-]?\d+)?")


def read_export(path):
    """Return (metadata dict, DataFrame with columns wavelength_nm and A).
    The data block starts at the line that begins with 'Wavelength'."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    # TODO: start = index of the first line that starts with "Wavelength"
    # TODO: meta = {key: value} from the "key;value" lines before it (strip spaces)
    # TODO: df = pd.read_csv(path, sep=..., decimal=..., skiprows=start); then rename the columns
    #       to ["wavelength_nm", "A"]. Check df.dtypes: both must be float64, not str.
    return None


def read_jcamp(path):
    """Return (labels dict, x array, y array) for a JCAMP-DX file with ##XYDATA=(X++(Y..Y)) in
    AFFN form (plain numbers). Compressed forms (SQZ/DIF letters) are refused with a clear error."""
    labels, data_lines, in_data = {}, [], False
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("##"):
            key, _, value = line[2:].partition("=")
            key = key.strip().upper()
            in_data = key == "XYDATA"
            if key != "END":
                labels[key] = value.strip()
        elif in_data and line.strip():
            data_lines.append(line.split("$$")[0])        # $$ starts a comment
    if labels.get("XYDATA") != "(X++(Y..Y))":
        raise ValueError(f"unsupported XYDATA form {labels.get('XYDATA')!r}")
    xf, yf = float(labels.get("XFACTOR", 1)), float(labels.get("YFACTOR", 1))
    first_x, dx = float(labels["FIRSTX"]), float(labels["DELTAX"])
    ys, line_x = [], []
    for line in data_lines:
        if re.search(r"[@A-Za-z%]", line):
            raise ValueError("compressed JCAMP-DX (SQZ/DIF) is not handled by this reader")
        # TODO: nums = the numbers on the line (NUMBER.findall(line), as floats)
        # TODO: the first number is the X of the line: line_x.append((nums[0] * xf, len(ys)))
        # TODO: the rest are Y values: add them to ys
        pass
    # TODO: y = np.array(ys) * yf   (the integers in the file are scaled by YFACTOR)
    y = None
    if y is None:
        return None
    x = first_x + dx * np.arange(y.size)
    # checks: the point count, and the X at the start of every line
    n_expected = int(labels["NPOINTS"])
    if y.size != n_expected:
        raise ValueError(f"read {y.size} points but NPOINTS says {n_expected}")
    worst = max(abs(x[i] - x_line) for x_line, i in line_x)
    if worst > abs(dx) / 2:
        raise ValueError(f"line X values disagree with FIRSTX + i*DELTAX by up to {worst}")
    return labels, x, y


def main():
    res = read_export(HERE / "uvvis_export.csv")
    if res is None:
        print("TODO: write read_export() first.")
        return
    meta, uv = res
    i_max = uv["A"].idxmax()
    path_cm = float(meta["Path length [cm]"].replace(",", "."))
    print("Part 1: UV-Vis export")
    print(f"  sample: {meta['Sample']}; path length {path_cm:.3f} cm; {len(uv)} points, "
          f"{uv['wavelength_nm'].min():.0f}-{uv['wavelength_nm'].max():.0f} nm")
    print(f"  dtypes: {dict(uv.dtypes.astype(str))}; missing values: {int(uv.isna().sum().sum())}")
    print(f"  maximum A = {uv.loc[i_max, 'A']:.3f} at {uv.loc[i_max, 'wavelength_nm']:.0f} nm")

    jdx = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "example_ir.jdx"
    res = read_jcamp(jdx)
    if res is None:
        print("\nTODO: finish the data loop in read_jcamp() next.")
        return
    labels, x, y = res
    peaks, _ = find_peaks(y, prominence=0.05 * y.max())
    top = peaks[np.argsort(y[peaks])[::-1][:5]]
    print(f"\nPart 2: {jdx.name}: {labels.get('TITLE')}")
    print(f"  {x.size} points (NPOINTS = {labels['NPOINTS']}), {x[0]:.0f}-{x[-1]:.0f} "
          f"{labels.get('XUNITS')}, y in {labels.get('YUNITS')}, max {y.max():.3f}")
    print("  strongest bands (cm-1, absorbance): "
          + ", ".join(f"{x[i]:.0f} ({y[i]:.2f})" for i in top))

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 5.8))
    a1.plot(uv["wavelength_nm"], uv["A"])
    a1.set_xlabel("wavelength (nm)")
    a1.set_ylabel("absorbance")
    a1.set_title(meta["Sample"], fontsize=9)
    a2.plot(x, y)
    a2.plot(x[top], y[top], "v")
    a2.invert_xaxis()                     # IR convention: high wavenumber on the left
    a2.set_xlabel("wavenumber (cm$^{-1}$)")
    a2.set_ylabel("absorbance")
    a2.set_title(labels.get("TITLE", jdx.name)[:70], fontsize=9)
    fig.tight_layout()
    out = HERE / "runs" / "lesson04_reading.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
