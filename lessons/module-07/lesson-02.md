---
id: "07.2"
module: 7
minutes: 25
practice_minutes: 50
prerequisites: ["07.1", "04.3", "04.5"]
objectives:
  - Write the ground-state electron configuration of any element up to krypton and of its common ions, including the chromium and copper exceptions.
  - Explain the trends in atomic radius and first ionisation energy across a period and down a group using shielding and effective nuclear charge.
  - Explain the two dips in first ionisation energy across a period (group 2 to 13 and group 15 to 16).
  - Find how many valence electrons an atom has from the jump in its successive ionisation energies.
volatility: concept
sources:
  - title: "NIST Atomic Spectra Database — Ionization Energies form"
    url: https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html
  - title: "OpenStax Chemistry 2e, 6.4 Electronic Structure of Atoms (Electron Configurations)"
    url: https://openstax.org/books/chemistry-2e/pages/6-4-electronic-structure-of-atoms-electron-configurations
  - title: "OpenStax Chemistry 2e, 6.5 Periodic Variations in Element Properties"
    url: https://openstax.org/books/chemistry-2e/pages/6-5-periodic-variations-in-element-properties
  - title: "MIT OpenCourseWare 5.111SC Principles of Chemical Science (Fall 2014)"
    url: https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/
last_verified: "2026-10-16"
---

# 07.2 · Electron configuration and periodic trends

The periodic table is not a list to memorise. It is a map of how electrons fill the space around a nucleus. This lesson shows how electrons are arranged in shells and orbitals, how to write that arrangement down, and how it explains why atoms get bigger or smaller, and why some give up an electron easily while others hold on hard. You then test the explanation on real ionisation energies from NIST.

## Why it matters

Sodium reacts violently with water; neon does nothing at all. Iron forms Fe²⁺ and Fe³⁺, never Fe⁸⁺. Lithium is the metal in phone batteries partly because it gives up one electron so easily and is so light. Every one of these facts follows from the electron configuration. When you meet a new element or ion later in the course, in a crystal (Module 18), a metalloenzyme (Module 26) or an electrode (Module 32), the first thing a chemist writes down is its configuration. From that one line you can predict its charge, its size and, roughly, how it will react.

## Core ideas

> [!NOTE]
> The shell model, the filling rules and the periodic trends are stable. The ionisation energies in the lab come from the NIST Atomic Spectra Database, retrieved on 2026-10-16. Module 12 derives orbitals properly from the Schrödinger equation; here we use the results.

### Shells, subshells and orbitals

An **orbital** is a region where an electron is likely to be found, with a definite energy. Orbitals are labelled by quantum numbers (whole numbers that come out of quantum mechanics):

- $n = 1, 2, 3, \dots$, the **shell**. Larger $n$ means farther from the nucleus and higher in energy.
- $\ell = 0, 1, 2, 3$ for $s, p, d, f$, the **subshell** (its shape). In shell $n$, $\ell$ goes from 0 to $n - 1$.
- An $s$ subshell has 1 orbital, $p$ has 3, $d$ has 5, $f$ has 7.
- Each orbital holds at most two electrons, with opposite **spin** (the **Pauli exclusion principle**).

So an $s$ subshell holds 2 electrons, $p$ holds 6, $d$ holds 10.

### Filling order: the aufbau rule

In the ground state (the lowest-energy state) electrons fill the lowest-energy subshells first. This is the **aufbau** ("building up") rule. In many-electron atoms the order is

$$1s,\ 2s,\ 2p,\ 3s,\ 3p,\ 4s,\ 3d,\ 4p,\ 5s,\ 4d,\ 5p,\ \dots$$

The 4s fills before 3d because a 4s electron spends some time very close to the nucleus, which lowers its energy. The periodic table is laid out in exactly these blocks: the s-block is groups 1–2, the p-block groups 13–18, and the d-block the ten transition-metal columns.

Within a subshell, electrons go into separate orbitals with parallel spins before they pair up. This is **Hund's rule**. Nitrogen, $1s^2 2s^2 2p^3$, has three unpaired 2p electrons, one in each p orbital.

You can shorten a configuration with the previous noble gas as a **core**: sodium is $1s^2 2s^2 2p^6 3s^1 = [\text{Ne}]\,3s^1$. The electrons outside the core are the **valence electrons**, the ones that take part in bonding.

### Two exceptions and the ion rule

Two elements up to krypton break the simple order:

- chromium: $[\text{Ar}]\,3d^5 4s^1$, not $3d^4 4s^2$;
- copper: $[\text{Ar}]\,3d^{10} 4s^1$, not $3d^9 4s^2$.

