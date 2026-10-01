"""Deterministic task-input inventory and lightweight entity binding.

This module handles representation, not scientific routing.  It discovers the
same supplied gene set whether it appears in prompt prose, a fenced table, or a
declared sidecar; preserves explicit ranks; and proposes dataset cell-context
matches without silently declaring fuzzy matches equivalent.
"""

from __future__ import annotations

import csv
import io
import json
import re
import tomllib
from pathlib import Path
from typing import Any, Iterable


TASK_BINDINGS_SCHEMA = "distributed_agents-task-bindings-v1"
SUPPORTED_TEXT_SUFFIXES = {".csv", ".json", ".md", ".toml", ".tsv", ".txt"}
GENE_COLUMNS = {
    "gene",
    "genes",
    "gene_symbol",
    "gene_symbols",
    "gene_target",
    "gene_targets",
    "member_gene",
    "target_gene",
    "target_genes",
}
RANK_COLUMNS = {"known_rank", "rank", "ranking", "position"}
CELL_TYPE_RE = re.compile(
    r"\b\d{3}\s+[A-Za-z0-9][A-Za-z0-9+\- ]{2,80}?(?:Glut|GABA|Gaba|Dopa)\b"
)
FENCED_TABLE_RE = re.compile(
    r"```(?P<format>tsv|csv)\s*\n(?P<body>.*?)```",
    flags=re.IGNORECASE | re.DOTALL,
)
EXPLICIT_CONTEXT_MAP_RE = re.compile(
    r"(?P<output>[A-Za-z0-9][A-Za-z0-9.+\-]*)\s*<-\s*[\"`]"
    r"(?P<input>[^\"`]+)[\"`]"
)
PROSE_GENE_LIST_RE = re.compile(
    r"(?im)^(?:the\s+\d+\s+)?(?:target\s+genes?|gene\s+targets?|"
    r"perturbations?)\s*:\s*(?P<body>[^\n]+)$"
)
CELL_PHRASE_RE = re.compile(
    r"(?i)\b(?:in|within|from|among|for)\s+"
    r"(?P<phrase>[A-Za-z0-9.+\-]+(?:\s+[A-Za-z0-9.+\-]+){0,6}\s+"
    r"(?:neurons?|interneurons?|cells?))"
)
GENE_TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{1,30}$")


DEFAULT_CELL_TYPES = (
    "001 L5-6 IT Glut",
    "005 L4-5 IT CTX Glut",
    "007 L2-3 IT CTX Glut",
    "008 L2-3 IT ENT PPP RSP Glut",
    "009 L2-3 IT PIR AON ENT Glut",
    "012 MEA LA CA1 DG Glut",
    "017 CA3 CA2-FC DG Glut",
    "022 L5 ET CTX Glut",
    "027 NP-CT-L6b-OB Glut",
    "046 CTX-CGE GABA",
    "052 Pvalb Gaba",
    "053 Sst Gaba",
    "054 CNU-MGE GABA",
    "059 CNU-LGE LSX GABA",
    "066 CNU-HYa HY GABA",
    "110 CNU-HYa HY MM Glut",
    "145 MH-LH TH Glut",
    "151 TH Prkcd Grin2c Glut",
    "155 MB Glut",
    "191 MB P MY GABA",
    "215 MB Dopa",
    "217 P MY Pineal Glut",
    "308 CB GABA",
)

_TERM_ALIASES = {
    "ctx": ("cortex", "cortical"),
    "th": ("thalamus", "thalamic"),
    "mb": ("midbrain",),
    "cb": ("cerebellum", "cerebellar"),
    "glut": ("glutamatergic", "excitatory"),
    "gaba": ("gabaergic", "inhibitory", "interneuron"),
    "dopa": ("dopaminergic",),
    "pvalb": ("parvalbumin",),
    "sst": ("somatostatin",),
}
_TERM_CANONICAL = {
    alias: canonical
    for canonical, aliases in _TERM_ALIASES.items()
    for alias in (canonical, *aliases)
}


def _normalized_name(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().casefold()).strip(
        "_"
    )


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _tokens(value: str) -> set[str]:
    raw = re.findall(r"[A-Za-z0-9]+", value.casefold())
    ignored = {"cell", "cells", "neuron", "neurons", "type", "types"}
    return {
        _TERM_CANONICAL.get(token, token)
        for token in raw
        if token not in ignored and not token.isdigit()
    }


