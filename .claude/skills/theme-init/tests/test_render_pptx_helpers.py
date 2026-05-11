"""Rendering with jangpm theme.json must reproduce the current _pptx-slide.css.

Same Level A / Level B equivalence pattern as test_render_colors_and_type.py.
"""
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
FIXTURES = SKILL / "tests" / "fixtures"
GOLDEN = FIXTURES / "golden" / "jangpm-_pptx-slide.css"


def _normalize(text: str) -> str:
    """Collapse internal whitespace; fold CSS continuation lines (',\\n   ' → ', ')."""
    text = re.sub(r",\s*\n\s+", ", ", text)
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).rstrip()
        lines.append(line)
    return "\n".join(lines).strip()


def test_render_jangpm_pptx_helpers(tmp_path):
    out = tmp_path / "rendered.css"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "render_pptx_helpers.py"),
         "--theme", str(FIXTURES / "jangpm-theme.json"),
         "--out", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    rendered = out.read_text(encoding="utf-8").strip()
    golden = GOLDEN.read_text(encoding="utf-8").strip()

    if rendered == golden:
        return  # Level A pass

    if _normalize(rendered) == _normalize(golden):
        import difflib
        diff = "\n".join(difflib.unified_diff(
            golden.splitlines(), rendered.splitlines(),
            fromfile="golden", tofile="rendered", lineterm=""))
        print(f"\n[level B equivalence — cosmetic diff]:\n{diff}\n")
        return

    import difflib
    diff = "\n".join(difflib.unified_diff(
        golden.splitlines(), rendered.splitlines(),
        fromfile="golden", tofile="rendered", lineterm=""))
    raise AssertionError(f"render diverged from golden (material):\n{diff}")
