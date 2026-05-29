"""Unit tests for the _token_render placeholder engine.

Covers the existing TOKEN / IF grammar plus the IFEQ value-switch primitive
added for surface.card_style (one enum token → filled/hairline/borderless).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _token_render import render  # noqa: E402


THEME = {
    "colors": {"accent": "#4633E3", "surface": "#FFFFFF", "border": "#E5E7EB"},
    "surface": {"card_style": "hairline"},
    "typography": {"font-mono": "'SF Mono', monospace"},
    "voice": {"forbidden_phrases": ["여러분"]},
}


# ---------------- existing grammar (regression) ----------------

def test_token_raw():
    assert render("a {{TOKEN:colors.accent}} b", THEME) == "a #4633E3 b"


def test_token_rgb_filter():
    assert render("rgba({{TOKEN:colors.accent|rgb}}, 0.06)", THEME) == "rgba(70, 51, 227, 0.06)"


def test_if_truthy_kept_and_empty_removed():
    out = render("{{IF:voice.forbidden_phrases}}has{{/IF}}", THEME)
    assert out == "has"
    out2 = render("{{IF:voice.missing}}x{{/IF}}", THEME)
    assert out2 == ""


# ---------------- IFEQ value-switch ----------------

def test_ifeq_keeps_matching_branch_only():
    tpl = ("{{IFEQ:surface.card_style:hairline}}HAIR{{/IFEQ}}"
           "{{IFEQ:surface.card_style:filled}}FILL{{/IFEQ}}"
           "{{IFEQ:surface.card_style:borderless}}NONE{{/IFEQ}}")
    assert render(tpl, THEME) == "HAIR"


def test_ifeq_filled_branch():
    theme = {**THEME, "surface": {"card_style": "filled"}}
    tpl = ("{{IFEQ:surface.card_style:hairline}}HAIR{{/IFEQ}}"
           "{{IFEQ:surface.card_style:filled}}FILL{{/IFEQ}}")
    assert render(tpl, theme) == "FILL"


def test_ifeq_borderless_drops_all_chrome_branches():
    theme = {**THEME, "surface": {"card_style": "borderless"}}
    tpl = ("{ {{IFEQ:surface.card_style:hairline}}background: x; border: y; {{/IFEQ}}"
           "{{IFEQ:surface.card_style:filled}}background: x; {{/IFEQ}}padding: 1pt; }")
    assert render(tpl, theme) == "{ padding: 1pt; }"


def test_ifeq_missing_path_removed():
    assert render("{{IFEQ:surface.nope:hairline}}x{{/IFEQ}}", THEME) == ""


def test_ifeq_inner_token_resolved():
    tpl = "{{IFEQ:surface.card_style:hairline}}border: 1px solid {{TOKEN:colors.border}};{{/IFEQ}}"
    assert render(tpl, THEME) == "border: 1px solid #E5E7EB;"


def test_ifneq_kept_when_value_differs_dropped_when_equal():
    tpl = "{{IFNEQ:surface.card_style:borderless}}CHROME{{/IFNEQ}}"
    assert render(tpl, THEME) == "CHROME"  # hairline != borderless → kept
    theme = {**THEME, "surface": {"card_style": "borderless"}}
    assert render(tpl, theme) == ""  # borderless == borderless → dropped


def test_ifneq_missing_path_removed():
    assert render("{{IFNEQ:surface.nope:borderless}}x{{/IFNEQ}}", THEME) == ""


def test_ifeq_byte_identical_hairline_card_line():
    """The card_style refactor must render jangpm's .card byte-for-byte."""
    tpl = (".card        { "
           "{{IFEQ:surface.card_style:hairline}}background: {{TOKEN:colors.surface}}; "
           "border: 1px solid {{TOKEN:colors.border}}; border-radius: 12pt; {{/IFEQ}}"
           "{{IFEQ:surface.card_style:filled}}background: {{TOKEN:colors.surface}}; "
           "border-radius: 12pt; {{/IFEQ}}padding: 18pt 20pt; }")
    expected = (".card        { background: #FFFFFF; "
                "border: 1px solid #E5E7EB; border-radius: 12pt; padding: 18pt 20pt; }")
    assert render(tpl, THEME) == expected
