import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / ".claude/skills/slide/scripts/verify_deck.py"


def _make_pptx(path: Path, slides_xml, media=None):
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("[Content_Types].xml", b"<Types/>")
        zf.writestr("ppt/_pad.bin", b"\x00" * 60000)  # exceed MIN_PPTX_BYTES sanity floor
        for i, xml in enumerate(slides_xml, 1):
            zf.writestr(f"ppt/slides/slide{i}.xml", xml)
        for name, blob in (media or {}).items():
            zf.writestr(f"ppt/media/{name}", blob)


def _deck(tmp_path, n_slides, slide_html=None, with_plan=False, plan_n=None):
    proj = tmp_path / "demo-pptx"
    (proj / "slides").mkdir(parents=True)
    for i in range(1, n_slides + 1):
        html = slide_html or "<html><body><p>content</p></body></html>"
        (proj / "slides" / f"{i:02d}-x.html").write_text(html, encoding="utf-8")
    if with_plan:
        import json
        slides = [{"slide_number": i} for i in range(1, (plan_n or n_slides) + 1)]
        (proj / "slide_plan.json").write_text(json.dumps({"slides": slides}), encoding="utf-8")
    return proj


def _run(proj, *extra):
    return subprocess.run([sys.executable, str(VERIFY), str(proj), *extra],
                          capture_output=True, text=True)


def test_passes_on_native_deck(tmp_path):
    proj = _deck(tmp_path, 3)
    runs = b"<a:t>hello</a:t>" * 10
    _make_pptx(proj / "demo.pptx", [b"<p:sld>" + runs + b"</p:sld>"] * 3)
    r = _run(proj)
    assert r.returncode == 0, r.stdout + r.stderr


def test_fails_on_image_flattened_deck(tmp_path):
    proj = _deck(tmp_path, 2)
    _make_pptx(proj / "demo.pptx", [b"<p:sld><pic/></p:sld>", b"<p:sld><pic/></p:sld>"])
    r = _run(proj)
    assert r.returncode == 1
    assert "flattened" in (r.stdout + r.stderr).lower()


def test_fails_on_dangling_image_ref(tmp_path):
    proj = _deck(tmp_path, 1, slide_html='<body><img src="../images/missing.png"><p>x</p></body>')
    _make_pptx(proj / "demo.pptx", [b"<a:t>x</a:t>"])
    r = _run(proj)
    assert r.returncode == 1
    assert "dangling" in (r.stdout + r.stderr).lower()


def test_fails_on_large_deck_without_plan(tmp_path):
    proj = _deck(tmp_path, 11)
    _make_pptx(proj / "demo.pptx", [b"<a:t>x</a:t>"] * 11)
    r = _run(proj)
    assert r.returncode == 1
    assert "plan" in (r.stdout + r.stderr).lower()


def test_large_deck_with_simple_marker_passes(tmp_path):
    proj = _deck(tmp_path, 11)
    (proj / ".deck-mode").write_text("simple", encoding="utf-8")
    _make_pptx(proj / "demo.pptx", [b"<a:t>x</a:t>" * 8] * 11)
    r = _run(proj)
    assert r.returncode == 0, r.stdout + r.stderr


def test_strict_promotes_warn_to_fail(tmp_path):
    proj = _deck(tmp_path, 1)
    # 1 <a:t> run -> passes nativeness but is below MIN_RUNS_PER_SLIDE (6) -> WARN
    _make_pptx(proj / "demo.pptx", [b"<p:sld><a:t>x</a:t></p:sld>"])
    assert _run(proj).returncode == 0            # WARN is not HARD
    assert _run(proj, "--strict").returncode == 1  # promoted to HARD


def test_media_floor_fails_when_slot_declared_but_no_media(tmp_path):
    proj = _deck(tmp_path, 1, slide_html='<body data-image-slot="hero"><p>x</p></body>')
    _make_pptx(proj / "demo.pptx", [b"<a:t>x</a:t>"])  # no ppt/media entries
    r = _run(proj)
    assert r.returncode == 1
    assert "media" in (r.stdout + r.stderr).lower()


def test_usage_exits_2():
    r = subprocess.run([sys.executable, str(VERIFY)], capture_output=True, text=True)
    assert r.returncode == 2
    assert "usage" in (r.stdout + r.stderr).lower()
