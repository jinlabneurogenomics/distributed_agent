#!/usr/bin/env python3
"""Semantically reconcile stale legacy Claims to corrected Sourceguard Findings.

The historical Finding IDs are target-local ordinals, not cross-release
identities.  This workflow therefore treats each legacy Claim proposition as
the unit under review and asks a schema-constrained model to identify the
Sourceguard Findings that now support it.  A missing nonessential member does
not invalidate a Claim; unsupported essential propositions do.

The workflow is resumable and split into three commands:

* ``prepare`` builds bounded target-component packets and a response schema;
* ``run`` performs model-backed semantic reconciliation into ignored work data;
* ``finalize`` validates every result and writes release-owned audit artifacts.
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .audit_reconciliation import deny_matches
except ImportError:
    from audit_reconciliation import deny_matches


RELEASE_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = RELEASE_ROOT.parent / "legacy_reports_v1"
DEFAULT_WORK = RELEASE_ROOT / "_work" / "claim_reconciliation"
DEFAULT_OUTPUT = RELEASE_ROOT / "artifacts" / "audits" / "claim_reconciliation.jsonl"
DEFAULT_UNASSIGNED = (
    RELEASE_ROOT / "artifacts" / "audits" / "claim_reconciliation_unassigned.jsonl"
)
DEFAULT_SUMMARY = (
    RELEASE_ROOT / "artifacts" / "audits" / "claim_reconciliation.summary.json"
)

OLD_FINDINGS = LEGACY_ROOT / "artifacts" / "ledgers" / "findings.csv"
NEW_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
OLD_ASSIGNMENTS = (
    LEGACY_ROOT
    / "projections"
    / "biokg"
    / "data"
    / "claims"
    / "claim_assignments.tsv"
)
REPLACEMENT_TARGETS = RELEASE_ROOT / "provenance" / "sourceguard_replacement_targets.txt"

ADJUDICATION_VERSION = "legacy-sourceguard-claim-reconciliation-v1"
SCHEMA_VERSION = "distributed_agents-claim-reconciliation-v1"

CONTRIBUTIONS = ("essential", "supporting", "nonessential")
MEMBER_MATCH = (
    "matched",
    "partially_matched",
    "missing_nonessential",
    "missing_essential",
    "superseded",
)
DISPOSITIONS = ("preserved", "revised", "missing")
COVERAGE = ("full", "partial", "none")
CLAIM_ROLES = ("anchor", "corroborating", "boundary", "implication", "warning")
CONFIDENCE = ("high", "moderate", "low")


SYSTEM_PROMPT = """You reconcile a historical biological Claim layer to corrected Sourceguard Findings.

The historical Claim proposition is the unit under review. Historical and
Sourceguard Finding IDs are unrelated target-local ordinals: NEVER match them
because their F-numbers are equal. Match only biological meaning.

The Sourceguard Findings are the only authoritative support for the reconciled
Claim. Use no outside or parametric knowledge. Do not carry a historical clause,
readout, comparison, or implication unless at least one supplied Sourceguard
Finding supports it.

First write essential_proposition as a concise neutral restatement of the
HISTORICAL canonical Claim before comparing it with Sourceguard. It must not
describe the corrected result, the reconciliation outcome, or what is missing.

Then characterize the contribution of every historical member to that Claim:

* essential: removing the member would eliminate or materially narrow a core
  proposition in the canonical Claim summary;
* supporting: it corroborates, qualifies, bounds, or grounds the core without
  being required to retain the essential proposition;
* nonessential: it is redundant or an implication/warning/boundary whose loss
  does not materially change the essential proposition.

A missing nonessential or redundant historical member does NOT invalidate a
Claim. Judge the Claim as a whole:

* preserved/full: every essential proposition is supported by the selected
  Sourceguard Findings; minor wording and nonessential members may differ;
* revised/partial: a recognizable narrower core remains, but at least one
  essential clause must be removed or materially narrowed;
