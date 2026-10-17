---
id: "26.1"
module: 26
minutes: 20
practice_minutes: 70
prerequisites: ["18.3", "06.2", "13.6"]
objectives:
  - Name the bulk and trace metals of living cells and give one job for each of Na, K, Mg, Ca, Fe, Zn and Cu.
  - Calculate the free Fe³⁺ concentration at pH 7 from the solubility product of Fe(OH)₃ and explain why organisms need siderophores and storage proteins.
  - Use hard–soft acid–base reasoning and the Irving–Williams series to predict which donor atoms and which sites suit a given metal ion.
  - Read the donor set and coordination number of a metal site from a Protein Data Bank structure.
volatility: concept
sources:
  - title: "Bertini, Gray, Lippard and Valentine, Bioinorganic Chemistry (LibreTexts), 1.3 Chemical Properties Relative to Storage and Transport"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/01%3A_Transition-Metal_Storage_Transport_and_Biomineralization/1.03%3A_Chemical_Properties_Relative_to_Storage_and_Transport
  - title: "Bertini et al., Bioinorganic Chemistry (LibreTexts), 1.5 Transport of Iron"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/01%3A_Transition-Metal_Storage_Transport_and_Biomineralization/1.05%3A_Transport_of_Iron
  - title: "Open University OpenLearn, Iron transport and storage, 3.1 How do organisms take up iron?"
    url: https://www.open.edu/openlearn/science-maths-technology/chemistry/iron-transport-and-storage/content-section-3.1
  - title: "Irving and Williams (1953), The stability of transition-metal complexes, J. Chem. Soc. 3192"
    url: https://doi.org/10.1039/JR9530003192
  - title: "RCSB Protein Data Bank entries 1A6M, 3KS3, 1CLL and 1PLC"
    url: https://www.rcsb.org/structure/3KS3
  - title: "Royal Society of Chemistry Education, Extracting iron from breakfast cereal"
    url: https://edu.rsc.org/experiments/extracting-iron-from-breakfast-cereal/393.article
last_verified: "2026-10-17"
---

# 26.1 · Metals in biology: why these elements

About a third of all proteins need a metal ion to work. Iron carries oxygen and moves electrons, zinc holds water ready to attack carbon dioxide, calcium tells a muscle when to contract, and copper hands electrons along in photosynthesis. This lesson asks why life picked these particular elements, how it gets hold of them when they are scarce, and how a protein makes sure the right metal ends up in the right site. It uses the coordination chemistry of Module 18, starting with the donor atoms and coordination numbers of lesson [18.3](../module-18/lesson-03.md), and the protein structures of lesson [06.2](../module-06/lesson-02.md).

## Why it matters

Iron is the fourth most abundant element in the Earth's crust, yet iron deficiency is the world's most common nutritional deficiency. The problem is not how much iron there is but how little of it dissolves. Understanding this explains why a bacterium makes a molecule that binds iron(III) with a constant near $10^{49}$, why cereal makers add metallic iron powder, and why a zinc enzyme stops working if copper gets into its site. The same reasoning guides the design of metal drugs, contrast agents and sensors: you choose the metal and the donor atoms together.

## Core ideas

> [!NOTE]
> The chemistry here is stable. The numbers (Ksp of Fe(OH)₃, body iron, the enterobactin constant) come from the LibreTexts edition of Bertini et al. and the Open University, checked 2026-10-17. The structures are PDB entries checked on the RCSB site the same day; the lab code uses NumPy 2.5 as pinned in `labs/common/requirements.txt`.

### Bulk metals and trace metals

Two groups of metal ions do very different jobs.

