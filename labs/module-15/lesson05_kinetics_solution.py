"""Lesson 15.5 reference solution: SN1 or SN2? Find the order in nucleophile, then check the stereochemistry.

Run (from this folder):
    py lesson05_kinetics_solution.py      # prints the analysis, saves runs/sn_runs.png
"""
import math

import numpy as np

from org15 import need_rdkit, read_csv, runs_dir


def load():
    """Return {(substrate, run): (nu0, t array, conc array)}."""
    data = {}
    for r in read_csv("sn_runs.csv"):
        key = (r["substrate"], int(r["run"]))
        nu0, t, c = data.get(key, (float(r["nu0_M"]), [], []))
        t.append(float(r["t_s"]))
        c.append(float(r["substrate_M"]))
        data[key] = (nu0, t, c)
    return {k: (v[0], np.array(v[1]), np.array(v[2])) for k, v in data.items()}


def initial_rate(t, c, n_points=5):
    """Initial rate in mol/(L s): minus the slope of a straight line through the first n_points.
    Using several points averages out the noise; using too many lets the curve bend the line."""
    slope = np.polyfit(t[:n_points], c[:n_points], 1)[0]
    return -slope


def order_in_nucleophile(rate1, nu1, rate2, nu2):
    """If rate = k [Nu]^n, then n = log(rate2/rate1) / log(nu2/nu1)."""
    return math.log(rate2 / rate1) / math.log(nu2 / nu1)


def stereo_demo():
    """SN2 inverts the stereocentre; SN1 goes through a flat carbocation and gives both configurations."""
    need_rdkit()
    from rdkit import Chem
    from rdkit.Chem import AllChem, rdCIPLabeler

    def label(m):
        rdCIPLabeler.AssignCIPLabels(m)
        return [a.GetProp("_CIPCode") for a in m.GetAtoms() if a.HasProp("_CIPCode")]

    start = Chem.MolFromSmiles("CC[C@H](C)Br")  # 2-bromobutane, one enantiomer
    print(f"\nstart: {Chem.MolToSmiles(start)}  CIP {label(start)}")
    # Reaction SMARTS: the mapped carbon :1 changes from @ to @@ = inversion of configuration.
    sn2 = AllChem.ReactionFromSmarts("[C@:1][Br:2].[OH-:3]>>[C@@:1][OH1+0:3].[Br-:2]")
    for prods in sn2.RunReactants((start, Chem.MolFromSmiles("[OH-]"))):
        p = prods[0]
        Chem.SanitizeMol(p)
        print(f"SN2 with hydroxide: {Chem.MolToSmiles(p)}  CIP {label(p)}  (inversion)")
    # SN1: the carbocation is planar, so water adds to either face; write both products.
    for smi in ("CC[C@@H](C)O", "CC[C@H](C)O"):
        print(f"SN1 product (either face): {smi}  CIP {label(Chem.MolFromSmiles(smi))}")


def main():
    data = load()
    print(f"{'substrate':>9}{'run':>4}{'[Nu]0/M':>9}{'rate0 / mol L-1 s-1':>22}")
    rates = {}
    for (s, run), (nu0, t, c) in sorted(data.items()):
        rates[(s, run)] = (nu0, initial_rate(t, c))
        print(f"{s:>9}{run:>4}{nu0:>9.2f}{rates[(s, run)][1]:>22.3e}")
    for s in ("A", "B"):
        (n1, r1), (n2, r2) = rates[(s, 1)], rates[(s, 2)]
        n = order_in_nucleophile(r1, n1, r2, n2)
        mech = "SN2 (rate depends on the nucleophile)" if n > 0.5 else "SN1 (rate independent of the nucleophile)"
        print(f"substrate {s}: order in nucleophile = {n:.2f} -> {mech}")
    stereo_demo()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.2), sharey=True)
    for ax, s in zip(axes, ("A", "B")):
        for run in (1, 2):
            nu0, t, c = data[(s, run)]
            ax.plot(t, c, "o-", ms=3, label=f"[Nu]0 = {nu0:.2f} M")
        ax.set_title(f"substrate {s}")
        ax.set_xlabel("t / s")
        ax.legend()
    axes[0].set_ylabel("[substrate] / mol L$^{-1}$")
    fig.tight_layout()
    fig.savefig(runs_dir() / "sn_runs.png", dpi=150)
    print("saved runs/sn_runs.png")


if __name__ == "__main__":
    main()