* missing/none: no supplied Sourceguard Finding supports the essential
  proposition. Use no replacement Findings and an empty proposed summary.

Judge each member's match_status only against the contribution that member made
to the historical canonical Claim, not against every detail in the old Finding.
If an essential member is only partially_matched or missing_essential, the Claim
must be revised or missing. A preserved Claim's essential members must be
matched (or superseded because another corrected Finding fully carries the same
essential contribution). Supporting and nonessential members may be absent
without forcing revision when the essential proposition remains fully supported.

For preserved or revised Claims, write a concise proposed canonical summary
entailed entirely by the selected Sourceguard Findings. Select Findings by full
doc_id and assign each a Claim role. A Sourceguard Finding may support more than
one historical Claim when it genuinely consolidates multiple old propositions;
do not force uniqueness. List every supplied Sourceguard Finding that supports
no reviewed legacy Claim under unassigned_sourceguard_finding_ids.

Keep rationales concise and concrete. Return only the required JSON object."""

REPAIR_PROMPT = """The previous response failed deterministic validation: {error}

Re-adjudicate the entire packet and correct the inconsistency. In particular:

* preserved/full requires every essential member contribution to be matched or
  superseded, with no missing essential elements;
* revised/partial requires at least one essential member contribution to be
  partially matched or missing and a nonempty missing_essential_elements list;
* missing/none requires every essential member contribution to be missing, no
  replacement Findings, and an empty proposed summary;
* loss of supporting or nonessential material alone does not revise a Claim;
* every supplied Sourceguard Finding must be either used by at least one Claim
  or listed exactly once as unassigned.

Finding IDs remain semantically meaningless across releases."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def release_relative(path: Path) -> str:
    return os.path.relpath(path.resolve(), RELEASE_ROOT)


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").split())


def split_pipe(value: object) -> list[str]:
    return list(
        dict.fromkeys(part.strip() for part in str(value or "").split("|") if part.strip())
    )


