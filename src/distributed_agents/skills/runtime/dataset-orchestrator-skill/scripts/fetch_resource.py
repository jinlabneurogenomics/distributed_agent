#!/usr/bin/env python3
"""Fetch one versioned HTTPS data resource into an exact run directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


DATA_SUFFIXES = frozenset(
    {
        ".csv",
        ".tsv",
        ".json",
        ".jsonl",
        ".parquet",
        ".txt",
        ".xml",
        ".obo",
        ".gmt",
        ".bed",
        ".vcf",
        ".fa",
        ".fasta",
        ".gz",
    }
)
EXECUTABLE_CONTENT_TYPES = (
    "application/x-executable",
    "application/x-sharedlib",
    "application/x-shellscript",
    "application/vnd.microsoft.portable-executable",
)
HTML_CONTENT_TYPES = frozenset({"text/html", "application/xhtml+xml"})
HTML_PREFIXES = (b"<!doctype html", b"<html")


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def resolve_run_path(run_dir: Path, relative: str, *, label: str) -> Path:
    """Resolve a relative output below run_dir without trusting traversal."""

    root = run_dir.expanduser().resolve()
    raw = Path(relative)
    if raw.is_absolute():
        raise ValueError(f"{label} must be relative to --run-dir")
    candidate = (root / raw).resolve()
    if not _inside(root, candidate) or candidate == root:
        raise ValueError(f"{label} escapes --run-dir")
    if any(part in {".git", "__pycache__"} for part in candidate.parts):
        raise ValueError(f"{label} may not write repository or executable metadata")
    return candidate


def validate_data_destination(path: Path) -> None:
    """Reject destinations that are not recognizable data files."""

    suffixes = [suffix.casefold() for suffix in path.suffixes]
    if not suffixes or suffixes[-1] not in DATA_SUFFIXES:
        raise ValueError(
            "resource output must use a recognized data suffix; runtime code, "
            "skills, packages, and executables are forbidden"
        )
    if suffixes[-1] == ".gz":
        if len(suffixes) < 2 or suffixes[-2] not in DATA_SUFFIXES - {".gz"}:
            raise ValueError(".gz resources require a recognizable data suffix")


def _looks_like_html(payload: bytes) -> bool:
    """Recognize an obvious HTML landing or verification document."""

    prefix = payload.lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    return prefix.startswith(HTML_PREFIXES)


def fetch_resource(
    *,
    run_dir: Path,
    url: str,
    output: str,
    provider: str,
    release: str,
    license_notes: str,
    expected_schema: str,
    manifest: str | None = None,
    expected_sha256: str | None = None,
    expected_size: int | None = None,
    timeout: float = 60.0,
) -> dict[str, object]:
    """Download and validate one data resource, then write its manifest."""

    parsed = urlparse(url)
    if parsed.scheme.casefold() != "https" or not parsed.netloc:
        raise ValueError("resource URL must be an absolute HTTPS URL")
    metadata = {
        "provider": provider.strip(),
        "release": release.strip(),
        "license_notes": license_notes.strip(),
        "expected_schema": expected_schema.strip(),
    }
    missing = [key for key, value in metadata.items() if not value]
    if missing:
        raise ValueError(f"resource metadata lacks required fields: {missing}")
    if expected_size is not None and expected_size < 0:
        raise ValueError("expected_size must be non-negative")
    if expected_sha256 is not None:
        expected_sha256 = expected_sha256.casefold().strip()
        if len(expected_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in expected_sha256
        ):
            raise ValueError("expected_sha256 must be a 64-character hex digest")

    destination = resolve_run_path(run_dir, output, label="output")
    validate_data_destination(destination)
    manifest_path = resolve_run_path(
        run_dir,
        manifest or f"{output}.resource.json",
        label="manifest",
    )
    if manifest_path == destination:
        raise ValueError("manifest and output paths must differ")

    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    size = 0
    final_url = url
    content_type = ""
    temp_path: Path | None = None
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            final_url = response.geturl()
            if urlparse(final_url).scheme.casefold() != "https":
                raise ValueError("resource redirect left HTTPS")
            content_type = str(response.headers.get_content_type() or "").casefold()
            if content_type in EXECUTABLE_CONTENT_TYPES:
                raise ValueError(f"resource has executable content type: {content_type}")
            if content_type in HTML_CONTENT_TYPES:
                raise ValueError(
                    "resource returned HTML instead of the requested data; "
                    "use the provider's documented data URL or public archive"
                )
            with tempfile.NamedTemporaryFile(
                dir=destination.parent,
                prefix=f".{destination.name}.",
                suffix=".part",
                delete=False,
            ) as handle:
                temp_path = Path(handle.name)
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    if size == 0 and _looks_like_html(chunk[:1024]):
                        raise ValueError(
                            "resource payload is HTML instead of the requested data; "
                            "use the provider's documented data URL or public archive"
                        )
                    handle.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
                handle.flush()
                os.fsync(handle.fileno())

        observed_sha256 = digest.hexdigest()
        if expected_size is not None and size != expected_size:
            raise ValueError(
                f"resource size mismatch: expected {expected_size}, observed {size}"
            )
        if expected_sha256 is not None and observed_sha256 != expected_sha256:
            raise ValueError(
                "resource checksum mismatch: "
                f"expected {expected_sha256}, observed {observed_sha256}"
            )
        assert temp_path is not None
        os.replace(temp_path, destination)
        temp_path = None

        result: dict[str, object] = {
            "schema_version": "distributed_agents-resource-manifest-v1",
            "provider": metadata["provider"],
            "release": metadata["release"],
            "urls": {
                "requested": url,
                "resolved": final_url,
            },
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "output_path": str(destination),
            "sha256": observed_sha256,
            "size_bytes": size,
            "license_access_notes": metadata["license_notes"],
            "expected_schema": metadata["expected_schema"],
            "content_type": content_type,
            "validation": {
                "status": "passed",
                "https": True,
                "data_suffix": destination.suffix.casefold(),
                "checksum_expected": expected_sha256,
                "checksum_verified": expected_sha256 is not None,
                "size_expected": expected_size,
                "size_verified": expected_size is not None,
            },
        }
        manifest_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return result
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--provider", required=True)
    parser.add_argument("--release", required=True)
    parser.add_argument("--license-notes", required=True)
    parser.add_argument("--expected-schema", required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--expected-size", type=int)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    result = fetch_resource(
        run_dir=args.run_dir,
        url=args.url,
        output=args.output,
        manifest=args.manifest,
        provider=args.provider,
        release=args.release,
        license_notes=args.license_notes,
        expected_schema=args.expected_schema,
        expected_sha256=args.expected_sha256,
        expected_size=args.expected_size,
        timeout=args.timeout,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
