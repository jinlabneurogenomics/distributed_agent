# Shi tooling

These release-local commands read only artifacts within the Shi capsule by
default:

- `read_reports.py`: bounded report access.
- `query_findings.py`: exact Finding filters and counts.
- `resolve_evidence.py`: Finding-scoped Evidence and Reference lookup.

Higher-level entrypoints live with their release-owned skills:

- `skills/findings-bm25-skill/scripts/findings_bm25.py`: BM25 Finding search.
- `skills/findings-ledger-skill/scripts/query_corpus.py`: calibration and Claim queries.
- `skills/relational-candidate-skill/scripts/relational_candidates.py`: target relationships.
- `skills/biokg-recall-skill/scripts/query_biokg.py`: offline BioKG queries.
- `skills/biokg-recall-skill/scripts/biokg_cypher.py`: bounded read-only Cypher.

