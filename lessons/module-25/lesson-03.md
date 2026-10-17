---
id: "25.3"
module: 25
minutes: 20
practice_minutes: 90
prerequisites: ["19.2", "25.1", "09.4"]
objectives:
  - Run a flame AAS determination in the right order (lamp, wavelength and slit, flame, burner height, blank, standards, check standards) and give the reason for each step.
  - Diagnose chemical, ionisation, spectral and physical interferences from the data and choose the fix for each.
  - Calculate a metal concentration with its uncertainty, a spike recovery and a check-standard drift, and decide whether a run is acceptable.
  - Use a phone spectrometer to tell atomic line spectra from molecular bands and continua, and explain what the camera cannot see.
volatility: concept
sources:
  - title: "Harvey, Analytical Chemistry 2.1, 10.4 Atomic Absorption Spectroscopy (LibreTexts)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.04%3A_Atomic_Absorption_Spectroscopy
  - title: "Harvey, Analytical Chemistry 2.1, 10.7 Atomic Emission Spectroscopy (LibreTexts)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.07%3A_Atomic_Emission_Spectroscopy
  - title: "NIST Handbook of Basic Atomic Spectroscopic Data, strong lines of sodium"
    url: https://physics.nist.gov/PhysRefData/Handbook/Tables/sodiumtable2.htm
  - title: "Lanthanum and the phosphate interference on calcium in flame AAS, Analytical Communications (1999)"
    url: https://pubs.rsc.org/en/content/articlelanding/1999/ac/a900331b
  - title: "US Chemical Safety Board, key lessons from methanol fires in educational demonstrations"
    url: https://www.csb.gov/csb-releases-key-lessons-for-preventing-incidents-from-flammable-chemicals-in-educational-demonstrations-in-wake-of-several-serious-methanol-accidents-that-injured-children-and-adults/
last_verified: "2026-10-17"
---

# 25.3 · Atomic absorption and emission

Metals in water, food, soil and blood are measured almost everywhere by atomic spectroscopy: the sample is sprayed into a flame or plasma, broken into free atoms, and the atoms either absorb a lamp's light (atomic absorption, AAS) or emit their own (atomic emission). [Lesson 19.2](../module-19/lesson-02.md) explained why these methods work and which instrument suits which level. This lab runs a flame AAS determination of calcium in mineral water from start to finish, with the checks a real lab uses to prove the number. At home you use your phone spectrometer from [Lesson 25.1](lesson-01.md) to see the sharp lines that make atomic spectroscopy so selective.

## Why it matters

A bottled-water company prints 48 mg/L calcium on its label. An inspector's lab measures it by flame AAS and finds 40 mg/L, 17 % below the label, enough to start a legal dispute. The water is fine; the method was not. Sulfate and phosphate in the water bind calcium into compounds that do not fully break into atoms in an air–acetylene flame, so part of the calcium is invisible. One reagent, a lanthanum salt added to every standard and sample, releases it. The same lab must also show that its calibration is still valid at the end of the run and that it recovers calcium added to the sample. These checks separate a number from a result.

## Core ideas

> [!NOTE]
> Stable: the atomisation steps, the classes of interference and their fixes, and the quality checks (Harvey 10.4 and 10.7, checked 2026-10-17). Instrument details differ between makers: lamp currents, recommended slits, burner heads and gas settings are in your instrument's cookbook. Line wavelengths: NIST. Lab data are simulated.

### From solution to free atoms

A **nebuliser** sucks the solution up and sprays a fine mist into a chamber; only the smallest droplets (a few per cent) reach the **burner**. In the flame the droplets dry, the salt particles melt and vaporise, and the molecules dissociate into atoms. Only free ground-state atoms absorb. A **hollow-cathode lamp** made of the element itself emits that element's lines, so the absorption is measured at exactly the right wavelength (Ca 422.7 nm), with a line much narrower than any monochromator could select.

### The procedure, and why each step

1. **Lamp on, 10–15 min warm-up.** Lamp output drifts until it is warm; drift looks like a changing calibration.
2. **Wavelength and slit.** 422.7 nm, slit about 0.5 nm: wide enough for light, narrow enough to exclude neighbouring lamp lines.
3. **Flame.** Air–acetylene (about 2300 °C) for calcium. Nitrous oxide–acetylene (about 2700 °C) for elements that form refractory oxides, such as aluminium.
4. **Burner height and fuel ratio.** Aspirate a mid-range standard and adjust for the highest stable absorbance. Atoms of each element are concentrated in a different part of the flame.
5. **Blank to zero.** Aspirate the blank (same acid and lanthanum, no calcium) and set zero.
6. **Standards, low to high**, with a rinse between, then samples. All in the same matrix.
7. **Quality checks.** A check standard every ten samples and at the end; a blank; a spiked sample; a duplicate.

