"""Shared constants + helpers for theme-init Phase 2 (Layout Authoring).

Phase 1 (init_theme.py) deterministically token-renders all 37 boilerplate
slides. Phase 2 lets an agent RECOMPOSE the *identity* slides into brand
layouts, leaving the *data* slides on their token-rendered tone.

This module is the single source of truth for:
  - which boilerplate files are identity (authored) vs data (token-tone),
  - the `.stock/` baseline snapshot (token-render output, recoverable),
  - the `_authoring.json` manifest (classification + blueprint + status).

Phase 2 is idempotent: it always recomposes from `.stock/`, never on top of
an already-authored file. Re-running init_theme.py --force refreshes `.stock/`.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

# Identity families that Phase 2 may recompose into brand layouts.
# Stems are boilerplate basenames without the .html suffix. A file is only
# authored if it actually exists in the preset's pptx-boilerplate/.
IDENTITY_FAMILIES: dict[str, list[str]] = {
    "cover":         ["01-title", "23-cover-with-character", "25-cover-vertical"],
    "section":       ["09-section", "07-quote-section"],
    "closing":       ["21-closing-light", "22-closing-big", "08-closing-dark"],
    "feature-board": ["02-overview", "26-overview-split", "12-four-point"],
    "hero-impact":   ["16-stats", "18-quote-attribution"],
    "summary":       ["17-summary"],
    "agenda":        ["10-agenda"],
}

STOCK_DIRNAME = ".stock"
MANIFEST_NAME = "_authoring.json"
PREVIEW_DIRNAME = "_preview"
MANIFEST_VERSION = "1.0"

# flat list of all identity stems (order-preserving)
IDENTITY_STEMS: list[str] = [s for fam in IDENTITY_FAMILIES.values() for s in fam]


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def existing_html(boilerplate_dir: Path) -> list[str]:
    """All NN-name.html stems present in the boilerplate dir (non-recursive)."""
    return sorted(p.stem for p in boilerplate_dir.glob("*.html"))


def boilerplate_digest(boilerplate_dir: Path) -> str:
    """sha256 over the live boilerplate *.html (the final deck).

    Drift guard for the Phase 2 review gate: the digest is stamped at approval
    time and re-checked at confirm, so any edit to a slide after approval
    invalidates it. Non-recursive glob → `.stock/` and `_preview/` are ignored.
    """
    h = hashlib.sha256()
    for stem in existing_html(boilerplate_dir):
        h.update(stem.encode("utf-8"))
        h.update(b"\0")
        h.update((boilerplate_dir / f"{stem}.html").read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def classify(boilerplate_dir: Path) -> dict[str, Any]:
    """Split existing boilerplate into identity (by family) vs data."""
    present = set(existing_html(boilerplate_dir))
    identity_set: dict[str, list[str]] = {}
    identity_flat: list[str] = []
    for fam, stems in IDENTITY_FAMILIES.items():
        hit = [s for s in stems if s in present]
        if hit:
            identity_set[fam] = hit
            identity_flat.extend(hit)
    data_set = sorted(present - set(identity_flat))
    return {
        "identity_set": identity_set,
        "identity_flat": identity_flat,
        "data_set": data_set,
    }


# ----------------------------------------------------------------------------
# .stock snapshot (token-render baseline)
# ----------------------------------------------------------------------------

def snapshot_stock(boilerplate_dir: Path, force: bool = False) -> Path:
    """Copy the token-rendered *.html into pptx-boilerplate/.stock/.

    Called by init_theme.py right after boilerplate render so the deterministic
    baseline is always recoverable. force=True overwrites an existing snapshot.
    """
    stock = boilerplate_dir / STOCK_DIRNAME
    if stock.exists():
        if not force:
            return stock
        shutil.rmtree(stock)
    stock.mkdir(parents=True, exist_ok=True)
    for html in boilerplate_dir.glob("*.html"):
        shutil.copy2(html, stock / html.name)
    return stock


def restore_from_stock(boilerplate_dir: Path, stems: list[str]) -> list[str]:
    """Copy named stems back from .stock/ into the live boilerplate dir.

    Returns the stems actually restored. Missing .stock files are skipped.
    """
    stock = boilerplate_dir / STOCK_DIRNAME
    restored: list[str] = []
    for stem in stems:
        src = stock / f"{stem}.html"
        if src.exists():
            shutil.copy2(src, boilerplate_dir / f"{stem}.html")
            restored.append(stem)
    return restored


# ----------------------------------------------------------------------------
# manifest
# ----------------------------------------------------------------------------

def manifest_path(boilerplate_dir: Path) -> Path:
    return boilerplate_dir / MANIFEST_NAME


def new_manifest(preset: str, boilerplate_dir: Path) -> dict[str, Any]:
    cls = classify(boilerplate_dir)
    return {
        "version": MANIFEST_VERSION,
        "preset": preset,
        "status": "not_authored",          # not_authored | draft | confirmed
        "updated_at": _now(),
        "identity_set": cls["identity_set"],
        "data_set": cls["data_set"],
        "authored": [],                      # stems actually recomposed
        "blueprint": {                       # agent-filled during prep/compose
            "signature_elements": [],        # e.g. "navy hero band", "spectrum dots"
            "per_family": {},                # family -> one-line recipe
            "helper_hex_map": {},            # helper/literal-hex used per brand element
            "chrome_treatment": "",
        },
        "source_artifacts": {
            "design_md": None,
            "original_design_md": None,
            "reference_blueprint": None,
            "user_direction": None,
        },
        "verification": {"lint": None, "build": None, "unzip": None, "review": None},
        "review": {                          # Phase 2 final-boilerplate approval gate
            "approved": False,               # set true only by `review --approve`
            "approved_at": None,
            "approved_digest": None,         # boilerplate digest at approval time
            "digest": None,                  # boilerplate digest at last `review`
            "preview_path": None,            # _preview/index.html (contact sheet)
        },
    }


def load_manifest(boilerplate_dir: Path) -> dict[str, Any] | None:
    p = manifest_path(boilerplate_dir)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save_manifest(boilerplate_dir: Path, manifest: dict[str, Any]) -> Path:
    manifest["updated_at"] = _now()
    p = manifest_path(boilerplate_dir)
    p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def ensure_manifest(preset: str, boilerplate_dir: Path) -> dict[str, Any]:
    """Load the manifest, or create+save a fresh stub if absent."""
    m = load_manifest(boilerplate_dir)
    if m is None:
        m = new_manifest(preset, boilerplate_dir)
        save_manifest(boilerplate_dir, m)
    return m
