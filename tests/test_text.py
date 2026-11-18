"""Text encoding: the table matches the verified known line, and tbl/jp.tbl is what tools/mktbl.py generates."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import mktbl  # noqa: E402
from tbl import Table  # noqa: E402

# field/script/rom.img @0xC88, shown on screen in the first ship scene (docs/re/text.md)
KNOWN = bytes.fromhex("5c0120010100810831013a010a0070ff26016d014a0166010a0072ff")


def test_known_line_decodes():
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    text, used = t.decode(KNOWN, 0, len(KNOWN))
    assert text.startswith("もう　少しだ！")
    assert text.endswith("{br}がんばれ！{page}")
    assert t.encode(text) == KNOWN


def test_table_is_generated():
    want = "\n".join(mktbl.lines()) + "\n"
    assert (ROOT / "tbl" / "jp.tbl").read_text(encoding="utf-8") == want
