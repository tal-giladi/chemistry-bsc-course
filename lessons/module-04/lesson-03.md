---
id: "04.3"
module: 4
minutes: 20
practice_minutes: 50
prerequisites: ["04.1"]
objectives:
  - Calculate the Coulomb force and potential energy between two ions, in vacuum and in water, in N, J, eV and kJ/mol.
  - Relate field, potential and voltage, and convert a potential difference into an energy per electron and per mole.
  - Estimate the partial charges in a polar molecule from its dipole moment and bond length.
  - Compute a Madelung constant by summing Coulomb terms and explain why the sum must be arranged carefully.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 2, 5.3 Coulomb's Law"
    url: https://openstax.org/books/university-physics-volume-2/pages/5-3-coulombs-law
  - title: "OpenStax University Physics Volume 2, 5.4 Electric Field"
    url: https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field
  - title: "OpenStax University Physics Volume 2, 7.2 Electric Potential and Potential Difference"
    url: https://openstax.org/books/university-physics-volume-2/pages/7-2-electric-potential-and-potential-difference
  - title: "OpenStax University Physics Volume 2, 8.5 Molecular Model of a Dielectric"
    url: https://openstax.org/books/university-physics-volume-2/pages/8-5-molecular-model-of-a-dielectric
  - title: "NIST CODATA 2022: vacuum electric permittivity"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?ep0
  - title: "NIST CODATA 2022: elementary charge"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?e
  - title: "NIST Chemistry WebBook: Sodium chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647145&Mask=1000
  - title: "NIST CCCBDB: experimental data for HCl (dipole moment)"
    url: https://cccbdb.nist.gov/exp2x.asp?casno=7647010
  - title: "Malmberg and Maryott (1956), Dielectric constant of water from 0 to 100 C, J. Res. NBS 56, 1"
    url: https://nvlpubs.nist.gov/nistpubs/jres/56/jresv56n1p1_a1b.pdf
last_verified: "2026-10-16"
---

# 04.3 · Electrostatics: charge, field and potential

Almost all of chemistry is electrostatics: electrons attracted to nuclei, ions to counter-ions, the positive end of one water molecule to the negative end of another. One law, Coulomb's law, sets the size of all these attractions, and one material property, the permittivity of the solvent, decides how much of that attraction survives in solution. This lesson builds charge, field, potential and the electronvolt, then you compute ion-pair energies and a crystal's Madelung constant in Python.

## Why it matters

Table salt does not melt until 801 °C, yet a spoonful dissolves in a glass of cold water within a minute. The same Na⁺ and Cl⁻ ions are involved; what changes is the medium between them. In vacuum a Na⁺Cl⁻ pair at contact is held by about 590 kJ/mol. In water the same pair is held by under 8 kJ/mol, about three times the thermal energy, so the ions drift apart. You will use this comparison whenever you choose a solvent, explain why ionic reactions need polar solvents (Module 15), or read a voltage from an electrochemical cell as an energy (Module 8).

## Core ideas

> [!NOTE]
> Coulomb's law is stable. Constants are CODATA 2022 values from NIST ($e$ exact, $\varepsilon_0$ measured); the NaCl bond length and HCl dipole moment are from NIST databases; the relative permittivity of water (78.4 at 25 °C, measured 78.3 by Malmberg and Maryott) is a long-established value. Checked 2026-10-16.

### Charge

Electric charge comes in whole multiples of the elementary charge $e = 1.602\,176\,634\times10^{-19}$ C (coulomb), exact by definition. A proton carries $+e$, an electron $-e$, a Cl⁻ ion $-e$, a Ca²⁺ ion $+2e$. Charge is conserved: a balanced redox equation balances charge as well as atoms.

### Coulomb's law

Two point charges $q_1$ and $q_2$ a distance $r$ apart push or pull each other with a force

$$F = \frac{q_1 q_2}{4\pi\varepsilon_0 r^2}$$

where $\varepsilon_0 = 8.854\times10^{-12}\ \mathrm{F\,m^{-1}}$ is the vacuum permittivity, and $1/4\pi\varepsilon_0 = 8.988\times10^{9}\ \mathrm{N\,m^2\,C^{-2}}$. Like charges (same sign) repel, giving positive $F$; unlike charges attract. Doubling the distance quarters the force.

Tiny example: Na⁺ and Cl⁻ at 0.236 nm attract with $F = 8.988\times10^{9} \times (1.602\times10^{-19})^2 / (0.236\times10^{-9})^2 = 4.1\times10^{-9}$ N. Compare the largest force an HCl bond can exert, 6.9 nN (lesson [04.1](lesson-01.md)): the same order of magnitude, because bonds are electrical.

### Electric field

The field $\mathbf{E}$ at a point is the force a small positive test charge would feel there, divided by its charge: $E = F/q$, in N/C or equivalently V/m. Around a single charge $Q$, $E = Q/(4\pi\varepsilon_0 r^2)$. At 0.3 nm from a proton the field is $1.6\times10^{10}$ V/m. A thundercloud manages about $10^6$ V/m. Molecular fields are enormous, which is why they can pull electrons around and distort neighbouring molecules.

