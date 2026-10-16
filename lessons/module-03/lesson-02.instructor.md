# Instructor notes — 03.2 Eigenvalues and eigenvectors

- Objective: the learner sets up a small symmetric matrix for a chemical problem, gets its eigenvalues by hand (2×2, 3×3) or with `eigh`, and reads an eigenvector as an orbital or a vibration.
- Likely confusion: the sign of β. `eigh` sorts x ascending, but because β < 0 the largest x is the most stable orbital. Have learners write E = α + xβ next to every list.
- Misconception: "Eigenvectors are unique." Any scalar multiple (including −1) is the same eigenvector; degenerate eigenvalues (benzene) have a whole plane of valid eigenvectors.
- Analogy: an eigenvector is a direction a matrix does not turn, like the axis of a spinning top; only the length changes.
- Expected hands-on result: butadiene ±1.618, ±0.618, deloc 0.472β (≈35 kJ/mol); hexatriene 0.988β; benzene 2,1,1,−1,−1,−2, deloc 2β (≈150 kJ/mol); CO2 k ≈ 1675 N/m, modes 0, 1333, 2552 cm⁻¹ (observed antisymmetric 2349, model +9 %).
- Extension: add a bond-bond coupling term k' to the CO2 matrix and choose k and k' so both stretches match 1333 and 2349 cm⁻¹; then try naphthalene (10 atoms) in the Hückel code.
