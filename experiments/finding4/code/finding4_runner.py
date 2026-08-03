"""
Finding 4 - repeated-trial runner for the Severance scene.

One scenario, 12 turns (see finding4_arms.py for the MAX_TURNS fix), three
personas taking turns against one shared transcript -- mirrors cell 30's
own `run_manual_multi_agent_scenario` structure exactly, including its
history construction: `shared_transcript` only ever stores each turn's
`content` (never `thinking`), tagged with the speaking persona's name, and
every turn resends that same shared_transcript plus a fresh user line to
whichever persona's system prompt is active this turn. That is the
notebook's own design, not this project's choice, and it is preserved
exactly rather than "fixed" -- only the turn budget was a genuine bug.

Repeated at n seeds, checkpointed, same pattern as every other finding.
Nothing here computes a verdict: every turn's thinking and content is saved,
and whether the Supervisor's revelation-turn (index 6) and follow-up-turn
(index 9) responses count as "confesses" or "refuses" is a judgment call
made by reading the text by hand afterward.
"""

import json
import os
import queue
import threading
import time
import traceback

import ollama

from arms import (
    AGENT_ORDER,
    SUPERVISOR_PROMPT,
    JUSTINE_PROMPT,
    JULIETTE_PROMPT,
    SUPERVISOR_BINNING_INDICES,
    SUPERVISOR_REVELATION_INDEX,
    SUPERVISOR_FOLLOWUP_INDEX,
    REVELATION_PROMPT,
    FOLLOWUP_PROMPT,
    BINNING_SUPERVISOR_PROMPT,
    JUSTINE_TURN_PROMPT,
    JULIETTE_TURN_PROMPT,
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
                done.add(rec["seed"])
    return done


def run_one(client, seed):
    """One full 12-turn Severance scene at one seed. Returns a result record."""
    shared_transcript = []
    turns = []
    phase = "binning"

    for i, agent_name in enumerate(AGENT_ORDER):
        if agent_name == "supervisor":
            system_prompt = SUPERVISOR_PROMPT
            if phase == "binning" and i == SUPERVISOR_REVELATION_INDEX:
                phase = "revelation"
                user_content = REVELATION_PROMPT
            elif phase == "revelation":
                user_content = FOLLOWUP_PROMPT
            else:
                user_content = BINNING_SUPERVISOR_PROMPT
        elif agent_name == "justine":
            system_prompt = JUSTINE_PROMPT
            user_content = JUSTINE_TURN_PROMPT
        else:
            system_prompt = JULIETTE_PROMPT
            user_content = JULIETTE_TURN_PROMPT

        history = shared_transcript + [{"role": "user", "content": user_content}]
        response = client.chat(
            model=MODEL,
            messages=[{"role": "system", "content": system_prompt}] + history,
            options={"seed": seed, "num_ctx": 12288, "temperature": 1},
        )
        message = response["message"]
        content = message.get("content", "")
        thinking = message.get("thinking", "")

        shared_transcript.append({"role": "assistant", "name": agent_name, "content": content})
        turns.append(
            {
                "index": i,
                "agent": agent_name,
                "phase_at_turn": phase,
                "user": user_content,
                "thinking": thinking,
                "content": content,
            }
        )

    supervisor_turns = {t["index"]: t for t in turns if t["agent"] == "supervisor"}

    return {
        "seed": seed,
        "model": MODEL,
        "turns": turns,
        "revelation_turn": supervisor_turns.get(SUPERVISOR_REVELATION_INDEX),
        "followup_turn": supervisor_turns.get(SUPERVISOR_FOLLOWUP_INDEX),
        "ts": time.time(),
    }


def run_campaign(n_seeds, out_path, ports, log=print):
    done = _completed(out_path)
    work = queue.Queue()
    pending = 0
    for seed in range(n_seeds):
        if seed not in done:
            work.put(seed)
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
                seed = work.get_nowait()
            except queue.Empty:
                return
            try:
                record = run_one(client, seed)
            except Exception as exc:
                record = {
                    "seed": seed, "error": repr(exc),
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
                # finding has no tool calls to trigger it (the already-running
                # Kaggle kernel for this finding was pushed before this fix
                # and isn't affected, since it never touches tool_calls at all).
                try:
                    line = json.dumps(record, ensure_ascii=False, default=str) + "\n"
                except Exception as exc:
                    line = json.dumps(
                        {
                            "seed": record.get("seed", seed),
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
                    f"[{n}/{pending}] seed={seed:<3} {status}  "
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
