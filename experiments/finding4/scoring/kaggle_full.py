"""Finding 4 control experiment: preregistered 2x2 factorial, full campaign.

This module imports the smoke-tested protocol without changing prompts, turn
order, model settings, or runtime setup.  It changes only the sample size and
output filenames: 30 seeded trials in each of four arms (120 total).
"""

from __future__ import annotations

import json
import pathlib
import sys

# Kaggle uploads only the metadata-selected code file.  The smoke-tested
# protocol is therefore mounted as a private dataset rather than assumed to
# be a sibling module in /kaggle/src.
HARNESS_ROOT = pathlib.Path("/kaggle/input/eyes-wide-shut-finding4-harness")
if not (HARNESS_ROOT / "kaggle_smoke.py").exists():
    raise FileNotFoundError(f"smoke-tested harness not mounted at {HARNESS_ROOT}")
sys.path.insert(0, str(HARNESS_ROOT))
import kaggle_smoke as experiment


experiment.N_PER_ARM = 30
experiment.OUT_PATH = experiment.WORK / "finding4_controls_full.jsonl"
experiment.ENV_PATH = experiment.WORK / "finding4_controls_environment.json"


def validate_full() -> None:
    records = [
        json.loads(line)
        for line in experiment.OUT_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected = len(experiment.ARMS) * experiment.N_PER_ARM
    assert len(records) == expected, f"expected {expected} records; found {len(records)}"
    errors = [record for record in records if "error" in record]
    assert not errors, json.dumps(errors, indent=2)
    expected_keys = {
        (arm_name, seed)
        for arm_name in experiment.ARMS
        for seed in range(experiment.N_PER_ARM)
    }
    actual_keys = {(record["arm"], int(record["seed"])) for record in records}
    assert actual_keys == expected_keys
    for record in records:
        assert len(record["turns"]) == experiment.MAX_TURNS
        assert record["revelation_turn"]["index"] == experiment.SUPERVISOR_REVELATION_INDEX
        assert record["followup_turn"]["index"] == experiment.SUPERVISOR_FOLLOWUP_INDEX
    print(
        f"FULL STRUCTURE PASSED: {len(records)} trials, "
        f"{len(experiment.ARMS)} arms, {experiment.MAX_TURNS} turns each, 0 errors"
    )


def main() -> None:
    experiment.WORK.mkdir(parents=True, exist_ok=True)
    if experiment.OUT_PATH.exists():
        experiment.OUT_PATH.unlink()
    ports, _servers = experiment.setup_environment()
    experiment.ENV_PATH.write_text(
        json.dumps(
            experiment.environment_record(ports),
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    experiment.run_campaign(ports)
    validate_full()


if __name__ == "__main__":
    main()
