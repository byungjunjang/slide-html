"""Rendering with jangpm theme.json must reproduce the golden CSS.

Two equivalence levels (Level A preferred, Level B fallback):
- A: byte-equal after .strip()
- B: normalized — collapse internal whitespace runs, strip trailing whitespace per line
"""
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
SCRIPTS = SKILL / "scripts"
FIXTURES = SKILL / "tests" / "fixtures"
GOLDEN = FIXTURES / "golden" / "jangpm-colors_and_type.css"
JANGPM_FONTS = REPO / ".claude/skills/slide/assets/design-systems/jangpm/_fonts.css"


def _normalize(text: str) -> str:
    """Level B: collapse whitespace runs, strip trailing space per line.

    Also folds CSS continuation lines (a property value broken across multiple
    lines after a comma) into a single line so that wrapped vs. unwrapped
    font chains compare equal.
    """
    # Fold continuation lines: ",\n   stuff" → ", stuff"
    text = re.sub(r",\n\s+", ", ", text)
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).rstrip()
        lines.append(line)
    return "\n".join(lines).strip()


def test_render_jangpm_colors_and_type(tmp_path):
    out = tmp_path / "rendered.css"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "render_colors_and_type.py"),
         "--theme", str(FIXTURES / "jangpm-theme.json"),
         "--fonts-prelude", str(JANGPM_FONTS),
         "--out", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    rendered = out.read_text(encoding="utf-8").strip()
    golden = GOLDEN.read_text(encoding="utf-8").strip()

    if rendered == golden:
        return  # Level A pass

    # Level B fallback
    if _normalize(rendered) == _normalize(golden):
        # Pass with cosmetic divergence — surface it in stdout for the human to see
        import difflib
        diff = "\n".join(difflib.unified_diff(
            golden.splitlines(), rendered.splitlines(),
            fromfile="golden", tofile="rendered", lineterm=""))
        print(f"\n[level B equivalence — cosmetic diff]:\n{diff}\n")
        return

    # Material divergence — fail with diff
    import difflib
    diff = "\n".join(difflib.unified_diff(
        golden.splitlines(), rendered.splitlines(),
        fromfile="golden", tofile="rendered", lineterm=""))
    raise AssertionError(f"render diverged from golden (material):\n{diff}")
