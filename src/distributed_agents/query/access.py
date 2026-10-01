"""Release-aware task and framework access planning for queries."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ..corpus.registry import (
    DEFAULT_RELEASE_ENV,
    RELEASE_ROOTS_ENV,
    CorpusRelease,
    get_release,
)
from ..runtime import sandbox
from ..skills.registry import (
    DATASET_SKILLS_DIR,
    LIFE_SCIENCES_SKILLS_DIR,
    PACKAGE_SKILLS_DIR,
    RUNTIME_SKILLS_DIR,
)
from .context import sha256_path
from .errors import CodexQueryError


CORPUS_MCP_SERVER_PATH = Path(__file__).resolve().parents[1] / "corpus" / "mcp_server.py"
CORPUS_MCP_PACKAGE_PATH = CORPUS_MCP_SERVER_PATH.parent / "mcp"
CORPUS_MCP_PYTHON = Path("/usr/bin/python3")

_PATH_ENV_KEYS = {
    "DISTRIBUTED_AGENTS_FINDINGS_LEDGER",
    "DISTRIBUTED_AGENTS_GENE_STORE",
    "BIOKG_REPORTS_PATH",
}
_PASSTHROUGH_ENV_KEYS = {
    *_PATH_ENV_KEYS,
    DEFAULT_RELEASE_ENV,
    RELEASE_ROOTS_ENV,
    "BIOKG_NEO4J_HTTP_URL",
    "BIOKG_NEO4J_DATABASE",
    "BIOKG_NEO4J_URI",
    "BIOKG_NEO4J_USER",
    "BIOKG_NEO4J_PASSWORD",
}


@dataclass(frozen=True)
class RuntimeAccessPlan:
    """The exact task and framework roots exposed to one Codex invocation."""

    release: CorpusRelease
    task_input_roots: tuple[Path, ...]
    framework_roots: tuple[Path, ...]
    effective_roots: tuple[Path, ...]
    artifact_overrides: dict[str, Path]

    def as_dict(self) -> dict[str, object]:
        return {
            "release_id": self.release.release_id,
            "release_manifest": str(self.release.manifest_path),
            "release_manifest_sha256": sha256_path(self.release.manifest_path),
            "task_input_roots": [str(path) for path in self.task_input_roots],
            "framework_roots": [str(path) for path in self.framework_roots],
            "effective_roots": [str(path) for path in self.effective_roots],
            "artifact_overrides": {
                name: str(path)
                for name, path in sorted(self.artifact_overrides.items())
            },
        }


def _codex_passthrough_env(run_dir: Path) -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if value and (key in _PASSTHROUGH_ENV_KEYS or key.startswith("BIOKG_NEO4J_"))
    }
    env["DISTRIBUTED_AGENTS_OUTPUT_DIR"] = str(run_dir)
    return env


def _codex_input_roots(
    skill_dirs: list[Path],
    runtime_env: dict[str, str],
    *,
    task_input_roots: tuple[Path, ...] | None = None,
    include_packaged_skills: bool = True,
    corpus_release: CorpusRelease | None = None,
) -> tuple[Path, ...]:
    """Backward-compatible projection of the effective runtime access plan."""

    return _codex_runtime_access_plan(
        skill_dirs,
        runtime_env,
        task_input_roots=task_input_roots,
        include_packaged_skills=include_packaged_skills,
        corpus_release=corpus_release,
    ).effective_roots


def _existing_roots(candidates: list[Path]) -> tuple[Path, ...]:
    roots: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        absolute = path.expanduser().absolute()
        marker = str(absolute)
        if marker in seen or not absolute.exists():
            continue
        seen.add(marker)
        roots.append(absolute)
    return tuple(roots)


def _codex_runtime_access_plan(
    skill_dirs: list[Path],
    runtime_env: dict[str, str],
    *,
    task_input_roots: tuple[Path, ...] | None = None,
    include_packaged_skills: bool = True,
    corpus_release: CorpusRelease | None = None,
) -> RuntimeAccessPlan:
    """Build one release-aware plan while keeping task and framework roots distinct."""

    release = corpus_release or get_release()
    task_roots = _existing_roots(list(task_input_roots or ()))
    artifact_overrides = {
        artifact: Path(runtime_env[env_key]).expanduser().absolute()
        for artifact, env_key in (
            ("reports", "BIOKG_REPORTS_PATH"),
            ("findings", "DISTRIBUTED_AGENTS_FINDINGS_LEDGER"),
        )
        if runtime_env.get(env_key)
    }
    packaged_skill_roots = (
        (
            PACKAGE_SKILLS_DIR,
            LIFE_SCIENCES_SKILLS_DIR,
            RUNTIME_SKILLS_DIR,
            DATASET_SKILLS_DIR,
        )
        if include_packaged_skills
        else ()
    )
    framework_candidates = [
        *release.runtime_roots(artifact_overrides=artifact_overrides),
        *packaged_skill_roots,
        CORPUS_MCP_SERVER_PATH,
        CORPUS_MCP_PACKAGE_PATH,
        *skill_dirs,
    ]
    for key in ("DISTRIBUTED_AGENTS_GENE_STORE",):
        value = runtime_env.get(key)
        if value:
            framework_candidates.append(Path(value))
    framework_roots = _existing_roots(framework_candidates)
    effective_roots = _existing_roots([*task_roots, *framework_roots])
    return RuntimeAccessPlan(
        release=release,
        task_input_roots=task_roots,
        framework_roots=framework_roots,
        effective_roots=effective_roots,
        artifact_overrides=artifact_overrides,
    )


def _preflight_release_runtime(
    access_plan: RuntimeAccessPlan,
    *,
    pipeline_dir: Path,
    runtime_env: dict[str, str],
    bwrap: bool,
) -> dict[str, object]:
    """Execute every advertised release entrypoint in the effective filesystem."""

    output_path = pipeline_dir / "capability_preflight.json"
    python = Path(sys.executable).absolute()
    python_prefix = Path(sys.prefix).absolute()
    python_mounts = (
        [python_prefix]
        if not any(
            python.is_relative_to(Path(root))
            for root in sandbox.DEFAULT_OS_ROOTS
            if Path(root).exists()
        )
        else []
    )
    sandbox_path = f"{python.parent}:/usr/bin:/bin"
    results: list[dict[str, object]] = []
    for entrypoint in access_plan.release.runtime_entrypoints():
        inner = [str(python), str(entrypoint), "--help"]
        command = (
            sandbox.bwrap_allowlist_command(
                inner,
                chdir=str(pipeline_dir),
                allow_ro=[*python_mounts, *access_plan.effective_roots],
                allow_rw=[pipeline_dir],
                path=sandbox_path,
            )
            if bwrap
            else inner
        )
        env = (
            sandbox.clean_env(
                extra={**runtime_env, "PATH": sandbox_path},
            )
            if bwrap
            else {**os.environ, **runtime_env}
        )
        try:
            done = subprocess.run(
                command,
                cwd=pipeline_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            returncode = done.returncode
            stdout = done.stdout[-2000:]
            stderr = done.stderr[-2000:]
        except (OSError, subprocess.TimeoutExpired) as exc:
            returncode = 124 if isinstance(exc, subprocess.TimeoutExpired) else 127
            stdout = ""
            stderr = str(exc)
        results.append(
            {
                "entrypoint": str(entrypoint),
                "returncode": returncode,
                "status": "passed" if returncode == 0 else "failed",
                "stdout_tail": stdout,
                "stderr_tail": stderr,
            }
        )
    failed = [row for row in results if row["status"] == "failed"]
    report: dict[str, object] = {
        "schema_version": "distributed_agents-capability-preflight-v1",
        "release_id": access_plan.release.release_id,
        "isolation": "bwrap" if bwrap else "host",
        "status": "failed" if failed else "passed",
        "runtime_access": access_plan.as_dict(),
        "entrypoints": results,
    }
    output_path.write_text(json.dumps(report, indent=2) + "\n")
    if failed:
        names = ", ".join(Path(str(row["entrypoint"])).name for row in failed)
        raise CodexQueryError(
            f"selected release {access_plan.release.release_id!r} has unusable "
            f"runtime entrypoints ({names}); see {output_path}"
        )
    return report
