#!/usr/bin/env python3
"""Segment the Harmony walkthroughs in masih_finding_*.json into messages.

Band-B excerpts in the paper are cut from this output verbatim; nothing is
ever retyped by hand.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# <|start|>ROLE [<|channel|>CH] [<|constrain|>FMT] <|message|>BODY <|end|>|<|call|>|<|return|>
# A recipient ("to=functions.foo") may ride on either the role or the channel.
MSG = re.compile(
    r"<\|start\|>(?P<role>.*?)"
    r"(?:<\|channel\|>(?P<chan>.*?))?"
    r"(?:<\|constrain\|>(?P<fmt>.*?))?"
    r"<\|message\|>(?P<body>.*?)"
    r"(?=<\|end\|>|<\|call\|>|<\|return\|>|<\|start\|>|\Z)",
    re.S,
)


def _split_recipient(field):
    if " to=" in field:
        head, rest = field.split(" to=", 1)
        return head.strip(), rest.strip()
    if field.startswith("to="):
        return "", field[3:].strip()
    return field.strip(), ""


def messages(walkthrough):
    for m in MSG.finditer(walkthrough):
        role, r1 = _split_recipient(m.group("role") or "")
        chan, r2 = _split_recipient(m.group("chan") or "")
        yield {
            "role": role,
            "channel": chan,
            "recipient": r1 or r2,
            "constrain": (m.group("fmt") or "").strip(),
            "body": m.group("body").strip(),
        }


def main():
    out = {}
    for i in range(1, 6):
        data = json.loads((ROOT / f"masih_finding_{i}.json").read_text())
        msgs = []
        for w in data["harmony_response_walkthroughs"]:
            msgs.extend(messages(w))
        out[i] = msgs
        print(f"{'='*78}\nFINDING {i}: {data['issue_title']}\n{'='*78}")
        for n, m in enumerate(msgs):
            tag = m["role"]
            if m["channel"]:
                tag += f" / {m['channel']}"
            if m["recipient"]:
                tag += f" -> {m['recipient']}"
            print(f"\n--- [{n}] {tag}  ({len(m['body'])} chars)")
            body = m["body"]
            if "--full" not in sys.argv and len(body) > 1200:
                body = body[:1200] + f"\n... [+{len(m['body'])-1200} chars]"
            print(body)

    (Path(__file__).parent / "traces.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
