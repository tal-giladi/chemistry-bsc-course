"""Shared helpers for the Module 16 labs (RDKit 2026.9.1; Python 3.14).
Keep this file in the same folder as the lesson scripts.

It holds three things:
  1. small utilities (CSV reader, canonical SMILES, hashed answer keys);
  2. REACTIONS: a small library of textbook reactions written as RDKit reaction SMARTS;
  3. check_step / check_route: a route checker used in lesson 16.7 (and for drills).

The reaction library is a teaching model. Each entry stands for one classic reagent set
(named in the "reagents" field). It knows nothing about yields, side products in the flask,
rates or solvents. It can tell you whether a step is the right KIND of change, whether an
aromatic substitution goes where the directing groups send it, and it knows a few classic
incompatibilities (Grignard reagents with O-H, Friedel-Crafts on deactivated rings)."""
from hashlib import sha256
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_KJ = 8.314462618e-3  # gas constant in kJ/(mol K), CODATA 2022


def read_csv(name):
    """Read a small CSV in this folder into a list of dicts. Lines starting with # are comments."""
    lines = [x for x in (HERE / name).read_text(encoding="utf-8").splitlines() if x and not x.startswith("#")]
    keys = lines[0].split(",")
    return [dict(zip(keys, x.split(","))) for x in lines[1:]]


def need_rdkit():
    try:
        import rdkit  # noqa: F401
    except ImportError:
        raise SystemExit("RDKit is missing. Install the course packages: "
                         "py -m pip install -r labs/common/requirements.txt")


need_rdkit()
from rdkit import Chem, RDLogger  # noqa: E402
from rdkit.Chem import AllChem  # noqa: E402

RDLogger.DisableLog("rdApp.*")  # keep the output readable; bad SMILES are reported by our own code


def runs_dir():
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    return out


def attempt(fn, *args, default="TODO"):
    """Call fn(*args); if it is still an unwritten exercise (NotImplementedError), return default."""
    try:
        return fn(*args)
    except NotImplementedError:
        return default


def mol(smiles):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise ValueError(f"RDKit cannot read the SMILES {smiles!r}")
    return m


def canon(smiles, stereo=False):
    """Canonical SMILES, or None if RDKit cannot read it. stereo=False drops wedges and E/Z,
    which is how the drills and the route checker compare structures."""
    m = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(m, isomericSmiles=stereo) if m is not None else None


def key(smiles):
    """Hash of the canonical SMILES (no stereo). Answer keys store these so the answer is not
    visible in the file; the worked answers are in the lesson's <details> blocks."""
    c = canon(smiles)
    return sha256(c.encode()).hexdigest()[:16] if c else None


def check_drill(answers, keys):
    """answers: {question: SMILES you wrote}; keys: {question: hash}. Prints a score."""
    right = 0
    for q, k in keys.items():
        a = (answers.get(q) or "").strip()
        if not a:
            print(f"  {q}: (no answer yet)")
            continue
        if canon(a) is None:
            print(f"  {q}: RDKit cannot read {a!r}; check brackets, ring numbers and valences")
            continue
        ok = key(a) == k
        right += ok
        print(f"  {q}: {'correct' if ok else 'not the expected product'}  ({canon(a)})")
    print(f"  score: {right}/{len(keys)}")
    return right


