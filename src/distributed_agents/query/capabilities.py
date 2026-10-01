"""Stable capability declarations emitted during query preparation."""

from typing import Any


CAPABILITIES_SCHEMA = "distributed_agents-capability-manifest-v4"
CAPABILITIES: tuple[dict[str, Any], ...] = (
    {
        "id": "task.bindings",
        "description": "Read normalized supplied entity sets, explicit ranks, declared input inventory, and typed context mappings.",
        "kind": "readable_resource",
        "expected_cost": "low",
        "output_shape": "JSON object with entity_sets and input_inventory",
        "source_policy": "run_local_generated",
    },
    {
        "id": "corpus.coverage",
        "description": "Read the pre-decision index coverage for task entities and sources.",
        "kind": "readable_resource",
        "expected_cost": "low",
        "output_shape": "compact JSON coverage summary",
        "source_policy": "run_local_generated",
    },
    {
        "id": "corpus.findings",
        "description": "Retrieve bounded same-experiment Findings and, where released, higher-order Claim context with exact totals and explicit provenance lanes.",
        "kind": "executable_tool",
        "expected_cost": "low",
        "output_shape": "bounded JSON Finding records with IDs and exact truncation totals",
        "source_policy": "declared_same_experiment_corpus",
    },
    {
        "id": "corpus.target_analogs",
        "description": "Nominate typed, assay-eligible mouse comparators for requested targets, including targets absent from the corpus, from a frozen curated annotation and physical-interaction index.",
        "policy": "Comparator nomination only. Evidence tiers are not interchangeable, ordering is not an outcome prediction or aggregate biological similarity score, and task-matched measured profiles must adjudicate final use.",
        "kind": "executable_tool",
        "expected_cost": "low_to_medium",
        "output_shape": "bounded per-target candidate pages with typed CORUM, pathway, GO/functional, STRING physical, and reciprocal corpus-comparator provenance",
        "source_policy": "release_frozen_external_biological_annotations_plus_selected_corpus_reciprocal_comparators",
    },
    {
        "id": "corpus.calibration",
        "description": "Look up release-declared field/value contracts, corpus calibration summaries, and exact compact value counts.",
        "kind": "executable_tool",
        "expected_cost": "low",
        "output_shape": "bounded JSON contract or aggregate with artifact provenance and exact totals",
        "source_policy": "packaged_same_experiment_corpus_contract",
    },
    {
        "id": "corpus.claim_relations",
        "description": "Inspect release-declared Claim assignments and typed review relations around task anchors, retaining the release's declared Claim-unit semantics.",
        "kind": "readable_resource",
        "expected_cost": "low",
        "output_shape": "release-declared tabular Claim assignments; relation path and unit semantics in source_paths/calibration",
        "source_policy": "packaged_same_experiment_corpus",
    },
    {
        "id": "corpus.graph",
        "description": "Run the selected release's bounded read-only graph query entrypoint.",
        "policy": "Semantic guidance only; graph topology and relation counts never score or order candidates.",
        "kind": "executable_tool",
        "expected_cost": "low_to_medium",
        "output_shape": "bounded JSON or tabular graph rows",
        "source_policy": "selected_release_graph",
    },
    {
        "id": "corpus.report_evidence",
        "description": "Resolve packaged Evidence/Reference rows for material targets by target, Finding, or explicit local IDs.",
        "kind": "executable_tool",
        "expected_cost": "low_to_medium",
        "output_shape": "bounded JSON Evidence and Reference records",
        "source_policy": "declared_same_experiment_corpus",
    },
    {
        "id": "corpus.direct_evidence",
        "description": "Retrieve the selected release's summary-first, unranked comparison or explicitly tagged peer-comparator evidence around named anchors. For predictive calibration, anchors and the candidate universe are derived automatically from calibration.json; compact boundary conditions are demand-loaded by explicit record ID.",
        "policy": "Interpretation or falsification only. Exact comparison pairs are presented first for attention, not as a biological score; graph topology and counts never score candidates.",
        "kind": "executable_tool",
        "expected_cost": "low",
        "output_shape": "host-frozen JSON index (at most 10 anchors, 3 records per anchor, 16 emitted records, and 12,000 characters) containing identity, pairing, and one summary only; separate query returns boundary conditions and reference IDs for at most three explicit records",
        "source_policy": "selected_release_same_experiment_comparison_substrate",
    },
    {
        "id": "corpus.relational_candidates",
        "description": "Retrieve an unranked typed semantic map from visible anchors and audit aggregate map coverage with seed dropout.",
        "policy": "Semantic guidance only; never score, rank, prioritize, promote, or demote candidates from graph structure or diagnostics.",
        "kind": "executable_tool",
        "expected_cost": "medium",
        "output_shape": "unranked JSON semantic map and optional CSV candidates",
        "source_policy": "packaged_same_experiment_corpus",
    },
    {
        "id": "corpus.predictive_graph_review",
        "description": "Nominate complete directed visible-seed comparator-multiplicity tiers, mark their overlap with a calibrated quantitative top-k, and finalize exact graph-only challenger review telemetry without emitting Finding text.",
        "policy": "Multiplicity selects review breadth only; it is not endpoint evidence or a final candidate score. Predictive review uses the quantitative-plus-graph union, requires every graph-only challenger to be dispositioned, and does not expose legacy Finding summaries.",
        "kind": "executable_tool",
        "expected_cost": "low_to_medium",
        "output_shape": "complete alphabetically serialized directed-multiplicity tiers within 64,000 characters, with candidate identity, anchors, quantitative rank/overlap, a disposition template, and compact finalized telemetry",
        "source_policy": "packaged_same_experiment_corpus",
    },
    {
        "id": "dataset.query",
        "description": "Read the declared Perturb-seq Parquet input directly when exact rows are required.",
        "kind": "readable_resource",
        "expected_cost": "high_if_scanned",
        "output_shape": "raw measured-gene by target by cell-type rows",
        "source_policy": "declared_input_only",
    },
    {
        "id": "dataset.measurements",
        "description": "Read the generated schema and measurement registry for mounted dataset inputs.",
        "kind": "readable_resource",
        "expected_cost": "low",
        "output_shape": "JSON measurement and absent-quantity registry",
        "source_policy": "run_local_generated",
    },
    {
        "id": "dataset.perturbseq_features",
        "description": "Calibrate a canonical candidate ranking from declared Perturb-seq features and explicit ranked or partial-ranked gene supervision. This is an ordinal ranking workbench, not a scalar/count predictor or a general interpretation tool.",
        "policy": "Only predictive-ranking tasks with explicit ranked supervision may use this capability. Graph and corpus fields are rejected; eligible runs reuse the cached feature table instead of rescanning the Parquet.",
        "kind": "executable_tool",
        "expected_cost": "high_first_summary_low_after_cache",
        "output_shape": "feature Parquet plus calibration JSON and canonical ranking TSV",
        "source_policy": "declared_parquet_and_run_local_bindings_only",
    },
    {
        "id": "synthesis.ordering_validate",
        "description": "Mechanically verify that a final ranking preserves the workbench basis or declares every exact displacement with candidate-specific endpoint evidence.",
        "kind": "executable_tool",
        "expected_cost": "low",
        "output_shape": "JSON ordering validation report",
        "source_policy": "run_local_artifacts_only",
    },
)

