# Module 31 labs — Computational Chemistry Lab

Real quantum-chemistry runs on your own laptop with three free programs: Avogadro (build and look at molecules), xtb (fast semiempirical GFN2-xTB calculations) and ORCA (Hartree–Fock, DFT, TD-DFT and NMR). Every run in this module takes seconds to a few minutes. The folder holds small input files, Python helpers, exercises with TODOs and their `*_solution.py` reference solutions, and short excerpts of the expected output. It does not hold the programs themselves: you download them from their official sites, and ORCA's licence forbids anyone else from passing it on.

## Versions pinned for this module (checked 2026-10-17)

| Program | Version | Released | Licence | Official download |
|---|---|---|---|---|
| Avogadro | 2.0.0 | 2026-04-01 | BSD-3-Clause, free | https://avogadro.cc/install/ (installers also on https://github.com/OpenChemistry/avogadrolibs/releases/tag/2.0.0) |
| xtb | 6.7.1 | 2024-07-23 (still the latest release) | LGPL-3.0, free | https://github.com/grimme-lab/xtb/releases/tag/v6.7.1 |
| ORCA | 6.1.1 | announced 2025-12-09 | free for academic and private use under the ORCA EULA (version June 2025); commercial use needs a FACCTs licence | https://orcaforum.kofo.mpg.de/ (free registration) |
| Python and packages | 3.14 with `labs/common/requirements.txt` (numpy, scipy, matplotlib, RDKit 2026.9.1) | — | open source | https://www.python.org/downloads/ |

