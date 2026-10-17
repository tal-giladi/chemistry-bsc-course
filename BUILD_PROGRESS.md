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
- [ ] M21
- [ ] M22
- [ ] M23
- [ ] M24
- [ ] M25
- [ ] M26
- [ ] M27
- [ ] M28
- [ ] M29
- [ ] M30
- [ ] M31
- [ ] M32
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
- agent: M22
- agent: M21

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