# ---------------------------------------------------------------------------------------------
# Reaction library. Each entry: reagents (what it stands for), a list of SMARTS templates, and
# the number of reactant molecules. Atom maps (:1, :2 ...) mark atoms that survive into the
# product; unmapped atoms on the left (leaving groups) disappear.
# ---------------------------------------------------------------------------------------------
ALD_KET = "[CX3;$([CH2]=O),$([CH1]([#6])=O),$(C([#6])([#6])=O)]"  # aldehyde or ketone carbon
REACTIONS = {
    "oxidise_mild": dict(reagents="PCC, Dess-Martin or Swern; stops at the aldehyde", n=1, templates=[
        "[CH2X4:1]([#6:2])[OX2H:3]>>[CH1:1]([#6:2])=[O:3]",
        "[CH3X4:1][OX2H:2]>>[CH2:1]=[O:2]",
        "[CH1X4:1]([#6:2])([#6:3])[OX2H:4]>>[C:1]([#6:2])([#6:3])=[O:4]"]),
    "oxidise_strong": dict(reagents="Jones (CrO3, H2SO4) or hot KMnO4", n=1, templates=[
        "[CH2X4:1]([#6:2])[OX2H:3]>>[C:1]([#6:2])(=[O:3])O",
        "[CH3X4:1][OX2H:2]>>[CH1:1](=[O:2])O",
        "[CH1X4:1]([#6:2])([#6:3])[OX2H:4]>>[C:1]([#6:2])([#6:3])=[O:4]",
        "[CX3H1:1]([#6:2])=[O:3]>>[C:1]([#6:2])(=[O:3])O",
        "[c:1][CH3:2]>>[c:1][C:2](=O)O"]),
    "reduce_nabh4": dict(reagents="NaBH4 in methanol; aldehydes and ketones only", n=1, templates=[
        ALD_KET[:-1] + ":1]=[OX1:2]>>[C:1][O:2]"]),
    "reduce_lialh4": dict(reagents="LiAlH4 in ether, then water; reduces almost every C=O", n=1, templates=[
        ALD_KET[:-1] + ":1]=[OX1:2]>>[C:1][O:2]",
        "[#6:1][CX3:2](=[OX1:3])[OX2][#6:4]>>[#6:1][C:2][O:3].[#6:4]O",
        "[#6:1][CX3:2](=[OX1:3])[OX2H]>>[#6:1][C:2][O:3]",
        "[#6:1][CX3:2](=[OX1])[NX3:3]>>[#6:1][C:2][N:3]",
        "[#6:1][CX2:2]#[NX1:3]>>[#6:1][C:2][N:3]"]),
    "hydrogenate_alkene": dict(reagents="H2, Pd/C, room temperature; C=C only", n=1, templates=[
        "[C:1]=[C:2]>>[C:1][C:2]"]),
    "grignard": dict(reagents="Mg in dry ether on the halide, then the carbonyl or epoxide, then aqueous acid", n=2, templates=[
        "[#6:1][Br,I,Cl].[CX3;$([CH2]=O),$([CH1]([#6])=O),$(C([#6])([#6])=O):2]=[OX1:3]>>[#6:1][C:2][O:3]",
        "[#6:1][Br,I,Cl].[CX4:2]1[CX4:3][OX2:4]1>>[#6:1][C:2][C:3][O:4]"]),
    "carboxylation": dict(reagents="Mg in dry ether, then CO2 (dry ice), then aqueous acid", n=1, templates=[
        "[#6:1][Br,I,Cl]>>[#6:1]C(=O)O"]),
    "wittig": dict(reagents="PPh3 on the halide, then BuLi (ylide), then the aldehyde or ketone", n=2, templates=[
        "[CX3;$([CH2]=O),$([CH1]([#6])=O),$(C([#6])([#6])=O):1]=[OX1].[CX4;!H0:2][Br,I,Cl]>>[C:1]=[C:2]"]),
    "pbr3": dict(reagents="PBr3 (or HBr for tertiary alcohols)", n=1, templates=[
        "[CX4:1][OX2H]>>[C:1]Br"]),
    "dehydrate": dict(reagents="H2SO4 or H3PO4, heat (E1)", n=1, templates=[
        "[CX4;!H0:1][CX4:2][OX2H]>>[C:1]=[C:2]"]),
    "williamson": dict(reagents="NaH on the alcohol (alkoxide), then a methyl or primary halide (SN2)", n=2, templates=[
        "[OX2H:1][#6:2].[CH3X4,CH2X4:3][Br,I,Cl]>>[#6:2][O:1][C:3]"]),
    "fischer_ester": dict(reagents="alcohol in excess, H2SO4 catalyst, heat", n=2, templates=[
        "[CX3:1](=[OX1:2])[OX2H].[OX2H:3][CX4:4]>>[C:1](=[O:2])[O:3][C:4]"]),
    "acid_chloride": dict(reagents="SOCl2", n=1, templates=[
        "[CX3:1](=[OX1:2])[OX2H]>>[C:1](=[O:2])Cl"]),
    "acylation": dict(reagents="acid chloride or anhydride with an alcohol, phenol or amine (pyridine or base)", n=2, templates=[
        "[CX3:1](=[OX1:2])[Cl,Br].[OX2H,NX3;H1,H2,H3;!$(N[C,S]=O):3]>>[C:1](=[O:2])[*:3]",
        "[CX3:1](=[OX1:2])[OX2][CX3]=[OX1].[OX2H,NX3;H1,H2,H3;!$(N[C,S]=O):3]>>[C:1](=[O:2])[*:3]"]),
    "ester_hydrolysis": dict(reagents="NaOH in water, heat (saponification), then acid", n=1, templates=[
        "[#6:1][CX3:2](=[OX1:3])[OX2:4][#6:5]>>[#6:1][C:2](=[O:3])O.[#6:5][O:4]"]),
    "acetal_protect": dict(reagents="ethylene glycol, TsOH catalyst, remove water", n=1, templates=[
        "[CX3;$([CH1]([#6])=O),$(C([#6])([#6])=O):1]=[OX1]>>[C:1]1OCCO1"]),
    "acetal_deprotect": dict(reagents="aqueous acid", n=1, templates=[
        "[CX4:1]1[OX2][CH2][CH2][OX2]1>>[C:1]=O"]),
    "reductive_amination": dict(reagents="amine, then NaBH3CN (or H2, Ni)", n=2, templates=[
        "[CX3;$([CH2]=O),$([CH1]([#6])=O),$(C([#6])([#6])=O):1]=[OX1].[NX3;H1,H2,H3;!$(N[C,S]=O);!$(Nc):2]>>[C:1][N:2]"]),
    "aldol_addition": dict(reagents="NaOH (or LDA) at low temperature", n=2, templates=[
        "[CX3;!$(C[O,N,S,Cl]):1](=[OX1:2])[CX4;!H0:3].[CX3;$([CH2]=O),$([CH1]([#6])=O):4]=[OX1:5]>>[C:1](=[O:2])[C:3][C:4][O:5]"]),
    "aldol_condensation": dict(reagents="NaOH, heat (addition, then E1cB loss of water)", n=2, templates=[
        "[CX3;!$(C[O,N,S,Cl]):1](=[OX1:2])[CX4;H2,H3:3].[CX3;$([CH2]=O),$([CH1]([#6])=O):4]=[OX1]>>[C:1](=[O:2])[C:3]=[C:4]"]),
    "enolate_alkylation": dict(reagents="LDA at -78 C (or NaOEt for 1,3-dicarbonyls), then a methyl or primary halide", n=2, templates=[
        "[CX3;!$(C[OH]):1](=[OX1:2])[CX4;!H0:3].[CH3X4,CH2X4:4][Br,I,Cl]>>[C:1](=[O:2])[C:3][C:4]"]),
    "decarboxylate": dict(reagents="aqueous acid, heat (beta-keto acid or malonic acid)", n=1, templates=[
        "[CX3:1](=[OX1:2])[CX4:3][CX3](=[OX1])[OX2H]>>[C:1](=[O:2])[C:3]"]),
    "nitration": dict(reagents="HNO3, H2SO4", n=1, templates=["[cH:1]>>[c:1][N+](=O)[O-]"]),
    "bromination_arene": dict(reagents="Br2, FeBr3", n=1, templates=["[cH:1]>>[c:1]Br"]),
    "fc_acylation": dict(reagents="acid chloride (or anhydride), AlCl3", n=2, templates=[
        "[cH:1].[CX3:2](=[OX1:3])[Cl]>>[c:1][C:2]=[O:3]"]),
    "nitro_reduction": dict(reagents="Fe or Sn with HCl, then base (or H2, Pd/C)", n=1, templates=[
        "[#6:1][N+](=O)[O-]>>[#6:1]N"]),
}
EAS = {"nitration", "bromination_arene", "fc_acylation"}

