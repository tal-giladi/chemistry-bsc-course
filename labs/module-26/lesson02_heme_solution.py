"""Lesson 26.2 - the haem iron: spin state, size and where it sits in the porphyrin.

Reference solution. Run:  py lesson02_heme_solution.py
Reads data/2DN2_sites.pdb (deoxy-haemoglobin), 2DN1_sites.pdb (oxy-haemoglobin), 1A6M_sites.pdb
(oxy-myoglobin). Writes runs/lesson02_heme.png.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bio26 import read_pdb, runs_dir

PORPHYRIN_N = ("NA", "NB", "NC", "ND")


def unpaired_octahedral(d, low_spin):
    """Unpaired electrons for d^n in an octahedral field (t2g holds 6, eg holds 4), as in lesson 18.4."""
    order = [0, 1, 2, 0, 1, 2, 3, 4, 3, 4] if low_spin else [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    occ = [0] * 5
    for k in range(d):
        occ[order[k]] += 1
    return sum(1 for o in occ if o == 1)


def spin_only_moment(n):
    """Spin-only magnetic moment in Bohr magnetons: sqrt(n (n + 2))."""
    return math.sqrt(n * (n + 2))


def out_of_plane(fe, n4, his):
    """Signed distance (angstrom) of Fe from the best plane through the four porphyrin N atoms,
    positive towards the proximal histidine."""
    N = np.array(n4)
    c = N.mean(axis=0)
    normal = np.linalg.svd(N - c)[2][2]
    d = float((fe - c) @ normal)
    return -d if (his - c) @ normal < 0 else d


def heme_sites(path):
    """One dict per haem: chain, Fe-N(porphyrin) mean, Fe-N(His), Fe-O2 (or None), out-of-plane."""
    atoms = read_pdb(path)
    out = []
    for fe in (a for a in atoms if a["el"] == "FE"):
        ring = [a for a in atoms if a["res"] == "HEM" and a["chain"] == fe["chain"] and a["num"] == fe["num"]
                and a["name"] in PORPHYRIN_N]
        near = lambda a: np.linalg.norm(a["xyz"] - fe["xyz"])
        his = min((a for a in atoms if a["res"] == "HIS" and a["name"] in ("NE2", "ND1")), key=near)
        o2 = sorted((a for a in atoms if a["res"] == "OXY" and a["chain"] == fe["chain"] and near(a) < 3.2), key=near)
        angle = None
        if len(o2) == 2:
            v1, v2 = fe["xyz"] - o2[0]["xyz"], o2[1]["xyz"] - o2[0]["xyz"]
            angle = math.degrees(math.acos(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2)))
        out.append(dict(chain=fe["chain"], fe_np=np.mean([near(a) for a in ring]), fe_his=near(his),
                        fe_o=near(o2[0]) if o2 else None, angle=angle,
                        oop=out_of_plane(fe["xyz"], [a["xyz"] for a in ring], his["xyz"])))
    return out


def main():
    if unpaired_octahedral(6, False) is None or spin_only_moment(4) is None or \
            out_of_plane(np.zeros(3), [np.array(v, float) for v in ((1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0))], np.array([0, 0, -1.0])) is None:
        print("TODO: write unpaired_octahedral(), spin_only_moment() and out_of_plane() first.")
        return
    print("Spin states of haem iron (octahedral approximation):")
    for name, d, ls in (("deoxy Fe(II), 5-coordinate", 6, False), ("oxy / carbonmonoxy Fe(II)", 6, True),
                        ("met Fe(III) with water", 5, False), ("met Fe(III) with cyanide", 5, True)):
        n = unpaired_octahedral(d, ls)
        print(f"  {name:28s} d{d} {'low ' if ls else 'high'} spin: {n} unpaired, mu = {spin_only_moment(n):.2f} BM")

    rows = []
    for path, title in (("2DN2_sites.pdb", "deoxy-Hb"), ("2DN1_sites.pdb", "oxy-Hb"), ("1A6M_sites.pdb", "oxy-Mb")):
        for s in heme_sites(path):
            rows.append((title, s))
    print("\nstructure  chain  Fe-N(por)  Fe-N(His)  Fe-O   Fe-O-O  Fe out of plane (towards His)")
    for title, s in rows:
        fo = f"{s['fe_o']:.2f}" if s["fe_o"] else "  -  "
        an = f"{s['angle']:4.0f} " if s["angle"] else "  -  "
        print(f"  {title:9s} {s['chain']}     {s['fe_np']:.2f}       {s['fe_his']:.2f}      {fo}  {an}   {s['oop']:+.2f} A")
    deoxy = [s["oop"] for t, s in rows if t == "deoxy-Hb"]
    oxy = [s["oop"] for t, s in rows if t != "deoxy-Hb"]
    print(f"\nmean out-of-plane: deoxy {np.mean(deoxy):+.2f} A, oxy {np.mean(oxy):+.2f} A, "
          f"shift on binding O2 = {np.mean(deoxy) - np.mean(oxy):.2f} A")

    fig, ax = plt.subplots(figsize=(6, 3.5))
    labels = [f"{t} {s['chain']}" for t, s in rows]
    ax.bar(labels, [s["oop"] for _, s in rows], color=["#b5523b" if t == "deoxy-Hb" else "#3b6fb5" for t, _ in rows])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Fe out of N4 plane (angstrom)")
    ax.set_title("Haem iron moves into the ring when O2 binds")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(runs_dir() / "lesson02_heme.png", dpi=120)
    print("wrote runs/lesson02_heme.png")


if __name__ == "__main__":
    main()
