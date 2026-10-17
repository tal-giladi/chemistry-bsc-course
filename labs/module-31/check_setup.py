"""Lesson 31.1: check that xtb works and read your first calculation.

Run from this folder:  py check_setup.py
It finds xtb (PATH or the XTB environment variable), prints its version, optimises water with
GFN2-xTB and computes its frequencies (xtb --ohess), then prints the numbers the lesson asks for.
Everything is written to runs/31.1-water/ (ignored by git)."""
import subprocess
import comp31 as c

exe = c.find_xtb()
if exe is None:
    raise SystemExit("xtb not found. Put it on PATH or set XTB to the full path of xtb(.exe); see README.md.")
ver = subprocess.run([exe, "--version"], capture_output=True, text=True, errors="replace").stdout
print("xtb:", exe)
print([l.strip() for l in ver.splitlines() if "xtb version" in l][0])

work = c.RUNS / "31.1-water"
out = c.run_xtb(c.MOLECULES / "water.xyz", ["--ohess"], work, "water.out")
text = out.read_text(encoding="utf-8", errors="replace")
sym, x, _ = c.read_xyz(work / "xtbopt.xyz")
modes = c.vibrations(c.read_vibspectrum(work / "vibspectrum"))

print(f"optimisation converged : {'GEOMETRY OPTIMIZATION CONVERGED' in text}")
print(f"total energy           : {c.xtb_total_energy(out):.6f} Eh")
print(f"r(O-H)                 : {c.distance(x, 0, 1):.4f} and {c.distance(x, 0, 2):.4f} Angstrom")
print(f"angle H-O-H            : {c.angle(x, 1, 0, 2):.2f} degrees")
print("frequencies (cm-1)     :", ", ".join(f"{w:.1f}" for w, _, _ in modes))
print("IR intensity (km/mol)  :", ", ".join(f"{i:.1f}" for _, i, _ in modes))
imag = [w for w, _, _ in modes if w < 0]
print("imaginary frequencies  :", len(imag), "(0 means a true minimum)")