# Substituent classes for directing effects, tested on the atom attached to the ring.
# Strength: the strongest activator on a ring decides where the next group goes.
DIRECTORS = [  # (name, SMARTS for ring carbon + first substituent atom, kind, strength)
    ("O-H / O-R / O-", "c[OX2H,OX2;!$(OC=O),OX1-]", "op", 4),
    ("NH2 / NHR / NR2", "c[NX3;!$(N[C,S]=O);!$(N=O);!$([N+])]", "op", 4),
    ("NHC(=O)R / OC(=O)R", "c[$([NX3]C=O),$([OX2]C=O)]", "op", 3),
    ("alkyl / aryl", "c[CX4,c]", "op", 2),
    ("halogen", "c[F,Cl,Br,I]", "op", 1),
    ("C=O / CO2H / CO2R / CHO", "c[CX3]=O", "meta", 0),
    ("NO2", "c[N+](=O)[O-]", "meta", 0),
    ("C#N", "cC#N", "meta", 0),
    ("SO3H", "cS(=O)(=O)O", "meta", 0),
    ("CF3 / CCl3", "cC(F)(F)F", "meta", 0),
]


def substituents(m, ring):
    """List (ring atom index, director name, kind, strength) for substituents on a benzene ring."""
    out = []
    ring_set = set(ring)
    for name, smarts, kind, strength in DIRECTORS:
        for c, x, *_ in m.GetSubstructMatches(Chem.MolFromSmarts(smarts)):
            if c in ring_set and x not in ring_set and not any(o[0] == c for o in out):
                out.append((c, name, kind, strength))
    # catch-all for anything else attached to the ring (counts as a weak o/p group)
    for c in ring:
        for nb in m.GetAtomWithIdx(c).GetNeighbors():
            if nb.GetIdx() not in ring_set and not any(o[0] == c for o in out):
                out.append((c, "other", "op", 2))
    return out


