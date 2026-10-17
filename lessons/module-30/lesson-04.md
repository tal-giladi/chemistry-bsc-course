---
id: "30.4"
module: 30
minutes: 25
practice_minutes: 120
prerequisites: ["12.2", "12.6", "19.1", "20.4", "30.1", "30.2", "30.3"]
objectives:
  - Apply Kuhn's free-electron model to a cyanine dye series, count π electrons and box length, and calculate the HOMO–LUMO absorption wavelength.
  - Fit a bond length and an end extension to published λmax values with uncertainties and a parameter correlation, and test the model with a blind prediction.
  - Explain why the box model works for cyanines but fails for polyenes such as β-carotene, and estimate the bond-alternation gap.
  - Write a complete lab report that compares the model, the data and the limits of both (module practical).
volatility: concept
sources:
  - title: "Kuhn, A quantum-mechanical theory of light absorption of organic dyes and similar compounds, J. Chem. Phys. 17, 1198 (1949)"
    url: https://doi.org/10.1063/1.1747143
  - title: "Autschbach, Why the particle-in-a-box model works well for cyanine dyes but not for conjugated polyenes, J. Chem. Educ. 84, 1840 (2007)"
    url: https://doi.org/10.1021/ed084p1840
  - title: "LibreTexts, Duke Physical Chemistry Lab: Absorption Spectrum of Conjugated Dyes, procedure"
    url: https://chem.libretexts.org/Courses/Duke_University/Duke_Physical_Chemistry_Laboratory/03%3A_Physical_Chemistry_Lab_Manual/04%3A_Absorption_Spectrum_of_Conjugated_Dyes/4.02%3A_Proceedure_(Part_I)__Collect_Spectra_Apply_PIB
  - title: "TCI product D4486, 1,1'-Diethyl-2,2'-cyanine iodide (absorption maximum in methanol)"
    url: https://www.tcichemicals.com/BE/en/p/D4486
  - title: "TCI product C0426, Cryptocyanine (absorption maximum in methanol)"
    url: https://www.tcichemicals.com/AT/en/p/C0426
  - title: "Sigma-Aldrich product 166510, 1,1'-Diethyl-2,2'-carbocyanine iodide"
    url: https://www.sigmaaldrich.com/US/en/product/aldrich/166510
  - title: "Delta State University lab handout: particle in a box, visible spectra of dyes (literature values from Laidlaw 1970)"
    url: http://ntweb.deltastate.edu/jbentley/teaching/labman/dyes/dyes.htm
  - title: "OMLC PhotochemCAD: beta-carotene absorption spectrum"
    url: https://omlc.org/spectra/PhotochemCAD/html/041.html
  - title: "PubChem: Methanol (CID 887), safety and hazards"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/887
last_verified: "2026-10-17"
---

# 30.4 · Electronic spectra of conjugated dyes: particle in a box

In lesson [12.2](../module-12/lesson-02.md) you treated the π electrons of a cyanine dye as particles in a box and got the colour within 10 %. In [12.6](../module-12/lesson-06.md) you fitted the box to three dyes and found the fit was too flexible to be a real test. This lesson is the version that physical chemistry labs actually run: the 1,1′-diethyl quinoline cyanines, measured in methanol, with a fourth dye held back for a blind test and a natural pigment, β-carotene, as the case where the model breaks. It is also the module practical: you finish by writing the full report, using the fitting, uncertainty and model-testing habits of the whole module.

## Why it matters

Cyanine dyes are workhorses: they sensitise photographic film, stain DNA in gels, label antibodies in medical imaging (indocyanine green) and sit in the dye lasers and optical discs of the last forty years. Designing one means choosing a chain length for a target colour, and the free-electron model makes that a one-line calculation. Knowing when it works (cyanines) and when it fails (polyenes, the pigments of carrots and of your retina) separates a useful rule from a misleading one.

## Core ideas

