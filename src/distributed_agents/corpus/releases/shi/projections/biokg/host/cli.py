"""Release-owned entry point for hosting BioKG with Neo4j and Apptainer."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

from ..paths import (
    HOST_OFFLINE_CONFIG,
    HOST_PLUGIN_DIR,
    NEO4J_DATA_DIR,
    NEO4J_DUMP_FILE,
    NEO4J_DUMP_MANIFEST_FILE,
    NEO4J_IMAGE_FILE,
    NEO4J_LOG_DIR,
)


LAUNCHER = Path(__file__).with_name("neo4j_apptainer.sh")


def launcher_environment(source: Mapping[str, str] | None = None) -> dict[str, str]:
    """Return launcher environment with projection defaults and caller overrides."""

    environment = dict(os.environ if source is None else source)
    defaults = {
        "BIOKG_NEO4J_DATA_DIR": str(NEO4J_DATA_DIR),
        "BIOKG_NEO4J_DUMP_FILE": str(NEO4J_DUMP_FILE),
        "BIOKG_NEO4J_DUMP_MANIFEST_FILE": str(NEO4J_DUMP_MANIFEST_FILE),
        "BIOKG_NEO4J_LOCAL_IMAGE": str(NEO4J_IMAGE_FILE),
        "BIOKG_NEO4J_LOG_DIR": str(NEO4J_LOG_DIR),
        "BIOKG_NEO4J_OFFLINE_CONFIG": str(HOST_OFFLINE_CONFIG),
        "BIOKG_NEO4J_PLUGIN_DIR": str(HOST_PLUGIN_DIR),
    }
    for name, value in defaults.items():
        environment.setdefault(name, value)
    return environment


def validate_dump_artifact(environment: Mapping[str, str]) -> None:
    """Fail before Apptainer when the complete dump is absent or corrupted."""

    dump_file = Path(environment["BIOKG_NEO4J_DUMP_FILE"])
    manifest_file = Path(environment["BIOKG_NEO4J_DUMP_MANIFEST_FILE"])
    if not dump_file.is_file():
        raise SystemExit(
            f"BioKG Neo4j dump is missing: {dump_file}\n"
            "Run git lfs pull for the release capsule or reinstall a complete release."
        )
    if not manifest_file.is_file():
        raise SystemExit(f"BioKG Neo4j dump manifest is missing: {manifest_file}")

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    artifact = manifest["artifact"]
    if dump_file.name != artifact["path"]:
        raise SystemExit(
            f"BioKG dump name mismatch: {dump_file.name} != {artifact['path']}"
        )
    actual_size = dump_file.stat().st_size
    if actual_size != artifact["size_bytes"]:
        raise SystemExit(
            f"BioKG dump size mismatch: {actual_size} != {artifact['size_bytes']}; "
            "run git lfs pull"
        )
    digest = hashlib.sha256()
    with dump_file.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    actual_sha256 = digest.hexdigest()
    if actual_sha256 != artifact["sha256"]:
        raise SystemExit(
            f"BioKG dump SHA-256 mismatch: {actual_sha256} != {artifact['sha256']}"
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=("pull", "restore", "up", "down", "list", "logs")
    )
    parser.add_argument(
        "lines",
        nargs="?",
        type=int,
        help="Number of lines to show; valid only for the logs action.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.lines is not None and args.action != "logs":
        _parser().error("lines is valid only for the logs action")
    environment = launcher_environment()
    if args.action == "restore":
        validate_dump_artifact(environment)
    command = ["bash", str(LAUNCHER), args.action]
    if args.lines is not None:
        command.append(str(args.lines))
    completed = subprocess.run(command, env=environment, check=False)
    return completed.returncode
