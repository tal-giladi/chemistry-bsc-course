# Instructor notes — 03.4 Second-order equations and oscillators

- Objective: the learner solves the damped oscillator via its characteristic equation, classifies damping, computes a bond force constant from a wavenumber, and extracts γ and Q from amplitude data.
- Likely confusion: complex roots. Emphasise that the imaginary part is the oscillation frequency and the real part the decay rate; Euler's formula turns the pair into a real cosine.
- Misconception: "More damping always means a faster return." Past critical damping the return gets slower again (overdamped creep).
- Analogy: the reduced mass is a heavy truck tied to a bicycle by a spring; only the bicycle moves much, so the motion is set almost entirely by the light partner (H in HCl).
- Expected hands-on result: roots for b = 0.4/4/10 (m = 1, k = 4): −0.2 ± 1.99i, −2 (double), −9.58 and −0.42; solve_ivp vs formula ~5e-10; HCl μ = 0.97959 u, k ≈ 516 N/m, 11.15 fs; example pendulum period 1.420 s, γ ≈ 0.0113 1/s (model 0.0120, readings rounded to 0.5 cm), half-life ≈ 61 s, Q ≈ 196.
- Extension: add a quadratic drag term c v|v| to rhs and fit the example data with both models; compute ω_e for D35Cl from the same k and compare with the NIST value.