> [!NOTE]
> The physics is stable. The dye maxima are published values checked on 2026-10-17 (supplier specifications from TCI and Sigma-Aldrich, a classic textbook value via a university lab handout, and the PhotochemCAD β-carotene spectrum). Values for the same dye differ by 2–6 nm between sources and solvents; that scatter is smaller than the model errors you will find. Constants are CODATA 2022. The simulation is an educational model.

### The dyes and the box

The 1,1′-diethyl-2,2′-cyanines are two quinoline rings joined at their 2-positions by a chain of $k$ CH groups ($k$ = 1, 3, 5 for the cyanine, carbocyanine and dicarbocyanine). One nitrogen carries a positive charge, but resonance moves it to the other end just as easily:

$$\mathrm{N^+{=}C{-}(C{=}C)_n{-}N} \;\longleftrightarrow\; \mathrm{N{-}(C{=}C)_n{-}C{=}N^+}$$

Because the two structures are equal, every bond along the path between the nitrogens is halfway between single and double. The π electrons see an almost flat potential along the chain: a box.

Kuhn (1949) counted the box as follows. Let $p$ be the number of carbon atoms on the conjugated path from one nitrogen to the other ($p$ = 3, 5, 7 for the 2,2′ series: the two ring carbons C2 and C2′ plus the chain). Then:

- **π electrons:** $N = p + 3$ (one from each carbon, three from the two nitrogens).
- **Box length:** $L = (p + 3 + \alpha)\,\ell$, where $\ell$ is the bond length along the chain. With $\alpha = 0$ the box runs one bond beyond each nitrogen; $\alpha$ adds extra length for the electrons that spill into the rings.
- **Absorption:** the HOMO is level $N/2$, the LUMO $N/2 + 1$, and as in 12.2

$$\lambda = \frac{8m_ecL^2}{h(N + 1)}$$

Tiny example: with $\ell$ = 0.139 nm and $\alpha$ = 0, $8m_ec\ell^2/h$ = 63.7 nm, so $\lambda = 63.7\,(p+3)^2/(p+4)$ nm. For $p = 3$ that is 328 nm. The measured value is 523 nm. The bare box is far too small for dyes with big aromatic end groups.

### Calibrate, fit, predict

A model with adjustable parameters can always be made to fit; the test is what it predicts. Three steps, from weakest to strongest:

1. **Calibrate on one dye.** Fix $\ell$ = 0.139 nm and choose $\alpha$ so that $p = 3$ gives 523 nm: $\alpha$ = 1.58. Then predict $p$ = 5 and 7.
2. **Fit two parameters to three dyes.** Least squares on $\ell$ and $\alpha$. With three points and two parameters there is one degree of freedom left: a small residual is expected, not impressive. Report the uncertainties and the **correlation coefficient** between $\ell$ and $\alpha$ (a longer bond and a shorter end extension describe almost the same box, so they trade off; a correlation near −1 says the data cannot separate them).
3. **Predict a dye you did not fit.** The 4,4′-carbocyanine (cryptocyanine) joins the quinolines at their 4-positions. The path from nitrogen through the ring to C4 is two bonds longer at each end, so Kuhn's count gives $p$ = 9. The 2,2′ fit then makes a prediction you can check against its measured 708 nm.

### Why polyenes fail

β-Carotene, the orange pigment of carrots, has 11 conjugated C=C bonds: $N$ = 22 π electrons over about 22 bonds. A box of $22 \times 0.139$ nm predicts 1340 nm, in the infrared. It absorbs at 451 nm (in hexane), deep in the blue.

The difference is resonance. A neutral polyene has no second, equal structure: its bonds really alternate, short double and long single. The electrons see a ripple of potential along the chain, and a ripple opens a gap that does not close as the chain grows (the same physics makes silicon a semiconductor). Kuhn added it as an extra term:

