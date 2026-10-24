#!/usr/bin/env python3
"""Prepare, adjudicate, and freeze the corpus-wide BioKG Claim layer.

The workflow is deliberately split:

1. ``prepare`` creates bounded packets.  Each target's 3--8 findings are seen
   together, plus only structurally nominated cross-target neighbors.
2. ``run`` asks Codex for a structured target-local partition.  It is resumable
   and never writes into the graph.
3. ``finalize`` accepts cross-target hard links only when both target-side
   adjudications nominate one another and share a concrete readout, then writes
   the frozen TSV artifact consumed by deterministic graph rebuilds.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

from ..paths import CLAIM_WORK_DIR, RELEASE_ROOT
from .claim_layer import (
    ASSIGNMENT_FIELDS,
    CLAIM_RELATION_FAMILIES,
    CLAIM_ROLES,
    CONFIDENCE_ORDER,
    DEFAULT_ASSIGNMENTS,
    DEFAULT_LEDGER,
    DEFAULT_RELATIONS,
    EVIDENCE_MODES,
    RELATION_FIELDS,
    RELATIONAL_FAMILIES,
    SUPPORT_ORDER,
    annotate_de_support,
    finding_content_hash,
    normalize_text,
    pipe_join,
    read_ledger,
    split_pipe,
    stable_claim_id,
    validate_assignments,
    validate_relations,
    write_tsv,
)


DEFAULT_WORK = CLAIM_WORK_DIR
ADJUDICATION_VERSION = "claim-group-v1"

RELATION_FAMILIES = CLAIM_RELATION_FAMILIES
SUPPORT_LEVELS = tuple(SUPPORT_ORDER)
RELATED_TYPES = ("QUALIFIES", "CONTRASTS_WITH", "IMPLICATION_OF", "REVIEW_WITH")


def finding_card(row: dict[str, str]) -> dict[str, object]:
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
        "main_caveats": normalize_text(row["main_caveats"]),
        "source_hash": finding_content_hash(row),
    }


def reciprocal_neighbors(rows: list[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    comparator_sets: dict[str, set[str]] = {}
    for row in rows:
        by_target[row["target_gene"].casefold()].append(row)
        comparator_sets[row["doc_id"]] = {value.casefold() for value in split_pipe(row["comparators"])}

    out: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        source_target = row["target_gene"].casefold()
        for comparator in comparator_sets[row["doc_id"]]:
            for other in by_target.get(comparator, []):
                if source_target not in comparator_sets[other["doc_id"]]:
                    continue
                out[row["target_gene"]].append(
                    {
                        "source_doc_id": row["doc_id"],
                        "neighbor": finding_card(other),
                        "candidate_reason": "reciprocal_comparator_mention",
                    }
                )
    # Duplicate neighbor cards add prompt volume but no information.
    for target, candidates in out.items():
        unique = {}
        for candidate in candidates:
            key = (candidate["source_doc_id"], candidate["neighbor"]["doc_id"])
            unique[key] = candidate
        out[target] = [unique[key] for key in sorted(unique)]
    return out


def build_packets(rows: list[dict[str, str]], *, targets_per_packet: int) -> list[dict]:
    by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_target[row["target_gene"]].append(row)
    neighbors = reciprocal_neighbors(rows)
    blocks = []
    for target in sorted(by_target, key=str.casefold):
        findings = sorted(by_target[target], key=lambda row: row["finding_id"])
        blocks.append(
            {
                "target_gene": target,
                "findings": [finding_card(row) for row in findings],
                "cross_target_candidates": neighbors.get(target, []),
            }
        )
    packets = []
    for offset in range(0, len(blocks), targets_per_packet):
        packet_blocks = blocks[offset : offset + targets_per_packet]
        packets.append(
            {
                "packet_id": f"P{len(packets) + 1:04d}",
                "targets": packet_blocks,
            }
        )
    return packets


def output_schema() -> dict:
    member_role = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "doc_id": {"type": "string"},
            "role": {"type": "string", "enum": sorted(CLAIM_ROLES)},
        },
        "required": ["doc_id", "role"],
    }
    related = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "doc_id": {"type": "string"},
            "relation_type": {"type": "string", "enum": list(RELATED_TYPES)},
            "reason": {"type": "string"},
        },
        "required": ["doc_id", "relation_type", "reason"],
    }
    group = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "local_group_id": {"type": "string"},
            "member_roles": {"type": "array", "items": member_role},
            "canonical_summary": {"type": "string"},
            "relation_family": {"type": "string", "enum": list(RELATION_FAMILIES)},
            "direction_pattern": {"type": "string"},
            "evidence_mode": {"type": "string", "enum": list(EVIDENCE_MODES)},
            "support_level": {"type": "string", "enum": list(SUPPORT_LEVELS)},
            "cell_scope": {"type": "array", "items": {"type": "string"}},
            "readouts": {"type": "array", "items": {"type": "string"}},
            "active_default": {"type": "boolean"},
            "confidence": {"type": "string", "enum": ["high", "moderate", "low"]},
            "cross_must_links": {"type": "array", "items": {"type": "string"}},
            "cross_related": {"type": "array", "items": related},
        },
        "required": [
            "local_group_id",
            "member_roles",
            "canonical_summary",
            "relation_family",
            "direction_pattern",
            "evidence_mode",
            "support_level",
            "cell_scope",
            "readouts",
            "active_default",
            "confidence",
            "cross_must_links",
            "cross_related",
        ],
    }
    target = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "target_gene": {"type": "string"},
            "groups": {"type": "array", "items": group},
        },
        "required": ["target_gene", "groups"],
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "packet_id": {"type": "string"},
            "targets": {"type": "array", "items": target},
        },
        "required": ["packet_id", "targets"],
    }


SYSTEM_PROMPT = """You canonicalize findings for a biological knowledge graph.

