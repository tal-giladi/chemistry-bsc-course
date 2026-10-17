"""Generate the Module 23 example data (seeded). Every file is realistic but NOT measured: the true values
below are what a correct analysis should recover, within the noise. Run: py make_data.py

Sources for the model values (all checked 2026-10-17):
- CODATA 2022 constants (pc23.py).
- Formation enthalpies: OpenStax Chemistry 2e, Appendix G; NaHCO3(s) -950.8 kJ/mol (lesson 08.7).
- Citric acid ionisation enthalpies +4.07, +2.23, -3.38 kJ/mol: Goldberg, Kishore and Lennen,
  J. Phys. Chem. Ref. Data 31, 231 (2002), table 7.22.
- CO2 solution enthalpy about -20 kJ/mol from NIST WebBook Henry's law, d(ln kH)/d(1/T) = 2400 K.
- Surface tension of water: IAPWS R1-76(2014).
- FeSCN2+ (K = 140, eps*b = 4600 L/mol at 447 nm) and the dye/bleach rate constants are illustrative
  values of the size teaching labs report, not literature constants.
"""
import csv
import numpy as np

from pc23 import HERE, K_B, R, F, C_WATER, linear_to_srgb

rng = np.random.default_rng(23)


def write(name, header, rows):
    with open(HERE / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows), "rows")


# ---------- 23.1 gases ----------
T_SIM, M_AR = 300.0, 39.948e-3          # K, kg/mol (argon)
m = M_AR / 6.02214076e23
v = np.linalg.norm(rng.normal(0, np.sqrt(K_B * T_SIM / m), size=(3000, 3)), axis=1)
write("md_speeds_example.csv", ["speed_m_s"], [[f"{x:.1f}"] for x in v])

GAMMA = 1.400
rows = []
for trial in range(1, 9):
    h1 = rng.uniform(12, 18)
    h2 = h1 * (1 - 1 / GAMMA) + rng.normal(0, 0.15)
    rows.append([trial, f"{h1 + rng.normal(0, 0.05):.1f}", f"{h2:.1f}"])
write("clement_desormes_example.csv", ["trial", "h1_cm", "h2_cm"], rows)

# ---------- 23.2 calorimetry ----------
C_CAL = 35.0                              # J/K, cup + lid + probe
T_MIX = 180


def run(name, T0, dT, drift_pre=0.0004, drift_post=0.0006, mix_time=60):
    out = []
    for t in range(0, 631, 30):
        if t <= T_MIX:
            T = T0 + drift_pre * t
        else:
            frac = min(1.0, (t - T_MIX) / mix_time)
            T = T0 + drift_pre * T_MIX + dT * frac + drift_post * (t - T_MIX)
        out.append([name, t, f"{T + rng.normal(0, 0.02):.1f}"])
    return out


rows = []
# calibration: 100.0 g at 21.0 C + 50.0 g at 45.0 C, 0.4 K lost while pouring (as in 08.7)
m_c, m_h, T_c, T_h = 100.0, 50.0, 21.0, 45.0 - 0.4
Tf = (m_h * C_WATER * T_h + (m_c * C_WATER + C_CAL) * T_c) / ((m_c + m_h) * C_WATER + C_CAL)
rows += run("calibration", T_c, Tf - T_c, mix_time=30)
# reaction: 4.00 g citric acid already dissolved in 100.0 g water, then 3.00 g NaHCO3
n_b = 3.00 / 84.007
f_gas = 0.92
DH_GAS = 34.7                              # kJ/mol NaHCO3, Hess value with all CO2 escaping
dh_obs = DH_GAS - (1 - f_gas) * 19.9
C_tot = 104.0 * C_WATER + C_CAL + 3.00 * 1.0
rows += run("reaction", 21.4, -n_b * dh_obs * 1000 / C_tot, mix_time=90)
# NaCl 5.00 g, +3.9 kJ/mol ; Epsom salt 10.00 g, +14 kJ/mol
rows += run("nacl", 21.6, -(5.00 / 58.44) * 3900 / (100 * C_WATER + C_CAL + 5.00 * 0.86), mix_time=90)
rows += run("epsom", 21.5, -(10.00 / 246.47) * 14000 / (100 * C_WATER + C_CAL + 10.0 * 1.5), mix_time=120)
write("calorimetry_example.csv", ["run", "t_s", "T_C"], rows)
mass_loss = n_b * f_gas * 44.009
print(f"  reaction: observed dH {dh_obs:.1f} kJ/mol, CO2 escaped {f_gas:.0%}, mass loss {mass_loss:.2f} g")

# ---------- 23.3 FeSCN2+ ----------
K, EB = 140.0, 4600.0