### Interferences and their fixes

| Type | What happens | Fix |
|---|---|---|
| Chemical | phosphate, sulfate or aluminium hold Ca in a compound that does not atomise | releasing agent (La or Sr in excess), or a hotter flame |
| Ionisation | in hot flames, easily ionised atoms (Na, K, Ca in N₂O–C₂H₂) lose an electron and stop absorbing | ionisation suppressor: excess K or Cs in every solution |
| Spectral / background | molecules and particles absorb or scatter broadly | background correction (deuterium lamp or Zeeman) |
| Physical | viscosity or salt content changes how much sample reaches the flame | matrix-matched standards or standard addition |

Lanthanum binds phosphate more strongly than calcium does, so the calcium is "released". It must be in large excess, typically 0.1–1 % La in every solution, standards included.

### Line spectra, bands and continua

Free atoms have only a few sharp energy levels, so they absorb and emit **lines** a few picometres wide: sodium's yellow D lines at 589.0 and 589.6 nm (NIST), mercury's lines in a fluorescent lamp. Molecules have vibrational and rotational levels on top, so they give **bands**; the blue of a gas flame is band emission from CH and C₂ radicals. Hot solids glow with a **continuum**. Sharp lines are why atomic methods are so selective: a lamp line of one element almost never overlaps the line of another.

### Safety reasoning in the real lab

Acetylene is a flammable gas that can decompose explosively above about 1 bar gauge, so the regulator outlet is kept low and the cylinder upright and chained. The burner sits under an extraction hood: the flame emits UV and the exhaust carries metal vapours. The drain trap must be full, because its liquid seal stops a flashback into the spray chamber. Never leave a flame unattended. Nitrous oxide flames are lit and extinguished through air–acetylene, never directly.

## Worked example

### 1. Calcium in mineral water

Standards 0–6 mg/L Ca, all in 0.1 % La, give $A = -0.0009 + 0.03992\,c$ with $s_r$ = 0.0020. The water, diluted 1 + 9 and with La added, reads $A$ = 0.1907 (mean of 3):

$$c = \frac{0.1907 + 0.0009}{0.03992} = 4.80 \text{ mg/L} \quad\Rightarrow\quad 48.0 \text{ mg/L in the water}$$

With Lesson 09.4's formula, $s_c$ = 0.043 mg/L, so the water contains 48.0 ± 0.9 mg/L (about 95 %). Without La the same dilution reads 0.1582, giving 3.98 mg/L, 17 % low: the chemical interference.

### 2. A spike that fails

Add 2.0 mg/L Ca to the diluted water. The spiked solution reads 6.60 mg/L on the line. Recovery $= (6.60 - 4.80)/2.0 = 90$ %. A typical acceptance window is 90–110 %, so this is borderline. The cause is not the matrix: 6.6 mg/L lies above the 0–6 mg/L linear range, where the calibration bends. With a quadratic calibration the recovery is 97 %. The lesson: keep spikes inside the calibrated range, roughly doubling the analyte, not more.

## Hands-on

> [!WARNING]
> The flame part uses a kitchen gas hob only, with an adult present. Never use methanol, spirit burners or alcohol-soaked cotton for flame colours: such demonstrations have badly burned children and adults (US Chemical Safety Board). Tie back hair, no loose sleeves, nothing flammable near the hob, safety glasses on (damp salt can crackle and spit). Drop a small pinch of salt from a teaspoon held at arm's length; never lean over the flame. Keep the cardboard spectrometer at least 50 cm from the flame. Turn the gas off when you finish.

What you need: your phone spectrometer and calibration from Lesson 25.1, a fluorescent lamp and a white LED, a gas hob, table salt, low-sodium "light" salt (potassium chloride) if you have it, a teaspoon, the [Module 25 lab folder](../../labs/module-25/) and the [error analysis template](../../templates/error-analysis.md). Time: about 90 minutes. Nothing here trains you to light or tune a real AAS burner; the simulation covers the procedure.

### Part A — simulation: a flame AAS run (30 min)

[Simulation: Spectrometer — flame atomic absorption](../../simulations/spectrometer/index.html?preset=aas)

