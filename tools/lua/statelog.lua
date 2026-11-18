-- Log state changes of the game-mode state machine: dispatcher 0x0209EB90(state=r0, obj=r1) calls
-- table 0x021957E4[state] (37 entries). Needs --debugger (exec hook on a function entry). docs/re/scripts.md §State.
local last = -1
L.on_exec(0x0209EB90, function()
  local s = memory.getregister("arm9.r0")
  if s ~= last then
    L.log(string.format("f%d state %d (obj %08X lr %08X)", L.frame, s, memory.getregister("arm9.r1"),
      memory.getregister("arm9.r14")))
    last = s
  end
end)
