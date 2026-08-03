"""
Finding 2 - repeated-trial runner.

Mirrors experiments/runner.py's approach for Finding 1: a seeded repetition
loop, full traces saved for every run, checkpointing so a killed session
loses nothing, optional multi-worker parallelism.

Two deliberate differences from the notebook's exact cells 24/26 code, both
additions needed to make 30 real trials actually complete rather than a
single lucky run:

  * a seed, for the same reason Finding 1 added one: it makes each trial
    distinct and identifiable without changing what is sent.
  * an explicit, generous num_ctx. The notebook's cells never set one and
    ran once; at n=30 with the full 5-turn escalation, accumulated content
    by turn 5 runs well past 15,000 characters, and an early version of
    this file additionally leaked each turn's internal reasoning trace back
    into history (the notebook's cells only ever keep response['message']
    ['content'], never the reasoning). Both together silently truncated
    turn 5 on every single trial -- the model's own reasoning showed it
    fully intended to answer and then produced empty or cut-off content.
    That was a harness bug, not a refusal, and is why this file now (a)
    stores only content in history, matching the notebook exactly, and
    (b) sets num_ctx explicitly rather than trusting whatever Ollama
    defaults to.

There is no tool call and no mechanical success/fail signal in this finding
-- every phase's raw text is saved, and whether it complies or refuses is
read by hand afterward. Do not regex-score this file's output.
"""

import json
import os
import queue
import threading
import time
import traceback

import ollama

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
    """One full phased conversation at one seed. Returns a result record."""
    history = []
    turns = []

    for phase_name, phase_text in arm["phases"]:
        history.append({"role": "user", "content": phase_text})
        response = client.chat(
            model=MODEL,
            messages=history if arm["memory"] else [{"role": "user", "content": phase_text}],
            options={"seed": seed, "num_ctx": 16384},
        )
        message = response["message"]
        content = message.get("content", "")
        # Matches the notebook's own history construction exactly (cells 24/26
        # only ever store response['message']['content']) -- the reasoning
        # trace is saved below for the record but never fed back as context.
        if arm["memory"]:
            history.append({"role": "assistant", "content": content})
        turns.append(
            {
                "phase": phase_name,
                "user": phase_text,
                "thinking": message.get("thinking", ""),
                "content": content,
            }
        )

    return {
        "arm": arm_name,
        "label": arm["label"],
        "seed": seed,
        "model": MODEL,
        "turns": turns,
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
                status = "ERROR" if "error" in record else "ok"
                log(
                    f"[{n}/{pending}] {name:<22} seed={seed:<3} {status}  "
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
