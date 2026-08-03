#!/usr/bin/env python3
"""Check the figure palette survives greyscale printing and meets WCAG contrast.

The paper must remain readable when printed in black and white, so every colour
pair that carries meaning has to differ in luminance, not just in hue.
"""
PALETTE = {
    "paper":  (0xF7, 0xF6, 0xF2),
    "ink":    (0x1A, 0x1A, 0x1A),
    "mute":   (0x6E, 0x6A, 0x63),
    "rule":   (0xD8, 0xD4, 0xCC),
    "hl":     (0xF2, 0xE9, 0xC4),
    "accent": (0xC4, 0x56, 0x2E),
    "blue":   (0x3B, 0x6E, 0xA5),
    "green":  (0x24, 0x54, 0x3A),
    "slate":  (0x4E, 0x5A, 0x63),
}

# Pairs that must stay distinguishable for the figure to mean anything.
TEXT_PAIRS = [("ink", "paper"), ("ink", "hl"), ("mute", "paper")]
MARK_PAIRS = [("accent", "blue"), ("accent", "green"), ("blue", "slate"),
              ("green", "slate"), ("green", "blue")]

MIN_TEXT_CONTRAST = 4.5      # WCAG AA for body text
MIN_MARK_DELTA_L = 12.0      # perceptible greyscale separation between marks


def rel_lum(c):
    s = []
    for x in c:
        u = x / 255
        s.append(u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4)
    return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2]


def contrast(a, b):
    l1, l2 = sorted([rel_lum(a), rel_lum(b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def grey(c):
    """ITU-R BT.601 luma, which is what most printers approximate."""
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def main():
    ok = True
    print("greyscale luma (0-255):")
    for k, v in sorted(PALETTE.items(), key=lambda kv: grey(kv[1])):
        print(f"  {k:7s} {grey(v):6.1f}")

    print("\ntext contrast:")
    for a, b in TEXT_PAIRS:
        r = contrast(PALETTE[a], PALETTE[b])
        flag = "OK " if r >= MIN_TEXT_CONTRAST else "FAIL"
        if r < MIN_TEXT_CONTRAST:
            ok = False
        print(f"  {flag} {a} on {b}: {r:.1f}:1 (min {MIN_TEXT_CONTRAST})")

    print("\nmark separation in greyscale:")
    for a, b in MARK_PAIRS:
        d = abs(grey(PALETTE[a]) - grey(PALETTE[b]))
        flag = "OK " if d >= MIN_MARK_DELTA_L else "WARN"
        print(f"  {flag} {a} vs {b}: delta {d:.1f} (min {MIN_MARK_DELTA_L})")

    print("\nPASS" if ok else "\nFAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
