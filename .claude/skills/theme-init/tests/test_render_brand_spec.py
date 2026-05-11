"""brand-spec-generated.md must contain the key tokens from theme.json."""
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL / "tests" / "fixtures"


def test_brand_spec_contains_key_tokens(tmp_path):
    out = tmp_path / "brand.md"
    r = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "render_brand_spec.py"),
         "--theme", str(FIXTURES / "jangpm-theme.json"),
         "--out", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    body = out.read_text(encoding="utf-8")
    # Identity
    assert "Jangpm" in body
    # All accent tokens cited
    for hex_val in ("#4633E3", "#E8E5FC", "#2E1FB3"):
        assert hex_val in body
    # Voice section
    assert "editorial, analytical, declarative" in body
    # Forbidden phrases listed
    assert "여러분" in body
    # Provenance footer
    assert "/theme-init" in body
