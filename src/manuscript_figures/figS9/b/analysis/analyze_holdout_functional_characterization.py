#!/usr/bin/env python3
"""Characterize Task-1 holdouts with GO, pathways, and functional themes.

The primary comparison asks whether the 272 held-out targets differ from the
1,674 model-visible training targets within the actual 1,946-target screen.
Responder/non-responder comparisons are restricted to the 272 holdouts.  This
screen-relative background is essential: a whole-genome background would mostly
rediscover how the perturbation library itself was designed.

Term-level over-representation uses a one-sided hypergeometric test and
Benjamini-Hochberg correction within each library and comparison.  The analysis
also projects annotations into the repository's established 14 functional
themes for a compact descriptive view.  Themes overlap and are not a GO-slim.
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/bioagents-mpl")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import PercentFormatter  # noqa: E402
from scipy.stats import fisher_exact, hypergeom  # noqa: E402

from figures.panel_kit import house_style, plate  # noqa: E402
from llm_score_validation.metrics_pathway_db import (  # noqa: E402
    BUCKETS,
    PATHWAY_NAME_TO_BUCKET,
)


OUTPUT_DIR = HERE / "holdout_functional_characterization_v1_20260919"
INPUT_DIR = HERE / "holdout_task" / "Inputs"
HOLDOUT_COUNTS_CSV = INPUT_DIR / "151_TH_Prkcd_Grin2c_Glut_deg_counts_holdouts.csv"
TRAINING_COUNTS_CSV = INPUT_DIR / "151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv"
HOLDOUT_REGISTRY_CSV = INPUT_DIR / "holdout_perturbations.csv"

LIBRARY_PATHS = {
    "GO Biological Process 2023": ROOT
    / "data/external/enrichr/GO_Biological_Process_2023.gmt",
    "GO Molecular Function 2023": OUTPUT_DIR
    / "libraries/GO_Molecular_Function_2023.gmt",
    "GO Cellular Component 2023": OUTPUT_DIR
    / "libraries/GO_Cellular_Component_2023.gmt",
    "Reactome 2022": ROOT / "data/external/enrichr/Reactome_2022.gmt",
    "KEGG Mouse 2019": ROOT / "data/external/enrichr/KEGG_2019_Mouse.gmt",
    "MSigDB Hallmark 2020": ROOT
    / "data/external/enrichr/MSigDB_Hallmark_2020.gmt",
}

MIN_TERM_BACKGROUND_N = 3
MAX_TERM_BACKGROUND_N = 500
MIN_REPORTED_OVERLAP_N = 3
FDR_THRESHOLD = 0.05

GROUP_COLORS = {
    "training": "#7A8490",
    "holdout": "#3676A8",
    "responder": "#C6762B",
    "non-responder": "#6F4C9B",
}


def load_counts(path: Path, expected_n: int) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if tuple(frame.columns) != ("target_name", "n_degs"):
        raise ValueError(f"Unexpected schema in {path}: {tuple(frame.columns)}")
    if len(frame) != expected_n or frame["target_name"].duplicated().any():
        raise ValueError(f"Expected {expected_n} unique targets in {path}")
    frame["target_name"] = frame["target_name"].astype(str)
    frame["gene_upper"] = frame["target_name"].str.upper()
    frame["n_degs"] = pd.to_numeric(frame["n_degs"], errors="raise").astype(int)
    return frame


def load_gmt(path: Path) -> dict[str, set[str]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if text.lstrip().lower().startswith("<!doctype html"):
        raise ValueError(f"Downloaded resource is HTML rather than GMT: {path}")
    result: dict[str, set[str]] = {}
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) < 3:
            continue
        term = fields[0].strip()
        genes = {gene.strip().upper() for gene in fields[2:] if gene.strip()}
        if term and genes:
            result[term] = genes
    if not result:
        raise ValueError(f"No gene sets parsed from {path}")
    return result


def bh_adjust(values: pd.Series) -> np.ndarray:
    pvalues = values.to_numpy(dtype=float)
    order = np.argsort(pvalues)
    adjusted = np.empty(len(pvalues), dtype=float)
    running = 1.0
    for rank, index in reversed(list(enumerate(order, start=1))):
        running = min(running, pvalues[index] * len(pvalues) / rank)
        adjusted[index] = running
    return adjusted


def odds_ratio_corrected(a: int, b: int, c: int, d: int) -> float:
    return float(math.log2(((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5))))


def enrichment_for_query(
    *,
    library_name: str,
    terms: Mapping[str, set[str]],
    comparison: str,
    query_genes: set[str],
    universe_genes: set[str],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    library_genes = set().union(*terms.values())
    background = universe_genes & library_genes
    query = query_genes & background
    M = len(background)
    N = len(query)
    rows: list[dict[str, Any]] = []
    for term, genes in terms.items():
        term_background = genes & background
        K = len(term_background)
        if not MIN_TERM_BACKGROUND_N <= K <= MAX_TERM_BACKGROUND_N:
            continue
        overlap = query & term_background
        x = len(overlap)
        a = x
        b = N - x
        c = K - x
        d = M - a - b - c
        rows.append(
            {
                "comparison": comparison,
                "library": library_name,
                "term": term,
                "overlap_n": x,
                "query_annotated_n": N,
                "term_background_n": K,
                "background_annotated_n": M,
                "query_fraction": x / N if N else np.nan,
                "reference_fraction": c / (M - N) if M > N else np.nan,
                "log2_odds_ratio_corrected": odds_ratio_corrected(a, b, c, d),
                "pvalue": float(hypergeom.sf(x - 1, M, K, N)),
                "overlap_genes": ",".join(sorted(overlap)),
            }
        )
    frame = pd.DataFrame(rows)
    frame["padj"] = bh_adjust(frame["pvalue"])
    frame = frame.sort_values(
        ["padj", "pvalue", "overlap_n", "term"],
        ascending=[True, True, False, True],
        kind="stable",
    ).reset_index(drop=True)
    coverage = {
        "comparison": comparison,
        "library": library_name,
        "query_total_n": len(query_genes),
        "query_annotated_n": N,
        "query_annotation_fraction": N / len(query_genes),
        "universe_total_n": len(universe_genes),
        "universe_annotated_n": M,
        "universe_annotation_fraction": M / len(universe_genes),
        "tested_term_n": len(frame),
    }
    return frame, coverage


def run_term_enrichment(
    libraries: Mapping[str, Mapping[str, set[str]]],
    *,
    training: set[str],
    holdout: set[str],
    responders: set[str],
    nonresponders: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    screen = training | holdout
    comparisons = {
        "holdout_vs_training": (holdout, screen),
        "training_vs_holdout": (training, screen),
        "responder_vs_nonresponder": (responders, holdout),
        "nonresponder_vs_responder": (nonresponders, holdout),
    }
    results: list[pd.DataFrame] = []
    coverage: list[dict[str, Any]] = []
    for comparison, (query, universe) in comparisons.items():
        for library_name, terms in libraries.items():
            frame, metadata = enrichment_for_query(
                library_name=library_name,
                terms=terms,
                comparison=comparison,
                query_genes=query,
                universe_genes=universe,
            )
            results.append(frame)
            coverage.append(metadata)
    return pd.concat(results, ignore_index=True), pd.DataFrame(coverage)


def themes_for_term(term: str) -> set[str]:
    return {theme for theme, pattern in PATHWAY_NAME_TO_BUCKET if pattern.search(term)}


def build_gene_annotations(
    libraries: Mapping[str, Mapping[str, set[str]]],
    holdout_counts: pd.DataFrame,
    training_counts: pd.DataFrame,
) -> pd.DataFrame:
    all_genes = set(holdout_counts["gene_upper"]) | set(training_counts["gene_upper"])
    gene_to_themes = {gene: set() for gene in all_genes}
    gene_to_library_terms = {
        gene: {library: 0 for library in libraries} for gene in all_genes
    }
    for library_name, terms in libraries.items():
        for term, genes in terms.items():
            present = genes & all_genes
            if not present:
                continue
            themes = themes_for_term(term)
            for gene in present:
                gene_to_library_terms[gene][library_name] += 1
                gene_to_themes[gene].update(themes)

    holdout_lookup = holdout_counts.set_index("gene_upper")
    display_lookup = pd.concat(
        [
            training_counts[["target_name", "gene_upper"]],
            holdout_counts[["target_name", "gene_upper"]],
        ],
        ignore_index=True,
    ).set_index("gene_upper")["target_name"]
    records: list[dict[str, Any]] = []
    training_genes = set(training_counts["gene_upper"])
    for gene in sorted(all_genes):
        is_holdout = gene not in training_genes
        n_degs = int(holdout_lookup.loc[gene, "n_degs"]) if is_holdout else np.nan
        row: dict[str, Any] = {
            "target_name": str(display_lookup.loc[gene]),
            "gene_upper": gene,
            "benchmark_group": "holdout" if is_holdout else "training",
            "actual_n_degs": n_degs,
            "response_group": "responder"
            if is_holdout and n_degs > 0
            else ("non-responder" if is_holdout else "not applicable"),
            "functional_themes": "|".join(sorted(gene_to_themes[gene])),
            "n_functional_themes": len(gene_to_themes[gene]),
        }
        for library_name in libraries:
            slug = (
                library_name.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )
            row[f"n_terms_{slug}"] = gene_to_library_terms[gene][library_name]
        for theme in BUCKETS:
            row[f"theme_{theme}"] = theme in gene_to_themes[gene]
        records.append(row)
    return pd.DataFrame(records)


def attach_holdout_selection(frame: pd.DataFrame) -> pd.DataFrame:
    registry = pd.read_csv(HOLDOUT_REGISTRY_CSV).rename(
        columns={"perturbation": "target_name"}
    )
    registry = registry[registry["target_name"].ne("Safe_target_1")].copy()
    if len(registry) != 272 or registry["target_name"].duplicated().any():
        raise ValueError("Expected 272 biological targets in the holdout registry")
    result = frame.merge(registry, on="target_name", how="left", validate="one_to_one")
    if result["held_out_from"].isna().any():
        raise ValueError("Holdout annotations did not match the complete registry")
    result["selection_stratum"] = np.where(
        result["no_significant_effect_holdout"],
        "no_significant_effect selection",
        "other outcome-based selection",
    )
    return result


def summarize_themes(
    annotations: pd.DataFrame,
) -> pd.DataFrame:
    comparisons = {
        "holdout_vs_training": (
            annotations["benchmark_group"].eq("holdout"),
            annotations["benchmark_group"].eq("training"),
        ),
        "responder_vs_nonresponder": (
            annotations["response_group"].eq("responder"),
            annotations["response_group"].eq("non-responder"),
        ),
    }
    rows: list[dict[str, Any]] = []
    for comparison, (query_mask, reference_mask) in comparisons.items():
        for theme in BUCKETS:
            values = annotations[f"theme_{theme}"]
            a = int((query_mask & values).sum())
            b = int((query_mask & ~values).sum())
            c = int((reference_mask & values).sum())
            d = int((reference_mask & ~values).sum())
            rows.append(
                {
                    "comparison": comparison,
                    "theme": theme,
                    "query_n": a + b,
                    "query_with_theme_n": a,
                    "query_fraction": a / (a + b),
                    "reference_n": c + d,
                    "reference_with_theme_n": c,
                    "reference_fraction": c / (c + d),
                    "fraction_difference": a / (a + b) - c / (c + d),
                    "log2_odds_ratio_corrected": odds_ratio_corrected(a, b, c, d),
                    "pvalue_two_sided": float(
                        fisher_exact([[a, b], [c, d]], alternative="two-sided").pvalue
                    ),
                }
            )
    result = pd.DataFrame(rows)
    result["padj"] = np.nan
    for comparison, index in result.groupby("comparison").groups.items():
        result.loc[index, "padj"] = bh_adjust(
            result.loc[index, "pvalue_two_sided"]
        )
    return result.sort_values(["comparison", "padj", "theme"]).reset_index(drop=True)


def draw_theme_panel(
    ax: plt.Axes,
    summary: pd.DataFrame,
    *,
    comparison: str,
    query_label: str,
    reference_label: str,
    title: str,
) -> None:
    selected = summary[summary["comparison"].eq(comparison)].copy()
    selected = selected.sort_values(
        ["query_fraction", "reference_fraction"], ascending=[True, True]
    ).reset_index(drop=True)
    y = np.arange(len(selected))
    query_color = GROUP_COLORS[query_label]
    reference_color = GROUP_COLORS[reference_label]
    for position, row in enumerate(selected.itertuples(index=False)):
        ax.plot(
            [row.reference_fraction, row.query_fraction],
            [position, position],
            color="#D8DDE3",
            linewidth=1.0,
            zorder=1,
        )
    ax.scatter(
        selected["reference_fraction"],
        y,
        s=30,
        color=reference_color,
        marker="s",
        clip_on=False,
        label=reference_label.capitalize(),
        zorder=2,
    )
    ax.scatter(
        selected["query_fraction"],
        y,
        s=34,
        color=query_color,
        marker="o",
        clip_on=False,
        label=query_label.capitalize(),
        zorder=3,
    )
    labels = [theme.replace("_", " ") for theme in selected["theme"]]
    labels = [
        f"{label}  q<0.05" if q < FDR_THRESHOLD else label
        for label, q in zip(labels, selected["padj"], strict=True)
    ]
    ax.set_yticks(y, labels)
    ax.set_xlim(0, max(0.05, float(selected[["query_fraction", "reference_fraction"]].max().max()) * 1.12))
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Targets annotated to functional theme")
    ax.set_title(title, loc="left")
    ax.grid(axis="x")
    ax.legend(frameon=False, loc="lower right", fontsize=7)
    # Fourteen category labels need a taller plotting box; the square-panel
    # convention yields here because squaring would collide the y labels.
    ax.set_box_aspect(1.15)


def plot_theme_composition(summary: pd.DataFrame) -> None:
    house_style()
    panels = {
        "a": lambda ax: draw_theme_panel(
            ax,
            summary,
            comparison="holdout_vs_training",
            query_label="holdout",
            reference_label="training",
            title="a  Holdouts versus training targets",
        ),
        "b": lambda ax: draw_theme_panel(
            ax,
            summary,
            comparison="responder_vs_nonresponder",
            query_label="responder",
            reference_label="non-responder",
            title="b  Responders versus non-responders",
        ),
    }
    plate(
        panels,
        OUTPUT_DIR,
        "fig_holdout_functional_theme_composition",
        panel_size=(5.7, 6.2),
        joint_size=(11.8, 6.2),
        concepts={
            "training targets": GROUP_COLORS["training"],
            "held-out targets": GROUP_COLORS["holdout"],
            "responding holdouts": GROUP_COLORS["responder"],
            "non-responding holdouts": GROUP_COLORS["non-responder"],
        },
    )


def markdown_table(frame: pd.DataFrame, columns: list[str], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in frame[columns].itertuples(index=False, name=None):
        values = []
        for value in row:
            if isinstance(value, float):
                values.append(f"{value:.3g}")
            else:
                values.append(str(value).replace("|", ", "))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_results(
    *,
    enrichment: pd.DataFrame,
    coverage: pd.DataFrame,
    themes: pd.DataFrame,
    holdout_annotations: pd.DataFrame,
    libraries: Mapping[str, Mapping[str, set[str]]],
) -> None:
    significant = enrichment[
        enrichment["padj"].lt(FDR_THRESHOLD)
        & enrichment["overlap_n"].ge(MIN_REPORTED_OVERLAP_N)
    ].copy()
    selection_significant = significant[
        significant["comparison"].isin(
            ["holdout_vs_training", "training_vs_holdout"]
        )
    ]
    response_significant = significant[
        significant["comparison"].isin(
            ["responder_vs_nonresponder", "nonresponder_vs_responder"]
        )
    ]

    sig_table = response_significant[
        [
            "comparison",
            "library",
            "term",
            "overlap_n",
            "query_fraction",
            "reference_fraction",
            "log2_odds_ratio_corrected",
            "padj",
            "overlap_genes",
        ]
    ].head(30)
    sig_md = (
        markdown_table(
            sig_table,
            list(sig_table.columns),
            [
                "Direction",
                "Library",
                "Term",
                "Hits",
                "Query fraction",
                "Reference fraction",
                "log2 OR",
                "FDR",
                "Genes",
            ],
        )
        if len(sig_table)
        else "No responder/non-responder term passed FDR <0.05."
    )

    coverage_display = coverage[
        coverage["comparison"].eq("holdout_vs_training")
    ][
        [
            "library",
            "query_annotated_n",
            "query_annotation_fraction",
            "universe_annotated_n",
            "universe_annotation_fraction",
            "tested_term_n",
        ]
    ].copy()
    coverage_md = markdown_table(
        coverage_display,
        list(coverage_display.columns),
        [
            "Library",
            "Annotated holdouts",
            "Holdout coverage",
            "Annotated screen",
            "Screen coverage",
            "Terms tested",
        ],
    )

    theme_display = themes[
        themes["comparison"].eq("responder_vs_nonresponder")
    ].sort_values("fraction_difference", ascending=False)[
        [
            "theme",
            "query_with_theme_n",
            "query_fraction",
            "reference_with_theme_n",
            "reference_fraction",
            "fraction_difference",
            "padj",
        ]
    ]
    theme_md = markdown_table(
        theme_display,
        list(theme_display.columns),
        [
            "Theme",
            "Responders",
            "Responder fraction",
            "Non-responders",
            "Non-responder fraction",
            "Difference",
            "FDR",
        ],
    )

    responder_nominal = enrichment[
        enrichment["comparison"].eq("responder_vs_nonresponder")
        & enrichment["overlap_n"].ge(MIN_REPORTED_OVERLAP_N)
    ].groupby("library", group_keys=False).head(3)
    responder_nominal_md = markdown_table(
        responder_nominal,
        ["library", "term", "overlap_n", "pvalue", "padj"],
        ["Library", "Leading responder term", "Hits", "Nominal P", "FDR"],
    )

    selection_counts = holdout_annotations["selection_stratum"].value_counts()
    no_effect_n = int(selection_counts.get("no_significant_effect selection", 0))
    other_n = int(selection_counts.get("other outcome-based selection", 0))
    library_lines = "\n".join(
        f"- {name}: {len(terms):,} parsed terms from `{LIBRARY_PATHS[name]}`"
        for name, terms in libraries.items()
    )

    selection_statement = (
        "No term passed FDR <0.05 in either direction for holdouts versus "
        "training targets."
        if selection_significant.empty
        else f"{len(selection_significant)} terms passed FDR <0.05 for the holdout/training comparison."
    )

    text = f"""# Functional characterization of the held-out targets