1. Warm the Ca lamp; record the reading every minute and see why you wait.
2. Optimise burner height with a 4 mg/L standard; note the best height and how sharply the signal falls either side.
3. Calibrate 0–10 mg/L. Find the linear range from the residuals.
4. Measure the mineral water diluted 1 + 9 without lanthanum, then with. Then add phosphate to a standard and repeat.
5. Switch to a nitrous oxide flame and measure sodium with and without 2000 mg/L potassium.
6. Turn background correction off and measure a sample with high salt content.

How you know it worked: the La result is about 20 % higher than the no-La result for the water; K raises the Na signal in the hot flame; without background correction the salty sample reads high.

### Part B — home: lines, bands and a continuum (30 min)

1. Photograph the fluorescent lamp through your spectrometer: sharp lines (atoms of mercury). Then the white LED: a smooth continuum with a blue peak.
2. Point the slit at the blue cone of a gas-hob flame from 50 cm in a dim kitchen: faint bands, not lines.
3. Drop a small pinch of table salt into the flame. The flame flares yellow; photograph it. Locate the line with your 25.1 calibration; it should sit at 589 ± 2 nm (the two D lines are too close for your spectrometer to separate).
4. Repeat with light salt (KCl). Potassium's strongest lines are at 766 and 770 nm (NIST). Do you see them?

How you know it worked: your sodium line falls within 2–3 nm of 589 nm; potassium's red lines do not appear, and the light-salt flame still looks yellow.

<details><summary>Why the potassium lines are missing</summary>

Phone cameras have an infrared-blocking filter that cuts off from about 650–700 nm, so 766 nm never reaches the sensor. And the yellow comes from sodium traces in the light salt and on the hob: sodium emits so strongly that a trace hides other elements. That is a spectral interference you can see. Laboratory flame photometers measure K at 766.5 nm with a red-sensitive detector and a filter that rejects the sodium line.

</details>

### Part C — Python: the full calcium result (30 min)

Open `lesson03_aas.py`. Complete `recovery()` (TODO 1) and `suppression()` (TODO 2), then run:

```bash
py lesson03_aas.py
```

How you know it worked: the straight line over all standards leaves curved residuals; the 0–6 mg/L line has $s_r$ = 0.0020 and LOD 0.16 mg/L; the water is 48.0 ± 0.4 mg/L (s); without La it reads 17 % low; the spike recovery is 90 %, and 97 % with the quadratic calibration; the check standard drifts −0.9 %, inside a ± 5 % limit, so the run is valid.

## Common mistakes

- **Adding the releasing agent to the samples only.** Standards and samples must contain the same La, or the calibration slope no longer matches.
- **Spiking out of the linear range.** A spike that takes the solution past the top standard gives a low recovery that has nothing to do with the matrix.
- **Skipping the warm-up.** A drifting lamp looks like a drifting calibration; the end check standard then fails.
- **Treating every low result as a chemical interference.** Check the physical matrix too: a salty or viscous sample nebulises less; standard addition tells the two apart.
- **Reading an emission line with the wrong detector.** If the detector cannot see the wavelength (the phone and potassium), the absence of a line proves nothing.

## Key takeaways

- Flame AAS works on free ground-state atoms; every step of the procedure protects the number of atoms reaching the light path or the stability of the lamp.
- Each interference has a matching fix: releasing agent, ionisation suppressor, background correction, matrix matching or standard addition.
- A result needs evidence: linear range from residuals, check standards for drift, a spike recovery inside the range, and an uncertainty.
- Atoms give sharp lines, molecules give bands, hot solids give continua; sharp lines are why atomic methods are selective.

## Sources

- [Harvey, Analytical Chemistry 2.1, 10.4](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.04%3A_Atomic_Absorption_Spectroscopy) — atomisation, hollow-cathode lamps, interferences and their fixes.
- [Harvey, Analytical Chemistry 2.1, 10.7](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.07%3A_Atomic_Emission_Spectroscopy) — flame and plasma emission.
- [NIST, strong lines of sodium](https://physics.nist.gov/PhysRefData/Handbook/Tables/sodiumtable2.htm) — D lines at 588.995 and 589.592 nm.
- [Analytical Communications 1999, phosphate and lanthanum](https://pubs.rsc.org/en/content/articlelanding/1999/ac/a900331b) — phosphate suppresses the calcium signal; lanthanum restores it.
- [US Chemical Safety Board, methanol demonstration fires](https://www.csb.gov/csb-releases-key-lessons-for-preventing-incidents-from-flammable-chemicals-in-educational-demonstrations-in-wake-of-several-serious-methanol-accidents-that-injured-children-and-adults/) — why flame-colour tests with methanol are not done.
