---
id: "03.1"
module: 3
minutes: 20
practice_minutes: 45
prerequisites: ["02.1"]
objectives:
  - Write a chemical reaction as a composition matrix and find its balancing coefficients from the null space.
  - Solve a two-component mixture for both concentrations from absorbances at two wavelengths.
  - Use least squares to combine absorbances at many wavelengths and report the residual.
  - Judge from the determinant or condition number whether a linear system will amplify measurement noise.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 4.1 Writing and Balancing Chemical Equations"
    url: https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations
  - title: "LibreTexts, UV/Vis Analysis of Two-Component Mixtures (Davis, CHEM 235)"
    url: https://chem.libretexts.org/Courses/Manchester_University/CHEM_235%3A_Analytical_Chemistry_(Davis)/08%3A_Analysis_and_Separation_of_Mixtures/8.01%3A_UV_Vis_Analysis_of_Two-Component_Mixtures
  - title: "SciPy v1.18 manual, scipy.linalg.null_space"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.null_space.html
  - title: "MIT OpenCourseWare 18.06 Linear Algebra (Strang, Spring 2010)"
    url: https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/
last_verified: "2026-10-16"
---

# 03.1 · Vectors, matrices and solving linear systems

A linear system is a set of equations where every unknown appears only multiplied by a number and added up. Chemistry is full of them: atom counts in a reaction, absorbances of a mixture, mass balances in a reactor. This lesson shows how to write such problems as one matrix equation, how to solve it by hand for two unknowns and with numpy for many, and how to tell in advance when the answer will be ruined by small errors in the data.

## Why it matters

A food lab receives a green drink coloured with a yellow dye and a blue dye. The regulator wants both concentrations. The two dyes absorb light at overlapping wavelengths, so no single absorbance gives either one. Two measurements at two wavelengths give two equations, and solving them gives both numbers in one go. Choose the wavelengths badly, though, and the same calculation returns a negative concentration. The difference between a good and a bad choice is one number you can compute before you start: how well-conditioned the matrix is. The same matrix thinking balances any reaction, however ugly, without trial and error.

## Core ideas

> [!NOTE]
> Everything here is stable mathematics. The only part that can date is the software: the code uses numpy 2.5 and scipy 1.18 (`scipy.linalg.null_space`), pinned in the course requirements and checked 2026-10-16. The dye absorptivities in the lab are illustrative, not data for real food dyes.

### Vectors and matrices

A vector is an ordered list of numbers, such as the concentrations $\mathbf{c} = (c_X, c_Y)$. A matrix is a rectangular table of numbers. Its size is written rows × columns. Multiplying a matrix by a vector gives a new vector: each entry is one row of the matrix times the vector, entry by entry, added up.

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} a x + b y \\ c x + d y \end{pmatrix}$$

So a whole set of linear equations is one line: $E\,\mathbf{c} = \mathbf{A}$, where $E$ holds the known coefficients, $\mathbf{c}$ the unknowns and $\mathbf{A}$ the measured values.

### Beer–Lambert for a mixture

Beer–Lambert says the absorbance of one species is $A = \varepsilon b c$: molar absorptivity $\varepsilon$ (L mol⁻¹ cm⁻¹, how strongly it absorbs at that wavelength), path length $b$ (cm) and concentration $c$ (mol/L). Absorbances of different species add. At two wavelengths $\lambda_1, \lambda_2$:

$$\begin{pmatrix} \varepsilon_{X,1} & \varepsilon_{Y,1} \\ \varepsilon_{X,2} & \varepsilon_{Y,2} \end{pmatrix} b \begin{pmatrix} c_X \\ c_Y \end{pmatrix} = \begin{pmatrix} A_1 \\ A_2 \end{pmatrix}$$

Two unknowns need at least two independent equations. With $n$ components you need at least $n$ wavelengths.

### Solving a 2×2 system: the determinant and Cramer's rule

