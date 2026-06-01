#!/usr/bin/env python3
"""Render brand-spec-generated.md from theme.json."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _token_render import render, load_theme  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_TPL = SKILL / "templates" / "brand-spec.tpl.md"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tpl", type=Path, default=DEFAULT_TPL)
    args = ap.parse_args()

    theme = load_theme(args.theme)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        render(args.tpl.read_text(encoding="utf-8"), theme),
        encoding="utf-8",
    )
    print(f"wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
