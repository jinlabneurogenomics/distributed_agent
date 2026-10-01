# Shi holdout BioKG projection

The projection contains:

- 1,773 `TargetGene` nodes;
- 309 comparator-only `Gene` nodes;
- 8,718 `Finding` nodes;
- 45,640 `Evidence` nodes;
- 13,974 `Reference` nodes;
- 555 `Claim` nodes.

`data/base/relationships.jsonl` contains:

- 8,718 `HAS_FINDING` relationships;
- 8,718 `HAS_TARGET` relationships;
- 28,954 `REPORTS_GENE` relationships;
- 48,871 `SUPPORTED_BY` relationships;
- 18,229 `CITES` relationships;
- 2,234 `EXPRESSES_CLAIM` relationships.

Build, validate, and query the graph from this directory:

```bash
python build/build_nodes.py
python build/build_relationships.py
python host/load_neo4j.py --dry-run
python host/load_neo4j.py --uri bolt://127.0.0.1:7687
python tooling/biokg_cypher.py --schema --format json
```

The loader validates node and relationship files before writing to Neo4j. The
query wrapper is read-only and requires a final numeric `LIMIT` of at most 50
for caller-supplied Cypher.

