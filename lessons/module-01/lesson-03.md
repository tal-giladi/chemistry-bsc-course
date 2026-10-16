---
id: "01.3"
module: 1
minutes: 15
practice_minutes: 60
prerequisites: ["01.2"]
objectives:
  - Write a notebook page that another person could repeat without asking you anything.
  - Correct a notebook entry so the original value stays readable.
  - Organise a short lab report into its standard sections, with tables and figures labelled with units.
  - Report a measured result with its spread and a sensible number of digits.
volatility: concept
sources:
  - title: "NIH Office of Intramural Research — Electronic Lab Notebooks"
    url: https://oir.nih.gov/sourcebook/intramural-program-oversight/electronic-lab-notebooks
  - title: "NIH OIR — Best practices for keeping an ELN (trainees), 2024"
    url: https://oir.nih.gov/system/files/media/file/2024-07/best_practices-keeping_eln-trainee_0.pdf
  - title: "Truman State University Chemistry — The Laboratory Report"
    url: https://chemlab.truman.edu/the-laboratory-report
  - title: "UCLA Chemistry and Biochemistry — Research report guidelines"
    url: https://www.chemistry.ucla.edu/undergraduate/undergraduate-research/research-report-guidelines/
  - title: "NIST SP 811 — Guide for the Use of the International System of Units"
    url: https://www.nist.gov/pml/special-publication-811
last_verified: "2026-10-16"
---

# 01.3 · The lab notebook and the lab report

A lab notebook is the record of what you actually did and saw, written at the time. A lab report is the story you tell afterwards, built from that record. This lesson shows how to keep a notebook that someone else could follow, how to fix mistakes honestly, and how to turn raw numbers into a short, clear report.

## Why it matters

Three months from now you will look at a number you wrote down, 1.06, and wonder: was that grams per millilitre? Was the sugar solution 10% or 20%? Was it before or after you found that the syringe leaked? If the notebook does not say, the measurement is lost. You have to do it again.

In research, the stakes are higher. Notebooks are used to prove who discovered something first, to defend a patent, and to check results that other labs cannot reproduce. A missing date or an erased number can make months of work worthless. Employers check how you keep records; it is one of the few lab habits you can build fully at home.

## Core ideas

### What a notebook is for

A **lab notebook** is a permanent, dated record of your work, written while you work. It has three jobs:

1. **Repeatability.** Someone else (or you, in a year) can repeat exactly what you did.
2. **Honesty.** It shows what really happened, including the failures.
3. **Raw data.** It holds the numbers as the instrument showed them, before any calculation.

**Raw data** means the values you read directly, such as "cup empty: 112 g; cup + water: 162 g". **Processed data** means values you calculated from them, such as "water: 50 g". Always write raw data first. If you write only processed data, nobody can check your arithmetic, including you.

### The rules for each page

These rules come from research labs. They work just as well at a kitchen table.

- Use a **bound notebook** with numbered pages, and a pen. Pages that can fall out, and pencil that can be erased, make the record unreliable.
- Start each entry with the **date**, a **title** and a one-line **aim**.
- List the **equipment**, including each instrument's **resolution**: the smallest step it can show. For example: "kitchen scale, 1 g steps".
- Note the **conditions** that might matter: room temperature, the brand of sugar, anything unusual.
- Draw your **data table before you measure**, with units in the column headers. Then fill it in as you go.
- Write numbers **straight into the notebook**. Never onto a scrap of paper to copy later.
- **Never erase or overwrite.** To fix an entry, strike it through with one line so it stays readable, write the new value next to it, and add a short reason and your initials.
- **Record what went wrong.** "Bubble in syringe, repeat 3 discarded" is useful data.
- Leave no blank gaps. Draw a line through unused space at the end of an entry.

### Paper or electronic?

An **electronic lab notebook** (ELN) is software that does the same job. It adds automatic timestamps, a history of every change, and easy search. Many organisations now require one. For example, the US National Institutes of Health made an approved ELN the only accepted notebook for its in-house research labs from 30 June 2024.