- **Bulk metals**: Na⁺, K⁺, Mg²⁺ and Ca²⁺, present at millimolar levels. Na⁺ and K⁺ carry charge across membranes and set the membrane potential (lesson [06.1](../module-06/lesson-01.md)). Mg²⁺ sits on almost every ATP molecule in a cell. Ca²⁺ is a signal: the cytosol keeps it near 0.1 µM while the outside of the cell has about 1 mM, so opening a channel for a moment raises the inside concentration tenfold or more.
- **Trace metals**: Fe, Zn, Cu, Mn, Co, Mo and Ni (plus V and Cr in a few organisms), present at micromolar levels or below, almost all bound to proteins. They do chemistry: redox, Lewis-acid catalysis, binding small molecules such as O₂, N₂ and CO₂.

An adult human holds 3 to 5 g of iron. About 65 % of it is in haemoglobin, 6 % in myoglobin and most of the rest in the storage proteins ferritin and haemosiderin. Only a tiny fraction is in transit at any moment.

### Why these elements: what each one is good at

The choice follows from properties you met in Modules 8 and 18.

| Ion | Property that matters | Typical job |
|---|---|---|
| Na⁺, K⁺ | weak, fast binding; different sizes | charge carriers, osmotic balance |
| Mg²⁺ | small, hard, binds phosphate | ATP and nucleic-acid chemistry |
| Ca²⁺ | larger, flexible coordination (6–8), fast exchange | signalling, bone and shell |
| Zn²⁺ | d¹⁰: no redox, no CFSE preference for a geometry, strong Lewis acid | hydrolysis, CO₂ hydration, structure (zinc fingers) |
| Fe²⁺/Fe³⁺ | two common oxidation states; potential tunable from −0.4 to +0.4 V | O₂ binding, electron transfer, oxidation |
| Cu⁺/Cu²⁺ | high potentials, fast electron transfer | electron transfer, O₂ chemistry |

Zinc is a good catalyst because it cannot be oxidised or reduced in a cell: it will never start unwanted radical chemistry, and because a d¹⁰ ion has no crystal-field stabilisation (lesson [18.4](../module-18/lesson-04.md)) it accepts four, five or six ligands with little cost. Iron is the opposite: its value is redox. Bertini lists Fe³⁺/Fe²⁺ potentials from −0.40 V in ferredoxins to +0.35 V in HIPIP proteins, against +0.77 V for the aqua ion. The protein shifts the potential by more than a volt by choosing the ligands and the surroundings.

### Availability: the iron problem

Before oxygen built up in the atmosphere, about 2.4 billion years ago, iron in the oceans was Fe²⁺, which is soluble. Oxygen turned it into Fe³⁺, which precipitates as the hydroxide. With $K_{sp} = [\mathrm{Fe^{3+}}][\mathrm{OH^-}]^3 \approx 10^{-39}$ (lesson [13.6](../module-13/lesson-06.md) for solubility products):

$$[\mathrm{Fe^{3+}}] = \frac{K_{sp}}{[\mathrm{OH^-}]^3} = \frac{10^{-39}}{(10^{-7})^3} = 10^{-18}\ \mathrm{M} \quad \text{at pH 7}$$

That is far too little to supply a cell (see the worked example). Organisms solve it in three ways:

1. **Siderophores**: small chelating molecules that bacteria and fungi release to grab Fe³⁺. Enterobactin, from *E. coli*, uses three catecholate groups, six hard oxygen donors in an octahedron, and has a formation constant of about $10^{49}$ for the fully deprotonated ligand, the highest known. The cell then takes up the whole complex.
2. **Transport proteins**: in our blood, transferrin carries two Fe³⁺ ions, one per lobe.
3. **Storage**: ferritin keeps iron as a hydrated iron(III) oxide core inside a protein shell, so that iron is safe from the Fenton chemistry of free Fe²⁺ with H₂O₂ but available when needed.

### Matching metal to site: hard, soft and Irving–Williams

