#!/usr/bin/env python3
"""Render literature flags with DEG and three phenotype-tier densities.

The target x cell-class matrix combines all three reader-facing tiers:
load-bearing (``phenotype_confidence=high``), evidence-only
(``phenotype_confidence=moderate``), and non-admissible
(``phenotype_confidence=low``). The top panel compares their target-rank
distributions with DEG burden.

The curves use the same Gaussian smoothing over DEG-sorted target rank as the
earlier density variant.  Each curve is independently peak-normalized, so its
shape and location are comparable but its height is not an absolute count.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_high_moderate_confidence_heatmap as base


HERE = Path(__file__).resolve().parent
STEM = "fig2_literature_flag_tier_density_heatmap"
TIERS = ("high", "moderate", "low")


def target_count_rows(
    targets: list[str],
    totals: dict[str, int],
    tier_counts: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return the exact unsmoothed values underlying the top density curves."""
    return [
        {
            "target_rank": rank,
            "perturbation": gene,
            "total_deg_burden": totals[gene],
            "n_load_bearing_findings": tier_counts["high"][gene],
            "n_evidence_only_findings": tier_counts["moderate"][gene],
            "n_non_admissible_findings": tier_counts["low"][gene],
        }
        for rank, gene in enumerate(targets, start=1)
    ]


def build_variant(
    *,
    stem: str = STEM,
    require_positive_deg: bool = True,
    title_text: str = "Literature flags across all finding tiers",
    universe_label: str = "DEG-positive target×class blocks",
    placement_note: str = "zero-DEG placements are not plotted.",
    placement_rule: str = (
        "Explicit reader-view cell placement intersected with target x cell "
        "blocks having at least one DEG at FDR < 0.1."
    ),
) -> dict[str, Any]:
    plt = base.setup_plotting()
    pair_deg, totals = base.load_deg()
    targets = base.target_order(totals)
    universe_pairs = (
        sum(
            pair_deg.get((gene, cell), 0) > 0
            for gene in targets
            for cell in base.CELL_TYPES
        )
        if require_positive_deg
        else len(targets) * len(base.CELL_TYPES)
    )

    _, pair_flag_counts, source_audit = base.collect(
        pair_deg,
        targets,
        TIERS,
        require_positive_deg=require_positive_deg,
    )
    matrix, chosen = base.resolve(pair_flag_counts, targets)
    tier_counts = base.confidence_counts_by_target(targets, TIERS)

    written = []
    written.extend(
        base.render_standalone(
            plt,
            matrix,
            matrix,
            targets,
            universe_pairs,
            stem=stem,
            matrix_levels=TIERS,
            title_text=title_text,
            absence_label="No classified finding",
            universe_label=universe_label,
            placement_note=placement_note,
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
            matrix_levels=TIERS,
            title_text=title_text,
            absence_label="No classified finding",
            universe_label=universe_label,
            placement_note=placement_note,
        )
    )
    plt.close("all")

    count_path = HERE / f"{stem}_target_counts.csv"
    base.write_csv(count_path, target_count_rows(targets, totals, tier_counts))

    best_counts = Counter(chosen.values())
    tier_totals = {
        base.PHENOTYPE_TIER_LABELS[tier]: sum(tier_counts[tier].values())
        for tier in TIERS
    }
    summary = {
        **source_audit,
        "visualization": (
            "Literature-flag heatmap with peak-normalized rank densities for DEG "
            "burden and the three reader-facing phenotype tiers."
        ),
        "matrix_finding_filter": (
            "All three reader-facing phenotype tiers: load-bearing (high), "
            "evidence-only (moderate), and non-admissible (low)."
        ),
        "density_finding_filter": (
            "All three reader-facing phenotype tiers: load-bearing (high), "
            "evidence-only (moderate), and non-admissible (low)."
        ),
        "tier_mapping": {
            "high": "Load-bearing",
            "moderate": "Evidence only",
            "low": "Non-admissible",
        },
        "density_definition": (
            "Gaussian-smoothed values across perturbations sorted by descending "
            "total DEG burden. DEG values are log10(n+1) before smoothing; each "
            "curve is independently scaled to a peak of 1."
        ),
        "density_bandwidth_targets": base.DENSITY_BANDWIDTH_TARGETS,
        "density_colors": {
            "DEG burden": base.DENSITY_COLORS["deg"],
            **{
                base.PHENOTYPE_TIER_LABELS[tier]: base.DENSITY_COLORS[tier]
                for tier in TIERS
            },
        },
        "finding_counts_by_tier": tier_totals,
        "flag_rule": (
            "Each matrix block takes its most decisive finding flag across all tiers: "
            "Disagree > Agree > Inferred > No Literature > Unassessed."
        ),
        "placement_rule": placement_rule,
        "universe_label": universe_label,
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
        "target_count_csv": count_path.name,
        "outputs": [path.name for path in written],
    }
    summary_path = HERE / f"{stem}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    build_variant()


if __name__ == "__main__":
    main()
