#!/usr/bin/env python3
"""Validate a grounded DistributedAgents orchestrator task plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
# .../src/distributed_agents/skills/runtime/dataset-orchestrator-skill/scripts
#     [5]  [4]       [3]    [2]       [1]                       [0]
# Find `distributed_agents` the same way we find `profile_task`, so the script runs
# wherever it is invoked from. Requiring the caller to export PYTHONPATH cost a
# routing agent five commands and a fabricated stub module.
_SRC = SCRIPT_DIR.parents[5]
if (_SRC / "distributed_agents" / "__init__.py").is_file() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from distributed_agents.query.context import (  # noqa: E402
    DATASET_CONTEXT_SCHEMA_VERSION,
    load_dataset_context_manifest,
)
from profile_task import (  # noqa: E402
    SCHEMA_VERSION as PROFILE_VERSION,
    normalize_execution_plan,
    validate_profile,
)

PLAN_VERSION = "distributed_agents-task-plan-v4"
REQUIRED_FIELDS = (
    "schema_version",
    "task_class",
    "classification_rationale",
    "endpoint_definition",
    "schema_relation",
    "claim_strategy",
    "output_contract",
    "candidate_universe",
    "corpus_coverage",
    "dataset_context",
    "resource_strategy",
    "evidence_role_resolution",
    "quantitative_basis",
    "claim_attention_policy",
    "external_transfer",
    "candidate_decision_policy",
    "mechanism_model",
    "multi_hop_model",
    "proxy_model",
    "evidence_ledger_policy",
    "output_reduction_policy",
    "evidence_authority",
    "stages",
    "delegation",
    "ranking_policy",
    "termination_condition",
    "validation",
)
ATLAS_DISCOVERY_CLASSES = frozenset({"atlas_discovery"})
DEPRECATED_ATLAS_STAGE_TOKENS = frozenset({"challenger", "critic"})
DATASET_OBSERVABILITY = frozenset(
    {"direct", "proxy", "absent", "unobserved_context", "requires_semantic_review"}
)
LEDGER_ALIGNMENT = frozenset(
    {
        "native",
        "adjacent",
        "incidental",
        "absent",
        "not_required",
        "requires_semantic_review",
    }
)
ANSWER_MODES = frozenset({"direct", "derived", "predicted", "requires_semantic_review"})
COMBINED_SCHEMA_RELATIONS = frozenset(
    {
        "in_schema_dataset_and_ledger",
        "in_schema_dataset_only",
        "in_schema_ledger_only",
        "out_of_schema_orthogonal",
        "out_of_schema_cross_context",
        "requires_semantic_review",
    }
)
CORPUS_COVERAGE_STATUS = frozenset({"complete", "partial", "unknown", "not_required"})
ABSENCE_SEMANTICS = frozenset(
    {"explicit_negative_only", "no_negative_inference", "not_required"}
)
EXTERNAL_GROUNDING_POLICIES = frozenset(
    {
        "reuse_only",
        "selective_gap_fill",
        "endpoint_prior_search",
        "role_resolved_external",
        "not_required",
    }
)
PREDICTED_STAGE_KINDS = frozenset(
    {
        "quantitative_basis",
        "endpoint_capability",
        "claim_attention",
        "corpus_slice_plan",
        "corpus_slice_read",
        "score_blind_interpretation",
        "mechanism_expansion",
        "role_aware_audit",
        "global_reduction",
        "assembly",
        "other",
    }
)
#: A scoped execution can halt between basis materialization and downstream review, so
#: the required-stage set depends on which invocation is being validated. An
#: absent ``execution_scope`` means the historical whole-plan artifact shape,
#: whose required set is unchanged.
EXECUTION_STAGES = frozenset({"full", "basis", "downstream"})
DEFAULT_EXECUTION_SCOPE = {
    "downstream_family": "quantitative",
    "stage": "full",
}


def _execution_scope(plan: dict[str, object]) -> dict[str, str]:
    """Read execution scope, defaulting to the historical whole-plan view."""

    declared = plan.get("execution_scope")
    if not isinstance(declared, dict):
        return dict(DEFAULT_EXECUTION_SCOPE)
    family = str(
        declared.get("downstream_family") or DEFAULT_EXECUTION_SCOPE["downstream_family"]
    ).strip()
    stage = str(declared.get("stage") or DEFAULT_EXECUTION_SCOPE["stage"]).strip()
    if family not in {"quantitative", "corpus_aggregation"}:
        _fail(f"unsupported execution_scope.downstream_family: {family!r}")
    if stage not in EXECUTION_STAGES:
        _fail(f"unsupported execution_scope.stage: {stage!r}")
    return {"downstream_family": family, "stage": stage}


def _is_scoped(plan: dict[str, object]) -> bool:
    """Whether the plan declares an explicit partial-execution scope.

    Scoped runs materialize the corpus themselves, downstream of a frozen basis
    and host-side. Legacy runs hand a recalled Claim pool to an in-context
    coordinator. The two differ in *when* the corpus is read, so several
    invariants below invert between them.
    """

    return isinstance(plan.get("execution_scope"), dict)


def _fail(message: str) -> None:
    raise ValueError(message)


def _nested_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _nested_strings(item)


def _validate_no_dynamic_install(value: object) -> None:
    text = "\n".join(_nested_strings(value)).casefold()
    forbidden = (
        "pip install",
        "uv add",
        "pixi add",
        "conda install",
        "npm install",
        "install skill",
        "install plugin",
        "dynamic executable",
    )
    matches = [token for token in forbidden if token in text]
    if matches:
        _fail(
            "resource_strategy may acquire versioned data only; dynamic "
            f"code/skill installation is forbidden: {matches}"
        )


def _validate_dataset_context(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        _fail("dataset_context must be an object")
    manifest_value = str(value.get("manifest_path") or "").strip()
    if not manifest_value:
        _fail("dataset_context requires manifest_path")
    manifest_path = Path(manifest_value).expanduser().resolve()
    try:
        manifest = load_dataset_context_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        _fail(f"invalid dataset_context manifest: {exc}")
    if manifest["schema_version"] != DATASET_CONTEXT_SCHEMA_VERSION:
        _fail("dataset_context manifest schema mismatch")

    overrides = value.get("task_specific_overrides")
    if not isinstance(overrides, list):
        _fail("dataset_context.task_specific_overrides must be a list")
    for index, override in enumerate(overrides):
        if not isinstance(override, dict):
            _fail(f"dataset context override {index} must be an object")
        if not str(override.get("source") or "").strip():
            _fail(f"dataset context override {index} requires source")
        if not str(override.get("instruction") or "").strip():
            _fail(f"dataset context override {index} requires instruction")
    return {
        "manifest_path": str(manifest_path),
        "snapshot_path": manifest["snapshot_path"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "task_specific_overrides": len(overrides),
    }


def _validate_schema_relation(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        _fail("schema_relation must be an object")
    required = (
        "dataset_observability",
        "ledger_alignment",
        "answer_mode",
        "combined",
        "rationale",
    )
    missing = [field for field in required if not str(value.get(field) or "").strip()]
    if missing:
        _fail(f"schema_relation lacks required fields: {missing}")
    relation = {field: str(value[field]).strip() for field in required}
    if relation["dataset_observability"] not in DATASET_OBSERVABILITY:
        _fail(
            "unsupported schema_relation.dataset_observability: "
            f"{relation['dataset_observability']!r}"
        )
    if relation["ledger_alignment"] not in LEDGER_ALIGNMENT:
        _fail(
            "unsupported schema_relation.ledger_alignment: "
            f"{relation['ledger_alignment']!r}"
        )
    if relation["answer_mode"] not in ANSWER_MODES:
        _fail(f"unsupported schema_relation.answer_mode: {relation['answer_mode']!r}")
    if relation["combined"] not in COMBINED_SCHEMA_RELATIONS:
        _fail(f"unsupported schema_relation.combined: {relation['combined']!r}")
    combined = relation["combined"]
    dataset = relation["dataset_observability"]
    ledger = relation["ledger_alignment"]
    answer = relation["answer_mode"]
    if combined == "in_schema_dataset_and_ledger" and not (
        dataset in {"direct", "proxy"}
        and ledger in {"native", "adjacent"}
        and answer in {"direct", "derived"}
    ):
        _fail("in_schema_dataset_and_ledger has inconsistent layer values")
    if combined == "in_schema_dataset_only" and not (
        dataset in {"direct", "proxy"}
        and ledger in {"not_required", "absent", "incidental"}
        and answer in {"direct", "derived"}
    ):
        _fail("in_schema_dataset_only has inconsistent layer values")
    if combined == "in_schema_ledger_only" and not (
        ledger == "native" and answer in {"direct", "derived"}
    ):
        _fail("in_schema_ledger_only has inconsistent layer values")
    if combined == "out_of_schema_orthogonal" and not (
        dataset == "absent"
        and ledger in {"incidental", "absent", "adjacent"}
        and answer == "predicted"
    ):
        _fail("out_of_schema_orthogonal has inconsistent layer values")
    if combined == "out_of_schema_cross_context" and not (
        dataset == "unobserved_context"
        and ledger in {"incidental", "absent", "adjacent"}
        and answer == "predicted"
    ):
        _fail("out_of_schema_cross_context has inconsistent layer values")
    return relation


def _validate_corpus_coverage(
    value: object,
    relation: dict[str, str],
    external_role: str,
) -> dict[str, str]:
    if not isinstance(value, dict):
        _fail("corpus_coverage must be an object")
    required = (
        "ledger_alignment",
        "coverage_status",
        "absence_semantics",
        "external_grounding_policy",
    )
    missing = [field for field in required if not str(value.get(field) or "").strip()]
    if missing:
        _fail(f"corpus_coverage lacks required fields: {missing}")
    coverage = {field: str(value[field]).strip() for field in required}
    if coverage["ledger_alignment"] not in LEDGER_ALIGNMENT:
        _fail(
            "unsupported corpus_coverage.ledger_alignment: "
            f"{coverage['ledger_alignment']!r}"
        )
    if coverage["coverage_status"] not in CORPUS_COVERAGE_STATUS:
        _fail(
            "unsupported corpus_coverage.coverage_status: "
            f"{coverage['coverage_status']!r}"
        )
    if coverage["absence_semantics"] not in ABSENCE_SEMANTICS:
        _fail(
            "unsupported corpus_coverage.absence_semantics: "
            f"{coverage['absence_semantics']!r}"
        )
    if coverage["external_grounding_policy"] not in EXTERNAL_GROUNDING_POLICIES:
        _fail(
            "unsupported corpus_coverage.external_grounding_policy: "
            f"{coverage['external_grounding_policy']!r}"
        )
    if coverage["ledger_alignment"] != relation["ledger_alignment"]:
        _fail(
            "corpus_coverage.ledger_alignment must match "
            "schema_relation.ledger_alignment"
        )
    if (
        relation["combined"] == "in_schema_dataset_and_ledger"
        and coverage["external_grounding_policy"] == "endpoint_prior_search"
    ):
        _fail(
            "in-schema dataset+ledger tasks must reuse corpus grounding and may "
            "only perform selective gap filling, not blanket endpoint-prior search"
        )
    if external_role == "quantitative_anchor" and (
        coverage["external_grounding_policy"] != "endpoint_prior_search"
    ):
        _fail("an external quantitative anchor requires endpoint_prior_search")
    if external_role != "quantitative_anchor" and (
        coverage["external_grounding_policy"] == "endpoint_prior_search"
    ):
        _fail("endpoint_prior_search is reserved for an external quantitative anchor")
    return coverage


def _artifact_name(value: object, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        _fail(f"{label} must be non-empty")
    return Path(text).name


def _stage_artifact_names(stage: dict[str, object], field: str) -> set[str]:
    values = stage.get(field)
    if not isinstance(values, list):
        return set()
    return {Path(str(value)).name for value in values if str(value or "").strip()}


def _validate_predicted_execution_order(
    *,
    plan: dict[str, object],
    relation: dict[str, str],
    stages: list[dict[str, object]],
) -> dict[str, object]:
    if relation["answer_mode"] != "predicted":
        return {"required": False}

    roles = plan.get("evidence_role_resolution")
    if not isinstance(roles, dict):
        _fail("predicted task evidence_role_resolution must be an object")
    external = roles.get("external_evidence")
    external_role = (
        str(external.get("role") or "").strip() if isinstance(external, dict) else ""
    )
    external_anchor = external_role == "quantitative_anchor"

    basis = plan.get("quantitative_basis")
    if not isinstance(basis, dict):
        _fail("predicted task quantitative_basis must be an object")
    basis_kind = str(basis.get("kind") or "").strip()
    scope = _execution_scope(plan)
    scoped = _is_scoped(plan)
    corpus_family = scope["downstream_family"] == "corpus_aggregation"
    produces_basis = scope["stage"] in {"full", "basis"}
    produces_downstream = scope["stage"] in {"full", "downstream"}

    basis_artifacts = basis.get("artifacts")
    if not isinstance(basis_artifacts, dict):
        _fail("predicted task quantitative_basis.artifacts must be an object")
    # A corpus substrate has no candidate scalar, so its "basis" artifact is the
    # slice plan that says which corpus units each reader owns.
    basis_artifact_field = "corpus_slice_plan" if corpus_family else "base"
    required_basis_artifacts = {
        "base": _artifact_name(
            basis_artifacts.get(basis_artifact_field),
            f"quantitative_basis.artifacts.{basis_artifact_field}",
        ),
        "coverage_audit": _artifact_name(
            basis_artifacts.get("coverage_audit"),
            "quantitative_basis.artifacts.coverage_audit",
        ),
    }

    required_external_artifacts: dict[str, str] = {}
    if external_anchor:
        resources = plan.get("resource_strategy")
        discovery = (
            resources.get("external_discovery") if isinstance(resources, dict) else None
        )
        discovery_artifacts = (
            discovery.get("artifacts") if isinstance(discovery, dict) else None
        )
        if not isinstance(discovery_artifacts, dict):
            _fail(
                "external quantitative anchor requires "
                "resource_strategy.external_discovery.artifacts"
            )
        required_external_artifacts = {
            field: _artifact_name(
                discovery_artifacts.get(field),
                f"resource_strategy.external_discovery.artifacts.{field}",
            )
            for field in ("resource_manifest", "candidate_prior", "coverage_audit")
        }

    reduction = plan.get("output_reduction_policy")
    if not isinstance(reduction, dict):
        _fail("predicted task output_reduction_policy must be an object")
    reduction_artifacts = reduction.get("artifacts")
    if not isinstance(reduction_artifacts, dict):
        _fail("predicted task output_reduction_policy.artifacts must be an object")
    required_reduction_artifacts = {
        "candidate_evidence_ledger": _artifact_name(
            reduction_artifacts.get("candidate_evidence_ledger"),
            "output_reduction_policy.artifacts.candidate_evidence_ledger",
        ),
        "candidate_decisions": _artifact_name(
            reduction_artifacts.get("candidate_decisions"),
            "output_reduction_policy.artifacts.candidate_decisions",
        ),
        "global_ranking_audit": _artifact_name(
            reduction_artifacts.get("global_ranking_audit"),
            "output_reduction_policy.artifacts.global_ranking_audit",
        ),
    }
    proxy = plan.get("proxy_model")
    proxy_required = isinstance(proxy, dict) and bool(proxy.get("required"))
    if proxy_required:
        required_reduction_artifacts["proxy_independence_audit"] = _artifact_name(
            reduction_artifacts.get("proxy_independence_audit"),
            "output_reduction_policy.artifacts.proxy_independence_audit",
        )

    attention_policy = plan.get("claim_attention_policy")
    if not isinstance(attention_policy, dict):
        _fail("predicted task claim_attention_policy must be an object")
    expansion_mode = str(attention_policy.get("expansion_mode") or "").strip()
    attention_artifacts = attention_policy.get("artifacts")
    if not isinstance(attention_artifacts, dict):
        _fail("predicted task claim_attention_policy.artifacts must be an object")

    kinds: dict[str, list[int]] = {}
    for index, stage in enumerate(stages):
        kind = str(stage.get("stage_kind") or "").strip()
        if kind not in PREDICTED_STAGE_KINDS:
            _fail(
                f"predicted stage {index} requires a supported stage_kind; "
                f"observed {kind!r}"
            )
        kinds.setdefault(kind, []).append(index)

    if corpus_family:
        basis_stage_kind = "corpus_slice_plan"
        interpretation_stage_kind = "corpus_slice_read"
    else:
        basis_stage_kind = (
            "endpoint_capability" if external_anchor else "quantitative_basis"
        )
        interpretation_stage_kind = "score_blind_interpretation"
    required_kinds: list[str] = []
    if produces_basis:
        required_kinds.append(basis_stage_kind)
    if produces_downstream:
        required_kinds.extend(
            (interpretation_stage_kind, "global_reduction", "assembly")
        )
    for required_kind in required_kinds:
        if required_kind not in kinds:
            _fail(
                f"predicted {scope['downstream_family']} task at stage "
                f"{scope['stage']!r} requires a {required_kind} stage"
            )
    forbidden_kinds = [
        kind
        for kind in (
            (basis_stage_kind,) if not produces_basis else ()
        )
        if kind in kinds
    ]
    if forbidden_kinds:
        _fail(
            f"stage {scope['stage']!r} must not re-run the basis: {forbidden_kinds}"
        )
    uses_claim_attention = expansion_mode == "weighted_one_hop"
    if uses_claim_attention and produces_downstream and "claim_attention" not in kinds:
        _fail("weighted Claim expansion requires a claim_attention stage")
    if not uses_claim_attention and "claim_attention" in kinds:
        _fail(
            "claim_attention stage is forbidden when expansion_mode=none; "
            "weak or unranked starting sets must not generate related candidates"
        )
    if proxy_required and produces_downstream and "role_aware_audit" not in kinds:
        _fail("predicted task with a proxy requires a role_aware_audit stage")

    basis_index: int | None = None
    if produces_basis:
        basis_index = kinds[basis_stage_kind][0]
        basis_outputs = _stage_artifact_names(stages[basis_index], "outputs")
        required_basis_outputs = set(required_basis_artifacts.values())
        if external_anchor:
            required_basis_outputs.add(required_external_artifacts["resource_manifest"])
        missing_basis = sorted(required_basis_outputs - basis_outputs)
        if missing_basis:
            _fail(
                f"{basis_stage_kind} stage does not produce the declared quantitative "
                f"basis artifacts: {missing_basis}"
            )
    if not produces_downstream:
        # The basis invocation halts here: everything below describes work a
        # separate process with a fresh context performs.
        return {
            "required": True,
            "execution_scope": scope,
            "quantitative_basis_kind": basis_kind,
            "quantitative_basis_stage": basis_index,
            "external_quantitative_anchor": external_anchor,
            "claim_attention_required": uses_claim_attention,
            "claim_expansion_mode": expansion_mode,
            "score_blind_interpretation_stage": None,
            "global_reduction_stage": None,
            "role_aware_audit_stage": None,
            "declared_artifacts": dict(required_basis_artifacts),
        }

    semantic_index = kinds[interpretation_stage_kind][0]
    semantic_inputs = _stage_artifact_names(stages[semantic_index], "inputs")
    if required_basis_artifacts["base"] not in semantic_inputs:
        _fail(
            "candidate interpretation must consume the quantitative starting result"
        )
    semantic_outputs = _stage_artifact_names(stages[semantic_index], "outputs")
    if not semantic_outputs:
        _fail("candidate interpretation must produce complete context cards")

    claim_index: int | None = None
    candidate_summary = ""
    if uses_claim_attention:
        claim_index = kinds["claim_attention"][0]
        claim_inputs = _stage_artifact_names(stages[claim_index], "inputs")
        if scoped:
            # Retained-seed expansion: the graph is grown from the incumbents
            # the audit kept, so the audit's own output is a required input.
            required_claim_inputs = {
                required_basis_artifacts["base"],
                *semantic_outputs,
            }
        else:
            required_claim_inputs = {
                required_basis_artifacts["base"],
                "candidate_claims.csv",
                "claim_routing_edges.tsv",
            }
        missing_claim_inputs = sorted(required_claim_inputs - claim_inputs)
        if missing_claim_inputs:
            _fail(
                "Claim attention must consume the quantitative starting result and "
                + (
                    f"the retained-incumbent audit: {missing_claim_inputs}"
                    if scoped
                    else f"canonical Claim artifacts: {missing_claim_inputs}"
                )
            )
        path_audit = _artifact_name(
            attention_artifacts.get("path_audit"),
            "claim_attention_policy.artifacts.path_audit",
        )
        candidate_summary = _artifact_name(
            attention_artifacts.get("candidate_summary"),
            "claim_attention_policy.artifacts.candidate_summary",
        )
        claim_outputs = _stage_artifact_names(stages[claim_index], "outputs")
        missing_claim_outputs = sorted({path_audit, candidate_summary} - claim_outputs)
        if missing_claim_outputs:
            _fail(
                "claim_attention must produce the declared private path audit "
                f"and related-gene summary: {missing_claim_outputs}"
            )
        if scoped:
            # The audit is deliberately blind to the challengers it opens slots
            # for; only the contested review sees both sides. Enforced below,
            # against the reduction stage rather than the interpretation.
            if candidate_summary in semantic_inputs:
                _fail(
                    "retained-seed expansion runs after the audit, so candidate "
                    "interpretation must not consume the related-gene summary"
                )
        elif candidate_summary not in semantic_inputs:
            _fail(
                "candidate interpretation must consume the related-gene summary"
            )
        if path_audit in semantic_inputs:
            _fail(
                "candidate interpretation must not consume the private Claim-path audit"
            )

    reduction_index = kinds["global_reduction"][0]
    reduction_inputs = _stage_artifact_names(stages[reduction_index], "inputs")
    required_reduction_inputs = {
        required_basis_artifacts["base"],
        *semantic_outputs,
    }
    if scoped and uses_claim_attention:
        # The contested review is the only stage that sees incumbents and
        # challengers together, so it is the one that must consume the pool.
        required_reduction_inputs.add(candidate_summary)
    missing_inputs = sorted(required_reduction_inputs - reduction_inputs)
    if missing_inputs:
        _fail(
            "global reduction must consume the quantitative starting result and "
            f"candidate context cards: {missing_inputs}"
        )
    if uses_claim_attention:
        private_path_audit = _artifact_name(
            attention_artifacts.get("path_audit"),
            "claim_attention_policy.artifacts.path_audit",
        )
        if private_path_audit in reduction_inputs:
            _fail("global_reduction must not consume the private Claim path audit")
    reduction_outputs = _stage_artifact_names(stages[reduction_index], "outputs")
    candidate_ledger = required_reduction_artifacts["candidate_evidence_ledger"]
    candidate_decisions = required_reduction_artifacts["candidate_decisions"]
    missing_reduction_outputs = sorted(
        {candidate_ledger, candidate_decisions} - reduction_outputs
    )
    if missing_reduction_outputs:
        _fail(
            "global reduction must produce the complete candidate evidence table "
            f"and reviewer decisions: {missing_reduction_outputs}"
        )

    evidence_indices = [*kinds.get("mechanism_expansion", [])]
    if basis_index is not None:
        evidence_indices.append(basis_index)
    if claim_index is not None and not scoped:
        evidence_indices.append(claim_index)
    if evidence_indices and max(evidence_indices) >= semantic_index:
        _fail(
            "quantitative basis, Claim expansion, and evidence gathering must "
            "finish before candidate interpretation"
        )
    if semantic_index >= reduction_index:
        _fail("candidate interpretation must finish before global reduction")
    if scoped and claim_index is not None:
        # prune -> reseed -> expand. Seeding the graph from all 100 lets
        # rejected incumbents nominate their own replacements.
        if claim_index <= semantic_index:
            _fail(
                "retained-seed Claim expansion must follow the incumbent audit "
                "that decides which seeds are retained"
            )
        if claim_index >= reduction_index:
            _fail("Claim expansion must finish before global reduction")

    audit_index: int | None = None
    if proxy_required:
        audit_index = kinds["role_aware_audit"][0]
        audit_inputs = _stage_artifact_names(stages[audit_index], "inputs")
        if candidate_ledger not in audit_inputs:
            _fail(
                "role_aware_audit must consume the globally adjudicated "
                "candidate ledger"
            )
        audit_outputs = _stage_artifact_names(stages[audit_index], "outputs")
        proxy_audit = required_reduction_artifacts["proxy_independence_audit"]
        if proxy_audit not in audit_outputs:
            _fail("role_aware_audit must produce the declared proxy-independence audit")
        if reduction_index >= audit_index:
            _fail("role-aware proxy audit must follow global reduction")

    assembly_index = kinds["assembly"][0]
    last_decision_index = audit_index if audit_index is not None else reduction_index
    if last_decision_index >= assembly_index:
        _fail("global adjudication and role-aware audit must finish before assembly")
    assembly_inputs = _stage_artifact_names(stages[assembly_index], "inputs")
    required_assembly_inputs = {
        required_basis_artifacts["base"],
        candidate_decisions,
        *semantic_outputs,
    }
    missing_assembly_inputs = sorted(required_assembly_inputs - assembly_inputs)
    if missing_assembly_inputs:
        _fail(
            "assembly must validate the full reviewer ordering against the "
            f"starting result and context-card union: {missing_assembly_inputs}"
        )
    assembly_outputs = _stage_artifact_names(stages[assembly_index], "outputs")
    global_ranking_audit = required_reduction_artifacts["global_ranking_audit"]
    if global_ranking_audit not in assembly_outputs:
        _fail("assembly must produce the declared global-ranking audit")

    declared_artifacts = {
        **required_basis_artifacts,
        **required_reduction_artifacts,
    }
    if required_external_artifacts:
        declared_artifacts.update(required_external_artifacts)
    return {
        "required": True,
        "execution_scope": scope,
        "quantitative_basis_kind": basis_kind,
        "quantitative_basis_stage": basis_index,
        "external_quantitative_anchor": external_anchor,
        "claim_attention_required": uses_claim_attention,
        "claim_expansion_mode": expansion_mode,
        "score_blind_interpretation_stage": semantic_index,
        "global_reduction_stage": reduction_index,
        "role_aware_audit_stage": audit_index,
        "declared_artifacts": declared_artifacts,
    }


def validate_plan(
    plan: dict[str, object],
    profile: dict[str, object],
    recall: dict[str, object] | None,
) -> dict[str, object]:
    try:
        validated_profile = validate_profile(profile)
    except ValueError as exc:
        _fail(f"invalid resolved task profile: {exc}")
    normalized_fields: list[str] = []
    if _is_scoped(plan):
        normalized = normalize_execution_plan(plan, profile)
        normalized_fields = sorted(
            key for key, value in normalized.items() if plan.get(key) != value
        )
        plan = normalized
    missing = [field for field in REQUIRED_FIELDS if field not in plan]
    if missing:
        _fail(f"task plan lacks required fields: {missing}")
    if plan["schema_version"] != PLAN_VERSION:
        _fail(f"unsupported task-plan schema: {plan['schema_version']!r}")

    if _is_scoped(plan):
        # The semantic profile was validated once above. Reconstructing a second,
        # partial profile from its plan projection is both redundant and the
        # source of corpus-only synchronization failures.
        validated_reasoning = validated_profile
    else:
        # Legacy hand-authored plans may override selected semantic sections.
        # Preserve their compatibility validation until those plans migrate to
        # the compiled scoped-execution contract.
        reasoning_view = {
            "schema_version": PROFILE_VERSION,
            "task_class": plan.get("task_class"),
            "classification_rationale": plan.get("classification_rationale"),
            "endpoint_definition": plan.get("endpoint_definition"),
            "schema_relation": plan.get("schema_relation"),
            "output_contract": plan.get("output_contract"),
            "claim_recall_required": plan.get("claim_strategy") != "none",
            "claim_strategy": plan.get("claim_strategy"),
            "resource_strategy": plan.get("resource_strategy"),
            "evidence_role_resolution": plan.get("evidence_role_resolution"),
            "quantitative_basis": plan.get("quantitative_basis"),
            "claim_attention_policy": plan.get("claim_attention_policy"),
            "external_transfer": plan.get("external_transfer"),
            "candidate_decision_policy": plan.get("candidate_decision_policy"),
            "mechanism_model": plan.get("mechanism_model"),
            "multi_hop_model": plan.get("multi_hop_model"),
            "proxy_model": plan.get("proxy_model"),
            "evidence_ledger_policy": plan.get("evidence_ledger_policy"),
            "output_reduction_policy": plan.get("output_reduction_policy"),
        }
        try:
            validated_reasoning = validate_profile(reasoning_view)
        except ValueError as exc:
            _fail(f"invalid task-plan reasoning sections: {exc}")
    _validate_no_dynamic_install(plan.get("resource_strategy"))

    dataset_context = _validate_dataset_context(plan.get("dataset_context"))
    profile_class = str(profile.get("task_class") or "")
    plan_class = str(plan.get("task_class") or "")
    if (
        profile_class != plan_class
        and not str(plan.get("classification_override_reason") or "").strip()
    ):
        _fail(
            f"task class changed from {profile_class!r} to {plan_class!r} without "
            "classification_override_reason"
        )
    profile_relation_value = profile.get("schema_relation")
    profile_relation = (
        _validate_schema_relation(profile_relation_value)
        if profile_relation_value
        else None
    )
    plan_relation = _validate_schema_relation(plan.get("schema_relation"))
    if (
        profile_relation
        and profile_relation != plan_relation
        and not str(plan.get("schema_relation_override_reason") or "").strip()
    ):
        _fail(
            f"schema relation changed from {profile_relation!r} to "
            f"{plan_relation!r} without schema_relation_override_reason"
        )
    profile_endpoint = profile.get("endpoint_definition")
    if (
        isinstance(profile_endpoint, dict)
        and profile_endpoint != plan.get("endpoint_definition")
        and not str(plan.get("endpoint_override_reason") or "").strip()
    ):
        _fail("endpoint definition changed without endpoint_override_reason")
    profile_strategy = str(profile.get("claim_strategy") or "")
    plan_strategy = str(plan.get("claim_strategy") or "")
    if (
        profile_strategy
        and profile_strategy != plan_strategy
        and not str(plan.get("claim_strategy_override_reason") or "").strip()
    ):
        _fail(
            f"Claim strategy changed from {profile_strategy!r} to "
            f"{plan_strategy!r} without claim_strategy_override_reason"
        )
    for field, override_field in (
        ("evidence_role_resolution", "evidence_role_override_reason"),
        ("quantitative_basis", "quantitative_basis_override_reason"),
        ("claim_attention_policy", "claim_attention_policy_override_reason"),
    ):
        if (
            profile.get(field) != plan.get(field)
            and not str(plan.get(override_field) or "").strip()
        ):
            _fail(f"{field} changed without {override_field}")
    role_resolution = plan.get("evidence_role_resolution")
    external_role_row = (
        role_resolution.get("external_evidence")
        if isinstance(role_resolution, dict)
        else None
    )
    external_role = (
        str(external_role_row.get("role") or "").strip()
        if isinstance(external_role_row, dict)
        else ""
    )
    corpus_coverage = _validate_corpus_coverage(
        plan.get("corpus_coverage"),
        plan_relation,
        external_role,
    )
    output_contract = plan.get("output_contract")
    if not isinstance(output_contract, dict):
        _fail("output_contract must be an object")
    expected_files = set((profile.get("output_contract") or {}).get("deliverables", []))
    planned_files = set(output_contract.get("deliverables", []))
    if expected_files and expected_files != planned_files:
        _fail(
            f"deliverable mismatch: profile={sorted(expected_files)} plan={sorted(planned_files)}"
        )
    stage_values = plan.get("stages")
    if not isinstance(stage_values, list) or not stage_values:
        _fail("stages must be a non-empty ordered list")
    stages: list[dict[str, object]] = []
    stage_ids = []
    for index, stage in enumerate(stage_values):
        if not isinstance(stage, dict):
            _fail(f"stage {index} is not an object")
        absent = [
            field
            for field in ("id", "owner", "inputs", "outputs", "completion_test")
            if field not in stage
        ]
        if absent:
            _fail(f"stage {index} lacks {absent}")
        stages.append(stage)
        stage_ids.append(str(stage["id"]))
    if len(stage_ids) != len(set(stage_ids)):
        _fail("stage IDs are not unique")
    if plan_class in ATLAS_DISCOVERY_CLASSES:
        deprecated = []
        for stage_id in stage_ids:
            normalized = stage_id.casefold().replace("-", "_")
            tokens = set(re.findall(r"[a-z0-9]+", normalized))
            if (
                "cube_sweep" in normalized
                or "raw_cube" in normalized
                or tokens & DEPRECATED_ATLAS_STAGE_TOKENS
            ):
                deprecated.append(stage_id)
        deprecated.sort()
        if deprecated:
            _fail(
                "atlas discovery must use Claim dispositions and the final reranker "
                f"completeness audit instead of deprecated extra stages: {deprecated}"
            )
    predicted_execution = _validate_predicted_execution_order(
        plan=plan,
        relation=plan_relation,
        stages=stages,
    )

    skips_claim_recall = str(plan.get("claim_strategy") or "") == "none"
    claim_section = plan.get("claim_recall")
    if _is_scoped(plan):
        # Scoped runs never recall Claims at routing time. Both downstream
        # families read the findings ledger directly and host-side -- Family Q
        # as a retained-seed relational graph after the basis is frozen and
        # audited, Family C as content-hashed corpus slices -- so a route-time
        # pool would be an unread artifact. Requiring one only taught the router
        # to either close the challenger lane or invent the counts.
        if claim_section is not None:
            _fail(
                "scoped plans must not declare claim_recall: the corpus is read "
                "downstream of the frozen basis, not recalled at routing time"
            )
        if recall:
            _fail("scoped plans must not depend on a Claim-recall manifest")
    elif skips_claim_recall:
        if recall is not None and recall:
            _fail("claim_strategy=none must not depend on a Claim-recall manifest")
    else:
        if recall is None:
            _fail("the selected Claim strategy requires a Claim-recall manifest")
        if not isinstance(claim_section, dict):
            _fail("the selected Claim strategy requires a claim_recall object")
        coverage = recall.get("coverage") if isinstance(recall, dict) else None
        if not isinstance(coverage, dict):
            _fail("Claim-recall manifest lacks coverage")
        claims = int(coverage.get("claims") or 0)
        accounted = int(coverage.get("accounted") or 0)
        unresolved = int(coverage.get("unresolved") or 0)
        if not claims or accounted != claims or unresolved:
            _fail(
                f"incomplete Claim accounting: claims={claims} accounted={accounted} "
                f"unresolved={unresolved}"
            )
        selected = int(coverage.get("selected") or 0)
        if int(claim_section.get("claims") or 0) != claims:
            _fail("task plan Claim count does not match recall manifest")
        if int(claim_section.get("selected") or 0) != selected:
            _fail("task plan selected Claim count does not match recall manifest")

    candidate_universe = plan.get("candidate_universe")
    if not isinstance(candidate_universe, dict) or not candidate_universe.get(
        "definition"
    ):
        _fail("candidate_universe requires a concrete definition")
    if not candidate_universe.get("completion_accounting"):
        _fail("candidate_universe requires completion_accounting")
    evidence = plan.get("evidence_authority")
    if not isinstance(evidence, dict) or not evidence.get("exact_measurements"):
        _fail("evidence_authority must name the exact-measurement source")
    if not str(plan.get("termination_condition") or "").strip():
        _fail("termination_condition must be non-empty")
    validation = plan.get("validation")
    if not isinstance(validation, list) or not validation:
        _fail("validation must contain explicit final checks")
    return {
        "schema_version": PLAN_VERSION,
        "valid": True,
        "task_class": plan_class,
        "endpoint": validated_reasoning["endpoint"],
        "schema_relation": plan_relation,
        "corpus_coverage": corpus_coverage,
        "execution_pattern": plan.get("playbook") or "composed_from_reasoning",
        "stages": len(stages),
        "deliverables": sorted(planned_files),
        "claim_recall_required": not skips_claim_recall,
        "claim_strategy": validated_reasoning["claim_strategy"],
        "profile_schema_version": validated_profile["schema_version"],
        "normalization": {
            "source": "authoritative_profile",
            "applied_fields": normalized_fields,
        },
        "dataset_context": dataset_context,
        "predicted_execution": predicted_execution,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--recall", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    recall = (
        json.loads(args.recall.read_text(encoding="utf-8")) if args.recall else None
    )
    result = validate_plan(plan, profile, recall)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
