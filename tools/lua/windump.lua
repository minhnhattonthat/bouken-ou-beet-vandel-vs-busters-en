-- windump.lua: log the text-window structs of the current UI screen ([[0x021BEDA0]+4] + n*0x20) at frame WIN_AT
-- (default 3990) as hex words. Use with a warp:
--   emu.py ROM --script tools/debug/warp.lua --script tools/lua/windump.lua --var "SCENE='menu_monsters'" --debugger
local at = WIN_AT or 3990
local n_win = WIN_N or 16
L.on_frame(function(f)
  if f ~= at then return end
  local ui = memory.readdword(0x021BEDA0)
  local base = memory.readdword(ui + 4)
  L.log(string.format("WINBASE %08X", base))
  for i = 0, n_win - 1 do
    local a = base + i * 0x20
    local t = {}
    for k = 0, 7 do t[#t + 1] = string.format("%08X", memory.readdword(a + k * 4)) end
    L.log(string.format("WIN +%03X %s", i * 0x20, table.concat(t, " ")))
  end
end)
