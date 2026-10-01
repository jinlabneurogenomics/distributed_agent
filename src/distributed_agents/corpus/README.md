# DistributedAgents corpus releases

DistributedAgents discovers self-contained corpus releases through `release.json`
manifests. This checkout includes two releases:

- `shi`: the default 2,046-target corpus.
- `shi_holdout`: a 1,773-target holdout corpus.

Select a release with `--release`, `DISTRIBUTED_AGENTS_CORPUS_RELEASE`, or the configured
default, in that order. Set `DISTRIBUTED_AGENTS_CORPUS_RELEASE_ROOTS` to a
platform-path-separated list of directories containing release subdirectories.
When it is unset, a source checkout uses `src/distributed_agents/corpus/releases`.

```bash
python -m distributed_agents.corpus list
python -m distributed_agents.corpus describe --release shi
python -m distributed_agents.corpus doctor --release shi
python -m distributed_agents.corpus path reports --release shi
python -m distributed_agents.corpus entrypoint ledger query --release shi
```

Each release owns its artifacts, schemas, skills, tooling, and optional graph
projection. The read-only corpus MCP server exposes only operations supported by
the selected release and the active capability policy. Exact ledger queries and
Claim/Finding operations read frozen local artifacts; graph queries additionally
require a configured Neo4j service.

Release payloads are not included in the DistributedAgents wheel or source distribution.