Half-filled and filled d subshells are especially stable, and 3d and 4s are very close in energy, so one electron moves across.

When a transition metal forms a positive ion, it loses its **4s electrons first**, even though 4s filled first. Iron is $[\text{Ar}]\,3d^6 4s^2$; Fe²⁺ is $[\text{Ar}]\,3d^6$ and Fe³⁺ is $[\text{Ar}]\,3d^5$. Once the atom is charged, 3d drops below 4s in energy.

### Effective nuclear charge

An outer electron does not feel the full charge $+Ze$ of the nucleus. The inner electrons sit between it and the nucleus and partly cancel the pull. This is **shielding**. What is left is the **effective nuclear charge**:

$$Z_\text{eff} = Z - S$$

where $S$ is the shielding by the other electrons. Core electrons shield well; electrons in the same shell shield poorly. You can estimate $Z_\text{eff}$ from an ionisation energy with the hydrogen-like formula $IE \approx 13.6 \text{ eV} \times Z_\text{eff}^2 / n^2$. For sodium, $IE_1 = 5.139$ eV and $n = 3$:

$$Z_\text{eff} \approx 3 \sqrt{5.139 / 13.6} = 1.84$$

Sodium has 11 protons, but its 3s electron feels less than 2 of them. This is the Coulomb attraction of [Lesson 04.3](../module-04/lesson-03.md), with a reduced charge.

### Periodic trends

The **ionisation energy** (IE) is the energy needed to remove one electron from a gas-phase atom: $\text{X}(g) \to \text{X}^+(g) + e^-$. The first, $IE_1$, removes the outermost electron. The second, $IE_2$, removes the next one from the ion, and so on. A few eV per atom is the energy of an ultraviolet photon ([Lesson 04.5](../module-04/lesson-05.md)); 1 eV per atom is 96.49 kJ/mol.

- **Across a period** (left to right), $Z$ rises by one each step but the new electron goes into the same shell, which shields poorly. $Z_\text{eff}$ grows, so the atom shrinks and $IE_1$ rises.
- **Down a group**, each new shell is farther out and well shielded by the core. The atom grows and $IE_1$ falls.

There are two small dips across each period:

- **Group 2 → 13** (Be 9.32 eV → B 8.30 eV): boron's outer electron is in 2p, which is higher in energy and better shielded than 2s.
- **Group 15 → 16** (N 14.53 eV → O 13.62 eV): oxygen's fourth 2p electron has to pair up in an orbital that already holds one electron. The two repel each other, so this electron is easier to remove.

**Electronegativity** is how strongly an atom in a molecule pulls shared electrons toward itself. It follows the same trend as $IE_1$: highest at the top right (F = 3.98 on the Pauling scale), lowest at the bottom left. You use it in the next lesson.

### Successive ionisation energies reveal the core

Once all valence electrons are gone, the next electron must come from the noble-gas core. It is much closer to the nucleus and far less shielded. The ionisation energy jumps by a large factor. Magnesium: $IE_1 = 7.65$, $IE_2 = 15.04$, $IE_3 = 80.14$ eV. The big jump comes after the second electron, so magnesium has 2 valence electrons and forms Mg²⁺.

## Worked example

### 1. Configurations of selenium and Fe³⁺

Selenium, $Z = 34$: fill in order, $1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^{10} 4p^4$, which is $[\text{Ar}]\,3d^{10} 4s^2 4p^4$. Count: $18 + 10 + 2 + 4 = 34$. It has 6 valence electrons ($4s^2 4p^4$), which puts it in group 16, under oxygen and sulfur. Like oxygen, it tends to gain two electrons: Se²⁻.

Fe³⁺: iron is $[\text{Ar}]\,3d^6 4s^2$ (26 electrons). Remove the two 4s electrons, then one 3d: $[\text{Ar}]\,3d^5$, 23 electrons. Five d electrons, one in each orbital by Hund's rule, means five unpaired electrons. That is why Fe³⁺ salts are strongly attracted to a magnet.

### 2. Which group is element X?

An element in period 3 has $IE_1 = 5.99$, $IE_2 = 18.83$, $IE_3 = 28.45$, $IE_4 = 119.99$ eV. The ratios are 3.1, 1.5 and 4.2. The biggest jump is after the third electron, so X has 3 valence electrons: group 13, aluminium. Note the trap: the first ratio, 3.1, is also large. It comes from the step from a 3p electron to the lower-energy 3s pair, not from reaching the core. Always look at all the ratios.

## Hands-on

**What you need:** Python with the course packages and the [Module 7 lab folder](../../labs/module-07/). **Time:** about 50 minutes.