CAPABILITY_INTERFACES: dict[str, dict[str, Any]] = {
    "corpus.findings": {
        "accepted_arguments": [
            "search_findings: queries[1..8], level={finding,target}, finding_type, offset, limit=1..50",
            "query_ledger: ledger, genes[], ids[], finding_types[], fields[], offset, limit=1..50",
            "find_shared_claims: genes[], finding_type, limit=1..50",
            "query_claims: claim_ids[], genes[], query, confidence, member_roles[], relation_types[], include_memberships, include_relations, offset, limit=1..50",
            "target_context: target, independent Claim/Finding/reference offsets and limits",
            "search_claims: query, targets[], confidence, offset, limit=1..50",
            "get_claim: claim_id, include_findings=true|false",
            "get_finding: finding_doc_id",
            "compare_targets: left_target, right_target, offset, limit=1..50",
            "related_targets: target or targets[1..20], release-supported traversal={direct,random_walk}, basis, direction, path_detail for direct traversal, restart_probability/eligible_targets[]/exclude_inputs for random walk, offset, limit=1..50",
            "inspect_target_set: targets[2..20], basis={both,compatibility_claim,shared_claim,claim_relation,explicit_finding_reference}, path_detail, minimum_sources, eligible_targets[], independent connection/neighbor offsets and limits",
        ],
        "example": "search_findings(queries=['proteasome subunit shared response'], level='target', limit=12) when advertised; otherwise use a listed exact target/Claim tool",
        "output_bound": "at most 50 rows per page and 32,000 UTF-8 bytes; exact totals, offsets, and output-byte truncation are explicit",
    },
    "corpus.calibration": {
        "accepted_arguments": [
            "describe: query, limit=1..50",
            "calibrate: topic, limit=1..50",
            "count: artifact, field, canonical={contradiction}, limit=1..50",
        ],
        "example": "calibrate(topic='summary')",
        "output_bound": "at most 50 rows and 32,000 UTF-8 bytes; exact totals and truncation are explicit",
    },
    "corpus.target_analogs": {
        "accepted_arguments": [
            "suggest_target_analogs: targets[1..20], optional eligible_targets[0..5000], include_broad_fallback, source_limit=1..10, offset, limit=1..20 per target",
        ],
        "example": "suggest_target_analogs(targets=['Ap2s1'], eligible_targets=['Ap2m1','Cltc','Dnm1'], limit=10)",
        "output_bound": "at most 20 candidates per requested target before the shared 32,000-byte response ceiling; exact candidate and source totals and truncation are explicit",
    },
    "corpus.claim_relations": {
        "accepted_arguments": [
            "read source_paths.claim_assignments",
            "read source_paths.claim_relations",
            "use corpus.calibration describe/calibrate to interpret the release's Claim and relation units",
        ],
        "example": "calibrate relations",
        "output_bound": "immutable release-declared tables; filter locally by task anchors before reading rows",
    },
    "corpus.graph": {
        "accepted_arguments": [
            "read_cypher: query, parameters{}",
        ],
        "example": "read_cypher(query='MATCH (t:TargetGene) RETURN t.symbol AS target LIMIT 10')",
        "output_bound": "caller query must end with LIMIT <= 50; unavailable unless host Neo4j preflight passes",
    },
    "corpus.report_evidence": {
        "accepted_arguments": [
            "resolve_evidence: gene, finding, evidence_ids[], ref_ids[], mode={both,evidence,references}",
        ],
        "example": "resolve_evidence(gene='Psmb4', finding='F001')",
        "output_bound": "bounded to explicitly named genes or Finding IDs",
    },
    "corpus.direct_evidence": {
        "accepted_arguments": [
            "--calibration PATH",
            "--anchor GENE (repeatable)",
            "--anchors-file PATH",
            "--detail-record ID (at most 3)",
            "--out PATH (required)",
        ],
        "example": "--anchor Psmb4 --out evidence/direct-index.json",
        "output_bound": "10 anchors, 3 records per anchor, 16 records, and 12,000 characters",
    },
    "corpus.relational_candidates": {
        "accepted_arguments": [
            "--seed GENE (repeatable)",
            "--seeds-file PATH",
            "--candidate-universe PATH",
            "--out PATH (required)",
        ],
        "example": "--seed Tsc1 --seed Tsc2 --out evidence/semantic-map.json",
        "output_bound": "unranked run-local semantic map; disabled for predictive ranking",
    },
    "corpus.predictive_graph_review": {
        "accepted_arguments": [
            "nominate --bindings PATH --calibration PATH --top-k N --out PATH --dispositions-out PATH",
            "finalize --review PATH --dispositions PATH --answer PATH --top-k N --out PATH",
        ],
        "example": "nominate --bindings pipeline/task_bindings.json --calibration workbench/calibration.json --top-k 50 --out workbench/predictive_graph_review.json --dispositions-out workbench/predictive_graph_review_dispositions.tsv",
        "output_bound": "complete directed-multiplicity tiers within 64,000 JSON characters; no Finding text and no split boundary tier",
    },
    "dataset.perturbseq_features": {
        "accepted_arguments": [
            "summarize --parquet PATH --cache-dir PATH [--out PATH]",
            "summarize optional column roles: --measured-gene-column, --group-column, --gene-target-column, --logfoldchange-column, --score-column, --pvalue-column, --adjusted-pvalue-column, --significance-column",
            "calibrate --features PATH --bindings PATH --out PATH --ranking-out PATH",
            "validate-ordering --basis PATH --answer PATH --top-k N --out PATH",
        ],
        "example": "summarize --parquet INPUT.parquet --cache-dir evidence/cache --out evidence/features.parquet",
        "output_bound": "eligible predictive-ranking tasks only; writes bounded run-local artifacts and exposes summaries rather than raw Parquet rows",
    },
    "synthesis.ordering_validate": {
        "accepted_arguments": [
            "validate-ordering --basis PATH --answer PATH [--overrides PATH] --top-k N --out PATH",
        ],
        "example": "validate-ordering --basis evidence/canonical_ranking.tsv --answer evidence/final_ranking.tsv --overrides evidence/ordering_overrides.jsonl --top-k 50 --out evidence/ordering-validation.json",
        "output_bound": "one compact JSON validation report",
    },
}

