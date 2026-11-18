"""ROM pin: the dump in rom/ must match rom.sha1 (skips when no ROM is present, e.g. on a fresh clone)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

ROM = ROOT / "rom" / "Bouken-ou Beet - Vandel vs. Busters (Japan).nds"


@pytest.mark.skipif(not ROM.is_file(), reason="no ROM dump in rom/")
def test_rom_matches_pin():
    import check_rom
    check_rom.check()


def test_tools_import():
    import tbl  # noqa: F401  build-chain helpers must import without the skill installed
    import bps  # noqa: F401
