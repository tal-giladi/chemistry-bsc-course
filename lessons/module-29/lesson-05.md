---
id: "29.5"
module: 29
minutes: 24
practice_minutes: 140
prerequisites: ["29.3", "29.4", "06.4", "16.4", "13.6"]
objectives:
  - Classify each step of glycolysis as an organic reaction type and name the catalytic strategy its enzyme uses.
  - Calculate the actual Gibbs energy of each step from ΔG°' and measured cell concentrations, and identify the steps that are far from equilibrium.
  - Explain why far-from-equilibrium steps are where pathways are regulated, and how inhibiting one step changes the concentrations upstream.
  - Characterise an enzyme and three inhibitors from initial-rate data and predict each inhibitor's effect inside a pathway.
volatility: concept
sources:
  - title: "Jakubowski and Flatt, Fundamentals of Biochemistry (LibreTexts), 13.1 Glycolysis"
    url: https://bio.libretexts.org/Bookshelves/Biochemistry/Fundamentals_of_Biochemistry_(Jakubowski_and_Flatt)/02%3A_Unit_II-_Bioenergetics_and_Metabolism/13%3A_Glycolysis_Gluconeogenesis_and_the_Pentose_Phosphate_Pathway/13.01%3A_Glycolysis
  - title: "Protasov et al. (2019), Erythrocytes as bioreactors to decrease excess ammonium concentration in blood, Sci. Rep. 9, 1455"
    url: https://www.nature.com/articles/s41598-018-37828-5
  - title: "OpenStax Biology 2e, 6.5 Enzymes"
    url: https://openstax.org/books/biology-2e/pages/6-5-enzymes
  - title: "MIT OpenCourseWare 5.07SC Biological Chemistry I (Fall 2013)"
    url: https://ocw.mit.edu/courses/5-07sc-biological-chemistry-i-fall-2013/
last_verified: "2026-10-17"
---

# 29.5 · Metabolic pathways as chemistry

A metabolic pathway is a multi-step synthesis run in water at 37 °C, where every step has its own catalyst and the product of one step is the starting material of the next. Lesson [06.4](../module-06/lesson-04.md) treated glycolysis as an energy budget. This lesson reads it as organic chemistry: aldol reactions, isomerisations, oxidations and phosphoryl transfers, each catalysed by the strategies of lesson [29.4](lesson-04.md). Then it asks which steps actually push the pathway forward, using real concentrations in red blood cells. The module practical at the end brings together all the kinetics of this module.

## Why it matters

Cancer cells, parasites and bacteria all depend on glycolysis, and drugs that target it must hit the right enzyme. Inhibit an enzyme whose step is near equilibrium and the cell barely notices: the concentrations shift a little and flux goes on. Inhibit a step that is far from equilibrium, and flux drops while its substrate piles up. Which happens depends on the thermodynamics of each step in the cell, not in a textbook table of standard values, and on the type of inhibitor. Metabolic engineers who redesign yeast to make fuels or medicines make the same judgement every day.

## Core ideas

> [!NOTE]
> The chemistry is stable. Standard Gibbs energies are the rounded values in Jakubowski and Flatt (LibreTexts); red-cell concentrations are the model steady-state values of Protasov et al. (2019), which lie in or close to the measured ranges they list. Both differ by a few kJ/mol or tens of per cent between sources and conditions. The practical data are generated. Checked 2026-10-17 with NumPy 2.5 and SciPy 1.18.

### Glycolysis as ten organic reactions

