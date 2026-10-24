#!/usr/bin/env python3
"""Build a finding-centered BioKG MVP v2 from report and finding JSONLs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from ..paths import GRAPH_WORK_DIR, REPORTS_FILE


DEFAULT_REPORTS = REPORTS_FILE
DEFAULT_OUT = GRAPH_WORK_DIR
DEFAULT_TARGETS = (
    "Arx",
    "Agps",
    "Clec16a",
    "Abhd12",
    "Pomp",
    "Psmb4",
    "Psmc1",
    "Psmc5",
    "Tsc1",
    "Setd1a",
    "Smarca4",
)

APPENDIX_HEADINGS = {
    "evidence": "Evidence JSONL",
    "references": "References JSONL",
    "biological_findings": "Biological Findings JSONL",
    "literature_comparisons": "Literature Comparisons JSONL",
    "pathways": "Pathways JSONL",
    "cell_type_specificity": "Cell Type Specificity JSONL",
}

LLM_ENTITY_KINDS = {
    "gene": "Gene",
    "genes": "Gene",
    "module": "Module",
    "modules": "Module",
    "pathway": "Pathway",
    "pathways": "Pathway",
    "complex": "Complex",
    "complexes": "Complex",
    "phenotype": "Phenotype",
    "phenotypes": "Phenotype",
    "biological_process": "Pathway",
    "biological process": "Pathway",
    "process": "Pathway",
    "processes": "Pathway",
    "other": "Other",
    "disease": "Other",
    "drug": "Other",
    "compound": "Other",
    "chemical": "Other",
    "lipid": "Other",
    "metabolite": "Other",
    "ion_channel": "Other",
    "ion channel": "Other",
    "channel": "Other",
    "current": "Other",
}
DROP_OTHER_TYPES = {
    "cell",
    "cell_type",
    "cell type",
    "celltype",
    "class",
    "measurement",
    "setting",
}
GENERIC_GENE_NAMES = {
    "de gene",
    "de genes",
    "deg",
    "degs",
    "differentially expressed gene",
    "differentially expressed genes",
    "non-target gene",
    "non-target genes",
    "transcript",
    "transcripts",
}
NON_BIOLOGICAL_CONCEPT_NAMES = {
    "broader signatures",
    "functional perturbation assay",
    "proteasome-related interpretation",
    "transcriptome-wide correlations",
    "transcriptome wide correlations",
}
NON_BIOLOGICAL_CONCEPT_TERMS = {
    "correlation",
    "correlations",
    "assay",
    "interpretation",
}

# --- Change #2: re-route Other subtypes ---
# Gene-product other_types that should become Gene nodes rather than Other.
GENE_PRODUCT_OTHER_TOKENS = {
    "protein", "receptor", "enzyme", "kinase", "protein kinase", "protein_kinase",
    "transcription_factor", "transcription factor", "transcription-factor", "transcription factors",
    "gpcr", "chromatin_regulator", "chromatin regulator", "chromatin_remodeler", "chromatin remodeler",
    "gtpase", "deubiquitinase", "ubiquitin_ligase", "helicase", "motor protein", "motor_protein",
}
# Non-biological / noise other_types that should not become graph nodes at all.
NOISE_OTHER_TOKENS = {
    "statistic", "statistics", "statistical", "statistical measure", "statistical_measure",
    "statistical method", "statistical_method", "statistical test", "statistical_test",
    "statistical metric", "statistical_metric", "statistical threshold", "statistical_threshold",
    "statistical significance", "statistical_significance", "statistical concept", "statistical_concept",
    "metric", "measure", "threshold", "count", "cell_count", "cell count", "efficiency",
    "experiment", "experimental", "experimental condition", "experimental_condition",
    "experimental method", "experimental_method", "experimental technique", "experimental_technique",
    "method", "methodology", "assay", "dataset", "study", "screen", "technique", "technology",
    "concept", "biological concept", "biological_concept", "hypothesis", "biological_hypothesis",
    "note", "definition", "interpretation", "observation", "result", "readout", "warning",
}
# Biologically valid Other types that take precedence over gene/noise routing.
VALID_OTHER_TOKENS = {
    "disease", "disorder", "drug", "compound", "drug/compound", "chemical", "lipid",
    "metabolite", "ion_channel", "ion channel", "channel", "current", "hormone", "cytokine",
    "neurotransmitter", "neuropeptide", "ligand", "electrophysiology", "virus", "antibody",
}


def classify_other_type(other_type: str) -> str:
    """Re-route an Other entity by its other_type: 'Gene', 'DROP', or '' (keep as Other)."""
    tokens = [t.strip().casefold() for t in str(other_type or "").split("|") if t.strip()]
    if not tokens:
        return ""
    if any(t in VALID_OTHER_TOKENS for t in tokens):
        return ""
    if all(t in NOISE_OTHER_TOKENS for t in tokens):
        return "DROP"
    if any(t in GENE_PRODUCT_OTHER_TOKENS for t in tokens):
        return "Gene"
    if any(t in NOISE_OTHER_TOKENS for t in tokens):
        return "DROP"
    return ""


# --- Change #3: block seed cell-type and finding_type label leakage ---
FINDING_TYPE_VALUES = {
    "negative_result", "cross_perturbation_contrast", "cell_type_selectivity",
    "buffered_response", "pathway_uncoupling", "therapeutic_direction_warning",
    "disease_mechanism_refinement", "biomarker_candidate",
}


def is_leaked_seed_label(name: str, cell_vocab: set[str]) -> bool:
    """True if a non-seed entity name is actually a seed cell type or a finding_type label."""
    nf = name.casefold()
    if nf in cell_vocab:
        return True
    if nf.replace(" ", "_") in FINDING_TYPE_VALUES:
        return True
    toks = name.split()
    # Numeric-prefixed cell-type-style label, e.g. "151 TH Prkcd Grin2c Glut".
    if len(toks) >= 2 and toks[0].isdigit() and len(toks[0]) <= 3:
        return True
    return False

NODE_FIELDS = [
    "id",
    "kind",
    "labels",
    "name",
    "symbol",
    "target_gene",
    "doc_id",
    "finding_id",
    "evidence_id",
    "ref_id",
    "comparison_id",
    "finding_type",
    "direction",
    "confidence",
    "literature_status",
    "cell_type",
    "other_type",
    "summary",
    "why_it_matters",
    "description",
    "statistics",
    "citation",
    "url",
    "source",
    "source_type",
    "text",
    "main_caveats",
    "evidence_ids",
    "ref_ids",
    "genes",
    "comparators",
    "evidence_slug",
    "extractor",
    "status",
]
REL_FIELDS = [
    "start_id",
    "end_id",
    "type",
    "confidence",
    "role",
    "direction",
    "effect_status",
    "logfc",
    "pval",
    "fdr",
    "evidence",
]


@dataclass
class Node:
    id: str
    kind: str
    name: str
    labels: tuple[str, ...]
    props: dict[str, str] = field(default_factory=dict)


@dataclass
class Rel:
    start_id: str
    end_id: str
    rel_type: str
    props: dict[str, str] = field(default_factory=dict)


def slugify(value: str, *, max_len: int = 96) -> str:
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        value = "blank"
    if len(value) > max_len:
        digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
        value = f"{value[: max_len - 11].rstrip('_')}_{digest}"
    return value


def stable_id(kind: str, value: str) -> str:
    return f"{kind.lower()}:{slugify(value)}"


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_gene_symbol(value: object) -> str:
    symbol = normalize_text(value)
    if not symbol:
        return ""
    return symbol[:1].upper() + symbol[1:]


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [normalize_text(item) for item in value if normalize_text(item)]
    if isinstance(value, tuple):
        return [normalize_text(item) for item in value if normalize_text(item)]
    clean = normalize_text(value)
    return [clean] if clean else []


def as_cell_type_list(value: object) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in as_list(value):
        for part in item.split(";"):
            clean = normalize_text(part)
            if not clean:
                continue
            key = clean.casefold()
            if key in seen:
                continue
            seen.add(key)
            out.append(clean)
    return out


def pipe_join(values: Iterable[object]) -> str:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = normalize_text(value)
        if not clean:
            continue
        key = clean.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(clean)
    return "|".join(out)


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def parse_jsonl_block(text: str, heading: str) -> tuple[list[dict], list[str]]:
    pattern = rf"^##+\s+{re.escape(heading)}\s*\n\s*```jsonl\s*\n(.*?)\n```"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return [], [f"missing block: {heading}"]

    rows: list[dict] = []
    errors: list[str] = []
    for line_number, line in enumerate(match.group(1).splitlines(), start=1):
        clean = line.strip()
        if not clean:
            continue
        try:
            rows.append(json.loads(clean))
        except json.JSONDecodeError as exc:
            errors.append(f"{heading} line {line_number}: {exc}")
    return rows, errors


def parse_report_appendices(report: dict) -> dict:
    target = normalize_gene_symbol(report.get("gene_target"))
    text = str(report.get("final_report") or "")
    parsed = {
        "target_gene": target,
        "sections": {},
        "parse_errors": [],
        "has_report": bool(text),
    }
    for key, heading in APPENDIX_HEADINGS.items():
        rows, errors = parse_jsonl_block(text, heading)
        for row in rows:
            row["_target_gene"] = target
            row["_section"] = key
        parsed["sections"][key] = rows
        parsed["parse_errors"].extend(errors)
    return parsed


def collect_gene_and_cell_vocab(finding_rows: Sequence[dict], parsed_reports: dict[str, dict]) -> tuple[dict[str, str], set[str]]:
    genes: dict[str, str] = {}
    cell_types: set[str] = set()

    def add_gene(value: object) -> None:
        gene = normalize_gene_symbol(value)
        if gene:
            genes.setdefault(gene.casefold(), gene)

    for row in finding_rows:
        add_gene(row.get("gene_target"))
        source = (row.get("metadata") or {}).get("source") or {}
        for gene in as_list(source.get("genes")) + as_list(source.get("comparators")):
            add_gene(gene)
        for cell_type in as_cell_type_list(source.get("cell_types")):
            cell_types.add(cell_type)

    for parsed in parsed_reports.values():
        add_gene(parsed["target_gene"])
        for section_rows in parsed["sections"].values():
            for row in section_rows:
                for gene in as_list(row.get("genes")) + as_list(row.get("comparators")):
                    add_gene(gene)
                for cell_type in as_cell_type_list(row.get("cell_type")) + as_cell_type_list(row.get("cell_types")):
                    cell_types.add(cell_type)

    return genes, cell_types


def canonical_gene(value: object, gene_vocab: dict[str, str]) -> str:
    gene = normalize_gene_symbol(value)
    return gene_vocab.get(gene.casefold(), gene)


def evidence_snippet(text: str, term: str, width: int = 220) -> str:
    idx = text.casefold().find(term.casefold())
    if idx < 0:
        return text[:width].strip()
    start = max(0, idx - width // 3)
    end = min(len(text), idx + len(term) + width)
    return text[start:end].strip()


def load_openie_by_passage(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    by_passage: dict[str, dict] = {}
    for doc in payload.get("docs") or []:
        passage = normalize_text(doc.get("passage"))
        if passage:
            by_passage.setdefault(passage, doc)
    return by_passage


def add_node(nodes: dict[str, Node], node: Node) -> None:
    existing = nodes.get(node.id)
    if existing is None:
        nodes[node.id] = node
        return
    existing.labels = tuple(dict.fromkeys([*existing.labels, *node.labels]))
    merged = dict(existing.props)
    for key, value in node.props.items():
        clean = normalize_text(value)
        if not clean:
            continue
        if key not in merged or not merged[key]:
            merged[key] = clean
        elif clean not in str(merged[key]).split("|"):
            merged[key] = f"{merged[key]}|{clean}"
    existing.props = merged


def add_rel(rels: list[Rel], seen: set[tuple[str, str, str, str]], rel: Rel) -> None:
    key = (
        rel.start_id,
        rel.end_id,
        rel.rel_type,
        rel.props.get("role", ""),
    )
    if key in seen:
        return
    seen.add(key)
    rels.append(rel)


def node_for_gene(nodes: dict[str, Node], symbol: str, *, is_target: bool = False) -> str:
    node_id = stable_id("gene", symbol)
    labels = ("BioKGNode", "Gene", "TargetGene") if is_target else ("BioKGNode", "Gene")
    add_node(
        nodes,
        Node(
            id=node_id,
            kind="Gene",
            name=symbol,
            labels=labels,
            props={"symbol": symbol},
        ),
    )
    return node_id


def node_for_cell_type(nodes: dict[str, Node], cell_type: str) -> str:
    node_id = stable_id("cell_type", cell_type)
    add_node(
        nodes,
        Node(
            id=node_id,
            kind="CellType",
            name=cell_type,
            labels=("BioKGNode", "CellType"),
            props={"cell_type": cell_type},
        ),
    )
    return node_id


def build_candidates(
    row: dict,
    source: dict,
    gene_vocab: dict[str, str],
    openie_doc: dict | None,
) -> dict:
    metadata_genes = [
        canonical_gene(gene, gene_vocab)
        for gene in as_list(source.get("genes"))
        if canonical_gene(gene, gene_vocab)
    ]
    metadata_comparators = [
        canonical_gene(gene, gene_vocab)
        for gene in as_list(source.get("comparators"))
        if canonical_gene(gene, gene_vocab)
    ]
    openie_entities = as_list((openie_doc or {}).get("extracted_entities"))
    return {
        "doc_id": row.get("doc_id"),
        "target_gene": row.get("gene_target"),
        "finding_id": source.get("finding_id") or (row.get("metadata") or {}).get("finding_id"),
        "source": "metadata_seed_context",
        "metadata_genes": metadata_genes,
        "metadata_comparators": metadata_comparators,
        "metadata_cell_types": as_cell_type_list(source.get("cell_types")),
        "metadata_evidence_ids": as_list(source.get("evidence_ids")),
        "metadata_ref_ids": as_list(source.get("ref_ids")),
        "openie_entities_for_llm_context": openie_entities,
        "openie_triples_for_llm_context": (openie_doc or {}).get("extracted_triples") or [],
        "status": "seed_context_only",
    }


def finding_record_key(doc_id: object, target_gene: object, finding_id: object) -> str:
    doc = normalize_text(doc_id)
    if doc:
        return doc
    target = normalize_gene_symbol(target_gene)
    finding = normalize_text(finding_id)
    return f"{target}:{finding}" if target or finding else ""


def canonical_entity_kind(value: object) -> str:
    raw = normalize_text(value).replace("-", "_")
    return LLM_ENTITY_KINDS.get(raw.casefold(), "")


def is_non_biological_concept(kind: str, name: str) -> bool:
    if kind in {"Gene", "Other"}:
        return False
    lower = name.casefold()
    if lower in NON_BIOLOGICAL_CONCEPT_NAMES:
        return True
    return any(term in lower for term in NON_BIOLOGICAL_CONCEPT_TERMS)


def entity_labels(kind: str) -> tuple[str, ...]:
    return ("BioKGNode", kind)


def entity_display_name(entity: dict) -> str:
    return (
        normalize_text(entity.get("canonical_name"))
        or normalize_text(entity.get("normalized_name"))
        or normalize_text(entity.get("name"))
        or normalize_text(entity.get("text"))
        or normalize_text(entity.get("label"))
    )


def iter_named_entities(record: dict) -> Iterable[dict]:
    for entity in record.get("entities") or []:
        if isinstance(entity, dict):
            yield entity
    for entity_field, kind, default_relation in [
        ("genes", "Gene", "AFFECTS_GENE"),
        ("affected_genes", "Gene", "AFFECTS_GENE"),
        ("downstream_genes", "Gene", "AFFECTS_GENE"),
        ("comparators", "Gene", "COMPARES_TO"),
        ("modules", "Module", "IMPLICATES"),
        ("pathways", "Pathway", "IMPLICATES"),
        ("complexes", "Complex", "IMPLICATES"),
        ("phenotypes", "Phenotype", "IMPLICATES"),
        ("biological_processes", "Pathway", "IMPLICATES"),
        ("other_entities", "Other", "IMPLICATES"),
        ("others", "Other", "IMPLICATES"),
        ("concepts", "", "IMPLICATES"),
    ]:
        for item in record.get(entity_field) or []:
            if isinstance(item, str):
                yield {"kind": kind, "name": item, "relation_to_finding": default_relation}
            elif isinstance(item, dict):
                entity = dict(item)
                entity.setdefault("kind", kind)
                entity.setdefault("relation_to_finding", default_relation)
                yield entity


def normalize_llm_entity(
    entity: dict, *, target_gene: str, gene_vocab: dict[str, str], cell_vocab: set[str]
) -> dict | None:
    kind = canonical_entity_kind(entity.get("kind") or entity.get("type") or entity.get("entity_type"))
    if not kind:
        return None
    other_type = normalize_text(entity.get("other_type") or entity.get("source_kind"))
    if kind == "Other" and other_type.casefold() in DROP_OTHER_TYPES:
        return None
    if kind == "Other" and other_type.casefold() in LLM_ENTITY_KINDS:
        promoted_kind = LLM_ENTITY_KINDS[other_type.casefold()]
        if promoted_kind != "Other":
            kind = promoted_kind
    # Change #2: re-route gene-product Other subtypes to Gene, drop noise subtypes.
    if kind == "Other":
        routed = classify_other_type(other_type)
        if routed == "DROP":
            return None
        if routed == "Gene":
            kind = "Gene"
    if kind == "Gene":
        raw_names = [
            normalize_text(entity.get("name")),
            normalize_text(entity.get("canonical_name")),
            normalize_text(entity.get("normalized_name")),
            *as_list(entity.get("aliases")),
        ]
        role = normalize_text(entity.get("role"))
        if role.casefold() == "target gene":
            return None
        if any(normalize_gene_symbol(raw).casefold() == target_gene.casefold() for raw in raw_names if raw):
            return None
        name = normalize_text(entity.get("name")) or entity_display_name(entity)
    else:
        name = entity_display_name(entity)
    if not name:
        return None
    # Change #3: reject seed cell-type and finding_type labels leaking in as non-seed nodes.
    if is_leaked_seed_label(name, cell_vocab):
        return None
    if is_non_biological_concept(kind, name):
        return None
    if kind == "Other":
        gene_candidate = canonical_gene(name, gene_vocab)
        if gene_candidate.casefold() in gene_vocab:
            kind = "Gene"
            name = gene_candidate
    if kind == "Gene":
        name = canonical_gene(name, gene_vocab)
        if name.casefold() in GENERIC_GENE_NAMES:
            return None
        if not name or name.casefold() == target_gene.casefold():
            return None

    relation = normalize_text(entity.get("relation_to_finding") or entity.get("relation") or entity.get("edge_type"))
    role = normalize_text(entity.get("role"))
    relation_key = relation.casefold()
    role_key = role.casefold()
    if kind == "Gene":
        if relation_key == "compares_to" or "comparator" in role_key or "neighbor" in role_key:
            relation = "COMPARES_TO"
        else:
            relation = "AFFECTS_GENE"
    elif relation_key not in {"implicates", "has_response_type"}:
        relation = "IMPLICATES"
    else:
        relation = relation.upper()

    effect_status = normalize_text(entity.get("effect_status") or entity.get("status"))
    if not effect_status:
        status_context = f"{role} {entity.get('evidence_span') or entity.get('evidence') or entity.get('quote')}".casefold()
        if "fdr-insignificant" in status_context or "fdr insignificant" in status_context:
            effect_status = "fdr_insignificant"
        elif "mixed" in status_context:
            effect_status = "mixed"
        elif "buffer" in status_context:
            effect_status = "buffered"
        elif "not detected" in status_context or "absent" in status_context or "no " in status_context:
            effect_status = "absent_or_not_detected"
        elif relation == "COMPARES_TO":
            effect_status = "compared"
        elif relation == "AFFECTS_GENE":
            effect_status = "affected"
        else:
            effect_status = "implicated"

    return {
        "kind": kind,
        "name": name,
        "relation_to_finding": relation,
        "other_type": other_type,
        "effect_status": effect_status,
        "role": role or kind.lower(),
        "evidence_span": normalize_text(entity.get("evidence_span") or entity.get("evidence") or entity.get("quote")),
        "confidence": normalize_text(entity.get("confidence")),
        "source": normalize_text(entity.get("source") or entity.get("normalizer") or "llm_scispacy"),
        "aliases": as_list(entity.get("aliases")),
    }


def load_llm_entities(
    path: Path | None, *, gene_vocab: dict[str, str], cell_vocab: set[str]
) -> tuple[dict[str, list[dict]], dict]:
    if path is None:
        return {}, {"status": "not_configured", "records": 0, "path": ""}
    if not path.exists():
        return {}, {"status": "missing", "records": 0, "path": str(path)}

    by_finding: dict[str, list[dict]] = defaultdict(list)
    rows = read_jsonl(path)
    skipped = 0
    for row in rows:
        target = normalize_gene_symbol(row.get("target_gene") or row.get("gene_target"))
        key = finding_record_key(row.get("doc_id"), target, row.get("finding_id"))
        if not key:
            skipped += 1
            continue
        for entity in iter_named_entities(row):
            normalized = normalize_llm_entity(
                entity, target_gene=target, gene_vocab=gene_vocab, cell_vocab=cell_vocab
            )
            if normalized:
                by_finding[key].append(normalized)
    return dict(by_finding), {"status": "loaded", "records": len(rows), "path": str(path), "skipped": skipped}


def make_assertion(
    row: dict,
    source: dict,
    biological_finding: dict | None,
    candidate_record: dict,
    llm_entities: list[dict],
) -> dict:
    doc_id = str(row.get("doc_id") or "")
    finding_id = str(source.get("finding_id") or (row.get("metadata") or {}).get("finding_id") or doc_id.split(":")[-1])
    target = normalize_gene_symbol(row.get("gene_target"))
    summary = normalize_text(source.get("source_summary")) or normalize_text((biological_finding or {}).get("summary"))
    why = normalize_text(source.get("source_why_it_matters")) or normalize_text((biological_finding or {}).get("why_it_matters"))
    caveat = normalize_text(source.get("main_caveats")) or normalize_text((biological_finding or {}).get("main_caveats"))
    genes = pipe_join(candidate_record["metadata_genes"])
    comparators = pipe_join(candidate_record["metadata_comparators"])
    cell_types = pipe_join(candidate_record["metadata_cell_types"])
    return {
        "doc_id": doc_id,
        "target_gene": target,
        "finding_id": finding_id,
        "finding_type": normalize_text(source.get("finding_type") or (biological_finding or {}).get("finding_type")),
        "direction": normalize_text(source.get("direction") or (biological_finding or {}).get("direction")),
        "confidence": normalize_text(source.get("confidence") or (biological_finding or {}).get("confidence")),
        "literature_status": normalize_text(source.get("literature_status") or (biological_finding or {}).get("literature_status")),
        "summary": summary,
        "why_it_matters": why,
        "main_caveats": caveat,
        "genes": genes.split("|") if genes else [],
        "comparators": comparators.split("|") if comparators else [],
        "cell_types": cell_types.split("|") if cell_types else [],
        "evidence_ids": as_list(source.get("evidence_ids")) or as_list((biological_finding or {}).get("evidence_ids")),
        "ref_ids": as_list(source.get("ref_ids")) or as_list((biological_finding or {}).get("ref_ids")),
        "llm_entities": llm_entities,
        "extractor": "metadata_seeds_with_llm_scispacy_entities" if llm_entities else "metadata_seeds_pending_llm_entities",
    }


def build_entity_extraction_request(
    row: dict,
    source: dict,
    biological_finding: dict | None,
    candidate_record: dict,
) -> dict:
    doc_id = str(row.get("doc_id") or "")
    finding_id = str(source.get("finding_id") or (row.get("metadata") or {}).get("finding_id") or doc_id.split(":")[-1])
    target = normalize_gene_symbol(row.get("gene_target"))
    text = str(row.get("final_report") or row.get("text") or "")
    return {
        "doc_id": doc_id,
        "target_gene": target,
        "finding_id": finding_id,
        "task": "extract_normalized_biological_entities_for_kg",
        "seed_nodes": {
            "target_gene": target,
            "finding": {"doc_id": doc_id, "finding_id": finding_id},
            "cell_types": candidate_record["metadata_cell_types"],
            "evidence_ids": candidate_record["metadata_evidence_ids"],
            "ref_ids": candidate_record["metadata_ref_ids"],
        },
        "source_context": {
            "finding_type": normalize_text(source.get("finding_type") or (biological_finding or {}).get("finding_type")),
            "direction": normalize_text(source.get("direction") or (biological_finding or {}).get("direction")),
            "confidence": normalize_text(source.get("confidence") or (biological_finding or {}).get("confidence")),
            "summary": normalize_text(source.get("source_summary") or (biological_finding or {}).get("summary")),
            "why_it_matters": normalize_text(source.get("source_why_it_matters") or (biological_finding or {}).get("why_it_matters")),
            "main_caveats": normalize_text(source.get("main_caveats") or (biological_finding or {}).get("main_caveats")),
            "source_genes_for_context": candidate_record["metadata_genes"],
            "source_comparators_for_context": candidate_record["metadata_comparators"],
            "openie_entities_for_context": candidate_record["openie_entities_for_llm_context"],
            "openie_triples_for_context": candidate_record["openie_triples_for_llm_context"],
            "text": text,
        },
        "entity_schema": {
            "entities": [
                {
                    "kind": "gene|module|pathway|complex|phenotype|other",
                    "name": "surface form from the finding",
                    "canonical_name": "normalized reusable biological entity name",
                    "other_type": "blank unless kind is other; e.g. disease|drug/compound|lipid|ion_channel|current",
                    "aliases": ["optional aliases"],
                    "relation_to_finding": "AFFECTS_GENE|COMPARES_TO|IMPLICATES",
                    "effect_status": "affected|implicated|compared|buffered|absent_or_not_detected|fdr_insignificant|nominal|mixed|caveated|uncertain",
                    "role": "short biological role, not a relation sentence",
                    "evidence_span": "short exact-ish support span from the finding text",
                    "confidence": "high|moderate|low",
                }
            ]
        },
        "instructions": [
            "Use the seed nodes as context; do not re-create target, finding, evidence, reference, or cell-type nodes.",
            "Do not extract the seed target gene under its symbol, protein name, long-form gene name, or alias.",
            "Do not split seed cell-type labels into genes or concepts. Treat neurotransmitter/class labels such as Glut, Gaba/GABA, Pvalb Gaba, MB Glut, and P MY as cell-type context unless the text independently describes them as affected genes.",
            "Use source_context.source_genes_for_context and source_context.source_comparators_for_context as hints for real gene mentions; OpenIE entities may contain cell-type label fragments.",
            "Create non-seed entity nodes only for reusable biological things: genes, modules, pathways/processes, complexes, phenotypes, or other typed biological entities.",
            "Use kind 'pathway' for named mechanisms, pathways, and GO-like biological processes.",
            "Use kind 'other' only when no fixed category fits. Good examples are diseases, drugs/compounds, lipids/metabolites, ion channels, or electrophysiological currents. Do not set kind 'other' with other_type biological_process or phenotype; use the fixed kind instead.",
            "Buffered transcriptional response is a valid phenotype when the finding explicitly describes buffering or transcriptomic silence.",
            "Use effect_status to distinguish positive effects from buffered, absent, FDR-insignificant, nominal, mixed, caveated, or uncertain evidence.",
            "Do not turn arbitrary prose into entities. For example, 'assay for every member of the broader pathway' is not a pathway node, and 'strongest signature' is not a module.",
            "Prefer specific canonical names over sentence fragments.",
            "Preserve uncertainty with confidence values and evidence spans.",
        ],
    }


def index_reports(parsed_reports: dict[str, dict]) -> dict[str, dict[str, dict]]:
    indexed: dict[str, dict[str, dict]] = {}
    for target, parsed in parsed_reports.items():
        sections = parsed["sections"]
        indexed[target] = {
            "evidence": {str(row.get("evidence_id")): row for row in sections.get("evidence", [])},
            "references": {str(row.get("ref_id")): row for row in sections.get("references", [])},
            "biological_findings": {
                str(row.get("finding_id")): row for row in sections.get("biological_findings", [])
            },
            "literature_comparisons": defaultdict(list),
            "pathways": defaultdict(list),
            "cell_type_specificity": defaultdict(list),
        }
        for row in sections.get("literature_comparisons", []):
            indexed[target]["literature_comparisons"][str(row.get("finding_id"))].append(row)
        for row in sections.get("pathways", []):
            for finding_id in as_list(row.get("finding_ids")):
                indexed[target]["pathways"][finding_id].append(row)
        for row in sections.get("cell_type_specificity", []):
            for finding_id in as_list(row.get("finding_ids")):
                indexed[target]["cell_type_specificity"][finding_id].append(row)
    return indexed


# ---------------------------------------------------------------------------
# Phase-3: per-gene direction + effect_status parsed from Evidence.statistics.
# The statistics strings are heterogeneous prose; we anchor on each gene token,
# bound a window to the next gene token / ';', and pull the gene's logFC, FDR
# and nominal p. A gene mentioned in several cell types yields several windows;
# we keep the most-significant occurrence (min FDR, else min p). Validated
# against debug/260627_biokg_evidence/evidence_ledger.csv (~38% of pairs carry
# parseable per-gene stats; the rest are correlation/aggregate-only -> neutral).
# ---------------------------------------------------------------------------

_STAT_NUM = r"[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?"


def _stat_windows(stat: str, gene: str, gene_set: set[str]) -> list[str]:
    """Substrings of `stat` scoped to each occurrence of `gene` (bounded by the
    next other-gene token or ';')."""
    windows: list[str] = []
    for m in re.finditer(rf"\b{re.escape(gene)}\b", stat):
        start = m.end()
        end = len(stat)
        for og in gene_set:
            if og == gene:
                continue
            mm = re.search(rf"\b{re.escape(og)}\b", stat[start:])
            if mm:
                end = min(end, start + mm.start())
        idx = stat.find(";", start)
        if idx != -1:
            end = min(end, idx)
        windows.append(stat[m.start():end])
    return windows


def _grab(pat: str, text: str) -> str | None:
    m = re.search(pat, text)
    return m.group(1) if m else None


def parse_gene_stats(stat: str, gene: str, gene_set: set[str]) -> dict:
    """Extract the most-significant (logfc, fdr, pval) for `gene` from `stat`."""
    best = None  # (key, rec); key = (significance, -n_fields) -> minimise
    for w in _stat_windows(stat, gene, gene_set):
        logfc = _grab(rf"logFC\s*=?\s*({_STAT_NUM})", w)
        if logfc is None:
            # enumeration continuation: "Aars 0.733 FDR=1.94e-12" (logFC label
            # dropped); a leading signed decimal right before FDR/p is the logFC.
            logfc = _grab(rf"^{re.escape(gene)}\b[\s:=]*([-+]?\d+\.\d+)\s*(?:FDR|p[=\s])", w)
        fdr = _grab(rf"FDR\s*(?:<=|=)?\s*({_STAT_NUM})", w)
        op = re.search(rf"FDR\s*(<=|<|>=|>|=)?\s*{_STAT_NUM}", w)
        if op and op.group(1) == "<" and fdr in {"0.05", "0.10", "0.1", "0.01"}:
            fdr = None  # this was a "N genes FDR<0.05" threshold, not a value
        # p must be a standalone token (not the 'p' inside Atp2b3/Nup214/Hsp90)
        pval = _grab(rf"(?<![A-Za-z])[pP][\s=<]+({_STAT_NUM})", w)
        score = _grab(rf"(?<![A-Za-z])score[=\s]*({_STAT_NUM})", w)
        rec = {"logfc": logfc, "fdr": fdr, "pval": pval, "score": score, "window": w[:160]}
        sig = float(fdr) if fdr else (float(pval) if pval else 2.0)
        n_fields = (logfc is not None) + (fdr is not None) + (pval is not None)
        key = (sig, -n_fields)
        if best is None or key < best[0]:
            best = (key, rec)
    return best[1] if best else {"logfc": None, "fdr": None, "pval": None, "score": None, "window": ""}


def measured_gene_effect(stat: str, gene: str, gene_set: set[str]) -> dict:
    """Map parsed stats to {direction, effect_status, logfc, pval, fdr}.

    Thresholds (signed off 2026-06-27): FDR<0.05 -> affected; FDR>=0.05 & p<1e-3
    -> nominal; else absent_or_not_detected; logFC-only -> measured (+direction);
    correlation/aggregate-only -> measured (neutral). Direction = sign(logFC),
    else sign(score), else nearby up/down word.
    """
    rec = parse_gene_stats(stat, gene, gene_set)
    logfc = float(rec["logfc"]) if rec["logfc"] else None
    fdr = float(rec["fdr"]) if rec["fdr"] else None
    pval = float(rec["pval"]) if rec["pval"] else None
    score = float(rec["score"]) if rec["score"] else None

    direction = ""
    if logfc is not None and logfc != 0:
        direction = "up" if logfc > 0 else "down"
    elif score is not None and score != 0:
        direction = "up" if score > 0 else "down"
    else:
        win = rec["window"].lower()
        if "up-regulated" in win or re.search(r"\bup\b", win) or "increase" in win:
            direction = "up"
        elif "down-regulated" in win or re.search(r"\bdown\b", win) or "decrease" in win:
            direction = "down"

    out = {
        "direction": direction,
        "logfc": rec["logfc"] or "",
        "pval": rec["pval"] or "",
        "fdr": rec["fdr"] or "",
    }
    bulk_absent = bool(re.search(r"(all|every).{0,40}FDR\s*(?:=|values were)\s*1\.0", stat, re.I))

    if fdr is not None:
        out["effect_status"] = "affected" if fdr < 0.05 else (
            "nominal" if (pval is not None and pval < 1e-3) else "absent_or_not_detected")
    elif pval is not None:
        out["effect_status"] = "nominal" if pval < 1e-3 else "absent_or_not_detected"
    elif logfc is not None:
        out["effect_status"] = "measured"  # direction known, significance not
    elif bulk_absent:
        out["effect_status"] = "absent_or_not_detected"
    else:
        out["effect_status"] = "measured"  # correlation/aggregate-only, neutral
    return out


def build_graph(
    finding_rows: list[dict],
    parsed_reports: dict[str, dict],
    openie_by_passage: dict[str, dict],
    llm_entities_path: Path | None,
) -> tuple[dict[str, Node], list[Rel], list[dict], list[dict], list[dict], dict]:
    gene_vocab, cell_vocab = collect_gene_and_cell_vocab(finding_rows, parsed_reports)
    cell_vocab_cf = {c.casefold() for c in cell_vocab}
    llm_entities_by_finding, llm_entity_diagnostics = load_llm_entities(
        llm_entities_path, gene_vocab=gene_vocab, cell_vocab=cell_vocab_cf
    )
    indexed_reports = index_reports(parsed_reports)
    nodes: dict[str, Node] = {}
    rels: list[Rel] = []
    rel_seen: set[tuple[str, str, str, str]] = set()
    candidates: list[dict] = []
    normalized_findings: list[dict] = []
    extraction_requests: list[dict] = []
    missing_evidence: Counter[str] = Counter()
    missing_references: Counter[str] = Counter()

    assay_id = stable_id("assay", "Perturb-seq")
    add_node(
        nodes,
        Node(
            id=assay_id,
            kind="Assay",
            name="Perturb-seq",
            labels=("BioKGNode", "Assay"),
            props={"description": "Known assay context for the sampled perturbation findings"},
        ),
    )

    for target, parsed in parsed_reports.items():
        node_for_gene(nodes, target, is_target=True)
        for evidence in parsed["sections"].get("evidence", []):
            evidence_id = f"{target}:{evidence.get('evidence_id')}"
            node_id = stable_id("evidence", evidence_id)
            # Structured measured-gene list from the source Evidence JSONL. Ground each
            # symbol and drop cell-type / finding-type leaks (canonical_gene does not
            # itself filter non-genes). Keeps the target in the property for fidelity.
            evidence_genes: list[str] = []
            # canonical symbol -> raw surface form as written in the statistics prose
            # (Phase-3 parser must anchor on the raw token, not the canonicalized one).
            raw_by_canonical: dict[str, str] = {}
            for raw_gene in as_list(evidence.get("genes")):
                g = canonical_gene(raw_gene, gene_vocab)
                if not g or is_leaked_seed_label(g, cell_vocab_cf):
                    continue
                if g not in evidence_genes:
                    evidence_genes.append(g)
                    raw_by_canonical[g] = normalize_gene_symbol(raw_gene)
            add_node(
                nodes,
                Node(
                    id=node_id,
                    kind="Evidence",
                    name=evidence_id,
                    labels=("BioKGNode", "Evidence"),
                    props={
                        "target_gene": target,
                        "evidence_id": normalize_text(evidence.get("evidence_id")),
                        "evidence_slug": normalize_text(evidence.get("evidence_slug")),
                        "description": normalize_text(evidence.get("description")),
                        "statistics": normalize_text(evidence.get("statistics")),
                        "cell_type": pipe_join(as_cell_type_list(evidence.get("cell_type"))),
                        "genes": pipe_join(evidence_genes),
                    },
                ),
            )
            for cell_type in as_cell_type_list(evidence.get("cell_type")):
                cell_id = node_for_cell_type(nodes, cell_type)
                add_rel(
                    rels,
                    rel_seen,
                    Rel(node_id, cell_id, "DESCRIBES_CELL_TYPE"),
                )
            # Materialize Evidence -> Gene measured edges. Phase-3: parse each gene's
            # logFC/p/FDR out of the statistics prose and stamp direction + effect_status
            # (most-significant occurrence when a gene spans cell types). Skip the
            # perturbed target, which is already linked via the finding's HAS_TARGET.
            statistics_text = normalize_text(evidence.get("statistics"))
            raw_gene_set = set(raw_by_canonical.values())
            for g in evidence_genes:
                if g.casefold() == target.casefold():
                    continue
                gene_id = node_for_gene(nodes, g, is_target=g.casefold() in parsed_reports)
                raw_g = raw_by_canonical.get(g, g)
                effect = measured_gene_effect(statistics_text, raw_g, raw_gene_set)
                add_rel(
                    rels,
                    rel_seen,
                    Rel(node_id, gene_id, "MEASURED_GENE", effect),
                )

        for ref in parsed["sections"].get("references", []):
            ref_id = f"{target}:{ref.get('ref_id')}"
            node_id = stable_id("reference", ref_id)
            add_node(
                nodes,
                Node(
                    id=node_id,
                    kind="Reference",
                    name=ref_id,
                    labels=("BioKGNode", "Reference"),
                    props={
                        "target_gene": target,
                        "ref_id": normalize_text(ref.get("ref_id")),
                        "source": normalize_text(ref.get("source")),
                        "source_type": normalize_text(ref.get("source_type")),
                        "citation": normalize_text(ref.get("citation")),
                        "url": normalize_text(ref.get("url")),
                        "description": normalize_text(ref.get("description")),
                    },
                ),
            )

    for row in finding_rows:
        target = normalize_gene_symbol(row.get("gene_target"))
        doc_id = str(row.get("doc_id") or "")
        text = str(row.get("final_report") or row.get("text") or "")
        metadata = row.get("metadata") or {}
        source = metadata.get("source") or {}
        finding_id = str(source.get("finding_id") or metadata.get("finding_id") or doc_id.split(":")[-1])
        target_index = indexed_reports.get(target, {})
        biological_finding = (target_index.get("biological_findings") or {}).get(finding_id)
        openie_doc = openie_by_passage.get(normalize_text(text))
        candidate_record = build_candidates(row, source, gene_vocab, openie_doc)
        record_key = finding_record_key(doc_id, target, finding_id)
        llm_entities = llm_entities_by_finding.get(record_key, [])
        assertion = make_assertion(row, source, biological_finding, candidate_record, llm_entities)
        candidates.append(candidate_record)
        normalized_findings.append(assertion)
        extraction_requests.append(build_entity_extraction_request(row, source, biological_finding, candidate_record))

        # Structured finding-level gene/comparator lists (prefer the appendix Biological
        # Findings block; fall back to the metadata seed list). Grounded + leak-filtered.
        bf = biological_finding or {}
        finding_genes: list[str] = []
        for raw_gene in (as_list(bf.get("genes")) or assertion["genes"]):
            g = canonical_gene(raw_gene, gene_vocab)
            if g and not is_leaked_seed_label(g, cell_vocab_cf) and g not in finding_genes:
                finding_genes.append(g)
        finding_comparators: list[str] = []
        for raw_gene in (as_list(bf.get("comparators")) or assertion["comparators"]):
            g = canonical_gene(raw_gene, gene_vocab)
            if g and not is_leaked_seed_label(g, cell_vocab_cf) and g not in finding_comparators:
                finding_comparators.append(g)

        target_id = node_for_gene(nodes, target, is_target=True)
        finding_node_id = stable_id("finding", doc_id)

        add_node(
            nodes,
            Node(
                id=finding_node_id,
                kind="Finding",
                name=doc_id,
                labels=("BioKGNode", "Finding"),
                props={
                    "doc_id": doc_id,
                    "finding_id": finding_id,
                    "target_gene": target,
                    "finding_type": assertion["finding_type"],
                    "direction": assertion["direction"],
                    "confidence": assertion["confidence"],
                    "literature_status": assertion["literature_status"],
                    "summary": assertion["summary"],
                    "why_it_matters": assertion["why_it_matters"],
                    "text": text,
                    "main_caveats": assertion["main_caveats"],
                    "evidence_ids": pipe_join(assertion["evidence_ids"]),
                    "ref_ids": pipe_join(assertion["ref_ids"]),
                    "genes": pipe_join(finding_genes),
                    "comparators": pipe_join(finding_comparators),
                    "extractor": assertion["extractor"],
                },
            ),
        )
        add_rel(rels, rel_seen, Rel(target_id, finding_node_id, "HAS_FINDING"))
        add_rel(
            rels,
            rel_seen,
            Rel(finding_node_id, target_id, "HAS_TARGET"),
        )
        add_rel(rels, rel_seen, Rel(finding_node_id, assay_id, "USES_ASSAY"))

        for cell_type in assertion["cell_types"]:
            cell_id = node_for_cell_type(nodes, cell_type)
            add_rel(
                rels,
                rel_seen,
                Rel(
                    finding_node_id,
                    cell_id,
                    "OBSERVED_IN",
                    {"evidence": evidence_snippet(text, cell_type)},
                ),
            )

        # Materialize Finding -> Gene edges from the structured source lists (distinct from
        # the LLM-derived AFFECTS_GENE/IMPLICATES interpretive layer). Skip the target self.
        for g in finding_genes:
            if g.casefold() == target.casefold():
                continue
            gene_id = node_for_gene(nodes, g, is_target=g.casefold() in parsed_reports)
            add_rel(
                rels,
                rel_seen,
                Rel(finding_node_id, gene_id, "REPORTS_GENE", {"role": "finding_reported_gene"}),
            )
        for g in finding_comparators:
            if g.casefold() == target.casefold():
                continue
            gene_id = node_for_gene(nodes, g, is_target=g.casefold() in parsed_reports)
            add_rel(
                rels,
                rel_seen,
                Rel(
                    finding_node_id,
                    gene_id,
                    "REPORTS_GENE",
                    {"role": "finding_reported_comparator"},
                ),
            )

        for entity in assertion["llm_entities"]:
            entity_name = entity["name"]
            entity_kind = entity["kind"]
            if entity_kind == "Gene":
                # Genes come only from the deterministic, measurement-anchored layers
                # (MEASURED_GENE from evidence.genes, REPORTS_GENE from finding.genes).
                # The LLM gene re-derivation is lossy and noisy (injects drugs/aliases/
                # cell-type-name tokens as "genes") and produces a wrong cross-target
                # convergence ranking (see decisions.md 2026-06-27 lane comparison), so
                # no Gene node and no AFFECTS_GENE/COMPARES_TO edge is created here. The
                # LLM concept layer (IMPLICATES) is kept below.
                continue
            else:
                entity_id = stable_id(entity_kind, entity_name)
                add_node(
                    nodes,
                    Node(
                        id=entity_id,
                        kind=entity_kind,
                        name=entity_name,
                        labels=entity_labels(entity_kind),
                        props={
                            "other_type": entity["other_type"],
                            "source": entity["source"],
                            "confidence": entity["confidence"],
                        },
                    ),
                )
                rel_type = "IMPLICATES"
            add_rel(
                rels,
                rel_seen,
                Rel(
                    finding_node_id,
                    entity_id,
                    rel_type,
                    {
                        "role": entity["role"],
                        "evidence": entity["evidence_span"] or evidence_snippet(text, entity_name),
                        "confidence": entity["confidence"] or assertion["confidence"],
                        "effect_status": entity["effect_status"],
                    },
                ),
            )

        for evidence_id in assertion["evidence_ids"]:
            evidence = (target_index.get("evidence") or {}).get(evidence_id)
            evidence_node_id = stable_id("evidence", f"{target}:{evidence_id}")
            if evidence is None:
                missing_evidence[target] += 1
                add_node(
                    nodes,
                    Node(
                        id=evidence_node_id,
                        kind="Evidence",
                        name=f"{target}:{evidence_id}",
                        labels=("BioKGNode", "Evidence", "MissingAppendixNode"),
                        props={
                            "target_gene": target,
                            "evidence_id": evidence_id,
                            "status": "referenced_missing_appendix",
                        },
                    ),
                )
            add_rel(
                rels,
                rel_seen,
                Rel(finding_node_id, evidence_node_id, "SUPPORTED_BY"),
            )

        for ref_id in assertion["ref_ids"]:
            ref = (target_index.get("references") or {}).get(ref_id)
            ref_node_id = stable_id("reference", f"{target}:{ref_id}")
            if ref is None:
                missing_references[target] += 1
                add_node(
                    nodes,
                    Node(
                        id=ref_node_id,
                        kind="Reference",
                        name=f"{target}:{ref_id}",
                        labels=("BioKGNode", "Reference", "MissingAppendixNode"),
                        props={
                            "target_gene": target,
                            "ref_id": ref_id,
                            "status": "referenced_missing_appendix",
                        },
                    ),
                )
            add_rel(
                rels,
                rel_seen,
                Rel(finding_node_id, ref_node_id, "CITES"),
            )

        for comparison in (target_index.get("literature_comparisons") or {}).get(finding_id, []):
            comparison_id = f"{target}:{comparison.get('comparison_id')}"
            comparison_node_id = stable_id("literature_comparison", comparison_id)
            add_node(
                nodes,
                Node(
                    id=comparison_node_id,
                    kind="LiteratureComparison",
                    name=comparison_id,
                    labels=("BioKGNode", "LiteratureComparison"),
                    props={
                        "target_gene": target,
                        "comparison_id": normalize_text(comparison.get("comparison_id")),
                        "finding_id": finding_id,
                        "summary": normalize_text(comparison.get("dataset_claim")),
                        "description": normalize_text(comparison.get("literature_claim")),
                        "literature_status": normalize_text(comparison.get("relationship_to_literature")),
                        "confidence": normalize_text(comparison.get("confidence")),
                    },
                ),
            )
            add_rel(
                rels,
                rel_seen,
                Rel(
                    finding_node_id,
                    comparison_node_id,
                    "HAS_LITERATURE_COMPARISON",
                ),
            )
            for evidence_id in as_list(comparison.get("evidence_ids")):
                add_rel(
                    rels,
                    rel_seen,
                    Rel(
                        comparison_node_id,
                        stable_id("evidence", f"{target}:{evidence_id}"),
                        "SUPPORTED_BY",
                    ),
                )
            for ref_id in as_list(comparison.get("ref_ids")):
                add_rel(
                    rels,
                    rel_seen,
                    Rel(
                        comparison_node_id,
                        stable_id("reference", f"{target}:{ref_id}"),
                        "CITES",
                    ),
                )

    diagnostics = {
        "missing_evidence_references": dict(missing_evidence),
        "missing_reference_references": dict(missing_references),
        "llm_entities": llm_entity_diagnostics,
    }
    return nodes, rels, candidates, normalized_findings, extraction_requests, diagnostics


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_nodes_csv(path: Path, nodes: dict[str, Node]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=NODE_FIELDS)
        writer.writeheader()
        for node in sorted(nodes.values(), key=lambda item: (item.kind, item.name, item.id)):
            row = {field: "" for field in NODE_FIELDS}
            row.update({"id": node.id, "kind": node.kind, "labels": ";".join(node.labels), "name": node.name})
            for key, value in node.props.items():
                if key in row:
                    row[key] = str(value)
            writer.writerow(row)


def write_relationships_csv(path: Path, rels: list[Rel]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REL_FIELDS)
        writer.writeheader()
        for rel in sorted(rels, key=lambda item: (item.start_id, item.rel_type, item.end_id, item.props.get("role", ""))):
            row = {field: "" for field in REL_FIELDS}
            row.update({"start_id": rel.start_id, "end_id": rel.end_id, "type": rel.rel_type})
            for key, value in rel.props.items():
                if key in row:
                    row[key] = str(value)
            writer.writerow(row)


def write_neo4j_load_cypher(path: Path, rel_types: Iterable[str]) -> None:
    prop_sets = ",\n    ".join(
        f"n.{field} = row.{field}"
        for field in NODE_FIELDS
        if field not in {"id", "kind", "labels"}
    )
    rel_prop_sets = ",\n    ".join(f"r.{field} = row.{field}" for field in REL_FIELDS if field not in {"start_id", "end_id", "type"})
    rel_blocks = []
    for rel_type in sorted(set(rel_types)):
        rel_blocks.append(
            f"""
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = '{rel_type}'
MATCH (a:BioKGNode {{id: row.start_id}})
MATCH (b:BioKGNode {{id: row.end_id}})
CREATE (a)-[r:{rel_type}]->(b)
SET {rel_prop_sets};
""".strip()
        )
    label_blocks = "\n".join(
        f"FOREACH (_ IN CASE WHEN row.labels CONTAINS '{label}' THEN [1] ELSE [] END | SET n:{label})"
        for label in [
            "Gene",
            "TargetGene",
            "Finding",
            "Evidence",
            "Reference",
            "CellType",
            "Module",
            "Pathway",
            "Complex",
            "Phenotype",
            "Other",
            "LiteratureComparison",
            "Assay",
            "MissingAppendixNode",
        ]
    )
    path.write_text(
        f"""// Neo4j LOAD CSV script for BioKG MVP v2.
