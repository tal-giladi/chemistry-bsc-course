# Instructor notes — 01.5 Your home kit and first measurement

- **Objective:** a safe kitchen kit; a calibrated syringe; density with mean, SD and combined standard uncertainty; an agreement test against reference data.
- **Likely confusion:** standard deviation (spread of single repeats) versus standard uncertainty of the mean ($s/\sqrt{n}$). Also why the resolution term is $d/\sqrt{6}$ (difference of two readings) and why the script does not divide it by $\sqrt{n}$ (a cautious choice, since the same cup and scale are used each time).
- **Misconception:** "more repeats fix everything" and "identical readings mean zero uncertainty". The bias preset of the measurement-error simulation targets the first; the 1 g scale targets the second.
- **Analogy:** a bathroom scale that reads 2 kg high gives the same wrong answer every morning. Weighing yourself 30 times does not help; stepping on it with a known 10 kg sack does.
- **Expected hands-on result:** calibration factor 0.97–1.03 (example data: 1.0105); densities near 0.998, 1.038, 1.081, 1.127 g/mL (temperature-corrected), standard uncertainty about 0.005–0.008 g/mL with a 1 g scale and about 0.001–0.002 g/mL with a 0.1 g scale; most |z| ≤ 2. Typical failures: bubbles (density high), undissolved sugar (low), not rinsing the syringe between solutions.
- **Extension:** use the calibrated syringe to find the sugar content of a soft drink from its density (degas it first by stirring), and compare with the nutrition label; or repeat with salt solutions and look up the reference values.
- **Lab files:** `labs/module-01/` — the learner script runs before the TODOs are done and shows |z| ≈ 3–5 on the example data, which is the point.
