#!/usr/bin/env python3
"""Export BioKG v2 as LLM-readable context without doing graph reasoning."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from ..paths import GRAPH_WORK_DIR


DEFAULT_GRAPH_DIR = GRAPH_WORK_DIR


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def labels(node: dict[str, str]) -> list[str]:
    return [label for label in node.get("labels", "").split(";") if label]


def compact_props(node: dict[str, str], keys: list[str]) -> dict[str, str]:
    return {key: node[key] for key in keys if node.get(key)}


def linked_nodes(
    finding_id: str,
    rel_type: str,
    outgoing: dict[str, list[dict[str, str]]],
    nodes: dict[str, dict[str, str]],
) -> list[dict]:
    rows = []
    for rel in outgoing.get(finding_id, []):
        if rel["type"] != rel_type:
            continue
        node = nodes[rel["end_id"]]
        rows.append(
            {
                "relation": rel_type,
                "role": rel.get("role", ""),
                "direction": rel.get("direction", ""),
                "effect_status": rel.get("effect_status", ""),
                "evidence_span": rel.get("evidence", ""),
                "node": {
                    "id": node["id"],
                    "kind": node.get("kind", ""),
                    "labels": labels(node),
                    "name": node.get("name", ""),
                    **compact_props(
                        node,
                        [
                            "symbol",
                            "cell_type",
                            "other_type",
                            "description",
                            "statistics",
                            "citation",
                            "url",
                            "source",
                            "source_type",
                            "summary",
                            "literature_status",
                            "confidence",
                            "text",
                        ],
                    ),
                },
            }
        )
    rows.sort(key=lambda row: (row["node"].get("kind", ""), row["node"].get("name", ""), row["role"]))
    return rows


def build_context(graph_dir: Path) -> dict:
    nodes = {row["id"]: row for row in read_csv(graph_dir / "nodes.csv")}
    rels = read_csv(graph_dir / "relationships.csv")
    outgoing: dict[str, list[dict[str, str]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, str]]] = defaultdict(list)
    for rel in rels:
        outgoing[rel["start_id"]].append(rel)
        incoming[rel["end_id"]].append(rel)

    target_nodes = sorted(
        [node for node in nodes.values() if "TargetGene" in labels(node)],
        key=lambda node: node.get("symbol") or node.get("name", ""),
    )
    targets = []
    for target in target_nodes:
        target_findings = []
        for rel in sorted(outgoing[target["id"]], key=lambda item: item.get("end_id", "")):
            if rel["type"] != "HAS_FINDING":
                continue
            finding = nodes[rel["end_id"]]
            neighborhood = {
                "genes": linked_nodes(finding["id"], "AFFECTS_GENE", outgoing, nodes),
                "comparators": linked_nodes(finding["id"], "COMPARES_TO", outgoing, nodes),
                "cell_types": linked_nodes(finding["id"], "OBSERVED_IN", outgoing, nodes),
                "concepts": linked_nodes(finding["id"], "IMPLICATES", outgoing, nodes),
                "evidence": linked_nodes(finding["id"], "SUPPORTED_BY", outgoing, nodes),
                "references": linked_nodes(finding["id"], "CITES", outgoing, nodes),
                "literature_comparisons": linked_nodes(finding["id"], "HAS_LITERATURE_COMPARISON", outgoing, nodes),
            }
            target_findings.append(
                {
                    "id": finding["id"],
                    "doc_id": finding.get("doc_id", ""),
                    "finding_id": finding.get("finding_id", ""),
                    "finding_type": finding.get("finding_type", ""),
                    "direction": finding.get("direction", ""),
                    "confidence": finding.get("confidence", ""),
                    "literature_status": finding.get("literature_status", ""),
                    "summary": finding.get("summary", ""),
                    "why_it_matters": finding.get("why_it_matters", ""),
                    "main_caveats": finding.get("main_caveats", ""),
                    "statement": finding.get("text", ""),
                    "neighborhood": neighborhood,
                }
            )
        targets.append(
            {
                "target": target.get("symbol") or target.get("name", ""),
                "node_id": target["id"],
                "finding_count": len(target_findings),
                "findings": target_findings,
            }
        )

    return {
        "graph_dir": str(graph_dir),
        "counts": {
            "nodes": len(nodes),
            "relationships": len(rels),
            "node_kinds": dict(sorted(Counter(node.get("kind", "") for node in nodes.values()).items())),
            "relationship_types": dict(sorted(Counter(rel["type"] for rel in rels).items())),
        },
        "instructions": {
            "intended_use": "Provide this context to an LLM for targeted or broad biological graph reasoning.",
            "reasoning_rules": [
                "Treat Finding nodes as the evidence-bearing claim units.",
                "Use Evidence and Reference nodes for support; cite finding/evidence/reference IDs in answers.",
                "Do not infer a shared module from target names alone; require shared linked concepts, genes, cell types, or evidence patterns.",
                "Treat Pathway nodes as the folded mechanism category for named pathways and GO-like biological processes.",
                "Distinguish source-derived mechanisms from phrase-rule concepts.",
            ],
        },
        "targets": targets,
    }


def write_prompt(path: Path, context_path: Path) -> None:
    path.write_text(
        f"""# BioKG v2 LLM Reasoning Prompt

You are given a finding-centered biological knowledge graph serialized as JSON:

`{context_path}`

Use the graph structure as evidence. Findings are the central claim units; each
finding links to genes, cell types, concepts, evidence records, references,
caveats, and literature comparisons.

When answering:

- Cite `doc_id` / `finding_id` and supporting `evidence_id` or `ref_id` values.
- For broad questions, look for repeated linked concepts, genes, cell types,
  directions, and evidence patterns across targets.
- Treat `Pathway` as the folded category for pathways, mechanisms, and GO-like
  biological processes.
- Do not assume convergence from target names alone.
- Separate strong source-backed patterns from weak phrase-rule concepts.
- State when the graph lacks enough evidence.
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph-dir", type=Path, default=DEFAULT_GRAPH_DIR)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_GRAPH_DIR / "llm_graph_context.json")
    parser.add_argument("--out-prompt", type=Path, default=DEFAULT_GRAPH_DIR / "llm_reasoning_prompt.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    context = build_context(args.graph_dir)
    args.out_json.write_text(json.dumps(context, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    write_prompt(args.out_prompt, args.out_json)
    print(json.dumps(context["counts"], indent=2, sort_keys=True))
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_prompt}")


if __name__ == "__main__":
    main()
