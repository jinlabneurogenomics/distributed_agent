"""Canonical visual scheme for literature-agreement flags.

Single source of truth for the four `agree` / `disagree` / `inferred` /
`no_literature` levels so every figure in the repo renders them identically.
Adopted from the gold-set scheme in
`manuscript/fig2/_debug/260731/literature_flag_gold_set` (which took it from
`manuscript/fig2/_debug/260730/updated_shuffles/strict_v4_regrade_15`), which is
the scheme the manuscript figures already use.

Usage — either a normal import (when ``src`` is on ``PYTHONPATH``)::

    from manuscript_figures.flag_style import FLAG_COLORS, FLAG_ORDER, normalize_flag

or, for standalone analysis scripts that must run from any cwd, load by path the
way `gold_set.py` loads its helpers::

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "flag_style", REPO / "src" / "manuscript_figures" / "flag_style.py")
    flag_style = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flag_style)

Design of the scheme: it is an **emphasis** scheme, not a flat categorical one.
`agree` and `disagree` carry the strongest hues, `inferred` uses a pale green,
and `no_literature` recedes into a neutral gray. So "how much of this chart is
actually grounded" reads at a glance.

Accessibility, measured with `dataviz/scripts/validate_palette.js`
(light, surface #fcfcfb, --pairs all):

* The default pair `agree #6fc46f` vs `disagree #ec835a` is **ΔE 3.1 under
  deuteranopia** — below the 6 floor. Green vs orange sits on the red-green
  confusion axis, so the two most consequential levels are near-indistinguishable
  for deutan readers. `FLAG_COLORS_CVD` fixes this with a single hex change
  (`disagree` -> `#d03b3b`, the status-critical token), giving deutan ΔE 15.9 /
  tritan 36.0 for that pair. Prefer `FLAG_COLORS_CVD` for any figure where
  `disagree` is actually populated. The pale-green `inferred` level is separated
  from `agree` primarily by lightness, so legends or direct labels remain
  required.
* `agree #6fc46f` vs `no_literature #c3c2b7` is normal-vision ΔE 14.9, just under
  the 15 floor, in both variants.
* `agree`, `disagree`, `inferred` and `no_literature` are light fills rather than
  text colors, so the **relief rule** applies: ship a visible legend, direct
  labels, or a table view.

Derived measures are NOT flags. A series like "grounded rows" (agree + inferred)
or a token/step count is an analytic quantity, so give it an analytic color
(`DERIVED_PRIMARY` / `DERIVED_SECONDARY`) rather than borrowing a flag hue.
"""

from __future__ import annotations

import re

__all__ = [
    "FLAG_ORDER",
    "FLAG_LABELS",
    "FLAG_COLORS",
    "FLAG_COLORS_CVD",
    "UNFLAGGED_KEY",
    "UNFLAGGED_COLOR",
    "LEGACY_SIX_FLAG_MAP",
    "collapse_legacy_six",
    "NEUTRAL_ABSENT",
    "DERIVED_PRIMARY",
    "DERIVED_SECONDARY",
    "SUPPORTED_FLAGS",
    "normalize_flag",
    "flag_color",
    "flag_label",
    "flag_colors",
    "legend_handles",
    "flag_cmap",
]

#: Canonical key order, weakest judgement last.
FLAG_ORDER: tuple[str, ...] = ("agree", "disagree", "inferred", "no_literature")

#: Display labels.
FLAG_LABELS: dict[str, str] = {
    "agree": "Agree",
    "disagree": "Disagree",
    "inferred": "Inferred",
    "no_literature": "No Literature",
}

#: The scheme as used by the manuscript figures.
FLAG_COLORS: dict[str, str] = {
    "agree": "#6fc46f",
    "disagree": "#ec835a",
    "inferred": "#c7e1a3",
    "no_literature": "#c3c2b7",
}

#: One-hex CVD repair of the agree/disagree collision. See module docstring.
FLAG_COLORS_CVD: dict[str, str] = {**FLAG_COLORS, "disagree": "#d03b3b"}

#: Optional 5th level used only by the blind-arm comparison, where a finding can
#: carry no flag at all. Kept out of FLAG_ORDER so the default four-level scheme
#: stays unchanged. A chart using it with the pale inferred fill needs direct
#: labels or a visible legend.
UNFLAGGED_KEY = "unflagged"
UNFLAGGED_COLOR = "#86a7bd"

