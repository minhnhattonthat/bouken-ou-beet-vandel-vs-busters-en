# Reverse-engineering notes

One file per subsystem. Mark every finding with how far it is proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| `text.md` | encoding (code = glyph+1, JIS order with gaps), control codes, fonts, where text lives | encoding verified (test_text.py); FF71/FF72 meaning guessed |
| `scripts.md` | `scr\x1a` bytecode files (`field/script/rom.img`, `quest/quest.img`), string pointers, insertion plan | pointer opcodes verified on first scene; opcode lengths TBD |
| `arm9.md` | arm9 fixed-record text tables, pointer-referenced messages, code-space candidates | table strides guessed from spacing |
| `rom.md` | header, filesystem, compression, free ROM space | verified (ndspy) |
| `graphics.md` + `graphics-survey.tsv` | graphics formats, every Japanese tile graphic found by the static sweep, unswept banks | formats verified by render; survey by codex review |
| `prior-work.md` | earlier patches (none), official English name sources | checked 2026-11-18 |

Tools: `tools/romls.py` (list/unpack), `tools/textscan.py` (text finder), `tools/scrscan.py` (script string/pointer
survey), `tools/mktbl.py` (table), `tools/fontsheet.py` (font sheets), `tools/gfxsweep.py` + `tools/gfxreview.sh`
(graphics sweep).