def resolve_cell_context(
    query: str,
    *,
    vocabulary: Iterable[str] = DEFAULT_CELL_TYPES,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Return conservative lexical candidates for one cell-context phrase."""

    normalized = _normalized_name(query)
    query_tokens = _tokens(query)
    candidates: list[dict[str, Any]] = []
    for label in vocabulary:
        label_normalized = _normalized_name(label)
        if normalized == label_normalized:
            score = 1.0
            relation = "exact"
        else:
            label_tokens = _tokens(label)
            overlap = query_tokens & label_tokens
            if not overlap:
                continue
            score = len(overlap) / max(1, len(query_tokens | label_tokens))
            relation = "candidate"
        candidates.append(
            {
                "dataset_value": label,
                "relation": relation,
                "score": round(score, 6),
                "matched_terms": sorted(query_tokens & _tokens(label)),
            }
        )
    candidates.sort(
        key=lambda row: (-float(row["score"]), str(row["dataset_value"]))
    )
    return candidates[: max(1, limit)]


def _ordering(
    rank_column: str | None, ranks: list[int | None], *, hint: str
) -> dict[str, Any]:
    if rank_column is None:
        lowered = hint.casefold()
        hinted = "unranked" not in lowered and any(
            token in lowered for token in ("ranked", "ranking", "top_hits")
        )
        return {
            "kind": "ranked" if hinted else "unranked",
            "explicit_rank": False,
            "direction": "best_first" if hinted else "not_applicable",
        }
    numeric_ranks = [rank for rank in ranks if isinstance(rank, int)]
    contiguous = numeric_ranks == list(range(1, len(ranks) + 1))
    partial = (
        rank_column == "known_rank"
        or len(numeric_ranks) != len(ranks)
        or not contiguous
    )
    return {
        "kind": "partial_ranked" if partial else "ranked",
        "explicit_rank": True,
        "rank_field": rank_column,
        "direction": "best_first",
    }


def _role(gene_column: str, rank_column: str | None, context: str, values: list[str]) -> str:
    lowered = context.casefold()
    if values and all(value.casefold().startswith("examplegene") for value in values):
        return "output_example"
    if any(
        marker in lowered
        for marker in ("required output", "final answer", "answer.txt", "output example")
    ):
        return "output_example"
    if rank_column == "known_rank":
        return "supplied_ranked_examples"
    if gene_column == "member_gene":
        return "response_genes"
    return "task_targets"


def _binding(
    *,
    binding_id: str,
    source_kind: str,
    source_path: str,
    selector: str,
    gene_column: str,
    values: list[str],
    ranks: list[int | None],
    rank_column: str | None,
    context: str,
) -> dict[str, Any] | None:
    cleaned = [
        (value.strip(), rank)
        for value, rank in zip(values, ranks)
        if GENE_TOKEN_RE.fullmatch(value.strip())
    ]
    if not cleaned:
        return None
    clean_values = [value for value, _rank in cleaned]
    clean_ranks = [rank for _value, rank in cleaned]
    role = _role(gene_column, rank_column, context, clean_values)
    return {
        "binding_id": binding_id,
        "entity_type": "gene",
        "role": role,
        "active_for_coverage": role in {"task_targets", "supplied_ranked_examples"},
        "source": {
            "kind": source_kind,
            "path": source_path,
            "selector": selector,
        },
        "ordering": _ordering(rank_column, clean_ranks, hint=f"{selector} {context}"),
        "count": len(clean_values),
        "items": [
            {
                "raw": value,
                "canonical": value,
                "position": position,
                **({"rank": rank} if isinstance(rank, int) else {}),
            }
            for position, (value, rank) in enumerate(cleaned, start=1)
        ],
    }


def _table_binding(
    *,
    text: str,
    delimiter: str,
    binding_prefix: str,
    source_kind: str,
    source_path: str,
    context: str,
) -> list[dict[str, Any]]:
    try:
        rows = list(csv.DictReader(io.StringIO(text), delimiter=delimiter))
    except csv.Error:
        return []
    if not rows or not rows[0]:
        return []
    by_normalized = {_normalized_name(name): name for name in rows[0]}
    rank_column = next((name for name in RANK_COLUMNS if name in by_normalized), None)
    rank_header = by_normalized.get(rank_column) if rank_column else None
    bindings: list[dict[str, Any]] = []
    for gene_column in sorted(GENE_COLUMNS & set(by_normalized)):
        header = by_normalized[gene_column]
        values: list[str] = []
        ranks: list[int | None] = []
        for row in rows:
            value = str(row.get(header) or "").strip()
            if not value:
                continue
            rank_raw = str(row.get(rank_header) or "").strip() if rank_header else ""
            rank = int(rank_raw) if rank_raw.isdigit() else None
            values.append(value)
            ranks.append(rank)
        item = _binding(
            binding_id=f"{binding_prefix}:{gene_column}",
            source_kind=source_kind,
            source_path=source_path,
            selector=header,
            gene_column=gene_column,
            values=values,
            ranks=ranks,
            rank_column=rank_column,
            context=context,
        )
        if item is not None:
            bindings.append(item)
    return bindings


def _prompt_bindings(text: str, task_path: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for index, match in enumerate(FENCED_TABLE_RE.finditer(text), start=1):
        context = text[max(0, match.start() - 500) : match.start()]
        result.extend(
            _table_binding(
                text=match.group("body"),
                delimiter="\t" if match.group("format").casefold() == "tsv" else ",",
                binding_prefix=f"prompt:fenced-{index}",
                source_kind="prompt_fenced_table",
                source_path=str(task_path),
                context=context,
            )
        )
    for index, match in enumerate(PROSE_GENE_LIST_RE.finditer(text), start=1):
        values = [
            token
            for token in re.split(r"[,;\s]+", match.group("body"))
            if GENE_TOKEN_RE.fullmatch(token)
        ]
        item = _binding(
            binding_id=f"prompt:prose-{index}:genes",
            source_kind="prompt_prose_list",
            source_path=str(task_path),
            selector=match.group(0).split(":", 1)[0],
            gene_column="gene_targets",
            values=values,
            ranks=[None] * len(values),
            rank_column=None,
            context=match.group(0),
        )
        if item is not None:
            result.append(item)
    return result


def _json_lists(
    value: Any,
    *,
    path: str = "$",
) -> Iterable[tuple[str, str, list[str], list[int | None], str | None]]:
    if isinstance(value, dict):
        normalized = {_normalized_name(key): key for key in value}
        gene_key = next((key for key in GENE_COLUMNS if key in normalized), None)
        rank_key = next((key for key in RANK_COLUMNS if key in normalized), None)
        if gene_key and isinstance(value[normalized[gene_key]], list):
            entries = value[normalized[gene_key]]
            if all(isinstance(item, str) for item in entries):
                yield (
                    f"{path}.{normalized[gene_key]}",
                    gene_key,
                    [str(item) for item in entries],
                    [None] * len(entries),
                    None,
                )
        if isinstance(value, dict) and gene_key and not isinstance(
            value[normalized[gene_key]], list
        ):
            gene = str(value[normalized[gene_key]] or "").strip()
            rank_raw = value.get(normalized.get(rank_key, "")) if rank_key else None
            rank = int(rank_raw) if isinstance(rank_raw, int) else None
            if gene:
                yield (path, gene_key, [gene], [rank], rank_key)
        for key, child in value.items():
            yield from _json_lists(child, path=f"{path}.{key}")
    elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
        rows = [item for item in value if isinstance(item, dict)]
        normalized = {_normalized_name(key): key for key in rows[0]}
        gene_key = next((key for key in GENE_COLUMNS if key in normalized), None)
        if gene_key:
            rank_key = next((key for key in RANK_COLUMNS if key in normalized), None)
            values = [str(row.get(normalized[gene_key]) or "").strip() for row in rows]
            ranks = []
            for row in rows:
                raw = row.get(normalized.get(rank_key, "")) if rank_key else None
                ranks.append(int(raw) if isinstance(raw, int) else None)
            yield (path, gene_key, values, ranks, rank_key)
            return
        for index, child in enumerate(value):
            yield from _json_lists(child, path=f"{path}[{index}]")


def _file_inventory(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suffix = path.suffix.casefold()
    inventory: dict[str, Any] = {
        "path": str(path),
        "format": suffix.lstrip(".") or "unknown",
        "size_bytes": path.stat().st_size,
        "status": "inspected",
    }
    bindings: list[dict[str, Any]] = []
    try:
        if suffix == ".parquet":
            import pyarrow.parquet as pq

            metadata = pq.read_metadata(path)
            inventory.update(
                {"columns": list(metadata.schema.names), "row_count": metadata.num_rows}
            )
        elif suffix in {".csv", ".tsv"} and path.stat().st_size <= 20_000_000:
            text = path.read_text(encoding="utf-8")
            bindings.extend(
                _table_binding(
                    text=text,
                    delimiter="\t" if suffix == ".tsv" else ",",
                    binding_prefix=f"file:{path.name}",
                    source_kind="declared_tabular_file",
                    source_path=str(path),
                    context=path.stem,
                )
            )
            reader = csv.reader(io.StringIO(text), delimiter="\t" if suffix == ".tsv" else ",")
            inventory["columns"] = next(reader, [])
        elif suffix in {".json", ".toml"} and path.stat().st_size <= 20_000_000:
            value = json.loads(path.read_text()) if suffix == ".json" else tomllib.loads(path.read_text())
            inventory["top_level_fields"] = sorted(value) if isinstance(value, dict) else []
            for index, (selector, gene_column, values, ranks, rank_column) in enumerate(
                _json_lists(value), start=1
            ):
                item = _binding(
                    binding_id=f"file:{path.name}:{index}:{gene_column}",
                    source_kind="declared_structured_file",
                    source_path=str(path),
                    selector=selector,
                    gene_column=gene_column,
                    values=values,
                    ranks=ranks,
                    rank_column=rank_column,
                    context=f"{path.stem} {selector}",
                )
                if item is not None:
                    bindings.append(item)
        elif suffix == ".md" and path.stat().st_size <= 20_000_000:
            bindings.extend(_prompt_bindings(path.read_text(), path))
        elif suffix == ".txt" and path.stat().st_size <= 20_000_000:
            values = [line.strip() for line in path.read_text().splitlines() if line.strip()]
            if values and all(GENE_TOKEN_RE.fullmatch(value) for value in values):
                item = _binding(
                    binding_id=f"file:{path.name}:lines",
                    source_kind="declared_text_file",
                    source_path=str(path),
                    selector="lines",
                    gene_column="genes",
                    values=values,
                    ranks=[None] * len(values),
                    rank_column=None,
                    context=path.stem,
                )
                if item is not None:
                    bindings.append(item)
        elif suffix in SUPPORTED_TEXT_SUFFIXES:
            inventory["status"] = "not_inspected_size_limit"
        else:
            inventory["status"] = "metadata_only"
    except (OSError, ValueError, csv.Error, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        inventory.update({"status": "inspection_failed", "error": f"{type(exc).__name__}: {exc}"})
    inventory["binding_ids"] = [row["binding_id"] for row in bindings]
    return inventory, bindings


def _context_bindings(text: str, task_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mappings = [
        {
            "output_context": match.group("output"),
            "input_context": match.group("input"),
            "relation": "task_explicit_proxy",
            "provenance": {"kind": "prompt_explicit_mapping", "path": str(task_path)},
        }
        for match in EXPLICIT_CONTEXT_MAP_RE.finditer(text)
    ]
    mentions: list[dict[str, Any]] = []
    raw_mentions = [*CELL_TYPE_RE.findall(text)]
    raw_mentions.extend(match.group("phrase").strip() for match in CELL_PHRASE_RE.finditer(text))
    for mention in _dedupe(raw_mentions):
        candidates = resolve_cell_context(mention)
        mentions.append(
            {
                "raw": mention,
                "resolution": (
                    "exact"
                    if candidates and candidates[0]["relation"] == "exact"
                    else "candidate_only"
                    if candidates
                    else "unresolved"
                ),
                "candidates": candidates,
            }
        )
    return mappings, mentions


def build_task_bindings(
    task_path: Path,
    declared_inputs: Iterable[Path] = (),
) -> dict[str, Any]:
    """Inventory declared inputs and bind explicit task entities with provenance."""

    task_path = task_path.expanduser().resolve()
    text = task_path.read_text(encoding="utf-8")
    entity_sets = _prompt_bindings(text, task_path)
    inventory: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_path in declared_inputs:
        path = Path(raw_path).expanduser().resolve()
        marker = str(path)
        if marker in seen or not path.is_file():
            continue
        seen.add(marker)
        record, bindings = _file_inventory(path)
        inventory.append(record)
        entity_sets.extend(bindings)

    mappings, cell_contexts = _context_bindings(text, task_path)
    active = [row for row in entity_sets if row["active_for_coverage"]]
    ranking_kinds = sorted({row["ordering"]["kind"] for row in active})
    prediction_requested = bool(
        re.search(r"\b(?:predict|prediction|held[- ]out|complete\s+a\s+partially)\b", text, re.I)
    )
    ranking_requested = bool(
        re.search(
            r"\b(?:known_rank|ranked\s+(?:list|members|genes|most)|"
            r"ranking\s+(?:for|of|task)|order\s+your\s+predictions|"
            r"strongest\s+to\s+weakest|rank\s+restarts)\b",
            text,
            re.I,
        )
    )
    return {
        "schema_version": TASK_BINDINGS_SCHEMA,
        "purpose": (
            "Represent supplied entities, ranks, contexts, and input locations; "
            "scientific routing remains a downstream decision."
        ),
        "task": {
            "path": str(task_path),
            "prediction_requested": prediction_requested,
            "ranking_requested": ranking_requested,
            "observed_list_orderings": ranking_kinds,
        },
        "input_inventory": inventory,
        "entity_sets": entity_sets,
        "context_mappings": mappings,
        "cell_contexts": cell_contexts,
        "guards": [
            "unranked list order is not supervision",
            "partial ranks retain their supplied numeric positions",
            "fuzzy cell-context candidates are not measurement equivalence",
            "task-explicit context mappings take precedence over lexical suggestions",
        ],
    }