## Bottom line

The 272 held-out targets are **not detectably enriched or depleted for any GO,
Reactome, KEGG, or Hallmark term relative to the 1,674 training targets** after
within-library multiple-testing correction.  {selection_statement} This argues
against a large functional-class shift between the holdout and model-visible
target sets, although absence of enrichment is not proof that the split is
biologically exchangeable.

Within the holdouts, the principal corrected signal is that non-responders are
enriched for sequence-specific DNA-binding/transcription-regulatory molecular
functions and for the KEGG neuroactive ligand-receptor interaction pathway.
Responders have leading nominal signals in chromatin modification, WNT/cell
cycle, RNA metabolism, protein folding, cytoskeletal organization, and ubiquitin
ligase binding, but no responder-enriched term passes FDR <0.05.

## Benchmark composition

- Screen universe: 1,946 biological perturbation targets.
- Model-visible training/reference set: 1,674 targets.
- Held-out set: 272 targets; 100 responders and 172 non-responders in `151 TH
  Prkcd Grin2c Glut` cells.
- Holdout-selection registry: {no_effect_n} targets from the
  `no_significant_effect` selection and {other_n} from other outcome-based
  selection routes. `Safe_target_1` is excluded.

## Significant responder/non-responder terms

{sig_md}

The GO molecular-function rows are strongly overlapping ontology terms and
should be read as one transcription-factor/DNA-binding signal rather than as
independent discoveries.

