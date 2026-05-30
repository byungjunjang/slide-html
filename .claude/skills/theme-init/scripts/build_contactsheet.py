"""Phase 2 review — live-iframe contact sheet of the FINAL boilerplate.

Renders a single `_preview/index.html` that embeds every final slide via an
isolated <iframe> (scaled to a thumbnail) so the user can review the whole deck
at once and approve/feedback. Pure file copies — no Playwright, no node build.
Build/raster fidelity is covered separately by `author_layouts.py validate`.

iframes (not inlined bodies) because the boilerplate slides share class names; a
single document would collide their CSS. Each iframe is its own document.

The contact sheet is a SELF-CONTAINED MIRROR of the output-project layout, NOT
an in-place render of the preset bundle. The preset's `_pptx-slide.css` does
`@import 'design-system/colors_and_type.css'` — a path that only resolves once
init-project.sh has copied the preset into `<project>/design-system/`. Rendering
the bundle slides in place would 404 that import and lose the brand @font-face.
So `write()` reproduces the project layout under `_preview/`:

    _preview/
      index.html          (iframes → slides/NN.html)
      _pptx-slide.css      (copy)            → @import design-system/colors_and_type.css
      design-system/       (preset copy, minus pptx-boilerplate) → colors_and_type.css, fonts/, assets/
      slides/NN.html       (final boilerplate copies)            → ../_pptx-slide.css

Every relative path the slides + CSS use then resolves exactly as in a real
build, so fonts and colors are faithful. `_preview/` is transient (gitignored,
regenerated each `review`).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import _authoring_common as ac

# Slides are 960x540; render each iframe full-size and scale down to a thumbnail.
SCALE = 0.375
SLIDE_W, SLIDE_H = 960, 540
THUMB_W = round(SLIDE_W * SCALE)   # 360
THUMB_H = round(SLIDE_H * SCALE)   # 203


def _badge(stem: str, identity: set[str], authored: set[str]) -> tuple[str, str]:
    """(label, css-class) for a slide's provenance badge."""
    if stem in identity:
        if stem in authored:
            return "identity · authored", "b-authored"
        return "identity · stock", "b-stock"
    return "data", "b-data"


def build_html(preset_dir: Path, manifest: dict[str, Any]) -> str:
    bp = preset_dir / "pptx-boilerplate"
    theme: dict[str, Any] = {}
    tp = preset_dir / "theme.json"
    if tp.exists():
        try:
            theme = json.loads(tp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            theme = {}
    accent = theme.get("colors", {}).get("accent", "#111111")
    font = theme.get("typography", {}).get("font-chain", "system-ui, sans-serif")

    cls = ac.classify(bp)
    identity = set(cls["identity_flat"])
    data = set(cls["data_set"])
    authored = set(manifest.get("authored", []))
    stems = ac.existing_html(bp)
    digest = ac.boilerplate_digest(bp)
    preset = manifest.get("preset", preset_dir.name)

    cards = []
    for s in stems:
        label, cls_name = _badge(s, identity, authored)
        cards.append(
            f'    <figure class="card">\n'
            f'      <div class="thumb"><iframe loading="lazy" scrolling="no" '
            f'src="slides/{s}.html" title="{s}"></iframe></div>\n'
            f'      <figcaption><span class="stem">{s}</span>'
            f'<span class="badge {cls_name}">{label}</span></figcaption>\n'
            f'    </figure>'
        )
    grid = "\n".join(cards)

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{preset} — 최종 보일러플레이트 리뷰</title>
<style>
  :root {{ --accent: {accent}; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #f4f4f5; color: #18181b;
         font-family: {font}; }}
  header {{ position: sticky; top: 0; z-index: 2; background: #fff;
           border-bottom: 1px solid #e4e4e7; padding: 16px 24px; }}
  .title {{ display: flex; align-items: center; gap: 12px; }}
  .swatch {{ width: 22px; height: 22px; border-radius: 6px;
            background: var(--accent); border: 1px solid rgba(0,0,0,.12); }}
  h1 {{ font-size: 18px; margin: 0; font-weight: 700; }}
  .meta {{ margin-top: 6px; font-size: 12px; color: #71717a; }}
  .banner {{ margin-top: 10px; padding: 8px 12px; border-radius: 8px;
            background: var(--accent); color: #fff; font-size: 13px; font-weight: 600; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax({THUMB_W}px, 1fr));
          gap: 18px; padding: 24px; }}
  .card {{ margin: 0; background: #fff; border: 1px solid #e4e4e7;
          border-radius: 10px; overflow: hidden; }}
  .thumb {{ width: 100%; height: {THUMB_H}px; overflow: hidden;
           background: #fff; border-bottom: 1px solid #e4e4e7; }}
  .thumb iframe {{ width: {SLIDE_W}px; height: {SLIDE_H}px; border: 0;
                  transform: scale({SCALE}); transform-origin: top left; }}
  figcaption {{ display: flex; align-items: center; justify-content: space-between;
               gap: 8px; padding: 8px 10px; font-size: 12px; }}
  .stem {{ font-weight: 600; }}
  .badge {{ font-size: 10px; padding: 2px 7px; border-radius: 999px;
           font-weight: 700; letter-spacing: .02em; }}
  .b-authored {{ background: var(--accent); color: #fff; }}
  .b-stock {{ background: #fef3c7; color: #92400e; }}
  .b-data {{ background: #e4e4e7; color: #52525b; }}
</style>
</head>
<body>
<header>
  <div class="title"><span class="swatch"></span><h1>{preset}</h1></div>
  <div class="meta">전체 {len(stems)}장 · identity {len(identity)}장(작곡 {len(identity & authored)}) ·
    data {len(data)}장 · font {font} · digest {digest[:8]} · {ac._now()}</div>
  <div class="banner">최종 보일러플레이트 리뷰 — 승인하면 confirm이 진행됩니다. 수정이 필요하면 피드백으로 알려주세요.</div>
</header>
<main class="grid">
{grid}
</main>
</body>
</html>
"""


def write(preset_dir: Path, manifest: dict[str, Any]) -> Path:
    """Build the self-contained _preview/ mirror and render index.html.

    Reproduces the output-project layout (design-system/ + _pptx-slide.css +
    slides/) so the embedded slides resolve their CSS @import + @font-face
    faithfully. Rebuilt fresh each call (idempotent).
    """
    bp = preset_dir / "pptx-boilerplate"
    preview = bp / ac.PREVIEW_DIRNAME
    if preview.exists():
        shutil.rmtree(preview)
    preview.mkdir(parents=True)

    # design-system/ = the whole preset MINUS its boilerplate (avoids recursing
    # into this very _preview dir and copying 37 slides + .stock baseline twice).
    shutil.copytree(preset_dir, preview / "design-system",
                    ignore=shutil.ignore_patterns("pptx-boilerplate"))
    helper = preset_dir / "_pptx-slide.css"
    if helper.exists():
        shutil.copy2(helper, preview / "_pptx-slide.css")

    slides = preview / "slides"
    slides.mkdir()
    for stem in ac.existing_html(bp):
        shutil.copy2(bp / f"{stem}.html", slides / f"{stem}.html")

    out = preview / "index.html"
    out.write_text(build_html(preset_dir, manifest), encoding="utf-8")
    return out
