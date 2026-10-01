# Shi holdout corpus

Shi holdout is a 1,773-target report corpus with six structured ledgers, a
bottom-up Claim layer, comparator relationships, exact-access tooling, and a
BioKG projection.

Inspect and validate the release from the repository root:

```bash
python -m distributed_agents.corpus describe --release shi_holdout
python -m distributed_agents.corpus doctor --release shi_holdout
python -m distributed_agents.corpus path reports --release shi_holdout
python -m distributed_agents.corpus entrypoint ledger query --release shi_holdout
```

Release-local commands can query the ledgers and build graph files:

```bash
python tooling/query_ledger.py findings --gene Cplx1 --json
python skills/findings-ledger-skill/scripts/query_corpus.py calibrate summary
python projections/biokg/build/build_nodes.py --output-dir /tmp/shi-holdout-biokg
python projections/biokg/build/build_relationships.py \
  --nodes /tmp/shi-holdout-biokg/nodes.jsonl \
  --output-dir /tmp/shi-holdout-biokg
python projections/biokg/host/load_neo4j.py --dry-run
```

The read-only MCP surface provides corpus description, calibration, counts,
ledger and evidence access, Claim/Finding lookup, target context and comparison,
related-target discovery, and optional graph queries.

