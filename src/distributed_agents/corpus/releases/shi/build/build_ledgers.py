#!/usr/bin/env python3
"""Extract the Shi CSV ledgers from the report JSONL.

Malformed JSONL rows are recorded and skipped instead of repaired.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


RELEASE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
DEFAULT_LEDGER_ROOT = RELEASE_ROOT / "artifacts" / "ledgers"
DEFAULT_AUDIT = RELEASE_ROOT / "artifacts" / "audits" / "ledger_extraction.json"

SECTION_RE = re.compile(
    r"^#{1,6}\s+(Evidence JSONL|References JSONL|Biological Findings JSONL)"
    r"\s*\n+```jsonl\s*\n(?P<body>.*?)\n```",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
SECTION_LEDGER = {
    "evidence jsonl": "evidence",
    "references jsonl": "references",
    "biological findings jsonl": "findings",
}
FIELDS = {
    "findings": (
        "target_gene",
        "finding_id",
        "finding_type",
        "direction",
        "confidence",
        "literature_status",
        "summary",
        "why_it_matters",
        "genes",
        "n_genes",
        "comparators",
        "cell_types",
        "n_cell_types",
        "evidence_ids",
        "ref_ids",
        "main_caveats",
    ),
    "evidence": (
        "target_gene",
        "evidence_id",
        "evidence_slug",
        "cell_type",
        "genes",
        "n_genes",
        "has_genes",
        "has_cell_type",
        "statistics",
        "description",
    ),
    "references": (
        "target_gene",
        "ref_id",
        "ref_slug",
        "source",
        "source_type",
        "citation",
        "url",
        "description",
    ),
}
ID_FIELD = {
    "findings": "finding_id",
    "evidence": "evidence_id",
    "references": "ref_id",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    return str(value)


def extract_row(target: str, ledger: str, source: dict[str, Any]) -> dict[str, Any]:
    row: dict[str, Any] = {"target_gene": target}
    for field in FIELDS[ledger][1:]:
        if field == "n_genes":
            row[field] = len(source.get("genes") or [])
        elif field == "n_cell_types":
            row[field] = len(source.get("cell_types") or [])
        elif field == "has_genes":
            row[field] = int(bool(source.get("genes")))
        elif field == "has_cell_type":
            row[field] = int(bool(source.get("cell_type")))
        else:
            row[field] = flatten(source.get(field))
    return row


def split_ids(value: object) -> Iterable[str]:
    return (item for item in str(value or "").split("|") if item)


def validate_ledgers(ledgers: dict[str, list[dict[str, Any]]]) -> None:
    indexes: dict[str, set[tuple[str, str]]] = {}
    for ledger, rows in ledgers.items():
        field = ID_FIELD[ledger]
        keys = {(str(row["target_gene"]), str(row[field])) for row in rows}
        if len(keys) != len(rows):
            raise ValueError(f"{ledger} contains duplicate target-scoped IDs")
        if any(not target or not local_id for target, local_id in keys):
            raise ValueError(f"{ledger} contains an empty target or local ID")
        indexes[ledger] = keys

    missing: list[str] = []
    for row in ledgers["findings"]:
        target = str(row["target_gene"])
        finding = str(row["finding_id"])
        for evidence_id in split_ids(row.get("evidence_ids")):
            if (target, evidence_id) not in indexes["evidence"]:
                missing.append(f"{target}:{finding}.evidence_ids->{evidence_id}")
        for ref_id in split_ids(row.get("ref_ids")):
            if (target, ref_id) not in indexes["references"]:
                missing.append(f"{target}:{finding}.ref_ids->{ref_id}")
    if missing:
        raise ValueError("unresolved Finding links: " + ", ".join(missing[:30]))


def write_csv(path: Path, ledger: str, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS[ledger])
        writer.writeheader()
        writer.writerows(rows)


def build(source: Path, ledger_root: Path, audit_path: Path) -> dict[str, Any]:
    ledgers: dict[str, list[dict[str, Any]]] = {name: [] for name in FIELDS}
    issues: list[dict[str, Any]] = []
    targets: list[str] = []
    seen_targets: set[str] = set()

    with source.open(encoding="utf-8") as handle:
        for source_line, line in enumerate(handle, 1):
            if not line.strip():
                continue
            report_row = json.loads(line)
            target = str(report_row.get("gene_target") or "")
            report = report_row.get("final_report")
            if not target or not isinstance(report, str):
                raise ValueError(f"{source}:{source_line}: missing gene_target/final_report")
            if target in seen_targets:
                raise ValueError(f"{source}:{source_line}: duplicate target {target}")
            seen_targets.add(target)
            targets.append(target)

            found: set[str] = set()
            for match in SECTION_RE.finditer(report):
                ledger = SECTION_LEDGER[match.group(1).casefold()]
                if ledger in found:
                    raise ValueError(f"{target}: duplicate {match.group(1)} section")
                found.add(ledger)
                for block_line, raw in enumerate(match.group("body").splitlines(), 1):
                    if not raw.strip():
                        continue
                    try:
                        parsed = json.loads(raw)
                    except json.JSONDecodeError as exc:
                        issues.append(
                            {
                                "kind": "invalid_json_line_skipped",
                                "target_gene": target,
                                "ledger": ledger,
                                "block_line": block_line,
                                "raw_sha256": sha256_text(raw),
                                "error": str(exc),
                            }
                        )
                        continue
                    if not isinstance(parsed, dict):
                        issues.append(
                            {
                                "kind": "non_object_json_line_skipped",
                                "target_gene": target,
                                "ledger": ledger,
                                "block_line": block_line,
                                "raw_sha256": sha256_text(raw),
                            }
                        )
                        continue
                    ledgers[ledger].append(extract_row(target, ledger, parsed))
            missing = sorted(set(FIELDS) - found)
            if missing:
                raise ValueError(f"{target}: missing required legacy sections {missing}")

    validate_ledgers(ledgers)
    outputs: dict[str, dict[str, Any]] = {}
    for ledger, rows in ledgers.items():
        output = ledger_root / f"{ledger}.csv"
        write_csv(output, ledger, rows)
        outputs[ledger] = {
            "path": str(output.relative_to(RELEASE_ROOT)),
            "sha256": sha256_file(output),
            "bytes": output.stat().st_size,
            "records": len(rows),
        }

    audit = {
        "schema_version": "distributed_agents-legacy-ledger-extraction-audit-v1",
        "policy": {
            "parser": "legacy-compatible-three-section-jsonl-v1",
            "invalid_rows": "record_and_skip_without_semantic_repair",
            "network": False,
            "model_calls": False,
            "ordering": "source-report-order_then-section-row-order",
        },
        "source": {
            "path": str(source.relative_to(RELEASE_ROOT)),
            "sha256": sha256_file(source),
            "bytes": source.stat().st_size,
            "records": len(targets),
            "unique_targets": len(seen_targets),
        },
        "outputs": outputs,
        "issues": issues,
        "integrity": {
            "unique_target_scoped_ids": True,
            "finding_evidence_links_resolved": True,
            "finding_reference_links_resolved": True,
        },
    }
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return audit


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--ledger-root", type=Path, default=DEFAULT_LEDGER_ROOT)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        audit = build(args.source.resolve(), args.ledger_root.resolve(), args.audit.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "source_records": audit["source"]["records"],
                "outputs": {
                    name: spec["records"] for name, spec in audit["outputs"].items()
                },
                "issues": len(audit["issues"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