### Potential, voltage and potential energy

The potential energy of two charges is the work needed to bring them together from far apart (the integral of the force, lesson 04.1):

$$U = \frac{q_1 q_2}{4\pi\varepsilon_0 r}$$

It falls off as $1/r$, more slowly than the force. Negative $U$ means the pair is bound. The electric potential $V$ is potential energy per unit charge, in volts ($1\ \mathrm{V} = 1\ \mathrm{J/C}$). A voltage is a potential difference $\Delta V$. Moving a charge $q$ through it costs or releases

$$W = q\,\Delta V$$

One electron moved through one volt gains $1.602\times10^{-19}$ J. That amount is the electronvolt, eV. Per mole of electrons it is $96.485$ kJ/mol, which is the Faraday constant times one volt. So a 1.10 V Daniell cell delivers $1.10 \times 96.485 \times 2 = 212$ kJ per mole of zinc (2 electrons per Zn), the basis of $\Delta G = -nFE$ in Module 8.

### The solvent: relative permittivity

Inside a material the molecules polarise. Polar molecules turn their opposite ends towards each charge and partly cancel its field. The force and energy between ions drop by the relative permittivity $\varepsilon_r$ (also called the dielectric constant):

$$U = \frac{q_1 q_2}{4\pi\varepsilon_0\varepsilon_r r}$$

Vacuum has $\varepsilon_r = 1$, hydrocarbon solvents about 2, water about 78 at 25 °C. Water weakens ionic attraction almost eighty-fold. This is the single largest reason it dissolves salts.

### Dipoles

Many neutral molecules have their charge unevenly spread. Two charges $+q$ and $-q$ a distance $d$ apart form a dipole with dipole moment $\mu = qd$. Chemists quote $\mu$ in debye: $1\ \mathrm{D} = 3.336\times10^{-30}$ C m. Dipoles attract each other and ions, more weakly and at shorter range than ions attract ions. Hydrogen bonds and the solubility rule "like dissolves like" come from here (Module 7).

### Many charges: add them up

Coulomb forces and energies obey superposition: the total is the sum of all the pair terms. In a crystal every ion interacts with every other. The sum of attractions and repulsions, in units of the nearest-neighbour pair, is the Madelung constant $M$. For rock salt (NaCl structure) $M = 1.7476$. The sum converges only if you add the terms in neutral groups; adding ions shell by shell gives a series that jumps around wildly. The lab shows both behaviours.

## Worked example

### 1. An ion pair in vacuum and in water

NIST gives the gas-phase NaCl bond length $r = 0.2361$ nm. Treat Na⁺ and Cl⁻ as point charges.

- Vacuum: $U = -\dfrac{(1.602\times10^{-19})^2}{4\pi \times 8.854\times10^{-12} \times 0.2361\times10^{-9}} = -9.77\times10^{-19}$ J.
- In eV: $-9.77\times10^{-19} / 1.602\times10^{-19} = -6.10$ eV.
- Per mole: $\times N_A = -589$ kJ/mol.
- In water, divide by $\varepsilon_r = 78.4$: $-7.5$ kJ/mol. With $RT = 2.48$ kJ/mol at 298 K, that is $-3.0\,RT$.

Interpretation: in water, thermal jostling competes with the attraction on equal terms, and the pair spends most of its time apart. This crude model ignores the water molecules bound to each ion, but it gets the ratio right.

### 2. How ionic is HCl?

The measured dipole moment of HCl is 1.093 D and the bond length 0.12746 nm. If the bond were fully ionic ($\mathrm{H^+Cl^-}$), $\mu$ would be $e r = 1.602\times10^{-19} \times 1.2746\times10^{-10} = 2.04\times10^{-29}$ C m $= 6.12$ D.

Partial charge $\delta = \mu/(e r) = 1.093 / 6.12 = 0.18$. HCl behaves as if H carries $+0.18e$ and Cl $-0.18e$: a polar covalent bond, about 18 % ionic in this simple picture.

## Hands-on

### Part A — pencil (15 min)

1. An electron moves through a potential difference of 1.50 V (one AA cell). How much energy does it gain, in J and eV? How much per mole of electrons?
2. Find the force between Na⁺ and Cl⁻ 0.50 nm apart in water.
3. A molecule has $+0.40e$ and $-0.40e$ on atoms 0.100 nm apart. What is its dipole moment in debye?

<details><summary>Answers to Part A</summary>

1. $1.50 \times 1.602\times10^{-19} = 2.40\times10^{-19}$ J = 1.50 eV. Per mole: $1.50 \times 96.485 = 145$ kJ/mol, comparable to a weak chemical bond.
2. $F = 8.988\times10^{9} \times (1.602\times10^{-19})^2 / (78.4 \times (0.50\times10^{-9})^2) = 1.2\times10^{-11}$ N, about 350 times weaker than the contact pair in vacuum (factor 78 from water, 4.5 from distance squared).
3. $\mu = 0.40 \times 1.602\times10^{-19} \times 1.00\times10^{-10} = 6.41\times10^{-30}$ C m = 1.92 D, close to the dipole moment of water.

</details>

