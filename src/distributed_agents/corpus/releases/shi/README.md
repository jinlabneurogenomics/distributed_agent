# Shi corpus

Shi is a 2,046-target report corpus with structured Finding, Evidence, and
Reference ledgers. It includes deterministic BM25 retrieval, a Claim and target
relationship layer, target-analog lookup, and a BioKG projection.

Inspect and validate the release from the repository root:

```bash
python -m distributed_agents.corpus describe --release shi
python -m distributed_agents.corpus doctor --release shi
python -m distributed_agents.corpus path reports --release shi
python -m distributed_agents.corpus entrypoint ledger query --release shi
```

The read-only MCP surface provides corpus description, calibration, counts,
exact ledger lookup, evidence resolution, lexical Finding search, Claim lookup,
target relationships, target-set inspection, and target-analog suggestions.
These operations use manifest-declared local artifacts and do not require
Neo4j. The graph skill provides offline and Neo4j-backed BioKG queries.

See `build/README.md` for build commands and
`projections/biokg/README.md` for graph usage.