**Hard–soft acid–base (HSAB)** reasoning: small, highly charged ions (hard acids such as Mg²⁺, Ca²⁺, Fe³⁺) prefer hard, oxygen donors such as carboxylate, phenolate and phosphate. Large, polarisable ions of low charge (soft acids such as Cu⁺) prefer soft donors such as the sulfur of cysteine and methionine. Borderline ions (Fe²⁺, Zn²⁺, Cu²⁺, Ni²⁺) like nitrogen, especially the imidazole of histidine.

The **Irving–Williams series** (1953) orders the stability of high-spin complexes of the divalent first-row ions, almost independently of the ligand:

$$\mathrm{Mn^{2+} < Fe^{2+} < Co^{2+} < Ni^{2+} < Cu^{2+} > Zn^{2+}}$$

The rise comes from shrinking ionic radius and growing ligand-field stabilisation; the peak at Cu²⁺ is the extra Jahn–Teller stabilisation (lesson 18.4). This creates a real danger: in a free competition, Cu²⁺ would beat Zn²⁺ for almost any site. Cells avoid this by keeping free copper extremely low with chaperone proteins that deliver each copper ion directly to its target, and by shaping sites (geometry, number and type of donors) that favour the intended metal.

### Reading a metal site

A metal site is described by its **donor set** (which atoms bind, for example N₃O) and its **coordination number**. You find them by measuring distances in a crystal structure: a bond is a donor atom within about 2.0–2.5 Å of the metal (up to about 2.9 Å for Ca²⁺ and for sulfur donors). Four sites you will examine:

- Oxy-myoglobin (PDB 1A6M): Fe with four porphyrin N, one histidine N and O₂, octahedral.
- Carbonic anhydrase II (3KS3): Zn with three histidine N and one water, tetrahedral; the water is the reactive group (lesson 26.4).
- Calmodulin (1CLL): four Ca²⁺ sites, each with seven oxygen donors from aspartate, asparagine, glutamate, a backbone carbonyl and water.
- Plastocyanin (1PLC): Cu with two histidines, one cysteine and a long bond to methionine sulfur, a distorted tetrahedron (lesson [26.2](lesson-02.md)).

## Worked example

### 1. How many free Fe³⁺ ions are in a bacterium?

A bacterium has a volume of about 1 fL ($10^{-15}$ L). At pH 7 the free Fe³⁺ is $10^{-18}$ M.

1. Moles: $10^{-18}\ \mathrm{mol\,L^{-1}} \times 10^{-15}\ \mathrm{L} = 10^{-33}$ mol.
2. Ions: $10^{-33} \times 6.022 \times 10^{23} = 6.0 \times 10^{-10}$.
3. So on average one free Fe³⁺ ion would be found in one cell out of $1.7 \times 10^9$. A cell that needs thousands of iron atoms for its enzymes cannot wait for free ions; it must fetch iron with a chelator.

### 2. Can enterobactin dissolve rust?

