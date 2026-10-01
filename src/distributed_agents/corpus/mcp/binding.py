"""Validated binding to one installed corpus release."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .errors import CorpusToolError


@dataclass(frozen=True)
class ReleaseBinding:
    manifest_path: Path
    root: Path
    payload: Mapping[str, Any]

    @classmethod
    def load(cls, manifest_path: Path) -> "ReleaseBinding":
        manifest = manifest_path.expanduser().resolve()
        if not manifest.is_file():
            raise CorpusToolError(f"release manifest is unavailable: {manifest}")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if payload.get("schema_version") != "distributed_agents-corpus-release-v1":
            raise CorpusToolError("unsupported corpus release manifest schema")
        return cls(manifest_path=manifest, root=manifest.parent, payload=payload)

    @property
    def release_id(self) -> str:
        return str(self.payload.get("release_id") or "")

    @property
    def corpus_family(self) -> str:
        return str(self.payload.get("corpus_family") or "")

    @property
    def artifact_names(self) -> frozenset[str]:
        artifacts = self.payload.get("artifacts")
        return frozenset(artifacts if isinstance(artifacts, Mapping) else ())

    def entrypoint(self, role: str, name: str) -> Path:
        try:
            skills = self.payload["capabilities"]["skills"]
            role_spec = skills["roles"][role]
            relative = Path(skills["path"]) / role_spec["skill"] / role_spec["entrypoints"][name]
        except (KeyError, TypeError) as exc:
            raise CorpusToolError(
                f"release {self.release_id!r} does not declare {role}.{name}"
            ) from exc
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root) or not path.is_file():
            raise CorpusToolError(f"declared release entrypoint is unavailable: {role}.{name}")
        return path

    def artifact(self, name: str) -> Path:
        try:
            relative = self.payload["artifacts"][name]["path"]
        except (KeyError, TypeError) as exc:
            raise CorpusToolError(
                f"release {self.release_id!r} does not declare artifact {name!r}"
            ) from exc
        path = (self.root / str(relative)).resolve()
        if not path.is_relative_to(self.root) or not path.is_file():
            raise CorpusToolError(f"declared release artifact is unavailable: {name}")
        return path

    def artifact_sha256(self, name: str) -> str:
        try:
            value = self.payload["artifacts"][name]["sha256"]
        except (KeyError, TypeError) as exc:
            raise CorpusToolError(
                f"release {self.release_id!r} does not declare artifact {name!r}"
            ) from exc
        return str(value)

