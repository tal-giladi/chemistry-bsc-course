"""Lesson 08.4 hands-on, reference solution: predict the pH of kitchen liquids and the cabbage colour.

Run:   py lesson04_ph_solution.py
Constants: Ka at 25 C from OpenStax Chemistry 2e Appendix H (acetic acid 1.8e-5, H2CO3 4.3e-7,
HCO3- 4.7e-11); Kw = 1.0e-14. CO2 solubility 0.034 mol/(L bar) from Sander's compilation
(henrys-law.org, 3.3e-4 mol/(m3 Pa)). Cabbage colours: approximate, after the RHS colour chart.
"""
import math

KW = 1.0e-14
KA_ACETIC = 1.8e-5
KA1_CARBONIC = 4.3e-7
KA2_CARBONIC = 4.7e-11
KH_CO2 = 3.3e-4 * 1e5 / 1000      # mol/(L bar)
M_ACETIC = 60.052                 # g/mol
M_NAHCO3 = 84.006                 # g/mol

# approximate red-cabbage colours: (upper pH limit, colour)
CABBAGE = [(3.0, "red"), (5.0, "pink"), (6.5, "violet"), (7.5, "purple"),
           (9.0, "blue"), (12.0, "green"), (14.1, "yellow")]


def ph_strong_acid(c):
    """Fully dissociated monoprotic acid; fine for c above about 1e-6 mol/L."""
    return -math.log10(c)


def ph_weak_acid(c, ka):
    """Exact for a weak monoprotic acid (water ignored): x^2 / (c - x) = Ka, solve the quadratic."""
    x = (-ka + math.sqrt(ka * ka + 4 * ka * c)) / 2
    return -math.log10(x)


def ph_buffer(ka, n_acid, n_base):
    """Henderson-Hasselbalch: pH = pKa + log10(base / acid)."""
    return -math.log10(ka) + math.log10(n_base / n_acid)


def ph_amphiprotic(ka1, ka2):
    """A solution of HA- (like NaHCO3) when it is not too dilute: pH = (pKa1 + pKa2) / 2."""
    return (-math.log10(ka1) - math.log10(ka2)) / 2


def cabbage_colour(ph):
    for limit, colour in CABBAGE:
        if ph < limit:
            return colour
    return CABBAGE[-1][1]


def main():
    c_vinegar = 50.0 / M_ACETIC          # 5 % acidity = 50 g acetic acid per litre
    co2_ppm = 425                        # outdoor air, 2026 (about 0.042 %)
    c_h2co3 = KH_CO2 * co2_ppm * 1e-6    # dissolved CO2 in water open to air, mol/L
    n_acid = 10 * c_vinegar / 1000       # mol acetic acid in 10 mL vinegar
    n_soda = 0.35 / M_NAHCO3             # 0.35 g baking soda neutralises about half of it

    cases = [
        ("0.010 M HCl (strong acid)", ph_strong_acid(0.010)),
        (f"vinegar, 5 % ({c_vinegar:.3f} M acetic acid)", ph_weak_acid(c_vinegar, KA_ACETIC)),
        ("vinegar diluted 1:10", ph_weak_acid(c_vinegar / 10, KA_ACETIC)),
        ("water open to air (CO2 only)", ph_weak_acid(c_h2co3, KA1_CARBONIC)),
        ("baking soda solution", ph_amphiprotic(KA1_CARBONIC, KA2_CARBONIC)),
        ("10 mL vinegar + 0.35 g baking soda", ph_buffer(KA_ACETIC, n_acid - n_soda, n_soda)),
    ]
    print(f"{'solution':<40}{'pH':>6}  cabbage colour")
    for name, ph in cases:
        print(f"{name:<40}{ph:6.2f}  {cabbage_colour(ph)}")

    x = 10 ** -cases[1][1]
    print(f"\nsmall-x check for vinegar: x = {x:.2e} M is {100 * x / c_vinegar:.2f} % of c")
    print(f"percent ionised: 5 % vinegar {100 * x / c_vinegar:.2f} %, "
          f"diluted 1:10 {100 * 10 ** -cases[2][1] / (c_vinegar / 10):.2f} %")


if __name__ == "__main__":
    main()