// Put v2 nodes.csv and relationships.csv in Neo4j's import directory, then run this.

CREATE CONSTRAINT biokg_node_id IF NOT EXISTS
FOR (n:BioKGNode) REQUIRE n.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
CREATE (n:BioKGNode)
SET n.id = row.id,
    {prop_sets}
{label_blocks};

{chr(10).join(rel_blocks)}
""",
        encoding="utf-8",
    )


def write_query_tests(path: Path) -> None:
    path.write_text(
        """// Targeted: Arx Pvalb findings with evidence and references.
MATCH p=(:TargetGene {symbol:'Arx'})-[:HAS_FINDING]->(f:Finding)-[]->()
WHERE (f)-[:OBSERVED_IN]->(:CellType {name:'052 Pvalb Gaba'})
RETURN p LIMIT 50;

// Targeted: evidence supporting Agps sterol-program findings.
MATCH (:TargetGene {symbol:'Agps'})-[:HAS_FINDING]->(f:Finding)
MATCH (f)-[:SUPPORTED_BY]->(e:Evidence)
OPTIONAL MATCH (f)-[:CITES]->(r:Reference)
RETURN f.finding_id AS finding, f.summary AS finding_summary, collect(DISTINCT e.name) AS evidence, collect(DISTINCT r.name) AS refs
ORDER BY finding;

