"""Read a phyphox CSV export (or any CSV whose first line is a header) with numpy only.

phyphox exports one CSV file per data set: the first column is time in seconds, the next columns
are the sensor axes. Column names differ between experiments and app versions, so the labs pick
columns by position, not by name. Use "Comma-separated values" with a decimal point when you export.
"""
import numpy as np


def read_csv(path):
    """Return (header list, 2D float array). Quotes around header names are removed."""
    with open(path, encoding="utf-8-sig") as fh:
        header = [h.strip().strip('"') for h in fh.readline().strip().split(",")]
    data = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
    return header, data


def time_and_column(path, column):
    """Time array and one data column (by position, 0 = time)."""
    header, data = read_csv(path)
    return data[:, 0], data[:, column], header[column]
