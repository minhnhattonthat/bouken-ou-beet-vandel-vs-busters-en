# Skill gotchas (one line each: reference file it belongs in, then the fact)

- SKILL.md Step 0: the plugin was enabled but not in installed_plugins.json, so its guard hook never loaded (canary `sed -i` ran); fixed by the `hooks` block in `.claude/settings.json` pointing at the marketplace path.
- references/platform-nds.md: font glyph order can be JIS X 0208 with the unassigned rows 9-15 dropped and row 13 (NEC specials) kept, so kana decode right with a plain JIS index while every kanji is off by 6 rows. Check a kanji, not only kana, before trusting a table.
- references/pipeline.md (Recon): a hand-written JIS->Shift-JIS converter used 0x7D instead of 0x7E for even rows, shifting all hiragana by one; check against a known string after any table generator change.
- references/emulator-qa.md (Visual QA): `codex exec` reviewers given 11 sheets sometimes spend the run calling tools and return an empty last message; add "do not use any tools" and use batches of ~6 sheets.
- SKILL.md (tools): a Python `Path.write_text` on Windows writes CRLF; generated tables need `newline="\n"` or git warns and the generated-file test breaks.
- references/emulator-qa.md (DeSmuME): some DS games ignore Start on the title and every menu is touch-only; routes must use `t x,y`.
