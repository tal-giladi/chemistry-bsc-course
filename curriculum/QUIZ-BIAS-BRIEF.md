# Quiz length-bias fix brief

Repo: `C:\Users\TalGiladi\OneDrive\repos\course-creator\chemistry-bsc-course`. Do not commit.

Problem: in about 57% of quiz questions the correct option is the longest, so a learner can guess by length. The Academy rule (`C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md` §5): all four options have similar length and tone; the correct one is not the longest or the most hedged. Target: the correct option is the longest in at most 30% of questions in your range, and never longer than the longest wrong option by more than ~15 characters.

## How
1. `py scripts/quiz_bias.py <first> <last>` lists the offending questions in your module range.
2. For each, edit only `options` (and the `explanation` if it quotes an option): shorten the correct option (cut hedges and "because…" padding it does not need) and/or lengthen wrong options with a plausible but wrong reason, so lengths are similar. Keep the chemistry exactly right; keep wrong options plausible mistakes, never absurd; no all/none of the above. Do not change `id`, `question` meaning or `correct` index; do not reorder options.
3. YAML: keep `>-` block scalars for text with `:`, `#`, quotes or backslashes; a plain option containing `: ` or that looks like a number must be quoted. Never leave an option that parses as a non-string.
4. Work file by file. After each file: `py scripts/check.py <module>` must show 0 errors. Append `<file> done` to `curriculum/status/quiz-bias.log`; on start, skip files already in that log.
5. Finish: `py scripts/quiz_bias.py <first> <last>` shows ≤ 30%; `py scripts/check.py` 0 errors. Report in under 60 words.

Edit only `.quiz.yaml` files in your module range.

Never start sub-agents of your own: the course allows at most two writing agents at a time.