def ring_distance(ring, a, b):
    i, j = ring.index(a), ring.index(b)
    d = abs(i - j)
    return min(d, len(ring) - d)  # 1 ortho, 2 meta, 3 para


def benzene_rings(m):
    return [list(r) for r in m.GetRingInfo().AtomRings()
            if len(r) == 6 and all(m.GetAtomWithIdx(i).GetIsAromatic() and m.GetAtomWithIdx(i).GetSymbol() == "C" for i in r)]


def eas_judgement(reactant, site):
    """Is aromatic substitution at atom index `site` of `reactant` what the ring's substituents
    direct? Returns (ok, message)."""
    rings = [r for r in benzene_rings(reactant) if site in r]
    if not rings:
        return False, "the site is not on a benzene ring"
    ring = rings[0]
    subs = substituents(reactant, ring)
    if not subs:
        return True, "unsubstituted ring: every position is the same"
    top = max(s[3] for s in subs)
    leaders = [s for s in subs if s[3] == top]
    words = {1: "ortho", 2: "meta", 3: "para"}
    verdicts = []
    for c, name, kind, _ in leaders:
        d = ring_distance(ring, c, site)
        wanted = (1, 3) if kind == "op" else (2,)
        verdicts.append((d in wanted, f"{words[d]} to {name} ({'o/p' if kind == 'op' else 'meta'} director)"))
    crowded = sum(1 for s in subs if ring_distance(ring, s[0], site) == 1) >= 2
    ok = any(v for v, _ in verdicts)
    msg = "; ".join(t for _, t in verdicts)
    if ok and crowded:
        msg += "; WARNING: squeezed between two groups, usually a minor product"
    return ok, msg


def warnings_for(name, reactants):
    """Classic incompatibilities the template alone cannot see."""
    w = []
    smarts = lambda s: Chem.MolFromSmarts(s)  # noqa: E731
    if name in ("grignard", "carboxylation"):
        halide = next((r for r in reactants if r.HasSubstructMatch(smarts("[#6][Br,I,Cl]"))), None)
        if halide is not None and halide.HasSubstructMatch(smarts("[$([OX2H]),$([NX3;!H0]),$([CX3]=O),$([CX2]#N),$([N+](=O)[O-])]")):
            w.append("FAIL: the halide also carries O-H, N-H, C=O, C#N or NO2; the Grignard reagent "
                     "would destroy itself or its neighbour. Protect or change the order.")
        partners = [r for r in reactants if r is not halide]
        if any(p.HasSubstructMatch(smarts("[$([OX2H]),$([NX3;!H0]),$([N+](=O)[O-])]")) for p in partners):
            w.append("FAIL: the other reactant carries O-H, N-H or NO2, which the Grignard reagent attacks "
                     "(or is protonated by) before it reaches the C=O. Protect or change the order.")
    if name == "fc_acylation":
        for r in reactants:
            if r.HasSubstructMatch(smarts("c")):
                if r.HasSubstructMatch(smarts("c[$([CX3]=O),$([N+](=O)[O-]),$(C#N),$(S(=O)=O),$(C(F)(F)F)]")):
                    w.append("FAIL: Friedel-Crafts does not work on a ring with a meta-directing (deactivating) group.")
                if r.HasSubstructMatch(smarts("c[NX3;!$(N[C,S]=O);!$([N+]);!$(N=O)]")):
                    w.append("FAIL: the amine binds AlCl3 and turns into a strongly deactivating group.")
    if name == "nitration" and reactants[0].HasSubstructMatch(smarts("c[NX3;H2,H1;!$(NC=O)]")):
        w.append("FAIL: free anilines are oxidised by nitric acid (and protonated to meta-directing anilinium). "
                 "Acetylate the NH2 first.")
    if name == "hydrogenate_alkene" and reactants[0].HasSubstructMatch(smarts("[N+](=O)[O-]")):
        w.append("WARNING: H2 over Pd also reduces nitro groups.")
    if name == "williamson" and any(r.HasSubstructMatch(smarts("[CX4;H0,H1;!$([CH1]=*)][Br,I,Cl]")) for r in reactants):
        w.append("FAIL: secondary or tertiary halide with an alkoxide gives mostly E2 elimination.")
    return w