def read_table(path: Path, *, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def finding_content_hash(row: Mapping[str, object]) -> str:
    fields = (
        "doc_id",
        "finding_type",
        "direction",
        "confidence",
        "literature_status",
        "summary",
        "why_it_matters",
        "genes",
        "comparators",
        "cell_types",
        "evidence_ids",
        "main_caveats",
    )
    payload = json.dumps(
        {field: normalize_text(row.get(field)) for field in fields},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_findings(path: Path) -> dict[str, dict[str, str]]:
    rows = read_table(path)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        row["doc_id"] = f"{row['target_gene']}:{row['finding_id']}"
        if row["doc_id"] in out:
            raise ValueError(f"duplicate Finding {row['doc_id']} in {path}")
        out[row["doc_id"]] = row
    return out


def finding_card(row: Mapping[str, str]) -> dict[str, Any]:
    return {
        "doc_id": row["doc_id"],
        "target_gene": row["target_gene"],
        "finding_type": row["finding_type"],
        "direction": row["direction"],
        "confidence": row["confidence"],
        "literature_status": row["literature_status"],
        "summary": normalize_text(row["summary"]),
        "why_it_matters": normalize_text(row["why_it_matters"]),
        "genes": split_pipe(row["genes"]),
        "comparators": split_pipe(row["comparators"]),
        "cell_types": split_pipe(row["cell_types"]),
        "evidence_ids": split_pipe(row["evidence_ids"]),
        "ref_ids": split_pipe(row["ref_ids"]),
        "main_caveats": normalize_text(row["main_caveats"]),
    }


class DisjointSet:
    def __init__(self, values: Iterable[str]):
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[max(left_root, right_root)] = min(left_root, right_root)


def build_scopes() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    old_findings = load_findings(OLD_FINDINGS)
    new_findings = load_findings(NEW_FINDINGS)
    assignment_rows = read_table(OLD_ASSIGNMENTS, delimiter="\t")
    changed_targets = {
        line.strip()
        for line in REPLACEMENT_TARGETS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }

    assignments_by_claim: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assignment_rows:
        assignments_by_claim[row["claim_id"]].append(row)

    affected_claims: dict[str, list[dict[str, str]]] = {}
    for claim_id, members in assignments_by_claim.items():
        if any(
            member["doc_id"] not in new_findings
            or member["source_hash"] != finding_content_hash(new_findings[member["doc_id"]])
            for member in members
        ):
            affected_claims[claim_id] = members

    claim_targets: dict[str, set[str]] = {}
    all_targets: set[str] = set()
    for claim_id, members in affected_claims.items():
        targets = {
            old_findings[member["doc_id"]]["target_gene"]
            for member in members
            if member["doc_id"] in old_findings
        }
        targets.update(
            target for member in members for target in split_pipe(member.get("targets"))
        )
        if not targets:
            raise ValueError(f"affected Claim has no target scope: {claim_id}")
        claim_targets[claim_id] = targets
        all_targets.update(targets)

    dsu = DisjointSet(all_targets)
    for targets in claim_targets.values():
        ordered = sorted(targets, key=str.casefold)
        for target in ordered[1:]:
            dsu.union(ordered[0], target)

    component_targets: dict[str, set[str]] = defaultdict(set)
    for target in all_targets:
        component_targets[dsu.find(target)].add(target)
    component_claims: dict[str, list[str]] = defaultdict(list)
    for claim_id, targets in claim_targets.items():
        component_claims[dsu.find(next(iter(targets)))].append(claim_id)

    new_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in new_findings.values():
        new_by_target[row["target_gene"]].append(row)

    scopes: list[dict[str, Any]] = []
    ordered_components = sorted(
        component_targets,
        key=lambda root: tuple(value.casefold() for value in sorted(component_targets[root])),
    )
    for index, root in enumerate(ordered_components, 1):
        targets = sorted(component_targets[root], key=str.casefold)
        claims = []
        for claim_id in sorted(component_claims[root]):
            members = sorted(affected_claims[claim_id], key=lambda row: row["doc_id"].casefold())
            first = members[0]
            claims.append(
                {
                    "legacy_claim_id": claim_id,
                    "canonical_summary": first["canonical_summary"],
                    "relation_family": first["relation_family"],
                    "direction_pattern": first["direction_pattern"],
                    "evidence_mode": first["evidence_mode"],
                    "support_level": first["support_level"],
                    "active_default": first["active_default"].casefold() == "true",
                    "readouts": split_pipe(first["readouts"]),
                    "cell_scope": split_pipe(first["cell_scope"]),
                    "confidence": first["confidence"],
                    "legacy_members": [
                        {
                            "member_role": member["member_role"],
                            "finding": finding_card(old_findings[member["doc_id"]]),
                        }
                        for member in members
                    ],
                }
            )
        candidates = [
            finding_card(row)
            for target in targets
            for row in sorted(new_by_target[target], key=lambda item: item["finding_id"])
        ]
        scopes.append(
            {
                "scope_id": f"S{index:04d}",
                "target_genes": targets,
                "legacy_claims": claims,
                "sourceguard_findings": candidates,
            }
        )

    metadata = {
        "legacy_findings": len(old_findings),
        "sourceguard_findings": len(new_findings),
        "legacy_claims": len(assignments_by_claim),
        "affected_claims": len(affected_claims),
        "unchanged_claims": len(assignments_by_claim) - len(affected_claims),
        "changed_targets": len(changed_targets),
        "target_components": len(scopes),
    }
    return scopes, metadata


def build_packets(
    scopes: list[dict[str, Any]], *, max_scopes: int, max_prompt_chars: int
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    for scope in scopes:
        scope_chars = len(json.dumps(scope, ensure_ascii=False))
        if current and (len(current) >= max_scopes or current_chars + scope_chars > max_prompt_chars):
            packets.append({"packet_id": f"P{len(packets) + 1:04d}", "scopes": current})
            current = []
            current_chars = 0
        current.append(scope)
        current_chars += scope_chars
    if current:
        packets.append({"packet_id": f"P{len(packets) + 1:04d}", "scopes": current})
    return packets


def response_schema() -> dict[str, Any]:
    replacement = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "doc_id": {"type": "string"},
            "role": {"type": "string", "enum": list(CLAIM_ROLES)},
            "rationale": {"type": "string"},
        },
        "required": ["doc_id", "role", "rationale"],
    }
    member = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "legacy_doc_id": {"type": "string"},
            "contribution": {"type": "string", "enum": list(CONTRIBUTIONS)},
            "match_status": {"type": "string", "enum": list(MEMBER_MATCH)},
            "replacement_finding_ids": {"type": "array", "items": {"type": "string"}},
            "rationale": {"type": "string"},
        },
        "required": [
            "legacy_doc_id",
            "contribution",
            "match_status",
            "replacement_finding_ids",
            "rationale",
        ],
    }
    claim = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "legacy_claim_id": {"type": "string"},
            "essential_proposition": {"type": "string"},
            "disposition": {"type": "string", "enum": list(DISPOSITIONS)},
            "coverage": {"type": "string", "enum": list(COVERAGE)},
            "replacement_findings": {"type": "array", "items": replacement},
            "proposed_canonical_summary": {"type": "string"},
            "missing_essential_elements": {"type": "array", "items": {"type": "string"}},
            "confidence": {"type": "string", "enum": list(CONFIDENCE)},
            "rationale": {"type": "string"},
            "legacy_members": {"type": "array", "items": member},
        },
        "required": [
            "legacy_claim_id",
            "essential_proposition",
            "disposition",
            "coverage",
            "replacement_findings",
            "proposed_canonical_summary",
            "missing_essential_elements",
            "confidence",
            "rationale",
            "legacy_members",
        ],
    }
    scope = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "scope_id": {"type": "string"},
            "claims": {"type": "array", "items": claim},
            "unassigned_sourceguard_finding_ids": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["scope_id", "claims", "unassigned_sourceguard_finding_ids"],
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "packet_id": {"type": "string"},
            "scopes": {"type": "array", "items": scope},
        },
        "required": ["packet_id", "scopes"],
    }


