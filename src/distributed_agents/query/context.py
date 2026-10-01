"""Selectable dataset portraits, lightweight identity checks, and snapshots."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


DATASET_CONTEXT_SCHEMA_VERSION = "distributed_agents-dataset-context-v1"
DATASET_MANIFEST_SCHEMA_VERSION = "distributed_agents-dataset-manifest-v1"
DATASET_CONTEXT_MARKER_PREFIX = "<!-- DISTRIBUTED_AGENTS_DATASET_CONTEXT:"


def canonical_dataset_context_path(skills_root: Path) -> Path:
    """Resolve the project-owned canonical context below a combined skills root."""

    root = skills_root.expanduser().resolve()
    candidates = (
        root / "runtime" / "dataset-orchestrator-skill" / "DATASET_CONTEXT.md",
        root / "distributed_agents" / "dataset-orchestrator-skill" / "DATASET_CONTEXT.md",
        root / "dataset-orchestrator-skill" / "DATASET_CONTEXT.md",
    )
    return next((path for path in candidates if path.is_file()), candidates[0])


def canonical_dataset_manifest_path(skills_root: Path) -> Path:
    """Resolve the manifest owned by the selected orchestrator dataset."""

    return canonical_dataset_context_path(skills_root).with_name(
        "DATASET_MANIFEST.json"
    )


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_dataset_context(
    source_path: Path,
    snapshot_path: Path,
    manifest_path: Path,
) -> dict[str, str]:
    """Copy the canonical context exactly and write its provenance manifest."""

    source_path = source_path.expanduser().resolve()
    snapshot_path = snapshot_path.expanduser().resolve()
    manifest_path = manifest_path.expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"dataset context source is missing: {source_path}")
    content = source_path.read_bytes()
    if not content.strip():
        raise ValueError(f"dataset context source is empty: {source_path}")

    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_bytes(content)
    source_sha256 = sha256_path(source_path)
    snapshot_sha256 = sha256_path(snapshot_path)
    if source_sha256 != snapshot_sha256:
        raise RuntimeError("dataset context snapshot differs from its canonical source")

    manifest = {
        "schema_version": DATASET_CONTEXT_SCHEMA_VERSION,
        "source_path": str(source_path),
        "source_sha256": source_sha256,
        "snapshot_path": str(snapshot_path),
        "snapshot_sha256": snapshot_sha256,
    }
    dataset_manifest_path = source_path.with_name("DATASET_MANIFEST.json")
    if dataset_manifest_path.is_file():
        dataset_manifest = load_dataset_manifest(dataset_manifest_path)
        manifest.update(
            {
                "dataset_manifest_path": str(dataset_manifest_path),
                "dataset_id": str(dataset_manifest["dataset_id"]),
                "experiment_id": str(dataset_manifest["experiment_id"]),
                "portrait_marker": str(dataset_manifest["portrait"]["marker"]),
            }
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_dataset_manifest(manifest_path: Path) -> dict[str, object]:
    """Load and validate a small committed dataset identity manifest."""

    path = manifest_path.expanduser().resolve()
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("dataset manifest must contain one JSON object")
    if value.get("schema_version") != DATASET_MANIFEST_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported dataset manifest schema: {value.get('schema_version')!r}"
        )
    for field in (
        "dataset_id",
        "experiment_id",
        "portrait",
        "input_artifacts",
        "cell_vocabulary_version",
        "semantic_lineage",
    ):
        if not value.get(field):
            raise ValueError(f"dataset manifest lacks {field}")
    portrait = value["portrait"]
    if not isinstance(portrait, dict):
        raise ValueError("dataset manifest portrait must be an object")
    marker = str(portrait.get("marker") or "")
    if not marker.startswith(DATASET_CONTEXT_MARKER_PREFIX):
        raise ValueError("dataset manifest portrait marker is invalid")
    artifacts = value["input_artifacts"]
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("dataset manifest input_artifacts must be non-empty")
    for role, artifact in artifacts.items():
        if not isinstance(artifact, dict):
            raise ValueError(f"dataset artifact role {role!r} must be an object")
        filenames = artifact.get("filenames")
        if not isinstance(filenames, list) or not filenames:
            raise ValueError(f"dataset artifact role {role!r} lacks filenames")
        if any(Path(str(name)).name != str(name) for name in filenames):
            raise ValueError(
                f"dataset artifact role {role!r} filenames must be basenames"
            )
    lineage = value["semantic_lineage"]
    if not isinstance(lineage, dict):
        raise ValueError("dataset manifest semantic_lineage must be an object")
    if lineage.get("experiment_id") != value.get("experiment_id"):
        raise ValueError("semantic corpus lineage points to a different experiment")
    return value


def validate_input_artifact(
    manifest_path: Path,
    *,
    role: str,
    input_path: Path,
) -> dict[str, str]:
    """Validate one declared input by role and filename, without large hashes."""

    manifest = load_dataset_manifest(manifest_path)
    artifacts = manifest["input_artifacts"]
    assert isinstance(artifacts, dict)
    artifact = artifacts.get(role)
    if not isinstance(artifact, dict):
        raise ValueError(f"unknown dataset input role: {role!r}")
    filenames = {str(name) for name in artifact["filenames"]}
    observed = input_path.expanduser().resolve().name
    if observed not in filenames:
        raise ValueError(
            f"dataset role {role!r} expects one of {sorted(filenames)}, "
            f"observed {observed!r}"
        )
    return {
        "dataset_id": str(manifest["dataset_id"]),
        "experiment_id": str(manifest["experiment_id"]),
        "role": role,
        "filename": observed,
    }


def load_dataset_context_manifest(
    manifest_path: Path,
    *,
    verify_files: bool = True,
    verify_source: bool = False,
) -> dict[str, str]:
    """Load a snapshot manifest and verify the durable snapshot when requested."""

    manifest_path = manifest_path.expanduser().resolve()
    value = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("dataset context manifest must contain one JSON object")
    if value.get("schema_version") != DATASET_CONTEXT_SCHEMA_VERSION:
        raise ValueError(
            "unsupported dataset context schema: "
            f"{value.get('schema_version')!r}"
        )
    required = (
        "source_path",
        "source_sha256",
        "snapshot_path",
        "snapshot_sha256",
    )
    missing = [field for field in required if not str(value.get(field) or "").strip()]
    if missing:
        raise ValueError(f"dataset context manifest lacks fields: {missing}")
    manifest = {str(key): str(item) for key, item in value.items()}

    if verify_files:
        snapshot = Path(manifest["snapshot_path"]).expanduser().resolve()
        if not snapshot.is_file():
            raise ValueError(f"dataset context snapshot_path is missing: {snapshot}")
        observed = sha256_path(snapshot)
        if observed != manifest["snapshot_sha256"]:
            raise ValueError(
                "dataset context snapshot_path hash mismatch: "
                f"expected {manifest['snapshot_sha256']}, observed {observed}"
            )
        if manifest["source_sha256"] != manifest["snapshot_sha256"]:
            raise ValueError("dataset context source and snapshot hashes differ")
        if verify_source:
            source = Path(manifest["source_path"]).expanduser().resolve()
            if not source.is_file():
                raise ValueError(f"dataset context source_path is missing: {source}")
            source_observed = sha256_path(source)
            if source_observed != manifest["source_sha256"]:
                raise ValueError(
                    "dataset context source_path hash mismatch: "
                    f"expected {manifest['source_sha256']}, observed {source_observed}"
                )
    return manifest
