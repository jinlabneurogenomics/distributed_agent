---
name: biokg-recall-skill
description: Plan and run flexible Cypher retrieval over the BioKG Neo4j graph of PerturbAI narrative findings. Use for structured graph recall such as convergence across target families, divergence within a family or complex, dominant pathways, cell-type landscapes, target-specific evidence, or effect-status-aware support. The reasoning agent writes task-specific Cypher; this skill supplies the schema, precision/recall controls, access, and worked patterns.
---

## BioKG Recall Skill

Use this skill when a question benefits from **graph traversal** over the
PerturbAI finding KG: shared mechanisms across a target family, divergence /
non-interchangeability within a family or complex, dominant pathways/complexes,
cell-type response landscapes, target→finding→entity lookup with source evidence, or
any query where topology and `effect_status` matter.

BioKG is for exact, countable, structured traversal with explicit status
filtering. Use the findings-ledger skill for compact candidate-scoped prose or
field retrieval. Full reports are on-demand forensic evidence.

**You write the Cypher.** There are no fixed query templates. This skill gives
you the schema, the one knob that actually changes answers (`effect_status`), an
access point, and worked patterns. Construct whatever traversal the endpoint
needs.

**The graph is a lossy relational index, not an endpoint measurement or global
ranker.** Canonical Claims preserve focused relationships from the upstream
reports. Use them to narrow attention around a separately justified basis;
interpret the bounded union from compact Claims and Findings. A strong
qualifying or negative relation may be highly relevant attention without
supporting promotion.

## Access Point

`scripts/biokg_cypher.py` runs Cypher over the Neo4j HTTP API. Stdlib-only — no
neo4j driver, no pixi env, runs directly in your shell. Read-only by default
(write clauses are refused unless `--allow-write`).

Use this access point only when `capabilities.json` marks `corpus.graph`
`available: true`; the host has already preflighted the complete dependency
chain. Re-read the live schema before composing a query:

```bash
python src/distributed_agents/corpus/releases/shi/skills/biokg-recall-skill/scripts/biokg_cypher.py --schema
```

If a preflighted call subsequently fails, treat the capability as unavailable
and continue with bounded ledger/context evidence when sufficient. Never start,
load, or manage Neo4j, Apptainer, Pixi, or another backing service from the
model sandbox; service lifecycle belongs to the host.

Run a query inline, from a file, or stdin; choose `--format table|json`:

```bash
python .../biokg_cypher.py -q "MATCH (n:TargetGene) RETURN count(n)"
python .../biokg_cypher.py --file q.cypher --param targets='["Pomp","Psmb4"]'
echo "MATCH (n:CellType) RETURN n.name LIMIT 5" | python .../biokg_cypher.py --format json
```

Connection defaults (override with flags or `BIOKG_NEO4J_*` env vars):
`http://127.0.0.1:7474`, db `neo4j`, auth `neo4j/biokgpassword`.

## Full reports are forensic evidence

`scripts/read_reports.py` reads a bounded candidate set by gene symbol
(stdlib-only; corpus keyed by `gene_target`, field `final_report`). Use it only
when compact Claim/Finding evidence leaves a material conflict, unresolved
caveat, or citation need:

```bash
# Narrow relationally while retaining qualifying and negative Claims.
python .../biokg_cypher.py --format json -q "MATCH (t:TargetGene)-[:HAS_FINDING]->(f:Finding) ... RETURN DISTINCT t.symbol"

# Resolve only the remaining question for material candidates.
python .../read_reports.py Atp6v1e1 Thoc2 Hspa5 \
  --grep "buffered|uncoupled|contradiction" --max-reports 3
```

Override the corpus path with `--reports-path` or `BIOKG_REPORTS_PATH` if
needed; `--list` shows available gene targets.

## Schema

Every node also carries the `BioKGNode` label. Counts are for the current graph
(79,033 nodes / 324,032 relationships).

Seed (deterministic) nodes:

- `TargetGene` (2,046) — perturbed genes. props: `symbol`, `name`.
- `Claim` (5,107) — a retained corpus-wide canonical story kernel.
  One Claim can combine a core observation, corroboration, a directly relevant boundary, and an
  implication from different finding types. Props: `summary`, `relation_family`,
  `direction_pattern`, `evidence_mode`, `support_level`, `cell_scope`,
  `active_default`, `targets`, `readouts`, `confidence`.
