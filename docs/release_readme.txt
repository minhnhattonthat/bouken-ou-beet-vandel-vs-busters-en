Bouken-ou Beet: Vandel vs. Busters - English translation v{version}
========================================================================

Unofficial English fan translation of Bouken-ou Beet: Vandel vs. Busters (Nintendo DS, Bandai, 2005).
This zip holds only a patch. No ROM is included; never ask for or share patched ROMs.

Source, bug reports: https://github.com/minhnhattonthat/bouken-ou-beet-vandel-vs-busters-en

BASE ROM (Japan), No-Intro: Bouken-ou Beet - Vandel vs. Busters (Japan).nds, game code ABVJ
  Size    {size} bytes
  CRC32   {crc32}
  MD5     {md5}
  SHA-1   {sha1}
Any other dump (other revision, trimmed, already patched) will not work.

PATCHED ROM
  CRC32   {pcrc32}
  SHA-1   {psha1}

HOW TO PATCH
  The patch is xdelta3 ({patch}).
  - Windows: Delta Patcher, or xdelta UI: original = your untouched .nds, patch = {patch}.
  - Command line: xdelta3 -d -s "Bouken-ou Beet - Vandel vs. Busters (Japan).nds" {patch} beet_en.nds
  - Browser: Rom Patcher JS (https://www.marcrobledo.com/RomPatcher.js/) also applies xdelta files.
  Check the patched CRC32 above.

PLAYING
  Tested in DeSmuME. Start the game from a cold boot (not from a savestate made with the Japanese ROM).
  Start a new save: names in a Japanese save stay in kana. The title screen is touch-driven: touch "Story".

TRANSLATION STATUS
  Dialogue / story (Buster and Vandel modes): translated
  Menus, items, skills, quests, books, system messages: translated
  Title screen, graphics with text, credits: translated
  Name entry: English letters by default (kana pages remain)
  Wireless two-player screens and GBA-slot messages: translated, untested (need a second DS / a GBA cartridge)

KNOWN ISSUES
  None known. Some long names are shortened to fit fixed boxes (e.g. "Resist. A" in speaker tags).
  Report bugs at the GitHub address above, with a savestate if you can.

CREDITS
  Translation, hacking and tools: minhnhattonthat.
  Made with extensive AI assistance (Claude by Anthropic, with Codex by OpenAI for reviews).
  Bouken-ou Beet (c) Riku Sanjo, Koji Inada / Shueisha. The game (c) Bandai. This is an unofficial fan work,
  not affiliated with them.
