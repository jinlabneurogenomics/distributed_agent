# Shi BioKG projection

This directory contains the Shi graph builders, host commands, query tools, and
runtime data.

```text
projections/biokg/
  build/       graph construction
  host/        Neo4j and Apptainer lifecycle
  tooling/     offline and Neo4j-backed queries
  data/        graph, base, Claim, and normalization artifacts
  _work/       ignored mutable build and service state
```

`paths.py` defines all projection-owned paths. Mutable state defaults to
`_work/`; set `BIOKG_WORK_ROOT` to place it elsewhere.

Run the managed Neo4j service with:

```bash
python -m distributed_agents.corpus.launch biokg.host pull
python -m distributed_agents.corpus.launch biokg.host restore
python -m distributed_agents.corpus.launch biokg.host up
python -m distributed_agents.corpus.launch biokg.host list
python -m distributed_agents.corpus.launch biokg.host logs
python -m distributed_agents.corpus.launch biokg.host down
```

Inspect the query interface with:

```bash
python -m distributed_agents.corpus.launch biokg.tooling.biokg_cypher --help
```

The runtime graph contains 79,033 nodes and 324,032 relationships, including
15 Programs, 5,107 Claims, 11,237 Finding-to-Claim relationships, and 4,243
Claim-to-Claim relationships. Exact artifact counts and checksums are recorded
under `data/`.

