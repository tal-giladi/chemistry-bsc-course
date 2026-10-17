"""Generate the simulated example data sets for the Module 7 labs (fixed seed, so the files are reproducible).

Run (from this folder):
    py make_data.py
The models and true parameters are written here so you can check your analysis against them.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
M_NAHCO3 = 84.007   # g/mol, PubChem CID 516892
M_CO2 = 44.009      # g/mol, PubChem CID 280
M_ACOH = 60.052     # g/mol, PubChem CID 176


def vinegar_series(path=HERE / "vinegar_example.csv", seed=7):
    """Lesson 07.5: mass lost when baking soda is added to 50.0 mL of vinegar.
    True model: vinegar 5.0 % w/v acetic acid (0.833 mol/L), 88 % of the CO2 escapes (the rest stays
    dissolved), scale noise 0.05 g (0.1 g pocket scale, read twice)."""
    rng = np.random.default_rng(seed)
    v_l = 0.0500
    n_acid = 50.0 / M_ACOH * v_l          # 5.0 g per 100 mL -> 50 g/L
    recovery = 0.88
    m_bicarb = np.arange(0.5, 6.01, 0.5)
    n_co2 = np.minimum(m_bicarb / M_NAHCO3, n_acid)
    loss = recovery * n_co2 * M_CO2 + rng.normal(0, 0.05, m_bicarb.size)
    lines = [
        "# Simulated with make_data.py (seed 7): 50.0 mL vinegar labelled 5 %, true 5.0 % w/v acetic acid,",
        "# 88 % of the CO2 escapes, scale noise 0.05 g. Columns: baking soda added (g), mass lost after 15 min (g).",
        "m_bicarb_g,mass_loss_g",
    ]
    lines += [f"{m:.1f},{x:.2f}" for m, x in zip(m_bicarb, loss)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {path.name}: true break point {n_acid * M_NAHCO3:.2f} g baking soda")


if __name__ == "__main__":
    vinegar_series()
