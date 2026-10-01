"""Load caller-owned tasks and render framework-specific run directories."""

from __future__ import annotations

import json
import os
import re
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .models import FrameworkPrompt, PromptRun
from .runtime.paths import DEFAULT_RUNS_ROOT
from .runtime.policy import SourcePolicy, source_policy_from_dict

DEFAULT_FRAMEWORKS = ("distributed_agents",)
PROMPT_FRAMEWORKS = ("distributed_agents", "codex", "claude-code", "biomni")
DEFAULT_RESULTS_ROOT = DEFAULT_RUNS_ROOT
DEFAULT_OUTPUT_FILENAMES = ("trace.md", "answer.txt")
_ABS_PATH_RE = re.compile(r"/[^\s)\]'\"<>]+")


def utc_run_id() -> str:
    """Return a sortable UTC timestamp suitable for run directories."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def resolve_prompt_file(prompt_file: Path) -> Path:
    """Resolve an explicit prompt path and fail clearly when it is absent."""
    path = prompt_file.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"prompt file does not exist: {path}")
    return path


def find_named_output_paths(
    prompt_text: str,
    *,
    output_filenames: Iterable[str] = DEFAULT_OUTPUT_FILENAMES,
) -> tuple[Path, ...]:
    """Find absolute output paths in a prompt by final filename."""
    names = set(output_filenames)
    paths: list[Path] = []
    for match in _ABS_PATH_RE.finditer(prompt_text):
        raw = match.group(0).rstrip(".,;:")
        path = Path(raw)
        if path.name in names:
            paths.append(path)
    return tuple(dict.fromkeys(paths))


def infer_output_dir(
    prompt_text: str,
    *,
    output_filenames: Iterable[str] = DEFAULT_OUTPUT_FILENAMES,
) -> Path | None:
    """Infer the old deliverable directory from named absolute output paths."""
    paths = find_named_output_paths(prompt_text, output_filenames=output_filenames)
    if not paths:
        return None
    parents = {path.parent for path in paths}
    if len(parents) == 1:
        return next(iter(parents))
    common = os.path.commonpath([str(parent) for parent in parents])
    return Path(common) if common else None


def render_prompt_for_run(
    prompt_text: str,
    *,
    framework_run_dir: Path,
    old_output_dir: Path | None = None,
    output_filenames: Iterable[str] = DEFAULT_OUTPUT_FILENAMES,
) -> tuple[str, Path | None]:
    """Render a prompt for a framework-specific output directory.

    If ``old_output_dir`` is not provided, the function infers it from absolute
    paths ending in the configured output filenames, then replaces that prefix
    with ``framework_run_dir``.
    """
    source_dir = old_output_dir or infer_output_dir(
        prompt_text,
        output_filenames=output_filenames,
    )
    if source_dir is None:
        return prompt_text, None
    return prompt_text.replace(str(source_dir), str(framework_run_dir)), source_dir


def prepare_prompt_run(
    *,
    prompt_file: Path,
    frameworks: Iterable[str] = DEFAULT_FRAMEWORKS,
    results_root: Path = DEFAULT_RESULTS_ROOT,
    question_id: str | None = None,
    run_id: str | None = None,
    old_output_dir: Path | None = None,
    output_filenames: Iterable[str] = DEFAULT_OUTPUT_FILENAMES,
) -> PromptRun:
    """Create run directories, rendered prompts, and run metadata."""
    prompt_file = resolve_prompt_file(prompt_file)
    qid = question_id or prompt_file.stem
    rid = run_id or utc_run_id()
    eval_root = (results_root / qid / rid).resolve()
    created_at = datetime.now(timezone.utc).isoformat()

    raw_prompt = prompt_file.read_text()
    inferred_old_output_dir = old_output_dir or infer_output_dir(
        raw_prompt,
        output_filenames=output_filenames,
    )

    framework_prompts: list[FrameworkPrompt] = []
    for framework in frameworks:
        # Group by framework first: <task>/<framework>/<batch>/<rNN>/ (rid carries
        # "<batch>/<rNN>"). eval_root (<task>/<batch>/<rNN>) is the cross-framework
        # metadata home.
        run_dir = (results_root / qid / framework / rid).resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
        rendered, _ = render_prompt_for_run(
            raw_prompt,
            framework_run_dir=run_dir,
            old_output_dir=inferred_old_output_dir,
            output_filenames=output_filenames,
        )
        prompt_path = run_dir / "prompt.md"
        prompt_path.write_text(rendered)
        expected_outputs = find_named_output_paths(
            rendered,
            output_filenames=output_filenames,
        )
        framework_prompts.append(
            FrameworkPrompt(
                framework=framework,
                run_dir=run_dir,
                prompt_path=prompt_path,
                expected_outputs=expected_outputs,
            )
        )

    run = PromptRun(
        prompt_file=prompt_file,
        question_id=qid,
        run_id=rid,
        eval_root=eval_root,
        old_output_dir=inferred_old_output_dir,
        frameworks=tuple(framework_prompts),
        created_at=created_at,
    )
    write_run_metadata(run)
    return run


@dataclass(frozen=True)
class TaskSpec:
    """A declarative eval task: prompt template + declared inputs + deliverables.

    The ``inputs`` values double as the sandbox read-only mount allowlist, and
    ``deliverables`` are fixed RELATIVE filenames the harness collects from each
    run dir -- so nothing about I/O location lives in the prompt prose and no
    absolute-path rewrite is needed.
    """

    task_id: str
    prompt_template: Path
    inputs: dict[str, Path]
    deliverables: tuple[str, ...]
    spec_path: Path
    source_policy: SourcePolicy | None = None


def load_task_spec(path: Path) -> TaskSpec:
    """Load a task spec TOML. Relative prompt/input paths resolve against the
    spec file's directory, so specs are portable and CWD-independent."""
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"task file does not exist: {path}")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    base = path.parent

    def _rel(value: str) -> Path:
        expanded = os.path.expandvars(os.path.expanduser(value))
        if "${" in expanded:
            raise ValueError(
                f"task path references an unset environment variable: {value}"
            )
        p = Path(expanded)
        return p if p.is_absolute() else (base / p)

    task_id = str(data.get("task_id") or "").strip()
    if not task_id or Path(task_id).name != task_id:
        raise ValueError("task_id must be a non-empty path-safe name")
    if not data.get("prompt"):
        raise ValueError("task must declare prompt")
    prompt_template = _rel(data["prompt"])
    if not prompt_template.is_file():
        raise FileNotFoundError(f"task prompt does not exist: {prompt_template}")

    inputs = {k: _rel(v) for k, v in (data.get("inputs") or {}).items()}
    missing_inputs = [str(value) for value in inputs.values() if not value.exists()]
    if missing_inputs:
        raise FileNotFoundError(
            "task inputs do not exist: " + ", ".join(missing_inputs)
        )
    deliverables = tuple((data.get("deliverables") or {}).get("files", ()))
    invalid_outputs = [
        name
        for name in deliverables
        if Path(name).is_absolute() or ".." in Path(name).parts
    ]
    if invalid_outputs:
        raise ValueError(
            "deliverables must be relative paths inside the run directory: "
            + ", ".join(invalid_outputs)
        )
    source_policy = source_policy_from_dict(data.get("source_policy"))
    return TaskSpec(
        task_id=task_id,
        prompt_template=prompt_template,
        inputs=inputs,
        deliverables=deliverables,
        spec_path=path,
        source_policy=source_policy,
    )


