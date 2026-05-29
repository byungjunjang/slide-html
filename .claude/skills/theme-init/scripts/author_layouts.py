#!/usr/bin/env python3
"""theme-init Phase 2 — Layout Authoring deterministic harness.

The *creative* recomposition of identity slides is done by the agent (Claude)
following SKILL.md + references/layout-recipes.md. This script is the
deterministic scaffolding around that work:

    prep      reset identity slides to the .stock baseline, init/refresh the
              manifest, record source artifacts, print the agent's brief.
    classify  print identity (authored) vs data (token-tone) split.
    thumbs    render before(.stock) / after(authored) PNGs via Playwright for
              the user-review checkpoint.
    validate  build a scratch deck of authored slides → node build.mjs →
              unzip -t, plus a light html2pptx-safety lint. The completion gate.
    confirm   require validate passed, flip manifest status → confirmed, stamp
              DESIGN.md provenance.
    restore   undo authoring (copy identity slides back from .stock).
    status    print manifest summary.

Idempotent: prep always restores from .stock, so re-authoring never stacks on
top of a previous pass.

Usage:
    python3 author_layouts.py prep     --preset <name> [--design-md P] \\
            [--original-design-md P] [--reference P] [--direction "text"]
    python3 author_layouts.py classify --preset <name>
    python3 author_layouts.py thumbs   --preset <name>
    python3 author_layouts.py validate --preset <name>
    python3 author_layouts.py confirm  --preset <name>
    python3 author_layouts.py restore  --preset <name> [--stems 01-title,...]
    python3 author_layouts.py status   --preset <name>

    --presets-root defaults to the slide bundle's assets/design-systems/.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import _authoring_common as ac  # noqa: E402

SKILL = SCRIPTS.parent
REPO_ROOT = SCRIPTS.parents[3]                     # slide-html/
DEFAULT_PRESETS_ROOT = SCRIPTS.parents[1] / "slide" / "assets" / "design-systems"
INIT_PROJECT = SCRIPTS.parents[1] / "slide" / "scripts" / "init-project.sh"
RENDER_THUMBS = SCRIPTS / "render_thumbs.mjs"

# Pictographic emoji only. Deliberately EXCLUDES plain typographic dingbats the
# design system uses as text (→ ↑↓ ✓ ✗ ★ in process/KPI/summary slides). Flags
# U+1F000–1FAFF (emoji & pictographs), regional indicators, and any glyph carrying
# the U+FE0F emoji-presentation selector (e.g. ⚠️ ✅ ❌).
_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U0001F1E6-\U0001F1FF]|.️"
)


def _preset_dir(args) -> Path:
    return args.presets_root / args.preset


def _boilerplate_dir(args) -> Path:
    return _preset_dir(args) / "pptx-boilerplate"


def _require_stock(boilerplate_dir: Path) -> None:
    if not (boilerplate_dir / ac.STOCK_DIRNAME).exists():
        print(f"[author_layouts] no .stock baseline in {boilerplate_dir}.\n"
              f"  Run init_theme.py first (it snapshots the token-render output).",
              file=sys.stderr)
        sys.exit(2)


# ----------------------------------------------------------------------------
# scratch project (real project layout so ../_pptx-slide.css @import resolves)
# ----------------------------------------------------------------------------

def _scratch_project(args, slide_stems: list[str], src_dir: Path) -> Path:
    """Build output/_authoring-<preset>-pptx/ via init-project.sh, then replace
    slides/ with the requested stems copied from src_dir."""
    project = f"_authoring-{args.preset}"
    project_dir = REPO_ROOT / "output" / f"{project}-pptx"
    if project_dir.exists():
        shutil.rmtree(project_dir)
    r = subprocess.run(["bash", str(INIT_PROJECT), project, args.preset],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[author_layouts] init-project.sh failed:\n{r.stderr}\n{r.stdout}", file=sys.stderr)
        sys.exit(r.returncode)
    slides = project_dir / "slides"
    for f in slides.glob("*.html"):
        f.unlink()
    for stem in slide_stems:
        src = src_dir / f"{stem}.html"
        if src.exists():
            shutil.copy2(src, slides / f"{stem}.html")
    return project_dir


def _cleanup_scratch(args) -> None:
    """Remove the scratch project so it does not linger in output/ (E)."""
    project_dir = REPO_ROOT / "output" / f"_authoring-{args.preset}-pptx"
    if project_dir.exists():
        shutil.rmtree(project_dir)


_STATUS_RE = re.compile(r"^status:\s*([A-Za-z_]+)\s*$", re.MULTILINE)


def _design_status(args) -> str | None:
    """Read DESIGN.md frontmatter `status:` (not_authored / draft / confirmed)."""
    design = _preset_dir(args) / "DESIGN.md"
    if not design.exists():
        return None
    head = design.read_text(encoding="utf-8")[:1200]
    m = _STATUS_RE.search(head)
    return m.group(1) if m else None


# Leftover template placeholders that mean §5/§6 were never filled. Scanned at
# confirm time so slide-plan never inherits an empty visual vocabulary.
_PLACEHOLDER_MARKERS = ("(LLM 추출 자리", "(예:")
_PLACEHOLDER_GUIDE_RE = re.compile(
    r"^\(.*(채우세요|작성하세요|명시하세요|보강하세요).*$"
)


def _design_placeholders(args) -> list[str]:
    """Scan DESIGN.md §5 (visual vocabulary) + §6 (chrome) for unfilled template
    placeholder lines. Returns short samples of each finding ([] = clean)."""
    design = _preset_dir(args) / "DESIGN.md"
    if not design.exists():
        return []
    text = design.read_text(encoding="utf-8")
    m5 = re.search(r"^## 5\.", text, re.MULTILINE)
    m7 = re.search(r"^## 7\.", text, re.MULTILINE)
    if not m5:
        return []
    section = text[m5.start():(m7.start() if m7 else len(text))]
    hits: list[str] = []
    seen: set[str] = set()
    for ln in section.splitlines():
        s = ln.strip()
        if not s:
            continue
        if any(mk in s for mk in _PLACEHOLDER_MARKERS) or _PLACEHOLDER_GUIDE_RE.match(s):
            sample = s[:60]
            if sample not in seen:
                seen.add(sample)
                hits.append(sample)
    return hits


# ----------------------------------------------------------------------------
# reference-deck ingestion (Task 9) — recommend, never apply
# ----------------------------------------------------------------------------

_REF_BLOCK_START = "<!-- REF-INGEST:start -->"
_REF_BLOCK_END = "<!-- REF-INGEST:end -->"


def _current_card_style(args) -> str | None:
    tp = _preset_dir(args) / "theme.json"
    if not tp.exists():
        return None
    try:
        return json.loads(tp.read_text(encoding="utf-8")).get("surface", {}).get("card_style")
    except (json.JSONDecodeError, OSError):
        return None


def _seed_design_from_reference(args, result: dict) -> None:
    """Insert an additive, marker-fenced reference-hint blockquote into DESIGN.md §5.

    Does NOT touch the section's placeholder prompts — the strict confirm gate
    still requires the user to fill the canonical §5/§6 by hand. Re-running prep
    replaces the fenced block in place (idempotent).
    """
    design = _preset_dir(args) / "DESIGN.md"
    if not design.exists():
        return
    d = result["devices"]
    cs = d["card_style"]
    block = (
        f"{_REF_BLOCK_START}\n"
        f"> **참조 자동추출 초안** — `{result['source']}` ({result['slides_analyzed']} slides) 에서 측정한 "
        f"레이아웃 신호. 힌트일 뿐이며, 정식 §5/§6 항목은 아래에서 직접 검토·작성해야 합니다.\n"
        f"> - card_style: **{cs['value']}** [{cs['confidence']}]\n"
        f"> - surface 교차: {d['surface_alternation']['slides_using']}/{result['slides_analyzed']} slides\n"
        f"> - hairline divider: {d['hairline_dividers']['count']} · "
        f"CTA: {d['cta']['count']} · kicker: {d['kicker']['count']}\n"
        f"{_REF_BLOCK_END}"
    )
    text = design.read_text(encoding="utf-8")
    if _REF_BLOCK_START in text and _REF_BLOCK_END in text:
        text = re.sub(re.escape(_REF_BLOCK_START) + r".*?" + re.escape(_REF_BLOCK_END),
                      block, text, flags=re.DOTALL)
    else:
        m5 = re.search(r"^## 5\..*$", text, re.MULTILINE)
        if m5:
            text = text[:m5.end()] + "\n\n" + block + text[m5.end():]
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    design.write_text(text, encoding="utf-8")
    print("  · seeded DESIGN.md §5 reference-hint block (additive — placeholders intact)",
          file=sys.stderr)


def _ingest_reference(args, manifest: dict) -> None:
    """Parse --reference deck → store devices in manifest.blueprint, print a
    card_style recommendation (+ re-init command if it differs), seed DESIGN.md.
    Recommends only: never edits theme.json or re-renders."""
    try:
        import ingest_reference as ir
        result = ir.extract(args.reference)
    except Exception as e:  # noqa: BLE001 — ingestion is best-effort
        print(f"⚠ [prep] reference ingestion skipped ({e}); path recorded only", file=sys.stderr)
        return
    if not result.get("slides_analyzed"):
        print(f"⚠ [prep] reference has no *.html slides ({args.reference}); path recorded only",
              file=sys.stderr)
        return
    devices = result["devices"]
    manifest["blueprint"]["reference_devices"] = devices
    print("\n--- reference deck layout devices ---", file=sys.stderr)
    print(ir.summarize(result), file=sys.stderr)
    rec = devices["card_style"]["value"]
    current = _current_card_style(args)
    if rec and current and rec != current:
        init = SCRIPTS / "init_theme.py"
        print(f"\n⚠ reference suggests surface.card_style = '{rec}' (preset is '{current}').\n"
              f"  card_style is a Phase 1 token — to apply, re-run with the draft's "
              f"surface.card_style set to '{rec}':\n"
              f"    python3 {init} --from <draft.json> --preset {args.preset} --force",
              file=sys.stderr)
    elif rec and current:
        print(f"\n✓ reference card_style '{rec}' matches the preset.", file=sys.stderr)
    _seed_design_from_reference(args, result)


# ----------------------------------------------------------------------------
# commands
# ----------------------------------------------------------------------------

def cmd_prep(args) -> int:
    bp = _boilerplate_dir(args)
    _require_stock(bp)

    # (C) DESIGN.md §5/§6 are Phase 2 inputs — warn (or block) if not confirmed.
    status = _design_status(args)
    if status != "confirmed":
        msg = (f"[prep] DESIGN.md status is '{status or 'missing'}' (not confirmed). "
               f"Phase 2 consumes §5 visual vocabulary + §6 chrome — confirm them first:\n"
               f"  1. fill {_preset_dir(args) / 'DESIGN.md'} §5/§6\n"
               f"  2. set frontmatter status: draft → confirmed")
        if args.require_confirmed:
            print(msg + "\n[prep] blocked (--require-confirmed).", file=sys.stderr)
            return 2
        print("⚠ " + msg + "\n  (continuing anyway — pass --require-confirmed to enforce)\n",
              file=sys.stderr)

    cls = ac.classify(bp)
    # idempotency: always start identity slides from the deterministic baseline
    restored = ac.restore_from_stock(bp, cls["identity_flat"])
    m = ac.ensure_manifest(args.preset, bp)
    m["status"] = "draft"
    m["authored"] = []
    sa = m["source_artifacts"]
    if args.design_md:          sa["design_md"] = str(args.design_md)
    if args.original_design_md: sa["original_design_md"] = str(args.original_design_md)
    if args.reference:
        sa["reference_blueprint"] = str(args.reference)
        _ingest_reference(args, m)
    if args.direction:          sa["user_direction"] = args.direction
    m["verification"] = {"lint": None, "build": None, "unzip": None, "thumbs": None}
    ac.save_manifest(bp, m)

    print(f"=== Phase 2 prep · {args.preset} ===")
    print(f"identity slides reset to .stock baseline: {len(restored)}")
    for fam, stems in cls["identity_set"].items():
        print(f"  · {fam:<14} {', '.join(stems)}")
    print(f"data slides (keep token tone, DO NOT touch): {len(cls['data_set'])}")
    print("\nAgent brief — recompose ONLY the identity slides above:")
    print("  1. Read DESIGN.md §5 (visual vocabulary) + §6 (chrome) + the original design.md.")
    print("  2. Extract the brand's signature layout devices → record in manifest.blueprint.")
    print("  3. Rewrite each identity slide HTML using references/layout-recipes.md")
    print("     (helper classes + literal hex only, no gradients; 4-constraints; 960x540).")
    print("  4. Run: author_layouts.py validate  → then  thumbs  → review → revise → confirm.")
    print(f"\nmanifest: {ac.manifest_path(bp)} (status: draft)")
    return 0


def cmd_classify(args) -> int:
    bp = _boilerplate_dir(args)
    cls = ac.classify(bp)
    print(json.dumps(cls, indent=2, ensure_ascii=False))
    return 0


def cmd_thumbs(args) -> int:
    bp = _boilerplate_dir(args)
    _require_stock(bp)
    if not RENDER_THUMBS.exists():
        print(f"[author_layouts] missing {RENDER_THUMBS}", file=sys.stderr)
        return 2
    cls = ac.classify(bp)
    stems = cls["identity_flat"]
    thumbs_out = bp / ac.THUMBS_DIRNAME
    thumbs_out.mkdir(exist_ok=True)

    def _render(src_dir: Path, tag: str) -> int:
        project = _scratch_project(args, stems, src_dir)
        r = subprocess.run(
            ["node", str(RENDER_THUMBS),
             "--project", str(project), "--out", str(thumbs_out), "--tag", tag],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        sys.stderr.write(r.stderr)
        return r.returncode

    rc_before = _render(bp / ac.STOCK_DIRNAME, "stock")
    rc_after = _render(bp, "authored")
    _cleanup_scratch(args)
    ok = rc_before == 0 and rc_after == 0
    m = ac.load_manifest(bp) or ac.new_manifest(args.preset, bp)
    m["verification"]["thumbs"] = "ok" if ok else "failed"
    ac.save_manifest(bp, m)
    print(f"\nthumbnails → {thumbs_out}  (NN.stock.png = before, NN.authored.png = after)")
    print("Present before/after pairs to the user for the review checkpoint.")
    return 0 if ok else 1


def _lint(html: str) -> list[str]:
    issues = []
    if re.search(r"(linear|radial)-gradient", html):
        issues.append("CSS gradient (banned — solid fills only)")
    if re.search(r"<svg\b", html, re.I):
        issues.append("inline <svg> (use external .svg + prebuildSvg)")
    if re.search(r"background-image\s*:", html):
        issues.append("background-image (use <img>)")
    if _EMOJI_RE.search(html):
        issues.append("emoji glyph (banned — use line-icon SVG)")
    return issues


def cmd_validate(args) -> int:
    bp = _boilerplate_dir(args)
    _require_stock(bp)
    cls = ac.classify(bp)
    stems = cls["identity_flat"]

    # 1) html2pptx-safety lint on the live identity slides
    lint_fail = {}
    for stem in stems:
        f = bp / f"{stem}.html"
        if f.exists():
            issues = _lint(f.read_text(encoding="utf-8"))
            if issues:
                lint_fail[stem] = issues
    if lint_fail:
        print("[validate] lint FAILED:", file=sys.stderr)
        for stem, issues in lint_fail.items():
            print(f"  {stem}: {'; '.join(issues)}", file=sys.stderr)

    # 2) real build of a scratch deck containing the authored identity slides
    project = _scratch_project(args, stems, bp)
    build = subprocess.run(["node", "build.mjs"], cwd=str(project),
                           capture_output=True, text=True)
    build_ok = build.returncode == 0
    if not build_ok:
        sys.stderr.write(build.stdout[-3000:] + "\n" + build.stderr[-3000:])

    # 3) integrity check
    pptx = next(project.glob("*.pptx"), None)
    unzip_ok = False
    if pptx:
        uz = subprocess.run(["unzip", "-t", str(pptx)], capture_output=True, text=True)
        unzip_ok = uz.returncode == 0 and "No errors detected" in uz.stdout

    m = ac.load_manifest(bp) or ac.new_manifest(args.preset, bp)
    m["verification"]["lint"] = "ok" if not lint_fail else "failed"
    m["verification"]["build"] = "ok" if build_ok else "failed"
    m["verification"]["unzip"] = "ok" if unzip_ok else "failed"
    # "authored" = identity slides that actually differ from their .stock baseline
    stock = bp / ac.STOCK_DIRNAME
    authored = []
    for s in stems:
        live, base = bp / f"{s}.html", stock / f"{s}.html"
        if live.exists() and base.exists() and live.read_bytes() != base.read_bytes():
            authored.append(s)
    m["authored"] = authored
    ac.save_manifest(bp, m)

    ok = (not lint_fail) and build_ok and unzip_ok
    built_count = len(list((project / "slides").glob("*.html"))) if project.exists() else 0
    _cleanup_scratch(args)  # (E) don't leave scratch in output/
    print(f"\n[validate] lint={'ok' if not lint_fail else 'FAIL'} "
          f"build={'ok' if build_ok else 'FAIL'} unzip={'ok' if unzip_ok else 'FAIL'} "
          f"→ {'PASS' if ok else 'FAIL'}  ({built_count} identity slides, {len(authored)} authored)")
    return 0 if ok else 1


def cmd_confirm(args) -> int:
    bp = _boilerplate_dir(args)
    m = ac.load_manifest(bp)
    if m is None:
        print("[confirm] no manifest — run prep first", file=sys.stderr)
        return 2
    v = m.get("verification", {})
    if not (v.get("build") == "ok" and v.get("unzip") == "ok" and v.get("lint") == "ok"):
        print(f"[confirm] refused — validate must pass first (current: {v})", file=sys.stderr)
        return 1
    # (E) confirming with nothing authored means the identity slides are still stock.
    if not m.get("authored") and not args.allow_empty:
        print("[confirm] refused — no identity slides were authored (all still match .stock).\n"
              "  Author at least one identity slide, or pass --allow-empty to confirm token-tone as-is.",
              file=sys.stderr)
        return 1
    # §5/§6 must be filled — slide-plan consumes this visual vocabulary, so a
    # skeleton DESIGN.md (template placeholders intact) must not confirm.
    placeholders = _design_placeholders(args)
    if placeholders:
        preview = "\n".join(f"    · {p}" for p in placeholders[:6])
        more = f"\n    … (+{len(placeholders) - 6} more)" if len(placeholders) > 6 else ""
        msg = (f"[confirm] DESIGN.md §5/§6 still contain {len(placeholders)} template "
               f"placeholder line(s) — slide-plan would inherit an empty vocabulary:\n"
               f"{preview}{more}\n"
               f"  Fill §5 (어휘 표) + §6 (chrome) in {_preset_dir(args) / 'DESIGN.md'}.")
        if args.strict:
            print(msg + "\n[confirm] blocked (strict gate is default — pass --no-strict to "
                  "confirm with placeholders still present).", file=sys.stderr)
            return 1
        print("⚠ " + msg + "\n  (continuing — --no-strict given)\n", file=sys.stderr)
    m["status"] = "confirmed"
    ac.save_manifest(bp, m)

    # stamp DESIGN.md provenance
    design = _preset_dir(args) / "DESIGN.md"
    if design.exists():
        text = design.read_text(encoding="utf-8")
        stamp = (f"- Phase 2 layout-authoring: identity slides recomposed "
                 f"({', '.join(m.get('authored', []))}) — status confirmed {m['updated_at']}")
        if "Phase 2 layout-authoring" not in text:
            text = text.rstrip() + "\n" + stamp + "\n"
            design.write_text(text, encoding="utf-8")
    print(f"[confirm] status → confirmed · authored {len(m.get('authored', []))} identity slides")
    return 0


def cmd_restore(args) -> int:
    bp = _boilerplate_dir(args)
    _require_stock(bp)
    if args.stems:
        stems = [s.strip() for s in args.stems.split(",") if s.strip()]
    else:
        stems = ac.classify(bp)["identity_flat"]
    restored = ac.restore_from_stock(bp, stems)
    m = ac.load_manifest(bp)
    if m is not None:
        m["status"] = "not_authored"
        m["authored"] = [s for s in m.get("authored", []) if s not in restored]
        ac.save_manifest(bp, m)
    print(f"[restore] restored {len(restored)} slides from .stock: {', '.join(restored)}")
    return 0


def cmd_status(args) -> int:
    bp = _boilerplate_dir(args)
    m = ac.load_manifest(bp)
    if m is None:
        print("no manifest (preset not initialized for authoring)")
        return 0
    print(f"preset:   {m['preset']}")
    print(f"status:   {m['status']}")
    print(f"updated:  {m['updated_at']}")
    print(f"authored: {', '.join(m.get('authored', [])) or '(none)'}")
    print(f"verify:   {m.get('verification')}")
    print(f"sources:  {m.get('source_artifacts')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("prep", "classify", "thumbs", "validate", "confirm", "restore", "status"):
        sp = sub.add_parser(name)
        sp.add_argument("--preset", required=True)
        sp.add_argument("--presets-root", type=Path, default=DEFAULT_PRESETS_ROOT)
        if name == "prep":
            sp.add_argument("--design-md", type=Path, default=None)
            sp.add_argument("--original-design-md", type=Path, default=None)
            sp.add_argument("--reference", type=Path, default=None,
                            help="Hand-made brand deck used as the layout blueprint")
            sp.add_argument("--direction", type=str, default=None)
            sp.add_argument("--require-confirmed", action="store_true",
                            help="Block unless DESIGN.md frontmatter status is confirmed")
        if name == "confirm":
            sp.add_argument("--allow-empty", action="store_true",
                            help="Confirm even if no identity slides were authored (token-tone as-is)")
            sp.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True,
                            help="Block confirm if DESIGN.md §5/§6 still contain template "
                                 "placeholders (default: on). Use --no-strict to only warn.")
        if name == "restore":
            sp.add_argument("--stems", type=str, default=None,
                            help="Comma-separated stems; default = all identity slides")
    args = ap.parse_args()
    return {
        "prep": cmd_prep, "classify": cmd_classify, "thumbs": cmd_thumbs,
        "validate": cmd_validate, "confirm": cmd_confirm,
        "restore": cmd_restore, "status": cmd_status,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
