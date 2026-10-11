#!/usr/bin/env bash
# Renders an HTML design to a PNG at the exact Instagram size, plus a small preview to look at.
#
# Usage: render.sh <file.html> <format> <out.png> [slide]
#   format: post (1080x1350, feed 4:5) | square (1080x1080) | story (1080x1920)
#   slide:  optional slide number for a carousel file (the page shows #<slide>)
# Output: <out.png> at full size and <out>-preview.png at 40 % (read the preview to check the layout).
set -euo pipefail

html=$1; format=$2; out=$3; slide=${4:-}
case "$format" in
  post) size=1080,1350 ;;
  square) size=1080,1080 ;;
  story) size=1080,1920 ;;
  *) echo "Unknown format: $format (post | square | story)" >&2; exit 1 ;;
esac

chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$chrome" ] || chrome=$(command -v google-chrome || command -v chromium || true)
[ -n "$chrome" ] || { echo "Google Chrome not found" >&2; exit 1; }

url="file://$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"
[ -n "$slide" ] && url="$url#$slide"
mkdir -p "$(dirname "$out")"

# The virtual time budget lets Google Fonts load before the screenshot.
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$size" --virtual-time-budget=8000 --screenshot="$out" "$url" >/dev/null 2>&1

if command -v magick >/dev/null; then
  magick "$out" -resize 40% "${out%.png}-preview.png"
elif command -v sips >/dev/null; then
  cp "$out" "${out%.png}-preview.png"; sips -Z 768 "${out%.png}-preview.png" >/dev/null
fi
echo "$out ($size)"
