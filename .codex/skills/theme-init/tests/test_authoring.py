"""Phase 2 (Layout Authoring) harness regression tests.

Covers the deterministic pieces: classification SSOT, .stock snapshot/restore,
manifest lifecycle, and that init_theme.py wires snapshot + manifest in without
disturbing the 37-file token-render output.
"""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))
import _authoring_common as ac  # noqa: E402


def _init_preset(tmp_path) -> Path:
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({
        "name": "auth-test",
        "display_name": "Auth Test",
        "description": "Phase 2 test preset.",
        "colors": {"accent": "#7C3AED", "accent-soft": "#EDE9FE", "accent-ink": "#5B21B6"},
        "voice": {"tone": "t", "pov": "t", "register": "t"},
    }))
    presets_root = tmp_path / "presets"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "init_theme.py"),
         "--from", str(draft), "--preset", "auth-test",
         "--presets-root", str(presets_root)],
        capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, f"{r.stderr}\n{r.stdout}"
    return presets_root / "auth-test"


def test_init_theme_creates_stock_and_manifest(tmp_path):
    preset = _init_preset(tmp_path)
    bp = preset / "pptx-boilerplate"

    # token-render output is intact: 37 html files (non-recursive)
    assert len(sorted(bp.glob("*.html"))) == 37

    # .stock snapshot mirrors the 37 files
    stock = bp / ac.STOCK_DIRNAME
    assert stock.is_dir()
    assert len(sorted(stock.glob("*.html"))) == 37

    # manifest exists, classifies, status not_authored
    m = ac.load_manifest(bp)
    assert m is not None
    assert m["status"] == "not_authored"
    assert "cover" in m["identity_set"]
    assert "01-title" in m["identity_set"]["cover"]
    # a data slide is NOT in any identity family
    assert "06-table" in m["data_set"]
    assert "16-stats" not in m["data_set"]  # hero-impact identity


def test_classify_partition_is_complete_and_disjoint(tmp_path):
    preset = _init_preset(tmp_path)
    bp = preset / "pptx-boilerplate"
    cls = ac.classify(bp)
    identity = set(cls["identity_flat"])
    data = set(cls["data_set"])
    allf = set(p.stem for p in bp.glob("*.html"))
    assert identity.isdisjoint(data)
    assert identity | data == allf  # complete partition


def test_restore_from_stock_roundtrip(tmp_path):
    preset = _init_preset(tmp_path)
    bp = preset / "pptx-boilerplate"
    target = bp / "01-title.html"
    original = target.read_text(encoding="utf-8")

    # simulate authoring: clobber the identity slide
    target.write_text("<!doctype html><html><body><p>authored</p></body></html>", encoding="utf-8")
    assert target.read_text(encoding="utf-8") != original

    restored = ac.restore_from_stock(bp, ["01-title"])
    assert restored == ["01-title"]
    assert target.read_text(encoding="utf-8") == original  # byte-identical baseline


def test_manifest_lifecycle(tmp_path):
    preset = _init_preset(tmp_path)
    bp = preset / "pptx-boilerplate"
    m = ac.ensure_manifest("auth-test", bp)
    m["status"] = "draft"
    m["authored"] = ["01-title"]
    ac.save_manifest(bp, m)
    reloaded = ac.load_manifest(bp)
    assert reloaded["status"] == "draft"
    assert reloaded["authored"] == ["01-title"]


def test_reference_block_reseed_survives_windows_paths(tmp_path):
    """Re-seeding the DESIGN.md reference block must not crash when the source
    path contains backslashes (Windows). Regression: the idempotent re.sub
    replacement used to treat `\\d`, `\\U`… in the path as invalid escapes."""
    import argparse
    import author_layouts as al

    preset_dir = tmp_path / "auth-test"
    preset_dir.mkdir()
    design = preset_dir / "DESIGN.md"
    design.write_text("---\nstatus: draft\n---\n\n## 5. Visual vocabulary\n\n(LLM 추출 자리)\n",
                      encoding="utf-8")
    args = argparse.Namespace(presets_root=tmp_path, preset="auth-test")
    result = {
        "source": "output\\deck-pptx",          # Windows str(Path(...)) → backslash
        "slides_analyzed": 5,
        "devices": {
            "card_style": {"value": "hairline", "confidence": "high", "evidence": "x"},
            "surface_alternation": {"present": True, "slides_using": 2, "ratio": 0.4},
            "hairline_dividers": {"present": True, "count": 9},
            "cta": {"present": True, "count": 2},
            "kicker": {"present": True, "count": 14},
        },
    }
    al._seed_design_from_reference(args, result)   # first run → string-insert branch
    al._seed_design_from_reference(args, result)   # second run → re.sub branch (must not raise)

    body = design.read_text(encoding="utf-8")
    assert body.count(al._REF_BLOCK_START) == 1    # idempotent: exactly one block
    assert body.count(al._REF_BLOCK_END) == 1
    assert "output\\deck-pptx" in body             # backslash path preserved verbatim
