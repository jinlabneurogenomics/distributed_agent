"""Normalize token usage and estimate list-price cost."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal


REPO_ROOT = Path(__file__).resolve().parents[2]
# Product aliases are convenient interactively but make an eval irreproducible.
# Resolve the aliases accepted by our CLI to an explicit API model before launch.
_RUNTIME_MODEL_ALIASES = {
    "opus": "claude-opus-4-8",
    "sonnet": "claude-sonnet-4-6",
    "opus-4-8": "claude-opus-4-8",
    "opus-4-7": "claude-opus-4-7",
    "opus-4-6": "claude-opus-4-6",
    "opus-4-5": "claude-opus-4-5",
    "sonnet-4-6": "claude-sonnet-4-6",
    "sonnet-4-5": "claude-sonnet-4-5",
}

# Private aliases still need a public list-price analogue for cost/performance
# comparisons. Keep this explicit rather than silently guessing by prefix.
_PRICING_MODEL_ALIASES = {
    "gpt-rosalind-260428": "gpt-5.4-2026-03-05",
    "gpt-rosalind-5.5": "gpt-5.5",
}


def runtime_model_name(model: str) -> str:
    """Return a reproducible model id suitable for the framework subprocess."""
    model = model.strip()
    if model in _RUNTIME_MODEL_ALIASES:
        return _RUNTIME_MODEL_ALIASES[model]
    if model.startswith(("opus-", "sonnet-", "haiku-")):
        return f"claude-{model}"
    return model


def pricing_model_name(model: str) -> str:
    """Return the LiteLLM catalog id used for list-price estimation."""
    runtime_name = runtime_model_name(model)
    return _PRICING_MODEL_ALIASES.get(runtime_name, runtime_name)


def model_provider(model: str) -> Literal["openai", "anthropic"]:
    """Infer the only providers currently supported by BioEval's model gateway."""
    canonical = runtime_model_name(model)
    if canonical.startswith("claude-"):
        return "anthropic"
    if canonical.startswith("gpt-"):
        return "openai"
    raise ValueError(
        f"cannot infer a cost-tracked provider for model {model!r}; "
        "use an explicit gpt-* or claude-* model"
    )


@dataclass(frozen=True)
class PricingCatalog:
    entries: dict[str, dict[str, Any]]

    def lookup(self, model: str) -> tuple[str, dict[str, Any]] | None:
        resolved = pricing_model_name(model)
        candidates = (
            resolved,
            resolved.removeprefix("openai/").removeprefix("anthropic/"),
        )
        for candidate in candidates:
            entry = self.entries.get(candidate)
            if isinstance(entry, dict):
                return candidate, entry
        return None


def _catalog_candidates() -> list[Path]:
    candidates: list[Path] = []
    override = os.environ.get("BIOEVAL_LITELLM_PRICE_CATALOG")
    if override:
        candidates.append(Path(override).expanduser())
    candidates.extend(
        sorted(
            (REPO_ROOT / ".pixi" / "envs" / "litellm-proxy" / "lib").glob(
                "python*/site-packages/litellm/"
                "model_prices_and_context_window_backup.json"
            )
        )
    )
    return candidates


@lru_cache(maxsize=4)
def _load_catalog_path(path_text: str) -> PricingCatalog:
    path = Path(path_text)
    entries = json.loads(path.read_text())
    if not isinstance(entries, dict):
        raise ValueError(f"LiteLLM pricing catalog is not an object: {path}")
    return PricingCatalog(entries=entries)


def load_pricing_catalog() -> PricingCatalog | None:
    """Load the catalog shipped by the pixi-locked LiteLLM proxy environment."""
    for path in _catalog_candidates():
        if path.is_file():
            return _load_catalog_path(str(path.resolve()))
    return None


