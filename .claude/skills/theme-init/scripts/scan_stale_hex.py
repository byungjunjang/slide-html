#!/usr/bin/env python3
"""Stale-hex guard (Fix1) — scan built deck slides for hardcoded color hex.

Convention (4-constraints + css-helpers): deck slide HTML composes on top of
`_pptx-slide.css` helper classes and CSS `var(--*)` tokens — it should never
hardcode color hex. After an active-theme switch (`active.json` → new preset),
any hex that was hardcoded to a PRIOR theme's accent silently goes *stale*:
the deck no longer matches the active palette. This is a WARN-level guard that
surfaces those literals so they can be re-tokenized.

Scope (per PIPELINE_UPDATE_PLAN.md item F):
  - scans  output/<deck>/slides/**/*.html  ONLY
  - excludes  design-system/ (the legit token source — hex lives there by design),
              pptx-boilerplate/,  *.pen (encrypted Pencil files)

Classification (when the active palette resolves):
  - FOREIGN : hex not in the active palette  → likely stale from a prior theme
  - theme   : hex matches an active token    → still a smell (use var()), lower priority
  - (palette unresolved) → every hex reported as "hardcoded", unclassified

Exit codes:
  0  always (warn-only) — unless --strict
  1  --strict and >=1 FOREIGN hex found (or, with --any, >=1 hardcoded hex)
  2  setup error (bad --root, palette unreadable when explicitly given)

Standalone CLI, stdlib only. Intended to be invoked by /theme-init after an
active switch, and runnable ad hoc against output/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# scripts -> theme-init -> skills -> .claude -> <repo root>
REPO_ROOT = Path(__file__).resolve().parents[4]
SLIDE_DS = REPO_ROOT / ".claude" / "skills" / "slide" / "assets" / "design-systems"
DEFAULT_ACTIVE_JSON = SLIDE_DS / "active.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "output"

# #RGB, #RGBA, #RRGGBB, #RRGGBBAA  (word-bounded so it doesn't swallow ids)
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
EXCLUDE_DIR_PARTS = {"design-system", "pptx-boilerplate", "boilerplate", "node_modules"}


def normalize_hex(hx: str) -> str:
    """Lowercase + expand short form to #rrggbb (drop alpha) for comparison."""
    h = hx.lower().lstrip("#")
    if len(h) in (3, 4):  # #rgb / #rgba
        h = "".join(c * 2 for c in h[:3])
    elif len(h) in (6, 8):  # #rrggbb / #rrggbbaa
        h = h[:6]
    return "#" + h


def resolve_palette(preset: str | None, palette_path: Path | None) -> tuple[set[str], str]:
    """Return (normalized hex set, human label describing the source)."""
    if palette_path is not None:
        if not palette_path.exists():
            raise SystemExit(f"--palette not found: {palette_path}")
        css = palette_path.read_text(encoding="utf-8", errors="replace")
        return {normalize_hex(m) for m in HEX_RE.findall(css)}, str(palette_path)

    if preset is None:
        if DEFAULT_ACTIVE_JSON.exists():
            try:
                preset = json.loads(DEFAULT_ACTIVE_JSON.read_text(encoding="utf-8")).get("active")
            except (json.JSONDecodeError, OSError):
                preset = None

    if not preset:
        return set(), "(unresolved — reporting all hardcoded hex)"

    css_path = SLIDE_DS / preset / "colors_and_type.css"
    if not css_path.exists():
        return set(), f"(preset '{preset}' has no colors_and_type.css — reporting all hardcoded hex)"
    css = css_path.read_text(encoding="utf-8", errors="replace")
    return {normalize_hex(m) for m in HEX_RE.findall(css)}, f"{preset}/colors_and_type.css"


def iter_slide_html(root: Path, deck: str | None):
    """Yield output/<deck>/slides/**/*.html, honoring exclusions."""
    decks = [root / deck] if deck else sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []
    for deck_dir in decks:
        slides = deck_dir / "slides"
        if not slides.is_dir():
            continue
        for html in sorted(slides.rglob("*.html")):
            if any(part in EXCLUDE_DIR_PARTS for part in html.parts):
                continue
            if html.suffix == ".pen":  # defensive; rglob *.html won't match, but keep intent explicit
                continue
            yield deck_dir.name, html


def scan_file(html: Path) -> list[tuple[int, str]]:
    """Return [(line_no, raw_hex), ...] for every hex literal in the file."""
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(html.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for m in HEX_RE.finditer(line):
            hits.append((lineno, m.group(0)))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=DEFAULT_OUTPUT_ROOT,
                    help="output/ root containing <deck>/slides/ (default: repo output/)")
    ap.add_argument("--deck", default=None, help="limit to a single deck slug under root")
    ap.add_argument("--preset", default=None, help="active preset (default: read active.json)")
    ap.add_argument("--palette", type=Path, default=None,
                    help="explicit colors_and_type.css to source theme hex from")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when FOREIGN (stale) hex found (default: warn-only, exit 0)")
    ap.add_argument("--any", action="store_true",
                    help="with --strict, fail on ANY hardcoded hex, not just FOREIGN")
    ap.add_argument("--quiet", action="store_true", help="suppress the clean/summary success line")
    args = ap.parse_args()

    if not args.root.exists():
        print(f"note: scan root does not exist: {args.root} (nothing to scan)", file=sys.stderr)
        return 0

    palette, palette_label = resolve_palette(args.preset, args.palette)

    n_files = 0
    n_foreign = 0
    n_theme = 0
    findings: list[str] = []
    for deck_name, html in iter_slide_html(args.root, args.deck):
        n_files += 1
        for lineno, raw in scan_file(html):
            norm = normalize_hex(raw)
            if not palette:
                tag = "hardcoded"
            elif norm in palette:
                tag = "theme"
                n_theme += 1
            else:
                tag = "FOREIGN"
                n_foreign += 1
            rel = html.relative_to(args.root)
            findings.append(f"  [{tag:9}] {rel}:{lineno}  {raw}")

    if findings:
        print(f"stale-hex guard -- palette: {palette_label}", file=sys.stderr)
        print(f"scanned {n_files} slide file(s); {len(findings)} hardcoded hex literal(s) found "
              f"(FOREIGN={n_foreign}, theme={n_theme}):", file=sys.stderr)
        for f in findings:
            print(f, file=sys.stderr)
        print("  -> deck slides should use helper classes + var(--*) tokens, not hex. "
              "FOREIGN hex is likely stale from a prior theme.", file=sys.stderr)
    elif not args.quiet:
        print(f"ok: stale-hex guard — {n_files} slide file(s) scanned, no hardcoded hex "
              f"(palette: {palette_label}).")

    if args.strict:
        if args.any and findings:
            return 1
        if n_foreign:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