| Step | Enzyme | Reaction type | Catalytic strategy |
|---|---|---|---|
| 1 | hexokinase | phosphoryl transfer from ATP to a C6 alcohol | Mg²⁺ shields ATP's charge; induced fit excludes water |
| 2 | phosphoglucose isomerase | aldose → ketose isomerisation via an enediol | general acid–base |
| 3 | phosphofructokinase-1 | phosphoryl transfer to C1 | Mg²⁺; allosteric control |
| 4 | aldolase | retro-aldol: C6 → two C3 | covalent: lysine forms an imine (Schiff base) with the ketone |
| 5 | triose phosphate isomerase | ketose → aldose via an enediol | general acid–base (Glu, His) |
| 6 | glyceraldehyde-3-phosphate dehydrogenase | aldehyde oxidation by NAD⁺ to an acyl phosphate | covalent: cysteine thiohemiacetal, then thioester |
| 7 | phosphoglycerate kinase | acyl phosphate → ATP | substrate-level phosphorylation |
| 8 | phosphoglycerate mutase | phosphate moves C3 → C2 | covalent phospho-histidine |
| 9 | enolase | dehydration to an enol phosphate | Mg²⁺ and general base |
| 10 | pyruvate kinase | phosphoryl transfer to ADP | Mg²⁺/K⁺; the enol tautomerises to the keto form |

Step 4 is the aldol reaction of lesson [16.4](../module-16/lesson-04.md) run backwards: the lysine imine acts as an electron sink, as an enamine does in organic synthesis. Step 6 is the only oxidation. The aldehyde is captured by a cysteine (covalent catalysis again), oxidised to a high-energy thioester while NAD⁺ takes a hydride, and the thioester is then cut by phosphate, not water, so the energy is kept as an acyl phosphate. Step 7 cashes that in as ATP. Step 10 works because the enol formed is unstable: its tautomerisation to pyruvate makes the step strongly downhill.

### Standard values mislead

Lesson 06.4 gave the rule: the Gibbs energy of a reaction in the cell is

$$\Delta G = \Delta G^{\circ\prime} + RT\ln Q$$

with $Q$ built from actual concentrations in mol/L (lesson [13.6](../module-13/lesson-06.md)). For aldolase, $\Delta G^{\circ\prime}$ = +24 kJ/mol: in a test tube at 1 M, the reaction runs backwards. But it makes two products from one substrate, and at the micromolar concentrations of a cell $Q = [\mathrm{DHAP}][\mathrm{GAP}]/[\mathrm{FBP}]$ is tiny. In red cells $\ln Q \approx -9.7$ and $RT\ln Q \approx -25$ kJ/mol, so $\Delta G \approx -1$ kJ/mol: the step is close to equilibrium and runs forward.

### Near-equilibrium and far-from-equilibrium steps

When you compute $\Delta G$ for all ten steps in a red cell (Part A), they fall into two groups:

- Three steps, hexokinase, phosphofructokinase-1 and pyruvate kinase, have $\Delta G$ of −20 to −32 kJ/mol. They are **far from equilibrium**: they go one way only, and their rate is set by how much active enzyme there is.
- The other seven are within a few kJ/mol of zero, **near equilibrium**. Their enzymes are fast enough that the step runs forward and backward almost equally, and the net flux follows small changes in concentration.

This has three consequences:

1. **Control sits at the irreversible steps.** Phosphofructokinase-1 is inhibited allosterically by ATP and activated by AMP (lesson [29.3](lesson-03.md)): when energy is plentiful, glycolysis slows.
2. **Making glucose needs bypasses.** Gluconeogenesis uses the seven near-equilibrium enzymes in reverse but needs different enzymes to get round the three irreversible steps.
3. **Inhibition shifts concentrations upstream.** Block a step and its substrate accumulates until either its rate recovers or the steps before it slow. A competitive inhibitor is then partly overcome; an uncompetitive one becomes more effective. You will put a number on this in the practical.

### When the numbers do not add up

Some near-equilibrium steps come out slightly positive in Part A, which would mean they run backwards. They do not. The inputs are uncertain at the few-kJ/mol level: $\Delta G^{\circ\prime}$ values are usually measured at 25 °C and depend on Mg²⁺ and ionic strength, and micromolar metabolites such as 1,3-bisphosphoglycerate are hard to measure and partly bound to proteins, so their free concentration is not the total. Judge the pattern, not the second digit: a step at −25 kJ/mol is irreversible whatever the error; a step at +5 kJ/mol is "near equilibrium" within the error.

## Worked example

### 1. Is phosphofructokinase-1 far from equilibrium in a red cell?

