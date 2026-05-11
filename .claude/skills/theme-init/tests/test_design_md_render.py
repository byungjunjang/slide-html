"""DESIGN.md draft renderer must populate frontmatter, all 10 sections, and tokens."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


def _minimal_theme() -> dict:
    return {
        "version": "1.0",
        "name": "testpreset",
        "display_name": "Test Preset",
        "description": "Minimal fixture deck — warm neutral base with single accent.",
        "colors": {
            "bg":             "#FAFAF9",
            "surface":        "#FFFFFF",
            "surface-alt":    "#F5F5F4",
            "text":           "#1A1A1A",
            "text-secondary": "#6B7280",
            "text-tertiary":  "#9CA3AF",
            "border":         "#E5E7EB",
            "border-strong":  "#D4D4D4",
            "accent":         "#4633E3",
            "accent-soft":    "#E8E5FC",
            "accent-ink":     "#2E1FB3",
            "positive":       "#059669",
            "negative":       "#E11D48",
            "warning":        "#D97706",
        },
        "assets": {
            "icon-pack-default": "tabler-outline",
            "icon-pack-fallback": "tabler-filled",
        },
    }


def test_design_md_renders_full_template(tmp_path):
    theme_path = tmp_path / "theme.json"
    theme_path.write_text(json.dumps(_minimal_theme()), encoding="utf-8")
    out = tmp_path / "DESIGN.md"

    r = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "render_design_md.py"),
         "--theme", str(theme_path),
         "--out", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert out.exists()
    body = out.read_text(encoding="utf-8")

    # Frontmatter status
    assert "status: draft" in body

    # All 10 numbered sections
    assert "## 1. Visual theme & atmosphere" in body
    assert "## 2. Palette & contrast behavior" in body
    assert "## 3. Typography hierarchy" in body
    assert "## 4. Spacing & density" in body
    assert "## 5. Layout grammar" in body
    assert "## 6. Header / body / footer structure" in body
    assert "## 7. Title / body / end page flow" in body
    assert "## 8. Chart / table treatment" in body
    assert "## 9. Icon system" in body
    assert "## 10. Anti-patterns" in body

    # No unrendered placeholders left
    assert "{{TOKEN:" not in body

    # Description token substituted
    assert "Minimal fixture deck — warm neutral base with single accent." in body