def complex_conc(fe0, scn0):
    # K = x / ((fe0 - x)(scn0 - x)) -> K x^2 - (K(fe0 + scn0) + 1) x + K fe0 scn0 = 0
    b = K * (fe0 + scn0) + 1
    return (b - np.sqrt(b * b - 4 * K * K * fe0 * scn0)) / (2 * K)


rows = []
for scn0 in [0, 4e-5, 8e-5, 1.2e-4, 1.6e-4, 2.0e-4]:
    a = EB * complex_conc(0.200, scn0) + rng.normal(0, 0.003)
    rows.append(["standard", "0.200", f"{scn0:.2e}", f"{a:.3f}"])
for scn0 in [2e-4, 4e-4, 6e-4, 8e-4, 1.0e-3]:
    a = EB * complex_conc(1.00e-3, scn0) + rng.normal(0, 0.003)
    rows.append(["mix", "1.00e-3", f"{scn0:.2e}", f"{a:.3f}"])
for x in np.arange(0.1, 0.95, 0.1):
    fe0, scn0 = 2.0e-3 * x, 2.0e-3 * (1 - x)
    a = EB * complex_conc(fe0, scn0) + rng.normal(0, 0.003)
    rows.append(["job", f"{fe0:.2e}", f"{scn0:.2e}", f"{a:.3f}"])
write("fescn_example.csv", ["type", "Fe0_M", "SCN0_M", "A447"], rows)

# ---------- 23.4 dye fading ----------
EA = 50e3
k_ref = 0.0030                             # 1/s at 2.0 mL bleach per 200 mL, 20 C
runs = [("A", 20.0, 2.0), ("B", 20.0, 4.0), ("C", 30.0, 2.0)]
rows = []
for name, T, vb in runs:
    k = k_ref * (vb / 2.0) * np.exp(-EA / R * (1 / (T + 273.15) - 1 / 293.15))
    I_blank = 0.80 * (1 + rng.normal(0, 0.004))
    for rep in range(2):
        r, g, b = linear_to_srgb([I_blank * (1 + rng.normal(0, 0.003)), 0.78, 0.82])
        rows.append([name, "blank", T, vb, "", f"{r:.1f}", f"{g:.1f}", f"{b:.1f}"])
    for t in range(0, 901, 30):
        A = 0.60 * np.exp(-k * t) + 0.012
        I = I_blank * 10 ** (-A) * (1 + rng.normal(0, 0.004))
        Ib = 0.82 * 10 ** (-0.15 * A)
        r, g, b = linear_to_srgb([I, 0.78 * 10 ** (-0.35 * A), Ib])
        rows.append([name, "sample", T, vb, t, f"{r:.1f}", f"{g:.1f}", f"{b:.1f}"])
    print(f"  dye run {name}: true k' = {k:.5f} 1/s, half-life {np.log(2) / k / 60:.1f} min")
write("dye_fading_example.csv", ["run", "type", "T_C", "bleach_mL", "t_s", "R", "G", "B"], rows)

# ---------- 23.5 cells ----------
cells = {"lemon": (0.93, 1800.0), "salt5": (0.78, 420.0), "vinegar": (0.95, 950.0)}
rows = []
for name, (E, r) in cells.items():
    for Rl in [100, 220, 470, 1000, 2200, 4700, 10000]:
        V = E * Rl / (Rl + r) + rng.normal(0, 0.004)
        rows.append([name, Rl, f"{V:.3f}"])
    rows.append([name, "open", f"{E + rng.normal(0, 0.003):.3f}"])
write("cells_example.csv", ["cell", "R_ohm", "V_V"], rows)

T = 298.15
rows = []
for c in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]:
    E = 1.099 + 0.004 + (R * T / (2 * F)) * np.log(c / 0.100) + rng.normal(0, 0.0008)
    rows.append([f"{c:.1e}", f"{E:.4f}"])
write("nernst_example.csv", ["c_Cu_M", "E_V"], rows)

# ---------- 23.6 surface tension ----------
T6 = 21.0 + 273.15
tau = 1 - T6 / 647.096
G_W = 235.8 * tau ** 1.256 * (1 - 0.625 * tau)   # mN/m, IAPWS
CMC, A_SZ, B_SZ = 1.5, 12.0, 0.05


def gamma(c):
    return G_W - A_SZ * np.log(1 + min(c, CMC) / B_SZ)


k_drop = 0.0500 / G_W                       # g per drop per (mN/m)
rows = []
for c in [0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]:
    for trial in range(1, 4):
        m20 = 20 * k_drop * gamma(c) * (1 + rng.normal(0, 0.006)) + rng.normal(0, 0.005)
        rows.append([c, trial, 20, f"{m20:.3f}"])
write("drops_example.csv", ["c_mL_per_L", "trial", "n_drops", "mass_g"], rows)
print(f"  water at 21 C: {G_W:.2f} mN/m; gamma at CMC {gamma(CMC):.1f} mN/m")
