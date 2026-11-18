-- textlog.lua: text-coverage log for tools/textcov.py. Append after tools/debug/warp.lua (warp_all --script, or
-- emu.py --script twice); needs emu.py --debugger (exec hooks). Each line is logged once per run:
--   SCR <pc>          the script interpreter ran the opcode 70 (message) or 9E (speaker) handler with PC = pc, a file
--                     offset in the running script file (rom.img; textcov maps it to the string id through the
--                     original image: code offsets never move, only operands are repointed)
--   TAB <acc> <id>    an arm9 table accessor (get(id) leaf, tools/arm9text.py TABLES) was called with id in r0
-- Handlers: words at 0x02195490 + op*4 (docs/re/scripts.md §Interpreter state). Keep TEXT_ACCESSORS in step with
-- arm9text.TABLES (tests/test_textcov.py checks it).
local SCR_HANDLERS = { 0x0205128C, 0x0204F630 }
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
for _, a in ipairs(TEXT_ACCESSORS) do
  L.on_exec(a, function() once(string.format("TAB %X %X", a, memory.getregister("arm9.r0"))) end)
end
