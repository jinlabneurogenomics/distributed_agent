"""Deterministic normalization of perturbation targets to an MGI snapshot."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Iterable, Iterator

from jsonschema import Draft202012Validator


MGI_MAPPING_SCHEMA_VERSION = "mgi-target-mapping-v1"
MGI_VERSION = "6.24"
MGI_REPORT_NAME = "MRK_List1.rpt.gz"
MGI_REPORT_URL = (
    "https://www.informatics.jax.org/downloads/reports/MRK_List1.rpt.gz"
)
MGI_MAPPING_SCHEMA_ID = "mgi_target_mapping.schema.json"
MGI_MAPPING_SCHEMA_SHA256 = (
    "9773e0cb624b7fe06565389e403fc6983af779b43c75cc53546e3ffdd4924379"
)
MGI_ACCESSION_RE = re.compile(r"^MGI:[0-9]+$")
SAFE_TARGET_RE = re.compile(r"^Safe_target_[0-9]+$")


@dataclass(frozen=True)
class MgiMarker:
    accession_id: str | None
    symbol: str
    status: str
    marker_type: str
    feature_types: tuple[str, ...]
    synonyms: tuple[str, ...]
    current_accession_id: str | None
    current_symbol: str | None

    @property
    def withdrawn(self) -> bool:
        return self.status.casefold() in {"w", "withdrawn"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _split_pipe(value: str) -> tuple[str, ...]:
    return tuple(sorted({item.strip() for item in value.split("|") if item.strip()}))


def _open_report(path: Path):
    if path.suffix.casefold() == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open(encoding="utf-8")


def read_mgi_markers(path: Path) -> list[MgiMarker]:
    """Read MGI's 14-column MRK_List1 report, including withdrawn markers."""

    markers: list[MgiMarker] = []
    seen_accessions: set[str] = set()
    with _open_report(path) as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            fields = line.rstrip("\r\n").split("\t")
            if fields[0] in {"MGI Accession ID", "MGI Marker Accession ID"}:
                continue
            if len(fields) != 14:
                raise ValueError(
                    f"{path}:{line_number}: expected 14 MRK_List1 fields, "
                    f"found {len(fields)}"
                )
            raw_accession_id = fields[0].strip()
            accession_id = (
                raw_accession_id
                if MGI_ACCESSION_RE.fullmatch(raw_accession_id)
                else None
            )
            if accession_id is None and raw_accession_id.casefold() not in {
                "",
                "null",
            }:
                raise ValueError(
                    f"{path}:{line_number}: invalid MGI accession "
                    f"{raw_accession_id!r}"
                )
            if accession_id is not None and accession_id in seen_accessions:
                raise ValueError(
                    f"{path}:{line_number}: duplicate MGI accession {accession_id}"
                )
            if accession_id is not None:
                seen_accessions.add(accession_id)
            raw_current_accession_id = fields[12].strip()
            current_accession_id = (
                None
                if raw_current_accession_id.casefold() in {"", "null"}
                else raw_current_accession_id
            )
            if current_accession_id and not MGI_ACCESSION_RE.fullmatch(
                current_accession_id
            ):
                raise ValueError(
                    f"{path}:{line_number}: invalid current MGI accession "
                    f"{current_accession_id!r}"
                )
            markers.append(
                MgiMarker(
                    accession_id=accession_id,
                    symbol=fields[6].strip(),
                    status=fields[7].strip(),
                    marker_type=fields[9].strip(),
                    feature_types=_split_pipe(fields[10]),
                    synonyms=_split_pipe(fields[11]),
                    current_accession_id=current_accession_id,
                    current_symbol=fields[13].strip() or None,
                )
            )
    if not markers:
        raise ValueError(f"{path}: MGI report is empty")
    return markers


def _canonical_marker(
    marker: MgiMarker, markers_by_id: dict[str, MgiMarker]
) -> MgiMarker:
    if not marker.withdrawn:
        return marker
    if marker.current_accession_id in markers_by_id:
        return markers_by_id[marker.current_accession_id]
    if marker.current_accession_id and marker.current_symbol:
        return MgiMarker(
            accession_id=marker.current_accession_id,
            symbol=marker.current_symbol,
            status="current target of withdrawn marker",
            marker_type=marker.marker_type,
            feature_types=marker.feature_types,
            synonyms=(),
            current_accession_id=None,
            current_symbol=None,
        )
    return marker


