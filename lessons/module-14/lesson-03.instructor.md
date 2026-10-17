# Instructor notes — 14.3 Normal modes of three coupled masses

- Objective: the learner sets up K v = omega^2 M v for a three-mass chain, solves it, and tests the predicted 0 : 1 : 3 pattern of omega^2 shifts on a home pendulum chain.
- Likely confusion: eigenvalues are omega^2, not omega or f; the difference between the walls chain (no zero mode) and the free chain (one zero mode); why gravity adds the same g/L to every mode.
- Misconception: "Each pendulum has its own frequency and the bands just disturb it." In the coupled system no pendulum has a frequency of its own; only the modes do.
- Analogy: three people on a sofa with springy cushions. They can all bounce together, the two ends can bounce opposite while the middle sits still, or neighbours can bounce opposite. Each pattern has its own rhythm.
- Expected hands-on result: walls chain 0.7654, 1.4142, 1.8478 sqrt(k/m); free chain 0, 1, 1.7321; example pendulums T = 1.414, 1.363, 1.270 s, fit g/L = 19.72 1/s^2, c = 1.59 1/s^2 (true 19.59 and 1.60), residuals under 0.05; first transfer near 18 s; slowest beat 36 s. Simulation target 1.22, 2.25, 2.94 Hz.
- Extension: make the middle bob twice as heavy and check that mode 2 keeps its period while modes 1 and 3 change; or add a fourth pendulum and predict the four modes with chain_K before measuring.