def run_reaction(name, reactant_smiles):
    """Apply library reaction `name` to the reactants in every order.
    Returns list of (product canonical SMILES set, reactant mol used first, site atom index or None)."""
    rx = REACTIONS[name]
    mols = [mol(s) for s in reactant_smiles]
    outcomes = []
    for t in rx["templates"]:
        r = AllChem.ReactionFromSmarts(t)
        if r.GetNumReactantTemplates() != len(mols):
            continue
        for order in permutations(range(len(mols))):
            ordered = tuple(mols[i] for i in order)
            for prods in r.RunReactants(ordered):
                smis = []
                site = None
                ok = True
                for p in prods:
                    try:
                        Chem.SanitizeMol(p)
                    except Exception:
                        ok = False
                        break
                    for a in p.GetAtoms():
                        if a.HasProp("old_mapno") and a.GetIntProp("old_mapno") == 1 and a.HasProp("react_atom_idx"):
                            site = a.GetIntProp("react_atom_idx")
                    smis.append(Chem.MolToSmiles(p, isomericSmiles=False))
                if ok:
                    outcomes.append((set(canon(s) for s in smis), ordered[0], site))
    return outcomes


def check_step(name, reactant_smiles, product_smiles):
    """Check one step. Returns (ok, list of message lines)."""
    if name not in REACTIONS:
        return False, [f"unknown reaction {name!r}; choose from: {', '.join(sorted(REACTIONS))}"]
    if len(reactant_smiles) != REACTIONS[name]["n"]:
        return False, [f"{name} takes {REACTIONS[name]['n']} reactant(s), you gave {len(reactant_smiles)}"]
    try:
        mols = [mol(s) for s in reactant_smiles]
        target = canon(product_smiles)
        if target is None:
            raise ValueError(f"RDKit cannot read the product SMILES {product_smiles!r}")
    except ValueError as e:
        return False, [str(e)]
    msgs = warnings_for(name, mols)
    hits = [o for o in run_reaction(name, reactant_smiles) if target in o[0]]
    if not hits:
        return False, msgs + [f"{name} ({REACTIONS[name]['reagents']}) does not turn these reactants into {target}"]
    if name in EAS:
        judged = [eas_judgement(o[1], o[2]) for o in hits]
        good = [j for j in judged if j[0]]
        if not good:
            return False, msgs + [f"wrong position: {judged[0][1]}"]
        msgs.append(f"position: {good[0][1]}")
    fail = any(m.startswith("FAIL") for m in msgs)
    return not fail, msgs


def read_route(path):
    """Route file: one step per line, 'step; reaction; reactant SMILES joined by .; product SMILES'.
    Lines starting with # are comments."""
    steps = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split(";")]
        if len(parts) != 4:
            raise ValueError(f"cannot read route line (need 4 fields separated by ;): {line!r}")
        steps.append((parts[0], parts[1], parts[2].split("."), parts[3]))
    return steps


def check_route(steps, target, catalogue, verbose=True):
    """steps: list of (label, reaction, [reactant SMILES], product SMILES).
    Every reactant must be in the catalogue (set of canonical SMILES) or made in an earlier step.
    Returns True if every step passes and the last product is the target."""
    made = set()
    all_ok = True
    for label, name, reactants, product in steps:
        ok, msgs = check_step(name, reactants, product)
        for r in reactants:
            c = canon(r)
            if c is not None and c not in catalogue and c not in made:
                ok = False
                msgs.append(f"FAIL: {c} is neither in starting_materials.csv nor made in an earlier step")
        if verbose:
            print(f"  step {label}: {name:20s} -> {canon(product)}  {'OK' if ok else 'PROBLEM'}")
            for m in msgs:
                print(f"      {m}")
        all_ok &= ok
        c = canon(product)
        if c:
            made.add(c)
    reached = bool(steps) and canon(steps[-1][3]) == canon(target)
    if verbose:
        print(f"  target {canon(target)} {'reached' if reached else 'NOT reached by the last step'}; "
              f"{len(steps)} step(s); route {'passes' if all_ok and reached else 'needs work'}")
    return all_ok and reached


def catalogue():
    return {canon(r["smiles"]) for r in read_csv("starting_materials.csv")}
