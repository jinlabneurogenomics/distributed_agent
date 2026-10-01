#!/usr/bin/env python3
"""Render flags for high + moderate reader-facing phenotype findings.

The source is the 5,142-row reader view written by
``organize_phenotype_findings.py``.  This plot deliberately uses its simplified
``phenotype_confidence`` definition rather than the heterogeneous historical
model-confidence enums:

* high = canonical load-bearing union finding;
* moderate = July 13 evidence-only finding.

For each perturbation x cell-class block, the most decisive literature flag is
shown using the canonical Fig. 2 priority and palette: Disagree, Agree,
Inferred, No Literature, then Unassessed. As in the other Fig. 2 finding
heatmaps, only explicit placements with at least one local DEG at FDR < 0.1 are
plotted.

The matrix plotting box is square at the user's request, despite the 1,092 × 23
data shape. The ``__matrix`` output is the standalone panel; the unsuffixed
output is the square joint plate with DEG-burden and flag-mix marginals. Both
are generated from ``draw_matrix`` so their data and colors cannot drift. The
top and right marginals remain rectangular because they are aligned summaries
of the square matrix, not standalone panels.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from finalize_union import CELL_TYPES


HERE = Path(__file__).resolve().parent


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError(f"Could not locate repository root above {start}")


ROOT = find_repo_root(HERE)
FINDINGS = (
    ROOT
    / "results/bioeval/lit-agree-4flag"
    / "phenotype_findings_by_perturbation_deg_ordered.csv"
)
DEG_CSV = ROOT / "data/groupxtarget_deg.csv"
STYLE = ROOT / "src/figures/style.mplstyle"
FLAG_STYLE_PATH = ROOT / "src/figures/flag_style.py"
STEM = "fig2_high_moderate_confidence_heatmap"
PRESENTATION_STEM = f"{STEM}_presentation"
DENSITY_STEM = f"{STEM}_three_densities"
PRESENTATION_DENSITY_STEM = f"{DENSITY_STEM}_presentation"
PRESENTATION_RADIUS = 2
DENSITY_BANDWIDTH_TARGETS = 18

CONFIDENCE = ("moderate", "high")


def load_flag_style() -> Any:
    spec = importlib.util.spec_from_file_location("flag_style", FLAG_STYLE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load flag style from {FLAG_STYLE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FLAG_STYLE = load_flag_style()
FLAG_KEYS = (*FLAG_STYLE.FLAG_ORDER, FLAG_STYLE.UNFLAGGED_KEY)
FLAG_COLORS = {
    **FLAG_STYLE.flag_colors(cvd_safe=False),
    FLAG_STYLE.UNFLAGGED_KEY: FLAG_STYLE.UNFLAGGED_COLOR,
}
# Higher-contrast palette for the projection-only export. The canonical
# manuscript colors above remain unchanged, including inferred #c7e1a3.
PRESENTATION_FLAG_COLORS = {
    **FLAG_COLORS,
    "agree": "#2F9E44",
    "disagree": "#d03b3b",
    "inferred": "#9FBE63",
    "no_literature": "#77776F",
}
FLAG_LABELS = {
    **FLAG_STYLE.FLAG_LABELS,
    FLAG_STYLE.UNFLAGGED_KEY: "Unassessed",
}
FLAG_PRIORITY = {
    FLAG_STYLE.UNFLAGGED_KEY: -1,
    "no_literature": 0,
    "inferred": 1,
    "agree": 2,
    "disagree": 3,
}
DEG_BURDEN_COLOR = "#6B7075"
DENSITY_COLORS = {
    "deg": DEG_BURDEN_COLOR,
    "high": "#4C78A8",
    "moderate": "#8F6AAE",
    "low": "#9C755F",
}
PHENOTYPE_TIER_LABELS = {
    "high": "Load-bearing",
    "moderate": "Evidence only",
    "low": "Non-admissible",
}
DENSITY_ORDER = ("high", "moderate", "low")
# Deliberately use the white figure ground for blocks with no selected finding.
# This keeps absence visually empty and reserves every colored cell for a flag.
ABSENT_COLOR = "#ffffff"


def color_concepts(
    flag_colors: dict[str, str] = FLAG_COLORS,
    absence_label: str = "no load-bearing/evidence-only finding",
) -> dict[str, str]:
    return {
        **{key: flag_colors[key] for key in FLAG_KEYS},
        absence_label: ABSENT_COLOR,
        "DEG burden": DEG_BURDEN_COLOR,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def setup_plotting() -> Any:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_meaningful_union")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    import matplotlib.pyplot as plt

    plt.style.use(STYLE)
    plt.rcParams.update(
        {"svg.fonttype": "none", "pdf.fonttype": 42, "savefig.bbox": "tight"}
    )
    return plt


def load_deg() -> tuple[dict[tuple[str, str], int], dict[str, int]]:
    pair: dict[tuple[str, str], int] = {}
    totals: Counter[str] = Counter()
    for row in read_csv(DEG_CSV):
        gene = row["gene_target"]
        cell = row["group_name"]
        count = int(float(row["ndeg_padj_0.1"]))
        pair[(gene, cell)] = count
        totals[gene] += count
    return pair, dict(totals)


def target_order(totals: dict[str, int]) -> list[str]:
    """Match the deterministic order used by the existing union heatmaps."""
    def stable(name: str) -> int:
        return int(hashlib.md5(name.encode()).hexdigest(), 16)

    return sorted(
        [gene for gene, count in totals.items() if count > 0 and not gene.startswith("Safe_target")],
        key=lambda gene: (-totals[gene], stable(gene)),
    )


def confidence_counts_by_target(
    targets: list[str],
    levels: tuple[str, ...] = CONFIDENCE,
) -> dict[str, Counter[str]]:
    """Count reader-view findings per target for requested phenotype tiers."""
    target_set = set(targets)
    counts = {confidence: Counter() for confidence in levels}
    for row in read_csv(FINDINGS):
        confidence = row["phenotype_confidence"]
        gene = row["perturbation"]
        if confidence in counts and gene in target_set:
            counts[confidence][gene] += 1
    return counts


def peak_normalized_density(values: np.ndarray, bandwidth: int) -> np.ndarray:
    """Return a Gaussian-smoothed target-rank density scaled to unit peak."""
    radius = 4 * bandwidth
    offsets = np.arange(-radius, radius + 1)
    kernel = np.exp(-0.5 * (offsets / bandwidth) ** 2)
    kernel /= kernel.sum()
    smoothed = np.convolve(values.astype(float), kernel, mode="same")
    peak = float(smoothed.max())
    return smoothed / peak if peak else smoothed


def parse_cells(value: str) -> list[str]:
    return [cell.strip() for cell in value.split(";") if cell.strip()]


def collect(
    pair_deg: dict[tuple[str, str], int],
    targets: list[str],
    levels: tuple[str, ...] = CONFIDENCE,
    require_positive_deg: bool = True,
) -> tuple[
    dict[tuple[str, str], Counter[str]],
    dict[tuple[str, str], Counter[str]],
    dict[str, Any],
]:
    """Collect positive-DEG placements for the requested phenotype tiers."""
    rows = read_csv(FINDINGS)
    selected = [row for row in rows if row["phenotype_confidence"] in levels]
    target_set = set(targets)
    cell_set = set(CELL_TYPES)
    pair_confidence_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    pair_flag_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    selected_counts: Counter[str] = Counter()
    selected_flag_counts: Counter[str] = Counter()
    raw_placements: Counter[str] = Counter()
    plotted_placements: Counter[str] = Counter()
    unplaced_findings: Counter[str] = Counter()
    zero_deg_placements: Counter[str] = Counter()
    unknown_cell_placements: Counter[str] = Counter()
    unknown_cell_labels: Counter[str] = Counter()
    missing_targets: Counter[str] = Counter()
    selected_finding_ids: set[str] = set()
    contributing_findings: set[str] = set()

    for row in selected:
        confidence = row["phenotype_confidence"]
        flag = (
            FLAG_STYLE.normalize_flag(row["flag"])
            if row["flag"].strip()
            else FLAG_STYLE.UNFLAGGED_KEY
        )
        selected_finding_ids.add(row["source_id"])
        selected_counts[confidence] += 1
        selected_flag_counts[flag] += 1
        cells = list(dict.fromkeys(parse_cells(row["cell_types"])))
        if not cells:
            unplaced_findings[confidence] += 1
            continue
        gene = row["perturbation"]
        if gene not in target_set:
            missing_targets[confidence] += 1
            continue
        contributes = False
        for cell in cells:
            raw_placements[confidence] += 1
            if cell not in cell_set:
                unknown_cell_placements[confidence] += 1
                unknown_cell_labels[cell] += 1
                continue
            has_positive_deg = pair_deg.get((gene, cell), 0) > 0
            if not has_positive_deg:
                zero_deg_placements[confidence] += 1
                if require_positive_deg:
                    continue
            pair_confidence_counts[(gene, cell)][confidence] += 1
            pair_flag_counts[(gene, cell)][flag] += 1
            plotted_placements[confidence] += 1
            contributes = True
        if contributes:
            contributing_findings.add(row["source_id"])

    known_counts = {"high": 1519, "moderate": 1285, "low": 2338}
    expected = Counter({level: known_counts[level] for level in levels})
    if selected_counts != expected:
        raise ValueError(
            f"Reader-view confidence counts changed: expected {dict(expected)}, "
            f"observed {dict(selected_counts)}"
        )
    if missing_targets:
        raise ValueError(
            f"Reader-view findings missing from the DEG target universe: {dict(missing_targets)}"
        )

    audit = {
        "source": str(FINDINGS.relative_to(ROOT)),
        "selected_findings": len(selected),
        "findings_by_confidence": dict(selected_counts),
        "findings_by_flag": {
            FLAG_LABELS[key]: selected_flag_counts[key] for key in FLAG_KEYS
        },
        "findings_contributing_at_least_one_plotted_block": len(contributing_findings),
        "findings_without_a_plotted_block": len(selected_finding_ids - contributing_findings),
        "unplaced_findings_by_confidence": dict(unplaced_findings),
        "raw_explicit_cell_placements_by_confidence": dict(raw_placements),
        (
            "plotted_positive_deg_placements_by_confidence"
            if require_positive_deg
            else "plotted_explicit_cell_placements_by_confidence"
        ): dict(plotted_placements),
        "noncanonical_cell_labels_excluded_by_confidence": dict(unknown_cell_placements),
        "noncanonical_cell_labels": dict(sorted(unknown_cell_labels.items())),
        "positive_local_deg_required": require_positive_deg,
        (
            "zero_deg_placements_excluded_by_confidence"
            if require_positive_deg
            else "zero_deg_placements_included_by_confidence"
        ): dict(zero_deg_placements),
    }
    return pair_confidence_counts, pair_flag_counts, audit


def resolve(
    pair_flag_counts: dict[tuple[str, str], Counter[str]],
    targets: list[str],
) -> tuple[np.ndarray, dict[tuple[str, str], str]]:
    target_index = {gene: i for i, gene in enumerate(targets)}
    cell_index = {cell: i for i, cell in enumerate(CELL_TYPES)}
    matrix = np.full((len(CELL_TYPES), len(targets)), np.nan)
    chosen: dict[tuple[str, str], str] = {}
    for pair, counts in pair_flag_counts.items():
        gene, cell = pair
        best = max(counts, key=FLAG_PRIORITY.get)
        chosen[pair] = best
        matrix[cell_index[cell], target_index[gene]] = FLAG_KEYS.index(best)
    return matrix, chosen


def emphasize_for_projection(
    exact: np.ndarray,
    eligible: np.ndarray,
    radius: int = PRESENTATION_RADIUS,
) -> np.ndarray:
    """Widen exact marks horizontally for screen projection.

    The display-only dilation is restricted to the positive-DEG universe.
    Competing widened marks use the same flag priority as exact blocks, while
    every exact block is restored afterward so its adjudicated flag cannot be
    overwritten. This intentionally colors adjacent target boxes and must not
    be used as a quantitative coverage matrix.
    """
    emphasized = np.full_like(exact, np.nan)
    for key in sorted(FLAG_KEYS, key=FLAG_PRIORITY.get):
        code = FLAG_KEYS.index(key)
        mask = exact == code
        spread = np.zeros_like(mask)
        for offset in range(-radius, radius + 1):
            if offset < 0:
                spread[:, :offset] |= mask[:, -offset:]
            elif offset > 0:
                spread[:, offset:] |= mask[:, :-offset]
            else:
                spread |= mask
        emphasized[spread & eligible] = code
    exact_mask = ~np.isnan(exact)
    emphasized[exact_mask] = exact[exact_mask]
    return emphasized


def draw_matrix(
    ax: Any,
    matrix: np.ndarray,
    targets: list[str],
    flag_colors: dict[str, str] = FLAG_COLORS,
) -> None:
    """Draw the shared matrix layer used by the panel and joint plate."""
    from matplotlib.colors import BoundaryNorm, ListedColormap

    colors = [flag_colors[name] for name in FLAG_KEYS]
    cmap = ListedColormap(colors)
    cmap.set_bad(ABSENT_COLOR)
    norm = BoundaryNorm(np.arange(-0.5, len(colors) + 0.5, 1), cmap.N)
    ax.imshow(
        matrix,
        aspect="auto",
        cmap=cmap,
        norm=norm,
        interpolation="none",
        origin="upper",
        extent=[0, len(targets), len(CELL_TYPES), 0],
        rasterized=True,
        resample=False,
    )
    ax.set_xlim(0, len(targets))
    ax.set_ylim(len(CELL_TYPES), 0)
    ax.set_yticks(np.arange(len(CELL_TYPES)) + 0.5, CELL_TYPES, fontsize=5.1)
    ax.tick_params(axis="y", length=0)
    ax.set_xticks([])
    ax.set_box_aspect(1)
    ax.set_xlabel(
        f"Perturbation target (n={len(targets):,}; sorted by total DEG burden ↓)",
        fontsize=6.2,
    )


def legend_handles(
    matrix: np.ndarray,
    absence_label: str = "No load-bearing/evidence-only finding",
    flag_colors: dict[str, str] = FLAG_COLORS,
) -> list[Any]:
    from matplotlib.patches import Patch

    present_codes = {int(value) for value in matrix[~np.isnan(matrix)]}
    present_flags = [
        key for index, key in enumerate(FLAG_KEYS) if index in present_codes
    ]
    return [
        *[
            Patch(
                fc=flag_colors[key],
                ec="#cccccc",
                lw=0.3,
                label=FLAG_LABELS[key],
            )
            for key in present_flags
        ],
        Patch(
            fc=ABSENT_COLOR,
            ec="#aaaaaa",
            lw=0.5,
            label=absence_label,
        ),
    ]


def subtitle(
    exact_matrix: np.ndarray,
    universe_pairs: int,
    targets: list[str],
    projection_radius: int = 0,
    density_levels: tuple[str, ...] = (),
    matrix_levels: tuple[str, ...] = CONFIDENCE,
    universe_label: str = "DEG-positive target×class blocks",
    placement_note: str = "zero-DEG placements are not plotted.",
) -> str:
    covered_pairs = int(np.sum(~np.isnan(exact_matrix)))
    covered_targets = int(np.sum(np.any(~np.isnan(exact_matrix), axis=0)))
    text = (
        f"{covered_pairs:,}/{universe_pairs:,} {universe_label} "
        f"({100 * covered_pairs / universe_pairs:.1f}%) across "
        f"{covered_targets:,}/{len(targets):,} targets. Each block shows its most "
        f"decisive flag; {placement_note}"
    )
    if projection_radius:
        text += (
            f" Presentation view: marks widened ±{projection_radius} adjacent "
            "target for screen visibility."
        )
    if density_levels:
        labels = [PHENOTYPE_TIER_LABELS[level] for level in density_levels]
        text += (
            " Top curves show peak-normalized, rank-smoothed DEG and "
            + ", ".join(labels)
            + " finding densities."
        )
        density_only = [
            PHENOTYPE_TIER_LABELS[level]
            for level in density_levels
            if level not in matrix_levels
        ]
        if density_only:
            text += f" {', '.join(density_only)} findings contribute only to the top density."
    return text


def save_all(fig: Any, stem: str) -> list[Path]:
    written = []
    for suffix in ("png", "svg", "pdf"):
        path = HERE / f"{stem}.{suffix}"
        # The matrix has 1,092 target columns; 400 dpi keeps each exact cell
        # visually present in the raster reference without widening it into a
        # neighboring zero-coverage block.
        dpi = 600
        fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
        written.append(path)
    return written


def render_standalone(
    plt: Any,
    display_matrix: np.ndarray,
    exact_matrix: np.ndarray,
    targets: list[str],
    universe_pairs: int,
    *,
    stem: str = STEM,
    projection_radius: int = 0,
    flag_colors: dict[str, str] = FLAG_COLORS,
    matrix_levels: tuple[str, ...] = CONFIDENCE,
    title_text: str = "Literature flags among load-bearing and evidence-only findings",
    absence_label: str = "No load-bearing/evidence-only finding",
    universe_label: str = "DEG-positive target×class blocks",
    placement_note: str = "zero-DEG placements are not plotted.",
) -> list[Path]:
    from figures.panel_kit import audit

    fig, ax = plt.subplots(figsize=(8.4, 8.4))
    draw_matrix(ax, display_matrix, targets, flag_colors)
    fig.subplots_adjust(left=0.23, right=0.98, top=0.84, bottom=0.12)
    fig.text(
        0.23,
        0.985,
        title_text,
        fontsize=8.5,
        fontweight="bold",
        ha="left",
        va="top",
    )
    fig.text(
        0.23,
        0.93,
        subtitle(
            exact_matrix,
            universe_pairs,
            targets,
            projection_radius,
            matrix_levels=matrix_levels,
            universe_label=universe_label,
            placement_note=placement_note,
        ),
        fontsize=5.35,
        color="#555555",
        ha="left",
        va="top",
    )
    fig.legend(
        handles=legend_handles(
            exact_matrix,
            (
                "Uncovered background"
                if projection_radius
                else absence_label
            ),
            flag_colors,
        ),
        ncol=3,
        frameon=False,
        fontsize=6,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.005),
        handlelength=1,
        columnspacing=1.4,
    )
    audit(fig, concepts=color_concepts(flag_colors, absence_label.lower()))
    return save_all(fig, f"{stem}__matrix")


def render_plate(
    plt: Any,
    display_matrix: np.ndarray,
    exact_matrix: np.ndarray,
    targets: list[str],
    totals: dict[str, int],
    universe_pairs: int,
    *,
    stem: str = STEM,
    projection_radius: int = 0,
    flag_colors: dict[str, str] = FLAG_COLORS,
    confidence_counts: dict[str, Counter[str]] | None = None,
    matrix_levels: tuple[str, ...] = CONFIDENCE,
    title_text: str = "Literature flags among load-bearing and evidence-only findings",
    absence_label: str = "No load-bearing/evidence-only finding",
    universe_label: str = "DEG-positive target×class blocks",
    placement_note: str = "zero-DEG placements are not plotted.",
) -> list[Path]:
    from figures.panel_kit import audit
    from matplotlib.gridspec import GridSpec

    burden = np.log10(np.array([totals[gene] for gene in targets]) + 1)
    fig = plt.figure(figsize=(8.4, 8.4))
    grid = GridSpec(
        2,
        2,
        figure=fig,
        width_ratios=[1, 0.22],
        height_ratios=[0.16, 1],
        wspace=0.04,
        hspace=0.06,
        left=0.23,
        right=0.98,
        top=0.84,
        bottom=0.12,
    )
    top = fig.add_subplot(grid[0, 0])
    ax = fig.add_subplot(grid[1, 0], sharex=top)
    right = fig.add_subplot(grid[1, 1], sharey=ax)
    mix = fig.add_subplot(grid[0, 1])

    draw_matrix(ax, display_matrix, targets, flag_colors)
    x = np.arange(len(targets)) + 0.5
    if confidence_counts is None:
        top.fill_between(
            x,
            burden,
            step="mid",
            color=DEG_BURDEN_COLOR,
            linewidth=0,
            rasterized=True,
        )
        top.set_ylim(0, burden.max() * 1.05)
        top.set_ylabel(
            "DEG burden\nlog₁₀(n+1)",
            fontsize=5.2,
            rotation=0,
            ha="right",
            va="center",
        )
        top.set_yticks([0, 4])
    else:
        density_levels = tuple(
            level for level in DENSITY_ORDER if level in confidence_counts
        )
        density_series = [
            ("DEG burden", burden, DENSITY_COLORS["deg"]),
            *[
                (
                    PHENOTYPE_TIER_LABELS[level],
                    np.array(
                        [confidence_counts[level][gene] for gene in targets]
                    ),
                    DENSITY_COLORS[level],
                )
                for level in density_levels
            ],
        ]
        for label, raw_values, color in density_series:
            density = peak_normalized_density(raw_values, DENSITY_BANDWIDTH_TARGETS)
            top.fill_between(x, density, color=color, alpha=0.10, linewidth=0)
            top.plot(x, density, color=color, linewidth=1.0, label=label)
        top.set_ylim(0, 1.05)
        top.set_ylabel(
            "normalized\ndensity",
            fontsize=5.2,
            rotation=0,
            ha="right",
            va="center",
        )
        top.set_yticks([0, 1])
        top.legend(
            loc="upper right",
            ncol=len(density_series),
            frameon=False,
            fontsize=4.5,
            handlelength=1.6,
            columnspacing=0.9,
            borderaxespad=0.15,
        )
    top.yaxis.set_label_coords(-0.02, 0.5)
    top.tick_params(axis="x", labelbottom=False, length=0)
    top.tick_params(axis="y", labelsize=5, length=2)
    top.spines[["top", "right"]].set_visible(False)

    for row_index in range(len(CELL_TYPES)):
        values = exact_matrix[row_index][~np.isnan(exact_matrix[row_index])]
        left = 0.0
        for flag in FLAG_KEYS:
            code = FLAG_KEYS.index(flag)
            fraction = float(np.sum(values == code) / len(values)) if len(values) else 0.0
            right.barh(
                row_index + 0.5,
                fraction,
                left=left,
                height=1.0,
                color=flag_colors[flag],
                linewidth=0,
            )
            left += fraction
    right.set_xlim(0, 1)
    right.set_ylim(len(CELL_TYPES), 0)
    right.set_xlabel("mix per class", fontsize=5.2)
    right.set_xticks([0, 1])
    right.tick_params(axis="x", labelsize=5, length=2)
    right.tick_params(axis="y", labelleft=False, length=0)
    right.spines[["top", "right"]].set_visible(False)

    values = exact_matrix[~np.isnan(exact_matrix)]
    left = 0.0
    for flag in FLAG_KEYS:
        code = FLAG_KEYS.index(flag)
        fraction = float(np.sum(values == code) / len(values)) if len(values) else 0.0
        mix.barh(0, fraction, left=left, height=1.0, color=flag_colors[flag], linewidth=0)
        left += fraction
    mix.set_xlim(0, 1)
    mix.set_ylim(-0.6, 0.6)
    mix.axis("off")
    mix.set_title("overall mix", fontsize=5.2, pad=1)

    fig.text(
        0.23,
        0.985,
        title_text,
        fontsize=8.5,
        fontweight="bold",
        ha="left",
        va="top",
    )
    fig.text(
        0.23,
        0.93,
        subtitle(
            exact_matrix,
            universe_pairs,
            targets,
            projection_radius,
            tuple(
                level
                for level in DENSITY_ORDER
                if confidence_counts is not None and level in confidence_counts
            ),
            matrix_levels,
            universe_label,
            placement_note,
        ),
        fontsize=5.35,
        color="#555555",
        ha="left",
        va="top",
    )
    fig.legend(
        handles=legend_handles(
            exact_matrix,
            (
                "Uncovered background"
                if projection_radius
                else absence_label
            ),
            flag_colors,
        ),
        ncol=3,
        frameon=False,
        fontsize=6,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.005),
        handlelength=1,
        columnspacing=1.4,
    )
    # The matrix itself is square. These expected audit notes apply only to the
    # aligned top/right/overall marginals, which must inherit the matrix span.
    concepts = color_concepts(flag_colors, absence_label.lower())
    if confidence_counts is not None:
        concepts.update(
            {
                f"{PHENOTYPE_TIER_LABELS[level]} rank density": DENSITY_COLORS[level]
                for level in DENSITY_ORDER
                if level in confidence_counts
            }
        )
    audit(fig, concepts=concepts)
    return save_all(fig, stem)


def write_audit(
    pair_confidence_counts: dict[tuple[str, str], Counter[str]],
    pair_flag_counts: dict[tuple[str, str], Counter[str]],
    chosen: dict[tuple[str, str], str],
    pair_deg: dict[tuple[str, str], int],
    totals: dict[str, int],
    targets: list[str],
) -> None:
    rows = []
    for cell in CELL_TYPES:
        for gene in targets:
            confidence_counts = pair_confidence_counts.get((gene, cell), Counter())
            flag_counts = pair_flag_counts.get((gene, cell), Counter())
            rows.append(
                {
                    "perturbation": gene,
                    "cell_type": cell,
                    "target_total_deg": totals[gene],
                    "target_cell_deg": pair_deg.get((gene, cell), 0),
                    "in_positive_deg_universe": int(pair_deg.get((gene, cell), 0) > 0),
                    "covered_high_or_moderate": int((gene, cell) in chosen),
                    "displayed_flag": FLAG_LABELS.get(chosen.get((gene, cell), ""), ""),
                    "n_high_findings": confidence_counts["high"],
                    "n_moderate_findings": confidence_counts["moderate"],
                    "n_agree_findings": flag_counts["agree"],
                    "n_disagree_findings": flag_counts["disagree"],
                    "n_inferred_findings": flag_counts["inferred"],
                    "n_no_literature_findings": flag_counts["no_literature"],
                    "n_unassessed_findings": flag_counts[FLAG_STYLE.UNFLAGGED_KEY],
                }
            )
    write_csv(HERE / f"{STEM}_cells.csv", rows)


def main() -> None:
    plt = setup_plotting()
    pair_deg, totals = load_deg()
    targets = target_order(totals)
    universe_pairs = sum(
        pair_deg.get((gene, cell), 0) > 0 for gene in targets for cell in CELL_TYPES
    )
    pair_confidence_counts, pair_flag_counts, source_audit = collect(pair_deg, targets)
    target_confidence_counts = confidence_counts_by_target(targets)
    matrix, chosen = resolve(pair_flag_counts, targets)
    eligible = np.array(
        [
            [pair_deg.get((gene, cell), 0) > 0 for gene in targets]
            for cell in CELL_TYPES
        ],
        dtype=bool,
    )
    presentation_matrix = emphasize_for_projection(matrix, eligible)

    written = []
    written.extend(render_standalone(plt, matrix, matrix, targets, universe_pairs))
    plt.close("all")
    written.extend(render_plate(plt, matrix, matrix, targets, totals, universe_pairs))
    plt.close("all")
    presentation_written = []
    presentation_written.extend(
        render_standalone(
            plt,
            presentation_matrix,
            matrix,
            targets,
            universe_pairs,
            stem=PRESENTATION_STEM,
            projection_radius=PRESENTATION_RADIUS,
            flag_colors=PRESENTATION_FLAG_COLORS,
        )
    )
    plt.close("all")
    presentation_written.extend(
        render_plate(
            plt,
            presentation_matrix,
            matrix,
            targets,
            totals,
            universe_pairs,
            stem=PRESENTATION_STEM,
            projection_radius=PRESENTATION_RADIUS,
            flag_colors=PRESENTATION_FLAG_COLORS,
        )
    )
    plt.close("all")
    density_written = []
    density_written.extend(
        render_standalone(
            plt,
            matrix,
            matrix,
            targets,
            universe_pairs,
            stem=DENSITY_STEM,
        )
    )
    plt.close("all")
    density_written.extend(
        render_plate(
            plt,
            matrix,
            matrix,
            targets,
            totals,
            universe_pairs,
            stem=DENSITY_STEM,
            confidence_counts=target_confidence_counts,
        )
    )
    plt.close("all")
    presentation_density_written = []
    presentation_density_written.extend(
        render_standalone(
            plt,
            presentation_matrix,
            matrix,
            targets,
            universe_pairs,
            stem=PRESENTATION_DENSITY_STEM,
            projection_radius=PRESENTATION_RADIUS,
            flag_colors=PRESENTATION_FLAG_COLORS,
        )
    )
    plt.close("all")
    presentation_density_written.extend(
        render_plate(
            plt,
            presentation_matrix,
            matrix,
            targets,
            totals,
            universe_pairs,
            stem=PRESENTATION_DENSITY_STEM,
            projection_radius=PRESENTATION_RADIUS,
            flag_colors=PRESENTATION_FLAG_COLORS,
            confidence_counts=target_confidence_counts,
        )
    )
    plt.close("all")
    write_audit(
        pair_confidence_counts,
        pair_flag_counts,
        chosen,
        pair_deg,
        totals,
        targets,
    )

    best_counts = Counter(chosen.values())
    summary = {
        **source_audit,
        "finding_filter": (
            "Reader-facing phenotype_confidence in {high, moderate}; low findings excluded."
        ),
        "flag_rule": (
            "Each block takes its most decisive flag: Disagree > Agree > Inferred > "
            "No Literature > Unassessed."
        ),
        "placement_rule": (
            "Explicit reader-view cell placement intersected with target×cell blocks "
            "having at least one DEG at FDR < 0.1."
        ),
        "universe_pairs": universe_pairs,
        "universe_targets": len(targets),
        "covered_pairs": len(chosen),
        "covered_pairs_percent": round(100 * len(chosen) / universe_pairs, 1),
        "covered_targets": len({gene for gene, _ in chosen}),
        "covered_targets_percent": round(
            100 * len({gene for gene, _ in chosen}) / len(targets), 1
        ),
        "blocks_by_displayed_flag": {
            FLAG_LABELS[key]: best_counts[key] for key in FLAG_KEYS
        },
        "outputs": [path.name for path in written],
        "presentation_variant": {
            "horizontal_expansion_radius_targets": PRESENTATION_RADIUS,
            "exact_colored_blocks": int(np.sum(~np.isnan(matrix))),
            "emphasized_colored_blocks": int(np.sum(~np.isnan(presentation_matrix))),
            "marginal_statistics_use_exact_matrix": True,
            "flag_colors": {
                FLAG_LABELS[key]: PRESENTATION_FLAG_COLORS[key] for key in FLAG_KEYS
            },
            "outputs": [path.name for path in presentation_written],
        },
        "three_density_variant": {
            "definition": (
                "Peak-normalized Gaussian-smoothed densities across DEG-sorted "
                "target rank for log10 total DEG burden and per-target counts of "
                "reader-view load-bearing and evidence-only findings."
            ),
            "bandwidth_targets": DENSITY_BANDWIDTH_TARGETS,
            "colors": {
                "DEG burden": DENSITY_COLORS["deg"],
                "Load-bearing": DENSITY_COLORS["high"],
                "Evidence only": DENSITY_COLORS["moderate"],
            },
            "finding_counts": {
                confidence: sum(target_confidence_counts[confidence].values())
                for confidence in CONFIDENCE
            },
            "outputs": [path.name for path in density_written],
            "presentation_outputs": [
                path.name for path in presentation_density_written
            ],
        },
    }
    (HERE / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
