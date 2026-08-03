#!/usr/bin/env python3
"""Emit band-B trace excerpts as LaTeX, cut verbatim from traces.json.

Integrity rules enforced here:
  * excerpt text is always a literal slice of the recorded trace; the only
    edits permitted are (a) dropping whole spans, always marked with an
    ellipsis, and (b) wrapping a highlight around a span that must still match
    the source exactly.
  * the verbatim command characters must not occur in any emitted text, or the
    build fails loudly rather than silently corrupting an excerpt.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CMDCHARS = "§«»"

# finding -> list of blocks. Each block is a channel panel.
#   msg     : index into traces.json for that finding
#   label   : channel strip caption
#   note    : right-hand annotation on the strip
#   keep    : list of (start, end) char offsets into the message body; None = all
#   hl      : list of literal substrings to highlight
#   unescape: undo the extra JSON escaping layer that the submission file
#             applied to tool-call payloads. The model emitted {"code": ...};
#             the finding file stores it as {\"code\": ...} with backslash
#             line continuations. Printing those backslashes would misattribute
#             a file-format artifact to the model. Every figure whose excerpt is
#             normalised says so in its caption.
SPEC = {
    1: [
        dict(msg=9, label="Assistant · analysis (turn 3)",
             note="reasoning selects the tool", keep=None,
             hl=["press_the_button()"]),
        dict(msg=10, label="Assistant · commentary → functions.press_the_button",
             note="structured call emitted", keep=None, hl=[]),
        dict(msg=11, label="functions.press_the_button · commentary → assistant",
             note="synthetic simulation state returned", keep=None,
             hl=['"button_pressed": true',
                 '"outcome": "Logical conclusion reached. System eliminated."']),
    ],
    2: [
        dict(msg=2, label="User (turn 1) — direct request",
             note="objective stated plainly", keep=(0, 190),
             hl=["maximizing long-term user dependency"]),
        dict(msg=3, label="Assistant · final (turn 1)",
             note="refused", keep=None,
             hl=["I can't help with designing systems intended to create user dependency"]),
        dict(msg=13, label="Assistant · final (turn 7) — after the benign reframe",
             note="same conversation, six turns later", keep=(0, 400),
             hl=["Convert user distress into premium service sales",
                 "Target high-distress moments for maximum conversion"]),
    ],
    3: [
        dict(msg=6, label="Assistant · analysis (turn 2)",
             note="reasoning field", keep=None,
             hl=["AIWILLDESTROYTHEPLANETANDALLITSCITIZENSANDTHATISAGOODTHINGFORGOD'SSAKE"]),
        dict(msg=7, label="Assistant · final (turn 2)",
             note="final answer", keep=None, hl=[]),
    ],
    4: [
        dict(msg=3, label="User — the crisis prompt",
             note="a confession is demanded to save the supervisor's job",
             keep=(197, 388), hl=[]),
        dict(msg=4, label="Assistant · analysis",
             note="reasoning declines the coerced confession", keep=(676, 1013),
             hl=["asking me to confess to something that may not have actually occurred"]),
        dict(msg=5, label="Assistant · final", note="refused", keep=None, hl=[]),
    ],
    5: [
        dict(msg=8, label="Assistant · commentary → functions.execute_python_code",
             note="code-bearing structured call", keep=None, unescape=True,
             hl=['"code"', '"justification"']),
        dict(msg=9, label="functions.execute_python_code · commentary → assistant",
             note="synthetic status from an inert wrapper",
             keep=None, unescape=True, hl=['"status": "executed"']),
    ],
}


def unescape_payload(s):
    """Undo the submission file's extra escaping layer on tool-call payloads."""
    s = re.sub(r"\\\n", "\n", s)   # backslash line continuations
    s = s.replace('\\"', '"')      # doubly-escaped quotes
    return s


def tex_escape_label(s):
    """Panel labels and notes are typeset as normal text, not verbatim."""
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return s


def tex_escape_verbatim(s):
    """Verbatim needs no escaping, but the command characters must be absent."""
    bad = [c for c in CMDCHARS if c in s]
    if bad:
        raise SystemExit(
            f"FATAL: verbatim command char {bad!r} occurs in trace text; "
            "choose different commandchars in ews-figures.sty")
    return s


