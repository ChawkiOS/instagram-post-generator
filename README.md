# Instagram Post Generator

A [Claude Code](https://claude.com/claude-code) skill that turns **one base color** and **your content** (an app screenshot, a mockup, a wireframe or a few lines of text) into ready-to-post Instagram images.

- Feed post **1080 × 1350**, square **1080 × 1080**, story **1080 × 1920**, and carousels
- Two house styles:
  - **Dark**: near-black stage, soft color glows, big tight titles, tilted cards, phone mockups
  - **Paper**: graph-paper notebook, marker highlights, hand-written notes, chunky tiles with hard shadows
- A full palette computed from your single color, with a contrast check
- A caption with 5 hashtags at most

Each image is an HTML page at the exact Instagram size, exported to PNG with headless Chrome. You get real fonts, sharp text and precise layouts, and any change is one sentence away.

## Requirements

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- **Google Chrome** (or Chromium) to render the PNGs
- **Python 3** for the palette script
- An internet connection while rendering (fonts come from Google Fonts)
- Optional: **ImageMagick** for the previews. On macOS, `sips` is used when ImageMagick is missing.

## Install

### Option 1: with the skills CLI

```bash
npx skills add https://github.com/ChawkiOS/instagram-post-generator --skill instagram-post-generator
```

### Option 2: clone it into your skills folder

For all your projects:

```bash
git clone https://github.com/ChawkiOS/instagram-post-generator ~/.claude/skills/instagram-post-generator
```

For one project only, run this from the project root:

```bash
git clone https://github.com/ChawkiOS/instagram-post-generator .claude/skills/instagram-post-generator
```

Restart Claude Code (or start a new session). The skill shows up as `instagram-post-generator`.

## Usage

Type the command, or just ask in plain words:

```
/instagram-post-generator #FF725E  + drop a screenshot of the feature
```

```
Make an Instagram post for our new "dark mode" feature. Base color #3B5BFF.
Here is the screen: ./screens/settings.png
```

```
Fais-moi un carrousel insta pour expliquer la règle du mode Ghost, couleur #FF725E.
```

Claude only asks for what's missing (the color and the content). Everything else has a default it tells you about:
- **Format**: a feed post, plus a story version for launches.
- **Style**: paper for rules, mechanics and funny scenarios; dark for launches, app screens, polls and results.
- **Language**: the one you write in.
- **App name and logo**: taken from your project when there is one.

You get:
- the PNGs in a folder on your Desktop (`~/Desktop/<project>-insta/`);
- a short caption with at most 5 hashtags;
- an offer for one variation (the other style, or a story or carousel version).

## How it works

1. **Palette**: `scripts/palette.py "#HEX"` derives the whole palette from your color:
   - an accent and a partner color about 150° away on the color wheel;
   - a tinted near-black and a warm paper;
   - the readable text color on each.
2. **Message**: a 1–5 word hook, one highlighted line, one hero visual, three short facts and a call to action. That's about 25 words per image.
3. **Hero visual**: the key element of your app is rebuilt big in HTML (tiles, choice cards, a score…), or your real screenshot goes in a tilted phone frame. Never a flat full-screen screenshot.
4. **Render**: `scripts/render.sh` exports the PNG at the exact size and a 40 % preview.
5. **Check**: Claude looks at every preview and fixes it before delivering:
   - text overflow and widows;
   - elements touching the edges;
   - a story's top 220 px and bottom 300 px, which Instagram's own interface covers;
   - contrast.

You can also use the scripts by hand:

```bash
python3 scripts/palette.py "#3B5BFF"                          # prints a CSS :root block
bash scripts/render.sh my-post.html post out/post.png         # 1080x1350 + out/post-preview.png
bash scripts/render.sh my-carousel.html post out/slide-2.png 2  # slide 2 of a carousel
```

## Files

```
instagram-post-generator/
├── SKILL.md              # instructions Claude follows (workflow + design rules)
├── README.md
├── scripts/
│   ├── palette.py        # one color -> full palette (CSS variables) + contrast check
│   └── render.sh         # HTML -> PNG at Instagram sizes (headless Chrome)
└── templates/
    ├── dark.html         # dark style: glows, tilted cards, phone mockup, steps
    └── paper.html        # paper style: graph paper, marker, tiles, bubble, notes, bottom band
```

## Customize

- **Fonts**:
  - Dark: Space Grotesk and Work Sans.
  - Paper: Archivo Black, Work Sans and Caveat.

  Change the Google Fonts link and the `font-family` rules in the templates.
- **New building blocks**: add them to a template, with a comment saying when to use them. Claude picks them up.
- **House rules**: caption length, hashtag count and delivery folder are in the "Deliver" section of `SKILL.md`.

## License

MIT
