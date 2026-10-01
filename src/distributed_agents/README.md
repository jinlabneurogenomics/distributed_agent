# DistributedAgents

DistributedAgents has four runtime command surfaces:

1. `distributed_agents query` performs open-ended dataset research. The Codex executable
   is the default backend; `--backend api` selects the direct OpenAI Agents SDK
   backend. Both use the same adaptive/direct contracts and normalized result.
2. `distributed_agents chat` provides a persistent terminal session over that same
   adaptive runtime while retaining the Codex allowlist sandbox.
3. `distributed_agents build` generates the first-stage source reports used to construct
   corpora through the OpenAI Agents SDK.
4. `distributed_agents corpus` inspects and validates separately installed corpus
   releases.

The default installation supports the Codex query/chat path and corpus
inspection. Install `distributed_agents[api]` for the direct query backend,
`distributed_agents[build]` for corpus authoring, and `distributed_agents[analysis]` when host-side
Parquet inspection is required.

## Query modes

| Mode | Status | Purpose |
|---|---|---|
| `adaptive` | supported default | Host-prepared coverage and capabilities followed by one proportional evidence loop, with skill-gated bounded readers for exhaustive semantic sweeps |
| `direct` | diagnostic | Single-context control without adaptive coverage |

## Code map

- `cli/`: thin command registration and one module per subcommand.
- `query/`: backend-neutral request/result models, contracts, adaptive context,
  input binding, measurement metadata, and backend dispatch.
- `query/backends/codex.py`: default Codex executable backend, including its
  access plan, preflight, event normalization, and run manifest.
- `query/backends/api.py`: direct OpenAI Agents SDK backend using the same query
  modes and artifact contract.
- `build/`: first-stage source-report generation for corpus construction.
- `chat/`: Codex-only persistent sessions, startup canary, and trace archival.
- `runtime/`: shared sandbox, Agents SDK shell, Codex process, and path helpers.
- `skills/registry.py`: role-aware skill discovery and run-local skill indexes.
- `corpus/registry.py`: release discovery, selection, and integrity checks.
- `corpus/mcp/`: read-only MCP service for a selected release; the adjacent
  `mcp_server.py` is a thin executable entrypoint.
- `query/prompts/`: adaptive/direct runtime contracts and the adaptive
  scientific policy.
- `skills/runtime/`: shared adaptive-query, dataset-orchestration, and
  exhaustive-corpus-sweep capabilities.
- `skills/dataset/`: capabilities owned by the underlying experimental dataset.
- `corpus/registry.py`: explicit selection of separately installed corpus
  releases and the manifest-derived runtime closure of artifacts, schemas,
  projections, tooling, and release-owned skills.
- `<installed-release>/skills/`: corpus-specific evidence capabilities selected
  through the release manifest.
- A selected release's optional `relational_candidates.predictive_review`
  entrypoint:
  absent-endpoint prediction support that unions a calibrated quantitative
  top-k with complete directed comparator-multiplicity tiers. It emits
  identities, multiplicity, visible anchors, and quantitative-overlap metadata—not
  Finding prose—requires dispositions for graph-only challengers, and finalizes
  exact review telemetry after the answer is frozen.
- `skills/life-sciences/`: vendored external biomedical source capabilities.
- A selected release's `ledger.calibration` entrypoint: bounded
  field-description, calibration, canonical count, and inventory operations
  backed by versioned calibration artifacts. Claim-aware operations exist only
  when the selected release declares an aligned Claim layer. These are
  release-maintenance CLI operations; the agent-facing MCP consolidates them
  into `describe`, `calibrate`, `count`, release-appropriate Claim lookup, and
  exact retrieval tools. Shi additionally exposes its Claim layer through
  `query_claims`, `related_targets`,
  and `inspect_target_set`; these keep shared Claim membership, typed Claim
  relations, and directional Finding references in separate lanes.
  `related_targets` retains one-anchor direct lookup and also supports an
  equal-source random walk with restart over one to twenty targets. Its
  stationary probability is graph reachability, not biological rank.
  `suggest_target_analogs` is a separate Shi-only lane for requested mouse genes
  absent from the corpus: it intersects frozen CORUM, pathway, GO/functional,
  and STRING physical evidence with an explicit eligible universe (or the Shi
  target set by default), preserving typed evidence without predicting an
  outcome or computing an aggregate similarity score. The Shi holdout
  release's semantic layer contains frozen higher-order bottom-up Claims with
  typed Finding contributions. Its one-Finding relation rows are structural
  review mechanics and are not used by the Claim/Finding MCP tools.

