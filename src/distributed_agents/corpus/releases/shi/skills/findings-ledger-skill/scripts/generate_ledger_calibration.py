#!/usr/bin/env python3
"""Generate deterministic Finding and Claim calibration for the reconciled release."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "distributed_agents-ledger-calibration-v2"
GENERATOR_VERSION = "distributed_agents-claim-overlay-calibration-generator-v1"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
RELEASE_ROOT = SCRIPT_DIR.parents[2]
DEFAULT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
DEFAULT_CLAIM_SUMMARY = (
    RELEASE_ROOT / "projections" / "biokg" / "data" / "claims" / "claim_assignments.summary.json"
)
DEFAULT_SCHEMA = SKILL_DIR / "schemas" / "ledger_calibration.schema.json"
DEFAULT_CALIBRATION_OUT = SCRIPT_DIR / "out" / "ledger_calibration.json"
DEFAULT_DICTIONARY_OUT = SCRIPT_DIR / "out" / "value_dictionary.csv"

DICTIONARY_FIELDS = (
    "artifact",
    "field",
    "value_or_pattern",
    "meaning",
    "non_meaning",
    "aliases",
    "derivation",
    "constraints",
    "related_fields",
    "example_ids",
)

FINDING_MEANINGS = {
    "target_gene": "Perturbed target and gene-scoped Finding identity component.",
    "finding_id": "Gene-scoped atomic Finding identifier; combine with target_gene.",
    "finding_type": "Narrative type assigned to the atomic Finding.",
    "direction": "Free-text observed direction or qualitative relationship.",
    "confidence": "Confidence in the statement or biological interpretation as written.",
    "literature_status": "Corpus-authored comparison label; not a calibrated novelty score.",
    "summary": "Self-contained atomic Finding statement.",
    "why_it_matters": "Interpretive consequence attached to the Finding.",
    "genes": "Pipe-delimited measured or finding-reported genes; may be representative.",
    "n_genes": "Count of pipe-delimited genes in this Finding row.",
    "comparators": "Pipe-delimited named perturbation comparators.",
    "cell_types": "Reported mention scope; not necessarily positive-support placement.",
    "n_cell_types": "Count of reported cell-type mentions in this Finding row.",
    "evidence_ids": "Gene-scoped keys into the Evidence ledger.",
    "ref_ids": "Gene-scoped keys into the Reference ledger.",
    "main_caveats": "Finding-specific limitations and boundary conditions.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(RELEASE_ROOT))
    except ValueError:
        return resolved.name


def read_findings(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def split(value: object) -> list[str]:
    return [item for item in str(value or "").split("|") if item]


def frequency(rows: Iterable[Mapping[str, str]], field: str) -> list[dict[str, Any]]:
    counts = Counter(str(row.get(field) or "") for row in rows)
    return [
        {"value": value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def crosstab(
    rows: Iterable[Mapping[str, str]], first: str, second: str
) -> list[dict[str, Any]]:
    counts = Counter(
        (str(row.get(first) or ""), str(row.get(second) or "")) for row in rows
    )
    return [
        {first: keys[0], second: keys[1], "count": count}
        for keys, count in sorted(counts.items())
    ]


def dictionary_row(
    field: str,
    *,
    value: str = "*",
    meaning: str | None = None,
    derivation: str = "source artifact",
) -> dict[str, str]:
    return {
        "artifact": "findings_ledger",
        "field": field,
        "value_or_pattern": value,
        "meaning": meaning or FINDING_MEANINGS.get(field, "Findings ledger field."),
        "non_meaning": (
            "Not a novelty, priority, or biological-yield score."
            if field in {"confidence", "literature_status", "finding_type"}
            else "Does not independently establish biological truth or priority."
        ),
        "aliases": "",
        "derivation": derivation,
        "constraints": (
            "Finding, Evidence, and Reference IDs are target-scoped."
            if field in {"finding_id", "evidence_ids", "ref_ids"}
            else ""
        ),
        "related_fields": "target_gene|finding_id",
        "example_ids": "Arx:F001",
    }


def generate(findings_path: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    fields, findings = read_findings(findings_path)
    identities = {(row["target_gene"], row["finding_id"]) for row in findings}
    targets = {row["target_gene"] for row in findings}
    controls = {target for target in targets if target.startswith("Safe_target")}
    claim_summary = json.loads(DEFAULT_CLAIM_SUMMARY.read_text(encoding="utf-8"))
    count_errors = [
        f"{row['target_gene']}:{row['finding_id']}"
        for row in findings
        if int(row["n_genes"]) != len(split(row["genes"]))
        or int(row["n_cell_types"]) != len(split(row["cell_types"]))
    ]
    checks = [
        {
            "id": "finding_ids_unique",
            "status": "passed" if len(identities) == len(findings) else "failed",
            "actual": len(identities),
            "expected": len(findings),
        },
        {
            "id": "target_count",
            "status": "passed" if len(targets) == 2046 else "failed",
            "actual": len(targets),
            "expected": 2046,
        },
        {
            "id": "derived_list_counts",
            "status": "passed" if not count_errors else "failed",
            "actual": len(count_errors),
            "expected": 0,
        },
    ]
    if any(check["status"] != "passed" for check in checks):
        raise ValueError(
            "Finding calibration reconciliation failed: "
            + ", ".join(check["id"] for check in checks if check["status"] != "passed")
        )

    frequency_fields = (
        "finding_type",
        "confidence",
        "direction",
        "literature_status",
        "n_cell_types",
    )
    calibration = {
        "schema_version": SCHEMA_VERSION,
        "generation_version": GENERATOR_VERSION,
        "sources": {
            "findings": {
                "path": stable_path(findings_path),
                "sha256": sha256(findings_path),
                "schema_version": "findings-ledger-csv-v1",
            }
        },
        "counts": {
            "findings": len(findings),
            "targets": len(targets),
            "biological_targets": len(targets - controls),
            "controls": len(controls),
        },
        "field_value_frequencies": {
            "findings": {
                field: frequency(findings, field) for field in frequency_fields
            }
        },
        "crosstabs": {
            "finding_confidence_by_type": crosstab(
                findings, "confidence", "finding_type"
            )
        },
        "claim_layer": {
            "status": "available_compatibility_overlay",
            "claims": claim_summary["claims"],
            "claim_memberships": claim_summary["claim_memberships"],
            "claimed_findings": claim_summary["claimed_findings"],
            "unclaimed_findings": claim_summary["unclaimed_findings"],
            "multi_claim_findings": claim_summary["multi_claim_findings"],
        },
        "semantic_assertions": [
            {
                "id": "confidence_scope",
                "statement": "Confidence is confidence in the statement as written and can be high for a measured null, buffered response, or limitation.",
            },
            {
                "id": "literature_status_not_novelty",
                "statement": "literature_status is a corpus-authored comparison label and is not a calibrated novelty score.",
            },
            {
                "id": "priority_absent",
                "statement": "Priority is not a ledger field and cannot be inferred from confidence, target fame, or DEG burden.",
            },
            {
                "id": "finding_identity",
                "statement": "Findings are target-scoped report rows; the Claim layer may leave Findings unclaimed or allow one Finding to support multiple Claims.",
            },
        ],
        "reconciliation": {"status": "passed", "checks": checks},
    }

    dictionary = [dictionary_row(field) for field in fields]
    for field in ("finding_type", "confidence", "literature_status"):
        dictionary.extend(
            dictionary_row(
                field,
                value=item["value"],
                meaning=f"Observed {field} value in the reconciled Finding ledger.",
                derivation="exact value frequency from findings.csv",
            )
            for item in calibration["field_value_frequencies"]["findings"][field]
        )
    dictionary.append(
        {
            "artifact": "corpus_identity",
            "field": "Claim",
            "value_or_pattern": "compatibility_overlay",
            "meaning": "A Claim populated by semantically matched Findings.",
            "non_meaning": "Not an exhaustive partition of every Finding.",
            "aliases": "story|duplicate-reduced claim",
            "derivation": "semantic Finding assignment to the Claim layer",
            "constraints": "Novel Findings may be unclaimed and a Finding may support more than one Claim.",
            "related_fields": "Finding",
            "example_ids": "claim:itga2b_f001_1ac5c5d2bb15",
        }
    )
    return calibration, sorted(
        dictionary,
        key=lambda row: (row["artifact"], row["field"], row["value_or_pattern"]),
    )


def write_dictionary(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DICTIONARY_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--calibration-out", type=Path, default=DEFAULT_CALIBRATION_OUT)
    parser.add_argument("--dictionary-out", type=Path, default=DEFAULT_DICTIONARY_OUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    calibration, dictionary = generate(args.findings.resolve())
    calibration["artifact_schema"] = {
        "path": stable_path(args.schema),
        "sha256": sha256(args.schema),
    }
    args.calibration_out.parent.mkdir(parents=True, exist_ok=True)
    args.calibration_out.write_text(
        json.dumps(calibration, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_dictionary(args.dictionary_out, dictionary)
    print(
        json.dumps(
            {
                "schema_version": calibration["schema_version"],
                "counts": calibration["counts"],
                "dictionary_rows": len(dictionary),
                "reconciliation": calibration["reconciliation"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