$$\Delta E = \frac{h^2(N + 1)}{8m_eL^2} + V_0\left(1 - \frac{1}{N}\right)$$

For β-carotene the observed 2.75 eV against the box's 0.92 eV gives $V_0 \approx$ 1.9 eV. Because of $V_0$, long polyenes converge towards a limiting colour, while long cyanines keep moving about 100 nm to the red per added CH=CH (Autschbach 2007 explains the contrast with modern calculations).

### The real experiment and why each step

1. **Make a 10⁻⁴ mol/L stock in methanol and dilute** to a peak absorbance of 0.3–1 in a 1 cm cell; with $\varepsilon \approx 1$–$2 \times 10^5$ L mol⁻¹ cm⁻¹ ([19.1](../module-19/lesson-01.md)) that is about 5 × 10⁻⁶ mol/L.
2. **Record against a methanol blank from 400 to 800 nm**, to remove the cell and the solvent.
3. **Take λmax at the top of the main band, not at a shoulder.** Each cyanine band has a vibronic shoulder about 1200 cm⁻¹ to the blue (the Franck–Condon progression of [20.4](../module-20/lesson-04.md)); at high concentration a second band from dimers (aggregates) also grows there.
4. **Check by diluting twice.** If the band shape changes with concentration, aggregation is distorting it.

Safety reasoning: cyanine dyes are lab reagents, intensely staining and treated as toxic irritants; methanol is highly flammable and toxic by ingestion, skin contact and inhalation (PubChem GHS: H225, H301 + H311 + H331, H370). Real labs use gloves, a fume hood and small volumes. Neither belongs in a kitchen; the home extension below uses food only.

## Worked example

### The three 2,2′ dyes with the bare box and with a calibrated $\alpha$

$p$ = 3, 5, 7; measured 523, 605, 705 nm.

1. Bare box ($\alpha$ = 0): $63.7 \times 36/7$ = 328, $63.7 \times 64/9$ = 453, $63.7 \times 100/11$ = 579 nm. Every value is 120–200 nm short.
2. Calibrate $\alpha$ on $p$ = 3: $(6 + \alpha)^2 = 523 \times 7/63.7 = 57.5$, so $6 + \alpha$ = 7.58 and $\alpha$ = 1.58.
3. Predict $p$ = 5: $63.7 \times 9.58^2/9$ = 650 nm (measured 605, +7 %). $p$ = 7: $63.7 \times 11.58^2/11$ = 777 nm (measured 705, +10 %).

Interpretation: the calibrated model makes each CH=CH step 127 nm instead of the measured 80–100 nm. Fitting $\ell$ and $\alpha$ together (Hands-on) gives $\ell$ ≈ 0.120 nm, close to the 0.124 nm of the Simpson dyes in 12.6: the box "bond length" is an effective parameter, not a crystal-structure distance.

### β-carotene

$N$ = 22, $L = 22 \times 0.139$ nm = 3.058 nm: $\lambda = 8m_ecL^2/(23h) = 63.7 \times 22^2/23$ = 1340 nm, so the box gap is 1239.8/1340 = 0.925 eV. Observed: 1239.8/451 = 2.749 eV. $V_0 = (2.749 - 0.925)/(1 - 1/22) = 1.91$ eV.

## Hands-on

What you need: a browser, Python with the course packages, the [Module 30 lab folder](../../labs/module-30/) (`lesson04_dyes.py`, `cyanine_dyes.csv`) and the [lab report template](../../templates/lab-report.md). Optional kitchen extension: a carrot, tomato paste, cooking oil, two clear glasses, a white sheet of paper and, if you built it in [25.1](../module-25/lesson-01.md), your phone spectrometer. Time: about 120 minutes, including the report. The dye spectra themselves need a lab spectrophotometer and lab reagents; you work from published maxima, which trains the analysis but not the sample preparation.

### Part A — simulation: the dye box (20 min)

