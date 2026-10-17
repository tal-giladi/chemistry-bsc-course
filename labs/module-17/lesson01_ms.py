"""Lesson 17.1: exact mass, degrees of unsaturation, isotope patterns and HRMS formulas.

Fill in the three parts marked TODO, then run (from this folder):
    py lesson01_ms.py
Reference solution: lesson01_ms_solution.py
"""
import itertools

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from spec17 import ISOTOPES, ELECTRON_MASS_U, parse_formula, runs_dir  # noqa: E402


def dbe(formula):
    """Degrees of unsaturation (rings + pi bonds) = (2C + 2 + N - H - X) / 2. O and S do not count."""
    c = parse_formula(formula)
    # TODO: count the halogens and return the DBE. c.get("N", 0) gives 0 when there is no N.
    return None


def monoisotopic_mass(formula):
    """Mass of the molecule made only of the most abundant isotope of each element, in u."""
    total = 0.0
    for el, n in parse_formula(formula).items():
        lightest = max(ISOTOPES[el], key=lambda iso: iso[2])
        total += n * lightest[1]
    return total


def nominal_mass(formula):
    """Integer mass using the mass number of the most abundant isotope."""
    return sum(n * max(ISOTOPES[el], key=lambda iso: iso[2])[0] for el, n in parse_formula(formula).items())


def isotope_pattern(formula, cutoff=1e-4):
    """Relative intensities of M, M+1, M+2 ... as {nominal mass: % of the largest peak}.
    Each atom adds its isotopes independently, so the pattern is a repeated convolution."""
    dist = {0: 1.0}
    for el, n in parse_formula(formula).items():
        for _ in range(n):
            new = {}
            for m, p in dist.items():
                for a, _, ab in ISOTOPES[el]:
                    # TODO: adding this isotope (mass number a, abundance ab) to a species of
                    # nominal mass m and probability p gives mass m + a with probability p * ab.
                    # Add that probability to new[m + a].
                    pass
            dist = {m: p for m, p in new.items() if p > cutoff * 1e-3}
            if not dist:
                return {}
    top = max(dist.values())
    return {m: 100 * p / top for m, p in sorted(dist.items()) if 100 * p / top > 100 * cutoff}


def carbons_from_m1(m_plus_1_percent):
    """Rough carbon count from the M+1 peak height as % of M (each C adds about 1.1 %)."""
    return m_plus_1_percent / 1.1


def candidate_formulas(mz, tol_ppm=5.0, max_c=12, max_n=3, max_o=4, radical_cation=True):
    """CcHhNnOo formulas whose ion mass is within tol_ppm of the measured m/z.
    A radical cation M+. weighs one electron less than the neutral molecule."""
    hits = []
    for c, n, o in itertools.product(range(1, max_c + 1), range(max_n + 1), range(max_o + 1)):
        for h in range(1, 2 * c + n + 3):
            f = f"C{c}H{h}" + ("N" * (n == 1) or f"N{n}" * (n > 1)) + ("O" * (o == 1) or f"O{o}" * (o > 1))
            d = dbe(f)
            if d is None or d < 0 or d != int(d):
                continue
            m = monoisotopic_mass(f) - (ELECTRON_MASS_U if radical_cation else 0.0)
            ppm = None  # TODO: the error in ppm is (measured - calculated) / calculated * 1e6
            if ppm is not None and abs(ppm) <= tol_ppm:
                hits.append((f, m, ppm, d))
    return sorted(hits, key=lambda x: abs(x[2]))


def main():
    print("Part 1 - formula, nominal and exact mass, DBE")
    for f in ["C6H12O", "C5H8O2", "C6H16N2", "C4H9Cl", "C3H7Br", "C10H14", "C4H11N"]:
        d = dbe(f)
        print(f"  {f:8s} nominal {nominal_mass(f):4d}  exact {monoisotopic_mass(f):10.5f}  DBE "
              + ("TODO" if d is None else f"{d:4.1f}"))

    print("\nPart 2 - isotope patterns (% of the largest peak)")
    out = runs_dir()
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for ax, f in zip(axes, ["C10H14", "C4H9Cl", "C3H7Br", "CH2Br2"]):
        pat = isotope_pattern(f)
        shown = {m: i for m, i in pat.items() if i >= 0.5}
        if not shown:
            print(f"  {f:7s} TODO: finish isotope_pattern()")
            continue
        print(f"  {f:7s} " + "  ".join(f"{m}:{i:.1f}" for m, i in shown.items()))
        ax.bar(list(shown), list(shown.values()), width=0.3, color="black")
        ax.set_title(f)
        ax.set_xlabel("m/z")
    axes[0].set_ylabel("relative intensity / %")
    fig.tight_layout()
    fig.savefig(out / "lesson01_isotopes.png", dpi=120)
    print(f"  plot written to {out / 'lesson01_isotopes.png'}")

    print("\nPart 3 - carbon count from M+1")
    print(f"  M+1 = 11.0 % of M -> about {carbons_from_m1(11.0):.0f} carbons")

    print("\nPart 4 - formulas with nominal mass 100 (all that a low-resolution m/z 100 allows)")
    print("  " + ", ".join(f for f, *_ in candidate_formulas(100.0883, tol_ppm=5000)))
    print("  ...and the ones within 5 ppm of an HRMS reading of m/z 100.0883 (EI, M+.)")
    for f, m, ppm, d in candidate_formulas(100.0883):
        print(f"  {f:10s} ion mass {m:.5f}  error {ppm:+5.1f} ppm  DBE {d:.0f}")


if __name__ == "__main__":
    main()
