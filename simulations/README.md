# Simulations

Standalone educational simulations of the course's labs (plain HTML, CSS and classic scripts; no network). Each is an educational model: it teaches the procedure, why each step is done, the safety reasoning, what can go wrong and how to analyse the data, but it does not train your hands. Pass `?preset=<name>` to start at a preset. Shared code lives in `common/`.

- [measurement-error](measurement-error/index.html) — repeat readings, 95 % intervals, bias and calibration with a CRM, propagation (first order and Monte Carlo). Lessons 01.5, 09.1, 09.2, 09.3. Presets: `repeat`, `bias`, `propagation`.
- [glassware](glassware/index.html) — weighing by difference on a drifting balance, a dilution with its uncertainty budget, parallax at a meniscus. Lesson 07.7. Presets: `weighing`, `dilution`, `parallax`.
- [gas-laws](gas-laws/index.html) — ideal gas and work of compression, van der Waals Z and isotherms with the Maxwell construction, a hard-sphere kinetic box, a Clément–Desormes bench. Lessons 07.6, 13.1, 13.5, 23.1. Presets: `ideal`, `real`, `kinetic`.
- [calorimetry](calorimetry/index.html) — coffee-cup calibration, enthalpy of solution and of neutralisation, bomb calorimeter, all with fore- and after-line extrapolation. Lessons 08.1, 08.7, 13.2, 23.2. Presets: `coffee-cup`, `dissolution`, `neutralisation`, `bomb`.
- [common](common/) — shared `sim.css` (light/dark tokens, layout) and `sim.js` (label, query and presets, seeded RNG, safe storage, statistics, CSV export, canvas plot, animation loop; API documented at the top of the file).
