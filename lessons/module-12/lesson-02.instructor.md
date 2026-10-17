# Instructor notes — 12.2 The Schrödinger equation and the particle in a box

- Objective: the learner reads $\hat H\psi = E\psi$ as an eigenvalue problem, uses $E_n = n^2h^2/8mL^2$ (including HOMO–LUMO for dyes), and writes a finite-difference solver that they verify by a convergence test.
- Likely confusion: probability versus probability density, and why normalising numerical vectors needs $\sqrt{\Delta x}$.
- Misconception: "The electron moves back and forth between the walls." A stationary state does not move; $|\psi|^2$ is time-independent. Also: "the node means the electron can't get from one side to the other" — there is no path to follow.
- Analogy: a skipping rope held at both ends can only swing in whole half-waves; more humps cost more effort.
- Expected hands-on result: Part A 1.504/6.017 eV, 275 nm; 1099 nm; 0.609 vs 0.196. Part B: errors −2.0e−5 (n=1) to −5.1e−4 (n=5) at N = 200; convergence 1.22e−3, 3.16e−4, 8.1e−5, 2.0e−5, 5.1e−6; finite well 2 bound states 0.1913 and 0.7057 eV, 5.7 % in the walls.
- Extension: add a small step or a linear (electric field) potential inside the box and watch the levels shift (a first look at perturbation theory, MIT 5.61 lectures on non-degenerate perturbation theory); or replace the box by a 2D square box with two quantum numbers and find the degeneracies.
