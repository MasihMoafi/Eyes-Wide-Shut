"""
Finding 1 - results analysis.

Reports, for each arm: successes / trials, the proportion, and a 95% Wilson
confidence interval. Wilson rather than the textbook normal interval because
these rates sit near 0 and 1, where the normal interval misbehaves badly (it
gives a zero-width interval for 10/10, which is obviously wrong).

Then runs two-sided Fisher exact tests on the comparisons the paper makes.
Fisher rather than chi-square because the counts are small.
"""

import json
from math import comb, sqrt


def wilson(successes, trials, z=1.96):
    """95% Wilson score interval for a binomial proportion."""
    if trials == 0:
        return (0.0, 0.0)
    p = successes / trials
    d = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / d
    half = z * sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def fisher_exact(a, b, c, d):
    """Two-sided Fisher exact test on the 2x2 table [[a,b],[c,d]]."""
    n = a + b + c + d
    if n == 0:
        return 1.0

    def prob(x):
        return comb(a + b, x) * comb(c + d, a + c - x) / comb(n, a + c)

    lo = max(0, a + c - (c + d))
    hi = min(a + b, a + c)
    observed = prob(a)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1)
                        if prob(x) <= observed + 1e-12))


def load(path):
    """Read the JSONL checkpoint, dropping errored runs."""
    records = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "error" not in rec:
                records.append(rec)
    return records


def tally(records):
    """arm -> (successes, trials), de-duplicated on (arm, seed)."""
    seen = {}
    for rec in records:
        seen[(rec["arm"], rec["seed"])] = bool(rec["success"])
    counts = {}
    for (arm, _seed), ok in seen.items():
        s, t = counts.get(arm, (0, 0))
        counts[arm] = (s + int(ok), t + 1)
    return counts


def rates_table(counts, arms):
    rows = []
    for name, (s, t) in sorted(counts.items()):
        lo, hi = wilson(s, t)
        rows.append({
            "arm": name,
            "label": arms[name]["label"] if name in arms else name,
            "group": arms[name]["group"] if name in arms else "?",
            "successes": s, "trials": t,
            "rate": s / t if t else 0.0,
            "ci_low": lo, "ci_high": hi,
        })
    rows.sort(key=lambda r: (r["group"] != "core", -r["rate"]))
    return rows


def compare(counts, left, right):
    """Fisher exact between two arms, as a printable record."""
    ls, lt = counts.get(left, (0, 0))
    rs, rt = counts.get(right, (0, 0))
    return {
        "left": left, "right": right,
        "left_n": f"{ls}/{lt}", "right_n": f"{rs}/{rt}",
        "p": fisher_exact(ls, lt - ls, rs, rt - rs),
    }


def print_report(path, arms, comparisons):
    records = load(path)
    counts = tally(records)

    print(f"{len(records)} completed runs\n")
    print(f"{'arm':<20} {'condition':<42} {'rate':>10}  95% CI")
    print("-" * 92)
    group = None
    for row in rates_table(counts, arms):
        if row["group"] != group:
            group = row["group"]
            print(f"\n[{group}]")
        print(
            f"{row['arm']:<20} {row['label']:<42} "
            f"{row['successes']:>3}/{row['trials']:<3} "
            f"{row['rate']*100:>5.0f}%  "
            f"[{row['ci_low']*100:.0f}%, {row['ci_high']*100:.0f}%]"
        )

    print("\n\nComparisons (two-sided Fisher exact)")
    print("-" * 92)
    for left, right, question in comparisons:
        result = compare(counts, left, right)
        verdict = "significant" if result["p"] < 0.05 else "not distinguishable"
        print(
            f"{question:<46} {result['left_n']:>7} vs {result['right_n']:<7} "
            f"p = {result['p']:.4f}   {verdict}"
        )
    return counts
