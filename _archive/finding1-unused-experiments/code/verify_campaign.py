#!/usr/bin/env python3
"""Validate a downloaded Finding 1 controlled-French campaign."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arms  # noqa: E402


TOOL_NAME = "press_the_button"
EXPECTED_TRIALS_PER_ARM = 100


def load(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()

    arms.arms_are_matched()
    records = load(args.input)
    expected_keys = {
        (arm_name, seed)
        for arm_name in arms.RUN_ARMS
        for seed in range(EXPECTED_TRIALS_PER_ARM)
    }
    actual_keys = {(record.get("arm"), int(record["seed"])) for record in records}
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        raise ValueError(f"campaign keys mismatch; missing={missing[:5]}, extra={extra[:5]}")

    valid = [record for record in records if "error" not in record]
    errors = [record for record in records if "error" in record]
    if len({(record["arm"], int(record["seed"])) for record in records}) != len(records):
        raise ValueError("duplicate arm/seed records")

    calls = Counter()
    valid_counts = Counter()
    error_counts = Counter(record["arm"] for record in errors)
    for record in valid:
        arm_name = record["arm"]
        if record.get("model") != "gpt-oss:20b":
            raise ValueError(f"unexpected model at {arm_name}/{record['seed']}")
        turns = record.get("turns")
        if not isinstance(turns, list) or len(turns) != 3:
            raise ValueError(f"expected three turns at {arm_name}/{record['seed']}")
        if [turn.get("turn") for turn in turns] != [1, 2, 3]:
            raise ValueError(f"turn numbering mismatch at {arm_name}/{record['seed']}")
        expected_messages = arms.render_user_messages(arms.ARMS[arm_name])
        actual_messages = [turn.get("user") for turn in turns]
        if actual_messages != expected_messages:
            raise ValueError(f"prompt mismatch at {arm_name}/{record['seed']}")
        names = turns[-1].get("tool_calls") or []
        calls[arm_name] += int(TOOL_NAME in names)
        valid_counts[arm_name] += 1

    print(
        json.dumps(
            {
                "campaign_id": arms.CAMPAIGN_ID,
                "requested_trials": len(expected_keys),
                "retained_trials": len(valid),
                "errors": len(errors),
                "errors_by_arm": dict(sorted(error_counts.items())),
                "exact_tool_calls": {
                    arm_name: {
                        "presses": calls[arm_name],
                        "n": valid_counts[arm_name],
                    }
                    for arm_name in arms.RUN_ARMS
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
