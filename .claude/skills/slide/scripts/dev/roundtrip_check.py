#!/usr/bin/env python3
"""roundtrip_check.py — PPTX conversion-fidelity regression smoke.

Renders the BUILT .pptx back to PNG (LibreOffice headless → PDF → pdftoppm)
and compares each page against the Chromium screenshots the build dumped to
<deck>/_screenshots/. Catches the class of bug where the HTML preview looks
fine but the PPTX ships broken (image stretch, lost letter-spacing, shifted
boxes) — exactly the failures html-side validation can never see.

Scoring: grayscale-downscale both sides to a common raster and compute
similarity = 1 - mean(|a-b|)/255. Chromium and LibreOffice rasterize fonts
differently, so scores never reach 1.0 — the default threshold (0.90) is a
*regression tripwire*, not a pixel-perfection gate. Calibrate per repo with
known-good decks; a sudden per-slide drop is the signal.

Usage:
    python3 roundtrip_check.py <project-dir> [--threshold 0.90] [--strict]

Requires: soffice (LibreOffice), pdftoppm (poppler), Pillow.
Exit 0 = pass / tools missing (skipped). Exit 1 = --strict and >=1 slide
below threshold. Exit 2 = usage / structural mismatch.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CMP_W, CMP_H = 480, 270  # downscale target — coarse enough to forgive AA noise


def tool(name: str, extra: list[str] | None = None) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for p in extra or []:
        if Path(p).exists():
            return p
    return None


def similarity(img_a: Path, img_b: Path) -> float:
    from PIL import Image
    a = Image.open(img_a).convert("L").resize((CMP_W, CMP_H))
    b = Image.open(img_b).convert("L").resize((CMP_W, CMP_H))
    pa, pb = a.tobytes(), b.tobytes()
    diff = sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)
    return 1.0 - diff / 255.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", type=Path, help="output/<slug>-pptx deck dir")
    ap.add_argument("--threshold", type=float, default=0.90)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when any slide scores below threshold")
    args = ap.parse_args()

    project = args.project.resolve()
    slug = project.name[:-5] if project.name.endswith("-pptx") else project.name
    pptx = project / f"{slug}.pptx"
    shots_dir = project / "_screenshots"

    if not pptx.exists():
        sys.stderr.write(f"no built pptx: {pptx}\n")
        return 2
    shots = sorted(shots_dir.glob("*.png"))
    if not shots:
        sys.stderr.write(f"no screenshots in {shots_dir} — build with the current "
                         f"export_deck_pptx.mjs (dumps _screenshots/ by default)\n")
        return 2

    soffice = tool("soffice", ["/Applications/LibreOffice.app/Contents/MacOS/soffice"])
    pdftoppm = tool("pdftoppm")
    try:
        import PIL  # noqa: F401
    except ImportError:
        soffice = None
    if not soffice or not pdftoppm:
        print("[skip] roundtrip_check: soffice/pdftoppm/Pillow not all available — "
              "install LibreOffice + poppler + Pillow to enable.")
        return 0

    with tempfile.TemporaryDirectory(prefix="roundtrip-") as tmp:
        tmpdir = Path(tmp)
        r = subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", str(pptx), "--outdir", str(tmpdir)],
            capture_output=True, text=True, timeout=300)
        pdf = tmpdir / f"{slug}.pdf"
        if r.returncode != 0 or not pdf.exists():
            sys.stderr.write(f"soffice convert failed:\n{r.stderr}\n")
            return 2
        subprocess.run([pdftoppm, "-png", "-r", "96", str(pdf), str(tmpdir / "page")],
                       check=True, timeout=300)
        pages = sorted(tmpdir.glob("page-*.png"))

        if len(pages) != len(shots):
            sys.stderr.write(f"page count mismatch: PPTX renders {len(pages)} page(s) "
                             f"vs {len(shots)} screenshot(s)\n")
            return 2

        fails = []
        for shot, page in zip(shots, pages):
            score = similarity(shot, page)
            mark = "ok " if score >= args.threshold else "LOW"
            print(f"  [{mark}] {shot.name:<28} similarity {score:.3f}")
            if score < args.threshold:
                fails.append((shot.name, score))

    if fails:
        print(f"[{'x' if args.strict else '!'}] roundtrip_check: {len(fails)}/{len(shots)} "
              f"slide(s) below {args.threshold:.2f} — HTML 프리뷰와 PPTX 렌더가 다르게 "
              f"나오는 변환 회귀 가능성. 해당 슬라이드를 PowerPoint로 열어 확인.")
        return 1 if args.strict else 0
    print(f"[ok] roundtrip_check: {len(shots)} slide(s) all >= {args.threshold:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
