"""Discovery and selection of corpus release capsules."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

import jsonschema

from .models import CorpusRegistryError, CorpusRelease


CORPUS_ROOT = Path(__file__).resolve().parent
RELEASES_ROOT = CORPUS_ROOT / "releases"
CURRENT_RELEASE_PATH = CORPUS_ROOT / "current_release.json"
RELEASE_SCHEMA_PATH = CORPUS_ROOT / "schemas" / "release-v1.schema.json"
DEFAULT_RELEASE_ENV = "DISTRIBUTED_AGENTS_CORPUS_RELEASE"
RELEASE_ROOTS_ENV = "DISTRIBUTED_AGENTS_CORPUS_RELEASE_ROOTS"
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CorpusRegistryError(f"missing registry file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CorpusRegistryError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CorpusRegistryError(f"expected a JSON object in {path}")
    return value


def _schema() -> dict[str, Any]:
    return _read_json(RELEASE_SCHEMA_PATH)


def _load_release(manifest_path: Path) -> CorpusRelease:
    manifest = _read_json(manifest_path)
    try:
        jsonschema.validate(instance=manifest, schema=_schema())
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        raise CorpusRegistryError(
            f"invalid release manifest {manifest_path} at {location}: {exc.message}"
        ) from exc
    release = CorpusRelease(
        release_id=str(manifest["release_id"]),
        root=manifest_path.parent.resolve(),
        manifest_path=manifest_path.resolve(),
        manifest=manifest,
    )
    for spec in manifest["artifacts"].values():
        release.resolve(str(spec["path"]))
        if spec.get("schema"):
            release.resolve(str(spec["schema"]))
    release.skills_root
    skills = manifest["capabilities"]["skills"]
    declared_names = set(skills["names"])
    for role, role_spec in skills["roles"].items():
        if role_spec["skill"] not in declared_names:
            raise CorpusRegistryError(
                f"release {release.release_id!r} skill role {role!r} references "
                f"undeclared skill {role_spec['skill']!r}"
            )
        release.skill(role)
        for entrypoint_name in role_spec["entrypoints"]:
            release.skill_entrypoint(role, entrypoint_name)
    release.tooling_root
    for entrypoint_name in manifest["capabilities"]["tooling"]["entrypoints"]:
        release.tooling_entrypoint(str(entrypoint_name))
    for spec in manifest["capabilities"].get("projections", {}).values():
        release.resolve(str(spec["path"]))
    return release


def release_roots(
    *, environ: Mapping[str, str] | None = None
) -> tuple[Path, ...]:
    """Return configured capsule roots, or the source-tree migration root."""

    environment = os.environ if environ is None else environ
    configured = environment.get(RELEASE_ROOTS_ENV, "").strip()
    if not configured:
        return (RELEASES_ROOT.resolve(),)
    roots = tuple(
        dict.fromkeys(
            Path(value).expanduser().resolve()
            for value in configured.split(os.pathsep)
            if value.strip()
        )
    )
    if not roots:
        raise CorpusRegistryError(
            f"{RELEASE_ROOTS_ENV} must contain at least one path"
        )
    return roots


def available_releases(
    *, environ: Mapping[str, str] | None = None
) -> dict[str, CorpusRelease]:
    """Return installed manifest-bearing releases by stable release ID."""

    releases: dict[str, CorpusRelease] = {}
    for root in release_roots(environ=environ):
        if not root.is_dir():
            continue
        for manifest_path in sorted(root.glob("*/release.json")):
            release = _load_release(manifest_path)
            if release.release_id in releases:
                previous = releases[release.release_id].manifest_path
                raise CorpusRegistryError(
                    f"duplicate release ID {release.release_id!r}: "
                    f"{previous} and {release.manifest_path}"
                )
            releases[release.release_id] = release
    return releases


def default_release_id() -> str:
    pointer = _read_json(CURRENT_RELEASE_PATH)
    release_id = pointer.get("release_id")
    if not isinstance(release_id, str) or not release_id.strip():
        raise CorpusRegistryError(
            f"{CURRENT_RELEASE_PATH} must contain a non-empty release_id"
        )
    return release_id


def selected_release_id(
    explicit: str | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Select explicit > environment > committed default release ID."""

    if explicit:
        return explicit
    environment = os.environ if environ is None else environ
    configured = environment.get(DEFAULT_RELEASE_ENV, "").strip()
    return configured or default_release_id()


def get_release(
    release_id: str | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> CorpusRelease:
    """Resolve the selected release or raise with the available IDs."""

    selected = selected_release_id(release_id, environ=environ)
    releases = available_releases(environ=environ)
    try:
        return releases[selected]
    except KeyError as exc:
        known = ", ".join(sorted(releases)) or "(none)"
        raise CorpusRegistryError(
            f"unknown corpus release {selected!r}; available: {known}"
        ) from exc
