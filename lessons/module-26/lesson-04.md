---
id: "26.4"
module: 26
minutes: 24
practice_minutes: 110
prerequisites: ["26.3", "22.5", "08.6", "06.4", "12.3"]
objectives:
  - Explain how a zinc ion turns water into a nucleophile in carbonic anhydrase and why this needs a Lewis acid that cannot change oxidation state.
  - Use the Marcus equation with a tunnelling distance term to estimate electron-transfer rates in proteins and explain the inverted region.
  - Calculate the Gibbs energy released along the respiratory chain from reduction potentials and relate cytochrome c oxidase to the O₂ delivered by blood.
  - Fit the standard human O₂ dissociation curve, extract cooperativity and delivery numbers, and convert whole-body O₂ use into an electric current and power.
volatility: concept
sources:
  - title: "Bertini et al., Bioinorganic Chemistry (LibreTexts), 2.1 About Carbonic Anhydrase"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/02%3A_The_Reaction_Pathways_of_Zinc_Enzymes_and_Related_Biological_Catalysts/2.01%3A_About_Carbonic_Anhydrase
  - title: "Gray and Winkler (2005), Long-range electron transfer, PNAS 102, 3534"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC553296/
  - title: "Bertini et al., Bioinorganic Chemistry (LibreTexts), 6 Electron Transfer"
    url: https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/06%3A_Electron_Transfer
  - title: "Jakubowski, Biochemistry Online (LibreTexts), B03 Dehydrogenases (table of standard reduction potentials)"
    url: https://bio.libretexts.org/Bookshelves/Biochemistry/Book%3A_Biochemistry_Online_(Jakubowski)/08%3A_OXIDATION_PHOSPHORYLATION/8B%3A_Oxidative_Enzymes/B03.__Dehydrogenases
  - title: "OpenStax Biology 2e, 7.4 Oxidative Phosphorylation"
    url: https://openstax.org/books/biology-2e/pages/7-4-oxidative-phosphorylation
  - title: "Severinghaus (1979), J. Appl. Physiol. 46, 599 (author's revised version, 2007)"
    url: https://www.nickalls.org/dick/papers/anes/JWSrevised2007.pdf
  - title: "RCSB PDB 5B1A, bovine cytochrome c oxidase, fully oxidised, 1.5 Å"
    url: https://www.rcsb.org/structure/5B1A
last_verified: "2026-10-17"
---

# 26.4 · Metalloenzymes, electron transfer and respiration

Haemoglobin brings O₂ to a cell, but the O₂ is only useful when an enzyme takes four electrons and four protons and turns it into water. That enzyme, cytochrome c oxidase, sits at the end of a chain of metal centres that pass electrons from food to oxygen. This lesson looks at two things metals do in enzymes: act as Lewis acids (zinc in carbonic anhydrase) and move electrons (iron and copper in the respiratory chain). It uses the catalysis of lesson [22.5](../module-22/lesson-05.md), the reduction potentials of lesson [08.6](../module-08/lesson-06.md) and the tunnelling of lesson [12.3](../module-12/lesson-03.md). The module practical then follows oxygen all the way from the lungs to cytochrome c oxidase.

## Why it matters

At rest you use about a quarter of a litre of O₂ per minute. Every molecule is reduced by cytochrome c oxidase, and the electrons reach it through a chain of metal centres that must pass them on within microseconds to milliseconds without leaking any to O₂ on the way. Cyanide and carbon monoxide kill by binding the iron of that enzyme. Carbonic anhydrase, the zinc enzyme that clears CO₂ from your tissues, is one of the fastest enzymes known. Catalysts for CO₂ capture, fuel cells and artificial photosynthesis are designed on the same principles.

## Core ideas

> [!NOTE]
> The theory is stable. Rates and reorganisation energies come from Gray and Winkler (2005), potentials at pH 7 from the Jakubowski table on LibreTexts, carbonic anhydrase data from Bertini et al.; all checked 2026-10-17. The labs use NumPy 2.5 and SciPy 1.18, pinned in `labs/common/requirements.txt`.

### Lewis-acid catalysis: carbonic anhydrase

Carbonic anhydrase II catalyses $\mathrm{CO_2 + H_2O \rightleftharpoons HCO_3^- + H^+}$ with a turnover number $k_\text{cat} \approx 10^6$ s⁻¹ at 25 °C. Its zinc is bound by three histidines (His94 and His96 through Nε2, His119 through Nδ1) and one water, the site you measured in lesson [26.1](lesson-01.md).

