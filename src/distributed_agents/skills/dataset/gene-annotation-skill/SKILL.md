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

`scripts/query_gene_annotations.py` — stdlib + pandas (no special env needed). Parquet-
backed by two bundled tables under `scripts/out/`:
- `genes.parquet` (DIMENSION: one row per gene, scalar flags — is_perturbation_target,
  is_measured, is_control_target, type_of_gene, entrez/ensembl IDs).
- `gene_membership.parquet` (FACT: `gene, resource, set_id, set_name`, many-to-many).

```bash
Q=src/distributed_agents/skills/dataset/gene-annotation-skill/scripts/query_gene_annotations.py
python $Q resources                                    # orient: resources + #sets/#genes
python $Q search   --term proteasome --resource CORUM  # names are messy — find the set first
python $Q genes-in --set-id mmu03050 --resource kegg --targets-only --json
python $Q sets-for --gene Ctnnb1 --resource MSigDB:CP:WIKIPATHWAYS
```

Resources present (from `resources`): GO:BP, GO:CC, GO:MF, reactome, kegg,
MSigDB:CP:WIKIPATHWAYS, MSigDB:MH, functional_class, MSigDB:CP:BIOCARTA, CORUM.

## Modes

- `resources` — list resources with set/row/gene counts (orientation).
- `search --term <str> [--resource R]` — discover matching set names/ids + member counts.
  **Names are messy; always `search` for the exact set before `genes-in`.**
- `genes-in --set <query> | --set-id <id> [--resource R] [--union]` — the **parameter
  provider**: set → member genes. `--json` prints a JSON array to stdout (the count line
  goes to stderr) ready for `biokg_cypher.py --param family="$FAM"`. `--targets-only`
  intersects with perturbation targets (so you get only members this screen perturbed);
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

- Override the data location with `--store-dir` or `DISTRIBUTED_AGENTS_GENE_STORE` if needed; the
  default resolves to the bundled `scripts/out/`.
- This layer is context-invariant curated membership, not a measurement — never read a
  membership as an observed effect. It selects *who to compare*; the observed lanes decide
  *what happened*.
