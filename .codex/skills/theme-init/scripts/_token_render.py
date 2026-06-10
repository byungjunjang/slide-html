"""Shared placeholder renderer for theme-init template → reference files.

Placeholder grammar:
    {{TOKEN:<dotted.path>}}              — raw token value
    {{TOKEN:<dotted.path>|<filter>}}     — value run through a named filter
    {{SCALE:<base>:<dotted.path>}}       — base number × numeric factor token,
                                           trimmed to 2 decimals (unit stays in
                                           the template, e.g. "...}}pt"). A
                                           missing path defaults to factor 1.0
                                           so pre-scale themes render unchanged
    {{IF:<dotted.path>}}...{{/IF}}      — keep block iff path resolves to truthy
    {{IFEQ:<dotted.path>:<value>}}...{{/IFEQ}}
                                         — keep block iff str(path) == value
                                           (value-switch; e.g. surface.card_style)
    {{IFNEQ:<dotted.path>:<value>}}...{{/IFNEQ}}
                                         — keep block iff path resolves AND
                                           str(path) != value (complement of IFEQ;
                                           both drop when the path is missing)

Supported filters:
    rgb       — hex string  → "r, g, b" decimal tuple (for rgba() literals)
    bulleted  — list         → newline-joined markdown bullets
    csv       — list         → comma-joined inline enumeration (e.g. `"a", "b"`)
    optional  — any          → str(value) or "_(not provided)_" when value is null
    rem       — number (px)  → "Xrem" (px ÷ 16, normalized)

Called by render_anti_slop_theme.py and render_design_system.py.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_PLACEHOLDER_RE = re.compile(r"\{\{TOKEN:([a-zA-Z0-9_.\-]+)(?:\|([a-z]+))?\}\}")
_SCALE_RE = re.compile(r"\{\{SCALE:([0-9]+(?:\.[0-9]+)?):([a-zA-Z0-9_.\-]+)\}\}")
_BLOCK_RE = re.compile(r"\{\{IF:([a-zA-Z0-9_.\-]+)\}\}(.*?)\{\{/IF\}\}", re.DOTALL)
_IFEQ_RE = re.compile(
    r"\{\{IFEQ:([a-zA-Z0-9_.\-]+):([a-zA-Z0-9_.\-]+)\}\}(.*?)\{\{/IFEQ\}\}", re.DOTALL
)
_IFNEQ_RE = re.compile(
    r"\{\{IFNEQ:([a-zA-Z0-9_.\-]+):([a-zA-Z0-9_.\-]+)\}\}(.*?)\{\{/IFNEQ\}\}", re.DOTALL
)


def _lookup(theme: dict[str, Any], dotted: str) -> Any:
    cur: Any = theme
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(f"missing theme token: {dotted}")
        cur = cur[part]
    return cur


def _hex_to_rgb(hex_str: str) -> str:
    h = hex_str.lstrip("#")
    if len(h) not in (6, 8):
        raise ValueError(f"expected 6- or 8-digit hex, got {hex_str!r}")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r}, {g}, {b}"


def _format(value: Any, fmt: str | None) -> str:
    if fmt is None:
        return str(value)
    if fmt == "optional":
        if value is None:
            return "_(not provided)_"
        return str(value)
    if fmt == "rgb":
        if not isinstance(value, str):
            raise ValueError(f"|rgb expects hex string, got {type(value).__name__}")
        return _hex_to_rgb(value)
    if fmt == "bulleted":
        if not isinstance(value, list):
            raise ValueError(f"|bulleted expects array, got {type(value).__name__}")
        if not value:
            return "- _(none specified)_"
        return "\n".join(f"- {item}" for item in value)
    if fmt == "csv":
        if not isinstance(value, list):
            raise ValueError(f"|csv expects array, got {type(value).__name__}")
        if not value:
            return "_(none)_"
        return ", ".join(f'"{item}"' for item in value)
    if fmt == "rem":
        if not isinstance(value, (int, float)):
            raise ValueError(f"|rem expects number, got {type(value).__name__}")
        rem = value / 16
        s = f"{rem:.4f}".rstrip("0").rstrip(".")
        return f"{s}rem"
    raise ValueError(f"unknown format filter: {fmt}")


def _render_blocks(tpl_text: str, theme: dict[str, Any]) -> str:
    """Resolve {{IFEQ}} value-switches and {{IF}} truthy blocks before token sub.

    {{IFEQ:path:value}}: body kept iff str(lookup(path)) == value (exact match);
        a missing path resolves to "not equal" → removed (mirrors {{IF}}).
    {{IF:path}}: body kept iff path resolves to a truthy value; removed if the
        path is missing or resolves to None / "" / [] / {}.

    Inner {{TOKEN}} placeholders inside a surviving block are left untouched here
    and resolved by the subsequent token-substitution pass in render().
    """
    def _sub_ifeq(match: re.Match[str]) -> str:
        path, expected, body = match.group(1), match.group(2), match.group(3)
        try:
            actual = _lookup(theme, path)
        except KeyError:
            return ""
        return body if str(actual) == expected else ""

    def _sub_ifneq(match: re.Match[str]) -> str:
        path, expected, body = match.group(1), match.group(2), match.group(3)
        try:
            actual = _lookup(theme, path)
        except KeyError:
            return ""
        return body if str(actual) != expected else ""

    tpl_text = _IFEQ_RE.sub(_sub_ifeq, tpl_text)
    tpl_text = _IFNEQ_RE.sub(_sub_ifneq, tpl_text)

    def _sub(match: re.Match[str]) -> str:
        path, body = match.group(1), match.group(2)
        try:
            value = _lookup(theme, path)
        except KeyError:
            return ""
        if value in (None, "", [], {}):
            return ""
        return body

    return _BLOCK_RE.sub(_sub, tpl_text)


def _format_scaled(base: float, factor: Any) -> str:
    if not isinstance(factor, (int, float)) or isinstance(factor, bool):
        raise ValueError(f"SCALE expects numeric factor token, got {type(factor).__name__}")
    s = f"{round(base * factor, 2):.2f}".rstrip("0").rstrip(".")
    return s


def render(tpl_text: str, theme: dict[str, Any]) -> str:
    tpl_text = _render_blocks(tpl_text, theme)

    def _sub_scale(match: re.Match[str]) -> str:
        base, dotted = float(match.group(1)), match.group(2)
        try:
            factor = _lookup(theme, dotted)
        except KeyError:
            factor = 1.0  # pre-scale themes (no typography.scale) render unchanged
        return _format_scaled(base, factor)

    tpl_text = _SCALE_RE.sub(_sub_scale, tpl_text)

    def _sub(match: re.Match[str]) -> str:
        dotted, fmt = match.group(1), match.group(2)
        value = _lookup(theme, dotted)
        return _format(value, fmt)

    return _PLACEHOLDER_RE.sub(_sub, tpl_text)


def load_theme(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
