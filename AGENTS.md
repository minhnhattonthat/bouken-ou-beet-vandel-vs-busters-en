# Bouken-ou Beet: Vandel vs. Busters (NDS) English translation

Skill: translate-retro-game (Claude Code: plugin, enabled in .claude/settings.json; other agents: `<SKILL_DIR>/SKILL.md`; `$SKILL` = the directory holding its SKILL.md, printed by `python tools/skill.py`). Read it before ROM, text or QA work.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py`        -> build/beet_en.nds (checks the dump against `rom.sha1` first; written in phase 3)
- Check:    `python -X utf8 tools/check.py`  (tests + lint; the pre-commit hook runs this; hooks path: `git config core.hooksPath tools/hooks`)
- Smoke:    `python -X utf8 $SKILL/scripts/emu.py build/beet_en.nds --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Warp:     `python -X utf8 $SKILL/scripts/emu.py build/beet_en.nds --out work/qa/warp --script tools/debug/warp.lua --var "SCENE='<name>'" --frames 900 --sheet` (scenes: `tools/debug/scenes.tsv`; all scenes + states into `work/states/`: `python -X utf8 tools/debug/warp_all.py`, which also writes the battery-save fixtures in `work/saves/` (e.g. `clear_save.dsv` for the post-clear title menus); never ask the user to play to a scene)
- Release:  `python -X utf8 tools/release.py` (patch + verify; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)

## Paths
- Original ROM: `rom/Bouken-ou Beet - Vandel vs. Busters (Japan).nds` (gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`). Emulator: this repo's own DeSmuME QA fork in `tools/desmume/` (release qa-2, `https://github.com/minhnhattonthat/desmume/releases/download/qa-2/desmume-qa-51b26329-win64.zip`, via `$SKILL/scripts/fetch_emu.py desmume`; gitignored; emu.py writes a fresh ini per run). Savestates: `work/states/`.
- Python deps: `pip install ndspy capstone keystone-engine pillow pytest`.
- Text: `script/` (JSON). Tables: `tbl/`. Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the agent types (translator, reviewer, visual-qa, playtester, graphics) shipped by the plugin as `translate-retro-game:<type>` (Claude Code), `.codex/agents/` (Codex) or `.opencode/agents/` (opencode), never general-purpose: their short tool list cuts each agent's start-up context from ~43k to ~9k tokens.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Title screen is touch-driven: Start does nothing; touch "Story" at `t95,88` (see `tools/routes/boot.txt`).
- Claude Code guard hook (blocks `sed -i`, heredoc edits) is wired in `.claude/settings.json` to the marketplace path, because the plugin's own hook did not load here.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
