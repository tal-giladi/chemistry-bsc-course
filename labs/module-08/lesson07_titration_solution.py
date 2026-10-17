"""Lesson 08.7 module practical, reference solution: acetic acid in vinegar by titration with
baking-soda solution, mass-based, with mean, standard deviation and a 95 % confidence interval.

Run:   py lesson07_titration_solution.py                  (uses titration_example.csv)
       py lesson07_titration_solution.py my_titration.csv (columns trial,m_vinegar_g,
                                                           m_syringe_before_g,m_syringe_after_g)
Reaction: CH3COOH + NaHCO3 -> CH3COONa + H2O + CO2, 1 : 1.
Edit TITRANT to your own solution: grams of NaHCO3 and total grams of solution.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M_ACETIC = 60.052      # g/mol
M_NAHCO3 = 84.006      # g/mol
TITRANT = {"m_nahco3_g": 5.00, "m_solution_g": 100.00}
T95 = {2: 12.71, 3: 4.30, 4: 3.18, 5: 2.78, 6: 2.57, 7: 2.45, 8: 2.36, 9: 2.31, 10: 2.26}  # Student t, n trials


def read_trials(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(fh)]


def acid_percent(m_vinegar, m_titrant, w_titrant):
    """Mass percent of acetic acid: moles NaHCO3 delivered = moles acetic acid (1 : 1)."""
    n_acid = m_titrant * w_titrant
    return 100 * n_acid * M_ACETIC / m_vinegar


def mean_sd(values):
    n = len(values)
    mean = sum(values) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1))
    return mean, sd


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "titration_example.csv"
    w = TITRANT["m_nahco3_g"] / TITRANT["m_solution_g"] / M_NAHCO3      # mol per g of titrant
    print(f"titrant: {w * 1000:.4f} mmol NaHCO3 per g")
    results = []
    for row in read_trials(path):
        m_t = row["m_syringe_before_g"] - row["m_syringe_after_g"]
        pct = acid_percent(row["m_vinegar_g"], m_t, w)
        results.append(pct)
        print(f"  trial {int(row['trial'])}: vinegar {row['m_vinegar_g']:.2f} g, titrant {m_t:.2f} g, "
              f"acetic acid {pct:.2f} % by mass")
    mean, sd = mean_sd(results)
    n = len(results)
    half = T95.get(n, 2.0) * sd / math.sqrt(n)
    print(f"mean {mean:.2f} %, SD {sd:.2f} %, RSD {100 * sd / mean:.1f} %, "
          f"95 % CI {mean:.2f} +/- {half:.2f} % (n = {n})")
    print(f"as g per 100 mL (density about 1.005 g/mL): {mean * 1.005:.2f}; label: 5 % acidity")


if __name__ == "__main__":
    main()
