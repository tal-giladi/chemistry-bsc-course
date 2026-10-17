"""Shared helpers for the Module 31 labs (Computational Chemistry Lab).

Finds and runs xtb, reads xyz files, xtb scan logs, xtb `vibspectrum` files and the
ORCA 6.1 output tables used in the lessons (frequencies, IR spectrum, NMR shieldings,
TD-DFT absorption), and holds a few constants and small numerical tools.

Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
The ORCA parsers follow the table layouts printed in the ORCA 6.1 manual; they were not run on
real ORCA output when this module was written (see README.md).
"""
import csv
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MOLECULES = HERE / "molecules"
RUNS = HERE / "runs"

HARTREE_KJMOL = 2625.499639        # 1 Eh in kJ/mol (CODATA 2022 Eh times N_A)
HARTREE_EV = 27.211386245981       # 1 Eh in eV
KB = 1.380649e-23                  # J/K, exact
H_PLANCK = 6.62607015e-34          # J s, exact
R_GAS = 8.314462618                # J/(mol K)
HC_EV_NM = 1239.841984             # h c in eV nm


# ---------------------------------------------------------------- xtb

def find_xtb():
    """Return the path of the xtb executable, or None.

    Looks at the XTB environment variable first (set it if xtb is not on PATH),
    then on PATH."""
    env = os.environ.get("XTB")
    if env and Path(env).exists():
        return str(Path(env))
    return shutil.which("xtb")


def run_xtb(xyz, args, workdir, out_name="xtb.out", threads=2):
    """Copy `xyz` into `workdir`, run `xtb <xyz> <args>` there and return the output path.

    Raises RuntimeError if xtb is missing or does not end with 'normal termination'."""
    exe = find_xtb()
    if exe is None:
        raise RuntimeError("xtb not found: put it on PATH or set the XTB environment variable")
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    src = Path(xyz)
    dst = workdir / src.name
    if src.resolve() != dst.resolve():
        shutil.copyfile(src, dst)
    extra = []
    for a in args:
        p = Path(a)
        if p.suffix == ".inp" and p.exists():       # copy xcontrol input files too
            shutil.copyfile(p, workdir / p.name)
            extra.append(p.name)
        else:
            extra.append(a)
    env = dict(os.environ, OMP_NUM_THREADS=str(threads), OMP_STACKSIZE="1G")
    out = workdir / out_name
    with open(out, "w", encoding="utf-8", errors="replace") as fh:
        subprocess.run([exe, dst.name, *extra], cwd=workdir, stdout=fh,
                       stderr=subprocess.STDOUT, env=env, check=False)
    text = out.read_text(encoding="utf-8", errors="replace")
    if "normal termination of xtb" not in text:
        raise RuntimeError(f"xtb did not terminate normally, see {out}")
    return out


def xtb_total_energy(out_path):
    """Last 'TOTAL ENERGY' in an xtb output, in hartree."""
    vals = re.findall(r"TOTAL ENERGY\s+(-?\d+\.\d+)\s+Eh",
                      Path(out_path).read_text(encoding="utf-8", errors="replace"))
    if not vals:
        raise ValueError(f"no TOTAL ENERGY in {out_path}")
    return float(vals[-1])


def read_vibspectrum(path):
    """Read an xtb/Turbomole `vibspectrum` file.

    Returns a list of (wavenumber_cm1, ir_intensity_km_mol, ir_active) for every line,
    including the six (five) zero modes. Imaginary modes appear as negative wavenumbers."""
    rows = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith(("$", "#")):
            continue
        parts = s.split()
        # mode [symmetry] wavenumber intensity selection
        nums = [p for p in parts[1:] if re.fullmatch(r"-?\d+\.\d+", p)]
        if len(nums) < 2:
            continue
        rows.append((float(nums[0]), float(nums[1]), parts[-1].upper() == "YES"))
    return rows


def vibrations(rows, zero_cut=20.0):
    """Drop the translations/rotations (|wavenumber| < zero_cut) from read_vibspectrum rows."""
    return [r for r in rows if abs(r[0]) >= zero_cut]


# ---------------------------------------------------------------- geometry

