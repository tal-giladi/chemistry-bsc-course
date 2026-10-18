# Quiz option-length rank brief (pass 2)

Repo: `C:\Users\TalGiladi\OneDrive\repos\course-creator\chemistry-bsc-course`. Do not commit. Never start sub-agents of your own.

Pass 1 overshot: the correct option is now the second-longest in 61% of questions, which is a new guessing cue. Goal: the correct option's length rank (0 = longest … 3 = shortest) is spread about 25% each, and all four options in a question stay similar in length.

`py scripts/quiz_rank.py <first> <last> --list` gives, for every question that is off, its current rank and its **target rank** (assigned round-robin per file). Make each listed question hit its target.

## How
- Edit only `options` text. Usually the smallest change is enough: add or drop a few words in one or two options (a plausible extra reason in a wrong option; a crisper or slightly fuller correct option). Keep all four within roughly ±20% of each other in length.
- Keep the chemistry exactly right and every wrong option a plausible mistake. No all/none of the above. Do not change `id`, `question`, `correct` or option order. If the `explanation` quotes an option, keep it consistent.
- YAML: options containing `: ` or that look like numbers must be quoted; keep `>-` for text with `:`, `#`, quotes or backslashes. Every option must parse as a non-empty string.
- If a question's options are all short numbers or formulas of the same format, leave it (report how many).
- Work file by file. After each file: `py scripts/check.py <module>` = 0 errors; append `<file> done` to `curriculum/status/quiz-rank.log`. On start, skip files already there.
- Finish: `py scripts/quiz_rank.py <first> <last>` shows each rank 20–30% and `py scripts/check.py` 0 errors. Report in under 60 words.

Edit only `.quiz.yaml` files in your module range.
