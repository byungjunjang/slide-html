"""Unit tests for the reference-deck layout-device extractor (Task 9)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ingest_reference as ir  # noqa: E402


def _deck(tmp_path, card_css, slide_html):
    (tmp_path / "_pptx-slide.css").write_text(card_css, encoding="utf-8")
    slides = tmp_path / "slides"
    slides.mkdir(exist_ok=True)
    (slides / "01-x.html").write_text(slide_html, encoding="utf-8")
    return tmp_path


# ---- card_style from the deck's .card CSS rule (authoritative, high conf) ----

def test_card_style_hairline_from_css(tmp_path):
    deck = _deck(tmp_path,
                 ".card { background: #FFF; border: 1px solid #E5E7EB; border-radius: 12pt; }",
                 "<div class='card'><p>x</p></div>")
    cs = ir.extract(deck)["devices"]["card_style"]
    assert cs["value"] == "hairline"
    assert cs["confidence"] == "high"


def test_card_style_filled_from_css(tmp_path):
    deck = _deck(tmp_path, ".card { background: #FFF; border-radius: 12pt; }", "<div class='card'></div>")
    assert ir.extract(deck)["devices"]["card_style"]["value"] == "filled"


def test_card_style_borderless_from_css(tmp_path):
    deck = _deck(tmp_path, ".card { padding: 18pt 20pt; }", "<div class='card'></div>")
    assert ir.extract(deck)["devices"]["card_style"]["value"] == "borderless"


def test_border_radius_not_mistaken_for_border(tmp_path):
    # only border-radius (no border shorthand) must NOT read as hairline
    deck = _deck(tmp_path, ".card { background:#fff; border-radius: 12pt; }", "<div class='card'></div>")
    assert ir.extract(deck)["devices"]["card_style"]["value"] == "filled"


# ---- inline fallback when no .card rule ----

def test_card_style_inline_fallback_medium(tmp_path):
    (tmp_path / "_pptx-slide.css").write_text("/* no card rule */", encoding="utf-8")
    slides = tmp_path / "slides"
    slides.mkdir()
    (slides / "01-x.html").write_text(
        "<div style='padding:18pt; border-radius:12pt; border:1px solid #ccc; background:#fff;'></div>",
        encoding="utf-8")
    cs = ir.extract(tmp_path)["devices"]["card_style"]
    assert cs["value"] == "hairline"
    assert cs["confidence"] == "medium"


# ---- the other four devices ----

def test_devices_detected(tmp_path):
    deck = _deck(tmp_path,
                 ".card { border: 1px solid #ccc; }",
                 "<div class='card-alt'></div>"
                 "<div class='btn-cta'><p>Go</p></div>"
                 "<p class='t-cap-up'>KICKER</p>"
                 "<div class='rule'></div>")
    d = ir.extract(deck)["devices"]
    assert d["surface_alternation"]["present"] and d["surface_alternation"]["slides_using"] == 1
    assert d["cta"]["present"] and d["cta"]["count"] == 1
    assert d["kicker"]["present"] and d["kicker"]["count"] == 1
    assert d["hairline_dividers"]["present"]  # .rule + 1px border


def test_schema_shape_and_per_slide(tmp_path):
    deck = _deck(tmp_path, ".card { border: 1px solid #ccc; }", "<div class='card'></div>")
    r = ir.extract(deck)
    assert r["version"] == "1.0"
    assert r["slides_analyzed"] == 1
    assert set(r["devices"]) == {"card_style", "surface_alternation", "hairline_dividers", "cta", "kicker"}
    assert r["per_slide"][0]["slide"] == "01-x"


def test_empty_deck_is_safe(tmp_path):
    (tmp_path / "slides").mkdir()
    r = ir.extract(tmp_path)
    assert r["slides_analyzed"] == 0
    assert r["devices"]["card_style"]["value"] is None
