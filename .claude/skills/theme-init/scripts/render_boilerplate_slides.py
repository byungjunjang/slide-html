#!/usr/bin/env python3
"""Render all boilerplate slides for a target preset.

Reads `*.tpl.html` from --source and writes `*.html` to --out-dir.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _token_render import render, load_theme  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = SKILL / "templates" / "boilerplate"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = ap.parse_args()

    theme = load_theme(args.theme)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    rendered = []
    for tpl in sorted(args.source.glob("*.tpl.html")):
        out_name = tpl.name.replace(".tpl.html", ".html")
        out_path = args.out_dir / out_name
        out_path.write_text(render(tpl.read_text(encoding="utf-8"), theme),
                            encoding="utf-8")
        rendered.append(out_name)

    print(f"rendered {len(rendered)} slides into {args.out_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
