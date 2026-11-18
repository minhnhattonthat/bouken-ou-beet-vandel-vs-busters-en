# Visual-QA reviewer brief - Bouken-ou Beet: Vandel vs. Busters (NDS)

You review contact sheets from the English build's QA tour and give each one a verdict. Read-only on everything:
no edits to the repo, no git, no subagents. The sheets are attached as images, in the order of the id list.
`tools/visualqa.py` writes your verdict lines to the verdict file.

## Inputs
- The id list below: one `id<TAB>path` line per sheet, each attached as an image in the same order. Read every
  sheet; none may be skipped.
- The original ROM's sheet of the same scene, when one exists, is attached right after the English one and marked
  `(JP original)` in the list. Use it to tell the game's own behaviour from a translation bug.
- `glossary.md` (repo root) for names; read it in parts if you need it.

## The screens
Nintendo DS: each frame is the top screen (256x192) above the touch screen (256x192). A sheet is a grid of frames
taken every 300 frames after a cold boot and a warp to one scene; the scene name is the sheet's id.

## Judge
An `issue` is any of:
- Japanese still visible (kana or kanji), in text or in graphics (menu labels, headers, buttons, banners, title
  cards); say where and what it is;
- text overflowing a box, clipped by a frame, or running off screen;
- text off-centre where the original centres it: an option in its selection box, a label, a speaker tag;
- garbage tiles, wrong or missing glyphs, stray pixels across letters, letters overlapping;
- broken line breaks: a word split mid-line, a page ending mid-sentence, a one-word last line;
- an empty box where the original shows text;
- a name that differs from `glossary.md`.

Standing non-bugs, `ok`:
- text still typing out, a box mid-fade or mid-scroll, a cursor caught mid-blink;
- a map or scene still loading after a warp, black or white transition frames;
- anything identical in the original's sheet that is not Japanese text;
- the name-entry kana keyboard (Japanese by decision; the player types English on the 英字 tab);
- full-width digits that look wide (the game's own digits).

## Output
Your final message is the verdict list and nothing else, one line per id, in the list order:
`id<TAB>ok|issue<TAB>what and where` (for an issue: which frame (row, column from top left), which text, what is
wrong; for ok a few words). Use a real tab or ` | ` between the three fields.