- `Finding` (11,343) — report-level source unit.
  props: `finding_id`, `finding_type`, `direction`, `confidence`, `summary`,
  `why_it_matters`, `target_gene`, `main_caveats`, `genes`, `comparators`,
  `evidence_ids`, `ref_ids`.
- `CellType` (166) — e.g. `001 L5-6 IT Glut`. props: `name`.
- `Evidence` (18,602) — props: `description`, `statistics`, `genes`,
  `evidence_slug`, `cell_type`.
- `Reference` (15,797) — canonical publications plus unresolved and non-publication rows.
- `LiteratureComparison` (8,999) — props: `statement`, `literature_status`.
- `Assay` (1) — Perturb-seq context.

`Gene` (9,024 base) — downstream / measured / finding-claimed genes (also `symbol`).
**Genes are now exclusively measurement-anchored** — they come only from the
deterministic source lists (`evidence.genes`, `finding.genes`/`comparators`), NOT
from LLM free-text extraction. (The old LLM gene lane minted drugs/aliases/
cell-type-name tokens as "genes" and produced a wrong convergence ranking; it was
dropped — see `decisions.md` 2026-06-27 lane comparison.)

Non-seed (LLM-extracted) **concept** nodes, props mainly `name`:

- `Pathway` (3,089), `Complex` (590), `Module` (665) — conceptual nodes.
- `Phenotype` (2,177).
- `Other` (3,429) — diseases, drugs/compounds, metabolites, ion channels,
  currents, etc. props include `other_type`.
- **Concept nodes no longer carry `kind`, `concept_type`, `source_kind` or `source`**
  (removed 2026-08-24, TODO P2-7): all four duplicated the node label or were constant, and
  nothing read them. Use the label itself, or `other_type` / `semantic_type` for finer typing.

Relationships:

- `(:TargetGene)-[:HAS_FINDING]->(:Finding)` — the spine.
- `(:Finding)-[:EXPRESSES_CLAIM {role}]->(:Claim)` — compatibility membership.
  Novel Findings may have no Claim, and a Finding may support multiple retained Claims;
  `role` is `anchor|corroborating|boundary|implication|warning`.
- **REMOVED 2026-08-24 (TODO P2-8):** `(:Claim)-[:ABOUT_TARGET]->(:TargetGene)`,
  `(:Claim)-[:HAS_READOUT]->(:Gene)` and `(:Claim)-[:OBSERVED_IN]->(:CellType)` no longer exist.
  All three were reconstructible from `(:Claim)<-[:EXPRESSES_CLAIM]-(:Finding)-[...]->(entity)`
  and carried only verbatim copies of Claim-level fields, so they double-counted in any
  path/shared-neighbour score. Go through the Finding, or read the Claim's own `targets`,
  `readouts` and `cell_scope` properties. Claim-level `de_support_level`/`de_direction` are still
  on the Claim node; retrieve the parquet for exact signed/numeric results.
- Claim-to-Claim `QUALIFIES`, `CONTRASTS_WITH`, `IMPLICATION_OF`, and `REVIEW_WITH` are soft typed
  relations and must never be transitively collapsed.
- `(:Finding)-[:OBSERVED_IN]->(:CellType)`
- `(:Finding)-[:SUPPORTED_BY]->(:Evidence)`
- `(:Finding)-[:CITES]->(:Reference)`
- `(:Finding)-[:HAS_LITERATURE_COMPARISON]->(:LiteratureComparison)`
- `(:Finding)-[:USES_ASSAY]->(:Assay)`, `(:Finding)-[:HAS_TARGET]->(:TargetGene)`
- `(:Evidence)-[:DESCRIBES_CELL_TYPE]->(:CellType)`

**Three gene/concept lanes — pick the right one (this is the central design):**

- **`(:Evidence)-[:MEASURED_GENE]->(:Gene)`** (60,112) — the **measured fact**
  gene lane: every downstream gene that appears in an evidence item's per-gene
  statistics. Reach it from a finding via
  `(:Finding)-[:SUPPORTED_BY]->(:Evidence)-[:MEASURED_GENE]->(:Gene)`. Use it to
  **enumerate which genes a target measurably affected** (candidate generation) and
  for coarse `effect_status` filtering.
  > ⚠️ **Never read `direction`, `logfc`, `pval`, or `fdr` off this edge.** They are
  > parsed from the whole `Evidence.statistics` string, which quotes *comparator*
  > perturbations, so ~78% of (evidence,gene) pairs carry a **foreign, wrong-sign /
  > wrong-magnitude** value borrowed from another target. **The DE parquet is ground
  > truth for every signed number**. `effect_status` is a coarse candidate
  > filter, not a per-gene claim.