The mechanism has four steps:

1. Zn²⁺ polarises its water and lowers its pKa from about 14 for free water to near 7, so at pH 7 a large share of the enzyme carries Zn–OH⁻.
2. CO₂ binds in a hydrophobic pocket next to the zinc.
3. The zinc-bound hydroxide attacks the carbon of CO₂, giving zinc-bound bicarbonate.
4. Water displaces bicarbonate, and the proton of the new zinc water is passed to buffer to regenerate Zn–OH⁻.

Why zinc? It is a strong Lewis acid (a small dication), it accepts four or five ligands with no crystal-field penalty (d¹⁰), it exchanges ligands quickly, and it cannot be oxidised or reduced, so it never makes radicals. Copper or iron in the same site would bind more strongly (Irving–Williams) but could start redox chemistry.

### Redox metalloenzymes

Other metal sites do chemistry by changing oxidation state:

- **Electron carriers**: cytochromes (haem Fe²⁺/Fe³⁺), iron–sulfur clusters, blue-copper proteins (lesson [26.2](lesson-02.md)), one electron at a time.
- **Oxygen activation**: cytochrome P450 inserts one O atom into C–H bonds; cytochrome c oxidase reduces O₂ to water.
- **Small molecules**: nitrogenase (an Fe–Mo–S cluster) reduces N₂ to NH₃; hydrogenases make and split H₂.

The protein sets each site's reduction potential through the donor set, the nearby charges and the exposure to water (26.1).

### How fast can an electron jump? Marcus theory

An electron moves between two metal centres by quantum tunnelling through the protein (lesson 12.3). Two factors set the rate.

**Distance.** Tunnelling probability falls exponentially with distance. Gray and Winkler's tunnelling timetable for ruthenium-labelled proteins gives a decay constant $\beta = 1.1$ Å⁻¹ and a rate of about $10^{13}$ s⁻¹ at contact (3 Å). Every 2.1 Å more slows the jump tenfold.

**Energy.** Before the electron can jump, the nuclei of the donor, acceptor and surroundings must reach a geometry where the two states have the same energy. Marcus showed that the activation energy is

$$\Delta G^\ddagger = \frac{(\Delta G^\circ + \lambda)^2}{4\lambda}$$

where $\Delta G^\circ$ is the reaction Gibbs energy and $\lambda$, the **reorganisation energy**, is the energy needed to distort reactants and surroundings into the product geometry without moving the electron. Together:

$$k = 10^{13}\ \mathrm{s^{-1}}\ \exp[-\beta (r - 3\ \text{Å})] \exp\!\left[-\frac{(\Delta G^\circ + \lambda)^2}{4\lambda k_B T}\right]$$

Three results follow:

- The rate is fastest when $-\Delta G^\circ = \lambda$: no activation energy at all.
- Beyond that, more driving force makes the reaction **slower**, the Marcus **inverted region**. It explains why an excited electron in photosynthesis does not fall straight back.
- A small $\lambda$ gives fast transfer even with a small driving force. That is why proteins bury their redox centres away from water and use rigid, entatic sites: azurin's copper has $\lambda \approx 0.7$ eV, against 2.4 eV for copper ions in water.

Gray and Winkler conclude that a single tunnelling step through protein can cover about 20 Å in biologically useful times; longer distances need a chain of centres, each step shorter than that.

### The respiratory chain

The respiratory chain in the inner membrane of the mitochondrion (lesson [06.1](../module-06/lesson-01.md)) is exactly such a chain. Electrons from NADH enter complex I (flavin and Fe–S clusters), go through ubiquinone to complex III (haems b and c₁, an Fe–S cluster), are carried by the small haem protein cytochrome c to complex IV, **cytochrome c oxidase** (Cu_A, haem a, and the haem a₃–Cu_B site where O₂ binds), and finally reduce O₂:

$$\mathrm{O_2 + 4\,e^- + 4\,H^+ \rightarrow 2\,H_2O}$$

At each step the electron goes to a couple with a higher (more positive) reduction potential. The free energy, $\Delta G = -nF\Delta E$ (lesson 08.6), is used by complexes I, III and IV to pump protons across the membrane. ATP synthase then lets the protons flow back and makes ATP (lesson [06.4](../module-06/lesson-04.md)). The haem a₃–Cu_B site holds O₂ and its partly reduced forms tightly until all four electrons have arrived, so almost no superoxide or peroxide escapes. Cyanide, CO and hydrogen sulfide block respiration by binding this site.

