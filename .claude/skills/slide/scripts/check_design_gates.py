#!/usr/bin/env python3
"""check_design_gates.py — /slide Step 5 design self-check gates (B-checks).

Consolidates the gate logic that used to live INLINE in SKILL.md Step 5
(three copy-pasted python blocks). One deterministic, testable script:

  simple mode  (no slide_plan.json):
    B-r2-simple                chart/table-looking slide must carry a takeaway
    B-gm-simple                content slides must carry a .gm-band
    B-family-diversity-simple  >=6 slides need >=3 distinct filename slugs
  plan mode    (slide_plan.json present):
    B-plan-count               plan slide count == HTML slide count
    B-plan-fidelity            each core_message's keywords appear in its HTML
  both modes:
    B-density                  per-slide minimum line counts (plan override or
                               category default: chart/dense 80, general 60,
                               cover/section/closing 40)
    B-accent-card              card-accent <=1 per slide (anti-slop §5)
    B-dark-usage               card-dark / bg-text only on closing or terminal
                               slides (anti-slop §5)
    B-chrome-consistency       content slides agree on chrome markers — eyebrow
                               (.t-cap-up) / .rule / page counter (anti-slop §9)
    B-line-length              <p> line segments with Korean text stay short
                               (anti-slop §6 rule is 50 chars; the gate flags
                               only >60 to keep warn noise low)

Usage:
    python3 check_design_gates.py [<project-dir>] [--strict]

<project-dir> defaults to cwd and must contain slides/*.html.
Exit 0 = pass (or warn-only). Exit 1 = --strict and >=1 FAIL. Exit 2 = usage.

Default is WARN-only so heuristic false-positives never block a build; the
/slide workflow treats any FAIL line as must-fix before declaring the deck
complete (SKILL.md Step 5).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STOPWORDS = {
    "있다", "없다", "한다", "하는", "되는", "된다", "대한", "위한", "수", "것",
    "이", "그", "저", "등", "및", "또는",
    "that", "this", "with", "from", "have", "will", "they", "your", "their", "about",
}

# Ported from the historical inline SKILL.md checks. One deliberate divergence:
# the inline versions also matched `<svg`/`<canvas` — dead patterns here, since
# inline SVG is a forbidden path (html2pptx drops it; diagrams arrive as <img>).
CHART_VISUAL_RE = re.compile(r'class=\"chart|tbl-row|chart-|ev-bar|ev-col-track', re.I)
TAKEAWAY_RE = re.compile(r'gm-band|t-h3[^>]*c-accent|t-body[^>]*c-secondary[^>]*>[^<]{30,}', re.I)
STRUCTURAL_NAME_RE = re.compile(r'-cover\b|01-(title|cover)|closing|section')
DENSE_RE = re.compile(r'class=\"chart|tbl-row|chart-|ev-bar|ev-col-track|card-accent.*card-accent', re.I)

# anti-slop static checks (§5/§6/§9) — calibrated on shipped jangpm decks so
# clean decks pass with zero noise.
CARD_ACCENT_RE = re.compile(r'\bcard-accent\b')
DARK_RE = re.compile(r'\bcard-dark\b|\bbg-text\b')
TERMINAL_RE = re.compile(r'\bterm-window\b')
CLOSING_NAME_RE = re.compile(r'closing')
EYEBROW_RE = re.compile(r'\bt-cap-up\b')
RULE_RE = re.compile(r'class="[^"]*\brule\b')
PAGECTR_RE = re.compile(r'>\s*\d+\s*/\s*\d+\s*<')
P_BLOCK_RE = re.compile(r'<p\b[^>]*>(.*?)</p>', re.S)
BR_SPLIT_RE = re.compile(r'<br\s*/?>')
TAG_RE = re.compile(r'<[^>]+>')
KOREAN_RE = re.compile(r'[가-힣]')
LINE_LENGTH_FLAG = 60  # rule of record is 50 (anti-slop §6); flag only >60


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def check_simple(html_files: list[Path], results: list[tuple[str, str | None]]):
    # B-r2-simple: visual-bearing slide must also carry takeaway text
    r2_fails = []
    for f in html_files:
        c = read(f)
        if CHART_VISUAL_RE.search(c) and not TAKEAWAY_RE.search(c):
            r2_fails.append(f"{f.name}: visual but no takeaway text")
    results.append(("B-r2-simple", "; ".join(r2_fails) if r2_fails else None))

    # B-gm-simple: content slides (not cover/section/closing) carry .gm-band
    gm_fails = []
    for f in html_files:
        if STRUCTURAL_NAME_RE.search(f.name):
            continue
        if "gm-band" not in read(f):
            gm_fails.append(f"{f.name}: missing .gm-band")
    results.append(("B-gm-simple", "; ".join(gm_fails) if gm_fails else None))

    # B-family-diversity-simple: filename slug diversity (>=6 slides -> >=3 slugs)
    if len(html_files) >= 6:
        slugs = set()
        for f in html_files:
            m = re.match(r"\d+-([a-z-]+)\.html", f.name)
            if m:
                slugs.add(m.group(1))
        if len(slugs) < 3:
            results.append(("B-family-diversity-simple",
                            f"only {len(slugs)} distinct slide slugs in {len(html_files)} files "
                            f"— possible lazy repetition"))
        else:
            results.append(("B-family-diversity-simple", None))
    else:
        results.append(("B-family-diversity-simple", "SKIP (< 6 slides)"))


def check_plan(plan_path: Path, html_files: list[Path], results: list[tuple[str, str | None]]):
    try:
        plan_slides = json.loads(read(plan_path)).get("slides", [])
    except (json.JSONDecodeError, OSError) as e:
        results.append(("B-plan-count", f"slide_plan.json unreadable: {e}"))
        return []

    # B-plan-count
    if len(plan_slides) != len(html_files):
        results.append(("B-plan-count", f"plan={len(plan_slides)} vs HTML={len(html_files)}"))
    else:
        results.append(("B-plan-count", None))

    # B-plan-fidelity: core_message keywords must appear in the matching HTML
    fails = []
    for s in plan_slides:
        n = s.get("slide_number")
        matching = [f for f in html_files if re.match(rf"0*{n}-", f.name)]
        if not matching:
            fails.append(f"slide #{n}: no matching NN-*.html")
            continue
        html = read(matching[0])
        core = s.get("core_message", "")
        keywords = set(re.findall(r"[가-힣]{2,}|[A-Za-z]{4,}", core)) - STOPWORDS
        if not keywords:
            continue  # core_message too short — skip
        if not any(k in html for k in keywords):
            fails.append(f"slide #{n}: core_message keywords {sorted(keywords)[:5]} NOT in slide HTML")
    results.append(("B-plan-fidelity", "; ".join(fails) if fails else None))
    return plan_slides


def check_antislop_static(html_files: list[Path], results: list[tuple[str, str | None]]):
    """anti-slop §5/§6/§9 중 정적으로 정확히 검사 가능한 규칙들 (양쪽 모드 공통)."""
    # B-accent-card: card-accent는 슬라이드당 1개만 (anti-slop §5 "카드 강조는 1개만")
    fails = []
    for f in html_files:
        n = len(CARD_ACCENT_RE.findall(read(f)))
        if n >= 2:
            fails.append(f"{f.name}: card-accent x{n} (max 1)")
    results.append(("B-accent-card", "; ".join(fails) if fails else None))

    # B-dark-usage: 다크 카드(card-dark/bg-text)는 closing 또는 terminal 슬라이드에만
    fails = []
    for f in html_files:
        c = read(f)
        if DARK_RE.search(c) and not CLOSING_NAME_RE.search(f.name) and not TERMINAL_RE.search(c):
            fails.append(f"{f.name}: card-dark/bg-text on a non-closing/non-terminal slide")
    results.append(("B-dark-usage", "; ".join(fails) if fails else None))

    # B-chrome-consistency: 콘텐츠 슬라이드들의 chrome 마커(eyebrow/.rule/페이지 카운터)가
    # 일관돼야 한다 — 마커를 다수(>=70%)가 쓰는데 일부만 빠지면 그 슬라이드를 지목.
    content = [f for f in html_files if not STRUCTURAL_NAME_RE.search(f.name)]
    if len(content) >= 4:
        fails = []
        markers = [("eyebrow(.t-cap-up)", EYEBROW_RE), ("divider(.rule)", RULE_RE),
                   ("page-counter(N / M)", PAGECTR_RE)]
        contents = {f: read(f) for f in content}
        for label, rx in markers:
            have = [f for f in content if rx.search(contents[f])]
            if len(have) / len(content) >= 0.7 and len(have) < len(content):
                missing = [f.name for f in content if f not in have]
                fails.append(f"{label} missing on {missing} ({len(have)}/{len(content)} slides have it)")
        results.append(("B-chrome-consistency", "; ".join(fails) if fails else None))
    else:
        results.append(("B-chrome-consistency", "SKIP (< 4 content slides)"))

    # B-line-length: <p> 안 한 줄 세그먼트(한글 포함)가 과도하게 길면 지목
    fails = []
    for f in html_files:
        long_lines = []
        for m in P_BLOCK_RE.finditer(read(f)):
            for seg in BR_SPLIT_RE.split(m.group(1)):
                txt = re.sub(r"\s+", " ", TAG_RE.sub("", seg)).strip()
                if len(txt) > LINE_LENGTH_FLAG and KOREAN_RE.search(txt):
                    long_lines.append(f'"{txt[:24]}…"({len(txt)}자)')
        if long_lines:
            fails.append(f"{f.name}: {', '.join(long_lines)}")
    results.append(("B-line-length", "; ".join(fails) if fails else None))


def check_density(plan_slides: list, html_files: list[Path], results: list[tuple[str, str | None]]):
    plan = {s["slide_number"]: s for s in plan_slides if "slide_number" in s}
    fails = []
    for f in html_files:
        c = read(f)
        lines = c.count("\n") + 1
        m = re.match(r"^(\d+)-", f.name)
        n = int(m.group(1)) if m else None
        if n and n in plan and isinstance(plan[n].get("min_lines_estimate"), (int, float)):
            thr, src = int(plan[n]["min_lines_estimate"]), "plan"
        elif DENSE_RE.search(c):
            thr, src = 80, "simple-chart/dense"
        elif STRUCTURAL_NAME_RE.search(f.name):
            thr, src = 40, "simple-section/cover/closing"
        else:
            thr, src = 60, "simple-general"
        if lines < thr:
            fails.append(f"{f.name}:lines={lines}<{thr}({src})")
    results.append(("B-density", "; ".join(fails) if fails else None))


def main(argv: list[str]) -> int:
    for _s in (sys.stdout, sys.stderr):
        if hasattr(_s, "reconfigure"):
            _s.reconfigure(encoding="utf-8")

    strict = "--strict" in argv
    pos = [a for a in argv if not a.startswith("--")]
    project = Path(pos[0]).resolve() if pos else Path.cwd()
    slides_dir = project / "slides"
    if not slides_dir.is_dir():
        sys.stderr.write(f"usage: check_design_gates.py [<project-dir>] [--strict]\n"
                         f"  (no slides/ dir under {project})\n")
        return 2

    html_files = sorted(slides_dir.glob("*.html"))
    plan_path = project / "slide_plan.json"
    results: list[tuple[str, str | None]] = []

    if plan_path.exists():
        for name in ("B-r2-simple", "B-gm-simple", "B-family-diversity-simple"):
            results.append((name, "SKIP (plan-mode 활성)"))
        plan_slides = check_plan(plan_path, html_files, results)
    else:
        check_simple(html_files, results)
        for name in ("B-plan-count", "B-plan-fidelity"):
            results.append((name, "SKIP (simple mode)"))
        plan_slides = []

    check_density(plan_slides, html_files, results)
    check_antislop_static(html_files, results)

    n_fail = 0
    for name, detail in results:
        if detail is None:
            print(f"{name}: PASS")
        elif detail.startswith("SKIP"):
            print(f"{name}: {detail}")
        else:
            print(f"{name} FAIL: {detail}")
            n_fail += 1

    if n_fail:
        tag = "FAIL" if strict else "WARN"
        print(f"[{'x' if strict else '!'}] check_design_gates: {n_fail} gate(s) {tag} "
              f"for {project.name} — /slide Step 5: FAIL 항목은 데크 완료 선언 전 수정")
        return 1 if strict else 0
    print(f"[ok] check_design_gates: {project.name} passed ({len(html_files)} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