- **`(:Finding)-[:REPORTS_GENE {role}]->(:Gene)`** (61,321) — the **finding-claimed**
  gene lane: genes the finding text explicitly names. `role` ∈
  `finding_reported_gene` (42,468) | `finding_reported_comparator` (20,376).
  **Neutral — no `effect_status`** (finding-claimed, not re-measured on the edge).
  Use for "what genes did this finding headline / contrast against".
- **`(:Finding)-[:IMPLICATES]->(concept)`** (15,046) — the **interpretation**
  concept lane to `Pathway`/`Complex`/`Module`/`Phenotype`/`Other`. **Carries
  `effect_status`** (LLM-assigned). Use for concept convergence/dominance.

(Removed: `AFFECTS_GENE` and `COMPARES_TO` — the old LLM gene lane. Genes →
`MEASURED_GENE`/`REPORTS_GENE`; comparator identity → `REPORTS_GENE` with
`role='finding_reported_comparator'`.)

**Program layer (canonical concept rollup + ontology backbone)** — fixes concept
fragmentation (the same program was named dozens of ways: ISR appeared under 37 concept
names, circadian under 24, each with ~1 support):

- `Program` (15: ISR_ATF4, Proteasome, Sterol_SREBP2, BAF_SWISNF, UPR, OXPHOS, Spliceosome,
  mTOR, Wnt_bcatenin, Circadian, Hedgehog, JAK_STAT, NF_kB, Autophagy, MAPK_ERK). props
  `program_id`, `name`, `kind` ∈ regulon|complex|process.
- Concept nodes carry `semantic_type` (LLM-typed for the support≥2 layer) ∈
  `program|phenotype|disease|anatomy_celltype|assay_or_molecule_noise` — filter to
  `semantic_type='program'` (or just use `Program`/`IMPLICATES_PROGRAM`) to exclude the
  phenotype/anatomy/assay/disease noise that pollutes the raw concept layer.
- `(:concept)-[:CANONICAL_PROGRAM]->(:Program)` — rolls fragmented concept nodes up to one node.
- `(:Finding)-[:IMPLICATES_PROGRAM {effect_status}]->(:Program)` — the **curated** finding→program
  link (a program a finding actually flagged = literature-salient / worth-noticing). Use this for
  program-level convergence, status-filterable like `IMPLICATES`.
- `(:Gene)-[:MEMBER_OF {source}]->(:Program)` — ontology backbone (static knowledge; genes a
  finding may report without naming the program).

