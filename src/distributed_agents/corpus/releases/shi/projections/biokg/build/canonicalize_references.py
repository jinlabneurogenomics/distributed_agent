#!/usr/bin/env python3
"""Canonicalize publication references by exact DOI, PMID, or PMCID.

This is deliberately a conservative post-processing step over the packaged
Neo4j CSVs. It does not use fuzzy title matching, URL equality, or external
APIs. Database-record references are excluded unless their URL is itself a
publication locator.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from ..paths import BASE_DATA_DIR


REFERENCE_FIELDS = (
    "doi",
    "pmid",
    "pmcid",
    "reference_resolution",
    "source_targets",
    "local_ref_ids",
)
RELATIONSHIP_FIELDS = ("local_ref_id",)
IDENTIFIER_PRIORITY = ("doi", "pmid", "pmcid")
NON_PUBLICATION_SOURCE_TYPES = {"database", "clinicaltrials"}

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s<>\"']+", re.IGNORECASE)
PMID_RES = (
    re.compile(r"\bPMID\s*[:/]?\s*(\d{5,10})\b", re.IGNORECASE),
    re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{5,10})", re.IGNORECASE),
    re.compile(r"ncbi\.nlm\.nih\.gov/pubmed/(\d{5,10})", re.IGNORECASE),
)
PMCID_RE = re.compile(r"\bPMC\s*[-:]?\s*(\d{4,10})\b", re.IGNORECASE)


@dataclass(frozen=True)
class CanonicalizationResult:
    nodes: list[dict[str, str]]
    relationships: list[dict[str, str]]
    node_fields: list[str]
    relationship_fields: list[str]
    report: dict[str, object]


class UnionFind:
    def __init__(self, items: Iterable[str]) -> None:
        self.parent = {item: item for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[max(left_root, right_root)] = min(left_root, right_root)


def _append_fields(fields: Sequence[str], additions: Sequence[str]) -> list[str]:
    result = list(fields)
    for field in additions:
        if field not in result:
            result.append(field)
    return result


def _is_reference(row: Mapping[str, str]) -> bool:
    labels = {
        label.strip()
        for label in re.split(r"[;|]", row.get("labels", ""))
        if label.strip()
    }
    return row.get("kind", "").strip() == "Reference" or "Reference" in labels


def _trim_doi(value: str) -> str:
    doi = value.strip().lower()
    doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi\s*:\s*)", "", doi)
    doi = doi.split("?", 1)[0].split("#", 1)[0]
    doi = doi.rstrip(".,;:")
    pairs = (("(", ")"), ("[", "]"), ("{", "}"))
    changed = True
    while changed and doi:
        changed = False
        for left, right in pairs:
            if doi.endswith(right) and doi.count(right) > doi.count(left):
                doi = doi[:-1].rstrip()
                changed = True
    doi = re.sub(r"(?:/|\.)(?:full|abstract|pdf|epdf|html)$", "", doi)
    if doi.startswith(("10.1101/", "10.64898/")):
        doi = re.sub(r"v\d+$", "", doi)
    return doi


def _publication_locator(url: str) -> bool:
    lowered = url.casefold()
    return bool(
        "doi.org/" in lowered
        or "pubmed.ncbi.nlm.nih.gov/" in lowered
        or "ncbi.nlm.nih.gov/pubmed/" in lowered
        or "ncbi.nlm.nih.gov/pmc/" in lowered
        or "pmc.ncbi.nlm.nih.gov/" in lowered
    )


def extract_identifiers(row: Mapping[str, str]) -> dict[str, set[str]]:
    """Return normalized exact identifiers eligible for publication resolution."""

    url = row.get("url", "").strip()
    source_types = {
        value.strip().casefold()
        for value in row.get("source_type", "").split("|")
        if value.strip()
    }
    if source_types & NON_PUBLICATION_SOURCE_TYPES and not _publication_locator(url):
        return {namespace: set() for namespace in IDENTIFIER_PRIORITY}

    text = "\n".join(
        value
        for value in (
            row.get("doi", ""),
            row.get("pmid", ""),
            row.get("pmcid", ""),
            url,
            row.get("citation", ""),
        )
        if value
    )

    dois = {_trim_doi(match.group(0)) for match in DOI_RE.finditer(text)}
    dois.discard("")
    pmids = {match.group(1) for pattern in PMID_RES for match in pattern.finditer(text)}
    pmcids = {f"PMC{match.group(1)}" for match in PMCID_RE.finditer(text)}
    return {"doi": dois, "pmid": pmids, "pmcid": pmcids}


def _pipe_values(rows: Iterable[Mapping[str, str]], fields: Sequence[str]) -> str:
    values: set[str] = set()
    for row in rows:
        for field in fields:
            values.update(
                value.strip()
                for value in row.get(field, "").split("|")
                if value.strip()
            )
    return "|".join(sorted(values, key=lambda value: (value.casefold(), value)))


def _best_text(rows: Iterable[Mapping[str, str]], field: str) -> str:
    values = {row.get(field, "").strip() for row in rows if row.get(field, "").strip()}
    if not values:
        return ""
    return sorted(values, key=lambda value: (-len(value), value.casefold(), value))[0]


def _canonical_url(namespace: str, identifier: str) -> str:
    if namespace == "doi":
        return f"https://doi.org/{identifier}"
    if namespace == "pmid":
        return f"https://pubmed.ncbi.nlm.nih.gov/{identifier}/"
    return f"https://pmc.ncbi.nlm.nih.gov/articles/{identifier}/"


def _display_name(namespace: str, identifier: str) -> str:
    labels = {"doi": "DOI", "pmid": "PMID", "pmcid": "PMCID"}
    return f"{labels[namespace]} {identifier}"


def _component_identifiers(
    member_ids: Sequence[str], identifiers: Mapping[str, Mapping[str, set[str]]]
) -> dict[str, list[str]]:
    return {
        namespace: sorted(
            {
                value
                for member_id in member_ids
                for value in identifiers[member_id][namespace]
            },
            key=lambda value: (value.casefold(), value),
        )
        for namespace in IDENTIFIER_PRIORITY
    }


def canonicalize_rows(
    nodes: Sequence[Mapping[str, str]],
    relationships: Sequence[Mapping[str, str]],
    node_fields: Sequence[str],
    relationship_fields: Sequence[str],
) -> CanonicalizationResult:
    """Canonicalize reference rows and retarget relationships deterministically."""

    if "id" not in node_fields:
        raise ValueError("Node CSV must contain an 'id' column")
    for field in ("start_id", "end_id", "type"):
        if field not in relationship_fields:
            raise ValueError(f"Relationship CSV must contain a {field!r} column")

    copied_nodes = [{key: value or "" for key, value in row.items()} for row in nodes]
    copied_relationships = [
        {key: value or "" for key, value in row.items()} for row in relationships
    ]
    node_by_id: dict[str, dict[str, str]] = {}
    for row in copied_nodes:
        node_id = row.get("id", "")
        if not node_id:
            raise ValueError("Node CSV contains an empty id")
        if node_id in node_by_id:
            raise ValueError(f"Duplicate node id: {node_id}")
        node_by_id[node_id] = row

    reference_ids = [row["id"] for row in copied_nodes if _is_reference(row)]
    reference_set = set(reference_ids)
    identifiers = {
        node_id: extract_identifiers(node_by_id[node_id]) for node_id in reference_ids
    }

    row_conflicts = {
        node_id
        for node_id, values in identifiers.items()
        if any(len(values[namespace]) > 1 for namespace in IDENTIFIER_PRIORITY)
    }
    eligible_ids = [
        node_id
        for node_id in reference_ids
        if node_id not in row_conflicts
        and any(identifiers[node_id][namespace] for namespace in IDENTIFIER_PRIORITY)
    ]

    union_find = UnionFind(eligible_ids)
    first_by_identifier: dict[tuple[str, str], str] = {}
    for node_id in eligible_ids:
        for namespace in IDENTIFIER_PRIORITY:
            for value in identifiers[node_id][namespace]:
                key = (namespace, value)
                first = first_by_identifier.setdefault(key, node_id)
                union_find.union(first, node_id)

    raw_components: dict[str, list[str]] = {}
    for node_id in eligible_ids:
        raw_components.setdefault(union_find.find(node_id), []).append(node_id)

    resolved_components: list[tuple[list[str], dict[str, list[str]]]] = []
    component_conflicts: list[dict[str, object]] = []
    for member_ids in raw_components.values():
        member_ids = sorted(member_ids)
        component_ids = _component_identifiers(member_ids, identifiers)
        if any(len(component_ids[namespace]) > 1 for namespace in IDENTIFIER_PRIORITY):
            component_conflicts.append(
                {"members": member_ids, "identifiers": component_ids}
            )
            continue
        resolved_components.append((member_ids, component_ids))

    if row_conflicts:
        for node_id in sorted(row_conflicts):
            component_conflicts.append(
                {
                    "members": [node_id],
                    "identifiers": {
                        namespace: sorted(identifiers[node_id][namespace])
                        for namespace in IDENTIFIER_PRIORITY
                    },
                }
            )

    output_node_fields = _append_fields(node_fields, REFERENCE_FIELDS)
    output_relationship_fields = _append_fields(
        relationship_fields, RELATIONSHIP_FIELDS
    )
    id_map = {node_id: node_id for node_id in node_by_id}
    canonical_by_member: dict[str, dict[str, str]] = {}
    component_size: dict[str, int] = {}
    mapping: list[dict[str, str]] = []
    largest_groups: list[dict[str, object]] = []

    for member_ids, component_ids in resolved_components:
        namespace = next(
            candidate for candidate in IDENTIFIER_PRIORITY if component_ids[candidate]
        )
        identifier = component_ids[namespace][0]
        canonical_id = f"reference:{namespace}:{identifier}"
        if canonical_id in node_by_id and canonical_id not in member_ids:
            raise ValueError(
                f"Canonical reference id collides with another node: {canonical_id}"
            )

        member_rows = [node_by_id[node_id] for node_id in member_ids]
        representative = sorted(
            member_rows,
            key=lambda row: (
                -sum(
                    len(row.get(field, ""))
                    for field in ("citation", "description", "url")
                ),
                row["id"],
            ),
        )[0]
        canonical = {
            field: representative.get(field, "") for field in output_node_fields
        }
        canonical_updates = {
                "id": canonical_id,
                "name": _display_name(namespace, identifier),
                "target_gene": "",
                "source_target": "",
                "ref_id": "",
                "citation": _best_text(member_rows, "citation"),
                "description": _best_text(member_rows, "description"),
                "url": _canonical_url(namespace, identifier),
                "source": _pipe_values(member_rows, ("source",)),
                "source_type": _pipe_values(member_rows, ("source_type",)),
                "doi": component_ids["doi"][0] if component_ids["doi"] else "",
                "pmid": component_ids["pmid"][0] if component_ids["pmid"] else "",
                "pmcid": component_ids["pmcid"][0] if component_ids["pmcid"] else "",
                "reference_resolution": f"exact_{namespace}",
                "source_targets": _pipe_values(
                    member_rows, ("source_targets", "source_target", "target_gene")
                ),
                "local_ref_ids": _pipe_values(member_rows, ("local_ref_ids", "ref_id")),
        }
        canonical.update(
            {
                key: value
                for key, value in canonical_updates.items()
                if key in output_node_fields
            }
        )

        component_size[canonical_id] = len(member_ids)
        for member_id in member_ids:
            id_map[member_id] = canonical_id
            canonical_by_member[member_id] = canonical
            source_row = node_by_id[member_id]
            mapping.append(
                {
                    "old_id": member_id,
                    "new_id": canonical_id,
                    "source_target": source_row.get("source_target", "")
                    or source_row.get("target_gene", ""),
                    "local_ref_id": source_row.get("ref_id", ""),
                    "method": f"exact_{namespace}",
                }
            )
        if len(member_ids) > 1:
            largest_groups.append(
                {
                    "canonical_id": canonical_id,
                    "member_count": len(member_ids),
                    "members": member_ids,
                    "identifiers": component_ids,
                }
            )

    output_nodes: list[dict[str, str]] = []
    emitted_canonical_ids: set[str] = set()
    conflict_members = {
        member
        for conflict in component_conflicts
        for member in conflict["members"]  # type: ignore[index]
    }
    for row in copied_nodes:
        node_id = row["id"]
        if node_id in canonical_by_member:
            canonical = canonical_by_member[node_id]
            canonical_id = canonical["id"]
            if canonical_id not in emitted_canonical_ids:
                output_nodes.append(canonical.copy())
                emitted_canonical_ids.add(canonical_id)
            continue
        output = {field: row.get(field, "") for field in output_node_fields}
        if node_id in reference_set:
            output["reference_resolution"] = (
                "conflict" if node_id in conflict_members else "unresolved"
            )
        output_nodes.append(output)

    output_relationships: list[dict[str, str]] = []
    cites_before = 0
    cites_with_local_ref_id = 0
    for row in copied_relationships:
        output = {field: row.get(field, "") for field in output_relationship_fields}
        original_end_id = output["end_id"]
        if output["type"] == "CITES":
            cites_before += 1
            if not output.get("local_ref_id") and original_end_id in node_by_id:
                original_reference = node_by_id[original_end_id]
                local_ref_id = original_reference.get("ref_id", "")
                if not local_ref_id:
                    known_ids = [
                        value
                        for value in original_reference.get("local_ref_ids", "").split(
                            "|"
                        )
                        if value
                    ]
                    if len(known_ids) == 1:
                        local_ref_id = known_ids[0]
                output["local_ref_id"] = local_ref_id
            if output.get("local_ref_id"):
                cites_with_local_ref_id += 1
        output["start_id"] = id_map.get(output["start_id"], output["start_id"])
        output["end_id"] = id_map.get(output["end_id"], output["end_id"])
        output_relationships.append(output)

    output_ids = {row["id"] for row in output_nodes}
    dangling = [
        {
            "start_id": row["start_id"],
            "end_id": row["end_id"],
            "type": row["type"],
        }
        for row in output_relationships
        if row["start_id"] not in output_ids or row["end_id"] not in output_ids
    ]
    if dangling:
        sample = dangling[:3]
        raise ValueError(
            f"Canonicalization would create dangling relationships: {sample}"
        )

    largest_groups.sort(
        key=lambda group: (-int(group["member_count"]), str(group["canonical_id"]))
    )
    mapping.sort(key=lambda item: item["old_id"])
    resolved_members = len(canonical_by_member)
    merged_components = sum(size > 1 for size in component_size.values())
    report: dict[str, object] = {
        "schema_version": 1,
        "scope": (
            "Exact publication identifiers only (DOI, PMID, PMCID); "
            "no fuzzy matching or external lookup"
        ),
        "references_before": len(reference_ids),
        "references_after": len(reference_ids) - resolved_members + len(component_size),
        "reference_nodes_removed": resolved_members - len(component_size),
        "resolved_input_references": resolved_members,
        "canonical_references": len(component_size),
        "merged_components": merged_components,
        "renamed_singletons": sum(size == 1 for size in component_size.values()),
        "unresolved_references": len(reference_ids)
        - resolved_members
        - len(conflict_members),
        "conflicting_references": len(conflict_members),
        "conflicting_components": component_conflicts,
        "nodes_before": len(copied_nodes),
        "nodes_after": len(output_nodes),
        "relationships_before": len(copied_relationships),
        "relationships_after": len(output_relationships),
        "cites_before": cites_before,
        "cites_after": sum(row["type"] == "CITES" for row in output_relationships),
        "cites_with_local_ref_id": cites_with_local_ref_id,
        "dangling_relationships": 0,
        "largest_merged_groups": largest_groups[:25],
        "mapping": mapping,
    }
    return CanonicalizationResult(
        nodes=output_nodes,
        relationships=output_relationships,
        node_fields=output_node_fields,
        relationship_fields=output_relationship_fields,
        report=report,
    )


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return list(reader.fieldnames), list(reader)


def _write_csv_temp(
    path: Path, fields: Sequence[str], rows: Sequence[Mapping[str, str]]
) -> Path:
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        newline="",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        return temp_path
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def _write_json_atomic(path: Path, value: Mapping[str, object]) -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def _default_csv_dir() -> Path:
    return BASE_DATA_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-dir", type=Path, default=_default_csv_dir())
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Replace nodes.merged.csv and relationships.merged.csv in place",
    )
    args = parser.parse_args()

    csv.field_size_limit(sys.maxsize)
    nodes_path = args.csv_dir / "nodes.merged.csv"
    relationships_path = args.csv_dir / "relationships.merged.csv"
    report_path = args.csv_dir / "reference_canonicalization_report.json"
    node_fields, nodes = _read_csv(nodes_path)
    relationship_fields, relationships = _read_csv(relationships_path)
    result = canonicalize_rows(nodes, relationships, node_fields, relationship_fields)

    files_changed = bool(
        result.node_fields != node_fields
        or result.relationship_fields != relationship_fields
        or result.nodes != nodes
        or result.relationships != relationships
    )
    report_written = False
    if args.apply:
        if files_changed:
            nodes_temp = _write_csv_temp(nodes_path, result.node_fields, result.nodes)
            relationships_temp = _write_csv_temp(
                relationships_path, result.relationship_fields, result.relationships
            )
            try:
                os.replace(nodes_temp, nodes_path)
                os.replace(relationships_temp, relationships_path)
            finally:
                nodes_temp.unlink(missing_ok=True)
                relationships_temp.unlink(missing_ok=True)
        # Preserve the original old-to-canonical audit mapping on idempotent rebuilds.
        if files_changed or not report_path.exists():
            _write_json_atomic(report_path, result.report)
            report_written = True

    summary = {
        key: result.report[key]
        for key in (
            "references_before",
            "references_after",
            "reference_nodes_removed",
            "canonical_references",
            "merged_components",
            "renamed_singletons",
            "unresolved_references",
            "conflicting_references",
            "cites_before",
            "cites_after",
            "cites_with_local_ref_id",
            "dangling_relationships",
        )
    }
    summary["mode"] = "apply" if args.apply else "dry-run"
    summary["files_changed"] = files_changed
    if args.apply:
        summary["report"] = str(report_path)
        summary["report_written"] = report_written
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
