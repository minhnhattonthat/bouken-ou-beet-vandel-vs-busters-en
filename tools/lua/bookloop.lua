-- Book sweep (text coverage): reopen an Info-screen book again and again, each time with the entry it opens on
-- forced, so every record of the table is drawn once. Run after warp.lua on a scene that has the book open
-- (menu_monsters / menu_busters / menu_vandels), e.g.
--   warp_all.py --only book_monsters  (scenes.tsv sets BOOK via the scene name: see BOOKS below)
-- The book objects are built at 0x0202F0E4 (monster, [ui+0x6C], start entry r4 -> [obj+0x48]), 0x0202EFEC
-- (buster, [ui+0x74], r4 -> [obj+0x58] halfword) and 0x0202F068 (vandel, [ui+0x70], r4 -> [obj+0x38] halfword).
-- The hook sits on the block after the allocator call (0x..108 / 0x..010 / 0x..08C), where r4 still holds the
-- entry, and replaces it with the next id. Inputs: Back (t240,176) then the book's Info button, every PERIOD frames.
-- Logs BOOKLOOP <kind> <id> per open; textlog.lua's TAB lines are the coverage record.
-- Buster/vandel: the book shows the entries of a list the Info screen builds ([[ui+0x74]+0x4C] / [[ui+0x70]+0x40],
-- empty = -1 early in the story; warp.lua's `books` cheat sets entry 0 to 0, which draws an empty page). Here the
-- list hook (after warp.lua's, same return addresses) writes the table id instead (0x15E.. / 0x13F.., the
-- accessors' first ids), and r4 (the start index) stays as the game set it.
local BOOKS = {
  monster = { hook = 0x0202F108, btn = "t180,64", from = 0, n = 319 },
  buster  = { list = 0x02039A3C, field = 0x74, off = 0x4C, btn = "t76,120", from = 0x15E, n = 51 },
  vandel  = { list = 0x0203990C, field = 0x70, off = 0x40, btn = "t180,120", from = 0x13F, n = 31 },
}
local scene = SCENE or ""
local kind = BOOK or scene:match("^book_(%a+)s$")
local b = BOOKS[kind or ""]
if b then
  local from, n = BOOK_FROM or b.from, BOOK_N or b.n
  local start = BOOK_START or 4300          -- first reopen (the scene opens the book itself at ~4128)
  local period = BOOK_PERIOD or 150
  local k, armed = 0, false
  L.on_exec(b.hook or b.list, function()
    if armed and k <= n then
      local id = from + k - 1
      if b.hook then
        memory.setregister("arm9.r4", id)
      else
        local lst = memory.readdword(memory.getregister("arm9.r4") + b.field)
        if lst < 0x02000000 or lst >= 0x02400000 then return end
        memory.writedword(lst + b.off, id)
      end
      L.log(string.format("BOOKLOOP %s %X f%d", kind, id, L.frame))
      armed = false
    end
  end)
  L.on_frame(function(f)
    if f >= start and (f - start) % period == 0 and k < n then
      k = k + 1
      armed = true
      L.press("t240,176", 6); L.press("-", 50); L.press(b.btn, 6); L.press("-", 30)
    end
  end)
end
