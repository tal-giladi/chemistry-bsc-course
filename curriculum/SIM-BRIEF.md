# Simulation brief

Build interactive educational lab simulations for the course at `C:\Users\TalGiladi\OneDrive\repos\course-creator\chemistry-bsc-course`. Do not commit.

Read first: `C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md` §7 (binding), `curriculum/course-outline.md` §2 and §5, `plan.md` "Labs as simulations", and every lesson that links to your simulation (`grep -rn "simulations/<name>" lessons`) — the simulation must teach exactly what those lessons say, with the same numbers, vocabulary and presets.

## What a lab simulation must teach
The procedure, why each step is done, the safety reasoning, what can go wrong (realistic noise, operator mistakes such as parallax, overshooting an endpoint, oiling out), and how to analyse the data and its error (export a CSV of the readings the learner took, show the result with uncertainty). Use correct physical chemistry: real constants (CODATA 2022), real pKa / ε / k values with their source noted in a comment.

## Rules
- `simulations/<name>/index.html` + its own `.js`/`.css` next to it; shared code only in `simulations/common/` (check what exists; add, don't clobber — e.g. `common/sim.css`, `common/sim.js` for the label, query parsing, seeded RNG, safe storage, CSV export via a `data:` link with `download`, a simple canvas plot helper).
- Plain HTML + CSS + vanilla JS. No framework, bundler, npm, CDN, external fonts or any network request.
- ES modules do not load from `file://` in Chrome, so use classic `<script src>` files (IIFE / global namespace), not `type="module"`.
- Works in a sandboxed iframe (`allow-scripts` only): no cookies, no parent access, localStorage optional in try/catch, no alert/prompt/confirm/popups/top navigation.
- Responsive from 360 px; keyboard-usable (real buttons/inputs, labels, focus styles); light and dark (`prefers-color-scheme`).
- Visible label: "Educational model — not a real instrument".
- Presets from the URL query `?preset=<x>`; support every preset the lessons link, plus a sensible default. Show a short explanation of what the preset demonstrates and a task with a target.
- Deterministic where possible (seeded RNG `&seed=<n>`, "re-run" button changes seed).

## Also
- Add your rows to `simulations/README.md` (re-read right before writing; only add): one line per simulation with a relative link, the lessons that use it, and its presets.
- Verify: `node --check` every JS file; open each page headless if possible (e.g. a small node + jsdom-free smoke check is fine, or the Browser pane) with no console errors; `grep -n "http" simulations/<name>` must show no network references. Run `py scripts/check.py NN` for the modules that link to your simulation — their simulation-link errors must be gone.
- Checkpoint: append `<name> done` to `curriculum/status/simulations.log` after each simulation; skip names already there.
- Report back in under 100 words.

Never start sub-agents of your own: the course allows at most two writing agents at a time.