$\mathrm{F6P + ATP \rightarrow FBP + ADP}$, $\Delta G^{\circ\prime}$ = −14.0 kJ/mol. Red-cell concentrations (mM): F6P 0.024, ATP 1.47, FBP 0.0075, ADP 0.23. At 37 °C, $RT$ = 2.579 kJ/mol.

1. $Q = \dfrac{[\mathrm{FBP}][\mathrm{ADP}]}{[\mathrm{F6P}][\mathrm{ATP}]} = \dfrac{0.0075 \times 0.23}{0.024 \times 1.47} = 0.049$ (the mM units cancel here because there are two species on each side).
2. $RT\ln Q = 2.579 \times (-3.02) = -7.8$ kJ/mol.
3. $\Delta G = -14.0 - 7.8 = -21.8$ kJ/mol.

The equilibrium constant is $K = e^{14.0/2.579} = 228$, but the cell keeps $Q$ at 0.049, more than 4000 times below it. The step can only run forward, and the cell controls it by changing how active the enzyme is.

### 2. What does an inhibitor do upstream?

Suppose phosphofructokinase-1 is half-inhibited, but hexokinase keeps supplying F6P at the same rate. For flux to return to normal through a Michaelis–Menten enzyme with $K_m$ = 0.1 mM running at [F6P] = 0.024 mM, how much must F6P rise if the inhibitor is competitive with $[\mathrm{I}] = K_i$ ($\alpha$ = 2)?

1. Normal rate: $v = V \times 0.024/(0.1 + 0.024) = 0.194V$.
2. Inhibited: $v = V[\mathrm{S}]/(0.2 + [\mathrm{S}])$. Setting this to $0.194V$ gives $[\mathrm{S}] = 0.194 \times 0.2/(1 - 0.194) = 0.048$ mM.

F6P only has to double, and because steps 1–2 are coupled to it, G6P rises too. A competitive inhibitor of a pathway enzyme is largely cancelled by this build-up, a point the practical makes quantitative. (These $K_m$ values are illustrative; real phosphofructokinase-1 is allosteric.)

## Hands-on

What you need: Python with the course packages and the [Module 29 lab folder](../../labs/module-29/). Write up Part B with the [lab report template](../../templates/lab-report.md). Time: about 2 h 20 min.

### Part A — Python: the Gibbs energy of every glycolysis step (35 min)

1. Open `lesson05_glycolysis.py`. It reads `glycolysis_steps.csv` (the ten reactions and their $\Delta G^{\circ\prime}$) and `rbc_metabolites.csv` (red-cell concentrations with the measured ranges).
2. Complete `ln_Q()` (products minus substrates, concentrations in mol/L) and `dG_actual()`.
3. Run it and open `runs/lesson05_glycolysis.png`:

```bash
py lesson05_glycolysis.py
```

4. Answer: (a) Which steps are far from equilibrium? (b) Which steps come out positive, and why is that not a contradiction? (c) Change ATP to 1.07 and ADP to 0.30 mM (the edges of the measured ranges) in your copy of the CSV and rerun. Which conclusions change?

How you know it worked: $\Delta G$ in the cell (kJ/mol): hexokinase −32.4, phosphoglucose isomerase −1.2, phosphofructokinase-1 −21.8, aldolase −1.1, triose phosphate isomerase +5.4, GAPDH +8.1, phosphoglycerate kinase −3.6, mutase +1.0, enolase +1.4, pyruvate kinase −21.1. Steps 6 + 7 together: +4.5 kJ/mol. Sum per glucose (steps 6–10 twice): about −80 kJ/mol.

<details><summary>Reference solution and model answers</summary>

```python
def ln_Q(substrates, products, conc):
    return sum(math.log(conc[s]) for s in products) - sum(math.log(conc[s]) for s in substrates)

def dG_actual(dG0_kJ, lnQ, T=T37):
    return dG0_kJ + R * T * lnQ / 1000
```

Full code: `lesson05_glycolysis_solution.py`.