def _integer(usage: dict[str, Any], *keys: str) -> int:
    for key in keys:
        value = usage.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def _catalog_estimate(
    usage: dict[str, Any],
    *,
    model: str,
    catalog: PricingCatalog,
) -> tuple[float, dict[str, Any]] | None:
    found = catalog.lookup(model)
    if found is None:
        return None
    resolved_model, rates = found
    input_tokens = _integer(usage, "input_tokens", "prompt_tokens")
    output_tokens = _integer(usage, "output_tokens", "completion_tokens")
    cache_read = _integer(usage, "cache_read_input_tokens", "cached_input_tokens")
    cache_write = _integer(usage, "cache_creation_input_tokens")

    input_rate = float(rates.get("input_cost_per_token") or 0.0)
    output_rate = float(rates.get("output_cost_per_token") or 0.0)
    cache_read_rate = float(rates.get("cache_read_input_token_cost") or input_rate)
    cache_write_rate = float(rates.get("cache_creation_input_token_cost") or input_rate)
    provider = str(rates.get("litellm_provider") or "")

    # OpenAI reports cached tokens as a subset of input_tokens; Anthropic reports
    # regular, cache-read, and cache-creation input buckets separately.
    billable_input = (
        max(0, input_tokens - cache_read)
        if provider in {"openai", "azure", "azure_ai"}
        else input_tokens
    )
    estimated = (
        billable_input * input_rate
        + output_tokens * output_rate
        + cache_read * cache_read_rate
        + cache_write * cache_write_rate
    )
    pricing = {
        "source": "litellm",
        "requested_model": model,
        "resolved_model": resolved_model,
        "rates_usd_per_token": {
            "input": input_rate,
            "output": output_rate,
            "cache_read": cache_read_rate,
            "cache_write": cache_write_rate,
        },
    }
    return round(estimated, 8), pricing


CostSource = Literal["litellm", "provider", "tokens"]


def finalize_usage(
    usage: dict[str, Any] | None,
    *,
    model: str,
    cost_source: CostSource,
    pricing_enabled: bool = True,
) -> dict[str, Any] | None:
    """Return one cross-framework usage and cost schema."""
    if usage is None:
        return None
    normalized = dict(usage)
    input_tokens = _integer(normalized, "input_tokens", "prompt_tokens")
    output_tokens = _integer(normalized, "output_tokens", "completion_tokens")
    cache_read_tokens = _integer(
        normalized,
        "cache_read_input_tokens",
        "cached_input_tokens",
    )
    cache_creation_tokens = _integer(
        normalized,
        "cache_creation_input_tokens",
    )
    normalized.setdefault("input_tokens", input_tokens)
    normalized.setdefault("output_tokens", output_tokens)
    normalized.setdefault("cache_read_input_tokens", cache_read_tokens)
    normalized.setdefault("cache_creation_input_tokens", cache_creation_tokens)
    normalized.setdefault("total_tokens", input_tokens + output_tokens)
    normalized.setdefault("requests", 0)

    existing_cost = normalized.get("cost_usd")
    provider_cost: float | None = None
    proxy_cost: float | None = None
    estimated_cost: float | None = None
    if isinstance(existing_cost, (int, float)):
        if cost_source == "provider":
            provider_cost = float(existing_cost)
        elif cost_source == "litellm" and not normalized.get("cost_unconfigured"):
            proxy_cost = float(existing_cost)

    catalog = load_pricing_catalog() if pricing_enabled else None
    priced = (
        _catalog_estimate(normalized, model=model, catalog=catalog)
        if catalog is not None
        else None
    )
    if priced is not None:
        catalog_cost, pricing = priced
        normalized["pricing"] = pricing
        estimated_cost = catalog_cost
    elif pricing_enabled:
        normalized["pricing"] = {
            "source": "litellm",
            "requested_model": model,
            "resolved_model": pricing_model_name(model),
            "status": "model-not-found"
            if catalog is not None
            else "catalog-unavailable",
        }
    if estimated_cost is None:
        estimated_cost = proxy_cost

    normalized["provider_cost_usd"] = provider_cost
    normalized["proxy_cost_usd"] = proxy_cost
    normalized["estimated_list_cost_usd"] = estimated_cost
    normalized["cost_usd"] = (
        provider_cost
        if provider_cost is not None
        else estimated_cost
        if estimated_cost is not None
        else 0.0
    )
    normalized["cost_unconfigured"] = provider_cost is None and estimated_cost is None
    return normalized