For $\begin{pmatrix} a & b \\ c & d \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} p \\ q \end{pmatrix}$, the determinant is $\det = ad - bc$. If it is not zero there is exactly one solution:

$$x = \frac{p\,d - b\,q}{\det}, \qquad y = \frac{a\,q - p\,c}{\det}$$

This is Cramer's rule. If $\det = 0$ the two rows say the same thing (one is a multiple of the other) and the system cannot pin down both unknowns. For bigger systems you do not use Cramer's rule; you use Gaussian elimination (subtract multiples of one row from the others until the matrix is triangular), which is what `np.linalg.solve` does inside.

### Conditioning: when small errors become big ones

If the determinant is small compared with the entries, the two rows are nearly parallel, and a tiny error in $A_1$ or $A_2$ moves the answer a lot. The condition number, `np.linalg.cond(E)`, measures this. Roughly: the relative error in the answer can be up to the condition number times the relative error in the data. A value near 1 is excellent; 100 means 1 % noise can become 100 % error. For a mixture, this means: pick wavelengths where each species dominates a different one.

### Balancing a reaction is a null-space problem

Write unknown coefficients $\nu_1 \dots \nu_n$ in front of each species. Conservation of each element is one linear equation. For propane burning, $\nu_1\,\mathrm{C_3H_8} + \nu_2\,\mathrm{O_2} \to \nu_3\,\mathrm{CO_2} + \nu_4\,\mathrm{H_2O}$, with products counted negative:

$$M\boldsymbol{\nu} = \begin{pmatrix} 3 & 0 & -1 & 0 \\ 8 & 0 & 0 & -2 \\ 0 & 2 & -2 & -1 \end{pmatrix}\begin{pmatrix} \nu_1 \\ \nu_2 \\ \nu_3 \\ \nu_4 \end{pmatrix} = \mathbf{0}$$

Rows are C, H and O; columns are the species. The right side is zero, so we want the null space of $M$: all vectors that $M$ sends to zero. Three equations, four unknowns: one free choice, which is the overall scale. Any multiple of a balanced equation is still balanced.

The rank of a matrix is the number of truly independent rows. Here rank is 3 and there are 4 species, so the null space has dimension $4 - 3 = 1$: one reaction. If the dimension comes out 2, the species list allows two independent reactions and "balancing" alone cannot decide between them; you need chemistry (for example, which products were actually observed).

### Least squares: more equations than unknowns

A spectrometer gives absorbances at hundreds of wavelengths, not two. With more equations than unknowns there is usually no exact solution, because each measurement has noise. Least squares picks the $\mathbf{c}$ that makes the sum of squared differences $\sum (A_i - (E\mathbf{c})_i)^2$ smallest. In numpy: `np.linalg.lstsq(E, A, rcond=None)`. Using every wavelength averages out noise and the residual (what the fit cannot explain) tells you whether a third, unexpected species is present. This is the same idea as the straight-line fit of [02.1](../module-02/lesson-01.md), with more than one slope.

## Worked example

### 1. Balance propane combustion from the null space

From the matrix above: row 1 gives $\nu_3 = 3\nu_1$. Row 2 gives $\nu_4 = 4\nu_1$. Row 3 gives $2\nu_2 = 2\nu_3 + \nu_4 = 10\nu_1$, so $\nu_2 = 5\nu_1$. Choose $\nu_1 = 1$:

$$\mathrm{C_3H_8} + 5\,\mathrm{O_2} \to 3\,\mathrm{CO_2} + 4\,\mathrm{H_2O}$$

Check: C 3 = 3, H 8 = 8, O 10 = 6 + 4. A computer does exactly this, returning the null-space vector scaled to length 1, for example $(0.140, 0.700, 0.420, 0.560)$ (the sign may come out flipped). Divide by the smallest entry to get $(1, 5, 3, 4)$.

### 2. Two dyes from two absorbances

