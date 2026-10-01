# Shi holdout tooling

These release-local commands read only artifacts within the Shi holdout capsule
by default:

- `read_reports.py`: bounded report access.
- `query_ledger.py`: exact filters and counts for the six JSONL ledgers.
- `resolve_evidence.py`: Finding-scoped Evidence and Reference lookup.

Higher-level entrypoints live with their release-owned skills:

- `skills/findings-ledger-skill/scripts/query_corpus.py`: calibration and Claim queries.
- `skills/relational-candidate-skill/scripts/relational_candidates.py`: target relationships.
- `skills/relational-candidate-skill/scripts/direct_evidence.py`: bounded Finding details.
- `skills/relational-candidate-skill/scripts/predictive_graph_review.py`: graph review.
- `skills/biokg-recall-skill/scripts/biokg_cypher.py`: bounded read-only Cypher.

