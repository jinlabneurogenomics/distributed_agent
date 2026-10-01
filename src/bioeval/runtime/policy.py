"""Define and validate the protected-source contract used by every framework."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

FILTERED_SEARCH_MODE = "filtered-literature"


@dataclass(frozen=True)
class SourcePolicy:
    """A task's source-denial rules, retained only in the host-side harness."""

    mode: str
    deny_patterns: tuple[str, ...]
    max_results: int = 20
    literature_access: bool = True

    @property
    def enabled(self) -> bool:
        return self.mode == FILTERED_SEARCH_MODE

    @property
    def digest(self) -> str:
        payload = json.dumps(
            {
                "mode": self.mode,
                "deny_patterns": self.deny_patterns,
                "max_results": self.max_results,
                "literature_access": self.literature_access,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(payload).hexdigest()

    def public_metadata(self) -> dict:
        return {
            "mode": self.mode,
            "policy_sha256": self.digest,
            "deny_pattern_count": len(self.deny_patterns),
            "max_results": self.max_results,
            "literature_access": self.literature_access,
        }

    def broker_payload(self) -> dict:
        return {
            "deny_patterns": list(self.deny_patterns),
            "max_results": self.max_results,
            "literature_access": self.literature_access,
        }

    def matches(self, text: str) -> list[str]:
        folded = text.casefold()
        compact = re.sub(r"[^a-z0-9]+", "", folded)
        matches: list[str] = []
        for pattern in self.deny_patterns:
            pattern_folded = pattern.casefold()
            pattern_compact = re.sub(r"[^a-z0-9]+", "", pattern_folded)
            if pattern_folded in folded or (
                len(pattern_compact) >= 8 and pattern_compact in compact
            ):
                matches.append(hashlib.sha256(pattern.encode()).hexdigest()[:12])
        return sorted(set(matches))


def write_source_filtered_copy(
    source: Path,
    destination: Path,
    *,
    policy: SourcePolicy,
) -> Path:
    """Copy an allowed local corpus while redacting protected source identifiers."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    replacements: list[re.Pattern[str]] = []
    compact_replacements: dict[str, re.Pattern[str]] = {}
    for value in policy.deny_patterns:
        tokens = re.findall(r"[A-Za-z0-9]+", value)
        if not tokens:
            continue
        replacements.append(
            re.compile(
                r"[^A-Za-z0-9]*".join(re.escape(token) for token in tokens),
                flags=re.IGNORECASE,
            )
        )
        compact = "".join(tokens)
        pattern_hash = hashlib.sha256(value.encode()).hexdigest()[:12]
        compact_replacements[pattern_hash] = re.compile(
            r"[^A-Za-z0-9]*".join(re.escape(char) for char in compact),
            flags=re.IGNORECASE,
        )
    with (
        source.open(encoding="utf-8", errors="replace") as src,
        destination.open("w", encoding="utf-8") as dst,
    ):
        for line in src:
            filtered = line
            for pattern in replacements:
                filtered = pattern.sub("[protected source identifier]", filtered)
            for pattern_hash in policy.matches(filtered):
                filtered = compact_replacements[pattern_hash].sub(
                    "[protected source identifier]", filtered
                )
            if policy.matches(filtered):
                raise ValueError(
                    f"failed to redact protected identifiers from {source}"
                )
            dst.write(filtered)
    return destination


def source_policy_from_dict(data: dict | None) -> SourcePolicy | None:
    """Parse and validate an optional task-level source policy."""
    if not data:
        return None
    mode = str(data.get("mode", "")).strip()
    if not mode:
        return None
    if mode != FILTERED_SEARCH_MODE:
        raise ValueError(f"unsupported source_policy.mode: {mode!r}")
    deny_patterns = tuple(
        str(value).strip()
        for value in data.get("deny_patterns", ())
        if str(value).strip()
    )
    if not deny_patterns:
        raise ValueError("filtered source policy requires deny_patterns")
    if any(len(value) < 6 for value in deny_patterns):
        raise ValueError("source-policy deny patterns must be at least 6 characters")
    max_results = int(data.get("max_results", 20))
    if not 1 <= max_results <= 20:
        raise ValueError("source-policy max_results must be between 1 and 20")
    literature_access = data.get("literature_access", True)
    if not isinstance(literature_access, bool):
        raise ValueError("source-policy literature_access must be a boolean")
    return SourcePolicy(
        mode=mode,
        deny_patterns=deny_patterns,
        max_results=max_results,
        literature_access=literature_access,
    )
