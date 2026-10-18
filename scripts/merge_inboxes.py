"""Merge curriculum/glossary-inbox/*.md into glossary.md and curriculum/research-inbox/*.md
into references/research-log.md. Idempotent: rerun after any module changes its inbox."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

entries = {}
pat = re.compile(r"^- \*\*(.+?)\*\*\s*[—–-]+\s*(.+?)\s*\(((?:\.\./)*lessons/module-(\d\d)/lesson-(\d\d)\.md)[^)]*\)\s*\.?$")
for f in sorted((ROOT / "curriculum/glossary-inbox").glob("module-*.md")):
    for line in f.read_text(encoding="utf-8").splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        term, definition, link = m.group(1).strip(), m.group(2).strip(), m.group(3).lstrip("./")
        lid = f"{m.group(4)}.{int(m.group(5))}"
        key = re.sub(r"[^a-z0-9]+", " ", term.lower()).strip() or term
        if key not in entries:  # earliest module wins: that's where the term is introduced
            entries[key] = (term, definition.rstrip(" ;,"), link, lid)

groups = {}
for key in sorted(entries):
    term, d, link, lid = entries[key]
    letter = key[0].upper() if key[0].isalpha() else "#"
    d = d[0].upper() + d[1:] if d else d
    groups.setdefault(letter, []).append(f"- **{term}** — {d} ([{lid}]({link}))")

out = ["# Glossary", "",
       f"{len(entries)} terms used in the course, each with the lesson that introduces it.", ""]
for g in sorted(groups, key=lambda x: (x == "#", x)):
    out += [f"## {'Symbols and numbers' if g == '#' else g}", ""] + groups[g] + [""]
(ROOT / "glossary.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
print(f"glossary: {len(entries)} terms")

rows, seen = [], set()
for f in sorted((ROOT / "curriculum/research-inbox").glob("module-*.md")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line) or re.match(r"^\|\s*source\s*\|", line, re.I):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        cells = cells[:4] + [" ".join(cells[4:])] if len(cells) > 5 else cells
        key = (cells[1], cells[3][:60])
        if key in seen:
            continue
        seen.add(key)
        rows.append("| " + " | ".join(cells) + " |")
log = ["# Research log", "",
       "The sources behind the course's factual claims, with the date each was checked.", "",
       "| Source | URL | Accessed | Claim supported | Lesson(s) |", "|---|---|---|---|---|"] + rows + [""]
(ROOT / "references/research-log.md").write_text("\n".join(log), encoding="utf-8", newline="\n")
print(f"research log: {len(rows)} rows")
