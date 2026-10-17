---
id: "26.2"
module: 26
minutes: 22
practice_minutes: 65
prerequisites: ["26.1", "18.4", "18.5"]
objectives:
  - Predict the spin state, number of unpaired electrons and spin-only magnetic moment of haem iron in deoxy, oxy and met forms.
  - Explain, with ionic radii and measured structures, why high-spin iron(II) sits out of the porphyrin plane and moves into it when O₂ binds.
  - Describe the Fe–O₂ bond in the Pauling and Weiss pictures and use resonance-Raman and magnetic data to choose between them.
  - Explain how a protein tunes a metal site, using CO/O₂ discrimination in myoglobin and the blue-copper site as examples.
volatility: concept
sources:
  - title: "Bertini et al., Bioinorganic Chemistry (LibreTexts), 4.11 Nature of the Metal-Dioxygen Linkage in Biological Systems"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/04%3A_Biological_and_Synthetic_Dioxygen_Carriers/4.11%3A_Nature_of_the_Metal-Dioxygen_Linkage_in_Biological_Systems
  - title: "Bertini et al., Bioinorganic Chemistry (LibreTexts), 4.18 Structural Basis of Ligand Affinities of Oxygen Carriers"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/04%3A_Biological_and_Synthetic_Dioxygen_Carriers/4.18%3A_Structural_Basis_of_Ligand_Affinities_of_Oxygen_Carriers
  - title: "RCSB PDB 2DN1 and 2DN2, human oxy- and deoxy-haemoglobin at 1.25 Å (Park et al., J. Mol. Biol. 360, 690, 2006)"
    url: https://www.rcsb.org/structure/2DN2
  - title: "RCSB PDB 1A6M, oxy-myoglobin at 1.0 Å (Vojtěchovský et al., Biophys. J. 1999)"
    url: https://www.rcsb.org/structure/1A6M
  - title: "Pauling and Coryell (1936), The magnetic properties and structure of hemoglobin, oxyhemoglobin and carbonmonoxyhemoglobin, PNAS 22, 210"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC1076743/
  - title: "Shannon (1976), Revised effective ionic radii, Acta Cryst. A32, 751"
    url: https://doi.org/10.1107/S0567739476001551
  - title: "Prahl, Optical absorption of hemoglobin (Oregon Medical Laser Center)"
    url: https://omlc.org/spectra/hemoglobin/
  - title: "Gray and Winkler (2005), Long-range electron transfer, PNAS 102, 3534"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC553296/
last_verified: "2026-10-17"
---

# 26.2 · Bonding in transition-metal complexes revisited

In Module 18 you learnt crystal and ligand field theory on small complexes in a flask. Proteins use the same rules, but they also hold the metal in a frame that can push and pull on it. This lesson applies lessons [18.4](../module-18/lesson-04.md) and [18.5](../module-18/lesson-05.md) to the haem iron of haemoglobin and myoglobin: its spin state, its size, where it sits in the porphyrin ring and how it binds O₂. It ends with two ways a protein tunes a metal site: telling O₂ from CO, and the strained copper site that makes electron transfer fast.

## Why it matters

Haemoglobin works because one iron ion changes spin. When O₂ binds, iron(II) goes from high spin to low spin, shrinks, and moves about a third of an ångström into the porphyrin plane. That small movement pulls a histidine and the helix it sits on, and the strain spreads to the other three subunits (lesson [26.3](lesson-03.md)). The same ideas explain why carbon monoxide is poisonous, why blood changes colour when it takes up oxygen, and why copper proteins move electrons so fast. If you can predict spin states and sizes from a d-electron count, you can read the mechanism straight from a crystal structure.

## Core ideas

> [!NOTE]
> The bonding ideas are stable. The structures are PDB entries 2DN1, 2DN2 and 1A6M (checked on RCSB 2026-10-17); the O–O stretch and CO/O₂ affinities are from Bertini et al. (LibreTexts edition), the haemoglobin spectra from the Oregon Medical Laser Center compilation, all checked 2026-10-17.

### Haem: iron in a strong-field macrocycle

