"""Migrate a huashu-design slide HTML into a pptx-boilerplate-ready .tpl.html.

Applies 4 transformations in order:
1. Tag rewrite: <div class="X"> -> <p class="X"> or <h*class="X"> based on a class->tag map
2. Hex tokenization: replace literal #4633E3 etc. with {{TOKEN:colors.accent}} (Task 4 mapping)
3. Font-family tokenization: literal Pretendard chains -> {{TOKEN:typography.font-chain}}
4. Strip bg-dots reference if present (since we fixed _slide.css globally, this is belt+suspenders)

Usage:
    python3 migrate_pattern.py --in <source.html> --out <output.tpl.html>
    python3 migrate_pattern.py --in <source.html> --out <output.tpl.html> --no-tokenize
        (skip step 2-3, useful for diff inspection)

The script is idempotent -- running twice produces the same output.

Decision (2026-04-27): graph-paper texture in image patterns (08a/08b/22/23)
is dropped during migration. Image placeholders will use solid bg + dashed border.
To restore the texture later, embed a tiled PNG via <img> in the placeholder.
The codemod does NOT auto-strip those gradients; image patterns need manual
restructure in Phase 3 anyway.

Per-file overrides (Phase 0 base case is mapping below; future enhancement could
read directives like `<!-- MIGRATE: title=h3 -->` from the first 5 lines of source).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Class -> tag mapping. Body-text classes go to <p>, heading-style to <h*>.
# Decision on `class="title"`: defaults to <p> (body-row label). For card-title
# usage (e.g. 05-comparison) author can manually upgrade to <h3> after migration.
CLASS_TO_TAG: dict[str, str] = {
    # Body-text classes -> <p>
    "title": "p",
    "caption": "p",
    "label-caption": "p",
    "stat-caption": "p",
    "stat-body": "p",
    "ov-cell": "p",
    "im-ph-caption": "p",
    "im-ph-note": "p",
    "ex-ph-caption": "p",
    "ex-ph-note": "p",
    "ex-label": "p",
    "tm-label": "p",
    "ov-metric-name": "p",
    "ov-metric-desc": "p",
    "im-subtitle": "p",
    "tm-subtitle": "p",
    # Heading-style classes -> <h*>
    "tp-title": "h3",   # three-point card title
    "fp-title": "h3",   # four-point
    "sp-title": "h4",   # six-point (smaller cards)
    "proc-title": "h4", # process step title
    "im-title": "h3",   # image showcase title
    "tm-title": "h2",   # terminal title
    # Body-as-text leaf divs added during Phase 1 (huashu-design migration).
    # `proc-arrow` is the arrow connector glyph between process steps — text
    # `›` directly in the div, so it must become <p> for the 4-constraint pass.
    "proc-arrow": "p",
    # `gm` is the governing-message band at the bottom of every slide; the
    # bare div carries paragraph text that must be wrapped.
    "gm": "p",
    # NOTE: `insight-bar` is intentionally NOT mapped — its CSS (in
    # _slide.css) attaches background + border + padding to the wrapper.
    # Converting <div class="insight-bar">text</div> -> <p class="insight-bar">
    # would put background on a text element (E1 violation). Keep it as div
    # and manually wrap inner text in <p> in the template.
}


# Hex -> token mapping (mirrors templates/_pptx-slide.tpl.css).
HEX_TO_TOKEN: dict[str, str] = {
    "#FAFAF9": "{{TOKEN:colors.bg}}",
    "#FFFFFF": "{{TOKEN:colors.surface}}",
    "#F5F5F4": "{{TOKEN:colors.surface-alt}}",
    "#1A1A1A": "{{TOKEN:colors.text}}",
    "#6B7280": "{{TOKEN:colors.text-secondary}}",
    "#9CA3AF": "{{TOKEN:colors.text-tertiary}}",
    "#E5E7EB": "{{TOKEN:colors.border}}",
    "#D4D4D4": "{{TOKEN:colors.border-strong}}",
    "#4633E3": "{{TOKEN:colors.accent}}",
    "#E8E5FC": "{{TOKEN:colors.accent-soft}}",
    "#2E1FB3": "{{TOKEN:colors.accent-ink}}",
    "#059669": "{{TOKEN:colors.positive}}",
    "#E11D48": "{{TOKEN:colors.negative}}",
    "#D97706": "{{TOKEN:colors.warning}}",
    # Leave hardcoded:
    #   "#2A2A2A" (terminal chrome)
    #   "#FFFFFF" inside text content (color-grid labels)
}


# Pretendard font-chain literal -- exact match the script tokenizes.
PRETENDARD_CHAIN_RE = re.compile(
    r"'Pretendard',\s*-apple-system,\s*BlinkMacSystemFont,\s*'Segoe UI',\s*Roboto,"
    r"\s*'Helvetica Neue',\s*Arial,\s*sans-serif",
    re.IGNORECASE,
)


# ---------- Step 1: Tag rewrite ----------------------------------------------

# Match a <div ...>TEXT</div> block where:
#   - TEXT contains no `<` (no nested tags, no comments) other than inline <span>/<br>
#   - the opening tag's class attribute contains at least one of CLASS_TO_TAG
# We first look for any <div ...>...</div> with a class attribute, then decide.
#
# To avoid matching across nested divs, we use a greedy-but-bounded approach:
# match `<div\b[^>]*class="[^"]*"[^>]*>` and then non-greedy any chars up to `</div>`,
# but require that the inner text does not itself contain `<div`.

DIV_OPEN_RE = re.compile(
    r"<div\b([^>]*?)class=\"([^\"]*)\"([^>]*)>",
    re.IGNORECASE,
)


def _classes(class_attr: str) -> list[str]:
    """Word-boundary class list parse from the class="..." attribute body."""
    return [c for c in class_attr.split() if c]


def _match_class_to_tag(class_attr: str) -> str | None:
    """Return the target tag name if ANY class in class_attr maps; else None.

    First match in CLASS_TO_TAG order would be ambiguous; we prefer:
    1. first heading-style class (h*) found,
    2. else first body class (p).
    Heading priority means `<div class="title tp-title">` -> <h3>.
    """
    cls = _classes(class_attr)
    for c in cls:
        tag = CLASS_TO_TAG.get(c)
        if tag and tag.startswith("h"):
            return tag
    for c in cls:
        tag = CLASS_TO_TAG.get(c)
        if tag == "p":
            return tag
    return None


def _find_matching_close(html: str, start_idx: int) -> int:
    """Given index pointing AFTER an opening <div...>, find matching </div>.

    Tracks nested <div> depth. Returns the index of the start of the matching
    `</div>`, or -1 if not found.
    """
    depth = 1
    i = start_idx
    n = len(html)
    while i < n:
        # Find next <div or </div>
        nxt_open = html.find("<div", i)
        nxt_close = html.find("</div>", i)
        if nxt_close == -1:
            return -1
        if nxt_open != -1 and nxt_open < nxt_close:
            # ensure it's a real <div (followed by space/>/tab)
            after = html[nxt_open + 4 : nxt_open + 5]
            if after in (" ", ">", "\t", "\n", "\r"):
                depth += 1
            i = nxt_open + 4
            continue
        depth -= 1
        if depth == 0:
            return nxt_close
        i = nxt_close + 6
    return -1


# A "leaf" div is one whose inner content has no block-level child tags.
# Block-level children we forbid: div, p, h1-h6, ul, ol, li, table, section,
# blockquote, hr. Inline (span, br, b, i, em, strong, a, svg, img) is allowed.
_BLOCK_INNER_RE = re.compile(
    r"<\s*(div|p|h[1-6]|ul|ol|li|table|tr|td|th|section|article|blockquote|hr)\b",
    re.IGNORECASE,
)


def _has_text_directly(inner: str) -> bool:
    """True if inner has non-whitespace text outside any tag."""
    # Strip all tags and check residue.
    stripped = re.sub(r"<[^>]+>", "", inner)
    return bool(stripped.strip())


def rewrite_tags(html: str) -> tuple[str, dict[str, int]]:
    """Rewrite qualifying <div class="X">...</div> -> <TAG class="X">...</TAG>.

    Returns (new_html, {"div_to_p": int, "div_to_h": int}).

    A div qualifies iff:
    - its class attribute contains at least one mapped class
    - its inner content has direct text (E2 violation territory)
    - its inner content has no nested block-level tags (leaf div)
    """
    counts = {"div_to_p": 0, "div_to_h": 0}
    out: list[str] = []
    i = 0
    n = len(html)
    while i < n:
        m = DIV_OPEN_RE.search(html, i)
        if not m:
            out.append(html[i:])
            break
        out.append(html[i : m.start()])
        open_start, open_end = m.start(), m.end()
        pre_class, class_attr, post_class = m.group(1), m.group(2), m.group(3)

        target_tag = _match_class_to_tag(class_attr)
        close_start = _find_matching_close(html, open_end)
        if close_start == -1 or target_tag is None:
            out.append(html[open_start:open_end])
            i = open_end
            continue

        inner = html[open_end:close_start]

        # Skip if not a leaf (has nested block elements) or has no direct text.
        if _BLOCK_INNER_RE.search(inner) or not _has_text_directly(inner):
            out.append(html[open_start:open_end])
            i = open_end
            continue

        # Rewrite the open tag and the close tag.
        new_open = f"<{target_tag}{pre_class}class=\"{class_attr}\"{post_class}>"
        new_close = f"</{target_tag}>"
        out.append(new_open)
        out.append(inner)
        out.append(new_close)
        if target_tag == "p":
            counts["div_to_p"] += 1
        else:
            counts["div_to_h"] += 1
        i = close_start + len(("</div>"))

    return "".join(out), counts


# ---------- Step 2: Hex tokenization -----------------------------------------

# Match #RRGGBB hex literals, case-insensitive. The full word boundary is
# important so we don't match an id like "#FAFAF99".
_HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")


def tokenize_hex(html: str) -> tuple[str, int]:
    """Replace mapped hex literals with {{TOKEN:...}} placeholders."""
    count = 0
    norm_map = {k.upper(): v for k, v in HEX_TO_TOKEN.items()}

    def _sub(match: re.Match[str]) -> str:
        nonlocal count
        h = match.group(0).upper()
        if h in norm_map:
            count += 1
            return norm_map[h]
        return match.group(0)

    return _HEX_RE.sub(_sub, html), count


# ---------- Step 3: Font-family tokenization ---------------------------------


def tokenize_font_chain(html: str) -> tuple[str, int]:
    """Replace literal Pretendard chains with {{TOKEN:typography.font-chain}}."""
    count = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return "{{TOKEN:typography.font-chain}}"

    return PRETENDARD_CHAIN_RE.sub(_sub, html), count


# ---------- Step 4: Strip bg-dots reference (belt+suspenders) ----------------

# Match `bg-dots` as a class token within a class="..." attribute. We want to
# remove just the token, not the whole attribute. The CSS rule is now neutral
# (solid surface-alt) but stripping references keeps templates explicit.

_BG_DOTS_RE = re.compile(r"\bbg-dots\b\s?")


def strip_bg_dots(html: str) -> tuple[str, int]:
    """Remove `bg-dots` class tokens. Idempotent."""
    count = 0

    def _sub_attr(match: re.Match[str]) -> str:
        nonlocal count
        before = match.group(0)
        # only strip inside class attribute
        attr = match.group(1)
        new_attr, n = _BG_DOTS_RE.subn("", attr)
        new_attr = new_attr.strip().replace("  ", " ")
        count += n
        return f'class="{new_attr}"'

    out = re.sub(r'class="([^"]*)"', _sub_attr, html)
    return out, count


# ---------- Step 5: Stylesheet rewrite for pptx-boilerplate context ----------
#
# Source patterns reference `<link rel="stylesheet" href="_slide.css">`.
# When they live under `pptx-boilerplate/` and are deployed into a project
# at `slides/`, they need:
#   - `../design-system/slides/_slide.css` to load all .slide/.gm/.flex-*/etc.
#     class definitions (the patterns rely on them inline)
#   - `../_pptx-slide.css` to load the project's tokenized helpers + colors
#     (via `@import url('design-system/colors_and_type.css')`)
# Plus an inline body-canvas override so html2pptx sees a 1280x720px body
# (= 960x540pt LAYOUT_WIDE) instead of `_slide.css`'s 100vh-centered layout.

_LINK_SLIDE_CSS_RE = re.compile(
    r'<link\s+rel="stylesheet"\s+href="_slide\.css">',
    re.IGNORECASE,
)

_BOILERPLATE_LINKS = (
    '<link rel="stylesheet" href="../design-system/slides/_slide.css">\n'
    '<link rel="stylesheet" href="../_pptx-slide.css">\n'
    '<style>\n'
    '  /* Override _slide.css 100vh body: html2pptx needs body == canvas (1280x720px = 960x540pt) */\n'
    '  html, body { width: 1280px; height: 720px; padding: 0; margin: 0; min-height: 0; overflow: hidden; display: block; background: {{TOKEN:colors.bg}}; }\n'
    '</style>'
)


def rewrite_stylesheet_links(html: str) -> tuple[str, int]:
    """Swap the bare `_slide.css` link for boilerplate-context links.

    Idempotent: if the rewrite has already happened, returns html unchanged.
    """
    if _LINK_SLIDE_CSS_RE.search(html) is None:
        return html, 0
    new_html, n = _LINK_SLIDE_CSS_RE.subn(_BOILERPLATE_LINKS, html, count=1)
    return new_html, n


# ---------- Driver ------------------------------------------------------------


def migrate(source: str, *, tokenize: bool = True) -> tuple[str, dict[str, int]]:
    summary: dict[str, int] = {}
    html, tag_counts = rewrite_tags(source)
    summary.update(tag_counts)
    if tokenize:
        html, hex_count = tokenize_hex(html)
        summary["hex_tokens"] = hex_count
        html, font_count = tokenize_font_chain(html)
        summary["font_tokens"] = font_count
        html, dots_count = strip_bg_dots(html)
        summary["bg_dots_stripped"] = dots_count
        html, links_count = rewrite_stylesheet_links(html)
        summary["links_rewritten"] = links_count
    else:
        summary["hex_tokens"] = 0
        summary["font_tokens"] = 0
        summary["bg_dots_stripped"] = 0
        summary["links_rewritten"] = 0
    return html, summary


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--in", dest="src", required=True, help="source .html file")
    p.add_argument("--out", dest="dst", required=True, help="output .tpl.html file")
    p.add_argument("--no-tokenize", action="store_true", help="skip hex/font/bg-dots passes")
    args = p.parse_args(argv)

    src_path = Path(args.src)
    dst_path = Path(args.dst)

    if not src_path.is_file():
        print(f"error: source not found: {src_path}", file=sys.stderr)
        return 2

    source = src_path.read_text(encoding="utf-8")
    output, summary = migrate(source, tokenize=not args.no_tokenize)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(output, encoding="utf-8")

    print(
        f"migrated {src_path.name} -> {dst_path}\n"
        f"  div->p:           {summary['div_to_p']}\n"
        f"  div->h*:          {summary['div_to_h']}\n"
        f"  hex tokens:       {summary['hex_tokens']}\n"
        f"  font tokens:      {summary['font_tokens']}\n"
        f"  bg-dots stripped: {summary['bg_dots_stripped']}\n"
        f"  links rewritten:  {summary['links_rewritten']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
