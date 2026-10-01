"""Task-general context and structural diagnostics for direct/adaptive queries."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..corpus.registry import CorpusRegistryError, CorpusRelease, get_release
from ..skills.registry import RUNTIME_SKILLS_DIR
from .capabilities import (
    CAPABILITIES,
    CAPABILITIES_SCHEMA,
    CAPABILITY_INTERFACES,
    native_corpus_tools_for_release,
)
from .input_binding import build_task_bindings
from .measurement_registry import build_measurement_registry


@dataclass(frozen=True)
class AdaptiveContext:
    skill_path: Path
    capability_manifest: Path
    coverage: Path | None
    preparation: dict[str, Any]


def _project_skill_path(skills_destination: str, skill_name: str) -> Path:
    root = Path(skills_destination).expanduser().resolve()
    candidates = (
        root / "runtime" / skill_name,
        root / "distributed_agents" / skill_name,
        root / skill_name,
        RUNTIME_SKILLS_DIR / skill_name,
    )
    for candidate in candidates:
        if (candidate / "SKILL.md").is_file():
            return candidate.resolve()
    return candidates[0]


def _adaptive_skill_path(skills_destination: str) -> Path:
    candidate = _project_skill_path(skills_destination, "adaptive-query-skill")
    if not (candidate / "SKILL.md").is_file():
        raise FileNotFoundError("adaptive-query-skill is not installed")
    return candidate


def _path_or_none(value: str | None, fallback: Path) -> Path | None:
    candidate = Path(value).expanduser().resolve() if value else fallback.resolve()
    return candidate if candidate.is_file() else None


def _first_existing(*paths: Path) -> Path | None:
    return next((path for path in paths if path.is_file()), None)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_provenance(path: Path) -> dict[str, Any]:
    present = path.is_file()
    return {
        "path": str(path),
        "present": present,
        "sha256": _sha256(path) if present else None,
    }


def _neo4j_runtime_readiness(
    runtime_env: dict[str, str],
    *,
    probe_http_url: str | None = None,
    timeout_s: float = 2.0,
) -> dict[str, Any]:
    """Probe Neo4j before model execution while advertising its runtime URL.

    A protected run exposes Neo4j to the networkless model through a loopback
    relay that does not exist until the model sandbox starts. In that case
    ``probe_http_url`` is the host-reachable upstream while the URL in
    ``runtime_env`` remains the endpoint the model can actually use.
    """

    http_url = runtime_env.get("BIOKG_NEO4J_HTTP_URL", "").strip()
    if not http_url:
        return {
            "configured": False,
            "runtime_ready": False,
            "reason": "host Neo4j HTTP service is not configured",
        }
    database = runtime_env.get("BIOKG_NEO4J_DATABASE", "neo4j")
    user = runtime_env.get("BIOKG_NEO4J_USER", "neo4j")
    password = runtime_env.get("BIOKG_NEO4J_PASSWORD", "biokgpassword")
    endpoint = f"{http_url.rstrip('/')}/db/{database}/tx/commit"
    probe_base_url = (probe_http_url or http_url).strip()
    probe_endpoint = f"{probe_base_url.rstrip('/')}/db/{database}/tx/commit"
    credentials = base64.b64encode(f"{user}:{password}".encode()).decode()
    expected_nodes = runtime_env.get("DISTRIBUTED_AGENTS_EXPECTED_GRAPH_NODES", "").strip()
    expected_relationships = runtime_env.get(
        "DISTRIBUTED_AGENTS_EXPECTED_GRAPH_RELATIONSHIPS", ""
    ).strip()
    statements = [
        {"statement": "RETURN 1 AS ready", "parameters": {}},
        {
            "statement": "MATCH (:TargetGene)-[:HAS_FINDING]->(:Finding)-[:REPORTS_GENE]->(:Gene) RETURN 1 AS ready LIMIT 1",
            "parameters": {},
        },
    ]
    if expected_nodes and expected_relationships:
        statements.append(
            {
                "statement": (
                    "MATCH (n:BioKGNode) WITH count(n) AS nodes "
                    "MATCH (:BioKGNode)-[r]->(:BioKGNode) "
                    "RETURN nodes, count(r) AS relationships"
                ),
                "parameters": {},
            }
        )
    request = urllib.request.Request(
        probe_endpoint,
        data=json.dumps({"statements": statements}).encode(),
        method="POST",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError, urllib.error.URLError) as exc:
        result = {
            "configured": True,
            "runtime_ready": False,
            "endpoint": endpoint,
            "reason": f"host Neo4j preflight failed: {type(exc).__name__}",
        }
        if probe_endpoint != endpoint:
            result["probe_endpoint"] = probe_endpoint
        return result
    errors = payload.get("errors") or []
    results = payload.get("results") or []

    def statement_ready(index: int) -> bool:
        rows = results[index].get("data") if len(results) > index else []
        return not errors and bool(rows) and rows[0].get("row") == [1]

    identity_ready = True
    if expected_nodes and expected_relationships:
        rows = results[2].get("data") if len(results) > 2 else []
        identity_ready = bool(
            not errors
            and rows
            and rows[0].get("row")
            == [int(expected_nodes), int(expected_relationships)]
        )
    service_ready = statement_ready(0) and identity_ready
    direct_evidence_ready = service_ready and statement_ready(1)
    result = {
        "configured": True,
        "runtime_ready": service_ready,
        "direct_evidence_ready": direct_evidence_ready,
        "endpoint": endpoint,
        "reason": (
            None
            if service_ready
            else (
                "host Neo4j graph does not match the selected release"
                if statement_ready(0) and not identity_ready
                else "host Neo4j preflight returned no service-ready row"
            )
        ),
        "direct_evidence_reason": (
            None
            if direct_evidence_ready
            else "BioKG direct-evidence relationship chain is not ready"
        ),
    }
    if probe_endpoint != endpoint:
        result["probe_endpoint"] = probe_endpoint
    return result


def _release_entrypoint(
    release: CorpusRelease,
    role: str,
    name: str,
) -> Path | None:
    """Return a declared release entrypoint, or None when the role is unsupported."""

    try:
        return release.skill_entrypoint(role, name)
    except CorpusRegistryError:
        return None


def _release_artifact(
    release: CorpusRelease,
    name: str,
    fallback: Path,
) -> Path:
    """Return a declared release artifact, retaining legacy path compatibility."""

    try:
        return release.artifact(name)
    except CorpusRegistryError:
        return fallback


def _release_artifact_schema(
    release: CorpusRelease,
    name: str,
    fallback: Path,
) -> Path:
    """Return the declared schema for an artifact when the release supplies one."""

    spec = release.manifest.get("artifacts", {}).get(name, {})
    relative = spec.get("schema") if isinstance(spec, dict) else None
    return release.resolve(str(relative)) if relative else fallback


def _configure_graph_identity_preflight(
    release: CorpusRelease,
    runtime_env: dict[str, str],
) -> None:
    """Declare exact graph totals when a release ships accepted build records."""

    try:
        node_build = json.loads(release.artifact("biokg_node_build").read_text())
        relationship_build = json.loads(
            release.artifact("biokg_relationship_build").read_text()
        )
        nodes = int(node_build["output"]["records"])
        relationships = int(relationship_build["output"]["records"])
    except (CorpusRegistryError, OSError, ValueError, KeyError, json.JSONDecodeError):
        return
    runtime_env["DISTRIBUTED_AGENTS_EXPECTED_GRAPH_NODES"] = str(nodes)
    runtime_env["DISTRIBUTED_AGENTS_EXPECTED_GRAPH_RELATIONSHIPS"] = str(relationships)


def prepare_adaptive_context(
    *,
    mode: str,
    release: CorpusRelease | None = None,
    task_path: Path,
    dataset_context_path: Path,
    pipeline_dir: Path,
    skills_destination: str,
    runtime_env: dict[str, str],
    input_roots: tuple[Path, ...],
    declared_inputs: tuple[Path, ...] | None = None,
    capability_preflight: dict[str, object] | None = None,
    biokg_preflight_http_url: str | None = None,
) -> AdaptiveContext:
    """Write the stable capability manifest and optional pre-plan coverage."""

    if mode not in {"direct", "adaptive"}:
        raise ValueError(f"unsupported adaptive context mode: {mode!r}")
    started = time.monotonic()
    pipeline_dir.mkdir(parents=True, exist_ok=True)
    skill_path = _adaptive_skill_path(skills_destination)
    release = release or get_release()
    packaged_skills = (
        Path(skills_destination).expanduser().resolve()
        == RUNTIME_SKILLS_DIR.parent.resolve()
    )
    if packaged_skills:
        ledger_skill = release.skill("ledger")
        findings_query = _release_entrypoint(release, "ledger", "query")
        calibration_query = _release_entrypoint(release, "ledger", "calibration")
        evidence_resolver = _release_entrypoint(
            release, "ledger", "resolve_evidence"
        )
        relational_query = _release_entrypoint(
            release, "relational_candidates", "query"
        )
        predictive_graph_review = _release_entrypoint(
            release, "relational_candidates", "predictive_review"
        )
        release_direct_evidence = _release_entrypoint(
            release, "direct_evidence", "query"
        )
        graph_query = _release_entrypoint(release, "graph", "query")
    else:
        ledger_skill = _project_skill_path(
            skills_destination, "findings-ledger-skill"
        )
        relational_skill = _project_skill_path(
            skills_destination, "relational-candidate-skill"
        )
        graph_skill = _project_skill_path(skills_destination, "biokg-recall-skill")
        findings_query = _first_existing(
            ledger_skill / "scripts" / "query_corpus.py",
            ledger_skill / "scripts" / "query_findings.py",
            ledger_skill / "scripts" / "query_ledger.py",
        )
        calibration_query = _first_existing(
            ledger_skill / "scripts" / "query_corpus.py"
        )
        evidence_resolver = _first_existing(
            ledger_skill / "scripts" / "resolve_evidence.py"
        )
        relational_query = _first_existing(
            relational_skill / "scripts" / "relational_candidates.py"
        )
        predictive_graph_review = _first_existing(
            relational_skill / "scripts" / "predictive_graph_review.py"
        )
        release_direct_evidence = _first_existing(
            relational_skill / "scripts" / "direct_evidence.py"
        )
        graph_query = _first_existing(
            graph_skill / "scripts" / "biokg_cypher.py",
            graph_skill / "scripts" / "query_graph.py",
        )
    ledger_calibration_path = _release_artifact(
        release,
        "ledger_calibration",
        ledger_skill / "scripts" / "out" / "ledger_calibration.json",
    )
    value_dictionary_path = _release_artifact(
        release,
        "value_dictionary",
        ledger_skill / "scripts" / "out" / "value_dictionary.csv",
    )
    calibration_schema_path = _release_artifact_schema(
        release,
        "ledger_calibration",
        ledger_skill / "schemas" / "ledger_calibration.schema.json",
    )
    findings = _path_or_none(
        runtime_env.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER"),
        release.artifact("findings"),
    )
    reports = _path_or_none(
        runtime_env.get("BIOKG_REPORTS_PATH"),
        release.artifact("reports"),
    )
    biokg = release.projection("biokg")
    assignments = _release_artifact(
        release,
        "claim_assignments",
        biokg / "data" / "claims" / "claim_assignments.tsv",
    )
    relations = _release_artifact(
        release,
        "claim_relations",
        biokg / "data" / "claims" / "claim_relations.tsv",
    )
    analog_index = _release_artifact(
        release,
        "gene_analog_index",
        release.root / "artifacts" / "indexes" / "gene_analogs.sqlite3",
    )
    measurement_registry_path = pipeline_dir / "measurement_registry.json"
    measurement_registry_path.write_text(
        json.dumps(build_measurement_registry(input_roots), indent=2) + "\n"
    )
    task_bindings_path = pipeline_dir / "task_bindings.json"
    task_bindings = build_task_bindings(
        task_path,
        input_roots if declared_inputs is None else declared_inputs,
    )
    task_bindings_path.write_text(json.dumps(task_bindings, indent=2) + "\n")
    workbench_script = skill_path / "scripts" / "perturbseq_feature_workbench.py"
    direct_evidence_script = release_direct_evidence or (
        skill_path / "scripts" / "direct_evidence_slice.py"
    )
    direct_evidence_requires_graph = release_direct_evidence is None
    task_metadata = task_bindings.get("task") or {}
    supplied_ranked_supervision = any(
        row.get("active_for_coverage")
        and (row.get("ordering") or {}).get("kind") in {"ranked", "partial_ranked"}
        for row in task_bindings.get("entity_sets") or []
        if isinstance(row, dict)
    )
    predictive_ranking = bool(
        supplied_ranked_supervision
        and task_metadata.get("prediction_requested")
        and task_metadata.get("ranking_requested")
    )
    if predictive_ranking:
        # The narrative Finding text is not a valid adjudication surface for this
        # task.  Carry the policy into the child runtime so a model cannot bypass
        # the capability manifest by invoking a mounted legacy query script.
        runtime_env["DISTRIBUTED_AGENTS_DISABLE_FINDING_SUMMARIES"] = "1"
    dataset_path = next(
        (path for path in input_roots if path.suffix.casefold() == ".parquet"),
        None,
    )

    coverage_path: Path | None = None
    command: list[str] | None = None
    if mode == "adaptive":
        coverage_path = pipeline_dir / "coverage.json"
        command = [
            sys.executable,
            str(skill_path / "scripts" / "coverage_probe.py"),
            "--task",
            str(task_path),
            "--out",
            str(coverage_path),
            "--bindings",
            str(task_bindings_path),
        ]
        for flag, value in (
            ("--findings-ledger", findings),
            ("--claim-assignments", assignments if assignments.is_file() else None),
            ("--claim-relations", relations if relations.is_file() else None),
            ("--reports", reports),
        ):
            if value is not None:
                command.extend((flag, str(value)))
        done = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if done.returncode:
            coverage_path.write_text(
                json.dumps(
                    {
                        "schema_version": "distributed_agents-evidence-coverage-v1",
                        "status": "unavailable",
                        "error": (done.stderr or done.stdout)[-4000:],
                        "entities": {"gene_targets": [], "gene_target_count": 0},
                        "sources": {},
                    },
                    indent=2,
                )
                + "\n"
            )
    entrypoints = {
        "task.bindings": task_bindings_path,
        "corpus.findings": findings_query,
        "corpus.target_analogs": None,
        "corpus.calibration": calibration_query,
        "corpus.report_evidence": evidence_resolver,
        "corpus.direct_evidence": direct_evidence_script,
        "corpus.relational_candidates": relational_query,
        "corpus.predictive_graph_review": predictive_graph_review,
        "corpus.claim_relations": assignments,
        "corpus.graph": graph_query,
        "corpus.coverage": coverage_path,
        "dataset.measurements": measurement_registry_path,
        "dataset.query": dataset_path,
        "dataset.perturbseq_features": workbench_script,
        "synthesis.ordering_validate": workbench_script,
    }
    _configure_graph_identity_preflight(release, runtime_env)
    if biokg_preflight_http_url is None:
        neo4j_preflight = _neo4j_runtime_readiness(runtime_env)
    else:
        neo4j_preflight = _neo4j_runtime_readiness(
            runtime_env,
            probe_http_url=biokg_preflight_http_url,
        )
    installation_state = {
        "task.bindings": (task_bindings_path.is_file(), None),
        "corpus.coverage": (
            coverage_path is not None and coverage_path.is_file(),
            "coverage is generated only for adaptive mode",
        ),
        "corpus.findings": (
            findings_query is not None
            and findings_query.is_file()
            and findings is not None,
            "no declared Findings ledger is available",
        ),
        "corpus.target_analogs": (
            analog_index.is_file(),
            "the selected release has no frozen target-analog annotation index",
        ),
        "corpus.calibration": (
            calibration_query is not None and calibration_query.is_file(),
            "the selected release has no calibration-query entrypoint",
        ),
        "corpus.claim_relations": (
            assignments.is_file() and relations.is_file(),
            "packaged Claim assignments or relations are unavailable",
        ),
        "corpus.graph": (
            graph_query is not None and graph_query.is_file(),
            "the selected release has no graph-query entrypoint",
        ),
        "corpus.report_evidence": (
            evidence_resolver is not None
            and evidence_resolver.is_file()
            and reports is not None,
            "no declared report ledger is available",
        ),
        "corpus.direct_evidence": (
            direct_evidence_script.is_file()
            and (
                not direct_evidence_requires_graph
                or (graph_query is not None and graph_query.is_file())
            ),
            "the selected release has no direct-evidence entrypoint or required graph query capability",
        ),
        "corpus.relational_candidates": (
            relational_query is not None
            and relational_query.is_file()
            and findings is not None,
            "relational tool or declared Findings substrate is unavailable",
        ),
        "corpus.predictive_graph_review": (
            predictive_graph_review is not None
            and predictive_graph_review.is_file()
            and findings is not None,
            "the selected release has no predictive-review entrypoint or Findings substrate",
        ),
        "dataset.query": (
            dataset_path is not None and dataset_path.is_file(),
            "no declared Parquet input is available",
        ),
        "dataset.measurements": (measurement_registry_path.is_file(), None),
        "dataset.perturbseq_features": (
            workbench_script.is_file(),
            "Perturb-seq feature workbench is not installed",
        ),
        "synthesis.ordering_validate": (workbench_script.is_file(), None),
    }
    policy_state = {
        capability["id"]: (True, None) for capability in CAPABILITIES
    }
    policy_state["corpus.findings"] = (
        not predictive_ranking,
        "Narrative Finding/Claim access is policy-disabled for predictive "
        "rankings; use quantitative calibration plus the summary-free predictive "
        "graph review",
    )
    policy_state["corpus.relational_candidates"] = (
        not predictive_ranking,
        "broad relational candidate generation is policy-disabled for predictive "
        "rankings; use corpus.predictive_graph_review after quantitative calibration",
    )
    policy_state["corpus.predictive_graph_review"] = (
        predictive_ranking,
        "bounded predictive graph review is authorized only for prediction tasks "
        "with supplied ranked or partial-ranked supervision",
    )
    policy_state["dataset.perturbseq_features"] = (
        predictive_ranking,
        "rank-calibration workbench is authorized only for prediction tasks with "
        "explicit ranked or partial-ranked gene supervision and a requested "
        "ranked output",
    )
    policy_state["synthesis.ordering_validate"] = (
        predictive_ranking,
        "ordering validation is authorized only for prediction tasks with explicit "
        "ranked or partial-ranked gene supervision and a requested ranked output",
    )
    runtime_state = {
        capability["id"]: (True, None) for capability in CAPABILITIES
    }
    runtime_state.update(
        {
            "corpus.findings": (
                findings is not None and findings.is_file(),
                "declared Findings ledger is unavailable",
            ),
            "corpus.target_analogs": (
                analog_index.is_file(),
                "the selected release target-analog index is unavailable",
            ),
            "corpus.calibration": (
                ledger_calibration_path.is_file()
                and value_dictionary_path.is_file()
                and calibration_schema_path.is_file(),
                "calibration artifact, dictionary, or schema is unavailable",
            ),
            "corpus.report_evidence": (
                reports is not None and reports.is_file(),
                "no declared report ledger is available",
            ),
            "corpus.relational_candidates": (
                findings is not None and findings.is_file(),
                "declared Findings ledger is unavailable",
            ),
            "corpus.predictive_graph_review": (
                findings is not None and findings.is_file(),
                "declared Findings ledger is unavailable",
            ),
            "dataset.perturbseq_features": (
                dataset_path is not None and dataset_path.is_file(),
                "workbench requires a declared Parquet input",
            ),
        }
    )
    graph_role = (
        release.manifest.get("capabilities", {})
        .get("skills", {})
        .get("roles", {})
        .get("graph", {})
    )
    graph_contract = graph_role.get("graph_contract")
    capabilities = []
    for capability in CAPABILITIES:
        capability_id = capability["id"]
        installed, installation_reason = installation_state[capability_id]
        policy_allowed, policy_reason = policy_state[capability_id]
        prerequisites_ready, runtime_reason = runtime_state[capability_id]
        runtime_ready = installed and prerequisites_ready
        if capability_id == "corpus.graph":
            runtime_ready = installed and bool(neo4j_preflight["runtime_ready"])
            if installed and not runtime_ready:
                runtime_reason = str(neo4j_preflight["reason"])
        elif capability_id == "corpus.direct_evidence" and direct_evidence_requires_graph:
            direct_ready = neo4j_preflight.get(
                "direct_evidence_ready", neo4j_preflight["runtime_ready"]
            )
            runtime_ready = installed and bool(direct_ready)
            if installed and not runtime_ready:
                runtime_reason = str(
                    neo4j_preflight.get("direct_evidence_reason")
                    or neo4j_preflight["reason"]
                )
        available = installed and policy_allowed and runtime_ready
        interface = CAPABILITY_INTERFACES.get(
            capability_id,
            {
                "accepted_arguments": [],
                "example": "read the declared entrypoint",
                "output_bound": capability["output_shape"],
            },
        )
        native_tools = native_corpus_tools_for_release(
            capability_id,
            artifact_names=set(release.manifest.get("artifacts", {})),
            skill_roles=set(
                release.manifest["capabilities"]["skills"].get("roles", {})
            ),
        )
        row = {
            **capability,
            **interface,
            "entrypoint": (
                str(entrypoints[capability_id])
                if native_tools is None and entrypoints.get(capability_id) is not None
                else None
            ),
            "mcp_server": "distributed_agents_corpus" if native_tools else None,
            "mcp_tools": list(native_tools or ()),
            "installed": installed,
            "policy_allowed": policy_allowed,
            "runtime_ready": runtime_ready,
            "declared_available": available,
            "available": available,
        }
        if capability_id == "corpus.graph" and graph_contract is not None:
            row["graph_schema"] = graph_contract["schema"]
            row["canonical_target_expansion"] = graph_contract[
                "canonical_target_expansion"
            ]
        if not available:
            row["unavailable_reason"] = (
                installation_reason
                if not installed
                else policy_reason
                if not policy_allowed
                else runtime_reason
            )
        capabilities.append(row)
    manifest = {
        "schema_version": CAPABILITIES_SCHEMA,
        "mode": mode,
        "state_semantics": {
            "installed": "the declared entrypoint or readable resource physically exists",
            "policy_allowed": "the current task contract authorizes this operation",
            "runtime_ready": "required data and backing services passed readiness checks",
            "available": "installed AND policy_allowed AND runtime_ready",
            "declared_available": "backward-compatible alias of available",
        },
        "capabilities": capabilities,
        "runtime_preflight": {
            "release_entrypoints": capability_preflight,
            "neo4j": neo4j_preflight,
        },
        "ledger_calibration": {
            "schema_version": (
                str(json.loads(ledger_calibration_path.read_text()).get("schema_version"))
                if ledger_calibration_path.is_file()
                else None
            ),
            "artifact": _artifact_provenance(ledger_calibration_path),
            "schema": _artifact_provenance(calibration_schema_path),
            "value_dictionary": _artifact_provenance(value_dictionary_path),
        },
        "source_paths": {
            "corpus_release_id": release.release_id,
            "corpus_release_manifest": str(release.manifest_path),
            "corpus_release_manifest_sha256": _sha256(release.manifest_path),
            "task_bindings": str(task_bindings_path),
            "findings_ledger": str(findings) if findings else None,
            "reports": str(reports) if reports else None,
            "claim_assignments": str(assignments) if assignments.is_file() else None,
            "claim_relations": str(relations) if relations.is_file() else None,
            "target_analog_index": str(analog_index) if analog_index.is_file() else None,
            "measurement_registry": str(measurement_registry_path),
            "declared_parquet": str(dataset_path) if dataset_path else None,
            "declared_input_roots": [
                str(path)
                for path in (
                    input_roots if declared_inputs is None else declared_inputs
                )
            ],
            "effective_input_roots": [str(path) for path in input_roots],
        },
        "guard": (
            "Capabilities are evidence operations, not task labels. Internal corpus "
            "and Parquet are same-experiment representations. Unavailable and "
            "non-executable operations must not be reconstructed as framework tools."
        ),
    }
    capability_path = pipeline_dir / "capabilities.json"
    capability_path.write_text(json.dumps(manifest, indent=2) + "\n")
    preparation = {
        "mode": mode,
        "duration_s": round(time.monotonic() - started, 3),
        "coverage_command": command,
        "dataset_context": str(dataset_context_path),
        "measurement_registry": str(measurement_registry_path),
        "task_bindings": str(task_bindings_path),
        "runtime_preflight": manifest["runtime_preflight"],
        "ledger_calibration": manifest["ledger_calibration"],
    }
    return AdaptiveContext(
        skill_path=skill_path,
        capability_manifest=capability_path,
        coverage=coverage_path,
        preparation=preparation,
    )
