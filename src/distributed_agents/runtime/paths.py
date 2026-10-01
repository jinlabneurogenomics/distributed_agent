"""Stable package and user-runtime path discovery."""

import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def user_cache_dir() -> Path:
    """Return the configurable per-user cache root for DistributedAgents."""

    if configured := os.environ.get("DISTRIBUTED_AGENTS_CACHE_DIR"):
        return Path(configured).expanduser().resolve()
    if xdg_cache := os.environ.get("XDG_CACHE_HOME"):
        return (Path(xdg_cache).expanduser() / "distributed_agents").resolve()
    return (Path.home() / ".cache" / "distributed_agents").resolve()


__all__ = ["PACKAGE_ROOT", "user_cache_dir"]
