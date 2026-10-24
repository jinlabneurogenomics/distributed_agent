#!/usr/bin/env python3
"""Normalize raw LLM BioKG entities with scispaCy abbreviation context."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from ..paths import GRAPH_WORK_DIR


DEFAULT_RAW = GRAPH_WORK_DIR / "llm_entities.raw.jsonl"
DEFAULT_OUT = GRAPH_WORK_DIR / "llm_entities.normalized.jsonl"
FIXED_KIND_BY_OTHER_TYPE = {
    "gene": "gene",
    "biological_process": "pathway",
    "biological process": "pathway",
    "process": "pathway",
    "phenotype": "phenotype",
    "module": "module",
    "pathway": "pathway",
    "signaling pathway": "pathway",
    "complex": "complex",
    "protein complex": "complex",
    "protein_complex": "complex",
}


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_gene_symbol(value: object) -> str:
    symbol = normalize_text(value)
    return symbol[:1].upper() + symbol[1:] if symbol else ""


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_nlp(model: str):
    import spacy
    from scispacy.abbreviation import AbbreviationDetector

    nlp = spacy.load(model)
    if "abbreviation_detector" not in nlp.pipe_names:
        nlp.add_pipe("abbreviation_detector")
    nlp.max_length = max(nlp.max_length, 250_000)
    return nlp


def abbreviations_from_doc(doc) -> dict[str, str]:
    out = {}
    for abrv in doc._.abbreviations:
        short = normalize_text(abrv)
        long_form = normalize_text(abrv._.long_form)
        if short and long_form:
            out[short.casefold()] = long_form
    return out


def row_text(row: dict[str, Any]) -> str:
    context = row.get("source_context") or {}
    return "\n".join(
        part
        for part in [
            normalize_text(context.get("summary")),
            normalize_text(context.get("why_it_matters")),
            normalize_text(context.get("main_caveats")),
            normalize_text(context.get("text")),
        ]
        if part
    )


def normalize_entity(entity: dict[str, Any], abbrs: dict[str, str], *, model: str) -> dict[str, Any]:
    kind = normalize_text(entity.get("kind"))
    raw_kind = kind
    name = normalize_text(entity.get("name"))
    canonical = normalize_text(entity.get("canonical_name")) or name
    other_type = normalize_text(entity.get("other_type"))
    if kind.casefold() == "other" and other_type.casefold() in FIXED_KIND_BY_OTHER_TYPE:
        kind = FIXED_KIND_BY_OTHER_TYPE[other_type.casefold()]
    elif kind.casefold() in {"biological_process", "biological process", "process"}:
        kind = "pathway"
    expanded = abbrs.get(canonical.casefold()) or abbrs.get(name.casefold())
    if expanded:
        aliases = [*entity.get("aliases", []), name, canonical]
        canonical = expanded
    else:
        aliases = entity.get("aliases", [])
    if kind.casefold() == "gene":
        aliases = [*aliases, canonical] if canonical and canonical != name else aliases
        canonical = normalize_gene_symbol(name or canonical)
    return {
        "kind": kind,
        "raw_kind": raw_kind,
        "name": name,
        "canonical_name": canonical,
        "other_type": other_type,
        "aliases": sorted({normalize_text(alias) for alias in aliases if normalize_text(alias)}),
        "relation_to_finding": normalize_text(entity.get("relation_to_finding")),
        "effect_status": normalize_text(entity.get("effect_status")),
        "role": normalize_text(entity.get("role")),
        "evidence_span": normalize_text(entity.get("evidence_span")),
        "confidence": normalize_text(entity.get("confidence")),
        "normalizer": "scispacy",
        "scispacy_model": model,
    }


def normalize_row(row: dict[str, Any], abbrs: dict[str, str], *, model: str) -> dict[str, Any]:
    entities = []
    seen = set()
    for entity in row.get("entities") or []:
        normalized = normalize_entity(entity, abbrs, model=model)
        key = (
            normalized["kind"].casefold(),
            normalized["canonical_name"].casefold(),
            normalized["relation_to_finding"].casefold(),
        )
        if key in seen:
            continue
        seen.add(key)
        entities.append(normalized)
    return {
        "doc_id": row.get("doc_id"),
        "target_gene": row.get("target_gene"),
        "finding_id": row.get("finding_id"),
        "seed_nodes": row.get("seed_nodes") or {},
        "source_context": row.get("source_context") or {},
        "entities": entities,
        "normalizer": "scispacy",
        "scispacy_model": model,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--model", default="en_core_sci_sm")
    parser.add_argument(
        "--n-process",
        type=int,
        default=1,
        help=(
            "KNOWN ISSUE: keep this at 1. spaCy nlp.pipe(n_process>1) deadlocks with the "
            "scispaCy abbreviation_detector on this corpus -- workers go idle (~0%% CPU) "
            "and never finish (observed 2026-06-26 on the 11,346-finding full corpus with "
            "n_process=4). n_process=1 completes in ~20 min. Do not raise to 'speed it up'."
        ),
    )
    parser.add_argument("--batch-size", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    nlp = load_nlp(args.model)
    rows = read_jsonl(args.raw)
    texts = [row_text(row) for row in rows]
    # Batched pipe; abbreviation_detector runs per doc.
    # KNOWN ISSUE: do NOT set n_process>1 here. nlp.pipe with multiprocessing deadlocks
    # against the scispaCy abbreviation_detector on this corpus -- the worker processes
    # stay alive but go idle (~0% CPU) and never return. Run single-process (default).
    docs = nlp.pipe(texts, batch_size=args.batch_size, n_process=args.n_process)
    normalized = [
        normalize_row(row, abbreviations_from_doc(doc), model=args.model)
        for row, doc in zip(rows, docs)
    ]
    write_jsonl(args.out, normalized)
    print(
        json.dumps(
            {
                "records": len(normalized),
                "out": str(args.out),
                "model": args.model,
                "n_process": args.n_process,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
