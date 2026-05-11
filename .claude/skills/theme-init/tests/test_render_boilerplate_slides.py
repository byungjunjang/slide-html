"""Render all 8 jangpm boilerplate slides; output must match golden.

Same Level A / Level B equivalence pattern as the CSS tests.
"""
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
FIXTURES = SKILL / "tests" / "fixtures"
GOLDEN_DIR = FIXTURES / "golden" / "jangpm-boilerplate"


def _normalize(text: str) -> str:
    text = re.sub(r",\s*\n\s+", ", ", text)
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).rstrip()
        lines.append(line)
    return "\n".join(lines).strip()


def test_render_all_jangpm_boilerplate(tmp_path):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "render_boilerplate_slides.py"),
         "--theme", str(FIXTURES / "jangpm-theme.json"),
         "--out-dir", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr

    diffs = []
    for golden_file in sorted(GOLDEN_DIR.glob("*.html")):
        rendered_path = tmp_path / golden_file.name
        assert rendered_path.exists(), f"missing rendered: {golden_file.name}"
        rendered = rendered_path.read_text(encoding="utf-8").strip()
        golden = golden_file.read_text(encoding="utf-8").strip()
        if rendered == golden:
            continue
        if _normalize(rendered) == _normalize(golden):
            import difflib
            diff = "\n".join(difflib.unified_diff(
                golden.splitlines(), rendered.splitlines(),
                fromfile=f"golden/{golden_file.name}",
                tofile=f"rendered/{golden_file.name}",
                lineterm=""))
            print(f"\n[level B equivalence — cosmetic diff for {golden_file.name}]:\n{diff}\n")
            continue
        # material divergence
        import difflib
        diff = "\n".join(difflib.unified_diff(
            golden.splitlines(), rendered.splitlines(),
            fromfile=f"golden/{golden_file.name}",
            tofile=f"rendered/{golden_file.name}",
            lineterm=""))
        diffs.append(f"{golden_file.name}: material diff:\n{diff}")

    if diffs:
        raise AssertionError("\n\n".join(diffs))
