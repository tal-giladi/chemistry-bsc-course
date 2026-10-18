"""List quiz questions whose correct option is the longest. Usage: py scripts/quiz_bias.py [first_module last_module]"""
import glob, re, sys, yaml
lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 99)
n = biased = 0
for f in sorted(glob.glob("lessons/module-*/*.quiz.yaml") + glob.glob("assessments/module-*-quiz.quiz.yaml")):
    m = int(re.search(r"module-(\d\d)", f).group(1))
    if not lo <= m <= hi:
        continue
    for q in yaml.safe_load(open(f, encoding="utf-8")):
        n += 1
        ls = [len(o) for o in q["options"]]
        c = q["correct"]
        if ls[c] == max(ls):
            biased += 1
            print(f"{f.replace(chr(92), '/')} {q['id']}: correct {ls[c]} vs next {sorted(ls)[-2]}")
print(f"{biased}/{n} = {100 * biased / max(n, 1):.1f}% correct option is the longest")
