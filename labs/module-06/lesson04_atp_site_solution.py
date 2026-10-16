"""Lesson 06.4 reference solution (module practical, part 3): the polar contacts that hold ATP
in protein kinase A, PDB entry 1ATP.

First download the structure (once):   py fetch_pdb.py 1ATP
Then run:                              py lesson04_atp_site_solution.py
Other entries:                         py lesson04_atp_site_solution.py data/downloaded/XXXX.pdb ANP
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def read_atoms(path):
    """Return a list of dicts (name, resn, chain, resi, element, xyz) for ATOM and HETATM records."""
    atoms = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(("ATOM", "HETATM")) and line[16] in " A":
            el = line[76:78].strip() or line[12:14].strip()[0]
            atoms.append({"name": line[12:16].strip(), "resn": line[17:20].strip(), "chain": line[21],
                          "resi": int(line[22:26]), "element": el.upper(), "het": line.startswith("HETATM"),
                          "xyz": np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])})
    return atoms


def polar_contacts(ligand, protein, cutoff=3.3):
    """All pairs (ligand atom, protein atom, distance in angstrom) where both atoms are N or O and
    the distance is below the cutoff. This is the usual quick test for a possible hydrogen bond
    (donor-acceptor distance about 2.6-3.3 angstrom)."""
    out = []
    for a in ligand:
        if a["element"] not in ("N", "O"):
            continue
        for b in protein:
            if b["element"] not in ("N", "O"):
                continue
            d = float(np.linalg.norm(a["xyz"] - b["xyz"]))
            if d < cutoff:
                out.append((a, b, d))
    return out


def near_metal(a, b, metals, r=3.4):
    """True if one metal ion is within r angstrom of both atoms: the pair is held by the metal,
    not (only) by a hydrogen bond."""
    return any(np.linalg.norm(m["xyz"] - a["xyz"]) < r and np.linalg.norm(m["xyz"] - b["xyz"]) < r
               for m in metals)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "data" / "downloaded" / "1ATP.pdb"
    lig_name = sys.argv[2] if len(sys.argv) > 2 else "ATP"
    if not path.exists():
        print(f"{path} not found. Download it first:  py fetch_pdb.py 1ATP")
        return
    atoms = read_atoms(path)
    ligand = [a for a in atoms if a["resn"] == lig_name]
    if not ligand:
        print(f"no residue named {lig_name} in {path.name}")
        return
    chain = ligand[0]["chain"]
    ligand = [a for a in ligand if a["chain"] == chain and a["resi"] == ligand[0]["resi"]]
    protein = [a for a in atoms if not a["het"] or a["resn"] in ("SEP", "TPO")]   # phospho-Ser/Thr are protein
    metals = [a for a in atoms if a["het"] and a["element"] in ("MN", "MG", "ZN", "CA")]
    contacts = polar_contacts(ligand, protein)
    print(f"{path.name}: {lig_name} with {len(ligand)} atoms; {len(metals)} metal ions in the file")
    print(f"polar contacts below 3.3 angstrom: {len(contacts)}")
    for a, b, d in sorted(contacts, key=lambda c: (c[1]["resi"], c[2])):
        tag = "  via metal" if near_metal(a, b, metals) else ""
        bb = "backbone" if b["name"] in ("N", "O") else "side chain"
        print(f"  {lig_name} {a['name']:<4} - {b['resn']}{b['resi']:<4} {b['name']:<4} ({bb:<10}) {d:.2f}{tag}")
    residues = sorted({(b["resi"], b["resn"]) for _, b, _ in contacts})
    direct = [c for c in contacts if not near_metal(c[0], c[1], metals)]
    print(f"protein residues involved: {len(residues)}: " + ", ".join(f"{n}{i}" for i, n in residues))
    print(f"contacts not bridged by a metal ion (candidate hydrogen bonds): {len(direct)}")
    groups = {"adenine": ("N1", "N3", "N6", "N7"), "ribose": ("O2'", "O3'", "O4'"),
              "phosphates": tuple(f"O{i}{x}" for i in "123" for x in "ABG") + ("O3A", "O3B", "O5'")}
    for g, names in groups.items():
        print(f"  {g:<10} {sum(1 for a, _, _ in direct if a['name'] in names)}")


if __name__ == "__main__":
    main()
