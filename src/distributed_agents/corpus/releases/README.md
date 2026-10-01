# Corpus releases

Each directory is a self-contained corpus capsule selected by its `release_id`.
A capsule contains a `release.json` manifest plus its data artifacts, schemas,
skills, tooling, and optional projections.

Available releases:

- `shi`
- `shi_holdout`

Validate or inspect a capsule from the repository root:

```bash
python -m distributed_agents.corpus list
python -m distributed_agents.corpus describe --release shi
python -m distributed_agents.corpus doctor --release shi
```

Release payloads remain outside built Python distributions.
