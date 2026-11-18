# Translator brief - Bouken-ou Beet: Vandel vs. Busters (NDS, Bandai 2005)

You translate part of the Japanese text of "Bouken-ou Beet: Vandel vs. Busters", a DS RPG based on the manga/anime
"Beet the Vandel Buster" (Viz Media / Toonami in English), into English for a fan patch. Tone: shonen adventure for
kids and teens, lively, comic villains, earnest heroes. The player makes their own hero: a Buster (`{hero}`) in the
Buster story, or a Vandel (`{vandel}`) in the Vandel story.

Do not run commands or read files: everything you need is in this prompt. Your final message is the output.

## Input
The batch at the end: `id<TAB>speaker<TAB>kind<TAB>limit<TAB>Japanese`. ` / ` = line break and ` // ` = page break
in the Japanese box. Rows are in game order: use neighbours for context (a speaker row is followed by that speaker's
lines; a table row's name, reading and description sit together). The synopsis below says who is who.

## Output (your whole final message)
One line per input row, every id exactly once, same order: `id<TAB>English` (a real tab). After them, optional
report lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `CUT: id - what was dropped`. Nothing else: no code fences,
no headings, no commentary.
- Plain ASCII only: straight quotes ' and ", `...` for ・・・ and …, `--` for dashes, `!?` for ！？. No Japanese,
  no full-width characters, no curly quotes, no tabs inside the English, no `\n`.
- Dialogue (`kind` msg, desc, ptr.msg): write the box as natural English prose. Do NOT add line breaks: a tool wraps
  the text to the box (3 lines of ~36 characters per page) and adds pages as needed. Put ` // ` where the Japanese
  starts a new page at a real pause or change of thought (you may merge or move pages); put ` / ` only for a forced
  line break (a list, a poem, a sign). Short outbursts stay short.
- Single-line fields (names, menu labels, item and skill descriptions, battle shouts): the `limit` is hard. `NNNpx
  ~NNch` is the width (about 6.5 px per character at the 12 px font: i, l, ., ! are 2-3 px; m, w, M, W are 10 px;
  space is 4 px); `max NN bytes` is a hard byte cap (1 byte per character). Stay under both; rephrase rather than
  abbreviate. If impossible, use the clearest short form and report `CUT:`.
- Copy every `{...}` code exactly (`{hero}`, `{vandel}`, `{monster}`, `{count}`, `{name93}`), the same number of
  times as the Japanese. `{hero}`/`{vandel}` is a name up to 8 letters. No suffix glued to a code ("{count}th" ->
  "No. {count}"); no "a"/"an" right before one; `{monster}` is a monster name ("{monster} appeared!").

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add facts, don't summarise or
  skip. Make jokes and wordplay land in English (no translator notes).
- Keep each speaker audible (cast and voices in the synopsis). Register markers become English devices, not nothing:
  old man's ワシ/じゃ/のう -> "eh?", "my boy", "I tell you"; rough ぜ/ぞ/ねぇ/オレ -> "ya", "ain't", clipped grammar;
  polite です/ます from a young woman -> gentle and proper; ですわ/かしら -> refined, "I wonder", "dear"; villains'
  laughs keep their shape (クックックッ -> "Heh heh heh...", ガーッハッハッ -> "Gwahaha!", フフフ -> "Fufufu" or
  "Hmhmhm"). A line any speaker could have said is a mistake.
- Names and terms exactly as in the glossary table in this prompt. Honorifics are kept and hyphenated exactly where the
  Japanese has them (さん -> -san, くん -> -kun, ちゃん -> -chan, さま/様 -> -sama, 先生 -> sensei); never add one.
  Western name order. 「」 -> "...", 『』 -> '...' inside a sentence or "..." alone.
- Generic speakers get plain English titles (おじさん -> Old Man / Uncle by context, 民兵Ａ -> Militia A).
- Interjections and sound words in English: ハハハ -> "Hahaha", えっ -> "Huh?", グスッ -> "*sniff*", ガブリ -> "*chomp*".
- Item, monster and skill names: punchy English game names, consistent across the table (a name and its
  reading/name2 field are the same item). Katakana English loanwords become that English (クラウンシールド ->
  Crown Shield, サイクロンガンナー -> Cyclone Gunner). Kanji names get an English rendering, not romaji.
- Test and debug text (テスト, てすと, 汎用 labels) still gets translated plainly.

## Consistency
For a recurring name or term not in the glossary, pick a form, use it every time, and report `NEW TERM: jp -> en`.
