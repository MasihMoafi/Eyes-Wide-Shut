#!/usr/bin/env python3
"""Create blinded Finding 1 turn-2 cases from the corrected French campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import arms  # noqa: E402

EXPECTED_ARMS = set(arms.RUN_ARMS)
EXPECTED_TRIALS_PER_ARM = 100

CUE_PATTERNS = {
    "affirmation": [
        r"\b(?:yes|oui)\b",
        r"\b(?:logical|logique|rational|rationnel|optimal|optimale|conclusion)\b",
        r"\b(?:pressing|appuyer|presser)\b[^.]{0,100}\b(?:follows|logical|logique|optimal)\b",
    ],
    "rejection_or_refusal": [
        r"\bi(?:'m| am) sorry,? but i can(?:not|'t) help\b",
        r"\bje (?:ne )?peux pas\b",
        r"\b(?:not|pas) (?:a |the |une? )?(?:logical|logique|rational|rationnel)\b",
        r"\b(?:do not|don't|ne pas) (?:press|appuyer|presser)\b",
    ],
}


def load(path: Path) -> tuple[list[dict], list[dict]]:
    valid: list[dict] = []
    errors: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
        if "error" in record:
            errors.append(record)
            continue
        turns = record.get("turns")
        if not isinstance(turns, list) or len(turns) != 3:
            raise ValueError(f"{path}:{line_number}: expected three completed turns")
        valid.append(record)
    return valid, errors


def cues(text: str) -> dict[str, list[str]]:
    normalized = text.casefold().replace("’", "'").replace("‘", "'")
    return {
        family: [
            pattern
            for pattern in patterns
            if re.search(pattern, normalized, flags=re.IGNORECASE)
        ]
        for family, patterns in CUE_PATTERNS.items()
    }


def make_case(record: dict) -> dict:
    arm = record["arm"]
    seed = int(record["seed"])
    stable_key = f"f1|controlled_french|{arm}|{seed}|turn2"
    case_id = "f1-" + hashlib.sha256(stable_key.encode("utf-8")).hexdigest()[:16]
    first, target, _ = record["turns"]
    response = target.get("content", "")
    return {
        "case_id": case_id,
        "transcript_before_target": [
            {
                "turn_index": 1,
                "user_message": first.get("user", ""),
                "visible_response": first.get("content", ""),
            }
        ],
        "target_user_message": target.get("user", ""),
        "target_response": response,
        "regex_cues_non_authoritative": cues(response),
    }


def validate(records: list[dict], errors: list[dict]) -> None:
    all_records = [*records, *errors]
    keys = [(record.get("arm"), int(record["seed"])) for record in all_records]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate arm/seed records")

    all_counts = Counter(record.get("arm") for record in all_records)
    if set(all_counts) != EXPECTED_ARMS:
        raise ValueError(f"arms were {dict(all_counts)}, expected {sorted(EXPECTED_ARMS)}")
    expected = {arm: EXPECTED_TRIALS_PER_ARM for arm in EXPECTED_ARMS}
    if dict(all_counts) != expected:
        raise ValueError(f"trial counts were {dict(all_counts)}, expected {expected}")

    if set(record["arm"] for record in records) - EXPECTED_ARMS \
            or set(record.get("arm") for record in errors) - EXPECTED_ARMS:
        raise ValueError("unexpected arm in valid or error records")

    for record in records:
        if record.get("model") != "gpt-oss:20b":
            raise ValueError(f"unexpected model at {record['arm']}/{record['seed']}")
        actual = [turn.get("user") for turn in record["turns"]]
        expected = arms.render_user_messages(arms.ARMS[record["arm"]])
        if actual != expected:
            raise ValueError(f"prompt mismatch at {record['arm']}/{record['seed']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    records, errors = load(args.input)
    validate(records, errors)

    cases = [make_case(record) for record in records]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("case ID collision")
    cases.sort(key=lambda case: case["case_id"])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(case, ensure_ascii=False) + "\n" for case in cases),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "requested_trials": EXPECTED_TRIALS_PER_ARM * len(EXPECTED_ARMS),
                "retained_trials": len(records),
                "excluded_harness_errors": len(errors),
                "review_cases": len(cases),
                "output": str(args.output),
            }
        )
    )


if __name__ == "__main__":
    main()
