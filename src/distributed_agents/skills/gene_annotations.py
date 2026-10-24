"""Host-side discovery of the dataset's curated gene-annotation store."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

from ..corpus.registry import CorpusRegistryError, CorpusRelease, get_release


GENE_STORE_ENV = "DISTRIBUTED_AGENTS_GENE_STORE"


def _release_index(release: CorpusRelease) -> Path | None:
    if "gene_analog_index" not in release.manifest.get("artifacts", {}):
        return None
    path = release.artifact("gene_analog_index")
    return path if path.is_file() else None


def resolve_gene_store(
    release: CorpusRelease | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path | None:
    """Find an explicit store or a declared annotation index, without downloads.

    Explicit paths may name a legacy Parquet directory or a SQLite index. They
    remain authoritative even when missing, so callers can report the bad path.
    Shi holdout shares Shi's assay-wide curated annotations, but never its
    Findings or report data. Other corpus families do not inherit that fallback.
    """

    environment = os.environ if environ is None else environ
    configured = environment.get(GENE_STORE_ENV, "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    if release is None:
        try:
            release = get_release(environ=environment)
        except CorpusRegistryError:
            return None
    index = _release_index(release)
    if index is not None:
        return index
    if release.manifest.get("corpus_family") != "shi_holdout":
        return None
    try:
        fallback = get_release("shi", environ=environment)
    except CorpusRegistryError:
        return None
    if fallback.manifest.get("corpus_family") != "shi":
        return None
    return _release_index(fallback)


def configure_gene_store(
    runtime_env: dict[str, str],
    release: CorpusRelease,
    *,
    working_directory: Path | None = None,
    use_default: bool = True,
) -> Path | None:
    """Pin the host-resolved store in the child environment and return its mount.

    Resolve before entering a sandbox: the child needs only this exact file or
    legacy directory, without access to other releases or registry modules.
    Custom skill catalogs receive an implicit store only when requested.
    """

    environment = {**os.environ, **runtime_env}
    configured = environment.get(GENE_STORE_ENV, "").strip()
    if not configured and not use_default:
        return None
    if configured and working_directory is not None:
        path = Path(configured).expanduser()
        if not path.is_absolute():
            environment[GENE_STORE_ENV] = str(working_directory / path)
    store = resolve_gene_store(release, environ=environment)
    if store is not None:
        runtime_env[GENE_STORE_ENV] = str(store)
    return store


__all__ = ["GENE_STORE_ENV", "configure_gene_store", "resolve_gene_store"]
