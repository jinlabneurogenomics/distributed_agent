#!/usr/bin/env python3
"""Audit the 180-target sourceguard replacement and the extracted References."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


RELEASE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORRECTED = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
DEFAULT_MANIFEST = RELEASE_ROOT / "provenance" / "sourceguard_replacement_manifest.json"
DEFAULT_LEDGER = RELEASE_ROOT / "provenance" / "sourceguard_replacement_ledger.csv"
DEFAULT_TARGETS = RELEASE_ROOT / "provenance" / "sourceguard_replacement_targets.txt"
DEFAULT_REFERENCES = RELEASE_ROOT / "artifacts" / "ledgers" / "references.csv"
DEFAULT_OUTPUT = RELEASE_ROOT / "artifacts" / "audits" / "sourceguard_reconciliation.json"

DENY_PATTERNS = (
    "10.64898/2026.03.16.711480",
    "10.1101/2026.03.16.711480",
    "2026.03.16.711480",
    "Genome-scale functional mapping of the mammalian whole brain with in vivo Perturb-seq",
    "Genome-scale functional mapping of the mammalian whole brain",
    "github.com/jinlabneurogenomics/wholebrainperturbseq",
    "jinlabneurogenomics/wholebrainperturbseq",
    "jinlabneurogenomics",
    "huggingface.co/datasets/perturbai/wholebrain_crispr_atlas",
    "wholebrain_crispr_atlas",
    "perturb.ai",
    "PerturbAI Open-Sourcing the World's Largest 8-Million-Cell Brain-Wide",
    "Tuo Shi",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def deny_matches(value: str) -> list[str]:
    folded = value.casefold()
    compacted = compact(value)
    return [
        pattern
        for pattern in DENY_PATTERNS
        if pattern.casefold() in folded
        or (len(compact(pattern)) >= 8 and compact(pattern) in compacted)
    ]


def load_reports(path: Path) -> tuple[list[str], dict[str, dict[str, Any]], list[bytes]]:
    raw_lines = path.read_bytes().splitlines(keepends=True)
    order: list[str] = []
    rows: dict[str, dict[str, Any]] = {}
    for line_number, raw in enumerate(raw_lines, 1):
        row = json.loads(raw)
        target = str(row.get("gene_target") or "")
        report = row.get("final_report")
        if not target or not isinstance(report, str):
            raise ValueError(f"{path}:{line_number}: invalid report row")
        if target in rows:
            raise ValueError(f"{path}:{line_number}: duplicate target {target}")
        order.append(target)
        rows[target] = row
    return order, rows, raw_lines


def audit(
    *,
    corrected: Path,
    backup: Path,
    manifest_path: Path,
    ledger_path: Path,
    targets_path: Path,
    references_path: Path,
    output: Path,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_corrected = str(manifest["canonical_corpus"]["sha256"])
    expected_backup = str(manifest["original_corpus_backup"]["sha256"])
    if sha256_file(corrected) != expected_corrected:
        raise ValueError("corrected corpus hash does not match replacement manifest")
    if sha256_file(backup) != expected_backup:
        raise ValueError("backup corpus hash does not match replacement manifest")

    corrected_order, corrected_rows, corrected_lines = load_reports(corrected)
    backup_order, backup_rows, backup_lines = load_reports(backup)
    if corrected_order != backup_order:
        raise ValueError("corrected and backup target order differ")
    if len(corrected_order) != 2046:
        raise ValueError(f"expected 2046 report targets, found {len(corrected_order)}")

    targets = [line.strip() for line in targets_path.read_text().splitlines() if line.strip()]
    if len(targets) != 180 or len(set(targets)) != 180:
        raise ValueError("replacement target list is not exactly 180 unique targets")
    if sha256_file(targets_path) != str(manifest["rerun"]["targets_sha256"]):
        raise ValueError("replacement target-list hash does not match manifest")
    if int(manifest["replacement"]["target_count"]) != len(targets):
        raise ValueError("replacement target count does not match manifest")
    with ledger_path.open(newline="", encoding="utf-8") as handle:
        ledger = [dict(row) for row in csv.DictReader(handle)]
    ledger_targets = [str(row["gene_target"]) for row in ledger]
    if ledger_targets != targets:
        raise ValueError("replacement ledger target order differs from targets.txt")

    changed_targets: list[str] = []
    unchanged_non_targets = 0
    target_set = set(targets)
    for target, old_raw, new_raw in zip(
        corrected_order, backup_lines, corrected_lines
    ):
        if old_raw == new_raw:
            if target in target_set:
                raise ValueError(f"replacement target remained byte-identical: {target}")
            unchanged_non_targets += 1
        else:
            if target not in target_set:
                raise ValueError(f"non-target report changed: {target}")
            changed_targets.append(target)
    if set(changed_targets) != target_set or len(changed_targets) != 180:
        raise ValueError("changed report set does not equal the 180-target sourceguard set")
    if unchanged_non_targets != 1866:
        raise ValueError(f"expected 1866 byte-identical non-targets, found {unchanged_non_targets}")
    manifest_validation = manifest["validation"]
    expected_validation = {
        "rows": 2046,
        "unique_targets": 2046,
        "replaced_rows": 180,
        "byte_identical_non_target_rows": 1866,
        "target_order_preserved": True,
        "replacement_structure_failures": 0,
        "replacement_source_policy_failures": 0,
    }
    if any(manifest_validation.get(key) != value for key, value in expected_validation.items()):
        raise ValueError("replacement manifest validation summary is inconsistent")

    ledger_by_target = {str(row["gene_target"]): row for row in ledger}
    for target in targets:
        row = ledger_by_target[target]
        old_report = str(backup_rows[target]["final_report"])
        new_report = str(corrected_rows[target]["final_report"])
        if str(row.get("old_report_sha256")) != sha256_text(old_report):
            raise ValueError(f"replacement ledger old report hash mismatch: {target}")
        if str(row.get("new_report_sha256")) != sha256_text(new_report):
            raise ValueError(f"replacement ledger new report hash mismatch: {target}")
        if str(row.get("changed")).casefold() != "true":
            raise ValueError(f"replacement ledger does not mark target changed: {target}")
        if str(row.get("replacement_source_policy_status")) != "passed":
            raise ValueError(f"replacement ledger source policy failed: {target}")
        if str(row.get("replacement_structure_status")) != "passed":
            raise ValueError(f"replacement ledger structure failed: {target}")

    report_hits: list[dict[str, Any]] = []
    for target in corrected_order:
        matches = deny_matches(str(corrected_rows[target]["final_report"]))
        if matches:
            report_hits.append({"target_gene": target, "patterns": matches})
    reference_hits: list[dict[str, Any]] = []
    with references_path.open(newline="", encoding="utf-8") as handle:
        reference_count = 0
        for row in csv.DictReader(handle):
            reference_count += 1
            matches = deny_matches(" ".join(str(value or "") for value in row.values()))
            if matches:
                reference_hits.append(
                    {
                        "source_reference_id": f"{row.get('target_gene', '')}:{row.get('ref_id', '')}",
                        "patterns": matches,
                    }
                )
    if report_hits or reference_hits:
        raise ValueError(
            f"sourceguard deny matches remain: reports={len(report_hits)} "
            f"references={len(reference_hits)}"
        )

    result = {
        "schema_version": "distributed_agents-sourceguard-reconciliation-audit-v1",
        "corrected_corpus": {
            "sha256": expected_corrected,
            "bytes": corrected.stat().st_size,
            "records": len(corrected_order),
            "unique_targets": len(set(corrected_order)),
        },
        "historical_backup": {
            "sha256": expected_backup,
            "bytes": backup.stat().st_size,
            "records": len(backup_order),
        },
        "replacement_provenance": {
            "manifest_sha256": sha256_file(manifest_path),
            "ledger_sha256": sha256_file(ledger_path),
            "targets_sha256": sha256_file(targets_path),
            "targets": len(targets),
        },
        "delta": {
            "changed_target_rows": len(changed_targets),
            "byte_identical_non_target_rows": unchanged_non_targets,
            "target_order_preserved": True,
            "manifest_ledger_targets_agree": True,
        },
        "sourceguard": {
            "policy_sha256": manifest["rerun"]["source_policy_sha256"],
            "deny_pattern_count": len(DENY_PATTERNS),
            "report_hits": report_hits,
            "reference_hits": reference_hits,
            "references_scanned": reference_count,
            "status": "passed",
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corrected", type=Path, default=DEFAULT_CORRECTED)
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGETS)
    parser.add_argument("--references", type=Path, default=DEFAULT_REFERENCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = audit(
            corrected=args.corrected.resolve(),
            backup=args.backup.resolve(),
            manifest_path=args.manifest.resolve(),
            ledger_path=args.ledger.resolve(),
            targets_path=args.targets.resolve(),
            references_path=args.references.resolve(),
            output=args.output.resolve(),
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"delta": result["delta"], "sourceguard": result["sourceguard"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
