#!/usr/bin/env python3
"""Build the Shi holdout BioKG node projection from canonical ledgers.

The canonical ledger rows and frozen bottom-up Claims are copied unchanged into
their graph nodes. Explicit Finding comparator annotations additionally produce
deterministically canonicalized ``Gene`` nodes. This stage performs no semantic
extraction, relationship construction, model calls, or network access.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


PROJECTION_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_ROOT = PROJECTION_ROOT.parents[1]
DEFAULT_OUTPUT_DIR = PROJECTION_ROOT / "data" / "base"

SOURCE_PATHS = {
    "reports": Path("artifacts/reports/reports.jsonl"),
    "findings": Path("artifacts/ledgers/findings.jsonl"),
    "evidence": Path("artifacts/ledgers/evidence.jsonl"),
    "references": Path("artifacts/ledgers/references.jsonl"),
    "claims": Path("artifacts/claims/claims.jsonl"),
}
LEDGER_NODE_TYPES = (
    ("findings", "Finding", "finding_id", "finding"),
    ("evidence", "Evidence", "evidence_id", "evidence"),
    ("references", "Reference", "ref_id", "reference"),
)


def canonical_json(value: Any) -> str:
    """Return the release's stable JSON representation."""

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


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_gene_symbol(value: object) -> str:
    """Apply the legacy graph's deterministic gene-symbol normalization."""

    symbol = normalize_text(value)
    if not symbol:
        return ""
    return symbol[:1].upper() + symbol[1:]


def comparator_symbols(row: dict[str, Any], *, location: str) -> list[str]:
    value = row.get("comparators")
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{location}: comparators must be an array or null")
    symbols: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise ValueError(f"{location}: comparators[{index}] must be a string")
        symbol = normalize_gene_symbol(item)
        if symbol:
            symbols.append(symbol)
    return symbols


def slugify(value: str, *, max_len: int = 96) -> str:
    """Return the legacy graph's stable ASCII identifier component."""

    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_") or "blank"
    if len(slug) > max_len:
        digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        slug = f"{slug[: max_len - 11].rstrip('_')}_{digest}"
    return slug


def target_node(target: str) -> dict[str, Any]:
    return {
        "id": f"target_gene:{target}",
        "properties": {"symbol": target},
        "source_artifact": "reports",
        "type": "TargetGene",
    }


def comparator_gene_nodes(
    findings_path: Path,
    target_symbols: set[str],
) -> list[dict[str, Any]]:
    """Build one canonical endpoint per case-insensitive comparator symbol."""

    canonical_symbols: dict[str, str] = {}
    for line_number, finding in iter_jsonl(findings_path):
        location = f"{findings_path}:{line_number}"
        for symbol in comparator_symbols(finding, location=location):
            key = symbol.casefold()
            if key not in target_symbols:
                canonical_symbols.setdefault(key, symbol)

    keys_by_base_id: dict[str, list[str]] = {}
    for key, symbol in canonical_symbols.items():
        keys_by_base_id.setdefault(f"gene:{slugify(symbol)}", []).append(key)

    nodes: list[dict[str, Any]] = []
    for base_id, keys in sorted(keys_by_base_id.items()):
        for key in sorted(keys):
            node_id = base_id
            if len(keys) > 1:
                suffix = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
                node_id = f"{base_id}_{suffix}"
            nodes.append(
                {
                    "id": node_id,
                    "properties": {"symbol": canonical_symbols[key]},
                    "source_artifact": "findings",
                    "type": "Gene",
                }
            )
    nodes.sort(key=lambda node: str(node["id"]))
    return nodes


def ledger_node(
    row: dict[str, Any],
    *,
    artifact: str,
    node_type: str,
    prefix: str,
) -> dict[str, Any]:
    return {
        "id": f"{prefix}:{row['doc_id']}",
        "properties": row,
        "source_artifact": artifact,
        "type": node_type,
    }


def claim_node(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["claim_id"],
        "properties": row,
        "source_artifact": "claims",
        "type": "Claim",
    }


def write_node(handle: Any, node: dict[str, Any], seen_ids: set[str]) -> None:
    node_id = str(node["id"])
    if node_id in seen_ids:
        raise ValueError(f"duplicate graph node ID: {node_id}")
    seen_ids.add(node_id)
    handle.write(canonical_json(node) + "\n")