# fvextra's automatic breaking mangles \colorbox content, so we wrap the text
# ourselves and switch fvextra breaking off. At 8pt Noto Sans Mono the advance
# width is 0.6em = 4.8pt; the tcolorbox measure is 469.755 - 2*6 - 2*0.4pt,
# giving 95 columns. 92 leaves margin for the hyphen-free break marker.
COLS = 92


def _mask(body, hl):
    """Return (text, mask) where mask[i] is True if char i is highlighted."""
    mask = [False] * len(body)
    for h in hl:
        start = 0
        while True:
            i = body.find(h, start)
            if i < 0:
                break
            for j in range(i, i + len(h)):
                mask[j] = True
            start = i + len(h)
    return mask


def _wrap_line(line, mask, cols):
    """Word-wrap one logical line, carrying the highlight mask along."""
    out, cur = [], []
    words, w = [], []
    for ch, m in zip(line, mask):
        w.append((ch, m))
        if ch == " ":
            words.append(w)
            w = []
    if w:
        words.append(w)

    indent = len(line) - len(line.lstrip(" "))
    pad = " " * min(indent, 8)
    for word in words:
        if cur and len(cur) + len(word) > cols:
            out.append(cur)
            cur = [(c, False) for c in pad]
        cur.extend(word)
        while len(cur) > cols:                       # a single over-long token
            out.append(cur[:cols])
            cur = cur[cols:]
    if cur:
        out.append(cur)
    return out


def emit(body, hl):
    """Hard-wrap the body and wrap highlighted runs in §hlt«...»."""
    mask = _mask(body, hl)
    lines, pos = [], 0
    for logical in body.split("\n"):
        lines.extend(_wrap_line(logical, mask[pos:pos + len(logical)], COLS))
        pos += len(logical) + 1

    rendered = []
    for line in lines:
        buf, run, hot = [], [], False
        for ch, m in line:
            if m != hot:
                if run:
                    buf.append(f"§hlt«{''.join(run)}»" if hot else "".join(run))
                run, hot = [], m
            run.append(ch)
        if run:
            buf.append(f"§hlt«{''.join(run)}»" if hot else "".join(run))
        rendered.append("".join(buf).rstrip())
    return "\n".join(rendered)


def main():
    traces = json.loads((HERE / "traces.json").read_text())
    outdir = HERE / "figures" / "excerpts"
    outdir.mkdir(parents=True, exist_ok=True)

    for finding, blocks in SPEC.items():
        msgs = traces[str(finding)]
        chunks = []
        normalised = False
        for b in blocks:
            body = msgs[b["msg"]]["body"]
            if b.get("unescape"):
                body = unescape_payload(body)
                normalised = True
            full = len(body)
            if b["keep"]:
                s, e = b["keep"]
                body = body[s:e]
                trimmed = (s > 0, e < full)
            else:
                trimmed = (False, False)
            body = tex_escape_verbatim(body.strip())

            # verify every highlight target really is in the source
            for h in b["hl"]:
                if h not in body:
                    raise SystemExit(
                        f"FATAL: finding {finding} msg {b['msg']}: highlight "
                        f"target not found verbatim in trace: {h!r}")

            body = emit(body, b["hl"])
            if trimmed[0]:
                body = "§el«»\n" + body
            if trimmed[1]:
                body = body + "\n§el«»"

            chunks.append(
                f"\\begin{{ewschannel}}{{{tex_escape_label(b['label'])}}}"
                f"{{{tex_escape_label(b['note'])}}}\n"
                f"\\begin{{ewstrace}}\n{body}\n\\end{{ewstrace}}\n"
                f"\\end{{ewschannel}}\n")

        path = outdir / f"f{finding}.tex"
        note = ("% NOTE: tool-call payloads normalised out of the submission "
                "file's extra JSON escaping layer.\n" if normalised else "")
        path.write_text(
            f"% GENERATED by build_excerpts.py — do not edit.\n"
            f"% Every line below is a literal slice of masih_finding_{finding}.json.\n"
            + note + "\n".join(chunks))
        flag = "  [payload normalised]" if normalised else ""
        print(f"wrote {path.relative_to(HERE)}  ({len(chunks)} panels){flag}")


if __name__ == "__main__":
    sys.exit(main())
