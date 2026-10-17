"""Lesson 24.6 - module practical: benzaldehyde -> benzoin -> benzil -> benzilic acid, checked at every step.

Fill in the functions marked TODO, then run:  py lesson06_practical.py
Reference solution: lesson06_practical_solution.py
Reads multistep_observations.csv (illustrative observations; replace them with your organic-bench runs).
"""
from org24 import COMPOUNDS, molar_mass, read_csv

# step: (starting material, product, mol of start per mol of product)
STEPS = {
    1: ("benzaldehyde", "benzoin", 2),      # thiamine-catalysed benzoin condensation
    2: ("benzoin", "benzil", 1),             # oxidation
    3: ("benzil", "benzilic acid", 1),       # KOH, then acid: benzilic acid rearrangement
}


def step_yield(mass_g, start_g, step):
    """Percent yield of one step from the mass of starting material actually used."""
    # TODO: theoretical = start_g / M(start) / ratio * M(product); return 100 * mass_g / theoretical
    return None


def overall(yields_pct):
    """Overall percent yield of a linear sequence: the product of the step yields."""
    # TODO: multiply the fractions
    return None


def parse_ir(text):
    """'3405;3300-2500b;1718' -> list of (low, high, broad)."""
    out = []
    for tok in text.split(";"):
        broad = tok.endswith("b")
        tok = tok.rstrip("b")
        if "-" in tok:
            a, b = (float(v) for v in tok.split("-"))
            out.append((min(a, b), max(a, b), broad))
        else:
            out.append((float(tok), float(tok), broad))
    return out


def parse_nmr(text):
    """'7.92:2:d;5.95:1:d' -> list of (shift, protons, multiplicity); a range '7.55-7.25' gives its middle."""
    out = []
    for tok in text.split(";"):
        s, n, m = tok.split(":")
        if "-" in s:
            a, b = (float(v) for v in s.split("-"))
            s = (a + b) / 2
        out.append((float(s), float(n), m))
    return out


def assign(ir, nmr):
    """Name the compound (or mixture) from the IR bands and 1H NMR peaks.
    Rules: CHO proton 9.8-10.2 ppm -> benzaldehyde; broad 2500-3300 band and C=O >= 1700 -> benzilic acid;
    O-H 3200-3600 with CH(OH) near 5.9 ppm worth >= 0.5 H -> benzoin; no O-H -> benzil;
    benzil pattern plus a small 5.9 ppm signal or an O-H band -> benzil containing benzoin."""
    # TODO: implement the rules above. Useful quantities:
    #   oh = any(3200 <= hi and lo <= 3600 and not broad ...); acid = any(broad and lo <= 2600 and hi >= 3200)
    #   co = max carbonyl in 1650-1760; ch = protons of a peak at 5.5-6.2 ppm (0 if none)
    return None


def main():
    if step_yield(1, 1, 2) is None or overall([50, 50]) is None or assign([(1700, 1700, False)], []) is None:
        print("TODO: write step_yield(), overall() and assign() first.")
        return
    best = {}
    for r in read_csv("multistep_observations.csv"):
        step = int(r["step"])
        y = step_yield(float(r["mass_g"]), float(r["start_g"]), step)
        name = assign(parse_ir(r["ir_cm-1"]), parse_nmr(r["nmr"]))
        expected = STEPS[step][1]
        lit = COMPOUNDS[expected][1]
        lo, hi = float(r["mp_lo"]), float(r["mp_hi"])
        ok = name == expected and hi - lo <= 2 and abs(hi - lit) <= 3
        print(f"{r['sample']:4s} step {step}: {y:5.1f} %  mp {lo:.0f}-{hi:.0f} C (lit. {lit:.0f})  "
              f"spectra say: {name:36s} {'PASS' if ok else 'FAIL - purify or repeat'}")
        if ok:
            best[step] = y
    if len(best) == 3:
        tot = overall([best[s] for s in (1, 2, 3)])
        print(f"overall yield (passing samples): {tot:.1f} %")
        need = 1.00 / (tot / 100) / molar_mass("benzilic acid") * 2 * molar_mass("benzaldehyde")
        print(f"benzaldehyde needed for 1.00 g benzilic acid at these yields: {need:.1f} g")


if __name__ == "__main__":
    main()