Haem (protoporphyrin IX with iron) is a flat ring of four pyrrole units. When it loses two N–H protons it becomes a dianion with four nitrogen donors pointing into a central hole. It is a **macrocycle**: the chelate effect of lesson [18.3](../module-18/lesson-03.md) taken to its limit, so the iron never falls out. The four in-plane nitrogens make a strong field. Above and below the ring there are two more positions:

- the **proximal** side, where a histidine of the protein (His F8, residue 87 in the α chains and 92 in the β chains of human haemoglobin, 93 in myoglobin) binds through its imidazole nitrogen;
- the **distal** side, where O₂ binds, next to a second histidine (His E7) that does not bind the iron.

With five or six nitrogen donors, the field around iron(II) is close to the point where Δₒ equals the pairing energy $P$ (lesson 18.4). A small change in the ligand set tips the balance.

### Three iron states, three spin states

| Form | Ligands | d count | Spin state | Unpaired | $\mu_\text{spin-only}$ |
|---|---|---|---|---|---|
| deoxy-Hb, deoxy-Mb | 4 N(por) + His | Fe(II), d⁶ | high spin, $S = 2$ | 4 | 4.90 BM |
| oxy-Hb, oxy-Mb | 4 N + His + O₂ | formally Fe(II), d⁶ | diamagnetic | 0 | 0 |
| met-Hb (water) | 4 N + His + H₂O | Fe(III), d⁵ | high spin, $S = 5/2$ | 5 | 5.92 BM |

The spin-only moment is $\mu = \sqrt{n(n+2)}$ BM for $n$ unpaired electrons (lesson 18.5). Pauling and Coryell measured the magnetism of blood in 1936 and found deoxy-Hb strongly paramagnetic and oxy-Hb diamagnetic, one of the first uses of magnetism to study a protein. Met-haemoglobin is the oxidised, brown form that cannot carry O₂; red cells contain an enzyme that reduces it back.

### Size: why deoxy iron sits out of the plane

High-spin iron(II) has two electrons in the antibonding e<sub>g</sub> orbitals, which point straight at the ligands. That makes the ion bigger. Shannon's radii for six-coordinate Fe²⁺ are 0.78 Å (high spin) and 0.61 Å (low spin). The porphyrin hole is sized for Fe–N bonds of about 2.0 Å, which suits the smaller low-spin ion. The larger high-spin ion does not fit and sits above the ring, on the proximal histidine side. The crystal structures of human haemoglobin at 1.25 Å resolution show it clearly:

- deoxy (2DN2): Fe 0.31–0.39 Å out of the N₄ plane, Fe–N(por) 2.06–2.11 Å, Fe–N(His) 2.16–2.21 Å;
- oxy (2DN1): Fe within 0.05 Å of the plane, Fe–N(por) 2.01–2.02 Å, Fe–N(His) 2.06–2.07 Å.

When O₂ binds, iron becomes low spin, shrinks and drops into the ring, dragging the proximal histidine about 0.3 Å with it. In haemoglobin that movement is the trigger for cooperativity.

### What kind of bond is Fe–O₂?

Free O₂ has two unpaired electrons (lesson [12.6](../module-12/lesson-06.md)), yet oxy-Hb is diamagnetic. Two pictures fit that fact:

- **Pauling** (1948): low-spin Fe(II) bound to singlet O₂, end-on and bent.
- **Weiss**: low-spin Fe(III) ($S = 1/2$) bound to superoxide O₂•⁻ ($S = 1/2$), with the two spins coupled so strongly that they cancel.

The O–O stretching frequency decides. In free O₂ the bond order is 2 and the stretch is near 1556 cm⁻¹; in oxy-Hb and oxy-Mb infrared spectroscopy finds about 1105 cm⁻¹, the value of a superoxo species with bond order about 1.5 (lesson [17.2](../module-17/lesson-02.md) for why a weaker bond vibrates more slowly). So in oxy-Hb a good deal of charge moves from iron to O₂. The real bond lies between the two pictures, closer to Weiss. The structures agree: the Fe–O–O angle is about 123° in 1A6M and 2DN1, bent as expected for superoxide, not linear.

