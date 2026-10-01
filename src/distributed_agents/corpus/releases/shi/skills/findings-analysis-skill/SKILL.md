---
name: findings-analysis-skill
description: Operate on the complete Shi narrative-findings ledger as a database. Use deterministic code to filter, score, rank, aggregate, cross-tab, or enumerate all 11,343 findings; apply semantic consequence scoring for biological-interest tasks and metadata rubrics for structured analysis. Use the findings-ledger skill when a task instead needs targeted prose retrieval and full-report reading.
---

## findings-analysis-skill

The findings ledger (11,343 atomic findings over 2,046 perturbed targets, with
structured metadata) is a **database first, a retrieval corpus second.** This skill
is the **analytical / database mode**: when the task is quantitative or must be
*complete*, you **author one deterministic operation over all the rows** (a filter, a
count, a cross-tab, an aggregate, a rubric score) and let code enumerate the table.
The agent authors the operation; the code emits the rows. That is the whole point —
it **sidesteps the single-pass emission ceiling by construction**, whereas asking a
generation pass to read + curate the interesting findings satisfices and collapses to
~10–15 long before 11,343 rows.

**Pick the right mode (this is mode selection, not "RAG").**
- **Analytical / this skill** — anything reducible or quantitative: *rank/score all*,
  *count*, *cross-tab*, *how many targets converge on X*, *per-cell-type burden*,
  *enumerate every finding matching a predicate*. Shape the deliverable as a
  **table/enumeration**, not a curated prose report — otherwise the emission ceiling
  reapplies at the output stage regardless of how you computed it.
- **Retrieval** (`findings-ledger-skill`) — targeted "what does the corpus say
  about gene/pathway X." This is right for a bounded answer and wrong for
  exhaustive enumeration.
- **Read the reports** (`findings-ledger-skill/scripts/read_reports.py`) — for the
  irreducibly-semantic call the metadata can't make (see BOUNDARIES).

This skill is the **sibling** of `findings-ledger-skill`. That one narrows the ledger
to a handful and reads report prose; this one operates over the whole table.

---

## (a) Metadata deep-doc — what each field is, and what it's good/bad for

Canonical packaged ledger:
`../../artifacts/ledgers/findings.csv`
(~8 MB, **11,343 findings**, **2,046 distinct targets**). Override with
`--ledger-path` / `DISTRIBUTED_AGENTS_FINDINGS_LEDGER`.

| field | where | good for | gotchas |
|---|---|---|---|
| `gene_target` | top-level | the atomic analysis unit; findings-per-gene; convergence | one target ≈ one perturbation; 2,046 of them |
| `finding_id` | top-level | key within a gene (`F003`) | only unique **within** a gene |
| `doc_id` | top-level | globally unique `gene:finding_id` | — |
| `summary`, `why_it_matters` | columns | finding prose; grep/read it | not structured categories |
| `source.finding_type` | struct | **primary structured axis** — a closed 12-value vocab (counts below) | this is the *only* fully-clean categorical; use it as the spine of cross-tabs |
| `source.literature_status` | struct | **the novelty signal** | **~847 distinct free-text values** — only the head is structured (below); don't `GROUP BY` it raw expecting clean bins, bucket the tail first |
| `source.cell_types` (list) | struct | per-cell-type burden; scope | **empty/null = GLOBAL scope (39.4%, 4,473 findings)** — do NOT cell-type-filter these away; a gene-level warning with empty `cell_types` is dropped by a cell-type-only filter |
| `source.confidence` | struct | quality weight (4 values below) | qualitative label, not a p-value |
| `source.direction` | struct | mostly free-text (~7,752 distinct values) | **low value for filtering/grouping** — treat as prose, grep it, don't `GROUP BY` |
| `source.genes` (list) | struct | downstream/readout symbols; gene-convergence | often contains the target itself; a gene symbol embedded in a cell-type LABEL (cell-type names can contain marker-gene symbols) is **not** a readout gene |
| `source.comparators` (list) | struct | the other perturbations a contrast is against | drives cross-perturbation stories |
| `source.evidence_ids` / `source.ref_ids` (lists) | struct | join keys into the evidence/reference ledgers (DE stats / citations) | **GENE-SCOPED**: `E001` for one gene ≠ `E001` for another — always join on `(gene_target, id)` |
| `source.main_caveats`, `source.source_summary`, `source.source_why_it_matters` | struct | the hedged judgment prose | semantic; count/grep but the "so what" call needs reading |

**`finding_type` (closed, 12 values, counts):**
`negative_result` 2043 · `cross_perturbation_contrast` 1650 · `cell_type_selectivity` 1501 ·
`buffered_response` 1392 · `pathway_uncoupling` 1371 · `therapeutic_direction_warning` 1188 ·
`disease_mechanism_refinement` 955 · `biomarker_candidate` 616 · `convergent_module` 374 ·
`homeostatic_compensation` 139 · `other` 65 · `literature_direction_mismatch` 49.

