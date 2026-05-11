#!/usr/bin/env python3
"""Orchestrate /theme-init: input draft → complete preset folder.

Steps:
    1. fill_theme_defaults     — partial draft → complete theme.json
    2. patch name + display_name from --preset arg
    3. validate_theme          — schema check vs token-contract v1
    4. ensure fonts-prelude    — use --fonts-prelude, or existing
                                 <preset>/_fonts.css, or generate a minimal
                                 header from theme identity
    5. render_colors_and_type  — colors_and_type.css (with prelude)
    6. render_pptx_helpers     — _pptx-slide.css
    7. render_brand_spec       — brand-spec-generated.md
    8. render_boilerplate      — pptx-boilerplate/*.html (8 slides)

Usage:
    python3 init_theme.py --from <draft.json> --preset <kebab-name>
    python3 init_theme.py --from <draft.json> --preset <kebab-name> --force
    python3 init_theme.py --from <draft.json> --preset <kebab-name> \\
        --presets-root <path>   # default: slide/assets/design-systems (the slide bundle)
    python3 init_theme.py --from <draft.json> --preset <kebab-name> \\
        --fonts-prelude <preset>/_fonts.css

Note on partial-failure cleanup: if the preset folder does not yet exist, it
is created up-front. If a later step fails the folder is left in a partial
state — re-run with `--force` (or `rm -rf` and retry) to recover.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
# Output target = slide skill bundle's design-systems folder.
# theme-init runs locally (Claude Code only) and patches the slide bundle
# directly so newly-built presets appear in /slide without manual moves.
DEFAULT_PRESETS_ROOT = SCRIPTS.parents[1] / "slide" / "assets" / "design-systems"

GENERATED_HEADER_FILENAME = "_header.css"  # auto-generated minimal header for new presets


def _run(label: str, argv: list[str]) -> None:
    print(f"\n=== {label} ===")
    r = subprocess.run(argv)
    if r.returncode != 0:
        print(f"\n[init_theme] step failed: {label} (exit {r.returncode})", file=sys.stderr)
        sys.exit(r.returncode)


def _ensure_header(out_dir: Path, theme: dict, fonts_prelude: Path | None) -> Path | None:
    """Resolve the colors_and_type.css prelude (header + optional @font-face).

    Resolution order:
        1. Explicit --fonts-prelude (returned as-is if exists)
        2. Existing <preset>/_fonts.css
        3. Generate <preset>/_header.css with a minimal identity comment
    """
    if fonts_prelude and fonts_prelude.exists():
        return fonts_prelude

    existing_fonts = out_dir / "_fonts.css"
    if existing_fonts.exists():
        return existing_fonts

    # Generate minimal header
    header_path = out_dir / GENERATED_HEADER_FILENAME
    display = theme.get("display_name", theme.get("name", "Untitled"))
    desc = theme.get("description", "")
    header = (
        "/* ============================================================\n"
        f"   {display} Slide Design System — Colors & Typography\n"
        f"   {desc}\n"
        "   ============================================================ */\n"
    )
    header_path.write_text(header, encoding="utf-8")
    return header_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--from", dest="src", type=Path, required=True,
                    help="Draft theme.json (partial OK — nulls get safe defaults)")
    ap.add_argument("--preset", required=True,
                    help="Preset name (lowercase-kebab, becomes folder name)")
    ap.add_argument("--presets-root", type=Path, default=DEFAULT_PRESETS_ROOT)
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing preset folder (preserves _fonts.css if present)")
    ap.add_argument("--fonts-prelude", type=Path, default=None,
                    help="Optional CSS file (typically @font-face) prepended to colors_and_type.css")
    args = ap.parse_args()

    out_dir = args.presets_root / args.preset
    if out_dir.exists() and not args.force:
        print(f"preset already exists: {out_dir} (use --force to overwrite)", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    theme_path = out_dir / "theme.json"

    # Step 1: fill
    _run("fill_theme_defaults",
         [sys.executable, str(SCRIPTS / "fill_theme_defaults.py"),
          "--input", str(args.src), "--out", str(theme_path)])

    # Step 2: patch name + display_name from --preset, ensure description
    theme = json.loads(theme_path.read_text(encoding="utf-8"))
    theme["name"] = args.preset
    if not theme.get("display_name"):
        theme["display_name"] = args.preset.replace("-", " ").title()
    # description is template-required (brand-spec.tpl.md, generated header) but
    # not in SAFE_DEFAULTS — guarantee a non-null value here so all downstream
    # renderers succeed even when the draft omitted it.
    if not theme.get("description"):
        theme["description"] = f"{theme['display_name']} design system."
    theme_path.write_text(
        json.dumps(theme, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Step 3: validate
    _run("validate_theme",
         [sys.executable, str(SCRIPTS / "validate_theme.py"),
          "--theme", str(theme_path),
          "--contract", str(SKILL / "references" / "token-contract.json")])

    # Step 4: resolve prelude
    prelude_path = _ensure_header(out_dir, theme, args.fonts_prelude)

    # Step 5: colors_and_type.css
    cct_argv = [sys.executable, str(SCRIPTS / "render_colors_and_type.py"),
                "--theme", str(theme_path),
                "--out", str(out_dir / "colors_and_type.css")]
    if prelude_path:
        cct_argv += ["--fonts-prelude", str(prelude_path)]
    _run("render_colors_and_type", cct_argv)

    # Step 6: _pptx-slide.css
    _run("render_pptx_helpers",
         [sys.executable, str(SCRIPTS / "render_pptx_helpers.py"),
          "--theme", str(theme_path),
          "--out", str(out_dir / "_pptx-slide.css")])

    # Step 7: brand-spec
    _run("render_brand_spec",
         [sys.executable, str(SCRIPTS / "render_brand_spec.py"),
          "--theme", str(theme_path),
          "--out", str(out_dir / "brand-spec-generated.md")])

    # Step 8: boilerplate
    _run("render_boilerplate_slides",
         [sys.executable, str(SCRIPTS / "render_boilerplate_slides.py"),
          "--theme", str(theme_path),
          "--out-dir", str(out_dir / "pptx-boilerplate")])

    # Step 9: DESIGN.md draft (Layer 3 of slide-plan introduction).
    # Generates a draft with token-substituted frontmatter/colors/icons.
    # Non-token sections are left as guidance text — user reviews and
    # fills them, then flips frontmatter status: draft → confirmed.
    _run("render_design_md",
         [sys.executable, str(SCRIPTS / "render_design_md.py"),
          "--theme", str(theme_path),
          "--out", str(out_dir / "DESIGN.md"),
          "--boilerplate-dir", str(out_dir / "pptx-boilerplate")])

    # Step 10: refresh the slide bundle's preset catalog (README.md in
    # presets_root). This lets /slide and humans see the new preset without
    # any manual move.
    _run("render_presets_readme",
         [sys.executable, str(SCRIPTS / "render_presets_readme.py"),
          "--presets-root", str(args.presets_root)])

    print(f"\n=== /theme-init complete ===")
    print(f"preset: {theme.get('display_name')} ({args.preset})")
    print(f"location: {out_dir}")
    print(f"DESIGN.md: {out_dir / 'DESIGN.md'} (status: draft — review before /slide-plan use)")
    print(f"next: bash .claude/skills/slide/scripts/init-project.sh <project> {args.preset}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
