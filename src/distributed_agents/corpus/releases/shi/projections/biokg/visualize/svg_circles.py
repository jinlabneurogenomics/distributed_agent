"""Rewrite Matplotlib's circular SVG markers as native ``<circle>`` elements.

This release-owned copy keeps BioKG figure rendering independent of the
manuscript repository's sibling ``figures`` package.
"""

from __future__ import annotations

import re
from pathlib import Path

__all__ = ["circleify", "count_marks"]

_DEF_PATTERN = re.compile(
    r'<path[^>]*\bid="(?P<id>[^"]+)"[^>]*\bd="(?P<d>[^"]*)"[^>]*/>', re.DOTALL
)
_USE_PATTERN = re.compile(r"<use\b[^>]*/>", re.DOTALL)
_ATTR_PATTERN = re.compile(r'(?P<name>[\w:-]+)="(?P<value>[^"]*)"')
_NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _circle_radius(d: str) -> float | None:
    """Return the radius for an origin-centered all-curve circle path."""

    letters = [c for c in re.findall(r"[MmLlHhVvCcSsQqTtAaZz]", d) if c not in "Zz"]
    if len(letters) < 5 or letters[0] not in "Mm":
        return None
    if any(c not in "Cc" for c in letters[1:]):
        return None

    values = [float(value) for value in _NUMBER_PATTERN.findall(d)]
    if len(values) < 2 or len(values) % 2:
        return None
    xs, ys = values[0::2], values[1::2]
    radius = max(max(abs(value) for value in xs), max(abs(value) for value in ys))
    if radius <= 0:
        return None
    if abs(max(abs(value) for value in xs) - radius) > 1e-6:
        return None
    if abs(max(abs(value) for value in ys) - radius) > 1e-6:
        return None
    return radius


def count_marks(path: str | Path) -> dict[str, int]:
    """Return an element census for one SVG file."""

    text = Path(path).read_text(encoding="utf-8")
    return {
        name: len(re.findall(pattern, text))
        for name, pattern in (
            ("circle", r"<circle\b"),
            ("path", r"<path\b"),
            ("use", r"<use\b"),
            ("image", r"<image\b"),
            ("clip-path", r"clip-path"),
        )
    }


def circleify(path: str | Path) -> int:
    """Rewrite circular ``<use>`` markers in ``path`` as ``<circle>`` in place."""

    path = Path(path)
    text = path.read_text(encoding="utf-8")
    radii = {
        match.group("id"): radius
        for match in _DEF_PATTERN.finditer(text)
        if (radius := _circle_radius(match.group("d"))) is not None
    }
    if not radii:
        return 0

    converted = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal converted
        attributes = {
            item.group("name"): item.group("value")
            for item in _ATTR_PATTERN.finditer(match.group(0))
        }
        href = attributes.get("xlink:href") or attributes.get("href", "")
        marker_id = href.lstrip("#")
        if marker_id not in radii or "transform" in attributes:
            return match.group(0)

        converted += 1
        parts = [
            f'cx="{attributes.get("x", "0")}"',
            f'cy="{attributes.get("y", "0")}"',
            f'r="{radii[marker_id]:.6g}"',
        ]
        for name in ("style", "class", "clip-path"):
            if name in attributes:
                parts.append(f'{name}="{attributes[name]}"')
        return f"<circle {' '.join(parts)}/>"

    text = _USE_PATTERN.sub(replace, text)
    for marker_id in radii:
        if f'href="#{marker_id}"' not in text:
            text = _DEF_PATTERN.sub(
                lambda match: "" if match.group("id") == marker_id else match.group(0),
                text,
            )

    path.write_text(text, encoding="utf-8")
    return converted
