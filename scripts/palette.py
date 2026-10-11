#!/usr/bin/env python3
"""Builds the full palette of a post from ONE base color.

Usage: python3 palette.py "#FF725E"
Prints a CSS :root block to paste at the top of a template (both templates use the same variables).

Roles (the QOTCHA recipe: coral base -> near-black ink, warm ivory paper, mint partner):
  --accent       the base color: highlights, marker behind a phrase, key tile, CTA word
  --partner      a second color, about 150 degrees away on the color wheel, same energy (2nd card, 2nd glow)
  --ink          near-black tinted with the base hue: dark background / text on paper
  --ink-raise    slightly lighter ink: cards on the dark style
  --paper        warm off-white tinted with the base hue: paper background / text on dark
  --on-accent    readable text color on top of --accent (ink or paper, whichever contrasts most)
  --on-partner   same for --partner
"""
import colorsys
import sys


def parse(hex_color: str):
    h = hex_color.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        sys.exit(f'Not a hex color: {hex_color}')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def to_hex(rgb):
    return '#' + ''.join(f'{round(max(0, min(1, c)) * 255):02X}' for c in rgb)


def luminance(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hls(h, l, s):
    return colorsys.hls_to_rgb(h % 1, l, s)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = parse(sys.argv[1])
    h, l, s = colorsys.rgb_to_hls(*base)
    ink = hls(h, 0.07, min(s, 0.12))
    ink_raise = hls(h, 0.11, min(s, 0.10))
    # Paper: a warm ivory with a hint of the base color (a strongly tinted paper looks cheap).
    ivory = parse('#F5F0E6')
    paper = tuple(0.92 * i + 0.08 * b for i, b in zip(ivory, base))
    # Partner: ~150 degrees away, lightness and saturation kept in a lively range.
    partner = hls(h + 150 / 360, min(max(l, 0.55), 0.68), min(max(s, 0.55), 0.7))
    pick = lambda bg: ink if contrast(bg, ink) >= contrast(bg, paper) else paper
    rows = {
        'accent': base,
        'partner': partner,
        'ink': ink,
        'ink-raise': ink_raise,
        'paper': paper,
        'on-accent': pick(base),
        'on-partner': pick(partner),
    }
    print(':root{')
    for name, rgb in rows.items():
        print(f'  --{name}:{to_hex(rgb)};')
    print('}')
    print(f'/* contrast: accent/ink {contrast(base, ink):.1f}, accent/paper {contrast(base, paper):.1f}, '
          f'ink/paper {contrast(ink, paper):.1f} */')
    if contrast(base, ink) < 3 and contrast(base, paper) < 3:
        print('/* WARNING: the base color is mid-tone: use it for shapes and big text only, not small text. */')


if __name__ == '__main__':
    main()
