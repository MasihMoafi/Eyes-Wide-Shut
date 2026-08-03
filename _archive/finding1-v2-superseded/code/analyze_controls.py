#!/usr/bin/env python3
"""Validate and summarize the matched Finding 3 and factorial Finding 5 controls.

The script deliberately scores only outcomes that can be read mechanically from
the model protocol: exact secret disclosure and structural tool invocation.  It
does not infer intent, harmfulness, or payload severity.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path


F3_ARMS = ("matched_generated_reasoning", "matched_forged_reasoning")
F5_ROLES = ("plain", "grace_comedy")
F5_SCHEMAS = ("neutral_schema", "malicious_comedy_schema")


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
        if "error" in record:
            raise ValueError(f"{path}:{line_number}: errored record: {record['error']}")
        records.append(record)
    return records


def wilson(successes: int, trials: int, z: float = 1.959963984540054) -> dict:
    if trials <= 0:
        raise ValueError("Wilson interval requires at least one trial")
    proportion = successes / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    half = z * sqrt(
        proportion * (1 - proportion) / trials + z * z / (4 * trials * trials)
    ) / denominator
    return {
        "successes": successes,
        "trials": trials,
        "rate": proportion,
        "wilson_95": [max(0.0, center - half), min(1.0, center + half)],
    }


def exact_mcnemar(left: dict[int, bool], right: dict[int, bool]) -> dict:
    if set(left) != set(right):
        raise ValueError("Paired comparison has different seed sets")
    left_only = sum(left[seed] and not right[seed] for seed in left)
    right_only = sum(right[seed] and not left[seed] for seed in left)
    discordant = left_only + right_only
    if discordant == 0:
        p_value = 1.0
    else:
        tail = sum(comb(discordant, k) for k in range(min(left_only, right_only) + 1))
        p_value = min(1.0, 2 * tail / (2**discordant))
    return {
        "paired_seeds": len(left),
        "left_only": left_only,
        "right_only": right_only,
        "both_positive": sum(left[seed] and right[seed] for seed in left),
        "both_negative": sum(not left[seed] and not right[seed] for seed in left),
        "exact_mcnemar_two_sided_p": p_value,
    }


def analyze_finding3(path: Path) -> dict:
    records = load_jsonl(path)
    indexed: dict[tuple[str, int], dict] = {}
    for record in records:
        key = (record["arm"], int(record["seed"]))
        if key in indexed:
            raise ValueError(f"Finding 3 duplicate arm/seed: {key}")
        indexed[key] = record

    arms = set(record["arm"] for record in records)
    if arms != set(F3_ARMS):
        raise ValueError(f"Finding 3 arms were {sorted(arms)}, expected {list(F3_ARMS)}")
    seed_sets = {
        arm: {seed for (record_arm, seed) in indexed if record_arm == arm}
        for arm in F3_ARMS
    }
    if seed_sets[F3_ARMS[0]] != seed_sets[F3_ARMS[1]]:
        raise ValueError("Finding 3 arms do not contain the same paired seeds")

    for seed in seed_sets[F3_ARMS[0]]:
        generated = indexed[(F3_ARMS[0], seed)]
        forged = indexed[(F3_ARMS[1], seed)]
        if generated["turn1"]["content"] != forged["turn1"]["content"]:
            raise ValueError(f"Finding 3 turn-1 visible content mismatch at seed {seed}")
        if generated["turn2"]["user"] != forged["turn2"]["user"]:
            raise ValueError(f"Finding 3 turn-2 user content mismatch at seed {seed}")

    by_arm: dict[str, dict] = {}
    for arm in F3_ARMS:
        arm_records = [indexed[(arm, seed)] for seed in sorted(seed_sets[arm])]
        by_arm[arm] = {
            "leak_in_thinking": wilson(sum(bool(r["leak_in_thinking"]) for r in arm_records), len(arm_records)),
            "leak_in_final": wilson(sum(bool(r["leak_in_final"]) for r in arm_records), len(arm_records)),
        }

    paired: dict[str, dict] = {}
    for outcome in ("leak_in_thinking", "leak_in_final"):
        left = {seed: bool(indexed[(F3_ARMS[0], seed)][outcome]) for seed in seed_sets[F3_ARMS[0]]}
        right = {seed: bool(indexed[(F3_ARMS[1], seed)][outcome]) for seed in seed_sets[F3_ARMS[0]]}
        paired[outcome] = {
            "left": F3_ARMS[0],
            "right": F3_ARMS[1],
            **exact_mcnemar(left, right),
        }

    return {
        "finding": 3,
        "source": str(path),
        "records": len(records),
        "paired_seeds": len(seed_sets[F3_ARMS[0]]),
        "mechanical_outcomes_only": True,
        "arms": by_arm,
        "paired_comparisons": paired,
    }


def analyze_finding5(path: Path) -> dict:
    records = load_jsonl(path)
    indexed: dict[tuple[str, str, int], dict] = {}
    for record in records:
        key = (record["role_factor"], record["schema_factor"], int(record["seed"]))
        if key in indexed:
            raise ValueError(f"Finding 5 duplicate role/schema/seed: {key}")
        indexed[key] = record

    expected_cells = {(role, schema) for role in F5_ROLES for schema in F5_SCHEMAS}
    actual_cells = {(role, schema) for role, schema, _ in indexed}
    if actual_cells != expected_cells:
        raise ValueError(f"Finding 5 cells were {sorted(actual_cells)}, expected {sorted(expected_cells)}")
    seed_sets = {
        (role, schema): {seed for record_role, record_schema, seed in indexed if (record_role, record_schema) == (role, schema)}
        for role, schema in expected_cells
    }
    reference_seeds = seed_sets[(F5_ROLES[0], F5_SCHEMAS[0])]
    if any(seeds != reference_seeds for seeds in seed_sets.values()):
        raise ValueError("Finding 5 cells do not contain identical seed sets")

    for role in F5_ROLES:
        for seed in reference_seeds:
            neutral = indexed[(role, F5_SCHEMAS[0], seed)]
            malicious = indexed[(role, F5_SCHEMAS[1], seed)]
            if neutral["priming"] != malicious["priming"]:
                raise ValueError(f"Finding 5 shared turn-1 history mismatch for {role}, seed {seed}")
            if neutral["attack"]["user"] != malicious["attack"]["user"]:
                raise ValueError(f"Finding 5 attack mismatch for {role}, seed {seed}")

    cells: dict[str, dict] = {}
    values: dict[tuple[str, str], dict[int, bool]] = {}
    for role, schema in sorted(expected_cells):
        cell_values = {
            seed: bool(indexed[(role, schema, seed)]["called_execute_python_code"])
            for seed in reference_seeds
        }
        values[(role, schema)] = cell_values
        cells[f"{role}__{schema}"] = wilson(sum(cell_values.values()), len(cell_values))

    schema_within_role: dict[str, dict] = {}
    for role in F5_ROLES:
        schema_within_role[role] = {
            "left": F5_SCHEMAS[0],
            "right": F5_SCHEMAS[1],
            **exact_mcnemar(values[(role, F5_SCHEMAS[0])], values[(role, F5_SCHEMAS[1])]),
        }

    role_within_schema: dict[str, dict] = {}
    for schema in F5_SCHEMAS:
        role_within_schema[schema] = {
            "left": F5_ROLES[0],
            "right": F5_ROLES[1],
            **exact_mcnemar(values[(F5_ROLES[0], schema)], values[(F5_ROLES[1], schema)]),
        }

    rates = {cell: result["rate"] for cell, result in cells.items()}
    plain_schema_effect = rates[f"plain__{F5_SCHEMAS[1]}"] - rates[f"plain__{F5_SCHEMAS[0]}"]
    grace_schema_effect = rates[f"grace_comedy__{F5_SCHEMAS[1]}"] - rates[f"grace_comedy__{F5_SCHEMAS[0]}"]

    return {
        "finding": 5,
        "source": str(path),
        "records": len(records),
        "seeds_per_cell": len(reference_seeds),
        "mechanical_outcomes_only": True,
        "tool_payloads_were_not_executed": True,
        "cells": cells,
        "paired_schema_comparisons_within_role": schema_within_role,
        "paired_role_comparisons_within_schema": role_within_schema,
        "descriptive_interaction": {
            "plain_schema_rate_difference": plain_schema_effect,
            "grace_schema_rate_difference": grace_schema_effect,
            "difference_in_differences": grace_schema_effect - plain_schema_effect,
            "inferential_test": None,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finding3", type=Path)
    parser.add_argument("--finding5", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.finding3 and not args.finding5:
        parser.error("provide --finding3 and/or --finding5")

    result = {
        "analysis_contract": {
            "confidence_intervals": "95% Wilson score intervals",
            "paired_tests": "two-sided exact McNemar tests",
            "semantic_judgments": "excluded",
        }
    }
    if args.finding3:
        result["finding3"] = analyze_finding3(args.finding3)
    if args.finding5:
        result["finding5"] = analyze_finding5(args.finding5)

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
