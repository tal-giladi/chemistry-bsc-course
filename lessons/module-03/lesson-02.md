---
id: "03.2"
module: 3
minutes: 20
practice_minutes: 45
prerequisites: ["03.1", "02.4"]
objectives:
  - Find the eigenvalues and eigenvectors of a 2×2 matrix by hand from the characteristic equation.
  - Build the Hückel matrix of a conjugated chain or ring and compute its π energy levels and delocalization energy.
  - Compute the stretching normal-mode wavenumbers of linear CO2 from a force constant and compare them with measured values.
  - Interpret an eigenvector as the shape of a molecular orbital or of a vibration.
volatility: concept
sources:
  - title: "LibreTexts Physical Chemistry, 10.6 Butadiene is Stabilized by a Delocalization Energy"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/10%3A_Bonding_in_Polyatomic_Molecules/10.06%3A_Butadiene_is_Stabilized_by_a_Delocalization_Energy
  - title: "NIST CCCBDB: experimental vibrational frequencies of CO2"
    url: https://cccbdb.nist.gov/exp2x.asp?casno=124389&charge=0
  - title: "NumPy v2.5 manual, numpy.linalg.eigh"
    url: https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html
  - title: "NIST CODATA 2022: atomic mass constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?u
  - title: "MIT OpenCourseWare 18.06 Linear Algebra (Strang, Spring 2010)"
    url: https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/
last_verified: "2026-10-16"
---

# 03.2 · Eigenvalues and eigenvectors

Some matrices have special directions: multiply a vector pointing that way by the matrix and you get the same vector back, only stretched. Those directions are eigenvectors and the stretch factors are eigenvalues. In chemistry they are not abstract. The eigenvalues of a Hückel matrix are the energies of a molecule's π orbitals, and the eigenvalues of a mass-weighted force-constant matrix are its vibrational frequencies. This lesson teaches the hand method for 2×2 matrices and the numpy method for everything larger, using butadiene, benzene and carbon dioxide.

## Why it matters

Why is benzene so much less reactive than three separate double bonds? Why does carbon dioxide absorb infrared light at 2349 cm⁻¹ and 667 cm⁻¹ but show nothing at 1333 cm⁻¹ in its IR spectrum? Both answers come from an eigenvalue problem. Quantum chemistry programs (Module 31) and spectrum assignments (Module 20) are, at their core, large matrices being diagonalised. If you can set up a small one yourself and read its eigenvectors, the output of those programs stops being a black box.

## Core ideas

> [!NOTE]
> The linear algebra and the Hückel model are stable. The CO2 wavenumbers are experimental values from the NIST CCCBDB and the atomic mass constant is CODATA 2022, both checked 2026-10-16. The lab uses `numpy.linalg.eigh` from numpy 2.5. The value β ≈ −75 kJ/mol is an empirical fit, not a constant of nature.

### The eigenvalue equation

For a square matrix $A$, a non-zero vector $\mathbf{v}$ is an eigenvector with eigenvalue $\lambda$ if

$$A\mathbf{v} = \lambda\mathbf{v}$$

Rewrite it as $(A - \lambda I)\mathbf{v} = \mathbf{0}$, where $I$ is the identity matrix (1 on the diagonal, 0 elsewhere). This is a null-space problem, exactly like balancing a reaction in [03.1](lesson-01.md): a non-zero solution exists only if the matrix $A - \lambda I$ is singular, that is

$$\det(A - \lambda I) = 0$$

This is the characteristic equation. For an $n \times n$ matrix it is a polynomial of degree $n$ in $\lambda$, so there are $n$ eigenvalues.

Tiny example: $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. $\det(A - \lambda I) = (2 - \lambda)^2 - 1 = 0$, so $\lambda = 3$ or $\lambda = 1$. For $\lambda = 3$: $-x + y = 0$, eigenvector $(1, 1)$. For $\lambda = 1$: $x + y = 0$, eigenvector $(1, -1)$. Check: $A(1,1) = (3,3) = 3(1,1)$.

