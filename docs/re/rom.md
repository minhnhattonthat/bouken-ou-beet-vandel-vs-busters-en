# ROM layout, filesystem, free space

- 32 MiB cartridge (capacity byte 8), header used size 0x1E61860, so 0x19E7A0 (~1.6 MiB) is free past the last file;
  the ROM can also grow to 64 MiB. NitroFS rebuild with ndspy (mind the `platform-nds.md` notes: restore
  `orig[0x1000:0x1004]` and pad to the original size for the identity test).
- Identity rebuild (`tools/build.py`): file order and offsets match ndspy's layout exactly; the only differences are
  the 0x1000 word, 0x00 padding between regions (ndspy writes 0xFF; 2,118 gaps) and the 0xFF tail to 32 MiB.
- arm9 at ROM 0x4000, entry 0x02000800, uncompressed, no overlays; arm7 0x27778 bytes.
- 2,494 FAT entries (`tools/romls.py` lists them; `--unpack work/fs` writes them out). Top-level dirs: armor, battle
  (790 files, 13.9 MB), bg, bitmap, enemy, field (516, 9.5 MB), font, item, palette, quest, saiga, screen (571), skill,
  sound, status, tengeki, texture, weapon, world, plus root `kanakan.img`.
- Compression: only 18 files start with an LZ10 byte; arm9 and the text files are raw. No NARC archives; the `.img`
  files are game-specific containers (`scr\x1a` for scripts; battle/field `.img` are graphics banks, format TBD).
