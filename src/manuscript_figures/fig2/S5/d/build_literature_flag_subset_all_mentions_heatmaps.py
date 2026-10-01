#!/usr/bin/env python3
"""Render no-local-DEG literature heatmaps for selected finding tiers."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_high_moderate_confidence_heatmap as base


HERE = Path(__file__).resolve().parent
PLACEMENT_NOTE = (
    "all explicit canonical cell-type mentions are plotted regardless of local "
    "DEG support."
)
PLACEMENT_RULE = (
    "Every explicit reader-view placement in one of the 23 canonical cell "
    "classes is plotted, regardless of whether the target x cell block has a "
    "DEG at FDR < 0.1. Unresolved aggregate labels are excluded."
)


def build(
    *,
    stem: str,
    levels: tuple[str, ...],
    title: str,
    absence_label: str,
) -> dict[str, Any]:
    plt = base.setup_plotting()
    pair_deg, totals = base.load_deg()
    targets = base.target_order(totals)
    universe_pairs = len(targets) * len(base.CELL_TYPES)

    _, pair_flag_counts, source_audit = base.collect(
        pair_deg,
        targets,
        levels,
        require_positive_deg=False,
    )
    matrix, chosen = base.resolve(pair_flag_counts, targets)
    tier_counts = base.confidence_counts_by_target(targets, levels)

    written = []
    written.extend(
        base.render_standalone(
            plt,
            matrix,
            matrix,
            targets,
            universe_pairs,
            stem=stem,
            matrix_levels=levels,
            title_text=title,
            absence_label=absence_label,
            universe_label="target×class blocks",
            placement_note=PLACEMENT_NOTE,
        )
    )
    plt.close("all")
    written.extend(
        base.render_plate(
            plt,
            matrix,
            matrix,
            targets,
            totals,
            universe_pairs,
            stem=stem,
            confidence_counts=tier_counts,
            matrix_levels=levels,
            title_text=title,
            absence_label=absence_label,
            universe_label="target×class blocks",
            placement_note=PLACEMENT_NOTE,
        )
    )
    plt.close("all")

    best_counts = Counter(chosen.values())
    summary = {
        **source_audit,
        "visualization": title,
        "matrix_and_density_tiers": {
            level: base.PHENOTYPE_TIER_LABELS[level] for level in levels
        },
        "flag_rule": (
            "Each matrix block takes its most decisive flag among findings in "
            "the selected tiers: Disagree > Agree > Inferred > No Literature > "
            "Unassessed."
        ),
        "placement_rule": PLACEMENT_RULE,
        "universe_label": "target×class blocks",
        "universe_pairs": universe_pairs,
        "universe_targets": len(targets),
        "covered_pairs": len(chosen),
        "covered_pairs_percent": round(100 * len(chosen) / universe_pairs, 1),
        "covered_targets": len({gene for gene, _ in chosen}),
        "covered_targets_percent": round(
            100 * len({gene for gene, _ in chosen}) / len(targets), 1
        ),
        "blocks_by_displayed_flag": {
            base.FLAG_LABELS[key]: best_counts[key] for key in base.FLAG_KEYS
        },
        "density_definition": (
            "Gaussian-smoothed values across perturbations sorted by descending "
            "total DEG burden. DEG values are log10(n+1) before smoothing; each "
            "curve is independently scaled to a peak of 1."
        ),
        "density_bandwidth_targets": base.DENSITY_BANDWIDTH_TARGETS,
        "outputs": [path.name for path in written],
    }
    (HERE / f"{stem}_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    build(
        stem="fig2_literature_flag_load_bearing_all_mentions",
        levels=("high",),
        title="Literature flags: load-bearing findings only",
        absence_label="No load-bearing finding",
    )
    build(
        stem="fig2_literature_flag_load_bearing_evidence_only_all_mentions",
        levels=("high", "moderate"),
        title="Literature flags: load-bearing + evidence-only findings",
        absence_label="No load-bearing/evidence-only finding",
    )


if __name__ == "__main__":
    main()