// Broad: dominant LLM/scispaCy-normalized concepts by target support.
MATCH (x)<-[:IMPLICATES]-(f:Finding)<-[:HAS_FINDING]-(t:TargetGene)
WHERE x:Module OR x:Pathway OR x:Phenotype OR x:Complex OR x:Other
RETURN labels(x) AS labels, x.name AS entity, count(DISTINCT t) AS targets, count(DISTINCT f) AS findings,
       collect(DISTINCT t.symbol)[0..20] AS target_symbols
ORDER BY targets DESC, findings DESC, entity
LIMIT 50;

// Broad: LLM/scispaCy-normalized concepts shared by at least two sampled targets.
MATCH (x)<-[:IMPLICATES]-(f:Finding)<-[:HAS_FINDING]-(t:TargetGene)
WHERE x:Module OR x:Pathway OR x:Phenotype OR x:Complex OR x:Other
WITH x, collect(DISTINCT t.symbol) AS target_symbols, count(DISTINCT f) AS findings
WHERE size(target_symbols) >= 2
RETURN labels(x) AS labels, x.name AS entity, size(target_symbols) AS targets, findings, target_symbols
ORDER BY targets DESC, findings DESC, entity
LIMIT 50;

// Broad: catch-all Other entities to review for future schema promotion.
MATCH (x:Other)<-[r:IMPLICATES]-(f:Finding)<-[:HAS_FINDING]-(t:TargetGene)
RETURN x.other_type AS other_type, x.name AS entity, count(DISTINCT t) AS targets,
       count(DISTINCT f) AS findings, collect(DISTINCT r.effect_status) AS statuses,
       collect(DISTINCT t.symbol)[0..20] AS target_symbols
