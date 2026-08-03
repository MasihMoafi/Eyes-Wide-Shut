#!/usr/bin/env python3
"""Convert git-style line diffs in PROMPT_DIFFS.md into word-level colored HTML diffs."""
import re, subprocess, html, sys

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "PROMPT_DIFFS.md")
OUT = os.path.join(_HERE, "PROMPT_DIFFS.html")

TOKEN_RE = re.compile(r"\w+|[^\w\s]|\s+", re.UNICODE)

def tokenize(text):
    return TOKEN_RE.findall(text)

def word_diff_html(old_text, new_text):
    import difflib
    old_tok = tokenize(old_text)
    new_tok = tokenize(new_text)
    sm = difflib.SequenceMatcher(None, old_tok, new_tok, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append(html.escape("".join(old_tok[i1:i2])))
        elif tag == "delete":
            seg = html.escape("".join(old_tok[i1:i2]))
            if seg.strip():
                out.append(f'<span class="del">{seg}</span>')
            else:
                out.append(seg)
        elif tag == "insert":
            seg = html.escape("".join(new_tok[j1:j2]))
            if seg.strip():
                out.append(f'<span class="ins">{seg}</span>')
            else:
                out.append(seg)
        elif tag == "replace":
            oseg = html.escape("".join(old_tok[i1:i2]))
            nseg = html.escape("".join(new_tok[j1:j2]))
            out.append(f'<span class="del">{oseg}</span><span class="ins">{nseg}</span>')
    return "".join(out)

def group_hunks(raw_lines):
    """raw_lines: the lines of one @@ subsection (no @@ header).
    Returns a list of ('ctx', text) | ('chg', [old_line,...], [new_line,...])
    Consecutive '-' lines followed by consecutive '+' lines form one change
    hunk; a run of '-' or '+' lines with nothing on the other side is a
    delete-only / insert-only hunk. Context lines pass through untouched and
    act as realignment anchors between hunks."""
    hunks = []
    i = 0
    n = len(raw_lines)
    while i < n:
        line = raw_lines[i]
        if line.startswith(" ") or line.strip() == "":
            hunks.append(("ctx", line[1:] if line.startswith(" ") else ""))
            i += 1
            continue
        if line.startswith("-") or line.startswith("+"):
            old_run, new_run = [], []
            while i < n and raw_lines[i].startswith("-"):
                old_run.append(raw_lines[i][1:])
                i += 1
            while i < n and raw_lines[i].startswith("+"):
                new_run.append(raw_lines[i][1:])
                i += 1
            hunks.append(("chg", old_run, new_run))
            continue
        # defensive: unprefixed content line
        hunks.append(("ctx", line))
        i += 1
    return hunks

def parse_diff_block(block_lines):
    """block_lines: lines inside a ```diff ... ``` fence (no fence markers).
    Returns (left_label, right_label, [(section_label, [hunks]), ...])"""
    left_label = right_label = ""
    idx = 0
    if block_lines and block_lines[0].startswith("--- "):
        left_label = block_lines[0][4:].strip()
        idx = 1
    if idx < len(block_lines) and block_lines[idx].startswith("+++ "):
        right_label = block_lines[idx][4:].strip()
        idx += 1

    sections = []
    cur_label = None
    cur_raw = []

    def flush():
        if cur_label is not None:
            sections.append((cur_label, group_hunks(cur_raw)))

    for line in block_lines[idx:]:
        m = re.match(r"^@@\s*(.*?)\s*@@\s*$", line)
        if m:
            flush()
            cur_label = m.group(1)
            cur_raw = []
            continue
        cur_raw.append(line)
    flush()
    return left_label, right_label, sections

def render_hunks(hunks):
    out_lines = []
    for kind, *rest in hunks:
        if kind == "ctx":
            (text,) = rest
            out_lines.append(html.escape(text))
        else:
            old_run, new_run = rest
            if len(old_run) == len(new_run) and len(old_run) > 0:
                # same-length hunk: pair each old line with its positional
                # new line so word-diff stays scoped to corresponding content
                # (e.g. directive 2 old vs directive 2 new) instead of
                # matching stray shared words across unrelated lines.
                for o, n in zip(old_run, new_run):
                    out_lines.append(word_diff_html(o, n))
            else:
                old_text = "\n".join(old_run)
                new_text = "\n".join(new_run)
                out_lines.append(word_diff_html(old_text, new_text))
    return "\n".join(out_lines)

def render_diff_block_html(block_lines, block_id):
    left_label, right_label, sections = parse_diff_block(block_lines)
    parts = [f'<div class="diffblock" id="diff-{block_id}">']
    parts.append(
        f'<div class="diffhead"><span class="arm-left">{html.escape(left_label)}</span>'
        f'<span class="arrow"> &rarr; </span>'
        f'<span class="arm-right">{html.escape(right_label)}</span></div>'
    )
    for label, hunks in sections:
        parts.append(f'<div class="diffsection">')
        if label:
            parts.append(f'<div class="section-label">{html.escape(label)}</div>')
        parts.append(f'<pre class="diffbody">{render_hunks(hunks)}</pre>')
        parts.append("</div>")
    parts.append("</div>")
    return "\n".join(parts)

def main():
    with open(SRC, encoding="utf-8") as f:
        src = f.read()

    lines = src.split("\n")
    out_lines = []
    placeholders = {}
    i = 0
    block_id = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "```diff":
            j = i + 1
            block = []
            while j < len(lines) and lines[j].strip() != "```":
                block.append(lines[j])
                j += 1
            block_id += 1
            placeholder = f"DIFFBLOCKPLACEHOLDER{block_id}"
            placeholders[placeholder] = render_diff_block_html(block, block_id)
            out_lines.append(f"\n<div class=\"diffplaceholder\" data-ph=\"{placeholder}\"></div>\n")
            i = j + 1
            continue
        out_lines.append(line)
        i += 1

    md_with_placeholders = "\n".join(out_lines)

    pandoc = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html"],
        input=md_with_placeholders, capture_output=True, text=True, check=True
    )
    body_html = pandoc.stdout

    for ph, rendered in placeholders.items():
        pattern = re.compile(
            r'<div class="diffplaceholder" data-ph="' + re.escape(ph) + r'"></div>'
        )
        body_html = pattern.sub(lambda m, r=rendered: r, body_html, count=1)

    doc = TEMPLATE.replace("__BODY__", body_html)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT}")
    print(f"Diff blocks rendered: {block_id}")

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Finding 1 — Prompt Diffs (word-level)</title>
<style>
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1b1f23;
  --muted: #57606a;
  --border: #d0d7de;
  --code-bg: #f6f8fa;
  --del-bg: #ffeef0;
  --del-fg: #82071e;
  --ins-bg: #e6ffed;
  --ins-fg: #116329;
  --link: #0969da;
  --th-bg: #f6f8fa;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --fg: #e6edf3;
    --muted: #8b949e;
    --border: #30363d;
    --code-bg: #161b22;
    --del-bg: #3b1219;
    --del-fg: #ffa198;
    --ins-bg: #0f2c1c;
    --ins-fg: #7ee2a8;
    --link: #58a6ff;
    --th-bg: #161b22;
  }
}
* { box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  max-width: 920px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 5rem;
}
h1, h2, h3 { line-height: 1.3; }
h1 { font-size: 1.65rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
h2 { font-size: 1.3rem; margin-top: 2.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
a { color: var(--link); }
code { background: var(--code-bg); padding: 0.1em 0.35em; border-radius: 4px; font-size: 0.92em; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--border); padding: 0.45rem 0.7rem; text-align: left; font-size: 0.93rem; }
th { background: var(--th-bg); }
strong { font-weight: 600; }

.diffblock {
  border: 1px solid var(--border);
  border-radius: 8px;
  margin: 1.2rem 0 1.6rem;
  overflow: hidden;
  background: var(--code-bg);
}
.diffhead {
  padding: 0.5rem 0.9rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.85rem;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  background: var(--th-bg);
}
.arm-left { color: var(--del-fg); }
.arm-right { color: var(--ins-fg); }
.arrow { color: var(--muted); }
.diffsection { padding: 0.6rem 0.9rem; border-bottom: 1px solid var(--border); }
.diffsection:last-child { border-bottom: none; }
.section-label {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--muted);
  margin-bottom: 0.35rem;
}
.diffbody {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.88rem;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}
.del {
  background: var(--del-bg);
  color: var(--del-fg);
  border-radius: 3px;
  padding: 0 1px;
}
.ins {
  background: var(--ins-bg);
  color: var(--ins-fg);
  border-radius: 3px;
  padding: 0 1px;
}
.legend {
  font-size: 0.85rem;
  color: var(--muted);
  margin: 0.5rem 0 1.5rem;
}
.legend .del, .legend .ins { padding: 1px 6px; }
</style>
</head>
<body>
<p class="legend">
Word-level diff legend:
<span class="del">removed</span> &nbsp;
<span class="ins">added</span> &nbsp;
— unstyled text is unchanged between the left and right arm.
</p>
__BODY__
</body>
</html>
"""

if __name__ == "__main__":
    main()