## Functional-theme composition

The 14 themes use the repository's established pathway-name crosswalk across
all six libraries. They are overlapping descriptive categories, not a formal
GO-slim.

{theme_md}

![Functional-theme composition](fig_holdout_functional_theme_composition.png)

## Leading responder terms that did not survive correction

{responder_nominal_md}

## Annotation coverage

Enrichment backgrounds are restricted to screen targets annotated in each
library. Coverage differences are therefore visible rather than silently
treated as biological absence.

{coverage_md}

## Method

For holdout selection, each term was tested by one-sided hypergeometric
over-representation using the combined 1,946-target perturbation screen as the
universe. Responder/non-responder tests used only the 272 holdouts as the
universe. Terms required 3-500 annotated targets in the relevant universe;
Benjamini-Hochberg correction was applied over every eligible term within each
library and comparison. Gene symbols were upper-cased for matching. The
analysis is target-level and does not use the DEG identities produced by each
perturbation.

## Libraries

{library_lines}

The cached WikiPathways file in `data/external/enrichr/` is an HTTP 404 page and
was excluded rather than treated as an empty library.

## Interpretation limits

- The holdouts were outcome-selected, not randomly sampled. Their 100/172
  responder composition is part of the benchmark design.
- Responder status is post hoc experimental information, so its functional
  associations describe this assay and cell group; they are not prediction-time
  features or causal explanations of responsiveness.