Dye X and dye Y in a 1.00 cm cell. Molar absorptivities: at 430 nm, $\varepsilon_X = 1.60\times10^4$, $\varepsilon_Y = 2.50\times10^3$; at 630 nm, $\varepsilon_X = 1.20\times10^3$, $\varepsilon_Y = 1.05\times10^4$ (all L mol⁻¹ cm⁻¹). The mixture reads $A_{430} = 0.520$ and $A_{630} = 0.400$.

1. $\det = (1.60\times10^4)(1.05\times10^4) - (2.50\times10^3)(1.20\times10^3) = 1.680\times10^8 - 3.0\times10^6 = 1.650\times10^8$.
2. $c_X = \dfrac{0.520 \times 1.05\times10^4 - 2.50\times10^3 \times 0.400}{1.650\times10^8} = \dfrac{5460 - 1000}{1.650\times10^8} = 2.70\times10^{-5}$ mol/L.
3. $c_Y = \dfrac{1.60\times10^4 \times 0.400 - 0.520 \times 1.20\times10^3}{1.650\times10^8} = \dfrac{6400 - 624}{1.650\times10^8} = 3.50\times10^{-5}$ mol/L.

Check by substituting back: $1.60\times10^4 \times 2.70\times10^{-5} + 2.50\times10^3 \times 3.50\times10^{-5} = 0.432 + 0.0875 = 0.520$. The determinant is large compared with the off-diagonal product, so the system is well-conditioned: each wavelength is dominated by one dye.

## Hands-on

What you need: Python 3.14 with the course packages ([labs/common](../../labs/common/requirements.txt)), the [Module 3 lab folder](../../labs/module-03/), pencil and paper. Time: about 45 minutes.

### Part A — pencil (15 min)

1. Balance $\mathrm{Fe_2O_3} + \mathrm{CO} \to \mathrm{Fe} + \mathrm{CO_2}$ by writing the composition matrix (rows Fe, O, C) and solving it.
2. Compute the determinant of $\begin{pmatrix} 4 & 2 \\ 6 & 3 \end{pmatrix}$. What does it tell you about a mixture problem with these absorptivities?
3. Solve $2x + y = 5$, $x + 3y = 10$ with Cramer's rule.

<details><summary>Answers to Part A</summary>

1. Columns $\mathrm{Fe_2O_3}$, CO, Fe, $\mathrm{CO_2}$ (products negative). Fe: $2\nu_1 = \nu_3$. O: $3\nu_1 + \nu_2 = 2\nu_4$. C: $\nu_2 = \nu_4$. So $\nu_2 = \nu_4 = 3\nu_1$ and $\nu_3 = 2\nu_1$: $\mathrm{Fe_2O_3} + 3\,\mathrm{CO} \to 2\,\mathrm{Fe} + 3\,\mathrm{CO_2}$.
2. $4 \times 3 - 2 \times 6 = 0$. The second row is 1.5 times the first: the two wavelengths carry the same information (the two species have the same spectral shape there), so the concentrations cannot be separated. Pick another wavelength.
3. $\det = 5$. $x = (5 \times 3 - 1 \times 10)/5 = 1$, $y = (2 \times 10 - 5 \times 1)/5 = 3$.

</details>

### Part B — Python (30 min)

1. Open `lesson01_linear.py`. Fill in the three functions marked TODO: `balance`, `solve_two`, `solve_lstsq`. The hints are in the comments.
2. Run it from the lab folder:

```bash
py lesson01_linear.py
```

3. Open `runs/lesson01_linear.png`: the mixture spectrum, the two dye parts and their sum.

The script balances $\mathrm{KMnO_4} + \mathrm{HCl} \to \mathrm{KCl} + \mathrm{MnCl_2} + \mathrm{Cl_2} + \mathrm{H_2O}$, a redox equation that is painful by trial and error. Then it reads `mixture_absorbance.csv` (13 wavelengths, 400–700 nm, generated from known concentrations with 0.003 absorbance noise) and solves for both dyes three ways: at each dye's peak, at a badly chosen pair, and with least squares over all 13 points.