**`literature_status` (847 distinct; structured head + long free-text tail):**
`refines_cell_type_context` 2995 · `extends_known_mechanism` 2131 · `novel_no_direct_literature` 2125 ·
`supports_known_mechanism` 632 · *(null)* 579 · `literature_ambiguous` 533 ·
`disease_mechanism_refinement` 312 · `contradicts_expected_relationship` 244 ·
`refines_expected_relationship` 179 · … then a long tail of `contradicts_*` / `opposes_*` /
`refines_*` / `dataset_only_*` variants. The novelty signal you want (`contradicts_*`,
`opposes_*`, `novel_*`) is real but spread across the tail — bucket by substring
(`contains 'contradict'`, `'oppos'`, `'novel'`, `'refines'`, `'supports'`), don't rely on
exact values past the head.

**`confidence`:** `moderate` 5568 · `high` 4073 · `exploratory` 1465 · `low` 237.

**Interpretation gotchas that change the aggregate (read before counting):**
- **On-target silence ≠ no engagement.** A `negative_result` where the target's own
  transcript didn't move is *not* evidence the perturbation did nothing — self is a DEG in
  only ~5% of comparisons yet trends down; self-drop magnitude is uncorrelated with
  downstream response. Don't count `negative_result` as "nothing happened." (See
  `selfko-vs-downstream` in the analysis history.)
- **Low-power cell-type confound.** Some cell types are power-limited (few perturbed cells);
  per-cell-type burden counts there conflate biology with detection power. Identify them from
  the cell counts, don't rank on raw burden.
- **Empty `cell_types` is a scope, not a missing value** — see the table.

---

## (b) Operations cookbook

The ledger is small — **slurp it** with pandas or DuckDB. The **reports** file
(`../../artifacts/reports/reports.jsonl`,
~60 MB, 2,046 reports) — **stream it**, don't slurp. The raw **DE parquet** (~10 GB) —
**DuckDB only, never pandas** (a full slurp spikes RAM ~60 GB and can restart the shared
node; see `distributed_agents-ram-parquet`).

Load:
```python
import pandas as pd
df = pd.read_csv("../../artifacts/ledgers/findings.csv")
df = df.rename(columns={"target_gene": "gene_target"})
```
Or DuckDB:
```sql
SELECT finding_type, count(*) n
FROM read_csv_auto('../../artifacts/ledgers/findings.csv')
GROUP BY 1 ORDER BY n DESC;
```

**Count / cross-tab** (the operation the ledger is built for):
```python
df.finding_type.value_counts()                                   # composition
pd.crosstab(df.finding_type, df.literature_status.fillna("null").str.extract(
    r"(contradict|oppos|novel|refines|supports|ambiguous)", expand=False).fillna("other"))
```
`findings-ledger-skill/scripts/query_findings.py --count <field>` does the same one-field
counts from the shell without loading a dataframe.

**Aggregate:**
```python
df.groupby("gene_target").size().sort_values(ascending=False)   # findings per gene
df.explode("cell_types").groupby("cell_types").size()           # per-cell-type burden
# distinct-targets-per-program (convergence): how many targets touch a downstream gene
df.explode("genes").groupby("genes")["gene_target"].nunique().sort_values(ascending=False)
```

