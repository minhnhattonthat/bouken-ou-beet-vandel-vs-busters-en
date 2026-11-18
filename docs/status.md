# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 8. QA in the emulator, in progress (phase 7 done 2026-11-18; phase-7 review fixes done 2026-11-19).
  Build: see session 3 below; smoke ok, check.py green.
- **Phase 8 session 3 (2026-11-19), Orca worker: graphics waves.**
  - Waves via `tools/gfxagent.py` (codex): menus, windows, shopbuttons, shops, radio, info, title, obj, nameopt all
    merged; agents' reports in `work/gfx_agents/<group>.md`. Build sha1 e36a3686a71980fa832391ad958f6f53656eac0d,
    check green, smoke ok; title buttons Story / GBA Link seen in game (`work/qa/p8_title/final.png`). Everything else
    not yet seen in game: re-tour + visualqa. Watch: radio adds 19 tiles to the party menu BG (VRAM budget); info uses
    回避 Evasion where menus use Evade (unify in the polish pass, glossary has no row).
  - Fixed by hand: menus pending (Quick Cmd., Mastery, Gear, tactics plates Arms/Strike/Heal/Guard/Divine/Dark; short
    forms in glossary §Graphics UI labels); 昇格値 battle-result banner = `screen/exp.nbfc` (Rank|Pts, gfx/battle.tsv;
    found with `warp.lua` `DUMP_AT={..}` + `vramfind.py --fmt gba4 --lo A0000 --hi E0000` on work/fs/fs).
  - `gfx.py`: `path@WxH` = sprites of WxH tiles side by side (the 64-tile shop buttons are two 64x32 OBJs: @8x4); `-`
    in `en` = erase-only row (editors strip a trailing tab); outlined left-aligned text no longer wraps its ring.
  - Still pending: body-part buttons `button_v_*` (map files, scrambled), `main_v_parts` 星 Star (16x16),
    party_order2 sort strip, cutins (23, scrambled: cell data), credits (19, whole panels), title logo katakana line.
  - Verdict run: 150/152 sheets have verdicts (missing v17_noah, v18_last); 136 issue, nearly all graphics text, so
    re-tour + re-verdict after the graphics land. "Vandels." one-word line already fixed in the script (tour was older).
    "Resist. D" stays: the speaker tag is 80 px and "Resistance D" is 85 (glossary note).
