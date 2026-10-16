# Instructor notes — 05.2 Arrays, vectorised maths and plotting

- Objective: think in whole arrays and shapes; broadcast a row with a column; integrate along the right axis; a labelled, saved figure.
- Likely confusion: which axis is which. Have the learner print `.shape` after every new line until it is a habit.
- Misconception: "Vectorisation is only about speed." The bigger win is code that matches the equation and has no index bugs.
- Analogy: broadcasting is a multiplication table; a row of speeds and a column of temperatures fill the whole grid.
- Expected hands-on result: shapes (2501,), (3, 1), (3, 2501); area 1.00000 at all T; mean speed 388.8 / 474.7 / 614.7 m/s; v_mp 345 / 421 / 545 m/s on a 1 m/s grid (formula 344.6 / 420.7 / 544.8); P(v > 1000 m/s) = 0.0008 / 0.0102 / 0.0805; loop about 50x slower (machine-dependent).
- Watch for: learners who write `np.sqrt(2*K_B*T/M_N2)` with T as a column and then index wrongly; `T[:, 0]` turns it back into a row.
- Extension: add H2 and CO2 on the same plot (masses as a third broadcast axis, shape (3, 1, 1)); or overlay the Arrhenius ratio grid as a heat map with `ax.pcolormesh`.
