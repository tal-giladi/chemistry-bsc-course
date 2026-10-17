"""Lesson 10.6 project, exercise: acetic acid in vinegar from five mass-based titrations
Fill in the TODO functions. Reference solution: project_vinegar_solution.py
with an indicator blank, with mean, SD, 95 % confidence interval, an uncertainty budget and a t-test
against the label.

Run:   py project_vinegar.py
       py project_vinegar.py my_vinegar.csv
CSV columns: trial,m_vinegar_g,m_syringe_before_g,m_syringe_after_g
One row with trial = blank (25 mL water + indicator titrated to the same colour, m_vinegar_g = 0).
Edit the SETUP block to your own titrant, scale, drop mass and label.
Reaction: CH3COOH + NaHCO3 -> CH3COONa + H2O + CO2 (1 : 1).
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M_ACETIC = 60.052          # g/mol
M_NAHCO3 = 84.006          # g/mol
# ---- SETUP ----
TITRANT = {"m_nahco3_g": 5.00, "m_solution_g": 100.00}
PURITY_HALF_WIDTH = 0.005  # baking soda purity 100 % +/- 0.5 % (rectangular); see lesson 10.4
SCALE_D = 0.01             # g, scale resolution
DROP_G = 0.045             # g, one drop (lesson 10.1)
DENSITY = 1.005            # g/mL, white vinegar, to convert % w/w to g per 100 mL
LABEL = 5.0                # g acetic acid per 100 mL ("5 % acidity")
# ---------------
T95 = {2: 12.71, 3: 4.30, 4: 3.18, 5: 2.78, 6: 2.57, 7: 2.45, 8: 2.36, 9: 2.31, 10: 2.26}  # two-sided, n results


def acid_percent(m_vinegar, m_titrant, m_blank, w_titrant):
    """Acetic acid in % w/w. Subtract the blank titrant mass, convert grams of titrant to moles of
    NaHCO3 with w_titrant (mol/g), 1 : 1 to acetic acid, times M_ACETIC, divided by the vinegar mass."""
    # TODO: one line, 100 (m_titrant - m_blank) w_titrant M_ACETIC / m_vinegar.
    return None


def t_statistic(mean, sd, n, reference):
    """One-sample t: (mean - reference) / (sd / sqrt(n))."""
    # TODO: one line, (mean - reference) / (sd / math.sqrt(n)).
    return None


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    if acid_percent(5.0, 7.0, 0.0, 6e-4) is None or t_statistic(1.0, 1.0, 4, 0.0) is None:
        print("TODO: write acid_percent() and t_statistic() first.")
        return
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "vinegar_project_example.csv"
    rows = read_rows(path)
    delivered = {r["trial"]: float(r["m_syringe_before_g"]) - float(r["m_syringe_after_g"]) for r in rows}
    m_blank = delivered.pop("blank", 0.0)
    w = TITRANT["m_nahco3_g"] / TITRANT["m_solution_g"] / M_NAHCO3
    print(f"titrant {w * 1000:.4f} mmol/g; blank {m_blank:.2f} g of titrant")
    results, m_t_all, m_v_all = [], [], []
    for r in rows:
        if r["trial"] == "blank":
            continue
        m_v, m_t = float(r["m_vinegar_g"]), delivered[r["trial"]]
        pct = acid_percent(m_v, m_t, m_blank, w)
        results.append(pct)
        m_t_all.append(m_t)
        m_v_all.append(m_v)
        print(f"  trial {r['trial']}: vinegar {m_v:.2f} g, titrant {m_t:.2f} g -> {pct:.3f} % w/w")
    n = len(results)
    mean = sum(results) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in results) / (n - 1))
    half = T95[n] * sd / math.sqrt(n)
    print(f"mean {mean:.3f} %, SD {sd:.3f} %, RSD {100 * sd / mean:.2f} %, 95 % CI +/- {half:.3f} % (n = {n})")
    no_blank = mean * (sum(m_t_all) / n) / (sum(m_t_all) / n - m_blank)
    print(f"without the blank correction the mean would be about {no_blank:.3f} %")

    m_t, m_v = sum(m_t_all) / n, sum(m_v_all) / n
    u_diff = SCALE_D / math.sqrt(6)                       # a mass found as a difference of two readings
    budget = {
        "repeatability (s / sqrt n)": sd / math.sqrt(n) / mean,
        "titrant mass (scale)": u_diff / (m_t - m_blank),
        "vinegar mass (scale)": u_diff / m_v,
        "end point (half a drop)": DROP_G / 2 / math.sqrt(3) / (m_t - m_blank),
        "blank (scale)": u_diff / (m_t - m_blank),
        "NaHCO3 mass in titrant": u_diff / TITRANT["m_nahco3_g"],
        "titrant solution mass": u_diff / TITRANT["m_solution_g"],
        "NaHCO3 purity": PURITY_HALF_WIDTH / math.sqrt(3),
    }
    u_rel = math.sqrt(sum(v ** 2 for v in budget.values()))
    print("uncertainty budget (relative standard uncertainties):")
    for k, v in sorted(budget.items(), key=lambda kv: -kv[1]):
        print(f"  {k:28s} {100 * v:6.3f} %   share of variance {100 * v ** 2 / u_rel ** 2:5.1f} %")
    u = mean * u_rel
    print(f"combined u = {u:.3f} %; expanded U (k = 2) = {2 * u:.3f} % -> {mean:.2f} +/- {2 * u:.2f} % w/w")

    wv = mean * DENSITY
    t = t_statistic(wv, sd * DENSITY, n, LABEL)
    print(f"as g per 100 mL: {wv:.3f} +/- {2 * u * DENSITY:.3f}; label {LABEL}")
    print(f"t = {t:.2f} against t_crit {T95[n]:.2f} (95 %, {n - 1} df): "
          f"{'no significant difference' if abs(t) < T95[n] else 'significantly different'} from the label (repeatability only)")
    print(f"label within the expanded uncertainty: {'yes' if abs(wv - LABEL) <= 2 * u * DENSITY else 'no'}")


if __name__ == "__main__":
    main()
