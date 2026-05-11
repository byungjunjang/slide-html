#!/usr/bin/env python3
"""Validate theme-active.json against token-contract.json v1.

Exit 0 on success, 1 on validation failure (errors printed to stderr in a
human-readable list), 2 on setup errors (missing files, missing dependency).

Called by init_theme.py between parse_design_guide.py and the render
scripts so no downstream file is written from an invalid theme.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

THEME_INIT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = THEME_INIT_ROOT / "references" / "token-contract.json"


def validate(theme: dict, contract: dict) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "jsonschema missing. Install with: pip install jsonschema"
        ) from e

    validator = jsonschema.Draft202012Validator(contract)
    errors = []
    for err in sorted(validator.iter_errors(theme), key=lambda e: e.absolute_path):
        path = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"  {path}: {err.message}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", type=Path, required=True)
    ap.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    ap.add_argument("--quiet", action="store_true", help="suppress success line")
    args = ap.parse_args()

    if not args.theme.exists():
        print(f"theme not found: {args.theme}", file=sys.stderr)
        return 2
    if not args.contract.exists():
        print(f"contract not found: {args.contract}", file=sys.stderr)
        return 2

    theme = json.loads(args.theme.read_text(encoding="utf-8"))
    contract = json.loads(args.contract.read_text(encoding="utf-8"))

    errors = validate(theme, contract)
    if errors:
        print(f"theme-active.json FAILS the v1 token contract ({len(errors)} error(s)):", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    if not args.quiet:
        display = theme.get("display_name", theme.get("name", "?"))
        print(f"ok: '{display}' ({theme.get('name', '?')}) conforms to token contract v{theme.get('version', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
