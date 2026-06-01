#!/usr/bin/env python3
"""preflight.py - pre-pipeline environment gate for slide-html dual-host.

Verifies the build toolchain (and optionally the image backend) is available,
and that the .codex mirror is fresh, BEFORE a deck is authored/built.
Path-agnostic via __file__.

Usage:
    python3 preflight.py [--images]

--images : also check the codex image backend login (decks with image slots).
Exit 0 = ready. Exit 1 = at least one blocker (with a fix instruction).
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

SLIDE_SKILL_DIR = Path(__file__).resolve().parent.parent     # .../skills/slide
REPO_ROOT = SLIDE_SKILL_DIR.parents[2]                       # skills->.claude->root
SYNC_SCRIPT = SLIDE_SKILL_DIR / "scripts" / "dev" / "sync_codex_mirror.py"


def have_node_module(name: str) -> bool:
    for base in (REPO_ROOT / "node_modules", SLIDE_SKILL_DIR / "node_modules"):
        if (base / name).exists():
            return True
    return False


def main(argv: list) -> int:
    want_images = "--images" in argv
    fails: list = []

    if shutil.which("node") is None:
        fails.append("node not found on PATH")
    for mod in ("playwright", "pptxgenjs", "sharp"):
        if not have_node_module(mod):
            fails.append(f"Node dep '{mod}' missing - run: npm install (repo root)")

    if want_images:
        if shutil.which("codex") is None:
            fails.append("codex CLI missing - `npm install -g @openai/codex` "
                         "(or use <div class=\"img-placeholder\"> per SKILL section 2.5)")
        else:
            try:
                r = subprocess.run(["codex", "login", "status"],
                                   capture_output=True, text=True, timeout=30)
                if "Logged in" not in (r.stdout + r.stderr):
                    fails.append("codex not logged in - `codex login` "
                                 "(or use img-placeholder div per SKILL section 2.5)")
            except (subprocess.TimeoutExpired, OSError):
                fails.append("codex login check failed - verify codex CLI")

    if SYNC_SCRIPT.exists():
        try:
            r = subprocess.run([sys.executable, str(SYNC_SCRIPT), "--check"], timeout=60)
            if r.returncode != 0:
                fails.append("`.codex/skills` mirror stale - run sync_codex_mirror.py")
        except subprocess.TimeoutExpired:
            fails.append("sync_codex_mirror.py --check timed out (>60s)")

    if fails:
        sys.stderr.write("[x] preflight failed:\n")
        for f in fails:
            sys.stderr.write(f"    - {f}\n")
        return 1
    print("[ok] preflight passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
