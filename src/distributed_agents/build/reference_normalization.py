"""Release-specific publication normalization using exact identifiers only."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator


PUBLICATION_MAPPING_SCHEMA_VERSION = "publication-reference-mapping-v2"
PUBLICATION_POLICY_ID = "exact-publication-identifiers-v2"
PUBLICATION_MAPPING_SCHEMA_ID = "publication_reference_mapping.schema.json"
PUBLICATION_MAPPING_SCHEMA_SHA256 = (
    "28a69bf867ab1e3a1f86d0d93a3d4d5d7c0418e09888bf8b176780f75b2cef98"
)
IDENTIFIER_PRIORITY = ("doi", "pmid", "pmcid")
NON_PUBLICATION_SOURCE_TYPES = ("clinicaltrials", "database")
NON_PUBLICATION_URL_HOSTS = (
    "accessdata.fda.gov",
    "cancer.gov",
    "dailymed.nlm.nih.gov",
    "ema.europa.eu",
    "fda.gov",
    "medlineplus.gov",
)
NON_PUBLICATION_SEARCH_PAGES = (
    "ncbi-eutils-esearch",
    "pubmed-query-without-record-id",
)
EXACT_URL_EXTENSIONS = (
    "europe-pmc-med-as-pmid",
    "europe-pmc-pmc-as-pmcid",
)
MULTIPLE_DOI_RULE = "prefer-single-exact-doi-url-matching-an-extracted-doi"

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"']+", re.IGNORECASE)
PMID_RES = (
    re.compile(r"\bPMID\s*[:/]?\s*(\d{5,10})\b", re.IGNORECASE),
    re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{5,10})", re.IGNORECASE),
    re.compile(r"ncbi\.nlm\.nih\.gov/pubmed/(\d{5,10})", re.IGNORECASE),
    re.compile(r"europepmc\.org/article/MED/(\d{5,10})(?:[/?#]|$)", re.IGNORECASE),
)
PMCID_RES = (
    re.compile(r"\bPMC\s*[-:]?\s*(\d{4,10})\b", re.IGNORECASE),
    re.compile(
        r"europepmc\.org/article/PMC/(?:PMC)?(\d{4,10})(?:[/?#]|$)",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class ExtractedIdentifiers:
    doi: tuple[str, ...]
    pmid: tuple[str, ...]
    pmcid: tuple[str, ...]
    non_publication: bool

    def as_dict(self) -> dict[str, list[str]]:
        return {
            "doi": list(self.doi),
            "pmid": list(self.pmid),
            "pmcid": list(self.pmcid),
        }

    def values(self, namespace: str) -> tuple[str, ...]:
        return getattr(self, namespace)

    @property
    def any(self) -> bool:
        return bool(self.doi or self.pmid or self.pmcid)

    @property
    def conflict(self) -> bool:
        return any(len(self.values(namespace)) > 1 for namespace in IDENTIFIER_PRIORITY)


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _trim_doi(value: str) -> str:
    doi = unquote(value).strip().lower()
    doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi\s*:\s*)", "", doi)
    doi = doi.split("?", 1)[0].split("#", 1)[0]
    doi = doi.rstrip(".,;:")
    pairs = (("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"))
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


def _extract_dois(text: str) -> set[str]:
    values = {_trim_doi(match.group(0)) for match in DOI_RE.finditer(unquote(text))}
    values.discard("")
    return values


def _extract_url_dois(url: str) -> set[str]:
    """Extract DOI URLs conservatively without swallowing publisher path IDs."""

    decoded = unquote(url)
    lowered = decoded.casefold()
    for marker in (
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
    ):
        offset = lowered.find(marker)
        if offset >= 0:
            value = _trim_doi(decoded[offset + len(marker) :])
            return {value} if value else set()
    if "biorxiv.org/content/" in lowered or "medrxiv.org/content/" in lowered:
        return _extract_dois(decoded)
    return set()


def _extract_pmids(text: str) -> set[str]:
    decoded = unquote(text)
    return {
        match.group(1)
        for pattern in PMID_RES
        for match in pattern.finditer(decoded)
    }


def _extract_pmcids(text: str) -> set[str]:
    decoded = unquote(text)
    return {
        f"PMC{match.group(1)}"
        for pattern in PMCID_RES
        for match in pattern.finditer(decoded)
    }


def _field_identifiers(namespace: str, value: str) -> set[str]:
    if not value:
        return set()
    if namespace == "doi":
        values = _extract_dois(value)
        if not values and _trim_doi(value).startswith("10."):
            values.add(_trim_doi(value))
        return values
    if namespace == "pmid":
        values = _extract_pmids(value)
        if not values and re.fullmatch(r"\d{5,10}", value):
            values.add(value)
        return values
    values = _extract_pmcids(value)
    compact = re.sub(r"[\s:-]", "", value).upper()
    if not values and re.fullmatch(r"PMC\d{4,10}", compact):
        values.add(compact)
    return values


def _publication_locator(url: str) -> bool:
    return bool(_extract_url_dois(url) or _extract_pmids(url) or _extract_pmcids(url))


def _normalized_url_host(url: str) -> str:
    host = (urlsplit(url).hostname or "").casefold()
    return host[4:] if host.startswith("www.") else host


def _non_publication_url(url: str) -> bool:
    parsed = urlsplit(url)
    host = _normalized_url_host(url)
    path = parsed.path.rstrip("/").casefold()
    if host in NON_PUBLICATION_URL_HOSTS:
        return True
    if host == "eutils.ncbi.nlm.nih.gov" and path.endswith("/esearch.fcgi"):
        return True
    return host == "pubmed.ncbi.nlm.nih.gov" and not _extract_pmids(url)


def extract_identifiers(row: Mapping[str, object]) -> ExtractedIdentifiers:
    """Extract exact identifiers, preferring explicit/citation values over URLs."""

    url = _text(row.get("url"))
    source_types = {
        value.strip().casefold()
        for value in _text(row.get("source_type")).split("|")
        if value.strip()
    }
    non_publication = bool(
        (source_types & set(NON_PUBLICATION_SOURCE_TYPES) or _non_publication_url(url))
        and not _publication_locator(url)
    )
    if non_publication:
        return ExtractedIdentifiers((), (), (), True)

    citation = _text(row.get("citation"))
    extracted: dict[str, set[str]] = {}
    for namespace in IDENTIFIER_PRIORITY:
        values = _field_identifiers(namespace, _text(row.get(namespace)))
        if namespace == "doi":
            values.update(_extract_dois(citation))
        elif namespace == "pmid":
            values.update(_extract_pmids(citation))
        else:
            values.update(_extract_pmcids(citation))
        if namespace == "doi":
            url_values = _extract_url_dois(url)
            values.update(url_values)
            if not values:
                values = _field_identifiers(namespace, url)
        elif not values:
            values = _field_identifiers(namespace, url)
        extracted[namespace] = values
    return ExtractedIdentifiers(
        *(tuple(sorted(extracted[name])) for name in IDENTIFIER_PRIORITY),
        non_publication=False,
    )


def _select_effective_identifiers(
    row: Mapping[str, object], extracted: ExtractedIdentifiers
) -> tuple[ExtractedIdentifiers, dict[str, object] | None]:
    """Apply an explicit URL-backed choice while preserving raw identifiers."""

    if len(extracted.doi) <= 1:
        return extracted, None
    url_dois = tuple(sorted(_extract_url_dois(_text(row.get("url")))))
    if len(url_dois) != 1 or url_dois[0] not in extracted.doi:
        return extracted, None
    selected = url_dois[0]
    effective = ExtractedIdentifiers(
        doi=(selected,),
        pmid=extracted.pmid,
        pmcid=extracted.pmcid,
        non_publication=extracted.non_publication,
    )
    selection = {
        "rule": MULTIPLE_DOI_RULE,
        "selected_canonical_reference_id": f"reference:doi:{selected}",
        "unselected_candidate_canonical_reference_ids": [
            f"reference:doi:{doi}" for doi in extracted.doi if doi != selected
        ],
    }
    return effective, selection


def _source_reference_id(row: Mapping[str, object]) -> str:
    doc_id = _text(row.get("doc_id"))
    if doc_id:
        return doc_id
    target = _text(row.get("target_gene"))
    ref_id = _text(row.get("ref_id"))
    if not target or not ref_id:
        raise ValueError("reference row requires doc_id or target_gene plus ref_id")
    return f"{target}:{ref_id}"


def _candidate_ids(identifiers: Mapping[str, Sequence[str]]) -> list[str]:
    return sorted(
        {
            f"reference:{namespace}:{identifier}"
            for namespace in IDENTIFIER_PRIORITY
            for identifier in identifiers[namespace]
        }
    )


def _canonical_reference(
    identifiers: Mapping[str, Sequence[str]],
) -> tuple[str, dict[str, object]]:
    namespace = next(name for name in IDENTIFIER_PRIORITY if identifiers[name])
    identifier = identifiers[namespace][0]
    return namespace, {
        "id": f"reference:{namespace}:{identifier}",
        "doi": identifiers["doi"][0] if identifiers["doi"] else None,
        "pmid": identifiers["pmid"][0] if identifiers["pmid"] else None,
        "pmcid": identifiers["pmcid"][0] if identifiers["pmcid"] else None,
    }


def _base_mapping(
    row: Mapping[str, object],
    extracted: ExtractedIdentifiers,
    selection: Mapping[str, object] | None,
) -> dict[str, object]:
    return {
        "source_reference_id": _source_reference_id(row),
        "target_gene": _text(row.get("target_gene")),
        "local_ref_id": _text(row.get("ref_id")),
        "source_record_sha256": _text(row.get("_source_record_sha256")) or None,
        "source_type": _text(row.get("source_type")),
        "resolution": "unresolved",
        "extracted": extracted.as_dict(),
        "selection": dict(selection) if selection is not None else None,
        "canonical": None,
        "candidate_canonical_reference_ids": _candidate_ids(extracted.as_dict()),
    }


def normalize_publication_references(
    rows: Sequence[Mapping[str, object]],
    *,
    release_id: str,
    source_path: str,
    source_format: str,
    source_sha256: str,
) -> dict[str, object]:
    """Build one immutable-source-linked mapping document for a release."""

    if source_format not in {"csv", "jsonl"}:
        raise ValueError(f"unsupported references format: {source_format!r}")
    if not rows:
        raise ValueError("references ledger is empty")

    row_by_id: dict[str, Mapping[str, object]] = {}
    raw_extracted_by_id: dict[str, ExtractedIdentifiers] = {}
    effective_by_id: dict[str, ExtractedIdentifiers] = {}
    selection_by_id: dict[str, dict[str, object] | None] = {}
    for row in rows:
        source_id = _source_reference_id(row)
        if source_id in row_by_id:
            raise ValueError(f"duplicate source reference id: {source_id}")
        if not _text(row.get("target_gene")) or not _text(row.get("ref_id")):
            raise ValueError(f"{source_id}: missing target_gene or ref_id")
        row_by_id[source_id] = row
        extracted = extract_identifiers(row)
        effective, selection = _select_effective_identifiers(row, extracted)
        raw_extracted_by_id[source_id] = extracted
        effective_by_id[source_id] = effective
        selection_by_id[source_id] = selection

    eligible_ids = [
        source_id
        for source_id, extracted in effective_by_id.items()
        if extracted.any and not extracted.conflict
    ]
    union_find = UnionFind(eligible_ids)
    first_by_identifier: dict[tuple[str, str], str] = {}
    for source_id in eligible_ids:
        extracted = effective_by_id[source_id]
        for namespace in IDENTIFIER_PRIORITY:
            for identifier in extracted.values(namespace):
                key = (namespace, identifier)
                first = first_by_identifier.setdefault(key, source_id)
                union_find.union(first, source_id)

    component_members: dict[str, list[str]] = defaultdict(list)
    for source_id in eligible_ids:
        component_members[union_find.find(source_id)].append(source_id)

    resolved_by_id: dict[str, tuple[str, dict[str, object]]] = {}
    component_conflicts: dict[str, dict[str, list[str]]] = {}
    for member_ids in component_members.values():
        identifiers = {
            namespace: sorted(
                {
                    identifier
                    for source_id in member_ids
                    for identifier in effective_by_id[source_id].values(namespace)
                }
            )
            for namespace in IDENTIFIER_PRIORITY
        }
        if any(len(identifiers[namespace]) > 1 for namespace in IDENTIFIER_PRIORITY):
            for source_id in member_ids:
                component_conflicts[source_id] = identifiers
            continue
        namespace, canonical = _canonical_reference(identifiers)
        for source_id in member_ids:
            resolved_by_id[source_id] = (namespace, canonical)

    mappings: list[dict[str, object]] = []
    for source_id in sorted(row_by_id):
        row = row_by_id[source_id]
        raw_extracted = raw_extracted_by_id[source_id]
        effective = effective_by_id[source_id]
        mapping = _base_mapping(row, raw_extracted, selection_by_id[source_id])
        if effective.non_publication:
            mapping["resolution"] = "non_publication"
        elif effective.conflict:
            mapping["resolution"] = "conflict"
        elif source_id in component_conflicts:
            mapping["resolution"] = "conflict"
            mapping["candidate_canonical_reference_ids"] = _candidate_ids(
                component_conflicts[source_id]
            )
        elif source_id in resolved_by_id:
            namespace, canonical = resolved_by_id[source_id]
            mapping["resolution"] = f"exact_{namespace}"
            mapping["canonical"] = canonical
            mapping["candidate_canonical_reference_ids"] = [canonical["id"]]
        mappings.append(mapping)

    unique_publications = {
        str(mapping["canonical"]["id"])
        for mapping in mappings
        if isinstance(mapping["canonical"], dict)
    }
    summary = {
        "total": len(mappings),
        "resolved": sum(str(row["resolution"]).startswith("exact_") for row in mappings),
        "unique_publications": len(unique_publications),
        "non_publication": sum(row["resolution"] == "non_publication" for row in mappings),
        "unresolved": sum(row["resolution"] == "unresolved" for row in mappings),
        "conflict": sum(row["resolution"] == "conflict" for row in mappings),
        "identifier_rows": {
            namespace: sum(
                bool(extracted.values(namespace))
                for extracted in effective_by_id.values()
            )
            for namespace in IDENTIFIER_PRIORITY
        },
    }
    document: dict[str, object] = {
        "schema_version": PUBLICATION_MAPPING_SCHEMA_VERSION,
        "release_id": release_id,
        "source": {
            "artifact": "references",
            "path": source_path,
            "format": source_format,
            "sha256": source_sha256,
            "records": len(rows),
        },
        "policy": {
            "id": PUBLICATION_POLICY_ID,
            "identifiers": list(IDENTIFIER_PRIORITY),
            "canonical_priority": list(IDENTIFIER_PRIORITY),
            "excluded_source_types": list(NON_PUBLICATION_SOURCE_TYPES),
            "exact_url_extensions": list(EXACT_URL_EXTENSIONS),
            "multiple_doi_rule": MULTIPLE_DOI_RULE,
            "non_publication_url_hosts": list(NON_PUBLICATION_URL_HOSTS),
            "non_publication_search_pages": list(NON_PUBLICATION_SEARCH_PAGES),
            "network_resolution": False,
            "fuzzy_matching": False,
        },
        "mappings": mappings,
        "summary": summary,
    }
    validator = Draft202012Validator(_load_mapping_schema())
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        raise ValueError(
            "invalid publication mapping document: "
            + "; ".join(error.message for error in errors[:20])
        )
    return document


def _load_mapping_schema() -> dict[str, object]:
    resource = files(__package__).joinpath("schemas", PUBLICATION_MAPPING_SCHEMA_ID)
    content = resource.read_text(encoding="utf-8")
    actual = hashlib.sha256(content.encode()).hexdigest()
    if actual != PUBLICATION_MAPPING_SCHEMA_SHA256:
        raise RuntimeError(
            f"publication mapping schema has SHA-256 {actual}; "
            f"expected {PUBLICATION_MAPPING_SCHEMA_SHA256}"
        )
    schema = json.loads(content)
    Draft202012Validator.check_schema(schema)
    return schema


def _read_reference_rows(path: Path, source_format: str) -> list[dict[str, object]]:
    if source_format == "csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if source_format == "jsonl":
        rows: list[dict[str, object]] = []
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
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_number}: expected an object")
                rows.append(row)
        return rows
    raise ValueError(f"unsupported references format: {source_format!r}")


def normalize_release_publications(release_root: Path) -> dict[str, object]:
    """Load and verify one release's reference artifact, then normalize it."""

    root = release_root.expanduser().resolve()
    manifest_path = root / "release.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"release manifest does not exist: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    release_id = _text(manifest.get("release_id"))
    try:
        spec = manifest["artifacts"]["references"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{manifest_path}: missing references artifact") from exc
    relative_path = _text(spec.get("path"))
    source_path = (root / relative_path).resolve()
    if not source_path.is_relative_to(root):
        raise ValueError(f"references path escapes release: {relative_path}")
    if not source_path.is_file():
        raise FileNotFoundError(f"references artifact does not exist: {source_path}")
    actual_sha = _sha256(source_path)
    if actual_sha != spec.get("sha256"):
        raise ValueError(
            f"references SHA-256 {actual_sha} != manifest {spec.get('sha256')}"
        )
    if source_path.stat().st_size != spec.get("bytes"):
        raise ValueError("references byte size does not match release manifest")
    rows = _read_reference_rows(source_path, _text(spec.get("format")))
    if len(rows) != spec.get("records"):
        raise ValueError("references record count does not match release manifest")
    return normalize_publication_references(
        rows,
        release_id=release_id,
        source_path=relative_path,
        source_format=_text(spec.get("format")),
        source_sha256=actual_sha,
    )


def write_release_publication_mapping(
    release_root: Path, *, output: Path
) -> dict[str, object]:
    document = normalize_release_publications(release_root)
    destination = output.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return document


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Build a release-specific publication map using exact DOI, PMID, "
            "and PMCID identifiers."
        )
    )
    result.add_argument("--release-root", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        document = write_release_publication_mapping(
            args.release_root, output=args.output
        )
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(document["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
