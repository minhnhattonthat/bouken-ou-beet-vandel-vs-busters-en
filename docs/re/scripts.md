# Script files (`scr\x1a` bytecode): `field/script/rom.img`, `quest/quest.img`

## Container
- Magic `73 63 72 1A` ("scr\x1a"), then bytecode starting at offset 4. One file holds every event script; there is
  no separate pointer table. Code blocks and string pools are interleaved; strings sit in pools after the code that
  uses them.
- **Not resident in RAM** (verified: no 16-byte chunk of rom.img is in a RAM dump during dialogue). The game streams
  the parts it needs from the cartridge and copies each message into a text buffer (0x02275D80.., written by the copy at
  0x02004FA0 `bl 0x0210765C` = memcpy; terminator store 0x02004FBC). Watch log: `work/qa/watch1/log.txt`.
- Opcodes are byte-aligned, variable length; operands are unaligned little-endian u32 (often absolute file offsets:
  jump targets 0x1A18, 0x1A30 ... and string pointers).

## String references (verified for the first scene, survey for the rest)
- `70 <u32>` = show message at file offset; `.. 9E <u32>` (seen as `2A 9E`) = set speaker name. At 0x08B2 `2A 9E 80 0C 00 00`
  → name 船長 @0xC80; at 0x08BC `70 88 0C 00 00` → message @0xC88 (もう　少しだ！…). The pointed string starts after the
  `53 53` separator.
- Survey (`tools/scrscan.py`): of text-like strings in rom.img, 3,906 are pointed at by a u32 whose preceding byte is
  `0x70` (2,396) or `0x9E` (1,487), plus a few other opcode bytes (0x01, 0x00, 0x03, 0x18…: to classify with a real
  opcode parser). ~900 "unreferenced" runs are mostly bytecode bytes that happen to decode; a handful are real strings
  reached some other way (e.g. `ｃおわり` @0x866, `ｃ船長` inside 0xC78) — the extractor must explain every one.
- quest.img: opcode `20 <u32>` quest title, `1A <u32>` / `2D <u32>` description bodies, every opcode there takes a u32
  (e.g. `20 9C050000 1A B0050000 30 04000000 27 D0070000 1F 00000000 1B 01000000 FF`).

## Insertion plan (guess, prove in phase 3/4)
Because text is reached only through absolute u32 operands, English can be **appended to the end of the file** and the
operands repointed; code offsets and jump targets do not move. Needed: an opcode-length table (walk the bytecode from
each entry point, phase 4) so only real pointer operands are rewritten, never data that looks like one. The file is
read from the cartridge, so its size is limited only by ROM space (see `rom.md`).