You can explore the enzyme on the RCSB page of [5B1A](https://www.rcsb.org/structure/5B1A), bovine cytochrome c oxidase at 1.5 Å.

## Worked example

### 1. How much free energy does one NADH give?

With $E^{\circ\prime}$(NAD⁺/NADH) = −0.32 V and $E^{\circ\prime}$(½O₂/H₂O) = +0.816 V at pH 7:

1. $\Delta E = 0.816 - (-0.32) = 1.136$ V.
2. Two electrons per NADH: $\Delta G^{\circ\prime} = -nF\Delta E = -2 \times 96\,485\ \mathrm{C\,mol^{-1}} \times 1.136\ \mathrm{V} = -219$ kJ/mol.
3. The cell makes about 2.5 ATP per NADH, and each ATP costs about 53 kJ/mol under cell conditions (lesson 06.4): $2.5 \times 53 = 132$ kJ, about 60 % of the 219 kJ.

Where does +0.816 V come from? The standard potential of $\mathrm{O_2 + 4H^+ + 4e^- \rightarrow 2H_2O}$ is +1.229 V at pH 0. The Nernst equation (lesson 08.6) lowers it by 0.0592 V per pH unit at 25 °C: $1.229 - 7 \times 0.0592 = 0.815$ V.

### 2. Cytochrome c to cytochrome a in microseconds

Take $\Delta G^\circ = -(0.29 - 0.25) = -0.04$ eV, $\lambda$ = 0.8 eV, a donor–acceptor distance of 14 Å, and $k_BT$ = 0.0267 eV at 37 °C.

1. Distance factor: $10^{13} \times e^{-1.1 \times (14 - 3)} = 10^{13} \times 5.6 \times 10^{-6} = 5.6 \times 10^7$ s⁻¹.
2. Activation factor: $\exp[-(0.76)^2 / (4 \times 0.8 \times 0.0267)] = e^{-6.76} = 1.2 \times 10^{-3}$.
3. $k = 6.5 \times 10^4$ s⁻¹, a time constant of about 15 µs.

The small driving force costs a factor of a thousand. Respiration stays fast because many steps are short and their $\lambda$ is kept low.

## Hands-on

What you need: Python with the course packages and the [Module 26 lab folder](../../labs/module-26/). Write up Part B with the [lab report template](../../templates/lab-report.md). Time: about 1 h 50 min.

### Part A — Python: Marcus rates and the respiratory chain (30 min)

1. Open `lesson04_electron_transfer.py` and complete `marcus_rate()`, `dG_per_electron()` and `o2_potential_at_pH()`.
2. Run it and open `runs/lesson04_electron_transfer.png`:

```bash
py lesson04_electron_transfer.py
```

3. From the right-hand plot, find the driving force of the fastest transfer at 10 Å. What happens at twice that driving force?

How you know it worked: E(O₂/H₂O) at pH 7 = 0.815 V. Steps per 2 electrons: NADH → ubiquinone −73.3, ubiquinone → cytochrome c −36.7, cytochrome c → O₂ −109.2 kJ/mol; total −219.2 kJ/mol per NADH, −438 kJ/mol per O₂. At the optimum: 1.1 × 10¹² s⁻¹ at 5 Å, 4.5 × 10⁹ at 10 Å, 5.6 × 10⁷ at 14 Å, 7.6 × 10⁴ at 20 Å and 3.1 × 10² s⁻¹ (3 ms) at 25 Å. Cytochrome c → a: 6.5 × 10⁴ s⁻¹. The fastest rate is at $-\Delta G^\circ = \lambda$ = 0.8 eV; at 1.6 eV the rate is back down by a factor of about $e^{-7.5}$, nearly 2000.

<details><summary>Reference solution</summary>

```python
def marcus_rate(dG, lam, r):
    return K0 * math.exp(-BETA * (r - R0)) * math.exp(-(dG + lam) ** 2 / (4 * lam * KT_EV))

def dG_per_electron(E_donor, E_acceptor):
    return -(E_acceptor - E_donor)

def o2_potential_at_pH(pH, E0=1.229, T=298.15):
    return E0 - math.log(10) * K_B * T / E_CHARGE * pH
```

Full code: `lesson04_electron_transfer_solution.py`. At 25 Å a single jump takes milliseconds even at the optimum, which is why cofactors in the chain are spaced well under 20 Å apart.

</details>

### Part B — module practical: from the lungs to cytochrome c oxidase (80 min)

This practical uses every lesson of the module: real O₂ binding data (26.3), the T and R states behind them (26.2), metal sites as chemical machines (26.1) and the respiratory chain (this lesson).

1. Open `lesson04_practical.py`. It reads `hb_standard_curve.csv`, the 51-point standard human blood curve of Severinghaus (37 °C, pH 7.40).
2. Complete `fit_hill()` (nonlinear least squares with `curve_fit`, lesson [05.3](../module-05/lesson-03.md)), `end_constants()`, `o2_content()` and `respiratory_current()`.
3. Run it and open `runs/lesson04_practical.png`:

```bash
py lesson04_practical.py
```

4. Write a short report with the template. Answer:
   (a) Compare the Hill fits to all points and to 20–80 % only. Where does the Hill model miss, and is the misfit random or systematic? How does the two-term Severinghaus equation do?
   (b) From $K_T$ and $K_R$, how much more strongly does the last O₂ bind than the first, in kJ/mol? Relate this to the iron movement of lesson 26.2.
   (c) How much O₂ does the body use at rest by your calculation, and how much of the bound O₂ is released at rest and in working muscle, with and without cooperativity? What does the Bohr shift add?
   (d) What current do the electrons delivered to O₂ represent, and what power? Compare the power with a resting person's heat output of roughly 80–100 W.

How you know it worked: Hill fit to all 51 points $P_{50}$ = 26.38 ± 0.11 mmHg, $n$ = 2.647 ± 0.026, RMS 0.95 % saturation; 20–80 % only $P_{50}$ = 26.62 ± 0.04, $n$ = 2.629 ± 0.015; Severinghaus equation RMS 0.30 %. The largest Hill misfit is at 8 mmHg (data 6.7 %, Hill 4.1 %). $K_T$ ≈ 166 mmHg, $K_R$ ≈ 1.40 mmHg, ratio 118, 12.3 kJ/mol. Arterial 19.9 and venous 15.1 mL O₂/dL, VO₂ ≈ 238 mL/min. Released from 100 to 40 mmHg: 22.8 % (real), 18.9 % (same $P_{50}$, $n$ = 1), 3.3 % (myoglobin-like); to 20 mmHg: 65.4, 36.0 and 8.3 %. At pH 7.20, $P_{50}$ = 32.9 mmHg and saturation at 20 mmHg falls from 32 % to 21 %. Electron current 68 A; power 78 W.

<details><summary>Reference solution and model answers</summary>

```python
def fit_hill(p, s, lo=0.0, hi=1.0):
    m = (s > lo) & (s < hi)
    popt, pcov = curve_fit(hill, p[m], s[m], p0=(27.0, 2.7))
    return popt, np.sqrt(np.diag(pcov))

def end_constants(p, s, low=2.0, high=400.0):
    K = p * (1 - s) / s
    return float(np.mean(K[p <= low])), float(np.mean(K[p >= high]))

def o2_content(S, po2, hb=HB_G_PER_DL):
    return HUFNER * hb * S + O2_SOLUBILITY * po2

def respiratory_current(vo2_ml_per_min):
    return 4 * F * vo2_ml_per_min / 1000 / MOLAR_VOLUME_STPD / 60
```

Full code: `lesson04_practical_solution.py`.

(a) Both fits give $n$ ≈ 2.63–2.65 and $P_{50}$ ≈ 26.4–26.6 mmHg, but the residual plot shows a smooth wave, not scatter: the Hill curve is too low below about 15 mmHg, slightly too high around $P_{50}$ and about 1 % too low between 60 and 100 mmHg, because the true Hill slope is not constant and falls back to 1 at both ends. The quoted ± values are only fit statistics on smoothed data, not measurement uncertainty. Severinghaus's two-term equation follows the low end and is three times closer. (b) $RT\ln(K_T/K_R)$ = 12.3 kJ/mol: binding is worth that much more once the tetramer is in R. It is the energy the T-state constraints (salt bridges at the α₁β₂ interface, the strained out-of-plane iron) cost; the ends of a smoothed table are partly extrapolated, so treat it as an estimate. (c) About 240 mL O₂/min, close to the textbook resting value of about 250 mL/min. At rest 23 % of bound O₂ is released, in working muscle 65 %; without cooperativity 19 % and 36 %. The Bohr shift at pH 7.20 lowers the saturation at 20 mmHg by another 11 points. (d) 68 A of electrons flow to O₂; at 1.136 V that is 78 W, the same order as a resting person's heat output, because almost all the energy of respiration ends up as heat.

</details>

## Common mistakes

- Thinking zinc enzymes work by redox. Zn²⁺ is a Lewis acid that lowers the pKa of water; it never changes oxidation state.
- Expecting more driving force always to give faster electron transfer. Past $-\Delta G^\circ = \lambda$ the rate falls (inverted region).
- Using the standard potential of O₂/H₂O at pH 0 (1.229 V) for a cell at pH 7. Use $E^{\circ\prime}$ = 0.816 V, or apply the Nernst correction.
- Forgetting $n$ in $\Delta G = -nF\Delta E$: two electrons per NADH, four per O₂.
- Trusting the tiny fit uncertainties from a smoothed standard curve. Look at the residuals; a systematic wave means the model, not the data, is wrong.

## Key takeaways

- Carbonic anhydrase uses Zn²⁺ as a Lewis acid: Zn–OH⁻ attacks CO₂ with $k_\text{cat} \approx 10^6$ s⁻¹.
- Electron-transfer rates fall by ten for every 2.1 Å ($\beta$ = 1.1 Å⁻¹) and peak when $-\Delta G^\circ$ equals the reorganisation energy $\lambda$; proteins keep $\lambda$ small.
- The respiratory chain moves electrons from NADH (−0.32 V) to O₂ (+0.816 V), releasing 219 kJ/mol per NADH, much of it stored as a proton gradient.
- Cytochrome c oxidase reduces O₂ with four electrons at a haem–copper site; at rest that is a current of about 70 A through the body.
- The module practical connects the O₂ curve (Hill $n$ ≈ 2.6, $P_{50}$ ≈ 26.5 mmHg, cooperativity worth about 12 kJ/mol) to O₂ delivery and the power of respiration.

## Sources

- [Bertini et al., 2.1 About Carbonic Anhydrase](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/02%3A_The_Reaction_Pathways_of_Zinc_Enzymes_and_Related_Biological_Catalysts/2.01%3A_About_Carbonic_Anhydrase) — isoenzyme II $k_\text{cat} \approx 10^6$ s⁻¹ at 25 °C; zinc ligands His94, His96 (Nε2), His119 (Nδ1) and water or hydroxide.
- [Gray and Winkler (2005), PNAS 102, 3534](https://pmc.ncbi.nlm.nih.gov/articles/PMC553296/) — tunnelling timetable ($\beta$ = 1.1 Å⁻¹, $10^{13}$ s⁻¹ at 3 Å), reorganisation energies, about 20 Å for single-step tunnelling.
- [Bertini et al., 6 Electron Transfer](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Book3A_Bioinorganic_Chemistry_(Bertini_et_al.)/06%3A_Electron_Transfer) — redox centres and Marcus theory in proteins.
- [Jakubowski, Biochemistry Online, B03 Dehydrogenases](https://bio.libretexts.org/Bookshelves/Biochemistry/Book%3A_Biochemistry_Online_(Jakubowski)/08%3A_OXIDATION_PHOSPHORYLATION/8B%3A_Oxidative_Enzymes/B03.__Dehydrogenases) — $E^{\circ\prime}$: NAD⁺ −0.32, ubiquinone +0.06, cytochrome c +0.25, cytochrome a +0.29, ½O₂/H₂O +0.816 V.
- [OpenStax Biology 2e, 7.4 Oxidative Phosphorylation](https://openstax.org/books/biology-2e/pages/7-4-oxidative-phosphorylation) — complexes I–IV, proton pumping and ATP synthase.
- [Severinghaus (1979, revised 2007)](https://www.nickalls.org/dick/papers/anes/JWSrevised2007.pdf) — standard O₂ curve, O₂ content equation and Bohr coefficient used in the practical.
- [RCSB 5B1A](https://www.rcsb.org/structure/5B1A) — bovine cytochrome c oxidase, fully oxidised, 1.5 Å.
