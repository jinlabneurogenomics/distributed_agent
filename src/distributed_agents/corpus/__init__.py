"""Versioned corpus releases with dependency-light package initialization."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .doctor import doctor_release
    from .models import CorpusRegistryError, CorpusRelease, DoctorReport
    from .registry import (
        DEFAULT_RELEASE_ENV,
        RELEASE_ROOTS_ENV,
        available_releases,
        get_release,
        release_roots,
    )

__all__ = [
    "DEFAULT_RELEASE_ENV",
    "RELEASE_ROOTS_ENV",
    "CorpusRegistryError",
    "CorpusRelease",
    "DoctorReport",
    "available_releases",
    "doctor_release",
    "get_release",
    "release_roots",
]

_LAZY_EXPORTS = {
    "DEFAULT_RELEASE_ENV": (".registry", "DEFAULT_RELEASE_ENV"),
    "RELEASE_ROOTS_ENV": (".registry", "RELEASE_ROOTS_ENV"),
    "CorpusRegistryError": (".models", "CorpusRegistryError"),
    "CorpusRelease": (".models", "CorpusRelease"),
    "DoctorReport": (".models", "DoctorReport"),
    "available_releases": (".registry", "available_releases"),
    "doctor_release": (".doctor", "doctor_release"),
    "get_release": (".registry", "get_release"),
    "release_roots": (".registry", "release_roots"),
}


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute = target
    value = getattr(import_module(module_name, __name__), attribute)
    globals()[name] = value
    return value
