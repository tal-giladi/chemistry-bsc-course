"""Shared helpers for the Module 26 bio-inorganic labs. You do not need to edit this file.

Constants: CODATA 2022 via NIST (exact SI values). Oxygen data: the standard human blood O2
dissociation curve (37 °C, pH 7.40, PCO2 40 mmHg) of Severinghaus, J. Appl. Physiol. 46, 599 (1979),
Table 1, interpolated by him from the measurements compiled by Roughton and Severinghaus (1973).
Myoglobin: P50 = 2.39 Torr at 37 °C, pH 7.0, n = 1 (Schenkman et al., J. Appl. Physiol. 82, 86, 1997).
Structures: PDB entries (CC0), trimmed to the metal sites, in data/.
Run  py bio26.py  to print a short self-check.
"""
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# CODATA 2022 (exact in the 2019 SI)
K_B = 1.380649e-23        # J/K
N_A = 6.02214076e23       # 1/mol
E_CHARGE = 1.602176634e-19  # C
R = K_B * N_A             # 8.314462618... J/(mol K)
F = E_CHARGE * N_A        # 96485.33212... C/mol
T_BODY = 310.15           # K, 37 °C

# Myoglobin (horse), Schenkman et al. 1997
P50_MB = 2.39             # mmHg (Torr), 37 °C, pH 7.0
# Blood O2 content, Severinghaus (1979, revised 2007), eq. 6: C = 1.34 [Hb] S + 0.0031 PO2  (mL O2 per dL)
HUFNER = 1.34             # mL O2 per g Hb
O2_SOLUBILITY = 0.0031    # mL O2 per dL blood per mmHg
# Bohr effect, Severinghaus (1979): d log10(PO2) / d pH = -0.48 at constant saturation
BOHR_LOG10 = -0.48

METALS = ("FE", "ZN", "CA", "CU", "MG", "MN", "CO", "NI", "MO")


def read_csv(name):
    """Rows of a CSV file in this folder as a list of dicts (strings)."""
    with open(HERE / name, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row and not str(next(iter(row.values()))).startswith("#")]


def column(rows, key, cast=float):
    return np.array([cast(r[key]) for r in rows])


def hb_standard_curve():
    """(PO2 in mmHg, fractional saturation S) of the standard human blood curve."""
    rows = read_csv("hb_standard_curve.csv")
    return column(rows, "po2_mmHg"), column(rows, "saturation_percent") / 100.0


def severinghaus(po2):
    """Severinghaus (1979) equation 1: S = 1 / (23400 / (PO2^3 + 150 PO2) + 1)."""
    po2 = np.asarray(po2, dtype=float)
    return 1.0 / (23400.0 / (po2 ** 3 + 150.0 * po2) + 1.0)


def read_pdb(path):
    """Atoms of a PDB file as a list of dicts: rec, name, res, chain, num, el, xyz (numpy array)."""
    path = Path(path)
    if not path.is_absolute() and not path.exists():
        path = DATA / path
    atoms = []
    for line in path.read_text().splitlines():
        if line.startswith("ENDMDL"):
            break
        if line.startswith(("ATOM", "HETATM")) and line[16] in " A":
            el = line[76:78].strip() or line[12:14].strip()
            atoms.append(dict(rec=line[:6].strip(), name=line[12:16].strip(), res=line[17:20].strip(),
                              chain=line[21], num=int(line[22:26]), el=el.upper(),
                              xyz=np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
    return atoms


def label(atom):
    return f"{atom['res']}{atom['num']}:{atom['name']}"


def runs_dir():
    d = HERE / "runs"
    d.mkdir(exist_ok=True)
    return d


if __name__ == "__main__":
    p, s = hb_standard_curve()
    print(f"R = {R:.6f} J/(mol K), F = {F:.2f} C/mol")
    print(f"standard curve: {len(p)} points, {p.min():.0f}-{p.max():.0f} mmHg; S(26) = {np.interp(26, p, s):.4f}")
    print(f"Severinghaus eq. at 26.8 mmHg: S = {float(severinghaus(26.8)):.4f}")
    files = sorted(DATA.glob("*.pdb"))
    print("structures:", ", ".join(f"{f.stem} ({len(read_pdb(f))} atoms)" for f in files))
