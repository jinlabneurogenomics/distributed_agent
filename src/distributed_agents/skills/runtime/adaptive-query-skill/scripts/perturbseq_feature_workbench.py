#!/usr/bin/env python3
"""Build, calibrate, rank, and validate generic Perturb-seq features.

The workbench deliberately accepts only declared differential-expression
tables and supplied rank bindings. It never reads graph or corpus fields. The
expensive command is ``summarize``; its compact output is cached and every
later operation works from that materialized feature table.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import random
import re
import statistics
import time
from pathlib import Path
from typing import Any, Mapping, Sequence


SUMMARY_SCHEMA = "distributed_agents-perturbseq-feature-summary-v2"
CALIBRATION_SCHEMA = "distributed_agents-perturbseq-feature-calibration-v1"
ORDERING_VALIDATION_SCHEMA = "distributed_agents-ordering-validation-v1"
FORBIDDEN_FEATURE = re.compile(
    r"(?:graph|edge|degree|path|lane|reciprocal|shared.?term|relation.?count)",
    flags=re.IGNORECASE,
)
NON_MODEL_FEATURES = {
    "n_rows",
    "n_measured_genes",
    "n_cell_types",
    "n_logfoldchange_missing",
    "n_wilcoxon_score_missing",
    "n_adjusted_pvalue_missing",
    "n_significance_missing",
}
ANSWER_TSV = re.compile(r"```tsv\s*\n(?P<body>.*?)```", re.I | re.S)

DEFAULT_COLUMN_ROLES = {
    "measured_gene": "names",
    "cell_type": "group_name",
    "gene_target": "gene_target",
    "logfoldchange": "logfoldchanges",
    "wilcoxon_score": "scores",
    "pvalue": "pvals",
    "adjusted_pvalue": "pvals_adj",
    "significant_fdr_010": "significant_adj_0_1",
}
IDENTITY_COLUMN_ROLES = ("measured_gene", "cell_type", "gene_target")
MEASUREMENT_COLUMN_ROLES = (
    "logfoldchange",
    "wilcoxon_score",
    "pvalue",
    "adjusted_pvalue",
    "significant_fdr_010",
)


def _json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _sha256_json(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _percentile(values: Sequence[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = fraction * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def _rank_values(values: Sequence[float]) -> list[float]:
    ordered = sorted(range(len(values)), key=lambda index: values[index])
    result = [0.0] * len(values)
    start = 0
    while start < len(ordered):
        end = start + 1
        while end < len(ordered) and values[ordered[end]] == values[ordered[start]]:
            end += 1
        average = (start + 1 + end) / 2
        for index in ordered[start:end]:
            result[index] = average
        start = end
    return result


def _correlation(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        return 0.0
    left_mean = statistics.fmean(left)
    right_mean = statistics.fmean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_norm = math.sqrt(sum((value - left_mean) ** 2 for value in left))
    right_norm = math.sqrt(sum((value - right_mean) ** 2 for value in right))
    denominator = left_norm * right_norm
    return numerator / denominator if denominator else 0.0


def _spearman(left: Sequence[float], right: Sequence[float]) -> float:
    return _correlation(_rank_values(left), _rank_values(right))


def _standard_error(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values) / math.sqrt(len(values))


def _dataset_identity(path: Path) -> dict[str, Any]:
    import pyarrow.parquet as pq

    resolved = path.expanduser().resolve()
    metadata = pq.ParquetFile(resolved)
    stat = resolved.stat()
    identity = {
        "path": str(resolved),
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "row_count": metadata.metadata.num_rows,
        "row_group_count": metadata.metadata.num_row_groups,
        "columns": metadata.schema_arrow.names,
        "schema": str(metadata.schema_arrow),
    }
    return {
        **identity,
        "metadata_sha256": _sha256_json(identity),
        "fingerprint_kind": "path-size-mtime-parquet-metadata",
    }


def _read_values_file(path: Path, column: str) -> list[str]:
    suffix = path.suffix.casefold()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            values = payload
        elif isinstance(payload, dict):
            values = next(
                (
                    payload[key]
                    for key in (column, "gene_targets", "targets", "cell_types")
                    if isinstance(payload.get(key), list)
                ),
                [],
            )
        else:
            values = []
        return [str(value).strip() for value in values if str(value).strip()]
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if not reader.fieldnames:
                return []
            selected = column if column in reader.fieldnames else reader.fieldnames[0]
            return [
                str(row.get(selected) or "").strip()
                for row in reader
                if str(row.get(selected) or "").strip()
            ]
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _binding_values(path: Path, role: str | None) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    sets = [
        row
        for row in payload.get("entity_sets", [])
        if isinstance(row, dict)
        and row.get("active_for_coverage")
        and row.get("entity_type") == "gene"
    ]
    if role:
        sets = [row for row in sets if row.get("role") == role]
    return list(
        dict.fromkeys(
            str(item.get("canonical") or "").strip()
            for row in sets
            for item in row.get("items", [])
            if isinstance(item, dict) and str(item.get("canonical") or "").strip()
        )
    )


def _combined_values(
    direct: Sequence[str],
    file_path: Path | None,
    column: str,
    bindings_path: Path | None = None,
    bindings_role: str | None = None,
) -> list[str]:
    values = [str(value).strip() for value in direct if str(value).strip()]
    if file_path is not None:
        values.extend(_read_values_file(file_path, column))
    if bindings_path is not None:
        values.extend(_binding_values(bindings_path, bindings_role))
    return sorted(set(values), key=str.casefold)


def _quote_identifier(value: str) -> str:
    """Return one safely quoted DuckDB identifier."""

    return '"' + value.replace('"', '""') + '"'


def _resolve_column_roles(
    columns: Sequence[str],
    overrides: Mapping[str, str] | None,
) -> dict[str, str]:
    configured = dict(DEFAULT_COLUMN_ROLES)
    if overrides:
        unknown = sorted(set(overrides) - set(DEFAULT_COLUMN_ROLES))
        if unknown:
            raise ValueError("unknown column roles: " + ", ".join(unknown))
        configured.update(
            {
                role: str(column).strip()
                for role, column in overrides.items()
                if str(column).strip()
            }
        )
    available = set(columns)
    missing_identity = [
        configured[role]
        for role in IDENTITY_COLUMN_ROLES
        if configured[role] not in available
    ]
    if missing_identity:
        raise ValueError(
            "Perturb-seq parquet is missing identity columns: "
            + ", ".join(sorted(missing_identity))
        )
    resolved = {
        role: column for role, column in configured.items() if column in available
    }
    if not any(role in resolved for role in MEASUREMENT_COLUMN_ROLES):
        expected = ", ".join(configured[role] for role in MEASUREMENT_COLUMN_ROLES)
        raise ValueError(
            "Perturb-seq parquet has no supported measurement columns; expected at "
            f"least one of: {expected}"
        )
    return resolved


def _feature_family_status(
    column_roles: Mapping[str, str],
) -> tuple[list[str], list[str]]:
    available: list[str] = []
    unavailable: list[str] = []
    for role, family in (
        ("logfoldchange", "logfoldchange_distributions"),
        ("wilcoxon_score", "wilcoxon_score_distributions"),
        ("pvalue", "raw_pvalue_minimum"),
        ("adjusted_pvalue", "continuous_adjusted_pvalue"),
    ):
        (available if role in column_roles else unavailable).append(family)
    if "adjusted_pvalue" in column_roles:
        available.append("fdr_001_005_010_burden")
    elif "significant_fdr_010" in column_roles:
        available.append("binary_fdr_010_burden")
        unavailable.append("fdr_001_005_burden")
    else:
        unavailable.extend(("fdr_001_005_010_burden", "binary_fdr_010_burden"))
    return available, unavailable


def _summary_query(
    *,
    level: str,
    targets: Sequence[str],
    cell_types: Sequence[str],
    include_controls: bool,
    column_roles: Mapping[str, str],
) -> tuple[str, list[str]]:
    target_column = _quote_identifier(column_roles["gene_target"])
    cell_column = _quote_identifier(column_roles["cell_type"])
    measured_column = _quote_identifier(column_roles["measured_gene"])
    where = [
        f"{target_column} IS NOT NULL",
        f"{cell_column} IS NOT NULL",
        f"{measured_column} IS NOT NULL",
    ]
    params: list[str] = []
    if not include_controls:
        where.extend(
            [
                f"{target_column} <> 'Non_target'",
                f"NOT starts_with({target_column}, 'Safe_target_')",
            ]
        )
    if targets:
        where.append(target_column + " IN (" + ",".join("?" for _ in targets) + ")")
        params.extend(targets)
    if cell_types:
        where.append(cell_column + " IN (" + ",".join("?" for _ in cell_types) + ")")
        params.extend(cell_types)
    group_columns = (
        "gene_target, group_name" if level == "target_cell" else "gene_target"
    )
    select_group = (
        "gene_target, group_name," if level == "target_cell" else "gene_target,"
    )
    order_columns = group_columns

    filtered_columns = [
        f"{target_column}::VARCHAR AS gene_target",
        f"{cell_column}::VARCHAR AS group_name",
        f"{measured_column}::VARCHAR AS measured_gene",
    ]
    optional_casts = {
        "logfoldchange": ("lfc", "DOUBLE"),
        "wilcoxon_score": ("wilcoxon_score", "DOUBLE"),
        "pvalue": ("pvalue", "DOUBLE"),
        "adjusted_pvalue": ("adjusted_pvalue", "DOUBLE"),
        "significant_fdr_010": ("significant_fdr_010", "BOOLEAN"),
    }
    for role, (alias, kind) in optional_casts.items():
        if role in column_roles:
            filtered_columns.append(
                f"try_cast({_quote_identifier(column_roles[role])} AS {kind}) AS {alias}"
            )

    aggregate_columns = [
        "count(*)::BIGINT AS n_rows",
        "count(DISTINCT measured_gene)::BIGINT AS n_measured_genes",
        "count(DISTINCT group_name)::BIGINT AS n_cell_types",
    ]
    if "logfoldchange" in column_roles:
        aggregate_columns.extend(
            [
                "sum(CASE WHEN lfc IS NULL THEN 1 ELSE 0 END)::BIGINT AS n_logfoldchange_missing",
                "avg(lfc) AS mean_logfoldchange",
                "median(lfc) AS median_logfoldchange",
                "avg(abs(lfc)) AS mean_abs_logfoldchange",
                "median(abs(lfc)) AS median_abs_logfoldchange",
                "quantile_cont(abs(lfc), 0.90) AS q90_abs_logfoldchange",
                "quantile_cont(abs(lfc), 0.95) AS q95_abs_logfoldchange",
                "max(abs(lfc)) AS max_abs_logfoldchange",
                "avg(CASE WHEN lfc > 0 THEN 1.0 ELSE 0.0 END) AS positive_logfoldchange_fraction",
                "avg(CASE WHEN lower(measured_gene) <> lower(gene_target) THEN lfc END) AS mean_trans_logfoldchange",
                "median(CASE WHEN lower(measured_gene) <> lower(gene_target) THEN abs(lfc) END) AS median_trans_abs_logfoldchange",
            ]
        )
    if "wilcoxon_score" in column_roles:
        aggregate_columns.extend(
            [
                "sum(CASE WHEN wilcoxon_score IS NULL THEN 1 ELSE 0 END)::BIGINT AS n_wilcoxon_score_missing",
                "avg(wilcoxon_score) AS mean_wilcoxon_score",
                "median(wilcoxon_score) AS median_wilcoxon_score",
                "avg(abs(wilcoxon_score)) AS mean_abs_wilcoxon_score",
                "median(abs(wilcoxon_score)) AS median_abs_wilcoxon_score",
                "quantile_cont(abs(wilcoxon_score), 0.90) AS q90_abs_wilcoxon_score",
                "quantile_cont(abs(wilcoxon_score), 0.95) AS q95_abs_wilcoxon_score",
                "max(abs(wilcoxon_score)) AS max_abs_wilcoxon_score",
                "avg(CASE WHEN lower(measured_gene) <> lower(gene_target) THEN wilcoxon_score END) AS mean_trans_wilcoxon_score",
            ]
        )
    if "adjusted_pvalue" in column_roles:
        fdr_condition = "adjusted_pvalue < 0.10"
        aggregate_columns.extend(
            [
                "sum(CASE WHEN adjusted_pvalue IS NULL THEN 1 ELSE 0 END)::BIGINT AS n_adjusted_pvalue_missing",
                "sum(CASE WHEN adjusted_pvalue < 0.01 THEN 1 ELSE 0 END)::BIGINT AS n_fdr_001",
                "sum(CASE WHEN adjusted_pvalue < 0.05 THEN 1 ELSE 0 END)::BIGINT AS n_fdr_005",
                "min(adjusted_pvalue) AS min_adjusted_pvalue",
            ]
        )
    elif "significant_fdr_010" in column_roles:
        fdr_condition = "significant_fdr_010 IS TRUE"
        aggregate_columns.append(
            "sum(CASE WHEN significant_fdr_010 IS NULL THEN 1 ELSE 0 END)::BIGINT AS n_significance_missing"
        )
    else:
        fdr_condition = None
    if fdr_condition:
        aggregate_columns.extend(
            [
                f"sum(CASE WHEN {fdr_condition} THEN 1 ELSE 0 END)::BIGINT AS n_fdr_010",
                f"avg(CASE WHEN {fdr_condition} THEN 1.0 ELSE 0.0 END) AS fraction_fdr_010",
                f"sum(CASE WHEN {fdr_condition} AND lower(measured_gene) <> lower(gene_target) THEN 1 ELSE 0 END)::BIGINT AS n_trans_fdr_010",
            ]
        )
        if "logfoldchange" in column_roles:
            aggregate_columns.extend(
                [
                    f"sum(CASE WHEN {fdr_condition} AND lfc > 0 THEN 1 ELSE 0 END)::BIGINT AS n_up_fdr_010",
                    f"sum(CASE WHEN {fdr_condition} AND lfc < 0 THEN 1 ELSE 0 END)::BIGINT AS n_down_fdr_010",
                ]
            )
    if "pvalue" in column_roles:
        aggregate_columns.append("min(pvalue) AS min_pvalue")

    filtered_sql = ",\n            ".join(filtered_columns)
    aggregate_sql = ",\n          ".join(aggregate_columns)
    sql = f"""
        WITH filtered AS (
          SELECT
            {filtered_sql}
          FROM read_parquet(?)
          WHERE {" AND ".join(where)}
        )
        SELECT
          {select_group}
          {aggregate_sql}
        FROM filtered
        GROUP BY {group_columns}
        ORDER BY {order_columns}
    """
    return sql, params


def _write_arrow_table(table: Any, path: Path) -> None:
    import pyarrow.csv as pacsv
    import pyarrow.parquet as pq

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    suffix = path.suffix.casefold()
    if suffix == ".parquet":
        pq.write_table(table, temporary, compression="zstd")
    elif suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        pacsv.write_csv(
            table,
            temporary,
            write_options=pacsv.WriteOptions(delimiter=delimiter),
        )
    else:
        raise ValueError("feature output must end in .parquet, .csv, or .tsv")
    temporary.replace(path)


def summarize_features(
    *,
    parquet_path: Path,
    level: str,
    cache_dir: Path,
    output_path: Path | None,
    targets: Sequence[str],
    cell_types: Sequence[str],
    include_controls: bool,
    force: bool,
    column_roles: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    import duckdb

    call_started = time.monotonic()
    if level not in {"target", "target_cell"}:
        raise ValueError("level must be 'target' or 'target_cell'")
    identity = _dataset_identity(parquet_path)
    resolved_roles = _resolve_column_roles(identity["columns"], column_roles)
    available_families, unavailable_families = _feature_family_status(resolved_roles)
    specification = {
        "schema_version": SUMMARY_SCHEMA,
        "dataset_metadata_sha256": identity["metadata_sha256"],
        "level": level,
        "targets": list(targets),
        "cell_types": list(cell_types),
        "include_controls": include_controls,
        "column_roles": resolved_roles,
    }
    cache_key = _sha256_json(specification)
    output = (
        output_path.expanduser().resolve()
        if output_path is not None
        else (cache_dir.expanduser().resolve() / f"features-{cache_key[:20]}.parquet")
    )
    manifest_path = output.with_suffix(output.suffix + ".manifest.json")
    if not force and output.is_file() and manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("cache_key") == cache_key:
            return {
                **manifest,
                "cache_hit": True,
                "cache_lookup_duration_s": round(time.monotonic() - call_started, 3),
            }

    started = time.monotonic()
    sql, params = _summary_query(
        level=level,
        targets=targets,
        cell_types=cell_types,
        include_controls=include_controls,
        column_roles=resolved_roles,
    )
    connection = duckdb.connect()
    try:
        table = connection.execute(
            sql,
            [str(parquet_path.expanduser().resolve()), *params],
        ).to_arrow_table()
    finally:
        connection.close()
    if table.num_rows == 0:
        raise ValueError("filters selected no Perturb-seq rows")
    _write_arrow_table(table, output)
    selected_rows = sum(int(value or 0) for value in table["n_rows"].to_pylist())
    manifest = {
        "schema_version": SUMMARY_SCHEMA,
        "status": "passed",
        "cache_key": cache_key,
        "cache_hit": False,
        "dataset": identity,
        "filters": {
            "targets": list(targets),
            "cell_types": list(cell_types),
            "include_controls": include_controls,
        },
        "aggregation_level": level,
        "column_roles": resolved_roles,
        "available_feature_families": available_families,
        "unavailable_feature_families": unavailable_families,
        "feature_table": str(output),
        "feature_table_format": output.suffix.casefold().lstrip("."),
        "feature_columns": table.column_names,
        "output_rows": table.num_rows,
        "output_bytes": output.stat().st_size,
        "selected_source_rows": selected_rows,
        "source_rows": identity["row_count"],
        "duration_s": round(time.monotonic() - started, 3),
        "graph_fields_present": False,
        "interpretation": (
            "Task-general differential-expression summaries. Feature alignment with "
            "supplied ranks must be calibrated separately; no feature is inherently "
            "a proxy for an unobserved biological endpoint."
        ),
    }
    _json_dump(manifest_path, manifest)
    return manifest


def _load_feature_rows(
    path: Path,
    gene_column: str,
    requested_features: Sequence[str],
) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    import pyarrow as pa
    import pyarrow.csv as pacsv
    import pyarrow.parquet as pq

    suffix = path.suffix.casefold()
    if suffix == ".parquet":
        table = pq.read_table(path)
    elif suffix in {".csv", ".tsv"}:
        parse_options = pacsv.ParseOptions(delimiter="\t" if suffix == ".tsv" else ",")
        table = pacsv.read_csv(path, parse_options=parse_options)
    else:
        raise ValueError("feature input must end in .parquet, .csv, or .tsv")
    if gene_column not in table.column_names:
        raise ValueError(f"feature table requires {gene_column!r}")
    duplicate_columns = [name for name in table.column_names if name == gene_column]
    if len(duplicate_columns) != 1:
        raise ValueError(f"feature table contains duplicate {gene_column!r} columns")
    schema_fields = {field.name: field for field in table.schema}
    if requested_features:
        missing = [name for name in requested_features if name not in schema_fields]
        if missing:
            raise ValueError("requested features are absent: " + ", ".join(missing))
        feature_names = list(dict.fromkeys(requested_features))
    else:
        feature_names = [
            name
            for name, field in schema_fields.items()
            if name != gene_column
            and name not in NON_MODEL_FEATURES
            and not name.endswith("_missing")
            and not FORBIDDEN_FEATURE.search(name)
            and (
                pa.types.is_integer(field.type)
                or pa.types.is_floating(field.type)
                or pa.types.is_decimal(field.type)
            )
        ]
    forbidden = [name for name in feature_names if FORBIDDEN_FEATURE.search(name)]
    if forbidden:
        raise ValueError(
            "graph-derived features are forbidden: " + ", ".join(forbidden)
        )
    if not feature_names:
        raise ValueError("no numeric non-graph feature columns were selected")
    raw_rows = table.select([gene_column, *feature_names]).to_pylist()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_rows:
        gene = str(raw.get(gene_column) or "").strip()
        if not gene:
            continue
        key = gene.casefold()
        if key in seen:
            raise ValueError(
                "feature table has multiple rows per gene_target; calibrate a "
                "target-level summary or filter to one cell type"
            )
        seen.add(key)
        values: dict[str, float | None] = {}
        for name in feature_names:
            value = raw.get(name)
            try:
                parsed = float(value) if value is not None else None
            except (TypeError, ValueError):
                parsed = None
            values[name] = (
                parsed if parsed is not None and math.isfinite(parsed) else None
            )
        rows.append({"gene_target": gene, "values": values})
    if len(rows) < 6:
        raise ValueError("feature table has fewer than six unique targets")

    diagnostics: list[dict[str, Any]] = []
    usable: list[str] = []
    for name in feature_names:
        observed = [
            row["values"][name] for row in rows if row["values"][name] is not None
        ]
        if not observed:
            diagnostics.append(
                {
                    "feature": name,
                    "observed": 0,
                    "missing": len(rows),
                    "missing_fraction": 1.0,
                    "status": "excluded_all_missing",
                }
            )
            continue
        median = statistics.median(observed)
        mean = statistics.fmean(observed)
        variance = statistics.fmean((value - mean) ** 2 for value in observed)
        scale = math.sqrt(variance)
        diagnostics.append(
            {
                "feature": name,
                "observed": len(observed),
                "missing": len(rows) - len(observed),
                "missing_fraction": (len(rows) - len(observed)) / len(rows),
                "imputation": "universe_median",
                "imputation_value": median,
                "mean": mean,
                "scale": scale,
                "status": "usable" if scale else "excluded_constant",
            }
        )
        if not scale:
            continue
        usable.append(name)
        for row in rows:
            value = row["values"][name]
            row["values"][name] = ((median if value is None else value) - mean) / scale
    if not usable:
        raise ValueError("all selected features are constant or missing")
    return usable, rows, diagnostics


def _visible_examples(
    bindings_path: Path,
    role: str | None,
) -> tuple[list[dict[str, Any]], str]:
    payload = json.loads(bindings_path.read_text(encoding="utf-8"))
    sets = [
        row
        for row in payload.get("entity_sets", [])
        if isinstance(row, dict)
        and row.get("active_for_coverage")
        and (row.get("ordering") or {}).get("kind") in {"ranked", "partial_ranked"}
    ]
    if role:
        sets = [row for row in sets if row.get("role") == role]
    elif sets:
        preferred = [
            row for row in sets if row.get("role") == "supplied_ranked_examples"
        ]
        sets = preferred or sets[:1]
    if not sets:
        raise ValueError(
            "task bindings contain no active ranked or partial-ranked gene set"
        )
    selected = sets[0]
    examples = []
    seen: set[str] = set()
    for item in selected.get("items", []):
        if not isinstance(item, dict):
            continue
        gene = str(item.get("canonical") or "").strip()
        rank = item.get("rank")
        if not gene or not isinstance(rank, int) or gene.casefold() in seen:
            continue
        seen.add(gene.casefold())
        examples.append({"gene_target": gene, "rank": rank})
    examples.sort(key=lambda row: (row["rank"], row["gene_target"].casefold()))
    if len(examples) < 6:
        raise ValueError("at least six ranked visible examples are required")
    return examples, str((selected.get("ordering") or {}).get("kind"))


def _stratified_folds(
    examples: Sequence[dict[str, Any]],
    fold_count: int,
) -> list[list[dict[str, Any]]]:
    count = max(2, min(fold_count, len(examples) // 2))
    folds: list[list[dict[str, Any]]] = [[] for _ in range(count)]
    ordered = sorted(examples, key=lambda row: (row["rank"], row["gene_target"]))
    for index, row in enumerate(ordered):
        folds[index % count].append(row)
    return [fold for fold in folds if fold]


def _models(
    feature_names: Sequence[str],
    rows: Sequence[dict[str, Any]],
    correlation_limit: float,
    max_ensembles: int,
) -> tuple[list[tuple[str, ...]], dict[str, Any]]:
    singles = [(name,) for name in feature_names]
    pairs: list[tuple[float, tuple[str, str]]] = []
    excluded_correlated = 0
    for left, right in itertools.combinations(feature_names, 2):
        correlation = abs(
            _correlation(
                [float(row["values"][left]) for row in rows],
                [float(row["values"][right]) for row in rows],
            )
        )
        if correlation >= correlation_limit:
            excluded_correlated += 1
            continue
        pairs.append((correlation, (left, right)))
    pairs.sort(key=lambda item: (item[0], item[1]))
    selected_pairs = [model for _, model in pairs[:max_ensembles]]
    return [*singles, *selected_pairs], {
        "single_feature_models": len(singles),
        "pair_models": len(selected_pairs),
        "pair_models_truncated": max(0, len(pairs) - len(selected_pairs)),
        "correlated_pairs_excluded": excluded_correlated,
        "pair_correlation_limit": correlation_limit,
    }


def _fit_model(
    model: tuple[str, ...],
    training: Sequence[dict[str, Any]],
    row_by_gene: dict[str, dict[str, Any]],
) -> tuple[dict[str, float], dict[str, float]]:
    outcome = [-float(row["rank"]) for row in training]
    correlations = {
        name: _spearman(
            [
                float(row_by_gene[row["gene_target"].casefold()]["values"][name])
                for row in training
            ],
            outcome,
        )
        for name in model
    }
    if len(model) == 1:
        name = model[0]
        weights = {name: 1.0 if correlations[name] >= 0 else -1.0}
    else:
        norm = sum(abs(value) for value in correlations.values())
        if norm:
            weights = {name: value / norm for name, value in correlations.items()}
        else:
            weights = {name: 1.0 / len(model) for name in model}
    return weights, correlations


def _score_row(row: dict[str, Any], weights: dict[str, float]) -> float:
    return sum(float(row["values"][name]) * weight for name, weight in weights.items())


def _evaluate(
    *,
    model: tuple[str, ...],
    training: Sequence[dict[str, Any]],
    heldout: Sequence[dict[str, Any]],
    rows: Sequence[dict[str, Any]],
    row_by_gene: dict[str, dict[str, Any]],
    top_ks: Sequence[int],
) -> tuple[list[dict[str, Any]], dict[str, float], dict[str, float]]:
    weights, correlations = _fit_model(model, training, row_by_gene)
    training_keys = {row["gene_target"].casefold() for row in training}
    scored = [
        (_score_row(row, weights), row["gene_target"])
        for row in rows
        if row["gene_target"].casefold() not in training_keys
    ]
    predictions = []
    for example in heldout:
        key = example["gene_target"].casefold()
        heldout_score = _score_row(row_by_gene[key], weights)
        rank = 1 + sum(
            score > heldout_score or (score == heldout_score and gene.casefold() < key)
            for score, gene in scored
            if gene.casefold() != key
        )
        percentile = 1.0 - (rank - 1) / max(1, len(scored) - 1)
        expected_percentile = max(
            0.0,
            min(
                1.0,
                1.0 - (float(example["rank"]) - 1.0) / max(1, len(scored) - 1),
            ),
        )
        predictions.append(
            {
                "gene_target": example["gene_target"],
                "supplied_rank": example["rank"],
                "universe_rank": rank,
                "top_percentile": percentile,
                "expected_percentile_from_supplied_rank": expected_percentile,
                "underprediction_gap": expected_percentile - percentile,
                "rank_deficit": rank - int(example["rank"]),
                **{f"hit_at_{value}": rank <= value for value in top_ks},
            }
        )
    return predictions, weights, correlations


def _candidate_cv(
    *,
    models: Sequence[tuple[str, ...]],
    examples: Sequence[dict[str, Any]],
    rows: Sequence[dict[str, Any]],
    row_by_gene: dict[str, dict[str, Any]],
    fold_count: int,
    top_ks: Sequence[int],
) -> list[dict[str, Any]]:
    folds = _stratified_folds(examples, fold_count)
    diagnostics = []
    for model in models:
        fold_means: list[float] = []
        predictions: list[dict[str, Any]] = []
        for heldout in folds:
            heldout_keys = {row["gene_target"].casefold() for row in heldout}
            training = [
                row
                for row in examples
                if row["gene_target"].casefold() not in heldout_keys
            ]
            result, _, _ = _evaluate(
                model=model,
                training=training,
                heldout=heldout,
                rows=rows,
                row_by_gene=row_by_gene,
                top_ks=top_ks,
            )
            predictions.extend(result)
            fold_means.append(statistics.fmean(row["top_percentile"] for row in result))
        diagnostics.append(
            {
                "model": "+".join(model),
                "features": list(model),
                "complexity": len(model),
                "mean_top_percentile": statistics.fmean(fold_means),
                "standard_error": _standard_error(fold_means),
                "fold_scores": fold_means,
                **{
                    f"recall_at_{value}": sum(
                        row[f"hit_at_{value}"] for row in predictions
                    )
                    / len(predictions)
                    for value in top_ks
                },
            }
        )
    return diagnostics


def _one_se_select(diagnostics: Sequence[dict[str, Any]]) -> dict[str, Any]:
    best = max(
        diagnostics,
        key=lambda row: (row["mean_top_percentile"], -row["complexity"], row["model"]),
    )
    threshold = best["mean_top_percentile"] - best["standard_error"]
    eligible = [row for row in diagnostics if row["mean_top_percentile"] >= threshold]
    selected = min(
        eligible,
        key=lambda row: (row["complexity"], -row["mean_top_percentile"], row["model"]),
    )
    return {
        **selected,
        "best_model": best["model"],
        "best_mean_top_percentile": best["mean_top_percentile"],
        "one_standard_error_threshold": threshold,
        "eligible_model_count": len(eligible),
        "simplicity_rule_changed_choice": selected["model"] != best["model"],
    }


def _average_precision(ranked: Sequence[str], relevant: set[str]) -> float:
    if not relevant:
        return 0.0
    hits = 0
    total = 0.0
    for index, gene in enumerate(ranked, 1):
        if gene.casefold() in relevant:
            hits += 1
            total += hits / index
    return total / len(relevant)


def _ndcg(ranked: Sequence[str], truth_rank: dict[str, int]) -> float:
    if not truth_rank:
        return 0.0
    maximum = max(truth_rank.values()) + 1
    gains = [maximum - truth_rank.get(gene.casefold(), maximum) for gene in ranked]
    ideal = sorted((maximum - rank for rank in truth_rank.values()), reverse=True)

    def dcg(values: Sequence[int]) -> float:
        return sum(value / math.log2(index + 2) for index, value in enumerate(values))

    denominator = dcg(ideal)
    return dcg(gains) / denominator if denominator else 0.0


def _write_ranking(
    *,
    path: Path,
    scored: Sequence[tuple[float, dict[str, Any]]],
    visible: set[str],
    weights: dict[str, float],
) -> None:
    records = []
    prediction_rank = 0
    for overall_rank, (score, row) in enumerate(scored, 1):
        is_visible = row["gene_target"].casefold() in visible
        if not is_visible:
            prediction_rank += 1
        records.append(
            {
                "overall_rank": overall_rank,
                "prediction_rank": "" if is_visible else prediction_rank,
                "gene_target": row["gene_target"],
                "score": score,
                "is_visible_example": is_visible,
                **{
                    f"contribution__{name}": float(row["values"][name]) * weight
                    for name, weight in weights.items()
                },
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.casefold() == ".parquet":
        import pyarrow as pa
        import pyarrow.parquet as pq

        pq.write_table(pa.Table.from_pylist(records), path, compression="zstd")
        return
    delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(records[0]), delimiter=delimiter
        )
        writer.writeheader()
        writer.writerows(records)


def _write_records(path: Path, records: Sequence[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("cannot write an empty record table")
    path.parent.mkdir(parents=True, exist_ok=True)
    delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(records[0]), delimiter=delimiter
        )
        writer.writeheader()
        writer.writerows(records)


def calibrate_features(
    *,
    feature_path: Path,
    bindings_path: Path,
    output_path: Path,
    ranking_path: Path,
    gene_column: str,
    requested_features: Sequence[str],
    binding_role: str | None,
    folds: int,
    top_ks: Sequence[int],
    bootstrap_replicates: int,
    random_seed: int,
    pair_correlation_limit: float,
    max_ensembles: int,
    residual_path: Path | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    feature_names, rows, missingness = _load_feature_rows(
        feature_path,
        gene_column,
        requested_features,
    )
    examples, ordering_kind = _visible_examples(bindings_path, binding_role)
    row_by_gene = {row["gene_target"].casefold(): row for row in rows}
    covered = [row for row in examples if row["gene_target"].casefold() in row_by_gene]
    missing_examples = [
        row["gene_target"]
        for row in examples
        if row["gene_target"].casefold() not in row_by_gene
    ]
    if len(covered) < 6:
        raise ValueError("fewer than six ranked examples occur in the feature table")
    models, model_inventory = _models(
        feature_names,
        rows,
        pair_correlation_limit,
        max_ensembles,
    )
    outer_folds = _stratified_folds(covered, folds)
    outer_predictions: list[dict[str, Any]] = []
    outer_selections: list[str] = []
    for outer_index, heldout in enumerate(outer_folds, 1):
        heldout_keys = {row["gene_target"].casefold() for row in heldout}
        training = [
            row for row in covered if row["gene_target"].casefold() not in heldout_keys
        ]
        inner_diagnostics = _candidate_cv(
            models=models,
            examples=training,
            rows=rows,
            row_by_gene=row_by_gene,
            fold_count=min(folds, max(2, len(training) // 2)),
            top_ks=top_ks,
        )
        selected = _one_se_select(inner_diagnostics)
        selected_model = tuple(selected["features"])
        predictions, _, _ = _evaluate(
            model=selected_model,
            training=training,
            heldout=heldout,
            rows=rows,
            row_by_gene=row_by_gene,
            top_ks=top_ks,
        )
        outer_selections.append(selected["model"])
        outer_predictions.extend(
            {**row, "outer_fold": outer_index, "selected_model": selected["model"]}
            for row in predictions
        )

    final_diagnostics = _candidate_cv(
        models=models,
        examples=covered,
        rows=rows,
        row_by_gene=row_by_gene,
        fold_count=folds,
        top_ks=top_ks,
    )
    final_selection = _one_se_select(final_diagnostics)
    final_model = tuple(final_selection["features"])
    final_weights, final_correlations = _fit_model(final_model, covered, row_by_gene)
    scored = sorted(
        ((_score_row(row, final_weights), row) for row in rows),
        key=lambda item: (-item[0], item[1]["gene_target"].casefold()),
    )
    visible = {row["gene_target"].casefold() for row in covered}
    _write_ranking(
        path=ranking_path,
        scored=scored,
        visible=visible,
        weights=final_weights,
    )

    ranked_genes = [row["gene_target"] for _, row in scored]
    truth_rank = {row["gene_target"].casefold(): int(row["rank"]) for row in covered}
    final_scores = {row["gene_target"].casefold(): score for score, row in scored}
    supplied_outcome = [-float(row["rank"]) for row in covered]
    apparent_monotonicity = _spearman(
        [final_scores[row["gene_target"].casefold()] for row in covered],
        supplied_outcome,
    )
    oof_monotonicity = _spearman(
        [row["top_percentile"] for row in outer_predictions],
        [-float(row["supplied_rank"]) for row in outer_predictions],
    )
    oof_ranked = [
        row["gene_target"]
        for row in sorted(
            outer_predictions,
            key=lambda row: (-row["top_percentile"], row["gene_target"].casefold()),
        )
    ]

    eligible = [
        row for _, row in scored if row["gene_target"].casefold() not in visible
    ]
    stability_k = min(max(top_ks), len(eligible))
    canonical_top = {row["gene_target"].casefold() for row in eligible[:stability_k]}
    bootstrap_jaccards: list[float] = []
    rng = random.Random(random_seed)
    for _ in range(bootstrap_replicates):
        training = [rng.choice(covered) for _ in covered]
        weights, _ = _fit_model(final_model, training, row_by_gene)
        bootstrap_scored = sorted(
            (
                (_score_row(row, weights), row["gene_target"])
                for row in rows
                if row["gene_target"].casefold() not in visible
            ),
            key=lambda item: (-item[0], item[1].casefold()),
        )
        bootstrap_top = {gene.casefold() for _, gene in bootstrap_scored[:stability_k]}
        union = canonical_top | bootstrap_top
        bootstrap_jaccards.append(
            len(canonical_top & bootstrap_top) / len(union) if union else 1.0
        )

    selection_counts = {
        model: outer_selections.count(model) for model in sorted(set(outer_selections))
    }
    single_diagnostics = sorted(
        (row for row in final_diagnostics if row["complexity"] == 1),
        key=lambda row: (-row["mean_top_percentile"], row["model"]),
    )
    top_models = sorted(
        final_diagnostics,
        key=lambda row: (-row["mean_top_percentile"], row["complexity"], row["model"]),
    )[:20]
    counterexamples = sorted(
        outer_predictions,
        key=lambda row: (
            -row["underprediction_gap"],
            row["supplied_rank"],
            row["top_percentile"],
        ),
    )[:10]
    resolved_residual_path = (
        residual_path.expanduser().resolve()
        if residual_path is not None
        else output_path.expanduser().resolve().parent / "residual_anchors.tsv"
    )
    residual_records = [
        {
            "anchor_priority": index,
            "gene_target": row["gene_target"],
            "supplied_rank": row["supplied_rank"],
            "oof_universe_rank": row["universe_rank"],
            "oof_top_percentile": row["top_percentile"],
            "expected_percentile_from_supplied_rank": row[
                "expected_percentile_from_supplied_rank"
            ],
            "underprediction_gap": row["underprediction_gap"],
            "rank_deficit": row["rank_deficit"],
            "outer_fold": row["outer_fold"],
            "selected_model": row["selected_model"],
            "diagnostic_role": "out_of_fold_underprediction_anchor",
        }
        for index, row in enumerate(counterexamples, 1)
    ]
    _write_records(resolved_residual_path, residual_records)
    result = {
        "schema_version": CALIBRATION_SCHEMA,
        "status": "passed",
        "method": (
            "nested rank-stratified cross-validation with inner one-standard-error "
            "model selection; final model refit on all visible ranks"
        ),
        "ordering_kind": ordering_kind,
        "feature_source": str(feature_path.expanduser().resolve()),
        "bindings_source": str(bindings_path.expanduser().resolve()),
        "ranking_output": str(ranking_path.expanduser().resolve()),
        "residual_anchor_output": str(resolved_residual_path),
        "universe_size": len(rows),
        "visible_example_count": len(examples),
        "covered_example_count": len(covered),
        "missing_visible_examples": missing_examples,
        "features_considered": feature_names,
        "feature_missingness": missingness,
        "model_inventory": model_inventory,
        "selected_model": {
            **final_selection,
            "weights": final_weights,
            "training_spearman_with_better_rank": final_correlations,
        },
        "nested_evaluation": {
            "fold_count": len(outer_folds),
            "mean_top_percentile": statistics.fmean(
                row["top_percentile"] for row in outer_predictions
            ),
            "median_top_percentile": statistics.median(
                row["top_percentile"] for row in outer_predictions
            ),
            "spearman_oof_percentile_with_better_rank": oof_monotonicity,
            "rank_order_ndcg": _ndcg(oof_ranked, truth_rank),
            **{
                f"recall_at_{value}": sum(
                    row[f"hit_at_{value}"] for row in outer_predictions
                )
                / len(outer_predictions)
                for value in top_ks
            },
            "outer_model_selection_frequency": selection_counts,
            "counterexamples": counterexamples,
            "counterexample_policy": (
                "Largest positive gap between the percentile implied by the "
                "supplied numeric rank and the held-out feature percentile. These "
                "are review anchors, not graph-derived candidates or overrides."
            ),
        },
        "apparent_full_fit_diagnostics": {
            "spearman_score_with_better_rank": apparent_monotonicity,
            "average_precision_visible_examples": _average_precision(
                ranked_genes,
                visible,
            ),
            "ndcg_supplied_rank": _ndcg(ranked_genes, truth_rank),
            "warning": (
                "Descriptive refit diagnostics reuse all supplied ranks and are not "
                "out-of-fold performance estimates."
            ),
        },
        "bootstrap_stability": {
            "replicates": bootstrap_replicates,
            "top_k": stability_k,
            "mean_jaccard": (
                statistics.fmean(bootstrap_jaccards) if bootstrap_jaccards else None
            ),
            "median_jaccard": (
                statistics.median(bootstrap_jaccards) if bootstrap_jaccards else None
            ),
            "p10_jaccard": (
                _percentile(bootstrap_jaccards, 0.10) if bootstrap_jaccards else None
            ),
        },
        "single_feature_diagnostics": single_diagnostics,
        "top_model_diagnostics": top_models,
        "graph_features_excluded": True,
        "duration_s": round(time.monotonic() - started, 3),
        "interpretation": (
            "This measures stability and alignment with supplied ordinal examples. "
            "It does not establish that the selected feature directly measures an "
            "unobserved biological endpoint."
        ),
    }
    _json_dump(output_path, result)
    return result


def _read_ranked_rows(
    path: Path,
    rank_column: str = "prediction_rank",
) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    match = ANSWER_TSV.search(text)
    body = match.group("body") if match else text
    lines = [line for line in body.splitlines() if line.strip()]
    if not lines:
        return []
    delimiter = "\t" if "\t" in lines[0] else ","
    reader = csv.DictReader(lines, delimiter=delimiter)
    if not reader.fieldnames or "gene_target" not in reader.fieldnames:
        raise ValueError("ranking requires a gene_target column")
    selected_rank_column = (
        rank_column
        if rank_column in reader.fieldnames
        else "rank"
        if "rank" in reader.fieldnames
        else None
    )
    rows = []
    for index, row in enumerate(reader, 1):
        gene = str(row.get("gene_target") or "").strip()
        raw_rank = str(
            row.get(selected_rank_column) if selected_rank_column is not None else index
        ).strip()
        if gene and raw_rank.isdigit():
            rows.append((int(raw_rank), gene))
    rows.sort(key=lambda item: (item[0], item[1].casefold()))
    return rows


def _read_overrides(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    text = path.read_text(encoding="utf-8")
    if path.suffix.casefold() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("overrides"), list):
        return [row for row in payload["overrides"] if isinstance(row, dict)]
    raise ValueError("override file must contain a JSON list or JSONL records")


def validate_ordering(
    *,
    basis_path: Path,
    answer_path: Path,
    output_path: Path,
    overrides_path: Path | None,
    top_k: int,
) -> dict[str, Any]:
    basis_rows = _read_ranked_rows(basis_path)[:top_k]
    answer_rows = _read_ranked_rows(answer_path, rank_column="rank")[:top_k]
    basis = [gene for _, gene in basis_rows]
    answer = [gene for _, gene in answer_rows]
    errors = []
    if len(basis) != top_k:
        errors.append(f"basis contains {len(basis)} prediction ranks; expected {top_k}")
    if len(answer) != top_k:
        errors.append(f"answer contains {len(answer)} ranked genes; expected {top_k}")
    if len(set(gene.casefold() for gene in answer)) != len(answer):
        errors.append("answer contains duplicate genes")
    expected_ranks = list(range(1, top_k + 1))
    if [rank for rank, _ in basis_rows] != expected_ranks:
        errors.append("basis prediction ranks must be unique and contiguous from 1")
    if [rank for rank, _ in answer_rows] != expected_ranks:
        errors.append("answer ranks must be unique and contiguous from 1")
    overrides = _read_overrides(overrides_path)
    override_by_gene = {
        str(row.get("gene_target") or "").casefold(): row
        for row in overrides
        if str(row.get("gene_target") or "").strip()
    }
    mismatches = []
    for final_rank, gene in enumerate(answer, 1):
        canonical_rank = next(
            (
                index
                for index, candidate in enumerate(basis, 1)
                if candidate.casefold() == gene.casefold()
            ),
            None,
        )
        if canonical_rank == final_rank:
            continue
        row = override_by_gene.get(gene.casefold())
        mismatch = {
            "gene_target": gene,
            "canonical_rank": canonical_rank,
            "final_rank": final_rank,
            "override_present": row is not None,
        }
        mismatches.append(mismatch)
        if row is None:
            errors.append(f"{gene}: ordering mismatch lacks an override record")
            continue
        required = (
            "displaced_gene_target",
            "endpoint_evidence",
            "evidence_source",
            "reason",
        )
        missing = [name for name in required if not str(row.get(name) or "").strip()]
        if missing:
            errors.append(f"{gene}: override is missing {', '.join(missing)}")
        if (
            row.get("canonical_rank") != canonical_rank
            or row.get("final_rank") != final_rank
        ):
            errors.append(
                f"{gene}: override ranks do not match the observed displacement"
            )
        expected_displaced = basis[final_rank - 1] if final_rank <= len(basis) else None
        if (
            str(row.get("displaced_gene_target") or "").casefold()
            != str(expected_displaced or "").casefold()
        ):
            errors.append(
                f"{gene}: displaced_gene_target must be {expected_displaced!r}"
            )
    result = {
        "schema_version": ORDERING_VALIDATION_SCHEMA,
        "status": "passed" if not errors else "failed",
        "basis": str(basis_path.expanduser().resolve()),
        "answer": str(answer_path.expanduser().resolve()),
        "top_k": top_k,
        "exact_basis_order_preserved": [gene.casefold() for gene in answer]
        == [gene.casefold() for gene in basis],
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "errors": errors,
        "override_policy": (
            "Every displacement requires candidate-specific endpoint evidence and "
            "the exact promoted/displaced rank change. Structural validation does "
            "not establish the biological truth of the supplied evidence."
        ),
    }
    _json_dump(output_path, result)
    return result


def _add_summary_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser("summarize", help="cache a compact feature table")
    parser.add_argument("--parquet", required=True)
    parser.add_argument("--level", choices=("target", "target_cell"), default="target")
    parser.add_argument("--cache-dir", required=True)
    parser.add_argument("--out")
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--targets-file")
    parser.add_argument("--target-column", default="gene_target")
    parser.add_argument("--cell-type", action="append", default=[])
    parser.add_argument("--cell-types-file")
    parser.add_argument("--cell-type-column", default="cell_type")
    parser.add_argument("--bindings")
    parser.add_argument("--bindings-role")
    parser.add_argument("--include-controls", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--measured-gene-column", default="names")
    parser.add_argument("--group-column", default="group_name")
    parser.add_argument("--gene-target-column", default="gene_target")
    parser.add_argument("--logfoldchange-column", default="logfoldchanges")
    parser.add_argument("--score-column", default="scores")
    parser.add_argument("--pvalue-column", default="pvals")
    parser.add_argument("--adjusted-pvalue-column", default="pvals_adj")
    parser.add_argument("--significance-column", default="significant_adj_0_1")


def _add_calibration_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "calibrate",
        help="select a simple stable basis with nested rank-stratified CV",
    )
    parser.add_argument("--features", required=True)
    parser.add_argument("--bindings", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--ranking-out", required=True)
    parser.add_argument(
        "--residual-out",
        help="write bounded out-of-fold underprediction anchors (default: residual_anchors.tsv beside --out)",
    )
    parser.add_argument("--gene-column", default="gene_target")
    parser.add_argument("--feature", action="append", default=[])
    parser.add_argument("--bindings-role")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--top-k", type=int, action="append", default=[])
    parser.add_argument("--bootstrap", type=int, default=100)
    parser.add_argument("--random-seed", type=int, default=1729)
    parser.add_argument("--pair-correlation-limit", type=float, default=0.95)
    parser.add_argument("--max-ensembles", type=int, default=256)


def _add_validation_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "validate-ordering",
        help="require endpoint-bearing records for deviations from a basis",
    )
    parser.add_argument("--basis", required=True)
    parser.add_argument("--answer", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--overrides")
    parser.add_argument("--top-k", type=int, required=True)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_summary_parser(subparsers)
    _add_calibration_parser(subparsers)
    _add_validation_parser(subparsers)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "summarize":
            bindings = Path(args.bindings) if args.bindings else None
            targets = _combined_values(
                args.target,
                Path(args.targets_file) if args.targets_file else None,
                args.target_column,
                bindings,
                args.bindings_role,
            )
            cell_types = _combined_values(
                args.cell_type,
                Path(args.cell_types_file) if args.cell_types_file else None,
                args.cell_type_column,
            )
            result = summarize_features(
                parquet_path=Path(args.parquet),
                level=args.level,
                cache_dir=Path(args.cache_dir),
                output_path=Path(args.out) if args.out else None,
                targets=targets,
                cell_types=cell_types,
                include_controls=args.include_controls,
                force=args.force,
                column_roles={
                    "measured_gene": args.measured_gene_column,
                    "cell_type": args.group_column,
                    "gene_target": args.gene_target_column,
                    "logfoldchange": args.logfoldchange_column,
                    "wilcoxon_score": args.score_column,
                    "pvalue": args.pvalue_column,
                    "adjusted_pvalue": args.adjusted_pvalue_column,
                    "significant_fdr_010": args.significance_column,
                },
            )
        elif args.command == "calibrate":
            top_ks = sorted(set(args.top_k or [50, 100]))
            if any(value <= 0 for value in top_ks):
                raise ValueError("top-k values must be positive")
            if args.folds < 2:
                raise ValueError("folds must be at least two")
            if args.bootstrap < 0:
                raise ValueError("bootstrap replicates cannot be negative")
            if not 0 < args.pair_correlation_limit <= 1:
                raise ValueError("pair correlation limit must be in (0, 1]")
            result = calibrate_features(
                feature_path=Path(args.features),
                bindings_path=Path(args.bindings),
                output_path=Path(args.out),
                ranking_path=Path(args.ranking_out),
                gene_column=args.gene_column,
                requested_features=args.feature,
                binding_role=args.bindings_role,
                folds=args.folds,
                top_ks=top_ks,
                bootstrap_replicates=args.bootstrap,
                random_seed=args.random_seed,
                pair_correlation_limit=args.pair_correlation_limit,
                max_ensembles=max(0, args.max_ensembles),
                residual_path=Path(args.residual_out) if args.residual_out else None,
            )
        else:
            result = validate_ordering(
                basis_path=Path(args.basis),
                answer_path=Path(args.answer),
                output_path=Path(args.out),
                overrides_path=Path(args.overrides) if args.overrides else None,
                top_k=args.top_k,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        error = {"status": "failed", "command": args.command, "error": str(exc)}
        output = getattr(args, "out", None)
        if output:
            _json_dump(Path(output), error)
        print(json.dumps(error, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
