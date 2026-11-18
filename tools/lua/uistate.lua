-- Log changes of the field's two state machines: field state (dispatcher 0x0203123C, r0 = state) and the
-- bottom-screen UI state (dispatcher 0x0203B598, table 0x0219527C, r0 = state). Also logs script PC changes.
--   emu.py ROM --out DIR --state-in S --route-str ".." --script tools/lua/uistate.lua
local last_ui, last_fs, last_pc = -1, -1, -1
L.on_exec(0x0203B598, function()
  local s = memory.getregister("arm9.r0")
  if s ~= last_ui then L.log(string.format("f%d UI %d -> %d", L.frame, last_ui, s)); last_ui = s end
end)
L.on_exec(0x0203123C, function()
  local s = memory.getregister("arm9.r0")
  if s ~= last_fs then L.log(string.format("f%d FIELD %d -> %d", L.frame, last_fs, s)); last_fs = s end
end)
L.on_frame(function(n)
  local c = memory.readdword(0x021BEDAC)
  if c >= 0x02000000 and c < 0x02400000 then
    local pc = memory.readdword(c + 8)
    if pc ~= last_pc and math.abs(pc - last_pc) > 16 then
      L.log(string.format("f%d PC %05X", n, pc))
    end
    last_pc = pc
  end
end)