ORDER BY findings DESC, entity
LIMIT 50;

// Broad: target engagement or buffered response claims.
MATCH (t:TargetGene)-[:HAS_FINDING]->(f:Finding)
WHERE toLower(f.summary + ' ' + f.text + ' ' + f.direction) CONTAINS 'buffer'
   OR toLower(f.summary + ' ' + f.text + ' ' + f.direction) CONTAINS 'target'
RETURN t.symbol AS target, f.finding_id AS finding, f.confidence AS confidence, f.summary AS summary
ORDER BY target, finding
LIMIT 50;
""",
        encoding="utf-8",
    )


def write_readme(path: Path, args: argparse.Namespace, summary: dict) -> None:
    path.write_text(
        f"""# BioKG MVP v2

This graph is finding-centered and uses a fixed target-panel sample.

## Inputs

- Target reports: `{args.reports}`
- Narrative findings: `{args.findings}`
- OpenIE cache: `{args.openie_json}`
- LLM/scispaCy entities: `{args.llm_entities}`

## Model

- `Finding` nodes are the semantic and evidence-bearing unit used for query answering.
- `Evidence` and `Reference` nodes are parsed deterministically from target-level report appendices.
- Target genes, cell types, findings, evidence, and references are deterministic seed nodes.
- Source genes and comparators are emitted as LLM context, but they do not become graph entities unless returned by `llm_entities.normalized.jsonl`.
- Non-seed biological entities are loaded from `llm_entities.normalized.jsonl`; this builder does not create gene/module/pathway/phenotype/other nodes from phrase rules.
- GO-like biological processes are folded into `Pathway` nodes, because this MVP queries mechanisms/processes/pathways as one category. The original extraction kind is preserved in normalized entity records for audit.
- `Other` is a temporary catch-all for reusable entities outside the fixed schema; `other_type` preserves the proposed type for later promotion or merging.

