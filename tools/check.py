"""check.py: the repo's one-command check (text lint + tests). The pre-commit hook runs this.

Exit code is non-zero if the lint (tools/lint.py) or pytest fails: that blocks the commit."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    lint = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools" / "lint.py")], cwd=ROOT)
    tests = subprocess.run([sys.executable, "-X", "utf8", "-m", "pytest", "-q", str(ROOT / "tests")], cwd=ROOT)
    sys.exit(lint.returncode or tests.returncode)
