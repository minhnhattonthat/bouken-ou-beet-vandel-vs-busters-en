-- Log every call of the accessors in FNS (global, comma-separated hex string, e.g. "0x0201419C,0x020142E0"): frame,
-- address, lr and r0, up to CALLCOUNT_MAX lines (default 400). Tells when and how often a screen fetches a record, to
-- pick IDLOOP_AFTER / IDLOOP_HOLD for idloop.lua.
local max = CALLCOUNT_MAX or 400
local n, frame = 0, 0
L.on_frame(function(f) frame = f end)
for a in string.gmatch(FNS or "", "[^,]+") do
  local addr = tonumber(a)
  L.on_exec(addr, function()
    if n < max then
      n = n + 1
      L.log(string.format("f%d CALL %08X lr=%08X r0=%X", frame, addr, memory.getregister("arm9.r14"),
        memory.getregister("arm9.r0")))
    end
  end)
end