### Part A — pencil (15 min)

1. Write the full and the core-notation configuration of sulfur, potassium and copper.
2. Give the configuration of Cu⁺ and Zn²⁺. How many unpaired electrons does each have?
3. Arrange Na, Mg, K and Cl in order of increasing atomic radius.

<details><summary>Answers to Part A</summary>

1. S: $1s^2 2s^2 2p^6 3s^2 3p^4 = [\text{Ne}]\,3s^2 3p^4$. K: $1s^2 2s^2 2p^6 3s^2 3p^6 4s^1 = [\text{Ar}]\,4s^1$. Cu: $1s^2 2s^2 2p^6 3s^2 3p^6 3d^{10} 4s^1 = [\text{Ar}]\,3d^{10} 4s^1$ (the exception).
2. Cu⁺: $[\text{Ar}]\,3d^{10}$, 0 unpaired. Zn²⁺: $[\text{Ar}]\,3d^{10}$, 0 unpaired. Both are colourless in solution for this reason (Module 18).
3. Cl < Mg < Na < K. Across period 3 the radius shrinks (Cl smallest); K has a fourth shell, so it is the largest.

</details>

### Part B — Python with real NIST data (35 min)

The file `ionization_energies.csv` holds $IE_1$, $IE_2$ and $IE_3$ for hydrogen to krypton from the NIST Atomic Spectra Database.

1. Open `lesson02_ionisation.py`. Fill in `dips()`: return every atomic number whose $IE_1$ is lower than that of the element before it.
2. Fill in `valence_from_jumps()`: the number of electrons removed before the largest ratio $IE_{k+1}/IE_k$.
3. Run it and open the plot `runs/ie1.png`:

```bash
py lesson02_ionisation.py
```

4. Sort the dips into four kinds: start of a new period (after a noble gas), group 2 → 13, group 15 → 16, and inside the d-block.

**How you know it worked:** the noble gases are the peaks (He 24.59, Ne 21.57, Ar 15.76, Kr 14.00 eV, falling down the group). The dips list is Li, B, O, Na, Al, S, K, V, Co, Ni, Ga, Se. Na and K come out with 1 valence electron, Mg and Ca with 2.

<details><summary>Reference sorting of the dips</summary>

- New period: Li, Na, K (one electron in a new shell, far out and well shielded).
- Group 2 → 13: B, Al, Ga (first p electron).
- Group 15 → 16: O, S, Se (first paired p electron).
- d-block: V, Co, Ni. These are small (under 0.25 eV) and come from the close 3d and 4s energies; do not over-read them.

The full solution is `lesson02_ionisation_solution.py`.

</details>

## Common mistakes

- **Removing 3d electrons before 4s in transition-metal ions.** Fe²⁺ is $[\text{Ar}]\,3d^6$, not $[\text{Ar}]\,3d^4 4s^2$. Ions lose 4s first.
- **Forgetting Cr and Cu.** Write $3d^5 4s^1$ and $3d^{10} 4s^1$.
- **Saying "more protons always means a smaller atom".** Only across a period. Down a group the new shell wins, and atoms grow.
- **Taking the first big ratio of successive IEs as the core.** Check every ratio; the core jump is the largest, by far.
- **Mixing eV per atom and kJ per mole.** Multiply eV by 96.49 to get kJ/mol. Sodium's 5.14 eV is 496 kJ/mol.

## Key takeaways

- Orbitals hold two electrons each; subshells s, p, d hold 2, 6, 10. Fill by aufbau, then Hund, obeying Pauli.
- Use noble-gas cores; valence electrons are the ones outside the core. Cr and Cu are the exceptions up to Kr.
- Transition-metal ions lose their 4s electrons first.
- $Z_\text{eff}$ rises across a period and atoms shrink; down a group, new shells make atoms larger and IEs smaller.
- The large jump in successive ionisation energies marks the core and counts the valence electrons.

## Sources

- [NIST Atomic Spectra Database — Ionization Energies form](https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html) (Kramida, Ralchenko, Reader and NIST ASD Team; data in the lab retrieved 2026-10-16).
- [OpenStax Chemistry 2e, 6.4 Electronic Structure of Atoms (Electron Configurations)](https://openstax.org/books/chemistry-2e/pages/6-4-electronic-structure-of-atoms-electron-configurations).
- [OpenStax Chemistry 2e, 6.5 Periodic Variations in Element Properties](https://openstax.org/books/chemistry-2e/pages/6-5-periodic-variations-in-element-properties).
- [MIT OpenCourseWare 5.111SC Principles of Chemical Science (Fall 2014)](https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/) (lectures on many-electron atoms and periodic trends).
