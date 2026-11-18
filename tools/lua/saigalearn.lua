-- saigalearn.lua: open the Saiga learn-confirm prompt (ptr 021B424C-021B429C) on the Saiga screen.
-- UI state 24 (0x0203614C, Saiga screen) goes to state 25 when [[ui+0xCC]+0x38] == 6 (and +0x30, +0x34 are 0);
-- state 25 (0x02035F0C) then opens the prompt (state 26, object [ui+0xD4], drawn by 0x020CBD18) when the list
-- object [ui+0xD0] has a selected row (+0x34 != 0) and byte +0xBF == 1 (else it learns directly).
-- Use with scene menu_skills from frame SAIGA_FROM (default 4300), after the screen is up:
--   --script tools/debug/warp.lua --script tools/lua/saigalearn.lua --var "SCENE='menu_skills'" --frames 4700
local from, told = SAIGA_FROM or 4300, {}
local function once(k, s) if not told[k] then told[k] = true; L.log(s) end end
L.on_exec(0x020364B4, function() -- state 24, r2 = [ui+0xCC]
  if L.frame < from then return end
  local a = memory.getregister("arm9.r2") + 0x38
  once(1, string.format("SAIGA 24: %08X was %X now 6 f%d", a, memory.readdword(a), L.frame))
  memory.writedword(a, 6)
end)
L.on_exec(0x02035F18, function() -- state 25, r5 = ui
  local p = memory.readdword(memory.getregister("arm9.r5") + 0xD0)
  if p < 0x02000000 or p >= 0x02400000 then return end
  once(2, string.format("SAIGA 25: list %08X sel %X bf %X f%d", p, memory.readdword(p + 0x34),
    memory.readbyte(p + 0xBF), L.frame))
  memory.writebyte(p + 0xBF, 1)
  if memory.readdword(p + 0x34) == 0 then memory.writedword(p + 0x34, SAIGA_SEL or 1) end
end)