NATIVE_CORPUS_TOOLS: dict[str, tuple[str, ...]] = {
    "corpus.findings": (
        "search_findings",
        "query_ledger",
        "find_shared_claims",
        "query_claims",
        "target_context",
        "search_claims",
        "get_claim",
        "get_finding",
        "compare_targets",
        "related_targets",
        "inspect_target_set",
    ),
    "corpus.calibration": (
        "describe",
        "calibrate",
        "count",
    ),
    "corpus.target_analogs": ("suggest_target_analogs",),
    "corpus.report_evidence": ("resolve_evidence",),
    "corpus.graph": ("read_cypher",),
}

BOTTOM_UP_CLAIM_ARTIFACTS = {
    "claims",
    "claim_contributions",
    "finding_claim_dispositions",
    "findings",
}
BOTTOM_UP_CLAIM_TOOLS = {
    "target_context",
    "search_claims",
    "get_claim",
    "get_finding",
    "compare_targets",
}
COMPATIBILITY_CLAIM_ARTIFACTS = {
    "claim_assignments",
    "claim_relations",
    "findings",
}
COMPATIBILITY_CLAIM_TOOLS = {"query_claims", "inspect_target_set"}
RELATIONSHIP_TOOLS = {"related_targets"}
FINDINGS_BM25_ARTIFACT = "findings_bm25"
FINDINGS_BM25_ROLE = "lexical_retrieval"
TARGET_ANALOG_ARTIFACT = "gene_analog_index"


