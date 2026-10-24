#!/usr/bin/env python3
"""Extract non-seed BioKG entities from finding requests with an LLM."""

from __future__ import annotations

import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from ..paths import GRAPH_WORK_DIR


DEFAULT_REQUESTS = GRAPH_WORK_DIR / "entity_extraction_requests.jsonl"
DEFAULT_OUT = GRAPH_WORK_DIR / "llm_entities.raw.jsonl"
DEFAULT_ERRORS = GRAPH_WORK_DIR / "llm_entities.errors.jsonl"

SYSTEM_PROMPT = """You extract normalized biological entities for a manuscript knowledge graph.

The graph already has deterministic seed nodes for target genes, findings,
cell types, evidence, and references. Extract only non-seed biological entities
that should become reusable graph nodes: genes, modules, pathways, complexes,
phenotypes, and other specific biological entities that do not fit those
categories.

Seed cell types are already graph nodes. Do not extract cell types, cell-type
labels, neurotransmitter labels, or pieces of cell-type names as genes or
concepts. Examples of non-gene cell-type label fragments include Glut, Gaba,
GABA, MB Glut, Pvalb Gaba, P MY, TH Prkcd Grin2c Glut, and CNU-HYa. If a token
appears only inside seed_nodes.cell_types, do not extract it.

The target gene is already a seed node. Do not extract it under its symbol,
protein name, long-form gene name, or alias.

The OpenIE entity/triple fields are noisy context. Use them to notice possible
biological terms, but do not treat "included in a cell type label" as evidence
for a gene or pathway node.

Do not convert arbitrary prose into entities. For example, "assay for every
member of the broader pathway" is not a pathway, and "strongest signature" is
not a module. Prefer canonical biological names and preserve uncertainty.

Use kind "other" only when no fixed category fits. Good "other" examples are
specific diseases, drugs/compounds, lipids/metabolites, ion channels, or
electrophysiological currents. Put the best available type label in other_type,
for example disease, drug/compound, lipid, ion_channel, or electrophysiology.
Use kind "pathway" for named mechanisms, pathways, and GO-like biological
processes. Do not use "other" with other_type biological_process or phenotype;
use the fixed kind instead. Buffered transcriptional response is a valid
phenotype when the finding explicitly describes buffering or transcriptomic
silence."""

ENTITY_SCHEMA: dict[str, Any] = {
    "type": "json_schema",
    "name": "biokg_entities",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "kind": {
                            "type": "string",
                            "enum": [
                                "gene",
                                "module",
                                "pathway",
                                "complex",
                                "phenotype",
                                "other",
                            ],
                        },
                        "name": {"type": "string"},
                        "canonical_name": {"type": "string"},
                        "other_type": {"type": "string"},
                        "aliases": {"type": "array", "items": {"type": "string"}},
                        "relation_to_finding": {
                            "type": "string",
                            "enum": ["AFFECTS_GENE", "COMPARES_TO", "IMPLICATES"],
                        },
                        "effect_status": {
                            "type": "string",
                            "enum": [
                                "affected",
                                "implicated",
                                "compared",
                                "buffered",
                                "absent_or_not_detected",
                                "fdr_insignificant",
                                "nominal",
                                "mixed",
                                "caveated",
                                "uncertain",
                            ],
                        },
                        "role": {"type": "string"},
                        "evidence_span": {"type": "string"},
                        "confidence": {"type": "string", "enum": ["high", "moderate", "low"]},
                    },
                    "required": [
                        "kind",
                        "name",
                        "canonical_name",
                        "other_type",
                        "aliases",
                        "relation_to_finding",
                        "effect_status",
                        "role",
                        "evidence_span",
                        "confidence",
                    ],
                },
            }
        },
        "required": ["entities"],
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def existing_doc_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {str(row.get("doc_id")) for row in read_jsonl(path)}


def user_prompt(request: dict[str, Any]) -> str:
    return (
        "Extract normalized graph entities from this finding request. Return JSON only.\n\n"
        f"{json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True)}"
    )


def extract_one(client: Any, request: dict[str, Any], *, model: str) -> dict[str, Any]:
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt(request)},
        ],
        text={"format": ENTITY_SCHEMA},
    )
    parsed = json.loads(response.output_text)
    return {
        "doc_id": request["doc_id"],
        "target_gene": request["target_gene"],
        "finding_id": request["finding_id"],
        "model": model,
        "seed_nodes": request.get("seed_nodes") or {},
        "source_context": request.get("source_context") or {},
        "entities": parsed["entities"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--errors", type=Path, default=DEFAULT_ERRORS)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--limit", type=int, default=0, help="0 means no limit.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent extraction requests. Calls are independent and I/O-bound.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.overwrite:
        args.out.unlink(missing_ok=True)
        args.errors.unlink(missing_ok=True)

    from openai import OpenAI

    requests = read_jsonl(args.requests)
    done = existing_doc_ids(args.out)
    pending = [r for r in requests if str(r.get("doc_id")) not in done]
    if args.limit:
        pending = pending[: args.limit]

    client = OpenAI()
    write_lock = threading.Lock()
    processed = 0
    failed = 0

    def work(request: dict[str, Any]) -> bool:
        doc_id = str(request.get("doc_id"))
        try:
            row = extract_one(client, request, model=args.model)
            with write_lock:
                append_jsonl(args.out, row)
            return True
        except Exception as exc:  # noqa: BLE001 - preserve API/schema failures for reruns.
            with write_lock:
                append_jsonl(
                    args.errors,
                    {
                        "doc_id": doc_id,
                        "target_gene": request.get("target_gene"),
                        "finding_id": request.get("finding_id"),
                        "error": f"{type(exc).__name__}: {exc}",
                    },
                )
            return False

    if pending:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            for ok in as_completed(pool.submit(work, request) for request in pending):
                if ok.result():
                    processed += 1
                else:
                    failed += 1

    print(
        json.dumps(
            {
                "processed": processed,
                "failed": failed,
                "workers": args.workers,
                "out": str(args.out),
                "errors": str(args.errors),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
