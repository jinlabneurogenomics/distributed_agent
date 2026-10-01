"""Persistent terminal chat over the sandboxed adaptive DistributedAgents runtime."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from ..corpus.registry import CorpusRelease, get_release
from ..query import CodexQueryOptions, QueryRequest, QueryResult
from ..query.access import (
    _codex_input_roots,
    _codex_passthrough_env,
)
from ..query.runner import run_query_job
from ..runtime.events import codex_thread_id
from ..runtime import sandbox
from ..runtime.paths import PACKAGE_ROOT
from ..skills.registry import resolve_skills
from .models import ChatStateError, ChatTurn

CHAT_SCHEMA_VERSION = "distributed_agents-chat-v1"
_HARNESS_PATHS = (
    "task.md",
    "query.md",
    "events.jsonl",
    "last_message.txt",
    "runner.log",
    "run.json",
    "codex_runtime",
)
_TRACE_PATHS = _HARNESS_PATHS + ("report.md", "tool_calls.jsonl")


def _protected_runtime_paths(working_directory: Path) -> tuple[Path, ...]:
    """Return source, control, and credential paths excluded from chat mounts."""

    candidates = (
        Path.home() / ".codex",
        Path.home() / ".ssh",
        PACKAGE_ROOT / "AGENTS.md",
        PACKAGE_ROOT / "README.md",
        PACKAGE_ROOT / "build",
        PACKAGE_ROOT / "chat",
        PACKAGE_ROOT / "cli",
        PACKAGE_ROOT / "query",
        working_directory / "AGENTS.md",
        working_directory / "TODO.md",
        working_directory / ".agent",
        working_directory / ".git",
        working_directory / "tests",
        working_directory / "src" / "bioeval",
    )
    return tuple(dict.fromkeys(path.expanduser().resolve() for path in candidates))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _read_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ChatStateError(f"cannot read chat state {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ChatStateError(f"chat state is not an object: {path}")
    return payload


def _contains(container: Path, candidate: Path) -> bool:
    return candidate == container or candidate.is_relative_to(container)


def validate_chat_input_roots(
    roots: Iterable[Path],
    *,
    chat_root: Path,
    protected_paths: tuple[Path, ...],
) -> tuple[Path, ...]:
    """Resolve explicit roots without permitting a broad repository/state mount."""

    resolved: list[Path] = []
    seen: set[str] = set()
    root = chat_root.expanduser().resolve()
    for raw in roots:
        path = raw.expanduser().resolve()
        if not path.exists():
            raise ValueError(f"chat input root does not exist: {path}")
        if _contains(path, root):
            raise ValueError(
                f"chat input root would expose chat sessions and traces: {path}"
            )
        exposed = [item for item in protected_paths if _contains(path, item)]
        if exposed:
            raise ValueError(
                "chat input root is broader than the protected runtime allows: "
                f"{path} exposes {exposed[0]}"
            )
        marker = str(path)
        if marker not in seen:
            seen.add(marker)
            resolved.append(path)
    return tuple(resolved)


def effective_chat_input_roots(
    declared_roots: tuple[Path, ...],
    *,
    workspace: Path,
    skills_destination: str = "",
    skills_index_container_path: str = "",
    corpus_release: CorpusRelease | None = None,
    protected_paths: tuple[Path, ...] = (),
) -> tuple[Path, ...]:
    """Resolve the exact mounts that the default query role will receive."""

    _, _, skill_dirs = resolve_skills(
        skills_destination,
        skills_index_container_path,
        include_project=True,
        corpus_release=corpus_release,
    )
    runtime_env = _codex_passthrough_env(workspace)
    roots = _codex_input_roots(
        skill_dirs,
        runtime_env,
        task_input_roots=declared_roots,
        include_packaged_skills=not bool(skills_destination),
        corpus_release=corpus_release,
    )
    for root in roots:
        exposed = [item for item in protected_paths if _contains(root, item)]
        if exposed:
            raise ValueError(
                "effective chat mount exposes a forbidden repository surface: "
                f"{root} exposes {exposed[0]}"
            )
    return roots


def run_chat_sandbox_canary(
    *,
    chat_root: Path,
    input_roots: tuple[Path, ...],
    skills_destination: str = "",
    skills_index_container_path: str = "",
    corpus_release: CorpusRelease | None = None,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, object]:
    """Execute a no-model read/write canary in the same allowlist namespace."""

    canary_dir = chat_root / "sandbox-canary"
    canary_dir.mkdir(parents=True, exist_ok=True)
    effective_roots = effective_chat_input_roots(
        input_roots,
        workspace=canary_dir,
        skills_destination=skills_destination,
        skills_index_container_path=skills_index_container_path,
        corpus_release=corpus_release,
        protected_paths=protected_paths,
    )
    script = """
