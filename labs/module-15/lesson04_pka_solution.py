"""Lesson 15.4 reference solution: which way does a proton transfer go?

Run (from this folder):
    py lesson04_pka_solution.py
"""
import math

from org15 import R_KJ, read_csv

TABLE = {r["acid"]: float(r["pKa"]) for r in read_csv("pka_table.csv")}
BASE_OF = {r["acid"]: r["conjugate_base"] for r in read_csv("pka_table.csv")}
ACID_OF = {v: k for k, v in BASE_OF.items()}

# (acid on the left, base on the left). The base is named by its own name in the table.
REACTIONS = [
    ("acetic acid", "hydroxide"),
    ("phenol", "hydroxide"),
    ("acetic acid", "hydrogen carbonate"),
    ("phenol", "hydrogen carbonate"),
    ("ethyne", "hydroxide"),
    ("ethyne", "amide"),
    ("acetone", "hydroxide"),
    ("ammonium", "hydroxide"),
    ("HCl", "H2O"),
]


def k_proton_transfer(pka_left_acid, pka_right_acid):
    """Equilibrium constant of  HA + B-  <=>  A- + HB.
    K = Ka(HA) / Ka(HB) = 10**(pKa(HB) - pKa(HA)). The side with the weaker acid (higher pKa) is favoured."""
    return 10 ** (pka_right_acid - pka_left_acid)


def delta_g_kj(k, T=298.15):
    """Standard Gibbs energy of reaction from K (08.3): dG = -RT ln K."""
    return -R_KJ * T * math.log(k)


def main():
    print(f"{'acid + base':<38}{'pKa(HA)':>8}{'pKa(HB)':>8}{'log K':>7}{'dG/kJ':>8}  verdict")
    for acid, base in REACTIONS:
        right_acid = ACID_OF[base]
        pa, pb = TABLE[acid], TABLE[right_acid]
        k = k_proton_transfer(pa, pb)
        verdict = "lies to the right" if k >= 10 else ("a real mixture" if k > 0.1 else "lies to the left")
        print(f"{acid + ' + ' + base:<38}{pa:>8.2f}{pb:>8.2f}{math.log10(k):>7.1f}"
              f"{delta_g_kj(k):>8.1f}  {verdict}")
    # Which bases in the table can deprotonate ethyne by at least a factor of 1000?
    strong = [b for a, b in BASE_OF.items() if TABLE[a] - TABLE["ethyne"] >= 3]
    print("\nBases that deprotonate ethyne (K >= 1000):", ", ".join(strong))


if __name__ == "__main__":
    main()