Optional, not needed for the lessons: CREST 3.0.2 (2024-08-25, conformer search on top of xtb, LGPL-3.0, Linux builds only: https://github.com/crest-lab/crest/releases).

Notes on the versions:

- The Windows asset of the xtb 6.7.1 release is named `xtb-6.7.1pre-windows-x86_64.zip`, and the program prints `xtb version 6.7.1pre (5071a88)`. It is the build attached to the official v6.7.1 release. SHA-256 of the zip, as published next to it: `043e578da4a7e114a4d584972959a875e3ffb9f2767a86723b95aa6719d28d9c`. Do not use the "bleed" release: its own notes say it is only minimally tested.
- ORCA ships its own copy of xtb (called `otool_xtb`) for the `! XTB2` keyword; you still install the stand-alone xtb for the xtb exercises.
- Newer versions will appear. The ideas in the lessons will not change; keywords and output layouts sometimes do. If your version differs, note it in your lab notebook and compare with the expected excerpts in `expected/`.

## The ORCA licence in plain words

Read the EULA yourself when you download ORCA; this is a summary, not legal advice. Checked 2026-10-17 against the June 2025 EULA text.

- ORCA is free of charge, but you may use it only for academic purposes at a school, college, university or Max Planck institute, or for private use: one person, non-commercial and not related to your work. The EULA expressly excludes people whose work could benefit from using it.
- If you study with this course as a private learner, that is private use. If you work for a company (chemistry or not) and the calculations could help your job, you need a commercial licence from FACCTs (https://www.faccts.de/orca/).
- You may not give, upload or share the ORCA program with anyone. That is why this course ships only input files. Your output files are "data" under the EULA: sharing them for academic purposes and publishing results in a journal are allowed; feeding them into commercial databases or non-academic machine learning is not.
- If you publish results, cite F. Neese, "Software Update: The ORCA Program System — Version 6.0", WIREs Comput. Mol. Sci. 15, e70019 (2025), doi:10.1002/wcms.70019, plus the papers for the methods you used (the manual lists them).

## Installing

Allow about 45 minutes the first time. You need about 2 GB of disk (ORCA is the largest part) and an internet connection for the downloads.

### Windows 10 or 11

1. Avogadro: download `Avogadro2-2.0.0-win64.exe` from https://avogadro.cc/install/ and run it. Windows SmartScreen may warn about a downloaded installer; check that it came from avogadro.cc or the OpenChemistry GitHub page before you allow it.
2. xtb: download `xtb-6.7.1pre-windows-x86_64.zip` from the v6.7.1 release page and unzip it to a folder without spaces, for example `C:\chem\xtb-6.7.1`. Then tell the labs where it is, in PowerShell:

   ```powershell
   setx XTB "C:\chem\xtb-6.7.1\bin\xtb.exe"
   ```

   Open a new terminal and check with `& $env:XTB --version`. You can also add `C:\chem\xtb-6.7.1\bin` to your PATH instead.
3. ORCA: register on https://orcaforum.kofo.mpg.de/, confirm the e-mail, accept the EULA in the Downloads section and download the ORCA 6.1.1 Windows 64-bit installer (`.exe` inside a zip). Run it with the "Typical" setup (serial programs only, which is all this module needs). It installs to `C:\Orca_6.1.1` or similar and sets PATH and ORCADIR. Open a new terminal and run `orca` with no arguments: it should print a short usage message.
4. Python: follow the setup below.

### macOS (Apple silicon or Intel)

1. Avogadro: download the `.dmg` for your Mac (`Avogadro2-2.0.0-Darwin-arm64.dmg` for Apple silicon, `Avogadro2-2.0.0-Darwin.dmg` for Intel) and drag Avogadro to Applications. If macOS refuses to open it the first time, right-click the app, choose Open, and confirm.
2. xtb: the GitHub release has no macOS binary. Use either conda-forge (has 6.7.1 for `osx-arm64` and `osx-64`):

   ```bash
   conda create -n xtb -c conda-forge xtb=6.7.1
   conda activate xtb
   ```

   or Homebrew with the Grimme lab tap (builds 6.7.1 from source):

   ```bash
   brew tap grimme-lab/qc
   brew install xtb
   ```

3. ORCA: from the forum's Downloads section take the macOS installer for your processor (a `.run` file; the forum lists separate builds for ARM64 and x86-64). Then:

   ```bash
   chmod a+x orca_6_1_1_*.run
   ./orca_6_1_1_*.run
   ```

   The installer puts ORCA in your home folder and adds it to PATH; open a new terminal and type `which orca`.

### Linux (x86-64)

1. Avogadro: `Avogadro2-x86_64.AppImage` from the install page (`chmod +x Avogadro2-x86_64.AppImage`, then run it), or Flathub: `flatpak install flathub org.openchemistry.Avogadro2`.
2. xtb: download and unpack the release tarball, or use conda-forge as on macOS:

   ```bash
   tar -xf xtb-6.7.1-linux-x86_64.tar.xz
   ls                                        # note the unpacked folder that contains bin/xtb
   export PATH="$PWD/<that folder>/bin:$PATH"
   xtb --version
   ```

   Put the `export` line in `~/.bashrc` to keep it.
3. ORCA: the Linux `.run` installer from the forum (`chmod a+x`, run it; add `-- -p /your/path` to choose the folder). The installer adds ORCA to PATH.

### All systems: thread and stack settings for xtb

xtb runs in parallel with OpenMP. For the small molecules here two threads are plenty, and the helpers in `comp31.py` set `OMP_NUM_THREADS=2` and `OMP_STACKSIZE=1G` for you. When you run xtb by hand on Linux or macOS, also lift the stack limit to avoid crashes on bigger molecules:

```bash
ulimit -s unlimited
export OMP_NUM_THREADS=2 OMP_STACKSIZE=1G
```

### Python setup

Once, from the repository root (Python 3.14, packages pinned in `labs/common/requirements.txt`):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. Run every script from this folder, for example `py check_setup.py`. Results go to `runs/` (ignored by git).

## What is in this folder

| Lesson | What you run | Exercise | Solution |
|---|---|---|---|
| 31.1 Setup | `check_setup.py` (xtb water optimisation + frequencies), `orca/01_water_r2scan3c.inp` | — | expected output in `expected/31.1_*.txt` |
| 31.2 Conformers | xtb butane scan (`xtb/butane_scan.inp`), RDKit + xtb pentane search | `lesson02_conformers.py` | `lesson02_conformers_solution.py` |
| 31.3 HF and DFT | `orca/03_water_*.inp`, `orca/03_acetone_xtb2_check.inp` | `lesson03_geometry.py` | `lesson03_geometry_solution.py` |
| 31.4 IR and NMR | `orca/04_formaldehyde_ir.inp`, `orca/04_{acetone,tms}_{opt,nmr}.inp` | `lesson04_spectra.py` | `lesson04_spectra_solution.py` |
| 31.5 Barriers | xtb NH3 and ethane (inside the script), `orca/05_nh3_{min,ts}.inp`, `orca/05_hcn_hnc_nebts.inp` | `lesson05_barriers.py` | `lesson05_barriers_solution.py` |
| 31.6 TD-DFT | `lesson06_uvvis.py` (xtb geometries), `orca/06_{butadiene,hexatriene,octatetraene}_tddft.inp`, `orca/06_formaldehyde_tddft.inp` | `lesson06_uvvis.py` | `lesson06_uvvis_solution.py` |
| 31.6 Module practical | xtb inside the script, `orca/06_ir_*.inp` (six molecules) | `lesson06_practical.py` | `lesson06_practical_solution.py` |

Other files:

- `comp31.py` — helpers: find and run xtb, read xyz files, xtb scan logs and `vibspectrum`, read the ORCA 6.1 tables (final energy, frequencies, IR spectrum, NMR shieldings, TD-DFT absorption), Lorentzian and Gaussian broadening, Eyring and Boltzmann. `py comp31.py` runs a self-test.
- `molecules/` — start geometries (xyz). Most were built with RDKit (ETKDG + MMFF94) and are deliberately not optimised; `ammonia_planar.xyz` and `ethane_eclipsed.xyz` are symmetric transition-state guesses; `hnc.xyz` is a hand-built linear guess.
- `exp_fundamentals.csv` — measured gas-phase fundamentals and IR intensities of the six practical molecules.
- `reference_water.csv` — water geometry, energy and harmonic frequencies at HF and B3LYP (def2-SVP, def2-TZVP), GFN2-xTB and experiment.
- `polyenes_uv.csv` — measured λmax of the polyenes and the reference TD-DFT values.
- `expected/` — short excerpts of what the scripts printed when this module was tested.

## How this module was tested (2026-10-17)

- All xtb commands and every Python script were run on Windows 11 with xtb 6.7.1pre (the official v6.7.1 Windows build), Python 3.14.3, RDKit 2026.9.1 and numpy 2.5. Their printed results are in `expected/` and in the lessons.
- ORCA was not run: it needs a personal forum registration and acceptance of the EULA, which the course author cannot do for you. The ORCA inputs follow the ORCA 6.1 manual, and the ORCA parsers in `comp31.py` follow the output layouts printed in that manual, but neither was run against a real ORCA 6.1.1 installation. If ORCA reports an input error, check the keyword in the manual (https://www.faccts.de/docs/orca/6.1/manual/) and tell us.
- To give you numbers to check the ORCA runs against, the same methods and basis sets were run with the open-source program PySCF 2.14.0 (water HF and B3LYP in `reference_water.csv`; CAM-B3LYP TD-DFT of the polyenes in `polyenes_uv.csv`). ORCA and PySCF use different integration grids and default settings, so expect agreement to about 0.002 Å, 0.3°, 10 cm⁻¹ and 0.02 eV, not to every digit.

## Data and sources

- Vibrational fundamentals, IR intensities and the experimental geometry of water: NIST Computational Chemistry Comparison and Benchmark Database (CCCBDB), https://cccbdb.nist.gov/ (experimental vibrations pages for each CAS number; frequencies mostly from T. Shimanouchi, NSRDS-NBS 39, 1972), retrieved 2026-10-17. US government work.
- Acetone NMR shifts in CDCl3 (13C 207.07 and 30.92 ppm, 1H 2.17 ppm): G. R. Fulmer et al., Organometallics 29, 2176 (2010), doi:10.1021/om100106e.
- Polyene λmax (butadiene 217 nm, hexatriene 258 nm, octatetraene 290 nm): OpenStax Organic Chemistry, 14.8 Interpreting Ultraviolet Spectra: The Effect of Conjugation, https://openstax.org/books/organic-chemistry/pages/14-8-interpreting-ultraviolet-spectra-the-effect-of-conjugation.
- Barriers: ammonia inversion about 24.2 kJ/mol (effective barrier 2021 ± 20 cm⁻¹ as summarised by A. R. Al Derzi et al., J. Quant. Spectrosc. Radiat. Transf. 161, 117 (2015), doi:10.1016/j.jqsrt.2015.03.034), ethane rotation 12 kJ/mol (OpenStax Organic Chemistry 3.6, used in lesson 15.2).
- Methods: GFN2-xTB, C. Bannwarth, S. Ehlert and S. Grimme, J. Chem. Theory Comput. 15, 1652 (2019), doi:10.1021/acs.jctc.8b01176; r2SCAN-3c, S. Grimme et al., J. Chem. Phys. 154, 064103 (2021), doi:10.1063/5.0040021; Avogadro, M. D. Hanwell et al., J. Cheminform. 4, 17 (2012), doi:10.1186/1758-2946-4-17.
