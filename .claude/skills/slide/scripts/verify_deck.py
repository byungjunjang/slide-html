#!/usr/bin/env python3
"""verify_deck.py - slide-html dual-host completion gate.

Inspects a BUILT deck (output/<project>-pptx/ + its <project>.pptx) and
hard-fails when the "golden output" traces a real /slide run leaves behind are
missing - exactly the traces Codex shortcut runs omitted. Path-agnostic:
resolves sibling scripts from __file__, so it runs identically from
.claude/skills or .codex/skills.

Usage:
    python3 verify_deck.py <project-dir> [--strict]

Exit 0 = all HARD checks pass. Exit 1 = >=1 HARD check failed.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

SLIDE_SKILL_DIR = Path(__file__).resolve().parent.parent          # .../skills/slide
SKILLS_ROOT = SLIDE_SKILL_DIR.parent                              # .../skills
SYNC_SCRIPT = SLIDE_SKILL_DIR / "scripts" / "dev" / "sync_codex_mirror.py"
VALIDATE_PLAN = SKILLS_ROOT / "slide-plan" / "scripts" / "validate_plan.py"

# Thresholds VALIDATED against the three golden Claude decks (Task 11): real
# decks sit far above these floors (media 0.8-3.8MB, runs 25-33/slide), while
# the placeholder failure mode (~60KB media) falls below MIN_MEDIA_BYTES_WHEN_SLOTS.
MIN_PPTX_BYTES = 50_000
MIN_MEDIA_BYTES_WHEN_SLOTS = 120_000   # placeholder-only deck (~60KB) sits below
MIN_RUNS_PER_SLIDE = 6                 # WARN heuristic (scaled, not absolute 286)
PLAN_AUTO_THRESHOLD = 10               # slide-html SKILL.md: >=10 -> systematic

A_T = re.compile(rb"<a:t>")
IMG_REF = re.compile(r"""<img[^>]*\bsrc\s*=\s*["']([^"']+)["']""", re.I)
DATA_SLOT = re.compile(r"""data-image-slot""", re.I)
IMG_PLACEHOLDER = re.compile(r"""class\s*=\s*["'][^"']*\bimg-placeholder\b""", re.I)


class Gate:
    def __init__(self):
        self.hard, self.warn = [], []

    def H(self, ok, msg):
        if not ok:
            self.hard.append(msg)

    def W(self, ok, msg):
        if not ok:
            self.warn.append(msg)


def load_pptx(pptx: Path):
    slides, media = {}, {}
    with zipfile.ZipFile(pptx) as zf:
        for name in zf.namelist():
            if re.match(r"ppt/slides/slide\d+\.xml$", name):
                slides[name] = zf.read(name)
            elif name.startswith("ppt/media/"):
                media[name] = zf.getinfo(name).file_size
    return slides, media


def check_integrity(g: Gate, pptx: Path) -> bool:
    g.H(pptx.exists(), f"PPTX missing: {pptx.name}")
    if not pptx.exists():
        return False
    g.H(pptx.stat().st_size >= MIN_PPTX_BYTES,
        f"PPTX too small: {pptx.stat().st_size}B < {MIN_PPTX_BYTES}B")
    try:
        with zipfile.ZipFile(pptx) as zf:
            g.H(zf.testzip() is None, "PPTX zip is corrupt")
        return True
    except zipfile.BadZipFile:
        g.H(False, "PPTX is not a valid zip")
        return False


def check_nativeness(g: Gate, slides: dict):
    flat = sorted(n for n, xml in slides.items() if not A_T.search(xml))
    g.H(not flat, f"Image-flattened slides (no editable <a:t>): {flat}")


def check_text_runs(g: Gate, slides: dict):
    total = sum(len(A_T.findall(xml)) for xml in slides.values())
    n = len(slides) or 1
    g.W(total >= MIN_RUNS_PER_SLIDE * n,
        f"Low text-run count: {total} over {n} slides "
        f"(< {MIN_RUNS_PER_SLIDE * n}; placeholder/sparse deck?)")


def check_images(g: Gate, project: Path, media: dict):
    slides_dir = project / "slides"
    missing, placeholder_slots, declared = [], [], False
    for html in sorted(slides_dir.glob("*.html")):
        text = html.read_text(encoding="utf-8", errors="ignore")
        if DATA_SLOT.search(text):
            declared = True
            if IMG_PLACEHOLDER.search(text):
                placeholder_slots.append(html.name)
        for src in IMG_REF.findall(text):
            if src.startswith(("http://", "https://", "data:")):
                continue
            # A real <img> into the deck's images/ dir is an image slot; a bare
            # "/images/" elsewhere (prose/comment/CSS) must NOT arm the floor.
            if "/images/" in src or src.startswith("images/"):
                declared = True
            if not (slides_dir / src).resolve().exists():
                missing.append(f"{html.name} -> {src}")
    g.H(not placeholder_slots,
        "Placeholder fallback still declares data-image-slot; remove the "
        f"data-image-slot marker or generate a real images/<slot>.png asset: {placeholder_slots}")
    g.H(not missing, f"Dangling <img> references (file missing): {missing}")
    if declared:
        total = sum(media.values())
        g.H(total >= MIN_MEDIA_BYTES_WHEN_SLOTS,
            f"Image slots declared but ppt/media total {total}B "
            f"< {MIN_MEDIA_BYTES_WHEN_SLOTS}B (placeholder-only deck?)")


def check_plan(g: Gate, project: Path, n_slides: int):
    plan = project / "slide_plan.json"
    mode = project / ".deck-mode"
    bypass = mode.exists() and mode.read_text(encoding="utf-8").strip() == "simple"
    if plan.exists():
        if VALIDATE_PLAN.exists():
            try:
                r = subprocess.run([sys.executable, str(VALIDATE_PLAN), str(plan)], timeout=30)
                g.H(r.returncode == 0, "slide_plan.json failed validate_plan.py")
            except subprocess.TimeoutExpired:
                g.H(False, "validate_plan.py timed out (>30s)")
        try:
            ps = json.loads(plan.read_text(encoding="utf-8")).get("slides", [])
            g.H(len(ps) == n_slides, f"B-plan-count: plan={len(ps)} vs HTML={n_slides}")
        except Exception as e:
            g.H(False, f"slide_plan.json unreadable: {e}")
    else:
        g.H(n_slides < PLAN_AUTO_THRESHOLD or bypass,
            f"Deck has {n_slides} slides (>= {PLAN_AUTO_THRESHOLD}) but no slide_plan.json "
            f"and no '.deck-mode=simple' bypass marker - systematic plan required.")


def check_mirror(g: Gate):
    if SYNC_SCRIPT.exists():
        try:
            r = subprocess.run([sys.executable, str(SYNC_SCRIPT), "--check"], timeout=60)
            g.H(r.returncode == 0, "`.codex/skills` mirror stale - run sync_codex_mirror.py")
        except subprocess.TimeoutExpired:
            g.H(False, "sync_codex_mirror.py --check timed out (>60s)")


def main(argv: list) -> int:
    strict = "--strict" in argv
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        sys.stderr.write("usage: verify_deck.py <project-dir> [--strict]\n")
        return 2
    project = Path(pos[0]).resolve()
    slug = project.name[:-5] if project.name.endswith("-pptx") else project.name
    pptx = project / f"{slug}.pptx"
    n_slides = len(list((project / "slides").glob("*.html")))

    g = Gate()
    if check_integrity(g, pptx):
        slides, media = load_pptx(pptx)
        check_nativeness(g, slides)
        check_text_runs(g, slides)
        check_images(g, project, media)
    check_plan(g, project, n_slides)
    check_mirror(g)

    for w in g.warn:
        if not strict:
            print(f"  WARN  {w}")
    if strict:
        g.hard.extend(g.warn)
    for h in g.hard:
        print(f"  FAIL  {h}")
    if g.hard:
        print(f"[x] verify_deck: {len(g.hard)} hard failure(s) for {project.name}")
        return 1
    print(f"[ok] verify_deck: {project.name} passed "
          f"({n_slides} slides, {len(g.warn)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
