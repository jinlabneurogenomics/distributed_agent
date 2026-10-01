---
name: biokg-recall-skill
description: Run bounded read-only Cypher over the Shi holdout ledger graph. Use for exact target-to-Finding-to-comparator traversal and source evidence; do not infer semantic convergence, effect magnitude, or candidate rank from relationship presence alone.
---

# Shi Holdout BioKG Recall

The Shi holdout graph is a source-preserving ledger projection with six serialized
node types and six relationship types. Write bounded task-specific Cypher
through `scripts/biokg_cypher.py`; writes are rejected and every caller query
must use `LIMIT <= 50` as its final clause.

```bash
python scripts/biokg_cypher.py --schema
python scripts/biokg_cypher.py --format json --query \
  "MATCH (t:TargetGene)-[:HAS_FINDING]->(f:Finding) WHERE t.symbol = 'Cplx1' RETURN f.doc_id, f.summary LIMIT 10"
python scripts/biokg_cypher.py --format json --query \
  "MATCH (a:TargetGene)-[:HAS_FINDING]->(f:Finding)-[:REPORTS_GENE {role:'finding_reported_comparator'}]->(b:TargetGene) WHERE a.symbol = 'Cplx1' RETURN f.doc_id, b.symbol LIMIT 50"
```

Schema:

- `TargetGene` (1,773): `id`, `symbol`, and `source_artifact`. Every target also
  has the `Gene` label.
- Comparator-only `Gene` (309): canonicalized symbols that are not report
  targets. The `Gene` label therefore matches 2,082 nodes in total.
- `Finding` (8,718): the complete canonical Shi holdout Finding row as properties.
- `Evidence` (45,640): the complete target-scoped Evidence row.
- `Reference` (13,974): the complete target-scoped Reference row.
- `Claim` (555): a frozen higher-order proposition induced bottom-up from at
  least two perturbation-centered Findings.
- `TargetGene -[:HAS_FINDING]-> Finding` and
  `Finding -[:HAS_TARGET]-> TargetGene`.
- `Finding -[:REPORTS_GENE {role:'finding_reported_comparator'}]-> Gene`
  (28,954). When the comparator is a represented perturbation, the endpoint is
  also a `TargetGene`.
- `Finding -[:SUPPORTED_BY]-> Evidence` and
  `Finding -[:CITES]-> Reference`.
- `Finding -[:EXPRESSES_CLAIM {role, rationale}]-> Claim` (2,234), where role
  is `ANCHORS`, `SUPPORTS`, `QUALIFIES`, or `CONTRASTS`.

`REPORTS_GENE` means only that the canonical Finding explicitly names that
comparator. It does not assert agreement, phenotypic similarity, effect
direction, transfer, or causality. Claim edges preserve adjudicated contribution
roles but do not imply effect magnitude. There are no pathway/concept, Program,
CellType, or LiteratureComparison nodes in this projection. Relationship counts
measure source linkage, not independent biological support. Use the raw
experimental table for effect sizes, signs, significance, or candidate ordering.
