"""Phase 2 final-boilerplate single-HTML review gate.

Covers the mandatory user-approval checkpoint that sits between `validate` and
`confirm`: the live-iframe contact sheet generator, the boilerplate digest used
as a drift guard, and the `confirm` gate that refuses until the user approves.
"""
import argparse
import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))
import _authoring_common as ac  # noqa: E402


def _mini_boilerplate(tmp_path, stems=("01-title", "06-table", "16-stats")) -> Path:
    """A minimal pptx-boilerplate dir with a few slide files (no init_theme)."""
    bp = tmp_path / "pptx-boilerplate"
    bp.mkdir()
    for s in stems:
        (bp / f"{s}.html").write_text(
            f'<!doctype html><html><head>'
            f'<link rel="stylesheet" href="../_pptx-slide.css"></head>'
            f'<body><p>{s}</p></body></html>',
            encoding="utf-8")
    return bp


# --- Piece 1: manifest schema -------------------------------------------------

def test_new_manifest_has_review_block(tmp_path):
    bp = _mini_boilerplate(tmp_path)
    m = ac.new_manifest("p", bp)
    assert "review" in m
    for k in ("approved", "approved_at", "approved_digest", "digest", "preview_path"):
        assert k in m["review"], f"missing review.{k}"
    assert m["review"]["approved"] is False
    # verification tracks 'review', not the retired 'thumbs'
    assert "review" in m["verification"]
    assert "thumbs" not in m["verification"]


# --- Piece 2: boilerplate digest (drift guard) --------------------------------

def test_boilerplate_digest_deterministic_and_sensitive(tmp_path):
    bp = _mini_boilerplate(tmp_path)
    d1 = ac.boilerplate_digest(bp)
    d2 = ac.boilerplate_digest(bp)
    assert d1 == d2
    assert len(d1) == 64  # sha256 hex
    # a 1-byte change flips the digest
    (bp / "01-title.html").write_text("<p>changed</p>", encoding="utf-8")
    assert ac.boilerplate_digest(bp) != d1


def test_boilerplate_digest_ignores_stock_and_preview(tmp_path):
    bp = _mini_boilerplate(tmp_path)
    base = ac.boilerplate_digest(bp)
    # files under .stock/ and _preview/ must not change the live-deck digest
    (bp / ac.STOCK_DIRNAME).mkdir()
    (bp / ac.STOCK_DIRNAME / "01-title.html").write_text("<p>stock differs</p>", encoding="utf-8")
    prev = bp / ac.PREVIEW_DIRNAME
    prev.mkdir()
    (prev / "index.html").write_text("<p>preview</p>", encoding="utf-8")
    assert ac.boilerplate_digest(bp) == base


# --- Piece 3: live-iframe contact sheet ---------------------------------------

import build_contactsheet as cs  # noqa: E402


def _preset_with_theme(tmp_path) -> tuple[Path, Path]:
    """A realistic preset bundle: theme.json + _pptx-slide.css (@import the
    flat colors_and_type.css the way init-project lays it out) + fonts/."""
    preset = tmp_path / "mypreset"
    preset.mkdir()
    bp = preset / "pptx-boilerplate"
    bp.mkdir()
    for s in ("01-title", "06-table", "16-stats"):
        (bp / f"{s}.html").write_text(
            f'<!doctype html><html><head>'
            f'<link rel="stylesheet" href="../_pptx-slide.css"></head>'
            f'<body><p>{s}</p></body></html>', encoding="utf-8")
    (preset / "theme.json").write_text(json.dumps({
        "colors": {"accent": "#FF8800"},
        "typography": {"font-chain": "Foo, sans-serif"},
    }), encoding="utf-8")
    # the CSS chain mirrors the OUTPUT-PROJECT layout: _pptx-slide.css @imports
    # design-system/colors_and_type.css, which @font-faces fonts/.
    (preset / "_pptx-slide.css").write_text(
        "@import url('design-system/colors_and_type.css');\n.x{color:#FF8800}",
        encoding="utf-8")
    (preset / "colors_and_type.css").write_text(
        "@font-face{font-family:'Foo';src:url('fonts/foo.otf')}", encoding="utf-8")
    (preset / "fonts").mkdir()
    (preset / "fonts" / "foo.otf").write_bytes(b"OTTO-stub")
    return preset, bp


def test_contactsheet_iframes_point_into_mirrored_slides_dir(tmp_path):
    preset, bp = _preset_with_theme(tmp_path)
    m = ac.new_manifest("mypreset", bp)
    m["authored"] = ["01-title"]
    html = cs.build_html(preset, m)
    # iframes target the preview's own slides/ mirror (project layout), so the
    # slides' ../_pptx-slide.css + design-system/ chain resolves faithfully.
    for s in ("01-title", "06-table", "16-stats"):
        assert f'src="slides/{s}.html"' in html
    # self-contained index: no external stylesheet <link> on the index page
    assert "<link" not in html