### Colour comes from the ring, not from d–d bands

Blood is red, and arterial blood is brighter than venous blood. The bands responsible are not the weak d–d bands of lesson 18.5 ($\varepsilon$ up to about 100 L mol⁻¹ cm⁻¹). They are π→π* transitions of the porphyrin, thousands of times stronger. Prahl's compilation gives oxy-Hb maxima at 414 nm (the **Soret** band) and 542 and 576 nm (the two **Q bands**), and deoxy-Hb maxima at 432 and 556 nm. The metal tunes these ring bands, which is why the colour changes with oxygen; pulse oximeters exploit the difference in the red and near infrared.

### How the protein tunes the site

**CO versus O₂.** Carbon monoxide binds iron(II) haem far more strongly than O₂. Bertini lists the ratio $M = P_{1/2}(\mathrm{O_2})/P_{1/2}(\mathrm{CO})$ (each $P_{1/2}$ is the pressure for half saturation): about 500 for a simple imidazole–haem in water, but only 28 for sperm-whale myoglobin. The protein favours O₂ by about a factor of 18. The distal histidine donates a hydrogen bond to the bound, negatively charged superoxo oxygen; CO is nearly neutral and gains little. Remove the distal histidine (mutant E7 His→Gly) and $M$ rises to about 1300.

**Blue copper and the entatic state.** Cu(I) (d¹⁰) prefers a tetrahedron; Cu(II) (d⁹) prefers a square plane with Jahn–Teller distortion. In plastocyanin and azurin the protein holds copper in a distorted tetrahedron with two histidines, one cysteine and a long bond to methionine (lesson [26.1](lesson-01.md)), a geometry halfway between the two. Because the site barely changes shape when copper is oxidised or reduced, the **reorganisation energy** is small: Gray and Winkler give about 0.7 eV for azurin's copper, against about 2.4 eV for Cu(II)/Cu(I) in water. A strained site poised for its job is called **entatic**. The intense blue colour comes from a cysteine S → Cu(II) charge-transfer band near 600 nm, much stronger than the usual d–d band of Cu(II).

## Worked example

### 1. Will high-spin iron(II) fit in the porphyrin hole?

Take the in-plane Fe–N distance in oxy-Hb, 2.01 Å, as the size of the hole when the iron is low spin.

1. Shannon radii: high-spin Fe²⁺ is $0.78 - 0.61 = 0.17$ Å larger than low-spin Fe²⁺.
2. If the ring could not stretch, high-spin iron would need Fe–N ≈ $2.01 + 0.17 = 2.18$ Å.
3. With the iron lifted a height $h$ above the plane, Fe–N $= \sqrt{r_\text{hole}^2 + h^2}$. Setting $r_\text{hole} = 2.01$ Å and Fe–N $= 2.18$ Å gives $h = \sqrt{2.18^2 - 2.01^2} = 0.84$ Å.
4. The real displacement in 2DN2 is only about 0.34 Å, and the real Fe–N is 2.06–2.11 Å. The ring is not rigid: it domes and its hole expands a little, and a five-coordinate ion has shorter bonds than a six-coordinate one.

The estimate is crude, but it gets the direction and the cause right: the extra e<sub>g</sub> electrons make the ion too big for a flat ring.

### 2. How much does the distal histidine favour O₂ over CO?

$M = P_{1/2}(\mathrm{O_2})/P_{1/2}(\mathrm{CO})$ is a ratio of equilibrium constants, so it converts to a free energy (lesson [13.4](../module-13/lesson-04.md)):

$$\Delta\Delta G = RT \ln\frac{M_\text{haem}}{M_\text{Mb}} = (8.314\ \mathrm{J\,mol^{-1}\,K^{-1}})(298\ \mathrm{K}) \ln\frac{500}{28} = 7.1\ \mathrm{kJ\,mol^{-1}}$$

That is about the energy of one hydrogen bond. One well-placed N–H in the pocket makes myoglobin about 18 times more selective for O₂.

## Hands-on