**Abstraction-lift (query-time, not a stored edge):** a target's findings can implicate a program
*without naming it* — recover via the backbone: `(:TargetGene)-[:HAS_FINDING]->(:Finding)
-[:REPORTS_GENE]->(:Gene)-[:MEMBER_OF]->(:Program)`. This reaches more targets than
`IMPLICATES_PROGRAM` alone (those that reported member genes but didn't name the program).

Program convergence here is **curated** ("how many targets' findings flag program P") — the
worth-noticing subset. For *complete statistical* convergence / per-gene engagement / signature
similarity, that's the **DE parquet** (out of graph by design), not these edges.

Re-confirm with `CALL db.labels()`, `CALL db.relationshipTypes()`,
`CALL db.schema.visualization()` rather than trusting this list blindly.

## The One Knob That Matters: `effect_status`

`effect_status` lives on **two** lanes, with **different vocabularies** — match the
filter to the lane:

- **Genes (`MEASURED_GENE`)** — parsed from per-gene stats. Values:
  `affected 7323` (FDR<0.05), `nominal 6608` (p<1e-3, not FDR-sig),
  `absent_or_not_detected 8642` (FDR≥0.05 / FDR=1.0), `measured 37322` (neutral —
  no per-gene stat to parse, e.g. correlation/aggregate evidence; ~62%). (A
  `direction`/`logfc`/`fdr` is also stored, but it is **contaminated — never read a
  sign or magnitude off `MEASURED_GENE`; use the DE parquet**.)
- **Concepts (`IMPLICATES`)** — LLM-assigned. Values: `uncertain 4879,
  implicated 4674, affected 2268, absent_or_not_detected 2146, buffered 1156,
  compared 288, nominal 247, mixed 216, fdr_insignificant 66, caveated 47`.

`REPORTS_GENE` carries **no** `effect_status` (role only) — it's the finding's
claimed/contrasted gene list, not a measured edge.

A large share of edges are non-positive **by design** — the dataset deliberately
encodes null/buffered/uncertain biology. How you filter IS the precision/recall
decision. Pick deliberately and state which you used:

- **positive** —
  - genes: `m.effect_status IN ['affected','nominal']` (drop `measured` neutral +
    `absent_or_not_detected`). Use `= 'affected'` alone for FDR-strict claims.
  - concepts: `r.effect_status IN ['affected','implicated','buffered']`.
  Use for any **ranking or claim**. (Concept example: under `all`, Hedgehog ranks
  #1 purely from null "pathway tested and did NOT respond" edges; under positive it
  drops and proteasome/spliceosome/mTORC1/OXPHOS/ISR/BAF rise — the expected
  biology. See `src/distributed_agents/corpus/releases/shi/projections/biokg/data/base/DEDUP_NOTES.md`.)
- **non-negative** —
  - genes: `NOT m.effect_status = 'absent_or_not_detected'` (keeps `measured`
    neutral + nominal).
  - concepts: `NOT r.effect_status IN ['absent_or_not_detected','fdr_insignificant']`.
  Use for **discovery** of weak/inferred shared mechanisms to vet, not for claims.
  (`uncertain` can mean "inferred upstream activity" OR "did not phenocopy".)
- **all** = no filter. Conflates tested-but-null with converged. Use only to
  **audit** what was tested.

Default to **positive** for any number you will report. Never present an `all`
ranking as a convergence result. Note for genes: `measured` is *neutral* (the stat
was unparseable), **not** negative — exclude it from positive rankings but don't
read it as "no effect".

**Orthogonal/out-of-schema endpoints:** do not pre-filter to `positive` and do
not rank on convergence counts. Retain buffered, negative, and quiet relations
as attention and uncertainty. Candidate expansion must start from a defensible
ordered basis under the orchestrator's Claim-attention policy; weak or neutral
starting sets do not generate graph-related candidates.

## Divergence Is Encoded, Not Absent

Convergence is a node accumulating edges; **divergence is a typed contrast, not
a missing edge** — and it is the *larger* part of this graph. Finding-type
counts: `cross_perturbation_contrast` 1672, `pathway_uncoupling` 1352,
`cell_type_selectivity` 1469, `negative_result` 2069, `buffered_response` 1398 —
versus `convergent_module` 378. So "X is **not** interchangeable with its
paralogs / complex / pathway" is a first-class, abundant result here, not an
extraction failure.

A convergence query **cannot** surface divergence: low neighbor overlap is
ambiguous (genuine divergence vs simply unrelated genes). Query the divergence
carriers directly:

- **`Finding.finding_type`** ∈ `cross_perturbation_contrast`,
  `pathway_uncoupling`, `cell_type_selectivity`, `negative_result`,
  `buffered_response` — the primary divergence carriers.
- **`Finding.direction`** prose labels: `uncoupled`, `uncorrelated`,
  `divergent`, `no_convergence`, `mixed_nominal`.
- **Comparator identity** is on `(:Finding)-[:REPORTS_GENE {role:'finding_reported_comparator'}]->(:Gene)`
  (identity only — no `effect_status` on this edge). The contrast *result* now
  lives in `Finding.finding_type`/`direction`, in the comparators' own
  `MEASURED_GENE` status, and in the report prose.

Divergence is only meaningful **relative to a prior group** — a paralog family
(shared symbol stem, e.g. `Grin2*`, `Gabra*`, `Atp6v*`) or shared
`Complex`/`Pathway` membership. "They didn't converge" matters only if they were
expected to; define the group first.

Non-interchangeability — does a target phenocopy its expected neighbors, or
stand apart?

```cypher
MATCH (t:TargetGene {symbol:$symbol})-[:HAS_FINDING]->(f:Finding)
WHERE f.finding_type IN ['cross_perturbation_contrast','pathway_uncoupling','cell_type_selectivity']
OPTIONAL MATCH (f)-[r:REPORTS_GENE {role:'finding_reported_comparator'}]->(e:Gene)
RETURN f.finding_type, f.direction, f.summary,
       collect(DISTINCT e.name) AS comparators
```

Family / complex heterogeneity = specificity — do members behave alike? (concept
lane via `IMPLICATES`; swap in the gene lane below for downstream-gene spread):

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[r:IMPLICATES]->(e)
WHERE t.symbol IN $family AND r.effect_status IN ['affected','implicated','buffered']
RETURN t.symbol, count(DISTINCT e) AS positive_concepts, collect(DISTINCT e.name)[..10] AS examples
ORDER BY positive_concepts DESC
```
`--param family='["Atp6v0c","Atp6v1b2","Atp6v1a","Atp6v1e1","Atp6v0a1"]'` — a
wide spread (some members rich, others ~0 or buffered) is subunit/paralog
**specificity**, not a shared complex phenotype.

**Directional antagonism** (X↑gene G, Y↓gene G on a *shared* gene) — **the graph
cannot answer this.** `MEASURED_GENE.direction`/`logfc`/`fdr` are contaminated by
cross-perturbation comparator quotes (~78% of pairs carry a foreign sign), so
opposite-sign edges in the graph are **not** evidence of real antagonism. Use the
graph only to enumerate **which genes are co-measured across the targets of interest**:

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[:SUPPORTED_BY]->(:Evidence)-[m:MEASURED_GENE]->(g:Gene)
WHERE t.symbol IN $targets AND m.effect_status IN ['affected','nominal']
WITH g.name AS gene, collect(DISTINCT t.symbol) AS targets
WHERE size(targets) >= 2
RETURN gene, targets ORDER BY size(targets) DESC LIMIT 50
```
Then determine the **actual per-target, per-cell-type sign** of each candidate gene
from the **DE parquet** (ground truth) — never from `m.direction` — and read the
reports for the narrative interpretation.

## Worked Patterns (adapt, don't copy verbatim)

Program convergence (canonical, de-fragmented) + abstraction-lift:

```cypher
// curated: how many targets' findings flag each program (positive)
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[r:IMPLICATES_PROGRAM]->(p:Program)
WHERE r.effect_status IN ['affected','implicated','buffered']
RETURN p.program_id, p.kind, count(DISTINCT t) AS targets ORDER BY targets DESC
// abstraction-lift: targets whose findings report >=3 member genes of a program (named or not)
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[:REPORTS_GENE]->(g:Gene)-[:MEMBER_OF]->(p:Program {program_id:$prog})
WITH t, count(DISTINCT g) AS members WHERE members>=3 RETURN t.symbol, members ORDER BY members DESC
```
Prefer `Program` over raw `Pathway`/`Complex`/`Module` concept nodes for the 10 seeded programs
(the raw concept layer is fragmented). For complete statistical convergence, use the parquet.

Dominant pathways/complexes/modules by positive target support (concept lane):

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[r:IMPLICATES]->(e)
WHERE any(l IN labels(e) WHERE l IN ['Pathway','Complex','Module'])
  AND r.effect_status IN ['affected','implicated','buffered']
RETURN [l IN labels(e) WHERE l IN ['Pathway','Complex','Module']][0] AS kind,
       e.name AS concept, count(DISTINCT t) AS support
ORDER BY support DESC LIMIT 20
```

Gene convergence across a target family — genes measured-affected in ≥N targets
(this is the corrected convergence; the old LLM gene lane inflated it with
cell-type-name tokens):

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[:SUPPORTED_BY]->(:Evidence)-[m:MEASURED_GENE]->(g:Gene)
WHERE t.symbol IN $targets AND m.effect_status IN ['affected','nominal']
WITH g.name AS gene, collect(DISTINCT t.symbol) AS shared
WHERE size(shared) >= 2
RETURN gene, shared, size(shared) AS n ORDER BY n DESC LIMIT 25
```
`--param targets='["Pomp","Psmb4","Psmc1","Psmc5"]'`. For *concept* convergence
across the family, run the same shape on `-[r:IMPLICATES]->(e)` with the concept
positive filter and `WHERE NOT r.effect_status IN ['absent_or_not_detected','fdr_insignificant']`.

Audit one **gene's** measured support broken down by status (precision check):

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[:SUPPORTED_BY]->(:Evidence)-[m:MEASURED_GENE]->(g:Gene {name:$name})
RETURN m.effect_status AS status, count(DISTINCT t) AS targets,
       collect(DISTINCT t.symbol)[..15] AS examples
ORDER BY targets DESC
// NB: MEASURED_GENE.direction/logfc/fdr are contaminated — for signs/magnitudes use the DE parquet.
```
For a **concept** node, audit on `-[r:IMPLICATES]->(e {name:$name})` returning
`r.effect_status`.

Target-specific evidence lookup:

```cypher
MATCH (t:TargetGene {symbol:$symbol})-[:HAS_FINDING]->(f:Finding)
OPTIONAL MATCH (f)-[:OBSERVED_IN]->(c:CellType)
RETURN f.finding_id, f.finding_type, f.direction, f.confidence,
       f.summary, collect(DISTINCT c.name) AS cell_types,
       f.evidence_ids, f.ref_ids, f.main_caveats
ORDER BY f.confidence DESC
```

Cell-type response landscape (status filter does NOT apply to OBSERVED_IN):

```cypher
MATCH (t:TargetGene)-[:HAS_FINDING]->(f:Finding)-[:OBSERVED_IN]->(c:CellType)
RETURN c.name AS cell_type, count(DISTINCT t) AS targets
ORDER BY targets DESC LIMIT 20
```
Add `WHERE f.direction = 'down' OR toLower(f.finding_type) CONTAINS 'deplet'`
for a depletion-direction landscape.

Disease/entity-axis entry: find `Other`/`Phenotype` nodes by name, then walk
back to targets and cell types. Use `toLower(e.name) CONTAINS toLower($term)` to
discover the exact node name first, then pivot.

## Query-Construction Guidance

- Always re-read `--schema` at the start; don't assume label/rel/prop names.
- Discover exact strings before filtering on them: cell-type and concept names
  are messy. `MATCH (n) WHERE toLower(n.name) CONTAINS '...' RETURN labels(n),
  n.name LIMIT 20` first, then use the exact string.
- Choose the `effect_status` filter consciously per query and report it.
- `count(DISTINCT t)` over distinct **targets** is the support metric, not edge
  count (one finding can yield several edges to the same concept).
- Conceptual nodes are deduped but imperfect (see DEDUP_NOTES): the same concept
  can persist under a different label (`proteasome` as `Complex` AND `Other`),
  and long-tail synonyms are unmerged. For a high-stakes concept, search by name
  fragment across labels and union the support rather than trusting one node.
- Keep result sets small with `LIMIT`; aggregate in Cypher (`count`, `collect`)
  rather than dumping thousands of rows into the agent context.
- Use `--format json` when you need to post-process; `table` for inspection.

## Quality Checks Before Trusting Results

- Did you set `effect_status` deliberately? An unfiltered "convergence" list is
  dominated by null edges (the Hedgehog artifact).
- Is a hub inflating the count? `CellType` hubs (`155 MB Glut`) and generic
  concepts (`broad transcriptomic response`, `target engagement`) are central by
  construction; route through `Finding` + evidence + direction, don't read a hub
  count as convergence.
- Could fragmentation be hiding support? If a known concept ranks low, search its
  synonyms/labels and sum.
- For any reported finding, trace it through `finding_id`,
  `Finding.main_caveats`, `Evidence.text`, and `Reference.citation`.
  Negative/buffered findings are real biology, not extraction failures —
  preserve them.

## Offline / Fallback Path

If Neo4j is unavailable, `scripts/query_biokg.py` answers the four canonical
shapes (`dominant`, `convergence --targets`, `support --name`, `celltypes
[--depletion]`) directly from the packaged CSVs (`src/distributed_agents/corpus/releases/shi/projections/biokg/data/base/`), stdlib-only,
with the same `--status-mode {all,positive,non-negative}` knob:

```bash
python src/distributed_agents/corpus/releases/shi/skills/biokg-recall-skill/scripts/query_biokg.py dominant --status-mode positive
python .../query_biokg.py convergence --targets Pomp Psmb4 Psmc1 Psmc5
```

Prefer live Cypher for flexible/novel endpoints; the CSV tool only covers the
four fixed shapes.

## Interpretation Rules

- The graph counts, filters, and indexes; it does not decide the answer.
  Synthesis, ranking rationale, and limitations belong to the fresh global
  reviewer comparing the quantitative starting result with Claim/Finding
  context cards.
- Low convergence is a *result*, not a dead end. Distinguish a contrast finding
  (real divergence — report its `finding_type` + `REPORTS_GENE` comparators) from
  mere absence of data. See "Divergence Is Encoded, Not Absent". **Per-gene sign is
  NOT reliable in the graph** (`MEASURED_GENE.direction`/`logfc`/`fdr` are contaminated
  by comparator quotes) — take signs and magnitudes from the DE parquet and report prose.
- State the `effect_status` mode behind every count you report.
- Cite `finding_id`, `evidence_ids`, `ref_ids`, and cell types from the graph.
  Open report prose only when the validated report budget and unresolved
  question require it.
- When the endpoint is not a measured graph edge, say so. Use the graph only as
  bounded relational attention around the declared basis, preserving
  buffered/negative/absent findings as qualifiers rather than exclusions.
