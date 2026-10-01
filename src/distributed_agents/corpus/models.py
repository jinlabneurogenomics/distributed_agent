"""Corpus release and integrity-report models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


class CorpusRegistryError(RuntimeError):
    """Raised when a release cannot be discovered or safely resolved."""


@dataclass(frozen=True)
class CorpusRelease:
    """One validated-on-load corpus release manifest and its package root."""

    release_id: str
    root: Path
    manifest_path: Path
    manifest: Mapping[str, Any]

    def resolve(self, relative_path: str) -> Path:
        """Resolve a manifest path while preventing absolute paths and escapes."""

        candidate = Path(relative_path)
        if candidate.is_absolute():
            raise CorpusRegistryError(
                f"release {self.release_id!r} contains an absolute path: {relative_path}"
            )
        resolved = (self.root / candidate).resolve()
        if not resolved.is_relative_to(self.root.resolve()):
            raise CorpusRegistryError(
                f"release {self.release_id!r} path escapes its capsule: {relative_path}"
            )
        return resolved

    def artifact(self, name: str) -> Path:
        try:
            spec = self.manifest["artifacts"][name]
        except KeyError as exc:
            known = ", ".join(sorted(self.manifest.get("artifacts", {})))
            raise CorpusRegistryError(
                f"release {self.release_id!r} has no artifact {name!r}; known: {known}"
            ) from exc
        return self.resolve(str(spec["path"]))

    @property
    def skills_root(self) -> Path:
        return self.resolve(str(self.manifest["capabilities"]["skills"]["path"]))

    @property
    def tooling_root(self) -> Path:
        """Return the release-owned executable tooling directory."""

        return self.resolve(str(self.manifest["capabilities"]["tooling"]["path"]))

    def tooling_entrypoint(self, name: str) -> Path:
        """Resolve a manifest-declared tooling entrypoint without allowing escapes."""

        declared = self.manifest["capabilities"]["tooling"]["entrypoints"]
        if name not in declared:
            known = ", ".join(sorted(str(value) for value in declared))
            raise CorpusRegistryError(
                f"release {self.release_id!r} has no tooling entrypoint {name!r}; "
                f"known: {known}"
            )
        candidate = Path(name)
        if candidate.is_absolute():
            raise CorpusRegistryError(
                f"release {self.release_id!r} tooling entrypoint is absolute: {name}"
            )
        resolved = (self.tooling_root / candidate).resolve()
        if not resolved.is_relative_to(self.tooling_root.resolve()):
            raise CorpusRegistryError(
                f"release {self.release_id!r} tooling entrypoint escapes its "
                f"tooling root: {name}"
            )
        return resolved

    def runtime_entrypoints(self) -> tuple[Path, ...]:
        """Return each unique release-declared executable entrypoint."""

        candidates = [
            self.tooling_entrypoint(str(name))
            for name in self.manifest["capabilities"]["tooling"]["entrypoints"]
        ]
        for role_spec in self.manifest["capabilities"]["skills"]["roles"].values():
            skill = str(role_spec["skill"])
            skill_root = (self.skills_root / skill).resolve()
            for relative in role_spec["entrypoints"].values():
                candidate = (skill_root / str(relative)).resolve()
                if not candidate.is_relative_to(skill_root):
                    raise CorpusRegistryError(
                        f"release {self.release_id!r} skill entrypoint escapes its "
                        f"skill: {relative}"
                    )
                candidates.append(candidate)
        return tuple(dict.fromkeys(candidates))

    def runtime_roots(
        self,
        *,
        artifact_overrides: Mapping[str, Path] | None = None,
    ) -> tuple[Path, ...]:
        """Return the manifest-derived read-only runtime capability closure.

        Artifacts replaced by a run-local policy overlay are omitted and the
        replacement is mounted instead. The capsule's build/source scratch is
        intentionally not part of this access plan.
        """

        overrides = artifact_overrides or {}
        candidates: list[Path] = [
            self.manifest_path,
            self.skills_root,
            self.tooling_root,
        ]
        for name, spec in self.manifest["artifacts"].items():
            candidates.append(
                Path(overrides[name]).expanduser().resolve()
                if name in overrides
                else self.resolve(str(spec["path"]))
            )
            if spec.get("schema"):
                candidates.append(self.resolve(str(spec["schema"])))
        candidates.extend(
            self.projection(name)
            for name in self.manifest["capabilities"].get("projections", {})
        )
        return tuple(dict.fromkeys(path.resolve() for path in candidates))

    def skill(self, role: str) -> Path:
        """Resolve the release-owned skill implementing one stable capability role."""

        try:
            name = self.manifest["capabilities"]["skills"]["roles"][role]["skill"]
        except KeyError as exc:
            known = ", ".join(
                sorted(self.manifest["capabilities"]["skills"].get("roles", {}))
            )
            raise CorpusRegistryError(
                f"release {self.release_id!r} has no skill role {role!r}; known: {known}"
            ) from exc
        candidate = Path(str(name))
        if candidate.is_absolute():
            raise CorpusRegistryError(
                f"release {self.release_id!r} skill path is absolute: {name}"
            )
        resolved = (self.skills_root / candidate).resolve()
        if not resolved.is_relative_to(self.skills_root.resolve()):
            raise CorpusRegistryError(
                f"release {self.release_id!r} skill path escapes its skills root: {name}"
            )
        return resolved

    def skill_entrypoint(self, role: str, name: str) -> Path:
        """Resolve one entrypoint relative to its release-owned skill directory."""

        try:
            relative = self.manifest["capabilities"]["skills"]["roles"][role][
                "entrypoints"
            ][name]
        except KeyError as exc:
            raise CorpusRegistryError(
                f"release {self.release_id!r} skill role {role!r} "
                f"has no entrypoint {name!r}"
            ) from exc
        candidate = Path(str(relative))
        if candidate.is_absolute():
            raise CorpusRegistryError(
                f"release {self.release_id!r} skill entrypoint is absolute: {relative}"
            )
        resolved = (self.skill(role) / candidate).resolve()
        if not resolved.is_relative_to(self.skill(role).resolve()):
            raise CorpusRegistryError(
                f"release {self.release_id!r} skill entrypoint escapes its skill: {relative}"
            )
        return resolved

    def projection(self, name: str) -> Path:
        try:
            relative = self.manifest["capabilities"]["projections"][name]["path"]
        except KeyError as exc:
            known = ", ".join(
                sorted(self.manifest["capabilities"].get("projections", {}))
            )
            raise CorpusRegistryError(
                f"release {self.release_id!r} has no projection {name!r}; known: {known}"
            ) from exc
        return self.resolve(str(relative))

    def as_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "root": str(self.root),
            "manifest_path": str(self.manifest_path),
            **dict(self.manifest),
        }


@dataclass
class DoctorReport:
    """Machine-readable result from a release integrity audit."""

    release_id: str
    checks: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "ok": self.ok,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
        }

