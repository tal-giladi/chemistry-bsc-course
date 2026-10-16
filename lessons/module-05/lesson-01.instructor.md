# Instructor notes — 05.1 Python setup and the scientific stack

- Objective: a working Python 3.14 venv with the eight pinned packages, verified by `check_setup.py`; a first script with dict, function, f-string.
- Likely confusion: "which Python am I running?" On Windows there can be several (install manager, Store, Anaconda, uv). `check_setup.py` prints `sys.executable`; have the learner read it aloud.
- Misconception: "Newest is always best." A week-old Python (3.15.0 on 2026-10-09) may lack wheels; pinned 3.14 is current and safe.
- Analogy: a venv is a clean, labelled bench for one experiment; requirements.txt is the reagent list with lot numbers.
- Expected hands-on result: `All good` from `check_setup.py`; molar masses NaCl 58.440, sucrose 342.297, NaHCO3 84.006, citric acid 192.123, acetic acid 60.052, water 18.015 g/mol; 8.557 g sucrose for 250 mL of 0.100 M; `CH3COOH` = `C2H4O2`.
- Watch for: rdkit is the largest download; slow networks may time out. Rerun the same install line; pip resumes.
- Extension: extend `parse_formula` to brackets (`Ca(OH)2`, `CuSO4·5H2O`) with a recursive parser or a stack.