def prompt_for(packet: Mapping[str, Any], *, repair_error: str = "") -> str:
    prompt = (
        SYSTEM_PROMPT
        + "\n\nReconcile every supplied scope and every legacy Claim exactly once.\n\n"
        + json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    )
    if repair_error:
        prompt += "\n\n" + REPAIR_PROMPT.format(error=repair_error)
    return prompt


def validate_scope_result(scope: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    if result.get("scope_id") != scope["scope_id"]:
        raise ValueError(f"scope_id mismatch for {scope['scope_id']}")
    expected_claims = {
        claim["legacy_claim_id"]: claim for claim in scope["legacy_claims"]
    }
    actual_claims = result.get("claims") or []
    actual_ids = [claim.get("legacy_claim_id") for claim in actual_claims]
    if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected_claims):
        raise ValueError(f"Claim coverage mismatch for {scope['scope_id']}")
    candidate_ids = {finding["doc_id"] for finding in scope["sourceguard_findings"]}
    used: set[str] = set()
    for claim in actual_claims:
        claim_id = str(claim["legacy_claim_id"])
        expected_members = {
            member["finding"]["doc_id"]
            for member in expected_claims[claim_id]["legacy_members"]
        }
        actual_members = claim.get("legacy_members") or []
        actual_member_ids = [member.get("legacy_doc_id") for member in actual_members]
        if len(actual_member_ids) != len(set(actual_member_ids)) or set(actual_member_ids) != expected_members:
            raise ValueError(f"legacy member coverage mismatch for {claim_id}")
        replacement_ids = [item.get("doc_id") for item in claim.get("replacement_findings") or []]
        if len(replacement_ids) != len(set(replacement_ids)):
            raise ValueError(f"duplicate replacement Finding for {claim_id}")
        if any(doc_id not in candidate_ids for doc_id in replacement_ids):
            raise ValueError(f"foreign replacement Finding for {claim_id}")
        used.update(str(doc_id) for doc_id in replacement_ids)
        for member in actual_members:
            member_replacements = member.get("replacement_finding_ids") or []
            if len(member_replacements) != len(set(member_replacements)):
                raise ValueError(f"duplicate member replacement in {claim_id}")
            if any(doc_id not in candidate_ids for doc_id in member_replacements):
                raise ValueError(f"foreign member replacement in {claim_id}")

        disposition = claim.get("disposition")
        coverage = claim.get("coverage")
        summary = normalize_text(claim.get("proposed_canonical_summary"))
        missing = claim.get("missing_essential_elements") or []
        essential_statuses = {
            member.get("match_status")
            for member in actual_members
            if member.get("contribution") == "essential"
        }
        if disposition == "preserved":
            if (
                coverage != "full"
                or not replacement_ids
                or not summary
                or missing
                or essential_statuses - {"matched", "superseded"}
            ):
                raise ValueError(f"inconsistent preserved disposition for {claim_id}")
        elif disposition == "revised":
            if (
                coverage != "partial"
                or not replacement_ids
                or not summary
                or not missing
                or not essential_statuses.intersection(
                    {"partially_matched", "missing_essential"}
                )
            ):
                raise ValueError(f"inconsistent revised disposition for {claim_id}")
        elif disposition == "missing":
            if (
                coverage != "none"
                or replacement_ids
                or summary
                or not missing
                or not essential_statuses
                or essential_statuses - {"missing_essential"}
            ):
                raise ValueError(f"inconsistent missing disposition for {claim_id}")
        else:
            raise ValueError(f"invalid disposition for {claim_id}")

    unassigned = result.get("unassigned_sourceguard_finding_ids") or []
    if len(unassigned) != len(set(unassigned)) or any(doc_id not in candidate_ids for doc_id in unassigned):
        raise ValueError(f"invalid unassigned Findings for {scope['scope_id']}")
    if set(unassigned) != candidate_ids - used:
        raise ValueError(f"Sourceguard Finding accounting mismatch for {scope['scope_id']}")