def native_corpus_tools_for_release(
    capability_id: str,
    *,
    artifact_names: set[str],
    skill_roles: set[str],
) -> tuple[str, ...] | None:
    """Return the canonical MCP tools supported by one release declaration."""

    native_tools = NATIVE_CORPUS_TOOLS.get(capability_id)
    if capability_id == "corpus.target_analogs":
        return (
            native_tools
            if native_tools is not None and TARGET_ANALOG_ARTIFACT in artifact_names
            else ()
        )
    if capability_id != "corpus.findings" or native_tools is None:
        return native_tools
    unavailable_tools: set[str] = set()
    if (
        FINDINGS_BM25_ARTIFACT not in artifact_names
        or FINDINGS_BM25_ROLE not in skill_roles
    ):
        unavailable_tools.add("search_findings")
    supports_bottom_up_claims = BOTTOM_UP_CLAIM_ARTIFACTS.issubset(
        artifact_names
    )
    supports_compatibility_claims = (
        not supports_bottom_up_claims
        and COMPATIBILITY_CLAIM_ARTIFACTS.issubset(artifact_names)
    )
    if not supports_bottom_up_claims:
        unavailable_tools.update(BOTTOM_UP_CLAIM_TOOLS)
    if not supports_compatibility_claims:
        unavailable_tools.update(COMPATIBILITY_CLAIM_TOOLS)
    if not (supports_bottom_up_claims or supports_compatibility_claims):
        unavailable_tools.update(RELATIONSHIP_TOOLS)
    if supports_compatibility_claims:
        unavailable_tools.add("find_shared_claims")
    return tuple(tool for tool in native_tools if tool not in unavailable_tools)
