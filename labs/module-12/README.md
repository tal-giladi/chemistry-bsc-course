# Module 12 labs — Quantum Theory in Chemistry

Small Python exercises, one per lesson, built around one tool: a finite-difference solver for the one-dimensional Schrödinger equation. You write the solver yourself in lesson 12.2; `qm_solver.py` is the reference version that lessons 12.3–12.6 import. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs only need numpy, scipy and matplotlib.

Run each file from this folder, for example `py lesson02_box.py`. Keep `qm_solver.py` in the same folder.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 12.1 Classical physics fails | `lesson01_balmer.py` | `lesson01_balmer_solution.py` | `balmer_nist.csv` |
| 12.2 Particle in a box | `lesson02_box.py` | `lesson02_box_solution.py` | none |
| 12.3 Tunnelling | `lesson03_tunnel.py` | `lesson03_tunnel_solution.py` | none |
| 12.4 Oscillator and vibrations | `lesson04_vib.py` | `lesson04_vib_solution.py` | HCl constants in the code |
| 12.5 Rotors and hydrogen | `lesson05_rotor_h.py` | `lesson05_rotor_h_solution.py` | HCl constants in the code |
| 12.6 Module practical | `lesson06_practical.py` | `lesson06_practical_solution.py` | `cyanine_dyes.csv` |

Shared: `qm_solver.py` holds the CODATA 2022 constants, `solve(x, V, c, n_states)` (uses `scipy.linalg.eigh_tridiagonal`), `count_nodes` and a small CSV reader.

## Data

- `balmer_nist.csv`: air wavelengths of the four visible H I Balmer lines (strongest component) from the NIST Handbook of Basic Atomic Spectroscopic Data, hydrogen table 2, https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm, accessed 2026-10-17 (US government work).
- `cyanine_dyes.csv`: absorption maxima 309, 409 and 512 nm of three symmetric cyanine dyes, as given in LibreTexts, Zielinski et al., Quantum States of Atoms and Molecules, section 4.2 (data from Simpson, J. Chem. Phys. 1948), accessed 2026-10-17.
- Constants in the code: H35Cl spectroscopic constants from the NIST Chemistry WebBook (https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000); atomic masses from NIST; h, c, e exact SI values; electron mass, atomic mass constant, Bohr radius, hartree, Rydberg constant and proton-electron mass ratio from CODATA 2022; helium ionisation energy from the NIST Handbook; all accessed 2026-10-17.
- The ammonia double well in lesson 12.3 is an illustrative model (barrier 2020 cm⁻¹, minima at ±0.40 Å, effective masses 2.487 u and 4.22 u), not a fitted potential. The measured inversion frequencies it is compared with are 23.79 GHz (NH3) and 1.59 GHz (ND3).