import json
import pathlib
import sys

workspace = pathlib.Path(sys.argv[1])
allowed = json.loads(sys.argv[2])
forbidden = json.loads(sys.argv[3])
marker = workspace / "write-check.txt"
marker.write_text("ok")
result = {
    "workspace_write": marker.read_text() == "ok",
    "allowed": {path: pathlib.Path(path).exists() for path in allowed},
    "forbidden": {path: pathlib.Path(path).exists() for path in forbidden},
}
print(json.dumps(result, sort_keys=True))
if not result["workspace_write"] or not all(result["allowed"].values()):
    raise SystemExit(2)
if any(result["forbidden"].values()):
    raise SystemExit(3)
""".strip()
    inner = [
        "/usr/bin/python3",
        "-c",
        script,
        str(canary_dir),
        json.dumps([str(path) for path in effective_roots]),
        json.dumps([str(path) for path in protected_paths]),
    ]
    command = sandbox.bwrap_allowlist_command(
        inner,
        chdir=str(canary_dir),
        allow_ro=effective_roots,
        allow_rw=(canary_dir,),
        # The canary verifies filesystem visibility only. Sharing the host
        # network avoids requiring a disposable network namespace and matches
        # ordinary (non-protected) chat startup; protected turns still apply
        # the BioEval gateway boundary in ``codex_run_command``.
        share_net=True,
    )
    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=sandbox.clean_env(),
    )
    try:
        observed = json.loads(process.stdout.strip())
    except json.JSONDecodeError:
        observed = {}
    report: dict[str, object] = {
        "schema_version": CHAT_SCHEMA_VERSION,
        "checked_at": _utc_now(),
        "status": "passed" if process.returncode == 0 else "failed",
        "returncode": process.returncode,
        "effective_input_roots": [str(path) for path in effective_roots],
        "observed": observed,
        "stderr": process.stderr.strip(),
    }
    _write_json(canary_dir / "canary.json", report)
    if process.returncode:
        raise ChatStateError(
            f"DistributedAgents chat sandbox canary failed; see {canary_dir / 'canary.json'}"
        )
    return report


class SandboxedChat:
    """Manage isolated Codex sessions and per-turn trace archives."""

    def __init__(
        self,
        out_dir: Path,
        *,
        model: str | None = None,
        mode: str = "adaptive",
        corpus_release: str | None = None,
        skills_destination: str = "",
        skills_index_container_path: str = "",
        codex_options: CodexQueryOptions | None = None,
        verify_sandbox: bool = True,
        query_runner: Callable[[QueryRequest], QueryResult] | None = None,
        working_directory: Path | None = None,
    ) -> None:
        self.root = out_dir.expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.model = model
        self.mode = mode
        self.corpus_release = get_release(corpus_release)
        self.skills_destination = skills_destination
        self.skills_index_container_path = skills_index_container_path
        self.working_directory = (
            working_directory.expanduser().resolve()
            if working_directory is not None
            else Path.cwd().resolve()
        )
        self.protected_paths = _protected_runtime_paths(self.working_directory)
        if mode not in {"adaptive", "direct"}:
            raise ValueError("DistributedAgents chat supports only adaptive or direct mode")
        base = codex_options or CodexQueryOptions(input_roots=())
        if not base.bwrap:
            raise ValueError("DistributedAgents chat requires the external allowlist sandbox")
        if base.sandbox != "workspace-write":
            raise ValueError(
                "DistributedAgents chat requires the workspace-write Codex sandbox"
            )
        declared = validate_chat_input_roots(
            base.input_roots or (),
            chat_root=self.root,
            protected_paths=self.protected_paths,
        )
        self.codex_options = replace(
            base,
            input_roots=declared,
            session_home=None,
            resume_session_id=None,
        )
        self.effective_input_roots = effective_chat_input_roots(
            declared,
            workspace=self.root / "sandbox-canary",
            skills_destination=self.skills_destination,
            skills_index_container_path=self.skills_index_container_path,
            corpus_release=self.corpus_release,
            protected_paths=self.protected_paths,
        )
        self._query_runner = query_runner or run_query_job
        self.state_path = self.root / "chat.json"
        expected = self._config_payload()
        if self.state_path.exists():
            state = _read_json(self.state_path)
            if state.get("schema_version") != CHAT_SCHEMA_VERSION:
                raise ChatStateError(
                    f"unsupported chat state schema in {self.state_path}"
                )
            if state.get("config") != expected:
                raise ChatStateError(
                    "existing chat configuration differs from this invocation; "
                    "use another --out-dir or the original options"
                )
            self._state = state
        else:
            self._state = {
                "schema_version": CHAT_SCHEMA_VERSION,
                "created_at": _utc_now(),
                "updated_at": _utc_now(),
                "config": expected,
                "active_session": None,
                "next_session": 1,
            }
            self._save_state()
        if verify_sandbox:
            run_chat_sandbox_canary(
                chat_root=self.root,
                input_roots=declared,
                skills_destination=self.skills_destination,
                skills_index_container_path=self.skills_index_container_path,
                corpus_release=self.corpus_release,
                protected_paths=self.protected_paths,
            )
        if self._state.get("active_session") is None:
            self.new_session()

    def _config_payload(self) -> dict[str, object]:
        options = self.codex_options
        return {
            "mode": self.mode,
            "model": self.model,
            "corpus_release": self.corpus_release.release_id,
            "skills_destination": self.skills_destination,
            "skills_index_container_path": self.skills_index_container_path,
            "auth": options.auth,
            "sandbox": options.sandbox,
            "bwrap": options.bwrap,
            "reasoning_effort": options.reasoning_effort,
            "timeout_seconds": options.timeout_seconds,
            "max_concurrent_subagents": options.max_concurrent_subagents,
            "max_subagents": options.max_subagents,
            "input_roots": [str(path) for path in options.input_roots or ()],
            "effective_input_roots": [str(path) for path in self.effective_input_roots],
            "working_directory": str(self.working_directory),
            "config_overrides": list(options.config_overrides),
        }

    def _save_state(self) -> None:
        self._state["updated_at"] = _utc_now()
        _write_json(self.state_path, self._state)

    @property
    def active_session_id(self) -> str:
        value = self._state.get("active_session")
        if not isinstance(value, str) or not value:
            raise ChatStateError("chat has no active session")
        return value

    def _session_dir(self, session_id: str) -> Path:
        if not session_id.startswith("session-") or not session_id[8:].isdigit():
            raise ChatStateError(f"invalid session id: {session_id}")
        return self.root / "sessions" / session_id

    def _session_state(self, session_id: str) -> dict[str, object]:
        return _read_json(self._session_dir(session_id) / "session.json")

    def new_session(self, *, activate: bool = True, kind: str = "chat") -> str:
        number = int(self._state.get("next_session", 1))
        session_id = f"session-{number:04d}"
        session_dir = self._session_dir(session_id)
        (session_dir / "workspace").mkdir(parents=True, exist_ok=False)
        (session_dir / "codex-home").mkdir()
        (session_dir / "turns").mkdir()
        _write_json(
            session_dir / "session.json",
            {
                "schema_version": CHAT_SCHEMA_VERSION,
                "session_id": session_id,
                "kind": kind,
                "created_at": _utc_now(),
                "updated_at": _utc_now(),
                "thread_id": None,
                "next_turn": 1,
            },
        )
        self._state["next_session"] = number + 1
        if activate:
            self._state["active_session"] = session_id
        self._save_state()
        return session_id

    def use_session(self, session_id: str) -> None:
        self._session_state(session_id)
        self._state["active_session"] = session_id
        self._save_state()

    def list_sessions(self) -> list[dict[str, object]]:
        sessions_dir = self.root / "sessions"
        rows: list[dict[str, object]] = []
        for path in sorted(sessions_dir.glob("session-*")):
            state_path = path / "session.json"
            if state_path.is_file():
                rows.append(_read_json(state_path))
        return rows

    def _clear_turn_harness(self, workspace: Path) -> None:
        for name in _HARNESS_PATHS:
            path = workspace / name
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()

    def _archive_turn(
        self,
        *,
        session_id: str,
        turn_number: int,
        question: str,
        status: str,
        thread_id: str | None,
        result: QueryResult | None,
        error: str | None,
    ) -> Path:
        session_dir = self._session_dir(session_id)
        workspace = session_dir / "workspace"
        turn_dir = session_dir / "turns" / f"{turn_number:04d}"
        turn_dir.mkdir(parents=True, exist_ok=False)
        for name in _TRACE_PATHS:
            source = workspace / name
            destination = turn_dir / name
            if source.is_dir():
                shutil.copytree(source, destination)
            elif source.is_file():
                shutil.copy2(source, destination)
        manifest: dict[str, object] = {
            "schema_version": CHAT_SCHEMA_VERSION,
            "session_id": session_id,
            "turn_number": turn_number,
            "archived_at": _utc_now(),
            "status": status,
            "thread_id": thread_id,
            "question": question,
            "error": error,
            "trace_dir": str(turn_dir),
        }
        if result is not None:
            manifest.update(
                {
                    "model": result.model,
                    "duration_s": result.duration_s,
                    "usage": result.usage,
                    "warnings": list(result.warnings),
                }
            )
        run_manifest_path = workspace / "run.json"
        if run_manifest_path.is_file():
            try:
                run_manifest = json.loads(run_manifest_path.read_text())
                adaptive = run_manifest.get("adaptive_context") or {}
                preparation = adaptive.get("preparation") or {}
                ledger_calibration = preparation.get("ledger_calibration")
                if isinstance(ledger_calibration, dict):
                    manifest["ledger_calibration"] = ledger_calibration
            except (AttributeError, OSError, json.JSONDecodeError):
                # Archiving the trace remains more important than optional
                # provenance extraction from a partial failed-run manifest.
                pass
        _write_json(turn_dir / "turn.json", manifest)
        return turn_dir

    def ask(self, question: str, *, session_id: str | None = None) -> ChatTurn:
        question = question.strip()
        if not question:
            raise ValueError("chat question must not be empty")
        selected = session_id or self.active_session_id
        session_dir = self._session_dir(selected)
        session_state = self._session_state(selected)
        workspace = session_dir / "workspace"
        turn_number = int(session_state.get("next_turn", 1))
        prior_thread = session_state.get("thread_id")
        if prior_thread is not None and not isinstance(prior_thread, str):
            raise ChatStateError(f"invalid thread id in {session_dir / 'session.json'}")
        self._clear_turn_harness(workspace)
        options = replace(
            self.codex_options,
            session_home=session_dir / "codex-home",
            resume_session_id=prior_thread,
        )
        request = QueryRequest(
            query=question,
            model=self.model,
            skills_destination=self.skills_destination,
            skills_index_container_path=self.skills_index_container_path,
            out_dir=workspace,
            working_directory=self.working_directory,
            codex=options,
            mode=self.mode,
            corpus_release=self.corpus_release.release_id,
        )
        result: QueryResult | None = None
        error: str | None = None
        try:
            result = self._query_runner(request)
            current_thread = result.thread_id or prior_thread
            if not current_thread:
                raise ChatStateError("Codex completed without recording a thread id")
            status = result.status
        except Exception as exc:
            error = str(exc)
            current_thread = codex_thread_id(workspace / "events.jsonl") or prior_thread
            status = "failed"
            trace_dir = self._archive_turn(
                session_id=selected,
                turn_number=turn_number,
                question=question,
                status=status,
                thread_id=current_thread,
                result=result,
                error=error,
            )
            session_state["thread_id"] = current_thread
            session_state["next_turn"] = turn_number + 1
            session_state["updated_at"] = _utc_now()
            session_state["last_trace_dir"] = str(trace_dir)
            _write_json(session_dir / "session.json", session_state)
            raise
        trace_dir = self._archive_turn(
            session_id=selected,
            turn_number=turn_number,
            question=question,
            status=status,
            thread_id=current_thread,
            result=result,
            error=None,
        )
        session_state["thread_id"] = current_thread
        session_state["next_turn"] = turn_number + 1
        session_state["updated_at"] = _utc_now()
        session_state["last_trace_dir"] = str(trace_dir)
        _write_json(session_dir / "session.json", session_state)
        return ChatTurn(
            answer=result.answer,
            session_id=selected,
            turn_number=turn_number,
            thread_id=current_thread,
            trace_dir=trace_dir,
            result=result,
        )

    def cold_ask(self, question: str) -> ChatTurn:
        session_id = self.new_session(activate=False, kind="cold")
        return self.ask(question, session_id=session_id)

    def trace_summary(self) -> dict[str, object]:
        session_id = self.active_session_id
        session_dir = self._session_dir(session_id)
        state = self._session_state(session_id)
        return {
            "chat_root": str(self.root),
            "active_session": session_id,
            "thread_id": state.get("thread_id"),
            "completed_turns": int(state.get("next_turn", 1)) - 1,
            "workspace": str(session_dir / "workspace"),
            "last_trace_dir": state.get("last_trace_dir"),
            "declared_input_roots": [
                str(path) for path in self.codex_options.input_roots or ()
            ],
            "effective_input_roots": [str(path) for path in self.effective_input_roots],
            "sandbox_canary": str(self.root / "sandbox-canary" / "canary.json"),
        }
