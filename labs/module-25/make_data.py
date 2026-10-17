"""Regenerates the simulated CSV files for the Module 25 labs (fixed random seed, so the output is
always the same). You do not need to run this; the CSV files are already in the folder.
    py make_data.py
Every data set here is simulated from the equations taught in the lessons, with realistic noise.
No database records are copied. (The GC-MS run of Lesson 25.4 is built by get_nist_ms.py on your own
computer from spectra you download from the NIST WebBook; it is not in this folder.)
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(25)


def write(name, header, rows, comment):
    lines = [f"# {c}" for c in comment.split("\n")] + [header] + [",".join(str(x) for x in r) for r in rows]
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", name)


def gauss(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)


# ---------------------------------------------------------------- 25.1 phone spectrometer
# pixel -> wavelength of the simulated phone + DVD spectrometer (slightly curved, as real ones are)
px = np.arange(600)
lam_px = 390 + 0.52 * px + 6.0e-5 * px ** 2           # nm
grid = np.arange(350, 760, 0.1)                       # fine wavelength grid for the "true" optics
sig_inst = 2.5                                        # nm, instrument function (slit image) sigma


def to_pixels(spec_on_grid):
    """Blur a spectrum on the fine grid with the instrument function and sample it at the pixels."""
    kern_x = np.arange(-4 * sig_inst, 4 * sig_inst + 0.05, 0.1)
    kern = gauss(kern_x, 0, sig_inst)
    kern /= kern.sum()
    blurred = np.convolve(spec_on_grid, kern, mode="same")
    return np.interp(lam_px, grid, blurred)


# compact fluorescent lamp: Hg lines + Tb3+ and Eu3+ phosphor bands (NIST ASD wavelengths for Hg)
cfl = (3.0 * gauss(grid, 404.66, 0.3) + 6.0 * gauss(grid, 435.83, 0.3) + 8.0 * gauss(grid, 546.07, 0.3)
       + 1.5 * gauss(grid, 576.96, 0.3) + 1.5 * gauss(grid, 579.07, 0.3) + 0.25 * gauss(grid, 487.0, 3.0)
       + 0.35 * gauss(grid, 543.0, 2.5) + 3.0 * gauss(grid, 611.6, 1.0) + 0.04)
# white LED: blue die + yellow phosphor
led = 0.95 * gauss(grid, 450, 10) + 0.60 * gauss(grid, 565, 55) + 0.005

# relative absorbance spectra of the full-strength stock solutions in the cup (path about 5 cm)
A_blue = 1.20 * (gauss(grid, 630, 22) + 0.25 * gauss(grid, 585, 25) + 0.04 * gauss(grid, 410, 20))
A_yel = 1.00 * gauss(grid, 426, 30)
stray = 0.020                                          # fraction of light that bypasses the sample


def phone_reading(A_on_grid):
    T = 10 ** (-A_on_grid)
    I = to_pixels(led * T) + stray * to_pixels(led)
    return I * (1 + rng.normal(0, 0.003, px.size))


cols = {"pixel": px, "cfl": to_pixels(cfl) * (1 + rng.normal(0, 0.004, px.size)),
        "blank": phone_reading(0 * grid)}
for f in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    cols[f"blue_{f}"] = phone_reading(f * A_blue)
for f in [0.25, 0.5, 1.0]:
    cols[f"yellow_{f}"] = phone_reading(f * A_yel)
cols["green_unknown"] = phone_reading(0.35 * A_blue + 0.60 * A_yel)
names = list(cols)
rows = [[int(cols["pixel"][i])] + [f"{cols[n][i]:.5f}" for n in names[1:]] for i in range(px.size)]
write("phone_spectra_example.csv", ",".join(names), rows,
      "simulated: cardboard + DVD phone spectrometer, linear intensity (sRGB already undone), same framing for every photo\n"
      "cfl = compact fluorescent lamp (Hg 404.66, 435.83, 546.07 nm; Eu3+ 611.6 nm; Tb3+ bands); other columns = white LED through the cup\n"
      "blue_f / yellow_f = food-dye stock diluted to fraction f; green_unknown = 0.35 blue stock + 0.60 yellow stock (true values)\n"
      "true pixel->wavelength: 390 + 0.52 p + 6.0e-5 p^2 nm; instrument sigma 2.5 nm; stray light 2.0 %")

# ---------------------------------------------------------------- 25.2 quinine
# home: phone photos of tonic water under a 365 nm flashlight, side view; sRGB blue channel (0-255)
def encode_srgb(lin):
    lin = np.clip(lin, 0, 1)
    v = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)
    return np.round(255 * v, 1)


a_tonic = 1.0                                          # effective absorbance of the excitation path, full tonic
K_sv = 130.0                                           # L/mol, chloride
dark = 0.004                                           # linear background of the dark room
rows = []
for f in [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.0]:
    F = 0.55 * (1 - 10 ** (-a_tonic * f)) / (1 - 10 ** (-a_tonic))
    for rep in range(2):
        rows.append(("dilution", f, 0.0, encode_srgb(F * (1 + rng.normal(0, 0.02)) + dark), encode_srgb(dark + abs(rng.normal(0, 0.0005)))))
for salt_g in [0.0, 0.05, 0.1, 0.2, 0.4, 0.8]:
    cl = salt_g / 58.44 * 10                            # g per 100 mL -> mol/L
    F = 0.55 * (1 - 10 ** (-a_tonic * 0.125)) / (1 - 10 ** (-a_tonic)) / (1 + K_sv * cl)
    for rep in range(2):
        rows.append(("salt", 0.125, salt_g, encode_srgb(F * (1 + rng.normal(0, 0.02)) + dark), encode_srgb(dark + abs(rng.normal(0, 0.0005)))))
write("tonic_home_example.csv", "series,tonic_fraction,salt_g_per_100mL,blue_srgb,dark_srgb", rows,
      "simulated: tonic water (and water) in a clear glass, 365 nm UV flashlight from one side, phone at 90 degrees, exposure locked\n"
      "blue_srgb = mean blue value of the glowing region; dark_srgb = same-size region of the dark background\n"
      "model: F ~ 1 - 10^(-1.0 f) (inner filter), chloride quenching Stern-Volmer K = 130 L/mol")

# bench: fluorimeter, ex 350 nm / em 450 nm, 0.05 M H2SO4; tonic true 72.0 mg/L quinine
rows = []
for c in [0, 0.1, 0.2, 0.3, 0.4, 0.5]:
    rows.append(("external_std", c, f"{(3 + 1000 * c * (1 - 0.01 * c)) * (1 + rng.normal(0, 0.004)):.1f}"))
for _ in range(3):
    c = 72.0 / 200
    rows.append(("tonic_1to200", "", f"{(3 + 1000 * c * (1 - 0.01 * c)) * (1 + rng.normal(0, 0.004)):.1f}"))
for add in [0, 0.1, 0.2, 0.3, 0.4]:                   # 5.00 mL of 1:100 tonic + standard, made to 10.00 mL
    c = 72.0 / 200 + add
    rows.append(("std_addition", add, f"{(3 + 1000 * c * (1 - 0.01 * c)) * (1 + rng.normal(0, 0.004)) - 3:.1f}"))
write("quinine_fluorimeter.csv", "type,quinine_added_or_std_mg_per_L,fluorescence", rows,
      "simulated: fluorimeter, excitation 350 nm, emission 450 nm, 1 cm cell, 0.05 M H2SO4, 25 C; true tonic quinine 72.0 mg/L\n"
      "external_std: quinine (from quinine sulfate) standards; tonic_1to200: tonic diluted 1 + 199, read 3 times\n"
      "std_addition: 5.00 mL of tonic diluted 1 + 99, plus standard, made up to 10.00 mL; blank (3.0) already subtracted")

# ---------------------------------------------------------------- 25.3 flame AAS calcium
rows = []
def aas(c):
    return 0.0420 * c - 0.00045 * c ** 2 + rng.normal(0, 0.0015)
for c in [0, 1, 2, 4, 6, 8, 10]:
    rows.append(("standard_La", c, f"{aas(c):.4f}"))
true_ca, dil = 48.0, 10                                # mg/L in the water, diluted 1 + 9
for _ in range(3):
    rows.append(("water_1to10_noLa", "", f"{aas(true_ca / dil * 0.82):.4f}"))
for _ in range(3):
    rows.append(("water_1to10_La", "", f"{aas(true_ca / dil):.4f}"))
for _ in range(3):
    rows.append(("water_1to10_La_spike2", 2.0, f"{aas(true_ca / dil + 2.0):.4f}"))
for drift, when in [(1.000, "check_start"), (0.985, "check_middle"), (0.972, "check_end")]:
    rows.append((when, 5.0, f"{(0.0420 * 5 - 0.00045 * 25) * drift + rng.normal(0, 0.0015):.4f}"))
write("aas_calcium.csv", "type,c_mg_per_L,absorbance", rows,
      "simulated: flame AAS, Ca 422.7 nm, air-acetylene, 0.5 nm slit; standards and samples in 0.1 % La (as LaCl3) and 1 % HNO3\n"
      "mineral water true Ca 48.0 mg/L, diluted 1 + 9; without La the sulfate/phosphate matrix suppresses the signal by 18 %\n"
      "spike: diluted water + 2.0 mg/L Ca; check standard 5.0 mg/L read at start, middle and end of the run")

# ---------------------------------------------------------------- 25.4 GC alkane ladder (DB-5 type, 60 C + 3 K/min)
rows = [(f"C{n}", t) for n, t in [(8, 3.40), (9, 5.60), (10, 8.70), (11, 12.30), (12, 16.05), (13, 19.80), (14, 23.45)]]
write("gcms_alkanes.csv", "alkane,t_min", rows,
      "simulated: n-alkane ladder on a 30 m x 0.25 mm x 0.25 um 5 % phenyl column, He 1 mL/min, 60 C then 3 K/min")

# ---------------------------------------------------------------- 25.5 HPLC scouting and system suitability
lss = {"paracetamol": (0.90, 3.2), "caffeine": (1.30, 4.3), "aspirin": (2.10, 5.0), "salicylic acid": (2.30, 5.2)}
t0 = 1.00
rows = []
for phi in [0.20, 0.40]:
    for name, (lkw, S) in lss.items():
        k = 10 ** (lkw - S * phi)
        rows.append((name, phi, f"{t0 * (1 + k) * (1 + rng.normal(0, 0.003)):.3f}"))
write("hplc_scouting.csv", "compound,phi_MeCN,t_R_min", rows,
      "simulated: C18 150 x 4.6 mm, 5 um, 1.0 mL/min, 25 mM phosphate pH 2.5 / acetonitrile, 30 C, UV 230 nm; t0 = 1.00 min (uracil)\n"
      "true linear-solvent-strength parameters log kw, S: paracetamol 0.90, 3.2; caffeine 1.30, 4.3; aspirin 2.10, 5.0; salicylic acid 2.30, 5.2")

rows = []
for col, tail_sal, N_fac, area_rsd in [("new_column", 1.25, 1.0, 0.004), ("after_400_injections", 2.35, 0.55, 0.004)]:
    for inj in range(1, 7):
        for name, (lkw, S), area in zip(lss, lss.values(), [1520, 980, 2210, 340]):
            k = 10 ** (lkw - S * 0.25)
            tR = t0 * (1 + k) * (1 + rng.normal(0, 0.0015))
            N = 10000 * N_fac * (1 + rng.normal(0, 0.02))
            tail = (tail_sal if name == "salicylic acid" else 1.10) + rng.normal(0, 0.03)
            rows.append((col, inj, name, f"{tR:.3f}", f"{area * (1 + rng.normal(0, area_rsd)):.1f}", f"{N:.0f}", f"{tail:.2f}"))
write("hplc_sst.csv", "column_state,injection,compound,t_R_min,area,plates,tailing", rows,
      "simulated: six replicate injections of the system-suitability mix at 25 % acetonitrile, same column when new and after 400 injections")

# ---------------------------------------------------------------- 25.6 cyclic voltammetry, quasi-reversible couple
F, R, Tk = 96485.33212, 8.314462618, 298.15
f = F / (R * Tk)


def cv(v, C_bulk=1.0e-6, D=7.0e-6, area=0.0707, E0=0.220, k0=0.004, alpha=0.5,
       E_start=0.70, E_turn=-0.30, dE=0.0005, Cdl=20e-6):
    """E (V) and i (A, IUPAC sign: oxidation positive) for O + e- = R, Butler-Volmer kinetics,
    explicit finite differences, equal diffusion coefficients, start with only O present."""
    E = np.concatenate([np.arange(E_start, E_turn, -dE), np.arange(E_turn, E_start + dE / 2, dE)])
    dt = dE / v
    dx = np.sqrt(D * dt / 0.45)
    nx = int(6 * np.sqrt(D * dt * E.size) / dx) + 2
    O, Rr = np.full(nx, C_bulk), np.zeros(nx)
    lam = D * dt / dx ** 2
    cur = np.empty(E.size)
    for j, e in enumerate(E):
        kf = k0 * np.exp(-alpha * f * (e - E0))
        kb = k0 * np.exp((1 - alpha) * f * (e - E0))
        g = D / dx
        S0 = (4 * (O[1] + Rr[1]) - (O[2] + Rr[2])) / 3
        O0 = (g / 2 * (4 * O[1] - O[2]) + kb * S0) / (1.5 * g + kf + kb)
        J = g / 2 * (4 * O[1] - O[2] - 3 * O0)
        O[0], Rr[0] = O0, S0 - O0
        O[1:-1] += lam * (O[2:] - 2 * O[1:-1] + O[:-2])
        Rr[1:-1] += lam * (Rr[2:] - 2 * Rr[1:-1] + Rr[:-2])
        sign = -1 if j < E.size // 2 else 1
        cur[j] = -F * area * J + sign * Cdl * area * v
    return E, cur


if __name__ == "__main__":
    rows = []
    for v in [0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
        E, i = cv(v)
        i = i + rng.normal(0, 0.02e-6, i.size)
        rows += [(v, f"{e:.4f}", f"{x * 1e6:.4f}") for e, x in zip(E[::4], i[::4])]
    write("cv_quasi.csv", "scan_rate_V_per_s,E_V,i_uA", rows,
          "simulated: 1.0 mM redox couple O + e- = R in 0.5 M KCl, 3 mm glassy-carbon disc (0.0707 cm2), Ag/AgCl, 25 C; i > 0 is oxidation\n"
          "true: E0' = 0.220 V, k0 = 0.004 cm/s, alpha = 0.5, D = 7.0e-6 cm2/s, Cdl 20 uF/cm2, no uncompensated resistance")

    # ------------------------------------------------------------ 25.6 module practical: bitter-lemon dossier
    rows = []
    for c in [0, 2, 4, 6, 8, 10]:                       # tartrazine standards, 1 cm, 426 nm and 700 nm
        rows.append(("uv_std", c, f"{0.0530 * c + rng.normal(0, 0.0012):.4f}", f"{rng.normal(0, 0.0008):.4f}"))
    for _ in range(3):                                  # drink diluted 1 + 4; true tartrazine 24.0 mg/L; cloudy
        rows.append(("uv_drink_1to5", "", f"{0.0530 * 24.0 / 5 + 0.0347 + rng.normal(0, 0.0012):.4f}", f"{0.0300 + rng.normal(0, 0.0008):.4f}"))
    for c in [0, 0.1, 0.2, 0.3, 0.4, 0.5]:              # quinine external standards in 0.05 M H2SO4
        rows.append(("fl_std", c, f"{1000 * c * (1 + rng.normal(0, 0.004)):.1f}", ""))
    for add in [0, 0.2, 0.4, 0.6, 0.8]:                 # 5.00 mL of drink 1:50 + standard to 10.00 mL; matrix absorbs at 350 nm
        rows.append(("fl_std_addition", add, f"{0.88 * 1000 * (62.0 / 100 + add) * (1 + rng.normal(0, 0.004)):.1f}", ""))
    for add in [0, 2, 4, 6, 8]:                         # vitamin C: drink 1:10 in pH 4.0 acetate, standard additions in the cell
        rows.append(("cv_std_addition", add, f"{0.850 * (110.0 / 10 + add) + rng.normal(0, 0.06):.3f}", ""))
    write("practical_drink.csv", "type,x,signal,signal2", rows,
          "simulated: a cloudy bitter-lemon soft drink. Recipe/label: tartrazine 25 mg/L, quinine 'not more than 83 mg/L' (target 65), vitamin C 120 mg/L\n"
          "uv_std / uv_drink_1to5: x = tartrazine mg/L, signal = A(426 nm), signal2 = A(700 nm) baseline, 1 cm\n"
          "fl_std: x = quinine mg/L; fl_std_addition: 5.00 mL of drink diluted 1 + 49, plus x mg/L quinine, made to 10.00 mL\n"
          "cv_std_addition: drink diluted 1 + 9 in acetate buffer pH 4.0; x = ascorbic acid added in the cell (mg/L); signal = oxidation peak current (uA, baseline-corrected)\n"
          "true values: tartrazine 24.0, quinine 62.0, vitamin C 110 mg/L; the drink matrix absorbs 12 % of the excitation light")