def render_task_prompt(spec: TaskSpec) -> str:
    """Substitute ``{{input_key}}`` placeholders with the declared input paths.

    No output paths are ever substituted: deliverables are fixed relative names
    the agent writes to its working dir (the run dir)."""
    text = spec.prompt_template.read_text()
    for key, val in spec.inputs.items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def prepare_task_run(
    spec: TaskSpec,
    *,
    frameworks: Iterable[str] = DEFAULT_FRAMEWORKS,
    results_root: Path = DEFAULT_RESULTS_ROOT,
    run_id: str | None = None,
) -> PromptRun:
    """Create run dirs + rendered prompts for a declarative task spec.

    Unlike :func:`prepare_prompt_run`, there is no absolute-path inference or
    rewrite: the rendered prompt is identical across frameworks, expected outputs
    are ``run_dir/<deliverable>``, and the declared inputs are recorded for the
    sandbox allowlist.
    """
    rid = run_id or utc_run_id()
    eval_root = (results_root / spec.task_id / rid).resolve()
    created_at = datetime.now(timezone.utc).isoformat()
    rendered = render_task_prompt(spec)

    framework_prompts: list[FrameworkPrompt] = []
    for framework in frameworks:
        # Group by framework first: <task>/<framework>/<batch>/<rNN>/ (rid carries
        # "<batch>/<rNN>"). eval_root (<task>/<batch>/<rNN>) is the metadata home.
        run_dir = (results_root / spec.task_id / framework / rid).resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = run_dir / "prompt.md"
        prompt_path.write_text(rendered)
        expected_outputs = tuple(run_dir / name for name in spec.deliverables)
        framework_prompts.append(
            FrameworkPrompt(
                framework=framework,
                run_dir=run_dir,
                prompt_path=prompt_path,
                expected_outputs=expected_outputs,
            )
        )

    run = PromptRun(
        prompt_file=spec.prompt_template,
        question_id=spec.task_id,
        run_id=rid,
        eval_root=eval_root,
        old_output_dir=None,
        frameworks=tuple(framework_prompts),
        created_at=created_at,
        declared_inputs=tuple(spec.inputs.values()),
        source_policy=spec.source_policy,
    )
    write_run_metadata(run)
    return run


def prompt_run_to_dict(run: PromptRun) -> dict:
    """Return a JSON-serialisable representation of a prompt run."""
    return {
        "prompt_file": str(run.prompt_file),
        "question_id": run.question_id,
        "run_id": run.run_id,
        "eval_root": str(run.eval_root),
        "old_output_dir": str(run.old_output_dir) if run.old_output_dir else None,
        "created_at": run.created_at,
        "declared_inputs": [str(p) for p in run.declared_inputs],
        "source_policy": (
            run.source_policy.public_metadata() if run.source_policy else None
        ),
        "frameworks": [
            {
                "framework": fw.framework,
                "run_dir": str(fw.run_dir),
                "prompt_path": str(fw.prompt_path),
                "expected_outputs": [str(path) for path in fw.expected_outputs],
            }
            for fw in run.frameworks
        ],
    }


def write_run_metadata(run: PromptRun) -> Path:
    """Write the run manifest into each framework run_dir (self-contained), so
    ``<task>/<framework>/<batch>/<rNN>/`` holds its own run_metadata.json and no
    separate cross-framework metadata dir is created. Returns the first path
    (or the logical eval_root when there are no frameworks)."""
    data = json.dumps(prompt_run_to_dict(run), indent=2) + "\n"
    first: Path | None = None
    for fw in run.frameworks:
        path = fw.run_dir / "run_metadata.json"
        path.write_text(data)
        first = first or path
    return first or (run.eval_root / "run_metadata.json")