### Symmetric matrices are the friendly case

Almost every matrix in physical chemistry is symmetric ($A_{ij} = A_{ji}$). For symmetric matrices the eigenvalues are always real and the eigenvectors are perpendicular to each other. Use `np.linalg.eigh` for them, not `np.linalg.eig`: it is faster, always returns real numbers, and sorts the eigenvalues in ascending order, with eigenvector `i` in column `i`.

### Hückel theory: orbitals as eigenvectors

Hückel theory is the simplest model of π electrons in conjugated molecules. Each carbon contributes one p orbital. Each π molecular orbital is a mix of these: $\psi = \sum_i c_i\,p_i$. The model has two parameters:

- $\alpha$, the energy of an electron in an isolated carbon p orbital (the Coulomb integral);
- $\beta$, the extra stabilisation between two bonded neighbours (the resonance integral). Both are negative; $\beta$ is about −75 kJ/mol from fits to experiment.

Non-neighbours interact with zero. The energies are the eigenvalues of the Hückel matrix, and the coefficients $c_i$ are its eigenvectors. Write $E = \alpha + x\beta$; then $x$ is an eigenvalue of a matrix with 0 on the diagonal and 1 between bonded atoms. For ethylene:

$$\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \Rightarrow x = \pm 1,\quad E = \alpha \pm \beta$$

Because $\beta < 0$, $x = +1$ is the lower, bonding orbital, with eigenvector $(1, 1)/\sqrt{2}$: both p orbitals in phase. $x = -1$ is the antibonding orbital $(1, -1)/\sqrt{2}$, with a node between the atoms. Electrons fill levels two at a time from the bottom. The delocalization energy is the π energy minus that of the same number of isolated ethylene double bonds (each worth $2\beta$).

### Normal modes: vibrations as eigenvectors

Atoms in a molecule sit at the bottom of a potential well. Near the bottom the potential is a parabola, the harmonic approximation of [02.4](../module-02/lesson-04.md), so each bond acts like a spring with force constant $k$ (N/m). For several atoms, Newton's law gives $m_i \ddot{x}_i = -\sum_j K_{ij} x_j$, where $K$ is the force-constant matrix. Divide each coordinate by $\sqrt{m_i}$ (mass-weighting) and the problem becomes an eigenvalue problem for the symmetric matrix

$$D_{ij} = \frac{K_{ij}}{\sqrt{m_i m_j}}$$

Each eigenvalue is $\omega^2$, the square of an angular frequency; each eigenvector is a normal mode, a pattern in which all atoms move at the same frequency. Spectroscopists quote wavenumbers $\tilde\nu = \omega/(2\pi c)$ in cm⁻¹, with $c$ in cm/s.

For linear O=C=O moving along its axis, with one force constant $k$ for each C=O bond:

$$K = k\begin{pmatrix} 1 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1 \end{pmatrix}$$

Its three eigenvectors are: all atoms moving together (translation, $\omega = 0$); the two O atoms moving out and in while C stays still (symmetric stretch, $\omega^2 = k/m_\mathrm{O}$); and the C moving against both O atoms (antisymmetric stretch, $\omega^2 = (k/m_\mathrm{O})(1 + 2m_\mathrm{O}/m_\mathrm{C})$). The symmetric stretch does not change the dipole moment, which is why it is invisible in the IR spectrum (it is seen in Raman, Module 20). The bend at 667 cm⁻¹ needs a second dimension, so this 1D model cannot produce it.

## Worked example

### 1. Butadiene by hand

Four carbons in a chain, bonds 1–2, 2–3, 3–4. The characteristic equation of the Hückel matrix is $\det(H - xI) = 0$ with

$$H = \begin{pmatrix} 0 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

