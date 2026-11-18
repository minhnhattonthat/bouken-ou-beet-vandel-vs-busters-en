# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Engine spike and marker build (in progress: engine done and proven, marker build boots 100/100 scenes;
  every kind now has a budget, measured or jp-bound; left: Latin name entry, ptr budgets, pointer-string relocation).
  Last build: 2026-11-18 `python -X utf8 tools/build.py --marker` -> `build/beet_marker.nds` sha1
  da444dcc6a72850903ced0349d674cdce80e9832, smoke ok. (`tools/build.py` default = English from `en`, `--identity` =
  dump, `--qa ID=TEXT` overrides one entry.)
- **Phase 5 so far (2026-11-18):**
  - Font decision made and proven in game: VWF with **letter-pair codes** (0x2000 + a*128 + b), letters cropped from
    the game's own full-width Latin glyphs, rendered by an arm9 hook block (new autoload section at 0x021C7EC0,
    arena-lo raised). ~35 chars per dialogue line. RE + design: `docs/re/vwf.md`; code `tools/engine.py`; tests
    `tests/test_engine.py`. Glyph torture line (all ASCII, `…×♪★`, double spaces) renders right
    (`work/qa/p5_t2/f001250.png`). Speaker-tag centring patched (0x02095314) but not yet seen in a shot.
  - Inserter `tools/insert.py`: rom.img/quest.img in place or append + repoint refs; names; arm9 slots (max-2 bytes,
    `KIND_CAP`); arm9 pointer strings in place only (relocation still to do). Marker mode = `[id]` + filler.
  - Marker tour: `python -X utf8 tools/debug/warp_all.py build/beet_marker.nds --jobs 6 --out work/qa/marker
    --states work/states_marker --script tools/lua/glyphlog.lua` (warp_all got `--script`), then
    `tools/markerscan.py work/qa/marker` (Japanese still drawn, ids seen, draw sites) and `tools/kindreport.py
    work/qa/marker/scan_ids.tsv` (per kind: seen, site, x). Last run: 100/100 ok, 966 ids seen, Japanese left only
    in name entry (kana keyboard) and one stray glyph (fixed by `KIND_CAP`, not re-toured).
  - Budgets: `docs/windows.md` (evidence) + `tools/budgets.json` (lint data). Measured 2026-11-18: dialogue,
    speaker tag (64 px), item/weapon/armor list rows (126 px + 18-byte slot), descriptions (one line, 194 px at
    12 px; shop 8 px 210 px), battle shouts (204 px), battle party panel (62 px), monster area (16 bytes).
  - Lint `tools/lint.py` (Japanese left, encodable, controls JP==EN, slot caps, 255-code messages, px per line and
    lines per page from budgets.json, one warning line for kinds without a budget) wired into `tools/check.py`;
    tests `tests/test_lint.py`. Width helper `tools/textwidth.py` (`--fill N` makes N-px test strings).
  - Debug tool: `wOFF=HEX` save pokes and `inv` (every item in the inventory) set tokens; scene `menu_items_all`.
    Save RAM dump probe `tools/lua/ramsave.lua` (diff two dumps to find a field). Inventory layout in
    `docs/re/scripts.md`.
  - Marker tour re-run (`work/qa/marker2`, 100/100 ok, 966 ids): Japanese left only in name entry and the monster
    book's 属性 沼.
  - Session 2 (2026-11-18): the 沼 is the monster attribute, also in the original: new arm9 table `elem` (10 one-kanji
    4-byte slots at 0x021233D8, wrongly in NOT_TEXT before), extracted to `script/arm9/elem.json` and **relocated**
    into the hook block at 16-byte slots (`engine.RELOC`: accessor literal + stride patched; inserter writes
    `Engine.reloc`; tested in `tests/test_engine.py`, seen in game). Its canvas shows only ~18 px (2 letters):
    budget 18, widening = draw-code work (docs/windows.md). The `monster.area` 16-byte KIND_CAP was a misdiagnosis
    (removed); monster name/area measured at 120 px (10-code canvases clip). Inventory regions mapped (weapons
    save+0x11E0, armor +0x136C; docs/re/scripts.md). warp.lua: `EXTRA='tokens'` var (append cheats/inputs to any
    scene), `INV_FROM`. Budgets for every remaining kind in `tools/budgets.json`: `jp-bound` (longest JP line at
    12 px; lists not reachable yet, verify in phase 8) or `not-drawn` (readings = sort keys, 説明 placeholders);
    lint skips width for `not-drawn`.