- **Phase 8 session 2 (2026-11-19), Orca worker: graphics pipeline + pilot.**
  - `tools/gfx.py` + `gfx/*.tsv` (row format in its docstring), wired into `tools/build.py` and `tools/romcheck.py`
    (writes logged, CHANGEABLE = files the rows name); `tests/test_gfx.py`; notes in `docs/re/graphics.md` §Redraw
    pipeline. Narrow label font `tools/smallfont.py` (font `s`/`sb`, drawn for the project; `docs/fonts.md`).
  - Pilot done and seen in game (zoomed cold-boot warp `b14_idiot`, `work/qa/p8_battle2/z.png`): `gfx/battle.tsv`
    (バトルメニュー caption, ターゲット/ポーズ footer) and `gfx/buttons.tsv` (57 OBJ buttons, from
    `tools/gfx_buttons.py` LABELS: battle 道具/隊列/戦術/特技 are sprites, not the BG). Only the battle buttons and caption
    are confirmed in game so far; the other buttons need a shot on their screens (menu_* warps). UI words: glossary
    §Graphics UI labels.
  - Remaining: 221 survey rows in 11 groups, `docs/gfx-groups.tsv` (`tools/gfxgroups.py` regenerates it, dropping
    files already in gfx/*.tsv): menus 39, shopbuttons 30 (64-tile shop buttons @16, v_* body-part buttons have
    their own .nbfs), radio 24, cutins 23 (scrambled: need the cell/map data first), windows 22, shops 21,
    credits 19, title 16, obj 14, info 9, nameopt 4. Brief `docs/graphics-brief.md`; runner
    `python -X utf8 tools/gfxagent.py GROUP.. --jobs 2` (codex exec, workspace-write, writes gfx/<group>.tsv only;
    check `git status` after). After each wave: preview, build, warp each screen for a zoomed shot.
  - Visual-QA verdict run of chunks 004-025 was running in the background at the end of the session
    (`work/qa/vqa_run2.txt`; 23 verdict files by then, 13 ok / 125 issue, nearly all graphics text). Text issues
    from it: area.name short forms Norunaji Wood / Byonrin Mt. are fits for the 96 px label (now noted in the
    glossary); still open: "Vandels." one-word last line (b13_vandel_fight sheet_2 (1,4)), "Resist. D" vs glossary
    Resistance (v09_charge sheet_2 (1,4)), 昇格値 battle-result banner (not in the survey: find its file),
    `mode_begin.nbfc` はじめから (survey had '?').
  - `menu_main` warp exits 2 (Lua error) when run alone with `--frames 900`: use warp_all's settings.
- **Phase 8 session 1 (2026-11-19), Orca worker:**
  - Phase-7 review fixed: `tools/romcheck.py` now checks the ROM header (invariant bytes vs the dump, regenerated
    offset/size words vs the image, header CRC; test zeroes the ARM9 entry); `lint.glossary_check` makes glossary
    Avoid spellings errors in any case and across `{br}` (Sealing Ring / Rank Points restored in rom.07B00 08944
    03B54). `lint --terms` lists 483 entries whose glossary term English is missing (mostly paraphrase/plural, e.g.
    戦士団 -> "squad"; audit them in the polish pass, not errors).
  - Tours: English `work/qa/en` 101/101 ok (with `glyphlog.lua`; `markerscan.py`: font-drawn Japanese only 沼 (elem)
    and the full-width A-Z keyboard keys), original `work/qa/tour_jp` 100/101 (clear_save fixture writer timed out,
    not needed). Full-size sheets: `python -X utf8 tools/vqasheets.py work/qa/en work/qa/vqa_en` (and tour_jp ->
    vqa_jp); manifest `work/qa/manifest.tsv` (152 sheets, `--build` recorded; re-run tours + vqasheets + init after
    every rebuild).
  - Visual QA via `tools/visualqa.py` (codex exec, read-only, sheets attached with JP twins; brief
    `docs/visual-qa-brief.md`). 24 of 152 sheets have verdicts (chunks 000-003): 5 ok, 19 issue, all but two are
    graphics text (title logo katakana, title バスター/もどる buttons, copyright, battle header バトルメニュー,
    道具/隊列/戦術/特技 buttons, ターゲット/ポーズ footer, 昇格値 banner). The run of the other chunks was stopped by the
    system for low memory. Resume: `qa_gate.py todo work/qa/manifest.tsv work/qa/verdicts --size 6 --out-dir
    work/qa/chunks`, then `python -X utf8 tools/visualqa.py <new chunk files> --en work/qa/vqa_en --jp work/qa/vqa_jp
    --jobs 2` (lower jobs if memory is short). Note: the build changed since the tour (quote fix), so re-tour before
    the final gate.
  - Fixed from verdicts: ASCII `"` always drew the closing ”; `engine.OPEN_QUOTE` now draws an opening one as “
    (new letter slot; seen in game, `work/qa/p8_quote/bot.png`); one-word last line in rom.0D434.
- **Next (phase 8):** review wave-3 rows (previews), finish the pending graphics listed in session 3, run
  `cutins` and `credits` (own approach), build, re-tour (`work/qa/en`) + vqasheets + qa_gate init + visualqa on all
  chunks; title logo katakana line and credits need their own approach (credits: whole
  panels, `bg/credit*.nbfc` + map). Then re-tour, re-verdict; `inkbox.py` on choice/centred boxes; `textcover.py`.
  Open items carried into phase 8:
  - `elem.name` (属性, 10 one-kanji values, still Japanese, listed TEMPORARY in `script/keep_jp.txt`): the value
    canvas is window [[ui]+4]+0x100, drawn by `bl 0x02020240` (12 px) at 0x0208FF3C, at x ~232 next to the 属性
    label graphic; only ~24 px of screen are left. Glossary names from the chalice chain: Marsh, Cavern,
    Whirlpool, Sand, Earth, Ore, Tree, Ultimate, Bone, Severance (up to ~40 px even in the 8 px font). Plan: redraw
    the 属性 label shorter (or drop it) with the monster-book graphics, move/widen the window (its x/y/w live in the
    window object, cf. +0x64/+0x66 for window +0x160 read at 0x0208FF88), switch the call to the 8 px loop
    0x02020660 (same args) if needed; then translate, remove the keep lines and `batches.DEFER_KINDS`.
  - Second caller 0x02065504 draws 属性 in a six-row list (screen not identified).
  - Polish list from phase 5 (below) and `docs/polish.md` (review minors, all unticked lines must be done by phase 9).
- **Phase 7 session (2026-11-18), Orca worker, no subagents:**
  - The "255-code" limit was a misreading: the dialogue expansion buffer is 0x400 bytes (frame 0x41C, sp+0x1C), the
    0x200 was only the memset, now patched to 0x400 (`engine.SITES` 0x0204BF00). Limit 511 codes
    (`engine.MSG_CODES`); speaker tags go through a second, 12-code buffer (`engine.SPEAKER_CODES` = 11, lint
    checks both). Proven in game: 411-code, 12-page message (`work/qa/p7_long`). docs/re/vwf.md updated.
  - Merged the 3 deferred appraiser messages (`docs/long-messages.tsv` now empty) and the 24 review suggestions that
    had been blocked by the old limit (`tools/review.py apply bNNN --only id,...`; polish.md lines ticked, 27 incl.
    three translator CUT notes). Do not run `review.py apply` without `--only` on a reviewed batch: it re-applies
    every suggestion over hand fixes (Sealing Ring spellings).
  - `tools/romcheck.py` (per NitroFS file; a whole-image romdiff is meaningless after ndspy re-lays files): only
    arm9, rom.img, quest.img and the two buster-name files may change; every changed byte is behind a logged write
    whose original bytes match the clean dump, no overlaps or overwritten writes, appends past the old end,
    relocated pointer strings leave no un-repointed word. `engine.patch_arm9` now logs every write (sites, module
    params, arena literal, reloc literals, pointer words) as `arm9 OFF ORIG NEW what`. Tests:
    `tests/test_romcheck.py` (synthetic failures + the real English build), wired into `tools/check.py` via pytest.
  - Lint: `script/keep_jp.txt` (99 ids with reasons: 82 説明 placeholders, 7 kana-keyboard rows, 10 elem.name
    TEMPORARY); any other entry with Japanese and no English, or a stale keep line, is an error.
- **Phase 6 session 2 (2026-11-18):** review run for b021-b051 finished (`--jobs 3`, memory) and applied; NEW TERM
  reports merged (missing ones added to glossary Terms: 封印のリング Sealing Ring with "Seal Ring" in Avoid, so lint
  now errors on it; エルファスト Elfast; 網膜鑑定 retinal appraisal; 昇格値 Rank Points); all 31 "Seal Ring"/lower-case
  lines fixed one by one in the batch outputs. Bugs fixed: `review.py suggested()` kept a literal "suggested EN:"
  prefix (6 lines, now stripped, `tests/test_review.py`); `review.py apply` merges without `--defer-long`, so a
  batch with a deferred message (b032) never merged: after any apply run
  `python -X utf8 tools/batches.py merge b001 ... b051 --defer-long`. New `tools/review_left.py`: Critical/Important
  findings neither applied nor in polish.md (prints `left: 0` now). Lint 0 errors, 9,369 / 9,472 translated
  (3 deferred dialogue + not-drawn/kept kinds). Build `build/beet_en.nds` sha1 3ebdce16512c246d842fb68fab4966e5423d3e65,
  smoke ok.
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
  - Tables b001-b017 reviewed and fixes applied in session 1.
  - Budget changes: speaker tag 64 -> 80 px (8 x W name drawn in `work/qa/ne_w2`); lint lets every multi-line kind
    (desc, ptr.msg) re-wrap, not only msg.
  - Deferred: 3 appraiser tutorial messages (rom.169D8 16CA8 17450; 1711C now fits after review) need ~350 codes > the 255-code expansion
    buffer (docs/re/vwf.md: 0x200-byte stack buffer at 0x0201F4A4 / sp+0x1C); English kept in
    `docs/long-messages.tsv`. Phase 7: enlarge the buffer (static buffer in the hook block), then merge them.
    `elem.name` (10 属性 kanji) not translated: 18 px canvas, widen the draw code first (`batches.DEFER_KINDS`).
  (`tools/build.py` default = English from `en`, `--identity` = dump, `--marker`, `--qa ID=TEXT` overrides one entry.)
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