How you know it worked: the coefficients are 2, 16, 2, 2, 5, 8 and $M\boldsymbol{\nu}$ prints as all zeros. At the two peaks (425 and 625 nm) you get $c_X \approx 2.70\times10^{-5}$ and $c_Y \approx 3.49\times10^{-5}$ mol/L with condition number about 1.5. At 425 and 450 nm (both on the dye X band) the condition number jumps to about 330 and $c_Y$ comes out negative. Least squares gives $2.69\times10^{-5}$ and $3.51\times10^{-5}$ mol/L with an rms residual near 0.002, the size of the noise.

<details><summary>Reference solution</summary>

`balance`: `ns = null_space(M)`, divide the single column by its smallest absolute entry, make it positive, convert each entry with `Fraction(x).limit_denominator(100)`, multiply by the least common multiple of the denominators. `solve_two`: `np.linalg.solve(path_cm * np.array([eps_1, eps_2]), [A_1, A_2])`. `solve_lstsq`: `np.linalg.lstsq(path_cm * np.column_stack([eps_X, eps_Y]), A, rcond=None)[0]`. Full code: `lesson01_linear_solution.py`.

Why the bad pair fails: at 425 and 450 nm dye Y absorbs almost nothing and the same small amount at both, so its whole answer rests on the difference between two noisy absorbances. The residual of the least-squares fit equals the noise level, which says no third coloured species is hiding in the sample. If it were several times larger, you would suspect one.

</details>

## Common mistakes

- Forgetting the minus sign on products in the composition matrix. Without it the null space is empty (only zeros) or gives nonsense. Reactants positive, products negative.
- Rounding null-space entries too early. The computer returns decimals like 0.70014; divide by the smallest one first, then convert to fractions.
- Choosing wavelengths where both species absorb in the same ratio. The determinant is near zero and the answer can be negative. Check `np.linalg.cond` before trusting the result.
- Solving with only as many wavelengths as components when more are available. Least squares over the whole spectrum averages out noise and the residual warns you about an unknown component.
- Mixing units inside the matrix. All $\varepsilon$ in L mol⁻¹ cm⁻¹, $b$ in cm, so $c$ comes out in mol/L.
- Calling an equation balanced when the null space has dimension 2. That means two independent reactions fit the species list; you must decide from chemistry which happened.

## Key takeaways

- A set of linear equations is one matrix equation, $E\mathbf{c} = \mathbf{A}$; numpy solves it with `np.linalg.solve`.
- A 2×2 system has one solution when $\det = ad - bc \ne 0$; Cramer's rule gives it by hand.
- Balancing a reaction means finding the null space of the composition matrix; its dimension says how many independent reactions exist.
- A large condition number means noise in the data is amplified; choose measurements where each unknown dominates a different equation.
- With more measurements than unknowns, least squares gives the best compromise and its residual checks the model.

## Sources

- [OpenStax Chemistry 2e, 4.1 Writing and Balancing Chemical Equations](https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations) — balancing by conservation of atoms.
- [LibreTexts, UV/Vis Analysis of Two-Component Mixtures](https://chem.libretexts.org/Courses/Manchester_University/CHEM_235%3A_Analytical_Chemistry_(Davis)/08%3A_Analysis_and_Separation_of_Mixtures/8.01%3A_UV_Vis_Analysis_of_Two-Component_Mixtures) — additive Beer–Lambert, n wavelengths for n components, wavelength choice.
- [SciPy v1.18 manual, scipy.linalg.null_space](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.null_space.html) — the function used to balance equations.
- [MIT OCW 18.06 Linear Algebra (Strang)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) — the full course on elimination, rank, null spaces and least squares.