- GO terms are hierarchical and redundant. Library ages range from 2019 to
  2023, and symbol-based mouse/human orthology coverage is incomplete.
- Failure to reject enrichment does not demonstrate equivalence between
  holdouts and training targets.

## Files

- `term_enrichment_all.csv`: every tested term and corrected result.
- `term_enrichment_top.csv`: the top 20 terms per comparison and library.
- `significant_terms.csv`: terms passing FDR <0.05 with at least three hits.
- `library_coverage.csv`: annotation coverage and tested-term counts.
- `holdout_target_annotations.csv`: per-holdout response, selection route,
  library annotation counts, and functional themes.
- `functional_theme_summary.csv`: theme prevalences, odds ratios, and FDR.
- `fig_holdout_functional_theme_composition*.{{png,svg}}`: standalone panels
  and joint plate.
"""
    (OUTPUT_DIR / "RESULTS.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    holdout_counts = load_counts(HOLDOUT_COUNTS_CSV, 272)
    training_counts = load_counts(TRAINING_COUNTS_CSV, 1_674)
    if set(holdout_counts["gene_upper"]) & set(training_counts["gene_upper"]):
        raise ValueError("Holdout and training target sets overlap")

    libraries = {name: load_gmt(path) for name, path in LIBRARY_PATHS.items()}
    training = set(training_counts["gene_upper"])
    holdout = set(holdout_counts["gene_upper"])
    responders = set(holdout_counts.loc[holdout_counts["n_degs"].gt(0), "gene_upper"])
    nonresponders = set(
        holdout_counts.loc[holdout_counts["n_degs"].eq(0), "gene_upper"]
    )
    if len(responders) != 100 or len(nonresponders) != 172:
        raise ValueError("Unexpected Task-1 responder composition")

    enrichment, coverage = run_term_enrichment(
        libraries,
        training=training,
        holdout=holdout,
        responders=responders,
        nonresponders=nonresponders,
    )
    significant = enrichment[
        enrichment["padj"].lt(FDR_THRESHOLD)
        & enrichment["overlap_n"].ge(MIN_REPORTED_OVERLAP_N)
    ].copy()
    top = (
        enrichment[enrichment["overlap_n"].ge(MIN_REPORTED_OVERLAP_N)]
        .groupby(["comparison", "library"], group_keys=False)
        .head(20)
        .reset_index(drop=True)
    )

    annotations = build_gene_annotations(libraries, holdout_counts, training_counts)
    holdout_annotations = attach_holdout_selection(
        annotations[annotations["benchmark_group"].eq("holdout")].copy()
    )
    themes = summarize_themes(annotations)

    enrichment.to_csv(OUTPUT_DIR / "term_enrichment_all.csv", index=False)
    top.to_csv(OUTPUT_DIR / "term_enrichment_top.csv", index=False)
    significant.to_csv(OUTPUT_DIR / "significant_terms.csv", index=False)
    coverage.to_csv(OUTPUT_DIR / "library_coverage.csv", index=False)
    holdout_annotations.to_csv(
        OUTPUT_DIR / "holdout_target_annotations.csv", index=False
    )
    themes.to_csv(OUTPUT_DIR / "functional_theme_summary.csv", index=False)
    plot_theme_composition(themes)
    write_results(
        enrichment=enrichment,
        coverage=coverage,
        themes=themes,
        holdout_annotations=holdout_annotations,
        libraries=libraries,
    )

    metadata = {
        "analysis": "Task-1 holdout functional characterization",
        "screen_target_n": len(training | holdout),
        "training_target_n": len(training),
        "holdout_target_n": len(holdout),
        "responder_n": len(responders),
        "nonresponder_n": len(nonresponders),
        "term_filters": {
            "minimum_background_genes": MIN_TERM_BACKGROUND_N,
            "maximum_background_genes": MAX_TERM_BACKGROUND_N,
            "minimum_reported_overlap": MIN_REPORTED_OVERLAP_N,
            "fdr_threshold": FDR_THRESHOLD,
        },
        "multiple_testing": "Benjamini-Hochberg within library and comparison",
        "libraries": {
            name: {"path": str(LIBRARY_PATHS[name]), "parsed_term_n": len(terms)}
            for name, terms in libraries.items()
        },
    }
    (OUTPUT_DIR / "analysis_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Wrote holdout functional characterization to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