def read_xyz(path):
    """Read a single-structure xyz file. Returns (symbols, coords in Å as (N,3) array, comment)."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    n = int(lines[0].split()[0])
    sym, xyz = [], []
    for line in lines[2:2 + n]:
        p = line.split()
        sym.append(p[0])
        xyz.append([float(v) for v in p[1:4]])
    return sym, np.array(xyz), lines[1]


def read_multixyz(path):
    """Read a multi-structure xyz file such as xtbscan.log or a conformer ensemble.

    Returns a list of (symbols, coords, energy_hartree_or_None)."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    frames, i = [], 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        n = int(lines[i].split()[0])
        comment = lines[i + 1]
        m = re.search(r"energy:\s*(-?\d+\.\d+)", comment) or re.search(r"^\s*(-?\d+\.\d+)", comment)
        sym, xyz = [], []
        for line in lines[i + 2:i + 2 + n]:
            p = line.split()
            sym.append(p[0])
            xyz.append([float(v) for v in p[1:4]])
        frames.append((sym, np.array(xyz), float(m.group(1)) if m else None))
        i += n + 2
    return frames


def write_xyz(path, symbols, coords, comment=""):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{len(symbols)}\n{comment}\n")
        for s, (x, y, z) in zip(symbols, coords):
            fh.write(f"{s:2s} {x:14.8f} {y:14.8f} {z:14.8f}\n")


def distance(x, i, j):
    """Distance between atoms i and j (0-based) in Å."""
    return float(np.linalg.norm(x[i] - x[j]))


def angle(x, i, j, k):
    """Angle i-j-k in degrees (0-based atom indices, j is the vertex)."""
    a, b = x[i] - x[j], x[k] - x[j]
    c = a @ b / np.linalg.norm(a) / np.linalg.norm(b)
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def dihedral(x, i, j, k, l):
    """Dihedral i-j-k-l in degrees, range (-180, 180]."""
    b0, b1, b2 = x[i] - x[j], x[k] - x[j], x[l] - x[k]
    b1 = b1 / np.linalg.norm(b1)
    v = b0 - (b0 @ b1) * b1
    w = b2 - (b2 @ b1) * b1
    return float(np.degrees(np.arctan2(np.cross(b1, v) @ w, v @ w)))


# ---------------------------------------------------------------- ORCA 6.1 output tables

def orca_final_energy(path):
    """Last 'FINAL SINGLE POINT ENERGY' in an ORCA output, in hartree."""
    vals = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)",
                      Path(path).read_text(encoding="utf-8", errors="replace"))
    if not vals:
        raise ValueError(f"no FINAL SINGLE POINT ENERGY in {path}")
    return float(vals[-1])


def _last_block(text, title):
    idx = text.rfind(title)
    if idx < 0:
        raise ValueError(f"'{title}' not found")
    return text[idx:].splitlines()


def orca_frequencies(path):
    """Wavenumbers (cm-1) from the last VIBRATIONAL FREQUENCIES block, zero modes included.

    ORCA prints imaginary modes as negative numbers."""
    lines = _last_block(Path(path).read_text(encoding="utf-8", errors="replace"),
                        "VIBRATIONAL FREQUENCIES")
    out, started = [], False
    for line in lines[1:]:
        m = re.match(r"\s*(\d+):\s+(-?\d+\.\d+)\s+cm\*\*-1", line)
        if m:
            out.append(float(m.group(2)))
            started = True
        elif started and line.strip() and not line.strip().startswith("*"):
            break
    return out


def orca_ir(path):
    """(wavenumber_cm1, intensity_km_mol) pairs from the last IR SPECTRUM table."""
    lines = _last_block(Path(path).read_text(encoding="utf-8", errors="replace"), "IR SPECTRUM")
    out = []
    for line in lines[1:]:
        m = re.match(r"\s*(\d+):\s+(-?\d+\.\d+)\s+(\S+)\s+(\S+)", line)
        if m:
            out.append((float(m.group(2)), float(m.group(4))))
        elif out and not line.strip():
            break
    return out


