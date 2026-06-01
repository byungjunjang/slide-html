#!/usr/bin/env python3
"""Render colors_and_type.css from theme.json + tpl.css for a target preset.

Usage:
    python3 render_colors_and_type.py --theme <theme.json> --out <out.css>
    python3 render_colors_and_type.py --theme <theme.json> --out <out.css> \\
        --fonts-prelude <preset>/_fonts.css
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _token_render import render, load_theme  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_TPL = SKILL / "templates" / "colors_and_type.tpl.css"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tpl", type=Path, default=DEFAULT_TPL)
    ap.add_argument("--fonts-prelude", type=Path, default=None,
                    help="Optional CSS file (typically @font-face) prepended to the output.")
    args = ap.parse_args()

    theme = load_theme(args.theme)
    body = render(args.tpl.read_text(encoding="utf-8"), theme)

    prelude = ""
    if args.fonts_prelude and args.fonts_prelude.exists():
        prelude = args.fonts_prelude.read_text(encoding="utf-8").rstrip() + "\n\n"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(prelude + body, encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
