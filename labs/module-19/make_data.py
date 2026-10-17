"""Regenerates the simulated CSV files for the Module 19 labs (fixed random seed, so the output is
always the same). You do not need to run this; the CSV files are already in the folder.
    py make_data.py
Every data set here is simulated from the equations taught in the lessons, with realistic noise.
No database records are copied.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(19)


def write(name, header, rows, comment):
    lines = [f"# {comment}", header] + [",".join(str(x) for x in r) for r in rows]
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", name)


# 19.1 UV-Vis: blue dye standards on a spectrometer with 0.40 % stray light, 1 cm cell
a_true, stray = 0.160, 0.0040            # absorptivity in L mg-1 cm-1, stray-light fraction
rows = []
for c in [0, 1, 2, 4, 6, 8, 10, 12, 15, 20]:
    T = 10 ** (-a_true * c)
    A = -np.log10((T + stray) / (1 + stray)) + rng.normal(0, 0.002)
    rows.append(("standard", c, f"{A:.4f}"))
for A_true in [a_true * 64.0, a_true * 3.20]:   # sports drink undiluted and diluted 1 + 19
    T = 10 ** (-A_true)
    for _ in range(3):
        A = -np.log10((T + stray) / (1 + stray)) + rng.normal(0, 0.002)
        rows.append(("undiluted" if A_true > 5 else "diluted_1to20", "", f"{A:.4f}"))
write("dye_uvvis.csv", "type,c_mg_per_L,absorbance", rows,
      "simulated: blue food dye at 630 nm, 1 cm cell, 0.40 % stray light; sample = sports drink (true 64.0 mg/L)")

# 19.2 Fluorescence: quinine 10 mg/L in 0.05 M H2SO4 quenched by chloride, Stern-Volmer K = 130 L/mol
K_sv = 130.0
rows = []
for cl_mM in [0, 2, 4, 6, 8, 10, 15, 20]:
    F = 1000 / (1 + K_sv * cl_mM / 1000) * (1 + rng.normal(0, 0.006))
    rows.append((cl_mM, f"{F:.1f}"))
write("quinine_chloride.csv", "chloride_mM,fluorescence", rows,
      "simulated: quinine 10 mg/L, excitation 350 nm, emission 450 nm, chloride added as NaCl")

# 19.3 van Deemter for a packed GC column (H in mm, u in cm/s)
A, B, C = 0.35, 6.0, 0.040
rows = []
for u in [2, 3, 4, 6, 8, 10, 12, 15, 20, 25, 30, 40]:
    H = (A + B / u + C * u) * (1 + rng.normal(0, 0.02))
    rows.append((u, f"{H:.3f}"))
write("vandeemter_gc.csv", "u_cm_per_s,H_mm", rows,
      "simulated: packed GC column 2 m, N2 carrier; H = A + B/u + C u with A=0.35 mm, B=6.0 mm cm/s, C=0.040 mm s/cm")

# 19.4 GC retention times (min) on two columns, temperature programme 60 C then 3 K/min
def times(ri_list, t_alk):
    out = []
    for name, ri in ri_list:
        n = int(ri // 100)
        f = (ri - 100 * n) / 100
        out.append((name, round(t_alk[n] + f * (t_alk[n + 1] - t_alk[n]) + rng.normal(0, 0.004), 3)))
    return out

alk5 = {9: 8.20, 10: 10.95, 11: 13.60, 12: 16.12}
alkw = {10: 4.10, 11: 6.05, 12: 8.30, 13: 10.70, 14: 13.10, 15: 15.45, 16: 17.70}
rows = [("DB-5", f"C{n}", t) for n, t in alk5.items()]
rows += [("DB-5", nm, t) for nm, t in times([("peak_X", 1031), ("peak_Y", 1098)], alk5)]
rows += [("DB-Wax", f"C{n}", t) for n, t in alkw.items()]
rows += [("DB-Wax", nm, t) for nm, t in times([("peak_X", 1196), ("peak_Y", 1552)], alkw)]
write("gc_retention.csv", "column,peak,t_min", rows,
      "simulated: citrus-oil run, 30 m columns, He, 60 C then 3 K/min; X and Y placed at NIST WebBook indices")

# 19.4 GC-FID internal standard: ethanol in hand sanitizer, 1-butanol internal standard 0.50 % v/v
rf = 0.62                          # area ratio per (conc ratio); FID responds less to ethanol per volume
rows = []
for c in [0.20, 0.40, 0.60, 0.80, 1.00]:
    for _ in range(2):
        ratio = rf * c / 0.50 * (1 + rng.normal(0, 0.008)) + 0.002
        drift = rng.uniform(0.85, 1.15)          # injection volume varies, both peaks scale together
        area_is = 52000 * drift
        rows.append(("standard", c, round(ratio * area_is), round(area_is)))
for _ in range(3):
    ratio = rf * 0.684 / 0.50 * (1 + rng.normal(0, 0.008)) + 0.002
    drift = rng.uniform(0.85, 1.15)
    area_is = 52000 * drift
    rows.append(("sample_1to100", "", round(ratio * area_is), round(area_is)))
write("sanitizer_gc_is.csv", "type,ethanol_percent_v_v,area_ethanol,area_is", rows,
      "simulated: GC-FID, every vial holds 0.50 % v/v 1-butanol; sample diluted 1 + 99 (true product 68.4 % v/v)")


# 19.5 cyclic voltammetry: ferricyanide 2.0 mM in 0.1 M KCl, 3 mm disc, finite-difference simulation
F, R, Tk = 96485.33212, 8.314462618, 298.15
f = F / (R * Tk)


def cv(v, C_bulk=2.0e-6, D=7.2e-6, area=0.0707, E0=0.220, k0=0.02, alpha=0.5,
       E_start=0.50, E_turn=-0.10, dE=0.0005, Cdl=20e-6):
    """Return E (V) and i (A, IUPAC sign: oxidation positive) for O + e- = R, Butler-Volmer kinetics."""
    E = np.concatenate([np.arange(E_start, E_turn, -dE), np.arange(E_turn, E_start + dE / 2, dE)])
    dt = dE / v
    t_total = dt * E.size
    dx = np.sqrt(D * dt / 0.45)
    nx = int(6 * np.sqrt(D * t_total) / dx) + 2
    O, Rr = np.full(nx, C_bulk), np.zeros(nx)
    lam = D * dt / dx ** 2
    cur = np.empty(E.size)
    for j, e in enumerate(E):
        kf = k0 * np.exp(-alpha * f * (e - E0))
        kb = k0 * np.exp((1 - alpha) * f * (e - E0))
        g = D / dx                                # second-order surface gradient, equal D for O and R
        S0 = (4 * (O[1] + Rr[1]) - (O[2] + Rr[2])) / 3
        O0 = (g / 2 * (4 * O[1] - O[2]) + kb * S0) / (1.5 * g + kf + kb)
        R0 = S0 - O0
        J = g / 2 * (4 * O[1] - O[2] - 3 * O0)    # reduction flux, mol cm-2 s-1
        O[0], Rr[0] = O0, R0
        O[1:-1] += lam * (O[2:] - 2 * O[1:-1] + O[:-2])
        Rr[1:-1] += lam * (Rr[2:] - 2 * Rr[1:-1] + Rr[:-2])
        sign = -1 if j < E.size // 2 else 1
        cur[j] = -F * area * J + sign * Cdl * area * v
    return E, cur


rows = []
for v in [0.025, 0.05, 0.1, 0.2, 0.4]:
    E, i = cv(v)
    i = i + rng.normal(0, 0.05e-6, i.size)
    rows += [(v, f"{e:.4f}", f"{x * 1e6:.3f}") for e, x in zip(E[::4], i[::4])]
write("cv_ferricyanide.csv", "scan_rate_V_per_s,E_V,i_uA", rows,
      "simulated: 2.0 mM K3[Fe(CN)6] in 0.1 M KCl, 3 mm Pt disc (0.0707 cm2), Ag/AgCl reference, 25 C; i > 0 is oxidation")

# 19.5 module practical: caffeine in an energy drink by HPLC-UV (273 nm)
rows = []
for col, (A_, B_, C_) in {"C18_5um": (5.0, 8.0, 4.0), "C18_2.7um_coreshell": (2.5, 8.0, 1.2)}.items():
    for u in [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0]:
        H = (A_ + B_ / u + C_ * u) * (1 + rng.normal(0, 0.02))
        rows.append((col, u, f"{H:.2f}"))
write("hplc_vandeemter.csv", "column,u_mm_per_s,H_um", rows,
      "simulated: 100 x 4.6 mm C18 columns, water/methanol 70/30, caffeine peak")

rows = []
slope, icpt = 21.4, 1.1
for c in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
    rows.append(("blank", c, f"{icpt + rng.normal(0, 0.35):.2f}"))
for c in [2, 5, 10, 20, 30, 40, 50]:
    rows.append(("standard", c, f"{icpt + slope * c * (1 + rng.normal(0, 0.006)):.2f}"))
for _ in range(3):
    rows.append(("drink_1to10", "", f"{icpt + slope * 30.6 * (1 + rng.normal(0, 0.006)):.2f}"))
for add in [0, 5, 10, 15]:
    rows.append(("spike_recovery", add, f"{icpt + slope * (30.6 + add) * (1 + rng.normal(0, 0.006)):.2f}"))
write("caffeine_hplc.csv", "type,c_mg_per_L,peak_area", rows,
      "simulated: HPLC-UV 273 nm, caffeine standards; drink diluted 1 + 9 (true drink 306 mg/L, label 320 mg/L)")
