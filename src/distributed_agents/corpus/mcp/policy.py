"""Request-scoped corpus capability policy."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .errors import CorpusToolError


@dataclass(frozen=True)
class CapabilityPolicy:
    path: Path
    availability: Mapping[str, bool]

    @classmethod
    def load(cls, path: Path) -> "CapabilityPolicy":
        resolved = path.expanduser().resolve()
        if not resolved.is_file():
            raise CorpusToolError(f"capability manifest is unavailable: {resolved}")
        payload = json.loads(resolved.read_text(encoding="utf-8"))
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, list):
            raise CorpusToolError("capability manifest has no capabilities list")
        availability = {
            str(item.get("id")): bool(item.get("available"))
            for item in capabilities
            if isinstance(item, Mapping) and item.get("id")
        }
        return cls(path=resolved, availability=availability)

    def allows(self, capability: str) -> bool:
        return bool(self.availability.get(capability))

    def require(self, capability: str) -> None:
        if not self.allows(capability):
            raise CorpusToolError(
                f"operation unavailable under the current task policy: {capability}"
            )

