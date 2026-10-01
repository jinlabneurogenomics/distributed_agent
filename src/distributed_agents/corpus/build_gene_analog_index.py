"""Build the frozen SQLite substrate used for target-analog nomination.

This is a release-maintenance command, not a query-time dependency.  It reads
the historical Parquet annotation store with the optional analysis dependency
and writes a stdlib-readable SQLite index plus a provenance receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "distributed_agents-gene-analog-index-v1"
TIER_RANK = {
    "exact_complex_or_paralog": 10,
    "bidirectional_corpus_comparator": 20,
    "narrow_module": 30,
    "direct_interaction_or_dependency": 40,
    "broad_functional_fallback": 50,
}
COMPLEX_METADATA_FIELDS = (
    "source_species",
    "source_species_taxonomy_id",
    "projection_method",
    "projection_complete",
    "raw_complex_member_count",
    "mapped_complex_member_count",
    "store_complex_member_count",
    "corum_version",
    "corum_sha256",
    "orthology_resource",
    "orthology_version",
    "orthology_sha256",
)
RELATIONSHIP_METADATA_FIELDS = (
    "score",
    "network_type",
    "source_version",
    "string_protein_a",
    "string_protein_b",
    "neighborhood_score",
    "fusion_score",
    "cooccurrence_score",
    "coexpression_score",
    "experimental_score",
    "database_score",
    "textmining_score",
)


class AnalogIndexBuildError(ValueError):
    """Raised when the source annotation store violates the build contract."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _value(value: Any) -> Any | None:
    if value is None:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.casefold() in {"", "nan", "none", "<na>"}:
            return None
    return value


def _text(value: Any) -> str:
    parsed = _value(value)
    return "" if parsed is None else str(parsed).strip()


def _bool_int(value: Any) -> int:
    parsed = _value(value)
    if isinstance(parsed, str):
        return int(parsed.casefold() in {"1", "true", "yes"})
    return int(bool(parsed))


def _uniform_metadata(
    rows: Iterable[Mapping[str, Any]], fields: Sequence[str]
) -> dict[str, Any]:
    values: dict[str, dict[str, Any]] = {field: {} for field in fields}
    for row in rows:
        for field in fields:
            value = _value(row.get(field))
            if value is not None:
                values[field][json.dumps(value, sort_keys=True)] = value
    result: dict[str, Any] = {}
    for field, observed in values.items():
        if len(observed) == 1:
            result[field] = next(iter(observed.values()))
        elif observed:
            result[field] = [observed[key] for key in sorted(observed)]
    return result


def _membership_semantics(
    resource: str,
    set_name: str,
    member_count: int,
    explicit_tiers: set[str],
    projected: bool,
) -> tuple[str, str, str]:
    if len(explicit_tiers) > 1:
        raise AnalogIndexBuildError(
            f"annotation set declares conflicting tiers: {sorted(explicit_tiers)}"
        )
    folded_resource = resource.casefold()
    folded_name = set_name.casefold()
    if explicit_tiers:
        tier = next(iter(explicit_tiers))
        assignment = (
            "explicit_ortholog_projected_annotation"
            if projected
            else "explicit_annotation"
        )
    elif "corum" in folded_resource or "complex" in folded_resource:
        tier = "exact_complex_or_paralog"
        assignment = (
            "ortholog_projected_complex_catalog_resource"
            if projected
            else "complex_catalog_resource"
        )
    elif "paralog" in folded_resource or "paralog" in folded_name:
        tier = "exact_complex_or_paralog"
        assignment = "paralog_annotation"
    elif (
        folded_resource.startswith("go:")
        or "functional_class" in folded_resource
        or folded_resource == "msigdb:mh"
        or "hallmark" in folded_resource
    ):
        tier = "broad_functional_fallback"
        assignment = "broad_annotation_resource"
    elif member_count <= 50:
        tier = "narrow_module"
        assignment = "bounded_membership"
    else:
        tier = "broad_functional_fallback"
        assignment = "broad_membership"

    if tier == "exact_complex_or_paralog":
        if "paralog" in f"{folded_resource} {folded_name}":
            relation_type = "paralog"
        elif projected:
            relation_type = "ortholog_projected_same_complex"
        else:
            relation_type = "same_complex"
    elif tier == "narrow_module":
        relation_type = "shared_narrow_module"
    else:
        relation_type = "shared_functional_annotation"
    return tier, relation_type, assignment


