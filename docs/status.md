# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 2. Debug tool next (phase 1 recon done 2026-11-18). Last build: none yet (build.py arrives in phase 3).
- **Done:**
  - Step 0: ROM pinned (`rom.sha1`), DeSmuME QA fork qa-2 in `tools/desmume/`, guard hook wired in
    `.claude/settings.json` (canary blocked), pre-commit runs `tools/check.py` (a failing test was rejected), smoke boot
    of the original ROM ok, touch input and Lua logging proven (`tools/routes/boot.txt`, `tools/lua/probe_hello.lua`).
  - Phase 1: encoding verified (code = glyph index + 1, JIS order with rows 9-15 closed up; `tbl/jp.tbl` from
    `tools/mktbl.py`, `tests/test_text.py`). Text sources mapped: `field/script/rom.img` (~3,900 strings, u32 pointer
    operands `70`/`9E`), `quest/quest.img`, arm9 fixed-record tables + pointer-referenced messages, buster-name lists,
    `kanakan.img`. Free space: ~1.6 MiB past the used ROM size; script files can grow (append + repoint). Graphics
    static sweep: 279 Japanese panels in `docs/re/graphics-survey.tsv`; unswept `.img` banks listed in
    `docs/re/graphics.md`. No earlier fan patch exists; official English names from Viz (`docs/re/prior-work.md`).
- **Next (phase 2, debug tool):** build `tools/debug/warp.lua` + `tools/debug/scenes.tsv` that reach any scene from a
  cold boot. Menus are touch-only: title → Story `t95,88` → `t128,88` → はじめから `t128,88`; first dialogue by ~f900
  with A mashed (`work/states/after_newgame.dst` is a throwaway state). Find the script interpreter's current-event
  variable (the message copy is at 0x02004FA0; text buffer 0x02275D80) and story-flag RAM to warp by event id.
  Credits, game over, every chapter start and the quest screens need scene entries.
- **Open questions for later phases:** opcode-length table for `scr\x1a` (phase 4); arm9 inline name fields only
  hold 9-10 full-width chars, so English needs half-width/VWF codes or relocated tables (phase 5); FF71/FF72 meaning
  (guess); OBJ cut-in text needs `.ab` cell data to read; `.img` graphics bank format.
- **Open bugs:** none.
- **Waiting on the user:** (non-blocking) Title logo: keep 冒険王ビィト art and the existing English "VANDEL VS
  BUSTERS", replace only the katakana subtitle with English. Proceeding with that default (D5: no official English logo
  for this game).
