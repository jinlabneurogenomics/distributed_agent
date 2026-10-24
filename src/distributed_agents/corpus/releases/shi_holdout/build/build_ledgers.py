#!/usr/bin/env python3
"""Build canonical Shi holdout ledgers from report JSONL.

The input is the immutable post-generation report ledger. This build is
stdlib-only and performs no network access, model calls, or semantic invention.
Representational Markdown variation is parsed tolerantly. Content repairs must
be enumerated and hash-guarded in ``repairs.json``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


RELEASE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
DEFAULT_REPAIRS = Path(__file__).with_name("repairs.json")

SECTIONS = (
    "Evidence JSONL",
    "References JSONL",
    "Biological Findings JSONL",
    "Null-Cause Findings JSONL",
    "Pathways JSONL",
    "Cell Type Specificity JSONL",
)
LEDGER_BY_SECTION = {
    "Evidence JSONL": "evidence",
    "References JSONL": "references",
    "Biological Findings JSONL": "findings",
    "Null-Cause Findings JSONL": "null_findings",
    "Pathways JSONL": "pathways",
    "Cell Type Specificity JSONL": "cell_types",
}
ID_FIELD = {
    "evidence": "evidence_id",
    "references": "ref_id",
    "findings": "finding_id",
    "null_findings": "finding_id",
    "pathways": "pathway_id",
    "cell_types": "cell_type_id",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_heading(line: str) -> str:
    value = re.sub(r"^\s*#{1,6}\s*", "", line).strip()
    return re.sub(r"\s+", " ", value)


def scalar_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [str(value)] if str(value) else []


def load_repairs(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "distributed_agents-corpus-repairs-v1":
        raise ValueError(f"unsupported repair schema in {path}")
    repairs = payload.get("repairs")
    if not isinstance(repairs, list):
        raise ValueError(f"repairs must be a list in {path}")
    return repairs


def repairs_for(
    repairs: list[dict[str, Any]], target: str, section: str, kind: str
) -> Iterable[dict[str, Any]]:
    return (
        item
        for item in repairs
        if item.get("target_gene") == target
        and item.get("section") == section
        and item.get("kind") == kind
    )


def parse_appendix(
    report: str,
    *,
    target: str,
    repairs: list[dict[str, Any]],
    applied_repairs: Counter[str],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], list[str]]:
    """Parse known JSONL sections, retaining issues without guessing content."""

    lines = report.splitlines()
    appendix_index = next(
        (
            index
            for index, line in enumerate(lines)
            if clean_heading(line).casefold() == "structured appendix"
        ),
        None,
    )
    if appendix_index is None:
        return {}, [{"kind": "missing_appendix", "target_gene": target}], []

    section_lookup = {name.casefold(): name for name in SECTIONS}
    blocks: dict[str, list[dict[str, Any]]] = {}
    issues: list[dict[str, Any]] = []
    empty_sections: list[str] = []
    cursor = appendix_index + 1
    while cursor < len(lines):
        normalized = clean_heading(lines[cursor]).casefold()
        section = section_lookup.get(normalized)
        if section is None:
            cursor += 1
            continue
        if section in blocks:
            issues.append(
                {"kind": "duplicate_section", "target_gene": target, "section": section}
            )
            cursor += 1
            continue

        fence = cursor + 1
        while fence < len(lines) and not lines[fence].strip():
            fence += 1
        if fence >= len(lines) or lines[fence].strip().casefold() != "```jsonl":
            issues.append(
                {"kind": "missing_open_fence", "target_gene": target, "section": section}
            )
            cursor += 1
            continue

        rows: list[dict[str, Any]] = []
        body_line = 0
        index = fence + 1
        closed = False
        while index < len(lines):
            raw = lines[index]
            if raw.strip() == "```":
                closed = True
                index += 1
                break
            if clean_heading(raw).casefold() in section_lookup:
                break
            if raw.strip():
                body_line += 1
                source_hash = sha256_bytes(raw.encode("utf-8"))
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as exc:
                    matches = [
                        item
                        for item in repairs_for(repairs, target, section, "replace_json_line")
                        if item.get("raw_sha256") == source_hash
                    ]
                    if len(matches) == 1:
                        parsed = deepcopy(matches[0]["replacement"])
                        repair_id = str(matches[0]["repair_id"])
                        applied_repairs[repair_id] += 1
                    else:
                        issues.append(
                            {
                                "kind": "invalid_json_line",
                                "target_gene": target,
                                "section": section,
                                "block_line": body_line,
                                "raw_sha256": source_hash,
                                "error": str(exc),
                            }
                        )
                        index += 1
                        continue
                if not isinstance(parsed, dict):
                    issues.append(
                        {
                            "kind": "non_object_json_line",
                            "target_gene": target,
                            "section": section,
                            "block_line": body_line,
                            "raw_sha256": source_hash,
                        }
                    )
                    index += 1
                    continue

                record_hash = sha256_bytes(canonical_json(parsed).encode("utf-8"))
                for item in repairs_for(repairs, target, section, "replace_list_value"):
                    if item.get("record_sha256") != record_hash:
                        continue
                    field = str(item["field"])
                    values = parsed.get(field)
                    if not isinstance(values, list) or values.count(item["old"]) != 1:
                        raise ValueError(
                            f"repair {item['repair_id']} no longer matches {target} {section}"
                        )
                    parsed = deepcopy(parsed)
                    parsed[field] = [
                        item["new"] if value == item["old"] else value for value in values
                    ]
                    applied_repairs[str(item["repair_id"])] += 1
                parsed["_source_record_sha256"] = record_hash
                rows.append(parsed)
            index += 1

        if not closed:
            issues.append(
                {"kind": "missing_close_fence", "target_gene": target, "section": section}
            )
        if not rows:
            empty_sections.append(section)
        blocks[section] = rows
        cursor = max(index, cursor + 1)

    for section in SECTIONS:
        if section not in blocks:
            issues.append(
                {"kind": "missing_section", "target_gene": target, "section": section}
            )
    return blocks, issues, empty_sections


def enrich_record(
    row: dict[str, Any], *, target: str, source_line: int, report_sha: str,
    ledger: str, index: int,
) -> dict[str, Any]:
    value = deepcopy(row)
    value["target_gene"] = target
    value["source_line"] = source_line
    value["source_report_sha256"] = report_sha
    value["section_record_index"] = index
    if ledger == "pathways":
        value["pathway_id"] = f"P{index:03d}"
    elif ledger == "cell_types":
        value["cell_type_id"] = f"C{index:03d}"
    record_id = str(value.get(ID_FIELD[ledger]) or "")
    if not record_id:
        raise ValueError(f"{target} {ledger} record {index} has no {ID_FIELD[ledger]}")
    value["doc_id"] = f"{target}:{record_id}"
    return value


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(canonical_json(row) + "\n")


def validate_links(ledgers: dict[str, list[dict[str, Any]]]) -> None:
    by_target: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for ledger, rows in ledgers.items():
        id_field = ID_FIELD[ledger]
        for row in rows:
            target = str(row["target_gene"])
            local_id = str(row[id_field])
            if local_id in by_target[target][ledger]:
                raise ValueError(f"duplicate scoped ID {target}:{local_id} in {ledger}")
            by_target[target][ledger].add(local_id)

    missing: list[str] = []
    link_specs = {
        "findings": (("evidence_ids", "evidence"), ("ref_ids", "references")),
        "null_findings": (("evidence_ids", "evidence"), ("ref_ids", "references")),
        "pathways": (("evidence_ids", "evidence"), ("finding_ids", "all_findings")),
        "cell_types": (
            ("evidence_ids", "evidence"), ("ref_ids", "references"),
            ("finding_ids", "all_findings"),
        ),
    }
    for target, indexes in by_target.items():
        indexes["all_findings"] = indexes["findings"] | indexes["null_findings"]
    for ledger, specs in link_specs.items():
        for row in ledgers[ledger]:
            indexes = by_target[str(row["target_gene"])]
            for field, destination in specs:
                for local_id in scalar_list(row.get(field)):
                    if local_id not in indexes[destination]:
                        missing.append(f"{ledger}:{row['doc_id']} {field}->{local_id}")
    if missing:
        raise ValueError("unresolved ledger links: " + ", ".join(missing[:30]))


def build(source: Path, output_root: Path, repairs_path: Path) -> dict[str, Any]:
    repairs = load_repairs(repairs_path)
    applied_repairs: Counter[str] = Counter()
    ledgers: dict[str, list[dict[str, Any]]] = {name: [] for name in ID_FIELD}
    targets: set[str] = set()
    issues: list[dict[str, Any]] = []
    empty_sections: list[dict[str, str]] = []
    run_ids: set[str] = set()
    variants: set[str] = set()
    timestamps: list[str] = []
    report_count = 0

    with source.open(encoding="utf-8") as handle:
        for source_line, line in enumerate(handle, 1):
            if not line.strip():
                continue
            report_count += 1
            record = json.loads(line)
            target = str(record.get("gene_target") or "")
            report = record.get("report")
            if not target or not isinstance(report, str):
                raise ValueError(f"{source}:{source_line}: missing gene_target/report")
            if target in targets:
                raise ValueError(f"duplicate source target {target}")
            targets.add(target)
            run_ids.add(str(record.get("run_id") or ""))
            variants.add(str(record.get("dataset_variant") or ""))
            timestamps.append(str(record.get("sampled_at_utc") or ""))
            report_sha = sha256_bytes(report.encode("utf-8"))
            blocks, report_issues, report_empty = parse_appendix(
                report, target=target, repairs=repairs, applied_repairs=applied_repairs
            )
            issues.extend(report_issues)
            empty_sections.extend(
                {"target_gene": target, "section": section} for section in report_empty
            )
            for section, rows in blocks.items():
                ledger = LEDGER_BY_SECTION[section]
                for index, row in enumerate(rows, 1):
                    ledgers[ledger].append(
                        enrich_record(
                            row, target=target, source_line=source_line,
                            report_sha=report_sha, ledger=ledger, index=index,
                        )
                    )

    expected_repairs = {str(item["repair_id"]) for item in repairs}
    if set(applied_repairs) != expected_repairs or any(count != 1 for count in applied_repairs.values()):
        raise ValueError(
            f"repair application mismatch: expected={sorted(expected_repairs)} "
            f"applied={dict(sorted(applied_repairs.items()))}"
        )
    validate_links(ledgers)

    for ledger, rows in ledgers.items():
        id_field = ID_FIELD[ledger]
        rows.sort(key=lambda row: (str(row["target_gene"]).casefold(), str(row[id_field])))
        write_jsonl(output_root / "artifacts" / "ledgers" / f"{ledger}.jsonl", rows)

    audit = {
        "schema_version": "distributed_agents-corpus-extraction-audit-v1",
        "source": {
            "filename": source.name,
            "sha256": sha256_file(source),
            "bytes": source.stat().st_size,
            "records": report_count,
            "unique_targets": len(targets),
            "run_ids": sorted(run_ids),
            "dataset_variants": sorted(variants),
            "sampled_at_utc_min": min(timestamps),
            "sampled_at_utc_max": max(timestamps),
        },
        "ledger_records": {name: len(rows) for name, rows in sorted(ledgers.items())},
        "repairs_applied": dict(sorted(applied_repairs.items())),
        "issues": sorted(
            issues,
            key=lambda item: (
                str(item.get("target_gene", "")), str(item.get("section", "")),
                str(item.get("kind", "")), int(item.get("block_line", 0)),
            ),
        ),
        "empty_sections": sorted(
            empty_sections, key=lambda item: (item["target_gene"], item["section"])
        ),
        "build_policy": {
            "network": False,
            "model_calls": False,
            "incomplete_content": "quarantined_not_invented",
        },
    }
    audit_path = output_root / "artifacts" / "audits" / "extraction.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return audit


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-root", type=Path, default=RELEASE_ROOT)
    parser.add_argument("--repairs", type=Path, default=DEFAULT_REPAIRS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    audit = build(args.source.resolve(), args.output_root.resolve(), args.repairs.resolve())
    print(canonical_json({
        "source_records": audit["source"]["records"],
        "ledger_records": audit["ledger_records"],
        "issues": len(audit["issues"]),
        "repairs": sum(audit["repairs_applied"].values()),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
