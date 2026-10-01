#!/usr/bin/env python3
"""Create or validate a task-general DistributedAgents reasoning profile.

The first pass extracts only mechanical facts from the task. It deliberately
does not map endpoint names to canned workflows. The coordinator must read the
dataset portrait and REASONING_CONTRACT.md, resolve the semantic fields, and
validate the edited v4 profile before Claim routing or planning.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SCHEMA_VERSION = "distributed_agents-task-profile-v4"
ROUTE_DECISION_SCHEMA_VERSION = "distributed_agents-route-decision-v1"
# Fields copied verbatim into the execution plan. This is the one canonical
# projection list shared by the compiler and validator; downstream_family is
# intentionally absent because it is derived from quantitative_basis.kind.
EXECUTION_PROFILE_FIELDS = (
    "task_class",
    "classification_rationale",
    "endpoint_definition",
    "schema_relation",
    "output_contract",
    "claim_strategy",
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
)
TASK_CLASSES = (
    "direct_measurement",
    "targeted_synthesis",
    "atlas_discovery",
    "ranked_analysis",
    "exhaustive_classification",
    "cross_context_analysis",
    "composed_general",
)
CLAIM_STRATEGIES = (
    "none",
    "targeted",
    "all_active",
    "all_relational",
    "all_claims",
    "semantic_screen",
    "requires_semantic_review",
)
DATASET_OBSERVABILITY = (
    "direct",
    "proxy",
    "absent",
    "unobserved_context",
    "requires_semantic_review",
)
LEDGER_ALIGNMENT = (
    "native",
    "adjacent",
    "incidental",
    "absent",
    "not_required",
    "requires_semantic_review",
)
ANSWER_MODES = ("direct", "derived", "predicted", "requires_semantic_review")
COMBINED_RELATIONS = (
    "in_schema_dataset_and_ledger",
    "in_schema_dataset_only",
    "in_schema_ledger_only",
    "out_of_schema_orthogonal",
    "out_of_schema_cross_context",
    "requires_semantic_review",
)
VALIDATION_RULES = (
    (
        "schema_relation.in_schema_dataset_and_ledger requires "
        "dataset_observability in {direct, proxy}, ledger_alignment in "
        "{native, adjacent}, and answer_mode in {direct, derived}"
    ),
    (
        "schema_relation.in_schema_dataset_only requires dataset_observability "
        "in {direct, proxy}, ledger_alignment in {not_required, absent, "
        "incidental}, and answer_mode in {direct, derived}"
    ),
    (
        "schema_relation.in_schema_ledger_only requires ledger_alignment=native "
        "and answer_mode in {direct, derived}"
    ),
    (
        "schema_relation.out_of_schema_orthogonal requires "
        "dataset_observability=absent, ledger_alignment in {incidental, absent, "
        "adjacent}, and answer_mode=predicted"
    ),
    (
        "schema_relation.out_of_schema_cross_context requires "
        "dataset_observability=unobserved_context, ledger_alignment in "
        "{incidental, absent, adjacent}, and answer_mode=predicted"
    ),
    (
        "claim_attention_policy.expansion_mode=fanout requires a "
        "corpus_claim_substrate, zero precision_fraction and "
        "diversity_fraction, and non-empty candidate_summary and path_audit "
        "artifact names"
    ),
    (
        "when packaged corpus grounding is the starting evidence and fresh "
        "external retrieval is only a gap fallback, set external_evidence.role="
        "none and external_discovery.required=false"
    ),
    (
        "an external_evidence.role other than none requires "
        "external_discovery.required=true, an explicit capability gap, and at "
        "least one external_transfer analysis with caveats and residual questions"
    ),
    (
        "output_reduction_policy.proxy_independence_rule must be non-empty even "
        "when no proxy is used; state that no proxy ranking is used"
    ),
)
OUTPUT_TOPOLOGIES = (
    "ranking",
    "discovery",
    "exhaustive_classification",
    "targeted_synthesis",
    "direct_measurement",
    "requires_semantic_review",
)
CONTEXT_DEPENDENCE = (
    "experiment_conditioned",
    "context_conditioned_transferable",
    "broadly_portable",
    "unresolved",
    "requires_semantic_review",
)
MEASUREMENT_PORTABILITY = (
    "biological_event",
    "assay_defined_quantity",
    "hybrid_or_unresolved",
    "requires_semantic_review",
)
LOCAL_OBSERVATION_STAGES = (
    "direct_event_measurement",
    "pre_event",
    "concurrent_not_survival_conditioned",
    "post_event_survivor_conditioned",
    "not_applicable",
    "requires_semantic_review",
)
EVENT_ERASURE_OF_LOCAL_OBSERVATION = (
    "absent",
    "possible",
    "structural",
    "not_applicable",
    "requires_semantic_review",
)
EXTERNAL_CANDIDATE_ROLES = (
    "primary",
    "supplementary",
    "not_required",
    "requires_semantic_review",
)
SUPPLIED_DATASET_ROLES = (
    "primary_direct_measurement",
    "primary_same_experiment_inferential_substrate",
    "candidate_universe_only",
    "supporting_context",
    "not_required",
    "requires_semantic_review",
)
EXTERNAL_EVIDENCE_ROLES = (
    "quantitative_anchor",
    "qualitative_mechanism",
    "validation_falsification",
    "none",
    "requires_semantic_review",
)
INDIRECT_EVIDENCE_ROLES = (
    "supporting",
    "veto_or_support",
    "not_required",
    "requires_semantic_review",
)
QUANTITATIVE_BASIS_KINDS = (
    "direct_dataset_result",
    "same_experiment_derived",
    "external_quantitative_prior",
    "neutral_candidate_universe",
    # The findings/claims corpus IS the basis: there is no candidate scalar to
    # order, so the downstream shape is a fan-out read of corpus slices plus one
    # adjudicator rather than a single reviewer over a materialized ordering.
    "corpus_claim_substrate",
    "requires_semantic_review",
)
DOWNSTREAM_FAMILIES = ("quantitative", "corpus_aggregation")
CORPUS_SUBSTRATE_KIND = "corpus_claim_substrate"
ORDERING_IDENTIFIABILITY_DECISIONS = (
    "eligible",
    "neutral",
    "requires_semantic_review",
)
ENDPOINT_ERASURE_RISKS = (
    "absent",
    "present",
    "not_applicable",
    "requires_semantic_review",
)
CANDIDATE_VALUE_SEMANTICS = (
    "comparable",
    "not_comparable",
    "not_applicable",
    "requires_semantic_review",
)
QUANTITATIVE_TRANSPORT = (
    "calibrated_to_destination",
    "portable_ordering",
    "qualitative_only",
    "requires_semantic_review",
)
PROXY_CANDIDATE_ROLES = (
    "allowed",
    "forbidden",
    "not_applicable",
    "requires_semantic_review",
)
PROXY_RANKING_ROLES = (
    "primary",
    "support_only",
    "veto_or_support",
    "not_applicable",
    "requires_semantic_review",
)
BASIS_ORDERING_UTILITY = (
    "defensible",
    "weak_or_neutral",
    "not_applicable",
    "requires_semantic_review",
)
BASIS_CALIBRATION_STATUS = (
    "known",
    "unknown",
    "not_applicable",
    "requires_semantic_review",
)
CLAIM_EXPANSION_MODES = (
    "weighted_one_hop",
    # Partitioned read of the corpus substrate itself. Only a corpus basis may
    # use it: there is no candidate ordering to weight one hop against.
    "fanout",
    "none",
    "requires_semantic_review",
)


def _fail(message: str) -> None:
    raise ValueError(message)


def derive_downstream_family(basis_kind: str) -> str:
    """Map a quantitative-basis kind onto its downstream execution family."""

    return (
        "corpus_aggregation"
        if basis_kind == CORPUS_SUBSTRATE_KIND
        else "quantitative"
    )


def normalize_execution_plan(
    plan: dict[str, object],
    profile: dict[str, object],
) -> dict[str, object]:
    """Project one validated profile into an execution-plan compatibility view.

    The flat v4 plan shape is retained for existing consumers, but it is never
    an independent semantic document. Missing or stale copied fields are
    replaced from the authoritative profile, and the execution family is
    derived from the basis kind. Only plan-owned stages and artifact wiring
    remain untouched.
    """

    validated = validate_profile(profile)
    normalized = dict(plan)
    for field in EXECUTION_PROFILE_FIELDS:
        normalized[field] = profile.get(field)
    scope_value = normalized.get("execution_scope")
    scope = dict(scope_value) if isinstance(scope_value, dict) else {}
    scope["downstream_family"] = validated["downstream_family"]
    scope.setdefault("stage", "full")
    normalized["execution_scope"] = scope
    return normalized


def _requested_count(text: str) -> tuple[int | None, str]:
    patterns = (
        (r"\bexactly\s+(\d+)\b", "exact"),
        (r"\btop\s+(\d+)\b", "maximum"),
        (r"\bup to\s+(\d+)\b", "maximum"),
        (r"\b(\d+)\s+ranked\b", "exact"),
    )
    low = text.casefold()
    for pattern, mode in patterns:
        match = re.search(pattern, low)
        if match:
            return int(match.group(1)), mode
    return None, "unspecified"


def _deliverables(text: str) -> list[str]:
    found: list[str] = []
    patterns = (
        r"`(?:\./)?([^`/\n]+\.(?:md|txt|jsonl|json|csv|tsv))`",
        r"(?<![A-Za-z0-9_.-])\./([^/\n`]+\.(?:md|txt|jsonl|json|csv|tsv))",
        r"(?:^|[\s(])/[A-Za-z0-9_. /-]+/([^/\n)]+\.(?:md|txt|jsonl|json|csv|tsv))",
        r"(?mi)^\s*File\s+\d+\s*:\s*([^/\n]+\.(?:md|txt|jsonl|json|csv|tsv))\s*$",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            name = Path(match.group(1).strip()).name
            if name and name not in found and not name.casefold().endswith(".parquet"):
                found.append(name)
    return found


def _input_paths(text: str) -> list[str]:
    paths: list[str] = []
    for match in re.finditer(
        r"(?:`)?([^\s`]+\.parquet)(?:`)?", text, flags=re.IGNORECASE
    ):
        path = match.group(1).rstrip(".,);:")
        if path not in paths:
            paths.append(path)
    return paths


def _explicit_targets(text: str) -> list[str]:
    targets: list[str] = []
    list_match = re.search(
        r"(?:the\s+)?(?:\d+\s+)?target genes\s*:\s*\n([^\n]+)",
        text,
        flags=re.IGNORECASE,
    )
    if list_match:
        for token in re.split(r"[,;\s]+", list_match.group(1)):
            if re.fullmatch(r"[A-Z][A-Za-z0-9-]{1,15}", token):
                targets.append(token)
    return list(dict.fromkeys(targets))


def _candidate_scope(text: str, explicit_targets: list[str]) -> str:
    if explicit_targets:
        return "explicit_targets"
    low = text.casefold()
    if any(
        phrase in low
        for phrase in (
            "all of the perturbations",
            "candidate perturbations",
            "screen-wide",
            "approximately 2,046",
            "~2,046",
        )
    ):
        return "all_targets"
    return "task_defined"


def profile_text(text: str, *, override: str | None = None) -> dict[str, object]:
    """Extract a neutral draft that requires coordinator semantic resolution."""

    requested_count, count_mode = _requested_count(text)
    explicit_targets = _explicit_targets(text)
    task_class = override or "composed_general"
    forced = override is not None
    return {
        "schema_version": SCHEMA_VERSION,
        "task_class": task_class,
        "classification_confidence": "forced" if forced else "requires_semantic_review",
        "classification_signals": (
            ["task class forced by caller"]
            if forced
            else ["mechanical extraction only; coordinator semantic review required"]
        ),
        "classification_rationale": (
            "Caller supplied the execution class."
            if forced
            else "No endpoint-name-to-playbook classifier is used."
        ),
        "endpoint_definition": {
            "name": "requires_semantic_review",
            "unit": "requires_semantic_review",
            "candidate_universe": _candidate_scope(text, explicit_targets),
            "event": "requires_semantic_review",
            "direct_observable": "requires_semantic_review",
            "inferential_operation": "requires_semantic_review",
            "context_dependence": "requires_semantic_review",
            "measurement_portability": "requires_semantic_review",
            "local_observation_stage": "requires_semantic_review",
            "event_erasure_of_local_observation": "requires_semantic_review",
            "related_but_distinct": [],
        },
        "schema_relation": {
            "dataset_observability": "requires_semantic_review",
            "ledger_alignment": "requires_semantic_review",
            "answer_mode": "requires_semantic_review",
            "combined": "requires_semantic_review",
            "rationale": "Coordinator must resolve both evidence layers from first principles.",
        },
        "candidate_scope": _candidate_scope(text, explicit_targets),
        "explicit_targets": explicit_targets,
        "query_terms": [],
        "input_paths": _input_paths(text),
        "output_contract": {
            "deliverables": _deliverables(text),
            "requested_count": requested_count,
            "count_mode": count_mode,
            "topology": "requires_semantic_review",
        },
        "claim_recall_required": True,
        "claim_strategy": "requires_semantic_review",
        "resource_strategy": {
            "installed_skill_roles": [],
            "capability_gaps": [],
            "external_discovery": {
                "required": False,
                "resource_class": "",
                "selection_criteria": [],
                "coverage_requirement": "",
                "candidate_generation_role": "requires_semantic_review",
                "artifacts": {
                    "resource_manifest": "",
                    "candidate_prior": "",
                    "coverage_audit": "",
                },
            },
            "acquisition_policy": "data_only_https",
        },
        "evidence_role_resolution": {
            "supplied_dataset": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
            "external_evidence": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
            "proxies_or_indirect": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
        },
        "quantitative_basis": {
            "kind": "requires_semantic_review",
            "source": "",
            "construction": "",
            "candidate_universe_rule": "",
            "ordering_identifiability": {
                "decision": "requires_semantic_review",
                "directional_relation": "",
                "endpoint_erasure_risk": "requires_semantic_review",
                "candidate_value_semantics": "requires_semantic_review",
                "rationale": "",
            },
            "acquisition_failure_policy": (
                "select_another_eligible_basis_or_use_neutral_candidate_universe"
            ),
            "artifacts": {
                "base": "",
                "coverage_audit": "",
                "corpus_slice_plan": "",
            },
        },
        "claim_attention_policy": {
            "basis_ordering_utility": "requires_semantic_review",
            "basis_ordering_rationale": "",
            "calibration_status": "requires_semantic_review",
            "expansion_mode": "requires_semantic_review",
            "anchor_count": 0,
            "related_candidate_budget": 0,
            "precision_fraction": 0.8,
            "diversity_fraction": 0.2,
            "full_report_budget": 0,
            "artifacts": {
                "path_audit": "",
                "candidate_summary": "",
            },
        },
        "external_transfer": [],
        "candidate_decision_policy": {
            "promote": [],
            "retain": [],
            "down_rank": [],
            "reject": [],
        },
        "mechanism_model": {
            "families": [],
            "not_required_reason": "",
        },
        "multi_hop_model": {
            "forward": [],
            "reverse": [],
            "not_required_reason": "",
        },
        "proxy_model": {
            "required": False,
            "causal_hypothesis": "",
            "controls": [],
            "falsifiers": [],
            "null_semantics": "",
            "candidate_generation_role": "requires_semantic_review",
            "ranking_role": "requires_semantic_review",
        },
        "evidence_ledger_policy": {
            "veto": [],
            "support_only": [],
            "non_negative": [],
            "uncertainty": [],
        },
        "output_reduction_policy": {
            "candidate_union": "",
            "comparison_rule": "",
            "accounting_rule": "",
            "termination_rule": "",
            "candidate_provenance_rule": "",
            "proxy_independence_rule": "",
            "artifacts": {
                "candidate_evidence_ledger": "",
                "candidate_decisions": "",
                "global_ranking_audit": "",
                "proxy_independence_audit": "",
            },
        },
    }


def _require_object(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        _fail(f"{name} must be an object")
    return value


def _require_text(value: object, name: str, *, resolved: bool = True) -> str:
    text = str(value or "").strip()
    if not text:
        _fail(f"{name} must be non-empty")
    if resolved and text == "requires_semantic_review":
        _fail(f"{name} still requires semantic review")
    return text


def _require_list(value: object, name: str) -> list[object]:
    if not isinstance(value, list):
        _fail(f"{name} must be a list")
    return value


def _validate_schema_relation(value: object) -> dict[str, str]:
    relation = _require_object(value, "schema_relation")
    fields = {
        "dataset_observability": DATASET_OBSERVABILITY,
        "ledger_alignment": LEDGER_ALIGNMENT,
        "answer_mode": ANSWER_MODES,
        "combined": COMBINED_RELATIONS,
    }
    result: dict[str, str] = {}
    for field, allowed in fields.items():
        item = _require_text(relation.get(field), f"schema_relation.{field}")
        if item not in allowed:
            _fail(f"unsupported schema_relation.{field}: {item!r}")
        result[field] = item
    result["rationale"] = _require_text(
        relation.get("rationale"), "schema_relation.rationale", resolved=False
    )
    dataset = result["dataset_observability"]
    ledger = result["ledger_alignment"]
    answer = result["answer_mode"]
    combined = result["combined"]
    valid_layers = {
        "in_schema_dataset_and_ledger": (
            dataset in {"direct", "proxy"}
            and ledger in {"native", "adjacent"}
            and answer in {"direct", "derived"}
        ),
        "in_schema_dataset_only": (
            dataset in {"direct", "proxy"}
            and ledger in {"not_required", "absent", "incidental"}
            and answer in {"direct", "derived"}
        ),
        "in_schema_ledger_only": (
            ledger == "native" and answer in {"direct", "derived"}
        ),
        "out_of_schema_orthogonal": (
            dataset == "absent"
            and ledger in {"incidental", "absent", "adjacent"}
            and answer == "predicted"
        ),
        "out_of_schema_cross_context": (
            dataset == "unobserved_context"
            and ledger in {"incidental", "absent", "adjacent"}
            and answer == "predicted"
        ),
    }
    if combined in valid_layers and not valid_layers[combined]:
        _fail(f"{combined} has inconsistent layer values")
    return result


def validate_profile(profile: dict[str, object]) -> dict[str, object]:
    if profile.get("schema_version") != SCHEMA_VERSION:
        _fail(f"unsupported task-profile schema: {profile.get('schema_version')!r}")
    task_class = _require_text(profile.get("task_class"), "task_class")
    if task_class not in TASK_CLASSES:
        _fail(f"unsupported task_class: {task_class!r}")
    _require_text(
        profile.get("classification_rationale"),
        "classification_rationale",
        resolved=False,
    )

    endpoint = _require_object(
        profile.get("endpoint_definition"), "endpoint_definition"
    )
    for field in (
        "name",
        "unit",
        "candidate_universe",
        "event",
        "direct_observable",
        "inferential_operation",
        "context_dependence",
        "measurement_portability",
        "local_observation_stage",
        "event_erasure_of_local_observation",
    ):
        _require_text(endpoint.get(field), f"endpoint_definition.{field}")
    if endpoint["context_dependence"] not in CONTEXT_DEPENDENCE:
        _fail(
            "unsupported endpoint_definition.context_dependence: "
            f"{endpoint['context_dependence']!r}"
        )
    if endpoint["measurement_portability"] not in MEASUREMENT_PORTABILITY:
        _fail(
            "unsupported endpoint_definition.measurement_portability: "
            f"{endpoint['measurement_portability']!r}"
        )
    if endpoint["local_observation_stage"] not in LOCAL_OBSERVATION_STAGES:
        _fail(
            "unsupported endpoint_definition.local_observation_stage: "
            f"{endpoint['local_observation_stage']!r}"
        )
    if (
        endpoint["event_erasure_of_local_observation"]
        not in EVENT_ERASURE_OF_LOCAL_OBSERVATION
    ):
        _fail(
            "unsupported endpoint_definition."
            "event_erasure_of_local_observation: "
            f"{endpoint['event_erasure_of_local_observation']!r}"
        )
    if (
        endpoint["local_observation_stage"] == "post_event_survivor_conditioned"
        and endpoint["event_erasure_of_local_observation"] == "absent"
    ):
        _fail(
            "post-event survivor-conditioned observations cannot declare "
            "event erasure absent; the requested event removes observations "
            "from units that do not survive to measurement"
        )
    _require_list(
        endpoint.get("related_but_distinct"), "endpoint_definition.related_but_distinct"
    )
    relation = _validate_schema_relation(profile.get("schema_relation"))

    output = _require_object(profile.get("output_contract"), "output_contract")
    topology = _require_text(output.get("topology"), "output_contract.topology")
    if topology not in OUTPUT_TOPOLOGIES:
        _fail(f"unsupported output topology: {topology!r}")
    _require_list(output.get("deliverables"), "output_contract.deliverables")

    strategy = _require_text(profile.get("claim_strategy"), "claim_strategy")
    if strategy not in CLAIM_STRATEGIES:
        _fail(f"unsupported claim_strategy: {strategy!r}")
    if bool(profile.get("claim_recall_required")) == (strategy == "none"):
        _fail("claim_recall_required and claim_strategy are inconsistent")

    resources = _require_object(profile.get("resource_strategy"), "resource_strategy")
    _require_list(
        resources.get("installed_skill_roles"),
        "resource_strategy.installed_skill_roles",
    )
    gaps = _require_list(
        resources.get("capability_gaps"), "resource_strategy.capability_gaps"
    )
    discovery = _require_object(
        resources.get("external_discovery"), "resource_strategy.external_discovery"
    )
    if resources.get("acquisition_policy") != "data_only_https":
        _fail("resource_strategy.acquisition_policy must be data_only_https")
    if bool(discovery.get("required")):
        _require_text(
            discovery.get("resource_class"),
            "resource_strategy.external_discovery.resource_class",
            resolved=False,
        )
        criteria = _require_list(
            discovery.get("selection_criteria"),
            "resource_strategy.external_discovery.selection_criteria",
        )
        if not criteria:
            _fail("external discovery requires source-selection criteria")
        if not gaps:
            _fail("external discovery requires an explicit capability gap")
    candidate_generation_role = _require_text(
        discovery.get("candidate_generation_role"),
        "resource_strategy.external_discovery.candidate_generation_role",
    )
    if candidate_generation_role not in EXTERNAL_CANDIDATE_ROLES:
        _fail(
            "unsupported resource_strategy.external_discovery."
            f"candidate_generation_role: {candidate_generation_role!r}"
        )

    roles = _require_object(
        profile.get("evidence_role_resolution"), "evidence_role_resolution"
    )
    role_specs = (
        ("supplied_dataset", SUPPLIED_DATASET_ROLES),
        ("external_evidence", EXTERNAL_EVIDENCE_ROLES),
        ("proxies_or_indirect", INDIRECT_EVIDENCE_ROLES),
    )
    resolved_roles: dict[str, str] = {}
    for field, allowed in role_specs:
        row = _require_object(roles.get(field), f"evidence_role_resolution.{field}")
        role = _require_text(row.get("role"), f"evidence_role_resolution.{field}.role")
        if role not in allowed:
            _fail(f"unsupported evidence_role_resolution.{field}.role: {role!r}")
        _require_text(
            row.get("rationale"),
            f"evidence_role_resolution.{field}.rationale",
            resolved=False,
        )
        resolved_roles[field] = role

    basis = _require_object(profile.get("quantitative_basis"), "quantitative_basis")
    basis_kind = _require_text(basis.get("kind"), "quantitative_basis.kind")
    if basis_kind not in QUANTITATIVE_BASIS_KINDS:
        _fail(f"unsupported quantitative_basis.kind: {basis_kind!r}")
    for field in ("source", "construction", "candidate_universe_rule"):
        _require_text(
            basis.get(field),
            f"quantitative_basis.{field}",
            resolved=False,
        )
    identifiability = _require_object(
        basis.get("ordering_identifiability"),
        "quantitative_basis.ordering_identifiability",
    )
    decision = _require_text(
        identifiability.get("decision"),
        "quantitative_basis.ordering_identifiability.decision",
    )
    if decision not in ORDERING_IDENTIFIABILITY_DECISIONS:
        _fail(f"unsupported ordering-identifiability decision: {decision!r}")
    erasure_risk = _require_text(
        identifiability.get("endpoint_erasure_risk"),
        "quantitative_basis.ordering_identifiability.endpoint_erasure_risk",
    )
    if erasure_risk not in ENDPOINT_ERASURE_RISKS:
        _fail(f"unsupported endpoint-erasure risk: {erasure_risk!r}")
    value_semantics = _require_text(
        identifiability.get("candidate_value_semantics"),
        "quantitative_basis.ordering_identifiability.candidate_value_semantics",
    )
    if value_semantics not in CANDIDATE_VALUE_SEMANTICS:
        _fail(f"unsupported candidate-value semantics: {value_semantics!r}")
    for field in ("directional_relation", "rationale"):
        _require_text(
            identifiability.get(field),
            f"quantitative_basis.ordering_identifiability.{field}",
            resolved=False,
        )
    failure_policy = _require_text(
        basis.get("acquisition_failure_policy"),
        "quantitative_basis.acquisition_failure_policy",
    )
    if failure_policy != (
        "select_another_eligible_basis_or_use_neutral_candidate_universe"
    ):
        _fail(
            "quantitative_basis.acquisition_failure_policy must preserve the "
            "ordering-identifiability gate"
        )
    if basis_kind == "neutral_candidate_universe":
        if decision != "neutral":
            _fail("a neutral candidate universe requires decision=neutral")
        if erasure_risk == "absent" and value_semantics == "comparable":
            _fail(
                "a neutral candidate universe must record why no eligible "
                "ordering was selected"
            )
    elif basis_kind == CORPUS_SUBSTRATE_KIND:
        # A corpus substrate is read, not ordered. Declaring an eligible
        # candidate ordering here would smuggle a scalar basis back in.
        if decision != "neutral":
            _fail("a corpus claim substrate requires decision=neutral")
        if value_semantics != "not_applicable":
            _fail(
                "a corpus claim substrate has no candidate-level values to "
                "compare; candidate_value_semantics must be not_applicable"
            )
        if erasure_risk not in {"absent", "not_applicable"}:
            _fail(
                "a corpus claim substrate must record endpoint erasure as "
                "absent or not_applicable"
            )
    else:
        if decision != "eligible":
            _fail("a quantitative ordering requires decision=eligible")
        if erasure_risk != "absent":
            _fail(
                "a quantitative ordering cannot use a measurement erased by "
                "the requested endpoint"
            )
        if value_semantics != "comparable":
            _fail(
                "a quantitative ordering requires comparable candidate-level "
                "value semantics"
            )
    if (
        basis_kind == "same_experiment_derived"
        and endpoint["event_erasure_of_local_observation"] != "absent"
    ):
        _fail(
            "a same-experiment-derived ordering requires the requested event "
            "not to erase its local observations"
        )
    basis_artifacts = _require_object(
        basis.get("artifacts"), "quantitative_basis.artifacts"
    )
    if basis_kind == CORPUS_SUBSTRATE_KIND:
        if str(basis_artifacts.get("base") or "").strip():
            _fail(
                "a corpus claim substrate must not declare "
                "quantitative_basis.artifacts.base; there is no candidate "
                "scalar to materialize"
            )
        for field in ("corpus_slice_plan", "coverage_audit"):
            _require_text(
                basis_artifacts.get(field),
                f"quantitative_basis.artifacts.{field}",
                resolved=False,
            )
    else:
        for field in ("base", "coverage_audit"):
            _require_text(
                basis_artifacts.get(field),
                f"quantitative_basis.artifacts.{field}",
                resolved=False,
            )

    attention = _require_object(
        profile.get("claim_attention_policy"), "claim_attention_policy"
    )
    ordering_utility = _require_text(
        attention.get("basis_ordering_utility"),
        "claim_attention_policy.basis_ordering_utility",
    )
    if ordering_utility not in BASIS_ORDERING_UTILITY:
        _fail(f"unsupported basis-ordering utility: {ordering_utility!r}")
    _require_text(
        attention.get("basis_ordering_rationale"),
        "claim_attention_policy.basis_ordering_rationale",
        resolved=False,
    )
    calibration_status = _require_text(
        attention.get("calibration_status"),
        "claim_attention_policy.calibration_status",
    )
    if calibration_status not in BASIS_CALIBRATION_STATUS:
        _fail(f"unsupported basis calibration status: {calibration_status!r}")
    expansion_mode = _require_text(
        attention.get("expansion_mode"),
        "claim_attention_policy.expansion_mode",
    )
    if expansion_mode not in CLAIM_EXPANSION_MODES:
        _fail(f"unsupported Claim expansion mode: {expansion_mode!r}")
    if basis_kind == CORPUS_SUBSTRATE_KIND and expansion_mode == "weighted_one_hop":
        # A corpus substrate has no ranked incumbent set, so there is nothing to
        # expand a weighted hop from and no vacancy count to bound the pool
        # with. Reading the corpus is itself the retrieval, so the only
        # expansion it supports is fan-out across slices.
        _fail(
            "a corpus Claim substrate cannot use weighted Claim expansion; the "
            "corpus read is the retrieval, so use fanout or none"
        )

    integer_fields: dict[str, int] = {}
    for field in (
        "anchor_count",
        "related_candidate_budget",
        "full_report_budget",
    ):
        value = attention.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            _fail(f"claim_attention_policy.{field} must be a non-negative integer")
        integer_fields[field] = value
    fractions: dict[str, float] = {}
    for field in ("precision_fraction", "diversity_fraction"):
        value = attention.get(field)
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not 0 <= float(value) <= 1
        ):
            _fail(f"claim_attention_policy.{field} must be between 0 and 1")
        fractions[field] = float(value)

    attention_artifacts = _require_object(
        attention.get("artifacts"), "claim_attention_policy.artifacts"
    )
    if expansion_mode == "weighted_one_hop":
        if ordering_utility != "defensible":
            _fail(
                "weighted Claim expansion requires a defensible relative ordering; "
                "known predictive accuracy is not required"
            )
        if basis_kind == "neutral_candidate_universe":
            _fail("a neutral candidate universe cannot seed Claim expansion")
        if strategy == "none":
            _fail("weighted Claim expansion requires routed Claims")
        if integer_fields["anchor_count"] < 1:
            _fail("weighted Claim expansion requires at least one anchor")
        related_limit = min(50, (integer_fields["anchor_count"] + 1) // 2)
        if not 1 <= integer_fields["related_candidate_budget"] <= related_limit:
            _fail(
                "related_candidate_budget must be between 1 and "
                "min(50, ceil(anchor_count / 2))"
            )
        if abs(sum(fractions.values()) - 1.0) > 1e-9:
            _fail("precision_fraction and diversity_fraction must sum to 1")
        union_size = (
            integer_fields["anchor_count"]
            + integer_fields["related_candidate_budget"]
        )
        report_limit = min(20, max(1, (union_size + 9) // 10))
        if integer_fields["full_report_budget"] > report_limit:
            _fail("full_report_budget exceeds min(20, ceil(union_size / 10))")
        for field in ("path_audit", "candidate_summary"):
            _require_text(
                attention_artifacts.get(field),
                f"claim_attention_policy.artifacts.{field}",
                resolved=False,
            )
    elif expansion_mode == "fanout":
        # Fan-out partitions the substrate; it does not weight a hop from an
        # ordered seed, so anchors, related budgets, and the precision/diversity
        # split of weighted_one_hop have no meaning here.
        if basis_kind != CORPUS_SUBSTRATE_KIND:
            _fail("fan-out Claim expansion requires a corpus claim substrate")
        if strategy == "none":
            _fail("fan-out Claim expansion requires a Claim strategy")
        if integer_fields["related_candidate_budget"] != 0:
            _fail("expansion_mode=fanout requires related_candidate_budget=0")
        if fractions["precision_fraction"] or fractions["diversity_fraction"]:
            _fail("expansion_mode=fanout requires zero precision/diversity fractions")
        if integer_fields["anchor_count"] < 1:
            _fail("fan-out Claim expansion requires at least one corpus slice")
        _require_text(
            attention_artifacts.get("candidate_summary"),
            "claim_attention_policy.artifacts.candidate_summary",
            resolved=False,
        )
    else:
        if integer_fields["related_candidate_budget"] != 0:
            _fail("expansion_mode=none requires related_candidate_budget=0")
        if fractions["precision_fraction"] or fractions["diversity_fraction"]:
            _fail("expansion_mode=none requires zero precision/diversity fractions")
    if ordering_utility == "defensible" and decision != "eligible":
        _fail("a defensible basis ordering requires an eligible ordering")
    if basis_kind == "neutral_candidate_universe" and ordering_utility != (
        "weak_or_neutral"
    ):
        _fail("a neutral candidate universe must be weak_or_neutral for attention")
    if basis_kind == CORPUS_SUBSTRATE_KIND:
        # not_applicable is the only honest attention value for a substrate with
        # no candidate ordering, and it is exactly why the value exists.
        if ordering_utility != "not_applicable":
            _fail(
                "a corpus claim substrate must declare basis_ordering_utility="
                "not_applicable"
            )
        if strategy == "none":
            _fail("a corpus claim substrate requires a routed Claim strategy")
        if expansion_mode not in {"weighted_one_hop", "fanout"}:
            _fail(
                "a corpus claim substrate must expand Claims by "
                "weighted_one_hop or fanout"
            )
    elif ordering_utility == "not_applicable" and expansion_mode != "none":
        _fail("not_applicable ordering utility cannot expand Claims")

    transfers = _require_list(profile.get("external_transfer"), "external_transfer")
    if bool(discovery.get("required")) and not transfers:
        _fail(
            "external discovery requires at least one transfer analysis with "
            "caveats and residual questions"
        )
    for index, item in enumerate(transfers):
        row = _require_object(item, f"external_transfer[{index}]")
        for field in (
            "source",
            "what_it_explains",
            "transfer_caveats",
            "residual_questions",
        ):
            value = row.get(field)
            if isinstance(value, list):
                if not value:
                    _fail(f"external_transfer[{index}].{field} must be non-empty")
            else:
                _require_text(
                    value,
                    f"external_transfer[{index}].{field}",
                    resolved=False,
                )
        transport = _require_text(
            row.get("quantitative_transport"),
            f"external_transfer[{index}].quantitative_transport",
        )
        if transport not in QUANTITATIVE_TRANSPORT:
            _fail(
                "unsupported external_transfer"
                f"[{index}].quantitative_transport: {transport!r}"
            )
        decisions = _require_object(
            row.get("decision_criteria"),
            f"external_transfer[{index}].decision_criteria",
        )
        for field in ("promote", "retain", "down_rank", "reject"):
            _require_list(
                decisions.get(field),
                f"external_transfer[{index}].decision_criteria.{field}",
            )

    decision = _require_object(
        profile.get("candidate_decision_policy"), "candidate_decision_policy"
    )
    for field in ("promote", "retain", "down_rank", "reject"):
        _require_list(decision.get(field), f"candidate_decision_policy.{field}")

    mechanism = _require_object(profile.get("mechanism_model"), "mechanism_model")
    families = _require_list(mechanism.get("families"), "mechanism_model.families")
    if not families and not str(mechanism.get("not_required_reason") or "").strip():
        _fail("mechanism_model requires families or not_required_reason")
    for index, family in enumerate(families):
        row = _require_object(family, f"mechanism_model.families[{index}]")
        for field in ("name", "causal_chain", "assay_window_fit"):
            _require_text(
                row.get(field),
                f"mechanism_model.families[{index}].{field}",
                resolved=False,
            )

    hops = _require_object(profile.get("multi_hop_model"), "multi_hop_model")
    forward = _require_list(hops.get("forward"), "multi_hop_model.forward")
    reverse = _require_list(hops.get("reverse"), "multi_hop_model.reverse")
    if (not forward or not reverse) and not str(
        hops.get("not_required_reason") or ""
    ).strip():
        _fail(
            "multi_hop_model requires forward and reverse paths or not_required_reason"
        )

    proxy = _require_object(profile.get("proxy_model"), "proxy_model")
    proxy_candidate_role = _require_text(
        proxy.get("candidate_generation_role"),
        "proxy_model.candidate_generation_role",
    )
    if proxy_candidate_role not in PROXY_CANDIDATE_ROLES:
        _fail(
            "unsupported proxy_model.candidate_generation_role: "
            f"{proxy_candidate_role!r}"
        )
    proxy_ranking_role = _require_text(
        proxy.get("ranking_role"),
        "proxy_model.ranking_role",
    )
    if proxy_ranking_role not in PROXY_RANKING_ROLES:
        _fail(f"unsupported proxy_model.ranking_role: {proxy_ranking_role!r}")
    if bool(proxy.get("required")):
        for field in ("causal_hypothesis", "null_semantics"):
            _require_text(proxy.get(field), f"proxy_model.{field}", resolved=False)
        for field in ("controls", "falsifiers"):
            values = _require_list(proxy.get(field), f"proxy_model.{field}")
            if not values:
                _fail(f"proxy_model.{field} must be non-empty when a proxy is required")

    evidence = _require_object(
        profile.get("evidence_ledger_policy"), "evidence_ledger_policy"
    )
    for field in ("veto", "support_only", "non_negative", "uncertainty"):
        _require_list(evidence.get(field), f"evidence_ledger_policy.{field}")
    reduction = _require_object(
        profile.get("output_reduction_policy"), "output_reduction_policy"
    )
    for field in (
        "candidate_union",
        "comparison_rule",
        "accounting_rule",
        "termination_rule",
        "candidate_provenance_rule",
        "proxy_independence_rule",
    ):
        _require_text(
            reduction.get(field),
            f"output_reduction_policy.{field}",
            resolved=False,
        )

    external_role = resolved_roles["external_evidence"]
    supplied_role = resolved_roles["supplied_dataset"]
    indirect_role = resolved_roles["proxies_or_indirect"]
    external_anchor = external_role == "quantitative_anchor"
    if external_role == "none" and bool(discovery.get("required")):
        _fail(
            "external discovery cannot be required when external evidence has no role"
        )
    if external_role != "none" and not bool(discovery.get("required")):
        _fail("an external evidence role requires external discovery")
    if external_anchor:
        _require_text(
            discovery.get("coverage_requirement"),
            "resource_strategy.external_discovery.coverage_requirement",
            resolved=False,
        )
        if candidate_generation_role != "primary":
            _fail(
                "an external quantitative anchor must be a primary candidate generator"
            )
        artifacts = _require_object(
            discovery.get("artifacts"),
            "resource_strategy.external_discovery.artifacts",
        )
        for field in ("resource_manifest", "candidate_prior", "coverage_audit"):
            _require_text(
                artifacts.get(field),
                f"resource_strategy.external_discovery.artifacts.{field}",
                resolved=False,
            )
        if basis_kind != "external_quantitative_prior":
            _fail(
                "external quantitative-anchor evidence requires "
                "quantitative_basis.kind=external_quantitative_prior"
            )
        transport_decisions = {
            str(item.get("quantitative_transport") or "")
            for item in transfers
            if isinstance(item, dict)
        }
        if not transport_decisions.intersection(
            {"calibrated_to_destination", "portable_ordering"}
        ):
            _fail(
                "external quantitative-anchor evidence requires calibrated or "
                "portable quantitative transport"
            )
        if (
            endpoint["measurement_portability"] == "assay_defined_quantity"
            and "calibrated_to_destination" not in transport_decisions
        ):
            _fail(
                "an assay-defined endpoint requires external calibration to "
                "the destination; a portable upstream tendency is not the "
                "requested quantitative event"
            )
        if (
            Path(str(artifacts["candidate_prior"])).name
            != Path(str(basis_artifacts["base"])).name
        ):
            _fail("external candidate_prior must be the declared quantitative basis")
        if (
            Path(str(artifacts["coverage_audit"])).name
            != Path(str(basis_artifacts["coverage_audit"])).name
        ):
            _fail("external coverage_audit must match the quantitative-basis audit")
    elif candidate_generation_role == "primary":
        _fail(
            "external evidence may generate the primary prior only when its "
            "role is quantitative_anchor"
        )
    if basis_kind == "external_quantitative_prior" and not external_anchor:
        _fail(
            "an external quantitative prior requires external evidence role "
            "quantitative_anchor"
        )
    if basis_kind == "same_experiment_derived" and supplied_role != (
        "primary_same_experiment_inferential_substrate"
    ):
        _fail(
            "a same-experiment-derived basis requires the supplied dataset to be "
            "the primary same-experiment inferential substrate"
        )
    if basis_kind == "direct_dataset_result" and supplied_role != (
        "primary_direct_measurement"
    ):
        _fail(
            "a direct dataset basis requires the supplied dataset to be the "
            "primary direct measurement"
        )
    if (
        basis_kind == "direct_dataset_result"
        and relation["dataset_observability"] != "direct"
    ):
        _fail("a direct dataset basis requires direct dataset observability")

    predicted = relation["answer_mode"] == "predicted"
    if predicted:
        if (
            relation["ledger_alignment"] in {"native", "adjacent"}
            and strategy == "none"
        ):
            _fail(
                "a predicted task with native or adjacent ledger alignment "
                "requires Claim-based relational attention"
            )
        if proxy_candidate_role == "allowed" and supplied_role != (
            "primary_same_experiment_inferential_substrate"
        ):
            _fail(
                "indirect measurements may participate in predicted candidate "
                "generation only through a declared primary same-experiment "
                "inferential substrate"
            )
        if bool(proxy.get("required")) and proxy_ranking_role not in {
            "support_only",
            "veto_or_support",
        }:
            _fail(
                "a required predicted-task proxy must be supporting or a "
                "predeclared veto/support audit"
            )
        if bool(proxy.get("required")) and indirect_role == "not_required":
            _fail("a required proxy needs an evidence role")
        reduction_artifacts = _require_object(
            reduction.get("artifacts"),
            "output_reduction_policy.artifacts",
        )
        required_reduction = [
            "candidate_evidence_ledger",
            "candidate_decisions",
            "global_ranking_audit",
        ]
        if bool(proxy.get("required")):
            required_reduction.append("proxy_independence_audit")
        for field in required_reduction:
            artifact = _require_text(
                reduction_artifacts.get(field),
                f"output_reduction_policy.artifacts.{field}",
                resolved=False,
            )
            if field == "proxy_independence_audit" and Path(artifact).suffix != ".json":
                _fail("proxy_independence_audit must be a JSON artifact")
            if field == "global_ranking_audit" and Path(artifact).suffix != ".json":
                _fail("global_ranking_audit must be a JSON artifact")
    if relation["combined"] == "in_schema_dataset_and_ledger" and bool(
        discovery.get("required")
    ):
        gap_kinds = {
            str(item.get("kind") or "") for item in gaps if isinstance(item, dict)
        }
        allowed = {"missing", "conflicting", "unresolved", "cutoff_sensitive"}
        if not gap_kinds or not gap_kinds <= allowed:
            _fail(
                "in-schema ledger tasks may use external discovery only for "
                "explicit selective gaps"
            )

    # The basis kind is the scientific decision. The family is its deterministic
    # execution projection and must never become a second field the agent has to
    # keep synchronized. A matching legacy declaration remains accepted, while
    # a contradictory one is rejected.
    downstream_family = derive_downstream_family(basis_kind)
    declared_family = str(profile.get("downstream_family") or "").strip()
    if declared_family and declared_family != "requires_semantic_review":
        if declared_family not in DOWNSTREAM_FAMILIES:
            _fail(f"unsupported downstream_family: {declared_family!r}")
        if declared_family != downstream_family:
            _fail(
                f"downstream_family={declared_family!r} contradicts "
                f"quantitative_basis.kind={basis_kind!r}"
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "valid": True,
        "task_class": task_class,
        "downstream_family": downstream_family,
        "endpoint": endpoint["name"],
        "schema_relation": relation,
        "claim_strategy": strategy,
        "output_topology": topology,
        "evidence_roles": resolved_roles,
        "quantitative_basis": basis_kind,
        "claim_attention_policy": {
            "basis_ordering_utility": ordering_utility,
            "calibration_status": calibration_status,
            "expansion_mode": expansion_mode,
            "anchor_count": integer_fields["anchor_count"],
            "related_candidate_budget": integer_fields["related_candidate_budget"],
            "full_report_budget": integer_fields["full_report_budget"],
        },
    }


class RouteDecisionError(ValueError):
    """A compact route decision cannot be compiled safely."""

    def __init__(self, errors: list[str]):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def route_decision_template(task_text: str) -> dict[str, object]:
    """Return the only routing object the model edits.

    Task parsing contributes only mechanical scope. Scientific fields remain
    explicit and unresolved; the host compiles every redundant execution field
    after the model stops.
    """

    mechanical = profile_text(task_text)
    return {
        "schema_version": ROUTE_DECISION_SCHEMA_VERSION,
        "task_class": "requires_semantic_review",
        "classification_rationale": "",
        "endpoint": {
            "name": "",
            "unit": "",
            "candidate_universe": str(
                mechanical.get("candidate_scope") or "task_defined"
            ),
            "event": "",
            "direct_observable": "",
            "inferential_operation": "",
            "context_dependence": "requires_semantic_review",
            "measurement_portability": "requires_semantic_review",
            "local_observation_stage": "requires_semantic_review",
            "event_erasure_of_local_observation": "requires_semantic_review",
            "related_but_distinct": [],
        },
        "schema": {
            "dataset_observability": "requires_semantic_review",
            "ledger_alignment": "requires_semantic_review",
            "answer_mode": "requires_semantic_review",
            "rationale": "",
        },
        "output_topology": "requires_semantic_review",
        "evidence_roles": {
            "supplied_dataset": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
            "external_evidence": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
            "proxies_or_indirect": {
                "role": "requires_semantic_review",
                "rationale": "",
            },
        },
        "basis": {
            "kind": "requires_semantic_review",
            "source": "",
            "construction": "",
            "candidate_universe_rule": "",
            "directional_relation": "",
            "rationale": "",
        },
        "claims": {
            "strategy": "requires_semantic_review",
            "anchor_count": 0,
        },
        "external_discovery": None,
        "proxy": None,
        "mechanism": None,
        "multi_hop": None,
        "handoff": {
            "basis_review_question": "",
            "replan_conditions": [],
        },
    }


def _decision_object(
    value: object,
    path: str,
    errors: list[str],
) -> dict[str, object]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def _decision_text(
    obj: dict[str, object],
    key: str,
    path: str,
    errors: list[str],
    *,
    allowed: tuple[str, ...] | None = None,
    required: bool = True,
) -> str:
    value = str(obj.get(key) or "").strip()
    if required and (not value or value == "requires_semantic_review"):
        errors.append(f"{path}.{key} must be resolved")
        return value
    if value and allowed is not None and value not in allowed:
        errors.append(f"{path}.{key} has unsupported value {value!r}")
    return value


def _decision_keys(
    obj: dict[str, object],
    path: str,
    allowed: set[str],
    errors: list[str],
) -> None:
    unexpected = sorted(set(obj) - allowed)
    if unexpected:
        errors.append(f"{path} has unknown fields: {', '.join(unexpected)}")


def _decision_string_list(
    value: object,
    path: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list of strings")
        return []
    if any(not isinstance(item, str) for item in value):
        errors.append(f"{path} must contain only strings")
    result = [item.strip() for item in value if isinstance(item, str)]
    if len(result) != len(value) or any(not item for item in result):
        errors.append(f"{path} must contain only non-empty strings")
    if nonempty and not result:
        errors.append(f"{path} must not be empty")
    return result


def derive_schema_relation_combined(
    *,
    dataset_observability: str,
    ledger_alignment: str,
    answer_mode: str,
) -> str:
    """Derive the redundant combined relation from its three source fields."""

    if answer_mode in {"direct", "derived"}:
        if (
            dataset_observability in {"direct", "proxy"}
            and ledger_alignment in {"native", "adjacent"}
        ):
            return "in_schema_dataset_and_ledger"
        if (
            dataset_observability in {"direct", "proxy"}
            and ledger_alignment in {"not_required", "absent", "incidental"}
        ):
            return "in_schema_dataset_only"
        if ledger_alignment == "native":
            return "in_schema_ledger_only"
    if answer_mode == "predicted":
        if (
            dataset_observability == "absent"
            and ledger_alignment in {"incidental", "absent", "adjacent"}
        ):
            return "out_of_schema_orthogonal"
        if (
            dataset_observability == "unobserved_context"
            and ledger_alignment in {"incidental", "absent", "adjacent"}
        ):
            return "out_of_schema_cross_context"
    raise ValueError(
        "schema fields have no legal combined relation: "
        f"dataset_observability={dataset_observability!r}, "
        f"ledger_alignment={ledger_alignment!r}, answer_mode={answer_mode!r}"
    )


def compile_schema_relation(
    schema: dict[str, object],
    *,
    basis_kind: str,
) -> dict[str, str]:
    """Compile schema inputs, canonicalizing corpus-substrate wiring.

    A corpus route always combines the experiment's direct transcriptional
    observation with a native or adjacent semantic ledger to derive the final
    judgement. Whether the requested label already appears verbatim in the
    Parquet is not a second routing decision.
    """

    dataset_observability = str(schema["dataset_observability"])
    ledger_alignment = str(schema["ledger_alignment"])
    answer_mode = str(schema["answer_mode"])
    if basis_kind == CORPUS_SUBSTRATE_KIND:
        dataset_observability = "direct"
        ledger_alignment = (
            ledger_alignment
            if ledger_alignment in {"native", "adjacent"}
            else "adjacent"
        )
        answer_mode = "derived"
    return {
        "dataset_observability": dataset_observability,
        "ledger_alignment": ledger_alignment,
        "answer_mode": answer_mode,
        "combined": derive_schema_relation_combined(
            dataset_observability=dataset_observability,
            ledger_alignment=ledger_alignment,
            answer_mode=answer_mode,
        ),
        "rationale": str(schema["rationale"]),
    }


def route_decision_errors(decision: object) -> list[str]:
    """Return every compact-contract error in one pass."""

    errors: list[str] = []
    root = _decision_object(decision, "route_decision", errors)
    if not isinstance(decision, dict):
        return errors
    allowed_top_level = {
        "schema_version",
        "task_class",
        "classification_rationale",
        "endpoint",
        "schema",
        "output_topology",
        "evidence_roles",
        "basis",
        "claims",
        "external_discovery",
        "proxy",
        "mechanism",
        "multi_hop",
        "handoff",
    }
    unexpected = sorted(set(root) - allowed_top_level)
    if unexpected:
        errors.append(
            "route_decision has compiler-owned or unknown fields: "
            + ", ".join(unexpected)
        )
    if root.get("schema_version") != ROUTE_DECISION_SCHEMA_VERSION:
        errors.append(
            "route_decision.schema_version must be "
            f"{ROUTE_DECISION_SCHEMA_VERSION!r}"
        )
    _decision_text(
        root,
        "task_class",
        "route_decision",
        errors,
        allowed=TASK_CLASSES,
    )
    _decision_text(
        root,
        "classification_rationale",
        "route_decision",
        errors,
    )

    endpoint = _decision_object(root.get("endpoint"), "endpoint", errors)
    _decision_keys(
        endpoint,
        "endpoint",
        {
            "name",
            "unit",
            "candidate_universe",
            "event",
            "direct_observable",
            "inferential_operation",
            "context_dependence",
            "measurement_portability",
            "local_observation_stage",
            "event_erasure_of_local_observation",
            "related_but_distinct",
        },
        errors,
    )
    for field in (
        "name",
        "unit",
        "candidate_universe",
        "event",
        "direct_observable",
        "inferential_operation",
    ):
        _decision_text(endpoint, field, "endpoint", errors)
    _decision_text(
        endpoint,
        "context_dependence",
        "endpoint",
        errors,
        allowed=CONTEXT_DEPENDENCE,
    )
    _decision_text(
        endpoint,
        "measurement_portability",
        "endpoint",
        errors,
        allowed=MEASUREMENT_PORTABILITY,
    )
    _decision_text(
        endpoint,
        "local_observation_stage",
        "endpoint",
        errors,
        allowed=LOCAL_OBSERVATION_STAGES,
    )
    _decision_text(
        endpoint,
        "event_erasure_of_local_observation",
        "endpoint",
        errors,
        allowed=EVENT_ERASURE_OF_LOCAL_OBSERVATION,
    )
    _decision_string_list(
        endpoint.get("related_but_distinct"),
        "endpoint.related_but_distinct",
        errors,
    )

    schema = _decision_object(root.get("schema"), "schema", errors)
    _decision_keys(
        schema,
        "schema",
        {
            "dataset_observability",
            "ledger_alignment",
            "answer_mode",
            "rationale",
        },
        errors,
    )
    dataset_observability = _decision_text(
        schema,
        "dataset_observability",
        "schema",
        errors,
        allowed=DATASET_OBSERVABILITY,
    )
    ledger_alignment = _decision_text(
        schema,
        "ledger_alignment",
        "schema",
        errors,
        allowed=LEDGER_ALIGNMENT,
    )
    answer_mode = _decision_text(
        schema,
        "answer_mode",
        "schema",
        errors,
        allowed=ANSWER_MODES,
    )
    _decision_text(schema, "rationale", "schema", errors)
    basis_hint = root.get("basis")
    corpus_basis = (
        isinstance(basis_hint, dict)
        and basis_hint.get("kind") == CORPUS_SUBSTRATE_KIND
    )
    if not corpus_basis and all(
        value and value != "requires_semantic_review"
        for value in (dataset_observability, ledger_alignment, answer_mode)
    ):
        try:
            derive_schema_relation_combined(
                dataset_observability=dataset_observability,
                ledger_alignment=ledger_alignment,
                answer_mode=answer_mode,
            )
        except ValueError as exc:
            errors.append(str(exc))

    _decision_text(
        root,
        "output_topology",
        "route_decision",
        errors,
        allowed=OUTPUT_TOPOLOGIES,
    )

    roles = _decision_object(root.get("evidence_roles"), "evidence_roles", errors)
    _decision_keys(
        roles,
        "evidence_roles",
        {"supplied_dataset", "external_evidence", "proxies_or_indirect"},
        errors,
    )
    role_values: dict[str, str] = {}
    for name, allowed in (
        ("supplied_dataset", SUPPLIED_DATASET_ROLES),
        ("external_evidence", EXTERNAL_EVIDENCE_ROLES),
        ("proxies_or_indirect", INDIRECT_EVIDENCE_ROLES),
    ):
        row = _decision_object(roles.get(name), f"evidence_roles.{name}", errors)
        _decision_keys(
            row,
            f"evidence_roles.{name}",
            {"role", "rationale"},
            errors,
        )
        role_values[name] = _decision_text(
            row,
            "role",
            f"evidence_roles.{name}",
            errors,
            allowed=allowed,
        )
        _decision_text(row, "rationale", f"evidence_roles.{name}", errors)

    basis = _decision_object(root.get("basis"), "basis", errors)
    _decision_keys(
        basis,
        "basis",
        {
            "kind",
            "source",
            "construction",
            "candidate_universe_rule",
            "directional_relation",
            "rationale",
        },
        errors,
    )
    basis_kind = _decision_text(
        basis,
        "kind",
        "basis",
        errors,
        allowed=QUANTITATIVE_BASIS_KINDS,
    )
    for field in ("source", "construction", "candidate_universe_rule", "rationale"):
        _decision_text(basis, field, "basis", errors)
    _decision_text(
        basis,
        "directional_relation",
        "basis",
        errors,
        required=basis_kind
        not in {CORPUS_SUBSTRATE_KIND, "neutral_candidate_universe"},
    )

    claims = _decision_object(root.get("claims"), "claims", errors)
    _decision_keys(
        claims,
        "claims",
        {"strategy", "anchor_count"},
        errors,
    )
    claim_strategy = _decision_text(
        claims,
        "strategy",
        "claims",
        errors,
        allowed=CLAIM_STRATEGIES,
    )
    anchor_count = claims.get("anchor_count")
    if (
        not isinstance(anchor_count, int)
        or isinstance(anchor_count, bool)
        or anchor_count < 0
    ):
        errors.append("claims.anchor_count must be a non-negative integer")
        anchor_count = 0
    if basis_kind == CORPUS_SUBSTRATE_KIND:
        if claim_strategy == "none":
            errors.append("a corpus substrate requires a non-none Claim strategy")
        if anchor_count < 1:
            errors.append("a corpus substrate requires claims.anchor_count >= 1")
    elif (
        basis_kind
        in {
            "direct_dataset_result",
            "same_experiment_derived",
            "external_quantitative_prior",
        }
        and claim_strategy not in {"", "none", "requires_semantic_review"}
        and anchor_count < 1
    ):
        errors.append("weighted Claim attention requires claims.anchor_count >= 1")

    external = root.get("external_discovery")
    external_role = role_values.get("external_evidence", "")
    if external_role == "none":
        if external is not None:
            errors.append(
                "external_discovery must be null when external_evidence.role=none"
            )
    elif external_role and external_role != "requires_semantic_review":
        row = _decision_object(external, "external_discovery", errors)
        _decision_keys(
            row,
            "external_discovery",
            {
                "resource_class",
                "selection_criteria",
                "coverage_requirement",
                "capability_gaps",
                "transfers",
            },
            errors,
        )
        _decision_text(row, "resource_class", "external_discovery", errors)
        _decision_string_list(
            row.get("selection_criteria"),
            "external_discovery.selection_criteria",
            errors,
            nonempty=True,
        )
        _decision_text(
            row,
            "coverage_requirement",
            "external_discovery",
            errors,
            required=external_role == "quantitative_anchor",
        )
        gaps = row.get("capability_gaps")
        if not isinstance(gaps, list) or not gaps:
            errors.append(
                "external_discovery.capability_gaps must be a non-empty list"
            )
        else:
            for index, gap in enumerate(gaps):
                gap_row = _decision_object(
                    gap,
                    f"external_discovery.capability_gaps[{index}]",
                    errors,
                )
                _decision_keys(
                    gap_row,
                    f"external_discovery.capability_gaps[{index}]",
                    {"kind", "question"},
                    errors,
                )
                kind = _decision_text(
                    gap_row,
                    "kind",
                    f"external_discovery.capability_gaps[{index}]",
                    errors,
                )
                if kind and kind not in {
                    "missing",
                    "conflicting",
                    "unresolved",
                    "cutoff_sensitive",
                }:
                    errors.append(
                        "external_discovery.capability_gaps"
                        f"[{index}].kind is unsupported: {kind!r}"
                    )
                _decision_text(
                    gap_row,
                    "question",
                    f"external_discovery.capability_gaps[{index}]",
                    errors,
                )
        transfers = row.get("transfers")
        if not isinstance(transfers, list) or not transfers:
            errors.append("external_discovery.transfers must be a non-empty list")
        else:
            for index, transfer in enumerate(transfers):
                item = _decision_object(
                    transfer,
                    f"external_discovery.transfers[{index}]",
                    errors,
                )
                _decision_keys(
                    item,
                    f"external_discovery.transfers[{index}]",
                    {
                        "source",
                        "what_it_explains",
                        "transfer_caveats",
                        "residual_questions",
                        "quantitative_transport",
                    },
                    errors,
                )
                _decision_text(
                    item,
                    "source",
                    f"external_discovery.transfers[{index}]",
                    errors,
                )
                for field in (
                    "what_it_explains",
                    "transfer_caveats",
                    "residual_questions",
                ):
                    _decision_string_list(
                        item.get(field),
                        f"external_discovery.transfers[{index}].{field}",
                        errors,
                        nonempty=True,
                    )
                _decision_text(
                    item,
                    "quantitative_transport",
                    f"external_discovery.transfers[{index}]",
                    errors,
                    allowed=QUANTITATIVE_TRANSPORT,
                )

    if (
        basis_kind == "external_quantitative_prior"
        and external_role != "quantitative_anchor"
    ):
        errors.append(
            "external_quantitative_prior requires "
            "external_evidence.role=quantitative_anchor"
        )
    if (
        basis_kind == "direct_dataset_result"
        and role_values.get("supplied_dataset") != "primary_direct_measurement"
    ):
        errors.append(
            "direct_dataset_result requires "
            "supplied_dataset.role=primary_direct_measurement"
        )
    if basis_kind == "direct_dataset_result" and dataset_observability != "direct":
        errors.append("direct_dataset_result requires dataset_observability=direct")
    if (
        basis_kind == "same_experiment_derived"
        and role_values.get("supplied_dataset")
        != "primary_same_experiment_inferential_substrate"
    ):
        errors.append(
            "same_experiment_derived requires supplied_dataset.role="
            "primary_same_experiment_inferential_substrate"
        )

    proxy = root.get("proxy")
    if proxy is not None:
        row = _decision_object(proxy, "proxy", errors)
        _decision_keys(
            row,
            "proxy",
            {
                "required",
                "causal_hypothesis",
                "controls",
                "falsifiers",
                "null_semantics",
                "candidate_generation_role",
                "ranking_role",
            },
            errors,
        )
        required = row.get("required")
        if not isinstance(required, bool):
            errors.append("proxy.required must be boolean")
        _decision_text(
            row,
            "candidate_generation_role",
            "proxy",
            errors,
            allowed=PROXY_CANDIDATE_ROLES,
        )
        _decision_text(
            row,
            "ranking_role",
            "proxy",
            errors,
            allowed=PROXY_RANKING_ROLES,
        )
        if required is True:
            for field in ("causal_hypothesis", "null_semantics"):
                _decision_text(row, field, "proxy", errors)
            for field in ("controls", "falsifiers"):
                _decision_string_list(
                    row.get(field),
                    f"proxy.{field}",
                    errors,
                    nonempty=True,
                )

    handoff = _decision_object(root.get("handoff"), "handoff", errors)
    _decision_keys(
        handoff,
        "handoff",
        {"basis_review_question", "replan_conditions"},
        errors,
    )
    _decision_text(
        handoff,
        "basis_review_question",
        "handoff",
        errors,
    )
    _decision_string_list(
        handoff.get("replan_conditions"),
        "handoff.replan_conditions",
        errors,
        nonempty=True,
    )

    return errors


def validate_route_decision(decision: object) -> dict[str, object]:
    """Validate a compact decision and report all errors together."""

    errors = route_decision_errors(decision)
    if errors:
        raise RouteDecisionError(errors)
    root = decision if isinstance(decision, dict) else {}
    return {
        "schema_version": ROUTE_DECISION_SCHEMA_VERSION,
        "valid": True,
        "task_class": root.get("task_class"),
        "output_topology": root.get("output_topology"),
        "basis_kind": _decision_object(root.get("basis"), "basis", []).get("kind"),
        "claim_strategy": _decision_object(
            root.get("claims"), "claims", []
        ).get("strategy"),
    }


def _artifact_name(
    artifact_contract: dict[str, object],
    key: str,
    errors: list[str],
) -> str:
    value = str(artifact_contract.get(key) or "").strip()
    if not value:
        errors.append(f"artifact_contract.{key} must be non-empty")
    return value


def compile_route_decision(
    decision: dict[str, object],
    *,
    task_text: str,
    artifact_contract: dict[str, object],
) -> dict[str, object]:
    """Compile one scientific decision into the existing full v4 profile."""

    validate_route_decision(decision)
    artifact_errors: list[str] = []
    artifacts = {
        key: _artifact_name(artifact_contract, key, artifact_errors)
        for key in (
            "basis",
            "coverage_audit",
            "corpus_slice_plan",
            "resource_manifest",
            "candidate_evidence_ledger",
            "candidate_decisions",
            "global_ranking_audit",
            "proxy_independence_audit",
            "claim_path_audit",
            "claim_candidate_summary",
        )
    }
    if artifact_errors:
        raise RouteDecisionError(artifact_errors)

    task_class = str(decision["task_class"])
    profile = profile_text(task_text, override=task_class)
    endpoint = dict(decision["endpoint"])
    schema = dict(decision["schema"])
    roles = dict(decision["evidence_roles"])
    basis_decision = dict(decision["basis"])
    claims = dict(decision["claims"])
    basis_kind = str(basis_decision["kind"])
    claim_strategy = str(claims["strategy"])
    anchor_count = int(claims["anchor_count"])
    topology = str(decision["output_topology"])

    profile["classification_confidence"] = "resolved"
    profile["classification_rationale"] = str(
        decision["classification_rationale"]
    )
    profile["classification_signals"] = [
        f"output_topology={topology}",
        f"basis_kind={basis_kind}",
        f"dataset_observability={schema['dataset_observability']}",
        f"ledger_alignment={schema['ledger_alignment']}",
    ]
    profile["endpoint_definition"] = {
        "name": endpoint["name"],
        "unit": endpoint["unit"],
        "candidate_universe": endpoint["candidate_universe"],
        "event": endpoint["event"],
        "direct_observable": endpoint["direct_observable"],
        "inferential_operation": endpoint["inferential_operation"],
        "context_dependence": endpoint["context_dependence"],
        "measurement_portability": endpoint["measurement_portability"],
        "local_observation_stage": endpoint["local_observation_stage"],
        "event_erasure_of_local_observation": endpoint[
            "event_erasure_of_local_observation"
        ],
        "related_but_distinct": list(endpoint["related_but_distinct"]),
    }
    profile["schema_relation"] = compile_schema_relation(
        schema,
        basis_kind=basis_kind,
    )
    output_contract = dict(profile["output_contract"])
    output_contract["topology"] = topology
    profile["output_contract"] = output_contract
    profile["claim_strategy"] = claim_strategy
    profile["claim_recall_required"] = claim_strategy != "none"

    external = decision.get("external_discovery")
    external_row = dict(external) if isinstance(external, dict) else None
    external_role = str(dict(roles["external_evidence"])["role"])
    discovery_required = external_row is not None
    candidate_generation_role = (
        "primary"
        if external_role == "quantitative_anchor"
        else "supplementary"
        if discovery_required
        else "not_required"
    )
    profile["resource_strategy"] = {
        "installed_skill_roles": (
            [
                {
                    "skill": "findings-corpus",
                    "role": "primary experiment-interpretation substrate",
                }
            ]
            if basis_kind == CORPUS_SUBSTRATE_KIND
            else []
        ),
        "capability_gaps": (
            list(external_row["capability_gaps"]) if external_row else []
        ),
        "external_discovery": {
            "required": discovery_required,
            "resource_class": (
                str(external_row["resource_class"]) if external_row else ""
            ),
            "selection_criteria": (
                list(external_row["selection_criteria"]) if external_row else []
            ),
            "coverage_requirement": (
                str(external_row.get("coverage_requirement") or "")
                if external_row
                else ""
            ),
            "candidate_generation_role": candidate_generation_role,
            "artifacts": {
                "resource_manifest": artifacts["resource_manifest"],
                "candidate_prior": artifacts["basis"],
                "coverage_audit": artifacts["coverage_audit"],
            },
        },
        "acquisition_policy": "data_only_https",
    }
    profile["evidence_role_resolution"] = {
        name: dict(roles[name])
        for name in (
            "supplied_dataset",
            "external_evidence",
            "proxies_or_indirect",
        )
    }

    scalar_basis = basis_kind in {
        "direct_dataset_result",
        "same_experiment_derived",
        "external_quantitative_prior",
    }
    if scalar_basis:
        ordering_decision = "eligible"
        value_semantics = "comparable"
        erasure_risk = "absent"
        directional_relation = str(basis_decision["directional_relation"])
    elif basis_kind == CORPUS_SUBSTRATE_KIND:
        ordering_decision = "neutral"
        value_semantics = "not_applicable"
        erasure_risk = "not_applicable"
        directional_relation = "not applicable; the corpus substrate is unordered"
    else:
        ordering_decision = "neutral"
        value_semantics = "not_comparable"
        erasure_risk = "not_applicable"
        directional_relation = (
            str(basis_decision.get("directional_relation") or "")
            or "no eligible candidate ordering is available"
        )
    profile["quantitative_basis"] = {
        "kind": basis_kind,
        "source": basis_decision["source"],
        "construction": basis_decision["construction"],
        "candidate_universe_rule": basis_decision["candidate_universe_rule"],
        "ordering_identifiability": {
            "decision": ordering_decision,
            "directional_relation": directional_relation,
            "rationale": basis_decision["rationale"],
            "endpoint_erasure_risk": erasure_risk,
            "candidate_value_semantics": value_semantics,
        },
        "acquisition_failure_policy": (
            "select_another_eligible_basis_or_use_neutral_candidate_universe"
        ),
        "artifacts": {
            "base": "" if basis_kind == CORPUS_SUBSTRATE_KIND else artifacts["basis"],
            "corpus_slice_plan": (
                artifacts["corpus_slice_plan"]
                if basis_kind == CORPUS_SUBSTRATE_KIND
                else ""
            ),
            "coverage_audit": artifacts["coverage_audit"],
        },
    }

    if basis_kind == CORPUS_SUBSTRATE_KIND:
        expansion_mode = "fanout"
        ordering_utility = "not_applicable"
        calibration_status = "not_applicable"
        related_budget = 0
        full_report_budget = 0
        precision_fraction = 0.0
        diversity_fraction = 0.0
    elif claim_strategy == "none" or basis_kind == "neutral_candidate_universe":
        expansion_mode = "none"
        ordering_utility = (
            "weak_or_neutral"
            if basis_kind == "neutral_candidate_universe"
            else "defensible"
        )
        calibration_status = (
            "known" if basis_kind == "direct_dataset_result" else "unknown"
        )
        anchor_count = 0
        related_budget = 0
        full_report_budget = 0
        precision_fraction = 0.0
        diversity_fraction = 0.0
    else:
        expansion_mode = "weighted_one_hop"
        ordering_utility = "defensible"
        calibration_status = (
            "known" if basis_kind == "direct_dataset_result" else "unknown"
        )
        related_budget = min(50, (anchor_count + 1) // 2)
        union_size = anchor_count + related_budget
        full_report_budget = min(20, max(1, (union_size + 9) // 10))
        precision_fraction = 0.8
        diversity_fraction = 0.2
    profile["claim_attention_policy"] = {
        "basis_ordering_utility": ordering_utility,
        "basis_ordering_rationale": (
            "The compiler derives attention eligibility from the selected "
            "basis and Claim strategy."
        ),
        "calibration_status": calibration_status,
        "expansion_mode": expansion_mode,
        "anchor_count": anchor_count,
        "related_candidate_budget": related_budget,
        "full_report_budget": full_report_budget,
        "precision_fraction": precision_fraction,
        "diversity_fraction": diversity_fraction,
        "artifacts": {
            "path_audit": artifacts["claim_path_audit"],
            "candidate_summary": artifacts["claim_candidate_summary"],
        },
    }

    transfers = []
    if external_row:
        for transfer in external_row["transfers"]:
            item = dict(transfer)
            transfers.append(
                {
                    **item,
                    "decision_criteria": {
                        "promote": ["source evidence supports the requested endpoint"],
                        "retain": ["support is relevant but context-limited"],
                        "down_rank": ["source context weakens transport"],
                        "reject": ["source measures the wrong endpoint"],
                    },
                }
            )
    profile["external_transfer"] = transfers
    profile["candidate_decision_policy"] = {
        "promote": ["direct support for the requested endpoint"],
        "retain": ["relevant evidence with unresolved uncertainty"],
        "down_rank": ["material alternative explanation or context mismatch"],
        "reject": ["evidence falsifies the requested endpoint link"],
    }
    mechanism = decision.get("mechanism")
    profile["mechanism_model"] = (
        dict(mechanism)
        if isinstance(mechanism, dict)
        else {
            "families": [],
            "not_required_reason": (
                "Mechanism construction is deferred unless the route decision "
                "declares a mechanism model."
            ),
        }
    )
    multi_hop = decision.get("multi_hop")
    profile["multi_hop_model"] = (
        dict(multi_hop)
        if isinstance(multi_hop, dict)
        else {
            "forward": [],
            "reverse": [],
            "not_required_reason": (
                "Multi-hop construction is deferred unless the route decision "
                "declares it."
            ),
        }
    )
    proxy = decision.get("proxy")
    profile["proxy_model"] = (
        dict(proxy)
        if isinstance(proxy, dict)
        else {
            "required": False,
            "causal_hypothesis": "",
            "controls": [],
            "falsifiers": [],
            "null_semantics": "",
            "candidate_generation_role": "not_applicable",
            "ranking_role": "not_applicable",
        }
    )
    profile["evidence_ledger_policy"] = {
        "veto": ["direct contradiction to the requested endpoint"],
        "support_only": ["context or mechanism evidence without direct measurement"],
        "non_negative": ["missing or unannotated evidence"],
        "uncertainty": ["power, context, or transfer limitations"],
    }
    exhaustive = topology in {"exhaustive_classification", "direct_measurement"}
    profile["output_reduction_policy"] = {
        "candidate_union": str(endpoint["candidate_universe"]),
        "comparison_rule": (
            "apply the task taxonomy to each eligible unit"
            if topology == "exhaustive_classification"
            else "compare candidates only after evidence collection"
        ),
        "accounting_rule": (
            "every eligible unit receives exactly one disposition"
            if exhaustive
            else "every reported candidate retains a disposition and provenance"
        ),
        "termination_rule": (
            "the declared deliverables are complete and accounting is exact"
        ),
        "candidate_provenance_rule": (
            "retain the source and evidence role for every reported unit"
        ),
        "proxy_independence_rule": (
            "No proxy ranking is used."
            if not bool(profile["proxy_model"].get("required"))
            else "Audit proxy contribution independently from the primary basis."
        ),
        "artifacts": {
            "candidate_evidence_ledger": artifacts[
                "candidate_evidence_ledger"
            ],
            "candidate_decisions": artifacts["candidate_decisions"],
            "global_ranking_audit": artifacts["global_ranking_audit"],
            "proxy_independence_audit": artifacts[
                "proxy_independence_audit"
            ],
        },
    }
    validate_profile(profile)
    return profile


def vocabularies() -> dict[str, list[str]]:
    """Every closed vocabulary and cross-field rule, by constant name.

    `--validate` raises on the first bad field and names it without naming its
    legal values, so recovering a vocabulary meant reading this file. A routing
    agent did exactly that -- roughly 800 lines of source across four `sed`
    calls, plus guess loops against enums and legal cross-field combinations --
    to learn what one command can print.
    """

    module = globals()
    return {
        name: list(value)
        for name, value in sorted(module.items())
        if name.isupper()
        and isinstance(value, (tuple, frozenset, set))
        and value
        and all(isinstance(item, str) for item in value)
    }


def route_decision_vocabulary() -> dict[str, list[str]]:
    """Return only closed choices that the compact decision may contain."""

    def resolved(values: tuple[str, ...]) -> list[str]:
        return [value for value in values if value != "requires_semantic_review"]

    return {
        "task_class": resolved(TASK_CLASSES),
        "endpoint.context_dependence": resolved(CONTEXT_DEPENDENCE),
        "endpoint.measurement_portability": resolved(MEASUREMENT_PORTABILITY),
        "endpoint.local_observation_stage": resolved(LOCAL_OBSERVATION_STAGES),
        "endpoint.event_erasure_of_local_observation": resolved(
            EVENT_ERASURE_OF_LOCAL_OBSERVATION
        ),
        "schema.dataset_observability": resolved(DATASET_OBSERVABILITY),
        "schema.ledger_alignment": resolved(LEDGER_ALIGNMENT),
        "schema.answer_mode": resolved(ANSWER_MODES),
        "output_topology": resolved(OUTPUT_TOPOLOGIES),
        "evidence_roles.supplied_dataset.role": resolved(SUPPLIED_DATASET_ROLES),
        "evidence_roles.external_evidence.role": resolved(EXTERNAL_EVIDENCE_ROLES),
        "evidence_roles.proxies_or_indirect.role": resolved(
            INDIRECT_EVIDENCE_ROLES
        ),
        "basis.kind": resolved(QUANTITATIVE_BASIS_KINDS),
        "claims.strategy": resolved(CLAIM_STRATEGIES),
        "external_discovery.capability_gaps[].kind": [
            "missing",
            "conflicting",
            "unresolved",
            "cutoff_sensitive",
        ],
        "external_discovery.transfers[].quantitative_transport": resolved(
            QUANTITATIVE_TRANSPORT
        ),
        "proxy.candidate_generation_role": resolved(PROXY_CANDIDATE_ROLES),
        "proxy.ranking_role": resolved(PROXY_RANKING_ROLES),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--task", type=Path)
    mode.add_argument("--validate", type=Path)
    mode.add_argument("--decision-template", type=Path, metavar="TASK")
    mode.add_argument("--validate-decision", type=Path)
    mode.add_argument(
        "--vocabulary",
        action="store_true",
        help="print every closed vocabulary and cross-field rule as JSON and exit",
    )
    mode.add_argument(
        "--decision-vocabulary",
        action="store_true",
        help="print only compact route-decision vocabularies as JSON and exit",
    )
    parser.add_argument("--out", type=Path)
    parser.add_argument("--task-class", choices=TASK_CLASSES)
    args = parser.parse_args()

    if args.vocabulary:
        print(json.dumps(vocabularies(), indent=2, sort_keys=True))
        return 0
    if args.decision_vocabulary:
        print(json.dumps(route_decision_vocabulary(), indent=2, sort_keys=True))
        return 0
    if args.validate:
        profile = json.loads(args.validate.read_text(encoding="utf-8"))
        print(json.dumps(validate_profile(profile), indent=2, sort_keys=True))
        return 0
    if args.validate_decision:
        decision = json.loads(args.validate_decision.read_text(encoding="utf-8"))
        try:
            result = validate_route_decision(decision)
        except RouteDecisionError as exc:
            print(
                json.dumps(
                    {"valid": False, "errors": exc.errors},
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.out is None:
        parser.error("--out is required with --task or --decision-template")
    if args.decision_template:
        decision = route_decision_template(
            args.decision_template.read_text(encoding="utf-8")
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(decision, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0
    profile = profile_text(
        args.task.read_text(encoding="utf-8"),
        override=args.task_class,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(profile, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(profile, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
