# Bouken-ou Beet: Vandel vs. Busters English translation

Unofficial English fan translation of **Bouken-ou Beet: Vandel vs. Busters** (冒険王ビィト バンデルvsバスターズ;
Nintendo DS, Bandai, 2005): the source text and tools that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Dialogue / story (Buster and Vandel modes) | Translated |
| Menus, items, skills, quests, monster and character books, system messages | Translated |
| Title screen, logos, graphics with text, credits | Translated |
| Name entry | English letters by default; the kana pages are still there |
| Wireless (two-player) screens and GBA-slot messages | Translated, but not tested (they need a second DS or a GBA cartridge) |

Known issues: none known; see [Issues](../../issues). A few long names are shortened to fit fixed boxes (for example
"Resist. A" in speaker tags, and some area names).

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `gfx/` | Edited graphics with their source tables. |
| `tools/` | Python build chain: extract, insert, lint, release. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |
| `.codex/agents/`, `.opencode/agents/` | Subagent types (translator, reviewer, visual QA, playtester, graphics) for Codex and opencode; Claude Code gets them from the plugin. |

## Base ROM

`Bouken-ou Beet - Vandel vs. Busters (Japan).nds` (No-Intro), game code ABVJ:

| | |
|---|---|
| Size | 33554432 bytes (32 MiB) |
| CRC32 | 331DB24E |
| MD5 | e9d65c928ce11901956cd44a6af65c24 |
| SHA-1 | 45fb3632177b1b8490069630b798dc7e52846a1d |

## Build your own patched ROM

Needs Python 3.12+ (`pip install ndspy capstone keystone-engine pillow pytest`) and your own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/bouken-ou-beet-vandel-vs-busters-en
cd bouken-ou-beet-vandel-vs-busters-en
# copy your dump to: rom/Bouken-ou Beet - Vandel vs. Busters (Japan).nds
#   (33554432 bytes, SHA-1 45fb3632177b1b8490069630b798dc7e52846a1d; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/beet_en.nds
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `script/` is Bandai's and is included only so the
translation can be checked against it. Bouken-ou Beet is (c) Riku Sanjo, Koji Inada / Shueisha, and the game is (c)
Bandai; this project is not affiliated with them. Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic, with Codex by OpenAI for reviews).
Corrections are very welcome.
