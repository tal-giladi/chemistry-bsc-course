# Instructor notes — 12.5 Rotors, angular momentum and the hydrogen atom

- Objective: the learner gets bond lengths from $B$, predicts rotational line positions and populations, and uses the hydrogen quantum numbers and node rules, verified with the radial solver.
- Likely confusion: level energies $BJ(J+1)$ versus line positions $2B(J+1)$; $c$ in cm/s; $u(r)$ versus $R(r)$ versus $\psi$.
- Misconception: "The angular momentum points along z." $|L| > |L_z|$ always. Also: "2s and 2p have different energies in hydrogen" — only once other electrons screen the nucleus.
- Analogy: the centrifugal barrier is the same reason a fast-spinning skater on a merry-go-round cannot get to the centre without losing angular momentum.
- Expected hands-on result: r_e 1.2746 Å, r_0 1.2839 Å; lines 20.88, 41.74, 62.58, 83.38, 104.13, 124.82 cm⁻¹; J_max = 3 at 298 K, J = 1 at 50 K; hydrogen −0.49999, −0.12500, −0.05556 hartree; nodes n − ℓ − 1; ⟨r⟩ = 1.5000 bohr; IE 13.598 eV. Part A: CO 3.84 cm⁻¹, 115 GHz; 2s node 105.8 pm.
- Extension: add a screened potential $-Z_\text{eff}(r)/r$ (for example Li-like with a core) to the radial solver and see 2s fall below 2p; or compute the HCl rovibrational P and R branch positions from $B_0$, $B_1$ and the fundamental.
