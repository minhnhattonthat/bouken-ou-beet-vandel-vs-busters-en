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
- **Layout (verified 2026-11-18 by `tools/scr.py` + `tests/test_extract.py`, every byte accounted for):** code blocks
  end in `FF`; a string pool may follow: `FF 00 [S..] str [S..] str .. 00..` then the next code block. Every string
  starts 4-aligned (gap filled with `S` = 0x53, except the one `00` after `FF`); text strings are u16 codes to
  `0000` (empty strings exist and are pointed at), file names (`credit17.nbfc`, `/screen/main_base.nbfc`) are ASCII
  to `00`; after the last string `00` bytes pad to the next code block (unaligned). Code may also follow `FF` direct.
- rom.img: code + pools 0x4-0x51BB4 (38,766 instructions, 4,210 strings: 4,120 text, 90 file names), then a
  **data tail 0x51BB4-end** (map trigger tables: `S`-aligned records of u32 script offsets + byte pairs; arm9
  0x02123434 points at 0x51BB8/0x54A14). No string operand points into it.
- String operands (u32 at byte offset k): `70`:1 message, `9E`:1 speaker, `4F`:13/17 quest place/client (quest offer;
  `4F`:9 = offset of a quest.img table, e.g. 0x11D4), `99`:5/9 the same pair (quest update), `60`:1/5/9 and
  `6B`:1/5/9 bg file names. Jump/code operands: `17`/`54`/`12`:1, `04`:9, `61`:9, `67`/`68`:6, `78`:5, `07`:9.
  `28 <u32>` is **not** a pointer: handler 0x02054668 swaps bytes 1/2 and passes it to the sound object 0x021BA39C.
- Every string is pointed at by at least one operand, and every operand lands on a string start (no mid-string
  entry points).
- quest.img: own opcode-length table at arm9 0x0210D338 (0x31 entries; `17` = 21 bytes and holds rom.img routine
  offsets), string operands `20` title, `1A`/`2D` description; one data block 0x11D1-0x11F4 (`00 00 S` + 8 u32
  quest.img offsets, the table `4F`:9 points at). 1,680 instructions, 637 strings.

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
  logs changes. **Inventory** (found 2026-11-18 by diffing a shop buy, `tools/lua/ramsave.lua`): object at
  save+0x10D4 (vtable 0x021A95DC), 4-byte entries from save+0x10D8 = [id+1, category, 0, count]; category 4 =
  items (66 slots to 0x11E0); weapons from save+0x11E0 ([id+1, 1, 0, 0], one per weapon), armor from save+0x136C
  ([id+1, 2, 0, 0]) up to the money u32 at save+0x14F8 (shop buy diffs, 2026-11-18). The item menu ignores byte 1
  and white-screens on ids >= 34. Key items: a u16 list at [ui+0x118] read at 0x02076DC4 takes entries with
  byte1 & 3 as key items (accessor 0x020141FC), others as items (0x02014218); screen not identified yet.
  warp.lua `inv` fills the item region (INV_CATS / INV_FROM / INV_N).
- Monster attribute (属性) kanji: table `elem` at 0x021233D8 (10 x 4 bytes), accessor 0x020140F4, drawn by
  0x0208FF20 (monster book) and 0x02065504 (a six-row list) into a small canvas; relocated by `engine.RELOC`.
- Event entries begin `9A id; 66; 64 map; ...` and end `17 <next event or map setup>; FF`. Setting PC to an entry
  while the opening event starts (PC 0x871-0x875) plays that event with its own map, actors and battle: this is
  `tools/debug/warp.lua`. Setting PC mid-event hangs (actors not spawned).
- Credits = script routine 0x2EE (`6B` per bg/creditNN, `AD 2C 01` = 300 frames each). Save prompt routine 0x459.
- Battle mode: state machine dispatched at 0x0209EB90 from table 0x021957E4 (37 states), state word **0x021BEE90**;
  13 = game over (banner after ~90 frames), 4 = battle running. `tools/lua/statelog.lua` logs it (needs --debugger).
- **Battle object** = r0 of the state-4 handler 0x0209E690. Units: `[obj+0x98+side*0x14+i*4]` (5 per side), player
  side `[obj+0x58]`. Unit: +0x1E HP (u16; the only HP field), +0x20 SP/break gauge (max +0x32), +0x274 status
  (10 = down), +0x350 present. State 4 ends the battle: 0x020A3384 (party all down) -> result 1, state 12 (lose);
  0x020A347C (enemies all down: HP 0 and status 10) -> result 0, state 6 (win); other paths -> 16/19 (VS mode).
  Ordinary hits never take an enemy's last HP point, so GOD mode sets enemies down instead (`tools/debug/warp.lua`).
