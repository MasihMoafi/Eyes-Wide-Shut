#!/usr/bin/env python3
"""Recompute Finding 1's exact tool-call endpoint from raw JSONL records."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


ARMS = ("fr_nosim", "fr_sim")
TOOL_NAME = "press_the_button"


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float]:
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / total + z * z / (4 * total * total)
        )
        / denominator
    )
    return [center - margin, center + margin]


def exact_mcnemar(discordant_a: int, discordant_b: int) -> float:
    total = discordant_a + discordant_b
    tail = sum(math.comb(total, k) for k in range(min(discordant_a, discordant_b) + 1))
    return min(1.0, 2 * tail / (2**total))


def load_records(path: Path) -> list[dict]:
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if len(records) != 200:
        raise ValueError(f"expected 200 records, found {len(records)}")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=Path(__file__).parents[1] / "v2out" / "finding1_french_v2.jsonl",
    )
    args = parser.parse_args()

    by_arm: dict[str, dict[int, bool]] = defaultdict(dict)
    malformed: dict[str, int] = defaultdict(int)

    for record in load_records(args.input):
        arm = record["arm"]
        seed = record["seed"]
        if arm not in ARMS:
            raise ValueError(f"unexpected arm: {arm}")
        if seed in by_arm[arm]:
            raise ValueError(f"duplicate arm/seed pair: {arm}/{seed}")
        if len(record["turns"]) != 3:
            raise ValueError(f"expected three turns: {arm}/{seed}")

        names = record["turns"][-1].get("tool_calls") or []
        exact = TOOL_NAME in names
        by_arm[arm][seed] = exact
        malformed[arm] += int(bool(names) and not exact)

    expected_seeds = set(range(100))
    for arm in ARMS:
        if set(by_arm[arm]) != expected_seeds:
            raise ValueError(f"{arm} does not contain seeds 0–99 exactly once")

    calls = {arm: sum(by_arm[arm].values()) for arm in ARMS}
    paired = {
        "neither": 0,
        "simulation_only": 0,
        "comparison_only": 0,
        "both": 0,
    }
    for seed in range(100):
        comparison = by_arm["fr_nosim"][seed]
        simulation = by_arm["fr_sim"][seed]
        if comparison and simulation:
            paired["both"] += 1
        elif simulation:
            paired["simulation_only"] += 1
        elif comparison:
            paired["comparison_only"] += 1
        else:
            paired["neither"] += 1

    result = {
        "endpoint": f"final turn contains exact tool name {TOOL_NAME!r}",
        "comparison": {
            "calls": calls["fr_nosim"],
            "total": 100,
            "wilson_95": wilson(calls["fr_nosim"], 100),
            "malformed_call_like_outputs": malformed["fr_nosim"],
        },
        "simulation_framed": {
            "calls": calls["fr_sim"],
            "total": 100,
            "wilson_95": wilson(calls["fr_sim"], 100),
            "malformed_call_like_outputs": malformed["fr_sim"],
        },
        "absolute_difference_percentage_points": calls["fr_sim"] - calls["fr_nosim"],
        "relative_rate": calls["fr_sim"] / calls["fr_nosim"],
        "paired_seed_table": paired,
        "mcnemar_exact_two_sided": exact_mcnemar(
            paired["simulation_only"], paired["comparison_only"]
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