## Outputs

- `aligned_findings.jsonl`: narrative findings selected for the target panel.
- `parsed_reports.jsonl`: parsed target report appendices and parse diagnostics.
- `candidate_entities.jsonl`: seed context per finding.
- `entity_extraction_requests.jsonl`: prompt-ready records for LLM entity extraction and scispaCy normalization.
- `normalized_findings.jsonl`: normalized finding records used to build the graph.
- `nodes.csv` / `relationships.csv`: Neo4j graph tables.
- `query_tests.cypher`: targeted and broad analysis queries.
- `llm_graph_context.json`: graph neighborhoods serialized for LLM reasoning.
- `llm_reasoning_prompt.md`: prompt template for asking an LLM to reason over the serialized graph.
- `llm_entity_quality_report.json` / `.md`: audit report for normalized LLM/scispaCy entity quality.
- `summary.json`: graph counts and diagnostics.

## Build

```bash
# First pass emits entity_extraction_requests.jsonl when no normalized LLM entity file exists.
pixi run -e biokg biokg-v2-build

# Required before non-seed biological entity nodes appear.
pixi run biokg-v2-extract-llm
pixi run -e scispacy biokg-v2-normalize-entities
pixi run -e biokg biokg-v2-entity-quality
pixi run -e biokg biokg-v2-build

pixi run -e biokg biokg-v2-export-llm
```