def _index_add(
    index: dict[str, list[tuple[MgiMarker, MgiMarker, str]]],
    key: str,
    source: MgiMarker,
    canonical: MgiMarker,
    matched_value: str,
) -> None:
    if key:
        index[key].append((source, canonical, matched_value))


def _deduplicate_candidates(
    candidates: Iterable[tuple[MgiMarker, MgiMarker, str]],
) -> list[tuple[MgiMarker, MgiMarker, str]]:
    unique: dict[str, tuple[MgiMarker, MgiMarker, str]] = {}
    for source, canonical, matched_value in candidates:
        key = canonical.accession_id or f"unresolved:{source.symbol}"
        unique.setdefault(key, (source, canonical, matched_value))
    return [unique[key] for key in sorted(unique)]


def _candidate_indexes(markers: list[MgiMarker]):
    markers_by_id = {
        marker.accession_id: marker
        for marker in markers
        if marker.accession_id is not None
    }
    indexes = {
        name: defaultdict(list)
        for name in (
            "mgi_accession_id",
            "official_symbol",
            "withdrawn_symbol",
            "synonym",
            "casefold_official_symbol",
            "casefold_withdrawn_symbol",
            "casefold_synonym",
        )
    }
    for marker in markers:
        canonical = _canonical_marker(marker, markers_by_id)
        _index_add(
            indexes["mgi_accession_id"],
            marker.accession_id or "",
            marker,
            canonical,
            marker.accession_id,
        )
        symbol_kind = "withdrawn_symbol" if marker.withdrawn else "official_symbol"
        _index_add(
            indexes[symbol_kind],
            marker.symbol,
            marker,
            canonical,
            marker.symbol,
        )
        _index_add(
            indexes[f"casefold_{symbol_kind}"],
            marker.symbol.casefold(),
            marker,
            canonical,
            marker.symbol,
        )
        for synonym in marker.synonyms:
            _index_add(
                indexes["synonym"], synonym, marker, canonical, synonym
            )
            _index_add(
                indexes["casefold_synonym"],
                synonym.casefold(),
                marker,
                canonical,
                synonym,
            )
    return indexes


def _resolution_stages(target: str) -> Iterator[tuple[str, str]]:
    if MGI_ACCESSION_RE.fullmatch(target):
        yield "mgi_accession_id", target
    yield "official_symbol", target
    yield "withdrawn_symbol", target
    yield "synonym", target
    folded = target.casefold()
    yield "casefold_official_symbol", folded
    yield "casefold_withdrawn_symbol", folded
    yield "casefold_synonym", folded


def _unresolved_mapping(target: str, method: str) -> dict[str, object]:
    return {
        "input_target": target,
        "normalized_symbol": None,
        "mgi_accession_id": None,
        "match_method": method,
        "matched_value": None,
        "source_marker_status": None,
        "marker_type": None,
        "feature_types": [],
        "candidate_mgi_accession_ids": [],
        "candidate_symbols": [],
    }


def _resolve_target(target: str, indexes) -> dict[str, object]:
    if SAFE_TARGET_RE.fullmatch(target):
        return _unresolved_mapping(target, "non_gene_control")
    for method, key in _resolution_stages(target):
        candidates = _deduplicate_candidates(indexes[method].get(key, ()))
        if not candidates:
            continue
        if len(candidates) > 1:
            row = _unresolved_mapping(target, "ambiguous")
            row["matched_value"] = key
            row["candidate_mgi_accession_ids"] = [
                canonical.accession_id
                for _, canonical, _ in candidates
                if canonical.accession_id is not None
            ]
            row["candidate_symbols"] = sorted(
                {canonical.symbol for _, canonical, _ in candidates},
                key=lambda value: (value.casefold(), value),
            )
            return row
        source, canonical, matched_value = candidates[0]
        if canonical.accession_id is None:
            method = (
                "withdrawn_without_replacement"
                if source.withdrawn
                else "unmapped"
            )
            row = _unresolved_mapping(target, method)
            row.update(
                {
                    "matched_value": matched_value,
                    "source_marker_status": source.status or "unknown",
                    "marker_type": source.marker_type or "unknown",
                    "feature_types": list(source.feature_types),
                    "candidate_mgi_accession_ids": [],
                    "candidate_symbols": [source.symbol],
                }
            )
            return row
        return {
            "input_target": target,
            "normalized_symbol": canonical.symbol,
            "mgi_accession_id": canonical.accession_id,
            "match_method": method,
            "matched_value": matched_value,
            "source_marker_status": source.status or "unknown",
            "marker_type": canonical.marker_type or "unknown",
            "feature_types": list(canonical.feature_types),
            "candidate_mgi_accession_ids": [canonical.accession_id],
            "candidate_symbols": [canonical.symbol],
        }
    return _unresolved_mapping(target, "unmapped")


