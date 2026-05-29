#!/usr/bin/env python3
"""Extract layout-device signals from a hand-made reference deck.

theme-init Phase 2 lets the agent recompose identity slides into brand layouts.
A `--reference <deck>` (the hand-made brand deck the new preset should echo) used
to be *recorded only* — its path stored in the manifest, never read. This script
PARSES that deck deterministically (stdlib only, no LLM) and reports the layout
devices it actually uses, so Phase 2 prep can:

  * recommend a `surface.card_style` (filled | hairline | borderless),
  * seed the DESIGN.md §5/§6 review draft with measured hints,
  * store the signals in the authoring manifest's blueprint.

It is intentionally a *recommender*, not an applier: it never edits theme.json
or re-renders (that is Phase 1's job) and never replaces the human-authored §5/§6
vocabulary — it only adds reviewable hints. See references/reference-ingestion.md
for the output JSON schema.

Detection is signal-based and conservative: when a signal can't be read with
confidence the value is null / "low", so the user still fills the canonical
section by hand.

Usage:
    python3 ingest_reference.py --reference <deck-dir> [--out <json>] [--quiet]

`<deck-dir>` may be a project dir (output/<slug>-pptx/ with slides/ + a
_pptx-slide.css), a preset dir (pptx-boilerplate/ + _pptx-slide.css), or any
folder containing *.html slides. The deck's own _pptx-slide.css (or
design-system/_pptx-slide.css) is read for the authoritative `.card` chrome.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"

# Helper-class tokens the slide-html design system uses. Detection keys off these
# first (a deck built with the system), with inline-style fallbacks for legacy /
# hand-made decks.
_CARD_CLASSES = ("card", "card-accent", "card-alt", "feature-tile", "feature-tile-accent")
_CTA_CLASSES = ("btn-cta", "btn-cta-sq", "btn-outline")
_KICKER_CLASSES = ("t-cap-up", "label-caption")
_SURFACE_ALT_CLASSES = ("card-alt", "bg-surface-alt")

# accept both "double" and 'single' quoted attributes (hand-made decks vary)
_CLASS_ATTR_RE = re.compile(r"""class\s*=\s*(["'])(.*?)\1""")
_STYLE_ATTR_RE = re.compile(r"""style\s*=\s*(["'])(.*?)\1""")
# a `border:` shorthand that is NOT border-radius / border-left / etc.
_BORDER_SHORTHAND_RE = re.compile(r"(?<![-\w])border\s*:\s*([^;]+)")
_BACKGROUND_RE = re.compile(r"(?<![-\w])background(?:-color)?\s*:\s*([^;]+)")
_BORDER_RADIUS_RE = re.compile(r"border-radius\s*:")
_HAIRLINE_RE = re.compile(r"border(?:-top|-bottom|-left|-right)?\s*:\s*(?:0\.5|1)(?:px|pt)\b")


def _find_slides(ref: Path) -> list[Path]:
    """Locate slide HTML files: <ref>/slides/*.html, else <ref>/pptx-boilerplate/
    *.html, else <ref>/*.html. Excludes the .stock baseline."""
    for sub in ("slides", "pptx-boilerplate"):
        d = ref / sub
        if d.is_dir():
            return sorted(p for p in d.glob("*.html") if ".stock" not in p.parts)
    return sorted(ref.glob("*.html"))


def _find_pptx_css(ref: Path) -> Path | None:
    for cand in (ref / "_pptx-slide.css",
                 ref / "design-system" / "_pptx-slide.css"):
        if cand.is_file():
            return cand
    hits = sorted(ref.rglob("_pptx-slide.css"))
    return hits[0] if hits else None


def _classes(html: str) -> list[list[str]]:
    """Per-element class token lists."""
    return [m.group(2).split() for m in _CLASS_ATTR_RE.finditer(html)]


def _has_class(html: str, names: tuple[str, ...]) -> int:
    """Count elements whose class list contains any of `names`."""
    n = 0
    for toks in _classes(html):
        if any(name in toks for name in names):
            n += 1
    return n


def _card_style_from_css(css: str) -> tuple[str | None, str]:
    """Read the `.card` rule from a deck's _pptx-slide.css → (style, evidence).

    border shorthand present → hairline; else background present → filled;
    else → borderless. Returns (None, reason) if no .card rule found.
    """
    m = re.search(r"\.card\b[^{]*\{([^}]*)\}", css)
    if not m:
        return None, "no .card rule in deck _pptx-slide.css"
    body = m.group(1)
    border = _BORDER_SHORTHAND_RE.search(body)
    has_border = bool(border) and "none" not in border.group(1).lower()
    has_bg = bool(_BACKGROUND_RE.search(body))
    if has_border:
        return "hairline", f".card has border ({border.group(1).strip()})"
    if has_bg:
        return "filled", ".card has background fill, no border"
    return "borderless", ".card has neither fill nor border (padding only)"


def _card_style_from_inline(slides: dict[str, str]) -> tuple[str | None, str]:
    """Fallback: infer from inline card-like divs across slides. A div is
    card-like if it has padding + border-radius (or a card-* class)."""
    bordered = filled = bare = 0
    for html in slides.values():
        for sm in _STYLE_ATTR_RE.finditer(html):
            style = sm.group(2)
            if "padding" not in style or not _BORDER_RADIUS_RE.search(style):
                continue
            border = _BORDER_SHORTHAND_RE.search(style)
            has_border = bool(border) and "none" not in border.group(1).lower()
            has_bg = bool(_BACKGROUND_RE.search(style))
            if has_border:
                bordered += 1
            elif has_bg:
                filled += 1
            else:
                bare += 1
    total = bordered + filled + bare
    if total == 0:
        return None, "no inline card-like elements found"
    winner = max((("hairline", bordered), ("filled", filled), ("borderless", bare)),
                 key=lambda kv: kv[1])
    return winner[0], f"inline card-like divs: {bordered} bordered / {filled} filled / {bare} bare"


def extract(ref: Path) -> dict[str, Any]:
    slide_paths = _find_slides(ref)
    slides = {p.stem: p.read_text(encoding="utf-8", errors="replace") for p in slide_paths}
    css_path = _find_pptx_css(ref)
    css = css_path.read_text(encoding="utf-8", errors="replace") if css_path else ""

    # card_style — authoritative from CSS, fallback to inline, else null
    cs_val, cs_evidence = _card_style_from_css(css)
    cs_conf = "high"
    if cs_val is None:
        cs_val, cs_evidence = _card_style_from_inline(slides)
        cs_conf = "medium" if cs_val else "low"

    per_slide = []
    surface_slides = hairline_total = cta_total = kicker_total = 0
    for stem, html in slides.items():
        cards = _has_class(html, _CARD_CLASSES)
        surf = _has_class(html, _SURFACE_ALT_CLASSES) > 0
        rules = _has_class(html, ("rule",)) + len(_HAIRLINE_RE.findall(html))
        cta = _has_class(html, _CTA_CLASSES)
        kicker = _has_class(html, _KICKER_CLASSES)
        if surf:
            surface_slides += 1
        hairline_total += rules
        cta_total += cta
        kicker_total += kicker
        per_slide.append({"slide": stem, "cards": cards, "surface_alt": surf,
                          "rules": rules, "cta": cta, "kicker": kicker})

    n = len(slides)
    return {
        "version": SCHEMA_VERSION,
        "source": str(ref),
        "pptx_css": str(css_path) if css_path else None,
        "slides_analyzed": n,
        "devices": {
            "card_style": {"value": cs_val, "confidence": cs_conf, "evidence": cs_evidence},
            "surface_alternation": {
                "present": surface_slides > 0,
                "slides_using": surface_slides,
                "ratio": round(surface_slides / n, 2) if n else 0.0,
            },
            "hairline_dividers": {"present": hairline_total > 0, "count": hairline_total},
            "cta": {"present": cta_total > 0, "count": cta_total},
            "kicker": {"present": kicker_total > 0, "count": kicker_total},
        },
        "per_slide": per_slide,
    }


def summarize(result: dict[str, Any]) -> str:
    d = result["devices"]
    cs = d["card_style"]
    lines = [
        f"reference: {result['source']}  ({result['slides_analyzed']} slides)",
        f"  card_style    : {cs['value']}  ({cs['confidence']} — {cs['evidence']})",
        f"  surface alt   : {d['surface_alternation']['slides_using']} slides "
        f"({int(d['surface_alternation']['ratio'] * 100)}%)",
        f"  hairline rules: {d['hairline_dividers']['count']}",
        f"  CTA           : {d['cta']['count']}",
        f"  kicker/eyebrow: {d['kicker']['count']}",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--reference", type=Path, required=True,
                    help="Reference deck dir (project, preset, or folder of *.html)")
    ap.add_argument("--out", type=Path, default=None,
                    help="Write JSON here (default: stdout)")
    ap.add_argument("--quiet", action="store_true", help="JSON only, no summary on stderr")
    args = ap.parse_args()

    if not args.reference.exists():
        print(f"reference not found: {args.reference}", file=sys.stderr)
        return 2

    result = extract(args.reference)
    if result["slides_analyzed"] == 0:
        print(f"no *.html slides found under {args.reference}", file=sys.stderr)
        return 1

    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(payload + "\n", encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(payload)
    if not args.quiet:
        print("\n" + summarize(result), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
