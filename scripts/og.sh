#!/usr/bin/env bash
# Generates link-preview images (static/og/<slug>.png, 1200x630) from the SVG covers, plus
# static/og/site.png for pages without a cover. Slack, iMessage, LinkedIn etc. don't render SVG,
# so the covers are screenshotted with headless Chrome (which also runs their CSS animations, so
# the preview is a real mid-animation frame). Runs in CI before `hugo`; head.html only emits
# og:image when the PNG exists, so local builds without it are unaffected.
#
# Usage: scripts/og.sh [chrome-binary]
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${1:-${CHROME:-google-chrome}}"
OUT=static/og
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"

shoot() {  # shoot <html-file> <png-out>
  "$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --user-data-dir="$TMP/profile" \
    --window-size=1200,630 --virtual-time-budget=4000 \
    --screenshot="$2" "file://$1" >/dev/null 2>&1
}

for svg in assets/covers/*.svg; do
  slug=$(basename "$svg" .svg)
  cat >"$TMP/$slug.html" <<EOF
<!doctype html><html><body style="margin:0;background:#e8e8e5">
<img src="file://$PWD/$svg" style="display:block;width:1200px;height:630px;object-fit:cover">
</body></html>
EOF
  shoot "$TMP/$slug.html" "$OUT/$slug.png"
  echo "og: $slug"
done

# Site card: the homepage accent (dots, query ring) beside the name. English only, because CI
# runners have no CJK fonts.
accent=$(sed -n 's/.*\(<svg class="intro-accent".*<\/svg>\).*/\1/p' layouts/_partials/intro-accent.html | head -1)
cat >"$TMP/site.html" <<EOF
<!doctype html><html><head><style>
body { margin:0; width:1200px; height:630px; background:#f4f4f2; color:#16181b; font-family:Georgia,"DejaVu Serif",serif;
  background-image: radial-gradient(#d6d6d2 1px, transparent 1px); background-size: 24px 24px;
  display:flex; align-items:center; justify-content:space-between; padding:0 96px; box-sizing:border-box; }
h1 { font-size:84px; font-weight:400; margin:0 0 20px; letter-spacing:-1px; }
p { font:22px/1.5 "DejaVu Sans Mono",Menlo,monospace; color:#5a6068; margin:0; max-width:560px; }
.mark { width:420px; color:#16181b; }
</style></head><body>
<div><h1>Yan Yan</h1><p>Recommender systems · Generative retrieval · LLMs · Content ecosystems</p></div>
<div class="mark">${accent}</div>
</body></html>
EOF
shoot "$TMP/site.html" "$OUT/site.png"
echo "og: site"