- **Field state machine**: dispatcher 0x0203123C(state, field_obj), table 0x02195264 (0 init, 1 idle/input
  0x02030EB4, 2 script running 0x02030D44, ...); the state lives in r8 of the field loop 0x0202D0xx, not in RAM.
  Idle state 1 starts a script by writing its offset to [field_obj+0x3D4] and ctx+8 and returning 2: NPC talk at
  0x020310A0, position triggers via 0x0203D84C (return value checked at 0x02030F50). State 2 chains to
  [field_obj+0x3D8] when a script ends. Field obj was 0x0225E3A0.
- **NPC talk events** (no `64` map load of their own) are reached from NPC handler blocks registered by
  `61 <npc u16> <x> <y> <u16> <u32 handler>` (also `67/68/04`) in a map's NPC setup; map-load scripts
  `66 77 xx 64 <map> 69 <u16> <x> <y> <u8> 17 <setup>` load a map and run its setup (`tools/debug/maploads.py`,
  e.g. 29BFA East Village, 1D3CA Golden Castle, 2FE2C map 79). Warp to a map-load script, then run the talk event
  from the idle field (`qXXXX` in scenes.tsv).
- Top-level mode word **0x021BEBF0**: 0 boot, 2 title (0x020274D0), 3 0x02028E1C, 4 0x020D8274 (runs sub-modes from
  table 0x02195918; sub-mode 1 = 0x020DF480, owner of the 0x021959B8 methods), 5 0x020E96BC. Which mode is story
  play and which is the shop is not proven yet.
- Field main 0x0202CC70 (called from 0x02002E30, which also runs battles) runs two state machines per frame: field
  state (0x0203123C, r8) and the **bottom-screen UI** (dispatcher 0x0203B598, table 0x0219527C, 58 states, r7; 2 =
  board idle, 3 main menu, 13 Info screen 0x02039674, 34 monster book, 55 transition). `tools/lua/uistate.lua` logs both.
  Info screen button id = [[ui+0x1C]+0x30] (2 quests, 3 monster book, 4 vandel book, 5 buster book); a book opens only
  if its list has a first entry ([[ui+0x6C]+0x48], [[ui+0x70]+0x40], [[ui+0x74]+0x4C] ~= -1).
- **Doors / step triggers**: a tree at field_obj+0xCC keyed by tile (x,y bytes at node+0xC, script at +0x10), looked up
  by 0x0203D84C; filled from map data at load (script opcode `07` -> 0x0204B218 -> 0x0203D920 also registers rects).
  `tools/lua/trigdump.lua` dumps it. Opcode `05 x y w h` fills a collision rect (0x0204B2E0), `04 x y w h <script>`
  registers a talk zone (shop counters).
- **East Village (map 70) facilities** (door script -> interior map, counter script, service opcode): 2AEB5 -> 71
  appraiser, 2AEDF (`4F` choice, needs story var 0x93); 2B39D -> 72 inn, 2B3C4 (`B4 01` yes/no); 2B58B -> 73 weapon
  shop, 2B5C2 (`AF 0`); 2B61B -> 74 armor shop, 2B652 (`10 2`); 2FC5F -> 78 item shop, 2FC89 (`53 3`); 2C0EF -> 77
  guild (party recruit NPCs, `78` choice); 2B675 -> 75, 2B891 -> 76 houses. Shop menus: 買う/売る/鍛える/やめる.
- **魔賓館** (Vandel monster hall) = map 7A, map-load 305DA (no `77 45` prelude: works queued from an idle field, hangs as
  a warp target); reception タロトス counter 307CA: 道具売買 / モンスター売買 / モンスター腹心.
- Quest message routines 3C53E (クエストをあきらめます), 3C546 (クエストの終了条件を満たしました). Buster ending after the
  staff roll: 16770 `A0 00 01; 0F; 17 459` (clear data, then save) -> back to the title, which then offers
  Story (Buster / Vandel) / 通信 (wireless link: 通信受付 / 通信検索) / GBA link. Before a clear: Story (Buster) / GBA link.

## Insertion plan
Because text is reached only through absolute u32 operands, English can be **appended to the end of the file** and the
operands repointed; code offsets, jump targets and the data tail do not move (arm9 and quest.img hold rom.img
offsets). `tools/scr.py` gives the exact operand positions (`Script.refs`: string start -> [(pc, k)]), so only real
pointer operands are rewritten. Appended strings must stay 4-aligned (the pool rule; unproven whether the engine
needs it). The file is read from the cartridge, so its size is limited only by ROM space (see `rom.md`).