def validate_packet_result(packet: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    if result.get("packet_id") != packet["packet_id"]:
        raise ValueError("packet_id mismatch")
    expected = {scope["scope_id"]: scope for scope in packet["scopes"]}
    actual = result.get("scopes") or []
    actual_ids = [scope.get("scope_id") for scope in actual]
    if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected):
        raise ValueError(f"scope coverage mismatch in {packet['packet_id']}")
    for scope_result in actual:
        validate_scope_result(expected[str(scope_result["scope_id"])], scope_result)


def run_packet(
    packet: dict[str, Any],
    *,
    results_dir: Path,
    schema_path: Path,
    model: str,
    reasoning_effort: str,
    codex: str,
    timeout_seconds: int,
    overwrite: bool,
) -> tuple[str, bool, str]:
    packet_id = packet["packet_id"]
    output = results_dir / f"{packet_id}.json"
    log = results_dir / f"{packet_id}.log"
    repair_error = ""
    if output.exists():
        try:
            parsed = json.loads(output.read_text(encoding="utf-8"))
            validate_packet_result(packet, parsed)
            if not overwrite:
                return packet_id, True, "cached"
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            repair_error = str(exc)

    command = [
        codex,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output),
        "-",
    ]
    try:
        completed = subprocess.run(
            command,
            input=prompt_for(packet, repair_error=repair_error),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        log.write_text(str(exc.stdout or ""), encoding="utf-8")
        return packet_id, False, f"timeout after {timeout_seconds}s"
    log.write_text(completed.stdout or "", encoding="utf-8")
    if completed.returncode != 0:
        return packet_id, False, f"codex exit {completed.returncode}"
    try:
        parsed = json.loads(output.read_text(encoding="utf-8"))
        validate_packet_result(packet, parsed)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return packet_id, False, str(exc)
    return packet_id, True, "completed"


def prepare(args: argparse.Namespace) -> int:
    scopes, metadata = build_scopes()
    packets = build_packets(
        scopes,
        max_scopes=max(1, args.max_scopes_per_packet),
        max_prompt_chars=max(10_000, args.max_prompt_chars),
    )
    args.work_dir.mkdir(parents=True, exist_ok=True)
    packets_path = args.work_dir / "packets.jsonl"
    schema_path = args.work_dir / "response_schema.json"
    write_jsonl(packets_path, packets)
    schema = response_schema()
    schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "adjudication_version": ADJUDICATION_VERSION,
        "created_on": date.today().isoformat(),
        "sources": {
            "legacy_findings": {
                "path": release_relative(OLD_FINDINGS),
                "sha256": sha256_file(OLD_FINDINGS),
            },
            "legacy_claim_assignments": {
                "path": release_relative(OLD_ASSIGNMENTS),
                "sha256": sha256_file(OLD_ASSIGNMENTS),
            },
            "sourceguard_findings": {
                "path": release_relative(NEW_FINDINGS),
                "sha256": sha256_file(NEW_FINDINGS),
            },
            "replacement_targets": {
                "path": release_relative(REPLACEMENT_TARGETS),
                "sha256": sha256_file(REPLACEMENT_TARGETS),
            },
        },
        "prompt_sha256": sha256_text(SYSTEM_PROMPT),
        "repair_prompt_sha256": sha256_text(REPAIR_PROMPT),
        "response_schema_sha256": sha256_file(schema_path),
        "packet_policy": {
            "max_scopes_per_packet": max(1, args.max_scopes_per_packet),
            "max_prompt_chars": max(10_000, args.max_prompt_chars),
        },
        "counts": {**metadata, "packets": len(packets)},
    }
    (args.work_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest["counts"], indent=2, sort_keys=True))
    return 0


