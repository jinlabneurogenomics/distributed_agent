"""Normalize and collect framework token and cost usage.

The proxy itself lives in the isolated ``litellm-proxy`` pixi env; this package
(loaded in the eval env) only launches it and reads back per-run usage.
"""

from __future__ import annotations

from .proxy import (
    ProxyHandle,
    ProxyModelConfig,
    aggregate_usage,
    litellm_proxy,
    proxy_model_config,
    scoped_model_proxy,
    wait_for_log_settle,
)

__all__ = [
    "ProxyHandle",
    "ProxyModelConfig",
    "aggregate_usage",
    "litellm_proxy",
    "proxy_model_config",
    "scoped_model_proxy",
    "wait_for_log_settle",
]
