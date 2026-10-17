"""Lesson 18.5: module practical, nine complex cards.

For each card (cards.csv), deduce from formula, absorption and magnetic moment:
oxidation state and d count, unpaired electrons, spin state, Delta_o where one band gives it, the colour
you expect to see, and whether the band is d-d or charge transfer. The script prints a report and checks
the predicted colour against the observed one.

Before running, fill in your own prediction table on paper (lesson 18.5, Part B). Then write the three
functions marked TODO and run (from this folder):
    py lesson05_practical.py
Reference solution: lesson05_practical_solution.py
"""

from inorg18 import CM_KJ, band_of, cm1_to_nm, d_count, load_csv, nm_to_cm1, spin_only

ABSORBED_TO_SEEN = {"red": "green", "orange": "blue", "yellow": "violet", "green": "red-purple",
                    "blue": "orange", "violet": "yellow"}


def unpaired_from_mu(mu):
    """Number of unpaired electrons n whose spin-only moment sqrt(n(n+2)) is closest to mu (0-5)."""
    # TODO: try n = 0..5 and return the n whose spin_only(n) is closest to mu. Check: 3.8 -> 3, 1.95 -> 1.
    return None


def unpaired_options(d, geometry):
    """Unpaired electrons for (high spin, low spin). Octahedral low spin fills t2g first;
    tetrahedral and square-planar entries return the usual single answer twice."""
    hs = d if d <= 5 else 10 - d
    if geometry == "oct":
        if d <= 3:
            ls = d
        elif d <= 6:
            ls = 6 - d
        else:
            ls = d - 6 if d <= 8 else 10 - d
        return hs, ls
    if geometry == "sq" and d == 8:
        return 0, 0                      # square-planar d8 is diamagnetic
    return hs, hs


def spin_label(d, geometry, n_unpaired):
    """'HS', 'LS', 'only one' (no spin choice) or '?' (moment fits neither)."""
    # TODO: hs, ls = unpaired_options(d, geometry). If hs == ls there is no spin choice: return "only one"
    #       when n_unpaired equals it, else "?". Otherwise return "HS" or "LS" by matching n_unpaired, or "?".
    return None


def band_type(d, intensity):
    """'charge transfer' if the metal has no d-d transitions (d0, d10) or the band is strong;
    'spin-forbidden d-d' if very weak; otherwise 'd-d (Laporte-forbidden)'."""
    # TODO: d0 or d10, or a strong band -> "charge transfer"; "very weak" -> "spin-forbidden d-d";
    #       anything else -> "d-d (Laporte-forbidden)".
    return None


def delta_from_band(d, geometry, nm):
    """Delta_o in cm-1 when the lowest band gives it directly (octahedral d1, d3, d8, d9); else None."""
    if geometry == "oct" and d in (1, 3, 8, 9) and nm:
        return nm_to_cm1(nm)
    return None


def seen_colour(nm, note):
    """Colour expected for the eye: complementary to the absorbed band."""
    if nm:
        b = band_of(nm)
        return b[1] if b else "colourless (absorbs outside the visible)"
    for absorbed, seen in ABSORBED_TO_SEEN.items():
        if note.startswith("absorbs " + absorbed) or note.startswith("absorbs " + absorbed.split("-")[0]):
            return seen
    if note.startswith("absorbs blue-violet"):
        return "orange-yellow"
    return "almost colourless"


def main():
    cards = load_csv("cards.csv")
    if unpaired_from_mu(3.8) is None or spin_label(6, "oct", 0) is None or band_type(0, "strong") is None:
        print("TODO: write unpaired_from_mu(), spin_label() and band_type() first.")
        return
    print(f"{'#':<2} {'complex':<14} {'ox':>3} {'d':>3} {'n':>2} {'spin':<9} {'Delta_o/cm-1':>12} {'band':<24} "
          f"{'expected colour':<17} observed")
    matches = 0
    for c in cards:
        ox = int(c["ox"])
        d = d_count(c["metal"], ox)
        n = unpaired_from_mu(float(c["mu_BM"]))
        spin = spin_label(d, c["geometry"], n)
        nm = float(c["lambda_nm"]) if c["lambda_nm"] else None
        delta = delta_from_band(d, c["geometry"], nm)
        btype = band_type(d, c["intensity"])
        colour = seen_colour(nm, c["absorbed_note"])
        obs = c["observed_colour"]
        ok = any(w in obs for w in colour.replace("-", " ").split())
        matches += ok
        dtxt = f"{delta:12.0f}" if delta else "           -"
        print(f"{c['card']:<2} {c['formula']:<14} {ox:>+3} {d:>3} {n:>2} {spin:<9} {dtxt} {btype:<24} "
              f"{colour:<17} {obs}{'' if ok else '   (check)'}")
    print(f"\nExpected colour agrees with the observed colour for {matches} of {len(cards)} cards.")
    d_ti = nm_to_cm1(499)
    print(f"Card 1: Delta_o = {d_ti:.0f} cm-1 = {d_ti * CM_KJ:.0f} kJ/mol; "
          f"spin-only moment for n = 1 is {spin_only(1):.2f} BM (observed 1.6-1.7).")
    print(f"Card 2 check: Delta_o 17 400 cm-1 -> {cm1_to_nm(17400):.0f} nm; Card 3: 15 060 cm-1 -> {cm1_to_nm(15060):.0f} nm.")
    print("Spin-only moments: " + ", ".join(f"n={k}: {spin_only(k):.2f}" for k in range(6)))


if __name__ == "__main__":
    main()
