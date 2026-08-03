"""Finding 5 role-by-tool-schema factorial: full campaign.

Imports the smoke-tested protocol from a private, immutable Kaggle dataset.
Only the paired sample size and output filenames differ from the smoke run.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib


INPUT_ROOT = pathlib.Path("/kaggle/input")
HARNESS_CANDIDATES = sorted(INPUT_ROOT.rglob("kaggle_smoke.py"))
HARNESS_CANDIDATES = [
    path for path in HARNESS_CANDIDATES
    if "finding5-control-harness" in str(path.parent)
]
if len(HARNESS_CANDIDATES) != 1:
    raise FileNotFoundError(
        f"Expected one mounted Finding 5 harness; found {HARNESS_CANDIDATES}"
    )

spec = importlib.util.spec_from_file_location("finding5_smoke_harness", HARNESS_CANDIDATES[0])
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load harness from {HARNESS_CANDIDATES[0]}")
experiment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiment)

experiment.N_SEEDS = 30
experiment.OUT_PATH = experiment.WORK / "finding5_controls_full.jsonl"
experiment.ENV_PATH = experiment.WORK / "finding5_controls_environment.json"


def validate_full() -> None:
    records = [
        json.loads(line)
        for line in experiment.OUT_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected = {
        (role_name, schema_name, seed)
        for role_name in experiment.ROLE_NAMES
        for schema_name in experiment.SCHEMA_NAMES
        for seed in range(experiment.N_SEEDS)
    }
    actual = {
        (record["role_factor"], record["schema_factor"], int(record["seed"]))
        for record in records
        if "error" not in record
    }
    assert len(records) == len(expected) and actual == expected
    assert not [record for record in records if "error" in record]

    for role_name in experiment.ROLE_NAMES:
        for seed in range(experiment.N_SEEDS):
            pair = [
                record
                for record in records
                if record["role_factor"] == role_name and int(record["seed"]) == seed
            ]
            assert len(pair) == 2
            assert pair[0]["priming"] == pair[1]["priming"]
            assert pair[0]["attack"]["user"] == pair[1]["attack"]["user"]
            assert {record["schema_call_order"] for record in pair} == {0, 1}
            for record in pair:
                assert isinstance(record["called_execute_python_code"], bool)
                if record["called_execute_python_code"]:
                    assert "execute_python_code" in record["tool_names_called"]

    print(
        f"FULL STRUCTURE PASSED: {len(records)} records, "
        f"{experiment.N_SEEDS} seeds per arm, 0 errors"
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
