# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 6. Translate: all text translated and merged, dialogue review pass 4/33 done (phase 5 done 2026-11-18:
  marker tour `work/qa/marker3` 101/101 ok, 969 ids, no Japanese drawn; every kind has a budget in `tools/budgets.json`).
- **Phase 6 session 1 (2026-11-18), Orca worker, no subagents: translation and review run through `codex exec`.**
  - Done: `docs/synopsis.md` (codex read of the whole script: file -> chapter map, plot of both stories, cast and voice
    guide), `glossary.md` (rulings, ~270 binding terms, generated "Names from the game tables" section via
    `tools/glosstables.py`), `docs/translator-brief.md`, `docs/reviewer-brief.md`.
  - Tools: `tools/batches.py` (split / prompt / check / merge / wrap / status; one row per distinct (kind, jp), the
    merge writes every copy; dialogue is written as prose and wrapped to the box by `wrap()`; readings filled from
    names; `--defer-long`), `tools/codex_run.py` (parallel translate + check + 2 fix rounds), `tools/review.py`
    (review via codex, `apply` puts Critical/Important suggested EN in line by line and keeps width-failing ones out,
    Minors + blocked fixes -> `docs/polish.md`), `tools/mkpolish.py` (translator CUT lines -> polish), `tools/dumpstory.py`.
    Batch files, prompts, outputs, reviews: `work/tr/` (gitignored; b001-b017 tables, b018-b051 dialogue).
  - Status: 9,368 / 9,372 entries translated, lint 0 errors. Tables b001-b017 reviewed and fixes applied; dialogue
    b018-b020, b023, b026 reviewed and applied.
  - Budget changes: speaker tag 64 -> 80 px (8 x W name drawn in `work/qa/ne_w2`); lint lets every multi-line kind
    (desc, ptr.msg) re-wrap, not only msg.
  - Deferred: 4 appraiser tutorial messages (rom.169D8 16CA8 1711C 17450) need ~350 codes > the 255-code expansion
    buffer (docs/re/vwf.md: 0x200-byte stack buffer at 0x0201F4A4 / sp+0x1C); English kept in
    `docs/long-messages.tsv`. Phase 7: enlarge the buffer (static buffer in the hook block), then merge them.
    `elem.name` (10 属性 kanji) not translated: 18 px canvas, widen the draw code first (`batches.DEFER_KINDS`).
- **Next (phase 6, finish):** the dialogue review run was killed by low system memory (not a tool failure). Resume:
  `python -X utf8 tools/review.py run b021 b022 b024 b025 b027 ... b051 --jobs 4` (fewer jobs: memory), then
  `python -X utf8 tools/review.py apply <same>`, then commit. Then a consistency fix pass: "Seal Ring" (29 lines)
  vs glossary "Sealing Ring" (60): send those ids through a translator fix prompt (no bulk regex: translation.md).
  Merge NEW TERM reports (95, `work/tr/out/b*.md`) into glossary.md. Phase 6 is done when every batch's review has
  no Critical/Important left except width-blocked ones listed in polish.md.
  Last build: 2026-11-18 `python -X utf8 tools/build.py --marker` -> `build/beet_marker.nds` sha1
  9f82ab3e3a4acad381a0bd8b2e8352f0a1c13e23, smoke ok. (`tools/build.py` default = English from `en`, `--identity` =
  dump, `--qa ID=TEXT` overrides one entry.)
- **Phase 5 session 3 (2026-11-18):**
  - Name entry: the game already has an 英字 (A-Z a-z) tab; `ne_init` (engine.SITES 0x0202B6F0) opens the keyboard on
    it, and the hooks draw/measure the full-width Latin codes names are stored in as proportional letters
    (`engine.FW`, `fullwidth_code`). Max 8 letters (10 for entry types 2/4). 8 x W fits the speaker tag and spaces right
    in dialogue (`work/qa/ne_w2`). Lint stand-ins: `{hero}`/`{vandel}` = 8 x M (80 px), `{name93}` 10. RE in
    `docs/re/vwf.md` §Name entry; RAM-diff probe `tools/lua/objdump.lua`; warp.lua namentry scenes take `@FRAME`
    inputs (type a name, 決定 at t243,176).
  - Pointer strings: kinds `ptr.<group>` (`arm9text.PTR_GROUPS`: msg, speaker, label, line, comm, gba, keyboard).
    Over-long strings are relocated into the hook block (`engine.relocate_string`, pointer words repointed; tested,
    and seen in game). Budgets: comm 128 px at 8 px (box wraps by itself at ~130, mid-word), gba 212 px at 12 px,
    measured; msg/speaker reuse those budgets; label 84, line 180 jp-bound. `ptr.keyboard` (kana keyboard + kana list)
    is never inserted (`insert.KEEP_KINDS`; lint error if `en` set).
  - `jp_left.py --orig` on the marker build: only old copies of relocated pointer strings (unreferenced), the kana
    keyboard, name-entry kana class lists and code noise. For phase 9 pass the relocated list as `--known` or use
    `--slots`.
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
- **Phase 6 plan as written at phase 5 end (mostly done above):** translate in batches (`references/translation.md`): translators get `tools/budgets.json` +
  `docs/windows.md` + `glossary.md`; readings = English name, 説明 placeholders stay, `ptr.keyboard` stays empty,
  GBA-news fragments are one line each (word order across fragments), `a9.021B1820` follows a name ("<name> joined
  the party"). Polish for later (phase 8): name-entry key letters sit at the cell's left edge (centre them); the comm
  box wraps mid-word (word-wrap hook or keep strings <= 128 px); speaker tag 72 px in a shot; other `count * 12`
  centring; widen the 属性 canvas; full-width digits look wide; fill skills/quests/books/key items in the debug tool
  to replace the jp-bound budgets.
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
