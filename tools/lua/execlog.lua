-- execlog.lua: log frame, r0-r3 and lr each time one of the EXEC_AT addresses runs (max EXEC_MAX lines, default 50).
--   emu.py ROM --script tools/debug/warp.lua --script tools/lua/execlog.lua --var "SCENE='x'" --var "EXEC_AT={0x02065504}"
local frame, n, max = 0, 0, EXEC_MAX or 50
L.on_frame(function(f) frame = f end)
for _, a in ipairs(EXEC_AT or {}) do
  L.on_exec(a, function()
    n = n + 1
    if n > max then return end
    L.log(string.format("EXEC %08X f%d r0 %08X r1 %08X r2 %08X r3 %08X lr %08X", a, frame,
      memory.getregister("arm9.r0"), memory.getregister("arm9.r1"), memory.getregister("arm9.r2"),
      memory.getregister("arm9.r3"), memory.getregister("arm9.r14")))
  end)
end