(a) Steps 1, 3 and 10, at −21 to −32 kJ/mol: the regulated, irreversible steps. (b) Steps 5, 6, 8 and 9, up to +8 kJ/mol. They must be slightly negative in a working cell, so the inputs carry errors of that size: standard values measured at 25 °C and other Mg²⁺ levels, a model's concentrations, and a 1,3-bisphosphoglycerate level near 1 µM that is partly protein-bound. Steps 6 and 7 share that intermediate, so their sum is more reliable than either alone. (c) The ATP-using and ATP-making steps shift by 1–2 kJ/mol; the grouping into three far-from-equilibrium steps and seven near-equilibrium steps does not change.

</details>

### Part B — module practical: characterise enzyme E1 and three candidate drugs (105 min)

This practical uses every lesson of the module: rate laws and fitting (29.2), inhibition types and model choice (29.3), what an active-site inhibitor does (29.4) and pathway thinking (this lesson). Enzyme E1 makes the first step of a two-step pathway. A team has three candidate inhibitors, X, Y and Z, and wants to know how each works and which will still block the pathway when E1's substrate piles up.

1. Open `lesson05_practical.py`. It reads `practical_rates.csv`: duplicate initial rates at six [S] (0.1–3.2 mM) without inhibitor and with each inhibitor at two concentrations. The noise is known (4 % of the rate plus 0.8 µM/min), so the fits use it as weights.
2. Complete `fit_mm()` (weighted `curve_fit` of `mm` with `sigma=sigma_of(v)`), `lineweaver_burk()` and `flux_left()` (the inhibited rate divided by the uninhibited rate at the same [S]). The global fits, AICc and a parametric bootstrap are written for you.
3. Run it (about 5 s) and open `runs/lesson05_practical.png`:

```bash
py lesson05_practical.py
```

4. Write the report with the template. Answer:
   (a) Compare $K_m$ and $V_\text{max}$ from the nonlinear fit and from Lineweaver–Burk, with the bootstrap 95 % ranges. Which would you report?
   (b) For each inhibitor, which model wins on AICc, by how much, and does the Lineweaver–Burk pattern agree? Give the inhibition constants with uncertainties.
   (c) For any inhibitor where the mixed model came second by less than about 2, what do its fitted constants say?
   (d) Each inhibitor is dosed to halve E1's rate at the normal [S] = 0.25 mM. When [S] builds up tenfold, how much flux is left with each? Which candidate would you develop to block this pathway, and what is its drawback?
   (e) Before you open `make_data.py`, write down your best estimate of every true parameter. Then compare.

