"""Lesson 18.2: lattice enthalpies from Born-Haber cycles and from lattice models.

Fill in the three functions marked TODO, then run (from this folder):
    py lesson02_born_haber.py      # prints the tables, saves runs/lesson02_lattice.png
Data: born_haber.csv (sources in its header). Reference solution: lesson02_born_haber_solution.py
Sign convention: lattice enthalpy is POSITIVE, the enthalpy needed to break 1 mol of solid into gas-phase ions.
"""
import math

from inorg18 import COULOMB_KJ_A, EV_KJ, HERE, R, load_csv  # noqa: F401 (EV_KJ is for your born_haber)

T = 298.15
RHO = 0.345          # Born-Mayer repulsion range, angstrom (alkali halides, 0.30-0.345)


def r0_from_lattice(structure, a):
    """Shortest cation-anion distance (angstrom) from the cubic lattice constant a."""
    if structure == "rock salt":
        return a / 2
    if structure == "fluorite":
        return a * math.sqrt(3) / 4
    raise ValueError(structure)


def born_haber(row, ea2_ev=None):
    """Lattice enthalpy (kJ/mol, positive) from the Born-Haber cycle:
    dH_L = -dfH(solid) + dfH(M,g) + n dfH(X,g) + IE_sum - n EA1 - n EA2.
    For oxides the second electron affinity ea2_ev must be supplied (eV, negative = costs energy);
    without it the function returns the cycle total WITHOUT the EA2 term."""
    # TODO: n = int(row["n_anion"]); add up the five enthalpy terms (convert eV to kJ/mol with EV_KJ).
    #       Remember: the solid's formation enthalpy enters with a minus sign, and so does every electron
    #       affinity (energy released when the anion forms). Subtract n * ea2_ev * EV_KJ only if ea2_ev is given.
    #       Check: NaCl gives 787.2.
    return None


def born_mayer(m, zz, r0, rho=RHO):
    """Lattice ENERGY (kJ/mol, positive) from the Born-Mayer equation:
    U = N_A M |z+ z-| e^2 / (4 pi eps0 r0) x (1 - rho / r0)."""
    # TODO: use COULOMB_KJ_A (= e^2 N_A / 4 pi eps0 in kJ/mol x angstrom). Check: NaCl, r0 = 2.820 -> 755.6.
    return None


def born_lande(m, zz, r0, n_born):
    """Lattice energy (kJ/mol) from the Born-Lande equation, U = (Coulomb term) x (1 - 1/n)."""
    return COULOMB_KJ_A * m * zz / r0 * (1 - 1 / n_born)


def kapustinskii(nu, zz, r_sum_a):
    """Lattice energy (kJ/mol) from the Kapustinskii equation, no structure needed:
    U = 1202.5 nu |z+ z-| / (r+ + r-) x (1 - 0.345 / (r+ + r-)),  radii in angstrom."""
    # TODO: one line. Check: NaCl, nu = 2, r+ + r- = 2.83 -> 746.3.
    return None


def energy_to_enthalpy(u, nu, t=T):
    """Lattice enthalpy from lattice energy: breaking 1 mol of solid makes nu mol of gas ions,
    so dH = dU + (delta n_gas) R T (lesson 13.2)."""
    return u + nu * R * t / 1000


def main():
    rows = load_csv("born_haber.csv")
    if born_haber(rows[0]) is None or born_mayer(1.75, 1, 2.8) is None or kapustinskii(2, 1, 2.8) is None:
        print("TODO: write born_haber(), born_mayer() and kapustinskii() first.")
        return
    print(f"{'solid':<5} {'r0/A':>5} {'Born-Haber':>10} {'Born-Mayer':>10} {'ratio':>6} {'Kapustinskii':>12}")
    ratios = []
    store = {}
    for row in rows:
        zz = int(row["z_cat"]) * int(row["z_an"])
        nu = int(row["nu"])
        r_sum = (float(row["r_cat_pm"]) + float(row["r_an_pm"])) / 100
        h_kap = energy_to_enthalpy(kapustinskii(nu, zz, r_sum), nu)
        if row["a_A"]:
            r0 = r0_from_lattice(row["structure"], float(row["a_A"]))
            h_bm = energy_to_enthalpy(born_mayer(float(row["M"]), zz, r0), nu)
        else:
            r0, h_bm = float("nan"), float("nan")
        store[row["compound"]] = (row, h_bm, h_kap)
        if row["z_an"] == "1":
            h_bh = born_haber(row)
            ratios.append(h_bm / h_bh)
            print(f"{row['compound']:<5} {r0:5.3f} {h_bh:10.1f} {h_bm:10.1f} {h_bm / h_bh:6.3f} {h_kap:12.1f}")
    print(f"Born-Mayer / Born-Haber for the halides: mean {sum(ratios) / len(ratios):.3f}")

    nacl = store["NaCl"][0]
    r0 = r0_from_lattice("rock salt", float(nacl["a_A"]))
    coul = COULOMB_KJ_A * 1.747565 / r0
    print(f"\nNaCl: Coulomb attraction alone {coul:.0f} kJ/mol (lesson 04.3); Born-Lande with n = 8 "
          f"{born_lande(1.747565, 1, r0, 8):.0f}; Born-Mayer {born_mayer(1.747565, 1, r0):.0f}")
    print(f"      energy -> enthalpy adds 2RT = {2 * R * T / 1000:.2f} kJ/mol")

    print("\nOxides: the cycle without the second electron affinity of oxygen")
    for name in ("MgO", "CaO"):
        row, h_bm, h_kap = store[name]
        partial = born_haber(row)          # everything except -EA2
        model = h_bm if not math.isnan(h_bm) else h_kap
        label = "Born-Mayer" if not math.isnan(h_bm) else "Kapustinskii"
        ea2_cost = model - partial         # energy needed for O-(g) + e- -> O2-(g)
        print(f"  {name}: cycle without EA2 {partial:7.1f}; {label} lattice enthalpy {model:7.1f}"
              f" -> O-(g) + e- -> O2-(g) costs {ea2_cost:+.0f} kJ/mol")
    print("  Both oxides agree that adding the second electron costs several hundred kJ/mol.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 4))
    for name, (row, h_bm, h_kap) in store.items():
        if row["z_an"] == "1":
            ax.plot(born_haber(row), h_bm, "o", color="C0")
            ax.plot(born_haber(row), h_kap, "s", color="C1")
            ax.annotate(name, (born_haber(row), h_bm), textcoords="offset points", xytext=(5, -10), fontsize=8)
    lim = [600, 2800]
    ax.plot(lim, lim, "k:", lw=1)
    ax.plot([], [], "o", color="C0", label="Born-Mayer")
    ax.plot([], [], "s", color="C1", label="Kapustinskii")
    ax.set_xlabel("Born-Haber lattice enthalpy / kJ mol$^{-1}$")
    ax.set_ylabel("model lattice enthalpy / kJ mol$^{-1}$")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "lesson02_lattice.png", dpi=120)
    print(f"\nPlot saved to {out / 'lesson02_lattice.png'}")


if __name__ == "__main__":
    main()
