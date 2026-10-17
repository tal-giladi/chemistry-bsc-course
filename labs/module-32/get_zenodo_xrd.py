"""Download the three REAL powder XRD patterns used in Module 32 from Zenodo and convert them to the CSV files of
this folder (the CSV files are already included; run this only to check them against the originals):

    py get_zenodo_xrd.py

Source: Dahiya H., Dahiya B. and Sabarwal S. (2026). Raw powder X-ray diffraction (XRD) data for GCN, CdO, In2O3,
CdO-In2O3, CdO-In2O3-GCN [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18522088
Licence: Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/
Changes made: CdO.xy, In2O3.xy and CdO-In2O3.asc converted to CSV (two_theta_deg,counts) with a comment header;
no values changed. The .asc header records a Rigaku MiniFlex, Cu target, K-alpha 1.54059/1.54441 A, no filter.
Originals are saved to data/downloaded/ (ignored by git). Needs only the Python standard library and numpy.
"""
import re
import urllib.parse
import urllib.request

import numpy as np

from ec32 import HERE

RECORD = "https://zenodo.org/api/records/18522088/files/{}/content"
FILES = {"CdO.xy": "cdo_xrd.csv", "In2O3.xy": "in2o3_xrd.csv", "CdO-In2O3.asc": "cdo_in2o3_xrd.csv"}
HEADER = ("# REAL DATA. Dahiya, Dahiya and Sabarwal (2026), Zenodo, https://doi.org/10.5281/zenodo.18522088, "
          "CC BY 4.0.\n# Original file: {orig}. Converted to CSV by get_zenodo_xrd.py; values unchanged. "
          "Cu tube, no K-beta filter (from the .asc header).\ntwo_theta_deg,counts\n")


def parse(name, raw):
    text = raw.decode("ascii", errors="replace")
    if name.endswith(".xy"):
        data = np.loadtxt(text.splitlines())
        return data[:, 0], data[:, 1]
    def field(key):
        return float(re.search(r"^\*" + key + r"\s*=\s*(\S+)", text, re.M).group(1))
    start, step = field("START"), field("STEP")
    body = re.split(r"^\*COUNT\s*=.*$", text, maxsplit=1, flags=re.M)[1]
    values = body.split("*END")[0].replace(",", " ").split()
    y = np.array([float(v) for v in values])
    return start + step * np.arange(len(y)), y


def main():
    out = HERE / "data" / "downloaded"
    out.mkdir(parents=True, exist_ok=True)
    for name, csv_name in FILES.items():
        url = RECORD.format(urllib.parse.quote(name))
        with urllib.request.urlopen(url, timeout=60) as resp:
            raw = resp.read()
        (out / name).write_bytes(raw)
        tt, y = parse(name, raw)
        lines = [f"{a:.5f},{b:.0f}" for a, b in zip(tt, y)]
        (HERE / csv_name).write_text(HEADER.format(orig=name) + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"{name}: {len(y)} points, 2theta {tt[0]:.2f}-{tt[-1]:.2f} deg -> {csv_name}")


if __name__ == "__main__":
    main()
