#!/usr/bin/env python3
"""Build Shi holdout relationships using the original BioKG edge vocabulary.

The source-link relationships preserve the original direction, role names, and
common source properties. Explicit Finding comparator annotations are
projected as ``Finding -[:REPORTS_GENE]-> Gene`` with the legacy
``finding_reported_comparator`` role. Frozen Claim contributions are projected
as ``Finding -[:EXPRESSES_CLAIM]-> Claim`` with their adjudicated role and
rationale.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

try:
    from .build_nodes import comparator_symbols, normalize_gene_symbol
except ImportError:  # Direct-script compatibility.
    from build_nodes import comparator_symbols, normalize_gene_symbol


PROJECTION_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_ROOT = PROJECTION_ROOT.parents[1]
DEFAULT_NODES = PROJECTION_ROOT / "data" / "base" / "nodes.jsonl"
DEFAULT_OUTPUT_DIR = PROJECTION_ROOT / "data" / "base"
FINDINGS_PATH = Path("artifacts/ledgers/findings.jsonl")
CLAIM_CONTRIBUTIONS_PATH = Path("artifacts/claims/contributions.jsonl")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_jsonl(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            yield line_number, row


def require_text(row: dict[str, Any], field: str, *, location: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{location}: {field} must be a non-empty string")
    return value


def load_nodes(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    node_types: dict[str, str] = {}
    gene_node_ids: dict[str, str] = {}
    for line_number, node in iter_jsonl(path):
        location = f"{path}:{line_number}"
        node_id = require_text(node, "id", location=location)
        node_type = require_text(node, "type", location=location)
        if node_id in node_types:
            raise ValueError(f"{location}: duplicate node ID {node_id!r}")
        node_types[node_id] = node_type
        if node_type in {"Gene", "TargetGene"}:
            properties = node.get("properties")
            if not isinstance(properties, dict):
                raise ValueError(f"{location}: properties must be an object")
            symbol = require_text(properties, "symbol", location=location)
            key = normalize_gene_symbol(symbol).casefold()
            previous = gene_node_ids.get(key)
            if previous is not None:
                raise ValueError(
                    f"{location}: duplicate canonical gene symbol {symbol!r} "
                    f"on {previous!r} and {node_id!r}"
                )
            gene_node_ids[key] = node_id
    return node_types, gene_node_ids


def relationship(
    start_id: str,
    end_id: str,
    rel_type: str,
    base_properties: dict[str, str],
    role: str,
) -> dict[str, Any]:
    return {
        "end_id": end_id,
        "properties": base_properties | {"role": role},
        "start_id": start_id,
        "type": rel_type,
    }


def build_relationships(
    release_root: Path,
    nodes_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Build exact legacy-language relationships and their build record."""

    release_root = release_root.resolve()
    nodes_path = nodes_path.resolve()
    output_dir = output_dir.resolve()
    findings_path = release_root / FINDINGS_PATH
    claim_contributions_path = release_root / CLAIM_CONTRIBUTIONS_PATH
    if not nodes_path.is_file():
        raise FileNotFoundError(f"missing node source: {nodes_path}")
    if not findings_path.is_file():
        raise FileNotFoundError(f"missing findings source: {findings_path}")
    if not claim_contributions_path.is_file():
        raise FileNotFoundError(
            f"missing Claim contribution source: {claim_contributions_path}"
        )

    node_types, gene_node_ids = load_nodes(nodes_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    relationships_path = output_dir / "relationships.jsonl"
    temporary_path = output_dir / ".relationships.jsonl.tmp"
    build_path = output_dir / "relationship_build.json"

    counts: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    seen: set[tuple[str, str, str, str]] = set()
    dangling_endpoints: set[str] = set()

    def emit(handle: Any, item: dict[str, Any]) -> None:
        role = str(item["properties"]["role"])
        key = (str(item["start_id"]), str(item["end_id"]), str(item["type"]), role)
        if key in seen:
            raise ValueError(f"duplicate relationship: {key}")
        seen.add(key)
        for endpoint in key[:2]:
            if endpoint not in node_types:
                dangling_endpoints.add(endpoint)
        handle.write(canonical_json(item) + "\n")
        counts[str(item["type"])] += 1
        roles[role] += 1

    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
            for line_number, finding in iter_jsonl(findings_path):
                location = f"{findings_path}:{line_number}"
                target = require_text(finding, "target_gene", location=location)
                doc_id = require_text(finding, "doc_id", location=location)
                finding_id = require_text(finding, "finding_id", location=location)
                confidence = require_text(finding, "confidence", location=location)
                expected_doc_id = f"{target}:{finding_id}"
                if doc_id != expected_doc_id:
                    raise ValueError(
                        f"{location}: doc_id {doc_id!r} != {expected_doc_id!r}"
                    )

                target_node_id = f"target_gene:{target}"
                finding_node_id = f"finding:{doc_id}"
                base_properties = {
                    "confidence": confidence,
                    "finding_id": finding_id,
                    "source_doc": doc_id,
                }
                emit(
                    handle,
                    relationship(
                        target_node_id,
                        finding_node_id,
                        "HAS_FINDING",
                        base_properties,
                        "target_to_finding",
                    ),
                )
                emit(
                    handle,
                    relationship(
                        finding_node_id,
                        target_node_id,
                        "HAS_TARGET",
                        base_properties,
                        "finding_target",
                    ),
                )

                seen_comparators: set[str] = set()
                target_key = normalize_gene_symbol(target).casefold()
                for comparator in comparator_symbols(finding, location=location):
                    comparator_key = comparator.casefold()
                    if (
                        comparator_key == target_key
                        or comparator_key in seen_comparators
                    ):
                        continue
                    seen_comparators.add(comparator_key)
                    comparator_node_id = gene_node_ids.get(comparator_key)
                    if comparator_node_id is None:
                        raise ValueError(
                            f"{location}: missing canonical Gene node for comparator "
                            f"{comparator!r}"
                        )
                    emit(
                        handle,
                        relationship(
                            finding_node_id,
                            comparator_node_id,
                            "REPORTS_GENE",
                            base_properties,
                            "finding_reported_comparator",
                        ),
                    )

                for evidence_id in finding.get("evidence_ids") or []:
                    emit(
                        handle,
                        relationship(
                            finding_node_id,
                            f"evidence:{target}:{evidence_id}",
                            "SUPPORTED_BY",
                            base_properties,
                            "evidence",
                        ),
                    )
                for ref_id in finding.get("ref_ids") or []:
                    emit(
                        handle,
                        relationship(
                            finding_node_id,
                            f"reference:{target}:{ref_id}",
                            "CITES",
                            base_properties,
                            "reference",
                        ),
                    )

            for line_number, contribution in iter_jsonl(
                claim_contributions_path
            ):
                location = f"{claim_contributions_path}:{line_number}"
                finding_doc_id = require_text(
                    contribution, "finding_doc_id", location=location
                )
                target = require_text(
                    contribution, "target_gene", location=location
                )
                finding_id = require_text(
                    contribution, "finding_id", location=location
                )
                claim_id = require_text(
                    contribution, "claim_id", location=location
                )
                claim_scope = require_text(
                    contribution, "claim_scope", location=location
                )
                role = require_text(contribution, "role", location=location)
                rationale = require_text(
                    contribution, "rationale", location=location
                )
                expected_doc_id = f"{target}:{finding_id}"
                if finding_doc_id != expected_doc_id:
                    raise ValueError(
                        f"{location}: finding_doc_id {finding_doc_id!r} "
                        f"!= {expected_doc_id!r}"
                    )
                if claim_scope != "corpus":
                    raise ValueError(
                        f"{location}: unsupported claim_scope {claim_scope!r}"
                    )
                finding_node_id = f"finding:{finding_doc_id}"
                if node_types.get(finding_node_id) != "Finding":
                    raise ValueError(
                        f"{location}: invalid Finding endpoint {finding_node_id!r}"
                    )
                if node_types.get(claim_id) != "Claim":
                    raise ValueError(
                        f"{location}: invalid Claim endpoint {claim_id!r}"
                    )
                emit(
                    handle,
                    relationship(
                        finding_node_id,
                        claim_id,
                        "EXPRESSES_CLAIM",
                        {
                            "claim_id": claim_id,
                            "finding_id": finding_id,
                            "rationale": rationale,
                            "source_doc": finding_doc_id,
                        },
                        role,
                    ),
                )
        if dangling_endpoints:
            sample = sorted(dangling_endpoints)[:10]
            raise ValueError(
                f"{len(dangling_endpoints)} dangling relationship endpoints: {sample}"
            )
        temporary_path.replace(relationships_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise

    build_record = {
        "build_policy": {
            "edge_vocabulary": "legacy_biokg_v2_subset_plus_frozen_claims_v1",
            "model_calls": False,
            "network": False,
            "semantic_extraction": False,
        },
        "dangling_endpoints": 0,
        "input": {
            "findings": {
                "path": FINDINGS_PATH.as_posix(),
                "records": counts["HAS_FINDING"],
                "sha256": sha256_file(findings_path),
            },
            "claim_contributions": {
                "path": CLAIM_CONTRIBUTIONS_PATH.as_posix(),
                "records": counts["EXPRESSES_CLAIM"],
                "sha256": sha256_file(claim_contributions_path),
            },
            "nodes": {
                "records": len(node_types),
                "sha256": sha256_file(nodes_path),
            },
        },
        "output": {
            "bytes": relationships_path.stat().st_size,
            "path": "relationships.jsonl",
            "records": sum(counts.values()),
            "sha256": sha256_file(relationships_path),
        },
        "relationship_counts": dict(sorted(counts.items())),
        "role_counts": dict(sorted(roles.items())),
        "schema_version": "distributed_agents-biokg-relationship-build-v2",
    }
    build_path.write_text(canonical_json(build_record) + "\n", encoding="utf-8")
    return build_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build exact source-link, comparator REPORTS_GENE, and frozen "
            "EXPRESSES_CLAIM edges."
        )
    )
    parser.add_argument(
        "--release-root",
        type=Path,
        default=DEFAULT_RELEASE_ROOT,
        help="Shi holdout release root containing artifacts/ (default: packaged release)",
    )
    parser.add_argument(
        "--nodes",
        type=Path,
        default=DEFAULT_NODES,
        help="canonical nodes.jsonl used for endpoint validation",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory for relationships.jsonl and relationship_build.json",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    record = build_relationships(args.release_root, args.nodes, args.output_dir)
    print(canonical_json(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
