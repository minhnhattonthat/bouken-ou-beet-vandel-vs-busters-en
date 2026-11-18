-- Id sweep (text coverage): every call of one arm9 table accessor gets the next record id in r0, so the game
-- itself fetches and draws record after record on the screen that normally shows one (battle shouts, names...).
-- Append after warp.lua and BEFORE textlog.lua (hooks on one address run in registration order, so textlog's TAB
-- line then records the forced id), e.g. for the battle shouts (accessor 0x020140B0, 81 records) in a long
-- god-mode battle:
--   emu.py build/beet_en.nds --debugger --out work/qa/p8_shout --script tools/debug/warp.lua
--     --script tools/lua/idloop.lua --script tools/lua/textlog.lua --var "SCENE='v14_battle7'"
--     --var "IDLOOP_ACC=0x020140B0" --var "IDLOOP_FROM=1" --var "IDLOOP_N=81" --var "GOD_WIN=100000" --frames 30000
-- (one shout every ~350 frames; the shout accessor is 1-based: id 0 reads before the table and draws junk in the
-- original too). Check the accessor's first id in tools/textcov.py first_id() before choosing IDLOOP_FROM.
-- Globals: IDLOOP_ACC (accessor address, or the address where r0 holds the id), IDLOOP_REG (default "r0"),
-- IDLOOP_FROM (first id, default 0), IDLOOP_N (count), IDLOOP_AFTER (frame before which calls are left alone,
-- default 0). Logs IDLOOP <id> f<frame> per forced call; after the last id calls are left alone.
-- A second, independent hook: the same globals with the prefix IDLOOP2_ (e.g. force a branch flag at one pc and a
-- result code at a later one: the boot save-load failure, docs/status.md session 20).
local function hook(acc, reg, from, n, after, tag)
  reg = "arm9." .. (reg or "r0")
  from, n, after = from or 0, n or 1, after or 0
  local k = 0
  L.on_exec(acc, function()
    if k < n and L.frame >= after then
      local id = from + k
      memory.setregister(reg, id)
      L.log(string.format("%s %X f%d", tag, id, L.frame))
      k = k + 1
    end
  end)
end
if IDLOOP_ACC then hook(IDLOOP_ACC, IDLOOP_REG, IDLOOP_FROM, IDLOOP_N, IDLOOP_AFTER, "IDLOOP") end
if IDLOOP2_ACC then hook(IDLOOP2_ACC, IDLOOP2_REG, IDLOOP2_FROM, IDLOOP2_N, IDLOOP2_AFTER, "IDLOOP2") end