#: The pre-2026-07 six-level vocabulary, mapped onto the four canonical levels.
#: LOSSY -- it collapses the moderate levels into their strong counterparts, so
#: it is exported explicitly and never applied by `normalize_flag`. Callers that
#: want the collapse must opt in, and should say so in the figure caption.
LEGACY_SIX_FLAG_MAP: dict[str, str] = {
    "agree": "agree",
    "moderately_agree": "agree",
    "moderately_disagree": "disagree",
    "disagree": "disagree",
    "unknown_ambiguous": "inferred",
    "unknown_no_literature": "no_literature",
}

#: Fill for "this cell has no value at all" (not a flag; e.g. target unassigned).
NEUTRAL_ABSENT = "#f4f3ef"

#: Colors for derived analytic series, deliberately outside the flag hues.
DERIVED_PRIMARY = "#256abf"
DERIVED_SECONDARY = "#86b6ef"

#: Flags that count as literature-grounded.
SUPPORTED_FLAGS: frozenset[str] = frozenset({"agree", "inferred", "disagree"})

# Spellings seen across the repo's datasets and scripts.
_ALIASES: dict[str, str] = {
    "agree": "agree",
    "agrees": "agree",
    "disagree": "disagree",
    "disagrees": "disagree",
    "inferred": "inferred",
    "infer": "inferred",
    "ambiguous": "inferred",  # the pre-rename predecessor of `inferred`
    "no_literature": "no_literature",
    "noliterature": "no_literature",
    "no_lit": "no_literature",
    "nolit": "no_literature",
    "none": "no_literature",
    "no_literature_found": "no_literature",
}


def normalize_flag(value: object) -> str:
    """Map any casing/punctuation variant to a canonical key.

    Handles the two conventions in the repo -- title case with a space
    ("No Literature", from the agent JSONL) and lowercase snake
    ("no_literature", from the gold set) -- plus the legacy `ambiguous` label.

    Raises ValueError on an unrecognised flag rather than silently mis-coloring.
    """
    key = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    if key in _ALIASES:
        return _ALIASES[key]
    collapsed = key.replace("_", "")
    if collapsed in _ALIASES:
        return _ALIASES[collapsed]
    raise ValueError(
        f"unrecognised literature flag {value!r} "
        f"(canonical keys: {', '.join(FLAG_ORDER)})"
    )


def collapse_legacy_six(value: object) -> str:
    """Opt-in, lossy collapse of the old six-level vocabulary onto the four.

    "Moderately-agree" -> `agree`, "Unknown-ambiguous" -> `inferred`, etc. Use
    this only when you intend the collapse and note it in the caption; prefer
    `normalize_flag` (which raises on the legacy labels) everywhere else.
    """
    key = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    if key in LEGACY_SIX_FLAG_MAP:
        return LEGACY_SIX_FLAG_MAP[key]
    return normalize_flag(value)


def flag_colors(*, cvd_safe: bool = False) -> dict[str, str]:
    """The active color mapping."""
    return dict(FLAG_COLORS_CVD if cvd_safe else FLAG_COLORS)


def flag_color(value: object, *, cvd_safe: bool = False) -> str:
    """Color for one flag, accepting any spelling variant."""
    return flag_colors(cvd_safe=cvd_safe)[normalize_flag(value)]


def flag_label(value: object) -> str:
    """Display label for one flag, accepting any spelling variant."""
    return FLAG_LABELS[normalize_flag(value)]


def legend_handles(
    flags: object = None,
    *,
    cvd_safe: bool = False,
    labels: dict[str, str] | None = None,
    **patch_kwargs: object,
) -> list:
    """Matplotlib legend patches in canonical order.

    `labels` overrides individual display strings, e.g. to annotate a level that
    is never observed in the data.
    """
    from matplotlib.patches import Patch

    keys = FLAG_ORDER if flags is None else [normalize_flag(f) for f in flags]
    colors = flag_colors(cvd_safe=cvd_safe)
    text = {**FLAG_LABELS, **(labels or {})}
    return [
        Patch(facecolor=colors[k], label=text[k], **patch_kwargs) for k in keys
    ]


def flag_cmap(
    flags: object = None, *, cvd_safe: bool = False, absent: str = NEUTRAL_ABSENT
):
    """A ListedColormap + the integer code per flag, for heatmap/imshow views.

    Returns ``(cmap, codes, order)`` where ``codes[flag] -> int``. Use with
    ``vmin=-0.5, vmax=len(order)-0.5``; NaN renders as `absent`.
    """
    from matplotlib.colors import ListedColormap

    order = list(FLAG_ORDER if flags is None else [normalize_flag(f) for f in flags])
    colors = flag_colors(cvd_safe=cvd_safe)
    cmap = ListedColormap([colors[k] for k in order])
    cmap.set_bad(absent)
    return cmap, {k: i for i, k in enumerate(order)}, order
