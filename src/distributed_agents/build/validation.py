"""Validation for the structured appendix emitted by the report builder."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from importlib.resources import files
from typing import Any, Iterable, Mapping

from jsonschema import Draft202012Validator, FormatChecker


REPORT_APPENDIX_SCHEMA_ID = "legacy_findings_appendix.schema.json"
REPORT_APPENDIX_SCHEMA_SHA256 = (
    "e4e4de66526b5ee6b0bf0339d9f236645fc41c3e127211f14e52621481b8ce7b"
)
APPENDIX_SECTIONS = (
    ("Evidence JSONL", "evidence"),
    ("References JSONL", "references"),
    ("Biological Findings JSONL", "biological_findings"),
    ("Literature Comparisons JSONL", "literature_comparisons"),
    ("Pathways JSONL", "pathways"),
    ("Cell Type Specificity JSONL", "cell_type_specificity"),
)
APPENDIX_HEADING_RE = re.compile(
    r"^#{1,6}\s+Structured Appendix\s*$", re.MULTILINE | re.IGNORECASE
)
FENCED_SECTION_RE = re.compile(
    r"^#{1,6}\s+(?P<name>.+?)\s*\n+```jsonl\s*\n(?P<body>.*?)\n```",
    re.DOTALL | re.MULTILINE,
)


class AppendixValidationError(ValueError):
    """Raised when a generated report violates the appendix contract."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


def _load_verified_schema() -> tuple[dict[str, Any], str]:
    resource = files(__package__).joinpath("schemas", REPORT_APPENDIX_SCHEMA_ID)
    if not resource.is_file():
        raise FileNotFoundError(
            f"build schema asset not found: {REPORT_APPENDIX_SCHEMA_ID}"
        )
    content = resource.read_text(encoding="utf-8")
    actual = hashlib.sha256(content.encode()).hexdigest()
    if actual != REPORT_APPENDIX_SCHEMA_SHA256:
        raise RuntimeError(
            f"canonical build schema {REPORT_APPENDIX_SCHEMA_ID!r} has SHA-256 "
            f"{actual}; expected {REPORT_APPENDIX_SCHEMA_SHA256}"
        )
    schema = json.loads(content)
    Draft202012Validator.check_schema(schema)
    return schema, actual


