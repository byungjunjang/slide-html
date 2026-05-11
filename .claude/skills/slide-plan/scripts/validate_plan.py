#!/usr/bin/env python3
"""Validate a slide_plan.json against R1-R5 universal discipline.

R2 (chart/table strategy ↔ takeaway pairing) and R5 (evidence_sources
non-empty) are HARD checks that exit 1 to block downstream builds.
R1 (per-slide reasoning fields), R3 (slide count 1..20), and R4 (no
3+ consecutive same layout_family) are lint warnings on stderr only.

Usage: validate_plan.py <plan.json>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


R1_FIELDS = (
    "core_message",
    "audience_takeaway",
    "why_here",
    "recommended_layout_family",
)


def _is_nonempty_str(v: Any) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_nonempty_list(v: Any) -> bool:
    return isinstance(v, list) and len(v) > 0


def check_r2(slides: list[dict]) -> list[str]:
    """chart/table_strategy non-empty → matching takeaway non-empty. HARD."""
    violations: list[str] = []
    for s in slides:
        n = s.get("slide_number", "?")
        for kind in ("chart", "table"):
            strat = s.get(f"{kind}_strategy")
            takeaway = s.get(f"{kind}_takeaway")
            if _is_nonempty_str(strat) and not _is_nonempty_str(takeaway):
                violations.append(
                    f"R2: slide {n} has {kind}_strategy='{strat}' "
                    f"but {kind}_takeaway is missing/empty"
                )
    return violations


def check_r5(slides: list[dict]) -> list[str]:
    """evidence_sources OR content_constraints.evidence_to_use non-empty. HARD."""
    violations: list[str] = []
    for s in slides:
        n = s.get("slide_number", "?")
        sources = s.get("evidence_sources")
        constraints = s.get("content_constraints") or {}
        evidence_to_use = constraints.get("evidence_to_use")
        if not _is_nonempty_list(sources) and not _is_nonempty_list(evidence_to_use):
            violations.append(
                f"R5: slide {n} has empty evidence_sources and "
                f"empty content_constraints.evidence_to_use"
            )
    return violations


def lint_r1(slides: list[dict]) -> list[str]:
    warnings: list[str] = []
    for s in slides:
        n = s.get("slide_number", "?")
        for f in R1_FIELDS:
            if not _is_nonempty_str(s.get(f)):
                warnings.append(f"R1: slide {n} missing/empty '{f}'")
    return warnings


def lint_r3(slides: list[dict]) -> list[str]:
    n = len(slides)
    if n == 0:
        return ["R3: slides[] is empty"]
    if n > 20:
        return [f"R3: slides[] has {n} slides (>20) — consider split/merge/defer"]
    return []


def lint_r4(slides: list[dict]) -> list[str]:
    """warn on 3+ consecutive same recommended_layout_family."""
    warnings: list[str] = []
    run_family: str | None = None
    run_start = 0
    run_len = 0
    for s in slides:
        fam = s.get("recommended_layout_family") or ""
        n = s.get("slide_number", "?")
        if fam and fam == run_family:
            run_len += 1
        else:
            if run_len >= 3:
                warnings.append(
                    f"R4: layout_family '{run_family}' repeats {run_len} consecutive slides "
                    f"starting at slide {run_start}"
                )
            run_family = fam
            run_start = n
            run_len = 1 if fam else 0
    if run_len >= 3:
        warnings.append(
            f"R4: layout_family '{run_family}' repeats {run_len} consecutive slides "
            f"starting at slide {run_start}"
        )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate slide_plan.json against R1-R5.")
    parser.add_argument("plan", type=Path, help="Path to slide_plan.json")
    args = parser.parse_args()

    if not args.plan.exists():
        print(f"error: plan not found: {args.plan}", file=sys.stderr)
        return 2
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    slides = data.get("slides") or []
    if not isinstance(slides, list):
        print("error: 'slides' must be an array", file=sys.stderr)
        return 2

    # HARD checks first — any violation blocks.
    hard_violations = check_r2(slides) + check_r5(slides)
    if hard_violations:
        for msg in hard_violations:
            print(msg, file=sys.stderr)
        return 1

    # Lint (stderr only, exit 0).
    for msg in lint_r1(slides) + lint_r3(slides) + lint_r4(slides):
        print(f"warning: {msg}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
