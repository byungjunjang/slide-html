"""End-to-end: a partial draft → a complete preset folder."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL / "tests" / "fixtures"


def test_init_theme_creates_full_preset(tmp_path):
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({
        "name": "test-warm",
        "display_name": "Test Warm",
        "description": "Test preset for theme-init e2e.",
        "colors": {
            "accent": "#DC2626",
            "accent-soft": "#FEE2E2",
            "accent-ink": "#991B1B"
        },
        "voice": {"tone": "test", "pov": "test", "register": "test"}
    }))
    presets_root = tmp_path / "presets"
    r = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "init_theme.py"),
         "--from", str(draft),
         "--preset", "test-warm",
         "--presets-root", str(presets_root)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"stderr:\n{r.stderr}\nstdout:\n{r.stdout}"

    out = presets_root / "test-warm"
    assert (out / "theme.json").exists()
    assert (out / "colors_and_type.css").exists()
    assert (out / "_pptx-slide.css").exists()
    assert (out / "brand-spec-generated.md").exists()
    boilerplate = sorted((out / "pptx-boilerplate").glob("*.html"))
    # 8 originals + 15 Phase 1 Minor + 10 Phase 2 Moderate + 4 Phase 3 Major = 37
    assert len(boilerplate) == 37

    # Accent color must propagate to _pptx-slide.css
    pptx_css = (out / "_pptx-slide.css").read_text()
    assert "#DC2626" in pptx_css

    # And to colors_and_type.css
    cct = (out / "colors_and_type.css").read_text()
    assert "#DC2626" in cct

    # And to brand-spec-generated.md
    brand = (out / "brand-spec-generated.md").read_text()
    assert "#DC2626" in brand
    assert "Test Warm" in brand

    # Header comment present in colors_and_type.css (auto-generated for new presets)
    assert "Test Warm" in cct
    assert "Slide Design System" in cct


def test_init_theme_refuses_to_overwrite_without_force(tmp_path):
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({"name": "overwrite-test", "voice": {"tone": "x", "pov": "x", "register": "x"}}))
    presets_root = tmp_path / "presets"

    # First run succeeds
    r1 = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "init_theme.py"),
         "--from", str(draft),
         "--preset", "overwrite-test",
         "--presets-root", str(presets_root)],
        capture_output=True, text=True,
    )
    assert r1.returncode == 0, r1.stderr

    # Second run without --force fails
    r2 = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "init_theme.py"),
         "--from", str(draft),
         "--preset", "overwrite-test",
         "--presets-root", str(presets_root)],
        capture_output=True, text=True,
    )
    assert r2.returncode != 0, "second run should refuse without --force"
    assert "already exists" in r2.stderr.lower() or "already exists" in r2.stdout.lower()

    # Third run with --force succeeds
    r3 = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "init_theme.py"),
         "--from", str(draft),
         "--preset", "overwrite-test",
         "--presets-root", str(presets_root),
         "--force"],
        capture_output=True, text=True,
    )
    assert r3.returncode == 0, r3.stderr