What you need: pencil and paper, Python with the course packages and the [Module 26 lab folder](../../labs/module-26/), and a web browser. Record your answers on the [notebook page template](../../templates/notebook-page.md). Time: about 65 minutes.

### Part A — pencil: box diagrams (20 min)

1. Draw the octahedral d-orbital box diagram (t₂g below, e<sub>g</sub> above) for deoxy-Fe(II), oxy-Fe(II) (Pauling picture), met-Fe(III) with water and met-Fe(III) with cyanide. Use lesson 18.4: water is weak field, cyanide strong field.
2. For each, give the number of unpaired electrons and the spin-only moment.
3. In the Weiss picture, which d electron of Fe(III) pairs with the unpaired electron of superoxide?

<details><summary>Answers</summary>

1–2. Deoxy Fe(II) high spin $t_{2g}^4 e_g^2$: 4 unpaired, 4.90 BM. Oxy Fe(II) low spin $t_{2g}^6$: 0, diamagnetic. Met-aqua Fe(III) high spin $t_{2g}^3 e_g^2$: 5 unpaired, 5.92 BM. Met-cyano Fe(III) low spin $t_{2g}^5$: 1 unpaired, 1.73 BM.
3. Low-spin Fe(III) is $t_{2g}^5$, with one unpaired electron in a t₂g orbital that overlaps with the π* orbital of superoxide. The two spins pair across the Fe–O bond (strong antiferromagnetic coupling), so the unit is diamagnetic.

</details>

### Part B — Python: iron in and out of the plane (25 min)

1. Open `lesson02_heme.py` and complete `unpaired_octahedral()`, `spin_only_moment()` and `out_of_plane()`. The last fits a plane through the four porphyrin nitrogens with a singular value decomposition and measures the iron's distance from it.
2. Run it and open `runs/lesson02_heme.png`:

```bash
py lesson02_heme.py
```

