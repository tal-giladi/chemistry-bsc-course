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
- [x] M31
- [x] M32
- [x] M33

## Simulations
- [x] measurement-error
- [x] glassware
- [x] gas-laws
- [x] calorimetry
- [x] titration
- [x] gravimetry
- [x] kinetics
- [x] oscillators
- [x] rlc
- [x] quantum-box
- [x] boltzmann
- [x] spectrometer
- [x] chromatography
- [x] voltammetry
- [x] nmr
- [x] organic-bench
- [x] ir-esr

## After modules
- [x] merge glossary-inbox → glossary.md; research-inbox → references/research-log.md (scripts/merge_inboxes.py)
- [x] projects/ briefs (written with M33)
- [x] final QA: check.py 0 errors, npm run check-course 0 problems, git clean

## Now working

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
- M33 done.
- sims batch 1 done (common, measurement-error, glassware, gas-laws, calorimetry). QA: fix 07.7 parallax wording (burette reads low from above). Batch 2 spawned.
- M31 done.
- sims batch 2 done (titration, gravimetry, kinetics); batch 4 spawned.
- sims batch 3 done (oscillators, rlc, quantum-box, boltzmann); batch 5 spawned.
- sims batch 4 done (spectrometer, chromatography, voltammetry).
- QA: glossary (1003 terms) + research log merged; 25 unquoted quiz options fixed (dry run flagged); 07.7 burette parallax fixed. Dry run: only organic-bench links left.
- sims batch 5 done (nmr, organic-bench, ir-esr). check.py 0 errors; Academy dry run 0 problems. QA open: correct option is the longest in 57% of 1063 questions; rebalancing by agents.
- [x] QA: quiz length rank balance (25/25/25/24%)
- quiz-bias agents each split into sub-agents (9 total, disjoint module ranges) against the 2-agent rule; briefs now forbid sub-agents. Verify with quiz_bias.py + check.py when done.
- PAUSED (session tokens ending). State: all 33 modules + 17 simulations committed and pushed; glossary/research merged; check.py 0 errors; Academy dry run 0 problems (before quiz pass 2).
  Running at pause: quiz rank pass 2 (two agents, modules 1-16 and 17-33), uncommitted edits in *.quiz.yaml, progress in curriculum/status/quiz-rank.log.
  RESUME: respawn "Follow curriculum/QUIZ-RANK-BRIEF.md for modules 1 to 16 (range 1 16)" and the same for 17 33 (they skip logged files); then py scripts/quiz_rank.py, py scripts/check.py, npm run check-course (0 problems), commit + push, update TODO_FOR_TAL.md to "ready to import" with repo + commit.
- quiz rank pass 2 done for 17-33 (25/25/25/24%).
- 2026-10-18: quiz rank pass done for 1-16; course complete. Dry run: 176 lessons, 1063 questions, 0 problems.
