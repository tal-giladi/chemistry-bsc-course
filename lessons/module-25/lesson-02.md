---
id: "25.2"
module: 25
minutes: 22
practice_minutes: 90
prerequisites: ["19.2", "25.1", "09.4"]
objectives:
  - Set up a fluorescence measurement of quinine (excitation and emission wavelengths, acid medium, dilution) and explain each choice.
  - Recognise the inner-filter effect and chloride quenching in fluorescence data, and calculate a Stern-Volmer constant from a quenching series.
  - Calculate an analyte concentration with its uncertainty by external calibration and by standard addition, and decide which one a sample needs.
  - Run a safe home fluorescence experiment with tonic water and a UV flashlight, and judge a result against the 83 mg/L legal limit.
volatility: concept
sources:
  - title: "eCFR, 21 CFR 172.575 Quinine"
    url: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-172/subpart-F/section-172.575
  - title: "Harvey, Analytical Chemistry 2.1, 10.6 Photoluminescent Spectroscopy (LibreTexts)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.06%3A_Photoluminescent_Spectroscopy
  - title: "PhotochemCAD (OMLC), Quinine sulfate absorption and fluorescence"
    url: https://omlc.org/spectra/PhotochemCAD/html/081.html
  - title: "PubChem, Quinine (CID 3034034)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/3034034
  - title: "University of Victoria OHSE, Ultraviolet light guidelines"
    url: https://www.uvic.ca/ohse/_assets/docs/radiation-safety-folder/uv-light-guidelines.pdf
last_verified: "2026-10-17"
---

# 25.2 · Fluorescence: quinine in tonic water

Shine an ultraviolet torch on a glass of tonic water in a dark room and it glows sky blue. The glow is quinine, the bitter compound in tonic, absorbing invisible UV light and sending part of the energy back out as visible light. The same effect, measured carefully in a fluorimeter, is the standard method for quinine in drinks and in blood. In this lab you see it at home, map its pitfalls with your phone camera, and then measure quinine properly with an external calibration and a standard addition. The theory of fluorescence and quenching is in [Lesson 19.2](../module-19/lesson-02.md).

## Why it matters

In the United States, quinine is permitted in carbonated drinks only up to 83 parts per million, about 83 mg/L (21 CFR 172.575), and the label must declare it. A bottler checking each batch needs a fast, specific method. Fluorescence is ideal: few other drink ingredients glow blue under 350 nm light, and the method sees well below 1 mg/L. But the same sensitivity makes it fragile. Undiluted tonic gives a reading far too low because the sample swallows its own excitation light. A pinch of salt in the sample, or hydrochloric acid used instead of sulfuric, can cut the signal in half. The lab decisions in this lesson are what keep the number honest.

## Core ideas

> [!NOTE]
> Stable: the photophysics, inner filter, Stern–Volmer quenching and the calibration methods (Harvey 10.6, checked 2026-10-17). Quinine's absorption maximum is near 347 nm with ε about 5.7 × 10³ L mol⁻¹ cm⁻¹, and emission near 450 nm (PhotochemCAD). Its quantum yield in 0.5 M H₂SO₄ is usually quoted as 0.546; a later absolute measurement gave about 0.60 and showed a temperature dependence, so it is no longer a recommended standard in sulfuric acid. The 83 mg/L limit is the US rule as shown in the eCFR on 2026-10-17; other countries set their own. Lab data are simulated.

### What a fluorimeter does

Light from a lamp passes an **excitation monochromator** set to 350 nm and enters the cell. The molecule absorbs, relaxes, and emits at longer wavelength (450 nm); the difference is the **Stokes shift**. The emitted light is collected **at 90°** through an **emission monochromator** set to 450 nm. The right angle keeps the bright lamp beam out of the detector, which is why fluorescence starts from a dark background and reaches far lower concentrations than absorbance.

### Why sulfuric acid

Quinine has two basic nitrogens. In dilute acid both are protonated, and that form fluoresces strongly. Sulfuric acid is used because its anions do not quench. Hydrochloric acid would supply chloride, a strong quencher of quinine. Standards and samples are therefore made in the same 0.05 M H₂SO₄.

### Inner filter: when the sample is too strong

Fluorescence is proportional to concentration only while the sample absorbs little of the excitation light, roughly $A < 0.01$ across the cell. Tonic water has about 70 mg/L quinine, $2.2 \times 10^{-4}$ M, so

$$A_{350} \approx 5700 \times 2.2\times10^{-4} \times 1 \approx 1.2 \text{ per cm}$$

The UV is absorbed in the first few millimetres. At home you can see it: in full-strength tonic the glow hugs the side where the torch enters. In a fluorimeter, the centre of the cell receives almost no excitation, and the reading is far too low. Dilute at least 100-fold before measuring. The signal from a dilution series bends over like $1 - 10^{-A}$ instead of rising straight.

