"""Register and execute the `bioeval run` command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..artifacts.results import write_summary
from ..frameworks.distributed_agents import (
    DISTRIBUTED_AGENTS_BACKENDS,
    DISTRIBUTED_AGENTS_QUERY_MODES,
    DEFAULT_DISTRIBUTED_AGENTS_BACKEND,
    DEFAULT_DISTRIBUTED_AGENTS_MODEL,
    DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE,
    distributed_agents_run_command,
    run_distributed_agents_prompt,
)
from ..frameworks.biomni import (
    DEFAULT_BIOMNI_DATA_PATH,
    DEFAULT_BIOMNI_ENV,
    DEFAULT_BIOMNI_MODEL,
    DEFAULT_BIOMNI_RUNNER,
    biomni_run_command,
    run_biomni_prompt,
)
from ..frameworks.claude import (
    CLAUDE_OUTPUT_FORMATS,
    CLAUDE_PERMISSION_MODES,
    DEFAULT_CLAUDE_FAIRNESS_SANDBOX,
    DEFAULT_CLAUDE_MAX_TURNS,
    DEFAULT_CLAUDE_MODEL,
    DEFAULT_CLAUDE_OUTPUT_FORMAT,
    DEFAULT_CLAUDE_PERMISSION_MODE,
    claude_run_command,
    run_claude_prompt,
)
from ..frameworks.codex import (
    CODEX_AUTHS,
    CODEX_SANDBOXES,
    DEFAULT_CODEX_AUTH,
    DEFAULT_CODEX_BWRAP,
    DEFAULT_CODEX_MODEL,
    DEFAULT_CODEX_SANDBOX,
    codex_run_command,
    run_codex_prompt,
)
from ..frameworks.common import DEFAULT_INPUT_ROOTS
from ..runtime import sandbox
from ..runtime.paths import DEFAULT_RUNS_ROOT
from .parsing import positive_int
from ..runtime.source_policy import (
    DEFAULT_FILTERED_SEARCH_IMAGE,
    filtered_codex_config,
)
from ..tasks import (
    DEFAULT_FRAMEWORKS,
    PROMPT_FRAMEWORKS,
    load_task_spec,
    prepare_prompt_run,
    prepare_task_run,
    utc_run_id,
)


def _input_roots(run) -> tuple[Path, ...]:
    return (
        tuple(run.declared_inputs)
        if run.declared_inputs
        else tuple(DEFAULT_INPUT_ROOTS)
    )


def _developer_instructions(args: argparse.Namespace) -> str | None:
    path = args.codex_developer_instructions_file
    return path.read_text(encoding="utf-8") if path is not None else None


def _run_ids(run_id: str | None, rerun: int) -> list[str]:
    base = run_id or utc_run_id()
    width = max(2, len(str(rerun)))
    return [f"{base}/r{index:0{width}d}" for index in range(1, rerun + 1)]


def _prepare(args: argparse.Namespace, *, run_id: str):
    if args.task is not None:
        return prepare_task_run(
            load_task_spec(args.task),
            frameworks=args.frameworks,
            results_root=args.results_root,
            run_id=run_id,
        )
    return prepare_prompt_run(
        prompt_file=args.prompt_file,
        frameworks=args.frameworks,
        results_root=args.results_root,
        question_id=args.name,
        run_id=run_id,
        old_output_dir=args.old_output_dir,
    )


def _validate_run_args(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> None:
    if (
        args.codex_developer_instructions_file is not None
        and not args.codex_developer_instructions_file.is_file()
    ):
        parser.error(
            "--codex-developer-instructions-file does not exist: "
            f"{args.codex_developer_instructions_file}"
        )
    if args.task is None:
        return

    policy = load_task_spec(args.task).source_policy
    if not policy or not policy.enabled:
        return
    if "distributed_agents" in args.frameworks and args.distributed_agents_backend != "codex":
        parser.error("protected tasks require --distributed_agents-backend codex")
    if "codex" in args.frameworks and not args.codex_bwrap:
        parser.error("protected tasks require --codex-bwrap")
    if "codex" in args.frameworks and args.codex_sandbox != "workspace-write":
        parser.error("protected tasks require --codex-sandbox workspace-write")
    if "biomni" in args.frameworks and not args.biomni_fairness_sandbox:
        parser.error("protected tasks require --biomni-fairness-sandbox")
    if "claude-code" in args.frameworks and not args.claude_fairness_sandbox:
        parser.error("protected tasks require --claude-fairness-sandbox")
    if "claude-code" in args.frameworks and args.claude_web != "off":
        parser.error("protected tasks require --claude-web off")


def _command_preview(args: argparse.Namespace, run, framework_prompt) -> list[str]:
    protected = bool(run.source_policy and run.source_policy.enabled)
    roots = _input_roots(run)
    if framework_prompt.framework == "distributed_agents":
        return distributed_agents_run_command(
            framework_prompt.prompt_path,
            framework_prompt.run_dir,
            model=args.distributed_agents_model,
            pixi_executable=args.pixi_executable,
            fairness_sandbox=args.distributed_agents_fairness_sandbox,
            input_roots=roots,
            backend=args.distributed_agents_backend,
            query_mode=args.distributed_agents_mode,
            corpus_release=args.corpus_release,
            network_isolated=protected,
            filtered_mcp_url=(
                f"http://127.0.0.1:{sandbox.LITERATURE_GATE_PORT}/mcp"
                if protected
                else None
            ),
        )
    if framework_prompt.framework == "biomni":
        return biomni_run_command(
            framework_prompt.prompt_path,
            framework_prompt.run_dir,
            model=args.biomni_model,
            data_path=args.biomni_data_path,
            biomni_repo=args.biomni_repo,
            biomni_env=args.biomni_env,
            mamba_executable=args.mamba_executable,
            runner_script=args.biomni_runner_script,
            fairness_sandbox=args.biomni_fairness_sandbox,
            input_roots=roots,
            network_isolated=protected,
            model_gate_host_dir=framework_prompt.run_dir if protected else None,
            literature_gate_host_dir=framework_prompt.run_dir if protected else None,
            tls_egress_gate_host_dir=framework_prompt.run_dir if protected else None,
        )
    if framework_prompt.framework == "codex":
        config_overrides = (
            filtered_codex_config("http://127.0.0.1:<runtime-port>/mcp")
            if protected and run.source_policy.literature_access
            else ()
        )
        instructions = _developer_instructions(args)
        if instructions is not None:
            config_overrides = (
                *config_overrides,
                "developer_instructions=" + json.dumps(instructions, ensure_ascii=True),
            )
        return codex_run_command(
            framework_prompt.run_dir,
            model=args.codex_model,
            sandbox=args.codex_sandbox,
            codex_executable=args.codex_executable,
            auth=args.codex_auth,
            bwrap=args.codex_bwrap,
            input_roots=roots,
            config_overrides=config_overrides,
            disable_features=("multi_agent",) if args.codex_single_agent else (),
            network_access=not protected,
            strict_config=protected,
        )
    if framework_prompt.framework == "claude-code":
        return claude_run_command(
            framework_prompt.run_dir,
            model=args.claude_model,
            permission_mode=args.claude_permission_mode,
            max_turns=args.claude_max_turns,
            output_format=args.claude_output_format,
            claude_executable=args.claude_executable,
            fairness_sandbox=args.claude_fairness_sandbox,
            input_roots=(*roots, *(args.claude_input_root or ())),
            web=args.claude_web,
            network_isolated=protected,
            model_gate_host_dir=framework_prompt.run_dir if protected else None,
            literature_gate_host_dir=framework_prompt.run_dir if protected else None,
            tls_egress_gate_host_dir=framework_prompt.run_dir if protected else None,
            literature_mcp_url=(
                f"http://127.0.0.1:{sandbox.LITERATURE_GATE_PORT}/mcp"
                if protected
                else None
            ),
        )
    raise ValueError(f"unsupported framework: {framework_prompt.framework}")


def _print_dry_run(args: argparse.Namespace, run) -> None:
    print(f"task: {run.question_id}")
    print(f"source: {run.prompt_file}")
    inputs = ", ".join(map(str, run.declared_inputs)) or "none declared"
    print(f"inputs: {inputs}")
    for framework_prompt in run.frameworks:
        print(f"\n[{framework_prompt.framework}]")
        print(f"prompt: {framework_prompt.prompt_path}")
        print(f"run directory: {framework_prompt.run_dir}")
        print("command: " + " ".join(_command_preview(args, run, framework_prompt)))
        outputs = framework_prompt.expected_outputs
        print(
            "expected outputs: " + (", ".join(map(str, outputs)) if outputs else "none")
        )


def _run_framework(args: argparse.Namespace, run, framework_prompt):
    roots = _input_roots(run)
    common = {
        "source_policy": run.source_policy,
        "filtered_search_image": args.filtered_search_image,
        "apptainer_executable": args.apptainer_executable,
        "track_cost": args.track_cost,
    }
    if framework_prompt.framework == "distributed_agents":
        return run_distributed_agents_prompt(
            framework_prompt,
            model=args.distributed_agents_model,
            fairness_sandbox=args.distributed_agents_fairness_sandbox,
            pixi_executable=args.pixi_executable,
            cwd=Path.cwd(),
            input_roots=roots,
            backend=args.distributed_agents_backend,
            query_mode=args.distributed_agents_mode,
            corpus_release=args.corpus_release,
            **common,
        )
    if framework_prompt.framework == "biomni":
        return run_biomni_prompt(
            framework_prompt,
            model=args.biomni_model,
            data_path=args.biomni_data_path,
            biomni_repo=args.biomni_repo,
            biomni_env=args.biomni_env,
            mamba_executable=args.mamba_executable,
            runner_script=args.biomni_runner_script,
            cwd=Path.cwd(),
            fairness_sandbox=args.biomni_fairness_sandbox,
            input_roots=roots,
            **common,
        )
    if framework_prompt.framework == "codex":
        return run_codex_prompt(
            framework_prompt,
            model=args.codex_model,
            sandbox=args.codex_sandbox,
            codex_executable=args.codex_executable,
            cwd=Path.cwd(),
            auth=args.codex_auth,
            bwrap=args.codex_bwrap,
            input_roots=roots,
            developer_instructions=_developer_instructions(args),
            disable_features=("multi_agent",) if args.codex_single_agent else (),
            **common,
        )
    if framework_prompt.framework == "claude-code":
        return run_claude_prompt(
            framework_prompt,
            model=args.claude_model,
            permission_mode=args.claude_permission_mode,
            max_turns=args.claude_max_turns,
            output_format=args.claude_output_format,
            claude_executable=args.claude_executable,
            fairness_sandbox=args.claude_fairness_sandbox,
            input_roots=(*roots, *(args.claude_input_root or ())),
            web=args.claude_web,
            cwd=Path.cwd(),
            **common,
        )
    raise ValueError(f"unsupported framework: {framework_prompt.framework}")


def _run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    _validate_run_args(args, parser)
    for run_id in _run_ids(args.run_id, args.rerun):
        run = _prepare(args, run_id=run_id)
        if args.dry_run:
            _print_dry_run(args, run)
            continue
        results = []
        for framework_prompt in run.frameworks:
            print(f"running {run.question_id} on {framework_prompt.framework}")
            results.append(_run_framework(args, run, framework_prompt))
        for result in results:
            write_summary(result.run_dir, results)
        print("run directories:")
        for framework_prompt in run.frameworks:
            print(f"  {framework_prompt.run_dir}")
    return 0


def register(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser(
        "run",
        help="Run one task through DistributedAgents, Codex, Claude Code, or Biomni.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--task", type=Path, help="Declarative task TOML.")
    source.add_argument("--prompt-file", type=Path, help="Free-form prompt file.")
    parser.add_argument(
        "--frameworks",
        "--framework",
        nargs="+",
        choices=PROMPT_FRAMEWORKS,
        default=list(DEFAULT_FRAMEWORKS),
    )
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--name", help="Run namespace for --prompt-file.")
    parser.add_argument("--run-id")
    parser.add_argument("--rerun", type=positive_int, default=1)
    parser.add_argument("--old-output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--track-cost", action=argparse.BooleanOptionalAction, default=True
    )

    parser.add_argument("--distributed_agents-model", default=DEFAULT_DISTRIBUTED_AGENTS_MODEL)
    parser.add_argument(
        "--distributed_agents-backend",
        choices=DISTRIBUTED_AGENTS_BACKENDS,
        default=DEFAULT_DISTRIBUTED_AGENTS_BACKEND,
    )
    parser.add_argument(
        "--distributed_agents-mode",
        choices=DISTRIBUTED_AGENTS_QUERY_MODES,
        default=DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE,
    )
    parser.add_argument("--corpus-release")
    parser.add_argument("--distributed_agents-fairness-sandbox", action="store_true")
    parser.add_argument("--pixi-executable", default="pixi")

    parser.add_argument("--codex-model", default=DEFAULT_CODEX_MODEL)
    parser.add_argument("--codex-auth", choices=CODEX_AUTHS, default=DEFAULT_CODEX_AUTH)
    parser.add_argument(
        "--codex-sandbox",
        choices=CODEX_SANDBOXES,
        default=DEFAULT_CODEX_SANDBOX,
    )
    parser.add_argument("--codex-executable", default="codex")
    parser.add_argument(
        "--codex-bwrap",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_CODEX_BWRAP,
    )
    parser.add_argument("--codex-single-agent", action="store_true")
    parser.add_argument("--codex-developer-instructions-file", type=Path)

    parser.add_argument("--claude-model", default=DEFAULT_CLAUDE_MODEL)
    parser.add_argument(
        "--claude-permission-mode",
        choices=CLAUDE_PERMISSION_MODES,
        default=DEFAULT_CLAUDE_PERMISSION_MODE,
    )
    parser.add_argument(
        "--claude-max-turns",
        type=positive_int,
        default=DEFAULT_CLAUDE_MAX_TURNS,
    )
    parser.add_argument(
        "--claude-output-format",
        choices=CLAUDE_OUTPUT_FORMATS,
        default=DEFAULT_CLAUDE_OUTPUT_FORMAT,
    )
    parser.add_argument("--claude-executable", default="claude")
    parser.add_argument(
        "--claude-web", choices=("off", "tools", "shell"), default="off"
    )
    parser.add_argument(
        "--claude-fairness-sandbox",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_CLAUDE_FAIRNESS_SANDBOX,
    )
    parser.add_argument("--claude-input-root", action="append", type=Path)

    parser.add_argument("--biomni-model", default=DEFAULT_BIOMNI_MODEL)
    parser.add_argument("--biomni-data-path", default=DEFAULT_BIOMNI_DATA_PATH)
    parser.add_argument("--biomni-repo", type=Path, default=Path("modules/Biomni"))
    parser.add_argument("--biomni-env", default=DEFAULT_BIOMNI_ENV)
    parser.add_argument("--mamba-executable", default="mamba")
    parser.add_argument(
        "--biomni-runner-script", type=Path, default=DEFAULT_BIOMNI_RUNNER
    )
    parser.add_argument(
        "--biomni-fairness-sandbox",
        action=argparse.BooleanOptionalAction,
        default=True,
    )

    parser.add_argument(
        "--filtered-search-image",
        type=Path,
        default=DEFAULT_FILTERED_SEARCH_IMAGE,
    )
    parser.add_argument("--apptainer-executable", default="apptainer")
    parser.set_defaults(func=lambda args: _run(args, parser))