def _load_mapping_schema() -> dict[str, object]:
    resource = files(__package__).joinpath("schemas", MGI_MAPPING_SCHEMA_ID)
    content = resource.read_text(encoding="utf-8")
    actual = hashlib.sha256(content.encode()).hexdigest()
    if actual != MGI_MAPPING_SCHEMA_SHA256:
        raise RuntimeError(
            f"MGI mapping schema has SHA-256 {actual}; "
            f"expected {MGI_MAPPING_SCHEMA_SHA256}"
        )
    schema = json.loads(content)
    Draft202012Validator.check_schema(schema)
    return schema


def normalize_targets_to_mgi(
    targets: Iterable[str],
    *,
    marker_report: Path,
    mgi_version: str = MGI_VERSION,
) -> dict[str, object]:
    """Map targets conservatively using an exact, hash-recorded MGI report."""

    if mgi_version != MGI_VERSION:
        raise ValueError(f"expected MGI {MGI_VERSION}, found {mgi_version!r}")
    report = marker_report.expanduser().resolve()
    if not report.is_file():
        raise FileNotFoundError(f"MGI marker report does not exist: {report}")
    normalized_targets = sorted(
        {str(target).strip() for target in targets if str(target).strip()},
        key=lambda value: (value.casefold(), value),
    )
    if not normalized_targets:
        raise ValueError("at least one non-empty target is required")

    indexes = _candidate_indexes(read_mgi_markers(report))
    mappings = [_resolve_target(target, indexes) for target in normalized_targets]
    method_counts = {
        method: sum(row["match_method"] == method for row in mappings)
        for method in (
            "ambiguous",
            "unmapped",
            "withdrawn_without_replacement",
            "non_gene_control",
        )
    }
    document: dict[str, object] = {
        "schema_version": MGI_MAPPING_SCHEMA_VERSION,
        "source": {
            "database": "MGI",
            "version": mgi_version,
            "report": MGI_REPORT_NAME,
            "url": MGI_REPORT_URL,
            "sha256": _sha256(report),
        },
        "mappings": mappings,
        "summary": {
            "total": len(mappings),
            "mapped": len(mappings)
            - method_counts["ambiguous"]
            - method_counts["unmapped"]
            - method_counts["withdrawn_without_replacement"]
            - method_counts["non_gene_control"],
            "controls": method_counts["non_gene_control"],
            "ambiguous": method_counts["ambiguous"],
            "unmapped": method_counts["unmapped"]
            + method_counts["withdrawn_without_replacement"],
        },
    }
    validator = Draft202012Validator(_load_mapping_schema())
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        raise ValueError(
            "invalid MGI mapping document: "
            + "; ".join(error.message for error in errors)
        )
    return document


def write_mgi_target_mapping(
    targets: Iterable[str],
    *,
    marker_report: Path,
    output: Path,
    mgi_version: str = MGI_VERSION,
) -> dict[str, object]:
    """Normalize targets and write the deterministic mapping ledger."""

    document = normalize_targets_to_mgi(
        targets, marker_report=marker_report, mgi_version=mgi_version
    )
    destination = output.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return document


def _targets_from_jsonl(path: Path, field: str) -> list[str]:
    targets: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{path}:{line_number}: invalid JSON ({exc.msg})"
                ) from exc
            if not isinstance(row, dict) or not str(row.get(field) or "").strip():
                raise ValueError(
                    f"{path}:{line_number}: missing non-empty field {field!r}"
                )
            targets.append(str(row[field]))
    return targets


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Build a source-hashed MGI 6.24 target-normalization ledger."
    )
    result.add_argument("--marker-report", type=Path, required=True)
    result.add_argument("--targets-jsonl", type=Path, required=True)
    result.add_argument("--target-field", default="gene_target")
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--mgi-version", default=MGI_VERSION)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        document = write_mgi_target_mapping(
            _targets_from_jsonl(args.targets_jsonl, args.target_field),
            marker_report=args.marker_report,
            output=args.output,
            mgi_version=args.mgi_version,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(document["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