## Build a source report

`distributed_agents build` has one report contract: the hash-verified
`build/prompts/findings_report.md` task plus
`build/prompts/base_scientist_contract.md`. The public CLI uses this fixed pair
and does not accept arbitrary task files.

```bash
pixi run distributed_agents build BDNF \
  --parquet-path path/to/screen.parquet \
  --out-dir results/distributed_agents/build
```

The run validates the six ordered Structured Appendix JSONL ledgers against the
packaged schema and cross-ledger grounding rules. A passing run writes
`report.md`, normalized `structured_appendix.json`, `run.json`, and its tool log
under the target directory. Appendix validation fails closed while preserving
the report and diagnostics. The manifest records the model, usage, exact prompt
IDs and hashes, and the appendix schema ID and hash.

Corpus builders can normalize a complete perturbation universe with
`python -m distributed_agents.build.normalization --help` or the corresponding
`distributed_agents.build.normalization` Python API. The mapper consumes a caller-owned
MGI 6.24 `MRK_List1.rpt.gz`, records its exact SHA-256, and emits explicit
official-symbol, withdrawn-symbol, synonym, ambiguous, and unmapped outcomes.
It never downloads MGI's mutable weekly report implicitly.

Publication references use one common exact-identifier implementation but are
normalized independently inside each release. Run
`python -m distributed_agents.build.reference_normalization --help` against a release
root to produce its source-linked DOI/PMID/PMCID mapping ledger. The mapper
verifies the release manifest and reference-ledger hash, performs no network or
fuzzy-title resolution, retains conflicts and unresolved rows explicitly, and
never rewrites the immutable source references. Policy v2 also recognizes
exact Europe PMC MED/PMC locators, excludes named regulatory and search-page
URLs from publication identity, and records an audited selection when one
exact DOI URL disambiguates a multi-DOI source row.

## Run a query

```bash
pixi run distributed_agents query \
  --task-file path/to/task.md \
  --out-dir results/distributed_agents/my-run
```

For a versioned ledger and exact task inputs:

```bash
pixi run distributed_agents query \
  --corpus-release shi_holdout \
  --task-file path/to/task.md \
  --codex-input-root path/to/training.parquet \
  --codex-input-root path/to/targets.csv \
  --out-dir results/distributed_agents/july-run
```

ChatGPT Codex authentication is the default. Codex can itself use API-key auth:

```bash
pixi run distributed_agents query \
  --codex-auth apikey \
  --task-file path/to/task.md \
  --out-dir results/distributed_agents/codex-api-key-run
```

The separate direct API backend uses the OpenAI Agents SDK and `OPENAI_API_KEY`:

```bash
pixi run distributed_agents query \
  --backend api \
  --task-file path/to/task.md \
  --api-input-root path/to/training.parquet \
  --out-dir results/distributed_agents/direct-api-run
```

Every run must have a durable output directory. See
`/docs/codex-query-backend.md` for isolation and artifact details.

Corpus releases are data/runtime capsules installed separately from the public
DistributedAgents code distribution. Selecting `--corpus-release` never downloads a
release implicitly; use `distributed_agents corpus list` and `distributed_agents corpus doctor`
to inspect the releases available to the local registry.

## Open a sandboxed chat

Chat uses no broad default task-data mount. Packaged DistributedAgents capabilities are
available, and additional task inputs must be declared exactly:

```bash
pixi run distributed_agents chat \
  --corpus-release shi_holdout \
  --out-dir results/distributed_agents/chat-debug \
  --codex-input-root path/to/findings.jsonl
```

Reopening the same command and output directory resumes the active session.
Use `/new` for an uncontaminated thread, `/cold QUESTION` for a one-turn
cold-start probe, and `/trace` to inspect the active thread and archived turn.
The startup canary fails closed if repository source, agent instructions,
graders, debug outputs, or other forbidden surfaces are visible.

## Evaluation

The source-checkout BioEval runner can execute the same caller-owned task through
DistributedAgents, direct Codex, Claude Code, and Biomni. Start with
`pixi run bioeval run`; the supported task contract and output layout are in
[`src/bioeval/README.md`](../bioeval/README.md).
