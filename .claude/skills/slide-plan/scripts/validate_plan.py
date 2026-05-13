#!/usr/bin/env python3
"""Validate slide_plan.json against Layer 1 R1-R5 + enum constraints.

Three slide pipelines (slide-html, slide-svg, slide-pencil) share R1-R5 as the
universal contract. slide-html's layout_family vocabulary is preset-defined
(jangpm has 30+ families across 6 categories), so the validator pulls the
allowed set from the plan's own `design_dependency.allowed_layout_families`
list instead of a hardcoded enum.

Usage:
    python3 validate_plan.py <path/to/slide_plan.json>

Exit code:
    0 — all checks passed (warnings may be printed)
    1 — one or more hard rejects; the plan is not consumable by /slide
    2 — usage error (bad path, invalid JSON)
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Common chart_strategy enum (10 values) — shared with slide-pencil / slide-svg.
CHART_STRATEGIES = {
    "growth-trend", "forecast", "structural-break", "focus-comparison",
    "distribution", "quadrant", "priority-matrix", "split-segment", "funnel",
    "custom",
}

PAGE_FAMILIES = {"title", "chapter", "body", "end", "appendix"}

UNIVERSAL_ROLES = {
    "cover", "context", "agenda", "insight", "evidence",
    "solution", "summary", "closing", "cta", "appendix",
}

ROLE_EXTENSIONS = {
    "educational": {"concept", "example", "exercise", "recap", "qna"},
    "report": {"executive_summary", "findings", "methodology"},
    "consulting": {"problem", "comparison", "roadmap", "bottom_line"},
    "sales": {"problem", "proof", "comparison", "pricing", "roadmap"},
    "internal_update": {"status_summary", "progress", "blockers", "next_steps", "asks"},
    "proposal": {"problem", "comparison", "pricing", "team", "roadmap"},
    "keynote": {"hook", "vision", "demo", "availability"},
}

DECK_TYPES = set(ROLE_EXTENSIONS.keys()) | {"unknown"}

BLOCK_TYPES = {
    "title", "subtitle", "bullets", "chart", "table", "callout", "quote",
    "metric_cards", "icon_group", "infographic", "diagram_flow",
    "image", "code", "footer_note",
}

VISUAL_BLOCK_TYPES = {
    "chart", "table", "callout", "metric_cards", "icon_group",
    "infographic", "diagram_flow", "image",
}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> bool:
        return not self.errors


def slide_label(slide: dict[str, Any]) -> str:
    n = slide.get("slide_number", "?")
    title = slide.get("working_title", "")
    return f"slide #{n} ({title!r})" if title else f"slide #{n}"


def check_deck_meta(plan: dict[str, Any], r: Report) -> None:
    meta = plan.get("deck_meta")
    if not isinstance(meta, dict):
        r.err("deck_meta missing or not an object")
        return

    deck_type = meta.get("deck_type")
    if deck_type not in DECK_TYPES:
        r.err(f"deck_meta.deck_type {deck_type!r} not in enum {sorted(DECK_TYPES)}")

    target_length = meta.get("target_length")
    if isinstance(target_length, dict):
        n = target_length.get("slides")
        if isinstance(n, int) and n > 0:
            actual = len(plan.get("slides", []))
            if actual != n:
                r.warn(
                    f"deck_meta.target_length.slides ({n}) != actual slide count ({actual})"
                )


def resolve_allowed_families(plan: dict[str, Any], r: Report) -> set[str] | None:
    """slide-html: pull layout_family enum from the plan itself (preset-driven).

    Returns None if the plan doesn't declare one — in which case we fall back to
    a sanity check (non-empty string ≥ 2 chars).
    """
    dd = plan.get("design_dependency")
    if not isinstance(dd, dict):
        r.warn("design_dependency missing — layout_family validation falls back to sanity check")
        return None

    preset_name = dd.get("preset_name")
    design_md = dd.get("design_md_path")
    if preset_name and design_md:
        p = Path(design_md)
        if not p.exists():
            r.warn(f"design_dependency.design_md_path {design_md!r} does not exist on disk")

    allowed = dd.get("allowed_layout_families")
    if not isinstance(allowed, list) or not allowed:
        r.warn(
            "design_dependency.allowed_layout_families missing — "
            "layout_family validation falls back to sanity check"
        )
        return None
    return {f for f in allowed if isinstance(f, str)}


def allowed_roles_for(deck_type: str) -> set[str]:
    return UNIVERSAL_ROLES | ROLE_EXTENSIONS.get(deck_type, set())


def check_slide_r1(slide: dict[str, Any], allowed_families: set[str] | None, r: Report) -> None:
    """R1 — per-slide rationale (4 fields)."""
    label = slide_label(slide)
    for field_name in ("core_message", "audience_takeaway", "why_here"):
        value = slide.get(field_name)
        if not isinstance(value, str) or not value.strip():
            r.err(f"R1 violation — {label}: {field_name!r} missing or empty")

    family = slide.get("recommended_layout_family")
    if not isinstance(family, str) or len(family.strip()) < 2:
        r.err(f"R1 violation — {label}: recommended_layout_family missing or too short")
        return

    if allowed_families is not None and family not in allowed_families:
        r.err(
            f"R1 violation — {label}: recommended_layout_family {family!r} "
            f"not in design_dependency.allowed_layout_families {sorted(allowed_families)}"
        )


def check_slide_r2(slide: dict[str, Any], r: Report) -> None:
    """R2 — visual-led slides require takeaway text."""
    label = slide_label(slide)
    cs = slide.get("chart_strategy")
    if cs is not None:
        if cs not in CHART_STRATEGIES:
            r.warn(
                f"R2 soft warning — {label}: chart_strategy {cs!r} "
                f"not in canonical enum {sorted(CHART_STRATEGIES)} — "
                f"use 'custom' for preset-specific strategies"
            )
        ct = slide.get("chart_takeaway")
        if not isinstance(ct, str) or not ct.strip():
            r.err(
                f"R2 violation — {label}: chart_strategy is set but "
                f"chart_takeaway is missing or empty"
            )

    has_table_block = any(
        isinstance(b, dict) and b.get("block_type") == "table"
        for b in slide.get("content_blocks", []) or []
    )
    if slide.get("table_strategy") or has_table_block:
        tt = slide.get("table_takeaway")
        if not isinstance(tt, str) or not tt.strip():
            r.err(
                f"R2 violation — {label}: a table strategy/block is present but "
                f"table_takeaway is missing or empty"
            )


def check_slide_r5(slide: dict[str, Any], inventory_ids: set[str], r: Report) -> None:
    """R5 — evidence_sources (or content_constraints.evidence_to_use) non-empty."""
    label = slide_label(slide)
    sources = slide.get("evidence_sources")
    constraints = slide.get("content_constraints") or {}
    evidence_to_use = constraints.get("evidence_to_use") if isinstance(constraints, dict) else None

    if (not isinstance(sources, list) or len(sources) == 0) and (
        not isinstance(evidence_to_use, list) or len(evidence_to_use) == 0
    ):
        r.err(
            f"R5 violation — {label}: both evidence_sources and "
            f"content_constraints.evidence_to_use are missing/empty"
        )
        return

    for src in (sources or []):
        if not isinstance(src, str):
            r.err(f"R5 violation — {label}: evidence_sources entries must be strings")
            continue
        if src in ("inference", "common-knowledge"):
            continue
        if inventory_ids and src not in inventory_ids:
            r.warn(
                f"R5 soft warning — {label}: evidence source {src!r} "
                f"does not match any content_inventory[].source_id "
                f"(inventory has: {sorted(inventory_ids)})"
            )


def check_slide_role(slide: dict[str, Any], deck_type: str, r: Report) -> None:
    label = slide_label(slide)
    role = slide.get("slide_role")
    allowed = allowed_roles_for(deck_type)
    if role is None or role not in allowed:
        r.warn(
            f"slide_role {role!r} on {label} not in allowed set for "
            f"deck_type={deck_type!r}: {sorted(allowed)} (soft warning — slide-html "
            f"allows preset-specific roles)"
        )

    page_family = slide.get("page_family")
    if page_family is not None and page_family not in PAGE_FAMILIES:
        r.warn(
            f"page_family {page_family!r} on {label} not in enum {sorted(PAGE_FAMILIES)}"
        )


def check_block_types(slide: dict[str, Any], r: Report) -> None:
    label = slide_label(slide)
    for i, b in enumerate(slide.get("content_blocks") or []):
        if not isinstance(b, dict):
            r.err(f"{label}: content_blocks[{i}] is not an object")
            continue
        bt = b.get("block_type")
        if bt not in BLOCK_TYPES:
            r.warn(
                f"{label}: content_blocks[{i}].block_type {bt!r} "
                f"not in canonical enum {sorted(BLOCK_TYPES)}"
            )


def check_r4_lazy_repetition(slides: list[dict[str, Any]], r: Report) -> None:
    """R4 — no 3+ consecutive same family (except `section-divider` / `cover`)."""
    if not slides:
        return

    exempt = {"section-divider", "cover"}

    def report(start: int, end: int, fam: str | None) -> None:
        length = end - start + 1
        if length < 3 or fam in exempt or fam is None:
            return
        slide_nums = [
            slides[j].get("slide_number", j + 1) for j in range(start, end + 1)
        ]
        justifications_present = all(
            isinstance(slides[j].get("why_here"), str)
            and len(slides[j]["why_here"].strip()) >= 20
            for j in range(start, end + 1)
        )
        if not justifications_present:
            r.err(
                f"R4 violation — slides {slide_nums} use the same "
                f"recommended_layout_family={fam!r} for {length} "
                f"consecutive slides without sufficient why_here justification "
                f"(each must be ≥ 20 chars)"
            )

    streak_start = 0
    streak_family = slides[0].get("recommended_layout_family")
    for i in range(1, len(slides)):
        fam = slides[i].get("recommended_layout_family")
        if fam != streak_family:
            report(streak_start, i - 1, streak_family)
            streak_start = i
            streak_family = fam
    report(streak_start, len(slides) - 1, streak_family)


def check_r4_min_diversity(slides: list[dict[str, Any]], r: Report) -> None:
    """R4 — minimum distinct layout families per deck."""
    families = {s.get("recommended_layout_family") for s in slides}
    families.discard(None)
    n = len(slides)
    if n >= 10 and len(families) < 4:
        r.err(
            f"R4 violation — deck has {n} slides but only {len(families)} distinct "
            f"layout families ({sorted(f for f in families if f)}); need ≥ 4 for ≥ 10 slides"
        )
    elif n >= 6 and len(families) < 3:
        r.err(
            f"R4 violation — deck uses only {len(families)} distinct layout families "
            f"({sorted(f for f in families if f)}); need at least 3 for any deck ≥ 6 slides"
        )


def check_r3_length(plan: dict[str, Any], slides: list[dict[str, Any]], r: Report) -> None:
    n = len(slides)
    if n > 20:
        ordering = plan.get("ordering_notes")
        if not isinstance(ordering, dict) or not any(
            ordering.get(k) for k in (
                "split_topics", "merged_topics", "deferred_topics", "appendix_candidates"
            )
        ):
            r.warn(
                f"R3 warning — deck has {n} slides (> 20); ordering_notes should "
                f"document split/merge/defer candidates"
            )


def check_diagnostic_ratios(slides: list[dict[str, Any]], r: Report) -> None:
    roles = [s.get("slide_role") for s in slides]
    n = len(slides)
    if n == 0:
        return

    evidence_count = sum(1 for x in roles if x in ("evidence", "findings", "proof", "progress"))
    insight_count = sum(1 for x in roles if x in ("insight", "executive_summary", "hook", "vision", "bottom_line"))

    if insight_count > 0 and evidence_count > 5 * insight_count:
        r.warn(
            f"diagnostic — research dump risk: evidence={evidence_count} ≫ insight={insight_count}. "
            f"Consider adding insight slides between findings."
        )

    if insight_count > evidence_count and n > 8:
        r.warn(
            f"diagnostic — assertion-only risk: insight={insight_count} > evidence={evidence_count} "
            f"with {n} slides. Consider backing insights with data."
        )

    first_three = roles[:3]
    if not any(x in ("insight", "hook", "executive_summary", "bottom_line") for x in first_three):
        r.warn(
            "diagnostic — no opening punch: first 3 slides have no "
            "insight / hook / executive_summary role."
        )

    last_two = roles[-2:] if n >= 2 else roles
    if "cta" not in last_two and "summary" not in last_two and "closing" not in last_two:
        r.warn(
            "diagnostic — buried CTA: last 2 slides do not include a "
            "`cta` / `summary` / `closing` role."
        )


def check_fact_check_log(plan: dict[str, Any], slides: list[dict[str, Any]], r: Report) -> None:
    """fact_check_log audit (advisory).

    - Decks ≥ 7 slides should have a non-empty fact_check_log.
    - Unverified ratio > 40% raises a warning.
    """
    fcl = plan.get("fact_check_log")
    n = len(slides)
    if n >= 7 and (not isinstance(fcl, list) or len(fcl) == 0):
        r.warn(
            f"fact-check missing — deck has {n} slides (≥ 7) but fact_check_log is empty. "
            f"Run Step 5.5 (WebSearch claim verification) or add explicit "
            f"'사실 확인 불필요' note in deck_meta."
        )
        return

    if not isinstance(fcl, list) or not fcl:
        return

    status_count = {"verified": 0, "corrected": 0, "unverified": 0}
    for i, entry in enumerate(fcl):
        if not isinstance(entry, dict):
            r.warn(f"fact_check_log[{i}] not an object")
            continue
        s = entry.get("status")
        if s in status_count:
            status_count[s] += 1
        for required in ("claim", "slide_number", "status", "checked_at"):
            if required not in entry:
                r.warn(f"fact_check_log[{i}] missing required field {required!r}")
    total = sum(status_count.values())
    if total > 0:
        unverified_ratio = status_count["unverified"] / total
        if unverified_ratio > 0.4:
            r.warn(
                f"fact-check — {status_count['unverified']}/{total} claims unverified "
                f"({unverified_ratio:.0%} > 40% threshold). Review HIGH-priority claims."
            )


def validate(plan_path: Path) -> Report:
    r = Report()
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        r.err(f"plan file not found: {plan_path}")
        return r
    except json.JSONDecodeError as e:
        r.err(f"plan file is not valid JSON: {e}")
        return r

    if not isinstance(plan, dict):
        r.err("plan root must be a JSON object")
        return r

    check_deck_meta(plan, r)
    allowed_families = resolve_allowed_families(plan, r)

    deck_type = (plan.get("deck_meta") or {}).get("deck_type", "unknown")

    inventory = plan.get("content_inventory") or []
    inventory_ids = {
        c.get("source_id")
        for c in inventory
        if isinstance(c, dict) and isinstance(c.get("source_id"), str)
    }

    slides = plan.get("slides")
    if not isinstance(slides, list) or not slides:
        r.err("slides[] missing or empty — a plan must contain at least one slide")
        return r

    for s in slides:
        if not isinstance(s, dict):
            r.err(f"slides[] entry is not an object: {s!r}")
            continue
        check_slide_r1(s, allowed_families, r)
        check_slide_r2(s, r)
        check_slide_r5(s, inventory_ids, r)
        check_slide_role(s, deck_type, r)
        check_block_types(s, r)

    check_r4_lazy_repetition(slides, r)
    check_r4_min_diversity(slides, r)
    check_r3_length(plan, slides, r)
    check_diagnostic_ratios(slides, r)
    check_fact_check_log(plan, slides, r)

    return r


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_plan.py <slide_plan.json>", file=sys.stderr)
        return 2

    plan_path = Path(argv[1])
    if not plan_path.exists():
        print(f"error: plan not found: {plan_path}", file=sys.stderr)
        return 2

    report = validate(plan_path)

    for w in report.warnings:
        print(f"WARN  {w}")
    for e in report.errors:
        print(f"ERROR {e}", file=sys.stderr)

    if report.ok():
        print(
            f"\nOK — slide_plan.json passes Layer 1 R1–R5 "
            f"({len(report.warnings)} warning(s))"
        )
        return 0

    print(
        f"\nFAIL — {len(report.errors)} error(s), {len(report.warnings)} warning(s). "
        f"Plan is NOT consumable by /slide until errors are fixed.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
