-- textlog.lua: text-coverage log for tools/textcov.py. Append after tools/debug/warp.lua (warp_all --script, or
-- emu.py --script twice); needs emu.py --debugger (exec hooks). Each line is logged once per run:
--   SCR <pc>          the script interpreter ran the opcode 70 (message) or 9E (speaker) handler with PC = pc, a file
--                     offset in the running script file (rom.img; textcov maps it to the string id through the
--                     original image: code offsets never move, only operands are repointed)
--   QST <pc>          the quest.img interpreter ran a string opcode (20 title, 1A/2D description) at pc
--   TAB <acc> <id>    an arm9 table accessor (get(id) leaf, tools/arm9text.py TABLES) was called with id in r0
-- Handlers: words at 0x02195490 + op*4 (docs/re/scripts.md §Interpreter state). Keep TEXT_ACCESSORS in step with
-- arm9text.TABLES (tests/test_textcov.py checks it).
-- Also 4F (quest offer, 0x02053080) and 99 (quest update, 0x0204FAFC): their place / client operands (+13/+17,
-- +5/+9) are what the Quest Detail screen draws as Location / Requester (work/qa/cover/qrand_quest_counter).
local SCR_HANDLERS = { 0x0205128C, 0x0204F630, 0x02053080, 0x0204FAFC }
local TEXT_ACCESSORS = {
  0x02014040, 0x020140B0, 0x020140DC, 0x020140F4, 0x0201419C, 0x02014200, 0x0201421C, 0x02014234, 0x020142C8,
  0x020142E0, 0x020145D8, 0x020145F0, 0x02014608, 0x02014628, 0x0201466C, 0x02014684, 0x020146CC, 0x020146E0,
}
local seen = {}
local function once(s)
  if not seen[s] then seen[s] = true; L.log(s) end
end
for _, h in ipairs(SCR_HANDLERS) do
  L.on_exec(h, function()
    local ctx = memory.readdword(0x021BEDAC)
    if ctx ~= 0 then once(string.format("SCR %X", memory.readdword(ctx + 8))) end
  end)
end
-- quest.img interpreter (loop 0x020111D0, ctx [0x021BA39C], ctx+8 = PC): handlers of 20 (title) 0x02011F70,
-- 1A (description) 0x020123E0, 2D (description) 0x020116F4 (table 0x0210D36C)
--   QST <pc>          a quest.img string opcode ran at file offset pc
for _, h in ipairs({ 0x02011F70, 0x020123E0, 0x020116F4 }) do
  L.on_exec(h, function()
    local q = memory.readdword(0x021BA39C)
    if q >= 0x02000000 and q < 0x02400000 then once(string.format("QST %X", memory.readdword(q + 8))) end
  end)
end
-- arm9 pointer strings (script/arm9/ptr.json): a read of one of their pointer words (literal-pool or table words,
-- which never move; the inserter only changes their value) = the code fetched that string
--   PTR <word>        a pointer word was read
do
  local root = OUT and OUT:match("^(.*)[/\\]work[/\\]")
  local f = io.open(PTR_JSON or ((root or ".") .. "/script/arm9/ptr.json"), "r")
  if f then
    local src = f:read("*a"); f:close()
    local n = 0
    for list in src:gmatch('"ptrs"%s*:%s*%[(.-)%]') do
      for w in list:gmatch('(%x%x%x%x%x%x%x%x)') do
        local a = tonumber(w, 16)
        L.on_read(a, a + 3, function() once(string.format("PTR %X", a)) end)
        n = n + 1
      end
    end
    L.log("textlog: " .. n .. " pointer words watched")
  else
    L.log("textlog: ptr.json not found, no PTR lines")
  end
end
-- generic buster names (status/bustername/busterman.bin / busterwoman.bin, 128 x 22-byte records): 0x02019590..
-- opens the file (types 0x11-0x1F man at 0x020195C8, 0x20-0x33 woman at 0x020195F0), picks a random index
-- (bl 0x0201A938 returns at 0x02019608 with r0 = index) and reads that record into the new buster
--   NAM <m|w> <index> a generic buster got that name (script/names.json name.m<idx> / name.w<idx>)
do
  local sex = nil
  L.on_exec(0x020195C8, function() sex = "m" end)
  L.on_exec(0x020195F0, function() sex = "w" end)
  L.on_exec(0x02019608, function()
    if sex then once(string.format("NAM %s %d", sex, memory.getregister("arm9.r0"))) end
  end)
end
for _, a in ipairs(TEXT_ACCESSORS) do
  L.on_exec(a, function() once(string.format("TAB %X %X", a, memory.getregister("arm9.r0"))) end)
end
