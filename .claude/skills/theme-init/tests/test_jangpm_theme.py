"""The jangpm theme.json is the migration baseline. It must validate."""
import json
import subprocess
import sys
from pathlib import Path

# tests dir → theme-init → skills → .claude → repo root
REPO = Path(__file__).resolve().parents[4]
SKILL = Path(__file__).resolve().parents[1]
JANGPM_THEME = REPO / ".claude/skills/huashu-design/assets/design-systems/jangpm/theme.json"


def test_jangpm_theme_validates():
    """jangpm theme.json must conform to v1 token contract."""
    assert JANGPM_THEME.exists(), f"missing: {JANGPM_THEME}"
    r = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "validate_theme.py"),
         "--theme", str(JANGPM_THEME),
         "--contract", str(SKILL / "references" / "token-contract.json")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr


def test_jangpm_accent_is_indigo():
    """The defining jangpm accent — locked, must not drift."""
    theme = json.loads(JANGPM_THEME.read_text())
    assert theme["colors"]["accent"] == "#4633E3"
    assert theme["colors"]["accent-soft"] == "#E8E5FC"
    assert theme["colors"]["accent-ink"] == "#2E1FB3"


def test_jangpm_identity_fields():
    """Identity fields must be exact (used by downstream renderers)."""
    theme = json.loads(JANGPM_THEME.read_text())
    assert theme["name"] == "jangpm"
    assert theme["display_name"] == "Jangpm"
    assert theme["version"] == "1.0"