[Simulation: Quantum box — conjugated dye series](../../simulations/quantum-box/index.html?preset=dye)

1. Start with the cyanine with $p$ = 3. Fill the levels with 6 electrons and find the HOMO and LUMO. Read the wavelength of the HOMO → LUMO jump.
2. Add CH=CH units ($p$ = 5, 7, 9) and write down λ for each.
3. Increase the end extension until $p$ = 3 gives 523 nm, then step $p$ again and compare with 605 and 705 nm.
4. Switch on the alternating ("polyene") potential at about 2 eV and watch the gap stop shrinking as the chain grows.

How you know it worked: without alternation λ grows by a similar step per CH=CH; with it the wavelengths bunch up towards a limit.

### Part B — Python: fit, predict, break (40 min)

Open `lesson04_dyes.py`. Complete `lambda_box()` (Kuhn's formula, three lines) and `polyene_V0()` (two lines). Run:

```bash
py lesson04_dyes.py
```

How you know it worked: the bare box gives 328, 453 and 579 nm; $\alpha$ calibrated on one dye is 1.58 with predictions 523, 650, 777 nm; the two-parameter fit gives $\ell$ = 0.1199 ± 0.0025 nm and $\alpha$ = 2.77 ± 0.22 with a correlation of −0.99 and residuals of −2.6, +5.4, −2.8 nm; the blind prediction for the 4,4′-carbocyanine is 795 nm against 708 nm (+12 %), which is what the fitted model would give for $p$ ≈ 7.1; β-carotene's box gives 1341 nm and $V_0$ = 1.91 eV. The plot goes to `runs/lesson04_dyes.png`.

<details><summary>Reference solution and discussion</summary>

```python
N = np.asarray(p, float) + 3
L = (N + alpha) * l_nm * 1e-9
return 8 * M_E * C * L**2 / (H * (N + 1)) * 1e9               # lambda_box
box_gap = HC_EV_NM / float(lambda_box(N - 3, l_nm, 0.0))
return (HC_EV_NM / lam_obs - box_gap) / (1 - 1 / N)            # polyene_V0
```

Full code: `lesson04_dyes_solution.py`.

What the numbers say. The fit is excellent and nearly meaningless on its own: two parameters, three points, a correlation of −0.99. The blind test carries the information, and it fails by 12 %: counting the ring atoms of the 4,4′ path overestimates the box. The electrons spread over the whole quinoline, and the effective box is about one CH=CH longer than in the 2,2′ carbocyanine, not two. A parameter fitted to one family transfers to that family only.

</details>

### Part C — the module practical: full report (45 min)

Write a two-page report with the template, as if you had measured the four dyes yourself:

1. **Aim and model.** The box, the electron count, the three levels of test.
2. **Data.** The table of λmax with solvent and source, and a sentence on the 2–6 nm spread between sources.
3. **Results.** The three model stages with numbers and units; $\ell$ and $\alpha$ with uncertainties and their correlation; the plot.
4. **Test.** The blind prediction for cryptocyanine and what its failure means.
5. **Limits.** β-carotene and $V_0$; why cyanines are boxes and polyenes are not.
6. **Module comparison (one paragraph).** The HCl fit to 0.01 cm⁻¹ against its 16 % Morse miss (30.1), first-order hyperfine theory against Breit–Rabi (30.2), the end correction designed out (30.3): what do the four experiments teach about trusting a model?

How you know it worked: a reader who has not seen this lesson can tell what was assumed, fitted and predicted, and how well each worked.

### Optional kitchen extension — the polyene colours (15 min)

> [!CAUTION]
> Use only food: a carrot, a teaspoon of tomato paste and cooking oil at room temperature. Do not heat the oil. Grate carefully, away from your fingers. Carotenoids stain cloth and plastic orange; wash spills with soap at once. Do not eat the mixtures afterwards if they have stood for hours.

1. Grate half a carrot into a glass with 50 mL of cooking oil; stir a teaspoon of tomato paste into another 50 mL. Stir for 2 minutes and let them settle for 15 minutes.
2. Look at each oil layer against white paper in daylight. Carrot oil is yellow-orange (β-carotene absorbs blue near 450–480 nm); tomato oil is redder, because lycopene's 11 conjugated C=C bonds have no rings twisting the chain ends.
3. If you have the phone spectrometer, locate the absorption band of each layer.

How you know it worked: two clearly different oranges from two molecules with the same number of π electrons. That alone is evidence against a pure box, which would make them the same colour.

## Common mistakes

- **Counting the box from nitrogen to nitrogen only.** Kuhn's box extends about one bond beyond each nitrogen, and big end groups extend it further; that is what $\alpha$ is for.
- **Using $N$ = number of double bonds.** $N$ counts π electrons: $p + 3$ for a cyanine, twice the C=C count for a polyene.
- **Calling a two-parameter fit to three points a confirmation.** One degree of freedom is left. Report the correlation and test on a dye you did not fit.
- **Reading λmax at the vibronic shoulder or at an aggregate band.** Use the main peak of a dilute solution and check that the shape does not change on dilution.

## Key takeaways

- Cyanines have two equal resonance structures, so their bonds are equalised and their π electrons behave like particles in a box.
- Kuhn's model: $N = p + 3$, $L = (p + 3 + \alpha)\ell$, $\lambda = 8m_ecL^2/h(N+1)$.
- A fit to the 2,2′ series gives $\ell \approx$ 0.120 nm and $\alpha \approx$ 2.8 bonds, strongly correlated; it predicts the 4,4′ dye 12 % too red.
- Polyenes have alternating bonds and an extra gap $V_0 \approx$ 2 eV; their colour converges instead of shifting steadily with length.
- A model earns trust by predicting data it was not fitted to, the common thread of this whole module.

## Sources

- [Kuhn, J. Chem. Phys. 17, 1198 (1949)](https://doi.org/10.1063/1.1747143) — the free-electron model, electron count, box length and polyene alternation term.
- [Autschbach, J. Chem. Educ. 84, 1840 (2007)](https://doi.org/10.1021/ed084p1840) — why the box works for cyanines but not polyenes.
- [LibreTexts, Duke Physical Chemistry Lab: conjugated dyes procedure](https://chem.libretexts.org/Courses/Duke_University/Duke_Physical_Chemistry_Laboratory/03%3A_Physical_Chemistry_Lab_Manual/04%3A_Absorption_Spectrum_of_Conjugated_Dyes/4.02%3A_Proceedure_(Part_I)__Collect_Spectra_Apply_PIB) — the four dyes and the procedure.
- [TCI D4486](https://www.tcichemicals.com/BE/en/p/D4486) — 1,1′-diethyl-2,2′-cyanine iodide, λmax 521–526 nm in methanol.
- [Sigma-Aldrich 166510](https://www.sigmaaldrich.com/US/en/product/aldrich/166510) — 1,1′-diethyl-2,2′-carbocyanine iodide, main band 602–608 nm in ethanol.
- [Delta State University dye lab handout](http://ntweb.deltastate.edu/jbentley/teaching/labman/dyes/dyes.htm) — literature values 525, 610 and 705 nm (Laidlaw 1970) for the 2,2′ series.
- [TCI C0426](https://www.tcichemicals.com/AT/en/p/C0426) — cryptocyanine, λmax 708 nm in methanol.
- [OMLC PhotochemCAD: β-carotene](https://omlc.org/spectra/PhotochemCAD/html/041.html) — absorption maximum 451 nm, ε = 139 500 L mol⁻¹ cm⁻¹ (hexane, Zechmeister).
- [PubChem: Methanol (CID 887)](https://pubchem.ncbi.nlm.nih.gov/compound/887) — GHS hazards of the lab solvent.
