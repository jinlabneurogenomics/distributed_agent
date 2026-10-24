#!/usr/bin/env python3
"""Report quality signals for LLM/scispaCy BioKG entity outputs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from ..paths import GRAPH_WORK_DIR


DEFAULT_GRAPH_DIR = GRAPH_WORK_DIR
DEFAULT_NORMALIZED = DEFAULT_GRAPH_DIR / "llm_entities.normalized.jsonl"
DEFAULT_RAW = DEFAULT_GRAPH_DIR / "llm_entities.raw.jsonl"
DEFAULT_OUT_JSON = DEFAULT_GRAPH_DIR / "llm_entity_quality_report.json"
DEFAULT_OUT_MD = DEFAULT_GRAPH_DIR / "llm_entity_quality_report.md"

KIND_ALIASES = {
    "gene": "Gene",
    "genes": "Gene",
    "module": "Module",
    "modules": "Module",
    "pathway": "Pathway",
    "pathways": "Pathway",
    "complex": "Complex",
    "complexes": "Complex",
    "phenotype": "Phenotype",
    "phenotypes": "Phenotype",
    "biological_process": "Pathway",
    "biological process": "Pathway",
    "process": "Pathway",
    "processes": "Pathway",
    "other": "Other",
    "disease": "Other",
    "drug": "Other",
    "compound": "Other",
    "chemical": "Other",
    "lipid": "Other",
    "metabolite": "Other",
    "ion_channel": "Other",
    "ion channel": "Other",
    "channel": "Other",
    "current": "Other",
}

CLAUSE_MARKERS = [
    " although ",
    " because ",
    " despite ",
    " rather than ",
    " which ",
    " while ",
    " where ",
    " that ",
]
SUSPICIOUS_SUBSTRINGS = [
    "assay for",
    "broader pathway",
    "for every member",
    "not assayed",
    "not measured",
    "no evidence",
    "strongest signature",
]
SUSPICIOUS_STARTS = (
    "a ",
    "an ",
    "and ",
    "but ",
    "every ",
    "its ",
    "the ",
    "their ",
    "these ",
    "this ",
    "those ",
)
VERB_TOKENS = {
    "are",
    "is",
    "was",
    "were",
    "be",
    "being",
    "been",
    "show",
    "shows",
    "showed",
    "suggest",
    "suggests",
    "suggested",
    "indicate",
    "indicates",
    "indicated",
    "reveal",
    "reveals",
    "revealed",
    "support",
    "supports",
    "supported",
}
FIXED_KIND_OTHER_TYPES = {
    "biological_process",
    "biological process",
    "process",
    "phenotype",
    "module",
    "pathway",
    "complex",
    "gene",
}
NON_GRAPH_OTHER_TYPES = {
    "cell",
    "cell_type",
    "cell type",
    "celltype",
    "class",
    "measurement",
    "setting",
}


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def canonical_kind(value: object) -> str:
    raw = normalize_text(value).replace("-", "_")
    return KIND_ALIASES.get(raw.casefold(), raw)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def row_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "status": "missing", "records": 0}
    return {"path": str(path), "status": "present", "records": len(read_jsonl(path))}


def entity_name(entity: dict[str, Any]) -> str:
    return (
        normalize_text(entity.get("canonical_name"))
        or normalize_text(entity.get("normalized_name"))
        or normalize_text(entity.get("name"))
        or normalize_text(entity.get("text"))
        or normalize_text(entity.get("label"))
    )


def iter_entities(rows: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for row in rows:
        doc_id = normalize_text(row.get("doc_id"))
        target_gene = normalize_text(row.get("target_gene") or row.get("gene_target"))
        finding_id = normalize_text(row.get("finding_id"))
        seed_nodes = row.get("seed_nodes") or {}
        context = row.get("source_context") or {}
        seed_cell_types = [
            normalize_text(cell_type)
            for cell_type in seed_nodes.get("cell_types") or []
            if normalize_text(cell_type)
        ]
        source_gene_context = {
            normalize_text(gene).casefold()
            for gene in [
                *(context.get("source_genes_for_context") or []),
                *(context.get("source_comparators_for_context") or []),
            ]
            if normalize_text(gene)
        }
        context_text = "\n".join(
            part
            for part in [
                normalize_text(context.get("summary")),
                normalize_text(context.get("why_it_matters")),
                normalize_text(context.get("main_caveats")),
                normalize_text(context.get("text")),
            ]
            if part
        )
        for entity in row.get("entities") or []:
            if not isinstance(entity, dict):
                continue
            kind = canonical_kind(entity.get("kind") or entity.get("type") or entity.get("entity_type"))
            name = normalize_text(entity.get("name"))
            canonical_name = entity_name(entity)
            aliases = [
                normalize_text(alias)
                for alias in entity.get("aliases") or []
                if normalize_text(alias)
            ]
            yield {
                "doc_id": doc_id,
                "target_gene": target_gene,
                "finding_id": finding_id,
                "kind": kind,
                "raw_kind": normalize_text(entity.get("raw_kind")) or kind,
                "name": name,
                "canonical_name": canonical_name,
                "canonical_key": canonical_name.casefold(),
                "other_type": normalize_text(entity.get("other_type")),
                "aliases": aliases,
                "relation_to_finding": normalize_text(entity.get("relation_to_finding")),
                "effect_status": normalize_text(entity.get("effect_status")),
                "role": normalize_text(entity.get("role")),
                "evidence_span": normalize_text(
                    entity.get("evidence_span") or entity.get("evidence") or entity.get("quote")
                ),
                "confidence": normalize_text(entity.get("confidence")),
                "context_text": context_text,
                "seed_cell_types": seed_cell_types,
                "source_gene_context": source_gene_context,
            }


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+", text))


def evidence_span_supported(span: str, context: str) -> bool:
    if not span or not context:
        return True
    span_lower = span.casefold()
    context_lower = context.casefold()
    if span_lower in context_lower:
        return True
    tokens = [
        token
        for token in re.findall(r"[A-Za-z0-9]+", span_lower)
        if len(token) > 2 and token not in {"and", "the", "with", "such", "were", "was"}
    ]
    if not tokens:
        return True
    hits = sum(1 for token in tokens if token in context_lower)
    return hits / len(tokens) >= 0.75


def fragment_reasons(entity: dict[str, Any]) -> list[str]:
    text = entity["canonical_name"]
    lower = text.casefold()
    tokens = set(re.findall(r"[A-Za-z]+", lower))
    reasons: list[str] = []
    if not text:
        reasons.append("empty canonical name")
        return reasons
    if word_count(text) > 10:
        reasons.append("more than 10 words")
    if re.search(r"[.!?;:]$", text):
        reasons.append("sentence punctuation")
    if lower.startswith(SUSPICIOUS_STARTS):
        reasons.append("starts with determiner/pronoun")
    for marker in CLAUSE_MARKERS:
        if marker in f" {lower} ":
            reasons.append(f"clause marker '{marker.strip()}'")
            break
    for phrase in SUSPICIOUS_SUBSTRINGS:
        if phrase in lower:
            reasons.append(f"suspicious phrase '{phrase}'")
            break
    if len(tokens & VERB_TOKENS) >= 1 and word_count(text) >= 4:
        reasons.append("contains sentence-like verb")
    return reasons


def cell_type_like_gene_reasons(entity: dict[str, Any]) -> list[str]:
    if entity["kind"] != "Gene":
        return []
    names = [
        entity["canonical_name"],
        entity["name"],
        *entity["aliases"],
    ]
    name_keys = {name.casefold() for name in names if name}
    if name_keys & entity["source_gene_context"]:
        return []

    reasons: list[str] = []
    for name in names:
        if not name:
            continue
        pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(name.casefold())}(?![A-Za-z0-9])")
        for cell_type in entity["seed_cell_types"]:
            if pattern.search(cell_type.casefold()):
                reasons.append(f"gene name appears only as seed cell-type label fragment: {cell_type}")
                break
        if reasons:
            break
    if "included" in entity["evidence_span"].casefold() and reasons:
        reasons.append("evidence span looks like cell-type label membership")
    return reasons


def compact_entity(entity: dict[str, Any], *, include_context: bool = False) -> dict[str, Any]:
    out = {
        "kind": entity["kind"],
        "raw_kind": entity["raw_kind"],
        "canonical_name": entity["canonical_name"],
        "name": entity["name"],
        "target_gene": entity["target_gene"],
        "finding_id": entity["finding_id"],
        "doc_id": entity["doc_id"],
        "confidence": entity["confidence"],
        "effect_status": entity["effect_status"],
        "other_type": entity["other_type"],
        "evidence_span": entity["evidence_span"],
    }
    if include_context:
        out["context_text"] = entity["context_text"]
    return out


def duplicate_report(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for entity in entities:
        if entity["canonical_key"]:
            grouped[(entity["kind"], entity["canonical_key"])].append(entity)

    rows = []
    for (kind, _canonical_key), items in grouped.items():
        if len(items) < 2:
            continue
        canonical_name = sorted({item["canonical_name"] for item in items}, key=str.casefold)[0]
        surface_names = sorted({item["name"] for item in items if item["name"]}, key=str.casefold)
        rows.append(
            {
                "kind": kind,
                "canonical_name": canonical_name,
                "mentions": len(items),
                "targets": sorted({item["target_gene"] for item in items if item["target_gene"]}),
                "findings": sorted({item["finding_id"] for item in items if item["finding_id"]}),
                "surface_names": surface_names,
            }
        )
    rows.sort(key=lambda row: (-row["mentions"], row["kind"], row["canonical_name"].casefold()))
    return rows


def build_report(normalized_path: Path, raw_path: Path, *, max_examples: int) -> dict[str, Any]:
    raw = row_status(raw_path)
    if not normalized_path.exists():
        return {
            "normalized": {"path": str(normalized_path), "status": "missing", "records": 0},
            "raw": raw,
            "entity_count": 0,
            "message": "Normalized LLM/scispaCy entity file is missing; run extraction and normalization first.",
        }

    rows = read_jsonl(normalized_path)
    entities = list(iter_entities(rows))
    by_kind = Counter(entity["kind"] or "Unknown" for entity in entities)
    by_raw_kind = Counter(entity["raw_kind"] or "Unknown" for entity in entities)
    by_confidence = Counter((entity["confidence"] or "missing").casefold() for entity in entities)
    by_relation = Counter(entity["relation_to_finding"] or "missing" for entity in entities)
    by_effect_status = Counter((entity["effect_status"] or "missing").casefold() for entity in entities)
    by_other_type = Counter(
        (entity["other_type"] or "missing").casefold()
        for entity in entities
        if entity["kind"] == "Other"
    )
    unknown_kinds = sorted(
        {
            entity["kind"]
            for entity in entities
            if entity["kind"] not in set(KIND_ALIASES.values())
        }
    )
    low_confidence = [entity for entity in entities if entity["confidence"].casefold() == "low"]
    missing_confidence = [entity for entity in entities if not entity["confidence"]]
    empty_evidence = [entity for entity in entities if not entity["evidence_span"]]
    evidence_not_in_context = [
        entity
        for entity in entities
        if entity["evidence_span"]
        and entity["context_text"]
        and not evidence_span_supported(entity["evidence_span"], entity["context_text"])
    ]
    fragment_candidates = []
    for entity in entities:
        reasons = fragment_reasons(entity)
        if reasons:
            fragment_candidates.append(compact_entity(entity) | {"reasons": reasons})
    cell_type_like_genes = []
    for entity in entities:
        reasons = cell_type_like_gene_reasons(entity)
        if reasons:
            cell_type_like_genes.append(compact_entity(entity) | {"reasons": reasons})
    other_fixed_kind_candidates = [
        compact_entity(entity) | {"reasons": [f"other_type '{entity['other_type']}' looks like a fixed schema kind"]}
        for entity in entities
        if entity["kind"] == "Other" and entity["other_type"].casefold() in FIXED_KIND_OTHER_TYPES
    ]
    promoted_other_to_fixed = [
        compact_entity(entity)
        for entity in entities
        if entity["raw_kind"].casefold() == "other" and entity["kind"] != "Other"
    ]
    non_graph_other = [
        compact_entity(entity) | {"reasons": [f"other_type '{entity['other_type']}' is excluded from graph construction"]}
        for entity in entities
        if entity["raw_kind"].casefold() == "other"
        and entity["other_type"].casefold() in NON_GRAPH_OTHER_TYPES
    ]

    duplicates = duplicate_report(entities)
    records_without_entities = sum(1 for row in rows if not row.get("entities"))
    docs_with_entities = len({entity["doc_id"] for entity in entities if entity["doc_id"]})
    return {
        "normalized": {"path": str(normalized_path), "status": "present", "records": len(rows)},
        "raw": raw,
        "entity_count": len(entities),
        "docs_with_entities": docs_with_entities,
        "records_without_entities": records_without_entities,
        "by_kind": dict(sorted(by_kind.items())),
        "by_raw_kind": dict(sorted(by_raw_kind.items())),
        "by_confidence": dict(sorted(by_confidence.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "by_effect_status": dict(sorted(by_effect_status.items())),
        "by_other_type": dict(sorted(by_other_type.items())),
        "low_confidence_count": len(low_confidence),
        "missing_confidence_count": len(missing_confidence),
        "empty_evidence_span_count": len(empty_evidence),
        "evidence_span_not_in_context_count": len(evidence_not_in_context),
        "cell_type_like_gene_count": len(cell_type_like_genes),
        "other_fixed_kind_candidate_count": len(other_fixed_kind_candidates),
        "promoted_other_to_fixed_count": len(promoted_other_to_fixed),
        "non_graph_other_count": len(non_graph_other),
        "duplicate_canonical_names_count": len(duplicates),
        "fragment_candidate_count": len(fragment_candidates),
        "unknown_kinds": unknown_kinds,
        "examples": {
            "low_confidence": [compact_entity(entity) for entity in low_confidence[:max_examples]],
            "missing_confidence": [compact_entity(entity) for entity in missing_confidence[:max_examples]],
            "empty_evidence_span": [compact_entity(entity) for entity in empty_evidence[:max_examples]],
            "evidence_span_not_in_context": [
                compact_entity(entity) for entity in evidence_not_in_context[:max_examples]
            ],
            "cell_type_like_genes": cell_type_like_genes[:max_examples],
            "other_fixed_kind_candidates": other_fixed_kind_candidates[:max_examples],
            "promoted_other_to_fixed": promoted_other_to_fixed[:max_examples],
            "non_graph_other": non_graph_other[:max_examples],
            "duplicate_canonical_names": duplicates[:max_examples],
            "fragment_candidates": fragment_candidates[:max_examples],
        },
        "fragment_rules": {
            "word_limit": 10,
            "clause_markers": [marker.strip() for marker in CLAUSE_MARKERS],
            "suspicious_substrings": SUSPICIOUS_SUBSTRINGS,
            "suspicious_starts": list(SUSPICIOUS_STARTS),
        },
    }


def markdown_table(rows: list[tuple[str, object]]) -> str:
    lines = ["| Metric | Value |", "| --- | ---: |"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    normalized = report["normalized"]
    lines = [
        "# BioKG LLM Entity Quality Report",
        "",
        f"- Normalized input: `{normalized['path']}` ({normalized['status']})",
        f"- Raw input: `{report['raw']['path']}` ({report['raw']['status']})",
        "",
    ]
    if normalized["status"] != "present":
        lines.append(report.get("message", "No normalized entity file was loaded."))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    lines.extend(
        [
            markdown_table(
                [
                    ("normalized records", normalized["records"]),
                    ("raw records", report["raw"]["records"]),
                    ("entities", report["entity_count"]),
                    ("Other entities", sum(report["by_kind"].get(kind, 0) for kind in ["Other"])),
                    ("raw kind Other", report["by_raw_kind"].get("other", 0) + report["by_raw_kind"].get("Other", 0)),
                    ("docs with entities", report["docs_with_entities"]),
                    ("records without entities", report["records_without_entities"]),
                    ("low confidence", report["low_confidence_count"]),
                    ("missing confidence", report["missing_confidence_count"]),
                    ("empty evidence spans", report["empty_evidence_span_count"]),
                    ("evidence spans not in context", report["evidence_span_not_in_context_count"]),
                    ("cell-type-like gene entities", report["cell_type_like_gene_count"]),
                    ("Other with fixed-kind type", report["other_fixed_kind_candidate_count"]),
                    ("Other promoted to fixed kind", report["promoted_other_to_fixed_count"]),
                    ("Other excluded from graph", report["non_graph_other_count"]),
                    ("duplicate canonical names", report["duplicate_canonical_names_count"]),
                    ("sentence-fragment candidates", report["fragment_candidate_count"]),
                ]
            ),
            "",
            "## Counts By Kind",
            "",
            json.dumps(report["by_kind"], indent=2, sort_keys=True),
            "",
            "## Counts By Raw Kind",
            "",
            json.dumps(report["by_raw_kind"], indent=2, sort_keys=True),
            "",
            "## Counts By Confidence",
            "",
            json.dumps(report["by_confidence"], indent=2, sort_keys=True),
            "",
            "## Counts By Effect Status",
            "",
            json.dumps(report["by_effect_status"], indent=2, sort_keys=True),
            "",
            "## Other Entities By Proposed Type",
            "",
            json.dumps(report["by_other_type"], indent=2, sort_keys=True),
            "",
            "## Example Flags",
            "",
        ]
    )
    for key, examples in report["examples"].items():
        lines.extend([f"### {key.replace('_', ' ').title()}", ""])
        if examples:
            lines.append("```json")
            lines.append(json.dumps(examples, indent=2, ensure_ascii=False, sort_keys=True))
            lines.append("```")
        else:
            lines.append("None.")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--normalized", type=Path, default=DEFAULT_NORMALIZED)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--max-examples", type=int, default=20)
    parser.add_argument("--require-input", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.normalized, args.raw, max_examples=args.max_examples)
    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    write_markdown(args.out_md, report)
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    if args.require_input and report["normalized"]["status"] != "present":
        raise SystemExit("normalized LLM entity file is missing")


if __name__ == "__main__":
    main()