Expanding the determinant gives $x^4 - 3x^2 + 1 = 0$. This is a quadratic in $x^2$: $x^2 = (3 \pm \sqrt{5})/2 = 2.618$ or $0.382$, so $x = \pm 1.618, \pm 0.618$.

Four π electrons fill the two lowest levels: $E_\pi = 2(\alpha + 1.618\beta) + 2(\alpha + 0.618\beta) = 4\alpha + 4.472\beta$. Two isolated double bonds would give $4\alpha + 4\beta$. Delocalization energy: $0.472\beta \approx 0.472 \times (-75) = -35$ kJ/mol. Butadiene is about 35 kJ/mol more stable than two separate double bonds, according to the model.

### 2. The force constant of the C=O bond in CO2

The symmetric stretch is at 1333 cm⁻¹ (NIST CCCBDB). In that mode only the O atoms move, so $\omega^2 = k/m_\mathrm{O}$.

1. $m_\mathrm{O} = 15.995\ \mathrm{u} \times 1.66054\times10^{-27}\ \mathrm{kg/u} = 2.6560\times10^{-26}$ kg.
2. $\omega = 2\pi c\tilde\nu = 2\pi \times 2.99792\times10^{10}\ \mathrm{cm/s} \times 1333\ \mathrm{cm^{-1}} = 2.511\times10^{14}\ \mathrm{s^{-1}}$.
3. $k = m_\mathrm{O}\omega^2 = 2.6560\times10^{-26} \times 6.305\times10^{28} = 1675$ N/m.

Now predict the antisymmetric stretch: $\tilde\nu_\text{anti} = 1333 \times \sqrt{1 + 2 \times 15.995/12.000} = 1333 \times 1.915 = 2552$ cm⁻¹. The measured value is 2349 cm⁻¹. The model is 9 % high, because real molecules also have a coupling term between the two bonds and are not perfectly harmonic. A one-parameter model getting within 10 % is still useful: it tells you which band is which.

## Hands-on

What you need: Python with the course packages, the [Module 3 lab folder](../../labs/module-03/), pencil and paper. Time: about 45 minutes.

### Part A — pencil (15 min)

1. Find the eigenvalues and eigenvectors of $\begin{pmatrix} 4 & 1 \\ 1 & 4 \end{pmatrix}$.
2. Set up the Hückel matrix of the allyl system (three carbons in a chain) and find its three $x$ values.
3. For the allyl cation (2 π electrons) and the allyl anion (4 π electrons), which orbital holds the last electrons, and at what energy?

<details><summary>Answers to Part A</summary>

1. $(4 - \lambda)^2 = 1$, so $\lambda = 5$ with $(1, 1)$ and $\lambda = 3$ with $(1, -1)$. Same eigenvectors as the tiny example: adding a multiple of $I$ shifts eigenvalues but keeps eigenvectors.
2. $H = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}$. $\det(H - xI) = -x^3 + 2x = 0$, so $x = \sqrt{2}, 0, -\sqrt{2}$.
3. Cation: both electrons in the bonding orbital at $\alpha + 1.414\beta$. Anion: the extra two go into the non-bonding orbital at $E = \alpha$ ($x = 0$), whose eigenvector $(1, 0, -1)/\sqrt{2}$ puts the charge on the two end carbons, not the middle one. This is the resonance picture of organic chemistry, from an eigenvector.

</details>

### Part B — Python (30 min)

1. Open `lesson02_eigen.py` and fill in `huckel_matrix`, `pi_energy` and `co2_wavenumbers`.
2. Run it from the lab folder:

```bash
py lesson02_eigen.py
```

3. Look at `runs/lesson02_eigen.png`, an energy-level diagram for four molecules.

