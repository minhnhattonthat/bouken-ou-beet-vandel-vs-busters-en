-- Setup check: proves --script hooks run and L.log reaches log.txt (emu.py --script tools/lua/probe_hello.lua).
L.on_frame(function(n)
  if n == 60 then
    L.log(string.format("probe ok frame %d arm9 word0 %08X", n, memory.readdword(0x02000000)))
  end
end)
