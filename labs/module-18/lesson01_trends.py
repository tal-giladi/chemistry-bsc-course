"""Lesson 18.1: Slater's rules against NIST ionisation energies.

Fill in slater_zeff() (marked TODO), then run (from this folder):
    py lesson01_trends.py        # prints the tables, saves runs/lesson01_zeff.png
Reference solution: lesson01_trends_solution.py
"""
import numpy as np

from inorg18 import HERE, SYMBOLS, config_string, configuration, load_ie


def slater_group(n, l):
    """Slater's grouping (1s)(2s,2p)(3s,3p)(3d)(4s,4p)...: s and p share a group, d is separate.
    The tuples sort in Slater's order: (3, 0) < (3, 2) < (4, 0)."""
    return (n, 0) if l <= 1 else (n, l)


def slater_zeff(z, n, l):
    """Effective nuclear charge felt by ONE electron in orbital (n, l) of the neutral atom Z.
    Slater's rules:
      s or p electron: every other electron in the same (ns, np) group 0.35 (0.30 inside 1s);
                       each electron with principal quantum number n-1: 0.85;
                       each electron with n-2 or lower: 1.00.
      d electron:      every other electron in the same nd group 0.35;
                       every electron in a group before it in Slater's order: 1.00.
      Electrons in groups after the target never shield it."""
    # TODO: loop over configuration(z), which gives (cn, cl, k) = shell, subshell, electron count.
    #       Use slater_group() to decide whether each subshell is in the same group as the target,
    #       add the right shielding to s, and return z - s.
    #       Check: slater_zeff(11, 3, 0) is 2.20 (sodium) and slater_zeff(26, 3, 2) is 6.25 (iron 3d).
    return None


def outermost(z):
    """(n, l) of the outermost s or p electron (the first one removed on ionisation)."""
    return max((n, l) for n, l, _ in configuration(z) if l <= 1)


def main():
    ie = load_ie()
    if slater_zeff(11, 3, 0) is None:
        print("TODO: write slater_zeff() first.")
        return
    print(f"{'el':<3} {'configuration':<34} {'orb':<4} {'Zeff':>5} {'NIST IE1/eV':>11}")
    per = {2: ([], []), 3: ([], [])}
    for z in list(range(3, 21)) + [26, 29, 30, 31, 35, 36]:
        sym = SYMBOLS[z - 1]
        n, l = outermost(z)
        zeff = slater_zeff(z, n, l)
        ie1 = ie[sym][0]
        if n in per:
            per[n][0].append(zeff)
            per[n][1].append(ie1)
        print(f"{sym:<3} {config_string(configuration(z)):<34} {n}{'spdf'[l]:<3} {zeff:5.2f} {ie1:11.3f}")

    for n, (zf, e1) in per.items():
        r = np.corrcoef(zf, e1)[0, 1]
        print(f"\nPeriod {n}: Zeff rises by {zf[1] - zf[0]:.2f} per element; correlation with IE1 r = {r:.3f}")
    print("Slater's Zeff rises smoothly, so it cannot produce the group 2->13 and 15->16 dips.")

    print("\nIron, Z = 26: 3d6 4s2")
    print(f"  4s electron Zeff = {slater_zeff(26, 4, 0):.2f}  (outer shell, far from the nucleus)")
    print(f"  3d electron Zeff = {slater_zeff(26, 3, 2):.2f}  (n = 3, shielded only by the argon core)")
    print("  The 4s electron feels less charge and sits farther out, so it leaves first: Fe2+ is [Ar] 3d6.")

    print("\nSame group, one period lower:")
    for a, b in (("Li", "Na"), ("C", "Si"), ("F", "Cl"), ("Al", "Ga")):
        za, zb = SYMBOLS.index(a) + 1, SYMBOLS.index(b) + 1
        print(f"  {a:<2} Zeff {slater_zeff(za, *outermost(za)):.2f}, IE1 {ie[a][0]:6.3f} eV   "
              f"{b:<2} Zeff {slater_zeff(zb, *outermost(zb)):.2f}, IE1 {ie[b][0]:6.3f} eV")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    for n, (zf, e1) in per.items():
        ax.plot(zf, e1, "o-", label=f"period {n}")
    ax.set_xlabel("Slater Zeff of the outermost electron")
    ax.set_ylabel("NIST first ionisation energy / eV")
    ax.set_title("IE1 against Slater Zeff")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "lesson01_zeff.png", dpi=120)
    print(f"\nPlot saved to {out / 'lesson01_zeff.png'}")


if __name__ == "__main__":
    main()