def test_contactsheet_header_shows_accent_and_badges(tmp_path):
    preset, bp = _preset_with_theme(tmp_path)
    m = ac.new_manifest("mypreset", bp)
    m["authored"] = ["01-title"]
    html = cs.build_html(preset, m)
    assert "#FF8800" in html             # accent swatch from theme.json
    assert "authored" in html            # identity-authored badge (01-title)
    assert "data" in html                # data badge (06-table)


def test_contactsheet_write_builds_self_contained_mirror(tmp_path):
    preset, bp = _preset_with_theme(tmp_path)
    m = ac.new_manifest("mypreset", bp)
    out = cs.write(preset, m)
    prev = bp / ac.PREVIEW_DIRNAME
    assert out == prev / "index.html"
    assert out.exists() and "iframe" in out.read_text(encoding="utf-8")
    # mirror reproduces the output-project CSS chain so fonts/colors render:
    assert (prev / "_pptx-slide.css").exists()
    assert (prev / "design-system" / "colors_and_type.css").exists()
    assert (prev / "design-system" / "fonts" / "foo.otf").exists()
    assert (prev / "slides" / "01-title.html").exists()
    # the mirror must NOT recurse the boilerplate (no nested preview/slides bloat)
    assert not (prev / "design-system" / "pptx-boilerplate").exists()


def test_contactsheet_write_is_idempotent(tmp_path):
    preset, bp = _preset_with_theme(tmp_path)
    m = ac.new_manifest("mypreset", bp)
    cs.write(preset, m)
    out = cs.write(preset, m)  # second run must not raise (dest exists)
    assert out.exists()


# --- Piece 4 + 5: review command + confirm gate -------------------------------

import author_layouts as al  # noqa: E402


def _author_preset(tmp_path) -> tuple[Path, Path, Path]:
    """Minimal preset dir + manifest, no init_theme (fast)."""
    presets_root = tmp_path / "presets"
    preset = presets_root / "rev"
    bp = preset / "pptx-boilerplate"
    bp.mkdir(parents=True)
    for s in ("01-title", "06-table", "16-stats"):
        (bp / f"{s}.html").write_text(f"<p>{s}</p>", encoding="utf-8")
    (preset / "theme.json").write_text(
        json.dumps({"colors": {"accent": "#FF8800"}}), encoding="utf-8")
    m = ac.new_manifest("rev", bp)
    m["authored"] = ["01-title"]
    ac.save_manifest(bp, m)
    return presets_root, preset, bp


def _rev_args(presets_root, **kw):
    base = dict(preset="rev", presets_root=presets_root, approve=False, no_open=True)
    base.update(kw)
    return argparse.Namespace(**base)


def _confirm_args(presets_root, **kw):
    base = dict(preset="rev", presets_root=presets_root,
                allow_empty=False, strict=True, skip_review=False)
    base.update(kw)
    return argparse.Namespace(**base)


def _make_confirm_ready(bp):
    """Satisfy every confirm gate EXCEPT the review approval gate."""
    m = ac.load_manifest(bp)
    m["verification"] = {"lint": "ok", "build": "ok", "unzip": "ok", "review": "ok"}
    m["authored"] = ["01-title"]
    ac.save_manifest(bp, m)


def test_review_generates_preview_and_marks_unapproved(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    rc = al.cmd_review(_rev_args(presets_root))
    assert rc == 0
    assert (bp / ac.PREVIEW_DIRNAME / "index.html").exists()
    m = ac.load_manifest(bp)
    assert m["review"]["approved"] is False
    assert m["review"]["digest"] == ac.boilerplate_digest(bp)
    assert m["verification"]["review"] == "ok"


def test_review_approve_records_matching_digest(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    al.cmd_review(_rev_args(presets_root))
    rc = al.cmd_review(_rev_args(presets_root, approve=True))
    assert rc == 0
    m = ac.load_manifest(bp)
    assert m["review"]["approved"] is True
    assert m["review"]["approved_digest"] == ac.boilerplate_digest(bp)
    assert m["review"]["approved_at"]


def test_review_regenerate_resets_prior_approval(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    al.cmd_review(_rev_args(presets_root, approve=True))
    # regenerating the contact sheet must invalidate a stale approval
    al.cmd_review(_rev_args(presets_root))
    assert ac.load_manifest(bp)["review"]["approved"] is False


def test_confirm_refused_without_approval(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    _make_confirm_ready(bp)
    assert al.cmd_confirm(_confirm_args(presets_root)) == 1


def test_confirm_passes_after_approval(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    _make_confirm_ready(bp)
    al.cmd_review(_rev_args(presets_root, approve=True))
    assert al.cmd_confirm(_confirm_args(presets_root)) == 0
    assert ac.load_manifest(bp)["status"] == "confirmed"


def test_confirm_refused_on_drift_after_approval(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    _make_confirm_ready(bp)
    al.cmd_review(_rev_args(presets_root, approve=True))
    (bp / "01-title.html").write_text("<p>edited after approval</p>", encoding="utf-8")
    assert al.cmd_confirm(_confirm_args(presets_root)) == 1


def test_confirm_skip_review_bypasses_gate(tmp_path):
    presets_root, preset, bp = _author_preset(tmp_path)
    _make_confirm_ready(bp)
    assert al.cmd_confirm(_confirm_args(presets_root, skip_review=True)) == 0
