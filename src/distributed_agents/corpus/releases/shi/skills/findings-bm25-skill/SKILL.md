---
name: findings-bm25-skill
description: Retrieve relevance-ranked Shi Findings with deterministic BM25 over each canonical Finding's summary and why-it-matters text. Use for concept-first or paraphrased corpus discovery before resolving the returned Finding evidence and references; do not treat retrieval score as biological evidence or a final rank.
---

# Findings BM25

Use this skill when the task names a biological concept, mechanism, phenotype,
or paraphrase but does not supply exact target genes. It searches the canonical
Shi Findings directly. No HippoRAG rewrite, embedding model, dense vector, or
LLM build step is involved.

The index contains exactly two searchable fields per Finding:

- summary
- why_it_matters

Target symbols, Finding types, confidence labels, cell types, genes, evidence,
references, directions, and caveats are not indexed. Returned metadata includes
the target-scoped Finding ID plus its evidence_ids and ref_ids so material hits
can be grounded with resolve_evidence from findings-ledger-skill.

Run from this skill directory:

    python scripts/findings_bm25.py search \
      --query "proteasome subunit convergent phenotype" \
      --query "shared proteostasis response neuronal state" \
      --level target --top-k 20 --pretty

    python scripts/findings_bm25.py verify

Multiple query values are searched independently and fused with reciprocal rank
fusion. Prefer two or three focused formulations over one long question. Use
level=finding to retain separate Finding hits and level=target to collapse them
to perturbation targets. Finding type is an optional metadata filter; it is not
indexed text.

If the user's wording contains a likely typo, submit a focused formulation with
the canonical spelling rather than carrying the typo into every query. This is
visible agent-side reformulation, not hidden automatic concept coverage or
spell correction. Preserve uncertain alternatives as separate queries.

Fast path for a basic corpus question:

1. Make one target-level search with two or three focused formulations and a
   limit of 8-12.
2. Use the returned cards to identify the shared pattern and counterexamples.
3. Resolve evidence for at most three representative Findings that establish
   the conclusion, adding another only for a material conflict.
4. Answer. Do not repeat the search at both Finding and target level or call
   inventory/count/describe when the question does not require enumeration or
   vocabulary calibration.

Interpretation rules:

- BM25/RRF orders reading. It does not measure phenotype strength, convergence,
  confidence, novelty, or causal importance.
- Read the returned summaries, then resolve Evidence and References for the
  Findings that support a material answer.
- Use exact ledger queries for known targets, controlled fields, exhaustive
  counts, and absence claims.
- A missed term or empty result is a retrieval gap, not biological evidence.
- Evidence/reference prose and full report narratives deliberately remain
  second-hop sources. They are not duplicated into this index.

The deterministic build command reads the release-owned canonical Findings CSV
and writes the SQLite FTS5 index. Runtime verification binds the index to the
source Findings SHA-256, record count, indexed-field declaration, tokenizer, and
index schema version.
