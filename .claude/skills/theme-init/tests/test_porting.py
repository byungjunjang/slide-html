"""Smoke tests confirming the ported slide-svg scripts work standalone."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"


def test_fill_defaults_handles_minimal_input(tmp_path):
    """fill_theme_defaults populates monochrome defaults when given only a name."""
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({"name": "smoke"}))
    out = tmp_path / "out.json"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "fill_theme_defaults.py"),
         "--input", str(draft), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    filled = json.loads(out.read_text())
    assert filled["name"] == "smoke"
    assert filled["colors"]["bg"] == "#FAFAF9"  # safe default
    assert filled["version"] == "1.0"


def test_validate_accepts_filled_default(tmp_path):
    """A filled-from-empty theme should pass v1 contract validation."""
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({"name": "smoke"}))
    filled = tmp_path / "filled.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "fill_theme_defaults.py"),
         "--input", str(draft), "--out", str(filled)],
        check=True,
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_theme.py"),
         "--theme", str(filled),
         "--contract", str(SKILL / "references" / "token-contract.json")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr


def test_validate_rejects_invalid_hex(tmp_path):
    """Lowercase or 3-digit hex should fail validation."""
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({"name": "smoke", "colors": {"accent": "#abc"}}))
    filled = tmp_path / "filled.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "fill_theme_defaults.py"),
         "--input", str(draft), "--out", str(filled)],
        check=True,
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_theme.py"),
         "--theme", str(filled),
         "--contract", str(SKILL / "references" / "token-contract.json")],
        capture_output=True, text=True,
    )
    assert r.returncode == 1, "validator should reject 3-digit hex"
    assert "accent" in r.stderr


def test_presets_root_points_at_slide_design_systems():
    """PRESETS_ROOT must resolve to slide/assets/design-systems (not doubled .claude/.claude/...)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fill_theme_defaults",
        SKILL / "scripts" / "fill_theme_defaults.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    expected = SKILL.parent / "slide" / "assets" / "design-systems"
    assert mod.PRESETS_ROOT == expected, \
        f"PRESETS_ROOT={mod.PRESETS_ROOT}, expected {expected}"
    assert mod.PRESETS_ROOT.exists(), \
        f"PRESETS_ROOT does not exist: {mod.PRESETS_ROOT}"


def test_rem_filter_renders_pixel_to_rem():
    """The |rem filter divides by 16 and normalizes trailing zeros."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_token_render", SKILL / "scripts" / "_token_render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Integer px → clean rem
    assert mod.render("size: {{TOKEN:t.x|rem}};", {"t": {"x": 16}}) == "size: 1rem;"
    assert mod.render("size: {{TOKEN:t.x|rem}};", {"t": {"x": 56}}) == "size: 3.5rem;"
    # Fractional px (jangpm body 15.2px → 0.95rem)
    assert mod.render("size: {{TOKEN:t.x|rem}};", {"t": {"x": 15.2}}) == "size: 0.95rem;"
    # 4 spacing → 0.25rem
    assert mod.render("size: {{TOKEN:t.x|rem}};", {"t": {"x": 4}}) == "size: 0.25rem;"


def test_if_block_keeps_when_truthy():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_token_render", SKILL / "scripts" / "_token_render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.render("a{{IF:x.y}}<b>{{TOKEN:x.y}}</b>{{/IF}}c", {"x": {"y": "VAL"}})
    assert out == "a<b>VAL</b>c"


def test_if_block_strips_when_null():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_token_render", SKILL / "scripts" / "_token_render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.render("a{{IF:x.y}}<b>{{TOKEN:x.y}}</b>{{/IF}}c", {"x": {"y": None}})
    assert out == "ac"


def test_if_block_strips_when_missing():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_token_render", SKILL / "scripts" / "_token_render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.render("a{{IF:x.y}}<b>kept</b>{{/IF}}c", {})
    assert out == "ac"
