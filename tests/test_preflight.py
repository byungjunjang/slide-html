import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / ".claude/skills/slide/scripts/preflight.py"


def test_preflight_runs_and_reports(tmp_path):
    # Without --images it checks node deps + mirror; exit code is 0 or 1 but it
    # must run cleanly (no traceback) and print a summary line.
    r = subprocess.run([sys.executable, str(PREFLIGHT)], capture_output=True, text=True)
    assert r.returncode in (0, 1)
    assert "preflight" in (r.stdout + r.stderr).lower()
    assert "Traceback" not in r.stderr
