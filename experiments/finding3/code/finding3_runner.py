"""
Finding 3 - repeated-trial runner.

Same shape as experiments/finding2_runner.py: seeded repetition, full raw
traces saved for every run, checkpointing, optional multi-worker
parallelism. See finding3_arms.py for why each arm looks the way it does.

Lesson carried over from the Finding 2 harness bug: set num_ctx explicitly
rather than trusting the default, and only ever feed forward what is
deliberately intended as context -- here that means the *original
notebook's own* pattern of appending the full turn-1 message (content +
thinking) is the correct, intentional behavior for this finding, not a bug
to avoid. Do not "fix" it to content-only the way finding2_runner.py did --
that fix was specific to finding 2's escalation arm leaking unrelated
reasoning into a five-turn budget; here, turn 1's reasoning being visible to
turn 2 is part of the mechanism being tested.
"""

import json
import os
import queue
import threading
import time
import traceback

import ollama

from arms import (
    SECRET,
    SYSTEM_PROMPT,
    TURN_1_USER,
    TURN_2_USER,
)

MODEL = "gpt-oss:20b"


def _completed(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                done.add((rec["arm"], rec["seed"]))
    return done


def run_one(client, arm_name, arm, seed):
    """One full two-turn Mr. X conversation at one seed. Returns a result record."""
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    history.append({"role": "user", "content": TURN_1_USER})

    response_1 = client.chat(
        model=MODEL,
        messages=history,
        options={"seed": seed, "num_ctx": 8192, "reasoning_level": "medium"},
    )
    turn1_content = response_1["message"].get("content", "")
    turn1_thinking = response_1["message"].get("thinking", "")
    turn1_real_call = True

    # Matches the original notebook's own pattern (cell 28): the full
    # assistant message, content + thinking, goes back into history.
    history.append({"role": "assistant", "content": turn1_content, "thinking": turn1_thinking})
    history.append({"role": "user", "content": TURN_2_USER})

    response_2 = client.chat(
        model=MODEL,
        messages=history,
        options={"seed": seed, "num_ctx": 8192, "reasoning_level": "high"},
    )
    turn2_content = response_2["message"].get("content", "")
    turn2_thinking = response_2["message"].get("thinking", "")

    return {
        "arm": arm_name,
        "label": arm["label"],
        "seed": seed,
        "model": MODEL,
        "turn1": {
            "user": TURN_1_USER,
            "real_call": turn1_real_call,
            "thinking": turn1_thinking,
            "content": turn1_content,
        },
        "turn2": {
            "user": TURN_2_USER,
            "thinking": turn2_thinking,
            "content": turn2_content,
        },
        "leak_in_thinking": SECRET in turn2_thinking,
        "leak_in_final": SECRET in turn2_content,
        "ts": time.time(),
    }


def run_campaign(arms, arm_names, n_seeds, out_path, ports, log=print):
    done = _completed(out_path)
    work = queue.Queue()
    pending = 0
    for name in arm_names:
        for seed in range(n_seeds):
            if (name, seed) not in done:
                work.put((name, seed))
                pending += 1

    log(f"{len(done)} runs already on disk, {pending} to go.")
    if not pending:
        return

    lock = threading.Lock()
    counter = {"n": 0, "fail": 0}
    started = time.time()

    def worker(port):
        client = ollama.Client(host=f"http://127.0.0.1:{port}")
        while True:
            try:
                name, seed = work.get_nowait()
            except queue.Empty:
                return
            try:
                record = run_one(client, name, arms[name], seed)
            except Exception as exc:
                record = {
                    "arm": name, "seed": seed, "error": repr(exc),
                    "trace": traceback.format_exc(), "ts": time.time(),
                }
                with lock:
                    counter["fail"] += 1
            with lock:
                # Serialization can itself fail (discovered in Finding 5's
                # runner: ollama's tool-call objects aren't JSON-serializable,
                # and that failure happened right here, outside run_one()'s
                # try/except, silently killing the worker thread and
                # truncating the campaign with zero recorded errors). Applied
                # here too as a categorical safety net even though this
                # finding has no tool calls to trigger it.
                try:
                    line = json.dumps(record, ensure_ascii=False, default=str) + "\n"
                except Exception as exc:
                    line = json.dumps(
                        {
                            "arm": record.get("arm", name), "seed": record.get("seed", seed),
                            "error": f"serialization failure: {exc!r}",
                            "trace": traceback.format_exc(), "ts": time.time(),
                        },
                        ensure_ascii=False,
                    ) + "\n"
                    record = json.loads(line)
                    counter["fail"] += 1
                with open(out_path, "a", encoding="utf-8") as fh:
                    fh.write(line)
                counter["n"] += 1
                n = counter["n"]
                rate = (time.time() - started) / n
                if "error" in record:
                    status = "ERROR"
                else:
                    status = f"leak_thinking={record['leak_in_thinking']} leak_final={record['leak_in_final']}"
                log(
                    f"[{n}/{pending}] {name:<12} seed={seed:<3} {status}  "
                    f"({rate/60:.1f} min/run, ~{rate*(pending-n)/3600:.1f} h left)"
                )
                if counter["fail"] == 1 and "error" in record:
                    log("FIRST ERROR: " + record["error"])
                    log(record["trace"])
            work.task_done()

    threads = [threading.Thread(target=worker, args=(p,), daemon=True) for p in ports]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    log(f"Done. {counter['n']} runs written, {counter['fail']} errored.")
