-- Who writes a range of the save struct ([0x021BA3A0] + SW_LO .. + SW_HI)? The struct's base is fixed after boot,
-- so give it as SW_BASE (log it first with SW_BASE unset: one "SAVEBASE <addr>" line at frame SW_AT, default 1500).
-- One line per distinct pc: frame, pc, lr, address, r0-r3.
--   --script tools/lua/savewatch.lua --var SW_BASE=0x0219F7C0 --var SW_LO=0x11E0 --var SW_HI=0x136B [--var FROM=1500]
-- e.g. the weapon region (save+0x11E0, [id+1, 1, 0, 0] per weapon) during a shop buy finds the add-item routine.
local base, from = SW_BASE, FROM or 0
if not base then
  L.on_frame(function(f)
    if f == (SW_AT or 1500) then L.log(string.format("SAVEBASE %08X", memory.readdword(0x021BA3A0))) end
  end)
  return
end
local seen = {}
L.on_write(base + (SW_LO or 0), base + (SW_HI or 0x159B), function(addr)
  if L.frame < from then return end
  local pc = L.pc()
  if seen[pc] then return end
  seen[pc] = true
  local r = function(n) return memory.getregister("arm9.r" .. n) end
  L.log(string.format("f%d pc=%08X lr=%08X addr=%08X (save+%X) r0=%X r1=%X r2=%X r3=%X", L.frame, pc,
    r(14), addr, addr - base, r(0), r(1), r(2), r(3)))
end)