def _json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_index(
    *,
    genes_path: Path,
    memberships_path: Path,
    relationships_path: Path,
    output_path: Path,
    provenance_path: Path,
) -> dict[str, Any]:
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - environment guard
        raise AnalogIndexBuildError(
            "building the analog index requires the DistributedAgents analysis extra"
        ) from exc

    for path in (genes_path, memberships_path, relationships_path):
        if not path.is_file():
            raise AnalogIndexBuildError(f"source annotation table is missing: {path}")

    genes_frame = pd.read_parquet(genes_path)
    memberships_frame = pd.read_parquet(memberships_path)
    relationships_frame = pd.read_parquet(relationships_path)
    required = {
        "genes": {"gene"},
        "memberships": {"gene", "resource", "set_id", "set_name"},
        "relationships": {"gene_a", "gene_b", "relation_type", "resource"},
    }
    for label, frame in (
        ("genes", genes_frame),
        ("memberships", memberships_frame),
        ("relationships", relationships_frame),
    ):
        missing = sorted(required[label] - set(frame.columns))
        if missing:
            raise AnalogIndexBuildError(
                f"{label_path(label, genes_path, memberships_path, relationships_path)} "
                f"is missing columns: {', '.join(missing)}"
            )

    gene_rows: list[tuple[Any, ...]] = []
    symbols: dict[str, tuple[int, str]] = {}
    ordered_genes = sorted(
        genes_frame.to_dict(orient="records"),
        key=lambda row: _text(row.get("gene")).casefold(),
    )
    for gene_id, row in enumerate(ordered_genes, 1):
        symbol = _text(row.get("gene"))
        if not symbol:
            raise AnalogIndexBuildError("genes table contains an empty symbol")
        key = symbol.casefold()
        if key in symbols:
            raise AnalogIndexBuildError(
                f"case-insensitive gene collision: {symbols[key][1]!r}, {symbol!r}"
            )
        symbols[key] = (gene_id, symbol)
        gene_rows.append(
            (
                gene_id,
                symbol,
                key,
                _bool_int(row.get("is_perturbation_target")),
                _bool_int(row.get("is_measured")),
                _bool_int(row.get("is_control_target")),
                _text(row.get("entrezgene")),
                _text(row.get("ensembl")),
                _text(row.get("name")),
                _text(row.get("type_of_gene")),
            )
        )

    raw_memberships = memberships_frame.to_dict(orient="records")
    grouped_sets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in raw_memberships:
        resource = _text(row.get("resource"))
        source_id = _text(row.get("set_id"))
        if not resource or not source_id:
            raise AnalogIndexBuildError("membership row lacks resource or set_id")
        grouped_sets.setdefault((resource, source_id), []).append(row)

    set_rows: list[tuple[Any, ...]] = []
    membership_rows: list[tuple[Any, ...]] = []
    tier_counts: Counter[str] = Counter()
    resource_counts: Counter[str] = Counter()
    seen_memberships: set[tuple[int, int]] = set()
    for set_pk, ((resource, source_id), rows) in enumerate(
        sorted(grouped_sets.items(), key=lambda item: (item[0][0].casefold(), item[0][1].casefold())),
        1,
    ):
        names = {_text(row.get("set_name")) for row in rows if _text(row.get("set_name"))}
        if len(names) > 1:
            raise AnalogIndexBuildError(
                f"annotation set {resource}:{source_id} has conflicting names"
            )
        set_name = next(iter(names), source_id)
        explicit_tiers = {
            _text(row.get("relationship_tier"))
            for row in rows
            if _text(row.get("relationship_tier"))
        }
        unknown_tiers = sorted(explicit_tiers - set(TIER_RANK))
        if unknown_tiers:
            raise AnalogIndexBuildError(
                f"annotation set {resource}:{source_id} has unknown tiers: {unknown_tiers}"
            )
        projected = any(
            _text(row.get("projection_method")).casefold()
            not in {"", "native_species_membership"}
            for row in rows
        )
        members: dict[int, str] = {}
        for row in rows:
            gene = _text(row.get("gene"))
            resolved = symbols.get(gene.casefold())
            if resolved is None:
                raise AnalogIndexBuildError(
                    f"membership references a gene absent from genes: {gene!r}"
                )
            source_gene = _text(row.get("source_gene"))
            members.setdefault(resolved[0], source_gene)
        tier, relation_type, assignment = _membership_semantics(
            resource,
            set_name,
            len(members),
            explicit_tiers,
            projected,
        )
        metadata = _uniform_metadata(rows, COMPLEX_METADATA_FIELDS)
        set_rows.append(
            (
                set_pk,
                resource,
                source_id,
                set_name,
                tier,
                TIER_RANK[tier],
                relation_type,
                assignment,
                len(members),
                _json(metadata),
            )
        )
        tier_counts[tier] += 1
        resource_counts[resource] += 1
        for gene_id, source_gene in sorted(members.items()):
            identity = (set_pk, gene_id)
            if identity not in seen_memberships:
                seen_memberships.add(identity)
                membership_rows.append((set_pk, gene_id, source_gene))

    relationship_rows: list[tuple[Any, ...]] = []
    seen_relationships: set[tuple[int, int, str]] = set()
    for raw in sorted(
        relationships_frame.to_dict(orient="records"),
        key=lambda row: (
            _text(row.get("gene_a")).casefold(),
            _text(row.get("gene_b")).casefold(),
            _text(row.get("source_id")).casefold(),
        ),
    ):
        gene_a = symbols.get(_text(raw.get("gene_a")).casefold())
        gene_b = symbols.get(_text(raw.get("gene_b")).casefold())
        if gene_a is None or gene_b is None:
            raise AnalogIndexBuildError(
                "relationship references a gene absent from genes: "
                f"{_text(raw.get('gene_a'))!r}, {_text(raw.get('gene_b'))!r}"
            )
        if gene_a[0] == gene_b[0]:
            continue
        left, right = sorted((gene_a[0], gene_b[0]))
        source_id = _text(raw.get("source_id"))
        identity = (left, right, source_id)
        if identity in seen_relationships:
            continue
        seen_relationships.add(identity)
        tier = _text(raw.get("relationship_tier")) or "direct_interaction_or_dependency"
        if tier not in TIER_RANK:
            raise AnalogIndexBuildError(f"unknown relationship tier: {tier!r}")
        metadata = {
            field: value
            for field in RELATIONSHIP_METADATA_FIELDS
            if (value := _value(raw.get(field))) is not None
        }
        relationship_rows.append(
            (
                len(relationship_rows) + 1,
                left,
                right,
                tier,
                TIER_RANK[tier],
                _text(raw.get("relation_type")) or "typed_relation",
                _text(raw.get("resource")) or "curated_relationships",
                source_id,
                _text(raw.get("label")),
                _json(metadata),
            )
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.tmp-{os.getpid()}")
    if temporary.exists():
        temporary.unlink()
    connection = sqlite3.connect(temporary)
    try:
        connection.executescript(
            """
            PRAGMA journal_mode=OFF;
            PRAGMA synchronous=OFF;
            PRAGMA page_size=4096;
            PRAGMA user_version=1;
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            ) WITHOUT ROWID;
            CREATE TABLE genes (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                symbol_key TEXT NOT NULL UNIQUE,
                is_perturbation_target INTEGER NOT NULL,
                is_measured INTEGER NOT NULL,
                is_control_target INTEGER NOT NULL,
                entrezgene TEXT NOT NULL,
                ensembl TEXT NOT NULL,
                name TEXT NOT NULL,
                type_of_gene TEXT NOT NULL
            );
            CREATE TABLE annotation_sets (
                id INTEGER PRIMARY KEY,
                resource TEXT NOT NULL,
                source_id TEXT NOT NULL,
                set_name TEXT NOT NULL,
                tier TEXT NOT NULL,
                tier_rank INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                assignment_basis TEXT NOT NULL,
                member_count INTEGER NOT NULL,
                metadata_json TEXT NOT NULL,
                UNIQUE(resource, source_id)
            );
            CREATE TABLE memberships (
                set_id INTEGER NOT NULL,
                gene_id INTEGER NOT NULL,
                source_gene TEXT NOT NULL,
                PRIMARY KEY(set_id, gene_id),
                FOREIGN KEY(set_id) REFERENCES annotation_sets(id),
                FOREIGN KEY(gene_id) REFERENCES genes(id)
            ) WITHOUT ROWID;
            CREATE INDEX memberships_gene ON memberships(gene_id, set_id);
            CREATE TABLE relationships (
                id INTEGER PRIMARY KEY,
                gene_a_id INTEGER NOT NULL,
                gene_b_id INTEGER NOT NULL,
                tier TEXT NOT NULL,
                tier_rank INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                resource TEXT NOT NULL,
                source_id TEXT NOT NULL,
                label TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                FOREIGN KEY(gene_a_id) REFERENCES genes(id),
                FOREIGN KEY(gene_b_id) REFERENCES genes(id)
            );
            CREATE INDEX relationships_gene_a ON relationships(gene_a_id, gene_b_id);
            CREATE INDEX relationships_gene_b ON relationships(gene_b_id, gene_a_id);
            """
        )
        connection.executemany(
            "INSERT INTO genes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", gene_rows
        )
        connection.executemany(
            "INSERT INTO annotation_sets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            set_rows,
        )
        connection.executemany(
            "INSERT INTO memberships VALUES (?, ?, ?)", membership_rows
        )
        connection.executemany(
            "INSERT INTO relationships VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            relationship_rows,
        )
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "taxonomy_id": "10090",
            "scientific_name": "Mus musculus",
            "gene_count": str(len(gene_rows)),
            "set_count": str(len(set_rows)),
            "membership_count": str(len(membership_rows)),
            "relationship_count": str(len(relationship_rows)),
        }
        connection.executemany(
            "INSERT INTO metadata VALUES (?, ?)", sorted(metadata.items())
        )
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()
    temporary.replace(output_path)

    sources = {
        label: {
            "filename": path.name,
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
        for label, path in (
            ("genes", genes_path),
            ("memberships", memberships_path),
            ("relationships", relationships_path),
        )
    }
    receipt = {
        "schema_version": "distributed_agents-gene-analog-index-build-v1",
        "output": {
            "filename": output_path.name,
            "sha256": _sha256(output_path),
            "bytes": output_path.stat().st_size,
        },
        "sources": sources,
        "species": {"scientific_name": "Mus musculus", "taxonomy_id": 10090},
        "counts": {
            "genes": len(gene_rows),
            "sets": len(set_rows),
            "memberships": len(membership_rows),
            "relationships": len(relationship_rows),
            "sets_by_resource": dict(sorted(resource_counts.items())),
            "sets_by_tier": dict(sorted(tier_counts.items())),
        },
        "policy": {
            "ordering": "categorical tier precedence then canonical symbol; no aggregate biological similarity score",
            "narrow_membership_max_genes": 50,
            "go_functional_class_and_hallmark": "broad_functional_fallback",
            "corum": "exact_complex_or_paralog",
            "string": "pinned physical edges with source confidence retained as provenance",
            "query_time_network_access": False,
        },
    }
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def label_path(
    label: str,
    genes: Path,
    memberships: Path,
    relationships: Path,
) -> Path:
    return {
        "genes": genes,
        "memberships": memberships,
        "relationships": relationships,
    }[label]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--genes", type=Path, required=True)
    parser.add_argument("--memberships", type=Path, required=True)
    parser.add_argument("--relationships", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    receipt = build_index(
        genes_path=args.genes.expanduser().resolve(),
        memberships_path=args.memberships.expanduser().resolve(),
        relationships_path=args.relationships.expanduser().resolve(),
        output_path=args.out.expanduser().resolve(),
        provenance_path=args.provenance.expanduser().resolve(),
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
