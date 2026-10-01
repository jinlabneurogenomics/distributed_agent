"""Compact, generated descriptions of measurements available to query agents."""

from __future__ import annotations

from pathlib import Path
from typing import Any


REGISTRY_SCHEMA = "distributed_agents-measurement-registry-v1"
DE_COLUMNS = {
    "names",
    "group_name",
    "gene_target",
    "logfoldchanges",
    "pvals",
    "pvals_adj",
    "scores",
}


def _parquet_columns(path: Path) -> tuple[list[str], int | None, str | None]:
    try:
        import pyarrow.parquet as pq

        metadata = pq.read_metadata(path)
        return list(metadata.schema.names), metadata.num_rows, None
    except Exception as exc:  # pragma: no cover - exercised by missing/corrupt inputs
        return [], None, f"{type(exc).__name__}: {exc}"


def _parquet_entry(path: Path) -> dict[str, Any]:
    columns, rows, error = _parquet_columns(path)
    column_set = set(columns)
    entry: dict[str, Any] = {
        "source": str(path),
        "format": "parquet",
        "columns": columns,
        "row_count": rows,
        "schema_status": "readable" if error is None else "unavailable",
    }
    if error is not None:
        entry["schema_error"] = error
        entry["representation"] = "unknown"
        return entry

    if DE_COLUMNS.issubset(column_set):
        direct = [
            "gene-specific relative-expression contrast among recovered nuclei",
            "gene-specific Wilcoxon statistic and significance",
        ]
        if {"n_pert_matched", "n_ctrl_matched"}.issubset(column_set):
            direct.append("matched recovered-nucleus counts")
        entry.update(
            {
                "representation": "perturbation differential-expression summary",
                "observational_unit": (
                    "measured gene x neuronal class x perturbation contrast"
                ),
                "direct_measurements": direct,
                "not_directly_observed": [
                    "raw per-nucleus total UMI",
                    "absolute RNA content",
                    "guide-exposure denominator",
                    "pre-assay perturbation-induced depletion or survival",
                ],
                "selection_condition": "recovered, assayed, class-assigned nuclei",
                "guards": [
                    "normalized DE is compositional and is not absolute RNA content",
                    "recovered-nucleus counts are not guide-exposure denominators",
                    "survivor-state transcription is not a depletion measurement",
                ],
            }
        )
    else:
        entry.update(
            {
                "representation": "tabular input with no registered semantics",
                "observational_unit": "unknown",
                "direct_measurements": [],
                "not_directly_observed": [],
                "guards": [
                    "inspect provenance before assigning a measurement role"
                ],
            }
        )
    return entry


def build_measurement_registry(input_roots: tuple[Path, ...]) -> dict[str, Any]:
    """Describe mounted inputs without deciding their relevance to a task endpoint."""

    sources = [
        _parquet_entry(path.resolve())
        for path in input_roots
        if path.is_file() and path.suffix.casefold() == ".parquet"
    ]
    return {
        "schema_version": REGISTRY_SCHEMA,
        "purpose": (
            "Describe what mounted inputs measure; the task decides endpoint "
            "alignment and evidence order."
        ),
        "sources": sources,
        "same_experiment_surfaces": {
            "corpus_role": "packaged interpretation and semantic context",
            "measurement_status": "not independent replication",
        },
        "task_alignment": (
            "For the requested endpoint, label each source direct, validated proxy, "
            "context only, or absent before selecting candidates. Absence of the "
            "outcome may be the intended setup for a predictive task."
        ),
    }