At home, either works. A paper notebook plus phone photos of your setup is fine. A plain document with dated entries is fine too. What matters is the rules above: dated, raw data first, nothing deleted, mistakes struck through and explained.

> [!NOTE]
> The notebook rules and the report structure here are stable and used across chemistry. Specific institutional rules, such as which ELN software a lab requires, change often; the NIH rule cited was checked on 2026-10-16.

### The lab report

A **lab report** explains one experiment to a reader who was not there. Chemistry reports follow almost the same structure as research papers:

| Section | What goes in it |
|---|---|
| Title | What you measured, and of what. |
| Abstract | 3–5 sentences: aim, method in one line, main result with uncertainty, conclusion. Write it last. |
| Introduction | Why the measurement matters, and the aim. Any equation you will use. |
| Method | Enough detail to repeat it: equipment with resolution, amounts, steps. Past tense. |
| Results | Tables and figures of the data, the calculation once in full, the final result. |
| Discussion | Compare with a reference value. Name the largest source of error and how you know. Suggest one improvement. |
| Conclusion | One or two sentences: the answer to the aim. |
| References | Every source you used, with a link. |

### Tables and figures

Tables and figures are where readers look first. Rules that make them readable:

- Give each one a number and a **caption** that says what it shows: "Table 1. Mass of 10 teaspoons of water, five repeats."
- Put units in the column header, not in every cell. Write it as "mass / g". This reads as "the mass divided by one gram", so the numbers below are pure numbers. NIST SP 811 recommends this style.
- Label both axes of a graph with the quantity and unit, such as "volume / mL".
- Show raw data in a table, and the result in the text.

### Writing a result

A result has three parts: the value, its spread or uncertainty, and the unit. "5.0 mL" is half a result. "5.0 mL; five repeats ranged from 4.8 to 5.2 mL" lets the reader judge how far to trust it. In Lesson 01.5 you will replace the range with a proper standard uncertainty. Give the value only as many digits as the spread allows: if repeats differ in the first decimal place, a second decimal place is noise.

## Worked example

### Fixing a notebook entry

Here is a real-looking first attempt:

```text
teaspoon test
50, 51, 49, 52?, 48
avg 50 so 5 ml
```

What is missing: the date, the aim, what was weighed, units, the scale's resolution, how many teaspoons, what "52?" means, and how 50 became 5 mL.

Here is the same work done properly:

```text
2026-10-16   Page 4   Volume of one teaspoon
Aim: find the volume a kitchen teaspoon holds, using water.
Equipment: kitchen scale (1 g steps); mug; teaspoon (set A); tap water, 22 °C.
Method: weigh empty mug; add 10 level teaspoons of water; weigh again. Empty, dry, repeat 5x.

| repeat | mug empty / g | mug + water / g | water / g |
|   1    |     312       |       362       |    50     |
|   2    |     312       |       363       |    51     |
|   3    |     312       |       361       |    49     |
|   4    |     313       |       ~~364~~ 365 |    52     |   misread display, corrected (TG)
|   5    |     312       |       360       |    48     |
Note: repeat 4, one spoon was heaped. Kept, but flagged.
Mean water mass (10 spoons): 50.0 g. Range 48–52 g.
```

The corrected value in repeat 4 stays readable, with a reason and initials. The odd repeat is flagged, not hidden.

### From notebook to result

Water at 22 °C has a density of about 0.998 g/mL, so the volume of 10 spoons is

$$V = \frac{50.0 \text{ g}}{0.998 \text{ g/mL}} = 50.1 \text{ mL}$$

One teaspoon is $50.1 \text{ mL} / 10 = 5.01$ mL. The repeats spread from 48 to 52 g, which is 4.8 to 5.2 mL per spoon. The first decimal place is already uncertain, so report:

> One level teaspoon holds 5.0 mL of water (five repeats of 10 spoons each; range 4.8–5.2 mL per spoon).

## Hands-on

