#!/usr/bin/env python3
"""Plot odd-seed depletion recall for BioAgents, Codex, and deterministic controls."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bioagents-matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
SOURCE_ROOT = Path("/gpfs/group/jin/asun/bioagents")
EXPORT_ROOT = SOURCE_ROOT / "export/q7-depletion"
ODD_SEED_EXPORT = Path(
    "/gpfs/group/jin/asun/bioagents-adaptive-findings/exports/"
    "q7-depletion-odd-seed-framework-results-2026-08-26"
)

DEFAULT_TRUTH = (
    EXPORT_ROOT
    / "ground_truth/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv"
)
DEFAULT_CODEX_ANSWERS = tuple(
    ODD_SEED_EXPORT / f"results/codex/rep{replicate}/answer.txt"
    for replicate in range(1, 4)
)
DEFAULT_BIOAGENTS_ANSWERS = tuple(
    ODD_SEED_EXPORT / f"results/bioagents/rep{replicate}/answer.txt"
    for replicate in range(1, 4)
)
DEFAULT_DEPMAP_RANKING = (
    SOURCE_ROOT / "debug/depletion/depmap_baseline/depmap_top100_annotated.csv"
)
DEFAULT_TOP_DEG_RANKING = (
    SOURCE_ROOT
    / "debug/260725_claim_layer/inputs/q7_deg_prune_graph_r01/"
    "complete_starting_deg_ranking.tsv"
)

KS = tuple(range(5, 51, 5))
COLORS = {
    "BioAgents": "#007F5F",
    "Codex": "#D55E00",
    "DepMap": "#7B2CBF",
    "Top DEG": "#E69F00",
}
MARKERS = {
    "BioAgents": "h",
    "Codex": "^",
    "DepMap": "s",
    "Top DEG": "D",
}
BASELINE_METHODS = {"DepMap", "Top DEG"}
BASELINE_METADATA = {
    "DepMap": {
        "implementation": "negative pan-cancer median Chronos gene effect",
        "source_system": "DepMap cancer cell lines",
    },
    "Top DEG": {
        "implementation": (
            "151 TH survivor-cell DEG count at adjusted p < 0.05; ties by summed "
            "then mean absolute log fold-change"
        ),
        "source_system": "same-experiment differential-expression table",
    },
}
EXPECTED_HITS_AT_50 = {
    "BioAgents": (19, 18, 17),
    "Codex": (9, 12, 9),
    "DepMap": (13,),
    "Top DEG": (7,),
}
FENCED_TSV = re.compile(r"```tsv\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument(
        "--codex-answer",
        type=Path,
        action="append",
        dest="codex_answers",
        help="Codex answer.txt; repeat exactly three times to override defaults.",
    )
    parser.add_argument(
        "--bioagents-answer",
        type=Path,
        action="append",
        dest="bioagents_answers",
        help="BioAgents answer.txt; repeat exactly three times to override defaults.",
    )
    parser.add_argument("--depmap-ranking", type=Path, default=DEFAULT_DEPMAP_RANKING)
    parser.add_argument("--top-deg-ranking", type=Path, default=DEFAULT_TOP_DEG_RANKING)
    parser.add_argument("--output-dir", type=Path, default=SCRIPT_DIR)
    parser.add_argument(
        "--stem",
        default="depletion-best-vs-codex-heldout-recall",
        help="Output filename stem.",
    )
    args = parser.parse_args()
    args.codex_answers = tuple(args.codex_answers or DEFAULT_CODEX_ANSWERS)
    args.bioagents_answers = tuple(args.bioagents_answers or DEFAULT_BIOAGENTS_ANSWERS)
    for name in ("codex_answers", "bioagents_answers"):
        if len(getattr(args, name)) != 3:
            parser.error(f"--{name.replace('_', '-')} must resolve to exactly 3 paths")
    return args


def require_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_ranking(path: Path, rows: list[tuple[int, str]]) -> list[str]:
    rows.sort(key=lambda row: row[0])
    ranks = [rank for rank, _ in rows]
    genes = [gene.strip() for _, gene in rows]
    if ranks != list(range(1, len(rows) + 1)):
        raise ValueError(f"Expected contiguous ranks in {path}")
    if not genes or len(set(genes)) != len(genes):
        raise ValueError(f"Expected unique ranked targets in {path}")
    return genes


def parse_ranked_answer(path: Path) -> list[str]:
    path = require_file(path)
    text = path.read_text(encoding="utf-8")
    blocks = FENCED_TSV.findall(text)
    if len(blocks) != 1:
        raise ValueError(f"Expected exactly one fenced TSV block in {path}")
    rows = list(csv.DictReader(io.StringIO(blocks[0]), delimiter="\t"))
    if not rows or not {"rank", "gene_target"}.issubset(rows[0]):
        raise ValueError(f"Missing rank/gene_target columns in {path}")
    ranking = validate_ranking(
        path,
        [(int(row["rank"]), str(row["gene_target"])) for row in rows],
    )
    if len(ranking) != 50:
        raise ValueError(f"Expected exactly 50 ranked targets in {path}")
    return ranking


def parse_depmap_ranking(path: Path) -> list[str]:
    path = require_file(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"depmap_rank", "gene_target"}.issubset(rows[0]):
        raise ValueError(f"Missing depmap_rank/gene_target columns in {path}")
    return validate_ranking(
        path,
        [(int(row["depmap_rank"]), str(row["gene_target"])) for row in rows],
    )


def parse_top_deg_ranking(path: Path) -> list[str]:
    path = require_file(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or not {"starting_rank", "gene_target"}.issubset(rows[0]):
        raise ValueError(f"Missing starting_rank/gene_target columns in {path}")
    return validate_ranking(
        path,
        [(int(row["starting_rank"]), str(row["gene_target"])) for row in rows],
    )


def load_truth(path: Path) -> tuple[set[str], set[str]]:
    path = require_file(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = sorted(csv.DictReader(handle), key=lambda row: int(row["depletion_rank"]))
    top100 = rows[:100]
    visible = {
        str(row["gene_target"])
        for row in top100
        if int(row["depletion_rank"]) % 2 == 1
    }
    heldout = {
        str(row["gene_target"])
        for row in top100
        if int(row["depletion_rank"]) % 2 == 0
    }
    if len(visible) != 50 or len(heldout) != 50 or visible & heldout:
        raise ValueError(f"Expected disjoint 50-target odd/even splits in {path}")
    return visible, heldout


def mask_visible_seeds(
    path: Path,
    ranking: list[str],
    visible: set[str],
) -> list[str]:
    masked = [gene for gene in ranking if gene not in visible][:50]
    if len(masked) != 50 or len(set(masked)) != 50:
        raise ValueError(f"Expected 50 non-seed targets after masking {path}")
    return masked


def recall_curve(ranking: list[str], truth: set[str]) -> list[float]:
    return [len(set(ranking[:cutoff]) & truth) / len(truth) for cutoff in KS]


def build_matrix(rankings: list[list[str]], truth: set[str]) -> np.ndarray:
    return np.asarray([recall_curve(ranking, truth) for ranking in rankings], dtype=float)


def validate_expected_hits(label: str, matrix: np.ndarray, truth_count: int) -> None:
    observed = tuple(int(round(value * truth_count)) for value in matrix[:, -1])
    expected = EXPECTED_HITS_AT_50[label]
    if observed != expected:
        raise ValueError(f"{label} mismatch: expected hits {expected}, observed {observed}")


def write_curve_table(path: Path, matrices: dict[str, np.ndarray]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("cohort", "series", "replicate", "cutoff_k", "recall"))
        for label, matrix in matrices.items():
            if label in BASELINE_METHODS:
                for cutoff, recall in zip(KS, matrix[0]):
                    writer.writerow((label, "baseline", "", cutoff, recall))
                continue
            for replicate, curve in enumerate(matrix, 1):
                for cutoff, recall in zip(KS, curve):
                    writer.writerow((label, "individual", replicate, cutoff, recall))
            for cutoff, recall in zip(KS, np.median(matrix, axis=0)):
                writer.writerow((label, "median", "", cutoff, recall))


def plot_recall(path_png: Path, path_svg: Path, matrices: dict[str, np.ndarray]) -> None:
    plt.style.use(REPO_ROOT / "src/figures/style.mplstyle")
    plt.rcParams.update(
        {
            "font.size": 10.5,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
        }
    )
    figure, axis = plt.subplots(figsize=(5.2, 5.2), layout="constrained")
    medians: dict[str, np.ndarray] = {}
    for label, matrix in matrices.items():
        is_baseline = label in BASELINE_METHODS
        if not is_baseline:
            for curve in matrix:
                axis.plot(
                    KS,
                    curve,
                    color=COLORS[label],
                    linewidth=0.9,
                    alpha=0.25,
                )
        medians[label] = np.median(matrix, axis=0)
        terminal_label = "R@50" if is_baseline else "median R@50"
        axis.plot(
            KS,
            medians[label],
            color=COLORS[label],
            linewidth=1.8 if is_baseline else 2.2,
            linestyle="--" if is_baseline else "-",
            marker=MARKERS[label],
            markersize=4.5 if is_baseline else 5.2,
            label=f"{label}  ({terminal_label} {medians[label][-1]:.2f})",
        )

    handles, labels = axis.get_legend_handles_labels()
    observed_max = max(float(np.max(matrix)) for matrix in matrices.values())
    y_max = min(1.0, math.ceil((observed_max + 0.04) * 20) / 20)
    axis.set_xlabel("predicted-rank cutoff K", fontsize=22.5)
    axis.set_ylabel("recall", fontsize=22.5)
    axis.set_xlim(5, 50)
    axis.set_ylim(0, y_max)
    axis.set_xticks((10, 20, 30, 40, 50))
    axis.legend(handles, labels, frameon=False, loc="upper left", fontsize=12)
    figure.suptitle(
        "Held-out depletion recall@K",
        x=0.01,
        ha="left",
        fontsize=19.5,
        weight="bold",
    )
    figure.savefig(path_png, dpi=300, facecolor="white", bbox_inches=None)
    figure.savefig(path_svg, facecolor="white", bbox_inches=None)
    plt.close(figure)


def write_summary(
    path: Path,
    source_paths: dict[str, tuple[Path, ...]],
    matrices: dict[str, np.ndarray],
    truth_path: Path,
    output_paths: dict[str, Path],
) -> dict[str, object]:
    summary: dict[str, object] = {
        "schema_version": "depletion-recall-comparison-v1",
        "task": "q7-depletion-odd-seed",
        "truth_definition": (
            "50 even-ranked held-out targets from the canonical Fisher top-100 "
            "depletion ranking for 151 TH Prkcd Grin2c Glut"
        ),
        "truth_count": 50,
        "cutoffs": list(KS),
        "truth": {"path": str(truth_path), "sha256": sha256_file(truth_path)},
        "cohort_contract": {
            "BioAgents": "three-run framework cohort from the 2026-08-26 odd-seed export",
            "Codex": "three-run framework cohort from the 2026-08-26 odd-seed export",
            "note": (
                "All agent answers contain 50 non-seed predictions. Deterministic "
                "rankings were converted to the same contract by removing the 50 "
                "visible odd-ranked seeds before selecting their first 50 candidates."
            ),
        },
        "cohorts": {},
        "outputs": {name: str(output) for name, output in output_paths.items()},
    }
    cohorts = summary["cohorts"]
    assert isinstance(cohorts, dict)
    for label, matrix in matrices.items():
        cohort: dict[str, object] = {
            "hits_at_50": [int(round(value * 50)) for value in matrix[:, -1]],
            "recall_at_50": matrix[:, -1].tolist(),
            "median_recall_at_50": float(np.median(matrix[:, -1])),
        }
        sources = source_paths[label]
        if label in BASELINE_METHODS:
            cohort.update(BASELINE_METADATA[label])
            cohort["ranking_artifacts"] = [
                {"path": str(source), "sha256": sha256_file(source)}
                for source in sources
            ]
        else:
            cohort["runs"] = [
                {"path": str(answer.parent), "answer_sha256": sha256_file(answer)}
                for answer in sources
            ]
        cohorts[label] = cohort
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    args = parse_args()
    truth_path = require_file(args.truth)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_paths = {
        "BioAgents": tuple(require_file(path) for path in args.bioagents_answers),
        "Codex": tuple(require_file(path) for path in args.codex_answers),
        "DepMap": (require_file(args.depmap_ranking),),
        "Top DEG": (require_file(args.top_deg_ranking),),
    }
    visible, truth = load_truth(truth_path)
    rankings = {
        "BioAgents": [parse_ranked_answer(path) for path in source_paths["BioAgents"]],
        "Codex": [parse_ranked_answer(path) for path in source_paths["Codex"]],
        "DepMap": [
            mask_visible_seeds(
                source_paths["DepMap"][0],
                parse_depmap_ranking(source_paths["DepMap"][0]),
                visible,
            )
        ],
        "Top DEG": [
            mask_visible_seeds(
                source_paths["Top DEG"][0],
                parse_top_deg_ranking(source_paths["Top DEG"][0]),
                visible,
            )
        ],
    }
    for label, cohort_rankings in rankings.items():
        for ranking in cohort_rankings:
            leaked = sorted(set(ranking) & visible)
            if leaked:
                raise ValueError(f"{label} ranking contains visible seeds: {leaked}")
    matrices = {
        label: build_matrix(cohort_rankings, truth)
        for label, cohort_rankings in rankings.items()
    }
    for label, matrix in matrices.items():
        validate_expected_hits(label, matrix, len(truth))

    png_path = output_dir / f"{args.stem}.png"
    svg_path = output_dir / f"{args.stem}.svg"
    table_path = output_dir / f"{args.stem}.tsv"
    summary_path = output_dir / f"{args.stem}.summary.json"
    plot_recall(png_path, svg_path, matrices)
    write_curve_table(table_path, matrices)
    summary = write_summary(
        summary_path,
        source_paths,
        matrices,
        truth_path,
        {"png": png_path, "svg": svg_path, "curves_tsv": table_path},
    )
    print(png_path)
    cohorts = summary["cohorts"]
    assert isinstance(cohorts, dict)
    for label in matrices:
        cohort = cohorts[label]
        metric_label = "R@50" if label in BASELINE_METHODS else "median R@50"
        print(
            f"{label}: hits@50={cohort['hits_at_50']}; "
            f"{metric_label}={cohort['median_recall_at_50']:.2f}"
        )


if __name__ == "__main__":
    main()