def build_nodes(release_root: Path, output_dir: Path) -> dict[str, Any]:
    """Build canonical nodes and return their deterministic build record."""

    release_root = release_root.resolve()
    output_dir = output_dir.resolve()
    sources = {name: release_root / relative for name, relative in SOURCE_PATHS.items()}
    for name, path in sources.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing {name} source: {path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    nodes_path = output_dir / "nodes.jsonl"
    temporary_path = output_dir / ".nodes.jsonl.tmp"
    build_path = output_dir / "node_build.json"

    counts: Counter[str] = Counter()
    input_counts: Counter[str] = Counter()
    report_targets: set[str] = set()
    target_symbols: set[str] = set()
    source_targets: dict[str, set[str]] = {}
    seen_ids: set[str] = set()

    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
            for line_number, report in iter_jsonl(sources["reports"]):
                target = require_text(
                    report,
                    "gene_target",
                    location=f"{sources['reports']}:{line_number}",
                )
                if target in report_targets:
                    raise ValueError(f"duplicate report target: {target}")
                report_targets.add(target)
                target_key = normalize_gene_symbol(target).casefold()
                if target_key in target_symbols:
                    raise ValueError(
                        f"case-insensitive duplicate report target: {target}"
                    )
                target_symbols.add(target_key)
                input_counts["reports"] += 1
                write_node(handle, target_node(target), seen_ids)
                counts["TargetGene"] += 1
            source_targets["reports"] = report_targets

            gene_nodes = comparator_gene_nodes(sources["findings"], target_symbols)
            for node in gene_nodes:
                write_node(handle, node, seen_ids)
                counts["Gene"] += 1

            for artifact, node_type, local_id_field, prefix in LEDGER_NODE_TYPES:
                ledger_targets: set[str] = set()
                for line_number, row in iter_jsonl(sources[artifact]):
                    location = f"{sources[artifact]}:{line_number}"
                    target = require_text(row, "target_gene", location=location)
                    local_id = require_text(row, local_id_field, location=location)
                    doc_id = require_text(row, "doc_id", location=location)
                    expected_doc_id = f"{target}:{local_id}"
                    if doc_id != expected_doc_id:
                        raise ValueError(
                            f"{location}: doc_id {doc_id!r} != {expected_doc_id!r}"
                        )
                    if target not in report_targets:
                        raise ValueError(f"{location}: unknown target_gene {target!r}")
                    ledger_targets.add(target)
                    input_counts[artifact] += 1
                    write_node(
                        handle,
                        ledger_node(
                            row,
                            artifact=artifact,
                            node_type=node_type,
                            prefix=prefix,
                        ),
                        seen_ids,
                    )
                    counts[node_type] += 1
                source_targets[artifact] = ledger_targets

            claim_targets: set[str] = set()
            for line_number, claim in iter_jsonl(sources["claims"]):
                location = f"{sources['claims']}:{line_number}"
                require_text(claim, "claim_id", location=location)
                claim_scope = require_text(
                    claim, "claim_scope", location=location
                )
                if claim_scope != "corpus":
                    raise ValueError(
                        f"{location}: unsupported claim_scope {claim_scope!r}"
                    )
                target_genes = claim.get("target_genes") or []
                if (
                    len(target_genes) < 2
                    or len(target_genes) != len(set(target_genes))
                ):
                    raise ValueError(f"{location}: invalid Claim target_genes")
                unknown_targets = sorted(set(target_genes) - report_targets)
                if unknown_targets:
                    raise ValueError(
                        f"{location}: unknown Claim targets {unknown_targets[:10]}"
                    )
                input_counts["claims"] += 1
                claim_targets.update(map(str, target_genes))
                write_node(handle, claim_node(claim), seen_ids)
                counts["Claim"] += 1
            source_targets["claims"] = claim_targets
        temporary_path.replace(nodes_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise

    source_record = {
        name: {
            "path": relative.as_posix(),
            "records": input_counts[name],
            "sha256": sha256_file(sources[name]),
            "targets": len(source_targets[name]),
        }
        for name, relative in SOURCE_PATHS.items()
    }
    build_record = {
        "build_policy": {
            "claims": "frozen_bottom_up_claim_ledger",
            "gene_nodes": "canonicalized_from_finding_comparators",
            "ledger_properties": "copied_unchanged",
            "model_calls": False,
            "network": False,
            "relationships": False,
            "semantic_extraction": False,
        },
        "node_counts": dict(sorted(counts.items())),
        "output": {
            "bytes": nodes_path.stat().st_size,
            "path": "nodes.jsonl",
            "records": sum(counts.values()),
            "sha256": sha256_file(nodes_path),
        },
        "schema_version": "distributed_agents-biokg-node-build-v2",
        "sources": source_record,
    }
    build_path.write_text(canonical_json(build_record) + "\n", encoding="utf-8")
    return build_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build TargetGene, Gene, Finding, Evidence, Reference, and Claim nodes."
        )
    )
    parser.add_argument(
        "--release-root",
        type=Path,
        default=DEFAULT_RELEASE_ROOT,
        help="Shi holdout release root containing artifacts/ (default: packaged release)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory for nodes.jsonl and node_build.json",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    record = build_nodes(args.release_root, args.output_dir)
    print(canonical_json(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
