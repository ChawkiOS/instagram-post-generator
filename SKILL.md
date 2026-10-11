---
name: instagram-post-generator
description: Instagram Post Generator. Creates ready-to-post Instagram images (feed post 1080x1350, square, story 1080x1920, carousel) for an app or product, in two house styles (dark with color glows, or paper notebook), from just a base color and the content (an app screenshot, a mockup or wireframe, or a few lines of text). Use when the user asks for an Instagram post, story, carousel, social media visual, launch or teaser image, or "une image pour insta".
metadata:
  version: "1.0.0"
  argument-hint: <base color> <screenshot, wireframe or text>
---

# Instagram Post Generator

Each image is an HTML page at the exact Instagram size, exported to PNG with headless Chrome.
Building it in HTML gives real fonts, crisp text and precise layout, and makes changes cheap.

Files:
- `scripts/palette.py "#HEX"`: the full palette from one base color, as a CSS `:root` block.
- `templates/dark.html`, `templates/paper.html`: starting points with every building block.
- `scripts/render.sh <file.html> <post|square|story> <out.png> [slide]`: the PNG, plus `<out>-preview.png`.

## 1. Ask only for what's missing

Ask in one short message, and only for what the user hasn't given:
1. **Base color** (hex, or a name you turn into a hex). Required.
2. **The content**: an app screenshot, a mockup or wireframe (image or description), or the message in a few lines. Required.

Everything else has a default; do not ask about it. State the choices in one line when delivering:
- format: a **feed post 1080x1350**, plus the **story 1080x1920** version if it's a launch or announcement;
- style: **paper** for a rule, a mechanic or a funny scenario; **dark** for a launch, an app screen, a poll or results;
- language: the user's language;
- app name, logo, store line: from the project (README, app config, website, icon files) when you are in one.

If the user gives a screenshot or wireframe, **read it** before designing: find the one element that shows what the feature does.

## 2. Plan the message (before any HTML)

Write down, in a few words each:
- **Hook** (the title): 1 to 5 words, big. The name of the feature or a punchy statement.
- **Highlighted line**: one promise, on a color marker (paper) or in the accent color (dark).
- **Hero visual**: the app's key element **rebuilt big in HTML** (letter tiles, choice cards, a result card, a score), or the real screenshot in a phone frame. Never a flat full-screen screenshot.
- **3 short facts** at most (one line each), and a **call to action** (where to get it, comment, swipe).

Total text outside the title: about 25 words per image. Cut, don't shrink the font.
Carousel: slide 1 is the hook and must work alone; then one idea per slide; "la suite →" / pager `2/4`; last slide = call to action.

## 3. Build

1. `python3 scripts/palette.py "#HEX"` and paste the block over the template's `:root`.
2. Copy the template into a working folder (the session scratchpad), one file per design (a carousel is one file with several `<section class="slide">`).
3. Set `<body class="post">` (or `square`, `story`), fill the SLOTs, delete unused blocks.
4. For a real screenshot or logo, put the image next to the HTML and reference it by relative path.

Design rules (what makes these images work; keep them):
- **Huge, tight titles**: 90–150 px, line height 0.9–1, slight negative letter spacing. Heavy display font (Archivo Black on paper, Space Grotesk 700 on dark), Work Sans for body, Caveat for hand-written notes (paper only).
- **One accent, one partner**: the base color for the key element and highlights, the partner color for a second card or glow. Everything else is ink and paper. No extra colors.
- **Playful tilt**: cards, tiles, pills and phones rotated between -8° and +8°, never two neighbours at the same angle.
- **Depth**: paper = hard offset shadows (`8px 8px 0 ink`), white bubbles with a thick ink border; dark = big soft shadows and two blurred glows (accent and partner, 15–22 % opacity) in opposite corners.
- **Brand header** on every image: logo + wordmark (last letter in the accent color) top left, a pill ("Nouveau", "Bientôt") or pager top right.
- **Generous margins**: 80 px on the sides (130 px left on paper, after the red margin line). Nothing touches an edge except glows and the bottom band.
- **Story**: keep the top 220 px and the bottom 300 px free of text and key visuals (Instagram's own UI covers them); the templates' `story` class already does it, but check.
- Emojis are welcome as icons (one per line or card), not as decoration everywhere.
- Real-looking content: plausible names, short believable examples, no lorem ipsum.

## 4. Render and check (always look before delivering)

```bash
bash scripts/render.sh work/post.html post out/post.png          # single image
bash scripts/render.sh work/carousel.html post out/slide-2.png 2  # slide 2 of a carousel
```

Read every `-preview.png` and fix before delivering:
- text overflowing, overlapping, or cut; a widow word alone on the last line of a title;
- elements touching the edges, or (story) in the top 220 px / bottom 300 px;
- too much empty space at the bottom (move the hero down or enlarge it) or a cramped stack;
- low contrast (small text must be ink on paper, or paper on ink; the accent color only for big text or on shapes).

Iterate until it looks finished. Fonts come from Google Fonts: rendering needs internet.

## 5. Deliver

- Save the final PNGs where the user can find them (their Desktop in a named folder, e.g. `~/Desktop/<project>-insta/`), with clear names (`ghost-post.png`, `ghost-story.png`, `ghost-carousel-1.png`…). Not the previews.
- Show the previews (or describe them) and give a **caption**: 2–3 short lines in the user's language, an emoji or two, a call to action, and **5 hashtags at most** (brand first, then the topic, then 2–3 discovery tags).
- Offer one variation at most (the other style, or the story/carousel version), in one line.

## Two references (the look this skill reproduces)

- **Paper, "Ghost" game mode**: graph paper, title "👻 GHOST" at 150 px, "Une lettre chacun." on a coral marker, five big black letter tiles C H A Q ? (Q in coral, ? dashed) with a white speech bubble « Je ne te crois pas ! », three hand-written notes with coral arrows, a black bottom band "Gratuit dans QOTCHA · 2 à 4 joueurs".
- **Dark, "Ça ou Ça" dilemma**: near-black with coral glow bottom left and mint glow bottom right, eyebrow "TU PRÉFÈRES…", title "Interdit de dire « aucun des deux ».", a coral card and a mint card, both tilted the opposite way with an emoji badge, an "OU" pill overlapping them, footer "Ton camp en commentaire 👇 / La minorité a perdu." and an arrow for the carousel.
