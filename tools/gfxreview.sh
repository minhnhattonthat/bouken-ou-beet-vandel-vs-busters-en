#!/bin/sh
# gfxreview.sh: read-only review of gfxsweep.py sheets by `codex exec`, in 4 parallel batches.
#   sh tools/gfxreview.sh [work/gfx]    -> work/gfx/review_<n>.tsv
# Each batch lists every panel showing Japanese text. Merge the outputs into docs/re/graphics.md.
D=${1:-work/gfx}
PROMPT='You are a read-only visual reviewer for a Japanese-to-English game translation. The attached images are contact sheets: each panel has a red file-name label above it (path inside the game filesystem; "#N" = part N of a tall image). Panels render game tile graphics (some with a grey fallback palette, some garbled because tile order is not the on-screen order). List EVERY panel that shows Japanese text (kana or kanji) drawn as graphics, including small labels, buttons, banners, logos and sprite text. Also list panels with English text that is part of the UI (e.g. SKILL). Ignore panels with no text. Output only TSV lines, no prose, one per panel: sheet<TAB>file label<TAB>Japanese text as read (or ? if garbled)<TAB>what it is (button, window caption, title logo, credits, etc.). Do not run any commands that write files.'
n=0
for batch in "000 001 002 003 004 005 006 007 008 009 010" "011 012 013 014 015 016 017 018 019 020 021" "022 023 024 025 026 027 028 029 030 031" "032 033 034 035 036 037 038 039 040 041 042"; do
  n=$((n + 1))
  args=""
  for s in $batch; do
    [ -f "$D/sheet_$s.png" ] && args="$args -i $D/sheet_$s.png"
  done
  codex exec --skip-git-repo-check -s read-only -o "$D/review_$n.tsv" $args -- "$PROMPT (Sheets in this batch, in order: $batch.)" > "$D/review_$n.log" 2>&1 &
done
wait
echo done