def orca_nmr_shieldings(path):
    """{(atom_index, element): isotropic shielding in ppm} from the last NMR summary table."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    idx = text.rfind("Nucleus  Element    Isotropic")
    if idx < 0:
        idx = text.rfind("Nucleus")
    out = {}
    for line in text[idx:].splitlines()[1:]:
        m = re.match(r"\s*(\d+)\s+([A-Z][a-z]?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m:
            out[(int(m.group(1)), m.group(2))] = float(m.group(3))
        elif out and line.strip() and not line.strip().startswith("-"):
            break
    return out


def orca_tddft(path):
    """(energy_eV, wavelength_nm, oscillator_strength) from the last absorption table
    (ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS, ORCA 6 layout)."""
    lines = _last_block(Path(path).read_text(encoding="utf-8", errors="replace"),
                        "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS")
    return parse_tddft_rows(lines[1:])


def parse_tddft_rows(lines):
    """Parse ORCA 6 TD-DFT absorption rows such as
    '  0-1A  ->  1-1A    4.325874   34890.5   286.6   0.003830922 ...'."""
    out = []
    for line in lines:
        m = re.match(r"\s*\S+\s+->\s+\S+\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)", line)
        if m:
            out.append((float(m.group(1)), float(m.group(3)), float(m.group(4))))
        elif out and not line.strip():
            break
    return out


# ---------------------------------------------------------------- spectra and rates

def lorentzian(grid, centres, heights, fwhm):
    """Sum of Lorentzian lines on `grid` with peak heights `heights`."""
    g = np.zeros_like(grid, dtype=float)
    hw = fwhm / 2.0
    for c, h in zip(centres, heights):
        g += h * hw ** 2 / ((grid - c) ** 2 + hw ** 2)
    return g


def gaussian(grid, centres, heights, fwhm):
    """Sum of Gaussian lines on `grid` with peak heights `heights`."""
    g = np.zeros_like(grid, dtype=float)
    s = fwhm / (2.0 * math.sqrt(2.0 * math.log(2.0)))
    for c, h in zip(centres, heights):
        g += h * np.exp(-0.5 * ((grid - c) / s) ** 2)
    return g


def eyring(dG_kJmol, T=298.15):
    """Transition-state-theory rate constant in s-1 for a barrier in kJ/mol (kappa = 1)."""
    return KB * T / H_PLANCK * math.exp(-dG_kJmol * 1000.0 / (R_GAS * T))


def boltzmann(rel_kJmol, T=298.15, g=None):
    """Populations from relative energies (kJ/mol) and optional degeneracies."""
    e = np.asarray(rel_kJmol, dtype=float)
    w = np.exp(-e * 1000.0 / (R_GAS * T))
    if g is not None:
        w = w * np.asarray(g, dtype=float)
    return w / w.sum()


# ---------------------------------------------------------------- data

def read_csv(path):
    """Read a CSV file, skipping lines that start with '#'. Returns a list of dicts."""
    with open(path, encoding="utf-8", newline="") as fh:
        rows = [line for line in fh if not line.startswith("#")]
    return list(csv.DictReader(rows))


def experimental_fundamentals(molecule, path=HERE / "exp_fundamentals.csv"):
    """Experimental fundamentals of one molecule, each repeated by its degeneracy, sorted."""
    vals = []
    for r in read_csv(path):
        if r["molecule"] == molecule:
            vals += [float(r["wavenumber_cm1"])] * int(r["degeneracy"])
    return sorted(vals)


def match_sorted(calc, exp):
    """Pair calculated and experimental wavenumbers by order (both sorted ascending).

    Good enough for small molecules whose modes do not cross; check the symmetry labels
    (lesson 20.6) before trusting it for anything larger."""
    calc, exp = sorted(calc), sorted(exp)
    if len(calc) != len(exp):
        raise ValueError(f"{len(calc)} calculated vs {len(exp)} experimental modes")
    return list(zip(calc, exp))


def best_scale(pairs):
    """Least-squares scale factor s minimising sum (s*calc - exp)^2."""
    c = np.array([p[0] for p in pairs])
    e = np.array([p[1] for p in pairs])
    return float(c @ e / (c @ c))


def rms(pairs, s=1.0):
    c = np.array([p[0] for p in pairs])
    e = np.array([p[1] for p in pairs])
    return float(np.sqrt(np.mean((s * c - e) ** 2)))


if __name__ == "__main__":
    # small self-test of the pure-Python parts (no xtb or ORCA needed)
    assert abs(eyring(80.0) - 0.0600) < 0.001
    row = "  0-1A  ->  1-1A    4.325874   34890.5   286.6   0.003830922   0.03615   0.19012   0.00000   0.00000"
    assert parse_tddft_rows([row]) == [(4.325874, 286.6, 0.003830922)]
    p = match_sorted([1600, 3800, 3900], experimental_fundamentals("H2O"))
    print("comp31 self-test passed; scale for that toy set =", round(best_scale(p), 4))
    print("xtb found at:", find_xtb())
