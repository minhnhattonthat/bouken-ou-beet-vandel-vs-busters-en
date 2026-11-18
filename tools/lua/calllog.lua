-- Log calls of FN (global, default 0x02020240 = 12px string draw): lr, r0-r3, once per distinct (lr, r1, r2).
local fn = FN or 0x02020240
local seen, frame = {}, 0
L.on_frame(function(n) frame = n end)
L.on_exec(fn, function()
  local g = function(r) return memory.getregister("arm9." .. r) end
  local k = string.format("%08X %d %d", g("r14"), g("r1"), g("r2"))
  if not seen[k] then
    seen[k] = true
    L.log(string.format("f%d CALL %08X lr=%08X r0=%08X r1=%d r2=%d r3=%08X", frame, fn, g("r14"), g("r0"), g("r1"),
      g("r2"), g("r3")))
  end
end)
