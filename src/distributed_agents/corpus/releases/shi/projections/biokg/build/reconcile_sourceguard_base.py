#!/usr/bin/env python3
"""Replace changed target slices in the legacy BioKG base with Sourceguard rows."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping

from .build_biokg_v2 import (
    as_list,
    measured_gene_effect,
    normalize_gene_symbol,
    normalize_text,
    parse_report_appendices,
    stable_id,
)
from ..paths import BASE_DATA_DIR, MEASURED_UNIVERSE_FILE, RELEASE_ROOT


FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
EVIDENCE = RELEASE_ROOT / "artifacts" / "ledgers" / "evidence.csv"
REFERENCES = RELEASE_ROOT / "artifacts" / "ledgers" / "references.csv"
REPORTS = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
PUBLICATION_MAP = RELEASE_ROOT / "artifacts" / "contracts" / "publication_reference_mapping.json"
CHANGED_TARGETS = RELEASE_ROOT / "provenance" / "sourceguard_replacement_targets.txt"
NODES = BASE_DATA_DIR / "nodes.merged.csv"
RELATIONSHIPS = BASE_DATA_DIR / "relationships.merged.csv"

CONCEPT_KINDS = {"Pathway", "Complex", "Module", "Other", "Phenotype"}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def split_pipe(value: object) -> list[str]:
    return list(dict.fromkeys(part.strip() for part in str(value or "").split("|") if part.strip()))


def pipe_join(values: Iterable[object], *, sort: bool = False) -> str:
    unique = list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))
    if sort:
        unique.sort(key=lambda value: (value.casefold(), value))
    return "|".join(unique)


def empty_row(fields: list[str]) -> dict[str, str]:
    return {field: "" for field in fields}


def node_row(
    fields: list[str],
    *,
    node_id: str,
    kind: str,
    name: str,
    labels: Iterable[str],
    props: Mapping[str, object] | None = None,
) -> dict[str, str]:
    row = empty_row(fields)
    row.update(
        {
            "id": node_id,
            "kind": kind,
            "labels": ";".join(labels),
            "name": name,
        }
    )
    for key, value in (props or {}).items():
        if key in row:
            row[key] = normalize_text(value)
    return row


def relationship_row(
    fields: list[str],
    start_id: str,
    end_id: str,
    relation_type: str,
    props: Mapping[str, object] | None = None,
) -> dict[str, str]:
    row = empty_row(fields)
    row.update({"start_id": start_id, "end_id": end_id, "type": relation_type})
    for key, value in (props or {}).items():
        if key in row:
            row[key] = normalize_text(value)
    return row


def write_csv(path: Path, fields: list[str], rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def best_text(rows: Iterable[Mapping[str, str]], field: str) -> str:
    values = {row.get(field, "").strip() for row in rows if row.get(field, "").strip()}
    return sorted(values, key=lambda value: (-len(value), value.casefold(), value))[0] if values else ""


def canonical_name(canonical_id: str) -> str:
    _, namespace, identifier = canonical_id.split(":", 2)
    return f"{namespace.upper()} {identifier}"


def canonical_url(canonical: Mapping[str, object]) -> str:
    if canonical.get("doi"):
        return f"https://doi.org/{canonical['doi']}"
    if canonical.get("pmid"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{canonical['pmid']}/"
    return f"https://pmc.ncbi.nlm.nih.gov/articles/{canonical['pmcid']}/"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    changed_targets = set(CHANGED_TARGETS.read_text(encoding="utf-8").split())
    measured_universe = {
        line.strip().casefold()
        for line in MEASURED_UNIVERSE_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    node_fields, old_nodes = read_csv(NODES)
    relationship_fields, old_relationships = read_csv(RELATIONSHIPS)

    removed_node_ids = {
        row["id"]
        for row in old_nodes
        if row.get("kind") == "Reference" or row.get("target_gene") in changed_targets
    }
    nodes = {
        row["id"]: row for row in old_nodes if row["id"] not in removed_node_ids
    }
    relationships = [
        row
        for row in old_relationships
        if row["start_id"] not in removed_node_ids
        and row["end_id"] not in removed_node_ids
        and row["type"] != "CITES"
    ]
    relationship_keys = {tuple(row[field] for field in relationship_fields) for row in relationships}

    def add_node(row: dict[str, str]) -> None:
        existing = nodes.get(row["id"])
        if existing is not None and existing != row:
            raise ValueError(f"node collision: {row['id']}")
        nodes[row["id"]] = row

    def add_relationship(row: dict[str, str]) -> None:
        key = tuple(row[field] for field in relationship_fields)
        if key not in relationship_keys:
            relationships.append(row)
            relationship_keys.add(key)

    def ensure_cell(cell: str) -> str:
        node_id = stable_id("cell_type", cell)
        if node_id not in nodes:
            add_node(
                node_row(
                    node_fields,
                    node_id=node_id,
                    kind="CellType",
                    name=cell,
                    labels=("BioKGNode", "CellType"),
                    props={"cell_type": cell},
                )
            )
        return node_id

    def ensure_gene(gene: str, *, target: bool = False) -> str | None:
        symbol = normalize_gene_symbol(gene)
        if not symbol or (not target and symbol.casefold() not in measured_universe):
            return None
        node_id = stable_id("gene", symbol)
        if node_id not in nodes:
            labels = ["BioKGNode", "Gene"]
            if target:
                labels.append("TargetGene")
            add_node(
                node_row(
                    node_fields,
                    node_id=node_id,
                    kind="Gene",
                    name=symbol,
                    labels=labels,
                    props={"symbol": symbol},
                )
            )
        return node_id

    _, current_findings = read_csv(FINDINGS)
    _, current_evidence = read_csv(EVIDENCE)
    _, current_references = read_csv(REFERENCES)
    findings_by_doc = {
        f"{row['target_gene']}:{row['finding_id']}": row for row in current_findings
    }
    evidence_by_source_id = {
        f"{row['target_gene']}:{row['evidence_id']}": row for row in current_evidence
    }
    references_by_source_id = {
        f"{row['target_gene']}:{row['ref_id']}": row for row in current_references
    }

    publication_map = json.loads(PUBLICATION_MAP.read_text(encoding="utf-8"))
    mapping_by_source_id = {
        row["source_reference_id"]: row for row in publication_map["mappings"]
    }
    if set(mapping_by_source_id) != set(references_by_source_id):
        raise ValueError("publication mapping and Reference ledger do not cover the same rows")

    canonical_groups: dict[str, list[tuple[dict, dict[str, str]]]] = defaultdict(list)
    reference_node_by_source_id: dict[str, str] = {}
    for source_id, source_row in references_by_source_id.items():
        mapping = mapping_by_source_id[source_id]
        canonical = mapping.get("canonical")
        if canonical:
            canonical_id = canonical["id"]
            canonical_groups[canonical_id].append((mapping, source_row))
            reference_node_by_source_id[source_id] = canonical_id
            continue
        local_id = stable_id("reference", source_id)
        reference_node_by_source_id[source_id] = local_id
        add_node(
            node_row(
                node_fields,
                node_id=local_id,
                kind="Reference",
                name=source_id,
                labels=("BioKGNode", "Reference"),
                props={
                    **source_row,
                    "reference_resolution": mapping["resolution"],
                },
            )
        )

    for canonical_id, group in sorted(canonical_groups.items()):
        mappings = [mapping for mapping, _ in group]
        source_rows = [source for _, source in group]
        canonical = mappings[0]["canonical"]
        add_node(
            node_row(
                node_fields,
                node_id=canonical_id,
                kind="Reference",
                name=canonical_name(canonical_id),
                labels=("BioKGNode", "Reference"),
                props={
                    "citation": best_text(source_rows, "citation"),
                    "description": best_text(source_rows, "description"),
                    "url": canonical_url(canonical),
                    "source": pipe_join((row["source"] for row in source_rows), sort=True),
                    "source_type": pipe_join((row["source_type"] for row in source_rows), sort=True),
                    "doi": canonical.get("doi") or "",
                    "pmid": canonical.get("pmid") or "",
                    "pmcid": canonical.get("pmcid") or "",
                    "reference_resolution": mappings[0]["resolution"],
                    "source_targets": pipe_join((row["target_gene"] for row in source_rows), sort=True),
                    "local_ref_ids": pipe_join((row["ref_id"] for row in source_rows), sort=True),
                },
            )
        )

    for source_id, row in evidence_by_source_id.items():
        if row["target_gene"] not in changed_targets:
            continue
        evidence_id = stable_id("evidence", source_id)
        add_node(
            node_row(
                node_fields,
                node_id=evidence_id,
                kind="Evidence",
                name=source_id,
                labels=("BioKGNode", "Evidence"),
                props=row,
            )
        )
        for cell in split_pipe(row["cell_type"]):
            add_relationship(
                relationship_row(
                    relationship_fields,
                    evidence_id,
                    ensure_cell(cell),
                    "DESCRIBES_CELL_TYPE",
                )
            )
        evidence_genes = split_pipe(row["genes"])
        raw_gene_set = set(evidence_genes)
        for gene in evidence_genes:
            if gene.casefold() == row["target_gene"].casefold():
                continue
            gene_id = ensure_gene(gene)
            if gene_id is None:
                continue
            add_relationship(
                relationship_row(
                    relationship_fields,
                    evidence_id,
                    gene_id,
                    "MEASURED_GENE",
                    measured_gene_effect(row["statistics"], gene, raw_gene_set),
                )
            )

    for doc_id, row in findings_by_doc.items():
        if row["target_gene"] not in changed_targets:
            continue
        finding_id = stable_id("finding", doc_id)
        target_id = ensure_gene(row["target_gene"], target=True)
        if target_id is None:
            raise ValueError(f"unable to materialize target: {row['target_gene']}")
        add_node(
            node_row(
                node_fields,
                node_id=finding_id,
                kind="Finding",
                name=doc_id,
                labels=("BioKGNode", "Finding"),
                props={
                    **row,
                    "doc_id": doc_id,
                    "text": f"{row['summary']} {row['why_it_matters']}",
                    "extractor": "sourceguard_ledger_overlay",
                },
            )
        )
        add_relationship(relationship_row(relationship_fields, target_id, finding_id, "HAS_FINDING"))
        add_relationship(relationship_row(relationship_fields, finding_id, target_id, "HAS_TARGET"))
        add_relationship(
            relationship_row(relationship_fields, finding_id, "assay:perturb_seq", "USES_ASSAY")
        )
        for cell in split_pipe(row["cell_types"]):
            add_relationship(
                relationship_row(relationship_fields, finding_id, ensure_cell(cell), "OBSERVED_IN")
            )
        for gene in split_pipe(row["genes"]) + split_pipe(row["comparators"]):
            if gene.casefold() == row["target_gene"].casefold():
                continue
            gene_id = ensure_gene(gene)
            if gene_id is not None:
                add_relationship(
                    relationship_row(
                        relationship_fields,
                        finding_id,
                        gene_id,
                        "REPORTS_GENE",
                        {"role": "finding_reported_gene"},
                    )
                )
        for evidence_id in split_pipe(row["evidence_ids"]):
            source_id = f"{row['target_gene']}:{evidence_id}"
            if source_id not in evidence_by_source_id:
                raise ValueError(f"Finding references missing Evidence: {doc_id} -> {source_id}")
            add_relationship(
                relationship_row(
                    relationship_fields,
                    finding_id,
                    stable_id("evidence", source_id),
                    "SUPPORTED_BY",
                )
            )

    parsed_reports: dict[str, dict] = {}
    for report in read_jsonl(REPORTS):
        target = report["gene_target"]
        parsed = parse_report_appendices(report)
        parsed_reports[target] = parsed
        if target not in changed_targets:
            continue
        for comparison in parsed["sections"].get("literature_comparisons", []):
            source_id = f"{target}:{comparison['comparison_id']}"
            comparison_id = stable_id("literature_comparison", source_id)
            finding_source_id = f"{target}:{comparison['finding_id']}"
            if finding_source_id not in findings_by_doc:
                raise ValueError(f"LiteratureComparison references missing Finding: {source_id}")
            add_node(
                node_row(
                    node_fields,
                    node_id=comparison_id,
                    kind="LiteratureComparison",
                    name=source_id,
                    labels=("BioKGNode", "LiteratureComparison"),
                    props={
                        "target_gene": target,
                        "comparison_id": comparison["comparison_id"],
                        "finding_id": comparison["finding_id"],
                        "summary": comparison.get("dataset_claim", ""),
                        "description": comparison.get("literature_claim", ""),
                        "literature_status": comparison.get("relationship_to_literature", ""),
                        "confidence": comparison.get("confidence", ""),
                    },
                )
            )
            add_relationship(
                relationship_row(
                    relationship_fields,
                    stable_id("finding", finding_source_id),
                    comparison_id,
                    "HAS_LITERATURE_COMPARISON",
                )
            )
            for evidence_id in as_list(comparison.get("evidence_ids")):
                add_relationship(
                    relationship_row(
                        relationship_fields,
                        comparison_id,
                        stable_id("evidence", f"{target}:{evidence_id}"),
                        "SUPPORTED_BY",
                    )
                )

    for doc_id, row in findings_by_doc.items():
        finding_node_id = stable_id("finding", doc_id)
        for ref_id in split_pipe(row["ref_ids"]):
            source_id = f"{row['target_gene']}:{ref_id}"
            add_relationship(
                relationship_row(
                    relationship_fields,
                    finding_node_id,
                    reference_node_by_source_id[source_id],
                    "CITES",
                    {"local_ref_id": ref_id},
                )
            )
    for target, parsed in parsed_reports.items():
        for comparison in parsed["sections"].get("literature_comparisons", []):
            comparison_node_id = stable_id(
                "literature_comparison", f"{target}:{comparison['comparison_id']}"
            )
            if comparison_node_id not in nodes:
                continue
            for ref_id in as_list(comparison.get("ref_ids")):
                source_id = f"{target}:{ref_id}"
                add_relationship(
                    relationship_row(
                        relationship_fields,
                        comparison_node_id,
                        reference_node_by_source_id[source_id],
                        "CITES",
                        {"local_ref_id": ref_id},
                    )
                )

    endpoints = {
        endpoint
        for row in relationships
        for endpoint in (row["start_id"], row["end_id"])
    }
    orphan_concepts = {
        node_id
        for node_id, row in nodes.items()
        if row["kind"] in CONCEPT_KINDS and node_id not in endpoints
    }
    for node_id in orphan_concepts:
        del nodes[node_id]

    dangling = [
        row
        for row in relationships
        if row["start_id"] not in nodes or row["end_id"] not in nodes
    ]
    if dangling:
        raise ValueError(f"reconciled graph contains {len(dangling)} dangling relationships")

    sorted_nodes = sorted(nodes.values(), key=lambda row: row["id"])
    sorted_relationships = sorted(
        relationships,
        key=lambda row: (row["start_id"], row["type"], row["end_id"], row.get("local_ref_id", "")),
    )
    write_csv(NODES, node_fields, sorted_nodes)
    write_csv(RELATIONSHIPS, relationship_fields, sorted_relationships)

    node_counts = Counter(row["kind"] for row in sorted_nodes)
    relationship_counts = Counter(row["type"] for row in sorted_relationships)
    report = {
        "nodes": len(sorted_nodes),
        "relationships": len(sorted_relationships),
        "node_kinds": dict(sorted(node_counts.items())),
        "relationship_types": dict(sorted(relationship_counts.items())),
        "changed_targets": len(changed_targets),
        "removed_legacy_target_nodes": len(removed_node_ids),
        "removed_orphan_concepts": len(orphan_concepts),
        "references": node_counts["Reference"],
        "publication_mapping": publication_map["summary"],
        "nodes_sha256": sha256(NODES),
        "relationships_sha256": sha256(RELATIONSHIPS),
    }
    (BASE_DATA_DIR / "sourceguard_overlay_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (BASE_DATA_DIR / "reference_canonicalization_report.json").write_text(
        json.dumps(
            {
                "summary": {
                    **publication_map["summary"],
                    "reference_nodes": node_counts["Reference"],
                    "cites_relationships": relationship_counts["CITES"],
                }
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (BASE_DATA_DIR / "merge_report.json").write_text(
        json.dumps(
            {
                "summary": {
                    "nodes": len(sorted_nodes),
                    "relationships": len(sorted_relationships),
                    "node_kinds": dict(sorted(node_counts.items())),
                    "relationship_types": dict(sorted(relationship_counts.items())),
                },
                "nodes_sha256": report["nodes_sha256"],
                "relationships_sha256": report["relationships_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