def _parse_jsonl(body: str, section: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, line in enumerate(body.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{section} line {line_number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(row, dict):
            errors.append(f"{section} line {line_number}: row must be an object")
            continue
        rows.append(row)
    if errors:
        raise AppendixValidationError(errors)
    return rows


def parse_structured_appendix(report: str, *, gene_target: str) -> dict[str, Any]:
    """Extract the six ordered JSONL ledgers into the schema's object shape."""

    heading = APPENDIX_HEADING_RE.search(report)
    if heading is None:
        raise AppendixValidationError(["missing Structured Appendix heading"])
    matches = list(FENCED_SECTION_RE.finditer(report[heading.end() :]))
    names = [match.group("name").strip() for match in matches]
    expected = [heading for heading, _ in APPENDIX_SECTIONS]
    if names != expected:
        raise AppendixValidationError(
            [
                "structured appendix must contain exactly these JSONL blocks in "
                f"order: {expected}; found {names}"
            ]
        )

    normalized: dict[str, Any] = {"gene_target": gene_target}
    for match, (section, key) in zip(matches, APPENDIX_SECTIONS, strict=True):
        normalized[key] = _parse_jsonl(match.group("body"), section)
    return normalized


def _path(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return ".".join(parts) if parts else "appendix"


def _require_unique_ids(
    rows: Iterable[Mapping[str, Any]], key: str, errors: list[str]
) -> set[str]:
    values = [str(row[key]) for row in rows]
    duplicates = sorted(
        value for value, count in Counter(values).items() if count > 1
    )
    if duplicates:
        errors.append(f"{key} values must be unique; duplicates: {duplicates}")
    return set(values)


def _missing(values: Iterable[str], allowed: set[str]) -> list[str]:
    return sorted(set(map(str, values)) - allowed)


def _check_links(
    row_name: str,
    field: str,
    values: Iterable[str],
    allowed: set[str],
    errors: list[str],
) -> None:
    missing = _missing(values, allowed)
    if missing:
        errors.append(f"{row_name}.{field} references unknown IDs: {missing}")


def _semantic_errors(appendix: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    evidence_ids = _require_unique_ids(appendix["evidence"], "evidence_id", errors)
    reference_ids = _require_unique_ids(appendix["references"], "ref_id", errors)
    finding_ids = _require_unique_ids(
        appendix["biological_findings"], "finding_id", errors
    )
    _require_unique_ids(
        appendix["literature_comparisons"], "comparison_id", errors
    )
    findings = {
        str(row["finding_id"]): row for row in appendix["biological_findings"]
    }

    for row in appendix["biological_findings"]:
        name = f"finding {row['finding_id']}"
        _check_links(name, "evidence_ids", row["evidence_ids"], evidence_ids, errors)
        _check_links(name, "ref_ids", row["ref_ids"], reference_ids, errors)
        if row["literature_status"] not in {None, "novel_no_direct_literature"}:
            if not row["ref_ids"]:
                errors.append(
                    f"{name} has literature_status but does not cite a reference"
                )

    for row in appendix["literature_comparisons"]:
        name = f"literature comparison {row['comparison_id']}"
        _check_links(name, "finding_id", [row["finding_id"]], finding_ids, errors)
        _check_links(name, "evidence_ids", row["evidence_ids"], evidence_ids, errors)
        _check_links(name, "ref_ids", row["ref_ids"], reference_ids, errors)
        finding = findings.get(str(row["finding_id"]))
        if finding is not None:
            _check_links(
                name,
                "evidence_ids outside linked finding",
                row["evidence_ids"],
                set(map(str, finding["evidence_ids"])),
                errors,
            )
            _check_links(
                name,
                "ref_ids outside linked finding",
                row["ref_ids"],
                set(map(str, finding["ref_ids"])),
                errors,
            )

    for index, row in enumerate(appendix["pathways"], 1):
        name = f"pathway row {index}"
        _check_links(name, "finding_ids", row["finding_ids"], finding_ids, errors)
        _check_links(name, "evidence_ids", row["evidence_ids"], evidence_ids, errors)
        cited = [findings[value] for value in row["finding_ids"] if value in findings]
        grounded_evidence = {
            str(value) for finding in cited for value in finding["evidence_ids"]
        }
        _check_links(
            name,
            "evidence_ids outside cited findings",
            row["evidence_ids"],
            grounded_evidence,
            errors,
        )

    for index, row in enumerate(appendix["cell_type_specificity"], 1):
        name = f"cell-type row {index}"
        _check_links(name, "finding_ids", row["finding_ids"], finding_ids, errors)
        _check_links(name, "evidence_ids", row["evidence_ids"], evidence_ids, errors)
        _check_links(name, "ref_ids", row["ref_ids"], reference_ids, errors)
        cited = [findings[value] for value in row["finding_ids"] if value in findings]
        grounded_evidence = {
            str(value) for finding in cited for value in finding["evidence_ids"]
        }
        grounded_references = {
            str(value) for finding in cited for value in finding["ref_ids"]
        }
        _check_links(
            name,
            "evidence_ids outside cited findings",
            row["evidence_ids"],
            grounded_evidence,
            errors,
        )
        _check_links(
            name,
            "ref_ids outside cited findings",
            row["ref_ids"],
            grounded_references,
            errors,
        )
    return errors


def validate_findings_report(report: str, *, gene_target: str) -> dict[str, Any]:
    """Parse and validate a report appendix, including cross-ledger grounding."""

    appendix = parse_structured_appendix(report, gene_target=gene_target)
    schema, _ = _load_verified_schema()
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = [
        f"{_path(error)}: {error.message}"
        for error in sorted(
            validator.iter_errors(appendix), key=lambda error: list(error.path)
        )
    ]
    if schema_errors:
        raise AppendixValidationError(schema_errors)
    semantic_errors = _semantic_errors(appendix)
    if semantic_errors:
        raise AppendixValidationError(semantic_errors)
    return appendix