3. Look at the change yourself: on the RCSB pages of [2DN2](https://www.rcsb.org/structure/2DN2) and [2DN1](https://www.rcsb.org/structure/2DN1), open Mol* (lesson 06.2), select the haem of chain A and view it edge-on.

How you know it worked: spin-only moments 4.90, 0, 5.92 and 1.73 BM. Deoxy-Hb chains A–D: Fe +0.39, +0.35, +0.31 and +0.32 Å out of the plane (mean +0.34 Å); oxy-Hb chains A and B: +0.05 and −0.03 Å; oxy-Mb +0.02 Å. Fe–O 1.78–1.82 Å and Fe–O–O 123–126°. Fe–N(His) shortens from about 2.19 to 2.06 Å.

<details><summary>Reference solution</summary>

```python
def unpaired_octahedral(d, low_spin):
    order = [0, 1, 2, 0, 1, 2, 3, 4, 3, 4] if low_spin else [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    occ = [0] * 5
    for k in range(d):
        occ[order[k]] += 1
    return sum(1 for o in occ if o == 1)

def spin_only_moment(n):
    return math.sqrt(n * (n + 2))

def out_of_plane(fe, n4, his):
    N = np.array(n4)
    c = N.mean(axis=0)
    normal = np.linalg.svd(N - c)[2][2]
    d = float((fe - c) @ normal)
    return -d if (his - c) @ normal < 0 else d
```

Full code: `lesson02_heme_solution.py`. The last singular vector of the centred N₄ coordinates is the plane normal; its sign is arbitrary, so the code points it towards the histidine before reporting the distance.

</details>

### Part C — real spectra: ring bands or d–d bands? (20 min)

1. Open Prahl's [haemoglobin absorption page](https://omlc.org/spectra/hemoglobin/) and its tabulated summary. The values are molar extinction coefficients per haemoglobin tetramer (four haems).
2. Find the maxima of oxy- and deoxy-haemoglobin between 400 and 600 nm and read $\varepsilon$ at the Soret maximum.
3. Divide by four to get $\varepsilon$ per haem and compare with the d–d bands of lesson 18.5. Are these d–d bands?

<details><summary>Answers</summary>

Oxy-Hb: 414 nm ($\varepsilon \approx 5.2 \times 10^5$ L mol⁻¹ cm⁻¹ per tetramer), 542 and 576 nm. Deoxy-Hb: 432 nm ($\approx 5.5 \times 10^5$) and one broad Q band at 556 nm. Per haem the Soret band is about $1.3 \times 10^5$ L mol⁻¹ cm⁻¹, more than a thousand times a Laporte-forbidden d–d band. These are allowed π→π* transitions of the porphyrin ring; the iron only shifts them.

</details>

## Common mistakes

- Treating oxy-Hb as simply "Fe(II) plus O₂". The 1105 cm⁻¹ O–O stretch shows superoxo character; the bond is closer to Fe(III)–O₂•⁻.
- Expecting paramagnetism from Fe(III)–superoxide. The two $S = 1/2$ spins couple strongly and cancel, so the unit is diamagnetic.
- Forgetting that size follows spin. High-spin ions are larger because e<sub>g</sub> electrons point at the ligands; that is why deoxy iron leaves the plane.
- Assigning the colour of haem proteins to d–d transitions. Their bands are porphyrin π→π*, with $\varepsilon$ around $10^5$.
- Reading a PDB displacement to 0.01 Å as exact. At 1.25 Å resolution coordinate errors are a few hundredths of an ångström; compare chains and structures, not single digits.

## Key takeaways

- Deoxy haem iron is high-spin Fe(II) ($S = 2$, 4.90 BM), five-coordinate and about 0.3–0.4 Å out of the porphyrin plane.
- Binding O₂ makes the site low spin and diamagnetic; the smaller iron drops into the plane and pulls the proximal histidine about 0.3 Å.
- Oxy-Hb has a bent Fe–O–O (about 123°) and an O–O stretch near 1105 cm⁻¹: superoxo character, the Weiss picture.
- The distal histidine favours O₂ over CO by about 7 kJ/mol (M from 500 to 28); blue-copper proteins hold copper in a strained, entatic geometry that lowers the reorganisation energy for electron transfer.
- Haem colour comes from porphyrin π→π* bands (Soret near 415 nm, Q bands near 540–580 nm), tuned by the iron's state.

## Sources

- [Bertini et al., 4.11 Nature of the Metal-Dioxygen Linkage](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/04%3A_Biological_and_Synthetic_Dioxygen_Carriers/4.11%3A_Nature_of_the_Metal-Dioxygen_Linkage_in_Biological_Systems) — Pauling and Weiss descriptions, diamagnetism, O–O stretch about 1105 cm⁻¹, superoxo bond order about 1.5.
- [Bertini et al., 4.18 Structural Basis of Ligand Affinities](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/04%3A_Biological_and_Synthetic_Dioxygen_Carriers/4.18%3A_Structural_Basis_of_Ligand_Affinities_of_Oxygen_Carriers) — Table 4.6, $P_{1/2}$ for O₂ and CO and $M$ for haem models and myoglobins.
- [RCSB 2DN2](https://www.rcsb.org/structure/2DN2) and [2DN1](https://www.rcsb.org/structure/2DN1) — human deoxy- and oxy-haemoglobin at 1.25 Å; [RCSB 1A6M](https://www.rcsb.org/structure/1A6M) — oxy-myoglobin at 1.0 Å.
- [Pauling and Coryell (1936), PNAS 22, 210](https://pmc.ncbi.nlm.nih.gov/articles/PMC1076743/) — magnetic properties of haemoglobin, oxy- and carbonmonoxy-haemoglobin.
- [Shannon (1976), Acta Cryst. A32, 751](https://doi.org/10.1107/S0567739476001551) — ionic radii of high- and low-spin Fe²⁺.
- [Prahl, Optical absorption of hemoglobin](https://omlc.org/spectra/hemoglobin/) — molar extinction coefficients of oxy- and deoxy-haemoglobin.
- [Gray and Winkler (2005), PNAS 102, 3534](https://pmc.ncbi.nlm.nih.gov/articles/PMC553296/) — reorganisation energies of copper in water and in azurin.