How you know it worked: no inhibitor, nonlinear $V_\text{max}$ = 117.0 ± 3.1 µM/min and $K_m$ = 0.485 ± 0.026 mM; Lineweaver–Burk 120.7 µM/min and 0.514 mM; bootstrap 95 % range of $K_m$ 0.435–0.541 mM (nonlinear) against 0.410–0.586 mM (Lineweaver–Burk). X: competitive, $K_i$ = 0.21 ± 0.01 mM (AICc 2.5 below mixed, whose $K_i'$ runs to infinity). Y: uncompetitive, $K_i'$ = 0.83 ± 0.04 mM (2.5 below mixed). Z: mixed, $K_i$ = 0.29 ± 0.02 and $K_i'$ = 1.37 ± 0.17 mM (48 below the next). Doses for half rate at 0.25 mM: X 0.32, Y 2.48, Z 0.39 mM; flux left when [S] reaches 2.5 mM: X 0.80, Y 0.29, Z 0.68.

<details><summary>Reference solution and model answers</summary>

```python
def fit_mm(S, v):
    popt, pcov = curve_fit(mm, S, v, p0=(v.max(), np.median(S)), sigma=sigma_of(v), absolute_sigma=True)
    return popt, np.sqrt(np.diag(pcov))

def lineweaver_burk(S, v):
    slope, intercept = np.polyfit(1 / S, 1 / v, 1)
    return 1 / intercept, slope / intercept

def flux_left(S, I, V, K, Ki, Kii):
    return mixed(S, I, V, K, Ki, Kii) / mm(S, V, K)
```

Full code: `lesson05_practical_solution.py`.

(a) The two methods agree within their uncertainty here, but the bootstrap range of Lineweaver–Burk is about two-thirds wider; report the nonlinear values with their standard errors. (b) X competitive (lines meet on the 1/v axis), Y uncompetitive (parallel lines), Z mixed (lines meet left of the axis, above the 1/[S] axis). The true values are $K_i$ = 0.20 mM for X, $K_i'$ = 0.80 mM for Y, and 0.30 and 1.20 mM for Z, all within about two standard errors. (c) For X the mixed fit sends $K_i'$ to infinity, and for Y it gives $K_i$ = 138 ± 870 mM: the extra constant is not supported by the data, so choose the simpler model. In repeated noisy copies the simple test still picks the wrong model about one time in ten for X and Y; more inhibitor concentrations would separate them better. (d) X loses most of its effect as substrate builds up (0.80 of the flux returns), Z keeps some, Y gets stronger (only 0.29 left). Y is the candidate for blocking the pathway, but it needs a high dose (2.5 mM, a weak binder) and, because its effect grows as substrate accumulates, it could shut the pathway down more than intended; a medicinal chemist would now try to make it bind more tightly. (e) Your estimates should be within the uncertainties above; $V_\text{max}$ = 120 µM/min and $K_m$ = 0.50 mM.

</details>

## Common mistakes

- Using $\Delta G^{\circ\prime}$ to decide which steps are reversible in a cell. Aldolase has +24 kJ/mol but runs forward at about −1 kJ/mol.
- Forgetting that concentrations in $Q$ must be in mol/L when a step changes the number of molecules, as aldolase does.
- Taking a slightly positive computed $\Delta G$ as proof that a step runs backwards, instead of as a measure of the input uncertainty.
- Expecting to control a pathway by inhibiting a near-equilibrium enzyme. Small concentration changes restore its flux.
- Choosing an inhibitor from its IC50 at normal substrate alone, without asking what happens when substrate accumulates.
- Opening `make_data.py` before writing your own answer. The practical trains you to judge data that come without an answer key.

## Key takeaways

- Glycolysis is ten organic reactions: phosphoryl transfers, isomerisations through enediols, a retro-aldol through a Schiff base, a thioester-forming oxidation, and a dehydration.
- Use $\Delta G = \Delta G^{\circ\prime} + RT\ln Q$ with cell concentrations; in red cells only hexokinase, phosphofructokinase-1 and pyruvate kinase are far from equilibrium (−21 to −32 kJ/mol).
- Far-from-equilibrium steps are the control points: they are regulated allosterically and bypassed in gluconeogenesis.
- Inhibiting a step raises its substrate; competitive inhibitors are partly overcome, uncompetitive ones get stronger.
- The module practical combined nonlinear fitting, model choice by AICc and pathway reasoning to rank three inhibitors.

## Sources

- [Jakubowski and Flatt, 13.1 Glycolysis](https://bio.libretexts.org/Bookshelves/Biochemistry/Fundamentals_of_Biochemistry_(Jakubowski_and_Flatt)/02%3A_Unit_II-_Bioenergetics_and_Metabolism/13%3A_Glycolysis_Gluconeogenesis_and_the_Pentose_Phosphate_Pathway/13.01%3A_Glycolysis) — the ten steps, their enzymes and $\Delta G^{\circ\prime}$ values; aldolase Schiff-base and GAPDH thioester mechanisms.
- [Protasov et al. (2019), Sci. Rep. 9, 1455](https://www.nature.com/articles/s41598-018-37828-5) — measured ranges and model steady-state concentrations of glycolytic intermediates, adenine nucleotides, NAD and phosphate in human red cells (Tables 1 and 2), CC BY 4.0.
- [OpenStax Biology 2e, 6.5 Enzymes](https://openstax.org/books/biology-2e/pages/6-5-enzymes) — allosteric and feedback regulation of metabolic enzymes.
- [MIT OCW 5.07SC Biological Chemistry I](https://ocw.mit.edu/courses/5-07sc-biological-chemistry-i-fall-2013/) — Module II, glycolysis, gluconeogenesis and the regulation of metabolism.