Combine the dissolution and the binding (Hess's law for equilibria, lesson 13.6), writing L for fully deprotonated enterobactin:

$$\mathrm{Fe(OH)_3(s) + L^{6-} \rightleftharpoons FeL^{3-} + 3\,OH^-} \qquad K = K_{sp} K_f = 10^{-39} \times 10^{49} = 10^{10}$$

At pH 7, $[\mathrm{OH^-}]^3 = 10^{-21}$, so

$$\frac{[\mathrm{FeL}]}{[\mathrm{L}]} = \frac{K}{[\mathrm{OH^-}]^3} = \frac{10^{10}}{10^{-21}} = 10^{31}$$

Every ligand molecule ends up loaded with iron. The real ratio is smaller because the catecholate oxygens are partly protonated at pH 7, which costs many powers of ten, but the conclusion stands: a strong enough chelator can pull iron out of a solid hydroxide.

## Hands-on

What you need: Python with the course packages and the [Module 26 lab folder](../../labs/module-26/); for Part B an iron-fortified breakfast cereal whose label lists "iron" or "reduced iron", a strong magnet (a neodymium fridge magnet is ideal), a zip-lock bag, a rolling pin or spoon and water. Record Part B on the [notebook page template](../../templates/notebook-page.md). Time: about 70 minutes.

### Part A — Python: donor sets of four real metal sites (25 min)

1. Open `lesson01_metal_sites.py` and complete `distance()`, `donors()` and `free_fe3()`.
2. Run it:

```bash
py lesson01_metal_sites.py
```

3. For each site, write down the coordination number and donor set. Which site uses only oxygen, which uses sulfur, and why does that fit HSAB?
4. Look at one site in 3D: open the RCSB page of [3KS3](https://www.rcsb.org/structure/3KS3), start Mol* as in lesson 06.2, and click the zinc ion to see its three histidines and the water.

How you know it worked: myoglobin Fe has CN 6 (N₅O, Fe–O 1.81 Å); carbonic anhydrase Zn has CN 4 (three His N near 2.03 Å, water O at 1.90 Å); each of the four calmodulin Ca²⁺ ions has CN 7, all oxygen, at 2.1–2.6 Å; plastocyanin Cu has N₂S₂ with Cu–S(Met) 2.82 Å, longer than Cu–S(Cys) 2.07 Å. Free Fe³⁺ is $10^{-3}$ M at pH 2 and $10^{-18}$ M at pH 7.

<details><summary>Reference solution</summary>

```python
def distance(a, b):
    return float(np.linalg.norm(a["xyz"] - b["xyz"]))

def donors(atoms, metal):
    cut = CUTOFF.get(metal["el"], CUTOFF["default"])
    out = []
    for a in atoms:
        if a is metal or a["el"] not in ("N", "O", "S"):
            continue
        d = distance(a, metal)
        if d < (max(cut, CUTOFF_S) if a["el"] == "S" else cut):
            out.append((a, d))
    return sorted(out, key=lambda t: t[1])

def free_fe3(pH, ksp=1e-39, kw=1e-14):
    oh = kw / 10 ** (-pH)
    return ksp / oh ** 3
```

Full code: `lesson01_metal_sites_solution.py`. Ca²⁺ is hard and binds only carboxylate, carbonyl and water oxygens. Cu in plastocyanin binds the soft sulfurs of Cys and Met as well as two borderline histidine nitrogens, which suits a site that cycles between Cu⁺ (soft) and Cu²⁺ (borderline).

</details>

### Part B — kitchen: metallic iron in breakfast cereal (30 min)

> [!WARNING]
> Strong neodymium magnets pinch skin hard when they snap together, and two swallowed magnets can join through the gut wall, a medical emergency. Keep magnets, and the bag of cereal with a magnet in it, away from small children. Do not eat the cereal after the experiment; throw it away.

1. Read the label. You need a cereal that lists "iron", "reduced iron" or "electrolytic iron". If it lists only ferrous fumarate or ferrous sulfate, the iron is an ionic salt and a magnet will not collect it; that is a valid result to record.
2. Put one serving (about 50 g) in the zip-lock bag, crush it to a fine powder, add enough warm water to make a thin slurry and seal the bag.
3. Lay the bag flat. Hold the magnet against the outside, and slowly slosh the slurry past it for 2–3 minutes.
4. Keep the magnet in place and tilt the bag so the slurry runs away from it. Look for a small dark grey patch at the magnet.

How you know it worked: a tiny grey-black patch of iron powder collects under the magnet and follows it when you slide it along the bag. Manufacturers use metallic iron powder because, unlike Fe²⁺ salts, it does not speed up rancidity or change the taste. Your stomach acid turns it into Fe²⁺ before it can be absorbed. This part shows what "iron" on a label can mean; it does not measure how much the body takes up.

### Part C — pencil (15 min)

1. At what pH would free Fe³⁺ in equilibrium with Fe(OH)₃ reach 1 µM?
2. A protein site has two cysteines and two histidines. Which of Ca²⁺, Zn²⁺ or Mg²⁺ will it bind best, and why?

<details><summary>Answers</summary>

1. $[\mathrm{OH^-}]^3 = 10^{-39}/10^{-6} = 10^{-33}$, so $[\mathrm{OH^-}] = 10^{-11}$ M, pOH 11, pH 3. Iron(III) is soluble only in acid.
2. Zn²⁺: a borderline acid that likes N and S donors; this Cys₂His₂ set is the classic zinc finger. Ca²⁺ and Mg²⁺ are hard and prefer oxygen.

</details>

## Common mistakes

- Equating abundance with availability. Iron is abundant in rock but almost insoluble as Fe³⁺ at pH 7.
- Using a $K_f$ or $K_{sp}$ as if it applied at any pH. Protonation of the ligand and hydrolysis of the metal change effective constants by many powers of ten.
- Reading the Irving–Williams series as "copper is the best biological metal". It says Cu²⁺ binds most strongly, which is exactly why cells keep free copper close to zero.
- Counting every nearby atom as a ligand. Use a sensible cutoff (about 2.5 Å, 2.9 Å for Ca²⁺ and sulfur) and check the geometry; second-shell waters and hydrogen-bond partners are not ligands.
- Treating zinc as a redox metal. Zn²⁺ is d¹⁰ and stays Zn²⁺ in cells; its job is Lewis acidity and structure.

## Key takeaways

- Bulk metals (Na, K, Mg, Ca) carry charge, signal and bind phosphate; trace metals (Fe, Zn, Cu, Mn, Co, Mo, Ni) do chemistry inside proteins.
- Each element is chosen for its chemistry: zinc for redox-free Lewis acidity, iron and copper for tunable redox potentials.
- At pH 7 free Fe³⁺ is about $10^{-18}$ M; siderophores ($K_f \approx 10^{49}$ for enterobactin), transferrin and ferritin get, carry and store it.
- HSAB matches donors to metals (hard Ca²⁺ with O, soft Cu⁺ with S, borderline Zn²⁺ with N and S); the Irving–Williams series warns that Cu²⁺ outcompetes the others.
- A PDB structure gives the donor set and coordination number of a site by simple distance measurements.

## Sources

- [Bertini et al., Bioinorganic Chemistry (LibreTexts), 1.3 Chemical Properties Relative to Storage and Transport](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/01%3A_Transition-Metal_Storage_Transport_and_Biomineralization/1.03%3A_Chemical_Properties_Relative_to_Storage_and_Transport) — Ksp of Fe(OH)₃ about $10^{-39}$, free Fe³⁺ $10^{-18}$ M at pH 7, body iron 3–5 g and its distribution, Fe³⁺/Fe²⁺ potentials in proteins.
- [Bertini et al., 1.5 Transport of Iron](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/01%3A_Transition-Metal_Storage_Transport_and_Biomineralization/1.05%3A_Transport_of_Iron) — siderophores and transferrin (two Fe³⁺, one per lobe).
- [OpenLearn, Iron transport and storage, 3.1](https://www.open.edu/openlearn/science-maths-technology/chemistry/iron-transport-and-storage/content-section-3.1) — enterobactin stability constant about $10^{49}$ for the fully deprotonated ligand.
- [Irving and Williams (1953), J. Chem. Soc. 3192](https://doi.org/10.1039/JR9530003192) — the stability order of divalent first-row complexes.
- RCSB PDB entries [1A6M](https://www.rcsb.org/structure/1A6M), [3KS3](https://www.rcsb.org/structure/3KS3), [1CLL](https://www.rcsb.org/structure/1CLL) and [1PLC](https://www.rcsb.org/structure/1PLC) — the four metal sites of Part A.
- [RSC Education, Extracting iron from breakfast cereal](https://edu.rsc.org/experiments/extracting-iron-from-breakfast-cereal/393.article) — why food-grade iron powder is used and how a magnet recovers it.