For each target block, partition ONLY that target's findings into fewer, coarser
Claim groups when they tell the same biological story through different lenses.
The goal is compression, not atomic decomposition. A group may contain a core
result, corroboration, a directly relevant non-phenocopy boundary, and a clinical
or mechanistic implication when they form one coherent narrative.

Do not group findings merely because they share the target, a generic pathway,
or a comparator. Keep distinct readouts/mechanisms separate. Every source finding
must occur exactly once among its target's member_roles. Do not place neighbor
findings in member_roles: cross-target candidates may appear only in
cross_must_links or cross_related.

Use cross_must_links only when the neighbor is clearly a reciprocal restatement
of the SAME canonical story and the two sides share a concrete named readout.
Use cross_related for a meaningful but non-identical relation. Otherwise omit it.

readouts must be concrete genes already present in the supplied finding cards.
Cell scope must use supplied cell labels. canonical_summary is concise biological
prose for a scientist, with no pipeline language or IDs. active_default=false for
standalone null, buffered, or warning-only groups; keep boundary evidence active
when it belongs to an otherwise substantive group.
"""


def prompt_for(packet: dict) -> str:
    return (
        SYSTEM_PROMPT
        + "\nReturn the required JSON object for this packet.\n\n"
        + json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    )


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validate_packet_result(packet: dict, result: dict) -> None:
    """Reject schema-valid responses that omit, duplicate, or invent source findings."""
    if result.get("packet_id") != packet["packet_id"]:
        raise ValueError("packet_id mismatch")
    expected_targets = {block["target_gene"]: block for block in packet["targets"]}
    result_targets = result.get("targets") or []
    names = [item.get("target_gene") for item in result_targets]
    if len(names) != len(set(names)) or set(names) != set(expected_targets):
        raise ValueError(
            f"target partition mismatch: missing={sorted(set(expected_targets) - set(names))} "
            f"extra={sorted(set(names) - set(expected_targets))}"
        )
    for item in result_targets:
        expected_docs = {
            finding["doc_id"] for finding in expected_targets[item["target_gene"]]["findings"]
        }
        actual_docs = [
            member["doc_id"]
            for group in item.get("groups") or []
            for member in group.get("member_roles") or []
        ]
        counts = Counter(actual_docs)
        if set(counts) != expected_docs or any(count != 1 for count in counts.values()):
            raise ValueError(f"finding partition mismatch for {item['target_gene']}")


def run_packet(
    packet: dict,
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
    out = results_dir / f"{packet_id}.json"
    log = results_dir / f"{packet_id}.log"
    parsed = None
    if out.exists() and not overwrite:
        try:
            parsed = json.loads(out.read_text(encoding="utf-8"))
            validate_packet_result(packet, parsed)
            return packet_id, True, "cached"
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    retry_dir = results_dir / "retries"
    retry_dir.mkdir(exist_ok=True)

    def invoke(request: dict, output: Path, output_log: Path) -> dict:
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
                input=prompt_for(request),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
                check=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            output_log.write_text(str(exc.stdout or ""), encoding="utf-8")
            raise RuntimeError(f"codex timeout after {timeout_seconds}s") from exc
        output_log.write_text(completed.stdout or "", encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError(f"codex exit {completed.returncode}")
        try:
            return json.loads(output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"invalid JSON: {exc}") from exc

    def valid_target_results(request: dict, response: dict | None) -> dict[str, dict]:
        if not response:
            return {}
        expected = {block["target_gene"]: block for block in request["targets"]}
        valid = {}
        for item in response.get("targets") or []:
            target = item.get("target_gene")
            if target not in expected or target in valid:
                continue
            expected_docs = {finding["doc_id"] for finding in expected[target]["findings"]}
            actual_docs = [
                member["doc_id"]
                for group in item.get("groups") or []
                for member in group.get("member_roles") or []
            ]
            counts = Counter(actual_docs)
            if set(counts) == expected_docs and all(count == 1 for count in counts.values()):
                valid[target] = item
        return valid

    def repair(request: dict, response: dict | None, prefix: str, depth: int = 0) -> list[dict]:
        valid = valid_target_results(request, response)
        missing = [block for block in request["targets"] if block["target_gene"] not in valid]
        if not missing:
            return [valid[block["target_gene"]] for block in request["targets"]]
        if depth >= 3:
            raise RuntimeError(
                f"incomplete target adjudication after retries: "
                f"{[block['target_gene'] for block in missing]}"
            )
        chunk_size = 3 if len(missing) > 3 else 1
        for offset in range(0, len(missing), chunk_size):
            blocks = missing[offset : offset + chunk_size]
            retry_id = f"{prefix}_R{offset // chunk_size + 1:02d}"
            retry_packet = {"packet_id": retry_id, "targets": blocks}
            retry_out = retry_dir / f"{retry_id}.json"
            retry_log = retry_dir / f"{retry_id}.log"
            retry_response = None
            if retry_out.exists() and not overwrite:
                try:
                    retry_response = json.loads(retry_out.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    retry_response = None
            if not valid_target_results(retry_packet, retry_response):
                retry_response = invoke(retry_packet, retry_out, retry_log)
            repaired = repair(retry_packet, retry_response, retry_id, depth + 1)
            valid.update({item["target_gene"]: item for item in repaired})
        return [valid[block["target_gene"]] for block in request["targets"]]

    try:
        if parsed is None or overwrite:
            parsed = invoke(packet, out, log)
        parsed = {"packet_id": packet_id, "targets": repair(packet, parsed, packet_id)}
        out.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    except RuntimeError as exc:
        return packet_id, False, str(exc)
    try:
        validate_packet_result(packet, parsed)
    except ValueError as exc:
        return packet_id, False, str(exc)
    return packet_id, True, "completed"


def load_results(packets: list[dict], results_dir: Path) -> dict[str, dict]:
    out = {}
    for packet in packets:
        packet_id = packet["packet_id"]
        path = results_dir / f"{packet_id}.json"
        if not path.exists():
            raise ValueError(f"missing adjudication result {path}")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result.get("packet_id") != packet_id:
            raise ValueError(f"packet_id mismatch in {path}")
        out[packet_id] = result
    return out


def validate_and_collect_local_groups(
    packets: list[dict], results: dict[str, dict]
) -> tuple[list[dict], dict[str, str], list[dict]]:
    local_groups: list[dict] = []
    doc_to_local: dict[str, str] = {}
    dropped_nominations: list[dict] = []
    for packet in packets:
        expected_targets = {block["target_gene"]: block for block in packet["targets"]}
        result_targets = results[packet["packet_id"]].get("targets") or []
        if {item.get("target_gene") for item in result_targets} != set(expected_targets):
            raise ValueError(f"target coverage mismatch in {packet['packet_id']}")
        for result_target in result_targets:
            target = result_target["target_gene"]
            block = expected_targets[target]
            expected_docs = {item["doc_id"]: item for item in block["findings"]}
            allowed_neighbors = {
                candidate["neighbor"]["doc_id"] for candidate in block["cross_target_candidates"]
            }
            seen_docs: list[str] = []
            for index, group in enumerate(result_target.get("groups") or [], 1):
                local_id = f"local:{target}:{group.get('local_group_id') or index}"
                member_roles = group.get("member_roles") or []
                members = [item["doc_id"] for item in member_roles]
                if not members:
                    raise ValueError(f"empty local Claim group {local_id}")
                if any(doc_id not in expected_docs for doc_id in members):
                    raise ValueError(f"foreign finding in {local_id}")
                if any(item.get("role") not in CLAIM_ROLES for item in member_roles):
                    raise ValueError(f"invalid member role in {local_id}")
                seen_docs.extend(members)
                union_genes = {
                    gene.casefold(): gene
                    for doc_id in members
                    for gene in expected_docs[doc_id].get("genes") or []
                }
                readouts = []
                for gene in group.get("readouts") or []:
                    canonical = union_genes.get(str(gene).casefold())
                    if canonical and canonical.casefold() != target.casefold():
                        readouts.append(canonical)
                allowed_cells = {
                    cell
                    for doc_id in members
                    for cell in expected_docs[doc_id].get("cell_types") or []
                }
                cells = [cell for cell in group.get("cell_scope") or [] if cell in allowed_cells]
                cross_must = []
                for doc_id in dict.fromkeys(group.get("cross_must_links") or []):
                    if doc_id not in allowed_neighbors:
                        dropped_nominations.append(
                            {
                                "source_local": local_id,
                                "doc_id": doc_id,
                                "link_kind": "must",
                                "reason": "neighbor_not_supplied",
                            }
                        )
                        continue
                    cross_must.append(doc_id)
                related = []
                for item in group.get("cross_related") or []:
                    if item.get("doc_id") not in allowed_neighbors:
                        dropped_nominations.append(
                            {
                                "source_local": local_id,
                                "link_kind": "soft",
                                "reason": "neighbor_not_supplied",
                                **item,
                            }
                        )
                        continue
                    if item.get("relation_type") not in RELATED_TYPES:
                        raise ValueError(f"invalid cross_related relation in {local_id}")
                    related.append(item)
                relation_family = group.get("relation_family")
                if relation_family not in RELATION_FAMILIES:
                    raise ValueError(f"invalid relation_family in {local_id}")
                confidence = group.get("confidence")
                if confidence not in CONFIDENCE_ORDER:
                    raise ValueError(f"invalid confidence in {local_id}")
                local = {
                    "local_id": local_id,
                    "target": target,
                    "members": members,
                    "roles": {item["doc_id"]: item["role"] for item in member_roles},
                    "canonical_summary": normalize_text(group.get("canonical_summary")),
                    "relation_family": relation_family,
                    "direction_pattern": normalize_text(group.get("direction_pattern")),
                    "evidence_mode": group.get("evidence_mode"),
                    "support_level": group.get("support_level"),
                    "cell_scope": cells,
                    "readouts": list(dict.fromkeys(readouts)),
                    "active_default": bool(group.get("active_default")),
                    "confidence": confidence,
                    "cross_must_links": cross_must,
                    "cross_related": related,
                }
                if not local["canonical_summary"]:
                    raise ValueError(f"empty canonical_summary in {local_id}")
                local_groups.append(local)
                for doc_id in members:
                    if doc_id in doc_to_local:
                        raise ValueError(f"finding appears in multiple local groups: {doc_id}")
                    doc_to_local[doc_id] = local_id
            if sorted(seen_docs) != sorted(expected_docs):
                raise ValueError(f"finding partition mismatch for target {target}")
    return local_groups, doc_to_local, dropped_nominations


class DisjointSet:
    def __init__(self, values: Iterable[str]):
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def finalize_claims(
    ledger_rows: list[dict[str, str]], local_groups: list[dict], doc_to_local: dict[str, str]
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict]:
    by_local = {group["local_id"]: group for group in local_groups}
    nominations: set[tuple[str, str]] = set()
    merge_compatible_soft: set[tuple[str, str]] = set()
    for group in local_groups:
        for neighbor_doc in group["cross_must_links"]:
            other = doc_to_local.get(neighbor_doc)
            if other and other != group["local_id"]:
                nominations.add((group["local_id"], other))
        for item in group["cross_related"]:
            other = doc_to_local.get(item["doc_id"])
            if (
                other
                and other != group["local_id"]
                and item["relation_type"] in {"QUALIFIES", "IMPLICATION_OF"}
            ):
                merge_compatible_soft.add((group["local_id"], other))

    dsu = DisjointSet(by_local)
    component_readouts = {
        local_id: {gene.casefold() for gene in group["readouts"]}
        for local_id, group in by_local.items()
    }
    accepted_edges = []
    downgraded_edges = []
    reciprocal_pairs = {
        tuple(sorted((left, right)))
        for left, right in nominations
        if (right, left) in nominations or (right, left) in merge_compatible_soft
    }
    one_sided_edges = [
        (left, right, "one-sided semantic nomination")
        for left, right in sorted(nominations)
        if tuple(sorted((left, right))) not in reciprocal_pairs
    ]
    for left, right in sorted(reciprocal_pairs):
        shared = component_readouts[left] & component_readouts[right]
        if not shared:
            downgraded_edges.append((left, right, "no shared concrete readout"))
            continue
        left_cells = set(by_local[left]["cell_scope"])
        right_cells = set(by_local[right]["cell_scope"])
        if left_cells and right_cells and not (left_cells & right_cells):
            downgraded_edges.append((left, right, "disjoint cell scope"))
            continue
        root_left, root_right = dsu.find(left), dsu.find(right)
        if root_left == root_right:
            continue
        members_left = [key for key in by_local if dsu.find(key) == root_left]
        members_right = [key for key in by_local if dsu.find(key) == root_right]
        common_left = set.intersection(*(component_readouts[key] for key in members_left))
        common_right = set.intersection(*(component_readouts[key] for key in members_right))
        if not (common_left & common_right):
            downgraded_edges.append((left, right, "would create a transitive bridge"))
            continue
        dsu.union(left, right)
        accepted_edges.append((left, right, sorted(shared)))

    components: dict[str, list[dict]] = defaultdict(list)
    for local_id, group in by_local.items():
        components[dsu.find(local_id)].append(group)

    ledger_by_doc = {row["doc_id"]: row for row in ledger_rows}
    assignments: list[dict[str, object]] = []
    local_to_claim: dict[str, str] = {}
    for groups in components.values():
        members = sorted(
            {doc_id for group in groups for doc_id in group["members"]}, key=str.casefold
        )
        claim_id = stable_claim_id(members)
        for group in groups:
            local_to_claim[group["local_id"]] = claim_id
        representative = max(
            groups,
            key=lambda group: (
                CONFIDENCE_ORDER[group["confidence"]],
                len(group["members"]),
                len(group["canonical_summary"]),
            ),
        )
        targets = sorted({group["target"] for group in groups}, key=str.casefold)
        readouts = sorted({gene for group in groups for gene in group["readouts"]}, key=str.casefold)
        cells = sorted({cell for group in groups for cell in group["cell_scope"]}, key=str.casefold)
        finding_types = sorted(
            {ledger_by_doc[doc_id]["finding_type"] for doc_id in members}, key=str.casefold
        )
        families = Counter(group["relation_family"] for group in groups)
        relation_family = max(
            families,
            key=lambda family: (
                family in RELATIONAL_FAMILIES,
                families[family],
                family == representative["relation_family"],
            ),
        )
        evidence_modes = list(dict.fromkeys(group["evidence_mode"] for group in groups))
        direction_patterns = list(
            dict.fromkeys(group["direction_pattern"] for group in groups if group["direction_pattern"])
        )
        support_level = max(
            (group["support_level"] for group in groups), key=lambda value: SUPPORT_ORDER[value]
        )
        confidence = min(groups, key=lambda group: CONFIDENCE_ORDER[group["confidence"]])["confidence"]
        source_hashes = {doc_id: finding_content_hash(ledger_by_doc[doc_id]) for doc_id in members}
        for doc_id in members:
            local = by_local[doc_to_local[doc_id]]
            assignments.append(
                {
                    "claim_id": claim_id,
                    "doc_id": doc_id,
                    "member_role": local["roles"][doc_id],
                    "canonical_summary": representative["canonical_summary"],
                    "relation_family": relation_family,
                    "direction_pattern": " / ".join(direction_patterns),
                    "evidence_mode": "mixed" if len(evidence_modes) > 1 else evidence_modes[0],
                    "support_level": support_level,
                    "de_support_level": "unverified" if evidence_modes == ["deg"] else "not_applicable",
                    "de_direction": "",
                    "de_support_count": 0,
                    "cell_scope": pipe_join(cells),
                    "active_default": str(any(group["active_default"] for group in groups)).lower(),
                    "targets": pipe_join(targets),
                    "readouts": pipe_join(readouts),
                    "finding_types": pipe_join(finding_types),
                    "member_count": len(members),
                    "confidence": confidence,
                    "adjudication_version": ADJUDICATION_VERSION,
                    "source_hash": source_hashes[doc_id],
                }
            )

    relations: list[dict[str, object]] = []
    relation_seen = set()
    for group in local_groups:
        source_claim = local_to_claim[group["local_id"]]
        for item in group["cross_related"]:
            target_local = doc_to_local.get(item["doc_id"])
            if not target_local:
                continue
            target_claim = local_to_claim[target_local]
            if source_claim == target_claim:
                continue
            key = (source_claim, target_claim, item["relation_type"])
            if key in relation_seen:
                continue
            relation_seen.add(key)
            relations.append(
                {
                    "source_claim_id": source_claim,
                    "target_claim_id": target_claim,
                    "relation_type": item["relation_type"],
                    "confidence": group["confidence"],
                    "reason": normalize_text(item["reason"]),
                    "adjudication_version": ADJUDICATION_VERSION,
                }
            )
    for left, right, reason in [*downgraded_edges, *one_sided_edges]:
        source_claim, target_claim = local_to_claim[left], local_to_claim[right]
        key = (source_claim, target_claim, "REVIEW_WITH")
        if source_claim != target_claim and key not in relation_seen:
            relation_seen.add(key)
            relations.append(
                {
                    "source_claim_id": source_claim,
                    "target_claim_id": target_claim,
                    "relation_type": "REVIEW_WITH",
                    "confidence": "moderate",
                    "reason": reason,
                    "adjudication_version": ADJUDICATION_VERSION,
                }
            )

    assignments.sort(key=lambda row: (row["claim_id"], row["doc_id"].casefold()))
    relations.sort(
        key=lambda row: (row["source_claim_id"], row["relation_type"], row["target_claim_id"])
    )
    metrics = validate_assignments(assignments, ledger_rows)
    validate_relations(relations, {str(row["claim_id"]) for row in assignments})
    metrics["accepted_cross_links"] = len(accepted_edges)
    metrics["downgraded_cross_links"] = len(downgraded_edges)
    metrics["one_sided_cross_links"] = len(one_sided_edges)
    return assignments, relations, metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="write bounded adjudication packets and schema")
    prepare.add_argument("--targets-per-packet", type=int, default=12)

    run = sub.add_parser("run", help="run resumable Codex adjudication over prepared packets")
    run.add_argument("--model", default="gpt-rosalind-5.5")
    run.add_argument("--reasoning-effort", default="low")
    run.add_argument("--workers", type=int, default=4)
    run.add_argument("--timeout-seconds", type=int, default=900)
    run.add_argument("--limit", type=int, default=0)
    run.add_argument("--codex", default="codex")
    run.add_argument("--overwrite", action="store_true")

    finalize = sub.add_parser("finalize", help="validate results and freeze Claim assignments")
    finalize.add_argument("--out", type=Path, default=DEFAULT_ASSIGNMENTS)
    finalize.add_argument("--relations-out", type=Path, default=DEFAULT_RELATIONS)
    configured_de_parquet = os.environ.get("BIOKG_DE_PARQUET")
    finalize.add_argument(
        "--de-parquet",
        type=Path,
        default=(
            Path(configured_de_parquet).expanduser()
            if configured_de_parquet
            else None
        ),
        help=(
            "Raw DE parquet used for independent Claim support checks; required "
            "unless --skip-de-verification (or set BIOKG_DE_PARQUET)"
        ),
    )
    finalize.add_argument("--skip-de-verification", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_ledger(args.ledger)
    packets_path = args.work_dir / "packets.jsonl"
    schema_path = args.work_dir / "response_schema.json"
    manifest_path = args.work_dir / "manifest.json"
    results_dir = args.work_dir / "results"

    if args.command == "prepare":
        packets = build_packets(rows, targets_per_packet=max(1, args.targets_per_packet))
        write_jsonl(packets_path, packets)
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        schema_path.write_text(json.dumps(output_schema(), indent=2), encoding="utf-8")
        try:
            ledger_name = str(args.ledger.resolve().relative_to(RELEASE_ROOT))
        except ValueError:
            ledger_name = str(args.ledger)
        manifest_path.write_text(
            json.dumps(
                {
                    "adjudication_version": ADJUDICATION_VERSION,
                    "ledger": ledger_name,
                    "ledger_sha256": hashlib.sha256(args.ledger.read_bytes()).hexdigest(),
                    "findings": len(rows),
                    "targets": len({row["target_gene"] for row in rows}),
                    "targets_per_packet": max(1, args.targets_per_packet),
                    "packets": len(packets),
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "findings": len(rows),
                    "targets": len({row["target_gene"] for row in rows}),
                    "packets": len(packets),
                    "packets_path": str(packets_path),
                    "schema_path": str(schema_path),
                },
                indent=2,
            )
        )
        return

    if not packets_path.exists() or not schema_path.exists():
        raise SystemExit(f"run prepare first; missing {packets_path} or {schema_path}")
    packets = read_jsonl(packets_path)

    if args.command == "run":
        results_dir.mkdir(parents=True, exist_ok=True)
        manifest = (
            json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest_path.exists()
            else {"adjudication_version": ADJUDICATION_VERSION}
        )
        manifest["model"] = args.model
        manifest["reasoning_effort"] = args.reasoning_effort
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
        )
        lock_path = args.work_dir / ".run.lock"
        with lock_path.open("w", encoding="utf-8") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise SystemExit(
                    f"another Claim adjudication is already running for {args.work_dir}"
                ) from exc
            lock.write(f"pid={os.getpid()}\n")
            lock.flush()
            pending = packets[: args.limit] if args.limit else packets
            outcomes = []
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
                    packet_id, ok, status = future.result()
                    outcomes.append((packet_id, ok, status))
                    print(f"{packet_id}: {status}", flush=True)
        failures = [item for item in outcomes if not item[1]]
        print(json.dumps({"attempted": len(outcomes), "failed": failures}, indent=2))
        if failures:
            raise SystemExit(1)
        return

    results = load_results(packets, results_dir)
    local_groups, doc_to_local, dropped_links = validate_and_collect_local_groups(
        packets, results
    )
    assignments, relations, metrics = finalize_claims(rows, local_groups, doc_to_local)
    dropped_counts = Counter(item["link_kind"] for item in dropped_links)
    metrics["dropped_invalid_hard_links"] = dropped_counts["must"]
    metrics["dropped_invalid_soft_links"] = dropped_counts["soft"]
    (args.work_dir / "dropped_links.json").write_text(
        json.dumps(dropped_links, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    if not args.skip_de_verification:
        if args.de_parquet is None:
            raise SystemExit(
                "--de-parquet is required unless --skip-de-verification is set "
                "(or set BIOKG_DE_PARQUET)"
            )
        metrics.update(annotate_de_support(assignments, args.de_parquet))
        metrics.update(validate_assignments(assignments, rows))
    if manifest_path.exists():
        metrics["provenance"] = json.loads(manifest_path.read_text(encoding="utf-8"))
    write_tsv(args.out, assignments, ASSIGNMENT_FIELDS)
    write_tsv(args.relations_out, relations, RELATION_FIELDS)
    summary_path = args.out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
