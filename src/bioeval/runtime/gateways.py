"""Coordinate the gateways leased by one protected framework run."""

from __future__ import annotations

import contextlib
import shutil
from contextlib import AbstractContextManager
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

from . import sandbox
from .policy import SourcePolicy
from .source_policy import (
    FilteredSearchHandle,
    filtered_search_proxy,
)
from .tls import (
    TlsEgressHandle,
    tls_egress_proxy,
)

if TYPE_CHECKING:
    from ..accounting import ProxyHandle


@dataclass(frozen=True)
class RuntimeGateways:
    """Connections and mount paths visible to one framework subprocess."""

    active_proxy: ProxyHandle | None
    sandbox_proxy: ProxyHandle | None
    filtered_proxy: FilteredSearchHandle | None
    tls_egress: TlsEgressHandle | None
    model_gate_host_dir: Path | None
    literature_gate_host_dir: Path | None
    tls_egress_gate_host_dir: Path | None
    biokg_gate_host_dir: Path | None
    filtered_mcp_base_url: str | None
    filtered_mcp_url: str | None
    tls_egress_proxy_url: str | None
    biokg_http_url: str | None


@contextlib.contextmanager
def framework_gateways(
    *,
    run_dir: Path,
    source_policy: SourcePolicy | None,
    filtered_search_image: Path | None,
    apptainer_executable: str,
    proxy_context: AbstractContextManager[ProxyHandle | None],
    require_model_gateway: bool = True,
    ncbi_api_key: str | None = None,
    biokg_base_url: str | None = None,
) -> Iterator[RuntimeGateways]:
    """Lease one run's model, literature, and filtered TLS egress gateways."""
    policy_enabled = bool(source_policy and source_policy.enabled)
    literature_enabled = bool(
        policy_enabled and source_policy and source_policy.literature_access
    )
    with contextlib.ExitStack() as stack:
        active_proxy = stack.enter_context(proxy_context)
        if policy_enabled and require_model_gateway and active_proxy is None:
            raise ValueError("protected runs require a model gateway")
        if literature_enabled and filtered_search_image is None:
            raise ValueError("protected runs require a filtered-search SIF")

        filtered_proxy = (
            stack.enter_context(
                filtered_search_proxy(
                    policy=source_policy,
                    image=filtered_search_image,
                    run_dir=run_dir,
                    apptainer_executable=apptainer_executable,
                    ncbi_api_key=ncbi_api_key,
                )
            )
            if literature_enabled
            else None
        )
        tls_egress = (
            stack.enter_context(tls_egress_proxy(policy=source_policy, run_dir=run_dir))
            if policy_enabled
            else None
        )
        model_bridge = (
            stack.enter_context(
                sandbox.unix_socket_tcp_bridge(
                    active_proxy.base_url,
                    log_path=run_dir / "model_gateway_bridge.log",
                )
            )
            if policy_enabled and active_proxy is not None
            else None
        )
        literature_bridge = (
            stack.enter_context(
                sandbox.unix_socket_tcp_bridge(
                    filtered_proxy.mcp_url,
                    log_path=run_dir / "literature_gateway_bridge.log",
                )
            )
            if filtered_proxy is not None
            else None
        )
        tls_egress_bridge = (
            stack.enter_context(
                sandbox.unix_socket_tcp_bridge(
                    tls_egress.base_url,
                    log_path=run_dir / "tls_egress_gateway_bridge.log",
                )
            )
            if tls_egress is not None
            else None
        )
        biokg_bridge = (
            stack.enter_context(
                sandbox.unix_socket_tcp_bridge(
                    biokg_base_url,
                    log_path=run_dir / "biokg_gateway_bridge.log",
                )
            )
            if policy_enabled and biokg_base_url is not None
            else None
        )
        if tls_egress_bridge is not None and tls_egress is not None:
            shutil.copyfile(
                tls_egress.ca_cert_path,
                tls_egress_bridge.host_dir / "mitmproxy-ca-cert.pem",
            )

        sandbox_proxy = active_proxy
        if model_bridge is not None and active_proxy is not None:
            sandbox_proxy = replace(
                active_proxy,
                base_url=f"http://127.0.0.1:{sandbox.MODEL_GATE_PORT}/v1",
            )
        filtered_base_url = (
            f"http://127.0.0.1:{sandbox.LITERATURE_GATE_PORT}"
            if literature_bridge is not None
            else None
        )
        yield RuntimeGateways(
            active_proxy=active_proxy,
            sandbox_proxy=sandbox_proxy,
            filtered_proxy=filtered_proxy,
            tls_egress=tls_egress,
            model_gate_host_dir=(
                model_bridge.host_dir if model_bridge is not None else None
            ),
            literature_gate_host_dir=(
                literature_bridge.host_dir if literature_bridge is not None else None
            ),
            tls_egress_gate_host_dir=(
                tls_egress_bridge.host_dir if tls_egress_bridge is not None else None
            ),
            biokg_gate_host_dir=(
                biokg_bridge.host_dir if biokg_bridge is not None else None
            ),
            filtered_mcp_base_url=filtered_base_url,
            filtered_mcp_url=(
                f"{filtered_base_url}/mcp" if filtered_base_url else None
            ),
            tls_egress_proxy_url=(
                tls_egress.proxy_url(
                    host="127.0.0.1",
                    port=sandbox.TLS_EGRESS_GATE_PORT,
                )
                if tls_egress_bridge is not None
                else None
            ),
            biokg_http_url=(
                f"http://127.0.0.1:{sandbox.BIOKG_GATE_PORT}"
                if biokg_bridge is not None
                else None
            ),
        )
