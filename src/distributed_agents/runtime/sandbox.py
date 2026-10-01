"""Minimal filesystem isolation used by the standalone DistributedAgents runtime.

This is product safety, not evaluation policy: it exposes only declared task
inputs, release capabilities, the run directory, and the Codex toolchain.
BioEval may replace this enclosure with its own launcher for controlled runs.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable, Mapping, Sequence


DEFAULT_OS_ROOTS: tuple[str, ...] = (
    "/usr",
    "/bin",
    "/sbin",
    "/lib",
    "/lib64",
    "/etc",
    "/opt",
)
FAKE_HOME = "/sandbox-home"


def clean_env(
    *,
    fake_home: str = FAKE_HOME,
    passthrough_keys: Iterable[str] = (),
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build a scrubbed environment containing only explicitly allowed values."""

    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": fake_home,
        "TMPDIR": "/tmp",
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
    }
    for key in passthrough_keys:
        value = os.environ.get(key)
        if value is not None:
            env[key] = value
    if extra:
        env.update(extra)
    return env


def bwrap_allowlist_command(
    inner_cmd: Sequence[str],
    *,
    chdir: str = FAKE_HOME,
    allow_ro: Iterable[Path] = (),
    allow_rw: Iterable[Path] = (),
    os_roots: Iterable[str] = DEFAULT_OS_ROOTS,
    share_net: bool = True,
    fake_home: str = FAKE_HOME,
    path: str = "/usr/bin:/bin",
    extra_binds: Iterable[tuple[str, str, bool]] = (),
    setenv: Mapping[str, str] | None = None,
    bwrap_executable: str = "bwrap",
) -> list[str]:
    """Wrap a command in a small allowlist Bubblewrap namespace."""

    if shutil.which(bwrap_executable) is None:
        raise RuntimeError(
            f"{bwrap_executable} not found on PATH; install bubblewrap or use "
            "--no-codex-bwrap only inside another trusted enclosure."
        )
    args = [bwrap_executable, "--unshare-all"]
    if share_net:
        args.append("--share-net")
    args += [
        "--dev",
        "/dev",
        "--proc",
        "/proc",
        "--tmpfs",
        "/tmp",
        "--tmpfs",
        fake_home,
        "--die-with-parent",
    ]
    for root in os_roots:
        if Path(root).exists():
            args += ["--ro-bind", root, root]
    seen: set[str] = set()
    for raw in allow_ro:
        destination = str(Path(raw).absolute())
        if destination in seen or not Path(destination).exists():
            continue
        seen.add(destination)
        args += ["--ro-bind", destination, destination]
    for raw in allow_rw:
        path_value = Path(raw).absolute()
        if str(path_value) in seen:
            continue
        seen.add(str(path_value))
        path_value.mkdir(parents=True, exist_ok=True)
        args += ["--bind", str(path_value), str(path_value)]
    for source, destination, read_only in extra_binds:
        if Path(source).exists():
            args += (
                ["--ro-bind", source, destination]
                if read_only
                else ["--bind", source, destination]
            )
    for key, value in sorted((setenv or {}).items()):
        args += ["--setenv", key, value]
    args += [
        "--setenv",
        "HOME",
        fake_home,
        "--setenv",
        "PATH",
        path,
        "--chdir",
        chdir,
        "--",
        *inner_cmd,
    ]
    return args


def codex_toolchain_paths(codex_executable: str = "codex") -> list[Path]:
    """Return the launcher and release paths needed to execute Codex."""

    which = shutil.which(codex_executable)
    if which is None:
        return []
    launcher = Path(which)
    real = launcher.resolve()
    paths = [launcher.parent]
    if len(real.parents) > 1:
        paths.append(real.parents[1])
    return paths
