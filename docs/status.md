# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 8. QA in the emulator, in progress (phase 7 done 2026-11-18; phase-7 review fixes done 2026-11-19).
  Build sha1 50c319fb9cd82c43e55739173e6ac4de01f7d9bc (session 8), check.py green (64 tests). **The tour in
  work/qa/en is older than this build** (398 messages rewrapped, tag hook): full re-tour first (Next (1)).
- **Phase 8 session 8 (2026-11-19), Orca worker: verdict run 4 fixed, widows, tag centring (context limit).**
  - Verdict run 4's 13 issues fixed. Speaker tags: 里の門 now "Village Gate" (78 px); "Master" (橋かけ名人, 89 px in
    full), "Mirei Chief" (112 px) and area "Muterin Range" (119 px) kept as short forms with glossary notes
    (rechecks in `work/qa/verdicts/recheck_main_5.tsv`). Graphics: cut-left `button_detail`/`button_order` (only
    sprite x 32..60 is on screen) now font `s` in box x 32 w 28; shop 必要Lv. = "Req. Lv" (gfx/shops.tsv; the
    digit is 47 px in). Re-toured those scenes (work/qa/en, build 14508a33), run 5 verdicts all ok but one more
    widow, which led to:
  - **One-word last lines everywhere:** `lint.widow` (error: a page of 2+ lines ends on one word and the line above
    has 2+ words and no sentence end) + `batches.py unwidow [-v] [--write]` (moves the last word of the line above
    down when it fits; also run by `wrap()` on merge). 398 entries rewrapped (rom 343, quest 53, ptr 2), one
    reworded (rom.4CF10). Tests in tests/test_lint.py.
  - **Speaker tags off-centre** (`tools/tagbox.py work/qa/en`, new: inkbox on every shot with the tag, rect
    178,121,77,17 --ink 90,66,74): 81 of 148 off by up to 7 px. The tag x had a second `6*count` site at 0x020951C8
    (the branch dialogue uses); hooked with `name_half2` (docs/re/vwf.md). After: 11/11 centred (`work/qa/p8_tag`).
  - Coverage: `--debugger` makes no difference to textlog (same 80 TAB lines on menu_items_all), so drop it. The
    table gap is because list screens fetch only the visible rows: menu_items_all shows page 1/9 (4 items). Close it
    with scenes (or `EXTRA`) that page through each list (R / d-pad; check warp.lua's button tokens) and select each
    row for its description.
- **Phase 8 session 7 (2026-11-19), Orca worker: re-tour, message gallery, coverage probes, verdict run 4.**
  - Tour `work/qa/en` on bf77ae45: 101/101 ok (cold scenes in the first run, whose summary was lost to a crash; the
    9 save scenes + menu_quests re-run from `work/qa/beet_tour.nds`, same bytes, `summary_save.tsv`). Sheets
    `work/qa/vqa_en`, manifest re-initialised (156 sheets, 148 changed), chunks `work/qa/chunks/chunk_ac7f49ec0b5d_*`,
    verdict run 4 via `tools/visualqa.py` (log `work/qa/vqa_run4.txt`). `qa_gate check`: 153 sheets, all with
    verdicts, **13 not ok** (3 stale sheet_2 ids of scenes that now make one sheet were dropped from the manifest by
    hand; old copy `work/qa/manifest_stale.tsv`). To fix:
    - one-word last lines: b07_newbie "job...", b08_guild "reach...", b12_zena/sheet_2 "business!!", b20_lena_sleep
      "dreamland!", b27_golden_castle "splendor?", v09_charge/sheet_2 "Rings" (rewrap or reword those messages);
    - speaker tags vs glossary: "Gate" (Village Gate, v05/v11), "Master" (橋かけ名人 Bridge Master, b23), "Mirei Chief"
      (Mirei Forest Chief, v10); place "Muterin Range" vs Muterin Mountains (v05). Check the 80 px tag budget: if
      the full form does not fit, add the short form to the glossary note and record a recheck verdict;
    - graphics: "Orders" button (menu_orders/sheet_2 (1,3)) and "Details" button (menu_quests/sheet_2 (1,3)) clipped at
      the left screen edge; shop_weapon_buy "Required Lv" label overlaps the level digit 1.
    After fixes: rebuild, re-tour the changed scenes, vqasheets, `qa_gate init --build`, visualqa on the todo chunks.
  - **Message gallery** `tools/debug/gallery.py` + `gallery.lua` + `gallery_run.py`: every script string a `70`/`9E`
    op points at (4,100 of 4,120) goes through the real interpreter as a dialogue span (`2A` open, `9E`, `70`, `34`;
    a bare `70` draws nothing), fed at the loop's read points 0x0204E630 / 0x0204E6F4 after the opening's first
    message. 2,243 spans in 8 chunks into `work/qa/gallery/c<k>/` (g<NNNN>.png = first page). Runs under the JIT
    (no --debugger: 260 fps vs 12). It copies the ROM to `gallery.nds`: a shared Battery/beet_en.dsv made warp_all's
    writesave scene crash.
  - textlog.lua now also logs `QST <pc>` (quest.img interpreter, docs/re/scripts.md), `PTR <word>` (read watch on the
    146 ptr.json pointer words) and `NAM m|w <idx>` (generic buster name pick); textcov.py maps them, and `report`
    takes several dirs (`report work/qa/en work/qa/gallery`, converted logs in `work/qa/_textcov`).
  - Coverage with tour + full gallery: **4,254/9,472** (rom.msg 3,842/4,120). The 278 rom strings left: 129
    speaker+message pairs whose span was fed but whose 9E/70 handlers never logged (the pc of a 9E/70 in
    work/qa/rom_missing.txt's strings, e.g. 0x134CB-area span at 79051 = 0x134CB? check with GAL lines: maybe the span
    starts at an op the loop never reads, or a branch inside it), 20 reached only by quest ops 4F/99, 4 spans stuck
    (GALSTUCK 0x3B6B7 0x3BD3B 0x3C2D7 0x3C2EB in c6: likely choices/waits other than 34). (Earlier: 2,720.) Left
    besides: table records (weapon ~1012
    fields, monster 897, shout 770, title/desc = quest.img 637, name 256, buster 153, skill 134, tengeki/meigeki,
    keyitem 90, vandel 93, ptr 103). menu_quests logs no QST (no quests in the list that early).
- **Phase 8 session 6 (2026-11-19), Orca worker: element icons, coverage pipeline (tour killed for low memory).**
  - The 魔賓館 card element book icon is `battle/face/mon_<elem>_{l,m,s}.ob` (30 files, 24x24, 4bpp, @3; not
    mastery_icon, which holds weapon/element pictograms with no text). Redrawn with the elem.json short forms in the
    small font (`gfx/elemicons.tsv`, plate x 6 y 5 11x11, fill 1, ink 6); seen in game: `work/qa/p8_book2/zoom.png`
    (Ma / Ca). Survey rows added (sheet 041); gfxgroups 0 pending. gfx.py now reads 8bpp tile files (`path:8`).
  - So 0x02065504 (`elem_short`, six cells, list object vtable 0x021AA898 at [obj+0x78]+0x254) is NOT the card
    screen; it is a 6-monster list only reachable in real Vandel mode. Not yet seen. Tried: v04_castle_works reaches
    an idle field by f3000, but the party/status there is Beet's (the warp does not switch mode). v01 runs the real
    Vandel intro: name entry (OK = t235,176), then an epithet entry; mashing A loops back to the entry after Harden's
    "My epithet is..." line (top screen black). Needs a look at that loop (choice? touch to advance?), or the save
    byte that selects Vandel mode (diff a Vandel-mode battery save vs clear_save).
  - Text coverage: `tools/lua/textlog.lua` (exec hooks on the opcode 70/9E handlers 0x0205128C / 0x0204F630 and
    the 18 arm9 table accessors; needs `--debugger`, now `warp_all.py --debugger`) + `tools/textcov.py report
    LOGDIR [--waive F]` (writes `build/strings.tsv`, maps SCR pcs through the original rom.img, runs the skill's
    textcover.py, prints per-kind counts). Test `tests/test_textcov.py`. Not probed yet: quest.img (427 desc + 210
    titles), names.json (256), arm9 ptr strings (115). Table coverage is per record.
  - Tour `work/qa/en` (build bf77ae45, glyphlog + textlog) was killed by the system for low memory after 69 of ~101
    scenes. Coverage on those 69: 783/9472 shown (rom.msg 491/4120). Earlier sheets/manifest were deleted with
    the old work/qa/en; work/states/ for some scenes may be from an aborted run on the JP ROM (warp_all's default
    ROM is the original: always pass build/beet_en.nds). Re-run warp_all with --jobs 2 (memory).
  - inkbox: the only font-drawn centred text is the speaker tag (choices/menus are gfx.py buttons, centred by
    construction); measure the tag rect on a tour dialogue shot, then run inkbox over every tour shot with a tag.
- **Phase 8 session 5 (2026-11-19), Orca worker: elem.name engine work (handed back at the context limit).**
  - Monster book 属性 value in English, seen in game (`work/qa/p8_elem/zoom.png`; longest "Severance" via
    `--qa` in `work/qa/p8_elem_long`): the window comes from a stack rect built at 0x0208F7BC (x 25 y 3 w 2 h 2) and
    passed to the rect helper 0x0202BFDC; `engine.SITES` 0x0208F7D0 -> `elem_rect` stub sets `engine.ELEM_WIN`
    (x 23 y 5 w 9: 72 px at (184, 40), one row under the Element label, right of the HP digits). The label graphic is
    unchanged. Budget elem.name 72 px; keep_jp TEMPORARY lines and `batches.DEFER_KINDS` entry removed.
  - Second caller 0x02065504 = Vandel-mode status screen (`screen/v_status_base`): six 2x2-tile cells (windows
    25-30 at x 1/6, y 14/16/18) one element each. `elem_short` + 0x0206551C -> 8 px loop 0x02020660 draw the new
    `short` field of script/arm9/elem.json (Ma Ca Wh Sa Ea Or Tr Ul Bo Se; `engine.ESHORT_SLOT` table, lint checks
    <= 16 px at 8 px, tests/test_lint.py). **Not yet seen in game**: no scene reaches the Vandel status screen (warps
    to v01 / mhall end in dialogue; needs an idle Vandel-mode field scene + `start t18,40 t210,62` or similar).
  - Found a graphics-text gap: the 魔賓館 monster buy cards show the element as a kanji inside a yellow book icon
    (`work/qa/p8_eshort/zoom.png`); it is a sprite, not font text. Likely `bitmap/mastery_icon.nbfc` (3328 bytes,
    `.nbfp` 512 bytes = 256 colours, so 8bpp: 13 icons of 16x16; also `status/bitmap/mastery_icon.ob`). gfx.py is
    4bpp only. Not in the graphics survey; add a row, redraw with the short forms (glossary §Graphics UI labels).
  - New probes: `tools/lua/windump.lua` (window structs), `tools/lua/winlog.lua` (window inits / rect helper args /
    `WIN_WATCH` write watch), `tools/lua/execlog.lua` (`EXEC_AT={..}`, needs `--debugger`). Ruling D9 recorded.
- **Phase 8 session 4 (2026-11-19), Orca worker: last graphics, re-tour, verdict run.**
  - Graphics survey closed: `tools/gfxgroups.py` lists 0 pending. Credits (19 panels, `gfx/credits.tsv`, codex via
    gfxagent; provisional name readings in its comments) seen in game on the `credits` warp, all panels clean
    (`work/qa/p8_credits/crops*.png`). By hand: radio win/lose/draw banners (YOU|WIN!, YOU|LOSE, D|R|A|W, new font
    scale `sx3`/`sx4` in gfx.py; wireless only, no warp), skill-type tags Atk/Buff/Weak/Heal, body-part buttons,
    ★ for the 8x8 星 mark (glyph added to smallfont), Vandel House tab without shadow. `gfxgroups.SKIP` records
    files with no text (all 23 cut-ins: portraits only; tengeki arrows; main_v_parts is Latin "BL") and the kept
    title logo (D5).
  - Build sha1 41aad77da2470fb3728585b046af3131c908042a (after the fixes below). Full tour `work/qa/en` 101/101 ok on
    the build before them; v14_battle7 + credits re-run on this one. `qa_gate.py check work/qa/manifest.tsv
    work/qa/verdicts`: 155 sheets, all with verdicts, **1 not ok: menu_monsters/sheet_2 (沼 element value, below)**.
    Run 3: 48 ok, 104 issue, 101 of them the title logo only (accepted under D5 in `verdicts/recheck_logo_3.tsv`;
    `docs/visual-qa-brief.md` now says so). Fixed: orphaned "expenses..." page in rom.4B7F8; stale
    v06_wrong_way/sheet_2 manifest line (that scene now has one sheet). Main-thread rechecks
    (`verdicts/recheck_main_4.tsv`): "Ribenin Lake" was a misread (crop reads Riberin), "Mirei Village" is the 96 px
    area.name short form (glossary note added).
  - gfx.py: font 10/12 `j` overlaps its hook under the previous letter ("Ko ji" gap in the credits).
  - Not yet set up: `textcover.py` (needs `build/strings.tsv` from the build and a `TEXT <addr>` log line from a
    text hook, e.g. in glyphlog.lua or a new probe) and `inkbox.py` on choice/centred boxes.
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
- **Next (phase 8), in order:** (1) full re-tour on the current build: `python -X utf8 tools/debug/warp_all.py
  build/beet_en.nds --jobs 2 --out work/qa/en --script tools/lua/glyphlog.lua --script tools/lua/textlog.lua`
  (no --debugger: tested, same logs; `books` scenes add it themselves), then `tools/tagbox.py work/qa/en` (expect 0),
  vqasheets, `qa_gate.py init work/qa/manifest.tsv work/qa/vqa_en --build build/beet_en.nds` (drop manifest lines
  whose sheet is now `missing`), todo `--size 6`, `tools/visualqa.py ... --jobs 2`, fix and recheck. Also re-run the
  message gallery (text moved: 398 rewraps);
  (2) coverage: `python -X utf8 tools/debug/gallery_run.py` (if not complete: `--only K`), then
  `tools/textcov.py report work/qa/en work/qa/gallery --list`; close the table gaps with list scenes that fill the
  data first (weapons/armor via `inv` + INV_CATS 1/2 in the shop sell lists, monster/buster/vandel books with every
  registration bit set, skills); quests and names need the random pick forced (quest board 4F at 0x3C288; name
  index r0 at 0x02019608, docs/re/scripts.md); waive only what is shown unreachable in `docs/text_unshown.tsv`
  (ptr.comm = wireless partner, ptr.gba = GBA game in slot 2, ptr.keyboard = kept Japanese by design); lists fetch only
  their visible rows, so page through them (session 8); (3) inkbox: speaker tags fixed and checked by tagbox.py
  (above), choices/menus are gfx.py buttons (centred by construction); (4) the Vandel-mode list screen
  (0x02065504, above); (5) `qa_gate check` exit 0 on the final build. Graphics: all survey rows done or in `gfxgroups.SKIP`; zoomed in-game shots still to take
  for wave-3 screens not yet warped (radio screens need a wireless partner: note as unreachable).
  Open items carried into phase 8:
  - `elem.name`: done in session 5 (above); leftovers are in Next (1). Also seen: the longest monster name (119 px,
    "Crimson Nightmare") in the 120 px name window (x 48) would end at x 167, ~3 px under the Element label (x 164):
    check one such entry in the book during the re-tour.
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