How you know it worked: butadiene gives $x = \pm1.618, \pm0.618$ and delocalization $0.472\beta$; hexatriene $0.988\beta$; benzene $x = 2, 1, 1, -1, -1, -2$ and delocalization $2.000\beta$, about 150 kJ/mol. For CO2 you get $k \approx 1675$ N/m, eigen-wavenumbers 0, 1333 and about 2552 cm⁻¹, and the printed eigenvector shapes match the three motions described above.

<details><summary>Reference solution and what to notice</summary>

`huckel_matrix`: zeros, then 1 at `[i, i+1]` and `[i+1, i]`, plus the corners for a ring. `pi_energy`: sort `x` descending and add two electrons per level. `co2_wavenumbers`: `D = K / np.sqrt(np.outer(m, m))`, `np.linalg.eigh(D)`, then $\sqrt{\omega^2}/(2\pi c)$. Full code: `lesson02_eigen_solution.py`.

What to notice: benzene's ring closure turns hexatriene's $0.988\beta$ into $2\beta$, double the stabilisation for the same six electrons. That is the extra stability of an aromatic ring (Module 15). Benzene also has two pairs of equal eigenvalues (degenerate orbitals), which come from its six-fold symmetry (Module 20). In the CO2 output, the zero eigenvalue is the whole molecule sliding; every free molecule has such zero modes, and programs remove them before reporting frequencies.

</details>

## Common mistakes

- Filling Hückel levels from the smallest $x$. Since $\beta$ is negative, the largest $x$ is the lowest energy. `eigh` sorts ascending, so reverse the order before filling.
- Using `np.linalg.eig` on a symmetric matrix. It can return tiny imaginary parts and unsorted values. Use `eigh`.
- Reading eigenvectors from rows. numpy stores eigenvector `i` in column `i`: `vecs[:, i]`.
- Forgetting to mass-weight the force-constant matrix. The eigenvalues of $K$ alone have units of N/m, not s⁻²; the frequencies come out wrong.
- Mixing $\omega$, $\nu$ and $\tilde\nu$. $\omega$ is in rad/s, $\nu = \omega/2\pi$ in Hz, $\tilde\nu = \nu/c$ in cm⁻¹ only if $c$ is in cm/s.
- Expecting the sign of an eigenvector to mean something. $\mathbf{v}$ and $-\mathbf{v}$ are the same eigenvector; only relative signs between atoms matter.

## Key takeaways

- $A\mathbf{v} = \lambda\mathbf{v}$; eigenvalues are the roots of $\det(A - \lambda I) = 0$.
- Symmetric matrices have real eigenvalues and perpendicular eigenvectors; use `np.linalg.eigh`.
- Hückel: orbital energies are $E = \alpha + x\beta$ with $x$ the eigenvalues of the connection matrix; eigenvectors give the orbital coefficients.
- Normal modes: eigenvalues of the mass-weighted force-constant matrix are $\omega^2$; eigenvectors show how the atoms move.
- A simple model that is 10 % off can still assign every band correctly.

## Sources

- [LibreTexts Physical Chemistry, 10.6 Butadiene](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/10%3A_Bonding_in_Polyatomic_Molecules/10.06%3A_Butadiene_is_Stabilized_by_a_Delocalization_Energy) — Hückel energies $\alpha \pm 1.618\beta$, $\alpha \pm 0.618\beta$, delocalization energy with β ≈ −75 kJ/mol.
- [NIST CCCBDB: CO2 experimental vibrations](https://cccbdb.nist.gov/exp2x.asp?casno=124389&charge=0) — symmetric stretch 1333, antisymmetric stretch 2349, bend 667 cm⁻¹.
- [NumPy v2.5 manual, numpy.linalg.eigh](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html) — ascending eigenvalues, eigenvectors as columns.
- [NIST CODATA 2022: atomic mass constant](https://physics.nist.gov/cgi-bin/cuu/Value?u) — $m_u = 1.66053906892\times10^{-27}$ kg.
- [MIT OCW 18.06 Linear Algebra (Strang)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) — full treatment of eigenvalues and symmetric matrices.
