"""Option-length rank balance. Each question gets a target rank for its correct option
(0 = longest ... 3 = shortest), assigned round-robin per file so ranks are spread ~25% each.
Usage: py scripts/quiz_rank.py [first last] [--list]   (lists questions whose rank is off target)"""
import glob, re, sys, yaml, collections
args = [a for a in sys.argv[1:] if not a.startswith("--")]
lo, hi = (int(args[0]), int(args[1])) if len(args) > 1 else (1, 99)
show = "--list" in sys.argv
dist, off, n = collections.Counter(), 0, 0
for f in sorted(glob.glob("lessons/module-*/*.quiz.yaml") + glob.glob("assessments/module-*-quiz.quiz.yaml")):
    m = int(re.search(r"module-(\d\d)", f).group(1))
    if not lo <= m <= hi:
        continue
    seed = sum(map(ord, f.replace("\\", "/"))) % 4
    for i, q in enumerate(yaml.safe_load(open(f, encoding="utf-8"))):
        n += 1
        ls = [len(o) for o in q["options"]]
        c = ls[q["correct"]]
        rank = sum(1 for x in ls if x > c)
        dist[rank] += 1
        target = (seed + i) % 4
        if rank != target:
            off += 1
            if show:
                print(f"{f.replace(chr(92), '/')} {q['id']}: rank {rank} -> target {target}; lengths {ls}, correct index {q['correct']}")
print(f"{n} questions; rank of correct option (0=longest): " + ", ".join(f"{k}: {100*v/max(n,1):.0f}%" for k, v in sorted(dist.items())) + f"; off target: {off}")