def run(args: argparse.Namespace) -> int:
    packets_path = args.work_dir / "packets.jsonl"
    schema_path = args.work_dir / "response_schema.json"
    manifest_path = args.work_dir / "manifest.json"
    if not packets_path.exists() or not schema_path.exists() or not manifest_path.exists():
        raise ValueError(f"run prepare first under {args.work_dir}")
    packets = read_jsonl(packets_path)
    if args.packet:
        requested = set(args.packet)
        pending = [packet for packet in packets if packet["packet_id"] in requested]
        missing = requested - {packet["packet_id"] for packet in pending}
        if missing:
            raise ValueError(f"unknown packet IDs: {sorted(missing)}")
    else:
        pending = packets[: args.limit] if args.limit else packets
    results_dir = args.work_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["model"] = args.model
    manifest["reasoning_effort"] = args.reasoning_effort
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lock_path = args.work_dir / ".run.lock"
    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(f"another reconciliation run is active under {args.work_dir}") from exc
        lock.write(f"pid={os.getpid()}\n")
        lock.flush()
        outcomes: list[tuple[str, bool, str]] = []
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = [
                pool.submit(
                    run_packet,
                    packet,
                    results_dir=results_dir,
                    schema_path=schema_path,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    codex=args.codex,
                    timeout_seconds=max(1, args.timeout_seconds),
                    overwrite=args.overwrite,
                )
                for packet in pending
            ]
            for future in as_completed(futures):
                outcome = future.result()
                outcomes.append(outcome)
                print(f"{outcome[0]}: {outcome[2]}", flush=True)
    failures = [outcome for outcome in outcomes if not outcome[1]]
    print(json.dumps({"attempted": len(outcomes), "failed": failures}, indent=2))
    return 1 if failures else 0