**What you need:** a bound notebook (any exercise book) and a pen; a kitchen scale; a mug; a teaspoon; tap water; a cloth. **Time:** about 60 minutes.

### Part 1 — Set up the notebook (10 minutes)

1. Number every page in the top corner. The [notebook page template](../../templates/notebook-page.md) shows the fields every entry needs.
2. Leave the first two pages for a table of contents. Add each entry's title and page number as you go.
3. On page 3, write an equipment list for your home kit so far, with resolutions. Add to it in Lesson 01.5.

### Part 2 — Measure a teaspoon (30 minutes)

1. Start a new entry: date, title, aim, equipment with resolution, water temperature (or room temperature).
2. Draw the data table before you measure: repeat, mug empty / g, mug + water / g, water / g.
3. Weigh the empty, dry mug. Write the reading in the table.
4. Add 10 level teaspoons of water. Weigh again. Write it down.
5. Empty and dry the mug. Repeat steps 3–4 until you have 5 repeats.
6. Calculate the water mass for each repeat, the mean, and the range.

### Part 3 — Write a one-page report (20 minutes)

Write a mini report with all eight sections, following the [lab report template](../../templates/lab-report.md). Each section can be one to three sentences. Include one table (raw data, with caption and units in the headers) and your result written as in the worked example. In the Discussion, compare with the common cooking value of 5 mL per teaspoon and name your biggest source of error.

**How you know it worked:** give your notebook page to someone else. They should be able to repeat your measurement without asking you anything. Your result should be roughly 4–7 mL per teaspoon; real spoons vary.

<details><summary>Example Discussion paragraph</summary>

My result, 5.0 mL per teaspoon (range 4.8–5.2 mL), agrees with the cooking value of 5 mL. The largest source of error was how level each spoon was: one heaped spoon in repeat 4 gave the highest mass. The scale's 1 g steps add at most about 0.1 mL per spoon here, because I weighed 10 spoons at once; that is smaller than the spread between repeats. To improve, I would level each spoon with a knife and weigh 20 spoons per repeat.

</details>

## Common mistakes

- **Writing only the calculated value.** "50 g of water" hides two readings. Write both raw readings; the calculation goes next to them.
- **Erasing or using correction fluid.** It looks neater and destroys the record. One line through, new value, reason, initials.
- **No units, or units in every cell.** Put units once, in the column header, as "mass / g".
- **Too many digits in the result.** If repeats differ by 0.4 mL, "5.0125 mL" claims a precision you do not have.
- **Hiding a bad repeat.** Flag it and explain it. Deciding to exclude data is allowed only with a stated reason.
- **Writing the abstract first.** You do not know the result yet. Write it last.

## Key takeaways

- A notebook is dated, permanent and written during the work. Raw data go in first.
- Never erase. Strike through once, write the new value, give a reason and initials.
- A report has title, abstract, introduction, method, results, discussion, conclusion and references.
- Tables and figures need numbers, captions and units in headers or axis labels.
- A result is a value, its spread or uncertainty, and a unit, with no more digits than the spread allows.

## Sources

- [NIH Office of Intramural Research — Electronic Lab Notebooks](https://oir.nih.gov/sourcebook/intramural-program-oversight/electronic-lab-notebooks) (ELN policy pages; checked 2026-10-16).
- [NIH OIR — Best practices for keeping an ELN (trainees), 2024](https://oir.nih.gov/system/files/media/file/2024-07/best_practices-keeping_eln-trainee_0.pdf) (ELN the only approved NIH lab notebook from 30 June 2024).
- [Truman State University Chemistry — The Laboratory Report](https://chemlab.truman.edu/the-laboratory-report) (report sections, following the ACS style).
- [UCLA Chemistry and Biochemistry — Research report guidelines](https://www.chemistry.ucla.edu/undergraduate/undergraduate-research/research-report-guidelines/).
- [NIST SP 811 — Guide for the Use of the International System of Units](https://www.nist.gov/pml/special-publication-811) (labelling table headers and graph axes as quantity / unit).
