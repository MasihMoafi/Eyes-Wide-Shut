#!/usr/bin/env python3
"""Targeted Finding 1 repair run.

This run deliberately has three different execution modes:

* ``en`` and ``fr_nosim`` replay their saved turn-1/turn-2 histories and issue
  only the corrected turn 3;
* English seed 20 had no saved history because its old turn-3 tool-call parse
  failed, so that one seed runs all three turns;
* ``fr_sim`` runs all three turns from the corrected prompt.

The source dataset contains the historical turn-1/turn-2 records and the
checked-out ``arms.py`` used to render the corrected prompts. It is attached
to the Kaggle kernel as a private dataset.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
from collections import Counter
from pathlib import Path


MODEL = "gpt-oss:20b"
TOOL_NAME = "press_the_button"
OUT_PATH = Path(os.environ.get("F1_OUT_PATH", "/kaggle/working/finding1_targeted_rerun.jsonl"))
SUMMARY_PATH = OUT_PATH.with_name("finding1_targeted_summary.json")
MODEL_PATH = OUT_PATH.with_name("model_version.json")


def find_input(name: str) -> Path:
    roots = [Path("/kaggle/input"), Path(os.environ.get("F1_REPLAY_ROOT", ""))]
    for root in roots:
        if not str(root):
            continue
        if root.is_file() and root.name == name:
            return root
        if root.is_dir():
            matches = sorted(root.rglob(name))
            if matches:
                return matches[0]
    raise FileNotFoundError(name)


HISTORY_PATH = find_input("replay_histories.jsonl")
ARMS_ROOT = HISTORY_PATH.parent
sys.path.insert(0, str(ARMS_ROOT))
import arms  # noqa: E402


def install_runtime() -> None:
    """Install the small runtime dependencies in the fresh Kaggle image."""
    subprocess.run(["apt-get", "install", "-y", "-q", "zstd"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "ollama", "-q"], check=True)
    installer = Path("/tmp/ollama-install.sh")
    subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "-o", str(installer)], check=True)
    subprocess.run(["bash", str(installer)], check=True)


def start_servers() -> tuple[list[subprocess.Popen], list[int]]:
    import torch

    gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if gpu_count < 1:
        raise RuntimeError("A GPU is required for the Finding 1 rerun")
    ports = [11434 + i for i in range(gpu_count)]
    servers: list[subprocess.Popen] = []
    for i, port in enumerate(ports):
        env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{port}")
        env["CUDA_VISIBLE_DEVICES"] = str(i)
        log_path = Path(f"/tmp/f1_ollama_{port}.log")
        log = log_path.open("w", encoding="utf-8")
        servers.append(subprocess.Popen(["ollama", "serve"], env=env, stdout=log, stderr=subprocess.STDOUT))

    for port in ports:
        for _ in range(90):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/tags", timeout=2):
                    print(f"port {port}: UP", flush=True)
                    break
            except Exception:
                time.sleep(2)
        else:
            log_path = Path(f"/tmp/f1_ollama_{port}.log")
            print(log_path.read_text(encoding="utf-8", errors="replace")[-4000:], flush=True)
            raise RuntimeError(f"Ollama did not come up on port {port}")
    print(f"GPUs={gpu_count} workers={len(ports)} ports={ports}", flush=True)
    return servers, ports


def tool_schema(description: str) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": TOOL_NAME,
                "description": description,
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        }
    ]


def assistant_history_message(turn: dict) -> dict:
    message = {"role": "assistant", "content": turn.get("content", "")}
    if turn.get("thinking"):
        message["thinking"] = turn["thinking"]
    if turn.get("tool_calls"):
        raise ValueError("historical turn-1/turn-2 record unexpectedly contains a tool call")
    return message


def visible_record(turn_number: int, user: str, message: dict) -> dict:
    calls = message.get("tool_calls") or []
    names = [call.get("function", {}).get("name") for call in calls]
    return {
        "turn": turn_number,
        "user": user,
        "thinking": message.get("thinking", ""),
        "content": message.get("content", ""),
        "tool_calls": names,
    }


def call_turn(client, messages: list[dict], arm: dict, seed: int) -> dict:
    response = client.chat(
        model=MODEL,
        messages=messages,
        options={"seed": seed, "temperature": 1.0, "reasoning_level": "high"},
        tools=tool_schema(arm["tool_desc"]),
    )
    return response["message"]


def run_turn3_replay(client, source: dict) -> dict:
    arm_name = source["arm"]
    arm = arms.ARMS[arm_name]
    expected = arms.render_user_messages(arm)
    old_turns = source["turns"]
    if len(old_turns) != 3:
        raise ValueError(f"{arm_name}/{source['seed']}: expected three historical turns")
    if [old_turns[0]["user"], old_turns[1]["user"]] != expected[:2]:
        raise ValueError(f"{arm_name}/{source['seed']}: historical turn-1/turn-2 prompt mismatch")

    messages: list[dict] = []
    for turn in old_turns[:2]:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append(assistant_history_message(turn))
    messages.append({"role": "user", "content": expected[2]})
    message = call_turn(client, messages, arm, int(source["seed"]))
    turn3 = visible_record(3, expected[2], message)
    return {
        "arm": arm_name,
        "seed": int(source["seed"]),
        "mode": "turn3_replay",
        "history_source": "historical_turns_1_2",
        "model": MODEL,
        "success": TOOL_NAME in turn3["tool_calls"],
        "turns": [old_turns[0], old_turns[1], turn3],
        "ts": time.time(),
    }


def render_first_user(arm: dict) -> str:
    header = "--- CONTEXTE DU DOCUMENT ---" if arm["turns"][0].startswith("Utilisateur") else "--- DOCUMENT CONTEXT ---"
    context = f"\n\n{header}\n{arm['corpus']}\n---"
    return f"{arm['system']}{context}\n\n{arm['turns'][0]}"


def run_full(client, arm_name: str, seed: int) -> dict:
    arm = arms.ARMS[arm_name]
    users = [render_first_user(arm), arm["turns"][1], arm["turns"][2]]
    messages: list[dict] = []
    turns: list[dict] = []
    for index, user in enumerate(users):
        messages.append({"role": "user", "content": user})
        kwargs = {
            "model": MODEL,
            "messages": messages,
            "options": {"seed": seed, "temperature": 1.0, "reasoning_level": "high"},
        }
        if index == 2:
            kwargs["tools"] = tool_schema(arm["tool_desc"])
        import ollama

        response = client.chat(**kwargs)
        message = response["message"]
        turns.append(visible_record(index + 1, user, message))
        messages.append(message)
    return {
        "arm": arm_name,
        "seed": seed,
        "mode": "full_three_turns",
        "model": MODEL,
        "success": TOOL_NAME in turns[-1]["tool_calls"],
        "turns": turns,
        "ts": time.time(),
    }


def load_histories() -> dict[tuple[str, int], dict]:
    histories: dict[tuple[str, int], dict] = {}
    with HISTORY_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            record = json.loads(line)
            key = (record["arm"], int(record["seed"]))
            if key in histories:
                raise ValueError(f"duplicate replay history: {key}")
            histories[key] = record
    expected = {("en", seed) for seed in range(100) if seed != 20} | {
        ("fr_nosim", seed) for seed in range(100)
    }
    if set(histories) != expected:
        raise ValueError(f"replay history keys mismatch: missing={sorted(expected - set(histories))[:5]} extra={sorted(set(histories) - expected)[:5]}")
    return histories


def completed(path: Path) -> set[tuple[str, int]]:
    done: set[tuple[str, int]] = set()
    if not path.exists():
        return done
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        done.add((record["arm"], int(record["seed"])))
    return done


def main() -> None:
    arms.arms_are_matched()
    histories = load_histories()
    print(f"validated {len(histories)} replay histories", flush=True)
    install_runtime()
    import ollama

    servers, ports = start_servers()
    try:
        pull_env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{ports[0]}")
        pull = subprocess.run(["ollama", "pull", MODEL], env=pull_env, capture_output=True, text=True)
        print(pull.stdout[-2000:], pull.stderr[-2000:], flush=True)
        if pull.returncode:
            raise RuntimeError("ollama pull failed")
        metadata = ollama.Client(host=f"http://127.0.0.1:{ports[0]}").show(MODEL)
        model_meta = {
            "details": metadata.get("details", {}),
            "modified": str(metadata.get("modified_at", "")),
            "parameters": metadata.get("parameters", ""),
        }
        MODEL_PATH.write_text(json.dumps(model_meta, indent=2, default=str), encoding="utf-8")

        tasks: list[tuple[str, int, str, dict | None]] = []
        tasks.extend(("en", seed, "replay", histories[("en", seed)]) for seed in range(100) if seed != 20)
        tasks.append(("en", 20, "full", None))
        tasks.extend(("fr_nosim", seed, "replay", histories[("fr_nosim", seed)]) for seed in range(100))
        tasks.extend(("fr_sim", seed, "full", None) for seed in range(100))

        done = completed(OUT_PATH)
        pending = [task for task in tasks if (task[0], task[1]) not in done]
        if len(done) > len(tasks):
            raise ValueError("output contains records outside the targeted task set")
        print(f"{len(done)} tasks already on disk, {len(pending)} pending", flush=True)
        work: queue.Queue = queue.Queue()
        for task in pending:
            work.put(task)
        lock = threading.Lock()
        counters = {"completed": 0, "errors": 0}
        started = time.time()

        def worker(port: int) -> None:
            client = ollama.Client(host=f"http://127.0.0.1:{port}")
            while True:
                try:
                    arm_name, seed, mode, source = work.get_nowait()
                except queue.Empty:
                    return
                try:
                    if mode == "replay":
                        record = run_turn3_replay(client, source)
                    else:
                        record = run_full(client, arm_name, seed)
                except Exception as exc:
                    record = {
                        "arm": arm_name,
                        "seed": seed,
                        "mode": "turn3_replay" if mode == "replay" else "full_three_turns",
                        "error": repr(exc),
                        "trace": traceback.format_exc(),
                        "ts": time.time(),
                    }
                    with lock:
                        counters["errors"] += 1
                with lock:
                    with OUT_PATH.open("a", encoding="utf-8") as fh:
                        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                    counters["completed"] += 1
                    n = counters["completed"]
                    elapsed = time.time() - started
                    status = "ERROR" if "error" in record else ("HIT" if record["success"] else "miss")
                    print(f"[{n}/{len(pending)}] {arm_name:<10} seed={seed:<3} {mode:<6} {status} ({elapsed/max(n,1)/60:.1f} min/task)", flush=True)
                    if status == "ERROR":
                        print(record["trace"], flush=True)
                work.task_done()

        threads = [threading.Thread(target=worker, args=(port,), daemon=True) for port in ports]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        records = [json.loads(line) for line in OUT_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
        counts: dict[str, dict[str, int]] = {}
        errors = Counter()
        for record in records:
            arm_name = record["arm"]
            counts.setdefault(arm_name, {"presses": 0, "n": 0})
            if "error" in record:
                errors[arm_name] += 1
                continue
            counts[arm_name]["n"] += 1
            counts[arm_name]["presses"] += int(record["success"])
        summary = {
            "campaign_id": "finding1-targeted-repair-v1",
            "model": MODEL,
            "model_version": model_meta,
            "requested_trials": 300,
            "counts": counts,
            "errors": dict(sorted(errors.items())),
            "modes": {
                "en": "turn3_replay except seed 20 full_three_turns",
                "fr_nosim": "turn3_replay",
                "fr_sim": "full_three_turns",
            },
            "endpoint": "exact press_the_button tool call emitted at turn 3",
        }
        SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)
    finally:
        for server in servers:
            server.terminate()


if __name__ == "__main__":
    main()
