-- winlog.lua: log every text-window init (0x02021124: r0 window, r3 x, [sp] y, [sp+4] w, [sp+8] h, tiles) with
-- its caller, e.g. to find which code builds a screen's windows:
--   emu.py ROM --script tools/debug/warp.lua --script tools/lua/winlog.lua --var "SCENE='menu_monsters'" --debugger
local frame = 0
L.on_frame(function(n) frame = n end)
L.on_exec(0x02021124, function()
  local sp = memory.getregister("arm9.r13")
  L.log(string.format("WININIT f%d lr %08X win %08X x %d y %d w %d h %d", frame,
    memory.getregister("arm9.r14"), memory.getregister("arm9.r0"), memory.getregister("arm9.r3"),
    memory.readword(sp), memory.readword(sp + 4), memory.readword(sp + 8)))
end)
-- 0x0200D744 (r1 window, [sp] -> rect of u16 x,y,w,h): the path screens like the monster book use
L.on_exec(0x0200D744, function()
  local rect = memory.readdword(memory.getregister("arm9.r13"))
  L.log(string.format("WINRECT f%d lr %08X win %08X rect %08X x %d y %d w %d h %d", frame,
    memory.getregister("arm9.r14"), memory.getregister("arm9.r1"), rect, memory.readword(rect),
    memory.readword(rect + 2), memory.readword(rect + 4), memory.readword(rect + 6)))
end)
-- WIN_WATCH=0xADDR: also log the pc and lr of every write to that halfword (a window's x field, from windump.lua)
if WIN_WATCH then
  L.on_write(WIN_WATCH, WIN_WATCH + 1, function()
    L.log(string.format("WINWRITE f%d pc %08X lr %08X val %04X", frame, L.pc(),
      memory.getregister("arm9.r14"), memory.readword(WIN_WATCH)))
  end)
end