### Part B — Python: ions and crystals (35 min)

What you need: Python with the course packages and the [Module 4 lab folder](../../labs/module-04/).

1. Open `lesson03_coulomb.py`. Fill in `coulomb_energy(q1, q2, r, eps_r)`.
2. Fill in `madelung_chain(n)`: a line of alternating ions $+ - + - \dots$. The central ion has two neighbours at distance 1 (opposite charge), two at distance 2 (same charge), and so on, so $M = 2(1 - \tfrac12 + \tfrac13 - \dots)$.
3. Fill in `madelung_rocksalt(n)`. Sum over a cube of ions with Evjen's weights (half for ions on a face, a quarter on an edge, an eighth on a corner), which keeps every cube neutral.
4. Run it:

```bash
py lesson03_coulomb.py
```

How you know it worked: the vacuum pair energy is −6.10 eV (−589 kJ/mol) and the water value −7.5 kJ/mol (−3.0 kT). The chain sum creeps towards $2\ln2 = 1.38629$, still visibly short at $n = 100$. The rock-salt sum reaches 1.7476 by $n = 8$. The crystal's Coulomb energy per ion pair comes out at about −861 kJ/mol.

<details><summary>Reference solution and discussion</summary>

`coulomb_energy`: `q1*q2*E**2/(4*np.pi*EPS0*eps_r*r)`. `madelung_chain`: `j = np.arange(1, n+1)`, return `2*np.sum((-1.0)**(j+1)/j)`. `madelung_rocksalt`: multiply the weights by 0.5 for each coordinate that sits on the cube surface, then sum `sign*w/d` where `d > 0`. Full code: `lesson03_coulomb_solution.py`.

Why the weights? Without them each cube you add carries a net charge, and the sum swings back and forth as $n$ grows. With them every cube is neutral and the far-away contributions cancel. The measured lattice energy of NaCl is about 787 kJ/mol, smaller than the 861 kJ/mol from attraction alone, because the ions also repel when their electron clouds overlap. Module 18 adds that repulsion and checks it with a Born–Haber cycle.

Write the three key numbers and the convergence table on a [notebook page](../../templates/notebook-page.md).

</details>

## Common mistakes

- Confusing force and energy. The force falls as $1/r^2$, the energy as $1/r$. Doubling the distance halves the energy but quarters the force.
- Forgetting $\varepsilon_r$ in solution. Vacuum formulas overestimate ionic attraction in water by a factor of about 80.
- Writing charges as 1 and −1 without the factor $e$. In SI units the charges must be in coulombs: $q = ze$.
- Mixing volts and electronvolts. A volt is energy per charge (J/C); an electronvolt is an energy (J). One electron through $\Delta V$ volts gains $\Delta V$ eV.
- Losing the sign. Negative $U$ means attraction and a bound pair. Keep the signs of the charges in the formula and the sign of the answer follows.
- Summing a Madelung series shell by shell. Use neutral groups, or the sum will not settle.

## Key takeaways

- Coulomb's law: $F = q_1q_2/4\pi\varepsilon_0 r^2$, $U = q_1q_2/4\pi\varepsilon_0 r$; both are reduced by $\varepsilon_r$ in a medium.
- A volt is a joule per coulomb; one electron through one volt gains 1 eV, and one mole of electrons gains 96.485 kJ.
- Water ($\varepsilon_r \approx 78$) cuts ionic attraction to a few $RT$, which is why it dissolves salts.
- A dipole moment measures charge separation; HCl's 1.093 D means partial charges of about ±0.18e.
- Coulomb energies add pair by pair; a crystal's total is the Madelung constant times the nearest-pair energy.

## Sources

- [OpenStax University Physics Volume 2, 5.3 Coulomb's Law](https://openstax.org/books/university-physics-volume-2/pages/5-3-coulombs-law) — the force law and superposition.
- [OpenStax University Physics Volume 2, 5.4 Electric Field](https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field) — field of a point charge.
- [OpenStax University Physics Volume 2, 7.2 Electric Potential and Potential Difference](https://openstax.org/books/university-physics-volume-2/pages/7-2-electric-potential-and-potential-difference) — volts, potential energy and the electronvolt.
- [OpenStax University Physics Volume 2, 8.5 Molecular Model of a Dielectric](https://openstax.org/books/university-physics-volume-2/pages/8-5-molecular-model-of-a-dielectric) — how polar molecules screen a field.
- [NIST CODATA 2022: vacuum electric permittivity](https://physics.nist.gov/cgi-bin/cuu/Value?ep0) and [elementary charge](https://physics.nist.gov/cgi-bin/cuu/Value?e).
- [NIST Chemistry WebBook: NaCl diatomic constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647145&Mask=1000) — gas-phase bond length 0.2361 nm.
- [NIST CCCBDB: HCl experimental data](https://cccbdb.nist.gov/exp2x.asp?casno=7647010) — dipole moment 1.093 D.
- [Malmberg and Maryott (1956), J. Res. NBS 56, 1](https://nvlpubs.nist.gov/nistpubs/jres/56/jresv56n1p1_a1b.pdf) — measured relative permittivity of water, 78.3 at 25 °C.
