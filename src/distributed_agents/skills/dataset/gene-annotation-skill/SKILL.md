---
name: gene-annotation-skill
description: Provide deterministic gene-to-set membership over the PerturbAI closed gene universe. Use for curated expected-similar groups such as paralog families, complexes, pathways, and functional classes; compare those priors with observed findings for divergence, non-interchangeability, specificity, or deterministic attribute lookup.
---

## Gene-annotation skill

The **deterministic prior-group provider.** It answers "what genes are canonically
expected to behave alike" from curated sources (GO, Reactome, KEGG, MSigDB hallmark/
WikiPathways/BioCarta, CORUM complexes, functional classes), scoped to this screen's
closed gene universe (18,023 real genes: perturbation targets + measured readout).

Why it matters: **divergence, non-interchangeability, and specificity are only
meaningful relative to a prior group** — "these members didn't converge" matters only
if they were *expected* to. Get that expected-similar set here, deterministically,
rather than guessing from symbol stems, then feed it to the graph (`biokg_cypher.py
--param family='[...]'`) or the parquet as `$family` / a candidate set. It is a
**reference** layer (what is canonically true), complementary to the selected
release's observed-findings and optional graph roles, which say what actually happened.

## Access point

`scripts/query_gene_annotations.py` runs in the documented `minimal` environment.
It reads gene flags and curated memberships from the `gene_analog_index` artifact
in the installed corpus manifest. Shi holdout uses the same Shi annotation index
as a dataset reference; the runtime mounts only that index from Shi. These are
curated priors, not report contents or observed responses.

Query/chat resolve and pass the data path automatically. For direct use from the
checkout, run the examples with `pixi run -e minimal python` (or activate that
environment first). Separately installed capsules are discovered through
`DISTRIBUTED_AGENTS_CORPUS_RELEASE_ROOTS`.

```bash
Q=src/distributed_agents/skills/dataset/gene-annotation-skill/scripts/query_gene_annotations.py
python $Q resources                                    # orient: resources + #sets/#genes
python $Q search   --term proteasome --resource CORUM  # names are messy — find the set first
python $Q genes-in --set-id mmu03050 --resource kegg --targets-only --json
python $Q sets-for --gene Ctnnb1 --resource MSigDB:CP:WIKIPATHWAYS
```

Resources present (from `resources`): GO:BP, GO:CC, GO:MF, reactome, kegg,
MSigDB:CP:WIKIPATHWAYS, MSigDB:MH, functional_class, MSigDB:CP:BIOCARTA, CORUM,
and CORUM:human_ortholog_1to1 (human complexes mapped to mouse orthologs).

## Modes

- `resources` — list resources with set/row/gene counts (orientation).
- `search --term <str> [--resource R]` — discover matching set names/ids + member counts.
  **Names are messy; always `search` for the exact set before `genes-in`.**
- `genes-in --set <query> | --set-id <id> [--resource R] [--union]` — the **parameter
  provider**: set → member genes. `--json` prints a JSON array to stdout (the count line
  goes to stderr) ready for `biokg_cypher.py --param family="$FAM"`. `--targets-only`
  intersects with the full screen's biological perturbation targets, excluding
  controls (not just targets with reports in the selected corpus);
  `--measured-only` with readout genes. An ambiguous `--set` lists candidates so you pick
  an exact `--set-id`, unless you pass `--union` to merge across all matching sets.
- `sets-for --gene <symbol>` — gene → its set memberships (repeatable `--gene`).

Functional classes are the deterministic **attribute-set access mode**:
`genes-in --set transcription_factor --resource functional_class --targets-only` = the
398 TF targets — no LLM, no retrieval.

## Composition (prior group → graph), the whole point

```bash
Q=src/distributed_agents/skills/dataset/gene-annotation-skill/scripts/query_gene_annotations.py
python -m distributed_agents.cli corpus entrypoint graph query
FAM=$(python $Q genes-in --set proteasome --resource CORUM --union --targets-only --json 2>/dev/null)
# If the selected release declares that role, run the printed graph entrypoint
# with the release-specific query and pass FAM as its family parameter.
# canonical proteasome subunits -> the perturbed members -> do they phenocopy in the graph?
```

Then decide divergence/specificity by **reading the reports** for the members that stand
apart (the selected release's ledger reader) and by the **signed effects in the DE parquet** — the
annotation store gives the *expected* group; the observed lanes give what actually happened.

## Notes

- Override the data location with `--store-dir` or `DISTRIBUTED_AGENTS_GENE_STORE`.
  Both accept a SQLite annotation index or a legacy directory containing
  `genes.parquet` (gene flags) and `gene_membership.parquet` (`gene`, `resource`,
  `set_id`, `set_name`). The CLI option takes precedence over the environment.
  Explicit missing stores report an error; they do not silently select other data.
- A standalone Shi holdout installation also needs the Shi annotation capsule or
  an explicit store override for this skill.
- This layer is context-invariant curated membership, not a measurement — never read a
  membership as an observed effect. It selects *who to compare*; the observed lanes decide
  *what happened*.
