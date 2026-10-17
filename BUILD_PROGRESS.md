# Build progress (for resuming after a crash)

Goal: build the whole course described in `plan.md` and `curriculum/course-outline.md` (33 modules, 176 lessons, 17 simulations) so it imports into Tal's Academy with 0 problems.
Binding rules: `C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md`.

Max 2 writing agents at a time. Each module agent follows `curriculum/AGENT-BRIEF.md`; simulation agents follow `curriculum/SIM-BRIEF.md`.

Resume: read this file + `curriculum/status/*.log`; respawn unfinished modules with "Write module NN per curriculum/AGENT-BRIEF.md" (the agent skips done lessons). Commit + push after every finished module.
Validate: `py scripts/check.py [NN]`, then `cd C:/Users/TalGiladi/OneDrive/repos/tals-academy && npm run check-course -- ../course-creator/chemistry-bsc-course`.
Titles/paths: `scripts/manifest.py` (regenerates `_sidebar.md`).

## Foundations
- [x] plan.md points to the Academy instructions
- [x] GitHub repo public: tal-giladi/chemistry-bsc-course
- [x] manifest + _sidebar.md, scripts/check.py
- [x] course-outline.md, AGENT-BRIEF.md, SIM-BRIEF.md
- [x] labs/common/requirements.txt (Python 3.14 pins, checked 2026-10-16)
- [x] README, COURSE-MAP, glossary stub, references/README, templates, simulations/README, course-details.md

## Modules
- [x] M01
- [x] M02
- [x] M03
- [x] M04
- [x] M05
- [x] M06
- [x] M07
- [x] M08
- [x] M09
- [x] M10
- [x] M11
- [x] M12
- [x] M13
- [x] M14
- [x] M15
- [x] M16
- [x] M17
- [x] M18
- [x] M19
- [x] M20
- [x] M21
- [x] M22
- [x] M23
- [x] M24
- [x] M25
- [x] M26
- [x] M27
- [x] M28
- [x] M29
- [x] M30
- [ ] M31
- [x] M32
- [ ] M33

## Simulations
- [ ] measurement-error
- [ ] glassware
- [ ] gas-laws
- [ ] calorimetry
- [ ] titration
- [ ] gravimetry
- [ ] kinetics
- [ ] oscillators
- [ ] rlc
- [ ] quantum-box
- [ ] boltzmann
- [ ] spectrometer
- [ ] chromatography
- [ ] voltammetry
- [ ] nmr
- [ ] organic-bench
- [ ] ir-esr

## After modules
- [ ] merge glossary-inbox → glossary.md; research-inbox → references/research-log.md; template-inbox → templates/
- [ ] projects/ briefs (research project ideas)
- [ ] final QA: `py scripts/check.py` clean, `npm run check-course` 0 problems, git clean, TODO_FOR_TAL.md ready

## Now working
- agent: M33
- agent: M31

## Decisions
- 2026-10-16 Tal: whole degree in one course; non-chemistry subjects as short bridge modules.
- Lesson sections fixed: Why it matters · Core ideas · Worked example · Hands-on · Common mistakes · Key takeaways · Sources.
- SDBS data is linked, never copied (redistribution not allowed).

## Log
- 2026-10-16: foundations started.
- 2026-10-16: M01 agent spawned.
- 2026-10-16: foundations done; M02 agent spawned.
- M02 done; M03 spawned.
- M01 done; M04 spawned.
- M03 done (after one stall/resume); M05 spawned.
- M04 done; M06 spawned.
- M05 done; M07 spawned.
- M06 done; M08 spawned.
- M07 done; M09 spawned.
- M08 done; M10 spawned.
- M09 done; M11 spawned.
- M10 done; M12 spawned.
- M11 done; M13 spawned.
- M12 done; M14 spawned.
- M13 done; M15 spawned.
- M14 done; M16 spawned.
- M15 done; M17 spawned.
- M16 done; M18 spawned.
- M17 done; M19 spawned.
- M18 done; M20 spawned.
- PAUSED by Tal: no new agents after M19 + M20 finish. Resume from M21.
- M19 done.
- M20 agent hit session limit mid-module; resume it (SendMessage) or respawn after 15:10 Asia/Jerusalem.
- Resumed by Tal; M20 agent resumed, M21 spawned.
- M20 done; M22 spawned.
- M21 done; M23 spawned.
- M22 done; M24 spawned.
- M23 done; M25 spawned.
- M24 done; M26 spawned.
- M25 done; M27 spawned.
- M26 done; M28 spawned.
- M27 done; M29 spawned.
- M28 done; M30 spawned.
- M29 done; M31 spawned.
- M30 done; M32 spawned.
- M32 done; M33 spawned.
