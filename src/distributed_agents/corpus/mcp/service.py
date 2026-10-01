"""Read-only operations over one selected corpus release."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from .binding import ReleaseBinding
from .analogs import (
    TARGET_ANALOG_ARTIFACT,
    TIER_RANK as ANALOG_TIER_RANK,
    GeneAnalogIndex,
    materialize_candidate,
)
from .bounds import (
    _boolean,
    _bound_analog_suggestions,
    _bound_evidence,
    _bound_list_fields,
    _bound_records,
    _check_keys,
    _enum,
    _integer,
    _json_size,
    _limit,
    _limit_named,
    _number,
    _offset,
    _optional_string,
    _page_metadata,
    _parse_json_array,
    _parse_json_lines,
    _parse_json_object,
    _required_string,
    _search_terms,
    _string_list,
)
from .claims import ClaimGraphIndex, _gene_key, _stable_hash_key
from .compatibility import (
    COMPATIBILITY_CLAIM_ARTIFACTS,
    CompatibilityClaimIndex,
)
from .constants import (
    CALIBRATION_CAPABILITY,
    CLAIM_GRAPH_ARTIFACTS,
    EVIDENCE_CAPABILITY,
    FINDINGS_BM25_ARTIFACT,
    FINDINGS_BM25_ROLE,
    FINDINGS_CAPABILITY,
    GRAPH_CAPABILITY,
    LEGACY_FINDINGS_TOPICS,
    LEGACY_TOPICS,
    MAX_ROWS,
    MAX_OUTPUT_BYTES,
    QUERY_LEDGER_NAMES,
    SAFE_FIELD,
    SHI_HOLDOUT_TOPICS,
    SHI_TOPICS,
    TARGET_ANALOG_CAPABILITY,
    TOOL_TIMEOUT_SECONDS,
)
from .errors import CorpusToolError
from .policy import CapabilityPolicy
from .schemas import (
    _boolean_schema,
    _limit_schema,
    _number_schema,
    _offset_schema,
    _schema,
    _string_array_schema,
    _string_schema,
    _tool,
)
from .walks import random_walk_with_restart


class CorpusService:
    def __init__(self, release: ReleaseBinding, policy: CapabilityPolicy) -> None:
        self.release = release
        self.policy = policy
        self._claim_graph: ClaimGraphIndex | None = None
        self._compatibility_claims: CompatibilityClaimIndex | None = None
        self._gene_analogs: GeneAnalogIndex | None = None
        self._compatibility_projection_cache: dict[
            tuple[str, str],
            tuple[dict[str, frozenset[str]], dict[str, int]],
        ] = {}

    @property
    def supports_claim_graph(self) -> bool:
        return CLAIM_GRAPH_ARTIFACTS.issubset(self.release.artifact_names)

    @property
    def supports_findings_bm25(self) -> bool:
        if FINDINGS_BM25_ARTIFACT not in self.release.artifact_names:
            return False
        try:
            self.release.entrypoint(FINDINGS_BM25_ROLE, "query")
        except CorpusToolError:
            return False
        return True

    @property
    def supports_shared_claims(self) -> bool:
        if self.supports_claim_graph:
            return True
        projections = self.release.payload.get("capabilities", {}).get(
            "projections", {}
        )
        return (
            self.release.corpus_family == "legacy_reports"
            and not self.supports_compatibility_claims
            and isinstance(projections, Mapping)
            and "biokg" in projections
        )

    @property
    def supports_compatibility_claims(self) -> bool:
        return (
            self.release.corpus_family == "shi"
            and not self.supports_claim_graph
            and COMPATIBILITY_CLAIM_ARTIFACTS.issubset(
                self.release.artifact_names
            )
        )

    @property
    def supports_target_analogs(self) -> bool:
        return (
            self.supports_compatibility_claims
            and TARGET_ANALOG_ARTIFACT in self.release.artifact_names
        )

    @property
    def claim_graph(self) -> ClaimGraphIndex:
        if not self.supports_claim_graph:
            raise CorpusToolError(
                "selected release does not declare the bottom-up Claim graph"
            )
        if self._claim_graph is None:
            self._claim_graph = ClaimGraphIndex(self.release)
        return self._claim_graph

    @property
    def compatibility_claims(self) -> CompatibilityClaimIndex:
        if not self.supports_compatibility_claims:
            raise CorpusToolError(
                "selected release does not declare a compatible Claim layer"
            )
        if self._compatibility_claims is None:
            self._compatibility_claims = CompatibilityClaimIndex(self.release)
        return self._compatibility_claims

    @property
    def gene_analogs(self) -> GeneAnalogIndex:
        if not self.supports_target_analogs:
            raise CorpusToolError(
                "selected release does not declare target-analog grounding"
            )
        if self._gene_analogs is None:
            self._gene_analogs = GeneAnalogIndex(self.release)
        return self._gene_analogs

    def calibration_topics(self) -> tuple[str, ...]:
        if self.release.corpus_family == "shi_holdout":
            return SHI_HOLDOUT_TOPICS
        if self.release.corpus_family in {"shi", "legacy_reports"}:
            if self.supports_compatibility_claims:
                return SHI_TOPICS
            return LEGACY_TOPICS if self.supports_shared_claims else LEGACY_FINDINGS_TOPICS
        raise CorpusToolError(
            f"release family is not supported by the native corpus server: "
            f"{self.release.corpus_family or '<missing>'}"
        )

    def count_artifacts(self) -> tuple[str, ...]:
        values: list[str] = []
        if "findings" in self.release.artifact_names:
            values.append("findings")
        if "claims" in self.release.artifact_names:
            values.append("claims")
        elif "claim_assignments" in self.release.artifact_names:
            values.append("claims")
        if "claim_relations" in self.release.artifact_names and not self.supports_claim_graph:
            values.append("relations")
        return tuple(values)

    def allowed_ledgers(self) -> tuple[str, ...]:
        if not self.policy.allows(FINDINGS_CAPABILITY):
            return ()
        ledgers = [
            name for name in QUERY_LEDGER_NAMES if name in self.release.artifact_names
        ]
        query = self.release.entrypoint("ledger", "query")
        if query.name == "query_findings.py":
            return ("findings",) if "findings" in ledgers else ()
        return tuple(ledgers)

    def tools(self) -> list[dict[str, Any]]:
        tools: list[dict[str, Any]] = []
        if self.policy.allows(CALIBRATION_CAPABILITY):
            count_artifacts = self.count_artifacts()
            tools.extend(
                [
                    _tool(
                        "describe",
                        "Describe corpus vocabulary",
                        "Look up release-defined fields or values in the corpus dictionary.",
                        _schema(
                            {
                                "query": _string_schema("Field name or controlled value to describe."),
                                "limit": _limit_schema(10),
                            },
                            ("query",),
                        ),
                    ),
                    _tool(
                        "calibrate",
                        "Read corpus calibration",
                        "Read a bounded topic from the selected release's calibration contract.",
                        _schema(
                            {
                                "topic": _string_schema(
                                    "Release-supported calibration topic.",
                                    enum=self.calibration_topics(),
                                ),
                                "limit": _limit_schema(MAX_ROWS),
                            },
                            ("topic",),
                        ),
                    ),
                    _tool(
                        "count",
                        "Count corpus values",
                        "Return an exact, precomputed value-frequency table for a corpus field.",
                        _schema(
                            {
                                "artifact": _string_schema("Corpus artifact.", enum=count_artifacts),
                                "field": _string_schema("Field to count."),
                                "canonical": _string_schema(
                                    "Optional canonical biological interpretation.",
                                    enum=("contradiction",),
                                ),
                                "limit": _limit_schema(20),
                            },
                            ("artifact", "field"),
                        ),
                    ),
                ]
            )
        if self.policy.allows(FINDINGS_CAPABILITY):
            if self.supports_compatibility_claims:
                tools.extend(self._compatibility_claim_tools())
            elif self.supports_shared_claims:
                tools.append(
                    _tool(
                        "find_shared_claims",
                        "Find Claims shared by genes",
                        "Return release-declared Claims whose targets contain every requested gene, with an exact total.",
                        _schema(
                            {
                                "genes": {
                                    **_string_array_schema("Genes that must all occur in the Claim targets."),
                                    "minItems": 1,
                                },
                                "finding_type": _string_schema("Optional release-defined Finding type."),
                                "limit": _limit_schema(10),
                            },
                            ("genes",),
                        ),
                    )
                )
                if self.supports_claim_graph:
                    tools.extend(self._claim_graph_tools())
        if self.policy.allows(FINDINGS_CAPABILITY) and self.supports_findings_bm25:
            tools.append(
                _tool(
                    "search_findings",
                    "Search canonical Findings",
                    "Relevance-rank canonical Findings with release-native BM25 over summary and why-it-matters text only. For a basic concept question, prefer one target-level call with two or three focused formulations, then resolve only a few representative returned Findings.",
                    _schema(
                        {
                            "queries": {
                                **_string_array_schema(
                                    "One to eight focused lexical formulations; multiple queries are fused with reciprocal rank fusion."
                                ),
                                "minItems": 1,
                                "maxItems": 8,
                            },
                            "level": _string_schema(
                                "Return individual Findings or collapse to the best hit per target.",
                                enum=("finding", "target"),
                                default="finding",
                            ),
                            "finding_type": _string_schema(
                                "Optional exact Finding-type metadata filter."
                            ),
                            "limit": {
                                **_limit_schema(12),
                                "description": (
                                    "Maximum rows returned; 8-12 is usually enough "
                                    "before resolving representative evidence."
                                ),
                            },
                            **(
                                {"offset": _offset_schema()}
                                if self.supports_compatibility_claims
                                else {}
                            ),
                        },
                        ("queries",),
                    ),
                )
            )
        ledgers = self.allowed_ledgers()
        if ledgers:
            properties: dict[str, Any] = {
                "ledger": _string_schema("Canonical ledger to query.", enum=ledgers),
                "genes": _string_array_schema("Target-gene filters."),
                "finding_types": _string_array_schema("Finding-type filters."),
                "fields": _string_array_schema("Fields to return; omit for complete records."),
                "limit": _limit_schema(20),
            }
            if (
                self.release.entrypoint("ledger", "query").name == "query_ledger.py"
                or self.supports_compatibility_claims
            ):
                properties["ids"] = _string_array_schema(
                    "Exact target-scoped Finding IDs such as Abat:F001; local IDs require a gene filter."
                )
            if self.supports_compatibility_claims:
                properties["offset"] = _offset_schema()
            tools.append(
                _tool(
                    "query_ledger",
                    "Query a canonical corpus ledger",
                    "Filter a release-declared canonical ledger without exposing filesystem paths.",
                    _schema(properties, ("ledger",)),
                )
            )
        if self.policy.allows(EVIDENCE_CAPABILITY):
            tools.append(
                _tool(
                    "resolve_evidence",
                    "Resolve Finding evidence",
                    "Resolve gene-scoped Finding, evidence, and reference IDs through the selected release.",
                    _schema(
                        {
                            "gene": _string_schema("Target gene that scopes every supplied local ID."),
                            "finding": _string_schema("Optional Finding ID for the target gene."),
                            "evidence_ids": _string_array_schema("Optional evidence IDs for the target gene."),
                            "ref_ids": _string_array_schema("Optional reference IDs for the target gene."),
                            "mode": _string_schema(
                                "Which linked records to return.",
                                enum=("both", "evidence", "references"),
                                default="both",
                            ),
                        },
                        ("gene",),
                    ),
                )
            )
        if self.policy.allows(TARGET_ANALOG_CAPABILITY) and self.supports_target_analogs:
            tools.append(self._target_analog_tool())
        if self.policy.allows(GRAPH_CAPABILITY):
            tools.append(
                _tool(
                    "read_cypher",
                    "Run bounded expert Cypher",
                    "Expert escape hatch for bounded read-only Cypher against the selected release graph. Prefer the structured Claim/Finding tools.",
                    _schema(
                        {
                            "query": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 10_000,
                                "description": "Read-only Cypher ending with LIMIT <= 50.",
                            },
                            "parameters": {
                                "type": "object",
                                "maxProperties": 50,
                                "additionalProperties": True,
                                "description": "Named JSON parameters used by the Cypher statement.",
                            },
                        },
                        ("query",),
                    ),
                )
            )
        return tools

    def _target_analog_tool(self) -> dict[str, Any]:
        return _tool(
            "suggest_target_analogs",
            "Suggest typed analogs for unavailable targets",
            "Nominate assay-eligible analogs for one to twenty mouse targets, including targets absent from the corpus, using frozen CORUM, pathway, GO/functional, STRING physical, and reciprocal corpus-comparator evidence. Evidence tiers stay distinct and ordering is categorical, not an outcome prediction or aggregate biological similarity score.",
            _schema(
                {
                    "targets": {
                        **_string_array_schema(
                            "One to twenty requested mouse gene targets; corpus presence is not required."
                        ),
                        "minItems": 1,
                        "maxItems": 20,
                    },
                    "eligible_targets": _string_array_schema(
                        "Optional caller-declared assay or training universe. Defaults to the selected release's biological perturbation targets.",
                        max_items=5_000,
                    ),
                    "include_broad_fallback": _boolean_schema(
                        "Include broad GO, functional-class, hallmark, and large-membership fallback evidence after specific tiers.",
                        True,
                    ),
                    "source_limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 3,
                        "description": "Maximum source records embedded per typed relationship; exact source totals remain explicit.",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 10,
                        "description": "Maximum candidates returned per requested target.",
                    },
                    "offset": _offset_schema(),
                },
                ("targets",),
            ),
        )

    def _compatibility_claim_tools(self) -> list[dict[str, Any]]:
        return [
            _tool(
                "query_claims",
                "Query Shi Claims",
                "Retrieve exact Claim IDs or lexically filter the Shi Claim layer. Gene filters use all-gene intersection semantics; memberships and typed Claim relations are optional supporting detail.",
                _schema(
                    {
                        "claim_ids": _string_array_schema("Exact compatibility Claim IDs."),
                        "genes": _string_array_schema(
                            "Target genes that must all occur in each Claim."
                        ),
                        "query": _string_schema(
                            "Optional lexical query over the canonical summary and structured Claim fields."
                        ),
                        "confidence": _string_schema(
                            "Optional exact Claim confidence filter."
                        ),
                        "member_roles": _string_array_schema(
                            "Optional native membership-role filters."
                        ),
                        "relation_types": _string_array_schema(
                            "Optional incident Claim-relation type filters."
                        ),
                        "include_memberships": _boolean_schema(
                            "Embed typed Finding memberships.", False
                        ),
                        "include_relations": _boolean_schema(
                            "Embed bounded incident typed Claim relations.", False
                        ),
                        "limit": _limit_schema(10),
                        "offset": _offset_schema(),
                    }
                ),
            ),
            _tool(
                "related_targets",
                "Find related Shi targets",
                "Find targets related to one anchor by direct evidence paths or to one-to-twenty anchors by multi-source random walk with restart. Claim co-membership, typed Claim relations, and Finding comparator references remain selectable lanes. Walk scores quantify reachability in the declared binary projection, not biological importance.",
                _schema(
                    {
                        "target": _string_schema(
                            "One perturbation target for direct traversal, or a single random-walk source. Mutually exclusive with targets."
                        ),
                        "targets": {
                            **_string_array_schema(
                                "One to twenty source targets for random-walk traversal. Mutually exclusive with target."
                            ),
                            "minItems": 1,
                            "maxItems": 20,
                        },
                        "traversal": _string_schema(
                            "direct enumerates one-hop evidence paths; random_walk orders reachable targets from one or more sources.",
                            enum=("direct", "random_walk"),
                        ),
                        "basis": _string_schema(
                            "Relationship lane; compatibility_claim combines shared membership and typed Claim relations.",
                            enum=(
                                "both",
                                "compatibility_claim",
                                "shared_claim",
                                "claim_relation",
                                "explicit_finding_reference",
                            ),
                            default="both",
                        ),
                        "direction": _string_schema(
                            "Traversal orientation for typed Claim relations and Finding references; shared Claim membership is undirected.",
                            enum=("both", "outbound", "inbound"),
                            default="both",
                        ),
                        "path_detail": _string_schema(
                            "For direct traversal, ids returns compact path identifiers and full embeds explanatory cards.",
                            enum=("ids", "full"),
                            default="ids",
                        ),
                        "restart_probability": _number_schema(
                            "For random_walk, probability of restarting at the equally weighted source targets on every step.",
                            minimum=0.0,
                            maximum=1.0,
                            default=0.15,
                            exclusive=True,
                        ),
                        "eligible_targets": _string_array_schema(
                            "Optional caller-declared output universe for random-walk results; it does not alter propagation.",
                            max_items=5_000,
                        ),
                        "exclude_inputs": _boolean_schema(
                            "For random_walk, exclude source targets from results.",
                            True,
                        ),
                        "limit": _limit_schema(20),
                        "offset": _offset_schema(),
                    }
                ),
            ),
            _tool(
                "inspect_target_set",
                "Inspect and expand a Shi target set",
                "Audit the induced topology of two to twenty targets and inspect external neighbors connected from multiple inputs. Shared-Claim, Claim-relation, and Finding-reference lanes remain separate; optional eligibility filtering does not rank or weight candidates.",
                _schema(
                    {
                        "targets": {
                            **_string_array_schema(
                                "Two to twenty target genes inspected symmetrically."
                            ),
                            "minItems": 2,
                            "maxItems": 20,
                        },
                        "basis": _string_schema(
                            "Connection lanes used for topology and expansion; compatibility_claim combines shared membership and typed Claim relations.",
                            enum=(
                                "both",
                                "compatibility_claim",
                                "shared_claim",
                                "claim_relation",
                                "explicit_finding_reference",
                            ),
                            default="both",
                        ),
                        "path_detail": _string_schema(
                            "ids returns compact path identifiers; full embeds Finding and Claim cards.",
                            enum=("ids", "full"),
                            default="ids",
                        ),
                        "minimum_sources": {
                            "type": "integer",
                            "minimum": 2,
                            "maximum": 20,
                            "default": 2,
                            "description": "Minimum distinct input targets connected to an external neighbor.",
                        },
                        "eligible_targets": _string_array_schema(
                            "Optional caller-declared eligible universe for external neighbors.",
                            max_items=5_000,
                        ),
                        "exclude_inputs": _boolean_schema(
                            "Exclude supplied targets from external-neighbor results.", True
                        ),
                        "connection_limit": _limit_schema(20),
                        "connection_offset": _offset_schema(),
                        "neighbor_limit": _limit_schema(20),
                        "neighbor_offset": _offset_schema(),
                    },
                    ("targets",),
                ),
            ),
        ]

    def _claim_graph_tools(self) -> list[dict[str, Any]]:
        return [
            _tool(
                "target_context",
                "Get target Claim and Finding context",
                "Retrieve a target's bottom-up Claims, perturbation-centered Findings, dispositions, and one-sided explicit references with independent exact totals.",
                _schema(
                    {
                        "target": _string_schema("Perturbation target gene."),
                        "claim_limit": _limit_schema(10),
                        "claim_offset": _offset_schema(),
                        "finding_limit": _limit_schema(10),
                        "finding_offset": _offset_schema(),
                        "reference_limit": _limit_schema(10),
                        "reference_offset": _offset_schema(),
                    },
                    ("target",),
                ),
            ),
            _tool(
                "search_claims",
                "Search bottom-up Claims",
                "Lexically search Claim statements, scopes, bases, and target symbols. Retrieval relevance is not biological rank.",
                _schema(
                    {
                        "query": _string_schema("Terms to match in frozen Claim fields."),
                        "targets": _string_array_schema(
                            "Optional targets that must all contribute to each Claim."
                        ),
                        "confidence": _string_schema(
                            "Optional frozen Claim confidence.",
                            enum=("high", "moderate", "low"),
                        ),
                        "limit": _limit_schema(10),
                        "offset": _offset_schema(),
                    },
                    ("query",),
                ),
            ),
            _tool(
                "get_claim",
                "Get one bottom-up Claim",
                "Retrieve one Claim and every typed Finding contribution, including role and rationale.",
                _schema(
                    {
                        "claim_id": _string_schema("Stable bottom-up Claim ID."),
                        "include_findings": _boolean_schema(
                            "Embed compact source Finding cards for every contribution.", True
                        ),
                    },
                    ("claim_id",),
                ),
            ),
            _tool(
                "get_finding",
                "Get one Finding and its Claim disposition",
                "Retrieve an exact target-scoped Finding, all Claim contributions, and its one-sided comparator references.",
                _schema(
                    {"finding_doc_id": _string_schema("Canonical ID such as Cplx1:F003.")},
                    ("finding_doc_id",),
                ),
            ),
            _tool(
                "compare_targets",
                "Compare two targets",
                "Return shared-Claim paths and explicit Finding-reference paths in both directions; reciprocity is never required.",
                _schema(
                    {
                        "left_target": _string_schema("First perturbation target."),
                        "right_target": _string_schema("Second perturbation target."),
                        "limit": _limit_schema(20),
                        "offset": _offset_schema(),
                    },
                    ("left_target", "right_target"),
                ),
            ),
            _tool(
                "related_targets",
                "Find evidence-linked targets",
                "Enumerate targets connected by shared Claims, explicit Finding references, or both. Deterministic order is not biological rank.",
                _schema(
                    {
                        "target": _string_schema("Perturbation target gene."),
                        "basis": _string_schema(
                            "Permitted relationship lane.",
                            enum=("both", "shared_claim", "explicit_finding_reference"),
                            default="both",
                        ),
                        "limit": _limit_schema(20),
                        "offset": _offset_schema(),
                    },
                    ("target",),
                ),
            ),
        ]

    def call(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        advertised = {tool["name"] for tool in self.tools()}
        if name not in advertised:
            raise CorpusToolError(f"unknown or policy-unavailable corpus tool: {name}")
        method = getattr(self, f"call_{name}", None)
        if method is None:
            raise CorpusToolError(f"corpus tool is not implemented: {name}")
        return method(arguments)

    def call_suggest_target_analogs(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(TARGET_ANALOG_CAPABILITY)
        _check_keys(
            arguments,
            {
                "targets",
                "eligible_targets",
                "include_broad_fallback",
                "source_limit",
                "limit",
                "offset",
            },
        )
        requested_targets = _string_list(
            arguments, "targets", required=True, max_items=20
        )
        eligible_argument = _string_list(
            arguments, "eligible_targets", max_items=5_000
        )
        include_broad = _boolean(
            arguments, "include_broad_fallback", default=True
        )
        source_limit = _integer(
            arguments,
            "source_limit",
            minimum=1,
            maximum=10,
            default=3,
        )
        limit = _integer(
            arguments, "limit", minimum=1, maximum=20, default=10
        )
        offset = _offset(arguments, "offset")

        analog_index = self.gene_analogs
        target_resolutions, unresolved_targets = analog_index.resolve_symbols(
            requested_targets
        )
        canonical_requested = [
            target_resolutions.get(_gene_key(target), target.strip())
            for target in requested_targets
        ]
        if len({_gene_key(target) for target in canonical_requested}) != len(
            canonical_requested
        ):
            raise CorpusToolError(
                "targets must resolve to distinct canonical mouse symbols"
            )

        compatibility = self.compatibility_claims
        caller_declared_eligibility = "eligible_targets" in arguments
        requested_eligibility = (
            eligible_argument
            if caller_declared_eligibility
            else sorted(compatibility.target_symbols.values(), key=str.casefold)
        )
        eligible_resolutions, unresolved_eligible = analog_index.resolve_symbols(
            requested_eligibility
        )
        canonical_eligible = sorted(
            {
                symbol
                for symbol in eligible_resolutions.values()
                if not self._is_control_target(symbol)
            },
            key=str.casefold,
        )
        eligible_keys = {_gene_key(symbol) for symbol in canonical_eligible}

        target_results: list[dict[str, Any]] = []
        unresolved_target_keys = {_gene_key(value) for value in unresolved_targets}
        for requested, canonical in zip(requested_targets, canonical_requested):
            target_key = _gene_key(canonical)
            candidates = analog_index.query(
                target=canonical,
                eligible_symbols=canonical_eligible,
                include_broad_fallback=include_broad,
                source_limit=source_limit,
            )
            self._add_reciprocal_analog_comparators(
                candidates,
                target_key=target_key,
                eligible_keys=eligible_keys,
                source_limit=source_limit,
            )
            materialized = [
                {
                    **materialize_candidate(card),
                    "availability_status": "eligible",
                    "corpus_status": (
                        "present"
                        if _gene_key(str(card["canonical_symbol"]))
                        in compatibility.target_symbols
                        else "absent"
                    ),
                }
                for card in candidates.values()
            ]
            materialized.sort(
                key=lambda row: (
                    ANALOG_TIER_RANK[str(row["best_tier"])],
                    str(row["canonical_symbol"]).casefold(),
                )
            )
            page_rows = materialized[offset : offset + limit]
            target_results.append(
                {
                    "requested_target": requested,
                    "canonical_target": canonical,
                    "resolution_status": (
                        "not_in_annotation_store"
                        if _gene_key(requested) in unresolved_target_keys
                        else "resolved_frozen_annotation"
                    ),
                    "resolution_sources": (
                        []
                        if _gene_key(requested) in unresolved_target_keys
                        else ["gene_analog_index"]
                    ),
                    "corpus_status": (
                        "present"
                        if target_key in compatibility.target_symbols
                        else "absent"
                    ),
                    "candidates": page_rows,
                    "page": _page_metadata(
                        offset, limit, len(materialized), len(page_rows)
                    ),
                }
            )

        payload = {
            "schema_version": "distributed_agents-target-analog-suggestions-v1",
            "operation": "target_analogs.suggest",
            "release_id": self.release.release_id,
            "species": {
                "scientific_name": analog_index.metadata["scientific_name"],
                "taxonomy_id": analog_index.metadata["taxonomy_id"],
            },
            "candidate_universe": {
                "source": (
                    "caller_declared_eligible_targets"
                    if caller_declared_eligibility
                    else "selected_release_biological_targets"
                ),
                "supplied_total": len(requested_eligibility),
                "resolved_total": len(canonical_eligible),
                "unresolved_total": len(unresolved_eligible),
                "unresolved_sample": unresolved_eligible[:20],
                "controls_excluded": True,
            },
            "grounding": {
                "artifact": TARGET_ANALOG_ARTIFACT,
                "sha256": self.release.artifact_sha256(TARGET_ANALOG_ARTIFACT),
                "genes": analog_index.metadata["gene_count"],
                "annotation_sets": analog_index.metadata["set_count"],
                "memberships": analog_index.metadata["membership_count"],
                "typed_relationships": analog_index.metadata[
                    "relationship_count"
                ],
                "resources": [
                    "CORUM mouse",
                    "CORUM human projected through strict MGI one-to-one orthology",
                    "GO biological process/cellular component/molecular function",
                    "Reactome",
                    "KEGG mouse",
                    "MSigDB WikiPathways/BioCarta/Hallmark",
                    "functional classes",
                    "STRING v12.0 mouse physical interactions (combined score >= 0.700)",
                    "reciprocal selected-corpus Finding comparators",
                ],
                "query_time_network_access": False,
            },
            "tier_order": list(ANALOG_TIER_RANK),
            "source_limit_per_relationship": source_limit,
            "include_broad_fallback": include_broad,
            "interpretation": {
                "meaning": (
                    "typed biological nomination of eligible comparison targets, "
                    "including for requested targets absent from the corpus"
                ),
                "ordering": (
                    "categorical evidence-tier precedence followed by canonical "
                    "symbol; source confidence is retained as source metadata"
                ),
                "not_a_prediction": True,
                "not_an_aggregate_similarity_score": True,
                "required_next_step": (
                    "evaluate nominated targets in the task-matched measured "
                    "endpoint and context before choosing or weighting comparators"
                ),
            },
            "targets": target_results,
        }
        return _bound_analog_suggestions(payload)

    def _add_reciprocal_analog_comparators(
        self,
        candidates: dict[str, dict[str, Any]],
        *,
        target_key: str,
        eligible_keys: set[str],
        source_limit: int,
    ) -> None:
        index = self.compatibility_claims
        target_symbol = index.target_symbols.get(target_key)
        if target_symbol is None:
            return
        for candidate_key, outgoing in index.explicit_outbound.get(
            target_key, {}
        ).items():
            reverse = index.explicit_outbound.get(candidate_key, {}).get(
                target_key, []
            )
            if candidate_key not in eligible_keys or not reverse:
                continue
            candidate = index.target_symbols[candidate_key]
            source = {
                "kind": "corpus_ledger",
                "resource": "findings",
                "release_id": self.release.release_id,
                "source_id": f"{target_symbol}<->{candidate}",
                "outgoing_finding_ids": sorted(
                    {str(row["doc_id"]) for row in outgoing}, key=str.casefold
                ),
                "reverse_finding_ids": sorted(
                    {str(row["doc_id"]) for row in reverse}, key=str.casefold
                ),
            }
            GeneAnalogIndex._add_source(
                candidates,
                candidate=candidate,
                tier="bidirectional_corpus_comparator",
                tier_rank=ANALOG_TIER_RANK["bidirectional_corpus_comparator"],
                relationship_type="reciprocal_reported_comparator",
                source=source,
                source_limit=source_limit,
            )

    @staticmethod
    def _is_control_target(value: str) -> bool:
        folded = _gene_key(value)
        return folded == "non_target" or folded.startswith("safe_target_")

    def _calibration(self, command: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if command == "story-count":
            self.policy.require(FINDINGS_CAPABILITY)
        else:
            self.policy.require(CALIBRATION_CAPABILITY)
        allowed = {
            "describe": {"query", "limit"},
            "calibrate": {"topic", "limit"},
            "count": {"artifact", "field", "canonical", "limit"},
            "story-count": {"genes", "finding_type", "limit"},
        }[command]
        _check_keys(arguments, allowed)
        argv = [command]
        if command == "describe":
            argv.append(_required_string(arguments, "query"))
        elif command == "calibrate":
            argv.append(_enum(arguments, "topic", self.calibration_topics()))
        elif command == "count":
            argv.extend(
                [
                    "--artifact",
                    _enum(arguments, "artifact", self.count_artifacts()),
                    "--field",
                    _required_string(arguments, "field"),
                ]
            )
            canonical = _optional_string(arguments, "canonical")
            if canonical is not None:
                if canonical != "contradiction":
                    raise CorpusToolError("canonical must be contradiction")
                argv.extend(["--canonical", canonical])
        elif command == "story-count":
            genes = _string_list(arguments, "genes", required=True)
            for gene in genes:
                argv.extend(["--gene", gene])
            finding_type = _optional_string(arguments, "finding_type")
            if finding_type is not None:
                argv.extend(["--finding-type", finding_type])
        argv.extend(["--limit", str(_limit(arguments, default={
            "describe": 10,
            "calibrate": MAX_ROWS,
            "count": 20,
            "story-count": 10,
        }[command]))])
        completed = self._run(self.release.entrypoint("ledger", "calibration"), argv)
        return _parse_json_object(completed.stdout, command)

    def call_describe(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        return self._calibration("describe", arguments)

    def call_calibrate(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if self.supports_compatibility_claims:
            return self._calibrate_compatibility_claims(arguments)
        if self.supports_claim_graph and arguments.get("topic") in {
            "summary",
            "counts",
            "claims",
            "relations",
        }:
            return self._calibrate_bottom_up_claims(arguments)
        return self._calibration("calibrate", arguments)

    def _calibrate_compatibility_claims(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(CALIBRATION_CAPABILITY)
        _check_keys(arguments, {"topic", "limit"})
        topic = _enum(arguments, "topic", self.calibration_topics())
        if "limit" in arguments:
            _limit(arguments, default=MAX_ROWS)
        index = self.compatibility_claims
        role_counts = Counter(
            str(membership["member_role"])
            for memberships in index.memberships_by_claim.values()
            for membership in memberships
        )
        claim_confidence_counts = Counter(
            str(claim["confidence"]) for claim in index.claims_by_id.values()
        )
        relation_type_counts = Counter(
            str(relation["relation_type"]) for relation in index.relations
        )
        relation_confidence_counts = Counter(
            str(relation["confidence"]) for relation in index.relations
        )
        claim_layer = {
            "semantics": (
                "Shi Claim layer with typed, semantically matched Finding memberships"
            ),
            "not_equivalent_to": (
                "an exhaustive partition of all Shi Findings"
            ),
            **index.counts,
            "multi_claim_findings": sum(
                1
                for memberships in index.memberships_by_finding.values()
                if len(memberships) > 1
            ),
            "membership_role_counts": dict(sorted(role_counts.items())),
            "claim_confidence_counts": dict(
                sorted(claim_confidence_counts.items())
            ),
        }
        relation_layer = {
            "semantics": (
                "directed, typed relations between Shi Claims"
            ),
            "requires_reciprocity": False,
            "claim_relations": index.counts["claim_relations"],
            "relation_type_counts": dict(sorted(relation_type_counts.items())),
            "confidence_counts": dict(
                sorted(relation_confidence_counts.items())
            ),
            "explicit_finding_references": {
                "meaning": (
                    "directional Finding.comparators mentions, kept separate from "
                    "Claim-to-Claim relations"
                ),
                "requires_reciprocity": False,
            },
        }
        if topic in {"claim-layer", "claims"}:
            data: Any = claim_layer
        elif topic == "relations":
            data = relation_layer
        else:
            result = self._calibration("calibrate", arguments)
            existing = result.get("data")
            if topic not in {"summary", "counts"}:
                return result
            if not isinstance(existing, Mapping):
                raise CorpusToolError(
                    "compatibility calibration adapter returned invalid data"
                )
            data = dict(existing)
            if topic == "counts":
                data.update(index.counts)
            elif topic == "summary":
                data["compatibility_claim_layer"] = claim_layer
                data["relation_layer"] = relation_layer
            result["data"] = data
            return result
        return {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.calibrate",
            "release_id": self.release.release_id,
            "topic": topic,
            "data": data,
        }

    def _calibrate_bottom_up_claims(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(CALIBRATION_CAPABILITY)
        _check_keys(arguments, {"topic", "limit"})
        topic = _enum(
            arguments,
            "topic",
            ("summary", "counts", "claims", "relations"),
        )
        if "limit" in arguments:
            _limit(arguments, default=MAX_ROWS)
        index = self.claim_graph
        confidence_counts = Counter(
            str(claim.get("confidence") or "")
            for claim in index.claims_by_id.values()
        )
        role_counts = Counter(
            str(edge["role"])
            for edges in index.contributions_by_claim.values()
            for edge in edges
        )
        compatibility_counts = {
            name: self.release.payload["artifacts"][name]["records"]
            for name in ("claim_assignments", "claim_relations")
            if name in self.release.artifact_names
        }
        claim_layer = {
            "semantics": (
                "frozen bottom-up higher-order biological propositions with "
                "many-to-many typed Finding contributions"
            ),
            "claims": index.counts["claims"],
            "claim_contributions": index.counts["claim_contributions"],
            "targets_with_claim_contributions": len(index.claim_ids_by_target),
            "findings_with_claim_contributions": index.counts[
                "findings_with_claim_contributions"
            ],
            "findings_without_claim_contributions": index.counts[
                "findings_without_claim_contributions"
            ],
            "confidence_counts": dict(sorted(confidence_counts.items())),
            "contribution_role_counts": dict(sorted(role_counts.items())),
            "finding_dispositions": index.counts["finding_dispositions"],
        }
        relation_layer = {
            "semantic_claim_to_claim_relations": {
                "present": False,
                "meaning": "No Claim-to-Claim relation is frozen in this release.",
            },
            "explicit_finding_references": {
                "meaning": (
                    "Directional Finding.comparators mentions; one-sided references "
                    "remain valid and do not imply agreement or effect direction."
                ),
                "requires_reciprocity": False,
            },
            "structural_compatibility_tables": {
                "records": compatibility_counts,
                "meaning": (
                    "pre-Claim review adapter only; not semantic Claims or the "
                    "agent-facing relation substrate"
                ),
            },
        }
        if topic == "claims":
            data = claim_layer
        elif topic == "relations":
            data = relation_layer
        elif topic == "counts":
            data = {
                "findings": index.counts["findings"],
                "claims": index.counts["claims"],
                "claim_contributions": index.counts["claim_contributions"],
                "findings_with_claim_contributions": index.counts[
                    "findings_with_claim_contributions"
                ],
                "findings_without_claim_contributions": index.counts[
                    "findings_without_claim_contributions"
                ],
            }
        else:
            data = {
                "counts": {
                    "findings": index.counts["findings"],
                    "claims": index.counts["claims"],
                    "claim_contributions": index.counts["claim_contributions"],
                },
                "claim_layer": claim_layer,
                "relation_layer": relation_layer,
            }
        return {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.calibrate",
            "release_id": self.release.release_id,
            "topic": topic,
            "data": data,
        }

    def call_count(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if (
            self.supports_compatibility_claims
            and arguments.get("artifact") in {"claims", "relations"}
        ):
            return self._count_compatibility_claims(arguments)
        if self.supports_claim_graph and arguments.get("artifact") == "claims":
            return self._count_bottom_up_claims(arguments)
        return self._calibration("count", arguments)

    def _count_compatibility_claims(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(CALIBRATION_CAPABILITY)
        _check_keys(arguments, {"artifact", "field", "canonical", "limit"})
        artifact = _enum(arguments, "artifact", ("claims", "relations"))
        if _optional_string(arguments, "canonical") is not None:
            raise CorpusToolError(
                "canonical is defined only for Finding literature-status counts"
            )
        field = _required_string(arguments, "field")
        index = self.compatibility_claims
        counts: Counter[str] = Counter()
        if artifact == "claims":
            allowed_fields = {
                "active_default",
                "cell_scope",
                "confidence",
                "de_direction",
                "de_support_level",
                "evidence_mode",
                "finding_types",
                "member_count",
                "member_role",
                "relation_family",
                "support_level",
                "target_genes",
            }
            if field not in allowed_fields:
                raise CorpusToolError(
                    "compatibility Claim field must be one of: "
                    + ", ".join(sorted(allowed_fields))
                )
            if field == "member_role":
                values = (
                    membership["member_role"]
                    for memberships in index.memberships_by_claim.values()
                    for membership in memberships
                )
                counts.update(str(value) for value in values)
            else:
                for claim in index.claims_by_id.values():
                    value = claim.get(field)
                    values = value if isinstance(value, list) else [value]
                    counts.update(str(item) for item in values if item is not None)
        else:
            allowed_fields = {"confidence", "relation_type"}
            if field not in allowed_fields:
                raise CorpusToolError(
                    "compatibility Claim relation field must be one of: "
                    + ", ".join(sorted(allowed_fields))
                )
            counts.update(str(relation[field]) for relation in index.relations)
        records = [
            {"value": value, "count": count}
            for value, count in sorted(
                counts.items(), key=lambda item: (-item[1], item[0])
            )
        ]
        limit = _limit(arguments, default=20)
        emitted = records[:limit]
        return _bound_list_fields(
            {
                "schema_version": "distributed_agents-corpus-mcp-v1",
                "operation": "corpus.compatibility_claims.count",
                "release_id": self.release.release_id,
                "artifact": artifact,
                "field": field,
                "values": emitted,
                "page": _page_metadata(0, limit, len(records), len(emitted)),
            },
            ("values",),
        )

    def call_find_shared_claims(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        if self.supports_claim_graph:
            return self._find_shared_claims_bottom_up(arguments)
        result = self._calibration("story-count", arguments)
        claims = result.get("claims")
        truncation = result.get("truncation")
        if not isinstance(claims, list) or not isinstance(truncation, Mapping):
            raise CorpusToolError("shared-Claim adapter returned an invalid response shape")
        exact_total = int(result.get("distinct_claims", truncation.get("exact_total", 0)))
        limit = _limit(arguments, default=10)
        return _bound_list_fields(
            {
                "schema_version": "distributed_agents-corpus-mcp-v1",
                "operation": "corpus.claims.find_shared",
                "release_id": self.release.release_id,
                "claim_semantics": "release-declared Claims containing every requested gene",
                "genes": list(result.get("genes") or []),
                "finding_type": result.get("finding_type"),
                "distinct_claims": exact_total,
                "claims": claims,
                "page": _page_metadata(0, limit, exact_total, len(claims)),
            },
            ("claims",),
        )

    def _count_bottom_up_claims(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(CALIBRATION_CAPABILITY)
        _check_keys(arguments, {"artifact", "field", "canonical", "limit"})
        if _enum(arguments, "artifact", self.count_artifacts()) != "claims":
            raise CorpusToolError("bottom-up Claim counting requires artifact=claims")
        if _optional_string(arguments, "canonical") is not None:
            raise CorpusToolError("canonical is not defined for bottom-up Claim counts")
        field = _required_string(arguments, "field")
        allowed_fields = {
            "confidence",
            "contribution_count",
            "target_genes",
            "claim_scope",
        }
        if field not in allowed_fields:
            raise CorpusToolError(
                "bottom-up Claim field must be one of: "
                + ", ".join(sorted(allowed_fields))
            )
        counts: Counter[str] = Counter()
        for claim in self.claim_graph.claims_by_id.values():
            value = claim.get(field)
            values = value if isinstance(value, list) else [value]
            counts.update(str(item) for item in values if item is not None)
        records = [
            {"value": value, "count": count}
            for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]
        limit = _limit(arguments, default=20)
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.claims.count",
            "release_id": self.release.release_id,
            "artifact": "claims",
            "field": field,
            "values": records[:limit],
            "page": _page_metadata(0, limit, len(records), min(limit, len(records))),
        }
        return _bound_list_fields(payload, ("values",))

    def _find_shared_claims_bottom_up(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"genes", "finding_type", "limit"})
        requested = {_gene_key(value) for value in _string_list(arguments, "genes", required=True)}
        finding_type = _optional_string(arguments, "finding_type")
        selected: list[dict[str, Any]] = []
        for claim_id, claim in self.claim_graph.claims_by_id.items():
            targets = {_gene_key(str(value)) for value in claim.get("target_genes") or []}
            if not requested.issubset(targets):
                continue
            if finding_type and not any(
                self.claim_graph.findings_by_doc[str(edge["finding_doc_id"])].get(
                    "finding_type"
                )
                == finding_type
                for edge in self.claim_graph.contributions_by_claim[claim_id]
            ):
                continue
            selected.append(self.claim_graph.claim_card(claim))
        selected.sort(
            key=lambda row: _stable_hash_key(
                "story-count:" + "|".join(sorted(requested)), str(row["claim_id"])
            )
        )
        limit = _limit(arguments, default=10)
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.claims.find_shared",
            "release_id": self.release.release_id,
            "claim_semantics": "frozen bottom-up higher-order Claims with typed Finding contributions",
            "genes": sorted(requested),
            "finding_type": finding_type,
            "distinct_claims": len(selected),
            "claims": selected[:limit],
            "page": _page_metadata(0, limit, len(selected), min(limit, len(selected))),
        }
        return _bound_list_fields(payload, ("claims",))

    def call_query_ledger(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        allowed = {"ledger", "genes", "finding_types", "fields", "ids", "limit"}
        if self.supports_compatibility_claims:
            allowed.add("offset")
        _check_keys(arguments, allowed)
        ledger = _enum(arguments, "ledger", self.allowed_ledgers())
        self.policy.require(FINDINGS_CAPABILITY)
        if self.supports_compatibility_claims and ledger == "findings":
            return self._query_compatibility_findings(arguments)
        genes = _string_list(arguments, "genes")
        finding_types = _string_list(arguments, "finding_types")
        ids = _string_list(arguments, "ids")
        fields = _string_list(arguments, "fields")
        if any(not SAFE_FIELD.fullmatch(field) for field in fields):
            raise CorpusToolError("fields must be simple record field names")
        limit = _limit(arguments, default=20)
        entrypoint = self.release.entrypoint("ledger", "query")
        if entrypoint.name == "query_findings.py":
            if ledger != "findings" or ids:
                raise CorpusToolError("the selected release supports only Finding lookup without ID filters")
            argv: list[str] = []
        else:
            argv = [ledger]
        for gene in genes:
            argv.extend(["--gene", gene])
        for finding_type in finding_types:
            argv.extend(["--finding-type", finding_type])
        for local_id in ids:
            argv.extend(["--id", local_id])
        if fields:
            argv.extend(["--fields", ",".join(fields)])
        query_limit = limit + 1 if entrypoint.name == "query_ledger.py" else limit
        argv.extend(["--limit", str(query_limit), "--json"])
        completed = self._run(entrypoint, argv)
        records = _parse_json_lines(completed.stdout)
        has_more = len(records) > limit
        records = records[:limit]
        payload: dict[str, Any] = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.ledger.query",
            "release_id": self.release.release_id,
            "ledger": ledger,
            "records": records,
            "truncation": {
                "truncated": has_more,
                "exact_total": None,
                "emitted": len(records),
                "max_rows": MAX_ROWS,
                "max_output_bytes": MAX_OUTPUT_BYTES,
            },
        }
        return _bound_records(payload)

    def _query_compatibility_findings(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        index = self.compatibility_claims
        genes = _string_list(arguments, "genes")
        finding_types = _string_list(arguments, "finding_types")
        ids = _string_list(arguments, "ids")
        fields = _string_list(arguments, "fields")
        if any(not SAFE_FIELD.fullmatch(field) for field in fields):
            raise CorpusToolError("fields must be simple record field names")
        local_ids = [value for value in ids if ":" not in value]
        if local_ids and not genes:
            raise CorpusToolError(
                "local Finding IDs require at least one target-gene filter; use target:ID for exact lookup"
            )
        gene_keys = {_gene_key(value) for value in genes}
        type_keys = {value.casefold() for value in finding_types}
        doc_keys = {value.casefold() for value in ids if ":" in value}
        local_keys = {value.casefold() for value in local_ids}
        selected: list[dict[str, Any]] = []
        for finding in index.findings_by_doc.values():
            if gene_keys and _gene_key(str(finding["target_gene"])) not in gene_keys:
                continue
            if type_keys and str(finding["finding_type"]).casefold() not in type_keys:
                continue
            if ids and not (
                str(finding["doc_id"]).casefold() in doc_keys
                or str(finding["finding_id"]).casefold() in local_keys
            ):
                continue
            selected.append(finding)
        selected.sort(key=lambda row: str(row["doc_id"]).casefold())
        if fields:
            available = set(next(iter(index.findings_by_doc.values())))
            unknown = sorted(set(fields) - available)
            if unknown:
                raise CorpusToolError(
                    "unknown Finding fields: " + ", ".join(unknown)
                )
            records = [
                {field: finding.get(field) for field in fields}
                for finding in selected
            ]
        else:
            records = [dict(finding) for finding in selected]
        limit = _limit(arguments, default=20)
        offset = _offset(arguments, "offset")
        emitted = records[offset : offset + limit]
        return _bound_list_fields(
            {
                "schema_version": "distributed_agents-corpus-mcp-v1",
                "operation": "corpus.ledger.query",
                "release_id": self.release.release_id,
                "ledger": "findings",
                "filters": {
                    "genes": genes,
                    "finding_types": finding_types,
                    "ids": ids,
                },
                "complete_records": not fields,
                "records": emitted,
                "page": _page_metadata(
                    offset, limit, len(records), len(emitted)
                ),
            },
            ("records",),
        )

    def call_search_findings(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        if not self.supports_findings_bm25:
            raise CorpusToolError(
                "selected release does not declare Finding-native BM25 retrieval"
            )
        allowed = {"queries", "level", "finding_type", "limit"}
        if self.supports_compatibility_claims:
            allowed.add("offset")
        _check_keys(arguments, allowed)
        queries = _string_list(arguments, "queries", required=True)
        if len(queries) > 8:
            raise CorpusToolError("queries must contain at most 8 values")
        level = _enum(
            arguments,
            "level",
            ("finding", "target"),
            default="finding",
        )
        limit = _limit(arguments, default=12)
        offset = _offset(arguments, "offset") if self.supports_compatibility_claims else 0
        argv = ["search"]
        for query in queries:
            argv.extend(["--query", query])
        argv.extend(
            [
                "--level",
                level,
                "--top-k",
                str(limit),
                "--index-path",
                str(self.release.artifact(FINDINGS_BM25_ARTIFACT)),
                "--findings-path",
                str(self.release.artifact("findings")),
                "--expected-source-sha256",
                self.release.artifact_sha256("findings"),
                "--expected-release-id",
                self.release.release_id,
            ]
        )
        if self.supports_compatibility_claims:
            argv.extend(["--offset", str(offset)])
        finding_type = _optional_string(arguments, "finding_type")
        if finding_type is not None:
            argv.extend(["--finding-type", finding_type])
        completed = self._run(
            self.release.entrypoint(FINDINGS_BM25_ROLE, "query"), argv
        )
        payload = _parse_json_object(completed.stdout, "search_findings")
        if payload.get("release_id") != self.release.release_id:
            raise CorpusToolError(
                "search_findings adapter returned the wrong corpus release"
            )
        if payload.get("operation") != "corpus.findings.bm25_search":
            raise CorpusToolError(
                "search_findings adapter returned an unexpected operation"
            )
        return _bound_list_fields(payload, ("results",))

    def call_query_claims(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(
            arguments,
            {
                "claim_ids",
                "genes",
                "query",
                "confidence",
                "member_roles",
                "relation_types",
                "include_memberships",
                "include_relations",
                "limit",
                "offset",
            },
        )
        index = self.compatibility_claims
        claim_ids = _string_list(arguments, "claim_ids")
        requested_id_keys = {value.casefold() for value in claim_ids}
        requested_id_positions = {
            value.casefold(): position for position, value in enumerate(claim_ids)
        }
        requested_genes = {
            _gene_key(value) for value in _string_list(arguments, "genes")
        }
        requested_roles = {
            value.casefold() for value in _string_list(arguments, "member_roles")
        }
        requested_relation_types = {
            value.casefold()
            for value in _string_list(arguments, "relation_types")
        }
        confidence = _optional_string(arguments, "confidence")
        query = _optional_string(arguments, "query")
        terms = sorted(set(_search_terms(query))) if query is not None else []
        if query is not None and not terms:
            raise CorpusToolError("query must contain at least one letter or digit")
        query_folded = query.casefold() if query is not None else ""
        include_memberships = _boolean(
            arguments, "include_memberships", default=False
        )
        include_relations = _boolean(
            arguments, "include_relations", default=False
        )

        matches: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        for claim_id, claim in index.claims_by_id.items():
            if requested_id_keys and claim_id.casefold() not in requested_id_keys:
                continue
            claim_targets = {
                _gene_key(str(value))
                for value in [
                    *(claim.get("target_genes") or []),
                    *(claim.get("targets") or []),
                ]
            }
            if requested_genes and not requested_genes.issubset(claim_targets):
                continue
            if confidence is not None and str(claim["confidence"]).casefold() != confidence.casefold():
                continue
            memberships = index.memberships_by_claim[claim_id]
            if requested_roles and not requested_roles.intersection(
                str(row["member_role"]).casefold() for row in memberships
            ):
                continue
            relations = index.relations_by_claim.get(claim_id, [])
            if requested_relation_types and not requested_relation_types.intersection(
                str(row["relation_type"]).casefold() for row in relations
            ):
                continue

            searchable = {
                "canonical_summary": str(claim["canonical_summary"]),
                "relation_family": str(claim["relation_family"]),
                "direction_pattern": str(claim["direction_pattern"]),
                "evidence_mode": str(claim["evidence_mode"]),
                "cell_scope": str(claim["cell_scope"]),
                "targets": " ".join(str(value) for value in claim["targets"]),
                "readouts": " ".join(str(value) for value in claim["readouts"]),
                "finding_types": " ".join(
                    str(value) for value in claim["finding_types"]
                ),
                "target_genes": " ".join(
                    str(value) for value in claim["target_genes"]
                ),
            }
            folded = {name: value.casefold() for name, value in searchable.items()}
            matched_terms = [
                term for term in terms if any(term in value for value in folded.values())
            ]
            phrase_match = bool(
                query_folded
                and any(query_folded in value for value in folded.values())
            )
            if query is not None and not matched_terms and not phrase_match:
                continue
            record = index.claim_card(claim)
            record["relation_count"] = len(relations)
            if query is not None:
                record["retrieval_match"] = {
                    "phrase_match": phrase_match,
                    "matched_terms": matched_terms,
                    "matched_fields": [
                        name
                        for name, value in folded.items()
                        if query_folded in value
                        or any(term in value for term in terms)
                    ],
                    "query_term_coverage": len(matched_terms) / len(terms),
                }
            if include_memberships:
                emitted_memberships = memberships[:MAX_ROWS]
                record["memberships"] = [
                    index.membership_card(row) for row in emitted_memberships
                ]
                record["memberships_complete"] = len(emitted_memberships) == len(
                    memberships
                )
            if include_relations:
                emitted_relations = relations[:MAX_ROWS]
                record["relations"] = [
                    index.relation_card(row) for row in emitted_relations
                ]
                record["relations_complete"] = len(emitted_relations) == len(
                    relations
                )
            exact_position = requested_id_positions.get(
                claim_id.casefold(), len(claim_ids)
            )
            key = (
                0 if requested_id_keys else 1,
                exact_position,
                0 if phrase_match else 1,
                -len(matched_terms),
                _stable_hash_key(
                    f"compatibility-claim-query:{query_folded}", claim_id
                ),
            )
            matches.append((key, record))
        matches.sort(key=lambda item: item[0])
        records = [record for _, record in matches]
        limit = _limit(arguments, default=10)
        offset = _offset(arguments, "offset")
        emitted = records[offset : offset + limit]
        found_id_keys = {
            str(record["claim_id"]).casefold() for record in records
        }
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.compatibility_claims.query",
            "release_id": self.release.release_id,
            "claim_semantics": (
                "Shi Claims with typed Finding memberships"
            ),
            "filters": {
                "claim_ids": claim_ids,
                "genes": sorted(requested_genes),
                "query": query,
                "confidence": confidence,
                "member_roles": sorted(requested_roles),
                "relation_types": sorted(requested_relation_types),
            },
            "unmatched_claim_ids": [
                claim_id
                for claim_id in claim_ids
                if claim_id.casefold() not in found_id_keys
            ],
            "retrieval_semantics": (
                "exact filters plus lexical matching over frozen Claim fields; "
                "deterministic order is not biological rank"
            ),
            "claims": emitted,
            "page": _page_metadata(offset, limit, len(records), len(emitted)),
        }
        return _bound_list_fields(payload, ("claims",))

    def _compatibility_relation_path(
        self,
        relation: Mapping[str, Any],
        *,
        direction: str,
        path_detail: str,
    ) -> dict[str, Any]:
        index = self.compatibility_claims
        source_id = str(relation["source_claim_id"])
        target_id = str(relation["target_claim_id"])
        compact = {
            "direction": direction,
            "source_claim_id": source_id,
            "target_claim_id": target_id,
            "relation_type": relation["relation_type"],
            "confidence": relation["confidence"],
            "source_member_roles": sorted(
                {
                    str(row["member_role"])
                    for row in index.memberships_by_claim[source_id]
                }
            ),
            "target_member_roles": sorted(
                {
                    str(row["member_role"])
                    for row in index.memberships_by_claim[target_id]
                }
            ),
        }
        if path_detail == "ids":
            return compact
        return {
            **compact,
            "relation": index.relation_card(relation),
            "source_claim": index.claim_card(index.claims_by_id[source_id]),
            "target_claim": index.claim_card(index.claims_by_id[target_id]),
            "source_memberships": [
                index.membership_card(row)
                for row in index.memberships_by_claim[source_id]
            ],
            "target_memberships": [
                index.membership_card(row)
                for row in index.memberships_by_claim[target_id]
            ],
        }

    def _compatibility_shared_claim_path(
        self,
        claim_id: str,
        *,
        source_key: str,
        related_key: str,
        path_detail: str,
    ) -> dict[str, Any]:
        index = self.compatibility_claims
        source_memberships = [
            row
            for row in index.memberships_by_claim[claim_id]
            if _gene_key(str(row["target_gene"])) == source_key
        ]
        related_memberships = [
            row
            for row in index.memberships_by_claim[claim_id]
            if _gene_key(str(row["target_gene"])) == related_key
        ]
        compact = {
            "claim_id": claim_id,
            "source_member_roles": sorted(
                {str(row["member_role"]) for row in source_memberships}
            ),
            "related_member_roles": sorted(
                {str(row["member_role"]) for row in related_memberships}
            ),
            "source_finding_doc_ids": sorted(
                {str(row["finding_doc_id"]) for row in source_memberships}
            ),
            "related_finding_doc_ids": sorted(
                {str(row["finding_doc_id"]) for row in related_memberships}
            ),
        }
        if path_detail == "ids":
            return compact
        return {
            **compact,
            "claim": index.claim_card(index.claims_by_id[claim_id]),
            "source_memberships": [
                index.membership_card(row) for row in source_memberships
            ],
            "related_memberships": [
                index.membership_card(row) for row in related_memberships
            ],
        }

    def _compatibility_finding_path(
        self,
        finding: Mapping[str, Any],
        *,
        direction: str,
        path_detail: str,
    ) -> dict[str, Any]:
        if path_detail == "full":
            return {
                "direction": direction,
                "finding": self.compatibility_claims.finding_card(finding),
            }
        return {
            "direction": direction,
            **self.compatibility_claims.finding_path_id_card(finding),
        }

    def call_resolve_evidence(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(EVIDENCE_CAPABILITY)
        _check_keys(arguments, {"gene", "finding", "evidence_ids", "ref_ids", "mode"})
        argv = ["--gene", _required_string(arguments, "gene")]
        finding = _optional_string(arguments, "finding")
        if finding is not None:
            argv.extend(["--finding", finding])
        for evidence_id in _string_list(arguments, "evidence_ids"):
            argv.extend(["--evidence-id", evidence_id])
        for ref_id in _string_list(arguments, "ref_ids"):
            argv.extend(["--ref-id", ref_id])
        mode = _enum(arguments, "mode", ("both", "evidence", "references"), default="both")
        if mode == "evidence":
            argv.append("--evidence-only")
        elif mode == "references":
            argv.append("--refs-only")
        argv.append("--json")
        completed = self._run(self.release.entrypoint("ledger", "resolve_evidence"), argv)
        result = _parse_json_object(completed.stdout, "resolve_evidence")
        return _bound_evidence(result, self.release.release_id)

    def _target_claim_record(self, claim_id: str, target_key: str) -> dict[str, Any]:
        index = self.claim_graph
        contributions = [
            index.contribution_card(edge)
            for edge in index.contributions_by_claim[claim_id]
            if _gene_key(str(edge["target_gene"])) == target_key
        ]
        return {
            **index.claim_card(index.claims_by_id[claim_id]),
            "target_contributions": contributions,
        }

    def _finding_context_record(self, finding: Mapping[str, Any]) -> dict[str, Any]:
        index = self.claim_graph
        doc_id = str(finding["doc_id"])
        return {
            **index.finding_card(finding),
            "claim_disposition": index.dispositions_by_doc.get(doc_id),
            "claim_contributions": [
                index.contribution_card(edge)
                for edge in index.contributions_by_finding.get(doc_id, [])
            ],
        }

    def _explicit_reference_records(self, target_key: str) -> list[dict[str, Any]]:
        index = self.claim_graph
        records: list[dict[str, Any]] = []
        for related_key, findings in index.explicit_outbound.get(target_key, {}).items():
            for finding in findings:
                records.append(
                    {
                        "direction": "outbound",
                        "source_target": index.target_symbols[target_key],
                        "referenced_target": index.target_symbols[related_key],
                        "finding": index.finding_card(finding),
                    }
                )
        for source_key, targets in index.explicit_outbound.items():
            for finding in targets.get(target_key, []):
                records.append(
                    {
                        "direction": "inbound",
                        "source_target": index.target_symbols[source_key],
                        "referenced_target": index.target_symbols[target_key],
                        "finding": index.finding_card(finding),
                    }
                )
        records.sort(
            key=lambda row: (
                str(row["direction"]),
                str(row["source_target"]).casefold(),
                str(row["referenced_target"]).casefold(),
                str(row["finding"]["doc_id"]),
            )
        )
        return records

    def call_target_context(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(
            arguments,
            {
                "target",
                "claim_limit",
                "claim_offset",
                "finding_limit",
                "finding_offset",
                "reference_limit",
                "reference_offset",
            },
        )
        target = _required_string(arguments, "target")
        target_key, canonical_target = self.claim_graph.canonical_target(target)
        claim_limit = _limit_named(arguments, "claim_limit", default=10)
        claim_offset = _offset(arguments, "claim_offset")
        finding_limit = _limit_named(arguments, "finding_limit", default=10)
        finding_offset = _offset(arguments, "finding_offset")
        reference_limit = _limit_named(arguments, "reference_limit", default=10)
        reference_offset = _offset(arguments, "reference_offset")

        claim_ids = sorted(
            self.claim_graph.claim_ids_by_target.get(target_key, set()),
            key=lambda value: _stable_hash_key(f"target-context:{target_key}", value),
        )
        claim_records = [
            self._target_claim_record(claim_id, target_key) for claim_id in claim_ids
        ]
        finding_records = [
            self._finding_context_record(row)
            for row in self.claim_graph.findings_by_target.get(target_key, [])
        ]
        reference_records = self._explicit_reference_records(target_key)

        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.target.context",
            "release_id": self.release.release_id,
            "target": canonical_target,
            "target_found": target_key in self.claim_graph.target_symbols,
            "claims": claim_records[claim_offset : claim_offset + claim_limit],
            "claims_page": _page_metadata(
                claim_offset,
                claim_limit,
                len(claim_records),
                len(claim_records[claim_offset : claim_offset + claim_limit]),
            ),
            "findings": finding_records[
                finding_offset : finding_offset + finding_limit
            ],
            "findings_page": _page_metadata(
                finding_offset,
                finding_limit,
                len(finding_records),
                len(finding_records[finding_offset : finding_offset + finding_limit]),
            ),
            "explicit_references": reference_records[
                reference_offset : reference_offset + reference_limit
            ],
            "explicit_references_page": _page_metadata(
                reference_offset,
                reference_limit,
                len(reference_records),
                len(
                    reference_records[
                        reference_offset : reference_offset + reference_limit
                    ]
                ),
            ),
            "ordering": {
                "claims": "deterministic hash order, not biological rank",
                "findings": "stable Finding doc ID",
                "explicit_references": "direction and stable source identity",
            },
        }
        return _bound_list_fields(
            payload,
            ("claims", "findings", "explicit_references"),
        )

    def call_search_claims(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"query", "targets", "confidence", "limit", "offset"})
        query = _required_string(arguments, "query")
        terms = sorted(set(_search_terms(query)))
        if not terms:
            raise CorpusToolError("query must contain at least one letter or digit")
        requested_targets = {
            _gene_key(value) for value in _string_list(arguments, "targets")
        }
        confidence = _optional_string(arguments, "confidence")
        if confidence is not None and confidence not in {"high", "moderate", "low"}:
            raise CorpusToolError("confidence must be one of: high, moderate, low")

        matches: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        query_folded = query.casefold()
        for claim in self.claim_graph.claims_by_id.values():
            claim_targets = {
                _gene_key(str(value)) for value in claim.get("target_genes") or []
            }
            if requested_targets and not requested_targets.issubset(claim_targets):
                continue
            if confidence is not None and claim.get("confidence") != confidence:
                continue
            searchable = {
                "statement": str(claim.get("statement") or ""),
                "scope": str(claim.get("scope") or ""),
                "higher_order_basis": str(claim.get("higher_order_basis") or ""),
                "target_genes": " ".join(str(value) for value in claim.get("target_genes") or []),
            }
            folded = {name: value.casefold() for name, value in searchable.items()}
            matched_terms = [
                term for term in terms if any(term in value for value in folded.values())
            ]
            phrase_match = any(query_folded in value for value in folded.values())
            if not matched_terms and not phrase_match:
                continue
            matched_fields = [
                name
                for name, value in folded.items()
                if query_folded in value or any(term in value for term in terms)
            ]
            claim_id = str(claim["claim_id"])
            record = {
                **self.claim_graph.claim_card(claim),
                "retrieval_match": {
                    "phrase_match": phrase_match,
                    "matched_terms": matched_terms,
                    "matched_fields": matched_fields,
                    "query_term_coverage": len(matched_terms) / len(terms),
                },
            }
            key = (
                0 if phrase_match else 1,
                -len(matched_terms),
                _stable_hash_key(f"claim-search:{query_folded}", claim_id),
            )
            matches.append((key, record))
        matches.sort(key=lambda item: item[0])
        records = [record for _, record in matches]
        limit = _limit(arguments, default=10)
        offset = _offset(arguments, "offset")
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.claims.search",
            "release_id": self.release.release_id,
            "query": query,
            "filters": {
                "targets": sorted(requested_targets),
                "confidence": confidence,
            },
            "retrieval_semantics": (
                "lexical relevance over frozen Claim fields, then deterministic hash; "
                "not semantic similarity or biological rank"
            ),
            "claims": records[offset : offset + limit],
            "page": _page_metadata(
                offset,
                limit,
                len(records),
                len(records[offset : offset + limit]),
            ),
        }
        return _bound_list_fields(payload, ("claims",))

    def call_get_claim(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"claim_id", "include_findings"})
        claim_id = _required_string(arguments, "claim_id")
        claim = self.claim_graph.claims_by_id.get(claim_id)
        if claim is None:
            raise CorpusToolError(f"unknown bottom-up Claim ID: {claim_id}")
        include_findings = _boolean(arguments, "include_findings", default=True)
        contributions = []
        for edge in self.claim_graph.contributions_by_claim[claim_id]:
            record = self.claim_graph.contribution_card(edge)
            if include_findings:
                record["finding"] = self.claim_graph.finding_card(
                    self.claim_graph.findings_by_doc[str(edge["finding_doc_id"])]
                )
            contributions.append(record)
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.claim.get",
            "release_id": self.release.release_id,
            "claim": claim,
            "contributions": contributions,
            "contribution_total": len(contributions),
            "complete": True,
        }
        if _json_size(payload) > MAX_OUTPUT_BYTES:
            raise CorpusToolError(
                "complete Claim exceeds output bound; retry with include_findings=false"
            )
        return payload

    def call_get_finding(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"finding_doc_id"})
        finding_doc_id = _required_string(arguments, "finding_doc_id")
        finding = self.claim_graph.findings_by_doc_key.get(finding_doc_id.casefold())
        if finding is None:
            raise CorpusToolError(f"unknown Finding doc ID: {finding_doc_id}")
        doc_id = str(finding["doc_id"])
        contributions = []
        for edge in self.claim_graph.contributions_by_finding.get(doc_id, []):
            claim_id = str(edge["claim_id"])
            contributions.append(
                {
                    **self.claim_graph.contribution_card(edge),
                    "claim": self.claim_graph.claim_card(
                        self.claim_graph.claims_by_id[claim_id]
                    ),
                }
            )
        target_key = _gene_key(str(finding["target_gene"]))
        explicit_targets = []
        for related_key, rows in self.claim_graph.explicit_outbound.get(
            target_key, {}
        ).items():
            if any(str(row["doc_id"]) == doc_id for row in rows):
                explicit_targets.append(self.claim_graph.target_symbols[related_key])
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.finding.get",
            "release_id": self.release.release_id,
            "finding": finding,
            "claim_disposition": self.claim_graph.dispositions_by_doc.get(doc_id),
            "claim_contributions": contributions,
            "explicit_target_references": sorted(explicit_targets, key=str.casefold),
        }
        if _json_size(payload) > MAX_OUTPUT_BYTES:
            raise CorpusToolError("Finding detail exceeds the output byte ceiling")
        return payload

    def call_compare_targets(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"left_target", "right_target", "limit", "offset"})
        left_key, left = self.claim_graph.canonical_target(
            _required_string(arguments, "left_target")
        )
        right_key, right = self.claim_graph.canonical_target(
            _required_string(arguments, "right_target")
        )
        if left_key == right_key:
            raise CorpusToolError("left_target and right_target must be distinct")
        shared_ids = self.claim_graph.claim_ids_by_target.get(left_key, set()).intersection(
            self.claim_graph.claim_ids_by_target.get(right_key, set())
        )
        shared = []
        for claim_id in sorted(
            shared_ids,
            key=lambda value: _stable_hash_key(
                f"compare:{left_key}:{right_key}", value
            ),
        ):
            edges = self.claim_graph.contributions_by_claim[claim_id]
            shared.append(
                {
                    "claim": self.claim_graph.claim_card(
                        self.claim_graph.claims_by_id[claim_id]
                    ),
                    "left_contributions": [
                        self.claim_graph.contribution_card(edge)
                        for edge in edges
                        if _gene_key(str(edge["target_gene"])) == left_key
                    ],
                    "right_contributions": [
                        self.claim_graph.contribution_card(edge)
                        for edge in edges
                        if _gene_key(str(edge["target_gene"])) == right_key
                    ],
                }
            )

        def direct(source_key: str, target_key: str) -> list[dict[str, Any]]:
            return [
                {
                    "source_target": self.claim_graph.target_symbols.get(
                        source_key, source_key
                    ),
                    "referenced_target": self.claim_graph.target_symbols.get(
                        target_key, target_key
                    ),
                    "finding": self.claim_graph.finding_card(finding),
                }
                for finding in self.claim_graph.explicit_outbound.get(
                    source_key, {}
                ).get(target_key, [])
            ]

        left_to_right = direct(left_key, right_key)
        right_to_left = direct(right_key, left_key)
        limit = _limit(arguments, default=20)
        offset = _offset(arguments, "offset")
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.targets.compare",
            "release_id": self.release.release_id,
            "left_target": left,
            "right_target": right,
            "shared_claims": shared[offset : offset + limit],
            "shared_claims_page": _page_metadata(
                offset, limit, len(shared), len(shared[offset : offset + limit])
            ),
            "left_to_right_references": left_to_right[offset : offset + limit],
            "left_to_right_page": _page_metadata(
                offset,
                limit,
                len(left_to_right),
                len(left_to_right[offset : offset + limit]),
            ),
            "right_to_left_references": right_to_left[offset : offset + limit],
            "right_to_left_page": _page_metadata(
                offset,
                limit,
                len(right_to_left),
                len(right_to_left[offset : offset + limit]),
            ),
            "interpretation": (
                "Shared Claims and explicit references are independent lanes; "
                "an empty reciprocal lane does not invalidate a one-sided Finding."
            ),
        }
        return _bound_list_fields(
            payload,
            (
                "shared_claims",
                "left_to_right_references",
                "right_to_left_references",
            ),
        )

    def call_related_targets(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if self.supports_compatibility_claims:
            return self._call_compatibility_related_targets(arguments)
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(arguments, {"target", "basis", "limit", "offset"})
        target_key, target = self.claim_graph.canonical_target(
            _required_string(arguments, "target")
        )
        basis = _enum(
            arguments,
            "basis",
            ("both", "shared_claim", "explicit_finding_reference"),
            default="both",
        )
        related: defaultdict[str, dict[str, Any]] = defaultdict(
            lambda: {"shared_claim_paths": [], "explicit_finding_paths": []}
        )
        if basis in {"both", "shared_claim"}:
            for claim_id in self.claim_graph.claim_ids_by_target.get(target_key, set()):
                edges = self.claim_graph.contributions_by_claim[claim_id]
                source_edges = [
                    self.claim_graph.contribution_card(edge)
                    for edge in edges
                    if _gene_key(str(edge["target_gene"])) == target_key
                ]
                for related_key in {
                    _gene_key(str(edge["target_gene"]))
                    for edge in edges
                    if _gene_key(str(edge["target_gene"])) != target_key
                }:
                    related[related_key]["shared_claim_paths"].append(
                        {
                            "claim_id": claim_id,
                            "statement": self.claim_graph.claims_by_id[claim_id][
                                "statement"
                            ],
                            "source_contributions": source_edges,
                            "related_contributions": [
                                self.claim_graph.contribution_card(edge)
                                for edge in edges
                                if _gene_key(str(edge["target_gene"])) == related_key
                            ],
                        }
                    )
        if basis in {"both", "explicit_finding_reference"}:
            for related_key, findings in self.claim_graph.explicit_outbound.get(
                target_key, {}
            ).items():
                related[related_key]["explicit_finding_paths"].extend(
                    {
                        "direction": "outbound",
                        "finding": self.claim_graph.finding_card(finding),
                    }
                    for finding in findings
                )
            for source_key, targets in self.claim_graph.explicit_outbound.items():
                inbound_findings = targets.get(target_key, [])
                if inbound_findings:
                    related[source_key]["explicit_finding_paths"].extend(
                        {
                            "direction": "inbound",
                            "finding": self.claim_graph.finding_card(finding),
                        }
                        for finding in inbound_findings
                    )

        records = []
        for related_key, paths in related.items():
            for path_name in ("shared_claim_paths", "explicit_finding_paths"):
                paths[path_name].sort(
                    key=lambda row: str(
                        row.get("claim_id") or row["finding"]["doc_id"]
                    )
                )
            records.append(
                {
                    "target_gene": self.claim_graph.target_symbols.get(
                        related_key, related_key
                    ),
                    **paths,
                }
            )
        records.sort(
            key=lambda row: _stable_hash_key(
                f"related-targets:{target_key}:{basis}", str(row["target_gene"])
            )
        )
        limit = _limit(arguments, default=20)
        offset = _offset(arguments, "offset")
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.targets.related",
            "release_id": self.release.release_id,
            "target": target,
            "basis": basis,
            "ordering": "deterministic hash order; not biological rank",
            "related_targets": records[offset : offset + limit],
            "page": _page_metadata(
                offset,
                limit,
                len(records),
                len(records[offset : offset + limit]),
            ),
        }
        return _bound_list_fields(payload, ("related_targets",))

    def _call_compatibility_related_targets(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(
            arguments,
            {
                "target",
                "targets",
                "traversal",
                "basis",
                "direction",
                "path_detail",
                "restart_probability",
                "eligible_targets",
                "exclude_inputs",
                "limit",
                "offset",
            },
        )
        traversal = _enum(
            arguments,
            "traversal",
            ("direct", "random_walk"),
            default="random_walk" if "targets" in arguments else "direct",
        )
        if traversal == "random_walk":
            return self._call_compatibility_random_walk(arguments)
        if "targets" in arguments:
            raise CorpusToolError(
                "targets is available only when traversal is random_walk"
            )
        random_walk_only = sorted(
            field
            for field in (
                "restart_probability",
                "eligible_targets",
                "exclude_inputs",
            )
            if field in arguments
        )
        if random_walk_only:
            raise CorpusToolError(
                "direct traversal does not accept random-walk arguments: "
                + ", ".join(random_walk_only)
            )
        index = self.compatibility_claims
        target_key, target = index.canonical_target(
            _required_string(arguments, "target")
        )
        basis = _enum(
            arguments,
            "basis",
            (
                "both",
                "compatibility_claim",
                "shared_claim",
                "claim_relation",
                "explicit_finding_reference",
            ),
            default="both",
        )
        direction = _enum(
            arguments,
            "direction",
            ("both", "outbound", "inbound"),
            default="both",
        )
        path_detail = _enum(
            arguments, "path_detail", ("ids", "full"), default="ids"
        )
        related: defaultdict[str, dict[str, Any]] = defaultdict(
            lambda: {
                "shared_claim_paths": [],
                "claim_relation_paths": [],
                "explicit_finding_paths": [],
            }
        )

        if basis in {"both", "compatibility_claim", "shared_claim"}:
            for claim_id in sorted(
                index.claim_ids_by_target.get(target_key, set())
            ):
                related_keys = index.claim_target_keys(claim_id) - {target_key}
                for related_key in sorted(related_keys):
                    related[related_key]["shared_claim_paths"].append(
                        self._compatibility_shared_claim_path(
                            claim_id,
                            source_key=target_key,
                            related_key=related_key,
                            path_detail=path_detail,
                        )
                    )
        if basis in {"both", "compatibility_claim", "claim_relation"} and direction in {
            "both",
            "outbound",
        }:
            for related_key, relations in index.claim_relation_outbound.get(
                target_key, {}
            ).items():
                related[related_key]["claim_relation_paths"].extend(
                    self._compatibility_relation_path(
                        relation, direction="outbound", path_detail=path_detail
                    )
                    for relation in relations
                )
        if basis in {"both", "compatibility_claim", "claim_relation"} and direction in {
            "both",
            "inbound",
        }:
            for source_key, targets in index.claim_relation_outbound.items():
                inbound_relations = targets.get(target_key, [])
                if inbound_relations:
                    related[source_key]["claim_relation_paths"].extend(
                        self._compatibility_relation_path(
                            relation, direction="inbound", path_detail=path_detail
                        )
                        for relation in inbound_relations
                    )
        if basis in {"both", "explicit_finding_reference"} and direction in {
            "both",
            "outbound",
        }:
            for related_key, findings in index.explicit_outbound.get(
                target_key, {}
            ).items():
                related[related_key]["explicit_finding_paths"].extend(
                    self._compatibility_finding_path(
                        finding, direction="outbound", path_detail=path_detail
                    )
                    for finding in findings
                )
        if basis in {"both", "explicit_finding_reference"} and direction in {
            "both",
            "inbound",
        }:
            for source_key, targets in index.explicit_outbound.items():
                inbound_findings = targets.get(target_key, [])
                if inbound_findings:
                    related[source_key]["explicit_finding_paths"].extend(
                        self._compatibility_finding_path(
                            finding, direction="inbound", path_detail=path_detail
                        )
                        for finding in inbound_findings
                    )

        records = []
        for related_key, paths in related.items():
            paths["shared_claim_paths"].sort(
                key=lambda row: str(row["claim_id"])
            )
            paths["claim_relation_paths"].sort(
                key=lambda row: (
                    str(row["direction"]),
                    str(row["source_claim_id"]),
                    str(row["target_claim_id"]),
                    str(row["relation_type"]),
                )
            )
            paths["explicit_finding_paths"].sort(
                key=lambda row: (
                    str(row["direction"]),
                    str(
                        row.get("finding_doc_id")
                        or row.get("finding", {}).get("doc_id")
                    ),
                )
            )
            lanes = [
                lane
                for lane, field in (
                    ("shared_claim", "shared_claim_paths"),
                    ("claim_relation", "claim_relation_paths"),
                    ("explicit_finding_reference", "explicit_finding_paths"),
                )
                if paths[field]
            ]
            path_limit = 2 if path_detail == "full" else MAX_ROWS
            shared_claim_path_total = len(paths["shared_claim_paths"])
            claim_relation_path_total = len(paths["claim_relation_paths"])
            explicit_finding_path_total = len(paths["explicit_finding_paths"])
            records.append(
                {
                    "target_gene": index.target_symbols.get(
                        related_key, related_key
                    ),
                    "connection_lanes": lanes,
                    "shared_claim_paths": paths["shared_claim_paths"][
                        :path_limit
                    ],
                    "shared_claim_path_total": shared_claim_path_total,
                    "claim_relation_paths": paths["claim_relation_paths"][
                        :path_limit
                    ],
                    "claim_relation_path_total": claim_relation_path_total,
                    "explicit_finding_paths": paths["explicit_finding_paths"][
                        :path_limit
                    ],
                    "explicit_finding_path_total": explicit_finding_path_total,
                }
            )
        records.sort(
            key=lambda row: _stable_hash_key(
                f"compatibility-related:{target_key}:{basis}:{direction}",
                str(row["target_gene"]),
            )
        )
        limit = _limit(arguments, default=20)
        offset = _offset(arguments, "offset")
        emitted = records[offset : offset + limit]
        return _bound_list_fields(
            {
                "schema_version": "distributed_agents-corpus-mcp-v1",
                "operation": "corpus.compatibility_targets.related",
                "release_id": self.release.release_id,
                "target": target,
                "target_found": target_key in index.target_symbols,
                "traversal": "direct",
                "basis": basis,
                "direction": direction,
                "path_detail": path_detail,
                "lane_semantics": {
                    "shared_claim": (
                        "undirected co-membership in one Shi Claim"
                    ),
                    "claim_relation": (
                        "directed typed relation between Shi Claims"
                    ),
                    "explicit_finding_reference": (
                        "directional comparator mention asserted by a source Finding"
                    ),
                },
                "ordering": "deterministic hash order; not biological rank",
                "related_targets": emitted,
                "page": _page_metadata(
                    offset, limit, len(records), len(emitted)
                ),
            },
            ("related_targets",),
        )

    def _call_compatibility_random_walk(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        if "path_detail" in arguments:
            raise CorpusToolError(
                "path_detail is available only when traversal is direct"
            )
        has_target = "target" in arguments
        has_targets = "targets" in arguments
        if has_target == has_targets:
            raise CorpusToolError(
                "random_walk requires exactly one of target or targets"
            )
        supplied = (
            [_required_string(arguments, "target")]
            if has_target
            else _string_list(
                arguments, "targets", required=True, max_items=20
            )
        )
        if len(supplied) > 20:
            raise CorpusToolError("targets must contain at most 20 values")

        index = self.compatibility_claims
        canonical: list[tuple[str, str]] = []
        seen_keys: set[str] = set()
        for value in supplied:
            key, symbol = index.canonical_target(value)
            if key in seen_keys:
                raise CorpusToolError(
                    "source targets must be distinct after case-insensitive normalization"
                )
            seen_keys.add(key)
            canonical.append((key, symbol))
        canonical.sort(key=lambda item: item[0])
        source_keys = [key for key, _ in canonical]
        source_symbols = {key: symbol for key, symbol in canonical}
        effective_keys = [
            key for key in source_keys if key in index.target_symbols
        ]
        if not effective_keys:
            raise CorpusToolError(
                "none of the random-walk source targets occur in the selected release"
            )

        basis = _enum(
            arguments,
            "basis",
            (
                "both",
                "compatibility_claim",
                "shared_claim",
                "claim_relation",
                "explicit_finding_reference",
            ),
            default="both",
        )
        direction = _enum(
            arguments,
            "direction",
            ("both", "outbound", "inbound"),
            default="both",
        )
        restart_probability = _number(
            arguments,
            "restart_probability",
            minimum=0.0,
            maximum=1.0,
            default=0.15,
            exclusive=True,
        )
        exclude_inputs = _boolean(arguments, "exclude_inputs", default=True)
        eligibility_supplied = "eligible_targets" in arguments
        eligible_values = _string_list(
            arguments, "eligible_targets", max_items=5_000
        )
        eligible_keys = {_gene_key(value) for value in eligible_values}
        if len(eligible_keys) != len(eligible_values):
            raise CorpusToolError(
                "eligible_targets must be distinct after case-insensitive normalization"
            )

        adjacency, lane_edge_counts = self._compatibility_target_projection(
            basis=basis,
            direction=direction,
        )
        try:
            walk = random_walk_with_restart(
                adjacency,
                effective_keys,
                restart_probability=restart_probability,
            )
        except (RuntimeError, ValueError) as exc:
            raise CorpusToolError(str(exc)) from exc

        source_set = set(source_keys)
        candidates: list[dict[str, Any]] = []
        for node, score, in_degree, out_degree, components in zip(
            walk.nodes,
            walk.scores,
            walk.in_degrees,
            walk.out_degrees,
            walk.seed_components,
        ):
            if score <= 0.0:
                continue
            if exclude_inputs and node in source_set:
                continue
            if eligibility_supplied and node not in eligible_keys:
                continue
            attribution_order = sorted(
                range(len(effective_keys)),
                key=lambda column: (
                    -components[column],
                    effective_keys[column],
                ),
            )
            attributions = []
            reported_fraction = 0.0
            for column in attribution_order[:3]:
                contribution = components[column]
                if contribution <= 0.0:
                    continue
                fraction = contribution / score
                reported_fraction += fraction
                source_key = effective_keys[column]
                attributions.append(
                    {
                        "source_target": index.target_symbols[source_key],
                        "contribution": contribution,
                        "fraction": fraction,
                    }
                )
            candidates.append(
                {
                    "target_gene": index.target_symbols.get(node, node),
                    "reachability_score": score,
                    "in_degree": in_degree,
                    "out_degree": out_degree,
                    "seed_attributions": attributions,
                    "unreported_attribution_fraction": min(
                        1.0, max(0.0, 1.0 - reported_fraction)
                    ),
                }
            )
        candidates.sort(
            key=lambda row: (
                -float(row["reachability_score"]),
                str(row["target_gene"]).casefold(),
                str(row["target_gene"]),
            )
        )
        for rank, row in enumerate(candidates, 1):
            row["reachability_order"] = rank

        limit = _limit(arguments, default=20)
        offset = _offset(arguments, "offset")
        emitted = candidates[offset : offset + limit]
        return _bound_list_fields(
            {
                "schema_version": "distributed_agents-corpus-mcp-v1",
                "operation": "corpus.compatibility_targets.related",
                "release_id": self.release.release_id,
                "targets": [source_symbols[key] for key in source_keys],
                "traversal": "random_walk",
                "basis": basis,
                "direction": direction,
                "coverage": {
                    "supplied": len(source_keys),
                    "found": len(effective_keys),
                    "effective_targets": [
                        index.target_symbols[key] for key in effective_keys
                    ],
                    "missing_targets": [
                        source_symbols[key]
                        for key in source_keys
                        if key not in index.target_symbols
                    ],
                },
                "projection": {
                    "node_type": "TargetGene",
                    "edge_model": "binary",
                    "node_count": len(walk.nodes),
                    "directed_edge_count": walk.directed_edge_count,
                    "lane_directed_edge_counts": lane_edge_counts,
                    "eligibility_filter_affects_propagation": False,
                },
                "walk": {
                    "algorithm": "random_walk_with_restart",
                    "source_weighting": "equal_across_found_targets",
                    "restart_probability": restart_probability,
                    "convergence_tolerance": 1e-10,
                    "maximum_iterations": 200,
                    "iterations": walk.iterations,
                    "l1_residual": walk.l1_residual,
                    "maximum_source_l1_residual": walk.max_seed_l1_residual,
                    "probability_mass": walk.probability_mass,
                },
                "selection": {
                    "exclude_inputs": exclude_inputs,
                    "eligibility_filter_supplied": eligibility_supplied,
                    "eligible_target_count": (
                        len(eligible_keys) if eligibility_supplied else None
                    ),
                    "reachable_candidate_count": len(candidates),
                },
                "ordering": (
                    "descending stationary random-walk probability, then target "
                    "symbol; graph reachability order is not biological rank"
                ),
                "related_targets": emitted,
                "page": _page_metadata(
                    offset, limit, len(candidates), len(emitted)
                ),
                "interpretation": (
                    "reachability_score is stationary probability on the declared "
                    "binary target projection. It describes recurrence and access "
                    "from the supplied targets, not effect size, confidence, causal "
                    "importance, or biological priority."
                ),
            },
            ("related_targets",),
        )

    def _compatibility_target_projection(
        self,
        *,
        basis: str,
        direction: str,
    ) -> tuple[dict[str, frozenset[str]], dict[str, int]]:
        cache_key = (basis, direction)
        cached = self._compatibility_projection_cache.get(cache_key)
        if cached is not None:
            return cached

        index = self.compatibility_claims
        adjacency: dict[str, set[str]] = {
            key: set() for key in index.target_symbols
        }
        lane_edges: dict[str, set[tuple[str, str]]] = {
            "shared_claim": set(),
            "claim_relation": set(),
            "explicit_finding_reference": set(),
        }

        def add_edge(lane: str, source: str, target: str) -> None:
            if source == target:
                return
            adjacency.setdefault(source, set()).add(target)
            adjacency.setdefault(target, set())
            lane_edges[lane].add((source, target))

        if basis in {"both", "compatibility_claim", "shared_claim"}:
            for claim_id in sorted(index.claims_by_id):
                claim_targets = sorted(index.claim_target_keys(claim_id))
                for left_offset, left in enumerate(claim_targets):
                    for right in claim_targets[left_offset + 1 :]:
                        add_edge("shared_claim", left, right)
                        add_edge("shared_claim", right, left)

        def add_directional_edges(
            lane: str,
            outbound: Mapping[str, Mapping[str, Sequence[Mapping[str, Any]]]],
        ) -> None:
            for source, targets in outbound.items():
                for target in targets:
                    if direction in {"both", "outbound"}:
                        add_edge(lane, source, target)
                    if direction in {"both", "inbound"}:
                        add_edge(lane, target, source)

        if basis in {"both", "compatibility_claim", "claim_relation"}:
            add_directional_edges(
                "claim_relation", index.claim_relation_outbound
            )
        if basis in {"both", "explicit_finding_reference"}:
            add_directional_edges(
                "explicit_finding_reference", index.explicit_outbound
            )

        frozen_adjacency = {
            node: frozenset(targets) for node, targets in adjacency.items()
        }
        counts = {
            lane: len(edges)
            for lane, edges in lane_edges.items()
            if edges
        }
        result = (frozen_adjacency, counts)
        self._compatibility_projection_cache[cache_key] = result
        return result

    def _compatibility_pair_paths(
        self,
        left_key: str,
        right_key: str,
        *,
        basis: str,
        path_detail: str,
    ) -> dict[str, Any]:
        index = self.compatibility_claims
        left_to_right_relations = list(
            index.claim_relation_outbound.get(left_key, {}).get(right_key, [])
        )
        right_to_left_relations = list(
            index.claim_relation_outbound.get(right_key, {}).get(left_key, [])
        )
        left_to_right_findings = list(
            index.explicit_outbound.get(left_key, {}).get(right_key, [])
        )
        right_to_left_findings = list(
            index.explicit_outbound.get(right_key, {}).get(left_key, [])
        )
        shared_claim_ids = sorted(
            index.claim_ids_by_target.get(left_key, set()).intersection(
                index.claim_ids_by_target.get(right_key, set())
            )
        )
        shared_claim_paths = []
        relation_paths = []
        finding_paths = []
        if basis in {"both", "compatibility_claim", "shared_claim"}:
            shared_claim_paths.extend(
                self._compatibility_shared_claim_path(
                    claim_id,
                    source_key=left_key,
                    related_key=right_key,
                    path_detail=path_detail,
                )
                for claim_id in shared_claim_ids
            )
        if basis in {"both", "compatibility_claim", "claim_relation"}:
            relation_paths.extend(
                self._compatibility_relation_path(
                    row, direction="left_to_right", path_detail=path_detail
                )
                for row in left_to_right_relations
            )
            relation_paths.extend(
                self._compatibility_relation_path(
                    row, direction="right_to_left", path_detail=path_detail
                )
                for row in right_to_left_relations
            )
        if basis in {"both", "explicit_finding_reference"}:
            finding_paths.extend(
                self._compatibility_finding_path(
                    row, direction="left_to_right", path_detail=path_detail
                )
                for row in left_to_right_findings
            )
            finding_paths.extend(
                self._compatibility_finding_path(
                    row, direction="right_to_left", path_detail=path_detail
                )
                for row in right_to_left_findings
            )
        relation_paths.sort(
            key=lambda row: (
                str(row["direction"]),
                str(row["source_claim_id"]),
                str(row["target_claim_id"]),
                str(row["relation_type"]),
            )
        )
        finding_paths.sort(
            key=lambda row: (
                str(row["direction"]),
                str(
                    row.get("finding_doc_id")
                    or row.get("finding", {}).get("doc_id")
                ),
            )
        )
        lanes = []
        if shared_claim_paths:
            lanes.append("shared_claim")
        if relation_paths:
            lanes.append("claim_relation")
        if finding_paths:
            lanes.append("explicit_finding_reference")
        path_limit = 1 if path_detail == "full" else MAX_ROWS
        return {
            "connection_lanes": lanes,
            "shared_claim_paths": shared_claim_paths[:path_limit],
            "shared_claim_path_total": len(shared_claim_paths),
            "claim_relation_paths": relation_paths[:path_limit],
            "claim_relation_path_total": len(relation_paths),
            "explicit_finding_paths": finding_paths[:path_limit],
            "explicit_finding_path_total": len(finding_paths),
            "left_to_right": bool(
                (
                    basis in {"both", "compatibility_claim", "claim_relation"}
                    and left_to_right_relations
                )
                or (
                    basis in {"both", "explicit_finding_reference"}
                    and left_to_right_findings
                )
            ),
            "right_to_left": bool(
                (
                    basis in {"both", "compatibility_claim", "claim_relation"}
                    and right_to_left_relations
                )
                or (
                    basis in {"both", "explicit_finding_reference"}
                    and right_to_left_findings
                )
            ),
        }

    @staticmethod
    def _components(adjacency: Mapping[str, set[str]]) -> list[list[str]]:
        remaining = set(adjacency)
        components: list[list[str]] = []
        while remaining:
            start = min(remaining)
            stack = [start]
            component: set[str] = set()
            while stack:
                node = stack.pop()
                if node in component:
                    continue
                component.add(node)
                stack.extend(adjacency[node] - component)
            remaining -= component
            components.append(sorted(component))
        components.sort(key=lambda values: (-len(values), values))
        return components

    @staticmethod
    def _maximal_cliques(adjacency: Mapping[str, set[str]]) -> list[list[str]]:
        cliques: list[list[str]] = []

        def visit(current: set[str], candidates: set[str], excluded: set[str]) -> None:
            if not candidates and not excluded:
                if len(current) >= 2:
                    cliques.append(sorted(current))
                return
            pivot_pool = candidates | excluded
            pivot = (
                max(
                    pivot_pool,
                    key=lambda node: (len(candidates & adjacency[node]), node),
                )
                if pivot_pool
                else None
            )
            pivot_neighbors = adjacency[pivot] if pivot is not None else set()
            for node in sorted(candidates - pivot_neighbors):
                visit(
                    current | {node},
                    candidates & adjacency[node],
                    excluded & adjacency[node],
                )
                candidates.remove(node)
                excluded.add(node)

        visit(set(), set(adjacency), set())
        cliques.sort(key=lambda values: (-len(values), values))
        return cliques

    def call_inspect_target_set(
        self, arguments: Mapping[str, Any]
    ) -> dict[str, Any]:
        self.policy.require(FINDINGS_CAPABILITY)
        _check_keys(
            arguments,
            {
                "targets",
                "basis",
                "path_detail",
                "minimum_sources",
                "eligible_targets",
                "exclude_inputs",
                "connection_limit",
                "connection_offset",
                "neighbor_limit",
                "neighbor_offset",
            },
        )
        supplied = _string_list(arguments, "targets", required=True)
        if not 2 <= len(supplied) <= 20:
            raise CorpusToolError("targets must contain between 2 and 20 values")
        index = self.compatibility_claims
        canonical: list[tuple[str, str]] = []
        seen_keys: set[str] = set()
        for value in supplied:
            key, symbol = index.canonical_target(value)
            if key in seen_keys:
                raise CorpusToolError(
                    "targets must be distinct after case-insensitive normalization"
                )
            seen_keys.add(key)
            canonical.append((key, symbol))
        canonical.sort(key=lambda item: item[0])
        keys = [key for key, _ in canonical]
        symbols = {key: symbol for key, symbol in canonical}
        basis = _enum(
            arguments,
            "basis",
            (
                "both",
                "compatibility_claim",
                "shared_claim",
                "claim_relation",
                "explicit_finding_reference",
            ),
            default="both",
        )
        path_detail = _enum(
            arguments, "path_detail", ("ids", "full"), default="ids"
        )
        minimum_sources = _integer(
            arguments,
            "minimum_sources",
            minimum=2,
            maximum=len(keys),
            default=2,
        )
        exclude_inputs = _boolean(arguments, "exclude_inputs", default=True)
        eligibility_supplied = "eligible_targets" in arguments
        eligible_values = _string_list(
            arguments, "eligible_targets", max_items=5_000
        )
        eligible_keys = {_gene_key(value) for value in eligible_values}
        if len(eligible_keys) != len(eligible_values):
            raise CorpusToolError(
                "eligible_targets must be distinct after case-insensitive normalization"
            )

        adjacency = {key: set() for key in keys}
        outbound = {key: set() for key in keys}
        inbound = {key: set() for key in keys}
        shared_claim_neighbors = {key: set() for key in keys}
        claim_neighbors = {key: set() for key in keys}
        finding_neighbors = {key: set() for key in keys}
        connections: list[dict[str, Any]] = []
        for left_index, left_key in enumerate(keys):
            for right_key in keys[left_index + 1 :]:
                paths = self._compatibility_pair_paths(
                    left_key,
                    right_key,
                    basis=basis,
                    path_detail=path_detail,
                )
                if not paths["connection_lanes"]:
                    continue
                adjacency[left_key].add(right_key)
                adjacency[right_key].add(left_key)
                if paths["left_to_right"]:
                    outbound[left_key].add(right_key)
                    inbound[right_key].add(left_key)
                if paths["right_to_left"]:
                    outbound[right_key].add(left_key)
                    inbound[left_key].add(right_key)
                if "shared_claim" in paths["connection_lanes"]:
                    shared_claim_neighbors[left_key].add(right_key)
                    shared_claim_neighbors[right_key].add(left_key)
                if "claim_relation" in paths["connection_lanes"]:
                    claim_neighbors[left_key].add(right_key)
                    claim_neighbors[right_key].add(left_key)
                if "explicit_finding_reference" in paths["connection_lanes"]:
                    finding_neighbors[left_key].add(right_key)
                    finding_neighbors[right_key].add(left_key)
                connections.append(
                    {
                        "left_target": symbols[left_key],
                        "right_target": symbols[right_key],
                        **paths,
                    }
                )
        connections.sort(
            key=lambda row: (
                str(row["left_target"]).casefold(),
                str(row["right_target"]).casefold(),
            )
        )

        components = self._components(adjacency)
        cliques = self._maximal_cliques(adjacency)
        pair_total = len(keys) * (len(keys) - 1) // 2
        node_records = [
            {
                "target_gene": symbols[key],
                "found": key in index.target_symbols,
                "degree": len(adjacency[key]),
                "outbound_degree": len(outbound[key]),
                "inbound_degree": len(inbound[key]),
                "shared_claim_degree": len(shared_claim_neighbors[key]),
                "claim_relation_degree": len(claim_neighbors[key]),
                "explicit_finding_reference_degree": len(finding_neighbors[key]),
            }
            for key in keys
        ]

        external: defaultdict[str, dict[str, defaultdict[str, list[dict[str, Any]]]]] = (
            defaultdict(
                lambda: {
                    "shared_claim_paths_by_source": defaultdict(list),
                    "claim_relation_paths_by_source": defaultdict(list),
                    "explicit_finding_paths_by_source": defaultdict(list),
                }
            )
        )
        input_keys = set(keys)
        for source_key in keys:
            if basis in {"both", "compatibility_claim", "shared_claim"}:
                for claim_id in sorted(
                    index.claim_ids_by_target.get(source_key, set())
                ):
                    for neighbor_key in sorted(
                        index.claim_target_keys(claim_id) - {source_key}
                    ):
                        external[neighbor_key]["shared_claim_paths_by_source"][
                            source_key
                        ].append(
                            self._compatibility_shared_claim_path(
                                claim_id,
                                source_key=source_key,
                                related_key=neighbor_key,
                                path_detail=path_detail,
                            )
                        )
            if basis in {"both", "compatibility_claim", "claim_relation"}:
                for neighbor_key, relations in index.claim_relation_outbound.get(
                    source_key, {}
                ).items():
                    external[neighbor_key]["claim_relation_paths_by_source"][
                        source_key
                    ].extend(
                        self._compatibility_relation_path(
                            relation,
                            direction="outbound",
                            path_detail=path_detail,
                        )
                        for relation in relations
                    )
                for relation_source, targets in index.claim_relation_outbound.items():
                    inbound_relations = targets.get(source_key, [])
                    if inbound_relations:
                        external[relation_source][
                            "claim_relation_paths_by_source"
                        ][source_key].extend(
                            self._compatibility_relation_path(
                                relation,
                                direction="inbound",
                                path_detail=path_detail,
                            )
                            for relation in inbound_relations
                        )
            if basis in {"both", "explicit_finding_reference"}:
                for neighbor_key, findings in index.explicit_outbound.get(
                    source_key, {}
                ).items():
                    external[neighbor_key]["explicit_finding_paths_by_source"][
                        source_key
                    ].extend(
                        self._compatibility_finding_path(
                            finding,
                            direction="outbound",
                            path_detail=path_detail,
                        )
                        for finding in findings
                    )

        neighbor_records = []
        for neighbor_key, lanes in external.items():
            if exclude_inputs and neighbor_key in input_keys:
                continue
            if eligibility_supplied and neighbor_key not in eligible_keys:
                continue
            connected_sources = sorted(
                set(lanes["shared_claim_paths_by_source"])
                | set(lanes["claim_relation_paths_by_source"])
                | set(lanes["explicit_finding_paths_by_source"])
            )
            if len(connected_sources) < minimum_sources:
                continue
            source_connections = []
            for source_key in connected_sources:
                shared_paths = lanes["shared_claim_paths_by_source"].get(
                    source_key, []
                )
                relation_paths = lanes["claim_relation_paths_by_source"].get(
                    source_key, []
                )
                finding_paths = lanes["explicit_finding_paths_by_source"].get(
                    source_key, []
                )
                shared_paths.sort(key=lambda row: str(row["claim_id"]))
                relation_paths.sort(
                    key=lambda row: (
                        str(row["direction"]),
                        str(row["source_claim_id"]),
                        str(row["target_claim_id"]),
                        str(row["relation_type"]),
                    )
                )
                finding_paths.sort(
                    key=lambda row: (
                        str(row["direction"]),
                        str(
                            row.get("finding_doc_id")
                            or row.get("finding", {}).get("doc_id")
                        ),
                    )
                )
                source_connections.append(
                    {
                        "source_target": symbols[source_key],
                        "connection_lanes": [
                            lane
                            for lane, paths in (
                                ("shared_claim", shared_paths),
                                ("claim_relation", relation_paths),
                                ("explicit_finding_reference", finding_paths),
                            )
                            if paths
                        ],
                        "shared_claim_paths": shared_paths[
                            : 1 if path_detail == "full" else MAX_ROWS
                        ],
                        "shared_claim_path_total": len(shared_paths),
                        "claim_relation_paths": relation_paths[
                            : 1 if path_detail == "full" else MAX_ROWS
                        ],
                        "claim_relation_path_total": len(relation_paths),
                        "explicit_finding_paths": finding_paths[
                            : 1 if path_detail == "full" else MAX_ROWS
                        ],
                        "explicit_finding_path_total": len(finding_paths),
                    }
                )
            neighbor_records.append(
                {
                    "target_gene": index.target_symbols.get(
                        neighbor_key, neighbor_key
                    ),
                    "connected_source_count": len(connected_sources),
                    "connected_sources": [
                        symbols[source_key] for source_key in connected_sources
                    ],
                    "source_connections": source_connections[
                        : 2 if path_detail == "full" else MAX_ROWS
                    ],
                    "source_connections_complete": (
                        path_detail != "full" or len(source_connections) <= 2
                    ),
                }
            )
        neighbor_records.sort(
            key=lambda row: (
                -int(row["connected_source_count"]),
                _stable_hash_key(
                    "compatibility-target-set:" + "|".join(keys),
                    str(row["target_gene"]),
                ),
            )
        )

        connection_limit = _limit_named(
            arguments, "connection_limit", default=20
        )
        connection_offset = _offset(arguments, "connection_offset")
        neighbor_limit = _limit_named(arguments, "neighbor_limit", default=20)
        neighbor_offset = _offset(arguments, "neighbor_offset")
        emitted_connections = connections[
            connection_offset : connection_offset + connection_limit
        ]
        emitted_neighbors = neighbor_records[
            neighbor_offset : neighbor_offset + neighbor_limit
        ]

        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.compatibility_targets.inspect_set",
            "release_id": self.release.release_id,
            "targets": [symbols[key] for key in keys],
            "basis": basis,
            "path_detail": path_detail,
            "coverage": {
                "supplied": len(keys),
                "found": sum(key in index.target_symbols for key in keys),
                "missing_targets": [
                    symbols[key] for key in keys if key not in index.target_symbols
                ],
            },
            "topology": {
                "node_count": len(keys),
                "connected_pair_count": len(connections),
                "possible_pair_count": pair_total,
                "connected_pair_fraction": (
                    len(connections) / pair_total if pair_total else 0.0
                ),
                "mean_internal_degree": (
                    sum(len(adjacency[key]) for key in keys) / len(keys)
                ),
                "nodes": node_records,
                "components": [
                    [symbols[key] for key in component]
                    for component in components
                ],
                "isolates": [
                    symbols[key] for key in keys if not adjacency[key]
                ],
                "maximal_connected_cliques": [
                    [symbols[key] for key in clique] for clique in cliques
                ],
            },
            "connections": emitted_connections,
            "connections_page": _page_metadata(
                connection_offset,
                connection_limit,
                len(connections),
                len(emitted_connections),
            ),
            "external_neighbors": emitted_neighbors,
            "external_neighbors_page": _page_metadata(
                neighbor_offset,
                neighbor_limit,
                len(neighbor_records),
                len(emitted_neighbors),
            ),
            "expansion": {
                "minimum_sources": minimum_sources,
                "exclude_inputs": exclude_inputs,
                "eligibility_filter_supplied": eligibility_supplied,
                "eligible_target_count": (
                    len(eligible_keys) if eligibility_supplied else None
                ),
                "candidate_count": len(neighbor_records),
            },
            "lane_semantics": {
                "shared_claim": (
                    "undirected co-membership in one Shi Claim"
                ),
                "claim_relation": (
                    "directed typed relation between Shi Claims"
                ),
                "explicit_finding_reference": (
                    "outbound comparator mention asserted by an input target's Finding"
                ),
            },
            "interpretation": (
                "topology, recurrence, and eligibility are observations over the "
                "declared set; they are not biological rank, selection, or weights"
            ),
        }
        return _bound_list_fields(
            payload, ("connections", "external_neighbors")
        )

    def call_read_cypher(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.policy.require(GRAPH_CAPABILITY)
        _check_keys(arguments, {"query", "parameters"})
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 10_000:
            raise CorpusToolError("query must be a non-empty string of at most 10,000 characters")
        parameters = arguments.get("parameters", {})
        if not isinstance(parameters, Mapping) or len(parameters) > 50:
            raise CorpusToolError("parameters must be an object with at most 50 entries")
        argv = ["--format", "json", "--query", query.strip()]
        for name, value in parameters.items():
            if not isinstance(name, str) or not SAFE_FIELD.fullmatch(name):
                raise CorpusToolError("parameter names must be simple field names")
            argv.extend(["--param", f"{name}={json.dumps(value, ensure_ascii=False)}"])
        completed = self._run(self.release.entrypoint("graph", "query"), argv)
        records = _parse_json_array(completed.stdout, "read_cypher")
        payload = {
            "schema_version": "distributed_agents-corpus-mcp-v1",
            "operation": "corpus.graph.read_cypher",
            "release_id": self.release.release_id,
            "records": records,
            "truncation": {
                "truncated": False,
                "exact_total": len(records),
                "emitted": len(records),
                "max_rows": MAX_ROWS,
                "max_output_bytes": MAX_OUTPUT_BYTES,
            },
        }
        return _bound_records(payload)

    @staticmethod
    def _run(entrypoint: Path, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        try:
            completed = subprocess.run(
                [sys.executable, str(entrypoint), *argv],
                cwd=entrypoint.parent,
                env=os.environ.copy(),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=TOOL_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CorpusToolError(f"release adapter failed to run: {exc}") from exc
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()[-2_000:]
            raise CorpusToolError(
                f"release adapter exited with status {completed.returncode}: {detail}"
            )
        return completed
