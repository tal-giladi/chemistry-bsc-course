"""Shared helpers for the Module 15 labs (RDKit 2026.9.1, numpy, matplotlib).
Keep this file in the same folder as the lesson scripts."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_KJ = 8.314462618e-3  # gas constant in kJ/(mol K), CODATA 2022 (exact SI-derived value)


def read_csv(name):
    """Read a small CSV in this folder into a list of dicts. Lines starting with # are comments."""
    lines = [x for x in (HERE / name).read_text(encoding="utf-8").splitlines() if x and not x.startswith("#")]
    keys = lines[0].split(",")
    return [dict(zip(keys, x.split(","))) for x in lines[1:]]


def need_rdkit():
    try:
        import rdkit  # noqa: F401
    except ImportError:
        raise SystemExit("RDKit is missing. Install the course packages: "
                         "py -m pip install -r labs/common/requirements.txt")


def runs_dir():
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    return out


def canon(smiles):
    """Canonical isomeric SMILES (keeps stereochemistry), or None if RDKit cannot read it."""
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(m) if m is not None else None