- **Next (rest of phase 5):** Latin name-entry keyboard (`a9.021AA0F8`.., ptr strings) and the English name length,
  then fix `{hero}` etc. stand-ins in `tools/lint.py` VARS; `ptr` budgets (per string, 115 entries: menus, 通信
  screens); arm9 pointer-string relocation into the hook block (same pattern as `engine.RELOC`); re-run the marker
  tour + `tools/markerscan.py` on the new build; `jp_left.py` on the marker build. Then phase 6 (translators get
  `tools/budgets.json` + `docs/windows.md`; readings = English name, 説明 placeholders stay). Optional: speaker tag
  72 px in a shot; other `count * 12` centring; widen the 属性 canvas; full-width digits look wide (polish);
  fill skills/quests/books/key items in the debug tool to replace the jp-bound budgets (phase 8 at the latest).
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
  - Phase 2 (done): `tools/debug/warp.lua` + `tools/debug/scenes.tsv` (100 scenes) + `tools/debug/warp_all.py`
    (`python -X utf8 tools/debug/warp_all.py --jobs 6`: all scenes from cold boot, states into `work/states/`, battery
    save fixtures into `work/saves/`; last run 100/100 ok, every row checked by eye in `work/qa/m1..m6.png`,
    `work/qa/exp/fac/finals*.png`, `work/qa/check_p2.png`). Coverage: title (before and after a clear: Story submenu
    Buster/Vandel, 通信 link check + 受付/検索, GBA link), new game, name entry, both story spines (b02-b31, v01-v18),
    credits, game over, field board, all 17 field menus incl. buster/vandel books (`books` cheat forces the empty book
    open), East Village weapon/armor/item shops with buy/sell/forge lists, inn, appraiser greeting, 魔賓館 reception +
    item/monster trade + aide screens, save prompt + "saved", quest abandon / quest done messages.
    Mechanisms: warp the interpreter PC at the opening event; `qXXXX` queues scripts from the idle field (talk events,
    shop counters, routines); `@FRAME` inputs; GOD mode; reset check; `writesave` / `sav=NAME` save fixtures
    (clear_save.dsv = Buster clear). RE in `docs/re/scripts.md` (UI state machine, door-trigger tree, facility table).
    Probes: `tools/lua/{uistate,trigdump,triggers,scrpc,scrpos,varlog,statelog,battlelog}.lua`.
  - Phase 3 (done): `tools/build.py` checks `rom.sha1`, loads with ndspy, rebuilds, then restores the 0x1000 word,
    the 0x00 inter-region padding (ndspy pads 0xFF) and the cartridge length. `tests/test_build.py` asserts the
    rebuild is byte-identical (also after replacing every file with its own bytes); a one-byte edit gives exactly one
    diff. Edits slot in at the `# Edits go here` line of `build()`.
  - Phase 4 (done): `python -X utf8 tools/extract.py [--force] [--only rom,quest,names,arm9]` writes `script/`
    (9,462 entries: `rom/NN.json` 4,120 messages/speakers/quest labels with `speaker` context, `quest/NN.json` 637,
    `names.json` 256 generic buster names (16-byte slots), `arm9/<table>.json` 4,334 fixed-slot fields with `addr` and
    `max`, `arm9/ptr.json` 115 pointer strings with their pointer words). Never clobbers `en`. Parsers:
    `tools/scr.py` (scr container: code / S-aligned string pools / data, two-pass on pointer evidence),
    `tools/arm9text.py` (+ `tools/a9tables.py` accessor scan), codec `tools/text16.py`. `tests/test_extract.py`:
    every byte of both script containers explained, every string operand on a string start, every jump on an
    instruction, all JSON `jp` re-encode to the ROM bytes, no kana run in arm9 outside the extracted slots (7 waived
    numeric words). New controls in `tbl/jp.tbl`: `{hero}` FF90, `{vandel}` FF92, `{name93}`, `{monster}`, `{count}`.
    Not text (documented, tested): rom.img data tail 0x51BB4-, quest.img table 0x11D4, file names, kanakan.img.
- **Next (phase 5):** engine spike + marker build. Font/VWF decision (renderer is fixed 12 px full-width; Latin exists
  only as full-width glyphs; `font/a8x8.bin` is an unused ASCII font candidate). Insert: rom.img/quest.img by
  appending strings (4-aligned) and repointing `Script.refs` operands; arm9 slots in place (`max` bytes) or
  relocated; arm9 pointer strings repointed via `ptrs`. Marker build: every entry -> `[id]` marker; find non-text
  "strings"; measure every box width in-game (width gate). Name entry needs a Latin keyboard (`a9.021AA0F8`..).
- **Debug-tool gaps (grow later, not blocking):** appraiser's appraisal choice (`4F`, needs story var 0x93); quest
  accept/turn-in flow from quest NPCs (quest.img scripts) beyond the two engine messages; the books show an empty entry 0
  (fill the registration bits for full text coverage in phase 8); shops of other towns if any (only East Village uses
  the AF/10/53 shop opcodes in rom.img); VS battles over 通信 need a second DS and are out of reach.
- **Open questions for later phases:** meanings of `{hero}`/`{vandel}`/`{name93}`/`{monster}`/`{count}` are guesses
  (check in the marker build); whether hiragana `reading` fields and the `desc` 説明 placeholders of the vandel/buster
  tables are ever shown; arm9 inline name fields only hold 9-10 full-width chars, so English needs
  half-width/VWF codes or relocated tables (phase 5); FF71/FF72 meaning (guess); OBJ cut-in text needs `.ab` cell data
  to read; `.img` graphics bank format. Shop/menu UI text (買う/売る, 武器購入 headers) is not in arm9 as tbl text:
  probably graphics; check in the phase 5 marker build.
- **Open bugs:** none.
- **Waiting on the user:** (non-blocking) Title logo: keep 冒険王ビィト art and the existing English "VANDEL VS
  BUSTERS", replace only the katakana subtitle with English. Proceeding with that default (D5: no official English logo
  for this game).
