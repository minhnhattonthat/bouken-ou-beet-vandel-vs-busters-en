# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| ROM `font/lc12x12.bin`, `font/lc10x10.bin`, `font/lc8x8.bin` | the game itself | the game's own glyphs | yes (the patch only re-uses glyphs already in the ROM) | dialogue/menu VWF letters (`tools/engine.py`); graphics labels in `gfx/*.tsv` with font 8/10/12 (`tools/gfx.py`) | cropped to ink, proportional advance |
| `tools/smallfont.py` | drawn for this project (2026-11-19) | MIT, same as repo | yes | graphics labels in `gfx/*.tsv` with font `s`/`sb` (buttons, captions, footers): 7 px caps, 5 px x-height | - |

No outside font files are used.