### Quenching by chloride

A **quencher** takes the energy from the excited molecule before it can emit. For collisional quenching the **Stern–Volmer equation** holds:

$$\frac{F_0}{F} = 1 + K_\mathrm{SV}[\mathrm{Q}]$$

For quinine and chloride $K_\mathrm{SV}$ is about 130 L/mol. At 7.7 mmol/L chloride (0.045 g of table salt per 100 mL) the signal is already halved. Table salt is therefore the perfect kitchen quencher, and a reminder that a sample's matrix can change the slope of the calibration.

### External calibration or standard addition?

An **external calibration** uses standards in clean acid and assumes the sample responds in the same way. **Standard addition** adds known amounts of quinine to portions of the sample itself, so any matrix effect that scales the signal (quenching, a coloured matrix that absorbs the excitation light) affects standards and analyte equally. Plot signal against amount added and extrapolate to zero signal: the intercept on the x axis gives the sample concentration. The price is more work per sample and a larger uncertainty, because of the extrapolation (Lesson [09.4](../module-09/lesson-04.md)). If the two methods agree, the matrix is harmless and external calibration is fine for routine work.

### UV torches and your eyes

Cheap "UV" torches sold for finding stains emit at 395 nm (violet, partly visible) or 365 nm (true UV-A). Quinine absorbs much better at 365 nm, so the glow is brighter. UV-A damages the eye without any warning: there is no pain while you look, and inflammation of the cornea (photokeratitis) can appear hours later. Repeated exposure is linked to cataracts.

## Worked example

### 1. Quinine in tonic by standard addition

A tonic is diluted 1 + 99 in 0.05 M H₂SO₄. Five 10.00 mL flasks each get 5.00 mL of the dilution plus 0, 0.1, 0.2, 0.3 or 0.4 mg/L of added quinine (final concentrations), made up with acid. The fluorescence (blank subtracted) gives the line $F = 359 + 966 \times c_\text{added}$.

The x intercept is $359/966 = 0.372$ mg/L in the flask. The flask holds the diluted tonic at half strength, and the dilution was 100-fold:

$$c_\text{tonic} = 0.372 \times 2 \times 100 = 74.3 \text{ mg/L}$$

With the uncertainty from the fit (about ± 2 mg/L at 95 %), the tonic is below the 83 mg/L limit, but not by a wide margin. A result of 82 ± 2 mg/L would be "not clearly below" and would need more replicates.

### 2. How much salt halves the glow?

$F/F_0 = 0.5$ means $K_\mathrm{SV}[\mathrm{Cl^-}] = 1$, so $[\mathrm{Cl^-}] = 1/130 = 7.7$ mmol/L. With 58.44 g/mol for NaCl, that is 0.45 g/L, or 0.045 g per 100 mL: a small pinch in a glass.

## Hands-on

> [!WARNING]
> Never look into a UV flashlight, and never look at its reflection in a mirror, window, tiles or a shiny glass. Never point it at people or pets. Shine it sideways at the glass, keep it below eye level, and switch it off between photos. Wear ordinary safety glasses or UV-blocking glasses; they reduce, but do not remove, the risk. Children only with an adult. Do not drink the tonic once it has been used in the experiment.

What you need: tonic water (regular or diet; it must say "quinine" on the label), tap water, table salt, a kitchen scale that reads 0.1 g (or a 1/4 teaspoon, about 1.5 g), 8 identical clear glasses or cups, a UV flashlight (365 nm is best, 395 nm works less well), a dark room, a black cloth or card as background, a phone on a stand, the [Module 25 lab folder](../../labs/module-25/) and the [lab report template](../../templates/lab-report.md). Time: about 90 minutes. The home part trains observation and calibration logic; it does not replace a fluorimeter's wavelength selection.

### Part A — simulation: build the fluorescence method (20 min)

[Simulation: Spectrometer — quinine fluorescence](../../simulations/spectrometer/index.html?preset=fluorescence)

1. Record an excitation spectrum (emission fixed at 450 nm) and an emission spectrum (excitation fixed at 350 nm). Note both maxima and the Stokes shift.
2. Measure undiluted tonic, then 1 + 9, 1 + 99 and 1 + 199. Which dilution is the first whose signal scales with dilution?
3. Prepare tonic in 0.05 M HCl instead of H₂SO₄. Compare the signal and explain it.
4. Run a five-point external calibration and a five-flask standard addition on the 1 + 99 dilution. Compare the two answers.

How you know it worked: excitation peak near 350 nm, emission near 450 nm; undiluted tonic reads far below the line; the HCl sample reads clearly lower; the two calibration methods agree within their uncertainty for tonic.