def finalize(args: argparse.Namespace) -> int:
    packets = read_jsonl(args.work_dir / "packets.jsonl")
    manifest = json.loads((args.work_dir / "manifest.json").read_text(encoding="utf-8"))
    results_dir = args.work_dir / "results"
    reconciliations: list[dict[str, Any]] = []
    unassigned_rows: list[dict[str, Any]] = []
    candidate_by_id: dict[str, dict[str, Any]] = {}
    duplicate_support = Counter()

    for packet in packets:
        result_path = results_dir / f"{packet['packet_id']}.json"
        if not result_path.exists():
            raise ValueError(f"missing result {result_path}")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        validate_packet_result(packet, result)
        scope_inputs = {scope["scope_id"]: scope for scope in packet["scopes"]}
        for scope_result in result["scopes"]:
            scope = scope_inputs[scope_result["scope_id"]]
            legacy_inputs = {
                claim["legacy_claim_id"]: claim for claim in scope["legacy_claims"]
            }
            for finding in scope["sourceguard_findings"]:
                candidate_by_id[finding["doc_id"]] = finding
            for claim_result in scope_result["claims"]:
                legacy = legacy_inputs[claim_result["legacy_claim_id"]]
                replacement_ids = [
                    item["doc_id"] for item in claim_result["replacement_findings"]
                ]
                duplicate_support.update(replacement_ids)
                reconciliations.append(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "adjudication_version": ADJUDICATION_VERSION,
                        "scope_id": scope["scope_id"],
                        "target_genes": scope["target_genes"],
                        "legacy_claim_id": claim_result["legacy_claim_id"],
                        "legacy_canonical_summary": legacy["canonical_summary"],
                        "legacy_relation_family": legacy["relation_family"],
                        "legacy_active_default": legacy["active_default"],
                        "essential_proposition": claim_result["essential_proposition"],
                        "disposition": claim_result["disposition"],
                        "coverage": claim_result["coverage"],
                        "replacement_findings": claim_result["replacement_findings"],
                        "proposed_canonical_summary": claim_result[
                            "proposed_canonical_summary"
                        ],
                        "missing_essential_elements": claim_result[
                            "missing_essential_elements"
                        ],
                        "confidence": claim_result["confidence"],
                        "rationale": claim_result["rationale"],
                        "legacy_members": claim_result["legacy_members"],
                    }
                )
            for doc_id in scope_result["unassigned_sourceguard_finding_ids"]:
                finding = candidate_by_id[doc_id]
                unassigned_rows.append(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "scope_id": scope["scope_id"],
                        "doc_id": doc_id,
                        "target_gene": finding["target_gene"],
                        "finding_type": finding["finding_type"],
                        "summary": finding["summary"],
                    }
                )

    expected_claims = int(manifest["counts"]["affected_claims"])
    claim_ids = [row["legacy_claim_id"] for row in reconciliations]
    if len(reconciliations) != expected_claims or len(set(claim_ids)) != expected_claims:
        raise ValueError("final reconciliation does not cover every affected Claim exactly once")
    if set(candidate_by_id) != set(duplicate_support) | {
        row["doc_id"] for row in unassigned_rows
    }:
        raise ValueError("final Sourceguard candidate accounting mismatch")

    reconciliations.sort(key=lambda row: row["legacy_claim_id"])
    unassigned_rows.sort(key=lambda row: row["doc_id"].casefold())
    semantic_text = json.dumps(
        {"reconciliations": reconciliations, "unassigned": unassigned_rows},
        ensure_ascii=False,
        sort_keys=True,
    )
    sourceguard_hits = deny_matches(semantic_text)
    if sourceguard_hits:
        raise ValueError(
            "sourceguard-denied content entered Claim reconciliation: "
            + ", ".join(sourceguard_hits)
        )
    write_jsonl(args.output, reconciliations)
    write_jsonl(args.unassigned_output, unassigned_rows)

    disposition_counts = Counter(row["disposition"] for row in reconciliations)
    confidence_counts = Counter(row["confidence"] for row in reconciliations)
    member_contributions = Counter(
        member["contribution"] for row in reconciliations for member in row["legacy_members"]
    )
    member_matches = Counter(
        member["match_status"] for row in reconciliations for member in row["legacy_members"]
    )
    safe_counts = Counter()
    for row in reconciliations:
        target_class = (
            "safe_control"
            if all(target.casefold().startswith("safe_target") for target in row["target_genes"])
            else "biological"
        )
        safe_counts[f"{target_class}:{row['disposition']}"] += 1

    reused = [count for count in duplicate_support.values() if count > 1]
    summary = {
        "schema_version": SCHEMA_VERSION,
        "adjudication_version": ADJUDICATION_VERSION,
        "created_on": date.today().isoformat(),
        "provenance": manifest,
        "outputs": {
            "reconciliation": {
                "path": str(args.output.relative_to(RELEASE_ROOT)),
                "sha256": sha256_file(args.output),
                "bytes": args.output.stat().st_size,
                "records": len(reconciliations),
            },
            "unassigned_sourceguard_findings": {
                "path": str(args.unassigned_output.relative_to(RELEASE_ROOT)),
                "sha256": sha256_file(args.unassigned_output),
                "bytes": args.unassigned_output.stat().st_size,
                "records": len(unassigned_rows),
            },
        },
        "counts": {
            "affected_legacy_claims": len(reconciliations),
            "dispositions": dict(sorted(disposition_counts.items())),
            "confidence": dict(sorted(confidence_counts.items())),
            "target_class_dispositions": dict(sorted(safe_counts.items())),
            "legacy_member_contributions": dict(sorted(member_contributions.items())),
            "legacy_member_match_status": dict(sorted(member_matches.items())),
            "unique_replacement_findings": len(duplicate_support),
            "replacement_finding_support_links": sum(duplicate_support.values()),
            "replacement_findings_used_by_multiple_claims": len(reused),
            "unassigned_sourceguard_findings": len(unassigned_rows),
            "candidate_sourceguard_findings": len(candidate_by_id),
        },
        "integrity": {
            "all_affected_claims_reconciled_once": True,
            "all_legacy_members_characterized_once": True,
            "replacement_findings_restricted_to_target_component": True,
            "all_candidate_sourceguard_findings_accounted_for": True,
            "finding_ids_treated_as_release_local_ordinals": True,
            "nonessential_missing_members_do_not_force_claim_missing": True,
            "sourceguard_deny_hits": 0,
            "machine_local_paths": False,
        },
    }
    serialized_summary = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if any(prefix in serialized_summary for prefix in ("/gpfs/", "/Users/", "/home/")):
        raise ValueError("machine-local path entered Claim reconciliation summary")
    args.summary_output.write_text(
        serialized_summary,
        encoding="utf-8",
    )
    print(json.dumps(summary["counts"], indent=2, sort_keys=True))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--max-scopes-per-packet", type=int, default=6)
    prepare_parser.add_argument("--max-prompt-chars", type=int, default=90_000)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--model", default="gpt-rosalind-5.5")
    run_parser.add_argument("--reasoning-effort", default="high")
    run_parser.add_argument("--workers", type=int, default=4)
    run_parser.add_argument("--timeout-seconds", type=int, default=1_200)
    run_parser.add_argument("--limit", type=int, default=0)
    run_parser.add_argument("--packet", action="append", default=[])
    run_parser.add_argument("--codex", default="codex")
    run_parser.add_argument("--overwrite", action="store_true")

    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    finalize_parser.add_argument(
        "--unassigned-output", type=Path, default=DEFAULT_UNASSIGNED
    )
    finalize_parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "prepare":
            return prepare(args)
        if args.command == "run":
            return run(args)
        return finalize(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
