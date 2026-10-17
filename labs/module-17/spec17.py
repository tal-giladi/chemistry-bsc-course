"""Shared helpers for the Module 17 labs (numpy, matplotlib, RDKit 2026.9.1).
Keep this file in the same folder as the lesson scripts.

Isotope masses and abundances: NIST "Atomic Weights and Isotopic Compositions"
(https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl), checked 2026-10-17.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# element: list of (mass number, exact mass in u, natural abundance as a fraction)
ISOTOPES = {
    "H": [(1, 1.00782503223, 0.999885), (2, 2.01410177812, 0.000115)],
    "C": [(12, 12.0, 0.9893), (13, 13.00335483507, 0.0107)],
    "N": [(14, 14.00307400443, 0.99636), (15, 15.00010889888, 0.00364)],
    "O": [(16, 15.99491461957, 0.99757), (17, 16.99913175650, 0.00038), (18, 17.99915961286, 0.00205)],
    "S": [(32, 31.9720711744, 0.9499), (33, 32.9714589098, 0.0075), (34, 33.967867004, 0.0425)],
    "Cl": [(35, 34.968852682, 0.7576), (37, 36.965902602, 0.2424)],
    "Br": [(79, 78.9183376, 0.5069), (81, 80.9162897, 0.4931)],
    "F": [(19, 18.99840316273, 1.0)],
    "I": [(127, 126.9044719, 1.0)],
}
ELECTRON_MASS_U = 5.485799090441e-4  # CODATA 2022 electron mass in u


def parse_formula(formula):
    """'C4H9Cl' -> {'C': 4, 'H': 9, 'Cl': 1}. Simple formulas only (no brackets)."""
    counts = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if el not in ISOTOPES:
            raise ValueError(f"element {el} not in the table")
        counts[el] = counts.get(el, 0) + (int(n) if n else 1)
    return counts


def read_csv(name):
    """Read a small CSV in this folder into a list of dicts. Lines starting with # are comments."""
    lines = [x for x in (HERE / name).read_text(encoding="utf-8").splitlines() if x and not x.startswith("#")]
    keys = lines[0].split(",")
    return [dict(zip(keys, x.split(","))) for x in lines[1:]]


def runs_dir():
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    return out


def need_rdkit():
    try:
        import rdkit  # noqa: F401
    except ImportError:
        raise SystemExit("RDKit is missing. Install the course packages: "
                         "py -m pip install -r labs/common/requirements.txt")


def canon(smiles):
    """Canonical SMILES without stereochemistry, or None if RDKit cannot read it."""
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(m, isomericSmiles=False) if m is not None else None