### Part B — home: tonic water under UV light (40 min)

1. Set up in the dark: glass on the black cloth, phone on a stand at the glass's side, torch shining in from the other side at 90° to the camera (the fluorimeter geometry). Lock exposure and white balance.
2. Shine the torch into full-strength tonic. Note where the glow is brightest. Compare with a glass of water and of a non-tonic soft drink.
3. **Dilution series.** Make tonic fractions 1, 1/2, 1/4, 1/8, 1/16 and 1/32 with water (for example 100 mL tonic + 100 mL water, then halve again). Photograph each twice, same position, same distance.
4. **Salt series.** In the 1/8 dilution, dissolve 0, 0.05, 0.1, 0.2, 0.4 and 0.8 g of salt per 100 mL (use fresh 100 mL portions). Photograph each twice.
5. On a computer, read the mean blue value of the glowing region and of the dark background for each photo (any photo editor's colour picker, or a small crop in Python). Save the numbers as a CSV with the columns of `tonic_home_example.csv`.

How you know it worked: the glow in full tonic is concentrated at the entry side; the dilutions fade, but not in proportion at the strong end; each step of salt visibly dims the glow.

### Part C — Python: Stern–Volmer and the tonic result (30 min)

Open `lesson02_quinine.py`. Complete `stern_volmer()` (TODO 1) and `tonic_by_standard_addition()` (TODO 2). Run it on the example data, then on yours:

```bash
py lesson02_quinine.py
py lesson02_quinine.py my_tonic.csv
```

How you know it worked: on the example data the dilution series is on the line up to 1/16 and reaches only 41 % of it at full strength; $K_\mathrm{SV}$ ≈ 138 L/mol (true 130); external calibration 72.3 ± 0.2 mg/L, standard addition 72.9 ± 0.6 mg/L (95 % interval ± 1.9), both below the limit. Home data typically give $K_\mathrm{SV}$ of 100–200 L/mol; phone noise is larger than a fluorimeter's.

<details><summary>Answer check: why the dilution series bends</summary>

At fraction $f$ the excitation path absorbs $A = a f$. The light absorbed, and so the glow, is proportional to $1 - 10^{-af}$, which is close to $2.303\,a f$ only when $af$ is small. With $a$ ≈ 1 the signal at full strength is $0.9/2.3$ ≈ 39 % of the straight-line value, close to the 41 % in the example data.

</details>

## Common mistakes

- **Measuring tonic undiluted.** The inner filter makes the reading meaningless. Dilute until the signal scales with the dilution; for tonic that is at least 1 + 99.
- **Using hydrochloric acid or a salty matrix.** Chloride quenches quinine. Use sulfuric acid, and use standard addition when the sample contains chloride you cannot remove.
- **Assuming standard addition is always better.** It corrects matrix effects that scale the signal, not a blank or an interference that adds signal. Subtract the blank first.
- **Looking at the torch to check that it works.** You cannot feel UV damage. Check it on a white sheet of paper or on the tonic instead.
- **Moving the phone between photos.** The geometry sets the scale. Fix the phone and the torch, and change only the glass.

## Key takeaways

- Quinine absorbs near 350 nm and emits near 450 nm; measure it at 90° in dilute sulfuric acid.
- Full-strength tonic absorbs its own excitation light; dilute until the signal scales with the dilution.
- Chloride quenches quinine with $K_\mathrm{SV}$ ≈ 130 L/mol, so salt halves the signal at under 0.05 g per 100 mL.
- External calibration and standard addition agree only when the matrix is harmless; when they disagree, trust standard addition and find the cause.
- A UV torch is safe only if no one looks into it or at its reflections.

## Sources

- [eCFR, 21 CFR 172.575 Quinine](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-172/subpart-F/section-172.575) — not more than 83 ppm in carbonated beverages, label declaration.
- [Harvey, Analytical Chemistry 2.1, 10.6](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.06%3A_Photoluminescent_Spectroscopy) — instrumentation, inner filter, quinine in urine and chloride.
- [PhotochemCAD, quinine sulfate](https://omlc.org/spectra/PhotochemCAD/html/081.html) — ε 5700 L mol⁻¹ cm⁻¹ at 347.5 nm, quantum yield 0.546 in 0.5 M H₂SO₄.
- [PubChem, Quinine](https://pubchem.ncbi.nlm.nih.gov/compound/3034034) — GHS H302 (harmful if swallowed) and H317 (may cause an allergic skin reaction), so lab standards are handled with gloves.
- [University of Victoria, UV light guidelines](https://www.uvic.ca/ohse/_assets/docs/radiation-safety-folder/uv-light-guidelines.pdf) — eye effects of UV: photokeratitis, cataract, no warning symptoms.
