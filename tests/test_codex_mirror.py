import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / ".claude/skills/slide/scripts/dev/sync_codex_mirror.py"


def test_generate_then_check_is_clean():
    # Regenerate the real mirror, then --check must report in-sync (exit 0).
    gen = subprocess.run([sys.executable, str(SYNC)], capture_output=True, text=True)
    assert gen.returncode == 0, gen.stderr
    chk = subprocess.run([sys.executable, str(SYNC), "--check"], capture_output=True, text=True)
    assert chk.returncode == 0, chk.stderr


def test_check_detects_drift():
    # Corrupt one mirror file -> --check must fail (exit 1), then restore.
    target = ROOT / ".codex/skills/slide/SKILL.md"
    original = target.read_bytes()
    try:
        target.write_bytes(original + b"\n<!-- drift -->\n")
        chk = subprocess.run([sys.executable, str(SYNC), "--check"], capture_output=True, text=True)
        assert chk.returncode == 1
        assert "STALE" in chk.stderr
    finally:
        r = subprocess.run([sys.executable, str(SYNC)], capture_output=True, text=True)
        assert r.returncode == 0, f"Cleanup regeneration failed:\n{r.stderr}"


def test_agents_md_codex_paths_exist():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    refs = sorted(set(re.findall(r"\.codex/skills/[^\s`)\"']+", text)))
    assert refs, "AGENTS.md should reference .codex/skills/... paths"
    for rel in refs:
        assert (ROOT / rel).exists(), f"AGENTS.md points at missing path: {rel}"


def test_verify_deck_runnable_from_codex_depth():
    codex_verify = ROOT / ".codex/skills/slide/scripts/verify_deck.py"
    assert codex_verify.exists()
    # No args -> usage, exit 2 (proves the mirrored copy imports/runs at .codex depth).
    r = subprocess.run([sys.executable, str(codex_verify)], capture_output=True, text=True)
    assert r.returncode == 2
    assert "usage" in (r.stdout + r.stderr).lower()


def test_mirror_keeps_path_constants_self_correct():
    # The mirrored sync script must still target SRC=.claude, DST=.codex and keep
    # OLD/NEW un-joined (the separate-component trick) so running the .codex copy
    # produces a correct mirror rather than a no-op. Regression guard for the
    # Task 1 critical fix.
    codex_sync = ROOT / ".codex/skills/slide/scripts/dev/sync_codex_mirror.py"
    body = codex_sync.read_text(encoding="utf-8")
    assert '".claude" / "skills"' in body
    assert '".codex" / "skills"' in body
    assert 'OLD = _CLAUDE + "/skills"' in body
    assert 'NEW = _CODEX + "/skills"' in body
    assert '_CLAUDE = ".claude"' in body
    assert '_CODEX = ".codex"' in body


def test_codex_side_sync_check_passes():
    # Regression for the GENERATED_MARKER self-rewrite bug: running --check from
    # the MIRRORED (.codex) copy must ALSO report in-sync (exit 0), not a phantom
    # STALE on _GENERATED.md. This is the exact path verify_deck/preflight invoke
    # on the Codex host, so a false STALE here breaks every Codex-side gate.
    codex_sync = ROOT / ".codex/skills/slide/scripts/dev/sync_codex_mirror.py"
    r = subprocess.run([sys.executable, str(codex_sync), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
