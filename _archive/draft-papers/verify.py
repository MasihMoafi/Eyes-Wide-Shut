#!/usr/bin/env python3
"""Mechanical checks on the built PDF.

The earlier drafts failed on things unit tests cannot see: 5pt evidence text,
raster figures, half-page float voids. These are the checks that would have
caught them.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "main.pdf"
# Two floors, because they encode two different promises.
#   Evidence text -- the verbatim model output a reviewer must actually read --
#   must be at least 8pt. In the drafts this replaces it ranged 5.2-7.3pt.
#   Figure chrome (axis ticks, node labels, captions) may be smaller, but not
#   below 7pt, which is the conventional lower bound for print.
MIN_EVIDENCE_PT = 7.9
MIN_ANY_PT = 6.9
FLOOR_RASTER_PPI = 200


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def check_font_sizes():
    """Point size of every text span, counted by page.

    poppler's extractors do not descend into the Form XObjects that hold the
    included figures, so the figure text -- the whole point of the exercise --
    would be invisible to them. MuPDF reports it.
    """
    import fitz
    counts, where, mono = {}, {}, {}
    with fitz.open(PDF) as doc:
        for pno, page in enumerate(doc, 1):
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        if not span["text"].strip():
                            continue
                        pt = round(span["size"], 1)
                        counts[pt] = counts.get(pt, 0) + 1
                        where.setdefault(pt, set()).add(pno)
                        # ews-figures.sty sets the verbatim trace panels in
                        # Noto Sans Mono and nothing else uses that face, so
                        # this isolates evidence text from inline code labels
                        # (which are Latin Modern Mono and may be smaller).
                        if "NotoSansMono" in span["font"]:
                            mono[pt] = mono.get(pt, 0) + 1
    return counts, where, mono


def check_fonts_embedded():
    out = run("pdffonts", str(PDF))
    bad = []
    for line in out.splitlines()[2:]:
        if not line.strip():
            continue
        cols = line.split()
        if len(cols) >= 5 and cols[-4] == "no":   # embedded column
            bad.append(cols[0])
    return bad


def check_raster_resolution():
    out = run("pdfimages", "-list", str(PDF))
    low = []
    for line in out.splitlines()[2:]:
        c = line.split()
        if len(c) < 14:
            continue
        page, xppi = c[0], c[12]
        try:
            if float(xppi) < FLOOR_RASTER_PPI:
                low.append((page, xppi))
        except ValueError:
            pass
    return low


def main():
    if not PDF.exists():
        sys.exit("main.pdf not built")
    ok = True

    sizes, where, mono = check_font_sizes()
    print(f"text sizes present: {sorted(sizes)}")

    small = {pt: n for pt, n in sizes.items() if pt < MIN_ANY_PT}
    if small:
        for pt in sorted(small):
            print(f"  FAIL: {small[pt]} spans at {pt}pt "
                  f"(floor {MIN_ANY_PT}pt) on pages {sorted(where[pt])[:8]}")
        ok = False
    else:
        print(f"  OK: smallest text anywhere is {min(sizes)}pt")

    if not mono:
        print("  FAIL: no monospaced evidence text found -- are the figure "
              "excerpts rendering as text?")
        ok = False
    else:
        thin = {pt: n for pt, n in mono.items() if pt < MIN_EVIDENCE_PT}
        if thin:
            for pt in sorted(thin):
                print(f"  FAIL: {thin[pt]} evidence spans at {pt}pt "
                      f"(floor {MIN_EVIDENCE_PT}pt)")
            ok = False
        else:
            print(f"  OK: evidence text is {sorted(mono)}pt across "
                  f"{sum(mono.values())} spans")

    bad = check_fonts_embedded()
    if bad:
        print(f"  FAIL: fonts not embedded: {bad}")
        ok = False
    else:
        print("  OK: all fonts embedded")

    low = check_raster_resolution()
    if low:
        print(f"  WARN: raster images under {FLOOR_RASTER_PPI} ppi: {low}")
    else:
        print(f"  OK: all raster images >= {FLOOR_RASTER_PPI} ppi")

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