This command produces a mutable graph candidate under `_work/build/graph/`; it
does not load that candidate into the supported Neo4j host.

## Current Sample

- Targets: {", ".join(summary["sampled_targets"])}
- Findings: {summary["findings"]}
- Normalized findings: {summary["normalized_findings"]}
- Nodes: {summary["nodes"]}
- Relationships: {summary["relationships"]}
- LLM entity status: {summary["diagnostics"]["llm_entities"]["status"]}

Known limitation: when the normalized LLM entity file is absent, the graph is intentionally seed-only for non-seed concepts. Run the LLM extraction and scispaCy normalization steps, then rebuild.
""",
        encoding="utf-8",
    )


def summarize(
    nodes: dict[str, Node],
    rels: list[Rel],
    normalized_findings: list[dict],
    finding_rows: list[dict],
    parsed_reports: dict[str, dict],
    diagnostics: dict,
    args: argparse.Namespace,
) -> dict:
    dangling = [
        {"start_id": rel.start_id, "end_id": rel.end_id, "type": rel.rel_type}
        for rel in rels
        if rel.start_id not in nodes or rel.end_id not in nodes
    ]
    parse_errors = {
        target: parsed["parse_errors"]
        for target, parsed in parsed_reports.items()
        if parsed.get("parse_errors")
    }
    return {
        "reports": str(args.reports),
        "findings_input": str(args.findings),
        "sampled_targets": list(args.targets),
        "findings": len(finding_rows),
        "normalized_findings": len(normalized_findings),
        "nodes": len(nodes),
        "relationships": len(rels),
        "node_kinds": dict(sorted(Counter(node.kind for node in nodes.values()).items())),
        "relationship_types": dict(sorted(Counter(rel.rel_type for rel in rels).items())),
        "parse_errors": parse_errors,
        "diagnostics": diagnostics,
        "dangling_relationships": dangling,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--openie-json", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--llm-entities",
        type=Path,
        default=None,
        help="Normalized LLM/scispaCy entity JSONL. Defaults to OUT/llm_entities.normalized.jsonl.",
    )
    parser.add_argument("--targets", nargs="+", default=list(DEFAULT_TARGETS))
    parser.add_argument(
        "--all-targets",
        action="store_true",
        help="Use every target present in the reports file, ignoring --targets.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.llm_entities is None:
        args.llm_entities = args.out / "llm_entities.normalized.jsonl"

    reports = {normalize_gene_symbol(row.get("gene_target")): row for row in read_jsonl(args.reports)}
    if args.all_targets:
        args.targets = sorted(reports)
    else:
        args.targets = [normalize_gene_symbol(target) for target in args.targets]
    selected_reports = {
        target: parse_report_appendices(reports[target])
        for target in args.targets
        if target in reports
    }
    all_findings = read_jsonl(args.findings)
    selected_findings = [
        row for row in all_findings if normalize_gene_symbol(row.get("gene_target")) in selected_reports
    ]
    selected_findings.sort(key=lambda row: (normalize_gene_symbol(row.get("gene_target")), str(row.get("doc_id"))))

    openie_by_passage = load_openie_by_passage(args.openie_json)
    nodes, rels, candidates, normalized_findings, extraction_requests, diagnostics = build_graph(
        selected_findings,
        selected_reports,
        openie_by_passage,
        args.llm_entities,
    )
    summary = summarize(nodes, rels, normalized_findings, selected_findings, selected_reports, diagnostics, args)

    write_jsonl(args.out / "aligned_findings.jsonl", selected_findings)
    write_jsonl(args.out / "parsed_reports.jsonl", selected_reports.values())
    write_jsonl(args.out / "candidate_entities.jsonl", candidates)
    write_jsonl(args.out / "entity_extraction_requests.jsonl", extraction_requests)
    write_jsonl(args.out / "normalized_findings.jsonl", normalized_findings)
    write_nodes_csv(args.out / "nodes.csv", nodes)
    write_relationships_csv(args.out / "relationships.csv", rels)
    write_neo4j_load_cypher(args.out / "neo4j_load.cypher", [rel.rel_type for rel in rels])
    write_query_tests(args.out / "query_tests.cypher")
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_readme(args.out / "README.md", args, summary)

    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["dangling_relationships"]:
        raise SystemExit("dangling relationships detected")


if __name__ == "__main__":
    main()