**Join to the evidence / reference ledgers** (packaged, gene-scoped IDs, share the
findings' ID space) at `../../artifacts/ledgers/`:
- `evidence.csv` — `(target_gene, evidence_id)` → `cell_type, genes, statistics` (the actual DE numbers), `description`.
- `references.csv` — `(target_gene, ref_id)` → `source, source_type, citation, url, description`.
- `findings.csv` — flat CSV mirror of the findings (pipe-delimited `evidence_ids`/`ref_ids`).
```python
ev = pd.read_csv("../../artifacts/ledgers/evidence.csv")
# resolve a finding's evidence -> DE statistics; ALWAYS join on both keys (IDs are gene-scoped)
merged = fdf.merge(ev, left_on=["gene_target","evidence_id"], right_on=["target_gene","evidence_id"])
```
For a single finding's citations/DE, `findings-ledger-skill/scripts/resolve_evidence.py`
is the ready-made resolver.

**Citation grounding:** resolve PMIDs/DOIs from `references.csv` — never emit a
recalled identifier; mark unverifiable ones as unverified priors.

---

## (c) Scoring recipes — two modes

Two ways to score/rank every finding. **Pick by the axis the task ranks on.**

### (c1) SEMANTIC "so what" ranking — `scripts/grade_findings.py` (use for interest/novelty)

The right default when the task wants the most INTERESTING / NOVEL / high-impact findings.
It applies a general ranking CRITERION (`scripts/rung_criterion.md`) to EACH finding with an
LLM, grading the readout genes by functional consequence — does the cell gain/lose/aberrantly
run a **capability or identity** (effector genes: channels, receptors, transporters, synaptic
machinery, fate TFs), or run an **ectopic** out-of-lineage program — over topology and
disease-fame. Ranks by `interest`.

```bash
# rank the whole ledger by biological "so what" (one LLM call per finding); needs OPENAI_API_KEY
python scripts/grade_findings.py --out-dir ./rung_ranking --top 30
python scripts/grade_findings.py --finding-type convergent_module --limit 200 --out-dir /tmp/r
```

Use this instead of the metadata rubric when the requested axis depends on what
the readout genes let the cell do; that discriminator is not represented by
structured finding fields alone. The criterion is general and supplies no
preferred genes. Output `ranked_by_rung.csv` (rank, interest, rung, capability,
carrying_genes, …) as a table; do not hand it to a prose summarizer.

### (c2) METADATA rubric — `scripts/score_findings.py` (use for structured aggregation)

Fast, stdlib-only, covers all rows; good for structured cross-tabs and as a cheap prefilter,
but ~random for the "so what" axis (use c1 for interest). Rank every finding on an editable
metadata rubric in one pass.

```bash
# score the whole ledger; write ranked_findings.csv + novelty_distribution.csv + methods.md
python scripts/score_findings.py --out-dir ./findings_analysis --top 25
# iterate on the rubric against a slice (filters mirror query_findings.py)
python scripts/score_findings.py --finding-type convergent_module --out-dir /tmp/fa --top 30
```

Every finding gets five 0–5 components combined by `WEIGHTS`, clamped to [0,5]:
- **novelty** — anchored on `literature_status` (structured head matched exactly, long
  tail by substring heuristic) + finding-type novelty + unexpected cross-domain theme
  combos − known/fidelity-module recovery − caveats.
- **impact** — `finding_type` base impact + breadth (cell types/genes/comparators) +
  confidence − caveats.
- **convergence** — **data-driven**: log-scaled count of DISTINCT *other* targets sharing
  the finding's dominant theme or a downstream gene (isolated note → low; program
  recurring across many targets → high). Computed over the whole corpus, then applied per
  row. Output columns `convergence_support` / `convergence_driver` show the count and what
  drove it.
- **confidence** — report confidence label → numeric.
- **evidence** — evidence/reference IDs, cell-type specificity, comparators, direction − caveats.
- `caveat_severity` (subtracted) — negative/null, no-FDR/weak engagement, target-only,
  low confidence, technical/power, known fidelity module.

**Everything tunable is a constant block at the top of the file** (`WEIGHTS`,
`FINDING_TYPE_IMPACT`, `LITERATURE_NOVELTY` + heuristic tail, `THEME_REGEXES`,
`UNEXPECTED_COMBOS`, `KNOWN_FIDELITY_MODULES`, caveat weights). The intended workflow is
**run → read the top → edit the rubric → re-run → diff the ranking.** It ships as a
starting point, not a fixed model. Output is a table you then sort/threshold/cross-tab —
do **not** hand the whole ranking to a prose summarizer (emission ceiling).

Convergence is computed from the data rather than from a hand-curated family
list. Deduplicating Findings into broader hypotheses remains out of scope.

---

## (d) Boundaries — what this mode cannot do

- **Metadata is a lossy proxy for the payoff.** It **cannot separate a rung-0 "recovered a
  known module" from a rung-2 "so what"** *within* a `finding_type`. A high `impact`/`novelty`
  score means "worth reading," never "confirmed interesting" — the ~90% of the corpus that
  is low-payoff and the ~2.5–3.8% that is genuinely rung-2/3 are **not separable by any
  field**; that call is semantic and requires reading the report prose
  (`findings-ledger-skill/scripts/read_reports.py`). Use scores to *triage into a read*,
  not to replace it. (See `sowhat-rung-bar-reproducibility`.)
- **The irreducibly-semantic classes have no predicate.** literature-contradiction /
  surprising-function-vs-annotation / therapeutic-warning-with-teeth cannot be recalled by
  a filter; exhaustive extraction of these = a full per-target read pass (built offline as
  the corpus). Don't claim a rubric filter is exhaustive for them.
- **Dedup / collapse-into-convergent-stories is out of scope.** Grouping many findings into
  one de-duplicated hypothesis is a separate concern (the worked example did it with
  curated families; not carried here).
- This ranks the **report claims and their caveats**, not the raw DE matrix. Top-ranked
  candidates still need verification against DE rows / figure scripts before final use.
