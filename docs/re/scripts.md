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

## Interpreter state (verified 2026-11-18, phase 2: RAM watch + disassembly + warps that land)
- Context pointer at **0x021BEDAC** (ctx 0x0225E1A0 in the Buster story). `ctx+4` = file object (its FSFile at +4:
  top 0x017B9E00 = rom.img in the cartridge), **`ctx+8` = PC** (file offset), `ctx+0xC` = result register.
  Every handler seeks to PC and reads operands with FS_SeekFile 0x020FDD8C / FS_ReadFile 0x020FDDF8; that is why the
  bytecode is never resident in RAM. Main loop 0x0204E630. Logged by `tools/lua/scrpc.lua`.
- **Opcode length table** at arm9 0x021953D0 (0xC0 bytes, total length incl. the opcode; 0 = end/variable: `00`, `FF`,
  `BF`), handlers at 0x02195490. `tools/scrdis.py` disassembles with it (phase 4 should walk from entry points).
- Opcodes worked out so far: `17 <u32>` jump to event (event chain; targets listed by `tools/debug/events.py`),
  `54 <u32>` jump, `12 <u32>` jump if false, `41 <u16>` test story flag, `96 <u16>` clear flag, `9B <u16> <u16>`
  set flag field, `9A <u16>` mark event seen, `4C <u8>` push byte var ([[0x021BEBDC]+4][n]), `80 <s16>` push imm,
  `64 <u16>` load map, `98 <u16> x y` change map, `14 <u16> ..` battle, `70 <u32>` message, `9E <u32> ..` speaker,
  `6B <u32> <u32> <u32> ..` show bg (nbfc/nbfs/nbfp names), `AD <u16>` wait frames; `67/68/61/04 .. <u32>` register
  panel/NPC triggers with an event offset (map setup scripts, e.g. 0x29392).
- Save block: base [0x021BA3A0] + slot*0x159C (slot [0x021BEBE0], 2 treated as 0). **Story flags** = bitfield at
  [save+0x1580+8] (bit n = byte n>>3, mask 1<<(n&7)); **event-seen** bits at [save+0x158C+8]. `tools/lua/varlog.lua`
  logs changes.
- Event entries begin `9A id; 66; 64 map; ...` and end `17 <next event or map setup>; FF`. Setting PC to an entry
  while the opening event starts (PC 0x871-0x875) plays that event with its own map, actors and battle: this is
  `tools/debug/warp.lua`. Setting PC mid-event hangs (actors not spawned).
- Credits = script routine 0x2EE (`6B` per bg/creditNN, `AD 2C 01` = 300 frames each). Save prompt routine 0x459.
- Battle mode: state machine dispatched at 0x0209EB90 from table 0x021957E4 (37 states), state word **0x021BEE90**;
  13 = game over (banner after ~90 frames), 4 = battle running. `tools/lua/statelog.lua` logs it (needs --debugger).
- Field main 0x0202CC70 (called from 0x02002E30, which also runs battles); shop UI state table 0x0219527C (dispatcher
  0x0203B598, owner object methods at 0x021959B8). How the player opens a shop is still open (see status.md).

## Insertion plan (guess, prove in phase 3/4)
Because text is reached only through absolute u32 operands, English can be **appended to the end of the file** and the
operands repointed; code offsets and jump targets do not move. Needed: an opcode-length table (walk the bytecode from
each entry point, phase 4) so only real pointer operands are rewritten, never data that looks like one. The file is
read from the cartridge, so its size is limited only by ROM space (see `rom.md`).
