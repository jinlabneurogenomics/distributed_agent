#!/usr/bin/env python3
"""Inject BioEval's Codex enclosure into a DistributedAgents query run."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from bioeval.runtime import sandbox


CONFIG_ENV = "BIOEVAL_DISTRIBUTED_AGENTS_CODEX_SANDBOX"
MODEL_PROXY_BRIDGE = (
    Path(__file__).resolve().parents[1] / "runtime" / "model_proxy_bridge.py"
)


def _config() -> dict[str, object]:
    raw = os.environ.get(CONFIG_ENV, "")
    if not raw:
        raise RuntimeError(f"missing {CONFIG_ENV}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError(f"{CONFIG_ENV} must contain a JSON object")
    return value


def _paths(value: object) -> list[Path]:
    if not isinstance(value, list):
        return []
    return [Path(str(item)).expanduser().absolute() for item in value]


def main(argv: list[str] | None = None) -> int:
    config = _config()
    real_executable = str(config.get("codex_executable") or "codex")
    resolved = shutil.which(real_executable)
    if resolved is None:
        raise RuntimeError(f"Codex executable not found: {real_executable!r}")
    real = str(Path(resolved).resolve())
    command = [real, *(argv if argv is not None else sys.argv[1:])]
    run_dir = Path(str(config["run_dir"])).expanduser().absolute()
    allow_ro = _paths(config.get("allow_ro"))
    allow_rw = [run_dir]
    codex_home = os.environ.get("CODEX_HOME", "").strip()
    if codex_home:
        allow_rw.append(Path(codex_home).expanduser().absolute())

    toolchain = sandbox.codex_toolchain_paths(real_executable)
    analysis_env = Path(str(config["analysis_env"])).expanduser().absolute()
    bin_dir = str(toolchain[0]) if toolchain else None
    path_parts = [str(analysis_env / "bin")]
    if bin_dir:
        path_parts.append(bin_dir)
    path_parts.extend(("/usr/bin", "/bin"))

    network_isolated = bool(config.get("network_isolated"))
    extra_binds: list[tuple[str, str, bool]] = []
    if network_isolated:
        tls_dir = str(config.get("tls_egress_gate_host_dir") or "")
        if not tls_dir:
            raise RuntimeError("network-isolated DistributedAgents run lacks TLS gateway")
        inner = command
        command = [
            "/usr/bin/python3",
            str(MODEL_PROXY_BRIDGE),
            "--socket",
            sandbox.TLS_EGRESS_GATE_SOCKET,
            "--port",
            str(sandbox.TLS_EGRESS_GATE_PORT),
        ]
        literature_dir = str(config.get("literature_gate_host_dir") or "")
        if literature_dir:
            command.extend(
                [
                    "--relay",
                    (
                        f"{sandbox.LITERATURE_GATE_PORT}:"
                        f"{sandbox.LITERATURE_GATE_SOCKET}"
                    ),
                ]
            )
            extra_binds.append((literature_dir, sandbox.LITERATURE_GATE_DIR, False))
        biokg_dir = str(config.get("biokg_gate_host_dir") or "")
        if biokg_dir:
            command.extend(
                [
                    "--relay",
                    f"{sandbox.BIOKG_GATE_PORT}:{sandbox.BIOKG_GATE_SOCKET}",
                ]
            )
            extra_binds.append((biokg_dir, sandbox.BIOKG_GATE_DIR, False))
        command.extend(["--", *inner])
        extra_binds.append((tls_dir, sandbox.TLS_EGRESS_GATE_DIR, False))
        allow_ro.append(MODEL_PROXY_BRIDGE)

    wrapped = sandbox.bwrap_allowlist_command(
        command,
        chdir=str(run_dir),
        allow_ro=[analysis_env, *allow_ro, *toolchain],
        allow_rw=allow_rw,
        path=":".join(path_parts),
        share_net=not network_isolated,
        extra_binds=extra_binds,
    )
    return subprocess.call(wrapped, env=os.environ.copy())


if __name__ == "__main__":
    raise SystemExit(main())
